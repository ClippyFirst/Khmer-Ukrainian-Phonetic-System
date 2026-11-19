from __future__ import annotations

import csv
from pathlib import Path


def test_pcgn_vowel_rows_are_reconciled_against_the_pinned_ungegn_candidate():
    root = Path(__file__).resolve().parents[1]
    path = root / "data/khmer/pcgn_ungegn_vowel_profile_comparison.csv"
    with path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))

    assert len(rows) == 48
    assert all(row["pcgn_source_locator"] for row in rows)
    assert all(
        row["candidate_source_locator"].startswith(
            "pheasaKhmer/khmer-engine@31b72cd4665f69678fc835da2f501771e42f097a:"
        )
        for row in rows
    )

    by_type = {}
    for row in rows:
        by_type.setdefault(row["record_type"], []).append(row)

    assert len(by_type["PCGN_DEPENDENT_NORMAL"]) == 17
    assert all(row["comparison"] == "MATCH" for row in by_type["PCGN_DEPENDENT_NORMAL"])
    assert len(by_type["PCGN_INDEPENDENT"]) == 12
    independent = {row["pcgn_table_row"]: row for row in by_type["PCGN_INDEPENDENT"]}
    assert independent["7"]["pcgn_a_series_or_value"] == "ŏ|ŭ"
    assert independent["7"]["candidate_a_series_or_value"] == "ŏ"
    assert independent["7"]["comparison"] == "ALTERNATIVE_COLLAPSED"
    assert sum(row["comparison"] == "MATCH" for row in by_type["PCGN_INDEPENDENT"]) == 11

    assert len(by_type["PCGN_SHORTENED"]) == 3
    assert by_type["PCGN_SHORTENED"][0]["comparison"] == "MATCH"
    assert all(
        row["comparison"] == "MATCH_WITH_EXTRA_KH_CODA"
        for row in by_type["PCGN_SHORTENED"][1:]
    )

    assert len(by_type["PCGN_ANUSVARA_VISARGA"]) == 8
    assert all(row["comparison"] == "MATCH" for row in by_type["PCGN_ANUSVARA_VISARGA"])
    candidate_only = [row for row in rows if row["comparison"] == "CANDIDATE_ONLY"]
    assert len(candidate_only) == 8
    assert {row["record_type"] for row in candidate_only} == {
        "UNGEGN_ONLY_INDEPENDENT",
        "UNGEGN_ONLY_NUCLEUS",
        "UNGEGN_ONLY_FALLBACK",
        "UNGEGN_ONLY_CODA_EXTENSION",
    }

    # The comparison is descriptive only: it must never turn the UNGEGN
    # candidate into the selected PCGN runtime profile or a pronunciation oracle.
    assert all(row["candidate_source_locator"].endswith("rules.py") for row in rows)
