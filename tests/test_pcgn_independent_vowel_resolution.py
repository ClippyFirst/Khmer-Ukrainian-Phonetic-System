from __future__ import annotations

import csv
from pathlib import Path

from khmer_ua.pcgn import (
    PCGN_INDEPENDENT_VOWEL_ROWS,
    analyze_pcgn_orthographic_chunk,
    resolve_pcgn_independent_vowel,
)


def resolve(source: str):
    return resolve_pcgn_independent_vowel(analyze_pcgn_orthographic_chunk(source))


def test_pcgn_independent_vowel_table_rows_are_mapped_without_series():
    cases = (
        ("ឥ", "ĕ", 3),
        ("ឦ", "ei", 4),
        ("ឯ", "ê", 14),
        ("ឰ", "ai", 15),
        ("ឱ", "aô", 16),
        ("ឲ", "aô", 16),
        ("ឳ", "au", 17),
        ("ឪ", "âu", 18),
        ("ឫ", "rœ̆", 19),
        ("ឬ", "rœ", 20),
        ("ឭ", "lœ̆", 21),
        ("ឮ", "lœ", 22),
    )
    for source, expected, row in cases:
        result = resolve(source)
        assert result.status == "RESOLVED", source
        assert result.source_character == source
        assert result.romanization == expected
        assert result.romanization_options == ()
        assert result.source_table_row == row
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_note9_keeps_uu_alternative_unresolved_and_traceable():
    result = resolve("ឧ")
    assert result.status == "UNRESOLVED"
    assert result.source_character == "ឧ"
    assert result.source_table_row == 7
    assert result.romanization is None
    assert result.romanization_options == ("ŏ", "ŭ")
    assert "PCGN_NOTE_9_Ŏ_OR_Ŭ_REQUIRES_REFERENCE_SELECTION" in result.warnings


def test_pcgn_independent_vowel_resolver_abstains_on_unlisted_or_mixed_input():
    for source in ("ឨ", "ឥក", "ឥា", "ឥឥ", "ឥx", "ក"):
        result = resolve(source)
        assert result.status == "UNRESOLVED", source
        assert result.romanization is None, source
        assert result.romanization_options == (), source
        assert result.ipa is None
        assert result.ukrainian is None


def test_pcgn_independent_vowel_schema_has_component_only_boundary():
    import json
    from pathlib import Path

    path = Path(__file__).resolve().parents[1] / "schemas/pcgn-independent-vowel-decision.schema.json"
    schema = json.loads(path.read_text(encoding="utf-8"))
    assert set(schema["required"]) == {
        "source_character", "romanization", "romanization_options", "source_table_row",
        "status", "ipa", "ukrainian", "source_locator", "warnings",
    }
    assert schema["properties"]["ipa"]["const"] is None
    assert schema["properties"]["ukrainian"]["const"] is None
    assert schema["properties"]["romanization_options"]["items"]["enum"] == ["ŏ", "ŭ"]
    assert schema["allOf"][2]["then"]["properties"]["romanization_options"]["const"] == ["ŏ", "ŭ"]
    assert schema["properties"]["source_character"]["enum"] == [
        "ឥ", "ឦ", "ឧ", "ឯ", "ឰ", "ឱ", "ឲ", "ឳ", "ឪ", "ឫ", "ឬ", "ឭ", "ឮ", "ឨ", None
    ]



def test_pcgn_note9_alternatives_are_not_selected_without_a_reference():
    result = resolve("ឧ")
    assert result.status == "UNRESOLVED"
    assert result.romanization is None
    assert result.romanization_options == ("ŏ", "ŭ")
    assert "PCGN_NOTE_9_Ŏ_OR_Ŭ_REQUIRES_REFERENCE_SELECTION" in result.warnings


def test_pcgn_independent_vowel_source_registry_matches_runtime_rows_and_note9():
    root = Path(__file__).resolve().parents[1]
    with (root / "data/khmer/romanization_pcgn_independent_vowels.csv").open(
        encoding="utf-8", newline=""
    ) as stream:
        rows = list(csv.DictReader(stream))

    resolved = {}
    unresolved = []
    for row in rows:
        source_characters = row["source_characters"].split("|")
        assert row["source_locator"].startswith("PCGN 1972 Independent/Dependent Vowel Characters table")
        assert row["source_url"] == "https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf"
        assert row["acceptance_boundary"]
        if row["status"] == "RESOLVED":
            assert row["romanization"]
            assert row["romanization_options"] == ""
            for character in source_characters:
                resolved[character] = (int(row["table_row"]), row["romanization"])
        else:
            assert row["status"] == "UNRESOLVED"
            assert row["romanization"] == ""
            assert row["romanization_options"].split("|") == ["ŏ", "ŭ"]
            assert source_characters == ["ឧ"]
            unresolved.append(row)

    assert resolved == PCGN_INDEPENDENT_VOWEL_ROWS
    assert len(unresolved) == 1
    assert unresolved[0]["table_row"] == "7"
