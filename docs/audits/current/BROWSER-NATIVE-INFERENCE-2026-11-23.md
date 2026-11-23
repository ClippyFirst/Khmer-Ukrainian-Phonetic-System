# Browser-native Khmer inference and worker audit — 2026-11-23

## Decision

Adopt a native-first browser architecture modelled on the Thai repository: JavaScript owns the public pipeline and orchestration; computationally expensive deterministic inference may run in a local Web Worker or WASM module. No runtime server/API, remote inference, telemetry, or transmission of user-entered text is permitted. Static assets, if later introduced, must be pinned, rights-reviewed, integrity-checked and fetched independently of user input.

## Current-state reconciliation

- The existing Khmer browser application already contains a deterministic JavaScript engine in `src/main.js`, including normalization, conservative segmentation, orthographic structure analysis, lexical fixtures, IPA-to-Ukrainian adaptation and evidence/status handling.
- Python `RuleBasedKhmerEngine` is a separate implementation. The current JS UI engine and Python parser/rule engine are not yet proven behaviorally equivalent. A full Python→JS port/parity gate remains TODO.
- The Thai repository provides the relevant architectural precedent: browser-native modules, worker isolation, deterministic data and explicit parity tests. Python is a reference/compatibility route rather than a required runtime dependency for supported browser inputs.
- Existing Khmer external candidates and third-party model research remain separate. No external weights, FST, lexicon or corpus were added by this change; unresolved asset provenance/licensing is not waived.

## Change on branch feat/khmer-native-worker-engine-20261123

- `src/khmer-engine.worker.js`: receives a structured local request and invokes the existing deterministic `convert()` engine.
- `src/khmer-engine-client.js`: lazy worker client; falls back to the same local synchronous implementation if Worker startup or execution fails.
- `src/main.js`: sends phonetic inference to the worker and discards stale responses using a render revision counter. Romanization remains a separate route.
- `tests/khmer-worker-contract.test.mjs`: checks worker wiring, worker-safe import guard and absence of network APIs in the inference modules. Added to both `npm test` and `npm run check`.
- `docs/DETERMINISTIC-RULE-ENGINE.md` and the master handoff record the new execution model and limits.

## Task ledger

| Task | Status | Evidence / acceptance |
|---|---|---|
| Offload existing deterministic browser inference from UI thread | PARTIAL | Worker/client and UI integration committed; exact-head CI and browser evidence still required |
| Keep all user text local | PARTIAL | Worker protocol is same-origin local messaging and contains no network API; verify built bundle and runtime network panel |
| Prevent stale render overwrite during rapid input | PARTIAL | Monotonic render revision guard added; requires browser race/regression test |
| Worker failure fallback | PARTIAL | Client falls back to the same local `convert()`; add simulated worker failure test |
| Full Python↔JavaScript structural/rule parity | TODO | Port missing Python semantics and establish shared fixtures with exact per-unit parity |
| Native Khmer lexical segmentation/OOV model | TODO | Evaluate and pin tokenizer/model only after exact asset rights and parity are established |
| Optional deterministic FST/WASM inference | DEFERRED | May be added if benchmark shows meaningful quality/speed improvement and asset rights are cleared |
| Independent adjudicated IPA gold and accuracy estimate | DEFERRED for beta; BLOCKED for accuracy claims | No expert gold corpus currently available |
| Third-party model/corpus redistribution | BLOCKED | Item-level data/model provenance and license scope remain unresolved |

## Verification

No local test/build/browser command was executed in this session because the local environment could not resolve GitHub for repository checkout. No passing CI or deployment is claimed here. Required next checks: full `npm test`, `npm run build`, Playwright browser suite, exact-head GitHub Actions, deployed Pages smoke and runtime network inspection. Merge only after exact-head checks pass.

## Release assessment

This is an incremental performance/UX improvement, not completion of the requested engine port. The repository remains a research/beta prototype; linguistic accuracy remains NOT_ASSESSED. The change is not release-ready until CI/build/browser checks pass. Full Python↔JavaScript parity and evidence-backed phonology remain separate acceptance gates.


## Exact-head verification addendum

- Code head `a8a00e1660b6b0fdba1c93475c766d8480f62bcd` passed Quality [45135417588](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45135417588) and Chromium [45135417537](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45135417537).
- Quality: Python 453 passed + 70 subtests; all Node web checks and Vite production build passed.
- Chromium: 33/33 passed, including actual worker execution and worker-asset failure fallback.
- The worker bundle was 136.40 kB. This is a bundle-size observation, not a throughput benchmark.
- The PR remains unmerged, so no GitHub Pages deployment or post-deploy smoke is claimed.
- Worker integration is DONE_VERIFIED. Full Python↔JS semantic parity and OOV/tokenizer integration remain TODO; third-party asset rights remain BLOCKED; expert IPA gold is deferred for beta and remains a blocker to accuracy claims.
