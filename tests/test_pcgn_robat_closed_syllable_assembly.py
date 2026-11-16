from __future__ import annotations

import json
from pathlib import Path

from khmer_ua.pcgn import analyze_pcgn_orthographic_chunk, assemble_pcgn_robat_closed_syllable


def assemble(onset: str, vowel: str, syllable: str, coda: str, marked_coda: str):
    return assemble_pcgn_robat_closed_syllable(
        analyze_pcgn_orthographic_chunk(onset),
        analyze_pcgn_orthographic_chunk(vowel),
        analyze_pcgn_orthographic_chunk(syllable),
        analyze_pcgn_orthographic_chunk(coda),
        analyze_pcgn_orthographic_chunk(marked_coda),
    )


def test_pcgn_note6_official_example_assembles_complete_syllable():
    result = assemble("ធ", "ធ", "ធម៌", "ម៌", "ម")
    assert result.status == "RESOLVED"
    assert result.series == "ô"
    assert result.onset_romanization == "th"
    assert result.vowel_romanization == "ô"
    assert result.marked_coda_consonant_romanization == "m"
    assert result.coda_romanization == "rm"
    assert result.romanization == "thôrm"
    assert result.ipa is None
    assert result.ukrainian is None


def test_pcgn_note6_assembles_normal_dependent_vowel_before_robat_coda():
    result = assemble("ក", "កា", "កាម៌", "ម៌", "ម")
    assert result.status == "RESOLVED"
    assert result.series == "â"
    assert result.vowel_romanization == "a"
    assert result.coda_romanization == "rm"
    assert result.romanization == "karm"


def test_pcgn_note6_requires_exact_caller_supplied_boundaries():
    cases = (
        ("ធ", "ធ", "ធម៌", "ម៌", "ក"),
        ("ធ", "ធ", "ធម", "ម៌", "ម"),
        ("ធ", "ធ", "ធម៌ក", "ម៌", "ម"),
        ("ធ", "ធា", "ធម៌", "ម៌", "ម"),
        ("ធ", "ធ", "ធម៌៌", "ម៌៌", "ម"),
        ("ធ", "ធ", "ធម៌", "ម", "ម"),
    )
    for onset, vowel, syllable, coda, marked_coda in cases:
        result = assemble(onset, vowel, syllable, coda, marked_coda)
        assert result.status == "UNRESOLVED", (onset, vowel, syllable, coda, marked_coda)
        assert result.romanization is None
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_note6_schema_keeps_component_provenance_and_orthographic_only_output():
    path = Path(__file__).resolve().parents[1] / "schemas/pcgn-robat-closed-syllable-assembly.schema.json"
    schema = json.loads(path.read_text(encoding="utf-8"))
    assert set(schema["required"]) == {
        "source_text", "normalized_text", "onset_text", "vowel_chunk_text", "coda_text",
        "marked_coda_text", "series", "onset_romanization", "vowel_romanization",
        "marked_coda_consonant_romanization", "coda_romanization", "romanization",
        "onset_table_rows", "vowel_table_row", "coda_table_row", "status", "ipa",
        "ukrainian", "source_locators", "warnings",
    }
    assert schema["properties"]["ipa"]["const"] is None
    assert schema["properties"]["ukrainian"]["const"] is None
