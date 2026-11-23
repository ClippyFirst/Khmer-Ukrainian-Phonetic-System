# Evidence-gated hybrid IPA candidate API

## Contract

`HybridKhmerEngine` always obtains the published `ipa` and `ukrainian` values from `RuleBasedKhmerEngine`. Explicitly injected external providers may add diagnostic candidates, but cannot vote, override, or otherwise alter those values.

Every provider must return a structured mapping containing:
- `ipa`: the raw IPA string;
- `kind`: `PHONEMIC`, `PHONETIC_BROAD`, or `PHONETIC_NARROW`;
- `status`: `COMPLETE` or `PARTIAL`;
- optional `profile` (defaults to the one currently selected by the project);
- `uncertainty`: required and non-empty for `PARTIAL`;
- optional `provenance` mapping.

Bare strings are rejected. Every candidate passes through `validate_ipa_candidate`; malformed notation and unsupported metadata become provider failures, not candidate strings. Raw IPA is preserved exactly. A PARTIAL candidate is retained for inspection but is not a complete pronunciation. COMPLETE remains a provider assertion, not independent adjudication.

## Example

```python
from khmer_ua import HybridKhmerEngine

engine = HybridKhmerEngine({
    "example-provider": lambda text: {
        "ipa": "kʰmae",
        "profile": "khmer-pph-careful-citation-v1",
        "kind": "PHONETIC_BROAD",
        "status": "PARTIAL",
        "uncertainty": ["not independently adjudicated"],
        "provenance": {"revision": "pinned-provider-revision"},
    }
})
result = engine.analyze("ខ្មែរ")
# result["ipa"] and result["ukrainian"] still come from RuleBasedKhmerEngine.
```

## Optional adapters and limitations

`make_mekongphon_backend` lazily loads the pinned external model only when explicitly injected and called. `make_command_backend` wraps a caller-supplied pinned CLI command. Neither adapter is enabled by default; optional dependencies are not installed by the core package.

Provider priority (MekongPhon 10, Khmer Phonemizer 20, Epitran 30, unknown 50, Goruut 90) is diagnostic ordering only, not a quality score. Provider execution is opt-in and may invoke external code; callers are responsible for pinning, sandboxing and reviewing the command/dependency and its rights.

The existing MekongPhon diagnostic harness and manual-only workflow are separate from this runtime API. No corpus is copied or automatically downloaded by this module. Corpus rights and train/evaluation split independence remain unresolved. Independent adjudicated Phnom Penh IPA gold remains 0; empirical accuracy remains null.

This is a research interface, not a production fallback or a phonological truth validator.

## Archived browser candidate snapshot

The static browser does not run Python providers or call external G2P services. It contains one explicit, phrase-scoped snapshot from Quality workflow run [45080727416](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45080727416), artifact [14777495017](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45080727416/artifacts/14777495017), stored in `data/khmer/provisional-ipa-candidates.json`.

For `កម្ពុជាប្រជាធិបតេយ្យ`:
- Khmer Phonemizer 0.0.3 produced `kampuciə prɑciətʰɨppaʔtaj`. The browser re-runs the canonical IPA→Ukrainian adapter over this saved IPA and checks it against the artifact's recorded mapping before selecting it for display.
- MekongPhon revision `20e069d384b240da76320e1569958568c12a54bc` produced `kampucieprɑcietʰiʔpaʔtay`; the current Ukrainian mapping is withheld at `y`.
- Epitran's raw output is retained only as a rejected backend failure because it contains a non-IPA Khmer combining mark.

The selected browser display is `/kampuciə prɑciətʰɨppaʔtaj/???` and `кампутьіє пратьієт'иппатай???`. The marker applies to the complete unadjudicated candidate. `profile_match=UNVERIFIED`; this snapshot is not expert gold, a measured-accuracy result, or evidence that the external provider's dialect/style equals the selected citation profile. The canonical deterministic result and all raw candidate/failure records remain separately inspectable. Provider order selects a display candidate only; it is not voting or ranking by accuracy.
