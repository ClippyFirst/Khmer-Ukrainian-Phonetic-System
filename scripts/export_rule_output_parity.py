"""Export deterministic Python rule-engine outputs for consonant/shifter parity."""
from __future__ import annotations
import json
from pathlib import Path
from khmer_ua.rule_engine import RuleBasedKhmerEngine

ROOT = Path(__file__).resolve().parents[1]
fixture = json.loads((ROOT / "data/tests/rule-output-parity.json").read_text(encoding="utf-8"))
engine = RuleBasedKhmerEngine()
rows = []
for source in fixture["cases"]:
    result = engine.analyze(source)
    if len(result.get("units", [])) != 1:
        raise RuntimeError(f"expected one unit for {source!r}")
    unit = result["units"][0]
    typed_unit = result["phonetic_result"]["units"][0]
    typed_ipa = typed_unit.get("typed_ipa")
    typed_ipa_parity = None if typed_ipa is None else {
        "phonemic_ipa": typed_ipa["phonemic_ipa"],
        "status": typed_ipa["status"],
        "segments": [
            {"ipa": segment["ipa"], "kind": segment["kind"], "certainty": segment["certainty"]}
            for segment in typed_ipa["segments"]
        ],
        "syllable_boundaries": typed_ipa["syllable_boundaries"],
        "vowel_length": typed_ipa["vowel_length"],
        "tone_category": typed_ipa["tone_category"],
        "tone_contour_ipa": typed_ipa["tone_contour_ipa"],
    }
    rows.append({
        "source": unit["source"],
        "ipa": unit.get("ipa"),
        "ukrainian": unit.get("ukrainian"),
        "status": unit["status"],
        "rule_trace": unit.get("rule_trace", []),
        "confidence_tier": unit.get("confidence_tier"),
        "evidence": unit.get("evidence", []),
        "typed_ipa": typed_ipa_parity,
        "typed_ukrainian": typed_unit.get("ukrainian"),
        "typed_ukrainian_kind": typed_unit.get("ukrainian_kind"),
    })
print(json.dumps({"schema": "khmer-rule-output-parity-reference/v1", "cases": rows}, ensure_ascii=False))
