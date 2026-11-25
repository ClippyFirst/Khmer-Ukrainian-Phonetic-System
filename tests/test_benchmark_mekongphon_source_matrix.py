import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = runpy.run_path(str(ROOT / "scripts" / "benchmark_mekongphon_source_matrix.py"))
load_source_cases = MODULE["load_source_cases"]
build_report = MODULE["build_report"]
normalize_ipa = MODULE["normalize_ipa"]


def test_source_matrix_selects_only_explicit_non_conflicting_ipa_cases():
    register = {
        "schema_version": "1.0.0",
        "cases": [
            {
                "id": "KHV-001",
                "orthography": "ក",
                "ipa": "/kɑː/",
                "ipa_source": "r12a-orthography",
                "status": "SOURCE_ATTESTED_NOT_GOLD",
                "evidence_level": "SOURCE_ATTESTED_NOT_GOLD",
                "limitations": ["representative form only"],
            },
            {
                "id": "KHV-002",
                "orthography": "គ",
                "ipa": None,
                "ipa_source": "unicode17-ch16",
                "status": "CONFLICTING_SOURCE_ANALYSES",
                "evidence_level": "CONFLICTING_SOURCE_ANALYSES",
                "limitations": ["conflicting analyses"],
            },
            {
                "id": "KHV-003",
                "orthography": "កា",
                "ipa": "[kaː]",
                "ipa_source": "r12a-orthography",
                "status": "SOURCE_ATTESTED_NOT_GOLD",
                "evidence_level": "SOURCE_ATTESTED_NOT_GOLD",
                "limitations": ["representative form only"],
            },
        ],
    }

    cases = load_source_cases(register)
    assert [case["id"] for case in cases] == ["KHV-001", "KHV-003"]
    assert normalize_ipa(cases[0]["ipa"]) == "kɑː"
    assert normalize_ipa(cases[1]["ipa"]) == "kaː"


def test_source_matrix_report_is_diagnostic_only_and_does_not_leak_rows():
    cases = [
        {"id": "KHV-001", "orthography": "ក", "ipa": "/kɑː/", "ipa_source": "r12a-orthography"},
        {"id": "KHV-005", "orthography": "កា", "ipa": "/kaː/", "ipa_source": "r12a-orthography"},
    ]
    report = build_report(
        cases,
        ["kɑː", "ka"],
        model_revision="20e069d384b240da76320e1569958568c12a54bc",
        corpus_sha256="a" * 64,
    )

    assert report["input_count"] == 2
    assert report["decoding"] == "greedy"
    assert report["source_attested_diagnostic"]["strict_matches"] == 1
    assert report["source_attested_diagnostic"]["character_errors"] == 1
    assert report["independent_gold_count"] == 0
    assert report["accuracy"] is None
    assert report["score_status"] == "SOURCE_ATTESTED_DIAGNOSTIC_NOT_ACCURACY"
    assert report["rule_promotion"] == "BLOCKED_INSUFFICIENT_CONTEXT_AND_INDEPENDENT_GOLD"
    assert report["records"][0]["case_id"] == "KHV-001"
    assert "orthography" not in report["records"][0]
    assert "raw_output" not in report["records"][0]
    assert "reference" not in report["records"][0]


def test_source_matrix_report_rejects_prediction_count_mismatch():
    cases = [{"id": "KHV-001", "orthography": "ក", "ipa": "/kɑː/", "ipa_source": "r12a-orthography"}]
    try:
        build_report(
            cases,
            [],
            model_revision="revision",
            corpus_sha256="b" * 64,
        )
    except ValueError as error:
        assert "one prediction per source case" in str(error)
    else:
        raise AssertionError("expected a prediction-count error")


def test_source_ipa_normalization_removes_only_outer_delimiters_and_nfc():
    assert normalize_ipa(" /kʰmae/ ") == "kʰmae"
    assert normalize_ipa("[kɑː]") == "kɑː"
    assert normalize_ipa("k.a") == "k.a"
    assert normalize_ipa("k  a") == "k  a"
