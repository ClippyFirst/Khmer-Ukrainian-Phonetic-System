from __future__ import annotations

import csv
import json
from pathlib import Path

from khmer_ua.pcgn import (
    PCGN_FINAL_CONSONANT_TABLE_LOCATOR,
    analyze_pcgn_orthographic_chunk,
    resolve_pcgn_final_consonant,
)


def resolve(source: str, *, has_vowel: bool = False, has_toandakhiat: bool = False):
    return resolve_pcgn_final_consonant(
        analyze_pcgn_orthographic_chunk(source),
        has_following_vowel_character=has_vowel,
        has_toandakhiat=has_toandakhiat,
    )


def test_pcgn_final_consonant_general_rule_maps_consonant_without_following_vowel():
    cases = (
        ("ក", "k", 1),
        ("ខ", "kh", 2),
        ("ង", "ng", 3),
        ("ច", "ch", 4),
        ("ញ", "nh", 6),
        ("ត", "t", 11),
        ("ព", "p", 13),
        ("ម", "m", 15),
        ("រ", "r", 17),
        ("ល", "l", 18),
        ("ស", "s", 20),
        ("ហ", "h", 21),
        ("ក្គ", "kk", 1),
    )
    for source, expected, row in cases:
        result = resolve(source)
        assert result.status == "GENERAL_RULE_APPLIED", source
        assert result.romanization == expected, source
        assert result.base_table_row == row, source
        assert result.following_vowel == ""
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_final_consonant_requires_no_vowel_character_or_toandakhiat():
    assert resolve("ក", has_vowel=True).status == "UNRESOLVED"
    assert resolve("ក", has_toandakhiat=True).status == "UNRESOLVED"
    assert resolve("កា").status == "UNRESOLVED"
    assert resolve("ក៍").status == "UNRESOLVED"


def test_pcgn_final_consonant_abstains_on_ba_alif_and_unsupported_clusters():
    for source in ("ប", "ប្ក", "ក្ប", "អ", "ក្x", "ក្ប្ល"):
        result = resolve(source)
        assert result.status == "UNRESOLVED", source
        assert result.romanization is None
        assert result.following_vowel is None


def test_pcgn_final_consonant_schema_and_rule_registry():
    root = Path(__file__).resolve().parents[1]
    schema = json.loads(
        (root / "schemas/pcgn-final-consonant-decision.schema.json").read_text(encoding="utf-8")
    )
    assert set(schema["required"]) == {
        "base_character", "base_table_row", "base_romanization",
        "subscript_character", "subscript_table_row", "subscript_romanization",
        "romanization", "following_vowel", "status", "ipa", "ukrainian",
        "source_locator", "warnings",
    }
    assert schema["properties"]["ipa"]["type"] == "null"
    assert schema["properties"]["ukrainian"]["type"] == "null"
    assert schema["properties"]["source_locator"]["const"] == PCGN_FINAL_CONSONANT_TABLE_LOCATOR

    with (root / "data/khmer/romanization_pcgn_final_consonant.csv").open(
        encoding="utf-8", newline=""
    ) as stream:
        rows = list(csv.DictReader(stream))
    assert rows == [{
        "rule_id": "PCGN_FINAL_NO_FOLLOWING_VOWEL",
        "source_condition": "Syllable-final consonant not accompanied by a vowel character or TOANDAKHIAT",
        "romanization_effect": "Consonant table component followed by no vowel letter",
        "source_locator": PCGN_FINAL_CONSONANT_TABLE_LOCATOR,
        "acceptance_boundary": "General rule only; caller supplies final position and absence of vowel/TOANDAKHIAT; BA and ALIF abstain",
    }]
