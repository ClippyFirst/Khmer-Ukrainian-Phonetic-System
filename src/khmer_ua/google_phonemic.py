"""Google Khmer phonemic token parsing and evidence-gated IPA adaptation.

The Google source notation is not IPA. This module keeps it as a distinct
intermediate representation and converts only through the pinned token map.
"""
from __future__ import annotations

import hashlib
import json
import unicodedata
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from .ipa import validate_ipa_candidate
from .ipa_result import TypedPhoneticResult, from_provisional_full_ipa

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MAP_PATH = ROOT / "data" / "khmer" / "google-phonemic-to-ipa.json"
DEFAULT_TSV_PATH = ROOT / "data" / "khmer" / "google-pronunciation-full.tsv"
DEFAULT_INVENTORY_PATH = ROOT / "data" / "khmer" / "google-phonology.json"
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

@dataclass(frozen=True)
class GooglePhonemicSourceRow:
    word: str
    source_phonemic: str
    source_row: int
    source_label: str | None = None


@dataclass(frozen=True)
class GooglePhonemicLexicalCandidate:
    word: str
    source_phonemic: str
    source_row: int
    source_label: str | None
    parsed: GooglePhonemicResult


@dataclass(frozen=True)
class GooglePhonemicLexicon:
    entries: dict[str, tuple[GooglePhonemicSourceRow, ...]]
    unresolved_rows: tuple[GooglePhonemicSourceRow, ...]
    manifest: dict[str, Any]
    mapping: dict[str, Any]

    def lookup(self, word: str) -> tuple[GooglePhonemicLexicalCandidate, ...]:
        normalized = unicodedata.normalize("NFC", word.strip())
        rows = self.entries.get(normalized, ())
        return tuple(
            GooglePhonemicLexicalCandidate(
                word=row.word,
                source_phonemic=row.source_phonemic,
                source_row=row.source_row,
                source_label=row.source_label,
                parsed=parse_google_phonemic(row.source_phonemic, self.mapping),
            )
            for row in rows
        )


def _contains_khmer(value: str) -> bool:
    return any("\u1780" <= character <= "\u17ff" for character in value)


@lru_cache(maxsize=1)
def load_google_phonemic_lexicon(
    path: str | Path | None = None,
    *,
    verify_hash: bool = True,
) -> GooglePhonemicLexicon:
    """Load the pinned source lexicon without silently resolving variants."""
    source_path = Path(path) if path is not None else DEFAULT_TSV_PATH
    raw_bytes = source_path.read_bytes()
    mapping = load_google_phone_map()
    expected_hash = mapping.get("source", {}).get("source_tsv_sha256")
    actual_hash = hashlib.sha256(raw_bytes).hexdigest()
    if verify_hash and expected_hash and actual_hash != expected_hash:
        raise ValueError(
            f"Google Khmer source TSV hash mismatch: expected {expected_hash}, got {actual_hash}"
        )

    inventory = json.loads(DEFAULT_INVENTORY_PATH.read_text(encoding="utf-8"))
    inventory_tokens = {row[0] for row in inventory.get("phones", [])}
    mapping_tokens = set(mapping["tokens"])
    if mapping_tokens != inventory_tokens:
        raise ValueError("Google phonemic IPA map does not match pinned phonology inventory")

    entries: dict[str, list[GooglePhonemicSourceRow]] = {}
    unresolved_rows: list[GooglePhonemicSourceRow] = []
    observed_tokens: set[str] = set()
    source_rows = 0
    nonempty_rows = 0
    for source_row, line in enumerate(raw_bytes.decode("utf-8").splitlines(), start=1):
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) < 2:
            continue
        word = unicodedata.normalize("NFC", fields[0].strip())
        if not word or not _contains_khmer(word):
            continue
        source_rows += 1
        phonemic = fields[1].strip()
        label = fields[2].strip() if len(fields) > 2 and fields[2].strip() else None
        if not phonemic:
            unresolved_rows.append(GooglePhonemicSourceRow(word, "", source_row, label))
            continue
        nonempty_rows += 1
        row = GooglePhonemicSourceRow(word, phonemic, source_row, label)
        entries.setdefault(word, []).append(row)
        observed_tokens.update(token for token in phonemic.split() if token != ".")

    if observed_tokens != mapping_tokens - {"sil", "pau"}:
        missing = sorted(observed_tokens - mapping_tokens)
        unused = sorted((mapping_tokens - {"sil", "pau"}) - observed_tokens)
        raise ValueError(
            f"Google phonemic token inventory drift: unmapped={missing}, unused={unused}"
        )

    frozen_entries = {word: tuple(rows) for word, rows in sorted(entries.items())}
    multi_variant_words = sum(1 for rows in frozen_entries.values() if len(rows) > 1)
    manifest = {
        "source_id": mapping["source"]["id"],
        "source_revision": mapping["source"]["source_revision"],
        "license": mapping["source"]["license"],
        "source_tsv_sha256": actual_hash,
        "source_rows": source_rows,
        "nonempty_pronunciation_rows": nonempty_rows,
        "empty_pronunciation_rows": len(unresolved_rows),
        "unique_spellings_with_pronunciation": len(frozen_entries),
        "multi_pronunciation_words": multi_variant_words,
        "observed_phone_tokens": len(observed_tokens),
        "inventory_phone_tokens": len(inventory_tokens),
        "ipa_gold_count": 0,
        "candidate_status": "PROVISIONAL",
    }
    return GooglePhonemicLexicon(
        entries=frozen_entries,
        unresolved_rows=tuple(unresolved_rows),
        manifest=manifest,
        mapping=mapping,
    )

