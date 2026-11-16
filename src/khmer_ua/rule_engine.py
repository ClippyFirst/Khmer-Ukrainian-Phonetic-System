"""Deterministic Khmer → IPA → Ukrainian research engine.

The engine keeps structural parsing, pronunciation evidence, IPA and target
adaptation as separate lanes. It returns aligned per-unit results and never
lets one unsupported unit erase neighboring results.
"""
from __future__ import annotations

import json
import unicodedata
from pathlib import Path
from typing import Any

from .normalize import normalize_khmer
from .parser import analyze as analyze_structure, segment_syllables
from .phonetic_result import PhoneticResult, PhoneticUnitResult, PhoneticUncertainty
from .practical import map_ipa_string

ROOT = Path(__file__).resolve().parents[2]
_FIXTURE_PATH = ROOT / "data" / "tests" / "web-fixtures.json"
with _FIXTURE_PATH.open(encoding="utf-8") as _handle:
    _LEXICON: dict[str, dict[str, Any]] = json.load(_handle)

_PROFILE = "khmer-pph-careful-citation-v1"
_ENGINE = "khmer-deterministic-rules-v1"
_UNKNOWN_IPA = "⟦NOT_ESTABLISHED⟧"
_UNKNOWN_UKRAINIAN = "⟦НЕВСТАНОВЛЕНО⟧"


def _map_ipa(ipa: str) -> tuple[str | None, str | None]:
    """Backward-compatible wrapper around the sole practical IPA adapter."""
    return map_ipa_string(ipa)


def _is_separator(character: str | None) -> bool:
    return character is None or character.isspace() or unicodedata.category(character).startswith("P")


def _tokenize_input(text: str) -> list[str]:
    """Prefer exact lexical fixtures, then use the structural parser per chunk.

    This is a conservative adapter boundary, not a claim of full Khmer word
    segmentation. Spaces and punctuation are retained as independent units.
    """
    characters = list(text)
    fixture_keys = sorted(_LEXICON, key=len, reverse=True)
    units: list[str] = []
    chunk: list[str] = []

    def flush_chunk() -> None:
        if chunk:
            units.extend(segment_syllables("".join(chunk)))
            chunk.clear()

    index = 0
    while index < len(characters):
        character = characters[index]
        if _is_separator(character):
            flush_chunk()
            units.append(character)
            index += 1
            continue

        remainder = "".join(characters[index:])
        fixture = None if index > 0 and characters[index - 1] == "្" else next(
            (
                key for key in fixture_keys
                if remainder.startswith(key)
                and _is_separator(characters[index + len(key)] if index + len(key) < len(characters) else None)
            ),
            None,
        )
        if fixture is not None:
            flush_chunk()
            units.append(fixture)
            index += len(fixture)
            continue

        chunk.append(character)
        index += 1

    flush_chunk()
    return units


def _provisional_preview(structure: Any) -> dict[str, Any] | None:
    """Expose only registered onset IPA; never infer a vowel from an incomplete unit."""
    syllables = structure.phonological_representation.get("syllables", [])
    if not syllables:
        return None
    previews = []
    for unit in syllables:
        base = unit.get("base_consonant")
        onset = unit.get("phonology", {}).get("onset_ipa")
        if not base or not onset:
            previews.append({
                "source": unit.get("raw_text", ""),
                "ipa": None,
                "ukrainian": "?",
                "status": "UNKNOWN",
                "position": None,
                "rule_id": None,
                "unresolved_graphemes": list(unit.get("raw_text", "")),
            })
            continue
        mapped, unsupported = map_ipa_string(onset)
        rendered = mapped if unsupported is None and mapped is not None else ""
        unresolved = [
            ch for ch in unit.get("raw_text", "")
            if ch != base and ch not in {"\u200c"}
        ]
        previews.append({
            "source": unit.get("raw_text", ""),
            "ipa": onset,
            "ukrainian": rendered + ("?" if unresolved or not rendered else ""),
            "status": "PROVISIONAL" if rendered else "UNKNOWN",
            "position": "onset",
            "rule_id": "KHMER-PREVIEW-ONSET-IPA-V1",
            "unresolved_graphemes": unresolved or ([] if rendered else [base]),
            "warnings": ["CONSONANT_POSITION_OR_RIME_NOT_ESTABLISHED"],
            "evidence": ["unicode17-ch16", "r12a-orthography"],
        })
    if not previews:
        return None
    has_hint = any(item.get("ipa") for item in previews)
    return {
        "status": "PROVISIONAL" if has_hint else "UNKNOWN",
        "ipa_preview": " ".join(item["ipa"] or "?" for item in previews) if has_hint else None,
        "ukrainian_preview": " ".join(item["ukrainian"] for item in previews),
        "syllables": previews,
        "warnings": ["LOW_CONFIDENCE", "TONE_NOT_INFERRED"],
    }


