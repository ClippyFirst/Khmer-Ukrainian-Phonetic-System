from __future__ import annotations

from khmer_ua.pcgn import PCGN_NO_SUBSCRIPT_FOR, analyze_pcgn_orthographic_chunk


def test_pcgn_analysis_preserves_base_and_subscript_without_claiming_syllable_parse():
    result = analyze_pcgn_orthographic_chunk("ក្ប")

    assert result.base_consonants == ("ក",)
    assert result.subscript_consonants == ("ប",)
    assert result.tokens[0].orthographic_register == "first"
    assert result.tokens[1].orthographic_register == "first"
    assert result.register_source == "NOT_SELECTED"
    assert [item.kind for item in result.tokens] == [
        "unstacked_consonant",
        "subscript_consonant",
    ]
    assert result.syllable_segmentation == "NOT_PERFORMED"
    assert result.series_decision == "UNRESOLVED"
    assert result.coda_decision == "UNRESOLVED"
    assert result.romanization is None
    assert result.ipa is None
    assert result.ukrainian is None


def test_pcgn_register_shifters_are_typed_and_not_applied_by_parser():
    result = analyze_pcgn_orthographic_chunk("ប៉ា៊")

    assert result.register_shifters == ("៉", "៊")
    assert result.register_shifter_positions == (1, 3)
    assert [item.kind for item in result.tokens] == [
        "unstacked_consonant",
        "register_shifter",
        "dependent_vowel",
        "register_shifter",
    ]
    assert result.series_decision == "UNRESOLVED"
    assert any("REGISTER_SHIFTER_EFFECT" in warning for warning in result.warnings)


def test_both_pcgn_shortening_marks_are_preserved_as_distinct_tokens():
    result = analyze_pcgn_orthographic_chunk("កា់័")

    assert result.shortening_marks == ("់", "័")
    assert [item.name for item in result.tokens if item.kind == "shortening_mark"] == [
        "BANTOC",
        "SAMYOK_SANNYA",
    ]
    assert any("SHORTENING_REQUIRES" in warning for warning in result.warnings)


def test_pcgn_robat_ahsda_and_toandakhiat_keep_context_and_position():
    result = analyze_pcgn_orthographic_chunk("ក៌៏៍")

    assert result.robat_positions == (1,)
    assert result.ahsda_positions == (2,)
    assert result.toandakhiat_positions == (3,)
    assert [item.kind for item in result.tokens] == [
        "unstacked_consonant",
        "robat",
        "ahsda_position_sensitive",
        "toandakhiat_silent_mark",
    ]
    assert any("ROBAT_REQUIRES" in warning for warning in result.warnings)
    assert any("AHSDA_BEHAVIOR" in warning for warning in result.warnings)
    assert any("TOANDAKHIAT_MARKED_CHARACTER" in warning for warning in result.warnings)


def test_multiple_unstacked_consonants_are_not_silently_assigned_as_coda_or_new_syllable():
    result = analyze_pcgn_orthographic_chunk("កត")

    assert result.base_consonants == ("ក", "ត")
    assert result.coda_decision == "UNRESOLVED"
    assert result.syllable_segmentation == "NOT_PERFORMED"
    assert "MULTIPLE_UNSTACKED_CONSONANTS_RETAINED_WITHOUT_SYLLABLE_ASSIGNMENT" in result.warnings


def test_malformed_coeng_and_unknown_components_fail_closed_without_losing_source():
    malformed = analyze_pcgn_orthographic_chunk("ក្x")

    assert malformed.status == "UNSUPPORTED"
    assert malformed.unresolved_components == ("្", "x")
    assert "".join(item.text for item in malformed.tokens) == "ក្x"
    assert malformed.romanization is None

    unknown = analyze_pcgn_orthographic_chunk("ក🙂")
    assert unknown.status == "UNSUPPORTED"
    assert unknown.unresolved_components == ("🙂",)


def test_pcgn_analysis_is_nfc_normalized_but_retains_original_input():
    decomposed = "ក" + "\u17C1" + "\u17B6"
    result = analyze_pcgn_orthographic_chunk(decomposed)

    assert result.raw_text == decomposed
    assert result.normalized_text == "កេា"
    assert "".join(item.text for item in result.tokens) == result.normalized_text


def test_pcgn_analysis_serializes_explicit_null_phonetic_outputs_and_provenance():
    result = analyze_pcgn_orthographic_chunk("ក")
    payload = result.to_dict()

    assert payload["romanization"] is None
    assert payload["ipa"] is None
    assert payload["ukrainian"] is None
    assert "pcgn-1972-notes-2-8" in payload["sources"]
    assert any("OMITTED_DIACRITICS" in warning for warning in payload["warnings"])


def test_empty_or_separator_only_chunk_is_not_reported_as_parsed_structure():
    assert analyze_pcgn_orthographic_chunk("").status == "UNSUPPORTED"
    assert analyze_pcgn_orthographic_chunk("  , ").status == "UNSUPPORTED"


def test_pcgn_analysis_schema_requires_explicit_abstention_fields():
    import json
    from pathlib import Path

    schema_path = Path(__file__).resolve().parents[1] / "schemas/pcgn-orthographic-analysis.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    required = set(schema["required"])

    assert {"tokens", "base_consonants", "subscript_consonants", "register_shifters", "register_shifter_positions"} <= required
    assert {"syllable_segmentation", "series_decision", "register_source", "coda_decision"} <= required
    assert {"romanization", "ipa", "ukrainian", "warnings", "sources"} <= required
    assert schema["properties"]["syllable_segmentation"]["const"] == "NOT_PERFORMED"
    assert schema["properties"]["series_decision"]["const"] == "UNRESOLVED"
    assert schema["properties"]["register_source"]["const"] == "NOT_SELECTED"
    assert schema["properties"]["romanization"]["type"] == "null"
    assert schema["properties"]["ipa"]["type"] == "null"
    assert schema["properties"]["ukrainian"]["type"] == "null"


def test_unmodeled_khmer_letters_are_not_accepted_as_known_pcgn_structure():
    result = analyze_pcgn_orthographic_chunk("ឣ")
    assert result.status == "UNSUPPORTED"
    assert result.unresolved_components == ("ឣ",)
    assert result.tokens[0].kind == "unmodeled_letter"


def test_pcgn_laa_has_no_subscript_form_per_consonant_table_note():
    result = analyze_pcgn_orthographic_chunk("ក្ឡ")
    assert result.status == "UNSUPPORTED"
    assert result.subscript_consonants == ()
    assert result.unresolved_components == ("្", "ឡ")
    assert result.tokens[-1].kind == "unsupported_pcgn_subscript"


def test_pcgn_no_subscript_inventory_is_explicit():
    assert PCGN_NO_SUBSCRIPT_FOR == frozenset("ឡ")
