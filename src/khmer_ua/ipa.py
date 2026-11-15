"""Conservative IPA boundary for the selected Khmer pronunciation profile.

This module validates notation and metadata supplied by another component. It
does not infer pronunciation, repair malformed output, or promote candidates
to the deterministic engine's published result.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import unicodedata
from typing import Sequence

PROFILES = {"khmer-pph-careful-citation-v1"}
IPA_KINDS = {"PHONEMIC", "PHONETIC_BROAD", "PHONETIC_NARROW"}
CANDIDATE_STATUSES = {"COMPLETE", "PARTIAL"}

# IPA uses a small set of structural symbols in addition to segment letters.
# Brackets/slashes are accepted only as balanced outer delimiters.
_IPA_SYMBOLS = set("ˈˌːˑ˥˦˧˨˩͜͡‿.·|/-[]")
_IPA_DIGITS = set("0123456789")


class IPACandidateStatus(str, Enum):
    COMPLETE = "COMPLETE"
    PARTIAL = "PARTIAL"


@dataclass(frozen=True)
class IPACandidate:
    """Validated, non-authoritative candidate with provenance and uncertainty."""

    raw_output: str
    ipa: str
    profile: str
    kind: str
    status: IPACandidateStatus
    provider: str
    uncertainty: tuple[str, ...]


def _is_ipa_segment_letter(character: str) -> bool:
    category = unicodedata.category(character)
    name = unicodedata.name(character, "")
    return category.startswith("L") and category != "Lm" and (
        "LATIN" in name or "GREEK" in name
    )


def _is_ipa_modifier_letter(character: str) -> bool:
    return (
        unicodedata.category(character) == "Lm"
        and "MODIFIER LETTER" in unicodedata.name(character, "")
    )


def _validate_ipa_notation(ipa: str) -> None:
    if not ipa or not ipa.strip():
        raise ValueError("candidate IPA must be a non-empty string")
    if ipa != ipa.strip():
        raise ValueError("candidate IPA must not have leading or trailing whitespace")
    if unicodedata.normalize("NFC", ipa) != ipa:
        raise ValueError("candidate IPA must be NFC-normalized; output is never silently rewritten")

    delimiters = [character for character in ipa if character in "/[]"]
    if delimiters and (
        len(ipa) < 2
        or (ipa[0], ipa[-1]) not in {("/", "/"), ("[", "]")}
        or any(character in "/[]" for character in ipa[1:-1])
    ):
        raise ValueError("candidate IPA has unbalanced or misplaced outer delimiters")

    has_segment = False
    previous_was_base = False
    for index, character in enumerate(ipa):
        category = unicodedata.category(character)
        if character in "/[]":
            continue
        if _is_ipa_segment_letter(character):
            has_segment = True
            previous_was_base = True
            continue
        if _is_ipa_modifier_letter(character):
            # Stress, length, tone and segment modifiers do not themselves
            # count as segment letters and do not rewrite the source string.
            continue
        if category.startswith("M"):
            if not previous_was_base:
                raise ValueError(f"orphan combining mark at IPA offset {index}")
            # A tie bar joins the preceding segment to the following one.
            previous_was_base = character in {"͡", "͜"}
            continue
        if character in _IPA_DIGITS:
            previous_was_base = False
            continue
        if character.isspace():
            previous_was_base = False
            continue
        if character in _IPA_SYMBOLS:
            if character in {"͡", "͜"} and not previous_was_base:
                raise ValueError(f"orphan IPA tie bar at offset {index}")
            previous_was_base = character in {"͡", "͜"}
            continue
        # IPA click letters are symbols rather than Unicode letters.
        if character in "ʘǀǃǂǁ":
            has_segment = True
            previous_was_base = True
            continue
        raise ValueError(
            f"unsupported non-IPA character U+{ord(character):04X} at IPA offset {index}"
        )

    if not has_segment:
        raise ValueError("candidate IPA must contain at least one IPA segment letter")


def validate_ipa_candidate(
    raw_output: str,
    *,
    profile: str,
    kind: str,
    status: str,
    provider: str,
    uncertainty: Sequence[str] = (),
) -> IPACandidate:
    """Validate a provider candidate without rewriting or promoting its output.

    raw_output is retained exactly as supplied and also used as the IPA value
    after syntax validation. PARTIAL candidates must explain their
    uncertainty; COMPLETE is a provider assertion, not a gold label.
    """
    if not isinstance(profile, str) or profile not in PROFILES:
        raise ValueError(f"unsupported pronunciation profile: {profile}")
    if not isinstance(kind, str) or kind not in IPA_KINDS:
        raise ValueError(f"unsupported IPA kind: {kind}")
    if not isinstance(status, str) or status not in CANDIDATE_STATUSES:
        raise ValueError(f"unsupported candidate status: {status}")
    if not isinstance(provider, str) or not provider.strip():
        raise ValueError("candidate provider must be a non-empty string")
    if isinstance(uncertainty, (str, bytes)) or not isinstance(uncertainty, Sequence):
        raise ValueError("candidate uncertainty must be a sequence of non-empty strings")
    notes = tuple(uncertainty)
    if any(not isinstance(note, str) or not note.strip() for note in notes):
        raise ValueError("candidate uncertainty must contain only non-empty strings")
    if status == "PARTIAL" and not notes:
        raise ValueError("PARTIAL candidate must include at least one uncertainty note")
    if not isinstance(raw_output, str):
        raise ValueError("candidate IPA must be a string")

    _validate_ipa_notation(raw_output)
    return IPACandidate(
        raw_output=raw_output,
        ipa=raw_output,
        profile=profile,
        kind=kind,
        status=IPACandidateStatus(status),
        provider=provider,
        uncertainty=notes,
    )


def render_ipa_profile(ipa: str, profile: str = "khmer-pph-careful-citation-v1") -> str:
    """Validate the selected profile and preserve supplied IPA unchanged."""
    if profile not in PROFILES:
        raise ValueError(f"unsupported pronunciation profile: {profile}")
    return ipa
