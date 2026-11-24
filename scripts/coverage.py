"""Generate a deterministic, evidence-gated Khmer vowel coverage inventory.

Run from the repository root:
    python scripts/coverage.py
    python scripts/coverage.py --check

The inventory reports evidence already present in the canonical registry. It never
infers pronunciation from Unicode names or structure and never labels examples gold.
"""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "khmer"
OUT = ROOT / "reports" / "khmer-coverage-audit.json"
PUBLIC_OUT = ROOT / "public" / "reports" / "khmer-coverage-audit.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))



def _nonempty_items(value):
    """Return explicitly stored non-empty orthographic markers without interpreting them."""
    if value is None:
        return []
    values = value if isinstance(value, list) else [value]
    return [item for item in values if item is not None and str(item).strip()]


def build_contextual_vowel_evidence(cases, sources, context_dimensions=None, coda_pattern_observations=None, lexical_coda_examples=None, lexical_stress_examples=None, reference_mapping_inventory=None, reference_mapping_observations=None):
    """Expose exact case-level context while refusing to infer missing phonology.

    This is an evidence inventory, not a Cartesian prediction matrix. In particular,
    an absent IPA length mark does not prove a short vowel, an orthographic final
    marker does not prove a phonological coda, and missing profile metadata stays
    explicitly unknown.
    """
    observations = []
    counts = Counter()
    status_counts = Counter()
    for case in sorted(cases, key=lambda item: item.get("id", "")):
        structure = case.get("grapheme_structure") or {}
        dependent = _nonempty_items(structure.get("dependent_vowels"))
        subscripts = _nonempty_items(structure.get("subscripts"))
        coda_marker = structure.get("coda")
        has_coda_marker = bool(_nonempty_items(coda_marker))
        ipa = case.get("ipa")
        has_length_mark = bool(ipa and "ː" in ipa)
        source_id = case.get("ipa_source")
        source = sources.get(source_id, {})
        profile = case.get("profile")
        observation = {
            "case_id": case.get("id"),
            "orthography": case.get("orthography"),
            "source_id": source_id,
            "source_role": source.get("role"),
            "evidence_status": case.get("status", "UNCLASSIFIED"),
            "base_consonant_class": case.get("base_consonant_class", "NOT_ESTABLISHED"),
            "dependent_vowel_sequence": dependent,
            "inherent_or_no_dependent_sign_context": not dependent,
            "subscript_sequence": subscripts,
            "register_shifter_sign": structure.get("register_shifter"),
            "orthographic_coda_marker": coda_marker,
            "phonological_syllable_type": case.get("phonological_syllable_type", "NOT_ESTABLISHED"),
            "profile": profile if profile else "NOT_SPECIFIED_PER_CASE",
            "source_transcription": ipa,
            "length_evidence": (
                "EXPLICIT_LENGTH_MARK_IN_SOURCE_TRANSCRIPTION" if has_length_mark else
                "NO_EXPLICIT_LENGTH_MARK_SHORTNESS_NOT_INFERRED" if ipa else
                "NOT_ESTABLISHED_NO_SOURCE_TRANSCRIPTION"
            ),
        }
        observations.append(observation)
        counts["cases_with_dependent_vowel" if dependent else "cases_without_dependent_vowel"] += 1
        counts["cases_with_subscripts" if subscripts else "cases_without_subscripts"] += 1
        counts["cases_with_orthographic_coda_marker" if has_coda_marker else "cases_without_orthographic_coda_marker"] += 1
        counts["cases_with_register_shifter" if structure.get("register_shifter") else "cases_without_register_shifter"] += 1
        counts["cases_with_explicit_length_mark" if has_length_mark else "cases_without_explicit_length_mark_or_ipa"] += 1
        counts["cases_with_explicit_profile" if profile else "cases_without_explicit_profile"] += 1
        counts["cases_with_source_transcription" if ipa else "cases_without_source_transcription"] += 1
        status_counts[observation["evidence_status"]] += 1

    return {
        "purpose": (
            "Case-level source evidence with orthographic context preserved. This is not a complete "
            "series × vowel × syllable × coda × length × profile cross-product and does not generate IPA."
        ),
        "observations": observations,
        "case_counts": dict(sorted(counts.items())),
        "evidence_status_counts": dict(sorted(status_counts.items())),
        "context_dimensions": {
            "base_consonant_class": "RECORDED_WHERE_PRESENT; not a complete lexical contrast set",
            "dependent_vowel_sequence": "EXACT_ORTHOGRAPHIC_SEQUENCE_RECORDED; no extrapolation to unseen cells",
            "subscripts_and_coeng": "ORTHOGRAPHIC_MARKERS_RECORDED; syllabification remains separate",
            "coda": "ORTHOGRAPHIC_MARKER_RECORDED; phonological coda class NOT_ESTABLISHED_PER_CASE",
            "syllable_type": "NOT_ESTABLISHED_UNLESS_EXPLICITLY_RECORDED",
            "vowel_length": "ONLY_EXPLICIT_SOURCE_LENGTH_MARKS_RECORDED; absence is not classified as short",
            "register_shifter": "EXACT_MARKER_RECORDED_WHERE_PRESENT; contextual phonetic effect not inferred",
            "profile": "NOT_SPECIFIED_PER_CASE_UNLESS_EXPLICITLY_RECORDED",
            "stress_and_harmony": "NOT_CAPTURED_IN_CURRENT_CASE_ROWS",
            "phonemic_vs_phonetic_level": "SOURCE_TRANSCRIPTION_CONVENTION_RETAINED; no normalization or merging",
        },
        "source_backed_context_dimensions": [
            {
                "id": item["id"],
                "dimension": item["dimension"],
                "source_ids": item["source_ids"],
                "locator": item["locator"],
                "profile_scope": item["profile_scope"],
                "evidence_status": item["evidence_status"],
                "implementation": item["implementation"],
            }
            for item in sorted(context_dimensions or [], key=lambda row: row["id"])
        ],
        "context_dimension_count": len(context_dimensions or []),
        "source_backed_coda_pattern_observations": [
            {
                "id": item["id"],
                "pattern": item["pattern"],
                "base_consonant_class": item["base_consonant_class"],
                "source_ipa": item["source_ipa"],
                "source_id": item["source_id"],
                "source_locator": item["source_locator"],
                "evidence_status": item["evidence_status"],
                "profile_scope": item["profile_scope"],
                "ukrainian_adaptation": item["ukrainian_adaptation"],
                "ukrainian_status": item["ukrainian_status"],
                "limitations": item["limitations"],
            }
            for item in sorted(coda_pattern_observations or [], key=lambda row: row["id"])
        ],
        "coda_pattern_observation_count": len(coda_pattern_observations or []),
        "source_backed_lexical_coda_examples": [
            {
                "id": item["id"],
                "orthography": item["orthography"],
                "source_phonological_transcription": item["source_phonological_transcription"],
                "transcription_system": item["transcription_system"],
                "gloss": item["gloss"],
                "phonological_context": item["phonological_context"],
                "source_id": item["source_id"],
                "source_locator": item["source_locator"],
                "profile_scope": item["profile_scope"],
                "evidence_status": item["evidence_status"],
                "ipa": item["ipa"],
                "ukrainian_adaptation": item["ukrainian_adaptation"],
                "ukrainian_status": item["ukrainian_status"],
                "limitations": item["limitations"],
            }
            for item in sorted(lexical_coda_examples or [], key=lambda row: row["id"])
        ],
        "lexical_coda_example_count": len(lexical_coda_examples or []),
        "source_backed_lexical_stress_examples": [
            {
                "id": item["id"],
                "orthography": item["orthography"],
                "source_phonological_transcription": item["source_phonological_transcription"],
                "transcription_system": item["transcription_system"],
                "gloss": item["gloss"],
                "phonological_context": item["phonological_context"],
                "source_id": item["source_id"],
                "source_locator": item["source_locator"],
                "profile_scope": item["profile_scope"],
                "evidence_status": item["evidence_status"],
                "ipa": item["ipa"],
                "ukrainian_adaptation": item["ukrainian_adaptation"],
                "ukrainian_status": item["ukrainian_status"],
                "limitations": item["limitations"],
            }
            for item in sorted(lexical_stress_examples or [], key=lambda row: row["id"])
        ],
        "lexical_stress_example_count": len(lexical_stress_examples or []),
        "reference_mapping_inventory": {
            "source_id": reference_mapping_inventory["source_id"],
            "source_locator": reference_mapping_inventory["source_locator"],
            "reported_table_rows": reference_mapping_inventory["reported_table_rows"],
            "license_status": reference_mapping_inventory["license_status"],
            "redistribution_status": reference_mapping_inventory["redistribution_status"],
            "runtime_eligible": reference_mapping_inventory["runtime_eligible"],
            "data_values_copied": reference_mapping_inventory["data_values_copied"],
            "notes": reference_mapping_inventory["notes"],
        },
        "source_backed_reference_mapping_observations": [
            {
                "id": item["id"],
                "source_transcription": item["source_transcription"],
                "consonant_class_scope": item["consonant_class_scope"],
                "orthographic_context": item["orthographic_context"],
                "source_id": item["source_id"],
                "source_locator": item["source_locator"],
                "mapping_kind": item["mapping_kind"],
                "evidence_status": item["evidence_status"],
                "profile_scope": item["profile_scope"],
                "license_id": item["license_id"],
                "license_url": item["license_url"],
                "attribution": item["attribution"],
                "changes_made": item["changes_made"],
                "runtime_eligible": item["runtime_eligible"],
                "ukrainian_adaptation": item["ukrainian_adaptation"],
                "ukrainian_status": item["ukrainian_status"],
                "limitations": item["limitations"],
            }
            for item in sorted(reference_mapping_observations or [], key=lambda row: row["id"])
        ],
        "reference_mapping_observation_count": len(reference_mapping_observations or []),
        "context_dimension_evidence_status_counts": dict(sorted(Counter(
            item["evidence_status"] for item in (context_dimensions or [])
        ).items())),
        "cross_product_assessment": {
            "status": "NOT_ESTABLISHED",
            "required_dimensions": [
                "profile × consonant series × dependent-vowel sequence",
                "vowel sequence × phonological coda identity",
                "vowel sequence × open/closed syllable type",
                "vowel sequence × measured vowel length",
                "vowel sequence × stress and harmony context",
                "register-shifter eligibility × lexical exception",
                "phonemic target × phonetic realization",
            ],
            "policy": "Do not fill missing combinations by analogy or Unicode structure.",
        },
    }


