from __future__ import annotations

import json
from pathlib import Path

from khmer_ua.pcgn import (
    analyze_pcgn_orthographic_chunk,
    assemble_pcgn_glottal_shortened_closed_syllable,
)


def assemble(syllable: str, coda: str, coda_class: str, word_initial: bool = False, followed_by_vowel: bool = False):
    return assemble_pcgn_glottal_shortened_closed_syllable(
        analyze_pcgn_orthographic_chunk("អ"),
        analyze_pcgn_orthographic_chunk(syllable),
        analyze_pcgn_orthographic_chunk(coda),
        coda_class,
        word_initial,
        followed_by_vowel,
    )


def test_pcgn_note4_note5_alif_inherent_bantoc_pattern_assembles():
    result = assemble("អក់", "ក", "k")
    assert result.status == "RESOLVED"
    assert result.pattern == "INHERENT_BANTOC"
    assert result.shortening_mark == "់"
    assert result.series == "â"
    assert result.vowel_romanization == "á"
    assert result.coda_romanization == "k"
    assert result.romanization == "’ák"
    assert result.romanization_options == ("’ák",)
    assert result.ipa is None
    assert result.ukrainian is None


def test_pcgn_note4_note5_alif_aa_bantoc_pattern_assembles():
    result = assemble("អាក់", "ក", "k")
    assert result.status == "RESOLVED"
    assert result.pattern == "AA_BANTOC"
    assert result.vowel_romanization == "ă"
    assert result.romanization == "’ăk"


def test_pcgn_note4_note5_alif_samyok_coda_pattern_assembles():
    result = assemble("អ័ក", "ក", "k")
    assert result.status == "RESOLVED"
    assert result.pattern == "SAMYOK_CODA"
    assert result.shortening_mark == "័"
    assert result.vowel_romanization == "ă"
    assert result.romanization == "’ăk"


def test_pcgn_note4_note5_optional_apostrophe_is_preserved():
    result = assemble("អាក់", "ក", "k", True, True)
    assert result.status == "RESOLVED"
    assert result.romanization == "’ăk"
    assert result.romanization_options == ("’ăk", "ăk")


def test_pcgn_note4_note5_coda_class_is_cross_checked_against_resolved_final():
    result = assemble("អាក់", "ក", "other")
    assert result.status == "UNRESOLVED"
    assert result.romanization is None
    assert "EXPLICIT_CODA_CLASS_MUST_MATCH_RESOLVED_PCGN_CODA_ROMANIZATION" in result.warnings


def test_pcgn_note4_note5_abstains_on_mismatched_or_unsupported_shapes():
    for syllable, coda, coda_class in (
        ("អក់", "ត", "k"),
        ("អាក់", "ត", "k"),
        ("អ័ក", "ក", "other"),
        ("អាក", "ក", "k"),
        ("អា់ក", "ក", "k"),
        ("អក់ត", "ក", "k"),
    ):
        result = assemble(syllable, coda, coda_class)
        assert result.status == "UNRESOLVED", (syllable, coda, coda_class)
        assert result.romanization is None
        assert result.romanization_options == ()
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_note4_note5_requires_explicit_boolean_context():
    for word_initial, followed_by_vowel in ((None, False), (False, None), (None, None)):
        result = assemble_pcgn_glottal_shortened_closed_syllable(
            analyze_pcgn_orthographic_chunk("អ"),
            analyze_pcgn_orthographic_chunk("អក់"),
            analyze_pcgn_orthographic_chunk("ក"),
            "k",
            word_initial,
            followed_by_vowel,
        )
        assert result.status == "UNRESOLVED"
        assert result.romanization is None


def test_pcgn_note4_note5_schema_preserves_pattern_coda_and_orthographic_boundary():
    path = Path(__file__).resolve().parents[1] / "schemas/pcgn-glottal-shortened-closed-syllable-assembly.schema.json"
    schema = json.loads(path.read_text(encoding="utf-8"))
    assert set(schema["required"]) == {
        "source_text", "normalized_text", "onset_text", "coda_text", "word_initial",
        "followed_by_vowel_letter", "series", "pattern", "shortening_mark", "coda_class",
        "onset_romanization", "vowel_romanization", "coda_romanization", "romanization",
        "romanization_options", "vowel_table_row", "coda_table_row", "status", "ipa",
        "ukrainian", "source_locators", "warnings",
    }
    assert schema["properties"]["ipa"]["const"] is None
    assert schema["properties"]["ukrainian"]["const"] is None
    assert schema["properties"]["pattern"]["enum"] == ["INHERENT_BANTOC", "AA_BANTOC", "SAMYOK_CODA", None]
