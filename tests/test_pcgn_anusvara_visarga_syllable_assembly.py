from __future__ import annotations

import json
from pathlib import Path

from khmer_ua.pcgn import analyze_pcgn_orthographic_chunk, assemble_pcgn_anusvara_visarga_syllable


def assemble(source: str, coda: str | None = None):
    onset = analyze_pcgn_orthographic_chunk(source[0])
    full = analyze_pcgn_orthographic_chunk(source)
    return assemble_pcgn_anusvara_visarga_syllable(onset, full, coda)


def test_pcgn_anusvara_visarga_assembler_covers_all_eight_table_rows_in_both_series():
    cases = (
        ("កុំ", None, "kom", 1, "â"),
        ("គុំ", None, "kŭm", 1, "ô"),
        ("កំ", None, "kâm", 2, "â"),
        ("គំ", None, "kum", 2, "ô"),
        ("កាំ", None, "kăm", 3, "â"),
        ("គាំ", None, "kŏâm", 3, "ô"),
        ("កះ", None, "kăh", 4, "â"),
        ("គះ", None, "keăh", 4, "ô"),
        ("កុះ", None, "kŏh", 5, "â"),
        ("គុះ", None, "kŭh", 5, "ô"),
        ("កេះ", None, "kéh", 6, "â"),
        ("គេះ", None, "kéh", 6, "ô"),
        ("កោះ", None, "kaôh", 7, "â"),
        ("គោះ", None, "kŏăh", 7, "ô"),
        ("កាំង", "ង", "kăng", 8, "â"),
        ("គាំង", "ង", "keăng", 8, "ô"),
    )
    for source, coda, expected, row, series in cases:
        result = assemble(source, coda)
        assert result.status == "RESOLVED", source
        assert result.romanization == expected, source
        assert result.source_table_row == row, source
        assert result.series == series, source
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_anusvara_visarga_assembler_requires_explicit_row8_nga_and_matching_onset():
    assert assemble("កាំង").status == "UNRESOLVED"
    assert assemble("កាំង", "ន").status == "UNRESOLVED"
    wrong = assemble_pcgn_anusvara_visarga_syllable(
        analyze_pcgn_orthographic_chunk("គ"),
        analyze_pcgn_orthographic_chunk("កុំ"),
    )
    assert wrong.status == "UNRESOLVED"
    assert wrong.romanization is None


def test_pcgn_anusvara_visarga_assembler_abstains_on_unlisted_or_malformed_chunks():
    for source in ("កាំះ", "កេាះ", "កំង", "កុះ់", "កា", "កុំក"):
        result = assemble(source, "ង" if source == "កំង" else None)
        assert result.status == "UNRESOLVED", source
        assert result.romanization is None
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_anusvara_visarga_assembler_schema_is_orthographic_only():
    path = Path(__file__).resolve().parents[1] / "schemas/pcgn-anusvara-visarga-syllable-assembly.schema.json"
    schema = json.loads(path.read_text(encoding="utf-8"))
    assert set(schema["required"]) == {
        "source_text", "normalized_text", "onset_text", "series", "source_components",
        "coda_character", "onset_romanization", "vowel_coda_romanization", "romanization",
        "source_table_row", "status", "ipa", "ukrainian", "source_locators", "warnings",
    }
    assert schema["properties"]["ipa"]["const"] is None
    assert schema["properties"]["ukrainian"]["const"] is None
    assert schema["properties"]["source_table_row"]["enum"] == [1, 2, 3, 4, 5, 6, 7, 8, None]
