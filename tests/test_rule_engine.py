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


def test_unknown_mixed_material_is_isolated_without_erasing_supported_neighbor():
    result = RuleBasedKhmerEngine().analyze("កx")
    assert result["ipa"] == "kɑː⟦INVALID_OR_UNSUPPORTED⟧"
    assert result["ukrainian"] == "ка⟦НЕПІДТРИМУЄТЬСЯ⟧"
    assert result["status"] == "EVIDENCE_LIMITED"
    assert [unit["source"] for unit in result["units"]] == ["ក", "x"]


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

    assert result["ipa"] == "kʰmae ⟦INVALID_OR_UNSUPPORTED⟧"
    assert result["ukrainian"] == "к'мае ⟦НЕПІДТРИМУЄТЬСЯ⟧"
    assert result["status"] == "EVIDENCE_LIMITED"
    assert result["complete"] is False
    assert result["partial"] is True

    typed = result["phonetic_result"]
    assert typed["schema"] == "khmer-phonetic-result/v1"
    assert typed["partial"] is True
    assert typed["units"][0]["ipa"] == "kʰmae"
    assert typed["units"][0]["ipa_kind"] == "UNRESOLVED"
    assert typed["units"][0]["rule_trace"] == ["KHMER_LEXICAL_FIXTURE", "IPA_TO_UKRAINIAN_LONGEST_MATCH"]
    assert typed["units"][0]["provenance"]["phonology"] == ["wiktionary:khmae"]
    assert typed["units"][0]["provenance"]["target_policy"] == ["data/ukrainian/practical-policy.json"]
    assert typed["units"][1]["status"] == "PUNCTUATION"
    assert typed["units"][1]["ipa_kind"] == "NOT_APPLICABLE"
    assert typed["units"][2]["status"] == "INVALID_OR_UNSUPPORTED"
    assert typed["units"][2]["ipa_kind"] == "UNRESOLVED"
    assert typed["units"][2]["uncertainty"][0]["status"] == "INVALID_OR_UNSUPPORTED"


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
    assert result["ipa"] == "kʰmae, ⟦INVALID_OR_UNSUPPORTED⟧!"


def test_typed_phonetic_result_matches_published_json_schema_shape():
    import json
    from pathlib import Path

    schema = json.loads(Path("schemas/phonetic-result.schema.json").read_text(encoding="utf-8"))
    result = RuleBasedKhmerEngine().analyze("ខ្មែរ ☃")["phonetic_result"]
    assert result["schema"] == schema["properties"]["schema"]["const"]
    assert result["pipeline"] == schema["properties"]["pipeline"]["const"]
    assert set(schema["required"]).issubset(result)
    assert result["units"]
    unit_schema = schema["$defs"]["unit"]
    for unit in result["units"]:
        assert set(unit_schema["required"]).issubset(unit)
        assert set(unit) == set(unit_schema["properties"])
        assert set(unit["provenance"]) == {"structure", "phonology", "target_policy"}
        assert isinstance(unit["rule_trace"], list)
        assert isinstance(unit["uncertainty"], list)
        for uncertainty in unit["uncertainty"]:
            assert set(unit_schema["properties"]["uncertainty"]["items"]["required"]).issubset(uncertainty)


def test_internal_ipa_kind_stays_explicitly_unresolved_until_convention_approval():
    result = RuleBasedKhmerEngine().analyze("ឆ")
    assert result["ipa"] == "cʰɑː"
    assert result["status"] == "PROPOSED"
    unit = result["phonetic_result"]["units"][0]
    assert unit["ipa_kind"] == "UNRESOLVED"
    assert unit["profile"] == "khmer-pph-careful-citation-v1"
