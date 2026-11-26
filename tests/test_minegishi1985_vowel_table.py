import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "data" / "khmer" / "source-extracts" / "minegishi-1985-vowel-sign-values.json"


def test_minegishi_vowel_table_preserves_all_source_rows_without_fabricating_unicode_or_ipa():
    payload = json.loads(TABLE.read_text(encoding="utf-8"))
    assert payload["source_id"] == "minegishi1985-modern-khmer-orthography-dialects"
    assert len(payload["rows"]) == 28
    assert len({row["id"] for row in payload["rows"]}) == 28
    assert all(row["evidence_status"] == "SOURCE_ATTESTED_NOT_GOLD" for row in payload["rows"])
    assert all(row["unicode_mapping_status"] == "NOT_CROSSWALKED" for row in payload["rows"])
    assert all(row["ipa_normalization_status"] == "SOURCE_PHONETIC_NOTATION_NOT_NORMALIZED_IPA" for row in payload["rows"])
    assert any(row["label_status"] == "unclear_diacritic" for row in payload["rows"])
    assert any(row["label_status"] == "unclear_final_mark" for row in payload["rows"])
    assert any("([i·ə])" in row["second_series_value"] for row in payload["rows"])
    assert any(row["first_series_value"] == "not used" for row in payload["rows"])
    assert any(row["second_series_value"] == "not used" for row in payload["rows"])
