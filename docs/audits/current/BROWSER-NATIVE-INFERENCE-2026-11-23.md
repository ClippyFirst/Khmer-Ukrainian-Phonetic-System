# Browser-native Khmer inference and worker audit — 2026-11-23

## Decision

Adopt a native-first browser architecture modelled on the Thai repository: JavaScript owns the public pipeline and orchestration; computationally expensive deterministic inference may run in a local Web Worker or WASM module. No runtime server/API, remote inference, telemetry, or transmission of user-entered text is permitted. Static assets, if later introduced, must be pinned, rights-reviewed, integrity-checked and fetched independently of user input.

## Current-state reconciliation

- The existing Khmer browser application already contains a deterministic JavaScript engine in `src/khmer-engine-core.js`, including normalization, conservative segmentation, orthographic structure analysis, lexical fixtures, IPA-to-Ukrainian adaptation and evidence/status handling.
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
| Offload existing deterministic browser inference from UI thread | DONE_VERIFIED | Exact-head CI and Chromium confirm the local Worker path runs |
| Keep all user text local in the inference path | DONE_VERIFIED | Worker/client use local messaging only; static contract test rejects network APIs in these modules. A separate manual network-panel audit remains optional follow-up |
| Prevent stale render overwrite during rapid input | DONE_VERIFIED | Chromium race test deliberately delays the first Worker response and confirms it cannot overwrite the second input |
| Worker failure fallback | DONE_VERIFIED | Chromium test aborts the Worker asset request and confirms the same local engine returns the result |
| Shared tokenizer boundary parity cases | DONE_VERIFIED | Python and browser tests consume `data/tests/tokenizer-parity.json`; Unicode 18 subscript-vowel+coda regression passes in both runtimes |
| Eight-case Python↔JavaScript structural parity harness | DONE_VERIFIED | CI compares token boundaries and core structural fields for eight representative inputs; exact-head run passed |
| Full Python↔JavaScript structural/rule semantic parity | PARTIAL | The executable parity harness covers representative cases; broader structure/IPA cases and full result-contract parity remain outstanding |
| Deterministic orthographic token boundaries and fixture matching | DONE_VERIFIED | Shared cross-runtime boundary fixtures and trie-based longest fixture matching; synthetic 8k stress benchmark 77.7× vs pre-trie implementation |
| Native Khmer lexical word segmentation/OOV model | TODO | Evaluate and pin lexical tokenizer/model only after exact asset rights and phonological parity are established |
| Optional deterministic FST/WASM inference | DEFERRED | May be added if benchmark shows meaningful quality/speed improvement and asset rights are cleared |
| Independent adjudicated IPA gold and accuracy estimate | DEFERRED for beta; BLOCKED for accuracy claims | No expert gold corpus currently available |
| Third-party model/corpus redistribution | BLOCKED | Item-level data/model provenance and license scope remain unresolved |

## Verification

Local checkout was unavailable, so local commands are not claimed. GitHub Actions on exact code head `c2dc56949ee519dfcdb13139e49002b92a3fa5bc` passed Quality [45136544361](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45136544361) and Chromium [45136544247](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45136544247). Quality: 453 Python tests + 70 subtests, all Node checks and Vite production build passed. Chromium: 34/34 passed, including Worker execution, Worker asset failure fallback, and an intentionally delayed first response proving stale results cannot overwrite newer input. The Worker bundle is 124.02 kB. No Pages deployment or post-deploy smoke is claimed because the PR remains unmerged.

## Release assessment

The Worker/UI engineering change is verified and ready for review, but the repository is not yet updated on `main` or deployed from this PR. This is not completion of the requested Python→JavaScript engine port: semantic parity, broader tokenizer/OOV integration and measured throughput remain open. The repository remains a research/beta prototype; linguistic accuracy is NOT_ASSESSED. Full Python↔JavaScript parity and evidence-backed phonology remain separate acceptance gates.


## Exact-head verification addendum

