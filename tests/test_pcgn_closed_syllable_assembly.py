from __future__ import annotations

import json
from pathlib import Path

from khmer_ua.pcgn import (
    assemble_pcgn_shortened_closed_syllable,
    analyze_pcgn_orthographic_chunk,
)


def assemble(onset: str, syllable: str, coda: str, coda_class: str):
    return assemble_pcgn_shortened_closed_syllable(
        analyze_pcgn_orthographic_chunk(onset),
        analyze_pcgn_orthographic_chunk(syllable),
        analyze_pcgn_orthographic_chunk(coda),
        coda_class,
    )


def test_pcgn_note5_closed_syllable_assembles_all_supported_patterns():
    cases = (
        ("ច", "ចាក់", "ក", "k", "chăk", "AA_BANTOC", "â"),
        ("រ្ព", "រ្ពាក់", "ក", "k", "rpeăk", "AA_BANTOC", "ô"),
        ("គ", "គាង់", "ង", "ng", "keăng", "AA_BANTOC", "ô"),
        ("គ", "គាហ់", "ហ", "h", "keăh", "AA_BANTOC", "ô"),
        ("ម", "មាត់", "ត", "other", "moăt", "AA_BANTOC", "ô"),
        ("ប", "បត់", "ត", "other", "bát", "INHERENT_BANTOC", "â"),
        ("គ", "គត់", "ត", "other", "kót", "INHERENT_BANTOC", "ô"),
        ("ច", "ច័ក", "ក", "k", "chăk", "SAMYOK_CODA", "â"),
        ("ភ", "ភ័ព", "ព", "other", "phoăp", "SAMYOK_CODA", "ô"),
    )
    for onset, syllable, coda, coda_class, expected, pattern, series in cases:
        result = assemble(onset, syllable, coda, coda_class)
        assert result.status == "RESOLVED", syllable
        assert result.romanization == expected, syllable
        assert result.pattern == pattern, syllable
        assert result.series == series, syllable
        assert result.coda_class == coda_class
        assert result.romanization == (
            result.onset_romanization + result.vowel_romanization + result.coda_romanization
        )
        assert result.ipa is None
        assert result.ukrainian is None
        assert "CODA_CLASS_CROSS_CHECKED_AGAINST_PCGN_CONSONANT_ROMANIZATION" in result.warnings


def test_pcgn_note5_closed_syllable_cross_checks_explicit_coda_class_and_character():
    assert assemble("ច", "ចាក់", "ក", "other").status == "UNRESOLVED"
    assert assemble("ច", "ចាក់", "ង", "ng").status == "UNRESOLVED"
    assert assemble("ច", "ចាក់", "ក", "k").status == "RESOLVED"


def test_pcgn_note5_closed_syllable_rejects_mismatched_boundaries_and_unsupported_codas():
    for onset, syllable, coda, coda_class in (
        ("គ", "ចាក់", "ក", "k"),
        ("ច", "ចាក់", "ត", "other"),
        ("ច", "ចាប់", "ប", "other"),
        ("ច", "ចាក់", "អ", "other"),
        ("ច", "ចាក់", "ក្x", "k"),
        ("ច", "ចាក់ក", "ក", "k"),
        ("ច", "ចាក", "ក", "k"),
        ("ច", "ចិក់", "ក", "k"),
        ("ច", "ចក់័", "ក", "k"),
    ):
        result = assemble(onset, syllable, coda, coda_class)
        assert result.status == "UNRESOLVED", (onset, syllable, coda, coda_class)
        assert result.romanization is None
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_closed_syllable_schema_preserves_orthographic_only_boundary():
    schema_path = Path(__file__).resolve().parents[1] / "schemas/pcgn-closed-syllable-assembly.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    assert set(schema["required"]) == {
        "source_text", "normalized_text", "onset_text", "coda_text", "series",
        "pattern", "shortening_mark", "coda_class", "onset_romanization",
        "vowel_romanization", "coda_romanization", "romanization",
        "onset_table_rows", "vowel_table_row", "coda_table_row", "status",
        "ipa", "ukrainian", "source_locators", "warnings",
    }
    assert schema["properties"]["ipa"]["const"] is None
    assert schema["properties"]["ukrainian"]["const"] is None
    assert schema["properties"]["coda_class"]["enum"] == ["k", "ng", "h", "other", None]
