from __future__ import annotations

from khmer_ua.pcgn import (
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
        ("គិ", "ĕ", 3, "ô"),
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
    )
    for source, expected, row, series in cases:
        result = resolve(source)
        assert result.status == "RESOLVED", source
        assert result.romanization == expected, source
        assert result.source_table_row == row, source
        assert result.series == series, source
        assert result.ipa is None
        assert result.ukrainian is None


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
    cases = ("កា់", "កាំ", "កាត", "កាី", "កា៌", "កា៏")
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
        "source_sign", "series", "romanization", "source_table_row",
        "status", "ipa", "ukrainian", "source_locator", "warnings",
    }
    assert schema["properties"]["ipa"]["const"] is None
    assert schema["properties"]["ukrainian"]["const"] is None
    assert schema["properties"]["source_table_row"]["enum"] == [2, 3, 4, 5, 6, 7, 8, 9, 13, 14, 15, None]
