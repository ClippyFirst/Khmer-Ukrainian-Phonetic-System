from khmer_ua.orthographic_syllable import parse_orthographic_syllable


def test_unicode_18_bnf_accepts_representative_single_base_orders():
    for source in ("ខ្ញុំ", "ស៊ី", "ប៉ី", "ក៌", "ក្"):
        result = parse_orthographic_syllable(source)
        assert result.status == "PARSED", (source, result.to_dict())
        assert result.to_dict()["schema"] == "khmer-orthographic-syllable/v1"


def test_unicode_18_bnf_accepts_documented_zwnj_shifter_exception():
    assert parse_orthographic_syllable("ប‌៊").status == "PARSED"


def test_unicode_18_bnf_rejects_out_of_order_components():
    assert parse_orthographic_syllable("កា៉").status == "INVALID_ORDER"
    assert parse_orthographic_syllable("ក្៌").status == "INVALID_ORDER"
    assert parse_orthographic_syllable("ក‌").status == "INVALID_ORDER"


def test_parser_does_not_guess_syllable_boundaries_for_multiple_bases():
    result = parse_orthographic_syllable("ច្រើន")
    assert result.status == "EVIDENCE_LIMITED"
    assert parse_orthographic_syllable("សង្គ្រាម").status == "EVIDENCE_LIMITED"


def test_parser_preserves_invalid_coeng_and_unknown_character_states():
    assert parse_orthographic_syllable("ក្").status == "PARSED"
    assert parse_orthographic_syllable("កx").status == "INVALID_OR_UNSUPPORTED"


def test_parser_preserves_exact_codepoint_component_spans():
    result = parse_orthographic_syllable("🧪ខ្ញុំ")
    assert result.status == "EVIDENCE_LIMITED"
    assert result.component_spans[0] == (0, 1)
    assert result.component_spans[1] == (1, 2)
