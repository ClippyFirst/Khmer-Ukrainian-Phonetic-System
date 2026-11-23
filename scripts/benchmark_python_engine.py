"""Comparable Python RuleBasedKhmerEngine throughput benchmark."""
from __future__ import annotations
import json
import statistics
import time
from pathlib import Path
from khmer_ua.rule_engine import RuleBasedKhmerEngine

ROOT = Path(__file__).resolve().parents[1]
fixtures = json.loads((ROOT / "data/tests/web-fixtures.json").read_text(encoding="utf-8"))
engine = RuleBasedKhmerEngine()
inputs = list(fixtures)
for _ in range(5):
    for value in inputs:
        engine.analyze(value)
rounds = 25
samples = []
for _ in range(rounds):
    start = time.perf_counter_ns()
    for value in inputs:
        engine.analyze(value)
    samples.append((time.perf_counter_ns() - start) / 1_000_000)
median_ms = statistics.median(samples)
print(json.dumps({
    "runtime": "python",
    "fixture_count": len(inputs),
    "rounds": rounds,
    "median_ms_per_fixture_batch": round(median_ms, 4),
    "fixtures_per_second": round(len(inputs) * 1000 / median_ms, 2),
}, ensure_ascii=False))
