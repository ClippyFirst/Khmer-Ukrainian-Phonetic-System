from __future__ import annotations

import csv
import json
from pathlib import Path

from khmer_ua.pcgn import (
    PCGN_INHERENT_VOWEL_TABLE_LOCATOR,
    analyze_pcgn_orthographic_chunk,
    resolve_pcgn_inherent_vowel,
)


def test_pcgn_inherent_vowel_maps_nonfinal_onsets_by_resolved_series():
    cases = (
        ("ក", "â"),
        ("គ", "ô"),
        ("ក្", None),
        ("ក្ម", "ô"),
        ("គ៊", None),
    )
    for source, expected in cases:
        result = resolve_pcgn_inherent_vowel(
            analyze_pcgn_orthographic_chunk(source), "NON_FINAL"
        )
        if expected is None:
            assert result.status == "UNRESOLVED", source
            assert result.romanization is None
        else:
            assert result.status == "RESOLVED", source
            assert result.series == expected
            assert result.romanization == expected
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_inherent_vowel_abstains_for_final_consonants_and_explicit_vowels():
    for source in ("ក", "គ", "កា", "កេ", "ក៍"):
        result = resolve_pcgn_inherent_vowel(
            analyze_pcgn_orthographic_chunk(source), "FINAL"
        )
        assert result.status == "UNRESOLVED"
        assert result.romanization is None

    for source in ("កា", "កេ", "ឥ", "ក្x", "កា់"):
        result = resolve_pcgn_inherent_vowel(
            analyze_pcgn_orthographic_chunk(source), "NON_FINAL"
        )
        assert result.status == "UNRESOLVED"
        assert result.romanization is None


def test_pcgn_inherent_vowel_schema_and_source_registry_are_bounded():
    root = Path(__file__).resolve().parents[1]
    schema = json.loads(
        (root / "schemas/pcgn-inherent-vowel-decision.schema.json").read_text(encoding="utf-8")
    )
    assert set(schema["required"]) == {
        "syllable_position", "series", "romanization", "source_table_row",
        "status", "ipa", "ukrainian", "source_locator", "warnings",
    }
    assert schema["properties"]["source_table_row"]["const"] == 1
    assert schema["properties"]["ipa"]["type"] == "null"
    assert schema["properties"]["ukrainian"]["type"] == "null"
    assert schema["properties"]["source_locator"]["const"] == PCGN_INHERENT_VOWEL_TABLE_LOCATOR

    with (root / "data/khmer/romanization_pcgn_inherent_vowel.csv").open(
        encoding="utf-8", newline=""
    ) as stream:
        rows = list(csv.DictReader(stream))
    assert rows == [{
        "table_row": "1",
        "source_symbol": "◌",
        "â_series": "â",
        "ô_series": "ô",
        "source_locator": PCGN_INHERENT_VOWEL_TABLE_LOCATOR,
        "acceptance_boundary": "Non-final onset only; final consonant without vowel sign or TOANDAKHIAT abstains",
    }]
