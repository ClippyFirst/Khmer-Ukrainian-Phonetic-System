from khmer_ua.orthographic_syllable import parse_orthographic_syllable, parse_orthographic_sequence


def test_unicode_18_bnf_accepts_representative_single_base_orders():
    for source in ("ខ្ញុំ", "ស៊ី", "ប៉ី", "ក៌", "ផ្ឯ"):
        result = parse_orthographic_syllable(source)
        assert result.status == "PARSED", (source, result.to_dict())
        assert result.to_dict()["schema"] == "khmer-orthographic-syllable/v1"


def test_unicode_18_bnf_accepts_documented_zwnj_shifter_exception():
    assert parse_orthographic_syllable("ប‌៊").status == "PARSED"


def test_unicode_18_bnf_rejects_out_of_order_components():
    assert parse_orthographic_syllable("កា៉").status == "INVALID_ORDER"
    assert parse_orthographic_syllable("កាី").status == "INVALID_ORDER"
    assert parse_orthographic_syllable("ក‌").status == "INVALID_ORDER"


def test_parser_does_not_guess_syllable_boundaries_for_multiple_bases():
    assert parse_orthographic_syllable("ច្រើន").status == "EVIDENCE_LIMITED"
    assert parse_orthographic_syllable("សង្គ្រាម").status == "EVIDENCE_LIMITED"


def test_parser_preserves_invalid_coeng_and_unknown_character_states():
    assert parse_orthographic_syllable("ក្").status == "INVALID_OR_UNSUPPORTED"
    assert parse_orthographic_syllable("កx").status == "INVALID_OR_UNSUPPORTED"


def test_parser_preserves_exact_codepoint_component_spans():
    result = parse_orthographic_syllable("🧪ខ្ញុំ")
    assert result.status == "INVALID_OR_UNSUPPORTED"
    assert result.component_spans[0] == (0, 1)
    assert result.component_spans[1] == (1, 2)


def test_unicode_18_parse_forest_returns_all_derivations_and_exact_spans():
    forest = parse_orthographic_sequence("ផ្ឯ")
    assert forest.status == "PARSED"
    assert forest.boundary_alternatives == (((0, 3),),)
    assert len(forest.alternatives) == 2  # repeated-S versus final-S derivation
    payload = forest.to_dict()
    assert payload["schema"] == "khmer-orthographic-parse-forest/v1"
    assert payload["offset_unit"] == "unicode_code_point"


def test_unicode_18_parse_forest_keeps_multiple_base_candidates_unselected():
    source = "ច្រើន"
    forest = parse_orthographic_sequence(source)
    assert forest.status == "EVIDENCE_LIMITED"
    assert forest.boundary_alternatives == (((0, 4), (4, 5)),)
    reconstructed = "".join(
        source[start:end]
        for path in forest.boundary_alternatives
        for start, end in path
    )
    assert reconstructed == source


def test_unicode_18_parse_forest_retains_all_component_order_examples():
    examples = (
        "ខ្ញុំ", "ច្រើន", "សង្គ្រាម", "ហើ្យ", "សញ្ញា", "ស៊ី", "ប៉ី",
        "ម៉្ងៃ", "ប‌៊ីយែរ", "ផ្ឯម", "អាយ៌", "ពត៌មាន",
    )
    for source in examples:
        forest = parse_orthographic_sequence(source)
        assert forest.status in {"PARSED", "EVIDENCE_LIMITED", "AMBIGUOUS"}, (source, forest.to_dict())
        for path in forest.boundary_alternatives:
            assert "".join(source[start:end] for start, end in path) == source


def test_unicode_18_parse_forest_exposes_rejected_order_and_no_ipa():
    forest = parse_orthographic_sequence("កាី")
    assert forest.status == "INVALID_ORDER"
    assert forest.rejected_spans
    assert "ipa" not in forest.to_dict()
    assert "ukrainian" not in forest.to_dict()