def build_report(signs, consonants, registers, evidence):
    """Build the report from canonical data without modifying or adjudicating it."""
    if not isinstance(signs, list) or not isinstance(consonants, list):
        raise ValueError("signs.json and consonants.json must contain JSON arrays")
    if not isinstance(registers, dict) or not isinstance(registers.get("registers"), list):
        raise ValueError("registers.json must contain a 'registers' array")
    if not isinstance(evidence, dict) or not isinstance(evidence.get("cases"), list):
        raise ValueError("vowel-context-register.json must contain a 'cases' array")

    cases = evidence["cases"]
    dependent = [s for s in signs if s.get("kind") == "dependent_vowel"]
    independent = [s for s in signs if s.get("kind") == "independent_vowel"]
    cells = {}
    for sign in dependent:
        if not sign.get("char") or not sign.get("codepoint"):
            raise ValueError(f"Dependent vowel lacks char/codepoint: {sign!r}")
        for series in ("first", "second"):
            matches = [
                case for case in cases
                if (case.get("grapheme_structure") or {}).get("dependent_vowels") == [sign["char"]]
                and case.get("base_consonant_class") == series
            ]
            conflicts = [case for case in matches if case.get("status") == "CONFLICTING_SOURCE_ANALYSES"]
            attested = [
                case for case in matches
                if case.get("ipa") and case.get("status") == "SOURCE_ATTESTED_NOT_GOLD"
            ]
            # Conflict takes precedence: never hide a disagreement behind another row.
            status = (
                "CONFLICTING_SOURCE_ANALYSES" if conflicts else
                "SOURCE_ATTESTED_NOT_GOLD" if attested else
                "NOT_ESTABLISHED"
            )
            cells[f'{sign["codepoint"]}:{series}'] = {
                "sign": sign["char"],
                "codepoint": sign["codepoint"],
                "series": series,
                "status": status,
                "case_ids": [case.get("id") for case in matches],
                "ipa_values": [] if conflicts else sorted({case["ipa"] for case in attested}),
                "conflicting_case_ids": [case.get("id") for case in conflicts],
                "limitation": (
                    "Source-attested examples are not gold and do not establish a universal rule."
                    if status == "SOURCE_ATTESTED_NOT_GOLD" else
                    "Conflicting analyses are retained; no single value is selected."
                    if status == "CONFLICTING_SOURCE_ANALYSES" else
                    "No exact sign × series IPA evidence; do not infer from Unicode structure."
                ),
            }

    features = Counter()
    source_statuses = Counter()
    for case in cases:
        structure = case.get("grapheme_structure") or {}
        features[
            "cases_with_dependent_vowel" if structure.get("dependent_vowels")
            else "cases_without_dependent_vowel"
        ] += 1
        for field, feature in (("subscripts", "cases_with_subscript"), ("coda", "cases_with_coda")):
            value = structure.get(field)
            if value and any(value if isinstance(value, list) else [value]):
                features[feature] += 1
        if structure.get("register_shifter"):
            features["cases_with_register_shifter"] += 1
        source_text = json.dumps(structure, ensure_ascii=False) + " " + str(case.get("register_condition", ""))
        for marker in ("NIKAHIT", "REAHMUK", "COENG"):
            if marker in source_text:
                features["cases_mentioning_" + marker.lower()] += 1
        status = str(case.get("status", "UNCLASSIFIED"))
        source_statuses[status] += 1
        features["cases_" + status.lower()] += 1

    total = len(cells)
    status_counts = Counter(cell["status"] for cell in cells.values())
    conflict_cases = [case for case in cases if case.get("status") == "CONFLICTING_SOURCE_ANALYSES"]
    contextual_evidence = build_contextual_vowel_evidence(
        cases, evidence.get("sources", {}), evidence.get("context_dimensions", []),
        evidence.get("coda_pattern_observations", []),
        evidence.get("lexical_coda_examples", []),
        evidence.get("lexical_stress_examples", []),
        evidence.get("reference_mapping_inventory", {}),
        evidence.get("reference_mapping_observations", [])
    )
    return {
        "schema_version": "1.0.0",
        "generated_by": "scripts/coverage.py",
        "evidence_source_file": "data/khmer/vowel-context-register.json",
        "orthographic_inventory": {
            "consonant_records": len(consonants),
            "register_records": len(registers["registers"]),
            "register_shifter_records": len(registers.get("shifters", [])),
            "dependent_vowel_signs": len(dependent),
            "independent_vowel_signs": len(independent),
            "expected_dependent_vowel_x_series_cells": total,
        },
        "dependent_vowel_by_series": cells,
        "coverage_summary": {
            "source_attested_not_gold_cells": status_counts["SOURCE_ATTESTED_NOT_GOLD"],
            "conflicting_cells": status_counts["CONFLICTING_SOURCE_ANALYSES"],
            "not_established_cells": status_counts["NOT_ESTABLISHED"],
            "coverage_fraction": round(status_counts["SOURCE_ATTESTED_NOT_GOLD"] / total, 4) if total else 0,
            "warning": (
                "First-order sign × series coverage only. This does not certify coda, length, "
                "syllable, register-shifter, lexical or pronunciation-profile contexts."
            ),
        },
        "source_registry_status_counts": dict(sorted(source_statuses.items())),
        "contextual_vowel_evidence": contextual_evidence,
        "source_conflict_case_ids": [case.get("id") for case in conflict_cases],
        "recorded_case_feature_counts": dict(sorted(features.items())),
        "dimensions_requiring_followup": [
            "inherent vowels × consonant series × lexical context",
            "each dependent vowel × series × length × open/closed syllable",
            "coda identity and coda-conditioned vowel quality",
            "NIKAHIT and REAHMUK, including lexical exceptions/conflicts",
            "COENG clusters and orthographic versus phonetic syllabification",
            "MUUSIKATOAN/TRIISAP and exceptional ប៉ construction",
            "standard versus Phnom Penh /r/-loss profiles with positive and negative examples",
            "/c/ versus /cʰ/ preserved in IPA before target adaptation",
            "independent vowels, rare signs, loanwords, malformed input",
        ],
        "interpretation": (
            "A cell is source-attested only for an exact sign and series match with an IPA value "
            "in the existing evidence register. This is SOURCE_ATTESTED_NOT_GOLD, never gold. "
            "Other cells remain NOT_ESTABLISHED; this audit generates no pronunciation. "
            "Conflicts elsewhere in the source registry are listed separately and are not "
            "misrepresented as dependent-vowel matrix conflicts."
        ),
    }


