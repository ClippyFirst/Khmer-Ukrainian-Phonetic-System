"""Evidence-register contract for provisional Khmer onset hints.

This validates provenance and parity with the existing inventory only; it does
not validate pronunciation accuracy or promote hints to canonical IPA.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "khmer"
REGISTRY = ROOT / "data" / "khmer-positional-onset-evidence.json"
SCHEMA = ROOT / "schemas" / "khmer-positional-onset-evidence.schema.json"


def test_registry_has_explicit_non_promotion_contract():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    assert registry["schema"] == "khmer-positional-onset-evidence/v1"
    assert registry["registry_status"] == "PARTIAL_SPECIALIST_REFERENCE_REGISTER"
    assert registry["promotion_policy"]["allowed"] == "PROVISIONAL_ONSET_PREVIEW_ONLY"
    prohibited = " ".join(registry["promotion_policy"]["prohibited"]).lower()
    assert "canonical ipa" in prohibited
    assert "accuracy" in prohibited
    assert "tone" in prohibited


def test_entries_match_existing_consonant_onset_inventory_exactly():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    consonants = json.loads((DATA / "consonants.json").read_text(encoding="utf-8"))
    by_char = {item["char"]: item for item in consonants}
    entries = registry["entries"]
    assert len(entries) == len(by_char) == 33
    assert len({item["entry_id"] for item in entries}) == len(entries)
    assert {item["grapheme"] for item in entries} == set(by_char)

    for entry in entries:
        char = entry["grapheme"]
        inventory = by_char[char]
        codepoint = f"U+{ord(char):04X}"
        assert entry["unicode_codepoint"] == codepoint
        assert entry["entry_id"] == f"ONSET-{ord(char):04X}"
        assert entry["position"] == "onset"
        assert entry["ipa_hint"] == inventory["onset_ipa"]
        assert entry["fallback_rule_id"] == "KHMER-PREVIEW-ONSET-IPA-V1"
        assert entry["allowed_use"] == "PROVISIONAL_ONSET_PREVIEW_ONLY"
        assert entry["review_status"] == "NOT_INDEPENDENTLY_REVIEWED"
        assert entry["profile_status"] == "NOT_ADJUDICATED_FOR_PROJECT_PPH_PROFILE"
        assert entry["limitations"]
        assert all("coda" in note.lower() or "cluster" in note.lower() or "gold" in note.lower() or "promote" in note.lower() or "tone" in note.lower() or "vowel" in note.lower() for note in entry["limitations"])
        assert entry["evidence"]
        for evidence in entry["evidence"]:
            assert evidence["source_id"] == "r12a-orthography"
            assert evidence["source_kind"] == "SPECIALIST_REFERENCE"
            assert codepoint in evidence["source_locator"]
            assert "Basic consonants" in evidence["source_locator"]
            assert evidence["scope"]


def test_registry_source_and_schema_are_consistent():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    sources = json.loads((DATA / "sources.json").read_text(encoding="utf-8"))
    source_ids = {item["id"] for item in sources}
    declared = {item["source_id"] for item in registry["sources"]}
    assert declared == {"r12a-orthography"}
    assert declared <= source_ids
    source = next(item for item in registry["sources"] if item["source_id"] == "r12a-orthography")
    assert source["primary_source"] is False
    assert source["source_kind"] == "SPECIALIST_REFERENCE"
    assert source["url"].startswith("https://")
    assert schema["$defs"]["entry"]["properties"]["position"]["const"] == "onset"
    assert schema["$defs"]["entry"]["properties"]["allowed_use"]["const"] == "PROVISIONAL_ONSET_PREVIEW_ONLY"
    assert schema["$defs"]["entry"]["properties"]["review_status"]["enum"] == [
        "NOT_INDEPENDENTLY_REVIEWED", "INDEPENDENTLY_REVIEWED"
    ]


def test_registry_cannot_be_misread_as_complete_positional_coverage():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    assert "not adjudicated" in registry["profile_scope"].lower()
    assert registry["registry_status"].startswith("PARTIAL")
    assert any("Primary phonetic evidence" in item for item in registry["promotion_policy"].values() if isinstance(item, str))
    assert all(item["position"] == "onset" for item in registry["entries"])
