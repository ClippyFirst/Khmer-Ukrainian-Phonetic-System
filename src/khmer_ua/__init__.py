MODEL_VERSION = "0.2.0"
SCHEMA_VERSION = "0.1.0"
DATA_VERSION = "2026-10-05-research-finalization"

from .parser import analyze, normalize_khmer
from .pcgn import (
    PCGNOrthographicAnalysis,
    PCGNSeriesDecision,
    PCGNVowelDecision,
    PCGNIndependentVowelDecision,
    PCGNShortenedVowelDecision,
    PCGN_NO_SUBSCRIPT_FOR,
    PCGNToken,
    PCGN_WEAK_SUBSCRIPTS,
    analyze_pcgn_orthographic_chunk,
    resolve_pcgn_series,
    resolve_pcgn_dependent_vowel,
    resolve_pcgn_independent_vowel,
    resolve_pcgn_shortened_vowel,
)
from .ipa import (
    IPACandidate,
    IPACandidateStatus,
    render_ipa_profile,
    validate_ipa_candidate,
)
from .practical import map_segment, map_sequence, map_ipa_string, explain_segment
from .rule_engine import RuleBasedKhmerEngine
from .hybrid import HybridKhmerEngine, create_hybrid_engine, make_mekongphon_backend, make_command_backend

__all__ = [
    "analyze",
    "PCGNOrthographicAnalysis",
    "PCGNToken",
    "PCGNSeriesDecision",
    "PCGNVowelDecision",
    "PCGNIndependentVowelDecision",
    "PCGNShortenedVowelDecision",
    "PCGN_NO_SUBSCRIPT_FOR",
    "PCGN_WEAK_SUBSCRIPTS",
    "resolve_pcgn_series",
    "resolve_pcgn_dependent_vowel",
    "resolve_pcgn_independent_vowel",
    "resolve_pcgn_shortened_vowel",
    "analyze_pcgn_orthographic_chunk",
    "normalize_khmer",
    "IPACandidate",
    "IPACandidateStatus",
    "render_ipa_profile",
    "validate_ipa_candidate",
    "map_segment",
    "map_sequence",
    "map_ipa_string",
    "explain_segment",
    "RuleBasedKhmerEngine",
    "HybridKhmerEngine",
    "create_hybrid_engine",
    "make_mekongphon_backend",
    "make_command_backend",
]