def _analyze_unit(unit: str) -> dict[str, Any]:
    fixture = _LEXICON.get(unit)
    if fixture is not None:
        raw_ipa = fixture.get("ipa")
        if not raw_ipa:
            return {
                "source": unit, "ipa": None, "ukrainian": None,
                "status": fixture.get("status", "EVIDENCE_LIMITED"),
                "rule_trace": ["KHMER_LEXICAL_FIXTURE_WITHHELD"],
                "reason": fixture.get("note", "The lexical fixture has no established IPA value."),
                "evidence": fixture.get("evidence", []),
            }
        ipa = raw_ipa.strip().strip("/")
        ukrainian, unsupported = map_ipa_string(ipa)
        return {
            "source": unit, "ipa": ipa, "ukrainian": ukrainian,
            "status": fixture.get("status", "PROPOSED") if unsupported is None else "NOT_ESTABLISHED",
            "rule_trace": ["KHMER_LEXICAL_FIXTURE", "IPA_TO_UKRAINIAN_LONGEST_MATCH"],
            "reason": fixture.get("note", "") if unsupported is None else f"Unsupported IPA sequence: {unsupported}",
            "evidence": fixture.get("evidence", []),
            "lexical_ua_reference": fixture.get("ua"),
            "lexical_mapping_agrees": ukrainian == fixture.get("ua") if ukrainian is not None else False,
        }

    structure = analyze_structure(unit)
    if structure.status == "INVALID_OR_UNSUPPORTED":
        return {
            "source": unit, "ipa": None, "ukrainian": None,
            "status": "INVALID_OR_UNSUPPORTED",
            "rule_trace": ["KHMER_STRUCTURAL_VALIDATION_FAILED"],
            "reason": "Unsupported or malformed source code point/sequence; inspect the structural grapheme trace.",
            "provisional_ipa": None,
            "provisional_ukrainian": "?",
            "fallback_status": "UNKNOWN",
            "fallback_trace": [{
                "source": unit, "ipa": None, "ukrainian": "?", "status": "UNKNOWN",
                "position": None, "rule_id": None, "unresolved_graphemes": list(unit),
            }],
            "evidence": [],
            "structure": structure.phonological_representation,
        }

    if len(structure.syllables) == 1:
        syllable = structure.syllables[0]
        if (
            syllable.get("status") == "ESTABLISHED_STRUCTURE"
            and syllable.get("base_consonant")
            and not syllable.get("subscripts")
            and not syllable.get("vowel_signs")
            and not syllable.get("independent_vowel")
        ):
            onset = syllable.get("phonology", {}).get("onset_ipa")
            register = syllable.get("register")
            if onset and register in {"first", "second"}:
                vowel = "ɑː" if register == "first" else "ɔː"
                ipa = onset + vowel
                ukrainian, unsupported = map_ipa_string(ipa)
                return {
                    "source": unit,
                    "ipa": ipa if unsupported is None else None,
                    "ukrainian": ukrainian,
                    "status": "PROPOSED" if unsupported is None else "NOT_ESTABLISHED",
                    "rule_trace": ["KHMER_REGISTER_SERIES_INHERENT_VOWEL", "IPA_TO_UKRAINIAN_LONGEST_MATCH"],
                    "reason": "Conservative series-based inherent-vowel rule; status remains proposed pending profile-matched adjudication.",
                    "evidence": [],
                    "structure": structure.phonological_representation,
                }

    preview = _provisional_preview(structure)
    return {
        "source": unit, "ipa": None, "ukrainian": None, "status": "NOT_ESTABLISHED",
        "provisional_ipa": preview["ipa_preview"] if preview else None,
        "provisional_ukrainian": preview["ukrainian_preview"] if preview else None,
        "fallback_status": preview["status"] if preview else "UNKNOWN",
        "fallback_trace": preview["syllables"] if preview else [],
        "rule_trace": ["KHMER_UNSUPPORTED_PATTERN_WITHHELD", "PROVISIONAL_ONSET_IPA_PREVIEW"],
        "reason": "Canonical IPA remains withheld. A separate low-confidence onset-only preview is offered where a registered consonant IPA is available; no vowel, coda or tone is inferred.",
        "structure": structure.phonological_representation,
    }


def _combine_status(units: list[dict[str, Any]]) -> str:
    statuses = {unit["status"] for unit in units}
    invalid = sum(unit["status"] == "INVALID_OR_UNSUPPORTED" for unit in units)
    if invalid and invalid == len(units):
        return "INVALID_OR_UNSUPPORTED"
    if invalid or "EVIDENCE_LIMITED" in statuses:
        return "EVIDENCE_LIMITED"
    if "NOT_ESTABLISHED" in statuses:
        return "NOT_ESTABLISHED"
    if "PROVISIONAL" in statuses:
        return "PROVISIONAL"
    if "PROPOSED" in statuses:
        return "PROPOSED"
    return "ESTABLISHED_STRUCTURE"


