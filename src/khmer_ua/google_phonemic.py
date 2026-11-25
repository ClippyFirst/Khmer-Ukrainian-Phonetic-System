"""Google Khmer phonemic token parsing and evidence-gated IPA adaptation.

The Google source notation is not IPA. This module keeps it as a distinct
intermediate representation and converts only through the pinned token map.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .ipa import validate_ipa_candidate
from .ipa_result import TypedPhoneticResult, from_provisional_full_ipa

DEFAULT_MAP_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "khmer"
    / "google-phonemic-to-ipa.json"
)
DEFAULT_PROFILE = "khmer-pph-careful-citation-v1"
PROVIDER = "google-khmer-pronunciation-lexicon"


@dataclass(frozen=True)
class GooglePhonemicResult:
    raw: str
    source_tokens: tuple[str, ...]
    ipa: str | None
    ipa_kind: str
    status: str
    mapping_status: str
    provenance: tuple[str, ...]
    uncertainty: tuple[str, ...]
    syllable_boundaries: tuple[int, ...]
    candidate: TypedPhoneticResult | None = None


def load_google_phone_map(path: str | Path | None = None) -> dict[str, Any]:
    """Load and minimally validate the pinned Google phone-to-IPA map."""
    map_path = Path(path) if path is not None else DEFAULT_MAP_PATH
    data = json.loads(map_path.read_text(encoding="utf-8"))
    if data.get("schema_version") != "google-phonemic-to-ipa/v1":
        raise ValueError("unsupported Google phonemic-to-IPA map schema")
    tokens = data.get("tokens")
    if not isinstance(tokens, dict) or not tokens:
        raise ValueError("Google phonemic-to-IPA map has no token inventory")
    for token, entry in tokens.items():
        if not isinstance(token, str) or not token or not isinstance(entry, dict):
            raise ValueError("invalid Google phone mapping entry")
        if "ipa" not in entry or not isinstance(entry.get("mapping_status"), str):
            raise ValueError(f"incomplete Google phone mapping for {token!r}")
    return data


def _unresolved(
    raw: str,
    tokens: tuple[str, ...],
    uncertainty: tuple[str, ...],
    *,
    provenance: tuple[str, ...] = (),
    boundaries: tuple[int, ...] = (),
) -> GooglePhonemicResult:
    return GooglePhonemicResult(
        raw=raw,
        source_tokens=tokens,
        ipa=None,
        ipa_kind="UNRESOLVED",
        status="UNRESOLVED",
        mapping_status="UNRESOLVED",
        provenance=provenance,
        uncertainty=uncertainty,
        syllable_boundaries=boundaries,
        candidate=None,
    )


def parse_google_phonemic(
    raw: str,
    mapping: dict[str, Any] | None = None,
    *,
    profile: str = DEFAULT_PROFILE,
    provider: str = PROVIDER,
) -> GooglePhonemicResult:
    """Convert a Google source phonemic string to typed, provisional IPA.

    Spaces delimit source phone tokens. A standalone dot marks a syllable
    boundary. Unknown, silence, pause, malformed-boundary, or unmapped tokens
    fail closed rather than being guessed.
    """
    phone_map = mapping if mapping is not None else load_google_phone_map()
    provenance = (
        f"GOOGLE_SOURCE:{phone_map.get('source', {}).get('id', 'unregistered')}",
        f"GOOGLE_PHONOLOGY:{phone_map.get('source', {}).get('source_revision', 'unversioned')}",
        f"IPA_MAP:{phone_map.get('map_version', 'unversioned')}",
    )
    if not isinstance(raw, str) or not raw.strip():
        return _unresolved(raw if isinstance(raw, str) else "", (), ("EMPTY_SOURCE_PHONEMIC",), provenance=provenance)

    tokens = tuple(raw.strip().split())
    if not tokens or tokens[0] == "." or tokens[-1] == ".":
        return _unresolved(raw, tokens, ("MALFORMED_SYLLABLE_BOUNDARY",), provenance=provenance)

    ipa_parts: list[str] = []
    uncertainty = ["TARGET_PROFILE_EQUIVALENCE_UNVERIFIED"]
    boundaries = [0]
    phone_index = 0
    previous_was_boundary = False
    used_mapping_statuses: list[str] = []

    for token in tokens:
        if token == ".":
            if previous_was_boundary or phone_index == boundaries[-1]:
                return _unresolved(raw, tokens, ("MALFORMED_SYLLABLE_BOUNDARY",), provenance=provenance)
            ipa_parts.append(".")
            boundaries.append(phone_index)
            previous_was_boundary = True
            continue

        entry = phone_map["tokens"].get(token)
        if entry is None:
            return _unresolved(
                raw,
                tokens,
                (f"UNMAPPED_GOOGLE_PHONE:{token}",),
                provenance=provenance,
                boundaries=tuple(boundaries),
            )
        ipa_value = entry.get("ipa")
        mapping_status = entry.get("mapping_status", "UNRESOLVED")
        if not isinstance(ipa_value, str) or not ipa_value:
            return _unresolved(
                raw,
                tokens,
                (f"NON_LEXICAL_GOOGLE_PHONE:{token}",),
                provenance=provenance,
                boundaries=tuple(boundaries),
            )
        ipa_parts.append(ipa_value)
        phone_index += 1
        previous_was_boundary = False
        used_mapping_statuses.append(mapping_status)
        if mapping_status != "SOURCE_CORROBORATED":
            uncertainty.append(f"UNVERIFIED_PHONE_MAPPING:{token}")

    if not used_mapping_statuses or previous_was_boundary:
        return _unresolved(raw, tokens, ("EMPTY_OR_TRAILING_SYLLABLE",), provenance=provenance)

    ipa = "".join(ipa_parts)
    try:
        validate_ipa_candidate(
            ipa,
            profile=profile,
            kind="PHONEMIC",
            status="COMPLETE",
            provider=provider,
            uncertainty=tuple(dict.fromkeys(uncertainty)),
        )
        candidate = from_provisional_full_ipa(
            ipa,
            kind="PHONEMIC",
            profile=profile,
            provenance=provenance,
            uncertainty=tuple(dict.fromkeys(uncertainty)),
        )
        if candidate.status == "UNRESOLVED":
            return _unresolved(raw, tokens, ("INVALID_MAPPED_IPA",), provenance=provenance)
    except ValueError as exc:
        return _unresolved(raw, tokens, (f"INVALID_MAPPED_IPA:{exc}",), provenance=provenance)

    if boundaries[-1] != phone_index:
        boundaries.append(phone_index)
    mapping_status = (
        "SOURCE_CORROBORATED"
        if all(status == "SOURCE_CORROBORATED" for status in used_mapping_statuses)
        else "PROVISIONAL"
    )
    return GooglePhonemicResult(
        raw=raw,
        source_tokens=tokens,
        ipa=ipa,
        ipa_kind="PHONEMIC",
        status="PROVISIONAL",
        mapping_status=mapping_status,
        provenance=provenance,
        uncertainty=tuple(dict.fromkeys(uncertainty)),
        syllable_boundaries=tuple(boundaries),
        candidate=candidate,
    )
