"""Typed, provenance-aware IPA values for the Khmer → Ukrainian pipeline.

IPA parsing is source-notation work and does not consult the Ukrainian
correspondence table. The target adapter is a separate consumer of this model.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import unicodedata
from typing import Iterable

RESULT_STATUSES = frozenset({"SUPPORTED", "UNCERTAIN", "PROVISIONAL", "UNRESOLVED"})
_MODIFIERS = frozenset({"ˈ", "ˌ", "ː", "ˑ"})
_TONE_MARKS = frozenset("˥˦˧˨˩")
_BOUNDARIES = frozenset({" ", "\t", "\n", ".", "·", "‧"})
_TIE_BARS = frozenset({"͡", "͜"})


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


def _is_ipa_base(character: str) -> bool:
    category = unicodedata.category(character)
    name = unicodedata.name(character, "")
    return category.startswith("L") and any(
        marker in name for marker in ("LATIN", "GREEK", "CLICK")
    )


def _is_modifier_letter(character: str) -> bool:
    return (
        unicodedata.category(character) == "Lm"
        and "MODIFIER LETTER" in unicodedata.name(character, "")
    )


def _segment_kind(symbol: str) -> str:
    if symbol in _TONE_MARKS:
        return "tone"
    if symbol in _MODIFIERS:
        return "modifier"
    if symbol in _BOUNDARIES:
        return "boundary"
    base = symbol[0] if symbol else ""
    if base in "aeiouɑɒæɛɜəɨɪɔɵœɐɤɯʊʌʏʉ":
        return "vowel"
    return "consonant"


def _tokenize_ipa(ipa: str, provenance: tuple[str, ...], certainty: str):
    segments: list[PhoneticSegment] = []
    unsupported: list[str] = []
    index = 0
    while index < len(ipa):
        character = ipa[index]
        if character in _BOUNDARIES or character in _MODIFIERS or character in _TONE_MARKS:
            segments.append(PhoneticSegment(character, _segment_kind(character), provenance, certainty))
            index += 1
            continue
        if not _is_ipa_base(character):
            unsupported.append(character)
            segments.append(PhoneticSegment(character, "unknown", provenance, "UNRESOLVED"))
            index += 1
            continue

        token = character
        index += 1
        while index < len(ipa) and unicodedata.category(ipa[index]).startswith("M") and ipa[index] not in _TIE_BARS:
            token += ipa[index]
            index += 1
        if index < len(ipa) and ipa[index] in _TIE_BARS:
            token += ipa[index]
            index += 1
            if index < len(ipa) and _is_ipa_base(ipa[index]):
                token += ipa[index]
                index += 1
                while index < len(ipa) and unicodedata.category(ipa[index]).startswith("M") and ipa[index] not in _TIE_BARS:
                    token += ipa[index]
                    index += 1
            else:
                unsupported.append(token)
        while index < len(ipa) and _is_modifier_letter(ipa[index]) and ipa[index] not in _TONE_MARKS and ipa[index] not in _MODIFIERS:
            token += ipa[index]
            index += 1
        segments.append(PhoneticSegment(token, _segment_kind(token), provenance, certainty))
    return tuple(segments), tuple(unsupported)


def _syllable_boundaries(segments: tuple[PhoneticSegment, ...]) -> tuple[int, ...]:
    boundaries = [0]
    for index, segment in enumerate(segments):
        if segment.kind == "boundary":
            if index not in boundaries:
                boundaries.append(index)
            if index + 1 not in boundaries:
                boundaries.append(index + 1)
    if len(segments) not in boundaries:
        boundaries.append(len(segments))
    return tuple(boundaries)


def from_ipa(
    ipa: str,
    *,
    status: str = "SUPPORTED",
    provenance: tuple[str, ...] = (),
    uncertainty: tuple[str, ...] = (),
) -> TypedPhoneticResult:
    """Parse supplied IPA symbols without consulting target correspondences."""
    if status not in {"SUPPORTED", "UNCERTAIN"}:
        raise ValueError(f"unsupported complete IPA status: {status}")
    if not isinstance(ipa, str) or not ipa.strip():
        return from_unknown_source_unit(
            "?",
            provenance=provenance,
            uncertainty=(*uncertainty, "EMPTY-IPA-RESULT"),
        )
    raw = ipa.strip()
    if len(raw) >= 2 and (raw[0], raw[-1]) in {("/", "/"), ("[", "]")}:
        raw = raw[1:-1]
    segments, unsupported = _tokenize_ipa(raw, provenance, status)
    if unsupported:
        return TypedPhoneticResult(
            phonemic_ipa=None,
            segments=segments,
            syllable_boundaries=_syllable_boundaries(segments),
            status="UNRESOLVED",
            provenance=provenance,
            uncertainty=tuple(dict.fromkeys((*uncertainty, "UNSUPPORTED-IPA-NOTATION"))),
        )
    return TypedPhoneticResult(
        phonemic_ipa=raw,
        segments=segments,
        syllable_boundaries=_syllable_boundaries(segments),
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
    append_unknown_tail: bool = True,
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
            return hint
        raw = hint.phonemic_ipa
        segments.extend(
            replace(segment, certainty="PROVISIONAL")
            for segment in hint.segments
        )
    # A contiguous unresolved tail is one uncertainty region, not one marker
    # per Khmer code point. The original graphemes remain on the source trace.
    unresolved_values = tuple(unresolved_graphemes)
    if append_unknown_tail or unresolved_values or not segments:
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
