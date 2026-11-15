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
_IPA_SYMBOLS = set("ˈˌːˑ͜͡‿.·|/-[]")
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


def _is_ipa_letter(character: str) -> bool:
    category = unicodedata.category(character)
    name = unicodedata.name(character, "")
    if not category.startswith("L"):
        return False
    # IPA segment inventories are based on Latin and Greek letters, including
    # IPA extensions and modifier letters. Other scripts are not guessed.
    return "LATIN" in name or "GREEK" in name or "MODIFIER LETTER" in name


def _validate_ipa_notation(ipa: str) -> None:
    if not ipa or not ipa.strip():
        raise ValueError("candidate IPA must be a non-empty string")
    if ipa != ipa.strip():
        raise ValueError("candidate IPA must not have leading or trailing whitespace")
    if unicodedata.normalize("NFC", ipa) != ipa:
        raise ValueError("candidate IPA must be NFC-normalized; output is never silently rewritten")

    has_letter = False
    previous_was_base = False
    for index, character in enumerate(ipa):
        category = unicodedata.category(character)
        if _is_ipa_letter(character):
            has_letter = True
            previous_was_base = True
            continue
        if category.startswith("M"):
            if not previous_was_base:
                raise ValueError(f"orphan combining mark at IPA offset {index}")
            # A tie bar is itself a combining mark; it still joins the
            # preceding segment to the following segment.
            previous_was_base = character in {"͡", "͜"}
            continue
        if character in _IPA_DIGITS or character in _IPA_SYMBOLS or character.isspace():
            if character in "/[]":
                continue
            if character not in {"ˈ", "ˌ", "ː", "ˑ", "͡", "͜", "‿", ".", "·", "|", "-", "/"} and not character.isspace():
                previous_was_base = False
            continue
        raise ValueError(
            f"unsupported non-IPA character U+{ord(character):04X} at IPA offset {index}"
        )

    if not has_letter:
        raise ValueError("candidate IPA must contain at least one IPA segment letter")

    if (ipa.startswith("/") != ipa.endswith("/")) or (ipa.startswith("[") != ipa.endswith("]")):
        raise ValueError("candidate IPA has unbalanced outer delimiters")


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
    if profile not in PROFILES:
        raise ValueError(f"unsupported pronunciation profile: {profile}")
    if kind not in IPA_KINDS:
        raise ValueError(f"unsupported IPA kind: {kind}")
    if status not in CANDIDATE_STATUSES:
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
