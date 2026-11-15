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
INDEPENDENT_VOWELS = {
    item["char"] for item in SIGNS if item.get("kind") == "independent_vowel"
}


@dataclass(frozen=True)
class PCGNToken:
    text: str
    kind: str
    codepoints: tuple[str, ...]
    name: str | None = None


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

    def token(value: str, kind: str, name: str | None = None) -> None:
        tokens.append(
            PCGNToken(
                text=value,
                kind=kind,
                codepoints=tuple(f"U+{ord(ch):04X}" for ch in value),
                name=name,
            )
        )

    while i < len(chars):
        ch = chars[i]
        if ch == COENG:
            if i + 1 < len(chars) and chars[i + 1] in CONSONANTS_BY_CHAR:
                subscript = chars[i + 1]
                subscripts.append(subscript)
                token(COENG + subscript, "subscript_consonant", CONSONANTS_BY_CHAR[subscript]["name"])
                i += 2
                continue
            token(ch, "malformed_coeng", "COENG")
            unresolved.append(ch)
            i += 1
            continue

        consonant = CONSONANTS_BY_CHAR.get(ch)
        if consonant:
            bases.append(ch)
            token(ch, "unstacked_consonant", consonant["name"])
            i += 1
            continue

        sign = SIGNS_BY_CHAR.get(ch)
        if sign:
            name = SPECIAL_MARKS.get(ch, sign.get("name"))
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
        warnings.append("REGISTER_SHIFTER_EFFECT_REQUIRES_PCgn_NOTE_2_CONTEXT")
    if shortening:
        warnings.append("SHORTENING_REQUIRES_PCgn_NOTE_5_PATTERN_SERIES_AND_CODA")
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
        coda_decision="UNRESOLVED",
        romanization=None,
        ipa=None,
        ukrainian=None,
        status="UNSUPPORTED" if unresolved else "STRUCTURE_ONLY",
        warnings=tuple(warnings),
        sources=("unicode17-ch16", "pcgn-1972-notes-2-8", PCGN_GUIDE),
    )


__all__ = [
    "PCGNOrthographicAnalysis",
    "PCGNToken",
    "analyze_pcgn_orthographic_chunk",
]
