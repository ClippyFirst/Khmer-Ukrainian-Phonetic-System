import importlib.util
from pathlib import Path

_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "evaluate_khpos.py"
_SPEC = importlib.util.spec_from_file_location("evaluate_khpos", _SCRIPT)
assert _SPEC and _SPEC.loader
_BENCHMARK = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_BENCHMARK)

prepare_sentence = _BENCHMARK.prepare_sentence
predicted_boundaries_from_units = _BENCHMARK.predicted_boundaries_from_units
score_predictions = _BENCHMARK.score_predictions


def test_khpos_compound_markers_are_removed_without_splitting_the_gold_token():
    sentence, raw_count = prepare_sentence("កម្ពុជា ប្រជាធិបតេយ្យ លោក~ស្រី ធម្ម_ជាតិ ជីវ^ភាព")
    assert raw_count == 5
    assert sentence.source == "កម្ពុជាប្រជាធិបតេយ្យលោកស្រីធម្មជាតិជីវភាព"
    assert len(sentence.gold_boundaries) == 4
    assert sentence.khmer_word_tokens == 5


def test_khpos_boundary_scoring_ignores_non_khmer_token_boundaries():
    sentence, _ = prepare_sentence("កម្ពុជា ។ លោក")
    assert sentence.source == "កម្ពុជា។លោក"
    assert sentence.gold_boundaries == frozenset()
    assert sentence.eligible_boundaries
    predictions = predicted_boundaries_from_units(
        [
            {"source": "កម្ពុជា"},
            {"source": "។"},
            {"source": "លោក"},
        ],
        sentence,
    )
    metrics = score_predictions([sentence], [predictions])
    assert metrics["gold_boundaries"] == 0
    assert metrics["predicted_boundaries"] == 0


def test_khpos_boundary_scoring_counts_only_between_adjacent_khmer_words():
    sentence, _ = prepare_sentence("កម្ពុជា ប្រជាធិបតេយ្យ")
    predictions = predicted_boundaries_from_units(
        [
            {"source": "កម្ពុជា"},
            {"source": " "},
            {"source": "ប្រជាធិបតេយ្យ"},
        ],
        sentence,
    )
    metrics = score_predictions([sentence], [predictions])
    assert metrics["true_positive_boundaries"] == 1
    assert metrics["false_positive_boundaries"] == 0
    assert metrics["false_negative_boundaries"] == 0
    assert metrics["boundary_f1"] == 1.0
