import json
from khmer_ua.romanization_ipa import build_romanization_ipa_candidate

cases = [
    ("ខ្មែរ", "khmer"),
    ("ង", "ng"),
    ("ប", "b"),
    ("ក", "kh"),
    ("្ក", "k"),
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
