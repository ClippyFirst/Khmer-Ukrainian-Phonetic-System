"""Comparable Python RuleBasedKhmerEngine throughput and coverage benchmark."""
from __future__ import annotations
import json
import statistics
import time
from collections import Counter
from pathlib import Path
from khmer_ua.rule_engine import RuleBasedKhmerEngine

ROOT = Path(__file__).resolve().parents[1]
fixtures = json.loads((ROOT / "data/tests/web-fixtures.json").read_text(encoding="utf-8"))
lexical = json.loads((ROOT / "data/tests/verified-lexical-corpus.json").read_text(encoding="utf-8"))
onset_fallbacks = json.loads((ROOT / "data/tests/khmer-onset-fallback-fixtures.json").read_text(encoding="utf-8"))
inputs = sorted(set(fixtures) | set(lexical) | {case["source"] for case in onset_fallbacks["cases"]})
engine = RuleBasedKhmerEngine()
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
outcomes = [engine.analyze(value) for value in inputs]
coverage = {
    "complete": sum(bool(item.get("complete")) for item in outcomes),
    "partial": sum(bool(item.get("partial")) for item in outcomes),
    "unresolved": sum(not item.get("complete") and not item.get("partial") for item in outcomes),
}
print(json.dumps({
    "runtime": "python",
    "corpus": "web-fixtures ∪ verified-lexical-corpus (input-only; not IPA gold)",
    "fixture_count": len(inputs),
    "rounds": rounds,
    "median_ms_per_fixture_batch": round(median_ms, 4),
    "fixtures_per_second": round(len(inputs) * 1000 / median_ms, 2),
    "coverage": coverage,
    "status_counts": dict(sorted(Counter(item.get("status", "UNKNOWN") for item in outcomes).items())),
}, ensure_ascii=False))