- Code head `a8a00e1660b6b0fdba1c93475c766d8480f62bcd` passed Quality [45135417588](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45135417588) and Chromium [45135417537](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45135417537).
- Quality: Python 453 passed + 70 subtests; all Node web checks and Vite production build passed.
- Chromium: 33/33 passed, including actual worker execution and worker-asset failure fallback.
- The worker bundle was 136.40 kB. This is a bundle-size observation, not a throughput benchmark.
- The PR remains unmerged, so no GitHub Pages deployment or post-deploy smoke is claimed.
- Worker integration is DONE_VERIFIED. Full Python↔JS semantic parity and OOV/tokenizer integration remain TODO; third-party asset rights remain BLOCKED; expert IPA gold is deferred for beta and remains a blocker to accuracy claims.


### Engine/UI module separation — 2026-11-23

The deterministic engine has been extracted into `src/khmer-engine-core.js`. The UI entry point `src/main.js` now imports only the functions it needs, while the Worker imports the core directly and no longer bundles the DOM-rendering entry point. Runtime, register-shifter and structural tests now import the core module; static source guards inspect both core and UI where appropriate. The core retains the existing deterministic rules and local romanization-derived fallback dependency; this is modularization, not a new phonology model.


## Isolated core and final verification

The worker now imports `src/khmer-engine-core.js` directly; the DOM entry point `src/main.js` imports the core for UI rendering. This avoids bundling the UI entry point into the Worker. Exact code head `9fd26941efb7e4936d921d700ee5215569449bda` passed Quality [45136120659](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45136120659) and Chromium [45136120671](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45136120671): 453 Python tests + 70 subtests, Node checks, Vite build, and 33 Chromium tests including Worker execution and failure fallback. Worker bundle reduced from 136.40 kB to 124.02 kB; this is not a throughput benchmark. The PR is unmerged; no Pages deployment is claimed.


## Final code-head verification — 2026-11-23

- Exact code head: `c2dc56949ee519dfcdb13139e49002b92a3fa5bc`.
- Quality [45136544361](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45136544361): 453 Python tests + 70 subtests; Node checks, worker contract and Vite build all passed.
- Chromium [45136544247](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45136544247): 34/34 passed; worker execution, worker asset failure fallback and delayed stale-response race all passed.


## Final branch/PR reconciliation

- The code implementation is on `feat/khmer-native-worker-engine-20261123`; branch tip `994d9dd07adb8f66c5662540f51105cb4f3c0295` passed Quality [45136761275](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45136761275) and Chromium [45136761235](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45136761235): 453 Python tests + 70 subtests and 34 Chromium tests, including Worker/fallback/stale-response cases.
- PR #520 is open and unmerged; therefore no Pages deployment is claimed.
- PR #519 was inspected and left untouched: it adds optional Python hybrid diagnostics, modifies overlapping UI/docs/test files, and is not the browser-native model port. Sequence/reconcile the overlapping files before merging either PR; do not merge blindly.


## Cross-runtime tokenizer parity and trie benchmark — 2026-11-23

- Corrected the browser boundary detector to mirror Python `_starts_new_orthographic_syllable()`: a consonant following a subscript independent-vowel sequence (Unicode 18 §16 example `ផ្ឯម`) remains in the same orthographic unit.
- Added shared data `data/tests/tokenizer-parity.json`; Python `tests/test_parser.py` and browser `tests/web-engine.test.mjs` consume the same expected cases for Unicode 18 subscript-vowel+coda, explicit consonant boundaries, Khmer/Latin isolation, numerals, punctuation/whitespace and ZWSP. Added a 4,096-code-point losslessness regression.
- Replaced repeated `chars.slice(index).join("")` + sorted fixture-key scans with a prebuilt deterministic trie. The trie records the longest lexical fixture whose next code point is a separator; fixture matching remains boundary-aware and does not cross COENG.
- Added `benchmarks/browser-tokenizer.mjs`, `npm run bench:tokenizer`, and a CI benchmark step. On GitHub Actions Node 24, an 8,000-code-point repeated Khmer-consonant stress input produced identical output in both implementations: pre-trie median 352.89 ms; trie median 4.54 ms; observed 77.7× speedup (about 1.76 million code points/s). This is a synthetic tokenizer stress benchmark, not a real-world end-to-end G2P or IPA inference speed claim.
- Exact code head: `abed3d7a4d0b3c3a9e94fa48a4e50b2819194d85`. Quality [45143908134](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45143908134): 454 Python tests + 70 subtests; Node checks, benchmark and Vite build passed. Chromium [45143908115](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45143908115): 34/34 passed.
- **Task ledger:** shared tokenizer boundary cases = DONE_VERIFIED; trie-based fixture lookup = DONE_VERIFIED; synthetic tokenizer benchmark = DONE_VERIFIED; full Python↔JS structural/phonological semantic parity = TODO; lexical word segmentation/OOV inference = TODO; external model/data redistribution rights = BLOCKED.
- Earlier commits `c1f70ef` and `72c09e5` exposed stale source guards that still expected the pre-trie implementation. The guards were updated to assert trie behavior; these intermediate failures are not current-head failures. The exact final head above is green.


