"""Typed, fail-closed structural analysis for BGN/PCGN Khmer romanization.

This module records orthographic components in a caller-supplied chunk. It
intentionally does not segment phonetic syllables, choose a PCGN series,
infer codas, recover omitted marks, or emit romanization/IPA/Ukrainian text.
"""
from __future__ import annotations

import unicodedata
from dataclasses import asdict, dataclass
from typing import Literal

from .data import CONSONANTS, SIGNS
from .normalize import normalize_khmer

PCGN_GUIDE = (
    "https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/"
    "ROMANIZATION_OF_KHMER.pdf"
)
COENG = "្"
SPECIAL_MARKS = {
    "៉": "MUUSIKATOAN",
    "៊": "TRIISAP",
    "់": "BANTOC",
    "័": "SAMYOK_SANNYA",
    "៌": "ROBAT",
    "៏": "AHSDA",
    "៍": "TOANDAKHIAT",
}
CONSONANTS_BY_CHAR = {item["char"]: item for item in CONSONANTS}
SIGNS_BY_CHAR = {item["char"]: item for item in SIGNS}
# PCGN Note 3 defines the weak set explicitly; do not add UNGEGN-only members.
PCGN_WEAK_SUBSCRIPTS = frozenset("ងញណនមយរលវ")
PCGN_NO_SUBSCRIPT_FOR = frozenset("ឡ")


@dataclass(frozen=True)
class PCGNToken:
    text: str
    kind: str
    codepoints: tuple[str, ...]
    name: str | None = None
    orthographic_register: str | None = None


@dataclass(frozen=True)
class PCGNOrthographicAnalysis:
    raw_text: str
    normalized_text: str
    tokens: tuple[PCGNToken, ...]
    base_consonants: tuple[str, ...]
    subscript_consonants: tuple[str, ...]
    register_shifters: tuple[str, ...]
    register_shifter_positions: tuple[int, ...]
    dependent_vowel_signs: tuple[str, ...]
    independent_vowels: tuple[str, ...]
    shortening_marks: tuple[str, ...]
    shortening_mark_positions: tuple[int, ...]
    robat_positions: tuple[int, ...]
    ahsda_positions: tuple[int, ...]
    toandakhiat_positions: tuple[int, ...]
    unresolved_components: tuple[str, ...]
    syllable_segmentation: Literal["NOT_PERFORMED"]
    series_decision: Literal["UNRESOLVED"]
    register_source: Literal["NOT_SELECTED"]
    coda_decision: Literal["UNRESOLVED"]
    romanization: None
    ipa: None
    ukrainian: None
    status: Literal["STRUCTURE_ONLY", "UNSUPPORTED"]
    warnings: tuple[str, ...]
    sources: tuple[str, ...]

    def to_dict(self) -> dict:
        """Return JSON-compatible data while preserving explicit null outputs."""
        return asdict(self)


def analyze_pcgn_orthographic_chunk(text: str) -> PCGNOrthographicAnalysis:
    """Classify orthographic tokens without claiming a syllable or reading.

    The caller must supply a chunk. This function does not decide where a
    phonetic syllable begins/ends; multiple unstacked consonants are retained.
    """
    normalized = normalize_khmer(text)
    chars = list(normalized)
    tokens: list[PCGNToken] = []
    bases: list[str] = []
    subscripts: list[str] = []
    shifters: list[str] = []
    shifter_positions: list[int] = []
    dependent_vowels: list[str] = []
    independent_vowels: list[str] = []
    shortening: list[str] = []
    shortening_positions: list[int] = []
    robat: list[int] = []
    ahsda: list[int] = []
    toandakhiat: list[int] = []
    unresolved: list[str] = []
    i = 0

    def token(
        value: str,
        kind: str,
        name: str | None = None,
        orthographic_register: str | None = None,
    ) -> None:
        tokens.append(
            PCGNToken(
                text=value,
                kind=kind,
                codepoints=tuple(f"U+{ord(ch):04X}" for ch in value),
                name=name,
                orthographic_register=orthographic_register,
            )
        )

    while i < len(chars):
        ch = chars[i]
        if ch == COENG:
            if i + 1 < len(chars) and chars[i + 1] in CONSONANTS_BY_CHAR:
                subscript = chars[i + 1]
                if subscript in PCGN_NO_SUBSCRIPT_FOR:
                    token(COENG + subscript, "unsupported_pcgn_subscript", CONSONANTS_BY_CHAR[subscript]["name"])
                    unresolved.extend((COENG, subscript))
                    i += 2
                    continue
                subscripts.append(subscript)
                token(
                    COENG + subscript,
                    "subscript_consonant",
                    CONSONANTS_BY_CHAR[subscript]["name"],
                    CONSONANTS_BY_CHAR[subscript].get("register"),
                )
                i += 2
                continue
            token(ch, "malformed_coeng", "COENG")
            unresolved.append(ch)
            i += 1
            continue

        consonant = CONSONANTS_BY_CHAR.get(ch)
        if consonant:
            bases.append(ch)
            token(ch, "unstacked_consonant", consonant["name"], consonant.get("register"))
            i += 1
            continue

        sign = SIGNS_BY_CHAR.get(ch)
        if sign:
            name = SPECIAL_MARKS.get(ch, sign.get("name"))
            if sign.get("kind") == "unmodeled_letter":
                token(ch, "unmodeled_letter", name)
                unresolved.append(ch)
                i += 1
                continue
            if ch in {"៉", "៊"}:
                shifters.append(ch)
                shifter_positions.append(i)
                token(ch, "register_shifter", name)
            elif ch in {"់", "័"}:
                shortening.append(ch)
                shortening_positions.append(i)
                token(ch, "shortening_mark", name)
            elif ch == "៌":
                robat.append(i)
                token(ch, "robat", name)
            elif ch == "៏":
                ahsda.append(i)
                token(ch, "ahsda_position_sensitive", name)
            elif ch == "៍":
                toandakhiat.append(i)
                token(ch, "toandakhiat_silent_mark", name)
            elif sign.get("kind") == "dependent_vowel":
                dependent_vowels.append(ch)
                token(ch, "dependent_vowel", name)
            elif sign.get("kind") == "independent_vowel":
                independent_vowels.append(ch)
                token(ch, "independent_vowel", name)
            else:
                token(ch, sign.get("kind", "sign"), name)
            i += 1
            continue

        if ch.isspace() or unicodedata.category(ch).startswith("P"):
            token(ch, "separator")
            i += 1
            continue

        token(ch, "unresolved_component", unicodedata.name(ch, "UNKNOWN"))
        unresolved.append(ch)
        i += 1

    warnings = [
        "ORTHOGRAPHIC_CHUNK_BOUNDARIES_ARE_CALLER_SUPPLIED",
        "PHONETIC_SYLLABLE_SEGMENTATION_NOT_PERFORMED",
        "PCGN_SERIES_SELECTION_NOT_PERFORMED",
        "CODA_AND_SYLLABLE_POSITION_NOT_INFERRED",
        "NO_ROMANIZATION_IPA_OR_UKRAINIAN_OUTPUT",
        "OMITTED_DIACRITICS_CANNOT_BE_RECOVERED_FROM_THIS_ANALYSIS",
    ]
    if len(bases) > 1:
        warnings.append("MULTIPLE_UNSTACKED_CONSONANTS_RETAINED_WITHOUT_SYLLABLE_ASSIGNMENT")
    if shifters:
        warnings.append("REGISTER_SHIFTER_EFFECT_REQUIRES_PCGN_NOTE_2_CONTEXT")
    if shortening:
        warnings.append("SHORTENING_REQUIRES_PCGN_NOTE_5_PATTERN_SERIES_AND_CODA")
    if robat:
        warnings.append("ROBAT_REQUIRES_FOLLOWING_ROMANIZED_CONSONANT")
    if ahsda:
        warnings.append("AHSDA_BEHAVIOR_REQUIRES_SYLLABLE_POSITION_AND_SERIES")
    if toandakhiat:
        warnings.append("TOANDAKHIAT_MARKED_CHARACTER_MUST_BE_IDENTIFIED_BEFORE_OMISSION")

    return PCGNOrthographicAnalysis(
        raw_text=text,
        normalized_text=normalized,
        tokens=tuple(tokens),
        base_consonants=tuple(bases),
        subscript_consonants=tuple(subscripts),
        register_shifters=tuple(shifters),
        register_shifter_positions=tuple(shifter_positions),
        dependent_vowel_signs=tuple(dependent_vowels),
        independent_vowels=tuple(independent_vowels),
        shortening_marks=tuple(shortening),
        shortening_mark_positions=tuple(shortening_positions),
        robat_positions=tuple(robat),
        ahsda_positions=tuple(ahsda),
        toandakhiat_positions=tuple(toandakhiat),
        unresolved_components=tuple(unresolved),
        syllable_segmentation="NOT_PERFORMED",
        series_decision="UNRESOLVED",
        register_source="NOT_SELECTED",
        coda_decision="UNRESOLVED",
        romanization=None,
        ipa=None,
        ukrainian=None,
        status="UNSUPPORTED" if unresolved or not any(ch in CONSONANTS_BY_CHAR or ch in SIGNS_BY_CHAR for ch in chars) else "STRUCTURE_ONLY",
        warnings=tuple(warnings),
        sources=("unicode17-ch16", "pcgn-1972-notes-2-8", PCGN_GUIDE),
    )



