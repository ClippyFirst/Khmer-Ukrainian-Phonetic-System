from __future__ import annotations

import json
from pathlib import Path

from khmer_ua.pcgn_unicode import (
    PCGN_CHARACTER_INVENTORY_LOCATOR,
    PCGN_SPECIAL_LETTER_CODEPOINTS,
    PCGN_SPECIAL_LETTERS,
    validate_pcgn_romanization_characters,
)


def test_pcgn_note10_special_letter_inventory_matches_exact_codepoints():
    expected = {
        "â": ("U+00E2",), "Â": ("U+00C2",),
        "ă": ("U+0103",), "Ă": ("U+0102",),
        "á": ("U+00E1",), "Á": ("U+00C1",),
        "ê": ("U+00EA",), "Ê": ("U+00CA",),
        "ĕ": ("U+0115",), "Ĕ": ("U+0114",),
        "é": ("U+00E9",), "É": ("U+00C9",),
        "ĭ": ("U+012D",), "Ĭ": ("U+012C",),
        "ô": ("U+00F4",), "Ô": ("U+00D4",),
        "ó": ("U+00F3",), "Ó": ("U+00D3",),
        "ŏ": ("U+014F",), "Ŏ": ("U+014E",),
        "œ": ("U+0153",), "Œ": ("U+0152",),
        "œ̆": ("U+0153", "U+0306"),
        "Œ̆": ("U+0152", "U+0306"),
        "ŭ": ("U+016D",), "Ŭ": ("U+016C",),
    }
    assert PCGN_SPECIAL_LETTER_CODEPOINTS == expected
    assert set(PCGN_SPECIAL_LETTERS) == set(expected)
    assert PCGN_CHARACTER_INVENTORY_LOCATOR == "PCGN 1972, Note 10 (p. 5)"


def test_pcgn_note10_accepts_all_listed_forms_and_basic_ascii_letters():
    source = "AaZz" + "".join(PCGN_SPECIAL_LETTERS)
    result = validate_pcgn_romanization_characters(source)

    assert result.status == "VALID"
    assert result.recognized_special_letters == PCGN_SPECIAL_LETTERS
    assert result.unsupported_letters == ()
    assert result.source_text == source
    assert result.codepoint_trace == tuple(f"U+{ord(ch):04X}" for ch in source)


def test_pcgn_note10_preserves_decomposed_breve_without_normalizing():
    source = "rœ\u0306"
    result = validate_pcgn_romanization_characters(source)

    assert result.status == "VALID"
    assert result.source_text == source
    assert result.recognized_special_letters == ("œ̆",)
    assert result.codepoint_trace == ("U+0072", "U+0153", "U+0306")
    assert result.warnings[1] == "SOURCE_CODEPOINTS_PRESERVED_NO_NORMALIZATION_OR_TRANSLITERATION"


def test_pcgn_note10_rejects_unlisted_letters_and_unlisted_combining_marks():
    result = validate_pcgn_romanization_characters("ēœ\u0301ក")

    assert result.status == "UNSUPPORTED_LETTER"
    assert result.unsupported_letters == ("ē", "\u0301", "ក")
    assert result.recognized_special_letters == ("œ",)


def test_pcgn_note10_passes_through_nonletters_without_claiming_to_validate_them():
    source = "’ rœ̆-123"
    result = validate_pcgn_romanization_characters(source)

    assert result.status == "VALID"
    assert result.recognized_special_letters == ("œ̆",)
    assert result.non_letter_characters == ("’", " ", "-", "1", "2", "3")
    assert "NON_LETTER_PUNCTUATION_SPACING_AND_DIGITS_NOT_VALIDATED" in result.warnings


def test_pcgn_note10_decision_schema_preserves_inventory_and_validation_scope():
    path = Path(__file__).resolve().parents[1] / (
        "schemas/pcgn-romanization-character-inventory-decision.schema.json"
    )
    schema = json.loads(path.read_text(encoding="utf-8"))

    assert set(schema["required"]) == {
        "source_text", "status", "recognized_special_letters",
        "unsupported_letters", "non_letter_characters", "codepoint_trace",
        "source_locator", "warnings",
    }
    assert schema["properties"]["source_locator"]["const"] == PCGN_CHARACTER_INVENTORY_LOCATOR
    assert schema["properties"]["unsupported_letters"]["type"] == "array"
    assert schema["allOf"][0]["then"]["properties"]["unsupported_letters"]["maxItems"] == 0
    assert schema["allOf"][1]["then"]["properties"]["unsupported_letters"]["minItems"] == 1
