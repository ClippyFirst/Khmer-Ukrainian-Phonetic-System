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
    rows.append({
        "source": unit["source"],
        "ipa": unit.get("ipa"),
        "ukrainian": unit.get("ukrainian"),
        "status": unit["status"],
        "rule_trace": unit.get("rule_trace", []),
        "confidence_tier": unit.get("confidence_tier"),
        "evidence": unit.get("evidence", []),
    })
print(json.dumps({"schema": "khmer-rule-output-parity-reference/v1", "cases": rows}, ensure_ascii=False))
