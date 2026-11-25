#!/usr/bin/env python3
"""Build the compact deterministic browser lexicon from the pinned Google source."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from khmer_ua.google_phonemic import load_google_phonemic_lexicon, parse_google_phonemic

DEFAULT_OUTPUT = ROOT / "data" / "khmer" / "google-phonemic-source-lexicon.json"


def build_google_phonemic_lexicon() -> dict[str, Any]:
    source = load_google_phonemic_lexicon()
    mapping = source.mapping
    entries: dict[str, list[list[Any]]] = {}
    unresolved_rows = [
        [row.word, row.source_row, row.source_label, "EMPTY_SOURCE_PHONEMIC"]
        for row in source.unresolved_rows
    ]
    mapping_status_counts: Counter[str] = Counter()
    mapped_rows = 0
    unresolved_nonempty_rows = 0

    for word, rows in source.entries.items():
        for row in rows:
            parsed = parse_google_phonemic(row.source_phonemic, mapping)
            if parsed.status != "PROVISIONAL" or parsed.ipa is None:
                unresolved_nonempty_rows += 1
                unresolved_rows.append([
                    row.word,
                    row.source_row,
                    row.source_label,
                    ";".join(parsed.uncertainty) or "UNRESOLVED_PHONEMIC_ADAPTER",
                ])
                continue
            mapped_rows += 1
            mapping_status_counts[parsed.mapping_status] += 1
            # Tuple layout: [source phonemic string, original TSV line, optional label].
            # The browser runs the same token-to-IPA adapter at lookup time.
            entries.setdefault(word, []).append([
                row.source_phonemic,
                row.source_row,
                row.source_label,
            ])

    if mapped_rows + unresolved_nonempty_rows != source.manifest["nonempty_pronunciation_rows"]:
        raise ValueError("Google phonemic lexicon row accounting does not reconcile")
    if unresolved_nonempty_rows:
        raise ValueError(f"{unresolved_nonempty_rows} non-empty Google phonemic rows failed IPA conversion")

    return {
        "schema_version": "google-phonemic-source-lexicon/v1",
        "source": {
            "id": mapping["source"]["id"],
            "revision": mapping["source"]["source_revision"],
            "license": mapping["source"]["license"],
            "source_tsv_path": "data/khmer/google-pronunciation-full.tsv",
            "source_tsv_sha256": source.manifest["source_tsv_sha256"],
            "phonology_path": "data/khmer/google-phonology.json",
            "phonology_git_blob_sha": mapping["source"]["phonology_git_blob_sha"],
            "ipa_map_path": "data/khmer/google-phonemic-to-ipa.json",
            "ipa_map_version": mapping["map_version"],
        },
        "manifest": {
            **source.manifest,
            "mapped_nonempty_rows": mapped_rows,
            "unresolved_nonempty_rows": unresolved_nonempty_rows,
            "mapping_status_counts": dict(sorted(mapping_status_counts.items())),
            "entry_tuple_layout": ["source_phonemic", "source_row", "source_label"],
        },
        "entries": {word: rows for word, rows in sorted(entries.items())},
        "unresolved_rows": sorted(unresolved_rows, key=lambda row: row[1]),
    }


def canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="fail if the committed artifact differs")
    args = parser.parse_args()

    expected = canonical_json(build_google_phonemic_lexicon())
    if args.check:
        if not args.output.exists():
            raise SystemExit(f"missing generated lexicon: {args.output}")
        actual = args.output.read_text(encoding="utf-8")
        if actual != expected:
            raise SystemExit(f"generated lexicon drift: {args.output}")
        print(f"Google phonemic source lexicon is reproducible: {len(expected.encode('utf-8'))} bytes")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(expected, encoding="utf-8")
    print(f"Wrote {args.output} ({len(expected.encode('utf-8'))} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
