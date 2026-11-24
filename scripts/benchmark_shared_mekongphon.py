#!/usr/bin/env python3
"""Run the same pinned MekongPhon holdout through independent Khmer G2P engines.

This is a source-attested diagnostic, not independent IPA gold. The script
prints aggregate metrics only; it never writes or redistributes corpus rows,
references, or per-word predictions.
"""
from __future__ import annotations

import argparse
import importlib.metadata
import json
import re
import sys
import time
import unicodedata
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from benchmark_mekongphon_model import (  # noqa: E402
    MODEL_REVISION,
    CORPUS_SOURCE_COMMIT,
    codepoint_levenshtein,
    load_rows,
    predict as predict_mekongphon,
)


def package_version(name: str) -> str | None:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def ipa_from_internal_result(result: dict) -> tuple[str, str]:
    """Keep canonical IPA distinct; expose only evidence-backed partial previews."""
    value = result.get("ipa")
    if isinstance(value, str) and value.strip():
        # The rule engine uses typed placeholders for unresolved units. Remove
        # placeholders only to measure how much partial IPA survives; never
        # interpret them as phones or upgrade the status.
        partial = re.sub(r"⟦[^⟧]+⟧", "", value).strip()
        if partial and partial != value:
            return partial, "PARTIAL_PLACEHOLDER_STRIPPED_FOR_DIAGNOSTIC"
        if "⟦" not in value:
            return value, str(result.get("status", "OUTPUT"))
    provisional = result.get("provisional_ipa")
    if isinstance(provisional, str) and provisional.strip():
        return provisional, "PROVISIONAL_ONSET_PREVIEW"
    return "", str(result.get("status", "UNRESOLVED"))


def phonemizer_output(text: str) -> str:
    from khmerphonemizer import phonemize_single
    from benchmark_g2p import phoneme_tokens
    raw = phonemize_single(text)
    if isinstance(raw, str):
        return raw
    tokens = phoneme_tokens(raw)
    if tokens is not None:
        return "".join(tokens)
    raise ValueError(f"unexpected khmerphonemizer output type: {type(raw).__name__}")


