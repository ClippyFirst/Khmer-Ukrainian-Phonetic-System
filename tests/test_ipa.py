import pytest

from khmer_ua.ipa import (
    IPACandidateStatus,
    render_ipa_profile,
    validate_ipa_candidate,
)


def test_selected_phnom_penh_careful_citation_profile_preserves_ipa():
    for ipa in ("krɑː", "pʰnum.krɑː", "ˈtrəː", "ar.krɑː"):
        assert render_ipa_profile(ipa) == ipa
        assert render_ipa_profile(ipa, "khmer-pph-careful-citation-v1") == ipa


@pytest.mark.parametrize("profile", [
    "careful_standard",
    "phnom_penh_colloquial",
    "established_form",
    "unknown",
])
def test_unselected_profiles_are_rejected(profile):
    with pytest.raises(ValueError, match="unsupported pronunciation profile"):
        render_ipa_profile("krɑː", profile)


def test_typed_candidate_preserves_raw_ipa_profile_kind_and_provider():
    raw = "ˈkʰmaeː˥.t͡ɕa"
    candidate = validate_ipa_candidate(
        raw,
        profile="khmer-pph-careful-citation-v1",
        kind="PHONETIC_BROAD",
        status="COMPLETE",
        provider="research-provider@1.2.3",
    )
    assert candidate.raw_output == raw
    assert candidate.ipa == raw
    assert candidate.profile == "khmer-pph-careful-citation-v1"
    assert candidate.kind == "PHONETIC_BROAD"
    assert candidate.status is IPACandidateStatus.COMPLETE
    assert candidate.provider == "research-provider@1.2.3"
    assert candidate.uncertainty == ()


def test_partial_candidate_must_retain_explicit_uncertainty():
    candidate = validate_ipa_candidate(
        "kʰmae",
        profile="khmer-pph-careful-citation-v1",
        kind="PHONETIC_BROAD",
        status="PARTIAL",
        provider="external-g2p",
        uncertainty=("coda not resolved", "tone not supplied"),
    )
    assert candidate.status is IPACandidateStatus.PARTIAL
    assert candidate.uncertainty == ("coda not resolved", "tone not supplied")


def test_partial_candidate_without_uncertainty_is_rejected():
    with pytest.raises(ValueError, match="must include at least one uncertainty"):
        validate_ipa_candidate(
            "kʰmae",
            profile="khmer-pph-careful-citation-v1",
            kind="PHONETIC_BROAD",
            status="PARTIAL",
            provider="external-g2p",
        )


@pytest.mark.parametrize("raw", ["", "   ", "???", "ក្មែរ", "kʰ🙂", "k\u0301"])
def test_invalid_or_unverifiable_candidate_notation_is_rejected(raw):
    with pytest.raises(ValueError):
        validate_ipa_candidate(
            raw,
            profile="khmer-pph-careful-citation-v1",
            kind="PHONETIC_BROAD",
            status="COMPLETE",
            provider="external-g2p",
        )


def test_unbalanced_delimiters_and_unsupported_metadata_are_rejected():
    args = {
        "profile": "khmer-pph-careful-citation-v1",
        "kind": "PHONETIC_BROAD",
        "status": "COMPLETE",
        "provider": "external-g2p",
    }
    for raw in ("/kʰmae", "kʰmae/", "[kʰmae", "kʰmae]", "kʰ/mae/"):
        with pytest.raises(ValueError, match="unbalanced"):
            validate_ipa_candidate(raw, **args)
    with pytest.raises(ValueError, match="at least one IPA segment"):
        validate_ipa_candidate("ˈː˥", **args)
    with pytest.raises(ValueError, match="unsupported IPA kind"):
        validate_ipa_candidate("kʰmae", **{**args, "kind": "PHONETIC_GUESS"})
    with pytest.raises(ValueError, match="unsupported pronunciation profile"):
        validate_ipa_candidate("kʰmae", **{**args, "profile": "phnom-penh-colloquial"})


def test_candidate_validator_preserves_tone_length_stress_and_syllable_boundaries():
    raw = "/ˈkʰmaeː˥.t͡ɕa/"
    candidate = validate_ipa_candidate(
        raw,
        profile="khmer-pph-careful-citation-v1",
        kind="PHONETIC_NARROW",
        status="COMPLETE",
        provider="external-g2p",
    )
    assert candidate.ipa == raw
    assert candidate.raw_output == raw



def test_tie_bars_require_two_adjacent_segment_letters():
    args = {
        "profile": "khmer-pph-careful-citation-v1",
        "kind": "PHONETIC_BROAD",
        "status": "COMPLETE",
        "provider": "external-g2p",
    }
    for raw in ("k͡", "/k͡/", "k͡ːa", "k͡͡a"):
        with pytest.raises(ValueError, match="tie bar"):
            validate_ipa_candidate(raw, **args)

    # A preceding segment diacritic remains attached to the first segment.
    raw = "t̪͡s"
    candidate = validate_ipa_candidate(raw, **args)
    assert candidate.ipa == raw

def test_combining_marks_cannot_float_across_a_space():
    with pytest.raises(ValueError, match="orphan combining mark"):
        validate_ipa_candidate(
            "k ̥",
            profile="khmer-pph-careful-citation-v1",
            kind="PHONETIC_BROAD",
            status="COMPLETE",
            provider="external-g2p",
        )
