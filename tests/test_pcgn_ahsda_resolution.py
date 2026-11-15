from __future__ import annotations

from khmer_ua.pcgn import analyze_pcgn_orthographic_chunk, resolve_pcgn_ahsda


def resolve(source: str, position: str | None, series: str | None):
    return resolve_pcgn_ahsda(analyze_pcgn_orthographic_chunk(source), position, series)


def test_pcgn_note7_ahsda_is_not_romanized_in_syllable_initial_position():
    result = resolve("ស៏", "INITIAL", None)
    assert result.status == "RESOLVED"
    assert result.marked_character == "ស"
    assert result.syllable_position == "INITIAL"
    assert result.effect == "MARK_NOT_ROMANIZED_INITIAL"
    assert result.romanization is None
    assert result.ipa is None
    assert result.ukrainian is None


def test_pcgn_note7_final_ahsda_supplies_series_vowel_component():
    cases = (
        ("តំណ៏", "â", "â"),
        ("ពម៏", "ô", "ô"),
    )
    for source, series, expected in cases:
        result = resolve(source, "FINAL", series)
        assert result.status == "RESOLVED", source
        assert result.marked_character in {"ណ", "ម"}
        assert result.syllable_position == "FINAL"
        assert result.series == series
        assert result.effect == "CONSONANT_VOWELLED_FINAL"
        assert result.romanization == expected
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_note7_requires_explicit_syllable_position_and_final_series():
    cases = (
        ("ស៏", None, None),
        ("តំណ៏", "FINAL", None),
        ("តំណ៏", "FINAL", "unknown"),
        ("តំណ៏", "MIDDLE", "â"),
    )
    for source, position, series in cases:
        result = resolve(source, position, series)
        assert result.status == "UNRESOLVED", (source, position, series)
        assert result.romanization is None
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_note7_abstains_on_misplaced_multiple_or_nonconsonant_ahsda():
    for source in ("ស", "ស៏ស", "ស៏៏", "កា៏"):
        result = resolve(source, "INITIAL", None)
        assert result.status == "UNRESOLVED", source
        assert result.romanization is None
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_note7_schema_preserves_position_and_series_context():
    import json
    from pathlib import Path

    path = Path(__file__).resolve().parents[1] / "schemas/pcgn-ahsda-decision.schema.json"
    schema = json.loads(path.read_text(encoding="utf-8"))
    assert set(schema["required"]) == {
        "marked_character", "syllable_position", "series", "effect",
        "romanization", "status", "ipa", "ukrainian", "source_locator", "warnings",
    }
    assert schema["properties"]["ipa"]["const"] is None
    assert schema["properties"]["ukrainian"]["const"] is None
