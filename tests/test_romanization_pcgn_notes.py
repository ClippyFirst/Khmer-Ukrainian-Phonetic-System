from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "khmer" / "romanization_pcgn_notes.csv"
SOURCE = "https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf"


def _rows():
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def test_all_eleven_pcgn_notes_are_registered_with_primary_source_locators():
    rows = _rows()
    assert len(rows) == 11
    assert [row["note_number"] for row in rows] == [str(i) for i in range(1, 12)]
    assert all(row["source_url"] == SOURCE for row in rows)
    assert all(row["source_locator"].strip() for row in rows)
    assert all(row["source_summary"].strip() for row in rows)
    assert all(row["conditions_or_exceptions"].strip() for row in rows)
    assert all(row["limitations"].strip() for row in rows)
    statuses = {row["note_number"]: row["implementation_status"] for row in rows}
    assert statuses["5"] == "PARTIAL_COMPONENT_RESOLVER"
    assert all(status == "DOCUMENTED_ONLY" for note, status in statuses.items() if note != "5")


def test_pcgn_note_three_keeps_the_pcgn_weak_subscript_set_exact():
    note = next(row for row in _rows() if row["note_number"] == "3")
    for character in "ងញណនមយរលវ":
        assert character in note["source_summary"]
    assert "ស" not in note["source_summary"]
    assert "do not extend" in note["limitations"].lower()
    assert "ambiguous" in note["limitations"].lower()


def test_pcgn_note_five_preserves_both_shortening_marks_and_the_exact_coda_set():
    note = next(row for row in _rows() if row["note_number"] == "5")
    assert "BANTOC" in note["source_summary"]
    assert "SAMYOK SANNYA" in note["source_summary"]
    assert "k/ng/h" in note["source_summary"]
    assert "oă otherwise" in note["source_summary"]
    assert "coda" in note["limitations"].lower()


def test_pcgn_notes_registry_is_not_misrepresented_as_ipa_or_ukrainian_gold():
    rows = _rows()
    headers = set(rows[0])
    assert not ({"ipa", "ipa_output", "ukrainian_candidate", "gold"} & headers)
    statuses = {row["note_number"]: row["implementation_status"] for row in rows}
    assert statuses["5"] == "PARTIAL_COMPONENT_RESOLVER"
    assert all(status == "DOCUMENTED_ONLY" for note, status in statuses.items() if note != "5")
