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
    assert all(None not in row for row in rows)
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
    assert sum(row["comparison"] == "MATCH" for row in by_type["PCGN_ANUSVARA_VISARGA"]) == 7
    anusvara_row_7 = next(
        row for row in by_type["PCGN_ANUSVARA_VISARGA"] if row["pcgn_table_row"] == "7"
    )
    assert anusvara_row_7["pcgn_source_pattern"] == "េ+ា+ះ"
    assert anusvara_row_7["candidate_key"] == "ោះ"
    assert anusvara_row_7["comparison"] == "VALUE_MATCH_KEY_SHAPE_DIFFERS"
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



def test_candidate_comparison_pcgn_cells_match_the_project_owned_source_registries():
    root = Path(__file__).resolve().parents[1]

    def read_csv(relative_path):
        with (root / relative_path).open(encoding="utf-8", newline="") as stream:
            return list(csv.DictReader(stream))

    comparison = read_csv("data/khmer/pcgn_ungegn_vowel_profile_comparison.csv")
    by_section = {}
    for row in comparison:
        by_section.setdefault(row["record_type"], {})[row["pcgn_table_row"]] = row

    dependent = {
        row["table_row"]: row
        for row in read_csv("data/khmer/romanization_pcgn_dependent_vowels.csv")
    }
    assert set(by_section["PCGN_DEPENDENT_NORMAL"]) == {str(i) for i in range(1, 18)}
    assert set(dependent) == {str(i) for i in range(2, 18)}
    for table_row, source in dependent.items():
        compared = by_section["PCGN_DEPENDENT_NORMAL"][table_row]
        assert compared["pcgn_source_pattern"] == source["source_signs"]
        assert compared["pcgn_a_series_or_value"] == source["â_series"]
        assert compared["pcgn_o_series"] == source["ô_series"]

    inherent = read_csv("data/khmer/romanization_pcgn_inherent_vowel.csv")
    inherent_comparison = by_section["PCGN_DEPENDENT_NORMAL"]["1"]
    assert len(inherent) == 1
    assert inherent_comparison["pcgn_source_pattern"] == inherent[0]["source_symbol"]
    assert inherent_comparison["pcgn_a_series_or_value"] == inherent[0]["â_series"]
    assert inherent_comparison["pcgn_o_series"] == inherent[0]["ô_series"]

    independent = {
        row["table_row"]: row
        for row in read_csv("data/khmer/romanization_pcgn_independent_vowels.csv")
    }
    assert set(by_section["PCGN_INDEPENDENT"]) == set(independent)
    for table_row, source in independent.items():
        compared = by_section["PCGN_INDEPENDENT"][table_row]
        source_value = source["romanization"] or source["romanization_options"]
        assert compared["pcgn_source_pattern"] == source["source_characters"]
        assert compared["pcgn_a_series_or_value"] == source_value

    anusvara_visarga = {
        row["table_row"]: row
        for row in read_csv("data/khmer/romanization_pcgn_anusvara_visarga.csv")
    }
    assert set(by_section["PCGN_ANUSVARA_VISARGA"]) == set(anusvara_visarga)
    for table_row, source in anusvara_visarga.items():
        compared = by_section["PCGN_ANUSVARA_VISARGA"][table_row]
        if table_row in {"1", "5", "6", "7"}:
            # These rows preserve the same explicit component boundaries in
            # both registries; require exact sequence equality.
            assert compared["pcgn_source_pattern"] == source["source_components"]
        else:
            # Rows 2, 3, 4 and 8 use a combined glyph/component in the
            # comparison matrix; preserve ordered concatenation.
            assert compared["pcgn_source_pattern"].replace("+", "") == source["source_components"].replace("+", "")
        if table_row == "7":
            assert source["source_components"] == "េ+ា+ះ"
        assert compared["pcgn_a_series_or_value"] == source["â_series"]
        assert compared["pcgn_o_series"] == source["ô_series"]
