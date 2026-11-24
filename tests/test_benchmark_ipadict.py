import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = runpy.run_path(str(ROOT / "scripts" / "benchmark_ipadict.py"))
load_ipa_dict = MODULE["load_ipa_dict"]
evaluate_multi_reference = MODULE["evaluate_multi_reference"]


def test_ipa_dict_loader_preserves_multiple_reference_alternatives(tmp_path):
    source = tmp_path / "km.txt"
    source.write_text(
        "ក\t/kɑɑ/\n"
        "ក\t/kɑɑ/, /ka/\n"
        "ខ\t/kʰɑɑ/\n",
        encoding="utf-8",
    )
    assert load_ipa_dict(source) == {
        "ក": ["ka", "kɑɑ"],
        "ខ": ["kʰɑɑ"],
    }


def test_multi_reference_scoring_accepts_any_listed_variant_and_counts_missing_output():
    refs = {
        "ក": ["kɑɑ", "ka"],
        "ខ": ["kʰɑɑ"],
    }
    report = evaluate_multi_reference(
        refs,
        ["ក", "ខ"],
        ["ka", ""],
        ["OUTPUT", "UNRESOLVED"],
        elapsed_seconds=0.02,
        version="test",
    )
    assert report["inputs"] == 2
    assert report["nonempty_outputs"] == 1
    assert report["strict_source_attested_matches"] == 1
    assert report["source_attested_exact_match_percent"] == 50
    assert report["codepoint_edits_best_of_reference_alternatives"] == 4
    assert report["selected_reference_codepoints"] == 6
    assert report["source_attested_codepoint_CER_percent"] == 66.67
    assert report["score_status"] == "SOURCE_ATTESTED_DIAGNOSTIC_NOT_ACCURACY"
