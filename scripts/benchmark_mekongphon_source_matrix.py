#!/usr/bin/env python3
"""Compare the pinned MekongPhon teacher with the repository's tiny source-backed IPA matrix.

This is a diagnostic gate for future rule distillation, not an accuracy benchmark.
The matrix contains representative source transcriptions, not independent gold.
The report intentionally omits source words, source IPA and raw model predictions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from benchmark_mekongphon_model import (  # noqa: E402
    MODEL_ID,
    MODEL_REVISION,
    codepoint_levenshtein,
    predict,
    sha256_file,
)

DEFAULT_REGISTER = ROOT / "data" / "khmer" / "vowel-context-register.json"


def normalize_ipa(value: str) -> str:
    """Apply only NFC and removal of one outer /.../ or [...] pair."""
    if not isinstance(value, str):
        raise ValueError("IPA value must be a string")
    normalized = unicodedata.normalize("NFC", value.strip())
    if len(normalized) >= 2 and (
        (normalized.startswith("/") and normalized.endswith("/"))
        or (normalized.startswith("[") and normalized.endswith("]"))
    ):
        normalized = normalized[1:-1]
    if not normalized:
        raise ValueError("IPA value must not be empty")
    return normalized


def load_source_cases(register: dict[str, Any]) -> list[dict[str, Any]]:
    """Select only explicit, non-conflicting, source-attested cases with IPA."""
    if not isinstance(register, dict) or not isinstance(register.get("cases"), list):
        raise ValueError("source register must contain a cases array")
    selected = []
    seen_ids: set[str] = set()
    seen_orthographies: set[str] = set()
    for case in register["cases"]:
        if case.get("status") != "SOURCE_ATTESTED_NOT_GOLD":
            continue
        if not isinstance(case.get("ipa"), str) or not case["ipa"].strip():
            continue
        case_id = case.get("id")
        orthography = case.get("orthography")
        source_id = case.get("ipa_source")
        if not all(isinstance(value, str) and value.strip() for value in (case_id, orthography, source_id)):
            raise ValueError("every selected source case requires id, orthography and ipa_source")
        normalized_orthography = unicodedata.normalize("NFC", orthography)
        if case_id in seen_ids:
            raise ValueError("duplicate source case ID: " + case_id)
        if normalized_orthography in seen_orthographies:
            raise ValueError("duplicate normalized source orthography: " + normalized_orthography)
        normalize_ipa(case["ipa"])
        seen_ids.add(case_id)
        seen_orthographies.add(normalized_orthography)
        selected.append({
            "id": case_id,
            "orthography": normalized_orthography,
            "ipa": case["ipa"],
            "ipa_source": source_id,
        })
    if not selected:
        raise ValueError("no non-conflicting source-attested IPA cases are available")
    return selected


def build_report(
    cases: list[dict[str, Any]],
    predictions: list[str],
    *,
    model_revision: str,
    corpus_sha256: str,
    runtime: dict[str, str] | None = None,
    decoding: str = "greedy",
) -> dict[str, Any]:
    if len(cases) != len(predictions):
        raise ValueError("expected one prediction per source case")
    if not cases:
        raise ValueError("cannot compare an empty source matrix")
    if decoding not in {"greedy", "beam4"}:
        raise ValueError("decoding must be 'greedy' or 'beam4'")

    strict_matches = 0
    total_errors = 0
    total_reference_codepoints = 0
    records = []
    for case, raw_output in zip(cases, predictions, strict=True):
        if not isinstance(raw_output, str) or not raw_output.strip():
            raise ValueError("every model prediction must be a non-empty string")
        reference = normalize_ipa(case["ipa"])
        hypothesis = normalize_ipa(raw_output)
        edits = codepoint_levenshtein(reference, hypothesis)
        exact = reference == hypothesis
        strict_matches += int(exact)
        total_errors += edits
        total_reference_codepoints += len(reference)
        records.append({
            "case_id": case["id"],
            "source_attested_exact_match": exact,
            "codepoint_edits": edits,
            "reference_codepoints": len(reference),
            "source_reference_sha256": hashlib.sha256(reference.encode("utf-8")).hexdigest(),
        })

    cer = total_errors / total_reference_codepoints if total_reference_codepoints else None
    return {
        "schema_version": "1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "engine": MODEL_ID,
        "engine_revision": model_revision,
        "engine_license": "Apache-2.0 as declared by the model card",
        "decoding": decoding,
        "profile": "khmer-pph-careful-citation-v1",
        "profile_match": "UNVERIFIED",
        "corpus": "data/khmer/vowel-context-register.json",
        "corpus_sha256": corpus_sha256,
        "source_ids": sorted({case["ipa_source"] for case in cases}),
        "input_count": len(cases),
        "source_case_count": len(cases),
        "reference_convention": "source transcription preserved verbatim apart from NFC and outer delimiter removal",
        "source_attested_diagnostic": {
            "strict_matches": strict_matches,
            "character_errors": total_errors,
            "reference_codepoints": total_reference_codepoints,
            "codepoint_cer": cer,
            "normalization": "Unicode NFC plus removal of one outer /.../ or [...] delimiter pair only",
            "interpretation": "Concordance with representative source transcriptions only; not independent project accuracy.",
        },
        "candidate_rules_emitted": 0,
        "rule_promotion": "BLOCKED_INSUFFICIENT_CONTEXT_AND_INDEPENDENT_GOLD",
        "independent_gold_count": 0,
        "accuracy": None,
        "score_status": "SOURCE_ATTESTED_DIAGNOSTIC_NOT_ACCURACY",
        "runtime": runtime or {},
        "provenance": {
            "harness_path": "scripts/benchmark_mekongphon_source_matrix.py",
            "harness_sha256": sha256_file(Path(__file__).resolve()),
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "github_event_sha": os.environ.get("GITHUB_SHA"),
            "github_ref": os.environ.get("GITHUB_REF"),
            "github_head_ref": os.environ.get("GITHUB_HEAD_REF"),
        },
        "records": records,
        "limitations": [
            "The selected matrix contains only representative source-attested forms, not a complete contextual cross-product.",
            "The source transcriptions are not independently adjudicated project IPA gold.",
            "The teacher's dialect, style and transcription convention are not demonstrated equivalent to the selected Phnom Penh careful-citation profile.",
            "The source matrix contains conflicting analyses that are deliberately excluded from this comparison.",
            "The model's output omits tone; this comparison cannot validate tone or phonation.",
            "Agreement on these examples does not authorize generalization to unseen vowel, coda, syllable or lexical contexts.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--register", type=Path, default=DEFAULT_REGISTER)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=8)
    args = parser.parse_args()
    if args.batch_size < 1:
        parser.error("--batch-size must be positive")

    register_bytes = args.register.read_bytes()
    register = json.loads(register_bytes)
    cases = load_source_cases(register)
    words = [case["orthography"] for case in cases]
    corpus_sha256 = hashlib.sha256(register_bytes).hexdigest()
    greedy_predictions, greedy_runtime = predict(
        words,
        model_revision=MODEL_REVISION,
        batch_size=args.batch_size,
        num_beams=1,
    )
    beam4_predictions, beam4_runtime = predict(
        words,
        model_revision=MODEL_REVISION,
        batch_size=args.batch_size,
        num_beams=4,
    )
    report = build_report(
        cases,
        greedy_predictions,
        model_revision=MODEL_REVISION,
        corpus_sha256=corpus_sha256,
        runtime=greedy_runtime,
        decoding="greedy",
    )
    beam4_report = build_report(
        cases,
        beam4_predictions,
        model_revision=MODEL_REVISION,
        corpus_sha256=corpus_sha256,
        runtime=beam4_runtime,
        decoding="beam4",
    )
    report["decoding_comparison"] = {
        "greedy": {
            "strict_matches": report["source_attested_diagnostic"]["strict_matches"],
            "character_errors": report["source_attested_diagnostic"]["character_errors"],
            "reference_codepoints": report["source_attested_diagnostic"]["reference_codepoints"],
            "codepoint_cer": report["source_attested_diagnostic"]["codepoint_cer"],
            "records": report["records"],
        },
        "beam4": {
            "strict_matches": beam4_report["source_attested_diagnostic"]["strict_matches"],
            "character_errors": beam4_report["source_attested_diagnostic"]["character_errors"],
            "reference_codepoints": beam4_report["source_attested_diagnostic"]["reference_codepoints"],
            "codepoint_cer": beam4_report["source_attested_diagnostic"]["codepoint_cer"],
            "records": beam4_report["records"],
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
    print(json.dumps({
        "output": str(args.output),
        "input_count": report["source_case_count"],
        "greedy": report["decoding_comparison"]["greedy"],
        "beam4": report["decoding_comparison"]["beam4"],
        "candidate_rules_emitted": 0,
        "rule_promotion": report["rule_promotion"],
        "accuracy": None,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
