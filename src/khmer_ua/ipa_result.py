"""Typed, provenance-aware IPA values for the Khmer → Ukrainian pipeline.

This is deliberately separate from the public result-envelope dataclasses in
phonetic_result.py. A TypedPhoneticResult represents the IPA adapter boundary;
it never reads Khmer graphemes and never promotes a provisional segment.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

RESULT_STATUSES = frozenset({"SUPPORTED", "UNCERTAIN", "PROVISIONAL", "UNRESOLVED"})
_MODIFIERS = frozenset({"ˈ", "ˌ", "ː", "ˑ"})
_BOUNDARIES = frozenset({" ", "\t", "\n", ".", "·", "‧"})


@dataclass(frozen=True)
class PhoneticSegment:
    ipa: str
    kind: str
    provenance: tuple[str, ...] = ()
    certainty: str = "SUPPORTED"


@dataclass(frozen=True)
class TypedPhoneticResult:
    phonemic_ipa: str | None
    segments: tuple[PhoneticSegment, ...]
    syllable_boundaries: tuple[int, ...] = (0,)
    vowel_length: str | None = None
    tone_category: str | None = None
    tone_contour_ipa: str | None = None
    status: str = "SUPPORTED"
    provenance: tuple[str, ...] = ()
    uncertainty: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        return {
            "phonemic_ipa": self.phonemic_ipa,
            "segments": [asdict(segment) for segment in self.segments],
            "syllable_boundaries": list(self.syllable_boundaries),
            "vowel_length": self.vowel_length,
            "tone_category": self.tone_category,
            "tone_contour_ipa": self.tone_contour_ipa,
            "status": self.status,
            "provenance": list(self.provenance),
            "uncertainty": list(self.uncertainty),
        }


def _ipa_symbols() -> tuple[str, ...]:
    # The correspondence inventory is used only to tokenize supplied IPA.
    # It is never used to infer a source-language pronunciation.
    from .practical import POLICY

    symbols = set(POLICY.get("segments", {}))
    symbols.update(POLICY.get("sequences", {}))
    return tuple(sorted((symbol for symbol in symbols if symbol), key=len, reverse=True))


def _strip_outer_delimiters(ipa: str) -> str:
    value = ipa.strip()
    if len(value) >= 2 and (value[0], value[-1]) in {("/", "/"), ("[", "]")}:
        return value[1:-1]
    return value


def _segment_kind(symbol: str) -> str:
    if symbol in _MODIFIERS:
        return "modifier"
    if symbol in _BOUNDARIES:
        return "boundary"
    base = symbol[0] if symbol else ""
    if base in "aeiouɑɒæɛɜəɨɪɔɵœɐɤɯʊʌʏʉ":
        return "vowel"
    return "consonant"


def _tokenize_ipa(ipa: str, provenance: tuple[str, ...], certainty: str):
    symbols = _ipa_symbols()
    segments: list[PhoneticSegment] = []
    unsupported: list[str] = []
    index = 0
    while index < len(ipa):
        char = ipa[index]
        if char in _BOUNDARIES or char in _MODIFIERS:
            segments.append(PhoneticSegment(char, _segment_kind(char), provenance, certainty))
            index += 1
            continue
        match = next((symbol for symbol in symbols if ipa.startswith(symbol, index)), None)
        if match is None:
            unsupported.append(char)
            segments.append(PhoneticSegment(char, "unknown", provenance, "UNRESOLVED"))
            index += 1
            continue
        segments.append(PhoneticSegment(match, _segment_kind(match), provenance, certainty))
        index += len(match)
    return tuple(segments), tuple(unsupported)


def from_ipa(
    ipa: str,
    *,
    status: str = "SUPPORTED",
    provenance: tuple[str, ...] = (),
    uncertainty: tuple[str, ...] = (),
) -> TypedPhoneticResult:
    """Tokenize an already supplied IPA string without inventing any phones."""
    if status not in RESULT_STATUSES - {"PROVISIONAL", "UNRESOLVED"}:
        raise ValueError(f"unsupported complete IPA status: {status}")
    if not isinstance(ipa, str) or not ipa.strip():
        return from_unknown_source_unit(
            "?", provenance=provenance,
            uncertainty=(*uncertainty, "EMPTY-IPA-RESULT"),
        )
    raw = _strip_outer_delimiters(ipa)
    segments, unsupported = _tokenize_ipa(raw, provenance, status)
    if unsupported:
        return TypedPhoneticResult(
            phonemic_ipa=None,
            segments=segments,
            syllable_boundaries=(0, len(segments)),
            status="UNRESOLVED",
            provenance=provenance,
            uncertainty=tuple(dict.fromkeys((*uncertainty, "UNSUPPORTED-IPA-SEGMENT"))),
        )
    return TypedPhoneticResult(
        phonemic_ipa=raw,
        segments=segments,
        syllable_boundaries=(0, len(segments)),
        vowel_length="long" if "ː" in raw else None,
        tone_category=None,
        tone_contour_ipa=None,
        status=status,
        provenance=provenance,
        uncertainty=uncertainty,
    )


def from_provisional_ipa(
    ipa_hint: str | None,
    *,
    unresolved_graphemes: Iterable[str] = (),
    provenance: tuple[str, ...] = (),
    uncertainty: tuple[str, ...] = (),
) -> TypedPhoneticResult:
    """Build provisional IPA + one explicit unknown region from registered hints."""
    segments: list[PhoneticSegment] = []
    raw = None
    if ipa_hint:
        hint = from_ipa(
            ipa_hint,
            status="UNCERTAIN",
            provenance=provenance,
            uncertainty=uncertainty,
        )
        if hint.status == "UNRESOLVED":
            return TypedPhoneticResult(
                None, hint.segments, hint.syllable_boundaries,
                status="UNRESOLVED", provenance=provenance,
                uncertainty=tuple(dict.fromkeys((*uncertainty, *hint.uncertainty))),
            )
        raw = hint.phonemic_ipa
        segments.extend(
            PhoneticSegment(segment.ipa, segment.kind, segment.provenance, "PROVISIONAL")
            for segment in hint.segments
        )
    # One contiguous unresolved tail is one uncertainty region, not one marker
    # per Khmer code point. The original graphemes remain on the source trace.
    if tuple(unresolved_graphemes) or not segments:
        segments.append(PhoneticSegment("?", "unknown", provenance, "PROVISIONAL"))
    if not segments:
        segments.append(PhoneticSegment("?", "unknown", provenance, "PROVISIONAL"))
    notes = tuple(dict.fromkeys((*uncertainty, "PHONETIC-READING-PROVISIONAL")))
    return TypedPhoneticResult(
        phonemic_ipa=None,
        segments=tuple(segments),
        syllable_boundaries=(0, len(segments)),
        vowel_length=None,
        tone_category=None,
        tone_contour_ipa=None,
        status="PROVISIONAL" if raw else "UNRESOLVED",
        provenance=provenance,
        uncertainty=notes,
    )


def from_unknown_source_unit(
    surface: str,
    *,
    provenance: tuple[str, ...] = (),
    uncertainty: tuple[str, ...] = (),
) -> TypedPhoneticResult:
    """Represent an unresolved source unit without fabricating an IPA phone."""
    if not surface:
        raise ValueError("An unknown source unit must not be empty")
    trace = tuple(dict.fromkeys((*provenance, "FALLBACK:UNKNOWN-SOURCE-UNIT")))
    return TypedPhoneticResult(
        phonemic_ipa=None,
        segments=(PhoneticSegment("?", "unknown", trace, "UNRESOLVED"),),
        syllable_boundaries=(0, 1),
        status="UNRESOLVED",
        provenance=trace,
        uncertainty=tuple(dict.fromkeys((*uncertainty, "PHONETIC-READING-UNKNOWN"))),
    )
