#!/usr/bin/env python3
"""Compare the same four Khmer IPA engines on the non-overlapping IPA-Dict subset.

IPA-Dict's Khmer data are derived from aakanee.com and carry CC BY-NC-SA 4.0
source-data terms. The runner is ephemeral and prints aggregate metrics only.
"""
from __future__ import annotations

import argparse
import csv
import importlib.metadata
import json
import re
import sys
import time
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from benchmark_mekongphon_model import (  # noqa: E402
    MODEL_REVISION,
    codepoint_levenshtein,
    load_rows,
    sha256_file,
    predict as predict_mekongphon,
)
from benchmark_shared_mekongphon import ipa_from_internal_result, phonemizer_output  # noqa: E402
from khmer_ua import RuleBasedKhmerEngine  # noqa: E402


def package_version(name: str) -> str | None:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def load_ipa_dict(path: Path) -> dict[str, list[str]]:
    references: dict[str, set[str]] = defaultdict(set)
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) != 2 or not parts[0].strip():
            raise ValueError(f"IPA-Dict line {line_number} must contain orthography<TAB>IPA")
        alternatives = re.findall(r"/([^/]+)/", parts[1])
        if not alternatives:
            raise ValueError(f"IPA-Dict line {line_number} contains no slash-delimited IPA")
        for alternative in alternatives:
            value = unicodedata.normalize("NFC", alternative)
            if value.strip():
                references[orthography].add(value)
    if not references:
        raise ValueError("IPA-Dict file contains no pronunciation rows")
    return {word: sorted(values) for word, values in references.items()}