@dataclass(frozen=True)
class PCGNSeriesDecision:
    series: Literal["â", "ô"] | None
    basis: Literal["BASE", "SUBSCRIPT", "UNRESOLVED"]
    status: Literal["RESOLVED", "UNRESOLVED"]
    onset_exception: Literal["BA_WITH_FOOT_P_IN_A_SERIES", "BA_WITH_MUUSIKATOAN_P_IN_A_SERIES", "BA_WITH_TRIISAP_P_IN_A_SERIES"] | None
    series_before_shifter: Literal["â", "ô"] | None
    shifter_effect: Literal["TRIISAP_A_TO_O", "MUUSIKATOAN_O_TO_A", "BA_MUUSIKATOAN_P_IN_A", "BA_TRIISAP_P_IN_A"] | None
    source_locator: str
    warnings: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def resolve_pcgn_series(
    analysis: PCGNOrthographicAnalysis,
) -> PCGNSeriesDecision:
    """Apply bounded BGN/PCGN Notes 2–3 series selection.

    Note 3 chooses the base/foot source. Note 2 shifters are applied to one base or one base-plus-foot cluster when
    the single mark is encoded immediately after the base, as required by
    Unicode Khmer syllabic order. The explicit Note 3 BA+TRIISAP exception
    is represented separately; shifters on BA+foot, multiple marks and
    wrong-way shifters abstain pending narrower adjudication.
    """
    def unresolved(reason: str) -> PCGNSeriesDecision:
        return PCGNSeriesDecision(
            series=None,
            basis="UNRESOLVED",
            status="UNRESOLVED",
            onset_exception=None,
            series_before_shifter=None,
            shifter_effect=None,
            source_locator="PCGN 1972, Notes 2–3 (pp. 2–3)",
            warnings=(reason, "NO_VOWEL_OR_ROMANIZATION_OUTPUT"),
        )

    if analysis.status != "STRUCTURE_ONLY":
        return unresolved("UNSUPPORTED_OR_UNRESOLVED_ORTHOGRAPHIC_COMPONENT")
    if len(analysis.base_consonants) != 1:
        return unresolved("EXACTLY_ONE_BASE_CONSONANT_REQUIRED")
    if len(analysis.subscript_consonants) > 1:
        return unresolved("MULTIPLE_SUBSCRIPTS_REQUIRE_READING_ADJUDICATION")

    base = analysis.base_consonants[0]
    base_register = CONSONANTS_BY_CHAR[base].get("register")
    if base_register not in {"first", "second"}:
        return unresolved("BASE_ORTHOGRAPHIC_REGISTER_UNAVAILABLE")

    if analysis.register_shifters:
        if len(analysis.register_shifters) != 1:
            return unresolved("MULTIPLE_REGISTER_SHIFTERS_REQUIRE_REVIEW")
        if analysis.register_shifter_positions != (1,):
            return unresolved("REGISTER_SHIFTER_NOT_IMMEDIATELY_AFTER_BASE")

        mark = analysis.register_shifters[0]
        # Note 1 defines the affected unit as either a consonant or a
        # consonant-plus-foot cluster. Unicode fixes the encoded order:
        # base, register shifter, then COENG+subscript.
        if base == "ប":
            if analysis.subscript_consonants:
                return unresolved("BA_WITH_FOOT_AND_REGISTER_SHIFTER_REQUIRES_ADJUDICATION")
            if mark == "៉":
                return PCGNSeriesDecision(
                    series="â",
                    basis="BASE",
                    status="RESOLVED",
                    onset_exception="BA_WITH_MUUSIKATOAN_P_IN_A_SERIES",
                    series_before_shifter="â",
                    shifter_effect="BA_MUUSIKATOAN_P_IN_A",
                    source_locator="PCGN 1972, Notes 2–3 (pp. 2–3)",
                    warnings=(
                        "PCGN_NOTE_3_BA_MUUSIKATOAN_P_IN_A_EXCEPTION",
                        "SERIES_METADATA_ONLY_NO_VOWEL_OR_ROMANIZATION",
                    ),
                )
            if mark == "៊":
                return PCGNSeriesDecision(
                    series="â",
                    basis="BASE",
                    status="RESOLVED",
                    onset_exception="BA_WITH_TRIISAP_P_IN_A_SERIES",
                    series_before_shifter="ô",
                    shifter_effect="BA_TRIISAP_P_IN_A",
                    source_locator="PCGN 1972, Notes 2–3 (pp. 2–3)",
                    warnings=(
                        "PCGN_NOTE_3_BA_TRIISAP_P_IN_A_EXCEPTION",
                        "PCGN_NOTE_2_TRIISAP_MARK_RECORDED_WITH_NOTE_3_BA_EXCEPTION",
                        "SERIES_METADATA_ONLY_NO_VOWEL_OR_ROMANIZATION",
                    ),
                )
            return unresolved("UNSUPPORTED_BA_REGISTER_SHIFTER_CONTEXT")

        # Determine the unshifted series of the whole graphic cluster using
        # Note 3 before applying the Note 2 mark.
        if not analysis.subscript_consonants:
            register = base_register
            basis: Literal["BASE", "SUBSCRIPT", "UNRESOLVED"] = "BASE"
        else:
            foot = analysis.subscript_consonants[0]
            foot_register = CONSONANTS_BY_CHAR[foot].get("register")
            if foot_register not in {"first", "second"}:
                return unresolved("SUBSCRIPT_ORTHOGRAPHIC_REGISTER_UNAVAILABLE")
            if foot in PCGN_WEAK_SUBSCRIPTS and base not in PCGN_WEAK_SUBSCRIPTS:
                register = base_register
                basis = "BASE"
            else:
                register = foot_register
                basis = "SUBSCRIPT"

        original: Literal["â", "ô"] = "â" if register == "first" else "ô"
        if mark == "៊" and original == "â":
            series: Literal["â", "ô"] = "ô"
            effect: Literal["TRIISAP_A_TO_O", "MUUSIKATOAN_O_TO_A", "BA_MUUSIKATOAN_P_IN_A"] = "TRIISAP_A_TO_O"
            warning = "PCGN_NOTE_2_TRIISAP_A_TO_O"
        elif mark == "៉" and original == "ô":
            series = "â"
            effect = "MUUSIKATOAN_O_TO_A"
            warning = "PCGN_NOTE_2_MUUSIKATOAN_O_TO_A"
        else:
            return unresolved("REGISTER_SHIFTER_DIRECTION_DOES_NOT_MATCH_CLUSTER_SERIES")

        return PCGNSeriesDecision(
            series=series,
            basis=basis,
            status="RESOLVED",
            onset_exception=None,
            series_before_shifter=original,
            shifter_effect=effect,
            source_locator="PCGN 1972, Notes 2–3 (pp. 2–3)",
            warnings=(
                warning,
                "PCGN_NOTE_2_APPLIED_TO_BASE_PLUS_FOOT_CLUSTER" if analysis.subscript_consonants else "PCGN_NOTE_2_APPLIED_TO_SINGLE_BASE",
                "SERIES_METADATA_ONLY_NO_VOWEL_OR_ROMANIZATION",
            ),
        )

    if not analysis.subscript_consonants:
        register = base_register
        basis: Literal["BASE", "SUBSCRIPT", "UNRESOLVED"] = "BASE"
        exception = None
    else:
        foot = analysis.subscript_consonants[0]
        foot_register = CONSONANTS_BY_CHAR[foot].get("register")
        if foot_register not in {"first", "second"}:
            return unresolved("SUBSCRIPT_ORTHOGRAPHIC_REGISTER_UNAVAILABLE")
        if base == "ប":
            register = "first"
            basis = "BASE"
            exception = "BA_WITH_FOOT_P_IN_A_SERIES"
        elif foot in PCGN_WEAK_SUBSCRIPTS and base not in PCGN_WEAK_SUBSCRIPTS:
            register = base_register
            basis = "BASE"
            exception = None
        else:
            register = foot_register
            basis = "SUBSCRIPT"
            exception = None

    series = "â" if register == "first" else "ô"
    warnings = ["PCGN_NOTE_3_SERIES_SELECTION_ONLY"]
    if exception:
        warnings.append("PCGN_NOTE_3_BA_WITH_FOOT_P_EXCEPTION")
    return PCGNSeriesDecision(
        series=series,
        basis=basis,
        status="RESOLVED",
        onset_exception=exception,
        series_before_shifter=series,
        shifter_effect=None,
        source_locator="PCGN 1972, Note 3 (pp. 2–3)",
        warnings=tuple(warnings),
    )


