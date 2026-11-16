from khmer_ua.orthographic_syllables import parse_orthographic_syllables


def test_unicode_18_examples_parse_and_reconstruct():
    examples = {
        "ទេ": ["ទេ"],
        "ខ្ញុំ": ["ខ្ញុំ"],
        "ច្រើន": ["ច្រើ", "ន"],
        "សង្គ្រាម": ["ស", "ង្គ្រា", "ម"],
        "ហើ្យ": ["ហើ្យ"],
        "ហើយ": ["ហើ", "យ"],
        "សញ្ញា": ["ស", "ញ្ញា"],
        "ស៊ី": ["ស៊ី"],
        "ប៉ី": ["ប៉ី"],
        "អាយ៌": ["អា", "យ៌"],
        "ម៉្ងៃ": ["ម៉្ងៃ"],
        "ប‌៊ីយែរ": ["ប‌៊ី", "យែ", "រ"],
        "ពត៌មាន": ["ព", "ត៌", "មា", "ន"],
        "រាជរ្សី": ["រា", "ជ", "រ្សី"],
        "ម៊្ហែត": ["ម៊្ហែ", "ត"],
        "វ‌ិទូ": ["វ‌ិ", "ទូ"],
        "វ‍ិទូ": ["វ‍ិ", "ទូ"],
    }
    for source, expected in examples.items():
        result = parse_orthographic_syllables(source)
        assert result.status == "PARSED"
        assert [item.source_text for item in result.syllables] == expected
        assert "".join(item.source_text for item in result.syllables) == source
        assert all(item.source_text == source[item.start:item.end] for item in result.syllables)
        assert all(item.end > item.start for item in result.syllables)
        assert "not phonological syllables" in result.notes[0]


def test_unicode_18_textual_zwnj_before_shifter_exception_is_explicit():
    result = parse_orthographic_syllables("ប\u200c៊")
    assert result.status == "PARSED"
    assert result.syllables[0].grammar_extensions == (
        "U+200C-before-shifter (§16.4.1 textual exception)",
    )


def test_multiple_base_scanner_limit_is_resolved_by_bnf_boundaries():
    result = parse_orthographic_syllables("សង្គ្រាម")
    assert result.status == "PARSED"
    assert [item.source_text for item in result.syllables] == ["ស", "ង្គ្រា", "ម"]


def test_invalid_coeng_and_unknown_characters_fail_closed():
    assert parse_orthographic_syllables("ក្").status == "INVALID_OR_UNSUPPORTED"
    assert parse_orthographic_syllables("កx").status == "INVALID_OR_UNSUPPORTED"
    assert parse_orthographic_syllables("ឣ").status == "INVALID_OR_UNSUPPORTED"
    assert parse_orthographic_syllables("ឤ").status == "INVALID_OR_UNSUPPORTED"
    assert parse_orthographic_syllables("\u17B4").status == "INVALID_OR_UNSUPPORTED"
    assert parse_orthographic_syllables("\u17B5").status == "INVALID_OR_UNSUPPORTED"
    assert parse_orthographic_syllables("\u17D8").status == "INVALID_OR_UNSUPPORTED"


def test_known_but_nonconforming_component_order_is_evidence_limited():
    result = parse_orthographic_syllables("កេិ")
    assert result.status == "EVIDENCE_LIMITED"
    assert result.alternatives == ()
    assert result.rejected_spans == ({"start": 2, "end": 3, "reason": "VOWEL at this position prevents a complete Unicode 18 §16.4 component-order production."},)


def test_offsets_are_exact_code_points_and_input_is_not_normalized():
    source = "ខ្ញុំ"
    result = parse_orthographic_syllables(source)
    assert result.syllables[0].start == 0
    assert result.syllables[0].end == len(source)
    assert result.source_text == source


def test_subscript_independent_vowel_example_preserves_role_ambiguity():
    result = parse_orthographic_syllables("ផ្ឯម")
    assert result.status == "AMBIGUOUS"
    assert result.to_dict()["parse_count"] == "2"
    assert result.to_dict()["segmentation_count"] == 1
    assert len(result.alternatives) == 1
    assert tuple(item.source_text for item in result.alternatives[0].syllables) == ("ផ្ឯ", "ម")
    assert {
        item.grammar_roles
        for item in result.alternatives[0].syllables[0].grammar_alternatives
    } == {
        ("BASE", "SUBSCRIPT_CLUSTER"),
        ("BASE", "TRAILING_SUBSCRIPT"),
    }


