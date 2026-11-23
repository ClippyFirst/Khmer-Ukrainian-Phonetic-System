#!/usr/bin/env python3
"""Evaluate Khmer word-boundary segmentation against the khPOS OPEN-TEST set.

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
    khmer_word_tokens: int


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\\0".encode("ascii")
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
    khmer_word_tokens = 0
    for index, token in enumerate(tokens):
        start = offset
        offset += len(token)
        if word_flags[index]:
            khmer_word_tokens += 1
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
            khmer_word_tokens=khmer_word_tokens,
        ),
        len(raw_tokens),
    )


def predicted_boundaries_from_units(
    units: Iterable[dict], sentence: BenchmarkSentence
) -> frozenset[int]:
    offset = 0
    predicted: set[int] = set()
    reconstructed: list[str] = []
    for unit in units:
        value = unit["source"]
        if value == " ":
            if offset in sentence.eligible_boundaries:
                predicted.add(offset)
        else:
            reconstructed.append(value)
            offset += len(value)
    if "".join(reconstructed) != sentence.source:
        raise AssertionError("engine units did not losslessly reconstruct the benchmark input")
    return frozenset(predicted)


def score_predictions(
    sentences: list[BenchmarkSentence],
    predictions: list[frozenset[int]],
) -> dict:
    if len(sentences) != len(predictions):
        raise ValueError("sentence and prediction counts differ")
    gold_total = predicted_total = true_positive = 0
    exact_with_gold = sentences_with_gold = 0
    khmer_tokens = 0
    for sentence, predicted in zip(sentences, predictions, strict=True):
        gold = sentence.gold_boundaries
        predicted_total += len(predicted)
        gold_total += len(gold)
        true_positive += len(gold & predicted)
        khmer_tokens += sentence.khmer_word_tokens
        if gold:
            sentences_with_gold += 1
            exact_with_gold += gold == predicted

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
        "sentences": len(sentences),
        "sentences_with_gold_boundaries": sentences_with_gold,
        "exact_sentence_matches_with_gold_boundaries": exact_with_gold,
        "exact_sentence_match_rate": (
            exact_with_gold / sentences_with_gold if sentences_with_gold else 0.0
        ),
        "khmer_gold_word_tokens": khmer_tokens,
        "gold_boundaries": gold_total,
        "predicted_boundaries": predicted_total,
        "true_positive_boundaries": true_positive,
        "false_positive_boundaries": false_positive,
        "false_negative_boundaries": false_negative,
        "boundary_precision": precision,
        "boundary_recall": recall,
        "boundary_f1": f1,
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
        python_predictions = [
            predicted_boundaries_from_units(
                engine.analyze(sentence.source)["units"], sentence
            )
            for sentence in sentences
        ]
        python_metrics = score_predictions(sentences, python_predictions)

        node_script = Path(__file__).with_name("evaluate_khpos_js.mjs")
        node = subprocess.run(
            ["node", str(node_script), str(corpus_path)],
            check=True,
            capture_output=True,
            text=True,
        )
        javascript_result = json.loads(node.stdout)
        javascript_metrics = javascript_result["metrics"]

        parity_fields = (
            "sentences",
            "sentences_with_gold_boundaries",
            "exact_sentence_matches_with_gold_boundaries",
            "khmer_gold_word_tokens",
            "gold_boundaries",
            "predicted_boundaries",
            "true_positive_boundaries",
            "false_positive_boundaries",
            "false_negative_boundaries",
        )
        differences = {
            key: {
                "python": python_metrics[key],
                "javascript": javascript_metrics[key],
            }
            for key in parity_fields
            if python_metrics[key] != javascript_metrics[key]
        }
        if differences:
            raise RuntimeError(
                "Python/JavaScript khPOS boundary benchmark parity failed: "
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
                "item as one gold token; score boundaries only between adjacent Khmer word tokens"
            ),
            "corpus_bytes": len(raw),
            "raw_token_count": raw_token_count,
            "python": python_metrics,
            "javascript": javascript_metrics,
            "python_javascript_parity": "PASS",
            "limitations": [
                "This is an external manually segmented benchmark, not an adjudicated gold set for the project's Phnom Penh careful-citation profile.",
                "The corpus mixes news, economics, politics, student/voter lists and other material; its target variety and tokenization policy are not identical to this project contract.",
                "Overlap between khPOS source texts and FineWeb-2 frequency-training text has not been ruled out.",
                "Do not interpret this score as general Khmer segmentation accuracy or as IPA/pronunciation accuracy.",
            ],
        }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
