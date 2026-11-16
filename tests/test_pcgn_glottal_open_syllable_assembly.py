from __future__ import annotations

import json
from pathlib import Path

from khmer_ua.pcgn import (
    PCGN_DEPENDENT_VOWEL_ROWS,
    analyze_pcgn_orthographic_chunk,
    assemble_pcgn_glottal_open_syllable,
)


def assemble(onset: str, syllable: str, word_initial: bool, followed_by_vowel: bool):
    return assemble_pcgn_glottal_open_syllable(
        analyze_pcgn_orthographic_chunk(onset),
        analyze_pcgn_orthographic_chunk(syllable),
        word_initial,
        followed_by_vowel,
    )


def test_pcgn_note4_alif_open_syllable_composes_apostrophe_and_a_series_vowel():
    result = assemble("អ", "អា", False, True)
    assert result.status == "RESOLVED"
    assert result.series == "â"
    assert result.onset_romanization == "’"
    assert result.vowel_romanization == "a"
    assert result.romanization == "’a"
    assert result.romanization_options == ("’a",)
    assert result.vowel_table_row == 2
    assert result.ipa is None
    assert result.ukrainian is None


def test_pcgn_note4_optional_word_initial_apostrophe_is_preserved_as_variant():
    result = assemble("អ", "អេ", True, True)
    assert result.status == "RESOLVED"
    assert result.romanization == "’é"
    assert result.romanization_options == ("’é", "é")
    assert "OPTIONAL_APOSTROPHE_VARIANT_PRESERVED_WHEN_NOTE_4_ALLOWS" in result.warnings


def test_pcgn_note4_nonoptional_context_keeps_apostrophe():
    for word_initial, followed_by_vowel in ((True, False), (False, True), (False, False)):
        result = assemble("អ", "អែ", word_initial, followed_by_vowel)
        assert result.status == "RESOLVED"
        assert result.romanization == "’ê"
        assert result.romanization_options == ("’ê",)


def test_pcgn_note4_assembler_covers_every_bounded_normal_dependent_vowel_pattern():
    for signs, (row, a_value, _o_value) in PCGN_DEPENDENT_VOWEL_ROWS.items():
        syllable = "អ" + "".join(signs)
        result = assemble("អ", syllable, False, True)
        assert result.status == "RESOLVED", (row, syllable, result.warnings)
        assert result.vowel_romanization == a_value
        assert result.vowel_table_row == row
        assert result.romanization == "’" + a_value


def test_pcgn_note4_assembler_abstains_on_wrong_boundaries_or_non_dependent_vowel():
    for onset, syllable in (
        ("អ", "កា"),
        ("ក", "កា"),
        ("អ", "អាត"),
        ("អ", "អិឥ"),
        ("អ", "អឥ"),
        ("អ", "អ៊ា"),
        ("អ", "អា់"),
    ):
        result = assemble(onset, syllable, False, True)
        assert result.status == "UNRESOLVED", (onset, syllable)
        assert result.romanization is None
        assert result.romanization_options == ()
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_note4_assembler_requires_explicit_boolean_context():
    for word_initial, followed_by_vowel in ((None, True), (True, None), (None, None)):
        result = assemble_pcgn_glottal_open_syllable(
            analyze_pcgn_orthographic_chunk("អ"),
            analyze_pcgn_orthographic_chunk("អា"),
            word_initial,
            followed_by_vowel,
        )
        assert result.status == "UNRESOLVED"
        assert result.romanization is None
        assert result.romanization_options == ()


def test_pcgn_note4_assembler_schema_keeps_optional_romanization_and_no_phonetic_output():
    path = Path(__file__).resolve().parents[1] / "schemas/pcgn-glottal-open-syllable-assembly.schema.json"
    schema = json.loads(path.read_text(encoding="utf-8"))
    assert set(schema["required"]) == {
        "source_text", "normalized_text", "onset_text", "word_initial",
        "followed_by_vowel_letter", "series", "onset_romanization",
        "vowel_romanization", "romanization", "romanization_options",
        "vowel_table_row", "status", "ipa", "ukrainian", "source_locators", "warnings",
    }
    assert schema["properties"]["ipa"]["const"] is None
    assert schema["properties"]["ukrainian"]["const"] is None
    assert schema["properties"]["romanization_options"]["minItems"] == 1
    assert schema["properties"]["romanization_options"]["maxItems"] == 2
