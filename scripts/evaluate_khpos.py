#!/usr/bin/env python3
"""Evaluate Khmer segmentation against the khPOS OPEN-TEST set.

The corpus is downloaded on demand, checksum-verified, and deleted after the run.
It is licensed CC BY-NC-SA 4.0 and is intentionally not bundled or uploaded.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import urllib.request
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from khmer_ua.rule_engine import RuleBasedKhmerEngine

UPSTREAM_REVISION = "0211405c145b0a340ad558569bd06c946b2296b4"
UPSTREAM_PATH = "corpus-draft-ver-1.0/data/OPEN-TEST.word"
UPSTREAM_URL = (
    "https://raw.githubusercontent.com/ye-kyaw-thu/khPOS/"
    f"{UPSTREAM_REVISION}/{UPSTREAM_PATH}"
)
EXPECTED_GIT_BLOB_SHA = "34cf93f298c06723419212f0f0777f3783537069"
EXPECTED_SENTENCES = 1000
EXPECTED_TOKENS = 10778
COMPOUND_MARKERS = str.maketrans("", "", "~_^")


@dataclass(frozen=True)
class BenchmarkSentence:
    source: str
    gold_boundaries: frozenset[int]
    eligible_boundaries: frozenset[int]
    gold_token_spans: frozenset[tuple[int, int]]
    gold_khmer_word_spans: frozenset[tuple[int, int]]
    khmer_word_tokens: int


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def is_khmer_word_token(token: str) -> bool:
    if not token:
        return False
    if not all(0x1780 <= ord(char) <= 0x17FF for char in token):
        return False
    return any(0x1780 <= ord(char) <= 0x17B3 for char in token)


def prepare_sentence(line: str) -> tuple[BenchmarkSentence, int]:
    raw_tokens = line.split()
    tokens = [
        unicodedata.normalize("NFC", token.translate(COMPOUND_MARKERS))
        for token in raw_tokens
    ]
    tokens = [token for token in tokens if token]
    source = "".join(tokens)
    word_flags = [is_khmer_word_token(token) for token in tokens]

    offset = 0
    gold_boundaries: set[int] = set()
    eligible_characters: set[int] = set()
    gold_token_spans: set[tuple[int, int]] = set()
    gold_khmer_word_spans: set[tuple[int, int]] = set()
    khmer_word_tokens = 0
    for index, token in enumerate(tokens):
        start = offset
        offset += len(token)
        gold_token_spans.add((start, offset))
        if word_flags[index]:
            khmer_word_tokens += 1
            gold_khmer_word_spans.add((start, offset))
            eligible_characters.update(range(start, offset))
        if index + 1 < len(tokens) and word_flags[index] and word_flags[index + 1]:
            gold_boundaries.add(offset)

    eligible_boundaries = {
        position
        for position in range(1, len(source))
        if position - 1 in eligible_characters and position in eligible_characters
    }
    return (
        BenchmarkSentence(
            source=source,
            gold_boundaries=frozenset(gold_boundaries),
            eligible_boundaries=frozenset(eligible_boundaries),
            gold_token_spans=frozenset(gold_token_spans),
            gold_khmer_word_spans=frozenset(gold_khmer_word_spans),
            khmer_word_tokens=khmer_word_tokens,
        ),
        len(raw_tokens),
    )


def predicted_spans_from_units(
    units: Iterable[dict], sentence: BenchmarkSentence
) -> tuple[frozenset[int], frozenset[tuple[int, int]], frozenset[tuple[int, int]]]:
    offset = 0
    predicted_boundaries: set[int] = set()
    predicted_token_spans: set[tuple[int, int]] = set()
    predicted_khmer_word_spans: set[tuple[int, int]] = set()
    reconstructed: list[str] = []
    for unit in units:
        value = unit["source"]
        if value == " ":
            if offset in sentence.eligible_boundaries:
                predicted_boundaries.add(offset)
            continue

        start = offset
        offset += len(value)
        reconstructed.append(value)
        if value:
            predicted_token_spans.add((start, offset))
            if is_khmer_word_token(value):
                predicted_khmer_word_spans.add((start, offset))

    if "".join(reconstructed) != sentence.source:
        raise AssertionError("engine units did not losslessly reconstruct the benchmark input")
    return (
        frozenset(predicted_boundaries),
        frozenset(predicted_token_spans),
        frozenset(predicted_khmer_word_spans),
    )


def _span_metrics(
    sentences: list[BenchmarkSentence],
    predictions: list[frozenset[tuple[int, int]]],
    gold_attribute: str,
) -> dict:
    gold_total = predicted_total = true_positive = 0
    exact_sentences = 0
    for sentence, predicted in zip(sentences, predictions, strict=True):
        gold = getattr(sentence, gold_attribute)
        gold_total += len(gold)
        predicted_total += len(predicted)
        true_positive += len(gold & predicted)
        exact_sentences += gold == predicted

    false_positive = predicted_total - true_positive
    false_negative = gold_total - true_positive
    precision = true_positive / predicted_total if predicted_total else 0.0
    recall = true_positive / gold_total if gold_total else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall
        else 0.0
    )
    return {
        "gold": gold_total,
        "predicted": predicted_total,
        "true_positive": true_positive,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "exact_sentence_matches": exact_sentences,
    }


def score_predictions(
    sentences: list[BenchmarkSentence],
    boundary_predictions: list[frozenset[int]],
    all_token_predictions: list[frozenset[tuple[int, int]]],
    khmer_word_predictions: list[frozenset[tuple[int, int]]],
) -> dict:
    if not (
        len(sentences)
        == len(boundary_predictions)
        == len(all_token_predictions)
        == len(khmer_word_predictions)
    ):
        raise ValueError("sentence and prediction counts differ")

    boundary_gold = boundary_predicted = boundary_true_positive = 0
    exact_boundary_sentences = sentences_with_gold_boundaries = 0
    for sentence, predicted in zip(sentences, boundary_predictions, strict=True):
        gold = sentence.gold_boundaries
        boundary_gold += len(gold)
        boundary_predicted += len(predicted)
        boundary_true_positive += len(gold & predicted)
        if gold:
            sentences_with_gold_boundaries += 1
            exact_boundary_sentences += gold == predicted

    boundary_fp = boundary_predicted - boundary_true_positive
    boundary_fn = boundary_gold - boundary_true_positive
    boundary_precision = (
        boundary_true_positive / boundary_predicted if boundary_predicted else 0.0
    )
    boundary_recall = (
        boundary_true_positive / boundary_gold if boundary_gold else 0.0
    )
    boundary_f1 = (
        2 * boundary_precision * boundary_recall / (boundary_precision + boundary_recall)
        if boundary_precision + boundary_recall
        else 0.0
    )

    return {
        "sentences": len(sentences),
        "sentences_with_gold_boundaries": sentences_with_gold_boundaries,
        "khmer_gold_word_tokens": sum(s.khmer_word_tokens for s in sentences),
        "all_token_word_level": _span_metrics(
            sentences, all_token_predictions, "gold_token_spans"
        ),
        "khmer_word_level": _span_metrics(
            sentences, khmer_word_predictions, "gold_khmer_word_spans"
        ),
        "khmer_boundary_level": {
            "gold": boundary_gold,
            "predicted": boundary_predicted,
            "true_positive": boundary_true_positive,
            "false_positive": boundary_fp,
            "false_negative": boundary_fn,
            "precision": boundary_precision,
            "recall": boundary_recall,
            "f1": boundary_f1,
            "exact_sentence_matches_with_gold_boundaries": exact_boundary_sentences,
            "exact_sentence_match_rate": (
                exact_boundary_sentences / sentences_with_gold_boundaries
                if sentences_with_gold_boundaries
                else 0.0
            ),
        },
    }


def download_corpus(destination: Path) -> bytes:
    request = urllib.request.Request(
        UPSTREAM_URL,
        headers={"User-Agent": "ClippyFirst-Khmer-Ukrainian-Research-Benchmark/1.0"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read()
    actual = git_blob_sha(data)
    if actual != EXPECTED_GIT_BLOB_SHA:
        raise RuntimeError(
            f"khPOS OPEN-TEST.word Git blob SHA mismatch: expected "
            f"{EXPECTED_GIT_BLOB_SHA}, got {actual}"
        )
    destination.write_bytes(data)
    return data


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="khpos-open-test-") as temporary:
        corpus_path = Path(temporary) / "OPEN-TEST.word"
        raw = download_corpus(corpus_path)
        text = raw.decode("utf-8-sig")
        lines = text.splitlines()
        if len(lines) != EXPECTED_SENTENCES:
            raise RuntimeError(
                f"Expected {EXPECTED_SENTENCES} khPOS test sentences, got {len(lines)}"
            )

        sentences: list[BenchmarkSentence] = []
        raw_token_count = 0
        for line in lines:
            sentence, count = prepare_sentence(line)
            sentences.append(sentence)
            raw_token_count += count
        if raw_token_count != EXPECTED_TOKENS:
            raise RuntimeError(
                f"Expected {EXPECTED_TOKENS} khPOS tokens, got {raw_token_count}"
            )

        engine = RuleBasedKhmerEngine()
        python_boundary_predictions = []
        python_all_token_predictions = []
        python_khmer_word_predictions = []
        for sentence in sentences:
            units = engine.analyze(sentence.source)["units"]
            boundaries, all_tokens, khmer_words = predicted_spans_from_units(
                units, sentence
            )
            python_boundary_predictions.append(boundaries)
            python_all_token_predictions.append(all_tokens)
            python_khmer_word_predictions.append(khmer_words)

        python_metrics = score_predictions(
            sentences,
            python_boundary_predictions,
            python_all_token_predictions,
            python_khmer_word_predictions,
        )

        node_script = Path(__file__).with_name("evaluate_khpos_js.mjs")
        node = subprocess.run(
            ["node", str(node_script), str(corpus_path)],
            check=True,
            capture_output=True,
            text=True,
        )
        javascript_result = json.loads(node.stdout)
        javascript_metrics = javascript_result["metrics"]

        parity_paths = (
            ("all_token_word_level", "gold"),
            ("all_token_word_level", "predicted"),
            ("all_token_word_level", "true_positive"),
            ("all_token_word_level", "false_positive"),
            ("all_token_word_level", "false_negative"),
            ("all_token_word_level", "exact_sentence_matches"),
            ("khmer_word_level", "gold"),
            ("khmer_word_level", "predicted"),
            ("khmer_word_level", "true_positive"),
            ("khmer_word_level", "false_positive"),
            ("khmer_word_level", "false_negative"),
            ("khmer_word_level", "exact_sentence_matches"),
            ("khmer_boundary_level", "gold"),
            ("khmer_boundary_level", "predicted"),
            ("khmer_boundary_level", "true_positive"),
            ("khmer_boundary_level", "false_positive"),
            ("khmer_boundary_level", "false_negative"),
            ("khmer_boundary_level", "exact_sentence_matches_with_gold_boundaries"),
        )
        differences = {}
        for section, field in parity_paths:
            if python_metrics[section][field] != javascript_metrics[section][field]:
                differences[f"{section}.{field}"] = {
                    "python": python_metrics[section][field],
                    "javascript": javascript_metrics[section][field],
                }
        if differences:
            raise RuntimeError(
                "Python/JavaScript khPOS benchmark parity failed: "
                + json.dumps(differences, ensure_ascii=False)
            )

        print(json.dumps({
            "benchmark": "khPOS OPEN-TEST manual word segmentation",
            "upstream_repository": "https://github.com/ye-kyaw-thu/khPOS",
            "upstream_revision": UPSTREAM_REVISION,
            "upstream_file": UPSTREAM_PATH,
            "upstream_git_blob_sha": EXPECTED_GIT_BLOB_SHA,
            "license": "CC BY-NC-SA 4.0",
            "use_policy": "on-demand non-commercial evaluation only; corpus is not bundled or uploaded",
            "surface_reconstruction": (
                "NFC; remove internal notation markers ~, _ and ^ while keeping each marked "
                "item as one gold token; all-token word F1 includes punctuation and non-Khmer "
                "tokens; Khmer-only word and boundary metrics exclude them"
            ),
            "corpus_bytes": len(raw),
            "raw_token_count": raw_token_count,
            "python": python_metrics,
            "javascript": javascript_metrics,
            "python_javascript_parity": "PASS",
            "limitations": [
                "The external paper's word-level khPOS scores use the same named open test split, but its exact preprocessing and marker treatment may differ; comparisons are contextual, not a strict reproduction.",
                "This is not an adjudicated gold set for the project's Phnom Penh careful-citation profile.",
                "The corpus mixes news, economics, politics, student/voter lists and other material; its target variety and tokenization policy are not identical to this project contract.",
                "Overlap between khPOS source texts and FineWeb-2 frequency-training text has not been ruled out.",
                "Do not interpret this score as general Khmer segmentation accuracy or as IPA/pronunciation accuracy.",
            ],
        }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
