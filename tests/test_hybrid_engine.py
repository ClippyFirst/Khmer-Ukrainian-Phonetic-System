import pytest

from khmer_ua import HybridKhmerEngine, RuleBasedKhmerEngine, create_hybrid_engine, make_khmerphonemizer_backend


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



def test_mappable_external_ipa_is_exposed_as_provisional_when_internal_ipa_is_unresolved():
    source = "កម្ពុជាប្រជាធិបតេយ្យ"
    baseline = RuleBasedKhmerEngine().analyze(source)
    result = HybridKhmerEngine({
        "khmer-phonemizer": lambda _: typed("/kɑː/")
    }).analyze(source)

    assert result["ipa"] == baseline["ipa"]
    assert result["ukrainian"] == baseline["ukrainian"]
    candidate = result["provisional_candidate"]
    assert candidate["status"] == "PROVISIONAL"
    assert candidate["provider"] == "khmer-phonemizer"
    assert candidate["ipa"] == "/kɑː/"
    assert candidate["ukrainian"] == "ка"
    assert "not independently adjudicated" in candidate["uncertainty"][0]



def test_valid_external_ipa_is_retained_even_when_ukrainian_mapping_is_missing():
    source = "កម្ពុជាប្រជាធិបតេយ្យ"
    result = HybridKhmerEngine({
        "khmer-phonemizer": lambda _: typed("q")
    }).analyze(source)

    candidate = result["provisional_candidate"]
    assert candidate["ipa"] == "q"
    assert candidate["status"] == "PROVISIONAL"
    assert candidate["ukrainian"] is None
    assert candidate["ukrainian_mapping_failure"] == "q"


def test_hybrid_prefers_first_ukrainian_mappable_candidate_without_dropping_other_ipa():
    result = HybridKhmerEngine({
        "khmer-phonemizer": lambda _: typed("/kɑː/"),
        "mekongphon": lambda _: typed("q"),
    }).analyze("កម្ពុជាប្រជាធិបតេយ្យ")

    assert [item["provider"] for item in result["external_candidates"]] == [
        "mekongphon", "khmer-phonemizer"
    ]
    assert result["external_candidates"][0]["ukrainian_candidate"] is None
    assert result["external_candidates"][1]["ukrainian_candidate"] == "ка"
    assert result["provisional_candidate"]["provider"] == "khmer-phonemizer"
    assert result["provisional_candidate"]["ukrainian"] == "ка"

def test_khmerphonemizer_adapter_returns_token_aligned_partial_ipa(monkeypatch):
    import sys
    from types import SimpleNamespace

    def fake_phonemize(text):
        assert text == "ខ្មែរ"
        return ["ខ្មែរ"], [["k", "ʰ", "m", "a", "e"]]

    monkeypatch.setitem(sys.modules, "khmerphonemizer", SimpleNamespace(phonemize=fake_phonemize))
    candidate = make_khmerphonemizer_backend()("ខ្មែរ")
    assert candidate["ipa"] == "kʰmae"
    assert candidate["status"] == "PARTIAL"
    assert candidate["kind"] == "PHONETIC_BROAD"
    assert candidate["profile_match"] == "UNVERIFIED"
    assert candidate["provenance"]["license"] == "MIT"


def test_hybrid_factory_can_opt_in_to_lazy_khmerphonemizer_provider():
    engine = create_hybrid_engine(include_khmerphonemizer=True)
    assert isinstance(engine, HybridKhmerEngine)
    assert "khmer-phonemizer" in engine.providers

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
