# Master execution plan and chat handoff — 2026-11-25

## Current continuation: NCKL Khmer-script respelling benchmark integration — 2026-11-25

- Integration branch: `integrate/nckl-respelling-benchmark-20261125`, based on the post-#572 `main` commit `747e9388e0d68b16f2cc29113b9fdea648d2d7b2`; source PR [#573](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/pull/573) was non-mergeable after #572 because both branches changed the master handoff and linguistic completion register. The seven-file change is being ported without overwriting the #572 updates.
- PR [#572](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/pull/572) is merged as `747e9388e0d68b16f2cc29113b9fdea648d2d7b2`. Its exact-head Quality, Chromium, khPOS, pinned Rust and shared IPA benchmark workflows passed.
- NCKL benchmark files: `scripts/benchmark_nckl_respelling.py`, `tests/test_benchmark_nckl_respelling.py`, `.github/workflows/optional-nckl-respelling-benchmark.yml`, and `docs/research/NCKL-RESPelling-BENCHMARK-2026-11-25.md`. Dataset and model revisions are pinned; inference uses MIT-licensed `khmer-g2p==0.1.0`; CI retains aggregate metrics only.
- Verified NCKL test results: 1,888 unique words, 100% output coverage, 83.16% exact match, 4.16% code-point CER, 93.06% syllable-count accuracy. This is Khmer-script respelling, not IPA; it does not measure or improve IPA accuracy.
- Rights gate remains BLOCKED for commercial use and redistribution pending direct NCKL terms clarification. No dataset rows, source words, references, predictions or per-word errors are committed or retained in CI artifacts.
- Public static service: existing Pages workflow builds/tests the site and deploys on pushes to `main`; deployment after this integration must be verified by its Actions run and live smoke step. No backend or live neural inference is added.
- Linguistic limits remain: independent adjudicated IPA gold = 0; pronunciation accuracy = NOT_ASSESSED; broad contextual Khmer phonology = PARTIAL; production neural inference = separately deferred pending rights, profile, privacy and runtime decisions.

---


## Current continuation: contextual romanization-mediated IPA — 2026-11-25

- Owner approved `docs/superpowers/specs/2026-11-25-romanization-mediated-ipa-design.md`; implementation plan: [2026-11-25-romanization-mediated-ipa.md](superpowers/plans/2026-11-25-romanization-mediated-ipa.md).
- Base main: `e972cd503f3670d08a2fbf0812efdc701513a810`.
- Working branch: `feat/romanization-mediated-ipa-20261125`; PR [#572](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/pull/572), merged by squash as `747e9388e0d68b16f2cc29113b9fdea648d2d7b2`.
- Latest branch head: `f471e3a16a84e248f954ebcf720ccbdbc5cb4016`.
- Implemented: `data/khmer/romanization_ipa_onsets.json` (source-registered PCGN onset classes plus six exact series/vowel exemplars); official source ID `bgn-pcgn-khmer-1972`; JS adapter `src/khmer-romanization-ipa.js`; Python adapter `src/khmer_ua/romanization_ipa.py`; UI in `src/main.js` displays provisional IPA candidate/status. Orthographic romanization remains separate and explicitly labelled “не вимова”.
- Behavior: longest leading PCGN token is cross-checked against original Khmer base consonant and registered onset IPA. Six exact vowel fixtures require both full Khmer spelling and ASCII romanization: `ក`→`ka`→`kɑː`; `គ`→`ko`→`kɔː`; `កី`→`kei`→`kəj`; `គី`→`ki`→`kiː`; `កា`→`ka`→`kaː`; `គា`→`kea`→`kiə`. The `ka` collision is disambiguated by retaining source spelling. BA b/p abstains. Every candidate remains PROVISIONAL and uses the existing IPA-only Ukrainian target adapter.
- Further evidence gate: the 54 R12a reference-mapping observations in `data/khmer/vowel-context-register.json` are all explicitly `runtime_eligible=false` / `SPECIALIST_REFERENCE_MAPPING_NOT_LEXICAL_TOKEN`. They are not promoted to executable rules. Added 26 negative regression contexts for observed PCGN vowel spellings and two wrong source/romanization pairs; they remain onset-only with unknown vowel tails.
- Explicit limit: general dependent vowels, codas, coeng/syllable-position rules, tone, stress and dialect detail remain PARTIAL / evidence-limited. No canonical IPA or pronunciation-accuracy claim changes.
- Tests: `tests/romanization-ipa.test.mjs`, `tests/test_romanization_ipa.py`, `tests/romanization-ipa-parity.test.mjs`, `scripts/export_romanization_ipa_parity.py`, and `tests/browser/site.spec.js`. Cross-runtime parity covers all registered onsets, six exact vowel fixtures, 26 negative vowel contexts and mismatch abstentions.
- Quality [45585936089](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45585936089): SUCCESS — 516 Python tests, 70 subtests, JS checks, structural/lexical/rule/segmentation parity, deterministic benchmarks and Vite build.
- Chromium [45585936078](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45585936078): SUCCESS.
- External khPOS [45585936092](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45585936092), shared Khmer IPA benchmark [45585936171](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45585936171), and pinned upstream Rust comparison [45585936083](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45585936083): SUCCESS.
- Local tests were not run because no local clone/runtime was available; GitHub Actions is the verification environment.
- Task ledger: bounded onset + six exact vowel adapter DONE_VERIFIED; browser integration DONE_VERIFIED; general contextual vowel/coda/syllable coverage PARTIAL / evidence-limited; independent expert-adjudicated IPA gold remains 0, deferred for public beta per issue #104, and pronunciation accuracy NOT_ASSESSED. PR #572 remains draft and unmerged pending review.


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


## Final continuation — romanization-mediated IPA fallback (2026-11-25)

**Owner decision:** the approved design is implemented on a dedicated branch. The implementation intentionally remains conservative: direct IPA is still preferred; the romanization mode may derive a typed PROVISIONAL IPA candidate from the original Khmer spelling plus its BGN/PCGN-derived ASCII romanization; every Ukrainian pronunciation output is passed through the existing IPA-only target adapter. The separate orthographic romanization card remains visible and explicitly says it is not pronunciation.

### Implementation and evidence boundary

- Branch: `feat/romanization-mediated-ipa-20261125`
- PR: [#572 — Add conservative romanization-mediated IPA fallback](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/pull/572)
- Exact final head: `20b860c01965ea2ea49cca439c26ab57ef351a8e`
- Base: `main` at `e972cd503f3670d08a2fbf0812efdc701513a810`
- 17 changed files; Python and JavaScript implementations; browser integration; source inventory, parity and negative tests.
- Registered Khmer onset tokens are checked against original Khmer consonants and source IPA. The BA b/p ambiguity abstains.
- Only six exact, source-aligned series/vowel syllable fixtures produce a full provisional IPA candidate, and only when both original Khmer spelling and ASCII romanization match.
- Twenty-six other observed PCGN vowel spellings and two deliberately mismatched fixtures are negative cases: they retain an onset-only PROVISIONAL candidate and an explicit unknown vowel tail. No unsupported vowel is inferred.
- A review of 54 R12a reference mappings found all are `runtime_eligible=false` / `SPECIALIST_REFERENCE_MAPPING_NOT_LEXICAL_TOKEN`; they are not executable lexical rules.
- No candidate is promoted to SUPPORTED or canonical IPA. No neural model, remote service, or new runtime dependency was introduced.

### Exact-head verification

All six GitHub commit checks on the exact head completed successfully:

| Check | Result | Evidence |
|---|---|---|
| Quality / Python + JS + parity + deterministic benchmarks + Vite build | PASS — 516 Python tests and 70 subtests; shared browser-runtime register contract passed | [45586289529](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45586289529) |
| Chromium | PASS — 44 Playwright tests | [45586289504](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45586289504) |
| External khPOS comparison | PASS | [45586289526](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45586289526) |
| Shared IPA engine held-out benchmark | PASS | [45586289507](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45586289507) |
| Pinned upstream Rust comparison | PASS | [45586289555](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45586289555) |
| Additional Quality workflow | PASS | Exact-head check run above |

Local execution was not available in this session; verification was performed by GitHub Actions. No claim of locally run tests is made.

### Current task ledger

| Task | Status | Acceptance / remaining work |
|---|---|---|
| `KHM-ROM-IPA-ADAPTER-001` | DONE_VERIFIED | Bounded source-checked onset inventory, six exact syllable fixtures, explicit abstention and 26 negative vowel cases; Python/JS semantic parity passed. |
| `KHM-ROM-IPA-UI-001` | DONE_VERIFIED | Romanization mode displays the IPA-mediated provisional lane; orthographic romanization remains separate and marked “не вимова”; Chromium 44/44. |
| `KHM-ROM-IPA-CONTEXT-001` | PARTIAL / evidence-limited | General vowel-series × dependent-vowel × coda × coeng/syllable-position rules, register harmony, stress/tone and dialect remain open. Requires profile-compatible lexical/audio evidence and specialist review; do not extrapolate from six fixtures or 54 reference mappings. |
| `KHM-IPA-GOLD-001` | DEFERRED for public beta | Per owner decision in [issue #104](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/issues/104), expert-adjudicated gold remains 0 and accuracy remains NOT_ASSESSED. It is still mandatory before expert-validated or production linguistic claims. Acceptance: versioned IPA convention, two independent annotators, third adjudicator and curator, private blind intake, rights-checked items and 30-item pilot. |
| Pronunciation accuracy | NOT_ASSESSED | No independent gold denominator; engineering/segmentation benchmarks are not pronunciation accuracy. |
| Production model/provider integration | DEFERRED / separately gated | No model or service was added; rights, profile, privacy, runtime and deployment requirements remain separate decisions. |

### PR and release state

- PR #572 was merged by squash as `747e9388e0d68b16f2cc29113b9fdea648d2d7b2`; its exact-head checks passed and it had no review threads.
- PR #519 remains separate and untouched; it is a divergent hybrid-inference proposal and must be reconciled independently.
- PR #572 was merged; Pages deployment is triggered by the subsequent `main` update and must be verified independently. No formal release tag was created.
- Assessment: the romanization-mediated fallback is engineering-verified within its narrow inventory. The repository remains a research-ready partial prototype, not a linguistically validated Khmer G2P product.
