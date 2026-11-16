from __future__ import annotations

import json
from pathlib import Path

from khmer_ua.pcgn import (
    PCGN_DEPENDENT_VOWEL_ROWS,
    analyze_pcgn_orthographic_chunk,
    assemble_pcgn_glottal_dependent_closed_syllable,
)


def assemble(onset: str, vowel: str, syllable: str, coda: str, word_initial: bool, followed_by_vowel: bool):
    return assemble_pcgn_glottal_dependent_closed_syllable(
        analyze_pcgn_orthographic_chunk(onset),
        analyze_pcgn_orthographic_chunk(vowel),
        analyze_pcgn_orthographic_chunk(syllable),
        analyze_pcgn_orthographic_chunk(coda),
        word_initial,
        followed_by_vowel,
    )


def test_pcgn_note4_alif_closed_syllable_assembles_onset_vowel_and_final_coda():
    result = assemble("អ", "អា", "អាក", "ក", False, True)
    assert result.status == "RESOLVED"
    assert result.series == "â"
    assert result.onset_romanization == "’"
    assert result.vowel_romanization == "a"
    assert result.coda_romanization == "k"
    assert result.romanization == "’ak"
    assert result.romanization_options == ("’ak",)
    assert result.vowel_table_row == 2
    assert result.ipa is None
    assert result.ukrainian is None


def test_pcgn_note4_alif_closed_syllable_preserves_optional_apostrophe_variant():
    result = assemble("អ", "អេ", "អេក", "ក", True, True)
    assert result.status == "RESOLVED"
    assert result.romanization == "’ék"
    assert result.romanization_options == ("’ék", "ék")


def test_pcgn_note4_alif_closed_syllable_covers_all_normal_dependent_vowel_patterns():
    for signs, (row, a_value, _o_value) in PCGN_DEPENDENT_VOWEL_ROWS.items():
        vowel = "អ" + "".join(signs)
        syllable = vowel + "ក"
        result = assemble("អ", vowel, syllable, "ក", False, True)
        assert result.status == "RESOLVED", (row, syllable, result.warnings)
        assert result.vowel_romanization == a_value
        assert result.vowel_table_row == row
        assert result.romanization == "’" + a_value + "k"


def test_pcgn_note4_alif_closed_syllable_rejects_mismatched_chunks_and_special_forms():
    for onset, vowel, syllable, coda in (
        ("អ", "អា", "អាក", "ត"),
        ("អ", "អា", "អាត", "ក"),
        ("ក", "កា", "កាក", "ក"),
        ("អ", "អា", "អា", "ក"),
        ("អ", "អ៊ា", "អ៊ាក", "ក"),
        ("អ", "អា់", "អា់ក", "ក"),
        ("អ", "អា", "អាកត", "ក"),
    ):
        result = assemble(onset, vowel, syllable, coda, False, True)
        assert result.status == "UNRESOLVED", (onset, vowel, syllable, coda)
        assert result.romanization is None
        assert result.romanization_options == ()
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_note4_alif_closed_syllable_requires_explicit_boolean_context():
    for word_initial, followed_by_vowel in ((None, True), (True, None), (None, None)):
        result = assemble_pcgn_glottal_dependent_closed_syllable(
            analyze_pcgn_orthographic_chunk("អ"),
            analyze_pcgn_orthographic_chunk("អា"),
            analyze_pcgn_orthographic_chunk("អាក"),
            analyze_pcgn_orthographic_chunk("ក"),
            word_initial,
            followed_by_vowel,
        )
        assert result.status == "UNRESOLVED"
        assert result.romanization is None
        assert result.romanization_options == ()


def test_pcgn_note4_alif_closed_syllable_schema_is_orthographic_only():
    path = Path(__file__).resolve().parents[1] / "schemas/pcgn-glottal-dependent-closed-syllable-assembly.schema.json"
    schema = json.loads(path.read_text(encoding="utf-8"))
    assert set(schema["required"]) == {
        "source_text", "normalized_text", "onset_text", "vowel_chunk_text", "coda_text",
        "word_initial", "followed_by_vowel_letter", "series", "onset_romanization",
        "vowel_romanization", "coda_romanization", "romanization", "romanization_options",
        "vowel_table_row", "coda_table_row", "status", "ipa", "ukrainian", "source_locators", "warnings",
    }
    assert schema["properties"]["ipa"]["const"] is None
    assert schema["properties"]["ukrainian"]["const"] is None
    assert schema["properties"]["romanization_options"]["maxItems"] == 2
