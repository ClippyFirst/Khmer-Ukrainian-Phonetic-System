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
    assert statuses["2"] == "PARTIAL_COMPONENT_RESOLVER"
    assert statuses["3"] == "PARTIAL_COMPONENT_RESOLVER"
    assert statuses["4"] == "PARTIAL_COMPONENT_RESOLVER"
    assert statuses["5"] == "PARTIAL_COMPONENT_RESOLVER"
    assert statuses["6"] == "PARTIAL_COMPONENT_RESOLVER"
    assert statuses["7"] == "PARTIAL_COMPONENT_RESOLVER"
    assert statuses["8"] == "PARTIAL_COMPONENT_RESOLVER"
    assert statuses["9"] == "PARTIAL_AMBIGUITY_CONTRACT"
    assert statuses["10"] == "PARTIAL_CHARACTER_INVENTORY"
    assert all(status == "DOCUMENTED_ONLY" for note, status in statuses.items() if note not in {"2", "3", "4", "5", "6", "7", "8", "9", "10"})


def test_pcgn_note_three_keeps_the_pcgn_weak_subscript_set_exact():
    note = next(row for row in _rows() if row["note_number"] == "3")
    for character in "ងញណនមយរលវ":
        assert character in note["source_summary"]
    assert "ស" not in note["source_summary"]
    assert "do not extend" in note["limitations"].lower()
    assert "ambiguous" in note["limitations"].lower()


def test_pcgn_note_four_preserves_the_word_initial_optional_apostrophe_boundary():
    note = next(row for row in _rows() if row["note_number"] == "4")
    assert "apostrophe" in note["source_summary"].lower()
    assert "word-initial" in note["conditions_or_exceptions"].lower()
    assert "both are true" in note["conditions_or_exceptions"].lower()
    assert "not inferred" in note["limitations"].lower()


def test_pcgn_note_five_preserves_both_shortening_marks_and_the_exact_coda_set():
    note = next(row for row in _rows() if row["note_number"] == "5")
    assert "BANTOC" in note["source_summary"]
    assert "SAMYOK SANNYA" in note["source_summary"]
    assert "k/ng/h" in note["source_summary"]
    assert "oă otherwise" in note["source_summary"]
    assert "coda" in note["limitations"].lower()


def test_pcgn_note_six_preserves_explicit_robat_r_c_mapping_boundary():
    note = next(row for row in _rows() if row["note_number"] == "6")
    assert "rC" in note["source_summary"]
    assert "caller supplies" in note["conditions_or_exceptions"].lower()
    assert "not inferred" in note["limitations"].lower()


def test_pcgn_note_seven_preserves_explicit_position_and_series_boundary():
    note = next(row for row in _rows() if row["note_number"] == "7")
    assert "syllable-initial" in note["source_summary"]
    assert "syllable-final" in note["source_summary"]
    assert "explicit caller-supplied syllable position" in note["conditions_or_exceptions"].lower()
    assert "never inferred" in note["limitations"].lower()


def test_pcgn_note_eight_preserves_explicit_silent_character_boundary():
    note = next(row for row in _rows() if row["note_number"] == "8")
    assert "not pronounced" in note["source_summary"].lower()
    assert "caller must identify" in note["conditions_or_exceptions"].lower()
    assert "not inferred" in note["limitations"].lower()


def test_pcgn_notes_registry_is_not_misrepresented_as_ipa_or_ukrainian_gold():
    rows = _rows()
    headers = set(rows[0])
    assert not ({"ipa", "ipa_output", "ukrainian_candidate", "gold"} & headers)
    statuses = {row["note_number"]: row["implementation_status"] for row in rows}
    assert statuses["2"] == "PARTIAL_COMPONENT_RESOLVER"
    assert statuses["3"] == "PARTIAL_COMPONENT_RESOLVER"
    assert statuses["4"] == "PARTIAL_COMPONENT_RESOLVER"
    assert statuses["5"] == "PARTIAL_COMPONENT_RESOLVER"
    assert statuses["6"] == "PARTIAL_COMPONENT_RESOLVER"
    assert statuses["7"] == "PARTIAL_COMPONENT_RESOLVER"
    assert statuses["8"] == "PARTIAL_COMPONENT_RESOLVER"
    assert statuses["9"] == "PARTIAL_AMBIGUITY_CONTRACT"
    assert statuses["10"] == "PARTIAL_CHARACTER_INVENTORY"
    assert all(status == "DOCUMENTED_ONLY" for note, status in statuses.items() if note not in {"2", "3", "4", "5", "6", "7", "8", "9", "10"})



def test_pcgn_note_two_registry_preserves_ba_muusikatoan_exception_and_limits():
    note = next(row for row in _rows() if row["note_number"] == "2")
    assert "MUUSIKATOAN" in note["source_summary"]
    assert "TRIISAP" in note["source_summary"]
    assert "Note 3 specifies" in note["conditions_or_exceptions"]
    assert "BA+MUUSIKATOAN" in note["limitations"]
    assert "series metadata only" in note["limitations"]



def test_pcgn_note_ten_registry_marks_only_the_bounded_letter_inventory_as_partial():
    note = next(row for row in _rows() if row["note_number"] == "10")
    assert note["implementation_status"] == "PARTIAL_CHARACTER_INVENTORY"
    assert "precomposed and decomposed" in note["source_summary"]
    assert "two-code-point sequences" in note["conditions_or_exceptions"]
    assert "non-letter characters" in note["limitations"].lower()
    assert "no normalization" in note["limitations"].lower()



def test_pcgn_note_nine_registry_preserves_alternatives_without_selecting_one():
    note = next(row for row in _rows() if row["note_number"] == "9")
    assert note["implementation_status"] == "PARTIAL_AMBIGUITY_CONTRACT"
    assert "ŏ or ŭ" in note["source_summary"]
    assert "both alternatives" in note["conditions_or_exceptions"]
    assert "no alternative is selected" in note["limitations"].lower()


def test_pcgn_note_two_registry_maps_shifter_names_to_unicode_codepoints():
    import unicodedata

    note_two = next(row for row in _rows() if row["note_number"] == "2")
    note_three = next(row for row in _rows() if row["note_number"] == "3")

    assert "TRIISAP ◌៊ (U+17CA)" in note_two["source_summary"]
    assert "MUUSIKATOAN ◌៉ (U+17C9)" in note_two["source_summary"]
    assert unicodedata.name(chr(0x17ca)) == "KHMER SIGN TRIISAP"
    assert unicodedata.name(chr(0x17c9)) == "KHMER SIGN MUUSIKATOAN"
    assert "TRIISAP" in note_two["conditions_or_exceptions"]
    assert "MUUSIKATOAN" in note_three["source_summary"]
    assert "TRIISAP" not in note_three["source_summary"]


def test_pcgn_note_three_ba_exception_uses_muusikatoan_not_triisap():
    note = next(row for row in _rows() if row["note_number"] == "3")
    assert "MUUSIKATOAN (◌៉, U+17C9)" in note["source_summary"]
    assert "TRIISAP" not in note["source_summary"]
