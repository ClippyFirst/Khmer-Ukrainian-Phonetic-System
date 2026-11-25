#!/usr/bin/env python3
"""Evaluate an offline neural Khmer respelling teacher followed by deterministic IPA phonemization.

The NCKL model emits Khmer-script respelling, not IPA. This harness splits
that output at its explicit syllable hyphens and sends each syllable through
the deterministic Khmer Phonemizer. It compares the bridge with direct
Khmer Phonemizer output on the same small source-attested lexical corpus.

Only aggregate metrics, case indices and hashes are retained. No words,
source IPA, NCKL respellings or generated IPA strings are written.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from benchmark_g2p import (  # noqa: E402
    load_corpus,
    package_version,
    phoneme_tokens,
    source_ipa_from_metadata,
    source_ipa_comparison_key,
)
from benchmark_nckl_respelling import (  # noqa: E402
    MODEL_ID,
    MODEL_REVISION,
    predict_words,
    codepoint_levenshtein,
)
from benchmark_mekongphon_model import sha256_file  # noqa: E402

DEFAULT_CORPUS = ROOT / "data" / "tests" / "verified-lexical-corpus.json"


def phonemize_one(value: str, phonemizer: Callable[[str], Any]) -> str:
    raw = phonemizer(value)
    tokens = phoneme_tokens(raw)
    if tokens is None:
        raise ValueError("Khmer Phonemizer returned an unsupported output shape")
    return "".join(tokens)


def phonemize_respelling(
    respelling: str,
    phonemizer: Callable[[str], Any],
) -> str:
    """Convert each NCKL respelling syllable independently, preserving order."""
    if not isinstance(respelling, str) or not respelling.strip():
        raise ValueError("NCKL respelling must be a non-empty string")
    syllables = respelling.split("-")
    if any(not syllable for syllable in syllables):
        raise ValueError("NCKL respelling contains an empty syllable")
    outputs = []
    for syllable in syllables:
        output = phonemize_one(syllable, phonemizer)
        if not output.strip():
            raise ValueError("Khmer Phonemizer returned an empty syllable output")
        outputs.append(output)
    return ".".join(outputs)


def load_source_corpus(path: Path) -> dict[str, dict[str, Any]]:
    corpus = load_corpus(path)
    selected = {
        word: metadata
        for word, metadata in corpus.items()
        if str(metadata.get("ipa_status", "")).startswith("SOURCE_ATTESTED")
        and isinstance(source_ipa_from_metadata(metadata), str)
    }
    if not selected:
        raise ValueError("no source-attested lexical IPA cases are available")
    return selected


def _metric_bundle(
    corpus: dict[str, dict[str, Any]],
    outputs: dict[str, str],
) -> dict[str, Any]:
    if set(outputs) != set(corpus):
        raise ValueError("expected one IPA output per source-attested input")
    exact_matches = 0
    total_edits = 0
    total_reference_codepoints = 0
    nonempty_outputs = 0
    records = []
    for index, (word, metadata) in enumerate(corpus.items(), start=1):
        source_ipa = source_ipa_from_metadata(metadata)
        if not isinstance(source_ipa, str) or not source_ipa.strip():
            raise ValueError("every selected source case requires non-empty IPA")
        reference = source_ipa_comparison_key(source_ipa)
        raw_output = outputs[word]
        if not isinstance(raw_output, str):
            raise ValueError("every pipeline output must be a string")
        hypothesis = source_ipa_comparison_key(raw_output) if raw_output.strip() else ""
        edits = codepoint_levenshtein(reference, hypothesis) if hypothesis else len(reference)
        exact = bool(hypothesis) and hypothesis == reference
        exact_matches += int(exact)
        total_edits += edits
        total_reference_codepoints += len(reference)
        nonempty_outputs += int(bool(raw_output.strip()))
        records.append({
            "case_index": index,
            "input_sha256": hashlib.sha256(word.encode("utf-8")).hexdigest(),
            "source_reference_sha256": hashlib.sha256(reference.encode("utf-8")).hexdigest(),
            "output_sha256": hashlib.sha256(hypothesis.encode("utf-8")).hexdigest() if hypothesis else None,
            "source_attested_exact_match": exact,
            "codepoint_edits": edits,
            "reference_codepoints": len(reference),
        })
    return {
        "input_count": len(corpus),
        "nonempty_outputs": nonempty_outputs,
        "output_coverage": nonempty_outputs / len(corpus),
        "strict_source_attested_matches": exact_matches,
        "source_attested_exact_match_rate": exact_matches / len(corpus),
        "character_errors": total_edits,
        "reference_codepoints": total_reference_codepoints,
        "character_error_rate": total_edits / total_reference_codepoints if total_reference_codepoints else None,
        "records": records,
    }


def build_report(
    corpus: dict[str, dict[str, Any]],
    respellings: dict[str, str],
    direct_outputs: dict[str, str],
    bridge_outputs: dict[str, str],
    *,
    model_revision: str,
    phonemizer_version: str | None,
    corpus_sha256: str,
    runtime: dict[str, Any] | None = None,
) -> dict[str, Any]:
    expected = set(corpus)
    if set(respellings) != expected or set(direct_outputs) != expected or set(bridge_outputs) != expected:
        raise ValueError("expected one respelling and two IPA outputs per input")
    if any(not isinstance(value, str) for value in respellings.values()):
        raise ValueError("every neural respelling must be a string")
    if any(not isinstance(value, str) for value in direct_outputs.values()):
        raise ValueError("every direct IPA output must be a string")
    if any(not isinstance(value, str) for value in bridge_outputs.values()):
        raise ValueError("every bridged IPA output must be a string")

    direct = _metric_bundle(corpus, direct_outputs)
    bridge = _metric_bundle(corpus, bridge_outputs)
    respelling_coverage = sum(bool(value.strip()) for value in respellings.values())
    return {
        "schema_version": "1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "task": "NCKL Khmer respelling -> deterministic Khmer Phonemizer -> IPA",
        "model": {
            "id": MODEL_ID,
            "revision": model_revision,
            "license": "MIT as declared by the model card",
            "target_representation": "NCKL Khmer-script pronunciation respelling; not IPA",
        },
        "deterministic_phonemizer": {
            "package": "khmerphonemizer",
            "version": phonemizer_version,
            "license": "MIT as declared by the package metadata",
        },
        "profile_match": "UNVERIFIED",
        "ipa_kind": "UNRESOLVED",
        "corpus": "data/tests/verified-lexical-corpus.json",
        "corpus_sha256": corpus_sha256,
        "input_count": len(corpus),
        "nckl_respelling_nonempty": respelling_coverage,
        "nckl_respelling_coverage": respelling_coverage / len(corpus),
        "normalization": "NFC and existing source-IPA diagnostic key: outer /.../, whitespace, syllable dots and stress marks removed; phone symbols, aspiration, length and diacritics retained",
        "direct_phonemizer": direct,
        "nckl_respelling_phonemizer": bridge,
        "bridge_improvement": {
            "strict_match_delta": bridge["strict_source_attested_matches"] - direct["strict_source_attested_matches"],
            "character_error_delta": bridge["character_errors"] - direct["character_errors"],
            "cer_delta": (
                bridge["character_error_rate"] - direct["character_error_rate"]
                if bridge["character_error_rate"] is not None and direct["character_error_rate"] is not None
                else None
            ),
        },
        "independent_gold_count": 0,
        "accuracy": None,
        "score_status": "SOURCE_ATTESTED_DIAGNOSTIC_NOT_ACCURACY",
        "rule_promotion": "BLOCKED_INDEPENDENT_GOLD_AND_PROFILE_VALIDATION",
        "rights": {
            "model_weights": "MIT as declared by the model card",
            "training_data": "NCKL Khmer Dictionary 2022; underlying dictionary rights remain with NCKL; no blanket redistribution license is declared",
            "runtime_outputs": "Ephemeral only; no respellings, source words, source IPA or generated IPA are retained in the report",
            "redistribution_status": "REVIEW_REQUIRED",
        },
        "runtime": runtime or {},
        "provenance": {
            "harness_path": "scripts/benchmark_nckl_phonemizer_bridge.py",
            "harness_sha256": sha256_file(Path(__file__).resolve()),
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "github_event_sha": os.environ.get("GITHUB_SHA"),
            "github_ref": os.environ.get("GITHUB_REF"),
            "github_head_ref": os.environ.get("GITHUB_HEAD_REF"),
        },
        "records": [
            {
                "case_index": index,
                "input_sha256": hashlib.sha256(word.encode("utf-8")).hexdigest(),
                "respelling_sha256": hashlib.sha256(respellings[word].encode("utf-8")).hexdigest() if respellings[word] else None,
            }
            for index, word in enumerate(corpus, start=1)
        ],
        "limitations": [
            "The selected corpus contains only source-attested Wiktionary lexical IPA strings, not independent expert IPA gold.",
            "The NCKL model predicts Khmer-script respelling, not IPA; the deterministic phonemizer's mapping from that respelling is a separate unvalidated adapter.",
            "The NCKL model's standard pronunciation profile is not demonstrated equivalent to the project's careful-citation profile.",
            "The NCKL source dictionary is copyrighted by NCKL; no dataset rows or generated outputs are retained or redistributed.",
            "The source corpus is small and includes no complete consonant-series × vowel × coda × syllable-type cross-product.",
            "Tone, phonation and connected-speech sandhi are not validated by this diagnostic.",
            "A positive result would justify further research only; it would not authorize generalized runtime rules or an accuracy claim.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=64)
    args = parser.parse_args()
    if args.batch_size < 1:
        parser.error("--batch-size must be positive")

    corpus_bytes = args.corpus.read_bytes()
    corpus = load_source_corpus(args.corpus)
    words = list(corpus)
    respellings, model_runtime = predict_words(words, batch_size=args.batch_size)

    try:
        from khmerphonemizer import phonemize_single
    except ImportError as exc:
        raise RuntimeError("install the optional pinned khmerphonemizer package") from exc

    direct_outputs: dict[str, str] = {}
    bridge_outputs: dict[str, str] = {}
    direct_started = time.perf_counter()
    for word in words:
        try:
            direct_outputs[word] = phonemize_one(word, phonemize_single)
        except Exception:
            direct_outputs[word] = ""
    direct_elapsed = time.perf_counter() - direct_started

    bridge_started = time.perf_counter()
    for word in words:
        try:
            bridge_outputs[word] = phonemize_respelling(respellings[word], phonemize_single)
        except Exception:
            bridge_outputs[word] = ""
    bridge_elapsed = time.perf_counter() - bridge_started

    runtime = {
        "nckl_model": model_runtime,
        "direct_phonemizer_elapsed_seconds": round(direct_elapsed, 6),
        "bridge_phonemizer_elapsed_seconds": round(bridge_elapsed, 6),
        "device": "cpu",
        "batch_size": args.batch_size,
    }
    report = build_report(
        corpus,
        respellings,
        direct_outputs,
        bridge_outputs,
        model_revision=MODEL_REVISION,
        phonemizer_version=package_version("khmerphonemizer"),
        corpus_sha256=hashlib.sha256(corpus_bytes).hexdigest(),
        runtime=runtime,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\\n"
    args.output.write_text(rendered, encoding="utf-8")
    print(json.dumps({
        "input_count": report["input_count"],
        "nckl_respelling_coverage": report["nckl_respelling_coverage"],
        "direct_phonemizer": {
            "exact": report["direct_phonemizer"]["strict_source_attested_matches"],
            "cer": report["direct_phonemizer"]["character_error_rate"],
        },
        "nckl_respelling_phonemizer": {
            "exact": report["nckl_respelling_phonemizer"]["strict_source_attested_matches"],
            "cer": report["nckl_respelling_phonemizer"]["character_error_rate"],
        },
        "bridge_improvement": report["bridge_improvement"],
        "independent_gold_count": 0,
        "accuracy": None,
        "rule_promotion": report["rule_promotion"],
        "output": str(args.output),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
