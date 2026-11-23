import pytest

from khmer_ua.parser import analyze
from khmer_ua.normalize import normalize_khmer

def test_nfc_is_stable():
    assert normalize_khmer("ខ្ញុំ") == "ខ្ញុំ"

def test_coeng_is_structural():
    r=analyze("ខ្ញុំ")
    s=r.syllables[0]
    assert "ញ" in s["subscripts"]
    assert s["base_consonant"]=="ខ"

def test_register_is_not_character_to_ua_mapping():
    r=analyze("កគ")
    assert r.syllables[0]["register"]=="first"
    assert r.syllables[1]["register"]=="second"

def test_independent_vowel():
    r=analyze("ឥ")
    assert r.syllables[0]["independent_vowel"]=="ឥ"

def test_malformed_sequence_is_not_confident():
    r=analyze("្")
    assert r.confidence==0.0
    assert r.syllables[0]["status"]=="INVALID_OR_UNSUPPORTED"
    assert r.status=="INVALID_OR_UNSUPPORTED"

def test_complex_unicode_examples():
    r=analyze("សង្គ្រាម")
    assert r.syllables[0]["subscripts"] == ["គ","រ"]


def test_unknown_non_khmer_material_isolated_from_supported_neighbor():
    r = analyze("កx")

    assert [unit["raw_text"] for unit in r.syllables] == ["ក", "x"]
    assert r.syllables[0]["status"] == "ESTABLISHED_STRUCTURE"
    assert r.syllables[1]["status"] == "INVALID_OR_UNSUPPORTED"
    assert r.status == "EVIDENCE_LIMITED"
    assert r.confidence == 0.0


def test_every_assigned_khmer_letter_and_mark_has_a_lossless_parser_record():
    import unicodedata

    from khmer_ua.parser import decompose_khmer_syllable, segment_syllables

    ranges = ((0x1780, 0x17FF), (0x19E0, 0x19FF))
    tested = 0
    for start, end in ranges:
        for codepoint in range(start, end + 1):
            char = chr(codepoint)
            if unicodedata.category(char)[0] not in {"L", "M"}:
                continue
            units = segment_syllables(char)
            assert "".join(units) == char, f"source lost for U+{codepoint:04X}"
            assert len(units) == 1
            parsed = decompose_khmer_syllable(units[0])
            assert "".join(item.text for item in parsed.graphemes) == char
            assert [cp for item in parsed.graphemes for cp in item.codepoints] == [
                f"U+{codepoint:04X}"
            ]
            tested += 1
    assert tested > 0


def test_unmodelled_khmer_letter_is_traced_as_unknown_not_as_ipa():
    from khmer_ua.parser import decompose_khmer_syllable

    # U+17F9 is a Khmer symbol rather than a consonant or vowel phoneme.
    parsed = decompose_khmer_syllable(chr(0x17F9))
    assert parsed.graphemes
    assert parsed.graphemes[0].codepoints == ("U+17F9",)
    assert parsed.status == "INVALID_OR_UNSUPPORTED"


def test_unmodelled_khmer_letters_are_explicitly_classified_without_ipa():
    from khmer_ua.parser import decompose_khmer_syllable

    expected = {
        chr(0x17A3): "U+17A3",
        chr(0x17A4): "U+17A4",
        chr(0x179D): "U+179D",
        chr(0x179E): "U+179E",
    }
    for char, codepoint in expected.items():
        parsed = decompose_khmer_syllable(char)
        assert parsed.status == "INVALID_OR_UNSUPPORTED"
        assert parsed.graphemes[0].kind == "unmodeled_letter"
        assert parsed.graphemes[0].codepoints == (codepoint,)


def test_unknown_khmer_material_does_not_drop_following_graphemes():
    from khmer_ua.parser import decompose_khmer_syllable

    source = "កxយ"
    parsed = decompose_khmer_syllable(source)
    assert parsed.status == "INVALID_OR_UNSUPPORTED"
    assert "".join(item.text for item in parsed.graphemes) == source
    assert [cp for item in parsed.graphemes for cp in item.codepoints] == [
        "U+1780", "U+0078", "U+1799"
    ]

