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
| 129-case Python↔JavaScript structural parity inventory | DONE_VERIFIED | CI compares token boundaries and core structural fields across all consonants, independent vowels, vowel signs, subscript inventory, eligible shifters and adversarial forms |
| 36-fixture Python↔JavaScript lexical IPA/UA parity | DONE_VERIFIED | CI compares per-unit source, canonical IPA, Ukrainian adaptation, status and mapping agreement for every browser lexical fixture |
| Full Python↔JavaScript structural/rule semantic parity | PARTIAL | 129 structural inventory cases and 36 lexical fixtures now pass; full output contract, all contextual rules and open vocabulary remain outstanding |
| Python↔JavaScript lexical fixture IPA/UA/status parity | DONE_VERIFIED | Exact-head CI compares all 36 shared lexicon fixtures, including mapping agreement |
| Deterministic orthographic token boundaries and fixture matching | DONE_VERIFIED | Shared cross-runtime boundary fixtures and trie-based longest fixture matching; synthetic 8k stress benchmark 77.7× vs pre-trie implementation |
| General lexical word segmentation/OOV model | TODO | Evaluate and pin lexical tokenizer/model only after exact asset rights and phonological parity are established |
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


## Independent-vowel structural parity — 2026-11-23

- Extended the executable parity fixture set from eight to nine cases with a standalone Khmer independent vowel. The browser parser now records it as an established orthographic base with no consonant register/onset, matching Python's structural representation; no pronunciation is invented.
- Exact head `8a2d86a85436ddec149cd55a7d1909ac0b2c7cc0`: Quality [45145337895](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45145337895) and [45145346826](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45145346826) passed: 455 Python tests + 70 subtests, Node checks, 9-case Python↔JS structural parity, tokenizer benchmark and Vite build. Chromium [45145346888](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45145346888): 34/34 passed.
- Tokenizer stress benchmark on this head: 8,000 code points; 6.26 ms trie median vs 466.00 ms pre-trie median, 74.4× in this synthetic test. This remains a tokenizer-only comparison, not a full phonology/G2P benchmark.
- Current parity scope is still deliberately bounded: nine representative cases, not complete Unicode inventory or full end-to-end Python/JS result equality.


## Structural parity inventory expansion — 2026-11-23

- Expanded the shared Python↔JavaScript structural corpus from 9 hand-picked inputs to **129 cases** generated from the repository's actual Khmer data inventory: all 33 consonants, all 15 independent vowels, dependent/composite/vowel-modifier signs attached to a base, every subscript consonant, every subscript independent vowel, and all eligible muusikatoan/triisap combinations, plus malformed/adversarial cases.
- Exact code head `a389530b5ffa8799b6194c939a00bce9309110e2`: Quality [45145785462](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45145785462) passed 455 Python tests + 70 subtests, Node checks, 129-case structural parity, tokenizer benchmark and Vite build. Chromium [45145796671](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45145796671) passed 34/34.
- Same-head synthetic tokenizer stress: 8,000 code points; trie median 8.19 ms, pre-trie median 490.16 ms, 59.9×. The absolute timing varies with CI host load; the repeated-run comparison is not a general end-to-end G2P performance guarantee.
- **Task ledger:** inventory-derived 129-case structural parity = DONE_VERIFIED; complete phonological rules and end-to-end Python/JS result parity = PARTIAL; tokenizer lexical/OOV word segmentation = TODO.


## Final continuation checkpoint — 2026-11-23

