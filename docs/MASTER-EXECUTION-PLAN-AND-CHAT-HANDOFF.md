## Current continuation: NCKL Khmer-script respelling benchmark — 2026-11-25

- Base main: `e972cd503f3670d08a2fbf0812efdc701513a810`.
- Working branch: `bench/nckl-respelling-20261125`; PR not yet opened.
- Added `scripts/benchmark_nckl_respelling.py`, `tests/test_benchmark_nckl_respelling.py`, `.github/workflows/optional-nckl-respelling-benchmark.yml`, and `docs/research/NCKL-RESPelling-BENCHMARK-2026-11-25.md`.
- Dataset pin: `phonsobon/khmer-G2P` revision `2733e664ed4d77dee4cc588a130bb4844c9da767`; model pin: `phonsobon/khmer-g2p` revision `7dbc6c3d1c1f5a9a8763be602fa679f130f20dca`; inference code uses MIT-licensed PyPI `khmer-g2p==0.1.0` with the explicit model revision. No unlicensed upstream GitHub source checkout remains.
- This is a separate **Khmer-script pronunciation-respelling** task, not IPA. The test split has 1,920 pairs / 1,888 unique words. The harness verifies train/validation/test word-disjointness and groups all alternative readings per word.
- Metrics: output coverage, exact match against any NCKL alternative, Unicode code-point CER using the minimum-edit alternative (same policy as the upstream evaluator), and syllable-count accuracy. No source rows, words, references, predictions or per-word errors are retained.
- Rights: dataset card labels content `other / nckl-khmer-dictionary-2022`, states underlying content remains © NCKL, and asks users to check terms before commercial use or redistribution. Only aggregate metrics are uploaded. Commercial use/redistribution remain blocked pending direct NCKL terms clarification.
- TDD RED: Quality [45581925948](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45581925948) failed with 6 expected missing-harness FileNotFoundError failures; 507 existing tests and 70 subtests passed.
- Quality GREEN: [45582195369](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45582195369) SUCCESS — full Python suite, npm checks, structural/lexical/rule/segmentation parity, engine/tokenizer benchmarks and Vite build.
- Initial optional model execution [45582195410](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45582195410) is superseded because it used upstream GitHub code without a standalone LICENSE. Final MIT-package rerun [45582973744](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45582973744) SUCCESS using `khmer-g2p==0.1.0` and the pinned Hub model revision. Aggregate artifact [15006794082](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45582973744/artifacts/15006794082) inspected; ZIP SHA-256 `915727bce6e27d28b2191f116ba6e8dc03fd0004c21d1c53e9b67e8709146f1e`; JSON SHA-256 `3fde5453bb9a739ea55ab4b7510716671898b7c3ddd5fb145410bb7cc7ec27fc`. Final metrics: 1,888 words, 100% coverage, 83.16% exact match, 4.16% CER, 93.06% syllable-count accuracy. Artifact contains aggregate data only.
- Independent IPA gold remains 0; this benchmark does not change IPA accuracy or canonical IPA. Production neural fallback is unchanged and remains blocked by separate profile/rights/runtime gates.

# Master execution plan and chat handoff — 2026-11-25

## Current continuation: shared Khmer IPA engine benchmark — 2026-11-25

