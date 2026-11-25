import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = runpy.run_path(str(ROOT / "scripts" / "benchmark_nckl_phonemizer_bridge.py"))
phonemize_respelling = MODULE["phonemize_respelling"]
source_ipa_comparison_key = MODULE["source_ipa_comparison_key"]
build_report = MODULE["build_report"]


def test_respelling_bridge_preserves_model_syllable_boundaries():
    calls = []

    def fake_phonemizer(syllable):
        calls.append(syllable)
        return "ipa:" + syllable

    assert phonemize_respelling("កា-ពុ-ជា", fake_phonemizer) == "ipa:កា.ipa:ពុ.ipa:ជា"
    assert calls == ["កា", "ពុ", "ជា"]


def test_respelling_bridge_rejects_empty_syllables_and_non_string():
    def fake_phonemizer(value):
        return "ipa"

    for value in ("កា--ជា", "-កា", "កា-", "", None):
        try:
            phonemize_respelling(value, fake_phonemizer)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected invalid respelling to fail: {value!r}")


def test_source_ipa_comparison_key_removes_notation_only():
    assert source_ipa_comparison_key("/pʰiə.ˈsaː/") == "pʰiəsaː"
    assert source_ipa_comparison_key("kʰmae") == "kʰmae"
    assert source_ipa_comparison_key("/kʰmaeː/") != source_ipa_comparison_key("/kʰmae/")


def test_bridge_report_is_aggregate_only_and_never_accuracy():
    corpus = {
        "ខ្មែរ": {
            "ipa": "/kʰmae/",
            "ipa_status": "SOURCE_ATTESTED_NOT_INDEPENDENTLY_ADJUDICATED",
            "sources": ["https://example.invalid/khmer"],
        },
        "ភាសា": {
            "ipa": "/pʰiə.ˈsaː/",
            "ipa_status": "SOURCE_ATTESTED_NOT_INDEPENDENTLY_ADJUDICATED",
            "sources": ["https://example.invalid/language"],
        },
    }
    respellings = {"ខ្មែរ": "ខ្មែរ", "ភាសា": "ភា-សា"}
    direct = {"ខ្មែរ": "kʰmae", "ភាសា": "pʰiəsaː"}
    bridge = {"ខ្មែរ": "kʰmae", "ភាសា": "pʰiəsaː"}
    report = build_report(
        corpus,
        respellings,
        direct,
        bridge,
        model_revision="7dbc6c3d1c1f5a9a8763be602fa679f130f20dca",
        phonemizer_version="0.0.3",
        corpus_sha256="a" * 64,
    )

    assert report["input_count"] == 2
    assert report["independent_gold_count"] == 0
    assert report["accuracy"] is None
    assert report["profile_match"] == "UNVERIFIED"
    assert report["direct_phonemizer"]["strict_source_attested_matches"] == 2
    assert report["nckl_respelling_phonemizer"]["strict_source_attested_matches"] == 2
    assert report["nckl_respelling_phonemizer"]["character_error_rate"] == 0
    assert "ខ្មែរ" not in str(report)
    assert "kʰmae" not in str(report)
    assert "pʰiəsaː" not in str(report)
    assert "ipa" not in report["records"][0]


def test_bridge_report_rejects_misaligned_prediction_maps():
    corpus = {"ខ្មែរ": {"ipa": "/kʰmae/", "ipa_status": "SOURCE_ATTESTED_NOT_INDEPENDENTLY_ADJUDICATED"}}
    try:
        build_report(
            corpus,
            {},
            {"ខ្មែរ": "kʰmae"},
            {"ខ្មែរ": "kʰmae"},
            model_revision="revision",
            phonemizer_version="0.0.3",
            corpus_sha256="b" * 64,
        )
    except ValueError as error:
        assert "one respelling and two IPA outputs per input" in str(error)
    else:
        raise AssertionError("expected prediction-map mismatch to fail")

def test_whole_respelling_preserves_hyphen_boundaries_for_phonemizer():
    calls = []

    def fake_phonemizer(value):
        calls.append(value)
        return "ipa:" + value

    assert MODULE["phonemize_respelling_whole"]("កា-ពុ-ជា", fake_phonemizer) == "ipa:កា-ពុ-ជា"
    assert calls == ["កា-ពុ-ជា"]


def test_spaced_respelling_passes_word_separators_without_splitting():
    calls = []

    def fake_phonemizer(value):
        calls.append(value)
        return "ipa:" + value

    assert MODULE["phonemize_respelling_spaced"]("កា-ពុ-ជា", fake_phonemizer) == "ipa:កា ពុ ជា"
    assert calls == ["កា ពុ ជា"]
