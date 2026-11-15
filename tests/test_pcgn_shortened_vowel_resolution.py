from __future__ import annotations

from khmer_ua.pcgn import (
    analyze_pcgn_orthographic_chunk,
    resolve_pcgn_shortened_vowel,
)


def resolve(source: str, onset: str, coda_class: str):
    return resolve_pcgn_shortened_vowel(
        analyze_pcgn_orthographic_chunk(source),
        analyze_pcgn_orthographic_chunk(onset),
        coda_class,
    )


def test_pcgn_note5_inherent_bantoc_row_maps_short_a_and_o_series():
    # The second example is a structural fixture for the ô-series table cell.
    cases = (
        ("បត់", "ប", "other", "â", "á", "INHERENT_BANTOC", 1),
        ("គត់", "គ", "other", "ô", "ó", "INHERENT_BANTOC", 1),
    )
    for source, onset, coda, series, expected, pattern, row in cases:
        result = resolve(source, onset, coda)
        assert result.status == "RESOLVED", source
        assert result.pattern == pattern
        assert result.series == series
        assert result.romanization == expected
        assert result.source_table_row == row
        assert result.shortening_mark == "់"
        assert result.coda_class == coda
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_note5_aa_bantoc_uses_coda_class_for_o_series():
    cases = (
        ("ចាក់", "ច", "k", "â", "ă"),
        ("រ្ពាក់", "រ្ព", "k", "ô", "eă"),
        ("គាង់", "គ", "ng", "ô", "eă"),
        ("គាហ់", "គ", "h", "ô", "eă"),
        ("មាត់", "ម", "other", "ô", "oă"),
    )
    for source, onset, coda, series, expected in cases:
        result = resolve(source, onset, coda)
        assert result.status == "RESOLVED", source
        assert result.pattern == "AA_BANTOC"
        assert result.series == series
        assert result.romanization == expected
        assert result.source_table_row == 2
        assert result.shortening_mark == "់"
        assert result.coda_class == coda
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_note5_samyok_sannya_uses_the_same_shortened_series_and_coda_rule():
    cases = (
        ("ច័ក", "ច", "k", "â", "ă"),
        ("ភ័ព", "ភ", "other", "ô", "oă"),
    )
    for source, onset, coda, series, expected in cases:
        result = resolve(source, onset, coda)
        assert result.status == "RESOLVED", source
        assert result.pattern == "SAMYOK_CODA"
        assert result.series == series
        assert result.romanization == expected
        assert result.source_table_row == 2
        assert result.shortening_mark == "័"
        assert result.coda_class == coda
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_note5_requires_explicit_coda_class_and_matching_onset_prefix():
    cases = (
        ("ចាក់", "ច", None),
        ("ចាក់", "គ", "k"),
        ("ចាក់", "ច", "unknown"),
        ("ចាក់", "ចា", "k"),
    )
    for source, onset, coda in cases:
        result = resolve_pcgn_shortened_vowel(
            analyze_pcgn_orthographic_chunk(source),
            analyze_pcgn_orthographic_chunk(onset),
            coda,
        )
        assert result.status == "UNRESOLVED", (source, onset, coda)
        assert result.romanization is None
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_note5_abstains_on_unlisted_shapes_and_ambiguous_context():
    cases = (
        ("ចិក់", "ច", "k"),       # a vowel sign not listed by Note 5
        ("ច់ក", "ច", "k"),        # BANTOC in the wrong position
        ("ចក់័", "ច", "k"),       # multiple shortening marks
        ("ចាក", "ច", "k"),        # no shortening mark
        ("ចាក់ក", "ច", "k"),      # more than one possible coda consonant
        ("ច័", "ច", "k"),          # no explicit coda consonant
    )
    for source, onset, coda in cases:
        result = resolve(source, onset, coda)
        assert result.status == "UNRESOLVED", source
        assert result.romanization is None
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_note5_schema_keeps_coda_context_explicit_and_outputs_component_only():
    import json
    from pathlib import Path

    path = Path(__file__).resolve().parents[1] / "schemas/pcgn-shortened-vowel-decision.schema.json"
    schema = json.loads(path.read_text(encoding="utf-8"))
    assert set(schema["required"]) == {
        "pattern", "shortening_mark", "series", "coda_character", "coda_class",
        "romanization", "source_table_row", "status", "ipa", "ukrainian",
        "source_locator", "warnings",
    }
    assert schema["properties"]["coda_class"]["enum"] == ["k", "ng", "h", "other", None]
    assert schema["properties"]["ipa"]["const"] is None
    assert schema["properties"]["ukrainian"]["const"] is None
