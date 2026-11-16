from __future__ import annotations

import json
from pathlib import Path

from khmer_ua.pcgn import assemble_pcgn_open_syllable, analyze_pcgn_orthographic_chunk


def assemble(onset: str, syllable: str):
    return assemble_pcgn_open_syllable(
        analyze_pcgn_orthographic_chunk(onset),
        analyze_pcgn_orthographic_chunk(syllable),
    )


def test_pcgn_open_syllable_assembles_source_located_cv_components():
    cases = (
        ("ក", "កា", "ka", "â", 2),
        ("គ", "គា", "kéa", "ô", 2),
        ("ថ្ម", "ថ្មា", "thma", "â", 2),
    )
    for onset, syllable, expected, series, vowel_row in cases:
        result = assemble(onset, syllable)
        assert result.status == "RESOLVED", syllable
        assert result.romanization == expected, syllable
        assert result.series == series, syllable
        assert result.vowel_table_row == vowel_row
        assert result.romanization == result.onset_romanization + result.vowel_romanization
        assert result.ipa is None
        assert result.ukrainian is None
        assert "CALLER_SUPPLIED_ONSET_AND_OPEN_SYLLABLE_BOUNDARIES" in result.warnings


def test_pcgn_open_syllable_uses_series_after_note2_note3_cluster_selection():
    result = assemble("ថ៊្ម", "ថ៊្មា")
    assert result.status == "RESOLVED"
    assert result.series == "ô"
    assert result.romanization == "thméa"


def test_pcgn_open_syllable_rejects_onset_that_does_not_match_exact_prefix():
    result = assemble("ក", "គា")
    assert result.status == "UNRESOLVED"
    assert result.romanization is None
    assert "CALLER_ONSET_MUST_MATCH_EXACT_SYLLABLE_TOKEN_PREFIX" in result.warnings


def test_pcgn_open_syllable_abstains_on_coda_shortening_and_special_marks():
    for onset, syllable in (
        ("ក", "កាត"), ("ក", "កា់"), ("ក", "កា៌"),
        ("ក", "កា៏"), ("ក", "កា៍"), ("ក", "កាំ"),
    ):
        result = assemble(onset, syllable)
        assert result.status == "UNRESOLVED", syllable
        assert result.romanization is None, syllable
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_open_syllable_abstains_on_alif_and_multiple_or_unmodeled_onsets():
    for onset, syllable in (("អ", "អា"), ("ក្ប្ល", "ក្ប្លា"), ("ក្x", "ក្xា")):
        result = assemble(onset, syllable)
        assert result.status == "UNRESOLVED", syllable
        assert result.romanization is None


def test_pcgn_open_syllable_schema_preserves_orthographic_only_boundary():
    schema_path = Path(__file__).resolve().parents[1] / "schemas/pcgn-syllable-assembly.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    assert set(schema["required"]) == {
        "source_text", "normalized_text", "onset_text", "series",
        "onset_romanization", "vowel_romanization", "romanization",
        "onset_base", "onset_subscript", "onset_table_rows",
        "vowel_table_row", "status", "ipa", "ukrainian",
        "source_locators", "warnings",
    }
    assert schema["properties"]["ipa"]["const"] is None
    assert schema["properties"]["ukrainian"]["const"] is None
    assert schema["properties"]["romanization"]["type"] == ["string", "null"]