- Current branch tip after canonical documentation updates: `f79126ae78ebcd4d5e70324c0c43736f622885b7`.
- Exact-tip Quality [45146037172](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45146037172) passed: 455 Python tests + 70 subtests, all Node checks, 129-case Python↔JS structural parity, tokenizer benchmark and Vite production build.
- The last code-bearing head is `a389530b5ffa8799b6194c939a00bce9309110e2`; its Chromium run [45145796671](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45145796671) passed 34/34. Subsequent commits to `f79126a` were documentation-only. A newer doc-head browser workflow was still running at checkpoint and is not counted as passed.
- Exact-tip tokenizer stress benchmark: 8,000 code points; trie median 2.69 ms, pre-trie median 242.72 ms, 90.3× on GitHub Actions Node 24. Synthetic tokenizer-only benchmark; not end-to-end G2P.
- PR [#520](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/pull/520) remains open and mergeable. PR #519 remains untouched and open due overlapping UI/docs/test files; reconcile before merging either. No merge, Pages deployment, or release was performed.
- **Task ledger:** Worker execution/fallback/race = DONE_VERIFIED; tokenizer parity cases = DONE_VERIFIED; 129-case structural parity = DONE_VERIFIED; trie optimization and benchmark = DONE_VERIFIED; full contextual phonology and end-to-end result parity = PARTIAL; lexical/OOV word segmentation = TODO; external assets rights = BLOCKED; expert IPA gold = DEFERRED for beta / BLOCKED for accuracy claims.


## Latest exact-head confirmation — 2026-11-23

- Latest branch tip at this checkpoint: `aace766c21476019952f1aa93f217396387de420`.
- Quality [45146465545](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45146465545): 455 Python tests + 70 subtests, Node checks, 129-case Python↔JS structural parity, tokenizer benchmark and Vite build passed.
- Chromium [45146465516](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45146465516): 34/34 passed. The worker bundle in this build is 124.63 kB.
- Same-head synthetic tokenizer stress benchmark: 8,000 code points; trie median 3.07 ms vs pre-trie 298.09 ms, 97.0×, about 2.60 million code points/s. This benchmark measures fixture lookup/orthographic tokenization only, not end-to-end G2P.
- The PR remains open for review; no merge, Pages deployment or release is claimed.


## Lexical IPA/UA parity across the full browser fixture set — 2026-11-23

- Added `scripts/export_lexical_parity.py`, `tests/cross-runtime-lexical-parity.mjs`, `npm run test:lexical-parity`, and a CI step comparing Python `RuleBasedKhmerEngine` with browser `convert()` for every row in `data/tests/web-fixtures.json`.
- All **36 lexical fixtures** now match across runtimes for source-unit alignment, canonical IPA (normalized only for the browser's slash display), Ukrainian adaptation, status and lexical-mapping agreement. A fixture without an IPA remains withheld in both paths; no value is synthesized.
- Exact code head `e584d986a7d7fe9ac177709374c29bd4298e93f2`: Quality [45147094378](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45147094378) passed 455 Python tests + 70 subtests, Node checks, 129-case structural parity, 36-fixture IPA/UA parity, tokenizer benchmark and Vite build. Chromium [45147094466](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45147094466) passed 34/34.
- Same-head 8,000-code-point tokenizer stress: trie median 3.23 ms, pre-trie 357.92 ms, 110.8×. Synthetic tokenizer-only comparison; no general G2P latency guarantee.
- **Task ledger:** 129-case structural parity = DONE_VERIFIED; 36-fixture IPA/UA/status parity = DONE_VERIFIED; complete contextual phonology and full result-schema parity = PARTIAL; lexical word segmentation/OOV inference = TODO.


## Lexical fixture parity extension — 2026-11-23

- Added an executable Python↔JavaScript lexical parity gate: Python `RuleBasedKhmerEngine` exports every entry from the shared browser lexicon fixture set, and Node compares browser-engine per-unit source, IPA, Ukrainian adaptation, status and lexical-mapping agreement.
- Coverage: **36/36 lexical fixtures** from `data/tests/web-fixtures.json`, including the negative multi-register-shifter entry and phrase-level examples. This is fixture parity, not proof of full Python/JS semantic equivalence or open-vocabulary G2P.
- Exact code head `e584d986a7d7fe9ac177709374c29bd4298e93f2`: Quality [45147094378](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45147094378) passed 455 Python tests + 70 subtests, Node checks, 129-case structural parity, 36-fixture lexical parity, tokenizer benchmark and Vite build. Browser [45147094466](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45147094466) passed 34/34, including local Worker, failed-asset fallback and stale-response race.
- Same-head synthetic 8,000-code-point tokenizer stress: trie median 3.23 ms vs pre-trie 357.92 ms, 110.8× on the CI runner. Tokenizer-only synthetic measurement, not an end-to-end Khmer phonemizer benchmark.
- **Task ledger:** lexical fixture IPA/UA/status parity = DONE_VERIFIED; full Python↔JS rule/result parity = PARTIAL; general lexical word segmentation/OOV remains TODO.


## Final exact-head lexical parity checkpoint — 2026-11-23

- Current branch tip before this note: `9a8ba02f65e0502555c0df8045e930ddcaca3a3d`.
- Exact-head Quality [45147375553](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45147375553): 455 Python tests + 70 subtests; Node checks; 129-case structural parity; 36-fixture lexical IPA/UA/status parity; tokenizer benchmark; Vite production build — PASS.
- Exact-head Chromium [45147375800](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45147375800): 34/34 passed.
- Tokenizer stress on this run: 8,000 code points; trie median 6.19 ms vs pre-trie 473.60 ms, 76.5×. CI-host variance means this is comparative synthetic evidence only.
- Full contextual phonology and complete result-schema parity remain PARTIAL; lexical word segmentation/OOV remains TODO; third-party model/corpus redistribution remains BLOCKED pending rights review.
