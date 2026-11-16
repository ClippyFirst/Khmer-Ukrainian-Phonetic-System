from __future__ import annotations

import json
from pathlib import Path

from khmer_ua.pcgn import (
    PCGN_INDEPENDENT_VOWEL_ROWS,
    analyze_pcgn_orthographic_chunk,
    assemble_pcgn_independent_vowel_closed_syllable,
)


def assemble(vowel: str, syllable: str, coda: str):
    return assemble_pcgn_independent_vowel_closed_syllable(
        analyze_pcgn_orthographic_chunk(vowel),
        analyze_pcgn_orthographic_chunk(syllable),
        analyze_pcgn_orthographic_chunk(coda),
    )


def test_pcgn_independent_vowel_closed_syllable_composes_vowel_and_final_coda():
    result = assemble("ឥ", "ឥក", "ក")
    assert result.status == "RESOLVED"
    assert result.independent_vowel == "ឥ"
    assert result.vowel_romanization == "ĕ"
    assert result.vowel_table_row == 3
    assert result.coda_romanization == "k"
    assert result.romanization == "ĕk"
    assert result.romanization_options == ()
    assert result.ipa is None
    assert result.ukrainian is None


def test_pcgn_independent_vowel_closed_syllable_covers_all_listed_resolved_vowels():
    for character, (row, romanization) in PCGN_INDEPENDENT_VOWEL_ROWS.items():
        result = assemble(character, character + "ក", "ក")
        assert result.status == "RESOLVED", (character, row, result.warnings)
        assert result.independent_vowel == character
        assert result.vowel_romanization == romanization
        assert result.vowel_table_row == row
        assert result.coda_romanization == "k"
        assert result.romanization == romanization + "k"


def test_pcgn_independent_vowel_closed_syllable_keeps_note9_ambiguous_vowel_unresolved():
    result = assemble("ឧ", "ឧក", "ក")
    assert result.status == "UNRESOLVED"
    assert result.independent_vowel == "ឧ"
    assert result.romanization is None
    assert result.romanization_options == ("ŏ", "ŭ")
    assert result.vowel_table_row == 7
    assert "PCGN_NOTE_9_Ŏ_OR_Ŭ_REQUIRES_REFERENCE_SELECTION" in result.warnings


def test_pcgn_independent_vowel_closed_syllable_rejects_mismatched_or_special_chunks():
    for vowel, syllable, coda in (
        ("ឥ", "ឥក", "ត"),
        ("ឥ", "ឥត", "ក"),
        ("ឥ", "ឥ", "ក"),
        ("ឥ", "ឥាក", "ក"),
        ("ក", "កក", "ក"),
        ("ឥ", "ឥកត", "ក"),
        ("ឥ", "ឥក៌", "ក"),
    ):
        result = assemble(vowel, syllable, coda)
        assert result.status == "UNRESOLVED", (vowel, syllable, coda, result.warnings)
        assert result.romanization is None
        assert result.romanization_options == ()
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_independent_vowel_closed_syllable_schema_is_orthographic_only():
    path = Path(__file__).resolve().parents[1] / "schemas/pcgn-independent-vowel-closed-syllable-assembly.schema.json"
    schema = json.loads(path.read_text(encoding="utf-8"))
    assert set(schema["required"]) == {
        "source_text", "normalized_text", "vowel_chunk_text", "coda_text", "independent_vowel",
        "vowel_romanization", "vowel_table_row", "coda_romanization", "coda_table_row",
        "romanization", "romanization_options", "status", "ipa", "ukrainian", "source_locators", "warnings",
    }
    assert schema["properties"]["ipa"]["const"] is None
    assert schema["properties"]["ukrainian"]["const"] is None
    assert schema["properties"]["romanization_options"]["maxItems"] == 2