def test_syllable_chaining_example_does_not_claim_phonetic_syllabification():
    # Unicode L2/22-290 gives this orthographic sequence as an example where
    # phonetic syllables and orthographic units do not correspond one-to-one.
    source = "".join(chr(cp) for cp in (
        0x179F, 0x1784, 0x17D2, 0x1782, 0x17D2, 0x179A, 0x17B6, 0x1798
    ))
    result = analyze(source)

    assert result.normalized == source
    assert result.phonetic_representation == {
        "status": "phoneticization_not_yet_established"
    }
    assert "".join(
        grapheme["text"]
        for syllable in result.syllables
        for grapheme in syllable["graphemes"]
    ) == source


def test_subscript_independent_vowel_is_a_structural_unit_not_a_phonetic_claim():
    from khmer_ua.parser import decompose_khmer_syllable

    # Unicode 18 Chapter 16 uses ផ្ឯម as an example of coeng + independent vowel.
    source = "ផ្ឯម"
    parsed = decompose_khmer_syllable(source)

    assert parsed.status == "ESTABLISHED_STRUCTURE"
    assert parsed.base_consonant == "ផ"
    assert parsed.subscripts == []
    assert parsed.subscript_independent_vowels == ["ឯ"]
    assert [(item.text, item.kind, item.codepoints) for item in parsed.graphemes] == [
        ("ផ", "consonant", ("U+1795",)),
        ("្ឯ", "subscript_independent_vowel", ("U+17D2", "U+17AF")),
        ("ម", "consonant", ("U+1798",)),
    ]
    assert parsed.ipa is None
    from khmer_ua.parser import analyze, segment_syllables
    assert segment_syllables(source) == [source]
    analyzed = analyze(source)
    assert len(analyzed.syllables) == 1
    assert analyzed.syllables[0]["subscript_independent_vowels"] == ["ឯ"]
    assert "unicode18-ch16" in analyzed.sources
    assert analyzed.phonetic_representation == {"status": "phoneticization_not_yet_established"}
    assert "unicode18-ch16" in parsed.sources


def test_coeng_pair_protection_uses_exact_source_codepoint_offsets():
    from khmer_ua.parser import khmer_subscript_sequence_spans
    from khmer_ua.word_boundaries import BoundaryCandidate, WordBoundaryAnalysis

    source = "🧪ផ្ឯម"
    spans = khmer_subscript_sequence_spans(source)
    assert spans == ((2, 4),)
    with pytest.raises(ValueError, match="splits a protected cluster"):
        WordBoundaryAnalysis(
            source,
            (BoundaryCandidate("split-coeng-pair", (3,), "PROPOSED"),),
            cluster_spans=spans,
        )


def test_coeng_pair_protection_does_not_claim_complete_syllable_boundaries():
    from khmer_ua.parser import khmer_subscript_sequence_spans

    assert khmer_subscript_sequence_spans("ខ្ញុំ") == ((1, 3),)
    assert khmer_subscript_sequence_spans("កx") == ()
    assert khmer_subscript_sequence_spans("្") == ()


def test_analysis_exposes_orthographic_component_scan_without_changing_ipa_claims():
    result = analyze("ខ្ញុំ")
    syllable = result.syllables[0]
    assert syllable["orthographic_structure_status"] == "ESTABLISHED_STRUCTURE"
    assert [(item["role"], item["text"], item["start"], item["end"]) for item in syllable["orthographic_components"]] == [
        ("BASE", "ខ", 0, 1),
        ("SUBSCRIPT", "្ញ", 1, 3),
        ("VOWEL", "ុ", 3, 4),
        ("OTHER_SIGN", "ំ", 4, 5),
    ]
    assert result.phonetic_representation == {"status": "phoneticization_not_yet_established"}


def test_mixed_script_and_numeric_runs_are_isolated_without_source_loss():
    from khmer_ua.parser import segment_syllables

    source = "កLlenguatgeគឆ្នាំ៦១១។"
    units = segment_syllables(source)

    assert "".join(units) == source
    assert "Llenguatge" in units
    assert "៦១១" in units
    assert not any("L" in unit and "ក" in unit for unit in units)
    assert units[-2:] == ["៦១១", "។"]



def test_zwnj_does_not_split_a_khmer_orthographic_unit():
    from khmer_ua.parser import segment_syllables

    source = "ប\u200C៊"
    assert segment_syllables(source) == [source]


def test_unicode18_subscript_independent_vowel_keeps_following_coda_in_same_unit():
    from khmer_ua.parser import segment_syllables

    # Unicode 18 §16 example: a consonant after a subscript independent vowel
    # is not an automatic orthographic syllable boundary.
    assert segment_syllables("ផ្ឯម") == ["ផ្ឯម"]
