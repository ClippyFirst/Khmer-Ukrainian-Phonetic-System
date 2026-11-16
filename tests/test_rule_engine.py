from khmer_ua.rule_engine import RuleBasedKhmerEngine
from khmer_ua import HybridKhmerEngine, create_hybrid_engine


def test_lexical_fixture_uses_fixed_ipa_and_ukrainian_policy():
    result = RuleBasedKhmerEngine().analyze("ខ្មែរ")
    assert result["ipa"] == "kʰmae"
    assert result["ukrainian"] == "к'мае"
    assert result["deterministic"] is True
    assert result["engine"] == "khmer-deterministic-rules-v1"


def test_known_negative_fixture_withholds_ipa():
    result = RuleBasedKhmerEngine().analyze("ស៊៉ា")
    assert result["ipa"] is None
    assert result["status"] == "EVIDENCE_LIMITED"


def test_rule_fallback_is_repeatable_and_explicitly_proposed():
    engine = RuleBasedKhmerEngine()
    first = engine.analyze("ឆ")
    second = engine.analyze("ឆ")
    assert first == second
    assert first["ipa"] == "cʰɑː"
    assert first["status"] == "PROPOSED"
    assert "KHMER_REGISTER_SERIES_INHERENT_VOWEL" in first["rule_trace"]


def test_unknown_mixed_material_is_not_guessed():
    result = RuleBasedKhmerEngine().analyze("កx")
    assert result["ipa"] is None
    assert result["status"] == "NOT_ESTABLISHED"


def test_hybrid_wrapper_preserves_rule_engine_as_final_authority():
    expected = RuleBasedKhmerEngine().analyze("ខ្មែរ")
    actual = HybridKhmerEngine().analyze("ខ្មែរ")
    assert actual["engine"] == expected["engine"]
    assert actual["ipa"] == expected["ipa"]
    assert actual["ukrainian"] == expected["ukrainian"]
    assert actual["external_candidates"] == []


def test_hybrid_factory_accepts_only_typed_provider_candidates():
    provider = lambda _: {
        "ipa": "kʰmae",
        "profile": "khmer-pph-careful-citation-v1",
        "kind": "PHONETIC_BROAD",
        "status": "PARTIAL",
        "uncertainty": ["not independently adjudicated"],
    }
    result = create_hybrid_engine({"external-model": provider}).analyze("ខ្មែរ")
    assert result["external_candidates"][0]["provider"] == "external-model"
    assert result["ipa"] == RuleBasedKhmerEngine().analyze("ខ្មែរ")["ipa"]


def test_mixed_input_preserves_supported_units_and_marks_only_unresolved_units():
    result = RuleBasedKhmerEngine().analyze("ខ្មែរ ☃")

    assert result["ipa"] == "kʰmae ⟦NOT_ESTABLISHED⟧"
    assert result["ukrainian"] == "к'мае ⟦НЕВСТАНОВЛЕНО⟧"
    assert result["status"] == "NOT_ESTABLISHED"
    assert result["complete"] is False
    assert result["partial"] is True

    typed = result["phonetic_result"]
    assert typed["schema"] == "khmer-phonetic-result/v1"
    assert typed["partial"] is True
    assert typed["units"][0]["ipa"] == "kʰmae"
    assert typed["units"][0]["provenance"]["phonology"] == ["wiktionary:khmae"]
    assert typed["units"][0]["provenance"]["target_policy"] == ["data/ukrainian/practical-policy.json"]
    assert typed["units"][1]["status"] == "NOT_ESTABLISHED"
    assert typed["units"][1]["uncertainty"][0]["status"] == "NOT_ESTABLISHED"


def test_reported_khmer_spelling_is_structural_not_phonetically_established():
    result = RuleBasedKhmerEngine().analyze("ព្រះរាជាណាចក្រ")

    assert result["complete"] is False
    assert result["ipa"].count("⟦NOT_ESTABLISHED⟧") >= 1
    assert all(unit["status"] != "INVALID_OR_UNSUPPORTED" for unit in result["units"])


def test_python_engine_preserves_punctuation_and_source_order():
    result = RuleBasedKhmerEngine().analyze("ខ្មែរ, ☃!")

    assert result["units"][0]["source"] == "ខ្មែរ"
    assert result["units"][1]["source"] == ","
    assert result["units"][2]["source"] == " "
    assert result["units"][3]["source"] == "☃"
    assert result["units"][4]["source"] == "!"
    assert result["ipa"] == "kʰmae, ⟦NOT_ESTABLISHED⟧!"
