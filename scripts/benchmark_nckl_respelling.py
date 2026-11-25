#!/usr/bin/env python3
"""Evaluate the MIT-licensed Khmer G2P package on the NCKL word-disjoint test split.

This is a separate Khmer-script pronunciation-respelling benchmark, NOT IPA.
The NCKL-derived dataset is fetched ephemerally; only aggregate metrics are
written. No source words, references, predictions, or row-level records are
stored in the repository or CI artifact.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DATASET_ID = "phonsobon/khmer-G2P"
DATASET_REVISION = "2733e664ed4d77dee4cc588a130bb4844c9da767"
MODEL_ID = "phonsobon/khmer-g2p"
MODEL_REVISION = "7dbc6c3d1c1f5a9a8763be602fa679f130f20dca"
MODEL_PACKAGE = "khmer-g2p"
MODEL_PACKAGE_VERSION = "0.1.0"
EXPECTED_SPLIT_ROWS = {"train": 34770, "validation": 1939, "test": 1920}
EXPECTED_TEST_UNIQUE_WORDS = 1888
ROOT = Path(__file__).resolve().parents[1]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def codepoint_levenshtein(reference: str, hypothesis: str) -> int:
    """Levenshtein distance over Unicode code points."""
    if len(reference) < len(hypothesis):
        reference, hypothesis = hypothesis, reference
    previous = list(range(len(hypothesis) + 1))
    for i, left in enumerate(reference, 1):
        current = [i]
        for j, right in enumerate(hypothesis, 1):
            current.append(min(
                current[-1] + 1,
                previous[j] + 1,
                previous[j - 1] + (left != right),
            ))
        previous = current
    return previous[-1]


def group_references(rows: list[dict[str, Any]]) -> dict[str, list[str]]:
    """Group multiple source-attested pronunciations by word."""
    grouped: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        word = row.get("word")
        pronunciation = row.get("pronunciation")
        if not isinstance(word, str) or not word.strip():
            raise ValueError("every NCKL row requires a non-empty word")
        if not isinstance(pronunciation, str) or not pronunciation.strip():
            raise ValueError("every NCKL row requires a non-empty pronunciation")
        grouped[word].append(pronunciation)
        if "syllables" in row and int(row["syllables"]) != pronunciation.count("-") + 1:
            raise ValueError("NCKL syllables field disagrees with pronunciation separators")
    return dict(grouped)


def validate_word_disjoint_splits(splits: dict[str, list[dict[str, Any]]]) -> None:
    """Fail closed if the pinned train/validation/test splits leak words."""
    required = {"train", "validation", "test"}
    if not required.issubset(splits):
        raise ValueError("dataset must provide train, validation and test splits")
    seen: dict[str, str] = {}
    for split_name in ("train", "validation", "test"):
        words = [row.get("word") for row in splits[split_name]]
        if any(not isinstance(word, str) or not word for word in words):
            raise ValueError(f"{split_name} contains an empty or invalid word")
        for word in set(words):
            previous = seen.get(word)
            if previous is not None:
                raise ValueError(f"word overlap between {previous} and {split_name}: {word}")
            seen[word] = split_name


def build_report(
    rows: list[dict[str, Any]],
    predictions: dict[str, str],
    *,
    model_revision: str,
    dataset_revision: str,
    model_package_version: str,
    runtime: dict[str, Any] | None = None,
) -> dict[str, Any]:
    references = group_references(rows)
    if not references:
        raise ValueError("cannot benchmark an empty NCKL split")
    if set(predictions) != set(references):
        raise ValueError("expected one prediction per unique word")
    if any(not isinstance(value, str) for value in predictions.values()):
        raise ValueError("every prediction must be a string")

    exact_matches = 0
    nonempty = 0
    total_edits = 0
    total_reference_characters = 0
    syllable_matches = 0
    for word, alternatives in references.items():
        prediction = predictions[word]
        best_reference = min(
            alternatives,
            key=lambda reference: codepoint_levenshtein(reference, prediction),
        )
        edits = codepoint_levenshtein(best_reference, prediction)
        exact = prediction in alternatives
        exact_matches += int(exact)
        nonempty += int(bool(prediction.strip()))
        total_edits += edits
        total_reference_characters += len(best_reference)
        syllable_matches += int(prediction.count("-") == best_reference.count("-"))

    unique_words = len(references)
    reference_pairs = len(rows)
    return {
        "schema_version": "1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "task": "Khmer-script NCKL pronunciation respelling",
        "target_representation": "Khmer-script respelling with hyphen syllable separators; not IPA",
        "dataset": {
            "id": DATASET_ID,
            "revision": dataset_revision,
            "split": "test",
            "license_label": "other / nckl-khmer-dictionary-2022",
            "rights_note": (
                "Underlying dictionary content is © National Council of Khmer Language (NCKL), "
                "Royal Academy of Cambodia. No blanket redistribution license is stated. "
                "This run stores aggregate metrics only; check NCKL terms before commercial use "
                "or redistribution."
            ),
        },
        "model": {
            "id": MODEL_ID,
            "revision": model_revision,
            "license": "MIT as declared by the Hugging Face model card",
            "package": MODEL_PACKAGE,
            "package_version": model_package_version,
            "parameters": 7461956,
        },
        "source_attested_test_metrics": {
            "reference_pairs": reference_pairs,
            "unique_words": unique_words,
            "nonempty_outputs": nonempty,
            "output_coverage": nonempty / unique_words,
            "word_exact_matches": exact_matches,
            "word_exact_match_rate": exact_matches / unique_words,
            "character_errors": total_edits,
            "reference_characters": total_reference_characters,
            "character_error_rate": total_edits / total_reference_characters,
            "syllable_count_matches": syllable_matches,
            "syllable_count_accuracy": syllable_matches / unique_words,
            "reference_policy": "For words with multiple NCKL readings, accept any exact alternative; CER uses the alternative with minimum code-point edit distance, matching the upstream evaluator's policy.",
            "normalization": "Unicode NFC is not applied; raw Khmer code-point strings are compared exactly.",
        },
        "independent_ipa_gold_count": 0,
        "ipa_accuracy": None,
        "interpretation": (
            "Held-out NCKL pronunciation-respelling test metrics for this external model only. "
            "Targets are Khmer-script respellings, not IPA; these scores cannot be compared with "
            "the repository's IPA CER or treated as independently adjudicated phonetic accuracy."
        ),
        "limitations": [
            "The test split is word-disjoint from the dataset's train and validation splits, but its labels are NCKL dictionary respellings, not independent IPA adjudication.",
            "Dictionary words only; names, slang, new loanwords and running-speech sandhi are outside the dataset scope.",
            "The dataset card notes that automatic checks may not catch all source errors.",
            "Only aggregate metrics are retained; no dataset rows, words, references, predictions or per-word errors are redistributed.",
            "Commercial use or redistribution requires checking NCKL's terms.",
        ],
        "runtime": runtime or {},
        "provenance": {
            "harness_path": "scripts/benchmark_nckl_respelling.py",
            "harness_sha256": sha256_file(Path(__file__).resolve()),
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "github_event_sha": os.environ.get("GITHUB_SHA"),
            "github_ref": os.environ.get("GITHUB_REF"),
            "github_head_ref": os.environ.get("GITHUB_HEAD_REF"),
        },
    }


def predict_words(
    words: list[str],
    *,
    batch_size: int = 64,
) -> tuple[dict[str, str], dict[str, Any]]:
    """Run the MIT-licensed PyPI package with an immutable Hub model revision."""
    if batch_size < 1:
        raise ValueError("batch_size must be positive")
    try:
        import torch
        from khmer_g2p import KhmerG2P
    except ImportError as exc:
        raise RuntimeError("install the pinned torch and khmer-g2p dependencies") from exc

    torch.set_num_threads(1)
    predictor = KhmerG2P(MODEL_ID, device="cpu", revision=MODEL_REVISION)
    predictions: dict[str, str] = {}
    started = time.perf_counter()
    for offset in range(0, len(words), batch_size):
        batch = words[offset:offset + batch_size]
        outputs = predictor(batch)
        if not isinstance(outputs, list) or len(outputs) != len(batch):
            raise ValueError("khmer-g2p package returned an unexpected batch result")
        predictions.update(zip(batch, outputs, strict=True))
    elapsed = time.perf_counter() - started
    return predictions, {
        "device": "cpu",
        "batch_size": batch_size,
        "inference_elapsed_seconds": round(elapsed, 6),
        "mean_latency_ms_per_unique_word": round(elapsed * 1000 / len(words), 4),
        "torch_version": torch.__version__,
        "model_package_version": importlib.metadata.version(MODEL_PACKAGE),
    }


def load_pinned_test_split() -> tuple[dict[str, list[dict[str, Any]]], dict[str, Any]]:
    try:
        from datasets import load_dataset
    except ImportError as exc:
        raise RuntimeError("install the pinned datasets dependency") from exc
    dataset = load_dataset(DATASET_ID, revision=DATASET_REVISION)
    splits = {name: [dict(row) for row in dataset[name]] for name in ("train", "validation", "test")}
    validate_word_disjoint_splits(splits)
    observed = {name: len(rows) for name, rows in splits.items()}
    if observed != EXPECTED_SPLIT_ROWS:
        raise ValueError(f"pinned NCKL split sizes changed: {observed}")
    if len(group_references(splits["test"])) != EXPECTED_TEST_UNIQUE_WORDS:
        raise ValueError("pinned NCKL test unique-word count changed")
    return splits, {
        "dataset_fingerprint": getattr(dataset["test"], "_fingerprint", None),
        "split_rows": observed,
        "test_unique_words": EXPECTED_TEST_UNIQUE_WORDS,
    }


def write_report(path: Path, report: dict[str, Any]) -> str:
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(rendered, encoding="utf-8")
    digest = sha256_file(path)
    path.with_suffix(path.suffix + ".sha256").write_text(digest + "\n", encoding="ascii")
    return digest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=64)
    args = parser.parse_args()

    splits, dataset_runtime = load_pinned_test_split()
    rows = splits["test"]
    references = group_references(rows)
    predictions, model_runtime = predict_words(list(references), batch_size=args.batch_size)
    package_version = importlib.metadata.version(MODEL_PACKAGE)
    if package_version != MODEL_PACKAGE_VERSION:
        raise ValueError(f"expected {MODEL_PACKAGE}=={MODEL_PACKAGE_VERSION}, found {package_version}")
    report = build_report(
        rows,
        predictions,
        model_revision=MODEL_REVISION,
        dataset_revision=DATASET_REVISION,
        model_package_version=package_version,
        runtime={**dataset_runtime, **model_runtime},
    )
    digest = write_report(args.output, report)
    print(json.dumps({
        "task": report["task"],
        "dataset_revision": DATASET_REVISION,
        "model_revision": MODEL_REVISION,
        "source_attested_test_metrics": report["source_attested_test_metrics"],
        "independent_ipa_gold_count": 0,
        "ipa_accuracy": None,
        "report_sha256": digest,
        "output": str(args.output),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
