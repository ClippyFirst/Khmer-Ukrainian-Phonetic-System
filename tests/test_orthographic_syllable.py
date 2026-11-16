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
    assert forest.to_dict()["selected_alternative"] is None
    assert any(item["start"] == 4 and "coda-versus-next-syllable" in item["reason"] for item in forest.rejected_spans)
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
    assert forest.rejected_spans[0]["start"] == 2
    assert forest.rejected_spans[0]["end"] == 3
    assert "ipa" not in forest.to_dict()
    assert "ukrainian" not in forest.to_dict()
    assert forest.rejected_spans[0]["start"] == 2


def test_unicode_18_examples_have_exact_candidate_boundary_parse_sets():
    expected = {
        "ខ្ញុំ": (((0, 5),),),
        "ច្រើន": (((0, 4), (4, 5)),),
        "សង្គ្រាម": (((0, 1), (1, 7), (7, 8)),),
        "ហើ្យ": (((0, 4),),),
        "សញ្ញា": (((0, 1), (1, 5)),),
        "ស៊ី": (((0, 3),),),
        "ប៉ី": (((0, 3),),),
        "ម៉្ងៃ": (((0, 5),),),
        "ប‌៊ីយែរ": (((0, 4), (4, 6), (6, 7)),),
        "ផ្ឯម": (((0, 3), (3, 4)),),
        "អាយ៌": (((0, 2), (2, 4)),),
        "ពត៌មាន": (((0, 1), (1, 3), (3, 5), (5, 6)),),
    }
    for source, candidate_paths in expected.items():
        forest = parse_orthographic_sequence(source)
        assert forest.boundary_alternatives == candidate_paths, (source, forest.to_dict())
        assert "".join(source[start:end] for path in forest.boundary_alternatives for start, end in path) == source
