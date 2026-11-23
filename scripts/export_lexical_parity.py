"""Export Python rule-engine outputs for every browser lexical fixture."""
from __future__ import annotations

import json
from pathlib import Path

from khmer_ua.rule_engine import RuleBasedKhmerEngine

ROOT = Path(__file__).resolve().parents[1]
fixtures = json.loads((ROOT / "data/tests/web-fixtures.json").read_text(encoding="utf-8"))
engine = RuleBasedKhmerEngine()
rows = []
for source in fixtures:
    result = engine.analyze(source)
    units = result.get("units", [])
    rows.append({
        "input": source,
        "units": [{
            "source": unit.get("source"),
            "ipa": unit.get("ipa"),
            "ukrainian": unit.get("ukrainian"),
            "status": unit.get("status"),
            "lexical_mapping_agrees": unit.get("lexical_mapping_agrees"),
        } for unit in units],
    })
print(json.dumps({"schema": "khmer-lexical-parity-reference/v1", "cases": rows}, ensure_ascii=False))
