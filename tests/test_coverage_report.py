import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "khmer-coverage-audit.json"
SCRIPT = ROOT / "scripts" / "coverage.py"


def test_coverage_report_is_generated_and_in_sync():
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    inventory = report["orthographic_inventory"]
    summary = report["coverage_summary"]
    cells = report["dependent_vowel_by_series"]

    assert inventory["dependent_vowel_signs"] > 0
    assert inventory["independent_vowel_signs"] > 0
    assert inventory["expected_dependent_vowel_x_series_cells"] == (
        inventory["dependent_vowel_signs"] * 2
    )
    assert len(cells) == inventory["expected_dependent_vowel_x_series_cells"]
    assert set(summary) >= {
        "source_attested_not_gold_cells",
        "conflicting_cells",
        "not_established_cells",
        "coverage_fraction",
    }
    assert (
        summary["source_attested_not_gold_cells"]
        + summary["conflicting_cells"]
        + summary["not_established_cells"]
        == len(cells)
    )
    assert all(
        cell["status"] in {
            "SOURCE_ATTESTED_NOT_GOLD",
            "CONFLICTING_SOURCE_ANALYSES",
            "NOT_ESTABLISHED",
        }
        for cell in cells.values()
    )
    assert report["source_conflict_case_ids"]
    assert report["interpretation"].find("never gold") >= 0


def test_conflicting_source_cases_are_not_lost_from_coverage_summary():
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    registry = json.loads(
        (ROOT / "data" / "khmer" / "vowel-context-register.json").read_text(encoding="utf-8")
    )
    expected = sorted(
        case["id"]
        for case in registry["cases"]
        if case.get("status") == "CONFLICTING_SOURCE_ANALYSES"
    )
    assert sorted(report["source_conflict_case_ids"]) == expected


def test_coverage_matrix_never_fabricates_ipa_for_unestablished_cells():
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    for cell in report["dependent_vowel_by_series"].values():
        if cell["status"] == "NOT_ESTABLISHED":
            assert cell["ipa_values"] == []



def test_public_report_is_identical_to_canonical_generated_report():
    public_report = ROOT / "public" / "reports" / "khmer-coverage-audit.json"
    assert public_report.exists()
    assert public_report.read_bytes() == REPORT.read_bytes()


def test_contextual_vowel_evidence_exposes_missing_dimensions_without_inference():
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    contextual = report["contextual_vowel_evidence"]
    observations = contextual["observations"]
    assert len(observations) == sum(report["source_registry_status_counts"].values())
    assert contextual["cross_product_assessment"]["status"] == "NOT_ESTABLISHED"
    assert contextual["context_dimensions"]["syllable_type"].startswith("NOT_ESTABLISHED")
    assert contextual["context_dimensions"]["vowel_length"].startswith("ONLY_EXPLICIT")
    assert contextual["context_dimensions"]["profile"].startswith("NOT_SPECIFIED")

    by_id = {row["case_id"]: row for row in observations}
    # KHV-001 has an explicit long mark in the cited source transcription.
    assert by_id["KHV-001"]["length_evidence"] == "EXPLICIT_LENGTH_MARK_IN_SOURCE_TRANSCRIPTION"
    # Missing/undocumented dimensions remain unknown; do not infer from spelling.
    assert by_id["KHV-001"]["phonological_syllable_type"] == "NOT_ESTABLISHED"
    assert by_id["KHV-001"]["profile"] == "NOT_SPECIFIED_PER_CASE"
    # A source transcription without a length mark is not automatically "short".
    no_mark = [row for row in observations if row["source_transcription"] and "ː" not in row["source_transcription"]]
    assert all("SHORTNESS_NOT_INFERRED" in row["length_evidence"] for row in no_mark)
    # Conflicting source analyses remain uncollapsed and retain their source status.
    conflicting = [row for row in observations if row["evidence_status"] == "CONFLICTING_SOURCE_ANALYSES"]
    assert conflicting
    assert all(row["source_transcription"] is None for row in conflicting)


def test_coverage_report_exposes_source_backed_context_dimensions():
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    registry = json.loads(
        (ROOT / "data" / "khmer" / "vowel-context-register.json").read_text(encoding="utf-8")
    )
    contextual = report["contextual_vowel_evidence"]
    dimensions = contextual["source_backed_context_dimensions"]
    expected = registry["context_dimensions"]

    assert contextual["context_dimension_count"] == len(expected)
    assert [item["id"] for item in dimensions] == sorted(item["id"] for item in expected)
    assert contextual["context_dimension_evidence_status_counts"] == {
        status: sum(1 for item in expected if item["evidence_status"] == status)
        for status in sorted({item["evidence_status"] for item in expected})
    }
    source_ids = set(registry["sources"])
    for item in dimensions:
        assert set(item["source_ids"]) <= source_ids
        assert item["locator"]
        assert item["profile_scope"]
        assert item["implementation"]
    assert contextual["cross_product_assessment"]["status"] == "NOT_ESTABLISHED"


def test_coverage_report_exposes_coda_pattern_evidence_without_lexical_promotion():
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    registry = json.loads(
        (ROOT / "data" / "khmer" / "vowel-context-register.json").read_text(encoding="utf-8")
    )
    contextual = report["contextual_vowel_evidence"]
    patterns = contextual["source_backed_coda_pattern_observations"]
    expected = registry["coda_pattern_observations"]

    assert contextual["coda_pattern_observation_count"] == len(expected) == 15
    assert [item["id"] for item in patterns] == sorted(item["id"] for item in expected)
    assert all(item["evidence_status"] == "SOURCE_ATTESTED_NOT_GOLD" for item in patterns)
    assert all(item["ukrainian_adaptation"] is None for item in patterns)
    assert all(item["ukrainian_status"] == "NOT_ESTABLISHED" for item in patterns)
    assert report["orthographic_inventory"]["expected_dependent_vowel_x_series_cells"] == 32


def test_coverage_report_keeps_custom_lexical_transcriptions_out_of_ipa():
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    registry = json.loads(
        (ROOT / "data" / "khmer" / "vowel-context-register.json").read_text(encoding="utf-8")
    )
    contextual = report["contextual_vowel_evidence"]
    examples = contextual["source_backed_lexical_coda_examples"]

    assert contextual["lexical_coda_example_count"] == len(registry["lexical_coda_examples"]) == 12
    assert [item["id"] for item in examples] == sorted(
        item["id"] for item in registry["lexical_coda_examples"]
    )
    assert all(item["ipa"] is None for item in examples)
    assert all(item["ukrainian_adaptation"] is None for item in examples)
    assert all("not IPA" in item["transcription_system"] for item in examples)
