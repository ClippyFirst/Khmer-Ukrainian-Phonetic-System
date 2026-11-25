import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "src"))

from khmer_ua.romanization_ipa import build_romanization_ipa_candidate

with (_ROOT / "data" / "khmer" / "romanization_ipa_onsets.json").open(encoding="utf-8") as handle:
    inventory = json.load(handle)

unlisted_vowels = [
    ("កិ", "ke"), ("គិ", "ki"), ("កឹ", "koe"), ("គឹ", "koe"),
    ("កឺ", "koe"), ("គឺ", "koe"), ("កុ", "ko"), ("គុ", "ku"),
    ("កូ", "ko"), ("គូ", "ku"), ("កេ", "ke"), ("គេ", "ke"),
    ("កែ", "ke"), ("គែ", "ke"), ("កៃ", "kai"), ("គៃ", "key"),
    ("កោ", "kao"), ("គោ", "ko"), ("កៅ", "kau"), ("គៅ", "kou"),
    ("កើ", "kaeu"), ("គើ", "keu"), ("កឿ", "koea"), ("គឿ", "koea"),
    ("កួ", "kuo"), ("គួ", "kuo"),
]
cases = [
    (entry["source_units"][0], entry["romanization"])
    for entry in inventory["entries"]
] + [
    (entry["source"], entry["romanization"])
    for entry in inventory.get("representative_syllables", [])
] + [
    ("ប", "b"),
    ("ក", "kh"),
    ("្ក", "k"),
] + unlisted_vowels + [
    ("កី", "ki"),
    ("គី", "kei"),
]
output = []
for source, romanized in cases:
    result = build_romanization_ipa_candidate(source, romanized)
    output.append({
        "source": source,
        "romanized": romanized,
        "status": result["status"],
        "ukrainian": result["ukrainian"],
        "romanized_onset": result["romanized_onset"],
        "typed_ipa": result["typed_ipa"].to_dict(),
        "provenance": list(result["provenance"]),
        "uncertainty": list(result["uncertainty"]),
    })
print(json.dumps(output, ensure_ascii=False))
