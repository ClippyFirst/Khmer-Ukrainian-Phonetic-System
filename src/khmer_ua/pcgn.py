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
    onset_exception: Literal["BA_WITH_FOOT_P_IN_A_SERIES", "BA_WITH_MUUSIKATOAN_P_IN_A_SERIES"] | None
    series_before_shifter: Literal["â", "ô"] | None
    shifter_effect: Literal["TRIISAP_A_TO_O", "MUUSIKATOAN_O_TO_A", "BA_MUUSIKATOAN_P_IN_A", "TRIISAP_NO_SHIFT_BA_EXCEPTION"] | None
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
    Unicode Khmer syllabic order. The Note 2 TRIISAP exception for BA is represented as no series shift;
    Note 3 BA+MUUSIKATOAN and BA+foot p-in-â exceptions are kept distinct.
    Shifters on BA+foot, multiple marks and wrong-way shifters abstain.
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
                # PCGN Note 2 explicitly exempts BA from TRIISAP's normal
                # â-to-ô shift. Note 3's p-in-â exception is MUUSIKATOAN
                # (◌៉), not TRIISAP (◌៊).
                return PCGNSeriesDecision(
                    series="ô",
                    basis="BASE",
                    status="RESOLVED",
                    onset_exception=None,
                    series_before_shifter="ô",
                    shifter_effect="TRIISAP_NO_SHIFT_BA_EXCEPTION",
                    source_locator="PCGN 1972, Notes 2–3 (pp. 2–3)",
                    warnings=(
                        "PCGN_NOTE_2_TRIISAP_EXEMPT_FOR_BA_NO_SERIES_SHIFT",
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
    warnings = [
        "PCGN_NOTE_3_SERIES_SELECTION_ONLY",
        "PCGN_NOTE_2_DIACRITICS_MAY_BE_OMITTED_CONSULT_REFERENCE_IF_SERIES_UNCERTAIN",
    ]
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
    ("ិ",): (3, "ĕ", "ĭ"),
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
    ("េ", "ា"): (16, "aô", "oŭ"),
    ("េ", "ៅ"): (17, "au", "ŏu"),
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


PCGN_CONSONANT_TABLE_LOCATOR = (
    "PCGN 1972, Consonant Characters and Subscript Consonant Forms table (pp. 1–2), Note 3"
)
# Rows 1–21 only. The glottal carrier in row 22 is delegated to Note 4.
PCGN_CONSONANT_ROMANIZATION_ROWS: dict[str, tuple[int, str]] = {
    "ក": (1, "k"), "គ": (1, "k"),
    "ខ": (2, "kh"), "ឃ": (2, "kh"),
    "ង": (3, "ng"),
    "ច": (4, "ch"), "ជ": (4, "ch"),
    "ឆ": (5, "chh"), "ឈ": (5, "chh"),
    "ញ": (6, "nh"),
    "ដ": (7, "d"), "ឌ": (7, "d"),
    "ឋ": (8, "th"), "ឍ": (8, "th"),
    "ថ": (9, "th"), "ធ": (9, "th"),
    "ណ": (10, "n"), "ន": (10, "n"),
    "ត": (11, "t"), "ទ": (11, "t"),
    "ប": (12, "b"),
    "ព": (13, "p"),
    "ផ": (14, "ph"), "ភ": (14, "ph"),
    "ម": (15, "m"),
    "យ": (16, "y"),
    "រ": (17, "r"),
    "ឡ": (18, "l"), "ល": (18, "l"),
    "វ": (19, "v"),
    "ស": (20, "s"),
    "ហ": (21, "h"),
}


@dataclass(frozen=True)
class PCGNConsonantDecision:
    base_character: str | None
    base_table_row: int | None
    base_romanization: str | None
    subscript_character: str | None
    subscript_table_row: int | None
    subscript_romanization: str | None
    series: Literal["â", "ô"] | None
    onset_exception: Literal[
        "BA_WITH_FOOT_P_IN_A_SERIES",
        "BA_WITH_MUUSIKATOAN_P_IN_A_SERIES",
    ] | None
    romanization: str | None
    status: Literal["RESOLVED", "UNRESOLVED"]
    ipa: None
    ukrainian: None
    source_locator: str
    warnings: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def resolve_pcgn_consonant(
    analysis: PCGNOrthographicAnalysis,
) -> PCGNConsonantDecision:
    """Resolve one base consonant and at most one foot to a PCGN onset.

    The Note 2–3 series resolver supplies the BA exception needed for the
    b/p alternation. Row 22 (អ) remains with the separate Note 4 glottal
    onset resolver. This returns a consonant-cluster component only.
    """
    def unresolved(reason: str) -> PCGNConsonantDecision:
        return PCGNConsonantDecision(
            base_character=analysis.base_consonants[0] if len(analysis.base_consonants) == 1 else None,
            base_table_row=None,
            base_romanization=None,
            subscript_character=analysis.subscript_consonants[0] if len(analysis.subscript_consonants) == 1 else None,
            subscript_table_row=None,
            subscript_romanization=None,
            series=None,
            onset_exception=None,
            romanization=None,
            status="UNRESOLVED",
            ipa=None,
            ukrainian=None,
            source_locator=PCGN_CONSONANT_TABLE_LOCATOR,
            warnings=(reason, "NO_COMPLETE_SYLLABLE_IPA_OR_UKRAINIAN_OUTPUT"),
        )

    if analysis.status != "STRUCTURE_ONLY":
        return unresolved("UNSUPPORTED_OR_UNRESOLVED_ORTHOGRAPHIC_COMPONENT")
    if len(analysis.base_consonants) != 1 or len(analysis.subscript_consonants) > 1:
        return unresolved("EXACTLY_ONE_BASE_AND_AT_MOST_ONE_FOOT_REQUIRED")
    if (
        analysis.dependent_vowel_signs
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
        return unresolved("CONSONANT_ONSET_ONLY_CHUNK_REQUIRED")

    base = analysis.base_consonants[0]
    if base == "អ":
        return unresolved("PCGN_ROW_22_ALIF_REQUIRES_NOTE_4_GLOTTAL_ONSET_CONTEXT")
    base_row = PCGN_CONSONANT_ROMANIZATION_ROWS.get(base)
    if base_row is None:
        return unresolved("BASE_CONSONANT_NOT_IN_PCGN_ROWS_1_TO_21")

    subscript = analysis.subscript_consonants[0] if analysis.subscript_consonants else None
    subscript_row = PCGN_CONSONANT_ROMANIZATION_ROWS.get(subscript) if subscript else None
    if subscript is not None and subscript_row is None:
        return unresolved("SUBSCRIPT_CONSONANT_NOT_IN_PCGN_ROWS_1_TO_21")

    series_decision = resolve_pcgn_series(analysis)
    if series_decision.status != "RESOLVED" or series_decision.series not in {"â", "ô"}:
        return unresolved("PCGN_NOTE_2_3_SERIES_MUST_BE_RESOLVED")

    base_romanization = base_row[1]
    if base == "ប" and series_decision.onset_exception in {
        "BA_WITH_FOOT_P_IN_A_SERIES",
        "BA_WITH_MUUSIKATOAN_P_IN_A_SERIES",
        "BA_WITH_TRIISAP_P_IN_A_SERIES",
    }:
        base_romanization = "p"

    subscript_romanization = None
    if subscript_row is not None:
        subscript_romanization = "p" if subscript == "ប" else subscript_row[1]

    parts = (base_romanization,) + ((subscript_romanization,) if subscript_romanization else ())
    return PCGNConsonantDecision(
        base_character=base,
        base_table_row=base_row[0],
        base_romanization=base_romanization,
        subscript_character=subscript,
        subscript_table_row=subscript_row[0] if subscript_row else None,
        subscript_romanization=subscript_romanization,
        series=series_decision.series,
        onset_exception=series_decision.onset_exception,
        romanization="".join(parts),
        status="RESOLVED",
        ipa=None,
        ukrainian=None,
        source_locator=PCGN_CONSONANT_TABLE_LOCATOR,
        warnings=(
            "PCGN_CONSONANT_CLUSTER_COMPONENT_ONLY",
            "BA_B_P_SELECTION_FOLLOWS_NOTE_3_EXCEPTION_WHEN_PRESENT",
            "ROW_22_ALIF_IS_HANDLED_BY_SEPARATE_NOTE_4_RESOLVER",
            "NO_SYLLABLE_SEGMENTATION_IPA_OR_UKRAINIAN_OUTPUT",
        ),
    )


PCGN_FINAL_CONSONANT_TABLE_LOCATOR = (
    "PCGN 1972, final-consonant no-following-vowel rule (p. 2) with consonant table (pp. 1–2)"
)


@dataclass(frozen=True)
class PCGNFinalConsonantDecision:
    syllable_position: Literal["FINAL"]
    has_following_vowel_character: bool
    has_toandakhiat: bool
    base_character: str | None
    base_table_row: int | None
    base_romanization: str | None
    subscript_character: str | None
    subscript_table_row: int | None
    subscript_romanization: str | None
    romanization: str | None
    following_vowel: Literal[""] | None
    status: Literal["GENERAL_RULE_APPLIED", "UNRESOLVED"]
    ipa: None
    ukrainian: None
    source_locator: str
    warnings: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def resolve_pcgn_final_consonant(
    analysis: PCGNOrthographicAnalysis,
    *,
    has_following_vowel_character: bool,
    has_toandakhiat: bool,
) -> PCGNFinalConsonantDecision:
    """Resolve a final consonant component under the PCGN general rule.

    The caller must isolate the final consonant chunk and explicitly confirm
    that it has neither a following vowel character nor TOANDAKHIAT. The guide
    says such a final consonant should generally have no vowel letter after it.
    BA and ALIF are withheld because their special Note 3/4 context is not
    resolved by this generic coda rule.
    """
    if type(has_following_vowel_character) is not bool or type(has_toandakhiat) is not bool:
        raise TypeError(
            "has_following_vowel_character and has_toandakhiat must be explicit booleans"
        )

    def unresolved(reason: str) -> PCGNFinalConsonantDecision:
        return PCGNFinalConsonantDecision(
            syllable_position="FINAL",
            has_following_vowel_character=has_following_vowel_character,
            has_toandakhiat=has_toandakhiat,
            base_character=analysis.base_consonants[0] if len(analysis.base_consonants) == 1 else None,
            base_table_row=None,
            base_romanization=None,
            subscript_character=analysis.subscript_consonants[0] if len(analysis.subscript_consonants) == 1 else None,
            subscript_table_row=None,
            subscript_romanization=None,
            romanization=None,
            following_vowel=None,
            status="UNRESOLVED",
            ipa=None,
            ukrainian=None,
            source_locator=PCGN_FINAL_CONSONANT_TABLE_LOCATOR,
            warnings=(reason, "NO_COMPLETE_SYLLABLE_IPA_OR_UKRAINIAN_OUTPUT"),
        )

    if has_following_vowel_character:
        return unresolved("FINAL_CONSONANT_IS_ACCOMPANIED_BY_A_VOWEL_CHARACTER")
    if has_toandakhiat:
        return unresolved("FINAL_CONSONANT_IS_ACCOMPANIED_BY_TOANDAKHIAT")
    if analysis.status != "STRUCTURE_ONLY":
        return unresolved("UNSUPPORTED_OR_UNRESOLVED_ORTHOGRAPHIC_COMPONENT")
    if len(analysis.base_consonants) != 1 or len(analysis.subscript_consonants) > 1:
        return unresolved("FINAL_CHUNK_REQUIRES_ONE_BASE_AND_AT_MOST_ONE_FOOT")
    if (
        analysis.dependent_vowel_signs
        or analysis.independent_vowels
        or analysis.shortening_marks
        or analysis.robat_positions
        or analysis.ahsda_positions
        or analysis.toandakhiat_positions
        or analysis.register_shifters
        or any(token.kind not in {"unstacked_consonant", "subscript_consonant"} for token in analysis.tokens)
    ):
        return unresolved("FINAL_CONSONANT_CHUNK_CONTAINS_UNSUPPORTED_MARKS_OR_VOWELS")

    base = analysis.base_consonants[0]
    if base in {"ប", "អ"}:
        return unresolved("BA_OR_ALIF_FINAL_CONTEXT_REQUIRES_SEPARATE_NOTE_3_OR_NOTE_4_DECISION")
    base_row = PCGN_CONSONANT_ROMANIZATION_ROWS.get(base)
    if base_row is None:
        return unresolved("FINAL_BASE_NOT_IN_SUPPORTED_PCGN_CONSONANT_ROWS")

    subscript = analysis.subscript_consonants[0] if analysis.subscript_consonants else None
    if subscript in {"ប", "អ"}:
        return unresolved("BA_OR_ALIF_FOOT_FINAL_CONTEXT_REQUIRES_SEPARATE_DECISION")
    subscript_row = PCGN_CONSONANT_ROMANIZATION_ROWS.get(subscript) if subscript else None
    if subscript is not None and subscript_row is None:
        return unresolved("FINAL_SUBSCRIPT_NOT_IN_SUPPORTED_PCGN_CONSONANT_ROWS")

    base_romanization = base_row[1]
    subscript_romanization = subscript_row[1] if subscript_row else None
    romanization = base_romanization + (subscript_romanization or "")
    return PCGNFinalConsonantDecision(
        syllable_position="FINAL",
        has_following_vowel_character=has_following_vowel_character,
        has_toandakhiat=has_toandakhiat,
        base_character=base,
        base_table_row=base_row[0],
        base_romanization=base_romanization,
        subscript_character=subscript,
        subscript_table_row=subscript_row[0] if subscript_row else None,
        subscript_romanization=subscript_romanization,
        romanization=romanization,
        following_vowel="",
        status="GENERAL_RULE_APPLIED",
        ipa=None,
        ukrainian=None,
        source_locator=PCGN_FINAL_CONSONANT_TABLE_LOCATOR,
        warnings=(
            "PCGN_FINAL_CONSONANT_HAS_NO_FOLLOWING_VOWEL_LETTER",
            "SOURCE_RULE_IS_GENERAL_NOT_ABSOLUTE",
            "CALLER_SUPPLIED_FINAL_POSITION_AND_ABSENCE_OF_VOWEL_AND_TOANDAKHIAT",
            "BA_AND_ALIF_FINAL_CASES_ABSTAIN",
            "NO_SYLLABLE_SEGMENTATION_IPA_OR_UKRAINIAN_OUTPUT",
        ),
    )


PCGN_INHERENT_VOWEL_TABLE_LOCATOR = (
    "PCGN 1972, Independent/Dependent Vowel Characters table row 1 (p. 2)"
)


@dataclass(frozen=True)
class PCGNInherentVowelDecision:
    syllable_position: Literal["NON_FINAL", "FINAL"] | None
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
            syllable_position=syllable_position if syllable_position in {"NON_FINAL", "FINAL"} else None,
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
    "PCGNSyllableAssembly",
    "PCGNClosedSyllableAssembly",
    "PCGNDependentClosedSyllableAssembly",
    "PCGNGlottalOpenSyllableAssembly",
    "assemble_pcgn_glottal_open_syllable",
    "PCGNGlottalDependentClosedSyllableAssembly",
    "assemble_pcgn_glottal_dependent_closed_syllable",
    "PCGNGlottalShortenedClosedSyllableAssembly",
    "assemble_pcgn_glottal_shortened_closed_syllable",
    "PCGNRobatClosedSyllableAssembly",
    "assemble_pcgn_robat_closed_syllable",
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
    "assemble_pcgn_open_syllable",
    "assemble_pcgn_shortened_closed_syllable",
    "assemble_pcgn_dependent_closed_syllable",
]


PCGN_OPEN_SYLLABLE_ASSEMBLY_LOCATORS = (
    PCGN_CONSONANT_TABLE_LOCATOR,
    PCGN_DEPENDENT_VOWEL_TABLE_LOCATOR,
)


@dataclass(frozen=True)
class PCGNSyllableAssembly:
    """A caller-segmented, open CV syllable assembled from PCGN components."""

    source_text: str
    normalized_text: str
    onset_text: str
    series: Literal["â", "ô"] | None
    onset_romanization: str | None
    vowel_romanization: str | None
    romanization: str | None
    onset_base: str | None
    onset_subscript: str | None
    onset_table_rows: tuple[int, ...]
    vowel_table_row: int | None
    status: Literal["RESOLVED", "UNRESOLVED"]
    ipa: None
    ukrainian: None
    source_locators: tuple[str, ...]
    warnings: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def assemble_pcgn_open_syllable(
    onset_analysis: PCGNOrthographicAnalysis,
    syllable_analysis: PCGNOrthographicAnalysis,
) -> PCGNSyllableAssembly:
    """Assemble one explicitly supplied open CV syllable from PCGN components.

    The caller, not this function, supplies the onset-only chunk and the
    complete open-syllable chunk. The latter must consist of that exact onset
    token prefix followed only by one supported dependent-vowel pattern.
    Coda-bearing, independent-vowel, shortened-vowel, special-mark, Alif,
    ambiguous, malformed and multi-syllable inputs abstain.

    This is a bounded orthographic romanization adapter, not phonetic
    syllabification, IPA generation or Ukrainian transcription. In
    particular, it never discovers Khmer word boundaries in running text.
    """
    def unresolved(reason: str) -> PCGNSyllableAssembly:
        return PCGNSyllableAssembly(
            source_text=syllable_analysis.raw_text,
            normalized_text=syllable_analysis.normalized_text,
            onset_text=onset_analysis.raw_text,
            series=None,
            onset_romanization=None,
            vowel_romanization=None,
            romanization=None,
            onset_base=(
                onset_analysis.base_consonants[0]
                if len(onset_analysis.base_consonants) == 1
                else None
            ),
            onset_subscript=(
                onset_analysis.subscript_consonants[0]
                if len(onset_analysis.subscript_consonants) == 1
                else None
            ),
            onset_table_rows=(),
            vowel_table_row=None,
            status="UNRESOLVED",
            ipa=None,
            ukrainian=None,
            source_locators=PCGN_OPEN_SYLLABLE_ASSEMBLY_LOCATORS,
            warnings=(reason, "NO_WORD_SEGMENTATION_IPA_OR_UKRAINIAN_OUTPUT"),
        )

    if (
        onset_analysis.status != "STRUCTURE_ONLY"
        or syllable_analysis.status != "STRUCTURE_ONLY"
    ):
        return unresolved("UNSUPPORTED_OR_UNRESOLVED_ORTHOGRAPHIC_COMPONENT")

    onset_tokens = tuple(onset_analysis.tokens)
    syllable_tokens = tuple(syllable_analysis.tokens)
    if not onset_tokens or syllable_tokens[:len(onset_tokens)] != onset_tokens:
        return unresolved("CALLER_ONSET_MUST_MATCH_EXACT_SYLLABLE_TOKEN_PREFIX")
    vowel_tokens = syllable_tokens[len(onset_tokens):]
    if not vowel_tokens or any(token.kind != "dependent_vowel" for token in vowel_tokens):
        return unresolved("OPEN_SYLLABLE_REQUIRES_ONLY_A_SUPPORTED_DEPENDENT_VOWEL_AFTER_ONSET")

    if (
        syllable_analysis.base_consonants != onset_analysis.base_consonants
        or syllable_analysis.subscript_consonants != onset_analysis.subscript_consonants
        or syllable_analysis.register_shifters != onset_analysis.register_shifters
        or syllable_analysis.independent_vowels
        or syllable_analysis.shortening_marks
        or syllable_analysis.robat_positions
        or syllable_analysis.ahsda_positions
        or syllable_analysis.toandakhiat_positions
    ):
        return unresolved("OPEN_SYLLABLE_MUST_HAVE_NO_CODA_OR_UNSUPPORTED_VOWEL_OR_MARK")

    series = resolve_pcgn_series(onset_analysis)
    onset = resolve_pcgn_consonant(onset_analysis)
    vowel = resolve_pcgn_dependent_vowel(syllable_analysis, series)
    if series.status != "RESOLVED" or onset.status != "RESOLVED" or vowel.status != "RESOLVED":
        reason = (
            series.warnings[0]
            if series.status != "RESOLVED"
            else onset.warnings[0]
            if onset.status != "RESOLVED"
            else vowel.warnings[0]
        )
        return unresolved(reason)

    rows = (onset.base_table_row,) + (
        (onset.subscript_table_row,) if onset.subscript_table_row is not None else ()
    )
    return PCGNSyllableAssembly(
        source_text=syllable_analysis.raw_text,
        normalized_text=syllable_analysis.normalized_text,
        onset_text=onset_analysis.raw_text,
        series=series.series,
        onset_romanization=onset.romanization,
        vowel_romanization=vowel.romanization,
        romanization=onset.romanization + vowel.romanization,
        onset_base=onset.base_character,
        onset_subscript=onset.subscript_character,
        onset_table_rows=rows,
        vowel_table_row=vowel.source_table_row,
        status="RESOLVED",
        ipa=None,
        ukrainian=None,
        source_locators=PCGN_OPEN_SYLLABLE_ASSEMBLY_LOCATORS,
        warnings=(
            "CALLER_SUPPLIED_ONSET_AND_OPEN_SYLLABLE_BOUNDARIES",
            "PCGN_ONSET_AND_DEPENDENT_VOWEL_COMPONENTS_CONCATENATED",
            "OPEN_CV_ORTHOGRAPHIC_ROMANIZATION_ONLY",
            "NO_CODA_WORD_SEGMENTATION_IPA_OR_UKRAINIAN_OUTPUT",
        ),
    )


PCGN_CLOSED_SYLLABLE_ASSEMBLY_LOCATORS = (
    PCGN_CONSONANT_TABLE_LOCATOR,
    PCGN_SHORTENED_VOWEL_TABLE_LOCATOR,
    PCGN_FINAL_CONSONANT_TABLE_LOCATOR,
)


@dataclass(frozen=True)
class PCGNClosedSyllableAssembly:
    """A caller-segmented, Note 5 closed syllable assembled from PCGN components."""

    source_text: str
    normalized_text: str
    onset_text: str
    coda_text: str
    series: Literal["â", "ô"] | None
    pattern: Literal["INHERENT_BANTOC", "AA_BANTOC", "SAMYOK_CODA"] | None
    shortening_mark: str | None
    coda_class: Literal["k", "ng", "h", "other"] | None
    onset_romanization: str | None
    vowel_romanization: str | None
    coda_romanization: str | None
    romanization: str | None
    onset_table_rows: tuple[int, ...]
    vowel_table_row: int | None
    coda_table_row: int | None
    status: Literal["RESOLVED", "UNRESOLVED"]
    ipa: None
    ukrainian: None
    source_locators: tuple[str, ...]
    warnings: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def assemble_pcgn_shortened_closed_syllable(
    onset_analysis: PCGNOrthographicAnalysis,
    syllable_analysis: PCGNOrthographicAnalysis,
    coda_analysis: PCGNOrthographicAnalysis,
    coda_class: Literal["k", "ng", "h", "other"] | str,
) -> PCGNClosedSyllableAssembly:
    """Assemble one caller-segmented PCGN Note 5 closed syllable.

    The caller supplies onset-only, complete-syllable and coda-only chunks,
    plus the Note 5 coda class. The exact Note 5 pattern resolver validates
    source token order; the final-consonant resolver validates the coda.
    The supplied class is cross-checked against the resolved PCGN coda value,
    so a caller cannot select the eă/oă branch inconsistently.

    Only the three listed Note 5 shapes and a single supported final base
    consonant are accepted. No word or syllable boundaries are inferred.
    This produces orthographic PCGN Latin only, never IPA or Ukrainian.
    """
    def unresolved(reason: str) -> PCGNClosedSyllableAssembly:
        return PCGNClosedSyllableAssembly(
            source_text=syllable_analysis.raw_text,
            normalized_text=syllable_analysis.normalized_text,
            onset_text=onset_analysis.raw_text,
            coda_text=coda_analysis.raw_text,
            series=None,
            pattern=None,
            shortening_mark=None,
            coda_class=coda_class if coda_class in PCGN_CODA_CLASSES else None,
            onset_romanization=None,
            vowel_romanization=None,
            coda_romanization=None,
            romanization=None,
            onset_table_rows=(),
            vowel_table_row=None,
            coda_table_row=None,
            status="UNRESOLVED",
            ipa=None,
            ukrainian=None,
            source_locators=PCGN_CLOSED_SYLLABLE_ASSEMBLY_LOCATORS,
            warnings=(reason, "NO_WORD_SEGMENTATION_IPA_OR_UKRAINIAN_OUTPUT"),
        )

    if (
        onset_analysis.status != "STRUCTURE_ONLY"
        or syllable_analysis.status != "STRUCTURE_ONLY"
        or coda_analysis.status != "STRUCTURE_ONLY"
    ):
        return unresolved("UNSUPPORTED_OR_UNRESOLVED_ORTHOGRAPHIC_COMPONENT")

    if (
        len(coda_analysis.tokens) != 1
        or coda_analysis.tokens[0].kind != "unstacked_consonant"
        or len(coda_analysis.base_consonants) != 1
        or coda_analysis.subscript_consonants
        or coda_analysis.register_shifters
        or coda_analysis.dependent_vowel_signs
        or coda_analysis.independent_vowels
        or coda_analysis.shortening_marks
        or coda_analysis.robat_positions
        or coda_analysis.ahsda_positions
        or coda_analysis.toandakhiat_positions
    ):
        return unresolved("CODA_MUST_BE_ONE_UNMARKED_UNSTACKED_CONSONANT")

    onset_tokens = tuple(onset_analysis.tokens)
    syllable_tokens = tuple(syllable_analysis.tokens)
    if not onset_tokens or syllable_tokens[:len(onset_tokens)] != onset_tokens:
        return unresolved("CALLER_ONSET_MUST_MATCH_EXACT_SYLLABLE_TOKEN_PREFIX")
    tail = syllable_tokens[len(onset_tokens):]
    if sum(token == coda_analysis.tokens[0] for token in tail) != 1:
        return unresolved("CALLER_CODA_MUST_MATCH_EXACTLY_ONE_SYLLABLE_TOKEN")
    if (
        syllable_analysis.base_consonants
        != onset_analysis.base_consonants + coda_analysis.base_consonants
        or syllable_analysis.subscript_consonants != onset_analysis.subscript_consonants
        or syllable_analysis.register_shifters != onset_analysis.register_shifters
    ):
        return unresolved("SYLLABLE_ONSET_AND_CODA_COMPONENTS_DO_NOT_MATCH_CALLER_CHUNKS")

    final = resolve_pcgn_final_consonant(
        coda_analysis,
        has_following_vowel_character=False,
        has_toandakhiat=False,
    )
    if final.status != "GENERAL_RULE_APPLIED" or final.romanization is None:
        return unresolved(final.warnings[0])

    expected_coda_class = (
        final.romanization
        if final.romanization in {"k", "ng", "h"}
        else "other"
    )
    if coda_class not in PCGN_CODA_CLASSES or coda_class != expected_coda_class:
        return unresolved("EXPLICIT_CODA_CLASS_MUST_MATCH_RESOLVED_PCGN_CODA_ROMANIZATION")

    series = resolve_pcgn_series(onset_analysis)
    onset = resolve_pcgn_consonant(onset_analysis)
    shortened = resolve_pcgn_shortened_vowel(
        syllable_analysis,
        onset_analysis,
        coda_class,
    )
    if (
        series.status != "RESOLVED"
        or onset.status != "RESOLVED"
        or shortened.status != "RESOLVED"
    ):
        reason = (
            series.warnings[0]
            if series.status != "RESOLVED"
            else onset.warnings[0]
            if onset.status != "RESOLVED"
            else shortened.warnings[0]
        )
        return unresolved(reason)
    if shortened.coda_character != coda_analysis.base_consonants[0]:
        return unresolved("NOTE_5_CODA_CHARACTER_DOES_NOT_MATCH_FINAL_COMPONENT")

    onset_rows = (onset.base_table_row,) + (
        (onset.subscript_table_row,) if onset.subscript_table_row is not None else ()
    )
    return PCGNClosedSyllableAssembly(
        source_text=syllable_analysis.raw_text,
        normalized_text=syllable_analysis.normalized_text,
        onset_text=onset_analysis.raw_text,
        coda_text=coda_analysis.raw_text,
        series=series.series,
        pattern=shortened.pattern,
        shortening_mark=shortened.shortening_mark,
        coda_class=shortened.coda_class,
        onset_romanization=onset.romanization,
        vowel_romanization=shortened.romanization,
        coda_romanization=final.romanization,
        romanization=onset.romanization + shortened.romanization + final.romanization,
        onset_table_rows=onset_rows,
        vowel_table_row=shortened.source_table_row,
        coda_table_row=final.base_table_row,
        status="RESOLVED",
        ipa=None,
        ukrainian=None,
        source_locators=PCGN_CLOSED_SYLLABLE_ASSEMBLY_LOCATORS,
        warnings=(
            "CALLER_SUPPLIED_ONSET_SYLLABLE_AND_CODA_BOUNDARIES",
            "PCGN_NOTE_5_SHORTENED_VOWEL_AND_FINAL_CONSONANT_COMPONENTS_ASSEMBLED",
            "CODA_CLASS_CROSS_CHECKED_AGAINST_PCGN_CONSONANT_ROMANIZATION",
            "NO_WORD_SEGMENTATION_IPA_OR_UKRAINIAN_OUTPUT",
        ),
    )


PCGN_DEPENDENT_CLOSED_SYLLABLE_ASSEMBLY_LOCATORS = (
    PCGN_CONSONANT_TABLE_LOCATOR,
    PCGN_DEPENDENT_VOWEL_TABLE_LOCATOR,
    PCGN_FINAL_CONSONANT_TABLE_LOCATOR,
)


@dataclass(frozen=True)
class PCGNDependentClosedSyllableAssembly:
    """A caller-segmented closed syllable with an ordinary dependent vowel."""

    source_text: str
    normalized_text: str
    onset_text: str
    vowel_chunk_text: str
    coda_text: str
    series: Literal["â", "ô"] | None
    onset_romanization: str | None
    vowel_romanization: str | None
    coda_romanization: str | None
    romanization: str | None
    onset_table_rows: tuple[int, ...]
    vowel_table_row: int | None
    coda_table_row: int | None
    status: Literal["RESOLVED", "UNRESOLVED"]
    ipa: None
    ukrainian: None
    source_locators: tuple[str, ...]
    warnings: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def assemble_pcgn_dependent_closed_syllable(
    onset_analysis: PCGNOrthographicAnalysis,
    vowel_analysis: PCGNOrthographicAnalysis,
    syllable_analysis: PCGNOrthographicAnalysis,
    coda_analysis: PCGNOrthographicAnalysis,
) -> PCGNDependentClosedSyllableAssembly:
    """Assemble an explicitly segmented onset + dependent vowel + final coda.

    The caller supplies four chunks: onset-only, onset-plus-normal-dependent-
    vowel, complete syllable, and coda-only. Exact token-prefix relationships
    are checked before the existing Note 2–3 series, consonant, dependent-
    vowel and final-consonant resolvers are composed.

    Only one unmarked final consonant and a normal dependent-vowel table
    pattern are accepted. Shortened/independent vowels, special marks, Alif,
    unsupported codas and ambiguous or malformed structures abstain. This
    is orthographic BGN/PCGN output, not IPA or Ukrainian transcription.
    """
    def unresolved(reason: str) -> PCGNDependentClosedSyllableAssembly:
        return PCGNDependentClosedSyllableAssembly(
            source_text=syllable_analysis.raw_text,
            normalized_text=syllable_analysis.normalized_text,
            onset_text=onset_analysis.raw_text,
            vowel_chunk_text=vowel_analysis.raw_text,
            coda_text=coda_analysis.raw_text,
            series=None,
            onset_romanization=None,
            vowel_romanization=None,
            coda_romanization=None,
            romanization=None,
            onset_table_rows=(),
            vowel_table_row=None,
            coda_table_row=None,
            status="UNRESOLVED",
            ipa=None,
            ukrainian=None,
            source_locators=PCGN_DEPENDENT_CLOSED_SYLLABLE_ASSEMBLY_LOCATORS,
            warnings=(reason, "NO_WORD_SEGMENTATION_IPA_OR_UKRAINIAN_OUTPUT"),
        )

    analyses = (onset_analysis, vowel_analysis, syllable_analysis, coda_analysis)
    if any(analysis.status != "STRUCTURE_ONLY" for analysis in analyses):
        return unresolved("UNSUPPORTED_OR_UNRESOLVED_ORTHOGRAPHIC_COMPONENT")

    if (
        len(coda_analysis.tokens) != 1
        or coda_analysis.tokens[0].kind != "unstacked_consonant"
        or len(coda_analysis.base_consonants) != 1
        or coda_analysis.subscript_consonants
        or coda_analysis.register_shifters
        or coda_analysis.dependent_vowel_signs
        or coda_analysis.independent_vowels
        or coda_analysis.shortening_marks
        or coda_analysis.robat_positions
        or coda_analysis.ahsda_positions
        or coda_analysis.toandakhiat_positions
    ):
        return unresolved("CODA_MUST_BE_ONE_UNMARKED_UNSTACKED_CONSONANT")

    onset_tokens = tuple(onset_analysis.tokens)
    vowel_tokens = tuple(vowel_analysis.tokens)
    syllable_tokens = tuple(syllable_analysis.tokens)
    if not onset_tokens or vowel_tokens[:len(onset_tokens)] != onset_tokens:
        return unresolved("CALLER_ONSET_MUST_MATCH_EXACT_VOWEL_CHUNK_PREFIX")
    if any(token.kind != "dependent_vowel" for token in vowel_tokens[len(onset_tokens):]):
        return unresolved("VOWEL_CHUNK_MUST_CONTAIN_ONLY_NORMAL_DEPENDENT_VOWEL_SIGNS_AFTER_ONSET")
    if (
        not vowel_tokens[len(onset_tokens):]
        or syllable_tokens[:len(vowel_tokens)] != vowel_tokens
        or syllable_tokens[len(vowel_tokens):] != tuple(coda_analysis.tokens)
    ):
        return unresolved("COMPLETE_SYLLABLE_MUST_EQUAL_VOWEL_CHUNK_PLUS_EXACT_FINAL_CODA")

    if (
        vowel_analysis.base_consonants != onset_analysis.base_consonants
        or vowel_analysis.subscript_consonants != onset_analysis.subscript_consonants
        or vowel_analysis.register_shifters != onset_analysis.register_shifters
        or syllable_analysis.base_consonants
        != onset_analysis.base_consonants + coda_analysis.base_consonants
        or syllable_analysis.subscript_consonants != onset_analysis.subscript_consonants
        or syllable_analysis.register_shifters != onset_analysis.register_shifters
    ):
        return unresolved("ONSET_VOWEL_AND_CODA_COMPONENTS_DO_NOT_MATCH_CALLER_CHUNKS")

    series = resolve_pcgn_series(onset_analysis)
    onset = resolve_pcgn_consonant(onset_analysis)
    vowel = resolve_pcgn_dependent_vowel(vowel_analysis, series)
    final = resolve_pcgn_final_consonant(
        coda_analysis,
        has_following_vowel_character=False,
        has_toandakhiat=False,
    )
    if (
        series.status != "RESOLVED"
        or onset.status != "RESOLVED"
        or vowel.status != "RESOLVED"
        or final.status != "GENERAL_RULE_APPLIED"
    ):
        reason = (
            series.warnings[0]
            if series.status != "RESOLVED"
            else onset.warnings[0]
            if onset.status != "RESOLVED"
            else vowel.warnings[0]
            if vowel.status != "RESOLVED"
            else final.warnings[0]
        )
        return unresolved(reason)

    onset_rows = (onset.base_table_row,) + (
        (onset.subscript_table_row,) if onset.subscript_table_row is not None else ()
    )
    return PCGNDependentClosedSyllableAssembly(
        source_text=syllable_analysis.raw_text,
        normalized_text=syllable_analysis.normalized_text,
        onset_text=onset_analysis.raw_text,
        vowel_chunk_text=vowel_analysis.raw_text,
        coda_text=coda_analysis.raw_text,
        series=series.series,
        onset_romanization=onset.romanization,
        vowel_romanization=vowel.romanization,
        coda_romanization=final.romanization,
        romanization=onset.romanization + vowel.romanization + final.romanization,
        onset_table_rows=onset_rows,
        vowel_table_row=vowel.source_table_row,
        coda_table_row=final.base_table_row,
        status="RESOLVED",
        ipa=None,
        ukrainian=None,
        source_locators=PCGN_DEPENDENT_CLOSED_SYLLABLE_ASSEMBLY_LOCATORS,
        warnings=(
            "CALLER_SUPPLIED_ONSET_VOWEL_SYLLABLE_AND_CODA_BOUNDARIES",
            "NORMAL_DEPENDENT_VOWEL_AND_FINAL_CONSONANT_COMPONENTS_ASSEMBLED",
            "PCGN_FINAL_NO_FOLLOWING_VOWEL_RULE_APPLIED_TO_EXPLICIT_FINAL_CHUNK",
            "NO_WORD_SEGMENTATION_IPA_OR_UKRAINIAN_OUTPUT",
        ),
    )


PCGN_GLOTTAL_OPEN_SYLLABLE_LOCATORS = (
    PCGN_GLOTTAL_ONSET_TABLE_LOCATOR,
    PCGN_DEPENDENT_VOWEL_TABLE_LOCATOR,
)


@dataclass(frozen=True)
class PCGNGlottalOpenSyllableAssembly:
    """A caller-segmented open syllable with the Note 4 Alif carrier."""

    source_text: str
    normalized_text: str
    onset_text: str
    word_initial: bool | None
    followed_by_vowel_letter: bool | None
    series: Literal["â"] | None
    onset_romanization: str | None
    vowel_romanization: str | None
    romanization: str | None
    romanization_options: tuple[str, ...]
    vowel_table_row: int | None
    status: Literal["RESOLVED", "UNRESOLVED"]
    ipa: None
    ukrainian: None
    source_locators: tuple[str, ...]
    warnings: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def assemble_pcgn_glottal_open_syllable(
    onset_analysis: PCGNOrthographicAnalysis,
    syllable_analysis: PCGNOrthographicAnalysis,
    word_initial: bool | None,
    followed_by_vowel_letter: bool | None,
) -> PCGNGlottalOpenSyllableAssembly:
    """Assemble one explicitly supplied Alif + dependent-vowel open syllable.

    The caller supplies the standalone Alif onset, the complete open-syllable
    chunk, and the two Note 4 context flags. The exact onset token prefix and
    remaining dependent-vowel tokens are checked. Note 4's optional initial
    apostrophe is preserved as an explicit output alternative; it is never
    silently discarded. This is orthographic PCGN Latin only, not IPA or
    Ukrainian transcription, and no word/syllable boundaries are inferred.
    """
    def unresolved(reason: str) -> PCGNGlottalOpenSyllableAssembly:
        return PCGNGlottalOpenSyllableAssembly(
            source_text=syllable_analysis.raw_text,
            normalized_text=syllable_analysis.normalized_text,
            onset_text=onset_analysis.raw_text,
            word_initial=word_initial if isinstance(word_initial, bool) else None,
            followed_by_vowel_letter=(
                followed_by_vowel_letter
                if isinstance(followed_by_vowel_letter, bool)
                else None
            ),
            series=None,
            onset_romanization=None,
            vowel_romanization=None,
            romanization=None,
            romanization_options=(),
            vowel_table_row=None,
            status="UNRESOLVED",
            ipa=None,
            ukrainian=None,
            source_locators=PCGN_GLOTTAL_OPEN_SYLLABLE_LOCATORS,
            warnings=(reason, "NO_WORD_SEGMENTATION_IPA_OR_UKRAINIAN_OUTPUT"),
        )

    if onset_analysis.status != "STRUCTURE_ONLY" or syllable_analysis.status != "STRUCTURE_ONLY":
        return unresolved("UNSUPPORTED_OR_UNRESOLVED_ORTHOGRAPHIC_COMPONENT")

    onset_tokens = tuple(onset_analysis.tokens)
    syllable_tokens = tuple(syllable_analysis.tokens)
    if not onset_tokens or syllable_tokens[:len(onset_tokens)] != onset_tokens:
        return unresolved("CALLER_ALIF_ONSET_MUST_MATCH_EXACT_SYLLABLE_TOKEN_PREFIX")
    tail = syllable_tokens[len(onset_tokens):]
    if not tail or any(token.kind != "dependent_vowel" for token in tail):
        return unresolved("ALIF_OPEN_SYLLABLE_REQUIRES_ONLY_DEPENDENT_VOWEL_TOKENS_AFTER_ONSET")
    if (
        syllable_analysis.base_consonants != onset_analysis.base_consonants
        or syllable_analysis.subscript_consonants
        or syllable_analysis.register_shifters != onset_analysis.register_shifters
        or tuple(token.text for token in tail) != syllable_analysis.dependent_vowel_signs
    ):
        return unresolved("ALIF_ONSET_AND_DEPENDENT_VOWEL_CHUNKS_DO_NOT_MATCH")

    glottal = resolve_pcgn_glottal_onset(
        onset_analysis,
        word_initial,
        followed_by_vowel_letter,
    )
    series = resolve_pcgn_series(onset_analysis)
    if glottal.status != "RESOLVED":
        return unresolved(glottal.warnings[0])
    if series.status != "RESOLVED" or series.series != "â":
        return unresolved("PCGN_NOTE_4_REQUIRES_THE_A_SERIES_ONSET_CARRIER")
    vowel = resolve_pcgn_dependent_vowel(syllable_analysis, series)
    if vowel.status != "RESOLVED" or vowel.romanization is None:
        return unresolved(vowel.warnings[0])

    options = tuple(glottal_option + vowel.romanization for glottal_option in glottal.romanization_options)
    return PCGNGlottalOpenSyllableAssembly(
        source_text=syllable_analysis.raw_text,
        normalized_text=syllable_analysis.normalized_text,
        onset_text=onset_analysis.raw_text,
        word_initial=word_initial,
        followed_by_vowel_letter=followed_by_vowel_letter,
        series="â",
        onset_romanization=glottal.romanization,
        vowel_romanization=vowel.romanization,
        romanization=options[0],
        romanization_options=options,
        vowel_table_row=vowel.source_table_row,
        status="RESOLVED",
        ipa=None,
        ukrainian=None,
        source_locators=PCGN_GLOTTAL_OPEN_SYLLABLE_LOCATORS,
        warnings=(
            "CALLER_SUPPLIED_ALIF_ONSET_AND_OPEN_SYLLABLE_BOUNDARIES",
            "PCGN_NOTE_4_GLottal_APOSTROPHE_CONTEXT_APPLIED".upper(),
            "OPTIONAL_APOSTROPHE_VARIANT_PRESERVED_WHEN_NOTE_4_ALLOWS",
            "A_SERIES_DEPENDENT_VOWEL_COMPONENT_ASSEMBLED",
            "NO_WORD_SEGMENTATION_IPA_OR_UKRAINIAN_OUTPUT",
        ),
    )


PCGN_GLOTTAL_DEPENDENT_CLOSED_SYLLABLE_LOCATORS = (
    PCGN_GLOTTAL_ONSET_TABLE_LOCATOR,
    PCGN_DEPENDENT_VOWEL_TABLE_LOCATOR,
    PCGN_FINAL_CONSONANT_TABLE_LOCATOR,
)


@dataclass(frozen=True)
class PCGNGlottalDependentClosedSyllableAssembly:
    """A caller-segmented closed syllable with Note 4 Alif as its onset."""

    source_text: str
    normalized_text: str
    onset_text: str
    vowel_chunk_text: str
    coda_text: str
    word_initial: bool | None
    followed_by_vowel_letter: bool | None
    series: Literal["â"] | None
    onset_romanization: str | None
    vowel_romanization: str | None
    coda_romanization: str | None
    romanization: str | None
    romanization_options: tuple[str, ...]
    vowel_table_row: int | None
    coda_table_row: int | None
    status: Literal["RESOLVED", "UNRESOLVED"]
    ipa: None
    ukrainian: None
    source_locators: tuple[str, ...]
    warnings: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def assemble_pcgn_glottal_dependent_closed_syllable(
    onset_analysis: PCGNOrthographicAnalysis,
    vowel_analysis: PCGNOrthographicAnalysis,
    syllable_analysis: PCGNOrthographicAnalysis,
    coda_analysis: PCGNOrthographicAnalysis,
    word_initial: bool | None,
    followed_by_vowel_letter: bool | None,
) -> PCGNGlottalDependentClosedSyllableAssembly:
    """Assemble a caller-segmented Note 4 Alif + vowel + final-coda syllable.

    The caller supplies standalone Alif, Alif-plus-dependent-vowel, complete
    syllable and one-consonant coda chunks, together with the explicit Note 4
    word-position flags. Exact token boundaries are checked. Only the normal
    dependent-vowel table and the existing general final-consonant rule are
    composed; unsupported coda contexts abstain. Optional apostrophe spelling
    remains an explicit output alternative when Note 4 permits it.
    """
    def unresolved(reason: str) -> PCGNGlottalDependentClosedSyllableAssembly:
        return PCGNGlottalDependentClosedSyllableAssembly(
            source_text=syllable_analysis.raw_text,
            normalized_text=syllable_analysis.normalized_text,
            onset_text=onset_analysis.raw_text,
            vowel_chunk_text=vowel_analysis.raw_text,
            coda_text=coda_analysis.raw_text,
            word_initial=word_initial if isinstance(word_initial, bool) else None,
            followed_by_vowel_letter=(
                followed_by_vowel_letter
                if isinstance(followed_by_vowel_letter, bool)
                else None
            ),
            series=None,
            onset_romanization=None,
            vowel_romanization=None,
            coda_romanization=None,
            romanization=None,
            romanization_options=(),
            vowel_table_row=None,
            coda_table_row=None,
            status="UNRESOLVED",
            ipa=None,
            ukrainian=None,
            source_locators=PCGN_GLOTTAL_DEPENDENT_CLOSED_SYLLABLE_LOCATORS,
            warnings=(reason, "NO_WORD_SEGMENTATION_IPA_OR_UKRAINIAN_OUTPUT"),
        )

    analyses = (onset_analysis, vowel_analysis, syllable_analysis, coda_analysis)
    if any(analysis.status != "STRUCTURE_ONLY" for analysis in analyses):
        return unresolved("UNSUPPORTED_OR_UNRESOLVED_ORTHOGRAPHIC_COMPONENT")

    coda_tokens = tuple(coda_analysis.tokens)
    if (
        len(coda_tokens) != 1
        or coda_tokens[0].kind != "unstacked_consonant"
        or len(coda_analysis.base_consonants) != 1
        or coda_analysis.subscript_consonants
        or coda_analysis.register_shifters
        or coda_analysis.dependent_vowel_signs
        or coda_analysis.independent_vowels
        or coda_analysis.shortening_marks
        or coda_analysis.robat_positions
        or coda_analysis.ahsda_positions
        or coda_analysis.toandakhiat_positions
    ):
        return unresolved("CODA_MUST_BE_ONE_UNMARKED_UNSTACKED_CONSONANT")

    onset_tokens = tuple(onset_analysis.tokens)
    vowel_tokens = tuple(vowel_analysis.tokens)
    syllable_tokens = tuple(syllable_analysis.tokens)
    if not onset_tokens or vowel_tokens[:len(onset_tokens)] != onset_tokens:
        return unresolved("CALLER_ALIF_ONSET_MUST_MATCH_EXACT_VOWEL_CHUNK_PREFIX")
    vowel_tail = vowel_tokens[len(onset_tokens):]
    if not vowel_tail or any(token.kind != "dependent_vowel" for token in vowel_tail):
        return unresolved("VOWEL_CHUNK_MUST_CONTAIN_ONLY_DEPENDENT_VOWEL_SIGNS_AFTER_ALIF")
    if (
        syllable_tokens[:len(vowel_tokens)] != vowel_tokens
        or syllable_tokens[len(vowel_tokens):] != coda_tokens
    ):
        return unresolved("COMPLETE_SYLLABLE_MUST_EQUAL_ALIF_VOWEL_CHUNK_PLUS_EXACT_FINAL_CODA")
    if (
        vowel_analysis.base_consonants != onset_analysis.base_consonants
        or vowel_analysis.subscript_consonants != onset_analysis.subscript_consonants
        or vowel_analysis.register_shifters != onset_analysis.register_shifters
        or syllable_analysis.base_consonants != onset_analysis.base_consonants + coda_analysis.base_consonants
        or syllable_analysis.subscript_consonants != onset_analysis.subscript_consonants
        or syllable_analysis.register_shifters != onset_analysis.register_shifters
    ):
        return unresolved("ALIF_ONSET_VOWEL_AND_CODA_COMPONENTS_DO_NOT_MATCH_CALLER_CHUNKS")

    glottal = resolve_pcgn_glottal_onset(
        onset_analysis,
        word_initial,
        followed_by_vowel_letter,
    )
    series = resolve_pcgn_series(onset_analysis)
    if glottal.status != "RESOLVED":
        return unresolved(glottal.warnings[0])
    if series.status != "RESOLVED" or series.series != "â":
        return unresolved("PCGN_NOTE_4_REQUIRES_THE_A_SERIES_ONSET_CARRIER")

    vowel = resolve_pcgn_dependent_vowel(vowel_analysis, series)
    final = resolve_pcgn_final_consonant(
        coda_analysis,
        has_following_vowel_character=False,
        has_toandakhiat=False,
    )
    if vowel.status != "RESOLVED" or vowel.romanization is None:
        return unresolved(vowel.warnings[0])
    if final.status != "GENERAL_RULE_APPLIED" or final.romanization is None:
        return unresolved(final.warnings[0])

    options = tuple(
        glottal_option + vowel.romanization + final.romanization
        for glottal_option in glottal.romanization_options
    )
    return PCGNGlottalDependentClosedSyllableAssembly(
        source_text=syllable_analysis.raw_text,
        normalized_text=syllable_analysis.normalized_text,
        onset_text=onset_analysis.raw_text,
        vowel_chunk_text=vowel_analysis.raw_text,
        coda_text=coda_analysis.raw_text,
        word_initial=word_initial,
        followed_by_vowel_letter=followed_by_vowel_letter,
        series="â",
        onset_romanization=glottal.romanization,
        vowel_romanization=vowel.romanization,
        coda_romanization=final.romanization,
        romanization=options[0],
        romanization_options=options,
        vowel_table_row=vowel.source_table_row,
        coda_table_row=final.base_table_row,
        status="RESOLVED",
        ipa=None,
        ukrainian=None,
        source_locators=PCGN_GLOTTAL_DEPENDENT_CLOSED_SYLLABLE_LOCATORS,
        warnings=(
            "CALLER_SUPPLIED_ALIF_VOWEL_SYLLABLE_AND_CODA_BOUNDARIES",
            "PCGN_NOTE_4_APOSTROPHE_CONTEXT_APPLIED",
            "OPTIONAL_APOSTROPHE_VARIANT_PRESERVED_WHEN_NOTE_4_ALLOWS",
            "NORMAL_A_SERIES_DEPENDENT_VOWEL_AND_FINAL_CONSONANT_ASSEMBLED",
            "NO_WORD_SEGMENTATION_IPA_OR_UKRAINIAN_OUTPUT",
        ),
    )


PCGN_GLOTTAL_SHORTENED_CLOSED_SYLLABLE_LOCATORS = (
    PCGN_GLOTTAL_ONSET_TABLE_LOCATOR,
    PCGN_SHORTENED_VOWEL_TABLE_LOCATOR,
    PCGN_FINAL_CONSONANT_TABLE_LOCATOR,
)


@dataclass(frozen=True)
class PCGNGlottalShortenedClosedSyllableAssembly:
    """A caller-segmented Note 5 closed syllable with the Note 4 Alif onset."""

    source_text: str
    normalized_text: str
    onset_text: str
    coda_text: str
    word_initial: bool | None
    followed_by_vowel_letter: bool | None
    series: Literal["â"] | None
    pattern: Literal["INHERENT_BANTOC", "AA_BANTOC", "SAMYOK_CODA"] | None
    shortening_mark: Literal["់", "័"] | None
    coda_class: Literal["k", "ng", "h", "other"] | None
    onset_romanization: str | None
    vowel_romanization: str | None
    coda_romanization: str | None
    romanization: str | None
    romanization_options: tuple[str, ...]
    vowel_table_row: int | None
    coda_table_row: int | None
    status: Literal["RESOLVED", "UNRESOLVED"]
    ipa: None
    ukrainian: None
    source_locators: tuple[str, ...]
    warnings: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def assemble_pcgn_glottal_shortened_closed_syllable(
    onset_analysis: PCGNOrthographicAnalysis,
    syllable_analysis: PCGNOrthographicAnalysis,
    coda_analysis: PCGNOrthographicAnalysis,
    coda_class: Literal["k", "ng", "h", "other"] | str,
    word_initial: bool | None,
    followed_by_vowel_letter: bool | None,
) -> PCGNGlottalShortenedClosedSyllableAssembly:
    """Assemble one explicit Note 5 shortened closed syllable with Alif onset.

    The caller supplies standalone Alif, complete Note 5 syllable, one
    unmarked coda consonant, the PCGN Note 5 coda class, and explicit Note 4
    word-position flags. Existing resolvers validate the Note 5 shape, Alif
    carrier context and coda class. No boundaries or coda class are inferred.
    Optional apostrophe spelling remains an explicit output alternative.
    """
    def unresolved(reason: str) -> PCGNGlottalShortenedClosedSyllableAssembly:
        return PCGNGlottalShortenedClosedSyllableAssembly(
            source_text=syllable_analysis.raw_text,
            normalized_text=syllable_analysis.normalized_text,
            onset_text=onset_analysis.raw_text,
            coda_text=coda_analysis.raw_text,
            word_initial=word_initial if isinstance(word_initial, bool) else None,
            followed_by_vowel_letter=(
                followed_by_vowel_letter
                if isinstance(followed_by_vowel_letter, bool)
                else None
            ),
            series=None,
            pattern=None,
            shortening_mark=None,
            coda_class=coda_class if coda_class in PCGN_CODA_CLASSES else None,
            onset_romanization=None,
            vowel_romanization=None,
            coda_romanization=None,
            romanization=None,
            romanization_options=(),
            vowel_table_row=None,
            coda_table_row=None,
            status="UNRESOLVED",
            ipa=None,
            ukrainian=None,
            source_locators=PCGN_GLOTTAL_SHORTENED_CLOSED_SYLLABLE_LOCATORS,
            warnings=(reason, "NO_WORD_SEGMENTATION_IPA_OR_UKRAINIAN_OUTPUT"),
        )

    if any(
        analysis.status != "STRUCTURE_ONLY"
        for analysis in (onset_analysis, syllable_analysis, coda_analysis)
    ):
        return unresolved("UNSUPPORTED_OR_UNRESOLVED_ORTHOGRAPHIC_COMPONENT")

    coda_tokens = tuple(coda_analysis.tokens)
    if (
        len(coda_tokens) != 1
        or coda_tokens[0].kind != "unstacked_consonant"
        or len(coda_analysis.base_consonants) != 1
        or coda_analysis.subscript_consonants
        or coda_analysis.register_shifters
        or coda_analysis.dependent_vowel_signs
        or coda_analysis.independent_vowels
        or coda_analysis.shortening_marks
        or coda_analysis.robat_positions
        or coda_analysis.ahsda_positions
        or coda_analysis.toandakhiat_positions
    ):
        return unresolved("CODA_MUST_BE_ONE_UNMARKED_UNSTACKED_CONSONANT")

    onset_tokens = tuple(onset_analysis.tokens)
    syllable_tokens = tuple(syllable_analysis.tokens)
    if not onset_tokens or syllable_tokens[:len(onset_tokens)] != onset_tokens:
        return unresolved("CALLER_ALIF_ONSET_MUST_MATCH_EXACT_SYLLABLE_TOKEN_PREFIX")
    tail = syllable_tokens[len(onset_tokens):]
    if sum(token == coda_tokens[0] for token in tail) != 1:
        return unresolved("CALLER_CODA_MUST_MATCH_EXACTLY_ONE_SYLLABLE_TOKEN")
    if (
        syllable_analysis.base_consonants != onset_analysis.base_consonants + coda_analysis.base_consonants
        or syllable_analysis.subscript_consonants != onset_analysis.subscript_consonants
        or syllable_analysis.register_shifters != onset_analysis.register_shifters
    ):
        return unresolved("ALIF_ONSET_AND_CODA_COMPONENTS_DO_NOT_MATCH_CALLER_CHUNKS")

    glottal = resolve_pcgn_glottal_onset(
        onset_analysis,
        word_initial,
        followed_by_vowel_letter,
    )
    series = resolve_pcgn_series(onset_analysis)
    if glottal.status != "RESOLVED":
        return unresolved(glottal.warnings[0])
    if series.status != "RESOLVED" or series.series != "â":
        return unresolved("PCGN_NOTE_4_REQUIRES_THE_A_SERIES_ONSET_CARRIER")

    final = resolve_pcgn_final_consonant(
        coda_analysis,
        has_following_vowel_character=False,
        has_toandakhiat=False,
    )
    if final.status != "GENERAL_RULE_APPLIED" or final.romanization is None:
        return unresolved(final.warnings[0])
    expected_coda_class = final.romanization if final.romanization in {"k", "ng", "h"} else "other"
    if coda_class not in PCGN_CODA_CLASSES or coda_class != expected_coda_class:
        return unresolved("EXPLICIT_CODA_CLASS_MUST_MATCH_RESOLVED_PCGN_CODA_ROMANIZATION")

    shortened = resolve_pcgn_shortened_vowel(syllable_analysis, onset_analysis, coda_class)
    if shortened.status != "RESOLVED" or shortened.romanization is None:
        return unresolved(shortened.warnings[0])
    if shortened.coda_character != coda_analysis.base_consonants[0]:
        return unresolved("NOTE_5_CODA_CHARACTER_DOES_NOT_MATCH_FINAL_COMPONENT")

    options = tuple(
        glottal_option + shortened.romanization + final.romanization
        for glottal_option in glottal.romanization_options
    )
    return PCGNGlottalShortenedClosedSyllableAssembly(
        source_text=syllable_analysis.raw_text,
        normalized_text=syllable_analysis.normalized_text,
        onset_text=onset_analysis.raw_text,
        coda_text=coda_analysis.raw_text,
        word_initial=word_initial,
        followed_by_vowel_letter=followed_by_vowel_letter,
        series="â",
        pattern=shortened.pattern,
        shortening_mark=shortened.shortening_mark,
        coda_class=shortened.coda_class,
        onset_romanization=glottal.romanization,
        vowel_romanization=shortened.romanization,
        coda_romanization=final.romanization,
        romanization=options[0],
        romanization_options=options,
        vowel_table_row=shortened.source_table_row,
        coda_table_row=final.base_table_row,
        status="RESOLVED",
        ipa=None,
        ukrainian=None,
        source_locators=PCGN_GLOTTAL_SHORTENED_CLOSED_SYLLABLE_LOCATORS,
        warnings=(
            "CALLER_SUPPLIED_ALIF_SYLLABLE_AND_CODA_BOUNDARIES",
            "PCGN_NOTE_4_APOSTROPHE_CONTEXT_APPLIED",
            "OPTIONAL_APOSTROPHE_VARIANT_PRESERVED_WHEN_NOTE_4_ALLOWS",
            "PCGN_NOTE_5_SHORTENED_VOWEL_AND_FINAL_CODA_ASSEMBLED",
            "CODA_CLASS_CROSS_CHECKED_AGAINST_PCGN_CONSONANT_ROMANIZATION",
            "NO_WORD_SEGMENTATION_IPA_OR_UKRAINIAN_OUTPUT",
        ),
    )


PCGN_ROBAT_CLOSED_SYLLABLE_LOCATORS = (
    PCGN_CONSONANT_TABLE_LOCATOR,
    PCGN_INHERENT_VOWEL_TABLE_LOCATOR,
    PCGN_DEPENDENT_VOWEL_TABLE_LOCATOR,
    PCGN_ROBAT_TABLE_LOCATOR,
)


@dataclass(frozen=True)
class PCGNRobatClosedSyllableAssembly:
    """A caller-segmented syllable with a final ROBAT-marked consonant."""

    source_text: str
    normalized_text: str
    onset_text: str
    vowel_chunk_text: str
    coda_text: str
    marked_coda_text: str
    series: Literal["â", "ô"] | None
    onset_romanization: str | None
    vowel_romanization: str | None
    marked_coda_consonant_romanization: str | None
    coda_romanization: str | None
    romanization: str | None
    onset_table_rows: tuple[int, ...]
    vowel_table_row: int | None
    coda_table_row: int | None
    status: Literal["RESOLVED", "UNRESOLVED"]
    ipa: None
    ukrainian: None
    source_locators: tuple[str, ...]
    warnings: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def assemble_pcgn_robat_closed_syllable(
    onset_analysis: PCGNOrthographicAnalysis,
    vowel_analysis: PCGNOrthographicAnalysis,
    syllable_analysis: PCGNOrthographicAnalysis,
    coda_analysis: PCGNOrthographicAnalysis,
    marked_coda_analysis: PCGNOrthographicAnalysis,
) -> PCGNRobatClosedSyllableAssembly:
    """Assemble one explicit syllable whose final consonant carries ROBAT.

    The caller supplies onset-only, onset-plus-vowel (or onset-only for an
    inherent vowel), complete syllable, marked-coda-plus-ROBAT, and bare
    marked-coda chunks. Exact token boundaries are checked. The existing
    consonant, inherent/dependent vowel and Note 6 resolvers are composed;
    no syllable or word boundary is inferred. Output is PCGN orthographic
    Latin only, never IPA or Ukrainian.
    """
    def unresolved(reason: str) -> PCGNRobatClosedSyllableAssembly:
        return PCGNRobatClosedSyllableAssembly(
            source_text=syllable_analysis.raw_text,
            normalized_text=syllable_analysis.normalized_text,
            onset_text=onset_analysis.raw_text,
            vowel_chunk_text=vowel_analysis.raw_text,
            coda_text=coda_analysis.raw_text,
            marked_coda_text=marked_coda_analysis.raw_text,
            series=None,
            onset_romanization=None,
            vowel_romanization=None,
            marked_coda_consonant_romanization=None,
            coda_romanization=None,
            romanization=None,
            onset_table_rows=(),
            vowel_table_row=None,
            coda_table_row=None,
            status="UNRESOLVED",
            ipa=None,
            ukrainian=None,
            source_locators=PCGN_ROBAT_CLOSED_SYLLABLE_LOCATORS,
            warnings=(reason, "NO_WORD_SEGMENTATION_IPA_OR_UKRAINIAN_OUTPUT"),
        )

    analyses = (onset_analysis, vowel_analysis, syllable_analysis, coda_analysis, marked_coda_analysis)
    if any(analysis.status != "STRUCTURE_ONLY" for analysis in analyses):
        return unresolved("UNSUPPORTED_OR_UNRESOLVED_ORTHOGRAPHIC_COMPONENT")

    onset_tokens = tuple(onset_analysis.tokens)
    vowel_tokens = tuple(vowel_analysis.tokens)
    syllable_tokens = tuple(syllable_analysis.tokens)
    coda_tokens = tuple(coda_analysis.tokens)
    marked_tokens = tuple(marked_coda_analysis.tokens)
    if not onset_tokens or vowel_tokens[:len(onset_tokens)] != onset_tokens:
        return unresolved("CALLER_ONSET_MUST_MATCH_EXACT_VOWEL_CHUNK_PREFIX")
    vowel_tail = vowel_tokens[len(onset_tokens):]
    if any(token.kind != "dependent_vowel" for token in vowel_tail):
        return unresolved("VOWEL_CHUNK_MUST_CONTAIN_ONLY_DEPENDENT_VOWEL_SIGNS_AFTER_ONSET")
    if syllable_tokens[:len(vowel_tokens)] != vowel_tokens or syllable_tokens[len(vowel_tokens):] != coda_tokens:
        return unresolved("COMPLETE_SYLLABLE_MUST_EQUAL_VOWEL_CHUNK_PLUS_EXACT_ROBAT_CODA")
    if (
        len(marked_tokens) != 1
        or marked_tokens[0].kind != "unstacked_consonant"
        or len(coda_tokens) != 2
        or coda_tokens[0] != marked_tokens[0]
        or coda_tokens[1].kind != "robat"
        or coda_analysis.robat_positions != (len(coda_analysis.normalized_text) - 1,)
    ):
        return unresolved("ROBAT_CODA_MUST_EQUAL_ONE_MARKED_UNSTACKED_CONSONANT_PLUS_FINAL_ROBAT")
    if (
        coda_analysis.base_consonants != marked_coda_analysis.base_consonants
        or coda_analysis.subscript_consonants
        or coda_analysis.dependent_vowel_signs
        or coda_analysis.independent_vowels
        or coda_analysis.shortening_marks
        or coda_analysis.ahsda_positions
        or coda_analysis.toandakhiat_positions
        or syllable_analysis.base_consonants != onset_analysis.base_consonants + marked_coda_analysis.base_consonants
        or syllable_analysis.subscript_consonants != onset_analysis.subscript_consonants
        or syllable_analysis.register_shifters != onset_analysis.register_shifters
        or vowel_analysis.base_consonants != onset_analysis.base_consonants
        or vowel_analysis.subscript_consonants != onset_analysis.subscript_consonants
        or vowel_analysis.register_shifters != onset_analysis.register_shifters
    ):
        return unresolved("ONSET_VOWEL_AND_ROBAT_CODA_COMPONENTS_DO_NOT_MATCH_CALLER_CHUNKS")

    series = resolve_pcgn_series(onset_analysis)
    onset = resolve_pcgn_consonant(onset_analysis)
    marked_coda = resolve_pcgn_consonant(marked_coda_analysis)
    if series.status != "RESOLVED" or onset.status != "RESOLVED" or marked_coda.status != "RESOLVED":
        reason = (
            series.warnings[0] if series.status != "RESOLVED"
            else onset.warnings[0] if onset.status != "RESOLVED"
            else marked_coda.warnings[0]
        )
        return unresolved(reason)

    if vowel_tail:
        vowel = resolve_pcgn_dependent_vowel(vowel_analysis, series)
        if vowel.status != "RESOLVED" or vowel.romanization is None:
            return unresolved(vowel.warnings[0])
        vowel_value = vowel.romanization
        vowel_row = vowel.source_table_row
    else:
        inherent = resolve_pcgn_inherent_vowel(onset_analysis, "NON_FINAL")
        if inherent.status != "RESOLVED" or inherent.romanization is None:
            return unresolved(inherent.warnings[0])
        vowel_value = inherent.romanization
        vowel_row = inherent.source_table_row

    robat = resolve_pcgn_robat(coda_analysis, marked_coda.romanization)
    if robat.status != "RESOLVED" or robat.romanization is None:
        return unresolved(robat.warnings[0])
    onset_rows = (onset.base_table_row,) + (
        (onset.subscript_table_row,) if onset.subscript_table_row is not None else ()
    )
    return PCGNRobatClosedSyllableAssembly(
        source_text=syllable_analysis.raw_text,
        normalized_text=syllable_analysis.normalized_text,
        onset_text=onset_analysis.raw_text,
        vowel_chunk_text=vowel_analysis.raw_text,
        coda_text=coda_analysis.raw_text,
        marked_coda_text=marked_coda_analysis.raw_text,
        series=series.series,
        onset_romanization=onset.romanization,
        vowel_romanization=vowel_value,
        marked_coda_consonant_romanization=marked_coda.romanization,
        coda_romanization=robat.romanization,
        romanization=onset.romanization + vowel_value + robat.romanization,
        onset_table_rows=onset_rows,
        vowel_table_row=vowel_row,
        coda_table_row=marked_coda.base_table_row,
        status="RESOLVED",
        ipa=None,
        ukrainian=None,
        source_locators=PCGN_ROBAT_CLOSED_SYLLABLE_LOCATORS,
        warnings=(
            "CALLER_SUPPLIED_ONSET_VOWEL_SYLLABLE_AND_ROBAT_CODA_BOUNDARIES",
            "PCGN_NOTE_6_ROBAT_COMPONENT_RESOLVED_FROM_MARKED_CONSONANT_TABLE_VALUE",
            "INHERENT_OR_NORMAL_DEPENDENT_VOWEL_COMPONENT_ASSEMBLED",
            "NO_WORD_SEGMENTATION_IPA_OR_UKRAINIAN_OUTPUT",
        ),
    )



PCGN_INDEPENDENT_VOWEL_CLOSED_SYLLABLE_LOCATORS = (
    PCGN_INDEPENDENT_VOWEL_TABLE_LOCATOR,
    PCGN_FINAL_CONSONANT_TABLE_LOCATOR,
)


@dataclass(frozen=True)
class PCGNIndependentVowelClosedSyllableAssembly:
    """A caller-segmented closed syllable with one independent vowel."""

    source_text: str
    normalized_text: str
    vowel_chunk_text: str
    coda_text: str
    independent_vowel: str | None
    vowel_romanization: str | None
    vowel_table_row: int | None
    coda_romanization: str | None
    coda_table_row: int | None
    romanization: str | None
    romanization_options: tuple[str, ...]
    status: Literal["RESOLVED", "UNRESOLVED"]
    ipa: None
    ukrainian: None
    source_locators: tuple[str, ...]
    warnings: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def assemble_pcgn_independent_vowel_closed_syllable(
    vowel_analysis: PCGNOrthographicAnalysis,
    syllable_analysis: PCGNOrthographicAnalysis,
    coda_analysis: PCGNOrthographicAnalysis,
) -> PCGNIndependentVowelClosedSyllableAssembly:
    """Assemble one explicit independent-vowel + final-coda syllable.

    The caller supplies the independent-vowel-only chunk, complete syllable,
    and final-consonant-only chunk. Exact token prefix/suffix and component
    identity are validated. The independent-vowel resolver must select one
    listed PCGN value (Note 9's ឧ remains unresolved); the final consonant
    must satisfy the existing generic no-following-vowel/no-TOANDAKHIAT rule.
    No syllable or word boundaries are inferred.
    """
    def unresolved(reason: str) -> PCGNIndependentVowelClosedSyllableAssembly:
        vowel_decision = resolve_pcgn_independent_vowel(vowel_analysis)
        return PCGNIndependentVowelClosedSyllableAssembly(
            source_text=syllable_analysis.raw_text,
            normalized_text=syllable_analysis.normalized_text,
            vowel_chunk_text=vowel_analysis.raw_text,
            coda_text=coda_analysis.raw_text,
            independent_vowel=vowel_decision.source_character,
            vowel_romanization=None,
            vowel_table_row=vowel_decision.source_table_row,
            coda_romanization=None,
            coda_table_row=None,
            romanization=None,
            romanization_options=vowel_decision.romanization_options,
            status="UNRESOLVED",
            ipa=None,
            ukrainian=None,
            source_locators=PCGN_INDEPENDENT_VOWEL_CLOSED_SYLLABLE_LOCATORS,
            warnings=(reason, "NO_WORD_SEGMENTATION_IPA_OR_UKRAINIAN_OUTPUT"),
        )

    analyses = (vowel_analysis, syllable_analysis, coda_analysis)
    if any(analysis.status != "STRUCTURE_ONLY" for analysis in analyses):
        return unresolved("UNSUPPORTED_OR_UNRESOLVED_ORTHOGRAPHIC_COMPONENT")

    vowel_tokens = tuple(vowel_analysis.tokens)
    syllable_tokens = tuple(syllable_analysis.tokens)
    coda_tokens = tuple(coda_analysis.tokens)
    if (
        len(vowel_tokens) != 1
        or vowel_tokens[0].kind != "independent_vowel"
        or len(vowel_analysis.independent_vowels) != 1
        or vowel_analysis.base_consonants
        or vowel_analysis.subscript_consonants
        or vowel_analysis.dependent_vowel_signs
        or vowel_analysis.register_shifters
        or vowel_analysis.shortening_marks
        or vowel_analysis.robat_positions
        or vowel_analysis.ahsda_positions
        or vowel_analysis.toandakhiat_positions
    ):
        return unresolved("VOWEL_CHUNK_MUST_BE_ONE_STANDALONE_INDEPENDENT_VOWEL")
    if not coda_tokens or syllable_tokens[:1] != vowel_tokens or syllable_tokens[1:] != coda_tokens:
        return unresolved("COMPLETE_SYLLABLE_MUST_EQUAL_EXACT_INDEPENDENT_VOWEL_PLUS_CODA_CHUNKS")
    if (
        syllable_analysis.independent_vowels != vowel_analysis.independent_vowels
        or syllable_analysis.base_consonants != coda_analysis.base_consonants
        or syllable_analysis.subscript_consonants != coda_analysis.subscript_consonants
        or syllable_analysis.dependent_vowel_signs
        or syllable_analysis.register_shifters
        or syllable_analysis.shortening_marks
        or syllable_analysis.robat_positions
        or syllable_analysis.ahsda_positions
        or syllable_analysis.toandakhiat_positions
    ):
        return unresolved("SYLLABLE_COMPONENTS_DO_NOT_MATCH_INDEPENDENT_VOWEL_AND_CODA_CHUNKS")

    vowel = resolve_pcgn_independent_vowel(vowel_analysis)
    if vowel.status != "RESOLVED" or vowel.romanization is None:
        return unresolved(vowel.warnings[0])
    final = resolve_pcgn_final_consonant(
        coda_analysis,
        has_following_vowel_character=False,
        has_toandakhiat=False,
    )
    if final.status != "GENERAL_RULE_APPLIED" or final.romanization is None:
        return unresolved(final.warnings[0])

    return PCGNIndependentVowelClosedSyllableAssembly(
        source_text=syllable_analysis.raw_text,
        normalized_text=syllable_analysis.normalized_text,
        vowel_chunk_text=vowel_analysis.raw_text,
        coda_text=coda_analysis.raw_text,
        independent_vowel=vowel.source_character,
        vowel_romanization=vowel.romanization,
        vowel_table_row=vowel.source_table_row,
        coda_romanization=final.romanization,
        coda_table_row=final.base_table_row,
        romanization=vowel.romanization + final.romanization,
        romanization_options=(),
        status="RESOLVED",
        ipa=None,
        ukrainian=None,
        source_locators=PCGN_INDEPENDENT_VOWEL_CLOSED_SYLLABLE_LOCATORS,
        warnings=(
            "CALLER_SUPPLIED_INDEPENDENT_VOWEL_SYLLABLE_AND_FINAL_CODA_BOUNDARIES",
            "PCGN_INDEPENDENT_VOWEL_TABLE_VALUE_AND_GENERIC_FINAL_CONSONANT_RULE_APPLIED",
            "NO_WORD_SEGMENTATION_IPA_OR_UKRAINIAN_OUTPUT",
        ),
    )


PCGN_ANUSVARA_VISARGA_SYLLABLE_LOCATORS = (
    PCGN_CONSONANT_TABLE_LOCATOR,
    PCGN_ANUSVARA_VISARGA_TABLE_LOCATOR,
)


@dataclass(frozen=True)
class PCGNAnusvaraVisargaSyllableAssembly:
    """A caller-segmented syllable using one exact PCGN anusvara/visarga row."""

    source_text: str
    normalized_text: str
    onset_text: str
    series: Literal["â", "ô"] | None
    source_components: tuple[str, ...] | None
    coda_character: str | None
    onset_romanization: str | None
    vowel_coda_romanization: str | None
    romanization: str | None
    source_table_row: int | None
    status: Literal["RESOLVED", "UNRESOLVED"]
    ipa: None
    ukrainian: None
    source_locators: tuple[str, ...]
    warnings: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def assemble_pcgn_anusvara_visarga_syllable(
    onset_analysis: PCGNOrthographicAnalysis,
    syllable_analysis: PCGNOrthographicAnalysis,
    coda_character: str | None = None,
) -> PCGNAnusvaraVisargaSyllableAssembly:
    """Assemble one caller-supplied onset plus an exact PCGN rows 1–8 sequence.

    The caller supplies the onset-only chunk, complete syllable chunk, and
    the explicit final NGA character only for table row 8. Existing consonant
    and anusvara/visarga table resolvers are composed; the table resolver
    validates the exact post-onset token sequence. No segmentation is inferred.
    """
    def unresolved(reason: str) -> PCGNAnusvaraVisargaSyllableAssembly:
        return PCGNAnusvaraVisargaSyllableAssembly(
            source_text=syllable_analysis.raw_text,
            normalized_text=syllable_analysis.normalized_text,
            onset_text=onset_analysis.raw_text,
            series=None,
            source_components=None,
            coda_character=coda_character if coda_character == "ង" else None,
            onset_romanization=None,
            vowel_coda_romanization=None,
            romanization=None,
            source_table_row=None,
            status="UNRESOLVED",
            ipa=None,
            ukrainian=None,
            source_locators=PCGN_ANUSVARA_VISARGA_SYLLABLE_LOCATORS,
            warnings=(reason, "NO_WORD_SEGMENTATION_IPA_OR_UKRAINIAN_OUTPUT"),
        )

    if onset_analysis.status != "STRUCTURE_ONLY" or syllable_analysis.status != "STRUCTURE_ONLY":
        return unresolved("UNSUPPORTED_OR_UNRESOLVED_ORTHOGRAPHIC_COMPONENT")
    onset_tokens = tuple(onset_analysis.tokens)
    syllable_tokens = tuple(syllable_analysis.tokens)
    if not onset_tokens or syllable_tokens[:len(onset_tokens)] != onset_tokens:
        return unresolved("CALLER_ONSET_MUST_MATCH_EXACT_SYLLABLE_TOKEN_PREFIX")

    onset = resolve_pcgn_consonant(onset_analysis)
    series = resolve_pcgn_series(onset_analysis)
    component = resolve_pcgn_anusvara_visarga(
        syllable_analysis,
        onset_analysis,
        coda_character,
    )
    if onset.status != "RESOLVED" or onset.romanization is None:
        return unresolved(onset.warnings[0])
    if series.status != "RESOLVED" or series.series not in {"â", "ô"}:
        return unresolved(series.warnings[0])
    if component.status != "RESOLVED" or component.romanization is None:
        return unresolved(component.warnings[0])

    return PCGNAnusvaraVisargaSyllableAssembly(
        source_text=syllable_analysis.raw_text,
        normalized_text=syllable_analysis.normalized_text,
        onset_text=onset_analysis.raw_text,
        series=series.series,
        source_components=component.source_components,
        coda_character=component.coda_character,
        onset_romanization=onset.romanization,
        vowel_coda_romanization=component.romanization,
        romanization=onset.romanization + component.romanization,
        source_table_row=component.source_table_row,
        status="RESOLVED",
        ipa=None,
        ukrainian=None,
        source_locators=PCGN_ANUSVARA_VISARGA_SYLLABLE_LOCATORS,
        warnings=(
            "CALLER_SUPPLIED_ONSET_AND_COMPLETE_SYLLABLE_BOUNDARIES",
            "PCGN_ANUSVARA_VISARGA_TABLE_ROW_RESOLVED_EXACTLY",
            "ROW_8_NGA_CODA_EXPLICITLY_CALLER_IDENTIFIED" if component.source_table_row == 8 else "NO_EXTRA_CODA_INFERRED",
            "NO_WORD_SEGMENTATION_IPA_OR_UKRAINIAN_OUTPUT",
        ),
    )
