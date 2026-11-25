"""Evidence-bounded romanization → provisional IPA onset adapter."""
from __future__ import annotations

import json
from pathlib import Path

from .ipa_result import from_provisional_ipa, from_unknown_source_unit
from .ipa_target import adapt_phonetic_result

_ROOT = Path(__file__).resolve().parents[2]
with (_ROOT / "data" / "khmer" / "romanization_ipa_onsets.json").open(encoding="utf-8") as _handle:
    _INVENTORY = json.load(_handle)
_ENTRIES = _INVENTORY["entries"]
_TOKENS = sorted({entry["romanization"] for entry in _ENTRIES}, key=len, reverse=True)


def _unresolved(source: str, reason: str, provenance: tuple[str, ...]) -> dict:
    trace = tuple(dict.fromkeys(("ROMANIZATION-MEDIATED-IPA-V1", *provenance)))
    typed = from_unknown_source_unit(
        source or "?",
        provenance=trace,
        uncertainty=(reason, "ROMANIZATION-DID-NOT-ESTABLISH-IPA"),
    )
    return {
        "status": "UNRESOLVED",
        "typed_ipa": typed,
        "ukrainian": adapt_phonetic_result(typed) or "???",
        "romanized_onset": None,
        "provenance": trace,
        "uncertainty": (reason, "ROMANIZATION-DID-NOT-ESTABLISH-IPA"),
    }


def build_romanization_ipa_candidate(source_unit: str, romanized_unit: str) -> dict:
    """Cross-check a PCGN onset token against source orthography; never infer a rime."""
    source = str(source_unit or "")
    romanized = str(romanized_unit or "").lower()
    provenance = (
        "ROMANIZATION-MEDIATED-IPA-V1",
        "data/khmer/romanization_ipa_onsets.json",
        "PCGN-1972-CONSONANT-TABLE",
        "data/khmer/consonants.json",
    )
    if not source or not romanized:
        return _unresolved(source, "EMPTY-SOURCE-OR-ROMANIZATION", provenance)
    if source[0] == "ប" and romanized[:1] in {"b", "p"}:
        return _unresolved(source, "AMBIGUOUS-PCGN-B-P-ALTERNATION", provenance)

    token = next((candidate for candidate in _TOKENS if romanized.startswith(candidate)), None)
    if token is None:
        return _unresolved(source, "NO-RECOGNIZED-PCGN-ONSET-TOKEN", provenance)

    entry = next(
        (
            candidate for candidate in _ENTRIES
            if candidate["romanization"] == token and source[0] in candidate["source_units"]
        ),
        None,
    )
    if entry is None:
        reason = (
            "AMBIGUOUS-PCGN-B-P-ALTERNATION"
            if source[0] == "ប"
            else "ROMANIZATION-SOURCE-ONSET-MISMATCH"
        )
        return _unresolved(source, reason, provenance)

    uncertainty = (
        "ROMANIZATION-MEDIATED-ONSET-ONLY",
        "VOWEL_CODA_AND_SYLLABLE_NOT_ESTABLISHED",
        "UPSTREAM-ROMANIZER-MAY-HAVE-DROPPED-DIACRITICS",
    )
    typed = from_provisional_ipa(
        entry["ipa"],
        unresolved_graphemes=tuple(source[1:]),
        provenance=(*provenance, entry["rule_id"]),
        uncertainty=uncertainty,
        append_unknown_tail=True,
    )
    return {
        "status": "PROVISIONAL",
        "typed_ipa": typed,
        "ukrainian": adapt_phonetic_result(typed) or "???",
        "romanized_onset": token,
        "provenance": (*provenance, entry["rule_id"]),
        "uncertainty": uncertainty,
    }
