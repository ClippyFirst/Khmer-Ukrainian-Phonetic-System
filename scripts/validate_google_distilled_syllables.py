#!/usr/bin/env python3
"""Validate the static neural-distilled Khmer syllable artifact."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "deterministic-khmer-phonology.schema.json"
MANIFEST_PATH = ROOT / "data" / "khmer" / "google-phonemic-source-lexicon.json"


def validate_artifact(path: Path) -> dict:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    artifact = json.loads(path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(artifact), key=lambda error: tuple(str(part) for part in error.absolute_path))
    if errors:
        details = "; ".join(
            f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
            for error in errors[:20]
        )
        raise ValueError(f"distilled syllable artifact schema validation failed: {details}")

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    source = artifact["source"]
    if source["revision"] != manifest["source"]["revision"]:
        raise ValueError("distilled artifact source revision does not match pinned lexicon")
    if source["tsv_sha256"] != manifest["source"]["source_tsv_sha256"]:
        raise ValueError("distilled artifact source TSV hash does not match pinned lexicon")

    accepted = len(artifact["candidates"])
    inventory_count = artifact["inventory"]["oov_syllable_candidates"]
    rejected_count = sum(artifact["rejected"].values())
    if accepted + rejected_count != inventory_count:
        raise ValueError(
            "distilled artifact count mismatch: "
            f"accepted {accepted} + rejected {rejected_count} != inventory {inventory_count}"
        )
    if artifact["teacher"]["accuracy"] is not None:
        raise ValueError("teacher artifact must not claim independent pronunciation accuracy")
    if artifact["teacher"]["profile_equivalence"] != "UNVERIFIED":
        raise ValueError("teacher target-profile equivalence must remain UNVERIFIED")

    candidates = {item["orthography"]: item for item in artifact["candidates"]}
    # Regression probes are test inputs, not lexical additions. They verify
    # that the generated CV/CVC transducer generalizes without word lookup.
    for probe in ("កិ",):
        candidate = candidates.get(probe)
        if candidate is None or candidate.get("tier") != "soft":
            raise ValueError(f"generated Soft CV/CVC candidate missing for regression probe {probe!r}")
        if not candidate.get("google_phonemic_tokens") or not candidate.get("ipa") or not candidate.get("ukrainian_candidate"):
            raise ValueError(f"generated Soft candidate is incomplete for regression probe {probe!r}")
    return artifact


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", type=Path)
    args = parser.parse_args()
    artifact = validate_artifact(args.artifact)
    print(json.dumps({
        "schema": artifact["schema"],
        "accepted_candidates": len(artifact["candidates"]),
        "accepted_soft_candidates": sum(item["tier"] == "soft" for item in artifact["candidates"]),
        "accepted_exploratory_candidates": sum(item["tier"] == "exploratory" for item in artifact["candidates"]),
        "rejected_candidates": sum(artifact["rejected"].values()),
        "source_revision": artifact["source"]["revision"],
        "accuracy": artifact["teacher"]["accuracy"],
        "profile_equivalence": artifact["teacher"]["profile_equivalence"],
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
