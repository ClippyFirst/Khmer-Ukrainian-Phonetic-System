"""Evidence container for Khmer word-boundary candidates.

This module deliberately does not segment Khmer or choose an ALA-LC profile.
Offsets are Unicode code-point offsets into the exact source_text supplied by
the caller. Cluster spans are caller-supplied protected intervals.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

EvidenceStatus = Literal["OBSERVED", "PROPOSED", "ADJUDICATED", "REJECTED", "UNRESOLVED"]
CandidateStatus = Literal["PROPOSED", "ADJUDICATED", "REJECTED", "UNRESOLVED"]


@dataclass(frozen=True)
class BoundaryEvidence:
    offset: int
    status: EvidenceStatus
    evidence_type: str
    source_locator: str | None = None
    note: str = ""
    language_of_origin: str | None = None

    def __post_init__(self) -> None:
        if isinstance(self.offset, bool) or not isinstance(self.offset, int) or self.offset < 1:
            raise ValueError("Boundary evidence offset must be a positive Unicode code-point offset.")
        if self.status not in {"OBSERVED", "PROPOSED", "ADJUDICATED", "REJECTED", "UNRESOLVED"}:
            raise ValueError(f"Unsupported boundary evidence status: {self.status}")
        if not self.evidence_type.strip():
            raise ValueError("Boundary evidence requires a non-empty evidence_type.")
        if self.source_locator is not None and not self.source_locator.strip():
            raise ValueError("source_locator must be null or a non-empty locator.")


@dataclass(frozen=True)
class BoundaryCandidate:
    candidate_id: str
    boundaries: tuple[int, ...]
    status: CandidateStatus
    evidence: tuple[BoundaryEvidence, ...] = ()
    note: str = ""

    def __post_init__(self) -> None:
        if not self.candidate_id.strip():
            raise ValueError("Boundary candidate requires a non-empty candidate_id.")
        if self.status not in {"PROPOSED", "ADJUDICATED", "REJECTED", "UNRESOLVED"}:
            raise ValueError(f"Unsupported boundary candidate status: {self.status}")
        if tuple(sorted(set(self.boundaries))) != self.boundaries:
            raise ValueError("Candidate boundaries must be unique and strictly increasing.")
        evidence_offsets = {item.offset for item in self.evidence}
        if not evidence_offsets.issubset(set(self.boundaries)):
            raise ValueError("Boundary evidence must refer to an offset in its candidate.")
        if self.status == "ADJUDICATED":
            adjudicated_offsets = {item.offset for item in self.evidence if item.status == "ADJUDICATED"}
            if not set(self.boundaries).issubset(adjudicated_offsets):
                raise ValueError("Every adjudicated boundary requires adjudicated evidence.")
            for item in self.evidence:
                if item.offset in self.boundaries and item.status == "ADJUDICATED" and not item.source_locator:
                    raise ValueError("Adjudicated boundary evidence requires a source_locator.")


@dataclass(frozen=True)
class WordBoundaryAnalysis:
    source_text: str
    candidates: tuple[BoundaryCandidate, ...] = ()
    cluster_spans: tuple[tuple[int, int], ...] = ()
    profile_id: str | None = None
    profile_version: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.source_text, str):
            raise TypeError("source_text must be a string.")
        if (self.profile_id is None) != (self.profile_version is None):
            raise ValueError("profile_id and profile_version must either both be set or both be null.")
        if self.profile_id is not None and (not self.profile_id.strip() or not self.profile_version.strip()):
            raise ValueError("Selected profile ID and version must be non-empty.")
        previous_end = 0
        for span in self.cluster_spans:
            if len(span) != 2:
                raise ValueError("Each protected cluster span must be a (start, end) pair.")
            start, end = span
            if any(isinstance(value, bool) or not isinstance(value, int) for value in span):
                raise ValueError("Cluster span offsets must be integers.")
            if start < 0 or end <= start or end > len(self.source_text):
                raise ValueError("Protected cluster span is outside source_text or empty.")
            if start < previous_end:
                raise ValueError("Protected cluster spans must be ordered and non-overlapping.")
            previous_end = end
        ids = [candidate.candidate_id for candidate in self.candidates]
        if len(ids) != len(set(ids)):
            raise ValueError("Boundary candidate IDs must be unique.")
        for candidate in self.candidates:
            for offset in candidate.boundaries:
                if isinstance(offset, bool) or not isinstance(offset, int) or not 0 < offset < len(self.source_text):
                    raise ValueError("Candidate boundary is outside source_text.")
                if any(start < offset < end for start, end in self.cluster_spans):
                    raise ValueError(f"Candidate boundary at code-point offset {offset} splits a protected cluster.")
            for item in candidate.evidence:
                if item.offset not in candidate.boundaries:
                    raise ValueError("Evidence offset does not belong to its candidate.")
                if not 0 < item.offset < len(self.source_text):
                    raise ValueError("Evidence offset is outside source_text.")

    @property
    def status(self) -> str:
        viable = [candidate for candidate in self.candidates if candidate.status != "REJECTED"]
        if not viable:
            return "NO_CANDIDATES"
        if len(viable) > 1:
            return "AMBIGUOUS"
        if viable[0].status == "ADJUDICATED":
            return "ADJUDICATED"
        if viable[0].status == "UNRESOLVED":
            return "UNRESOLVED"
        return "PROVISIONAL"

    @property
    def selected_boundaries(self) -> tuple[int, ...] | None:
        viable = [candidate for candidate in self.candidates if candidate.status != "REJECTED"]
        if len(viable) == 1 and viable[0].status == "ADJUDICATED":
            return viable[0].boundaries
        return None

    def to_dict(self) -> dict:
        return {
            "schema": "khmer-word-boundary-evidence/v1",
            "offset_unit": "unicode_codepoint",
            "source_text": self.source_text,
            "profile": {"id": self.profile_id, "version": self.profile_version},
            "cluster_spans": [{"start": start, "end": end} for start, end in self.cluster_spans],
            "status": self.status,
            "selected_boundaries": list(self.selected_boundaries) if self.selected_boundaries is not None else None,
            "candidates": [
                {
                    "candidate_id": candidate.candidate_id,
                    "boundaries": list(candidate.boundaries),
                    "status": candidate.status,
                    "note": candidate.note,
                    "evidence": [
                        {
                            "offset": item.offset,
                            "status": item.status,
                            "evidence_type": item.evidence_type,
                            "source_locator": item.source_locator,
                            "note": item.note,
                            "language_of_origin": item.language_of_origin,
                        }
                        for item in candidate.evidence
                    ],
                }
                for candidate in self.candidates
            ],
        }
