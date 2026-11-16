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


def test_unknown_non_khmer_material_does_not_pass_as_established_structure():
    r = analyze("កx")

    assert r.syllables[0]["status"] == "INVALID_OR_UNSUPPORTED"
    assert r.status == "INVALID_OR_UNSUPPORTED"
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
    assert parsed.phonology == {"onset_ipa": "pʰ"} or parsed.phonology.get("onset_ipa") is not None
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
