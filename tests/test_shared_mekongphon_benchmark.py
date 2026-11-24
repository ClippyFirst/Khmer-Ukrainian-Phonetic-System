import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = runpy.run_path(str(ROOT / "scripts" / "benchmark_shared_mekongphon.py"))
ipa_from_internal_result = MODULE["ipa_from_internal_result"]
evaluate = MODULE["evaluate"]


def test_internal_result_preserves_canonical_and_partial_statuses():
    assert ipa_from_internal_result({"ipa": "kʰmae", "status": "PROPOSED"}) == ("kʰmae", "PROPOSED")
    assert ipa_from_internal_result({
        "ipa": "kʰ⟦NOT_ESTABLISHED⟧",
        "status": "NOT_ESTABLISHED",
    }) == ("kʰ", "PARTIAL_PLACEHOLDER_STRIPPED_FOR_DIAGNOSTIC")
    assert ipa_from_internal_result({
        "ipa": None,
        "provisional_ipa": "s",
        "status": "NOT_ESTABLISHED",
    }) == ("s", "PROVISIONAL_ONSET_PREVIEW")
    assert ipa_from_internal_result({"ipa": None, "status": "NOT_ESTABLISHED"}) == ("", "NOT_ESTABLISHED")


def test_shared_engine_score_counts_empty_outputs_as_deletions():
    rows = [
        {"orth": "ក", "pron_no_tones": "ka"},
        {"orth": "ខ", "pron_no_tones": "kʰa"},
    ]
    report = evaluate(
        rows,
        ["ka", ""],
        ["OUTPUT", "UNRESOLVED"],
        elapsed_seconds=0.02,
        version="test",
    )
    assert report["inputs"] == 2
    assert report["nonempty_outputs"] == 1
    assert report["output_coverage_percent"] == 50
    assert report["strict_source_attested_matches"] == 1
    assert report["codepoint_edits"] == 3
    assert report["reference_codepoints"] == 5
    assert report["source_attested_codepoint_CER_percent"] == 60
    assert report["score_status"] == "SOURCE_ATTESTED_DIAGNOSTIC_NOT_ACCURACY"
