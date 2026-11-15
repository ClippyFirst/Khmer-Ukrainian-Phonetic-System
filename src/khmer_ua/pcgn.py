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



# PCGN Note 3 defines the weak set explicitly; do not add UNGEGN-only members.
PCGN_WEAK_SUBSCRIPTS = frozenset("ងញណនមយរលវ")


@dataclass(frozen=True)
class PCGNSeriesDecision:
    series: Literal["â", "ô"] | None
    basis: Literal["BASE", "SUBSCRIPT", "UNRESOLVED"]
    status: Literal["RESOLVED", "UNRESOLVED"]
    onset_exception: Literal["BA_WITH_FOOT_P_IN_A_SERIES"] | None
    source_locator: str
    warnings: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def resolve_pcgn_series(
    analysis: PCGNOrthographicAnalysis,
) -> PCGNSeriesDecision:
    """Apply only the explicit PCGN Note 3 base/foot series-selection rule.

    This does not apply Note 2 shifters or infer syllable boundaries/codas.
    Any shifter, ambiguous multi-foot shape, unsupported token or non-single
    base remains unresolved. The weak-foot set is exactly the PCGN set.
    """
    def unresolved(reason: str) -> PCGNSeriesDecision:
        return PCGNSeriesDecision(
            series=None,
            basis="UNRESOLVED",
            status="UNRESOLVED",
            onset_exception=None,
            source_locator="PCGN 1972, Note 3 (pp. 2–3)",
            warnings=(reason, "NO_VOWEL_OR_ROMANIZATION_OUTPUT"),
        )

    if analysis.status != "STRUCTURE_ONLY":
        return unresolved("UNSUPPORTED_OR_UNRESOLVED_ORTHOGRAPHIC_COMPONENT")
    if analysis.register_shifters:
        return unresolved("REGISTER_SHIFTER_PRESENT_NOTE_2_NOT_IMPLEMENTED")
    if len(analysis.base_consonants) != 1:
        return unresolved("EXACTLY_ONE_BASE_CONSONANT_REQUIRED")
    if len(analysis.subscript_consonants) > 1:
        return unresolved("MULTIPLE_SUBSCRIPTS_REQUIRE_READING_ADJUDICATION")

    base = analysis.base_consonants[0]
    base_register = CONSONANTS_BY_CHAR[base].get("register")
    if base_register not in {"first", "second"}:
        return unresolved("BASE_ORTHOGRAPHIC_REGISTER_UNAVAILABLE")

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
            # PCGN Note 3: ប with a foot is romanized p in the â series.
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

    series: Literal["â", "ô"] = "â" if register == "first" else "ô"
    warnings = ["PCGN_NOTE_3_SERIES_SELECTION_ONLY"]
    if exception:
        warnings.append("PCGN_NOTE_3_BA_WITH_FOOT_P_EXCEPTION")
    return PCGNSeriesDecision(
        series=series,
        basis=basis,
        status="RESOLVED",
        onset_exception=exception,
        source_locator="PCGN 1972, Note 3 (pp. 2–3)",
        warnings=tuple(warnings),
    )


__all__ = [
    "PCGNOrthographicAnalysis",
    "PCGNToken",
    "PCGNSeriesDecision",
    "PCGN_WEAK_SUBSCRIPTS",
    "resolve_pcgn_series",
    "analyze_pcgn_orthographic_chunk",
]
