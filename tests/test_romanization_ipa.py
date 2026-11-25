from khmer_ua.romanization_ipa import build_romanization_ipa_candidate


def test_confirms_romanized_onset_only_against_source_consonant_class():
    result = build_romanization_ipa_candidate("ខ្មែរ", "khmer")
    assert result["status"] == "PROVISIONAL"
    assert result["typed_ipa"].status == "PROVISIONAL"
    assert [segment.ipa for segment in result["typed_ipa"].segments] == ["kʰ", "?"]
    assert result["ukrainian"] == "к'???"
    assert "PCGN-ONSET-KH" in result["provenance"]


def test_rejects_romanization_token_conflicting_with_source_onset():
    result = build_romanization_ipa_candidate("ក", "kh")
    assert result["status"] == "UNRESOLVED"
    assert result["ukrainian"] == "???"


def test_does_not_guess_context_sensitive_pcgn_b_p_alternation():
    result = build_romanization_ipa_candidate("ប", "b")
    assert result["status"] == "UNRESOLVED"
    assert "AMBIGUOUS" in " ".join(result["uncertainty"])


def test_never_infers_vowel_from_ascii_romanization():
    result = build_romanization_ipa_candidate("ខ្មែរ", "khmer")
    assert result["typed_ipa"].phonemic_ipa is None
    assert any(segment.kind == "unknown" for segment in result["typed_ipa"].segments)
    assert "VOWEL_CODA_AND_SYLLABLE_NOT_ESTABLISHED" in result["uncertainty"]


def test_coeng_only_subscript_is_not_an_independent_onset():
    result = build_romanization_ipa_candidate("្ក", "k")
    assert result["status"] == "UNRESOLVED"


def test_provisional_segments_keep_provenance_and_certainty():
    result = build_romanization_ipa_candidate("ង", "ng")
    assert result["status"] == "PROVISIONAL"
    assert all(segment.certainty == "PROVISIONAL" for segment in result["typed_ipa"].segments)
    assert all(segment.provenance for segment in result["typed_ipa"].segments)


def test_exact_representative_series_vowels_are_provisional_without_unknown_tail():
    fixtures = (
        ("ក", "ka", "kɑː"),
        ("គ", "ko", "kɔː"),
        ("កី", "kei", "kəj"),
        ("គី", "ki", "kiː"),
        ("កា", "ka", "kaː"),
        ("គា", "kea", "kiə"),
    )
    for source, romanized, expected_ipa in fixtures:
        result = build_romanization_ipa_candidate(source, romanized)
        assert result["status"] == "PROVISIONAL"
        assert result["typed_ipa"].status == "PROVISIONAL"
        assert "".join(segment.ipa for segment in result["typed_ipa"].segments) == expected_ipa
        assert all(segment.certainty == "PROVISIONAL" for segment in result["typed_ipa"].segments)
        assert all(segment.kind != "unknown" for segment in result["typed_ipa"].segments)
        assert "NOT_GENERALIZED_TO_OTHER_VOWEL_OR_CODA_CONTEXTS" in result["uncertainty"]


def test_unlisted_vowel_signs_remain_unknown_instead_of_being_extrapolated():
    unlisted = (
        ("កិ", "ke"), ("គិ", "ki"), ("កឹ", "koe"), ("គឹ", "koe"),
        ("កឺ", "koe"), ("គឺ", "koe"), ("កុ", "ko"), ("គុ", "ku"),
        ("កូ", "ko"), ("គូ", "ku"), ("កេ", "ke"), ("គេ", "ke"),
        ("កែ", "ke"), ("គែ", "ke"), ("កៃ", "kai"), ("គៃ", "key"),
        ("កោ", "kao"), ("គោ", "ko"), ("កៅ", "kau"), ("គៅ", "kou"),
        ("កើ", "kaeu"), ("គើ", "keu"), ("កឿ", "koea"), ("គឿ", "koea"),
        ("កួ", "kuo"), ("គួ", "kuo"),
    )
    for source, romanized in unlisted:
        result = build_romanization_ipa_candidate(source, romanized)
        assert result["status"] == "PROVISIONAL", (source, romanized)
        assert result["romanized_onset"] == "k", (source, romanized)
        assert result["typed_ipa"].phonemic_ipa is None, (source, romanized)
        assert any(segment.kind == "unknown" for segment in result["typed_ipa"].segments), (source, romanized)


def test_wrong_romanization_for_an_exact_vowel_fixture_does_not_reuse_its_ipa():
    for source, romanized in (("កី", "ki"), ("គី", "kei")):
        result = build_romanization_ipa_candidate(source, romanized)
        assert result["status"] == "PROVISIONAL"
        assert result["typed_ipa"].phonemic_ipa is None
        assert any(segment.kind == "unknown" for segment in result["typed_ipa"].segments)
