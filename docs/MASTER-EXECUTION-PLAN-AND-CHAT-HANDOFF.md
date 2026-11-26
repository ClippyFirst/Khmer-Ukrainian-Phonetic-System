## Current continuation: deterministic neural-distilled Khmer IPA engine — 2026-11-25

**Current integration branch:** `feat/deterministic-neural-distillation-20261125`  
**Draft PR:** [#582](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/pull/582)  
**Base:** current `main` at `8838a1f33b03aa1bad7c045c216305bb3e60e3f9`  
**Branch head at this documentation update:** `9bec26c75ac82380ac6c45680a446afc71131eb4`  
**Default branch remains unchanged. No merge or deployment has been performed.**

### Decision and runtime architecture

The production goal is a **local deterministic engine developed from an offline neural teacher**, not a neural model running in every visitor's browser.

1. The source lexicon is pinned to Google `language-resources` revision `a90601024f07ab7e96c911243324e0adeb16da96`. It contains 62,179 Khmer rows: 62,118 non-empty phonemic transcriptions, 61 empty rows, 62,114 unique spellings and four multi-pronunciation spellings.
2. The pinned Google Festvox inventory defines 56 phones; all 54 tokens observed in non-empty lexical rows occur in that inventory. The phone inventory is not an IPA conversion table.
3. The dedicated `GOOGLE_PHONEMIC → typed IPA` adapter preserves syllable boundaries and length, tracks token mapping status and fails closed on unknown/non-lexical tokens. The six R12A screening cases match; the separate source-attested lexical diagnostic has 3/7 exact matches and four explicit conflicts. Neither result is a gold accuracy score.
4. A project-owned neural teacher is trained offline with a word-disjoint split and atomic phone-token targets. On the held-out Google source-label split it achieved 84.18% exact word match, 4.33% phone-token error rate and 100% source-label coverage. These metrics measure reproduction of Google labels, not independent contemporary Phnom Penh pronunciation accuracy.
5. Distillation produced 2,532 deterministic OOV syllable candidates. The held-out composition diagnostic achieved 63.86% exact match, 14.19% token error rate and 98.4% candidate coverage. These are teacher/student source-label diagnostics, not IPA accuracy.
6. The Pages build regenerates the distilled static JSON. The browser loads only that same-origin data table in Super-soft mode; it does not download model weights, run ONNX Runtime or send Khmer text to a server. If the Worker cannot start, the local fallback uses the same static table.
7. The previous standalone MekongPhon model panel and ONNX/WASM deployment have been removed from the proposed public UI/build. Its merged research implementation and archived outputs remain available for comparison, not as primary production output.

### Actual output-tier contract

- **Strict:** only source-located tier-B proposals; no unadjudicated Google lexical hits, onset-only previews, archived provider snapshots or neural-distilled OOV candidates.
- **Soft:** adds exact Google phonemic lexical candidates and partial onset IPA hints, all typed and marked `PROVISIONAL`.
- **Super-soft:** adds static neural-distilled OOV syllable candidates. It returns a non-empty display for every linguistic input unit by using explicit unresolved markers where no candidate exists. This is **100% non-empty display coverage**, not 100% full IPA coverage.
- BGN/PCGN orthographic fallback remains in a separate panel and is never used as the Ukrainian output of the IPA pipeline.
- Archived Khmer Phonemizer/MekongPhon/Epitran outputs are diagnostic-only and cannot replace the local deterministic engine's output.

### Task ledger

| Task | Status | Evidence / acceptance condition |
|---|---|---|
| Pin Google source TSV and phonology inventory with attribution | DONE_VERIFIED | Source revision, hashes, CC BY 4.0, 62,118 non-empty rows and 54/56 inventory coverage validated |
| Implement typed Google phonemic → IPA adapters in Python and JS | DONE_VERIFIED / pending exact-head rerun | Dedicated token map and parser; 6/6 R12A screening matches; unknown tokens fail closed; lexical conflicts retained |
| Generate and integrate 62,118-row static lexical shards | DONE_VERIFIED / pending exact-head rerun | Eight deterministic shards, 61 blank rows preserved, four ambiguous spellings retained, schema and parity tests |
| Train project-owned neural teacher | DONE_VERIFIED | Exact CI teacher job and saved artifact from run [45653367069](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45653367069); 84.18% exact, 4.33% PER, 100% source-label coverage |
| Distill teacher into OOV syllable candidates | DONE_VERIFIED as research artifact | Same run artifact inspected: 2,532 candidates, 63.86% exact, 14.19% PER, 98.4% composition coverage |
| Integrate Strict / Soft / Super-soft into browser output | PARTIAL | Engine, Worker, UI and regression tests changed; exact-head Quality/Chromium still required |
| Generate and publish static table in Pages build | PARTIAL | Workflow now caches offline teacher checkpoint and stages only distilled JSON; Pages deployment not yet run |
| Remove standalone model inference from production UI | PARTIAL | UI, CSP, Pages workflow and tests updated; exact-head checks pending |
| Independent IPA accuracy and profile equivalence | BLOCKED | Independent adjudicated IPA gold count remains 0; Google phonemic labels do not establish target-profile equivalence |
| Broader OOV/contextual phonology beyond the distilled syllable inventory | PARTIAL / evidence-limited | 2,532 candidates do not cover every Khmer syllable/context; no guessing or promotion from teacher agreement alone |

### Verification state and open blockers

- Previous teacher/distillation CI run [45653367069](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45653367069) completed successfully and its aggregate metrics/artifact were inspected.
- The code head `5007b8d0f6d28dac4f93aab8b3066f5ac24f1e43` triggered Quality run [45663895838](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45663895838), but GitHub Actions still reports it queued. The latest commits after that code head update documentation only; rerun exact-head checks if needed.
- Browser, pinned Rust, khPOS and shared held-out benchmark runs from this continuation were also queued at last inspection. Do not claim they passed until their exact run conclusions are available.
- Pages workflow has not run on this branch because deployment is triggered from `main`. The draft PR must be reviewed and merged before a production deployment can verify the staged static table.
- Open PR #519 is an older dual-transcription UI branch based on stale base `fe870f1b6d138d39bc271362cdda4165c1e3517e`; it is not reused or modified here. PR #578's MekongPhon browser port is already merged on main, but its standalone model UI/runtime is intentionally removed by this proposed continuation.
- No independent gold, pronunciation accuracy, or 100% full-IPA coverage is claimed.

---

## Browser-local MekongPhon port — 2026-11-25

- User requirement: the IPA-producing neural engine must execute on the public site, not only through a Python/provider integration. Branch: feat/browser-local-mekongphon-ipa-20261125; PR #578.
- Implemented a user-triggered, lazy browser-local model path: Khmer input → pinned ByteLevel BPE tokenizer → ONNX encoder/decoder → provisional IPA → existing typed IPA parser → Ukrainian practical adapter. Raw IPA is rendered before target mapping, so adapter limitations cannot hide the model candidate.
- Upstream model artifact: byumatrixlab/khmer-ipa at immutable revision 20e069d384b240da76320e1569958568c12a54bc; model card declares Apache-2.0. The training corpus is not redistributed; corpus rights remain unresolved.
- Export: FP32 encoder/decoder graphs are validation-only and removed before packaging; dynamically quantized INT8 pair is deployed (~35 MB). ONNX Runtime Web 1.23.2 (MIT) is integrity-pinned and vendored; WASM executes in a dedicated Web Worker. One-beam greedy decode, max output length 64 tokens, to keep browser latency bounded.
- Privacy: no inference backend, telemetry or external model API. Only same-origin static model/runtime assets are fetched after explicit click; the Khmer input is passed to a local worker and never sent over the network. CSP permits connect-src 'self' and wasm-unsafe-eval only as required for local assets/WASM.
- Export evidence: FP32 ONNX vs pinned Transformers generation is gated at ≤5% CER on three diagnostic probes; INT8 vs FP32 is gated at ≤5%. For the reported phrase, FP32 ONNX CER is 3.03%; INT8 matches FP32 exactly. These are export parity checks, not pronunciation accuracy.
- Browser tokenizer parity: all pinned encoder/decoder token ID probes match Transformers. Model-enabled production build Chromium: 46/46 Playwright tests passed, including real local inference and no-external-request assertion.
- Model output remains PROVISIONAL, profile match UNVERIFIED, not gold and never overrides canonical deterministic/lexical results. Independent adjudicated IPA gold remains 0; accuracy remains NOT_ASSESSED.
- Model assets are generated in CI and Pages build, not committed to git. The FP32 graphs are deleted before packaging. CI uploads the built model asset from dist/models/mekongphon.
- Remaining blockers: independent expert-adjudicated target-profile IPA gold; rights clarification for upstream training corpus; browser performance/coverage evaluation on longer, diverse inputs. The browser port itself is DONE_VERIFIED once final CI/Pages deployment checks pass.

---
## Final merge and deployment closeout — 2026-11-25

- Implementation PR [#576](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/pull/576) was merged by squash into main as `ecbae0fa6b3a44433c5d787ba0877613caf05834`.
- Final implementation Quality [45610176769](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45610176769): SUCCESS — 524 Python tests + 70 subtests, npm web checks, structural/lexical/rule/segmentation parity, deterministic benchmarks and Vite build.
- Final implementation Chromium [45610176751](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45610176751): SUCCESS — 45/45 Playwright tests.
- Production Pages deployment [45610398273](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45610398273): SUCCESS — production Chromium, deployment and deployed-site/runtime-asset smoke test all passed.
- Public app: https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System/ .
- This closeout only records the completed merge/deployment; it does not broaden the linguistic acceptance boundary. Source-attested examples remain unadjudicated, full phrase IPA is compositional, independent gold remains 0, and pronunciation accuracy remains NOT_ASSESSED.

---
## Current continuation: source-backed coverage for the reported Khmer assembly phrase — 2026-11-25

- Base: current default main at 64c7dcacdf40e182b6d72876820c20fcd6e9c5f3; branch fix/romanization-ipa-entry-20261125; PR [#576](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/pull/576).
- Regression was first added RED. Quality run [45609529222](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45609529222) failed at the intended assertion and reproduced the exact browser-engine result /s/??? /t/??? /ɓ/??? /kam.pu.ciə/ for សភាតំណាងប្រជាជនកម្ពុជា.
- Added source-located lexical span សភាតំណាង with /saʔ.pʰiə tɑm.naːŋ/, extracted only from the first two components of the archived Wiktionary compound entry សភាតំណាងរាស្ត្រ; added ប្រជាជន with /prɑː.ciə.cŭən/; reused the existing កម្ពុជា fixture /kam.pu.ciə/. All are PROPOSED / source-attested but not independently adjudicated.
- Added U+016D ŭ → Ukrainian у to the shared target policy. The source breve remains in displayed IPA; Ukrainian practical spelling does not encode this quantity distinction. Python and browser target-adapter tests cover it.
- Resulting browser IPA: /saʔ.pʰiə tɑm.naːŋ/ /prɑː.ciə.cŭən/ /kam.pu.ciə/; IPA-derived Ukrainian candidate: сап'іє тамнанг пратьієтьуен кампутьіє. The complete user phrase is compositional and is not itself directly source-attested; no gold/accuracy claim is made.
- Exact-head Quality [45609962020](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45609962020) SUCCESS: 524 Python tests + 70 subtests; npm run check, Python↔JS structural/lexical/rule/segmentation parity, deterministic engine/tokenizer benchmarks and Vite build all completed.
- Chromium [45609869453](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45609869453) SUCCESS: 45/45 Playwright tests, including the new reported-phrase UI assertion. Browser run code head bfdccc121d6f1bbd9af892b42bd3b2d091be33e0; subsequent change before final Quality head only lower-cased proposal markers in fixture notes.
- Task ledger: specific phrase lexical coverage and target adaptation DONE_VERIFIED; whole phrase's direct phrase-level source attestation PARTIAL (compositional); broad contextual G2P and open-vocabulary vowel/coda coverage remain PARTIAL/evidence-limited; independent expert IPA gold remains 0 and pronunciation accuracy NOT_ASSESSED. Public browser remains static and does not call external Python providers.

---
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


## Browser-local neural IPA engine port — final closeout (2026-11-25)

**Owner request:** make an IPA-producing engine available in the public website instead of stopping at unresolved markers. The implementation is merged and deployed.

- PR: [#578 — Port MekongPhon IPA inference into the browser](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/pull/578), merged by repository owner.
- PR #578 merge commit: `520a1592345ccabbf859bc88f024485631306f73`.
- PR #579 documentation closeout merged as `a23412eb5ec17568d49d65fd86a1d69a94dcce65`; latest main SHA at this handoff: `a23412eb5ec17568d49d65fd86a1d69a94dcce65`.
- Branch used: `feat/browser-local-mekongphon-ipa-20261125`.
- Public service: https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System/
- Model: `byumatrixlab/khmer-ipa`, revision `20e069d384b240da76320e1569958568c12a54bc`; pinned model-card metadata declares Apache-2.0. The upstream training/evaluation corpus is not copied or redistributed; its rights remain unresolved.

### Delivered behavior

- The canonical deterministic engine remains the primary source-backed path.
- The reported phrase `សភាតំណាងប្រជាជនកម្ពុជា` now has source-located lexical components and a direct IPA → Ukrainian result: `/saʔ.pʰiə tɑm.naːŋ/ /prɑː.ciə.cŭən/ /kam.pu.ciə/` → `сап'іє тамнанг пратьієтьуен кампутьіє`. These fixtures are PROPOSED / secondary lexical evidence, not independent expert gold.
- A separate “Запустити локальну модель” action runs MekongPhon in a dedicated browser Worker. It lazy-loads about 35 MB of same-origin INT8 ONNX model weights only after the user asks; input text remains in the browser and no inference endpoint is used.
- Browser ByteLevel BPE tokenizers are checked against the pinned Transformers tokenizers. The model's raw IPA is shown separately as PROVISIONAL and passed through the existing typed IPA → Ukrainian adapter; it never silently overwrites canonical deterministic output.
- For the reported phrase the ONNX candidate is `saʔpʰiedɑmnaaŋprɑciecʊənkampucie`. FP32 ONNX differs from pinned Transformers by 3.03% CER on this probe; INT8 matches FP32 exactly. This is port parity, not phonetic accuracy.
- ONNX Runtime Web 1.23.2 is vendored with verified npm integrity and MIT notice. The model training corpus is excluded.

### Exact verification evidence

| Gate | Status | Evidence |
|---|---|---|
| Python tests, web checks, parity suites, deterministic benchmarks and Vite build on merged main | DONE_VERIFIED | Quality [45625848740](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45625848740) SUCCESS |
| Pinned model export and tokenizer parity | DONE_VERIFIED | Main Pages workflow [45625848945](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45625848945): export and tokenizer parity passed |
| Browser-local inference | DONE_VERIFIED | Model-enabled Chromium test passed 46/46 in exact PR Quality [45624434366](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45624434366), including the reported phrase and no-external-request assertion |
| PR browser smoke | DONE_VERIFIED | [45624453942](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45624453942) SUCCESS |
| Main browser smoke | DONE_VERIFIED | [45625848767](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45625848767) SUCCESS |
| GitHub Pages deployment and deployed asset smoke | DONE_VERIFIED | [45625848945](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45625848945) SUCCESS; manifest revision, encoder/decoder ONNX files and WASM runtime were fetched successfully |
| Independent pronunciation accuracy | BLOCKED / NOT_ASSESSED | Independent adjudicated Phnom Penh IPA gold remains 0; MekongPhon profile match remains UNVERIFIED; model outputs remain PROVISIONAL |

### Remaining genuine blockers

1. **Linguistic validation:** establish a licensed, split-independent, expert-adjudicated Phnom Penh IPA gold corpus, dialect/profile protocol and annotator agreement. Until then do not claim model accuracy or promote model output to canonical SUPPORTED IPA.
2. **Training-corpus rights:** upstream model artifact license does not license the training corpus. Keep the corpus out of the repository, build and runtime assets until rights are independently clarified.
3. **General coverage:** this model improves fallback availability but does not prove complete contextual Khmer phonology, tone, register, syllabification or dialect handling for arbitrary input.

The engineering port and public deployment are DONE_VERIFIED. The product remains a research-ready public beta, not an expert-validated or production-linguistically-validated Khmer G2P system. No formal release tag was created.

## Deterministic neural-distilled Khmer IPA engine — current continuation (PR #582)

### Starting point and architecture decision

The requested target is a **local deterministic engine developed from an offline neural teacher**, not a neural model that runs on the website.

`pinned licensed phonemic source → offline neural teacher → evidence-gated static distillation → deterministic local engine → typed IPA → Ukrainian IPA adapter`.

The website does not load neural weights, ONNX Runtime or call a remote inference API. It runs the existing structural/rule engine, the local phonemic lexicon and a static candidate table generated offline. All Ukrainian phonetic output passes through the shared IPA adapter.

### Delivered implementation

- Pinned Google `language-resources` Khmer pronunciation lexicon at commit `a90601024f07ab7e96c911243324e0adeb16da96`; the TSV itself declares CC BY 4.0. The companion Festvox phonology JSON has unresolved file-license scope and is not copied or redistributed. The 54-token runtime map is validated directly against the licensed TSV.
- Added explicit Google phonemic-token → typed IPA adapter. Source tokens, syllable boundaries, vowel length, provenance and mapping uncertainty are preserved. Unknown tokens fail closed.
- Generated eight reproducible lexical shards covering 62,118 non-empty Khmer phonemic rows; four multi-pronunciation spellings remain multi-candidate, and 61 blank rows remain unresolved.
- Integrated exact-form lookup into Python and browser engines without promoting unadjudicated Google candidates into Strict.
- Trained a project-owned offline neural teacher with word-disjoint train/dev/test splits and atomic phoneme-token targets.
- Distilled 2,532 OOV orthographic syllable candidates into a static table. Browser Super-soft reads this same-origin JSON table; no model inference runs in the browser.
- Integrated the deterministic tiers into the local Web Worker and local fallback. The production interface no longer presents a standalone neural-model button.
- Fixed the status notice so local Google dictionary candidates and offline neural-distilled candidates are not mislabeled as external provider results.

### Evidence and limitations

- Prior complete Quality/teacher/distillation workflow [45653367069](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45653367069) passed on its exact head.
- Teacher held-out source-label metrics: 84.18% word exact, 4.33% phoneme-token error rate, 100% source-label coverage. These are not independent IPA accuracy.
- Distillation composition diagnostic: 2,532 candidates; 63.86% exact, 14.19% token error rate, 98.4% composition coverage under a syllable-count alignment assumption. Teacher agreement does not promote rules to SUPPORTED.
- Preliminary Google phonemic-to-IPA concordance: 6/6 R12A vowel-context examples; 3/7 overlapping source-attested lexical examples exact, with four conflicts preserved. This is not a gold benchmark.
- Independent adjudicated IPA gold remains 0. Google source profile equivalence to `khmer-pph-careful-citation-v1` remains UNVERIFIED. Accuracy is NOT_ASSESSED.
- Strict > Soft > Super-soft accuracy ordering cannot be demonstrated without independent gold. Soft coverage is designed to exceed Strict; Super-soft guarantees non-empty display output, but that does **not** mean 100% complete IPA or 100% known pronunciation.

### Current verification state

- Browser smoke failed on older heads due to stale test expectations about canonical unresolved markers and provenance, then exposed a real status-notice bug. Tests were updated to reflect the typed contract and the notice bug was fixed in `755a89c695e93594adb3c980f2cc87adde80f6fd`.
- External khPOS and pinned upstream Rust comparisons passed on the preceding head `12b2675fc44eecd0c12e5caf5a8409d91aabbf67`.
- Latest exact-head Quality/browser/benchmark reruns after `755a89c` and documentation updates remain pending at this handoff. Do not report release readiness yet.
- Container has no repository checkout and DNS to github.com fails; no local test commands were executed. GitHub Actions exact-head runs are the verification source.

### Current task ledger

| Work item | Status | Acceptance / blocker |
|---|---|---|
| MekongPhon direct IPA source-matrix diagnostic | DONE_VERIFIED as a failed promotion gate | 0/6 exact, 44.44% CER in greedy and beam-4; not selected as teacher |
| NCKL respelling → phonemizer bridge | DONE_VERIFIED as negative control | Split 8/12 exact; whole-string and spaced-string each 7/12 exact; all bridge variants 6.93% CER vs direct phonemizer 11/12 exact, 0.99% CER; not integrated |
| Google source inventory, token map and typed IPA adapter | DONE_VERIFIED on prior successful Quality run; exact latest head pending | Source hashes, inventory and six-case screening checked; four lexical conflicts remain |
| Google deterministic lexicon and cross-runtime lookup | DONE_VERIFIED on prior successful Quality run; exact latest head pending | Eight shards, ambiguity and blank rows preserved |
| Project-owned neural teacher | DONE_VERIFIED on prior teacher workflow | Current-head rerun pending; metrics are source-label prediction only |
| Static neural-distilled OOV table | DONE_VERIFIED as provisional research artifact | 2,532 candidates; zero promoted to SUPPORTED |
| Browser/Python deterministic tier integration | PARTIAL | Code exists; exact-head Quality/Chromium and whole-branch review pending |
| GitHub Pages deployment of this branch | DEFERRED until integration | Pages deploys from main only; this branch has not been deployed |
| Independent IPA accuracy/profile equivalence | BLOCKED | Gold count 0; target profile equivalence UNVERIFIED |
| Final release readiness | TODO | Requires one final green SHA, code review, artifact drift and clean build |

### Branch and PR reconciliation

- PR #582 remains draft on `feat/deterministic-neural-distillation-20261125`; no merge or deployment has been performed.
- PR #519 remains open and untouched because it is a divergent earlier provider/hybrid proposal.
- Earlier MekongPhon browser port is retained as historical research/diagnostic, not the primary deterministic engine.
- No user branch was deleted, no release was published, and no external settings or license choices were changed.

### Next genuine acceptance gates

1. Complete exact-head Quality and browser smoke; fix every real failure with regression tests.
2. Inspect current-head teacher/distillation artifacts and confirm deterministic regeneration.
3. Run Python suite, JS checks, cross-runtime parity, lexicon generator drift check, benchmarks, Vite build and Chromium production tests on one final SHA.
4. Review all PR #582 changes against main and reconcile the open divergent PR without blind merging.
5. Update this handoff and the audit with final commit and actual run links.
6. Keep independent accuracy/profile equivalence blocked until adjudicated IPA gold exists. Only then decide whether PR #582 is ready for integration and Pages deployment.


## Superseding execution status — 2026-11-25 (exact head 686a9f5)

This section supersedes earlier pending/queued statements above for the exact head `686a9f5dcdcdf6ffd08c934e45f95a48a3e18e61`. Base `main` remained `8838a1f33b03aa1bad7c045c216305bb3e60e3f9` during verification.

### Verified implementation and checks

- Quality workflow [45690493937](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45690493937): **success**. Python suite: 564 passed plus 70 subtests. Google teacher completed all 12/12 epochs; its held-out Google-source-label test reported 84.175% word exact match, 4.331% phone-token error rate and 100% output coverage. These are source-label prediction metrics, not independent IPA accuracy.
- The same run's deterministic distillation reported 2,532 accepted candidates and 89 rejected internal-boundary candidates from 2,621 OOV syllable candidates; 63.855% held-out composition exact match, 14.194% phone-token error rate and 98.419% composition coverage under the count-only assumption that orthographic syllable count equals Google phonological dot count. No rules were promoted. Accuracy is null / `NOT_ASSESSED_NO_INDEPENDENT_IPA_GOLD`; profile equivalence remains `UNVERIFIED`.
- The generated teacher artifact is attached to run 45690493937 (artifact 15059945245). Source is pinned at revision `a90601024f07ab7e96c911243324e0adeb16da96`, SHA-256 `b3f2e700d07d6c01a4c8cac5aa2f13b9a66885668ac482cc0c513f73c56495e5`, CC BY 4.0, 62,179 source rows, 62,118 non-empty rows and 61,214 unique spellings with pronunciation.
- The exact-head Pages build-check in run 45690493937: **success**; it staged the actual generated candidate table, built the Pages site and ran Chromium against that staged artifact. Pages-specific browser suite: **49 passed**, including the real static-table execution, same-origin worker, no external network requests for Khmer input, local fallback, latest-input race guard and no standalone neural model in production.
- Exact-head generic Chromium smoke [45690493765](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45690493765): **success, 48 passed**.
- Exact-head shared Khmer IPA engine benchmark [45690493847](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45690493847): **success**; external khPOS benchmark [45690493805](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45690493805): **success**; pinned upstream Rust comparison [45690494064](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45690494064): **success**.
- Earlier fixed-count expectations were removed. CI and browser assertions now validate the accounting invariant `accepted + rejected == OOV candidate inventory`, because teacher outputs may legitimately change the accepted/rejected split while preserving complete accounting.

### Final task ledger at this head

| Work item | Status | Evidence / remaining acceptance |
|---|---|---|
| Pinned Google source inventory, attribution and typed phonemic → IPA adapter | DONE_VERIFIED | Exact-head Quality success; no claim that source phonemic labels are independent IPA gold |
| Deterministic lexical shards and Python/browser parity | DONE_VERIFIED | Exact-head Quality success |
| Offline neural teacher and reproducible static OOV distillation | DONE_VERIFIED as provisional research pipeline | 12 epochs; artifact 15059945245; 2,532 accepted / 89 rejected; zero rules promoted |
| Browser worker, local fallback and deterministic tier integration | DONE_VERIFIED for implemented contract | Exact-head generic Chromium 48/48 and Pages artifact Chromium 49/49 |
| Production build with actual generated static table | DONE_VERIFIED | Exact-head `pages-build-check` success; this is a build check, not a deployment |
| Strict > Soft > Super-soft empirical accuracy ordering | BLOCKED | Requires independent adjudicated IPA gold; none exists |
| Independent pronunciation accuracy and Google target-profile equivalence | BLOCKED | IPA gold count 0; profile equivalence `UNVERIFIED` |
| Live GitHub Pages deployment | TODO pending PR integration | PR #582 is still a draft and has not been merged; after merge verify the main-branch Pages deployment and live URL/assets |

### Branch and integration state

- PR #582 remains the active implementation PR on `feat/deterministic-neural-distillation-20261125`; verified code head is `686a9f5dcdcdf6ffd08c934e45f95a48a3e18e61`. It was mergeable/clean against unchanged main when checked; integration and deployment have not yet occurred.
- PR #519 remains untouched because it is a divergent earlier provider/hybrid proposal. PR #572 is already merged. PR #573 remains closed/unmerged due unresolved licensing/data scope. No user branch was deleted, no force push was used, and no release was published.
- The implementation is now **build-verified and ready for integration review**, but it is not a linguistically validated production release: independent IPA accuracy and profile equivalence remain evidence-blocked. A successful Pages build-check must not be described as a live deployment.
- No local commands are claimed: the working container has no repository checkout and could not resolve GitHub DNS. All stated checks above are remote GitHub Actions results.


## Final superseding status — exact head 77e5ee4 (2026-11-25)

This entry supersedes the prior metrics and pending-status entries for this continuation. Verified branch head: `77e5ee43266a622978dd37e92cf54231a1921860`; base `main`: `8838a1f33b03aa1bad7c045c216305bb3e60e3f9`.

### Final exact-head verification

- Quality workflow [45697903503](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45697903503): **success**. Python tests: 564 passed plus 70 subtests; lexicon/schema/parity and web checks passed; teacher, distillation, source matrix and NCKL diagnostic jobs succeeded. The browser-model export job was correctly skipped for this architecture.
- Generic Chromium smoke [45697903507](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45697903507): **success, 48 passed**. Shared engine benchmark [45697903476](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45697903476), external khPOS benchmark [45697903391](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45697903391), and pinned upstream Rust comparison [45697903367](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45697903367): **all success**.
- Exact-head Pages build-check: **success**. It downloaded teacher artifact 15061573629, staged the generated table into `public/data`, verified staged/build artifact identity, built the Pages site and executed Chromium against the real static table: **49 passed**. This remains a build-check, not a live deployment.
- Teacher artifact source pin remains revision `a90601024f07ab7e96c911243324e0adeb16da96`, source TSV SHA-256 `b3f2e700d07d6c01a4c8cac5aa2f13b9a66885668ac482cc0c513f73c56495e5`, CC BY 4.0; 62,179 source rows, 62,118 non-empty rows, 61,214 unique spellings with pronunciation.

### Exact-head teacher and distillation metrics

- Teacher training completed 8 of 12 requested epochs. Held-out Google-source-label prediction: 82.7772% word exact match, 4.7722% phone-token error rate, 100% output coverage. These are source-label prediction metrics, not independent IPA accuracy.
- Distillation: 2,539 accepted provisional candidates + 82 rejected internal-boundary candidates = 2,621 OOV syllable candidates. Held-out composition diagnostic: 63.9279% word exact match, 13.2874% phone-token error rate, 98.6166% coverage and 100% syllable-boundary-count agreement under the count-only orthographic-syllable-count/Google-dot-count assumption. No rules were promoted.
- Checkpoint SHA-256: `96ecb67d06293cd1c9ead51911d7e842d2310412c7174d96281993cbb627590b`. Accuracy remains null / `NOT_ASSESSED_NO_INDEPENDENT_IPA_GOLD`; profile equivalence remains `UNVERIFIED`; IPA gold count remains 0. Metrics must not be described as independent phonetic accuracy.

### Provenance correction

The artifact stores its checkpoint digest at `artifact.teacher.checkpoint_sha256`, not at the artifact root or individual candidate rows. Both browser loading paths (Worker and local fallback) now propagate that digest into each candidate's `teacher_checkpoint_sha256` field. The engine result's `neural_teacher_checkpoint_sha256` therefore carries the actual checkpoint provenance instead of null. The worker contract test asserts propagation in both paths. This correction is in the verified exact head.

### Final ledger and integration state

| Item | Status | Evidence / remaining acceptance |
|---|---|---|
| Google source pin, attribution, typed phonemic → IPA adapter, deterministic lexicon and parity | DONE_VERIFIED | Exact-head Quality success |
| Offline teacher and static deterministic OOV table | DONE_VERIFIED as provisional research pipeline | Artifact 15061573629; metrics and limits above; zero rules promoted |
| Strict/Soft/Super-soft browser engine, same-origin worker, local fallback, provenance | DONE_VERIFIED for implemented contract | Exact-head 48/48 generic and 49/49 Pages-artifact Chromium tests |
| Production Pages build with real generated table | DONE_VERIFIED | Exact-head Pages build-check success; no live deploy yet |
| Empirical accuracy ordering Strict > Soft > Super-soft | BLOCKED | Requires independent adjudicated IPA gold |
| Independent pronunciation accuracy / target-profile equivalence | BLOCKED | IPA gold count 0; profile equivalence UNVERIFIED |
| Live GitHub Pages deployment | TODO pending PR merge | After merge verify main-branch deployment and live URL/assets |

PR #582 is marked ready for review, open, and mergeable against unchanged `main`; it has not yet been merged. PR #519 remains untouched as a divergent earlier provider/hybrid proposal; PR #572 is already merged; PR #573 remains closed/unmerged due unresolved licensing/data scope. No branches were deleted, no force push was used, and no release was published. The implementation is build-verified and integration-ready, but not a linguistically validated production release until independent IPA gold and target-profile evidence exist.


## Post-merge and live deployment verification — 2026-11-25

This is the final superseding deployment note. The implementation PR #582 was squash-merged to `main` as `62492f06c0b36a55427424dd017215679f2038d6` (parent: `8838a1f33b03aa1bad7c045c216305bb3e60e3f9`). The main-branch Quality workflow `45701433046` completed successfully. Main-branch Pages deployment workflow `45701432971` completed successfully: teacher artifact generation/distillation and validation, static-table staging, web checks, production build, production Chromium exercise, Pages configuration, and artifact upload all succeeded. The Pages deployment job itself concluded success.

**Live site:** https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System/ . A fresh live fetch returned the public beta application. Its built HTML references `assets/service-CqLRfFnl.js`, `assets/main-CuKGjaI7.js`, and `assets/main-D59EhEYu.css`. The deployed service bundle contains the local `khmer-engine.worker-Hh2spuQ0.js` Worker reference and fetches `../data/google-neural-distilled-syllables.json`; both the hashed Worker bundle and static JSON artifact were served successfully from the same GitHub Pages origin. A live browser interaction using `ខ្មែរ` in Strict rendered `/kʰmae/` and Ukrainian `к'мае`, romanization `Khmer`, with no reported browser console or network errors. This is a runtime smoke check on one lexical fixture, not a broad pronunciation accuracy test. A further live OOV/Super-soft interaction timed out and is **not** counted as verified; the exact-head CI Pages Chromium run remains the comprehensive build-time evidence (49 passed).

**Final teacher artifact evidence** (Quality PR run `45699114121`, artifact `15061573629`): teacher 12/12 epochs, 84.18% held-out Google-source-label word exact match, 4.33% phone-token error rate, 100% output coverage. Distillation yielded 2,532 accepted candidates + 89 rejected internal-boundary candidates = 2,621 OOV syllable candidates; held-out composition diagnostic 63.86% exact match, 14.19% phone-token error rate, 98.42% coverage. These are source-label prediction and composition diagnostics only, not independent IPA accuracy. No rules were promoted; independent adjudicated IPA gold remains 0 and target-profile equivalence remains UNVERIFIED. Do not carry forward earlier artifact metrics (2,539 + 82; 82.78% teacher exact match) as the final merged artifact metrics.

**Final disposition:** the deterministic engine is merged and deployed as a public research beta; implementation/build/runtime smoke gates are passed. It is not a linguistically validated production release. Strict/Soft/Super-soft empirical accuracy ordering, pronunciation accuracy, and target-profile equivalence remain evidence-blocked until an independent expert-adjudicated IPA gold corpus and explicit profile adjudication exist. The Super-soft 100% promise is display coverage with explicit unresolved markers, not 100% verified pronunciation accuracy.


## 2026-11-25 follow-up: generalize Soft Khmer → IPA and remove false unknown tails (PR #583)

**Status at this checkpoint: PARTIAL — implementation and regression tests are in PR #583; exact-head CI and Pages verification are pending.** This entry supersedes earlier statements that the neural-distilled candidate table is only consumed by Super-soft.

### New evidence from the reported failing input

The four syllables shown in the user reproduction were already present in the pinned Google phonemic source lexicon; no words were added to the dictionary:

| Khmer | Existing source phonemic row | Typed IPA candidate | Ukrainian adapter output |
|---|---|---|---|
| រុង | `r u ŋ` (row 45018) | `/ruŋ/` | рунг |
| ឡឺត | `l əə t` (row 60848) | `/ləːt/` | лет |
| ឡាវ | `l aa w` (row 60741) | `/laːw/` | лав |
| ឌី | `ɗ ii` (row 22023) | `/ɗiː/` | ді |

The neural teacher independently produced the same four source-token sequences from the orthographic input. The previous display added a trailing `???` to complete phonemic candidates, confusing profile uncertainty with a genuinely missing phoneme. The canonical Ukrainian IPA adapter maps consonantal `/w/` to `в`, not `у`; the legacy `compatibility_ru: у` value is not the default. Keep `/aw/` (a diphthong) distinct from `/aːw/` (long vowel plus consonant): the former maps to `ау`, while the latter maps to `ав`. The adapter must preserve `ː` until longest-match segmentation, then render long-vowel quantity without a separate Ukrainian mark. The separate BGN/PCGN orthographic route remains distinct.

### Implementation in PR #583

- Complete Google phonemic candidates now pass through the typed Google-phonemic → IPA → Ukrainian adapter without a fabricated `???` suffix. They remain explicitly `PROVISIONAL` because the selected pronunciation profile has not been independently adjudicated.
- The offline teacher's static artifact is being expanded from lexicon-derived OOV syllables to generated CV and CVC patterns using the pinned source vocabulary. This is a pattern-derived candidate space, not a patch adding the reported words to a dictionary.
- Soft consumes only generated CV/CVC candidates plus existing exact source-backed candidates. Super-soft additionally sees the broader exploratory OOV candidate inventory and orthographic fallbacks. Strict continues to exclude unadjudicated model candidates.
- All model-generated rows remain `PROVISIONAL`; no phonological rule is promoted to verified.

### Verification state

- Local inference using the saved teacher checkpoint produced `r u ŋ`, `l əə t`, `l aa w`, and `ɗ ii` for the four reported forms.
- The four source lexicon rows were independently located in the pinned eight-shard data.
- Regression tests now cover the four exact source-backed forms and the generated OOV CV form `កិ`; the latter is a test probe, not a lexical addition.
- An early regression exposed a real adapter bug: `/aːw/` was reduced to `/aw/` before longest-match segmentation, so the long vowel plus consonantal `/w/` was incorrectly rendered as `лау`. PR #585 fixed the adapter by preserving `ː` through matching; `/aw/ → ау`, `/aːw/ → ав`, `/laːw/ → лав`. The initial 48-test run is historical and superseded by exact-head checks on PR #585 and the subsequent Pages deployment.
- No independent adjudicated IPA gold was added. Accuracy, target-profile equivalence, and the empirical Strict > Soft > Super-soft accuracy ordering remain unverified.


## 2026-11-26 follow-up: Pages deployment validator fix (PR #586)

- PR #585 has now been squash-merged to main as `08b3ef4dcd77f9631d14682cd7e66878a90638e6`. It preserves `ː` through longest-match IPA mapping: `/aw/ → ау`, `/aːw/ → ав`; the reported phrase now renders `рунг лет лав ді` in the browser test. The fix is merged but awaits the next successful Pages deployment.
- The remaining deployment blocker is PR #586: `scripts/validate_google_distilled_syllables.py` now adds the repository `src` directory before importing `khmer_ua`, and a subprocess regression test removes `PYTHONPATH` to prove the validator is self-contained. CI is configured to run the offline teacher and Pages build-check on this branch. PR #586 remains open pending exact-head Quality, Chromium and Pages artifact verification.
- Do not claim the live Pages site contains PR #583 or PR #585 until the main deployment workflow succeeds and live app, Worker, static JSON artifact and the reported phrase are smoke-tested.


## 2026-11-26 final deployment and /w/ correction

- PR #583 merged as `58691bdc80c2c83882e765aa89ebcfb28a86f509`; it adds generated CV/CVC candidate generalization to Soft and removes fabricated `???` suffixes from complete source-backed phonemic candidates.
- PR #585 merged as `08b3ef4dcd77f9631d14682cd7e66878a90638e6`; it fixes the Ukrainian IPA adapter so consonantal `/w/` is `в`, not `у`, and preserves vowel length while matching. The exact reported phrase is `រុងឡឺត ឡាវឌី` → IPA `/ruŋ/ /ləːt/ /laːw/ /ɗiː/` → Ukrainian `рунг лет лав ді`. The separate short diphthong `/aw/` maps to `ау`; `/aːw/` maps to `ав`.
- PR #586 merged as `d2c37994245a3eaf4941cbbcdeb79fd0c60a1789`; it fixes the Pages validator's source-layout import and adds a subprocess regression check with `PYTHONPATH` removed.
- PR #586 exact-head Quality [45776759424](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45776759424), Chromium [45776759171](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45776759171), teacher/distillation and production Pages build-check all succeeded. The main deployment for `d2c37994245a3eaf4941cbbcdeb79fd0c60a1789` succeeded in [45778308083](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45778308083); its post-deploy smoke test passed. Main Chromium [45778308101](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45778308101) passed all 50 tests, including the exact reported phrase; the build-time artifact test was not skipped on the deployment build and passed.
- Live public site: https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System/. The current main branch and Pages deployment include the generalized deterministic Soft/Super-soft candidate table and the corrected `/w/ → в` adapter.
- Remaining linguistic limitation: all newly generated/model-derived candidates remain `PROVISIONAL`; independent expert-adjudicated IPA gold is still 0. The implementation is deployed and browser/build verified, but pronunciation accuracy and target-profile equivalence are not established.


## 2026-11-26 continuation: structural Khmer G2P coverage and independent IPA gold

**Research branch:** `research/phonological-structure-coverage-ipa-gold-20261126`  
**Base main:** `efc101626bce56dd26c2d4c97b3fe62558b8998a`  
**Branch implementation so far:** source/evidence audit and corpus registry; no production phonology rule has been guessed or added.

- New audit: `docs/audits/current/KHMER-PHONOLOGICAL-STRUCTURE-COVERAGE-AND-INDEPENDENT-GOLD-PLAN-2026-11-26.md`.
- Updated `data/khmer/sources.json` with Edinburgh DataShare cluster audio, OpenSLR SLR42 and MekongPhon evidence records.
- Existing baseline measured from main: 14 source-indexed vowel/register lexical cases (12 source-attested-not-gold, 2 conflicting) and only three dependent vowel signs represented; 32 dependent-vowel × series cells are expected. Most cells remain not established.
- Independent IPA gold currently has 0 records: gold.tsv contains only its header; annotations.jsonl, records.jsonl and splits.jsonl are empty.
- Strongest new gold-pilot source: Edinburgh DataShare DOI 10.7488/ds/2454, with 10 Phnom Penh speakers, 79 cluster items, repeated tokens at two speech rates and segmented TextGrids. Its end-user licence was inspected as CC BY 4.0. It still requires independent phonemic/narrow-phonetic IPA annotation and adjudication.
- OpenSLR SLR42 is CC BY-SA 4.0 audio + text, but detailed speaker/dialect/style coverage is not yet audited. MekongPhon is a useful external source-concordance reference but not independent gold for this project until training lineage and provenance are resolved.
- /w/ is already fixed on main as Ukrainian в; /aw/ and /aːw/ remain distinct diphthong vs long-vowel-plus-consonant mappings. Do not regress to у.
- Existing PR #584 remains open for a Pages validator self-contained import fix; unrelated to this linguistic research branch. PR #519 remains open/stale and untouched.
- Next executable tasks: inspect Edinburgh archive and TextGrid metadata; derive a speaker/item/rate/cluster manifest; create double-annotation pilot rows; then expand compositional rules only where the evidence supports them. No independent gold or accuracy claim is made yet.


- Additional source located and registered: UNESCO 2016 *Khmer Pronouncing Dictionary: Standard Khmer and Phnom Penh Dialect* (339 pages). Potential independent lexical/profile cross-check, but not audio gold; notation, exact coverage and copyright permissions remain unverified. No entries copied.


- Google/Sodimana et al. 2018 TTS corpus is another potential audio annotation source: paper reports 17 female speakers, 2,906 recordings, 3:58h, plus a separate 70,671-entry phonemic lexicon; CC BY 4.0 unless otherwise noted. The project teacher already uses the Google lexicon, so those labels cannot be treated as independent gold. Audio could be independently reannotated only after archive lineage, speaker metadata, dialect and file-level rights are verified.
- Exact-head PR #587 Quality run [45812080747](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45812080747) SUCCESS (Python tests and web checks); Chromium browser smoke [45812080707](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45812080707) SUCCESS. Documentation/evidence changes only; no runtime phonology changed.


- Extracted Minegishi 1985's complete 28-row two-series vowel-sign value table (§1.2, printed pp.45–46) to `data/khmer/source-extracts/minegishi-1985-vowel-sign-values.json`. Values remain the source's bracketed phonetic notation, not normalized IPA; unclear row-label diacritics are flagged and no Unicode mapping or engine rule is inferred. New regression test enforces these boundaries.


- UNESCO dictionary PDF preface was inspected: its authors define “Standard” as formal/institutional usage (universities, schools, administration, media) and question whether one uniform standard pronunciation had been clearly established. Treat it as a lexical profile reference, not an unquestioned homogeneous speech norm.
- Exact-head PR #587 verification on commit `441b46b4a84f7d28c3c9ac1d6a7ce04ec7dedf88`: Quality [45812970684](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45812970684) SUCCESS (**566 Python tests + 70 subtests; web checks PASS**); Chromium [45812970861](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45812970861) SUCCESS (**49 passed, 1 Pages-build-only test skipped**). The new Minegishi source-table regression passed. No production G2P code changed in this research PR.


## 2026-11-26 algorithmic correction: every /w/ → Ukrainian в

The owner clarified that IPA /w/ must map to Ukrainian **в in all contexts**. This supersedes the earlier target-policy distinction that rendered /aw/ as ау. The executable data/ukrainian/practical-policy.json policy is now version 2026-11-26.1: standalone /w/ remains в and the sequence /aw/ now maps to ав. Since Ukrainian practical spelling does not encode vowel length, /aw/ and /aːw/ both render ав; their IPA inputs remain distinct and preserve length. The Russian compatibility comparator's legacy /w/ → у is separate and is not used by the Ukrainian target adapter.

TDD evidence: added Python whole-IPA tests and JavaScript typed-IPA adapter tests for /w/, /wa/, /aw/, /aːw/ and /laːw/. Exact-head browser CI on the test-only commit 446bdf5521ff7b08b48d9d776ecac5774d8fa002 failed as expected: /aw/ returned ау instead of ав. The policy fix is on commit b70e0ed64e95d997f8dd36d51ef5ad50d54f7cc0; final CI is running and must be checked before claiming completion.

The broader structural work remains PARTIAL/BLOCKED: Minegishi's 28 source labels are still not crosswalked to Khmer Unicode; source audio archive download/inspection is still blocked by environment network access; independent adjudicated IPA gold remains 0. Do not infer a codepoint crosswalk or promote a rule without direct source evidence.
