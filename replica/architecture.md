# Architecture: Khmer typed IPA engine contract

## Stack

| Layer | Choice | Reason |
|---|---|---|
| Language engine | Existing Python 3.11+ package | Keep current deterministic Khmer reference engine |
| Browser engine | Existing JavaScript ES modules / Node 24 | Maintain exact runtime parity |
| UI | Existing static Vite application | No new frontend framework or runtime service |
| Background execution | Existing Web Worker | Keep user text local and avoid network dependency |
| Result schema | JSON Schema | Validate the typed IPA envelope |
| Data | Existing Khmer source registries and Ukrainian target policy | Do not import Lao linguistic data |
| Hosting | Existing GitHub Pages | No deployment change in this PR |

## Pipeline

```text
Khmer orthography
  → NFC/tokenization
  → Khmer structural parser
  → Khmer phonology / lexical rules
  → TypedPhoneticResult
  → adapt_phonetic_result / adaptPhoneticResult
  → Ukrainian practical orthography
```

The IPA parser does not read the Ukrainian correspondence table. The Ukrainian adapter does not read Khmer graphemes, Khmer positions or romanization. The adapter consumes only `TypedPhoneticResult`.

## Confidence mapping

| Engine input | Typed IPA status | Target behavior |
|---|---|---|
| Full proposed segmental IPA | `UNCERTAIN` | Map through the shared adapter; retain uncertainty |
| Parser-confirmed registered onset only | `PROVISIONAL` | Map known IPA run through the same adapter; render one `???` for unresolved remainder |
| No defensible IPA hint | `UNRESOLVED` | Render `???` |
| Independently supported IPA | `SUPPORTED` | Map through the same adapter |
| Valid IPA with no target correspondence | Keep `UNCERTAIN` / `SUPPORTED` | Withhold Ukrainian mapping; do not relabel source IPA as invalid |

The existing Khmer engine statuses (`PROPOSED`, `EVIDENCE_LIMITED`, `NOT_ESTABLISHED`, etc.) remain unchanged. The nested IPA status is a separate confidence contract; adaptation never promotes it.

## Python API

- `khmer_ua.ipa_result.TypedPhoneticResult`
- `khmer_ua.ipa_result.PhoneticSegment`
- `from_ipa()`
- `from_provisional_ipa()`
- `from_unknown_source_unit()`
- `khmer_ua.ipa_target.adapt_phonetic_result()`

## JavaScript API

- `src/khmer-ipa-result.js`
- `fromIpa()`
- `fromProvisionalIpa()`
- `fromUnknownSourceUnit()`
- `adaptPhoneticResult()`
- `serializePhoneticResult()`

JavaScript typed results are plain structured-clone-safe data. The Worker and synchronous fallback use the same `khmer-engine-core.js` implementation.

## CLI and UI

- `khmer-ua analyze` and `khmer-ua explain`: JSON result including the typed IPA envelope.
- `khmer-ua ipa`: canonical IPA, else provisional IPA + `???`, else `???`.
- `khmer-ua transliterate`: canonical Ukrainian, else IPA-derived provisional result, else `???`.
- Browser unit details show the typed IPA sequence, translated confidence label, provenance and translated uncertainty notes.

## The parts that bite

- A valid IPA symbol can be unrecognized by the target table; source IPA validity and target coverage are separate.
- A provisional result must always retain an unknown tail; it cannot become complete merely because the hint itself maps.
- Consecutive unresolved material is one unknown region, not one marker per Khmer code point.
- Length, stress, tone symbols and syllable boundaries must not be silently discarded by the IPA model.
- Tone is not inferred for Khmer by this change.
- Romanization and external G2P candidates remain independent diagnostic paths.

## Build order

1. Define typed IPA result and adapter tests (RED).
2. Implement Python model, adapter and engine integration.
3. Implement JavaScript model, adapter and browser engine integration.
4. Add schema, Python/JS parity and Worker structured-clone checks.
5. Route CLI through the same engine contract.
6. Expose typed status/provenance/uncertainty in UI.
7. Update execution register, audit, handoff and replica parity artifacts.