def evaluate_multi_reference(
    references: dict[str, list[str]],
    words: list[str],
    outputs: list[str],
    statuses: list[str],
    *,
    elapsed_seconds: float,
    version: str | None,
) -> dict:
    if not (len(words) == len(outputs) == len(statuses)):
        raise ValueError("every engine must return one output/status per word")
    exact = 0
    edits = 0
    reference_chars = 0
    available = 0
    partial = 0
    for word, output, status in zip(words, outputs, statuses, strict=True):
        alternatives = references[word]
        hypothesis = unicodedata.normalize("NFC", output)
        available += int(bool(hypothesis.strip()))
        partial += int(status.startswith(("PARTIAL", "PROVISIONAL")))
        exact += int(bool(hypothesis) and hypothesis in alternatives)
        scored = min(
            ((codepoint_levenshtein(reference, hypothesis), len(reference)) for reference in alternatives),
            key=lambda item: (item[0] / max(item[1], 1), item[0], item[1]),
        )
        edits += scored[0]
        reference_chars += scored[1]
    return {
        "version": version,
        "inputs": len(words),
        "nonempty_outputs": available,
        "output_coverage_percent": round(100 * available / len(words), 2),
        "partial_or_provisional_outputs": partial,
        "strict_source_attested_matches": exact,
        "source_attested_exact_match_percent": round(100 * exact / len(words), 2),
        "codepoint_edits_best_of_reference_alternatives": edits,
        "selected_reference_codepoints": reference_chars,
        "source_attested_codepoint_CER_percent": round(100 * edits / reference_chars, 2) if reference_chars else None,
        "elapsed_seconds": round(elapsed_seconds, 3),
        "ms_per_input": round(1000 * elapsed_seconds / len(words), 3),
        "score_status": "SOURCE_ATTESTED_DIAGNOSTIC_NOT_ACCURACY",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ipa-dict", type=Path, required=True)
    parser.add_argument("--mekong-train", type=Path, required=True)
    parser.add_argument("--mekong-eval", type=Path, required=True)
    args = parser.parse_args()

    refs_all = load_ipa_dict(args.ipa_dict)
    train_words = {unicodedata.normalize("NFC", row["orth"]) for row in load_rows(args.mekong_train)}
    eval_words = {unicodedata.normalize("NFC", row["orth"]) for row in load_rows(args.mekong_eval)}
    overlap_train = set(refs_all) & train_words
    overlap_eval = set(refs_all) & eval_words
    refs = {
        word: alternatives
        for word, alternatives in refs_all.items()
        if word not in train_words and word not in eval_words
    }
    words = sorted(refs)
    if len(words) < 100:
        raise ValueError(f"too few non-overlapping IPA-Dict words: {len(words)}")

    report = {
        "corpus": "open-dict-data/ipa-dict Khmer data/km.txt",
        "corpus_source_revision": "972cd67dd5f96bc5660e28070cde26e3928abcd7",
        "corpus_file_sha256": sha256_file(args.ipa_dict),
        "corpus_rows": sum(1 for line in args.ipa_dict.read_text(encoding="utf-8").splitlines() if line.strip()),
        "unique_orthographies": len(refs_all),
        "unique_orthographies_after_deduplication_and_leakage_filter": len(words),
        "words_overlapping_mekongphon_train_excluded": len(overlap_train),
        "words_overlapping_mekongphon_eval_excluded": len(overlap_eval),
        "multi_reference_words": sum(len(values) > 1 for values in refs.values()),
        "reference_normalization": "remove outer slash delimiters; Unicode NFC only; retain internal whitespace and IPA symbols",
        "multiple_reference_scoring": "best normalized code-point edit ratio among source-listed alternatives",
        "independent_gold_count": 0,
        "accuracy": None,
        "limitations": [
            "IPA-Dict Khmer is source-derived from aakanee.com and not independently adjudicated by this project.",
            "The source does not establish a profile equivalence with Phnom Penh careful-citation Khmer.",
            "Words overlapping the MekongPhon train or eval split are excluded to reduce model data leakage.",
            "The data source carries CC BY-NC-SA 4.0 terms; this run is ephemeral and aggregate-only.",
            "Character CER is a notation-sensitive diagnostic, not a phonetic-feature metric.",
        ],
        "engines": {},
    }

    engine = RuleBasedKhmerEngine()
    outputs, statuses = [], []
    started = time.perf_counter()
    for word in words:
        output, status = ipa_from_internal_result(engine.analyze(word))
        outputs.append(output)
        statuses.append(status)
    report["engines"]["project-rule-engine"] = evaluate_multi_reference(
        refs, words, outputs, statuses,
        elapsed_seconds=time.perf_counter() - started,
        version=engine.engine_id,
    )

    outputs, statuses = [], []
    started = time.perf_counter()
    for word in words:
        try:
            outputs.append(phonemizer_output(word))
            statuses.append("OUTPUT")
        except Exception as exc:
            outputs.append("")
            statuses.append(f"ERROR:{type(exc).__name__}")
    report["engines"]["khmerphonemizer"] = evaluate_multi_reference(
        refs, words, outputs, statuses,
        elapsed_seconds=time.perf_counter() - started,
        version=package_version("khmerphonemizer"),
    )

    import epitran
    epi = epitran.Epitran("khm-Khmr")
    outputs, statuses = [], []
    started = time.perf_counter()
    for word in words:
        try:
            value = epi.transliterate(word)
            outputs.append(value or "")
            statuses.append("OUTPUT" if value else "EMPTY")
        except Exception as exc:
            outputs.append("")
            statuses.append(f"ERROR:{type(exc).__name__}")
    report["engines"]["epitran-khm-Khmr"] = evaluate_multi_reference(
        refs, words, outputs, statuses,
        elapsed_seconds=time.perf_counter() - started,
        version=package_version("epitran"),
    )

    outputs, metadata = predict_mekongphon(words, model_revision=MODEL_REVISION)
    report["engines"]["mekongphon-neural"] = evaluate_multi_reference(
        refs, words, outputs, ["OUTPUT" if value.strip() else "EMPTY" for value in outputs],
        elapsed_seconds=float(metadata["inference_elapsed_seconds"]),
        version=f'{metadata["transformers_version"]} / {metadata["torch_version"]}',
    )
    report["engines"]["mekongphon-neural"]["model_revision"] = MODEL_REVISION
    report["engines"]["mekongphon-neural"]["device"] = metadata["device"]

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