PCGN_DEPENDENT_VOWEL_TABLE_LOCATOR = (
    "PCGN 1972, Independent/Dependent Vowel Characters table (pp. 2–3)"
)

# Normal (not shortened) dependent-vowel values from the official PCGN table.
# The two values are the â-series and ô-series columns respectively.
PCGN_DEPENDENT_VOWEL_ROWS: dict[tuple[str, ...], tuple[int, str, str]] = {
    ("ា",): (2, "a", "éa"),
    ("ិ",): (3, "ĕ", "ĕ"),
    ("ី",): (4, "ei", "i"),
    ("ឹ",): (5, "œ̆", "œ̆"),
    ("ឺ",): (6, "œ", "œ"),
    ("ុ",): (7, "ŏ", "ŭ"),
    ("ូ",): (8, "o", "u"),
    ("ួ",): (9, "uŏ", "uŏ"),
    ("េ", "ើ"): (10, "aeu", "eu"),
    ("េ", "ឿ"): (11, "œă", "œă"),
    ("េ", "ៀ"): (12, "iĕ", "iĕ"),
    ("េ",): (13, "é", "é"),
    ("ែ",): (14, "ê", "ê"),
    ("ៃ",): (15, "ai", "ey"),
    ("េ", "ា"): (16, "aô", "aô"),
    ("េ", "ៅ"): (17, "au", "au"),
}


@dataclass(frozen=True)
class PCGNVowelDecision:
    source_signs: tuple[str, ...] | None
    series: Literal["â", "ô"] | None
    romanization: str | None
    source_table_row: int | None
    status: Literal["RESOLVED", "UNRESOLVED"]
    ipa: None
    ukrainian: None
    source_locator: str
    warnings: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def resolve_pcgn_dependent_vowel(
    analysis: PCGNOrthographicAnalysis,
    series_decision: PCGNSeriesDecision,
) -> PCGNVowelDecision:
    """Map one ordinary dependent vowel sign to its PCGN Latin component.

    This is deliberately not a syllable romanizer. It accepts one base, at
    most one foot, one source-ordered dependent-vowel pattern (one or two
    signs), and an already-resolved Note 2/3 series. Shortening, codas,
    independent vowels and other marks abstain.
    """
    def unresolved(reason: str) -> PCGNVowelDecision:
        return PCGNVowelDecision(
            source_signs=None,
            series=None,
            romanization=None,
            source_table_row=None,
            status="UNRESOLVED",
            ipa=None,
            ukrainian=None,
            source_locator=PCGN_DEPENDENT_VOWEL_TABLE_LOCATOR,
            warnings=(reason, "NO_COMPLETE_SYLLABLE_OR_UKRAINIAN_OUTPUT"),
        )

    if analysis.status != "STRUCTURE_ONLY":
        return unresolved("UNSUPPORTED_OR_UNRESOLVED_ORTHOGRAPHIC_COMPONENT")
    if series_decision.status != "RESOLVED" or series_decision.series not in {"â", "ô"}:
        return unresolved("RESOLVED_PCGN_SERIES_REQUIRED")
    if len(analysis.base_consonants) != 1:
        return unresolved("EXACTLY_ONE_BASE_CONSONANT_REQUIRED")
    if len(analysis.subscript_consonants) > 1:
        return unresolved("MULTIPLE_SUBSCRIPTS_REQUIRE_READING_ADJUDICATION")
    if not 1 <= len(analysis.dependent_vowel_signs) <= 2:
        return unresolved("ONE_OR_TWO_DEPENDENT_VOWEL_SIGNS_REQUIRED")
    if analysis.independent_vowels:
        return unresolved("INDEPENDENT_VOWEL_NOT_SUPPORTED_BY_DEPENDENT_RESOLVER")
    if analysis.shortening_marks:
        return unresolved("SHORTENING_REQUIRES_PCGN_NOTE_5_CONTEXT")
    if analysis.robat_positions or analysis.ahsda_positions or analysis.toandakhiat_positions:
        return unresolved("SPECIAL_DIACRITIC_REQUIRES_POSITION_OR_CODA_CONTEXT")

    allowed_token_kinds = {
        "unstacked_consonant",
        "subscript_consonant",
        "register_shifter",
        "dependent_vowel",
    }
    if any(token.kind not in allowed_token_kinds for token in analysis.tokens):
        return unresolved("NON_VOWEL_COMPONENT_REQUIRES_CONTEXTUAL_ANALYSIS")

    signs = tuple(analysis.dependent_vowel_signs)
    row = PCGN_DEPENDENT_VOWEL_ROWS.get(signs)
    if row is None:
        return unresolved("DEPENDENT_VOWEL_NOT_IN_BOUNDED_NORMAL_TABLE_SUBSET")

    row_number, a_series_value, o_series_value = row
    value = a_series_value if series_decision.series == "â" else o_series_value
    return PCGNVowelDecision(
        source_signs=signs,
        series=series_decision.series,
        romanization=value,
        source_table_row=row_number,
        status="RESOLVED",
        ipa=None,
        ukrainian=None,
        source_locator=PCGN_DEPENDENT_VOWEL_TABLE_LOCATOR,
        warnings=(
            "NORMAL_DEPENDENT_VOWEL_COMPONENT_ONLY",
            "NO_ONSET_CODA_SYLLABLE_SEGMENTATION_IPA_OR_UKRAINIAN_OUTPUT",
        ),
    )


PCGN_INHERENT_VOWEL_TABLE_LOCATOR = (
    "PCGN 1972, Independent/Dependent Vowel Characters table row 1 (p. 2)"
)