def render_report():
    return json.dumps(
        build_report(
            load(DATA / "signs.json"),
            load(DATA / "consonants.json"),
            load(DATA / "registers.json"),
            load(DATA / "vowel-context-register.json"),
        ),
        ensure_ascii=False,
        indent=2,
    ) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the committed report is missing or stale")
    args = parser.parse_args(argv)
    try:
        rendered = render_report()
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"coverage audit input error: {error}", file=sys.stderr)
        return 2

    if args.check:
        for path in (OUT, PUBLIC_OUT):
            if not path.exists():
                print(f"coverage report missing: {path.relative_to(ROOT)}", file=sys.stderr)
                return 1
            if path.read_text(encoding="utf-8") != rendered:
                print("coverage report is stale: run python scripts/coverage.py and review the diff", file=sys.stderr)
                return 1
        print(f"coverage reports current: {OUT.relative_to(ROOT)} and {PUBLIC_OUT.relative_to(ROOT)}")
        return 0

    for path in (OUT, PUBLIC_OUT):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8")
    report = json.loads(rendered)
    summary = report["coverage_summary"]
    print(json.dumps({
        "output": str(OUT.relative_to(ROOT)),
        "dependent_signs": report["orthographic_inventory"]["dependent_vowel_signs"],
        "expected_cells": report["orthographic_inventory"]["expected_dependent_vowel_x_series_cells"],
        "source_attested_not_gold_cells": summary["source_attested_not_gold_cells"],
        "conflicting_cells": summary["conflicting_cells"],
        "not_established_cells": summary["not_established_cells"],
        "source_conflict_case_ids": report["source_conflict_case_ids"],
        "cases_audited": sum(report["source_registry_status_counts"].values()),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