- Current default-branch base: `de158a3fd47bc151b6f952b2a89c4e67360174fe` (includes merged PR #569).
- Benchmark branch: `bench/khmer-cross-engine-mekongphon-20261125`.
- PR [#570](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/pull/570) merged by squash as `4d928ae9010967c137f65044770523f8cef49c5a`; current `main` at closeout starts from this commit.
- Initial 100-word benchmark code head: `84830e3e8d2fe0c30e555ddef868ac864915fa52`; final two-source benchmark code/test head: `7a9f081795bcfcc5bc4c0b7d55179828cbe2a898` (subsequent PR commits are documentation/register updates only).
- Initial four-engine 100-word MekongPhon run [45499595763](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45499595763): SUCCESS; aggregate-only artifact [14970916634](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45499595763/artifacts/14970916634).
- Final two-source/four-engine run [45500823688](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45500823688): SUCCESS; aggregate-only artifact [14971017765](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45500823688/artifacts/14971017765). Exact-head Quality [45500823635](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45500823635) and Chromium [45500823563](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45500823563): SUCCESS.
- Exact-head project Quality run [45499595556](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45499595556): SUCCESS (Python, JS/web, parity, engine/tokenizer benchmarks, production build).
- Same 100 MekongPhon inputs: project rules 95% non-empty / 94 partial / 74.61% CER; Khmer Phonemizer 100% / 25.71%; Epitran 100% / 114.73%; MekongPhon neural 100% / 12.54%. On 1,509 IPA-Dict forms filtered against visible MekongPhon train/eval files: project rules 58.38% coverage / 858 partial / 83.41% CER; Khmer Phonemizer 100% / 33.40%; Epitran 100% / 114.50%; MekongPhon neural 100% / 14.52%. Neural exact matches drop from 64% on the small MekongPhon set to 14.45% on IPA-Dict. These are source-attested diagnostics, **not accuracy**; independent adjudicated IPA gold remains 0.
- Full methodology and findings: [KHMER-CROSS-ENGINE-BENCHMARK-2026-11-25.md](research/KHMER-CROSS-ENGINE-BENCHMARK-2026-11-25.md).
- Key interpretation: the deterministic engine's low score is driven by 94 onset-only/partial outputs, not 94 full but wrong canonical pronunciations. It is evidence of insufficient productive vowel/coda coverage and an overly restrictive only-output path. MekongPhon is the strongest fallback candidate on this small sample; profile equivalence and rights remain unresolved.
- NCKL/PhonSobon 38,629-pair pronunciation-respelling corpus is identified as a separate third benchmark source, but its targets are Khmer-script respellings rather than IPA and must be evaluated separately. IPA-Dict's 3,286-row Khmer list is the second IPA source; 1,509 words remained after filtering visible MekongPhon overlaps.
- Benchmark harness, report and updated master/register are merged to `main` in `4d928ae9010967c137f65044770523f8cef49c5a`. The exact source/test head `7a9f081795bcfcc5bc4c0b7d55179828cbe2a898` passed Python/JS quality, browser smoke and both dataset benchmark runs before the final documentation-only commits.
- Production neural fallback remains BLOCKED: the static Pages app has no inference backend and browser CSP blocks network calls. The candidate model has 33.6M float32 parameters and no hosted inference provider; a browser-local quantized build or an explicitly approved backend/privacy design is required. Do not silently add a server, transmit user text or bundle unreviewed weights. Next acceptance gate: profile-matched expert pilot, source/model rights review, and explicit runtime/privacy design.


## Previous task record (historical): Lao engine architecture alignment — 2026-11-24

- Repository: `ClippyFirst/Khmer-Ukrainian-Phonetic-System`.
- Starting `main`: `1b8649c4b874fbf34a66012d7e02aa1da04fb6da`.
- Working branch: `feat/khmer-lao-engine-contract-parity-20261124`.
- PR [#568](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/pull/568) was merged by squash as `50d22708a0bda8d47edfd476ae3ff3ed848d18f6`; PR #569 subsequently added the visible orthographic Ukrainian result and was merged as current base `de158a3fd47bc151b6f952b2a89c4e67360174fe`.
- Reference architecture: `ClippyFirst/Lao-Ukrainian-Phonetic-System`, especially `docs/lao-grapheme-ipa-preview.md`.
- Final source/test head: `f579e1444fbda2b186fdf8a04dc9f52f7ebc044e`. Subsequent commits through `3584ce714202c475f3e8f58cc69fe1f34530f9f0` update documentation, benchmark evidence, replica artifacts and handoff registers only. This final handoff refresh is documentation-only; the source/test head remains unchanged.
- Local clone was unavailable because the container could not resolve `github.com`. Repository edits were made directly on this isolated GitHub branch. No local test pass is claimed.
- The #568 implementation and #569 result-card fix are on main; #569's Chromium verification passed. No formal release tag or external setting change was performed.

### Implemented architecture

1. Added `TypedPhoneticResult` and `PhoneticSegment` without replacing the existing public `PhoneticResult` envelope.
2. Added typed statuses `SUPPORTED`, `UNCERTAIN`, `PROVISIONAL`, `UNRESOLVED`; current Khmer lexical proposals remain `UNCERTAIN`, not promoted to `SUPPORTED`.
3. Added source-independent IPA tokenization preserving segment sequence, syllable boundaries, length marks, tone symbols, certainty, provenance and uncertainty.
4. Added one IPA-only Ukrainian target adapter for complete and provisional phonetic results. It does not read Khmer graphemes or romanization.
5. Provisional onset IPA remains `PROVISIONAL`, carries `phonemic_ipa=null`, and always retains one explicit unknown tail; the adapter maps the known run and returns `???` for the remainder.
6. Valid IPA with no Ukrainian target correspondence remains valid IPA; the target value is withheld instead of guessed.
7. Preserved the separate `ORTHOGRAPHIC_ROMANIZATION_FALLBACK` candidate and the opt-in, non-canonical external-provider contract.
8. Integrated Python engine, JavaScript core, Worker output, CLI, UI unit details and `schemas/phonetic-result.schema.json`.
9. Added replica-skill recon, feature matrix, architecture, test plan, bug log and build log under `replica/`.

### Verification ledger

| Check | State | Evidence |
|---|---|---|
| Test-first RED for typed IPA model | DONE_VERIFIED | Initial PR-head Quality failure was the expected missing-module failure |
| Test-first RED for CLI contract | DONE_VERIFIED | Initial CLI tests failed because CLI still called structural parser only |
| Python suite | DONE_VERIFIED | 503 passed + 70 subtests in exact PR-head Quality run [45491600216](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45491600216) |
| Browser deterministic checks | DONE_VERIFIED | Exact PR-head Quality run [45491600216](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45491600216); web engine, runtime, Worker, typed IPA adapter and CLI tests passed |
| Python/JavaScript parity | DONE_VERIFIED | 129 structural, 38 lexical, 46 consonant/rule and 6 segmentation fixtures passed; typed IPA fields are included in rule-output parity |
| Benchmarks and Vite build | DONE_VERIFIED | Exact PR-head Quality run [45491600216](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45491600216) |
| Exact-head Chromium smoke | DONE_VERIFIED | [45491600082](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45491600082) passed 42/42 Playwright tests, including typed IPA detail disclosure |
| Exact-head pinned Rust comparison | DONE_VERIFIED | [45491600143](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45491600143) passed |
| External khPOS comparison | DONE_VERIFIED | [45491600273](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45491600273) passed |
| Linguistic accuracy | NOT_ASSESSED | Independent adjudicated IPA gold corpus remains empty |

### Task ledger

| Task | Status | Acceptance boundary |
|---|---|---|
| `KHM-LAO-ENGINE-CONTRACT-001` | DONE_VERIFIED | Typed result model, shared adapter, Python/JS parity, CLI, schema and uncertainty output; no language-rule transfer |
| `KHM-PROVISIONAL-OUTPUT-001` | DONE_VERIFIED on prior main | Existing onset-first primary output and separate orthographic fallback preserved |
| `KHM-PHON-CONTEXT-001` | PARTIAL | Full contextual vowel/coda/series/length matrix remains incomplete |
| `KHM-IPA-GOLD-001` | BLOCKED | Independent gold has 0 entries; two annotators and adjudicator still required |
| Pronunciation accuracy | NOT_ASSESSED | No gold denominator |
| Manual accessibility audit | DEFERRED | Outside this architecture change |

### PR and branch reconciliation

- PR #568 is historical and merged; it is no longer an open continuation branch. Its exact-head automated workflows passed before merge.
- PR #519 remains open and untouched. It is a separate, diverged hybrid-inference change (73 commits ahead / 200 behind, reported non-mergeable); do not merge blindly.
- Historical branches were not deleted or rewritten.
- No public deployment or formal release was requested or performed.

---

## Prior task record — provisional output and benchmark (historical)

- Repository: `ClippyFirst/Khmer-Ukrainian-Phonetic-System`
- Starting `main` for the provisional-output task: `422023d03283648bea9ca59ef0ea01caedf41698`.
- Final `main`: `fff886dfaca8979387dc6cacbd7417a89020a407`.
- Implementation branch: `feat/khmer-provisional-output-benchmarks-20261124`.
- [PR #566](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/pull/566) merged by squash; final merge commit above.
- Hosting: [GitHub Pages public service](https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System/).
- Methodology: [system page](https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System/system.html).
- No formal release tag was created.

## User-requested outcome: non-blocking output

The primary browser output no longer needs to suppress all useful material when full canonical IPA is unavailable.

1. If the source registry supports the onset, display an onset-only IPA-derived Ukrainian hint followed by `???`.
2. If no onset IPA hint is available but a BGN/PCGN-derived orthographic candidate exists, display that candidate followed by `???`, explicitly typed as `ORTHOGRAPHIC_ROMANIZATION_FALLBACK`.
3. If neither candidate exists, display `???`.

The browser visibly distinguishes `IPA_DERIVED_PARTIAL` from `ORTHOGRAPHIC_ROMANIZATION_FALLBACK`; the latter is explicitly **not IPA and not a pronunciation claim**. `display_status=PROVISIONAL` is separate from canonical `status`, `canonical_ipa`, and `canonical_ua`. The separate romanization mode remains separate. Unknown material is not silently deleted or guessed.

The Python reference engine preserves source-registered onset-only previews on withheld lexical fixtures and marks these as partial. It does not turn an orthographic fallback into IPA. Python/JavaScript parity tests cover shared onset fallback fixtures.

## Verified engineering benchmark

Quality run [45474564623](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45474564623), PR code head `ccb40414d85fde0a0d9b7c6ef9de285f9f7d5f2a):

| Measure | JavaScript core | Python engine |
|---|---:|---:|
| Runtime | Node v24.22.3 | Python 3.12.16 |
| Unique NFC inputs | 39 | 39 |
| Warm-up / measured batches | 5 / 25 | 5 / 25 |
| Median batch latency | 1.3028 ms | 5.2737 ms |
| Throughput | 29,934.7 inputs/s | 7,395.16 inputs/s |
| Complete / partial / unresolved | 37 / 2 / 0 | 37 / 2 / 0 |

Observed Node/Python ratio: 4.05× in this CI environment. This is not a browser-device latency guarantee or a pronunciation-accuracy score.

Tokenizer stress: 8,000 code points, 61,980 dictionary entries, 7.65 ms median, 1,046,065 code points/s, source preservation PASS. The external khPOS and pinned upstream Rust comparisons passed. These assess segmentation only.

Full benchmark and limitations: [KHMER-ENGINE-BENCHMARK-2026-11-24.md](research/KHMER-ENGINE-BENCHMARK-2026-11-24.md).

## Exact final-main verification

All workflows below completed successfully on final main commit `fff886dfaca8979387dc6cacbd7417a89020a407`:

- [Quality checks — 45474856164](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45474856164): Python suite, web checks, structural/lexical/consonant/segmentation parity, engine benchmark, tokenizer benchmark and production build.
- [Chromium browser smoke — 45474855979](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45474855979): PASS.
- [External khPOS segmentation benchmark — 45474855939](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45474855939): PASS.
- [Pinned upstream Rust comparison — 45474856176](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45474856176): PASS.
- [GitHub Pages deployment and live smoke test — 45474855848](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45474855848): PASS. The workflow fetched the deployed home page, methodology page, JavaScript and CSS assets successfully and exercised the production site in Chromium.

Local tests were not run in this session because the local clone/network route was unavailable; GitHub Actions executed the listed checks.

## Task ledger

| Task | Status | Boundary |
|---|---|---|
| `KHM-PROVISIONAL-OUTPUT-001` | DONE_VERIFIED | Main browser UI exposes onset-first partial output, then typed orthographic fallback, then `???`; Chromium passed |
| `KHM-ENGINE-BENCHMARK-001` | DONE_VERIFIED | Shared 39-input Python/Node benchmark, runtime versions, throughput and output coverage recorded |
| Tokenizer stress benchmark | DONE_VERIFIED | 8,000-code-point stress case; source preserved |
| External segmentation comparisons | DONE_VERIFIED | khPOS and pinned upstream Rust comparisons passed |
| `KHM-PHON-CONTEXT-001` | PARTIAL | Full profile × consonant series × vowel × coda × syllable type × length × tone/stress coverage is not established |
| `KHM-IPA-GOLD-001` | BLOCKED | Independent adjudicated IPA gold corpus has 0 entries; issue #104 requires two annotators and an adjudicator |
| Pronunciation accuracy | NOT_ASSESSED | No gold denominator exists; benchmark coverage is not accuracy |
| Manual accessibility audit | DEFERRED | Retained as previously scoped |

## PR and branch reconciliation

- PR #566 was reviewed against current main, had no merge conflicts or review-blocking comments, passed all four PR-head workflows, and was squash-merged.
- PR #519 remains open and untouched. It is a separate hybrid-inference change, currently diverged and reported non-mergeable; do not merge blindly. Reconcile its diff against current main before any future reuse.
- Historical branches were not deleted or rewritten.
- No formal release was created.

## Next genuine research blockers

1. Build a profile-compatible lexical/audio cross-product across consonant series, vowels, codas, syllable shape, length and tone/prosody.
2. Curate independent IPA gold with two annotators and a third adjudicator under issue #104; only then measure held-out pronunciation accuracy.
3. Continue specialist review of the provisional phonological rules and Ukrainian adaptation. Never promote romanization candidates to IPA or infer unsupported vowel/coda/tone values.

**Release assessment:** public beta is deployed and the engineering path is verified. This remains a research-ready partial prototype, not a linguistically validated G2P product.


### Final exact-head verification update — 2026-11-24 21:34 UTC

The pinned upstream Rust comparison has now completed successfully on the final PR head `3ecbbbdbe4ffefbb02c0c7e7c55fd017c2ee8443`.

| Required check | Final exact-head result |
|---|---|
| Quality / Python | PASS — 503 tests + 70 subtests |
| Browser / Chromium | PASS |
| External khPOS benchmark | PASS |
| Pinned upstream Rust comparison | PASS |
| GitHub commit check-runs | 5/5 successful |
| PR mergeability | mergeable=true |
| PR review threads | 0 |
| PR state | OPEN, non-draft; not merged |
| Main branch | unchanged at `1b8649c4b874fbf34a66012d7e02aa1da04fb6da` |

Exact workflow runs:
- [Quality checks](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45492207753)
- [Browser smoke](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45492207565)
- [External khPOS benchmark](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45492207569)
- [Pinned upstream Rust comparison](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45492207566)

The external benchmark pins upstream `Alujack/khmer-tokenizer` at `f38eae5924d4e41a46fd2204cf6951cdb0dc8908`, uses its 61,980-entry dictionary, and scores 1,000 corpus sentences / 10,778 gold tokens. The corpus is CC BY-NC-SA 4.0 and was downloaded temporarily by CI; it was not copied into the repository. The benchmark evaluates tokenization/segmentation, not phonetic transcription. Therefore it is valid external segmentation evidence but must not be cited as Khmer IPA accuracy.

The PR now meets its engineering acceptance criteria. It remains unmerged because no explicit merge instruction was given. The only remaining work for this branch is owner review/merge; linguistic research tasks remain as previously recorded (independent IPA gold = 0; pronunciation accuracy NOT_ASSESSED; full contextual phonology PARTIAL).