@dataclass(frozen=True)
class PCGNInherentVowelDecision:
    syllable_position: Literal["NON_FINAL", "FINAL"]
    series: Literal["â", "ô"] | None
    romanization: str | None
    source_table_row: int
    status: Literal["RESOLVED", "UNRESOLVED"]
    ipa: None
    ukrainian: None
    source_locator: str
    warnings: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def resolve_pcgn_inherent_vowel(
    analysis: PCGNOrthographicAnalysis,
    syllable_position: Literal["NON_FINAL", "FINAL"],
) -> PCGNInherentVowelDecision:
    """Resolve the inherent-vowel component in PCGN table row 1.

    Only an explicitly identified non-final onset cluster is mapped to â/ô.
    A final consonant without a vowel character or TOANDAKHIAT is governed
    by the guide's separate general no-vowel-following statement; this
    component resolver abstains there rather than assuming a syllable edge.
    """
    def unresolved(reason: str) -> PCGNInherentVowelDecision:
        return PCGNInherentVowelDecision(
            syllable_position=syllable_position,
            series=None,
            romanization=None,
            source_table_row=1,
            status="UNRESOLVED",
            ipa=None,
            ukrainian=None,
            source_locator=PCGN_INHERENT_VOWEL_TABLE_LOCATOR,
            warnings=(reason, "NO_COMPLETE_SYLLABLE_IPA_OR_UKRAINIAN_OUTPUT"),
        )

    if syllable_position not in {"NON_FINAL", "FINAL"}:
        return unresolved("EXPLICIT_SYLLABLE_POSITION_REQUIRED")
    if syllable_position == "FINAL":
        return unresolved("FINAL_CONSONANT_NO_VOWEL_RULE_REQUIRES_SEPARATE_CODA_CONTEXT")
    if analysis.status != "STRUCTURE_ONLY":
        return unresolved("UNSUPPORTED_OR_UNRESOLVED_ORTHOGRAPHIC_COMPONENT")
    if (
        len(analysis.base_consonants) != 1
        or len(analysis.subscript_consonants) > 1
        or analysis.dependent_vowel_signs
        or analysis.independent_vowels
        or analysis.shortening_marks
        or analysis.robat_positions
        or analysis.ahsda_positions
        or analysis.toandakhiat_positions
        or any(
            token.kind not in {"unstacked_consonant", "subscript_consonant", "register_shifter"}
            for token in analysis.tokens
        )
    ):
        return unresolved("ONSET_ONLY_CLUSTER_WITH_ONE_BASE_AND_AT_MOST_ONE_FOOT_REQUIRED")

    series_decision = resolve_pcgn_series(analysis)
    if series_decision.status != "RESOLVED" or series_decision.series not in {"â", "ô"}:
        return unresolved("PCGN_NOTE_2_3_SERIES_MUST_BE_RESOLVED")

    return PCGNInherentVowelDecision(
        syllable_position="NON_FINAL",
        series=series_decision.series,
        romanization=series_decision.series,
        source_table_row=1,
        status="RESOLVED",
        ipa=None,
        ukrainian=None,
        source_locator=PCGN_INHERENT_VOWEL_TABLE_LOCATOR,
        warnings=(
            "PCGN_TABLE_ROW_1_INHERENT_VOWEL_COMPONENT_ONLY",
            "NON_FINAL_POSITION_EXPLICITLY_CALLER_SUPPLIED",
            "NO_FINAL_CODA_OR_SYLLABLE_SEGMENTATION_INFERRED",
            "NO_IPA_OR_UKRAINIAN_OUTPUT",
        ),
    )


PCGN_ANUSVARA_VISARGA_TABLE_LOCATOR = (
    "PCGN 1972, Vowel Characters with Anusvara or Visarga table (p. 4)"
)
# Exact post-onset Unicode token sequences from the official table. The final
# NGA in row 8 is an explicit coda and is never inferred from a word string.
PCGN_ANUSVARA_VISARGA_ROWS: dict[tuple[str, ...], tuple[int, str, str]] = {
    ("ុ", "ំ"): (1, "om", "ŭm"),
    ("ំ",): (2, "âm", "um"),
    ("ា", "ំ"): (3, "ăm", "ŏâm"),
    ("ះ",): (4, "ăh", "eăh"),
    ("ុ", "ះ"): (5, "ŏh", "ŭh"),
    ("េ", "ះ"): (6, "éh", "éh"),
    ("ោ", "ះ"): (7, "aôh", "ŏăh"),
    ("ា", "ំ", "ង"): (8, "ăng", "eăng"),
}


@dataclass(frozen=True)
class PCGNAnusvaraVisargaDecision:
    source_components: tuple[str, ...] | None
    series: Literal["â", "ô"] | None
    coda_character: str | None
    romanization: str | None
    source_table_row: int | None
    status: Literal["RESOLVED", "UNRESOLVED"]
    ipa: None
    ukrainian: None
    source_locator: str
    warnings: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def resolve_pcgn_anusvara_visarga(
    analysis: PCGNOrthographicAnalysis,
    onset_analysis: PCGNOrthographicAnalysis,
    coda_character: str | None = None,
) -> PCGNAnusvaraVisargaDecision:
    """Resolve one exact PCGN table row containing NIKAHIT or REAHMUK.

    The caller supplies an onset-only analysis. Row 8 additionally requires
    the exact final NGA coda to be caller-identified. This resolver does not
    infer a syllable boundary, coda, pronunciation or IPA; it returns only
    the vowel-plus-final-consonant romanization component from table rows 1–8.
    """
    def unresolved(reason: str) -> PCGNAnusvaraVisargaDecision:
        return PCGNAnusvaraVisargaDecision(
            source_components=None,
            series=None,
            coda_character=coda_character if coda_character == "ង" else None,
            romanization=None,
            source_table_row=None,
            status="UNRESOLVED",
            ipa=None,
            ukrainian=None,
            source_locator=PCGN_ANUSVARA_VISARGA_TABLE_LOCATOR,
            warnings=(reason, "NO_COMPLETE_SYLLABLE_IPA_OR_UKRAINIAN_OUTPUT"),
        )

    if analysis.status != "STRUCTURE_ONLY" or onset_analysis.status != "STRUCTURE_ONLY":
        return unresolved("UNSUPPORTED_OR_UNRESOLVED_ORTHOGRAPHIC_COMPONENT")
    if (
        len(onset_analysis.base_consonants) != 1
        or len(onset_analysis.subscript_consonants) > 1
        or onset_analysis.dependent_vowel_signs
        or onset_analysis.independent_vowels
        or onset_analysis.shortening_marks
        or onset_analysis.robat_positions
        or onset_analysis.ahsda_positions
        or onset_analysis.toandakhiat_positions
        or any(
            token.kind not in {"unstacked_consonant", "subscript_consonant", "register_shifter"}
            for token in onset_analysis.tokens
        )
    ):
        return unresolved("ONSET_ANALYSIS_MUST_CONTAIN_ONE_BASE_AND_AT_MOST_ONE_FOOT_ONLY")

    series_decision = resolve_pcgn_series(onset_analysis)
    if series_decision.status != "RESOLVED" or series_decision.series not in {"â", "ô"}:
        return unresolved("PCGN_NOTE_2_3_ONSET_SERIES_MUST_BE_RESOLVED")

    onset_tokens = tuple(onset_analysis.tokens)
    if tuple(analysis.tokens[:len(onset_tokens)]) != onset_tokens:
        return unresolved("ONSET_ANALYSIS_DOES_NOT_MATCH_FULL_CHUNK_PREFIX")
    if (
        analysis.subscript_consonants != onset_analysis.subscript_consonants
        or analysis.register_shifters != onset_analysis.register_shifters
        or analysis.independent_vowels
        or analysis.shortening_marks
        or analysis.robat_positions
        or analysis.ahsda_positions
        or analysis.toandakhiat_positions
    ):
        return unresolved("FULL_CHUNK_CONTAINS_UNSUPPORTED_OR_MISMATCHED_CONTEXT")

    components = tuple(token.text for token in analysis.tokens[len(onset_tokens):])
    row = PCGN_ANUSVARA_VISARGA_ROWS.get(components)
    if row is None:
        return unresolved("ANUSVARA_VISARGA_SEQUENCE_NOT_IN_PCGN_TABLE_ROWS_1_TO_8")

    row_number, a_series_value, o_series_value = row
    if row_number == 8:
        if coda_character != "ង":
            return unresolved("PCGN_ROW_8_REQUIRES_EXPLICIT_FINAL_NGA_CODA")
        if analysis.base_consonants != onset_analysis.base_consonants + ("ង",):
            return unresolved("PCGN_ROW_8_FINAL_NGA_DOES_NOT_MATCH_FULL_CHUNK")
    else:
        if coda_character is not None:
            return unresolved("CODA_ARGUMENT_NOT_ALLOWED_FOR_PCGN_ROWS_1_TO_7")
        if analysis.base_consonants != onset_analysis.base_consonants:
            return unresolved("UNLISTED_CODA_OR_MULTIPLE_BASE_CONSONANTS")

    allowed_kinds = {
        "dependent_vowel", "vowel_modifier", "sign", "unstacked_consonant"
    }
    if any(token.kind not in allowed_kinds for token in analysis.tokens[len(onset_tokens):]):
        return unresolved("NON_TABLE_TOKEN_IN_ANUSVARA_VISARGA_SEQUENCE")

    value = a_series_value if series_decision.series == "â" else o_series_value
    return PCGNAnusvaraVisargaDecision(
        source_components=components,
        series=series_decision.series,
        coda_character="ង" if row_number == 8 else None,
        romanization=value,
        source_table_row=row_number,
        status="RESOLVED",
        ipa=None,
        ukrainian=None,
        source_locator=PCGN_ANUSVARA_VISARGA_TABLE_LOCATOR,
        warnings=(
            "PCGN_TABLE_ANUSVARA_VISARGA_COMPONENT_ONLY",
            "ONSET_SERIES_RESOLVED_FROM_SEPARATE_ONSET_ANALYSIS",
            "ROW_8_NGA_CODA_EXPLICITLY_CALLER_IDENTIFIED" if row_number == 8 else "NO_CODA_INFERRED",
            "NO_SYLLABLE_SEGMENTATION_IPA_OR_UKRAINIAN_OUTPUT",
        ),
    )


