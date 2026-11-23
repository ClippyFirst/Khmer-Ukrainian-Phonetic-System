"""Export Python n-best segmentation diagnostics for JS parity checks."""
from __future__ import annotations

import json
from pathlib import Path

from khmer_ua.rule_engine import RuleBasedKhmerEngine

ROOT = Path(__file__).resolve().parents[1]
fixture = json.loads((ROOT / "data/tests/word-segmentation-parity.json").read_text(encoding="utf-8"))
engine = RuleBasedKhmerEngine()
rows = []
for case in fixture["cases"]:
    result = engine.analyze(case["input"])
    rows.append({
        "input": case["input"],
        "candidate_runs": result["word_segmentation"]["candidate_runs"],
    })
print(json.dumps({
    "schema": "khmer-segmentation-candidate-parity/v1",
    "cases": rows,
}, ensure_ascii=False))