def evaluate(
    rows: list[dict[str, str]],
    outputs: list[str],
    statuses: list[str],
    *,
    elapsed_seconds: float,
    version: str | None,
) -> dict:
    if len(outputs) != len(rows) or len(statuses) != len(rows):
        raise ValueError("every engine must return one output/status per input")
    exact = 0
    edits = 0
    ref_chars = 0
    available = 0
    partial = 0
    for row, output, status in zip(rows, outputs, statuses, strict=True):
        reference = unicodedata.normalize("NFC", row["pron_no_tones"])
        hypothesis = unicodedata.normalize("NFC", output)
        exact += int(bool(hypothesis) and hypothesis == reference)
        edits += codepoint_levenshtein(reference, hypothesis)
        ref_chars += len(reference)
        available += int(bool(hypothesis.strip()))
        partial += int(status.startswith(("PARTIAL", "PROVISIONAL")))
    return {
        "version": version,
        "inputs": len(rows),
        "nonempty_outputs": available,
        "output_coverage_percent": round(100 * available / len(rows), 2),
        "partial_or_provisional_outputs": partial,
        "strict_source_attested_matches": exact,
        "source_attested_exact_match_percent": round(100 * exact / len(rows), 2),
        "codepoint_edits": edits,
        "reference_codepoints": ref_chars,
        "source_attested_codepoint_CER_percent": round(100 * edits / ref_chars, 2) if ref_chars else None,
        "elapsed_seconds": round(elapsed_seconds, 3),
        "ms_per_input": round(1000 * elapsed_seconds / len(rows), 3),
        "score_status": "SOURCE_ATTESTED_DIAGNOSTIC_NOT_ACCURACY",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, required=True)
    args = parser.parse_args()
    rows = load_rows(args.corpus)
    words = [row["orth"] for row in rows]
    report = {
        "corpus": "MekongPhon Khmer held-out lexical evaluation split",
        "corpus_source_commit": CORPUS_SOURCE_COMMIT,
        "input_count": len(rows),
        "reference_field": "pron_no_tones (source-reported IPA without tone)",
        "normalization": "Unicode NFC only; no phone, tone, length, or diacritic normalization",
        "independent_gold_count": 0,
        "accuracy": None,
        "engines": {},
        "limitations": [
            "MekongPhon's upstream repository snapshot has no declared corpus-data license.",
            "The 100-row held-out split is source-attested, not independently adjudicated.",
            "The model and the deterministic project engine do not share a demonstrated dialect/profile/IPA convention.",
            "The reference omits tone; this run does not evaluate tone or phonation.",
            "Character CER is a notation-sensitive string diagnostic, not a phonetic-feature metric.",
        ],
    }

    # Project deterministic engine.
    from khmer_ua import RuleBasedKhmerEngine
    engine = RuleBasedKhmerEngine()
    outputs, statuses = [], []
    started = time.perf_counter()
    for word in words:
        result = engine.analyze(word)
        output, status = ipa_from_internal_result(result)
        outputs.append(output)
        statuses.append(status)
    elapsed = time.perf_counter() - started
    report["engines"]["project-rule-engine"] = evaluate(
        rows, outputs, statuses, elapsed_seconds=elapsed, version=engine.engine_id
    )
    report["engines"]["project-rule-engine"]["profile"] = engine.profile

    # Khmer Phonemizer package (MIT; external candidate, profile unverified).
    try:
        outputs, statuses = [], []
        started = time.perf_counter()
        for word in words:
            try:
                outputs.append(phonemizer_output(word))
                statuses.append("OUTPUT")
            except Exception as exc:
                outputs.append("")
                statuses.append(f"ERROR:{type(exc).__name__}")
        elapsed = time.perf_counter() - started
        report["engines"]["khmerphonemizer"] = evaluate(
            rows, outputs, statuses, elapsed_seconds=elapsed,
            version=package_version("khmerphonemizer"),
        )
        report["engines"]["khmerphonemizer"]["profile"] = "UNVERIFIED"
    except Exception as exc:
        report["engines"]["khmerphonemizer"] = {"status": "BLOCKED", "reason": f"{type(exc).__name__}: {exc}"}

    # Epitran's published khm-Khmr mapping, if present in the pinned package.
    try:
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
        elapsed = time.perf_counter() - started
        report["engines"]["epitran-khm-Khmr"] = evaluate(
            rows, outputs, statuses, elapsed_seconds=elapsed,
            version=package_version("epitran"),
        )
        report["engines"]["epitran-khm-Khmr"]["profile"] = "UNVERIFIED"
    except Exception as exc:
        report["engines"]["epitran-khm-Khmr"] = {"status": "BLOCKED", "reason": f"{type(exc).__name__}: {exc}"}

    # Neural MekongPhon model pinned to the exact revision used by the
    # repository's existing benchmark harness.
    try:
        outputs, metadata = predict_mekongphon(words, model_revision=MODEL_REVISION)
        started = time.perf_counter()
        # The upstream helper includes inference time in metadata; its model
        # loading time is intentionally not mixed with per-input latency.
        elapsed = float(metadata["inference_elapsed_seconds"])
        statuses = ["OUTPUT" if value.strip() else "EMPTY" for value in outputs]
        report["engines"]["mekongphon-neural"] = evaluate(
            rows, outputs, statuses, elapsed_seconds=elapsed,
            version=f"{metadata['transformers_version']} / {metadata['torch_version']}",
        )
        report["engines"]["mekongphon-neural"]["model_id"] = "byumatrixlab/khmer-ipa"
        report["engines"]["mekongphon-neural"]["model_revision"] = MODEL_REVISION
        report["engines"]["mekongphon-neural"]["device"] = metadata["device"]
        report["engines"]["mekongphon-neural"]["profile"] = "UPSTREAM_PROFILE_NOT_YET_EQUIVALENCE_VERIFIED"
    except Exception as exc:
        report["engines"]["mekongphon-neural"] = {"status": "BLOCKED", "reason": f"{type(exc).__name__}: {exc}"}

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["engines"]["project-rule-engine"]["inputs"] == len(rows) else 2


if __name__ == "__main__":
    raise SystemExit(main())