PCGN_INDEPENDENT_VOWEL_TABLE_LOCATOR = (
    "PCGN 1972, Independent/Dependent Vowel Characters table (pp. 2–3), Notes §9"
)
PCGN_INDEPENDENT_VOWEL_ROWS: dict[str, tuple[int, str]] = {
    "ឥ": (3, "ĕ"),
    "ឦ": (4, "ei"),
    "ឯ": (14, "ê"),
    "ឰ": (15, "ai"),
    "ឱ": (16, "aô"),
    "ឲ": (16, "aô"),
    "ឳ": (17, "au"),
    "ឪ": (18, "âu"),
    "ឫ": (19, "rœ̆"),
    "ឬ": (20, "rœ"),
    "ឭ": (21, "lœ̆"),
    "ឮ": (22, "lœ"),
}


@dataclass(frozen=True)
class PCGNIndependentVowelDecision:
    source_character: str | None
    romanization: str | None
    romanization_options: tuple[str, ...]
    source_table_row: int | None
    status: Literal["RESOLVED", "UNRESOLVED"]
    ipa: None
    ukrainian: None
    source_locator: str
    warnings: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def resolve_pcgn_independent_vowel(
    analysis: PCGNOrthographicAnalysis,
) -> PCGNIndependentVowelDecision:
    """Map one listed independent vowel without assigning IPA or a series."""
    source_character = (
        analysis.independent_vowels[0]
        if len(analysis.independent_vowels) == 1
        else None
    )
    row = PCGN_INDEPENDENT_VOWEL_ROWS.get(source_character) if source_character else None
    table_row = row[0] if row else (7 if source_character == "ឧ" else None)

    def unresolved(
        reason: str,
        romanization_options: tuple[str, ...] = (),
    ) -> PCGNIndependentVowelDecision:
        return PCGNIndependentVowelDecision(
            source_character=source_character,
            romanization=None,
            romanization_options=romanization_options,
            source_table_row=table_row,
            status="UNRESOLVED",
            ipa=None,
            ukrainian=None,
            source_locator=PCGN_INDEPENDENT_VOWEL_TABLE_LOCATOR,
            warnings=(reason, "NO_IPA_OR_UKRAINIAN_OUTPUT"),
        )

    if analysis.status != "STRUCTURE_ONLY":
        return unresolved("UNSUPPORTED_OR_UNRESOLVED_ORTHOGRAPHIC_COMPONENT")
    if len(analysis.independent_vowels) != 1:
        return unresolved("EXACTLY_ONE_INDEPENDENT_VOWEL_REQUIRED")
    if analysis.base_consonants or analysis.subscript_consonants:
        return unresolved("MIXED_CONSONANT_AND_INDEPENDENT_VOWEL_INPUT")
    if analysis.dependent_vowel_signs or analysis.register_shifters or analysis.shortening_marks:
        return unresolved("MIXED_VOWEL_OR_REGISTER_MARK_INPUT")
    if analysis.robat_positions or analysis.ahsda_positions or analysis.toandakhiat_positions:
        return unresolved("SPECIAL_DIACRITIC_NOT_SUPPORTED")
    if any(token.kind != "independent_vowel" for token in analysis.tokens):
        return unresolved("NON_INDEPENDENT_VOWEL_TOKEN_PRESENT")

    if source_character == "ឧ":
        return unresolved(
            "PCGN_NOTE_9_Ŏ_OR_Ŭ_REQUIRES_REFERENCE_SELECTION",
            romanization_options=("ŏ", "ŭ"),
        )
    if row is None:
        return unresolved("INDEPENDENT_VOWEL_NOT_LISTED_IN_PCGN_TABLE_SUBSET")

    return PCGNIndependentVowelDecision(
        source_character=source_character,
        romanization=row[1],
        romanization_options=(),
        source_table_row=row[0],
        status="RESOLVED",
        ipa=None,
        ukrainian=None,
        source_locator=PCGN_INDEPENDENT_VOWEL_TABLE_LOCATOR,
        warnings=("INDEPENDENT_VOWEL_COMPONENT_ONLY", "NO_IPA_OR_UKRAINIAN_OUTPUT"),
    )



PCGN_SHORTENED_VOWEL_TABLE_LOCATOR = (
    "PCGN 1972, Independent/Dependent Vowel Characters table rows 1–2, Note 5"
)
PCGN_CODA_CLASSES = frozenset({"k", "ng", "h", "other"})


