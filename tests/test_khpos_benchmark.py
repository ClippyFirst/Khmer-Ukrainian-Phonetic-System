import importlib.util
import sys
from pathlib import Path

_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "evaluate_khpos.py"
_SPEC = importlib.util.spec_from_file_location("evaluate_khpos", _SCRIPT)
assert _SPEC and _SPEC.loader
_BENCHMARK = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _BENCHMARK
_SPEC.loader.exec_module(_BENCHMARK)

prepare_sentence = _BENCHMARK.prepare_sentence
predicted_spans_from_units = _BENCHMARK.predicted_spans_from_units
score_predictions = _BENCHMARK.score_predictions


def _score(sentence, units):
    boundaries, all_tokens, khmer_words = predicted_spans_from_units(units, sentence)
    return score_predictions([sentence], [boundaries], [all_tokens], [khmer_words])


def test_khpos_compound_markers_are_removed_without_splitting_the_gold_token():
    sentence, raw_count = prepare_sentence("កម្ពុជា ប្រជាធិបតេយ្យ លោក~ស្រី ធម្ម_ជាតិ ជីវ^ភាព")
    assert raw_count == 5
    assert sentence.source == "កម្ពុជាប្រជាធិបតេយ្យលោកស្រីធម្មជាតិជីវភាព"
    assert len(sentence.gold_token_spans) == 5
    assert len(sentence.gold_khmer_word_spans) == 5
    assert len(sentence.gold_boundaries) == 4


def test_khpos_all_token_metric_includes_punctuation_but_khmer_metric_excludes_it():
    sentence, _ = prepare_sentence("កម្ពុជា ។ លោក")
    assert sentence.source == "កម្ពុជា។លោក"
    assert sentence.gold_boundaries == frozenset()
    metrics = _score(
        sentence,
        [
            {"source": "កម្ពុជា"},
            {"source": "។"},
            {"source": "លោក"},
        ],
    )
    assert metrics["all_token_word_level"]["gold"] == 3
    assert metrics["all_token_word_level"]["true_positive"] == 3
    assert metrics["khmer_word_level"]["gold"] == 2
    assert metrics["khmer_word_level"]["true_positive"] == 2
    assert metrics["khmer_boundary_level"]["gold"] == 0


def test_khpos_word_level_and_boundary_metrics_are_perfect_for_exact_segmentation():
    sentence, _ = prepare_sentence("កម្ពុជា ប្រជាធិបតេយ្យ")
    metrics = _score(
        sentence,
        [
            {"source": "កម្ពុជា"},
            {"source": " "},
            {"source": "ប្រជាធិបតេយ្យ"},
        ],
    )
    assert metrics["all_token_word_level"]["f1"] == 1.0
    assert metrics["khmer_word_level"]["f1"] == 1.0
    assert metrics["khmer_boundary_level"]["f1"] == 1.0


def test_khpos_word_level_metrics_penalize_splitting_one_gold_word_into_two():
    sentence, _ = prepare_sentence("កម្ពុជាប្រជាធិបតេយ្យ")
    metrics = _score(
        sentence,
        [
            {"source": "កម្ពុជា"},
            {"source": " "},
            {"source": "ប្រជាធិបតេយ្យ"},
        ],
    )
    assert metrics["all_token_word_level"]["gold"] == 1
    assert metrics["all_token_word_level"]["predicted"] == 2
    assert metrics["all_token_word_level"]["true_positive"] == 0
    assert metrics["all_token_word_level"]["false_positive"] == 2
    assert metrics["all_token_word_level"]["false_negative"] == 1
    assert metrics["khmer_boundary_level"]["false_positive"] == 1
