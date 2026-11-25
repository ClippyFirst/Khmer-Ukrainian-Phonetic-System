import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "benchmark_nckl_respelling.py"


def load_module():
    spec = importlib.util.spec_from_file_location("nckl_respelling_benchmark", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_group_references_keeps_all_attested_readings_per_word():
    module = load_module()
    rows = [
        {"word": "ក", "pronunciation": "ក-ក"},
        {"word": "ក", "pronunciation": "ក"},
        {"word": "ខ", "pronunciation": "ខ"},
    ]
    grouped = module.group_references(rows)
    assert grouped == {"ក": ["ក-ក", "ក"], "ខ": ["ខ"]}


def test_metrics_accept_any_attested_alternative_and_count_syllables():
    module = load_module()
    rows = [
        {"word": "ក", "pronunciation": "ក-ក"},
        {"word": "ក", "pronunciation": "ក"},
        {"word": "ខ", "pronunciation": "ខ-ខ"},
    ]
    report = module.build_report(
        rows,
        {"ក": "ក", "ខ": "ខ"},
        model_revision="model-sha",
        dataset_revision="dataset-sha",
        upstream_code_revision="code-sha",
        runtime={"torch_version": "test"},
    )
    metrics = report["source_attested_test_metrics"]
    assert metrics["unique_words"] == 2
    assert metrics["reference_pairs"] == 3
    assert metrics["nonempty_outputs"] == 2
    assert metrics["word_exact_matches"] == 1
    assert metrics["word_exact_match_rate"] == 0.5
    assert metrics["character_errors"] == 1
    assert metrics["reference_characters"] == 3
    assert metrics["character_error_rate"] == 1 / 3
    assert metrics["syllable_count_matches"] == 1
    assert metrics["syllable_count_accuracy"] == 0.5


def test_report_never_calls_respelling_ipa_or_independent_gold():
    module = load_module()
    rows = [{"word": "ក", "pronunciation": "ក"}]
    report = module.build_report(
        rows,
        {"ក": "ក"},
        model_revision="model-sha",
        dataset_revision="dataset-sha",
        upstream_code_revision="code-sha",
    )
    assert report["task"] == "Khmer-script NCKL pronunciation respelling"
    assert report["target_representation"] == "Khmer-script respelling with hyphen syllable separators; not IPA"
    assert report["independent_ipa_gold_count"] == 0
    assert report["ipa_accuracy"] is None
    assert "not IPA" in report["interpretation"]


def test_aggregate_report_does_not_emit_source_words_or_predictions():
    module = load_module()
    report = module.build_report(
        [{"word": "ក գաղտնի", "pronunciation": "ក"}],
        {"ក գաղտնի": "ក"},
        model_revision="model-sha",
        dataset_revision="dataset-sha",
        upstream_code_revision="code-sha",
    )
    rendered = str(report)
    assert "ក գաղտնի" not in rendered
    assert "raw_output" not in rendered
    assert "records" not in report


def test_report_rejects_missing_or_extra_predictions():
    module = load_module()
    rows = [{"word": "ក", "pronunciation": "ក"}]
    try:
        module.build_report(
            rows,
            {},
            model_revision="model-sha",
            dataset_revision="dataset-sha",
            upstream_code_revision="code-sha",
        )
    except ValueError as error:
        assert "one prediction per unique word" in str(error)
    else:
        raise AssertionError("prediction mismatch should be rejected")


def test_reference_split_validation_rejects_word_overlap():
    module = load_module()
    splits = {
        "train": [{"word": "ក", "pronunciation": "ក"}],
        "validation": [{"word": "ខ", "pronunciation": "ខ"}],
        "test": [{"word": "ក", "pronunciation": "ក"}],
    }
    try:
        module.validate_word_disjoint_splits(splits)
    except ValueError as error:
        assert "word overlap" in str(error)
    else:
        raise AssertionError("word overlap should be rejected")
