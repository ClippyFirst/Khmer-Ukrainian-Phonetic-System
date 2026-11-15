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
    onset_exception: Literal["BA_WITH_FOOT_P_IN_A_SERIES", "BA_WITH_MUUSIKATOAN_P_IN_A_SERIES"] | None
    series_before_shifter: Literal["â", "ô"] | None
    shifter_effect: Literal["TRIISAP_A_TO_O", "MUUSIKATOAN_O_TO_A", "BA_MUUSIKATOAN_P_IN_A"] | None
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
    Unicode Khmer syllabic order. BA+TRIISAP, shifters on BA+foot, multiple
    marks and wrong-way shifters abstain pending narrower adjudication.
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
            return unresolved("BA_WITH_TRIISAP_EXCEPTION_NOT_RESOLVED")

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


__all__ = [
    "PCGNOrthographicAnalysis",
    "PCGNToken",
    "PCGNSeriesDecision",
    "PCGNVowelDecision",
    "PCGN_WEAK_SUBSCRIPTS",
    "PCGN_NO_SUBSCRIPT_FOR",
    "resolve_pcgn_series",
    "resolve_pcgn_dependent_vowel",
    "analyze_pcgn_orthographic_chunk",
]
