from __future__ import annotations

import csv
from pathlib import Path

from khmer_ua.pcgn import (
    PCGN_DEPENDENT_VOWEL_ROWS,
    analyze_pcgn_orthographic_chunk,
    resolve_pcgn_dependent_vowel,
    resolve_pcgn_series,
)


def resolve(source: str):
    analysis = analyze_pcgn_orthographic_chunk(source)
    return resolve_pcgn_dependent_vowel(analysis, resolve_pcgn_series(analysis))


def test_pcgn_dependent_vowel_series_conditioned_rows():
    cases = (
        ("កា", "a", 2, "â"),
        ("គា", "éa", 2, "ô"),
        ("កិ", "ĕ", 3, "â"),
        ("គិ", "ĭ", 3, "ô"),
        ("កី", "ei", 4, "â"),
        ("គី", "i", 4, "ô"),
        ("កឹ", "œ̆", 5, "â"),
        ("គឹ", "œ̆", 5, "ô"),
        ("កឺ", "œ", 6, "â"),
        ("គឺ", "œ", 6, "ô"),
        ("កុ", "ŏ", 7, "â"),
        ("គុ", "ŭ", 7, "ô"),
        ("កូ", "o", 8, "â"),
        ("គូ", "u", 8, "ô"),
        ("កួ", "uŏ", 9, "â"),
        ("គួ", "uŏ", 9, "ô"),
        ("កេ", "é", 13, "â"),
        ("គេ", "é", 13, "ô"),
        ("កែ", "ê", 14, "â"),
        ("គែ", "ê", 14, "ô"),
        ("កៃ", "ai", 15, "â"),
        ("គៃ", "ey", 15, "ô"),
        ("កេើ", "aeu", 10, "â"),
        ("គេើ", "eu", 10, "ô"),
        ("កេឿ", "œă", 11, "â"),
        ("គេឿ", "œă", 11, "ô"),
        ("កេៀ", "iĕ", 12, "â"),
        ("គេៀ", "iĕ", 12, "ô"),
        ("កេា", "aô", 16, "â"),
        ("គេា", "oŭ", 16, "ô"),
        ("កេៅ", "au", 17, "â"),
        ("គេៅ", "ŏu", 17, "ô"),
    )
    for source, expected, row, series in cases:
        result = resolve(source)
        assert result.status == "RESOLVED", source
        assert result.romanization == expected, source
        assert result.source_table_row == row, source
        assert result.series == series, source
        assert result.ipa is None
        assert result.ukrainian is None
        assert result.source_signs is not None


def test_pcgn_dependent_vowel_uses_note2_series_after_note3_cluster_selection():
    analysis = analyze_pcgn_orthographic_chunk("ថ៊្មា")
    series = resolve_pcgn_series(analysis)
    result = resolve_pcgn_dependent_vowel(analysis, series)

    assert series.series == "ô"
    assert result.status == "RESOLVED"
    assert result.romanization == "éa"
    assert result.source_table_row == 2
    assert result.series == "ô"


def test_pcgn_dependent_vowel_abstains_on_shortening_coda_multiple_signs_and_other_marks():
    cases = ("កា់", "កាំ", "កាត", "កាី", "កា៌", "កា៏", "កើេ")
    for source in cases:
        analysis = analyze_pcgn_orthographic_chunk(source)
        result = resolve_pcgn_dependent_vowel(analysis, resolve_pcgn_series(analysis))
        assert result.status == "UNRESOLVED", source
        assert result.romanization is None, source
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_dependent_vowel_requires_a_resolved_series_and_one_base():
    for source in ("ឥ", "កា៊", "ក្x", "ក្ប្ល"):
        analysis = analyze_pcgn_orthographic_chunk(source)
        result = resolve_pcgn_dependent_vowel(analysis, resolve_pcgn_series(analysis))
        assert result.status == "UNRESOLVED", source
        assert result.romanization is None


def test_pcgn_dependent_vowel_schema_has_explicit_component_only_boundary():
    import json
    from pathlib import Path

    path = Path(__file__).resolve().parents[1] / "schemas/pcgn-dependent-vowel-decision.schema.json"
    schema = json.loads(path.read_text(encoding="utf-8"))
    assert set(schema["required"]) == {
        "source_signs", "series", "romanization", "source_table_row",
        "status", "ipa", "ukrainian", "source_locator", "warnings",
    }
    assert schema["properties"]["ipa"]["const"] is None
    assert schema["properties"]["ukrainian"]["const"] is None
    assert schema["properties"]["source_signs"]["oneOf"][0]["maxItems"] == 2
    assert schema["properties"]["source_signs"]["oneOf"][0]["items"]["enum"] == [
        "ា", "ិ", "ី", "ឹ", "ឺ", "ុ", "ូ", "ួ", "េ", "ើ", "ឿ", "ៀ", "ែ", "ៃ", "ៅ"
    ]
    assert schema["properties"]["source_table_row"]["enum"] == [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, None]


def test_pcgn_ba_aa_shifter_exceptions_feed_the_correct_dependent_vowel_series():
    # Note 2 leaves BA+TRIISAP in the ô-series; Note 3 keeps BA+MUUSIKATOAN
    # in the â-series. Verify that the dependent-vowel adapter consumes those
    # decisions rather than independently re-deriving the base series.
    cases = (
        ("ប៊ា", "ô", "éa", "TRIISAP_NO_SHIFT_BA_EXCEPTION", None),
        (
            "ប៉ា",
            "â",
            "a",
            "BA_MUUSIKATOAN_P_IN_A",
            "BA_WITH_MUUSIKATOAN_P_IN_A_SERIES",
        ),
    )
    for source, series_value, expected, effect, exception in cases:
        analysis = analyze_pcgn_orthographic_chunk(source)
        series = resolve_pcgn_series(analysis)
        vowel = resolve_pcgn_dependent_vowel(analysis, series)

        assert series.status == "RESOLVED", source
        assert series.series == series_value, source
        assert series.shifter_effect == effect, source
        assert series.onset_exception == exception, source
        assert vowel.status == "RESOLVED", source
        assert vowel.series == series_value, source
        assert vowel.source_signs == ("ា",), source
        assert vowel.source_table_row == 2, source
        assert vowel.romanization == expected, source
        assert vowel.ipa is None
        assert vowel.ukrainian is None



def test_pcgn_dependent_vowel_source_registry_matches_all_runtime_rows():
    root = Path(__file__).resolve().parents[1]
    with (root / "data/khmer/romanization_pcgn_dependent_vowels.csv").open(
        encoding="utf-8", newline=""
    ) as stream:
        rows = list(csv.DictReader(stream))

    assert len(rows) == 16
    registry = {}
    for row in rows:
        key = tuple(row["source_signs"].split("+"))
        value = (int(row["table_row"]), row["â_series"], row["ô_series"])
        registry[key] = value
        assert row["source_url"] == "https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf"
        assert row["source_locator"] == "PCGN 1972, Independent/Dependent Vowel Characters table (pp. 2–4)"
        assert row["acceptance_boundary"] == "One exact dependent-vowel pattern and caller-supplied resolved series; component only, no IPA or Ukrainian output"

    assert registry == PCGN_DEPENDENT_VOWEL_ROWS