class RuleBasedKhmerEngine:
    """Deterministic rule/lexicon engine for Phnom Penh careful citation Khmer."""

    profile = _PROFILE
    engine_id = _ENGINE

    def analyze(self, text: str) -> dict[str, Any]:
        normalized = normalize_khmer(text)
        if not normalized:
            return {
                "input": text, "normalized": normalized, "profile": self.profile,
                "engine": self.engine_id, "deterministic": True,
                "ipa": None, "ukrainian": None, "status": "NOT_ESTABLISHED",
                "rule_trace": [], "reason": "Empty input.",
                "phonetic_result": PhoneticResult((), False, False).to_dict(),
            }

        tokens = _tokenize_input(normalized)
        rendered: list[dict[str, Any]] = []
        for token in tokens:
            if len(token) == 1 and _is_separator(token):
                rendered.append({
                    "source": token, "ipa": token, "ukrainian": token,
                    "status": "PUNCTUATION", "rule_trace": [], "reason": "", "evidence": [],
                })
            else:
                rendered.append(_analyze_unit(token))

        linguistic = [unit for unit in rendered if unit["status"] != "PUNCTUATION"]
        resolved = [unit for unit in linguistic if unit["status"] == "PROPOSED"]
        complete = bool(linguistic) and all(
            unit["status"] == "PROPOSED"
            and unit.get("ipa") is not None
            and unit.get("ukrainian") is not None
            for unit in linguistic
        )
        partial = not complete and bool(resolved)

        typed_units = []
        for unit in rendered:
            status = unit["status"]
            source_ipa = unit.get("ipa")
            source_ua = unit.get("ukrainian")
            ipa_value = source_ipa if source_ipa is not None else f"⟦{status}⟧"
            ua_value = source_ua if source_ua is not None else ("⟦НЕПІДТРИМУЄТЬСЯ⟧" if status == "INVALID_OR_UNSUPPORTED" else _UNKNOWN_UKRAINIAN)
            structure = unit.get("structure", {})
            structural_sources = ["unicode17-ch16"] if structure else []
            phonology_sources = list(unit.get("evidence", []))
            target_sources = ["data/ukrainian/practical-policy.json"] if source_ipa is not None and source_ua is not None else []
            unresolved_graphemes = []
            for syllable in structure.get("syllables", []):
                unresolved_graphemes.extend(
                    grapheme["text"] for grapheme in syllable.get("graphemes", [])
                    if grapheme["text"] != syllable.get("base_consonant")
                )
            uncertainty = ()
            if status not in {"PROPOSED", "PUNCTUATION"} or source_ipa is None or source_ua is None:
                uncertainty = (PhoneticUncertainty(
                    status=status,
                    note=unit.get("reason", ""),
                    unresolved_graphemes=tuple(unresolved_graphemes),
                ),)
            typed_units.append(PhoneticUnitResult(
                source=unit["source"],
                status=status,
                ipa=ipa_value,
                ukrainian=ua_value,
                profile=self.profile,
                provenance={
                    "structure": tuple(structural_sources),
                    "phonology": tuple(phonology_sources),
                    "target_policy": tuple(target_sources),
                },
                uncertainty=uncertainty,
            ))

        phonetic_result = PhoneticResult(
            units=tuple(typed_units),
            complete=complete,
            partial=partial,
        ).to_dict()

        if len(linguistic) == 1 and len(rendered) == 1:
            ipa = linguistic[0].get("ipa")
            ukrainian = linguistic[0].get("ukrainian")
        else:
            ipa = "".join(
                unit["ipa"] if unit.get("ipa") is not None else f"⟦{unit['status']}⟧"
                for unit in rendered
            )
            ukrainian = "".join(
                unit["ukrainian"] if unit.get("ukrainian") is not None else ("⟦НЕПІДТРИМУЄТЬСЯ⟧" if unit["status"] == "INVALID_OR_UNSUPPORTED" else _UNKNOWN_UKRAINIAN)
                for unit in rendered
            )

        structure = analyze_structure(normalized)
        rule_trace = list(dict.fromkeys(
            rule for unit in linguistic for rule in unit.get("rule_trace", [])
        ))
        evidence = list(dict.fromkeys(
            source for unit in linguistic for source in unit.get("evidence", [])
        ))
        reasons = list(dict.fromkeys(
            unit["reason"] for unit in linguistic if unit.get("reason")
        ))
        result: dict[str, Any] = {
            "input": text, "normalized": normalized, "profile": self.profile,
            "engine": self.engine_id, "deterministic": True,
            "ipa": ipa, "ukrainian": ukrainian,
            "status": _combine_status(linguistic),
            "rule_trace": rule_trace,
            "reason": " ".join(reasons),
            "evidence": evidence,
            "units": rendered,
            "phonetic_result": phonetic_result,
            "structure": structure.phonological_representation,
            "complete": complete,
            "partial": partial,
        }
        if len(linguistic) == 1:
            for key in ("provisional_ipa", "provisional_ukrainian", "fallback_status", "fallback_trace",
                        "lexical_ua_reference", "lexical_mapping_agrees"):
                if key in linguistic[0]:
                    result[key] = linguistic[0][key]
        return result


# Backward-compatible name: this is no longer an ensemble or a model hybrid.
HybridKhmerEngine = RuleBasedKhmerEngine


def create_hybrid_engine() -> RuleBasedKhmerEngine:
    """Compatibility factory returning the deterministic rule engine only."""
    return RuleBasedKhmerEngine()
