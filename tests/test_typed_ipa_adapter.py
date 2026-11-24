from dataclasses import FrozenInstanceError

import pytest

from khmer_ua.ipa_result import (
    TypedPhoneticResult,
    from_ipa,
    from_provisional_ipa,
    from_unknown_source_unit,
)
from khmer_ua.ipa_target import adapt_phonetic_result
from khmer_ua.rule_engine import RuleBasedKhmerEngine


def test_full_ipa_is_segmented_and_adapted_through_typed_boundary():
    result = from_ipa(
        "kʰmae",
        status="UNCERTAIN",
        provenance=("wiktionary:khmae",),
        uncertainty=("profile not independently adjudicated",),
    )

    assert isinstance(result, TypedPhoneticResult)
    assert result.status == "UNCERTAIN"
    assert result.phonemic_ipa == "kʰmae"
    assert [segment.ipa for segment in result.segments] == ["kʰ", "m", "a", "e"]
    assert all(segment.certainty == "UNCERTAIN" for segment in result.segments)
    assert adapt_phonetic_result(result, allow_uncertain=True) == "к'мае"
    assert result.status == "UNCERTAIN"


def test_provisional_ipa_keeps_known_onset_and_one_unknown_region():
    result = from_provisional_ipa(
        "k",
        unresolved_graphemes=("្", "ក"),
        provenance=("KHMER-PREVIEW-ONSET-IPA-V1",),
        uncertainty=("VOWEL_CODA_AND_SYLLABLE_NOT_ESTABLISHED",),
    )

    assert result.status == "PROVISIONAL"
    assert result.phonemic_ipa is None
    assert [segment.ipa for segment in result.segments] == ["k", "?"]
    assert [segment.certainty for segment in result.segments] == ["PROVISIONAL", "PROVISIONAL"]
    assert adapt_phonetic_result(result) == "к???"


def test_unknown_source_unit_is_explicit_and_renders_three_question_marks():
    result = from_unknown_source_unit(
        "☃",
        provenance=("KHMER_UNICODE_VALIDATION_FAILED",),
    )

    assert result.status == "UNRESOLVED"
    assert result.phonemic_ipa is None
    assert len(result.segments) == 1
    assert result.segments[0].kind == "unknown"
    assert adapt_phonetic_result(result) == "???"


def test_adapter_rejects_untyped_strings():
    with pytest.raises(TypeError, match="TypedPhoneticResult"):
        adapt_phonetic_result("kʰmae")


def test_typed_result_never_infers_tone_or_promotes_provisional_segments():
    result = from_provisional_ipa(
        "s",
        unresolved_graphemes=("៊", "៉"),
        provenance=("KHMER-PREVIEW-ONSET-IPA-V1",),
    )

    assert result.tone_category is None
    assert result.tone_contour_ipa is None
    assert all(segment.certainty == "PROVISIONAL" for segment in result.segments)
    with pytest.raises((FrozenInstanceError, AttributeError)):
        result.status = "SUPPORTED"


def test_engine_exposes_typed_ipa_result_for_canonical_and_provisional_units():
    engine = RuleBasedKhmerEngine()
    canonical = engine.analyze("ខ្មែរ")["phonetic_result"]["units"][0]
    provisional = engine.analyze("ក្ក")["phonetic_result"]["units"][0]

    assert canonical["typed_ipa"]["status"] == "UNCERTAIN"
    assert canonical["typed_ipa"]["phonemic_ipa"] == "kʰmae"
    assert canonical["ukrainian_kind"] == "IPA_DERIVED"
    assert provisional["typed_ipa"]["status"] == "PROVISIONAL"
    assert provisional["typed_ipa"]["phonemic_ipa"] is None
    assert provisional["ukrainian"] == "к???"
    assert provisional["ukrainian_kind"] == "IPA_DERIVED_PROVISIONAL"
