import pytest

from khmer_ua.word_boundaries import (
    BoundaryCandidate,
    BoundaryEvidence,
    WordBoundaryAnalysis,
)


def test_boundary_evidence_is_profile_neutral_and_withholds_selection():
    result = WordBoundaryAnalysis(
        source_text="កម្ពុជា",
        candidates=(
            BoundaryCandidate("dictionary-a", (2,), "PROPOSED"),
            BoundaryCandidate("annotator-b", (3,), "UNRESOLVED"),
        ),
        cluster_spans=((0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6)),
    )

    payload = result.to_dict()
    assert result.status == "AMBIGUOUS"
    assert result.selected_boundaries is None
    assert payload["offset_unit"] == "unicode_codepoint"
    assert payload["profile"] == {"id": None, "version": None}
    assert payload["selected_boundaries"] is None


def test_adjudicated_boundary_requires_per_boundary_adjudicated_evidence():
    evidence = BoundaryEvidence(
        offset=2,
        status="ADJUDICATED",
        evidence_type="independent_lexical_annotation",
        source_locator="pilot:item-014",
        note="Two independent annotations reconciled by adjudicator.",
    )
    result = WordBoundaryAnalysis(
        source_text="កម្ពុជា",
        candidates=(
            BoundaryCandidate("adjudicated-1", (2,), "ADJUDICATED", (evidence,)),
        ),
        profile_id="ala-lc-khmer",
        profile_version="2013",
    )

    assert result.status == "ADJUDICATED"
    assert result.selected_boundaries == (2,)
    assert result.to_dict()["selected_boundaries"] == [2]


def test_adjudicated_boundary_cannot_be_claimed_without_adjudicated_evidence():
    with pytest.raises(ValueError, match="adjudicated evidence"):
        BoundaryCandidate("bad", (2,), "ADJUDICATED", ())


def test_boundary_cannot_split_a_caller_protected_khmer_cluster():
    # Cluster spans are code-point intervals supplied by a trusted upstream
    # grapheme parser; the evidence model does not guess cluster boundaries.
    with pytest.raises(ValueError, match="splits a protected cluster"):
        WordBoundaryAnalysis(
            source_text="ក្ម",
            candidates=(BoundaryCandidate("bad", (1,), "PROPOSED"),),
            cluster_spans=((0, 2), (2, 3)),
        )


def test_offsets_are_unicode_code_points_not_utf16_code_units():
    source = "ក🧪ខ"
    result = WordBoundaryAnalysis(
        source_text=source,
        candidates=(BoundaryCandidate("after-emoji", (2,), "PROPOSED"),),
        cluster_spans=((0, 1), (1, 2), (2, 3)),
    )
    assert result.candidates[0].boundaries == (2,)
    assert result.to_dict()["source_text"] == source


def test_rejected_candidate_does_not_override_one_adjudicated_candidate():
    accepted = BoundaryCandidate(
        "accepted",
        (2,),
        "ADJUDICATED",
        (BoundaryEvidence(2, "ADJUDICATED", "adjudication", "pilot:item-1"),),
    )
    rejected = BoundaryCandidate("rejected", (3,), "REJECTED")
    result = WordBoundaryAnalysis("កម្ពុជា", (accepted, rejected))
    assert result.status == "ADJUDICATED"
    assert result.selected_boundaries == (2,)


def test_profile_id_and_version_must_be_selected_together():
    with pytest.raises(ValueError, match="both be set"):
        WordBoundaryAnalysis("កម្ពុជា", profile_id="ala-lc-khmer")