@dataclass(frozen=True)
class PCGNShortenedVowelDecision:
    pattern: Literal["INHERENT_BANTOC", "AA_BANTOC", "SAMYOK_CODA"] | None
    shortening_mark: Literal["់", "័"] | None
    series: Literal["â", "ô"] | None
    coda_character: str | None
    coda_class: Literal["k", "ng", "h", "other"] | None
    romanization: str | None
    source_table_row: int | None
    status: Literal["RESOLVED", "UNRESOLVED"]
    ipa: None
    ukrainian: None
    source_locator: str
    warnings: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def resolve_pcgn_shortened_vowel(
    analysis: PCGNOrthographicAnalysis,
    onset_analysis: PCGNOrthographicAnalysis,
    coda_class: Literal["k", "ng", "h", "other"] | None,
) -> PCGNShortenedVowelDecision:
    """Resolve only the PCGN Note 5 shortened-vowel component.

    The caller supplies an onset-only orthographic analysis and an explicit
    coda class. Neither phonetic syllable segmentation nor coda identity is
    inferred from the full chunk. The full chunk must match one of the exact
    Note 5 shapes: onset+coda+BANTOC, onset+AA+coda+BANTOC, or
    onset+SAMYOK+coda. Only the shortened vowel component is returned.
    """
    def unresolved(reason: str) -> PCGNShortenedVowelDecision:
        return PCGNShortenedVowelDecision(
            pattern=None,
            shortening_mark=None,
            series=None,
            coda_character=None,
            coda_class=coda_class if coda_class in PCGN_CODA_CLASSES else None,
            romanization=None,
            source_table_row=None,
            status="UNRESOLVED",
            ipa=None,
            ukrainian=None,
            source_locator=PCGN_SHORTENED_VOWEL_TABLE_LOCATOR,
            warnings=(reason, "NO_COMPLETE_SYLLABLE_IPA_OR_UKRAINIAN_OUTPUT"),
        )

    if analysis.status != "STRUCTURE_ONLY" or onset_analysis.status != "STRUCTURE_ONLY":
        return unresolved("UNSUPPORTED_OR_UNRESOLVED_ORTHOGRAPHIC_COMPONENT")
    if coda_class not in PCGN_CODA_CLASSES:
        return unresolved("EXPLICIT_PCGN_CODA_CLASS_REQUIRED")
    if (
        len(onset_analysis.base_consonants) != 1
        or len(onset_analysis.subscript_consonants) > 1
        or onset_analysis.dependent_vowel_signs
        or onset_analysis.independent_vowels
        or onset_analysis.shortening_marks
        or onset_analysis.robat_positions
        or onset_analysis.ahsda_positions
        or onset_analysis.toandakhiat_positions
        or any(
            token.kind not in {"unstacked_consonant", "subscript_consonant", "register_shifter"}
            for token in onset_analysis.tokens
        )
    ):
        return unresolved("ONSET_ANALYSIS_MUST_CONTAIN_ONE_BASE_AND_AT_MOST_ONE_FOOT_ONLY")

    series_decision = resolve_pcgn_series(onset_analysis)
    if series_decision.status != "RESOLVED" or series_decision.series not in {"â", "ô"}:
        return unresolved("PCGN_NOTE_2_3_ONSET_SERIES_MUST_BE_RESOLVED")

    onset_tokens = tuple(onset_analysis.tokens)
    if tuple(analysis.tokens[:len(onset_tokens)]) != onset_tokens:
        return unresolved("ONSET_ANALYSIS_DOES_NOT_MATCH_FULL_CHUNK_PREFIX")
    tail = tuple(token.kind for token in analysis.tokens[len(onset_tokens):])
    tail_text = tuple(token.text for token in analysis.tokens[len(onset_tokens):])
    if len(analysis.base_consonants) != 2:
        return unresolved("EXACTLY_ONE_ONSET_BASE_AND_ONE_EXPLICIT_CODA_CONSONANT_REQUIRED")
    if analysis.subscript_consonants != onset_analysis.subscript_consonants:
        return unresolved("FULL_CHUNK_FOOT_DOES_NOT_MATCH_ONSET_ANALYSIS")
    if analysis.register_shifters != onset_analysis.register_shifters:
        return unresolved("FULL_CHUNK_SHIFTER_DOES_NOT_MATCH_ONSET_ANALYSIS")
    if analysis.independent_vowels or analysis.robat_positions or analysis.ahsda_positions or analysis.toandakhiat_positions:
        return unresolved("INDEPENDENT_VOWEL_OR_SPECIAL_DIACRITIC_NOT_SUPPORTED")
    if len(analysis.shortening_marks) != 1 or len(analysis.shortening_mark_positions) != 1:
        return unresolved("EXACTLY_ONE_NOTE_5_SHORTENING_MARK_REQUIRED")

    coda_character = analysis.base_consonants[-1]
    mark = analysis.shortening_marks[0]
    mark_position = analysis.shortening_mark_positions[0]
    if mark == "់" and mark_position != len(analysis.normalized_text) - 1:
        return unresolved("BANTOC_MUST_BE_THE_FINAL_CODEPOINT_IN_THE_LISTED_PATTERN")
    if mark == "័" and mark_position != len(onset_analysis.normalized_text):
        return unresolved("SAMYOK_SANNYA_MUST_IMMEDIATELY_FOLLOW_THE_ONSET_CLUSTER")
    if mark == "់" and not analysis.dependent_vowel_signs:
        expected_tail = ("unstacked_consonant", "shortening_mark")
        pattern = "INHERENT_BANTOC"
        row = 1
    elif mark == "់" and analysis.dependent_vowel_signs == ("ា",):
        expected_tail = ("dependent_vowel", "unstacked_consonant", "shortening_mark")
        pattern = "AA_BANTOC"
        row = 2
    elif mark == "័" and not analysis.dependent_vowel_signs:
        expected_tail = ("shortening_mark", "unstacked_consonant")
        pattern = "SAMYOK_CODA"
        row = 2
    else:
        return unresolved("SHORTENING_MARK_AND_VOWEL_PATTERN_NOT_LISTED_IN_PCGN_NOTE_5")

    if tail != expected_tail:
        return unresolved("FULL_CHUNK_DOES_NOT_MATCH_EXACT_PCGN_NOTE_5_TOKEN_ORDER")
    if mark == "់" and tail_text[-1] != "់":
        return unresolved("BANTOC_MUST_FOLLOW_THE_CODA_IN_THE_LISTED_PATTERN")
    if mark == "័" and tail_text[0] != "័":
        return unresolved("SAMYOK_SANNYA_MUST_PRECEDE_THE_CODA_IN_THE_LISTED_PATTERN")

    if pattern == "INHERENT_BANTOC":
        value = "á" if series_decision.series == "â" else "ó"
    elif series_decision.series == "â":
        value = "ă"
    elif coda_class in {"k", "ng", "h"}:
        value = "eă"
    else:
        value = "oă"

    return PCGNShortenedVowelDecision(
        pattern=pattern,
        shortening_mark=mark,
        series=series_decision.series,
        coda_character=coda_character,
        coda_class=coda_class,
        romanization=value,
        source_table_row=row,
        status="RESOLVED",
        ipa=None,
        ukrainian=None,
        source_locator=PCGN_SHORTENED_VOWEL_TABLE_LOCATOR,
        warnings=(
            "PCGN_NOTE_5_SHORTENED_VOWEL_COMPONENT_ONLY",
            "ONSET_SERIES_RESOLVED_FROM_SEPARATE_ONSET_ANALYSIS",
            "CODA_CLASS_CALLER_SUPPLIED_NOT_INFERRED",
            "NO_CODA_ROMANIZATION_SYLLABLE_SEGMENTATION_IPA_OR_UKRAINIAN_OUTPUT",
        ),
    )



PCGN_ROBAT_TABLE_LOCATOR = (
    "PCGN 1972, Diacritical Marks table row 4 (p. 4), Note 6 (p. 5)"
)
PCGN_ROMANIZED_CONSONANT_VALUES = frozenset({
    "k", "kh", "ng", "ch", "chh", "nh", "d", "th", "t",
    "b", "p", "ph", "n", "m", "y", "r", "l", "v", "s", "h", "’",
})


