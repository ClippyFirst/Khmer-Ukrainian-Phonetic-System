#!/usr/bin/env python3
"""Build deterministic browser shards from the pinned Google phonemic source."""
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
SHARD_COUNT = 8


def canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def build_google_phonemic_lexicon() -> tuple[dict[str, Any], dict[int, dict[str, Any]]]:
    source = load_google_phonemic_lexicon()
    mapping = source.mapping
    buckets: dict[int, dict[str, list[list[Any]]]] = {index: {} for index in range(SHARD_COUNT)}
    unresolved_rows = [
        [row.word, row.source_row, row.source_label, "EMPTY_SOURCE_PHONEMIC"]
        for row in source.unresolved_rows
    ]
    mapping_status_counts: Counter[str] = Counter()
    mapped_rows = 0
    unresolved_nonempty_rows = 0

    for word, rows in source.entries.items():
        shard_id = ord(word[0]) % SHARD_COUNT
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
            buckets[shard_id].setdefault(word, []).append([
                row.source_phonemic,
                row.source_row,
                row.source_label,
            ])

    if mapped_rows + unresolved_nonempty_rows != source.manifest["nonempty_pronunciation_rows"]:
        raise ValueError("Google phonemic lexicon row accounting does not reconcile")
    if unresolved_nonempty_rows:
        raise ValueError(f"{unresolved_nonempty_rows} non-empty Google phonemic rows failed IPA conversion")

    shard_data: dict[int, dict[str, Any]] = {}
    shard_metadata = []
    for shard_id, entries in buckets.items():
        ordered_entries = {word: entries[word] for word in sorted(entries)}
        shard_data[shard_id] = {
            "schema_version": "google-phonemic-source-lexicon-shard/v1",
            "source_id": mapping["source"]["id"],
            "source_revision": mapping["source"]["source_revision"],
            "shard_id": shard_id,
            "entry_tuple_layout": ["source_phonemic", "source_row", "source_label"],
            "entries": ordered_entries,
        }
        shard_metadata.append({
            "id": shard_id,
            "path": f"google-phonemic-source-lexicon-{shard_id}.json",
            "word_count": len(ordered_entries),
            "candidate_count": sum(len(rows) for rows in ordered_entries.values()),
        })

    manifest = {
        "schema_version": "google-phonemic-source-lexicon/v1",
        "source": {
            "id": mapping["source"]["id"],
            "revision": mapping["source"]["source_revision"],
            "license": mapping["source"]["license"],
            "source_tsv_path": "data/khmer/google-pronunciation-full.tsv",
            "source_tsv_sha256": source.manifest["source_tsv_sha256"],
            "phonology_reference": mapping["inventory_reference"],
            "ipa_map_path": "data/khmer/google-phonemic-to-ipa.json",
            "ipa_map_version": mapping["map_version"],
        },
        "manifest": {
            **source.manifest,
            "mapped_nonempty_rows": mapped_rows,
            "unresolved_nonempty_rows": unresolved_nonempty_rows,
            "mapping_status_counts": dict(sorted(mapping_status_counts.items())),
            "entry_tuple_layout": ["source_phonemic", "source_row", "source_label"],
            "shard_count": SHARD_COUNT,
        },
        "shards": shard_metadata,
        "unresolved_rows": sorted(unresolved_rows, key=lambda row: row[1]),
    }
    return manifest, shard_data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="fail if committed artifacts differ")
    args = parser.parse_args()

    manifest, shards = build_google_phonemic_lexicon()
    expected_files = {
        args.output: canonical_json(manifest),
        **{
            args.output.parent / f"{args.output.stem}-{shard_id}.json": canonical_json(shard)
            for shard_id, shard in shards.items()
        },
    }

    if args.check:
        for path, expected in expected_files.items():
            if not path.exists():
                raise SystemExit(f"missing generated lexicon artifact: {path}")
            actual = path.read_text(encoding="utf-8")
            if actual != expected:
                raise SystemExit(f"generated lexicon drift: {path}")
        total_bytes = sum(len(value.encode("utf-8")) for value in expected_files.values())
        print(f"Google phonemic source lexicon is reproducible: {len(expected_files)} files, {total_bytes} bytes")
        return 0

    for path, value in expected_files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8")
    total_bytes = sum(len(value.encode("utf-8")) for value in expected_files.values())
    print(f"Wrote {len(expected_files)} Google phonemic lexicon files ({total_bytes} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