## Python rule-engine parity correction — 2026-11-23

- A shared Unicode 18 boundary case exposed a second cross-runtime defect: Python `RuleBasedKhmerEngine` could derive a series-based inherent vowel when a unit contained a subscript independent vowel. The browser implementation already withheld that derivation because the structure was incomplete.
- Updated Python's inherent-vowel gate to require no `subscript_independent_vowels`; added paired Python and browser regressions for `ផ្ឯម`. Both now preserve the single orthographic unit and withhold canonical IPA rather than guessing an inherent vowel.
- Exact code head `224ad5e6530596912a69b334fe98ea7329330f96` passed Quality [45144332414](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45144332414): 455 Python tests + 70 subtests, Node checks, tokenizer benchmark and Vite build. Chromium [45144332627](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45144332627): 34/34 passed.
- On the same exact head, the 8,000-code-point tokenizer stress benchmark measured 2.96 ms median for trie vs 223.12 ms for the pre-trie reference (75.3×); about 2.70 million code points/s. Synthetic stress input only; not a full G2P benchmark.
- Full Python↔JavaScript structural/phonological parity remains PARTIAL: this specific gate is now aligned, but broad shared per-unit structural and IPA fixtures remain outstanding.


## Executable Python↔JavaScript structural parity harness — 2026-11-23

- Added shared inputs `data/tests/structural-parity.json`, Python reference exporter `scripts/export_structural_parity.py`, Node comparator `tests/cross-runtime-structural-parity.mjs`, `npm run test:parity`, and a required CI step after Python dependencies and Node setup.
- The harness compares token boundaries plus base consonant, register, subscript consonants, subscript independent vowels, dependent vowel signs, independent-vowel field, structural status and onset IPA across eight representative inputs: bare consonant, both register shifters, subscript cluster, dependent vowel, Unicode 18 subscript-independent-vowel+coda, multiple shifters and malformed COENG.
- The first differential run exposed a real JS trace bug: malformed COENG returned INVALID but discarded the already recognized base consonant. The browser parser now preserves that base and the malformed tail in its structural trace, matching Python's fail-closed behavior.
- Exact head `c0df000e179d6da16c05c78960ede774966bdcf7`: Quality [45145033315](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45145033315) passed 455 Python tests + 70 subtests, Node checks, the new 8-case cross-runtime parity test, tokenizer benchmark and Vite build. Chromium [45145043709](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45145043709) passed 34/34.
- Same-head tokenizer stress benchmark: 8,000 code points; trie median 6.52 ms, pre-trie median 459.43 ms, 70.4×; about 1.23 million code points/s. CI-host variance is visible across runs; use this as a synthetic comparative stress result, not a universal speed guarantee.
- **Task ledger:** eight-case cross-runtime structural parity = DONE_VERIFIED; malformed-COENG trace preservation = DONE_VERIFIED; complete Python↔JS structural/phonological parity = PARTIAL; broader fixture coverage and all independent-vowel structural forms remain TODO.
