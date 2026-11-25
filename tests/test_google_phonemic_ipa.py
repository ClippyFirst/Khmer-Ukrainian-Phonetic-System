import json
import re
from pathlib import Path

import pytest

from khmer_ua.google_phonemic import (
    load_google_phone_map,
    parse_google_phonemic,
)

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "khmer"


def _source_rows():
    rows = {}
    for line in (DATA / "google-pronunciation-full.tsv").read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) < 2:
            continue
        word, phonemic = fields[0], fields[1]
        if any("\u1780" <= char <= "\u17ff" for char in word) and phonemic.strip():
            rows.setdefault(word, []).append(phonemic.strip())
    return rows


def _ipa_key(value):
    value = (value or "").strip().replace("ˈ", "").replace("ˌ", "")
    value = re.sub(r"^/|/$", "", value)
    return re.sub(r"[.\s]", "", value)


def test_google_phonemic_tokens_are_covered_by_pinned_inventory_and_map():
    mapping = load_google_phone_map()
    inventory = json.loads((DATA / "google-phonology.json").read_text(encoding="utf-8"))
    inventory_tokens = {row[0] for row in inventory["phones"]}
    observed = set()
    for pronunciations in _source_rows().values():
        for pronunciation in pronunciations:
            observed.update(token for token in pronunciation.split() if token != ".")

    assert len(observed) == 54
    assert observed <= inventory_tokens
    assert observed == set(mapping["tokens"]) - {"sil", "pau"}
    assert set(mapping["tokens"]) == inventory_tokens


def test_google_phonemic_to_ipa_preserves_syllable_boundaries_and_length():
    result = parse_google_phonemic("k ɑɑ . k ɔɔ")

    assert result.ipa == "kɑː.kɔː"
    assert result.ipa_kind == "PHONEMIC"
    assert result.status == "PROVISIONAL"
    assert result.mapping_status == "SOURCE_CORROBORATED"
    assert result.candidate.ipa_kind == "PHONEMIC"
    assert result.candidate.phonemic_ipa == result.ipa


def test_google_phonemic_to_ipa_maps_source_corroborated_diphthong_and_aspiration():
    result = parse_google_phonemic("ph ie . s aa")

    assert result.ipa == "pʰiə.saː"
    assert result.mapping_status == "SOURCE_CORROBORATED"
    assert result.ipa_kind == "PHONEMIC"


def test_provisional_phone_mapping_is_explicit_in_uncertainty():
    result = parse_google_phonemic("th ea")

    assert result.ipa == "tʰea"
    assert result.status == "PROVISIONAL"
    assert result.mapping_status == "PROVISIONAL"
    assert "UNVERIFIED_PHONE_MAPPING:th" in result.uncertainty
    assert "UNVERIFIED_PHONE_MAPPING:ea" in result.uncertainty


@pytest.mark.parametrize("raw", ["", "   ", ". k", "k .", "k . . ɑɑ", "k sil"])
def test_empty_malformed_or_nonlexical_phone_sequences_fail_closed(raw):
    result = parse_google_phonemic(raw)

    assert result.status == "UNRESOLVED"
    assert result.ipa is None
    assert result.candidate is None


def test_unknown_phone_token_is_not_guessed():
    result = parse_google_phonemic("k xyz")

    assert result.status == "UNRESOLVED"
    assert result.ipa is None
    assert "UNMAPPED_GOOGLE_PHONE:xyz" in result.uncertainty


def test_google_phonemic_adapter_matches_all_six_r12a_vowel_context_examples():
    pronunciations = _source_rows()
    matrix = json.loads((DATA / "vowel-context-register.json").read_text(encoding="utf-8"))
    cases = [
        case for case in matrix["cases"]
        if case.get("id", "").startswith("KHV-00")
        and case.get("ipa")
        and case.get("evidence_level") == "SOURCE_ATTESTED_NOT_GOLD"
    ]

    comparisons = []
    for case in cases:
        candidates = pronunciations.get(case["orthography"], [])
        assert len(candidates) == 1, case["id"]
        result = parse_google_phonemic(candidates[0])
        comparisons.append((case["id"], _ipa_key(result.ipa), _ipa_key(case["ipa"])))

    assert len(comparisons) == 6
    assert all(actual == expected for _, actual, expected in comparisons)


def test_google_lexical_conflicts_are_not_misrepresented_as_ipa_accuracy():
    pronunciations = _source_rows()
    lexical = json.loads((ROOT / "data" / "tests" / "verified-lexical-corpus.json").read_text(encoding="utf-8"))
    exact = []
    conflicts = []
    missing = []
    for word, record in lexical.items():
        reference = record.get("ipa") or record.get("source_reported_ipa")
        if not isinstance(reference, str) or not record.get("ipa_status", "").startswith("SOURCE_ATTESTED"):
            continue
        candidates = pronunciations.get(word, [])
        if not candidates:
            missing.append(word)
            continue
        results = [parse_google_phonemic(candidate) for candidate in candidates]
        if any(_ipa_key(result.ipa) == _ipa_key(reference) for result in results):
            exact.append(word)
        else:
            conflicts.append(word)

    assert len(exact) == 3
    assert len(conflicts) == 4
    assert len(missing) == 5
