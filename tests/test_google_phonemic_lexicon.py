import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from khmer_ua.google_phonemic import load_google_phonemic_lexicon


def test_google_phonemic_lexicon_manifest_matches_pinned_source_counts():
    lexicon = load_google_phonemic_lexicon()

    assert lexicon.manifest["source_rows"] == 62179
    assert lexicon.manifest["nonempty_pronunciation_rows"] == 62118
    assert lexicon.manifest["empty_pronunciation_rows"] == 61
    assert lexicon.manifest["unique_spellings_with_pronunciation"] == 62114
    assert lexicon.manifest["multi_pronunciation_words"] == 4
    assert lexicon.manifest["observed_phone_tokens"] == 54
    assert lexicon.manifest["mapped_phone_tokens"] == 54
    assert lexicon.manifest["ipa_gold_count"] == 0
    assert lexicon.manifest["candidate_status"] == "PROVISIONAL"


def test_google_phonemic_lookup_returns_a_typed_ipa_candidate():
    lexicon = load_google_phonemic_lexicon()

    candidates = lexicon.lookup("ក")
    assert len(candidates) == 1
    assert candidates[0].parsed.ipa == "kɑː"
    assert candidates[0].parsed.ipa_kind == "PHONEMIC"
    assert candidates[0].parsed.status == "PROVISIONAL"
    assert candidates[0].parsed.candidate.profile == "khmer-pph-careful-citation-v1"
    assert candidates[0].source_row > 0


def test_google_phonemic_lookup_preserves_all_pronunciation_variants():
    lexicon = load_google_phonemic_lexicon()

    candidates = lexicon.lookup("ការី")
    assert len(candidates) == 2
    assert {candidate.source_phonemic for candidate in candidates} == {
        "k aa . r ii",
        "k aa . r ə j",
    }
    assert all(candidate.parsed.status == "PROVISIONAL" for candidate in candidates)


def test_google_phonemic_lookup_does_not_promote_profile_conflicts():
    lexicon = load_google_phonemic_lexicon()

    candidates = lexicon.lookup("ខ្មែរ")
    assert len(candidates) == 1
    assert candidates[0].parsed.ipa == "kmae"
    assert candidates[0].parsed.status == "PROVISIONAL"
    assert "TARGET_PROFILE_EQUIVALENCE_UNVERIFIED" in candidates[0].parsed.uncertainty


def test_blank_google_pronunciation_rows_remain_unresolved():
    lexicon = load_google_phonemic_lexicon()

    assert len(lexicon.unresolved_rows) == 61
    blank_word = lexicon.unresolved_rows[0].word
    assert lexicon.lookup(blank_word) == ()


def test_google_phonemic_source_hash_is_verified(tmp_path: Path):
    source = Path(__file__).resolve().parents[1] / "data" / "khmer" / "google-pronunciation-full.tsv"
    altered = tmp_path / "altered.tsv"
    altered.write_bytes(source.read_bytes() + b"\n# altered\n")

    with pytest.raises(ValueError, match="source TSV hash mismatch"):
        load_google_phonemic_lexicon(altered, verify_hash=True)

def test_google_phonemic_manifest_and_all_shards_validate_against_schema():
    root = Path(__file__).resolve().parents[1]
    data_dir = root / "data" / "khmer"
    schema = json.loads(
        (root / "schemas" / "google-phonemic-source-lexicon.schema.json").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema)

    manifest = json.loads(
        (data_dir / "google-phonemic-source-lexicon.json").read_text(encoding="utf-8")
    )
    errors = list(validator.iter_errors(manifest))
    assert not errors, [error.message for error in errors]

    shards = sorted(data_dir.glob("google-phonemic-source-lexicon-[0-7].json"))
    assert len(shards) == 8
    for shard_path in shards:
        shard = json.loads(shard_path.read_text(encoding="utf-8"))
        errors = list(validator.iter_errors(shard))
        assert not errors, f"{shard_path.name}: {[error.message for error in errors]}"
        shard_id = int(shard_path.stem.rsplit("-", 1)[1])
        assert shard["shard_id"] == shard_id
        assert shard["source_revision"] == manifest["source"]["revision"]

