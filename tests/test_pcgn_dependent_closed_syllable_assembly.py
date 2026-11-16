from __future__ import annotations

import json
from pathlib import Path

from khmer_ua.pcgn import (
    PCGN_DEPENDENT_VOWEL_ROWS,
    assemble_pcgn_dependent_closed_syllable,
    analyze_pcgn_orthographic_chunk,
)


def assemble(onset: str, vowel_chunk: str, syllable: str, coda: str):
    return assemble_pcgn_dependent_closed_syllable(
        analyze_pcgn_orthographic_chunk(onset),
        analyze_pcgn_orthographic_chunk(vowel_chunk),
        analyze_pcgn_orthographic_chunk(syllable),
        analyze_pcgn_orthographic_chunk(coda),
    )


def test_pcgn_normal_dependent_vowel_closed_syllables_assemble_both_series():
    for onset, vowel_index in (("ក", 1), ("គ", 2)):
        for signs, row in PCGN_DEPENDENT_VOWEL_ROWS.items():
            vowel_chunk = onset + "".join(signs)
            syllable = vowel_chunk + "ត"
            result = assemble(onset, vowel_chunk, syllable, "ត")
            expected_vowel = row[vowel_index]
            assert result.status == "RESOLVED", (onset, signs)
            assert result.vowel_romanization == expected_vowel, (onset, signs)
            assert result.romanization == result.onset_romanization + expected_vowel + "t"
            assert result.vowel_table_row == row[0]
            assert result.series == ("â" if vowel_index == 1 else "ô")
            assert result.ipa is None
            assert result.ukrainian is None


def test_pcgn_normal_dependent_vowel_closed_syllable_composes_onset_vowel_and_coda():
    cases = (
        ("ក", "កា", "កាត", "ត", "kat", "â"),
        ("គ", "គា", "គាត", "ត", "kéat", "ô"),
        ("ថ្ម", "ថ្មា", "ថ្មាត", "ត", "thmat", "â"),
        ("ក", "កា", "កាក", "ក", "kak", "â"),
        ("ក", "កា", "កាង", "ង", "kang", "â"),
        ("ក", "កា", "កាហ", "ហ", "kah", "â"),
    )
    for onset, vowel_chunk, syllable, coda, expected, series in cases:
        result = assemble(onset, vowel_chunk, syllable, coda)
        assert result.status == "RESOLVED", syllable
        assert result.romanization == expected, syllable
        assert result.series == series
        assert result.romanization == (
            result.onset_romanization + result.vowel_romanization + result.coda_romanization
        )
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_normal_dependent_closed_syllable_requires_exact_caller_boundaries():
    for onset, vowel_chunk, syllable, coda in (
        ("ក", "កា", "គាត", "ត"),
        ("ក", "គា", "គាត", "ត"),
        ("ក", "កា", "កាតា", "ត"),
        ("ក", "កា", "កាត", "ង"),
        ("ក", "កា", "កាត", "ក្x"),
    ):
        result = assemble(onset, vowel_chunk, syllable, coda)
        assert result.status == "UNRESOLVED"
        assert result.romanization is None


def test_pcgn_normal_dependent_closed_syllable_abstains_on_shortening_and_special_context():
    for syllable in ("កា់", "កា័ក", "កា៌", "កា៏", "កា៍", "កាំ"):
        result = assemble("ក", "កា", syllable, "ត")
        assert result.status == "UNRESOLVED", syllable
        assert result.romanization is None
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_normal_dependent_closed_syllable_schema_preserves_orthographic_boundary():
    schema_path = Path(__file__).resolve().parents[1] / "schemas/pcgn-dependent-closed-syllable-assembly.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    assert set(schema["required"]) == {
        "source_text", "normalized_text", "onset_text", "vowel_chunk_text",
        "coda_text", "series", "onset_romanization", "vowel_romanization",
        "coda_romanization", "romanization", "onset_table_rows",
        "vowel_table_row", "coda_table_row", "status", "ipa", "ukrainian",
        "source_locators", "warnings",
    }
    assert schema["properties"]["ipa"]["const"] is None
    assert schema["properties"]["ukrainian"]["const"] is None
