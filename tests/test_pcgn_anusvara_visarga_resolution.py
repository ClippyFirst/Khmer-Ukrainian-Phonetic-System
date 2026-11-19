from __future__ import annotations

import csv
import json
from pathlib import Path

from khmer_ua.pcgn import (
    PCGN_ANUSVARA_VISARGA_ROWS,
    PCGN_ANUSVARA_VISARGA_TABLE_LOCATOR,
    analyze_pcgn_orthographic_chunk,
    resolve_pcgn_anusvara_visarga,
)


def resolve(source: str, coda_character: str | None = None):
    onset = analyze_pcgn_orthographic_chunk(source[0])
    full = analyze_pcgn_orthographic_chunk(source)
    return resolve_pcgn_anusvara_visarga(full, onset, coda_character)


def test_pcgn_anusvara_visarga_table_rows_are_series_conditioned():
    cases = (
        ("កុំ", "om", 1, "â", None),
        ("គុំ", "ŭm", 1, "ô", None),
        ("កំ", "âm", 2, "â", None),
        ("គំ", "um", 2, "ô", None),
        ("កាំ", "ăm", 3, "â", None),
        ("គាំ", "ŏâm", 3, "ô", None),
        ("កះ", "ăh", 4, "â", None),
        ("គះ", "eăh", 4, "ô", None),
        ("កុះ", "ŏh", 5, "â", None),
        ("គុះ", "ŭh", 5, "ô", None),
        ("កេះ", "éh", 6, "â", None),
        ("គេះ", "éh", 6, "ô", None),
        ("កេាះ", "aôh", 7, "â", None),
        ("គេាះ", "ŏăh", 7, "ô", None),
        ("កាំង", "ăng", 8, "â", "ង"),
        ("គាំង", "eăng", 8, "ô", "ង"),
    )
    for source, expected, row, series, coda in cases:
        result = resolve(source, coda)
        assert result.status == "RESOLVED", source
        assert result.romanization == expected, source
        assert result.source_table_row == row, source
        assert result.series == series, source
        assert result.coda_character == coda, source
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_anusvara_visarga_row_8_requires_explicit_nga_coda():
    assert resolve("កាំង").status == "UNRESOLVED"
    assert resolve("កាំង", "ង").status == "RESOLVED"
    assert resolve("កាំង", "ន").status == "UNRESOLVED"
    assert resolve("កាំ", "ង").status == "UNRESOLVED"


def test_pcgn_anusvara_visarga_requires_matching_onset_and_rejects_unlisted_patterns():
    full = analyze_pcgn_orthographic_chunk("កុំ")
    wrong_onset = analyze_pcgn_orthographic_chunk("គ")
    result = resolve_pcgn_anusvara_visarga(full, wrong_onset)
    assert result.status == "UNRESOLVED"
    assert result.romanization is None

    for source in ("កាំះ", "កោះ", "កំង", "កុះ់", "កា"):
        result = resolve(source)
        assert result.status == "UNRESOLVED", source
        assert result.romanization is None


def test_pcgn_anusvara_visarga_schema_and_csv_match_the_eight_source_rows():
    root = Path(__file__).resolve().parents[1]
    schema = json.loads(
        (root / "schemas/pcgn-anusvara-visarga-decision.schema.json").read_text(encoding="utf-8")
    )
    assert set(schema["required"]) == {
        "source_components", "series", "coda_character", "romanization",
        "source_table_row", "status", "ipa", "ukrainian", "source_locator", "warnings",
    }
    assert schema["properties"]["ipa"]["type"] == "null"
    assert schema["properties"]["ukrainian"]["type"] == "null"
    assert schema["properties"]["source_locator"]["const"] == PCGN_ANUSVARA_VISARGA_TABLE_LOCATOR

    with (root / "data/khmer/romanization_pcgn_anusvara_visarga.csv").open(
        encoding="utf-8", newline=""
    ) as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 8
    for row in rows:
        key = tuple(row["source_components"].split("+"))
        row_number, a_value, o_value = PCGN_ANUSVARA_VISARGA_ROWS[key]
        assert row_number == int(row["table_row"])
        assert a_value == row["â_series"]
        assert o_value == row["ô_series"]