def test_bnf_component_role_ambiguity_is_preserved_as_two_parse_trees():
    result = parse_orthographic_syllables("ក្ក")
    assert result.status == "AMBIGUOUS"
    assert result.syllables is None
    assert result.to_dict()["parse_count"] == "2"
    assert result.to_dict()["segmentation_count"] == 1
    alternatives = {
        item.grammar_roles
        for item in result.alternatives[0].syllables[0].grammar_alternatives
    }
    assert alternatives == {
        ("BASE", "SUBSCRIPT_CLUSTER"),
        ("BASE", "TRAILING_SUBSCRIPT"),
    }


def test_packed_forest_avoids_cartesian_expansion_for_many_ambiguous_syllables():
    source = "ក្ក" * 20
    result = parse_orthographic_syllables(source)
    payload = result.to_dict()
    assert result.status == "AMBIGUOUS"
    assert payload["parse_count"] == str(2 ** 20)
    assert payload["segmentation_count"] == 1
    assert len(result.alternatives[0].syllables) == 20
    assert all(len(item.grammar_alternatives) == 2 for item in result.alternatives[0].syllables)


def test_component_roles_distinguish_cluster_and_trailing_subscript():
    cluster = parse_orthographic_syllables("ខ្ញុំ")
    assert cluster.syllables[0].grammar_roles == (
        "BASE", "SUBSCRIPT_CLUSTER", "DEPENDENT_VOWEL", "OTHER_SIGN"
    )
    trailing = parse_orthographic_syllables("ហើ្យ")
    assert trailing.syllables[0].grammar_roles == (
        "BASE", "DEPENDENT_VOWEL", "TRAILING_SUBSCRIPT"
    )


def test_schema_matches_serialized_parse_contract():
    import json
    from pathlib import Path

    schema = json.loads(Path("schemas/orthographic-syllables.schema.json").read_text(encoding="utf-8"))
    payload = parse_orthographic_syllables("ខ្ញុំ").to_dict()
    assert payload["schema"] == schema["properties"]["schema"]["const"]
    assert set(payload) == set(schema["required"])
    assert payload["parse_count"] == "1"
    assert payload["segmentation_count"] == 1
    assert set(payload["syllables"][0]) == set(schema["$defs"]["syllable"]["required"])


def test_unicode_18_join_controls_and_robats_are_position_sensitive():
    assert parse_orthographic_syllables("ក\u200cេ").status == "PARSED"
    assert parse_orthographic_syllables("ក\u200dេ").status == "PARSED"
    assert parse_orthographic_syllables("ក\u200d៉").status == "EVIDENCE_LIMITED"
    assert parse_orthographic_syllables("ក៌៉").status == "EVIDENCE_LIMITED"
    assert parse_orthographic_syllables("ក្រ៌").status == "PARSED"


def test_unicode_18_subscript_independent_vowel_examples_preserve_packed_roles():
    for source in ("ឱ្យ", "ឱ្ម", "ហ្ឫទ័យ", "ប្រតឺងអ‌៊ឹះ", "ប្រតឺងអ៊ឹះ"):
        result = parse_orthographic_syllables(source)
        assert result.status == "AMBIGUOUS"
        assert result.to_dict()["parse_count"] == "2"
        assert result.syllables is None
        assert all(
            any(role in {"SUBSCRIPT_CLUSTER", "TRAILING_SUBSCRIPT"} for role in item.grammar_roles)
            for alternative in result.alternatives
            for syllable in alternative.syllables
            for item in syllable.grammar_alternatives
            if any(role in {"SUBSCRIPT_CLUSTER", "TRAILING_SUBSCRIPT"} for role in item.grammar_roles)
        )


def test_unicode_18_repetition_mark_is_not_a_syllable_component():
    result = parse_orthographic_syllables("ម៊្ហែតៗ")
    assert result.status == "INVALID_OR_UNSUPPORTED"
    assert [(item["start"], item["end"]) for item in result.rejected_spans] == [(6, 7)]
