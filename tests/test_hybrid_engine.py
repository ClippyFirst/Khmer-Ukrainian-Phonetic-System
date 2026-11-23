import pytest

from khmer_ua import HybridKhmerEngine, RuleBasedKhmerEngine, create_hybrid_engine


def typed(ipa, *, status="PARTIAL", uncertainty=("not independently adjudicated",), kind="PHONETIC_BROAD"):
    return {
        "ipa": ipa,
        "profile": "khmer-pph-careful-citation-v1",
        "kind": kind,
        "status": status,
        "uncertainty": uncertainty,
        "provenance": {"revision": "test-fixture"},
    }


def test_hybrid_without_providers_is_identical_to_rule_engine():
    source = "ខ្មែរ"
    expected = RuleBasedKhmerEngine().analyze(source)
    actual = HybridKhmerEngine().analyze(source)
    assert actual["ipa"] == expected["ipa"]
    assert actual["ukrainian"] == expected["ukrainian"]
    assert actual["external_candidates"] == []


def test_provider_candidate_uses_typed_ipa_boundary_and_preserves_raw_string():
    raw = "/ˈkʰmaeː˥.t͡ɕa/"
    result = HybridKhmerEngine({"mekongphon": lambda _: typed(raw)}).analyze("ខ្មែរ")
    candidate = result["external_candidates"][0]
    assert candidate["ipa_raw"] == raw
    assert candidate["status"] == "PARTIAL"
    assert candidate["uncertainty"] == ["not independently adjudicated"]
    assert candidate["promotion"].startswith("WITHHELD")
    assert result["ipa"] == RuleBasedKhmerEngine().analyze("ខ្មែរ")["ipa"]


def test_unresolved_canonical_exposes_first_mappable_provider_candidate_without_overwriting_it():
    canonical = RuleBasedKhmerEngine().analyze("ក្ក")
    result = HybridKhmerEngine({
        "mekongphon": lambda _: typed("kampucieprɑcietʰiʔpaʔtay"),
        "khmer-phonemizer": lambda _: typed("kʰmae"),
    }).analyze("ក្ក")

    assert result["ipa"] == canonical["ipa"]
    assert result["ukrainian"] == canonical["ukrainian"]
    assert result["external_candidates"][0]["ukrainian_candidate"] is None
    assert result["external_candidates"][0]["ukrainian_mapping_failure"] == "y"
    assert result["external_candidates"][1]["ukrainian_candidate"] == "к'мае"
    candidate = result["provisional_candidate"]
    assert candidate["provider"] == "khmer-phonemizer"
    assert candidate["ipa"] == "kʰmae"
    assert candidate["ukrainian"] == "к'мае"
    assert candidate["status"] == "PROVISIONAL"
    assert candidate["profile_match"] == "UNVERIFIED"
    assert candidate["uncertainty"]


def test_unmappable_provider_still_exposes_ipa_with_explicit_mapping_failure():
    result = HybridKhmerEngine({
        "mekongphon": lambda _: typed("kampucieprɑcietʰiʔpaʔtay")
    }).analyze("ក្ក")

    candidate = result["provisional_candidate"]
    assert candidate["ipa"] == "kampucieprɑcietʰiʔpaʔtay"
    assert candidate["ukrainian"] is None
    assert candidate["ukrainian_mapping_failure"] == "y"
    assert candidate["status"] == "PROVISIONAL"


def test_bare_string_provider_output_is_rejected():
    result = HybridKhmerEngine({"untyped": lambda _: "kʰmae"}).analyze("ខ្មែរ")
    assert result["external_candidates"] == []
    assert "typed candidate metadata" in result["backend_failures"][0]["reason"]


def test_malformed_ipa_provider_output_is_rejected():
    result = HybridKhmerEngine({"broken": lambda _: typed("ក្មែរ")}).analyze("ខ្មែរ")
    assert result["external_candidates"] == []
    assert "unsupported non-IPA" in result["backend_failures"][0]["reason"]


def test_partial_without_uncertainty_is_rejected():
    result = HybridKhmerEngine({
        "missing-uncertainty": lambda _: typed("kʰmae", uncertainty=())
    }).analyze("ខ្មែរ")
    assert result["external_candidates"] == []
    assert "must include at least one uncertainty" in result["backend_failures"][0]["reason"]


def test_provider_priority_orders_candidates_without_promoting_them():
    calls = []
    providers = {
        "goruut": lambda _: calls.append("goruut") or typed("kʰmae"),
        "khmer-phonemizer": lambda _: calls.append("khmer-phonemizer") or typed("kʰmae"),
        "mekongphon": lambda _: calls.append("mekongphon") or typed("kʰmae"),
    }
    result = HybridKhmerEngine(providers).analyze("ខ្មែរ")
    assert calls == ["mekongphon", "khmer-phonemizer", "goruut"]
    assert [item["priority"] for item in result["external_candidates"]] == [10, 20, 90]
    assert all(item["promotion"].startswith("WITHHELD") for item in result["external_candidates"])


def test_backend_failure_does_not_erase_internal_result():
    result = HybridKhmerEngine({
        "broken": lambda _: (_ for _ in ()).throw(RuntimeError("offline"))
    }).analyze("ខ្មែរ")
    assert result["backend_failures"][0]["reason"] == "offline"
    assert "ipa" in result


def test_factory_exports_typed_hybrid():
    engine = create_hybrid_engine({"provider": lambda _: typed("kʰmae")})
    assert isinstance(engine, HybridKhmerEngine)
    assert len(engine.analyze("ខ្មែរ")["external_candidates"]) == 1


def test_rule_engine_keeps_foreign_script_and_numerals_out_of_adjacent_khmer_units():
    result = RuleBasedKhmerEngine().analyze("កLlenguatgeគ៦១១")
    units = result["units"]

    assert "".join(unit["source"] for unit in units) == "កLlenguatgeគ៦១១"
    assert [unit["source"] for unit in units] == ["ក", "Llenguatge", "គ", "៦១១"]
    assert units[1]["status"] == "INVALID_OR_UNSUPPORTED"
    assert units[3]["status"] == "NON_LINGUISTIC"
    assert units[3]["ipa"] == "៦១១"
    assert units[3]["ukrainian"] == "៦១១"
    typed_numeral = result["phonetic_result"]["units"][3]
    assert typed_numeral["ipa_kind"] == "NOT_APPLICABLE"
    assert typed_numeral["uncertainty"] == []


def test_numeral_only_input_is_preserved_without_claiming_phonetic_output():
    result = RuleBasedKhmerEngine().analyze("៦១១")

    assert result["status"] == "NOT_ESTABLISHED"
    assert result["ipa"] == "៦១១"
    assert result["ukrainian"] == "៦១១"
    assert result["complete"] is False
    assert result["units"][0]["status"] == "NON_LINGUISTIC"
    assert result["phonetic_result"]["units"][0]["ipa_kind"] == "NOT_APPLICABLE"
