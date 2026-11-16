from khmer_ua.orthographic_structure import scan_orthographic_components


def test_unicode_18_component_roles_and_exact_offsets():
    source = "ខ្ញុំ"
    scan = scan_orthographic_components(source)

    assert scan.status == "ESTABLISHED_STRUCTURE"
    assert [(item.role, item.text, item.start, item.end) for item in scan.components] == [
        ("BASE", "ខ", 0, 1),
        ("SUBSCRIPT", "្ញ", 1, 3),
        ("VOWEL", "ុ", 3, 4),
        ("OTHER_SIGN", "ំ", 4, 5),
    ]
    assert scan.component_spans == ((0, 1), (1, 3), (3, 4), (4, 5))
    assert scan.to_dict()["offset_unit"] == "unicode_code_point"


def test_scanner_recognizes_unicode_18_orthographic_component_examples_losslessly():
    examples = (
        "ច្រើន",
        "សង្គ្រាម",
        "ហើ្យ",
        "សញ្ញា",
        "ស៊ី",
        "ប៉ី",
        "ម៉្ងៃ",
        "ប‌៊ីយែរ",
        "ផ្ឯម",
        "អាយ៌",
        "ពត៌មាន",
    )
    for source in examples:
        scan = scan_orthographic_components(source)
        assert "".join(item.text for item in scan.components) == source
        assert all(item.end > item.start for item in scan.components)
        assert all(item.codepoints for item in scan.components)


def test_scanner_keeps_subscript_independent_vowel_as_one_atomic_component():
    scan = scan_orthographic_components("ផ្ឯម")
    assert ("SUBSCRIPT", "្ឯ", 1, 3) in [
        (item.role, item.text, item.start, item.end) for item in scan.components
    ]


def test_scanner_marks_unsubscripted_base_ambiguity_instead_of_splitting():
    scan = scan_orthographic_components("សង្គ្រាម")
    assert scan.status == "EVIDENCE_LIMITED"
    assert any(item.status == "AMBIGUOUS_BASE_ROLE" for item in scan.components)
    assert any("coda versus syllable boundary" in note for note in scan.notes)


def test_scanner_fails_closed_for_malformed_coeng_and_unknown_characters():
    malformed = scan_orthographic_components("ក្")
    assert malformed.status == "INVALID_OR_UNSUPPORTED"
    assert any(item.status == "MALFORMED_COENG" for item in malformed.components)

    unknown = scan_orthographic_components("កx")
    assert unknown.status == "INVALID_OR_UNSUPPORTED"
    assert "".join(item.text for item in unknown.components) == "កx"


def test_scanner_offsets_are_codepoints_and_input_is_not_normalized():
    source = "🧪ខ្ញុំ"
    scan = scan_orthographic_components(source)
    assert scan.components[0].start == 0
    assert scan.components[0].end == 1
    assert scan.components[1].start == 1
    assert scan.components[1].end == 2
    assert scan.components[2].start == 2
    assert scan.components[2].end == 4


def test_component_schema_matches_serialized_scan_contract():
    import json
    from pathlib import Path

    schema = json.loads(Path("schemas/orthographic-components.schema.json").read_text(encoding="utf-8"))
    payload = scan_orthographic_components("ខ្ញុំ").to_dict()
    assert payload["schema"] == schema["properties"]["schema"]["const"]
    assert set(payload) == set(schema["required"])
    assert all(set(component) == set(schema["properties"]["components"]["items"]["required"]) for component in payload["components"])
