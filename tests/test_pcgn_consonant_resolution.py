from __future__ import annotations

import csv
import json
from pathlib import Path

from khmer_ua.pcgn import (
    PCGN_CONSONANT_ROMANIZATION_ROWS,
    PCGN_CONSONANT_TABLE_LOCATOR,
    analyze_pcgn_orthographic_chunk,
    resolve_pcgn_consonant,
)


def resolve(source: str):
    return resolve_pcgn_consonant(analyze_pcgn_orthographic_chunk(source))


def test_pcgn_consonant_table_rows_1_to_21_map_all_supported_base_characters():
    expected = {
        "ក": (1, "k"), "គ": (1, "k"),
        "ខ": (2, "kh"), "ឃ": (2, "kh"),
        "ង": (3, "ng"),
        "ច": (4, "ch"), "ជ": (4, "ch"),
        "ឆ": (5, "chh"), "ឈ": (5, "chh"),
        "ញ": (6, "nh"),
        "ដ": (7, "d"), "ឌ": (7, "d"),
        "ឋ": (8, "th"), "ឍ": (8, "th"),
        "ថ": (9, "th"), "ធ": (9, "th"),
        "ណ": (10, "n"), "ន": (10, "n"),
        "ត": (11, "t"), "ទ": (11, "t"),
        "ប": (12, "b"),
        "ព": (13, "p"),
        "ផ": (14, "ph"), "ភ": (14, "ph"),
        "ម": (15, "m"),
        "យ": (16, "y"),
        "រ": (17, "r"),
        "ឡ": (18, "l"), "ល": (18, "l"),
        "វ": (19, "v"),
        "ស": (20, "s"),
        "ហ": (21, "h"),
    }
    assert PCGN_CONSONANT_ROMANIZATION_ROWS == expected
    for source, (row, romanization) in expected.items():
        result = resolve(source)
        assert result.status == "RESOLVED", source
        assert result.base_table_row == row, source
        assert result.base_romanization == romanization, source
        assert result.romanization == romanization, source
        assert result.series in {"â", "ô"}
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_consonant_clusters_map_base_then_one_foot():
    cases = (
        ("ក្គ", "k", "k", "kk", 1, 1),
        ("ក្ប", "k", "p", "kp", 1, 12),
        ("ប្ក", "p", "k", "pk", 12, 1),
    )
    for source, base, foot, joined, base_row, foot_row in cases:
        result = resolve(source)
        assert result.status == "RESOLVED", source
        assert result.base_romanization == base, source
        assert result.subscript_romanization == foot, source
        assert result.romanization == joined, source
        assert result.base_table_row == base_row, source
        assert result.subscript_table_row == foot_row, source


def test_pcgn_ba_b_p_alternation_uses_note3_exceptions():
    cases = (
        ("ប", "b", None),
        ("ប៉", "p", "BA_WITH_MUUSIKATOAN_P_IN_A_SERIES"),
        ("ប៊", "b", None),
        ("ប្ក", "p", "BA_WITH_FOOT_P_IN_A_SERIES"),
    )
    for source, expected, exception in cases:
        result = resolve(source)
        assert result.status == "RESOLVED", source
        assert result.base_romanization == expected, source
        assert result.onset_exception == exception, source


def test_pcgn_consonant_resolver_delegates_alif_and_rejects_unsupported_context():
    alif = resolve("អ")
    assert alif.status == "UNRESOLVED"
    assert alif.romanization is None
    assert "NOTE_4_GLOTTAL_ONSET" in alif.warnings[0]

    for source in ("កា", "ក្x", "ក្ប្ល", "ក៉"):
        result = resolve(source)
        assert result.status == "UNRESOLVED", source
        assert result.romanization is None


def test_pcgn_consonant_schema_and_csv_match_the_official_table():
    root = Path(__file__).resolve().parents[1]
    schema = json.loads(
        (root / "schemas/pcgn-consonant-decision.schema.json").read_text(encoding="utf-8")
    )
    assert set(schema["required"]) == {
        "base_character", "base_table_row", "base_romanization",
        "subscript_character", "subscript_table_row", "subscript_romanization",
        "series", "onset_exception", "romanization", "status", "ipa",
        "ukrainian", "source_locator", "warnings",
    }
    assert schema["properties"]["ipa"]["type"] == "null"
    assert schema["properties"]["ukrainian"]["type"] == "null"
    assert schema["properties"]["source_locator"]["const"] == PCGN_CONSONANT_TABLE_LOCATOR

    with (root / "data/khmer/romanization_pcgn_consonants.csv").open(
        encoding="utf-8", newline=""
    ) as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 22
    for row in rows[:21]:
        row_number = int(row["table_row"])
        base_chars = row["base_characters"].split("|")
        for char in base_chars:
            assert PCGN_CONSONANT_ROMANIZATION_ROWS[char][0] == row_number
            assert PCGN_CONSONANT_ROMANIZATION_ROWS[char][1] == row["romanization"]
    assert rows[21]["table_row"] == "22"
    assert rows[21]["implementation"] == "DELEGATED_NOTE_4"
