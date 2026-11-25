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
