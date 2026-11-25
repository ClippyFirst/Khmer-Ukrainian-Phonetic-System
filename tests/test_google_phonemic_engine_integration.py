from khmer_ua.rule_engine import RuleBasedKhmerEngine


def test_google_lexicon_candidate_is_auxiliary_and_never_overwrites_canonical_abstention():
    result = RuleBasedKhmerEngine().analyze("ព្រះរាជាណាចក្រ")
    assert result["status"] == "NOT_ESTABLISHED"
    assert result["complete"] is False
    assert "⟦NOT_ESTABLISHED⟧" in result["ipa"]
    candidates = result["provisional_candidates"]
    assert candidates
    assert all(item["candidate_type"] == "GOOGLE_PHONEMIC_LEXICON" for item in candidates)
    assert all(item["status"] == "PROVISIONAL" and item["ipa_kind"] == "PHONEMIC" for item in candidates)
    assert all(item["source_row"] > 0 and item["ukrainian"] for item in candidates)
    assert all("AUXILIARY_CANDIDATE_DOES_NOT_REPLACE_CANONICAL_ENGINE_OUTPUT" in item["uncertainty"] for item in candidates)


def test_google_lexicon_does_not_override_existing_deterministic_rule_output():
    result = RuleBasedKhmerEngine().analyze("ឆ")
    assert result["ipa"] == "cʰɑː"
    assert result["status"] == "PROPOSED"
    assert result["provisional_candidates"] == []