@dataclass(frozen=True)
class PCGNRobatDecision:
    marked_character: str | None
    marked_consonant_romanization: str | None
    romanization: str | None
    status: Literal["RESOLVED", "UNRESOLVED"]
    ipa: None
    ukrainian: None
    source_locator: str
    warnings: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def resolve_pcgn_robat(
    analysis: PCGNOrthographicAnalysis,
    marked_consonant_romanization: str | None,
) -> PCGNRobatDecision:
    """Resolve the PCGN Note 6 rC component with explicit consonant context.

    The consonant value is supplied by the caller from the appropriate PCGN
    consonant-table context. This resolver does not infer the marked
    consonant's romanization or produce a complete syllable.
    """
    def unresolved(reason: str) -> PCGNRobatDecision:
        return PCGNRobatDecision(
            marked_character=None,
            marked_consonant_romanization=(
                marked_consonant_romanization
                if marked_consonant_romanization in PCGN_ROMANIZED_CONSONANT_VALUES
                else None
            ),
            romanization=None,
            status="UNRESOLVED",
            ipa=None,
            ukrainian=None,
            source_locator=PCGN_ROBAT_TABLE_LOCATOR,
            warnings=(reason, "NO_COMPLETE_SYLLABLE_IPA_OR_UKRAINIAN_OUTPUT"),
        )

    if analysis.status != "STRUCTURE_ONLY":
        return unresolved("UNSUPPORTED_OR_UNRESOLVED_ORTHOGRAPHIC_COMPONENT")
    if marked_consonant_romanization not in PCGN_ROMANIZED_CONSONANT_VALUES:
        return unresolved("EXPLICIT_PCGN_MARKED_CONSONANT_ROMANIZATION_REQUIRED")
    if len(analysis.robat_positions) != 1:
        return unresolved("EXACTLY_ONE_ROBAT_MARK_REQUIRED")
    if analysis.robat_positions[0] != len(analysis.normalized_text) - 1:
        return unresolved("ROBAT_MUST_BE_FINAL_IN_THE_SUPPORTED_COMPONENT_CHUNK")
    if len(analysis.tokens) < 2 or analysis.tokens[-1].kind != "robat":
        return unresolved("ROBAT_TOKEN_MUST_END_THE_COMPONENT_CHUNK")
    marked_token = analysis.tokens[-2]
    if marked_token.kind != "unstacked_consonant":
        return unresolved("ROBAT_MUST_IMMEDIATELY_FOLLOW_ONE_UNSTACKED_MARKED_CONSONANT")
    if marked_token.text not in CONSONANTS_BY_CHAR:
        return unresolved("MARKED_CHARACTER_IS_NOT_A_MODELED_KHMER_CONSONANT")

    return PCGNRobatDecision(
        marked_character=marked_token.text,
        marked_consonant_romanization=marked_consonant_romanization,
        romanization="r" + marked_consonant_romanization,
        status="RESOLVED",
        ipa=None,
        ukrainian=None,
        source_locator=PCGN_ROBAT_TABLE_LOCATOR,
        warnings=(
            "PCGN_NOTE_6_ROBAT_R_C_COMPONENT_ONLY",
            "MARKED_CONSONANT_ROMANIZATION_CALLER_SUPPLIED_NOT_INFERRED",
            "NO_ONSET_CODA_SYLLABLE_SEGMENTATION_IPA_OR_UKRAINIAN_OUTPUT",
        ),
    )



PCGN_AHSDA_TABLE_LOCATOR = (
    "PCGN 1972, Diacritical Marks table row 5 (p. 4), Note 7 (p. 5)"
)


@dataclass(frozen=True)
class PCGNAhsdaDecision:
    marked_character: str | None
    syllable_position: Literal["INITIAL", "FINAL"] | None
    series: Literal["â", "ô"] | None
    effect: Literal["MARK_NOT_ROMANIZED_INITIAL", "CONSONANT_VOWELLED_FINAL"] | None
    romanization: str | None
    status: Literal["RESOLVED", "UNRESOLVED"]
    ipa: None
    ukrainian: None
    source_locator: str
    warnings: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def resolve_pcgn_ahsda(
    analysis: PCGNOrthographicAnalysis,
    syllable_position: Literal["INITIAL", "FINAL"] | None,
    series: Literal["â", "ô"] | None,
) -> PCGNAhsdaDecision:
    """Resolve the position-sensitive PCGN Note 7 AHSDA component.

    Syllable position is explicit caller context, never inferred from an
    orthographic chunk. In final position the caller also supplies the
    consonant-series value. The result is only the AHSDA mark's effect.
    """
    def unresolved(reason: str) -> PCGNAhsdaDecision:
        return PCGNAhsdaDecision(
            marked_character=None,
            syllable_position=syllable_position if syllable_position in {"INITIAL", "FINAL"} else None,
            series=series if series in {"â", "ô"} else None,
            effect=None,
            romanization=None,
            status="UNRESOLVED",
            ipa=None,
            ukrainian=None,
            source_locator=PCGN_AHSDA_TABLE_LOCATOR,
            warnings=(reason, "NO_COMPLETE_SYLLABLE_IPA_OR_UKRAINIAN_OUTPUT"),
        )

    if analysis.status != "STRUCTURE_ONLY":
        return unresolved("UNSUPPORTED_OR_UNRESOLVED_ORTHOGRAPHIC_COMPONENT")
    if syllable_position not in {"INITIAL", "FINAL"}:
        return unresolved("EXPLICIT_AHSDA_SYLLABLE_POSITION_REQUIRED")
    if len(analysis.ahsda_positions) != 1:
        return unresolved("EXACTLY_ONE_AHSDA_MARK_REQUIRED")
    if analysis.ahsda_positions[0] != len(analysis.normalized_text) - 1:
        return unresolved("AHSDA_MUST_BE_FINAL_IN_THE_SUPPORTED_COMPONENT_CHUNK")
    if len(analysis.tokens) < 2 or analysis.tokens[-1].kind != "ahsda_position_sensitive":
        return unresolved("AHSDA_TOKEN_MUST_END_THE_COMPONENT_CHUNK")
    marked_token = analysis.tokens[-2]
    if marked_token.kind != "unstacked_consonant" or marked_token.text not in CONSONANTS_BY_CHAR:
        return unresolved("AHSDA_MUST_IMMEDIATELY_FOLLOW_ONE_MODELED_UNSTACKED_CONSONANT")

    if syllable_position == "INITIAL":
        if series is not None and series not in {"â", "ô"}:
            return unresolved("INVALID_CALLER_SUPPLIED_SERIES")
        return PCGNAhsdaDecision(
            marked_character=marked_token.text,
            syllable_position="INITIAL",
            series=series,
            effect="MARK_NOT_ROMANIZED_INITIAL",
            romanization=None,
            status="RESOLVED",
            ipa=None,
            ukrainian=None,
            source_locator=PCGN_AHSDA_TABLE_LOCATOR,
            warnings=(
                "PCGN_NOTE_7_AHSDA_MARK_NOT_ROMANIZED_IN_SYLLABLE_INITIAL_POSITION",
                "SYLLABLE_POSITION_CALLER_SUPPLIED_NOT_INFERRED",
                "NO_COMPLETE_SYLLABLE_IPA_OR_UKRAINIAN_OUTPUT",
            ),
        )

    if series not in {"â", "ô"}:
        return unresolved("EXPLICIT_RESOLVED_SERIES_REQUIRED_IN_SYLLABLE_FINAL_POSITION")
    return PCGNAhsdaDecision(
        marked_character=marked_token.text,
        syllable_position="FINAL",
        series=series,
        effect="CONSONANT_VOWELLED_FINAL",
        romanization=series,
        status="RESOLVED",
        ipa=None,
        ukrainian=None,
        source_locator=PCGN_AHSDA_TABLE_LOCATOR,
        warnings=(
            "PCGN_NOTE_7_FINAL_AHSDA_INDICATES_SERIES_VOWEL",
            "SYLLABLE_POSITION_AND_SERIES_CALLER_SUPPLIED_NOT_INFERRED",
            "VOWEL_COMPONENT_ONLY_NO_COMPLETE_SYLLABLE_IPA_OR_UKRAINIAN_OUTPUT",
        ),
    )



PCGN_TOANDAKHIAT_TABLE_LOCATOR = (
    "PCGN 1972, Diacritical Marks table row 6 (p. 4), Note 8 (p. 5)"
)


