# Evidence-gated hybrid IPA candidate API

## Contract

`HybridKhmerEngine` always obtains the canonical `ipa` and `ukrainian` values from `RuleBasedKhmerEngine`. Explicitly injected external providers are validated and retained individually. When canonical IPA is unresolved, the API additionally exposes a separate `provisional_candidate`: the first configured provider whose IPA maps completely through the Ukrainian adapter, or the first valid IPA candidate if none maps. This candidate is explicitly `PROVISIONAL`, carries provider provenance and uncertainty, and never overwrites canonical fields. Provider order is triage only; there is no majority vote, synthetic consensus, accuracy ranking, or automatic promotion.

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
# result["ipa"] and result["ukrainian"] remain canonical rule-engine fields.
# result["provisional_candidate"] is a separate candidate when canonical IPA is unresolved.
```

## Optional adapters and limitations

`make_khmerphonemizer_backend` lazily imports the pinned Khmer Phonemizer package and returns an unadjudicated `PHONETIC_BROAD` / `PARTIAL` candidate. Install it with `pip install -e ".[phonemizer]"` and explicitly enable it with `create_hybrid_engine(include_khmerphonemizer=True)`. The core package never auto-discovers or silently invokes external providers.

`make_mekongphon_backend` lazily loads the pinned external model only when explicitly injected and called. `make_command_backend` wraps a caller-supplied pinned CLI command. These adapters are also opt-in; optional dependencies are not installed by the core package. When canonical IPA is unresolved, the first mappable provider result is surfaced through `provisional_candidate`; if no candidate maps fully, the first valid IPA is still returned with its exact mapping failure. Canonical fields are unchanged.

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


## Typed IPA adapter integration — 2026-11-24

Provider candidates are now tokenized into the same source-independent `TypedPhoneticResult` model before target adaptation. The IPA parser preserves valid IPA even if the Ukrainian correspondence table cannot map it; the target adapter then withholds the Ukrainian value and the provider diagnostic retains the exact unsupported tail. Provider status, profile match, provenance and uncertainty remain separate from canonical engine status. A provider's `COMPLETE` assertion does not become `SUPPORTED` gold, and no provider candidate overwrites canonical IPA or Ukrainian output.

The target adapter consumes typed IPA only. It does not read Khmer graphemes or the romanization route. BGN/PCGN orthographic fallback remains a separate display candidate and is never passed through the IPA adapter.


## Browser-local MekongPhon port — 2026-11-25

The public Pages build now has a separate browser execution path for the pinned `byumatrixlab/khmer-ipa` model:
- Model revision: `20e069d384b240da76320e1569958568c12a54bc`; upstream model-card metadata declares Apache-2.0.
- Export: separate encoder/decoder ONNX graphs, dynamically quantized per-channel INT8; FP32 graphs are used for export validation and are not shipped.
- Runtime: vendored, integrity-pinned ONNX Runtime Web, WASM execution in a dedicated Web Worker; no remote inference endpoint.
- Tokenization: browser ByteLevel BPE implementation is checked against the pinned Transformers tokenizers before the Pages build.
- UX: model weights are lazy-loaded only after an explicit user action; the model's IPA and Ukrainian adaptation remain a separate `PROVISIONAL` candidate with model revision, elapsed time, input token count, model size and uncertainty visible. It does not replace canonical deterministic fields.
- Input privacy: Khmer input is processed in the browser and is not transmitted to a server.

The CI export workflow compares FP32 and INT8 generation against the pinned Transformers model and checks the browser output in production Chromium. This proves deployment/runtime parity only. It does **not** prove linguistic accuracy: there is still no independent adjudicated Phnom Penh IPA gold corpus, and the upstream model's profile equivalence is unverified. The model's upstream training corpus is not downloaded or redistributed. The standard Pages deployment workflow repeats the pinned export, tokenizer check and browser tests before publishing the model assets with the static site.

## Browser-local MekongPhon inference port — 2026-11-25

The earlier Python/provider integration is no longer the only place where the MekongPhon model can run. The site now exposes an explicit, optional browser-local path:

`Khmer input → pinned ByteLevel BPE tokenizers → ONNX encoder → ONNX decoder → IPA candidate → typed IPA parser → Ukrainian practical adapter`.

Implementation details:

- Upstream model: `byumatrixlab/khmer-ipa`, immutable revision `20e069d384b240da76320e1569958568c12a54bc`.
- Export: separate encoder/decoder ONNX graphs; FP32 graphs are used only for validation and removed from the deployable output; dynamically quantized INT8 graphs are shipped.
- Browser runtime: integrity-pinned `onnxruntime-web@1.23.2` (MIT), WebAssembly SIMD, one thread, dedicated Web Worker, same-origin asset fetches only.
- Decoder: greedy, max output length 64 tokens. The upstream beam-4 path remains part of the export parity diagnostic, but is not used in the browser due to latency.
- First use is user-triggered; model weights are about 35 MB and runtime WASM about 12 MB. The browser may cache static assets.
- The raw IPA candidate is committed to the UI before target adaptation. If the typed IPA parser or Ukrainian adapter cannot map some symbols, the raw candidate remains visible and the Ukrainian card explains the partial mapping.
- No input text is transmitted to an inference service. The worker receives the string through local structured-clone messaging; network activity is limited to same-origin model/runtime assets.

Verification: tokenizer parity against pinned Transformers tokenizers; ONNX FP32 generation compared with the pinned PyTorch model using a strict 5% CER ceiling; INT8-vs-FP32 generation comparison; model-enabled production build exercised in Chromium (46/46 Playwright tests). For the reported phrase, ONNX FP32 differs from the Transformers reference by 3.03% CER and INT8 matches the FP32 ONNX candidate exactly. This is **export parity**, not pronunciation accuracy.

Evidence/rights boundary: the upstream model artifact declares Apache-2.0 and the runtime is MIT. The training corpus is not redistributed and its independent rights remain unresolved. Every model output is `PROVISIONAL`; dialect/profile match is `UNVERIFIED`; no independent adjudicated IPA gold exists, so accuracy remains `NOT_ASSESSED`. The deterministic and lexical engines remain the canonical results; the neural candidate is a separate optional card and never silently overrides them.
