"""Emit a compact Python structural reference for the JS parity test."""
from __future__ import annotations

import json
from pathlib import Path

from khmer_ua.parser import analyze as analyze_structure, segment_syllables
from khmer_ua.rule_engine import RuleBasedKhmerEngine

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = json.loads((ROOT / "data/tests/structural-parity.json").read_text(encoding="utf-8"))
rows = []
engine = RuleBasedKhmerEngine()
for source in FIXTURE["cases"]:
    engine_result = engine.analyze(source)
    if len(engine_result.get("units", [])) != 1:
        raise RuntimeError(f"expected one rule-engine unit for {source!r}")
    engine_unit = engine_result["units"][0]
    tokens = segment_syllables(source)
    units = []
    for token in tokens:
        result = analyze_structure(token)
        syllables = result.phonological_representation.get("syllables", [])
        syllable = syllables[0] if len(syllables) == 1 else None
        if syllable is None:
            units.append({"source": token, "syllable": None})
            continue
        units.append({
            "source": token,
            "syllable": {
                "base_consonant": syllable.get("base_consonant"),
                "register": syllable.get("register"),
                "subscripts": syllable.get("subscripts", []),
                "subscript_independent_vowels": syllable.get("subscript_independent_vowels", []),
                "vowel_signs": syllable.get("vowel_signs", []),
                "independent_vowel": syllable.get("independent_vowel"),
                "status": syllable.get("status"),
                "inherent_vowel": syllable.get("inherent_vowel"),
                "register_shifter": syllable.get("phonology", {}).get("register_shifter"),
                "confidence": syllable.get("confidence", 0.0),
                "sources": syllable.get("sources", []),
                "graphemes": syllable.get("graphemes", []),
                "onset_ipa": syllable.get("phonology", {}).get("onset_ipa"),
            },
        })
    rows.append({
        "input": source, "tokens": tokens, "units": units,
        "engine_unit": {
            "source": engine_unit["source"],
            "ipa": engine_unit.get("ipa"),
            "ukrainian": engine_unit.get("ukrainian"),
            "status": engine_unit["status"],
        },
    })
print(json.dumps({"schema": "khmer-structural-parity-reference/v1", "cases": rows}, ensure_ascii=False))