@dataclass(frozen=True)
class PCGNToandakhiatDecision:
    marked_character: str | None
    marked_token_kind: Literal["unstacked_consonant", "subscript_consonant"] | None
    effect: Literal["OMIT_MARKED_CHARACTER"] | None
    romanization: None
    status: Literal["RESOLVED", "UNRESOLVED"]
    ipa: None
    ukrainian: None
    source_locator: str
    warnings: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def resolve_pcgn_toandakhiat(
    analysis: PCGNOrthographicAnalysis,
    marked_character: str | None,
) -> PCGNToandakhiatDecision:
    """Resolve the PCGN Note 8 silent-character omission component.

    The exact marked consonant grapheme is an explicit caller input. This
    resolver verifies that it is the consonant token immediately preceding
    the one final TOANDAKHIAT mark; it does not guess which character is
    silent or romanize the rest of the word.
    """
    def unresolved(reason: str) -> PCGNToandakhiatDecision:
        return PCGNToandakhiatDecision(
            marked_character=None,
            marked_token_kind=None,
            effect=None,
            romanization=None,
            status="UNRESOLVED",
            ipa=None,
            ukrainian=None,
            source_locator=PCGN_TOANDAKHIAT_TABLE_LOCATOR,
            warnings=(reason, "NO_COMPLETE_SYLLABLE_IPA_OR_UKRAINIAN_OUTPUT"),
        )

    if analysis.status != "STRUCTURE_ONLY":
        return unresolved("UNSUPPORTED_OR_UNRESOLVED_ORTHOGRAPHIC_COMPONENT")
    if not marked_character:
        return unresolved("EXPLICIT_TOANDAKHIAT_MARKED_CHARACTER_REQUIRED")
    if len(analysis.toandakhiat_positions) != 1:
        return unresolved("EXACTLY_ONE_TOANDAKHIAT_MARK_REQUIRED")
    if analysis.toandakhiat_positions[0] != len(analysis.normalized_text) - 1:
        return unresolved("TOANDAKHIAT_MUST_BE_FINAL_IN_THE_SUPPORTED_COMPONENT_CHUNK")
    if len(analysis.tokens) < 2 or analysis.tokens[-1].kind != "toandakhiat_silent_mark":
        return unresolved("TOANDAKHIAT_TOKEN_MUST_END_THE_COMPONENT_CHUNK")
    marked_token = analysis.tokens[-2]
    if marked_token.kind not in {"unstacked_consonant", "subscript_consonant"}:
        return unresolved("TOANDAKHIAT_MARKED_COMPONENT_MUST_BE_A_MODELED_CONSONANT")
    if marked_token.text != marked_character:
        return unresolved("CALLER_IDENTIFIED_MARKED_CHARACTER_DOES_NOT_MATCH_SOURCE_TOKEN")

    return PCGNToandakhiatDecision(
        marked_character=marked_token.text,
        marked_token_kind=marked_token.kind,
        effect="OMIT_MARKED_CHARACTER",
        romanization=None,
        status="RESOLVED",
        ipa=None,
        ukrainian=None,
        source_locator=PCGN_TOANDAKHIAT_TABLE_LOCATOR,
        warnings=(
            "PCGN_NOTE_8_MARKED_CHARACTER_NOT_PRONOUNCED_AND_NOT_ROMANIZED",
            "MARKED_CHARACTER_CALLER_IDENTIFIED_NOT_INFERRED",
            "NO_REMAINING_WORD_ROMANIZATION_IPA_OR_UKRAINIAN_OUTPUT",
        ),
    )



PCGN_GLOTTAL_ONSET_TABLE_LOCATOR = (
    "PCGN 1972, Consonant Characters row 22 and Note 4 (p. 5)"
)


@dataclass(frozen=True)
class PCGNGlottalOnsetDecision:
    source_character: str | None
    word_initial: bool | None
    followed_by_vowel_letter: bool | None
    romanization: str | None
    romanization_options: tuple[str, ...]
    status: Literal["RESOLVED", "UNRESOLVED"]
    ipa: None
    ukrainian: None
    source_locator: str
    warnings: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def resolve_pcgn_glottal_onset(
    analysis: PCGNOrthographicAnalysis,
    word_initial: bool | None,
    followed_by_vowel_letter: bool | None,
) -> PCGNGlottalOnsetDecision:
    """Resolve the PCGN Note 4 apostrophe component for អ.

    Word-initial position and the following vowel-letter context are explicit
    caller inputs. The apostrophe is optional only when both are true.
    """
    def unresolved(reason: str) -> PCGNGlottalOnsetDecision:
        return PCGNGlottalOnsetDecision(
            source_character=None,
            word_initial=word_initial if isinstance(word_initial, bool) else None,
            followed_by_vowel_letter=(
                followed_by_vowel_letter
                if isinstance(followed_by_vowel_letter, bool)
                else None
            ),
            romanization=None,
            romanization_options=(),
            status="UNRESOLVED",
            ipa=None,
            ukrainian=None,
            source_locator=PCGN_GLOTTAL_ONSET_TABLE_LOCATOR,
            warnings=(reason, "NO_COMPLETE_SYLLABLE_IPA_OR_UKRAINIAN_OUTPUT"),
        )

    if analysis.status != "STRUCTURE_ONLY":
        return unresolved("UNSUPPORTED_OR_UNRESOLVED_ORTHOGRAPHIC_COMPONENT")
    if not isinstance(word_initial, bool) or not isinstance(followed_by_vowel_letter, bool):
        return unresolved("EXPLICIT_WORD_POSITION_AND_FOLLOWING_VOWEL_CONTEXT_REQUIRED")
    if (
        analysis.base_consonants != ("អ",)
        or analysis.subscript_consonants
        or analysis.dependent_vowel_signs
        or analysis.independent_vowels
        or analysis.shortening_marks
        or analysis.robat_positions
        or analysis.ahsda_positions
        or analysis.toandakhiat_positions
        or len(analysis.tokens) != 1
        or analysis.tokens[0].kind != "unstacked_consonant"
    ):
        return unresolved("NOTE_4_COMPONENT_MUST_BE_THE_STANDALONE_ONSET_CARRIER_ALONE")

    series_decision = resolve_pcgn_series(analysis)
    if series_decision.status != "RESOLVED" or series_decision.series != "â":
        return unresolved("PCGN_NOTE_4_REQUIRES_THE_A_SERIES_ONSET_CARRIER")

    optional = word_initial and followed_by_vowel_letter
    options = ("’", "") if optional else ("’",)
    warnings = [
        "PCGN_NOTE_4_A_SERIES_ONSET_CARRIER_AS_APOSTROPHE",
        "WORD_POSITION_AND_FOLLOWING_VOWEL_CONTEXT_CALLER_SUPPLIED",
        "APOSTROPHE_COMPONENT_ONLY_NO_COMPLETE_SYLLABLE_IPA_OR_UKRAINIAN_OUTPUT",
    ]
    if optional:
        warnings.append("PCGN_NOTE_4_WORD_INITIAL_BEFORE_VOWEL_APOSTROPHE_OPTIONAL")
    return PCGNGlottalOnsetDecision(
        source_character="អ",
        word_initial=word_initial,
        followed_by_vowel_letter=followed_by_vowel_letter,
        romanization="’",
        romanization_options=options,
        status="RESOLVED",
        ipa=None,
        ukrainian=None,
        source_locator=PCGN_GLOTTAL_ONSET_TABLE_LOCATOR,
        warnings=tuple(warnings),
    )


__all__ = [
    "PCGNOrthographicAnalysis",
    "PCGNToken",
    "PCGNSeriesDecision",
    "PCGNVowelDecision",
    "PCGNIndependentVowelDecision",
    "PCGNShortenedVowelDecision",
    "PCGNRobatDecision",
    "PCGNAhsdaDecision",
    "PCGNToandakhiatDecision",
    "PCGNGlottalOnsetDecision",
    "PCGN_WEAK_SUBSCRIPTS",
    "PCGN_NO_SUBSCRIPT_FOR",
    "resolve_pcgn_series",
    "resolve_pcgn_dependent_vowel",
    "resolve_pcgn_independent_vowel",
    "resolve_pcgn_shortened_vowel",
    "resolve_pcgn_robat",
    "resolve_pcgn_ahsda",
    "resolve_pcgn_toandakhiat",
    "resolve_pcgn_glottal_onset",
    "analyze_pcgn_orthographic_chunk",
]
