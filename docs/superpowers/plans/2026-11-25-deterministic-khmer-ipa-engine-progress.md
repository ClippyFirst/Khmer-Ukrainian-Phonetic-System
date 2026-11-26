# Execution ledger — deterministic neural-distilled Khmer IPA engine

## Workspace and integration boundary

- Branch: `feat/deterministic-neural-distillation-20261125`
- Base: `8838a1f33b03aa1bad7c045c216305bb3e60e3f9`
- PR: [#582](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/pull/582), draft
- Latest code commit at this update: `755a89c695e93594adb3c980f2cc87adde80f6fd`
- The container has no repository checkout and cannot resolve github.com. All changes were made through the remote GitHub branch; exact-head GitHub Actions are the verification environment. This means no local test execution.
- Do not merge or deploy until exact-head gates and whole-branch review are complete. No merge/deploy has been performed.

## Architecture selected and implemented

**Offline neural teacher → static deterministic student → typed IPA → Ukrainian IPA adapter.**

- The website does not run a neural model, ONNX Runtime, or remote inference. The neural teacher trains offline from the pinned, licensed Google Khmer phonemic corpus.
- Runtime is deterministic: existing structural parser, local rule engine, local source phonemic lexicon, evidence-bearing token-to-IPA map, and a static table of neural-distilled OOV syllable candidates.
- Python and browser runtime share the typed IPA boundary and existing IPA → Ukrainian adaptation. The model never generates Ukrainian output directly.
- Strict / Soft / Super-soft expose progressively wider candidate sets. Strict does not promote unadjudicated Google/model predictions. Soft can use local phonemic dictionary candidates. Super-soft can additionally use the static neural-distilled syllable table. Unresolved remainder remains explicit.
- The model is an offline development dependency, not a visitor runtime dependency. Khmer input stays local in the browser; the static candidate table is fetched same-origin and cached by the browser.

## Task ledger

| Task | Status | Evidence / remaining acceptance |
|---|---|---|
| Compare MekongPhon direct IPA output against source-attested matrix | DONE_VERIFIED as a failed promotion diagnostic | Greedy and beam-4: 0/6 exact, 44.44% codepoint CER. Not an accuracy score; not selected as teacher. |
| Compare NCKL respelling bridge with direct Khmer Phonemizer | DONE_VERIFIED as a negative control | Split 8/12 exact, 6.93% CER; whole-string 7/12 and spaced-string 7/12 exact, each 6.93% CER; direct Phonemizer 11/12 exact, 0.99% CER. No bridge variant is integrated. |
| Pin Google Khmer phonemic source and project-authored token map | DONE_VERIFIED | The full TSV matches the pinned upstream file exactly and declares CC BY 4.0; 62,118 non-empty Khmer rows, 61 blank rows, 62,114 unique spellings, four multi-pronunciation spellings. The 54 observed lexical tokens are mapped directly. Companion Festvox phonology JSON has unresolved license scope and is not redistributed. |
| Typed Google phonemic → IPA adapter | DONE_VERIFIED on prior successful full Quality run; exact latest head pending | Atomic source tokens, long-vowel marks and syllable dots preserved; unmapped tokens fail closed; per-token evidence and uncertainty retained. 6/6 R12A screening examples match; 3/7 overlapping lexical examples match and four conflicts remain visible. These are not accuracy metrics. |
| Deterministic Google phonemic lexical shards and Python/browser lookup | DONE_VERIFIED on prior successful full Quality run; exact latest head pending | Eight reproducible shards; ambiguous variants preserved; blank rows unresolved; source hashes and attribution checked; no IPA promotion from corpus membership alone. |
| Project-owned offline neural teacher | DONE_VERIFIED on prior successful teacher workflow | Run [45653367069](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45653367069), artifact [15043450562](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45653367069#artifacts): held-out Google source-label prediction 84.18% word exact, 4.33% phoneme-token error rate, 100% source-label coverage. Not independent IPA accuracy. Current-head retraining is pending. |
| Distill neural teacher to static OOV syllable candidate table | DONE_VERIFIED as a research artifact | 2,532 candidates; 63.86% exact, 14.19% token error rate, 98.4% composition coverage under the documented syllable-count assumption. Teacher agreement only; zero candidates promoted to SUPPORTED. |
| Integrate deterministic tiers, worker and local fallback | PARTIAL pending exact-head CI/Chromium | Code and tests are implemented. Worker loads only same-origin static candidate JSON in Super-soft; fallback uses the same static table. No remote inference. Exact-head browser smoke is not yet green. |
| Production Pages artifact generation | PARTIAL / not deployed | Pages workflow trains/caches offline teacher, distills static table, stages it under `public/data`, runs checks/build/Chromium and smoke-tests the deployed asset. Workflow only deploys from main; PR branch is not deployed. |
| Accuracy ordering Strict > Soft > Super-soft | BLOCKED | Independent adjudicated IPA gold remains 0. Do not infer tier accuracy ordering from source-label prediction or model/student agreement. |
| Soft coverage > Strict; Super-soft non-empty output coverage = 100% | PARTIAL / contract implemented | Coverage is explicitly split into IPA candidate coverage and non-empty display coverage. Super-soft's 100% is non-empty output (unknown markers may remain), not 100% complete IPA. |
| Independent target-profile equivalence and pronunciation accuracy | BLOCKED | Gold count 0; Google corpus profile equivalence to `khmer-pph-careful-citation-v1` remains UNVERIFIED. |
| Whole-branch review and final release gates | TODO | Requires exact-head green Quality, Chromium browser smoke, current teacher/distillation workflow, artifact drift/clean build and read-only review. |

## Current exact-head CI history

- On `8213510d209eaffee07cff83d82ab5e56fbae629`, browser smoke failed at an assertion expecting the canonical IPA field to end in `???`; canonical IPA correctly retains `⟦NOT_ESTABLISHED⟧`. Corrected the test to distinguish canonical typed status from display-tier uncertainty.
- On `386b1f1eeae4bb328fa3bb2d401321021d9e9f3c`, browser smoke exposed stale expected provenance labels. Updated the test to assert the actual structured provenance emitted by the typed adapter.
- On `12b2675fc44eecd0c12e5caf5a8409d91aabbf67`, the browser regression suite reached the status-notice assertion. It exposed a real UI bug: local Google lexical candidates were described as external provider candidates. Updated the regression test first, then fixed `getStatusNotice` in commit `755a89c695e93594adb3c980f2cc87adde80f6fd` to distinguish local Google, neural-distilled, partial and external candidate types.
- Latest exact-head Quality and browser-smoke workflows for `755a89c695e93594adb3c980f2cc87adde80f6fd`: pending at this ledger update. Do not claim they passed.
- Benchmarks on previous exact heads passed: shared Khmer IPA engine, external khPOS and pinned upstream Rust segmentation comparison. They must be rerun or confirmed on final head.

## Previous PRs and branches

- PR #582 remains draft and is the active continuation branch.
- PR #519 remains open and untouched; it is a divergent earlier provider/hybrid proposal, not the base for this deterministic neural-distilled architecture.
- Earlier MekongPhon browser model port is retained only as historical research/diagnostic; the production UI path on this branch removes its standalone model button and ONNX runtime.
- No branch was deleted, no conflicting PR was merged, no release was published, and no Pages deployment was initiated.

## Commands / checks actually executed

- Remote CI run [45653367069](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45653367069): Quality, Google teacher, distillation/source matrix and NCKL diagnostic jobs all succeeded on that run's exact head.
- Remote browser smoke [45668568863](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45668568863): failed at the old status-notice expectation; this prompted the local-vs-external notice fix.
- Remote external khPOS benchmark on `12b2675`: success.
- Remote pinned upstream Rust comparison on `12b2675`: success.
- Remote shared engine benchmark on `12b2675`: in progress at last observation.
- Latest branch push `755a89c` triggered new Quality/browser/benchmark runs; exact results are pending.
- No local `pytest`, `npm run check`, build, or Playwright command is claimed as executed in this environment.

## Next acceptance gates

1. Inspect exact-head Quality and browser smoke on `755a89c`; fix every failure with a regression test and rerun.
2. Inspect exact-head teacher/distillation artifacts and verify reproducibility and metric semantics.
3. Run generated Google lexicon `--check`, Python tests, JS checks, cross-runtime parity, benchmarks, Vite build and Chromium tests on one final SHA.
4. Review branch diff against main and resolve PR #519/#582 overlap without merging blindly.
5. Update master handoff and repository audit with final SHA and evidence. Keep pronunciation accuracy/profile equivalence blocked until independent adjudicated IPA gold exists.
6. Only then present the PR for integration; deployment remains a separate Pages/main-branch event.


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
| ឡាវ | `l aa w` (row 60741) | `/laːw/` | лау |
| ឌី | `ɗ ii` (row 22023) | `/ɗiː/` | ді |

The neural teacher independently produced the same four source-token sequences from the orthographic input. The previous display added a trailing `???` to complete phonemic candidates, confusing profile uncertainty with a genuinely missing phoneme. The Ukrainian adapter's `aw → ау` sequence is intentional; the separate BGN/PCGN orthographic route can still display a different spelling.

### Implementation in PR #583

- Complete Google phonemic candidates now pass through the typed Google-phonemic → IPA → Ukrainian adapter without a fabricated `???` suffix. They remain explicitly `PROVISIONAL` because the selected pronunciation profile has not been independently adjudicated.
- The offline teacher's static artifact is being expanded from lexicon-derived OOV syllables to generated CV and CVC patterns using the pinned source vocabulary. This is a pattern-derived candidate space, not a patch adding the reported words to a dictionary.
- Soft consumes only generated CV/CVC candidates plus existing exact source-backed candidates. Super-soft additionally sees the broader exploratory OOV candidate inventory and orthographic fallbacks. Strict continues to exclude unadjudicated model candidates.
- All model-generated rows remain `PROVISIONAL`; no phonological rule is promoted to verified.

### Verification state

- Local inference using the saved teacher checkpoint produced `r u ŋ`, `l əə t`, `l aa w`, and `ɗ ii` for the four reported forms.
- The four source lexicon rows were independently located in the pinned eight-shard data.
- Regression tests now cover the four exact source-backed forms and the generated OOV CV form `កិ`; the latter is a test probe, not a lexical addition.
- An initial browser smoke run failed only because its new expectation used `лав`; the actual configured `aw → ау` adapter correctly returned `лау`. The assertion was corrected. Exact-head verification on `f6041dac3428fe4d049d3980ef8855e1ca225274`: the Quality test job passed 564 Python tests plus 70 subtests, all JavaScript checks, Python/JavaScript parity checks, deterministic-engine benchmarks and the site build; browser smoke run [45711511779](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45711511779) passed 48 tests with one Pages-only artifact test skipped; external khPOS benchmark [45711511868](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45711511868) succeeded. The Quality workflow's neural-teacher training/distillation and Pages artifact build-check are still running; no deployment has occurred.
- No independent adjudicated IPA gold was added. Accuracy, target-profile equivalence, and the empirical Strict > Soft > Super-soft accuracy ordering remain unverified.


## 2026-11-26 follow-up: post-merge verification and blockers

- PR #583 merged as `58691bdc80c2c83882e765aa89ebcfb28a86f509`. Exact-head Quality [45772026933](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45772026933) passed 564 Python tests + 70 subtests, offline teacher training/distillation and Pages build-check; Chromium [45772026932](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45772026932) passed 49 tests; external khPOS [45772026897](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45772026897) passed.
- Main Pages deployment [45773125196](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45773125196) failed before deploy because the validator could not import `khmer_ua` without `PYTHONPATH=src`. A separate branch adds explicit `src` resolution and a subprocess test with `PYTHONPATH` removed.
- New teacher/distillation metrics: 84.1754% held-out Google-label exact match, 4.3309% phone-token error, 100% coverage; 13,941 accepted candidate rows (11,633 Soft + 2,308 exploratory), 3,804 rejected internal-boundary rows; held-out composition diagnostic 63.8554% exact, 14.1937% token error, 98.4189% coverage. These are not independent IPA accuracy; gold count remains zero.
- PR #585 fixes the long-vowel/diphthong collision in the Ukrainian adapter. Keeping `ː` until longest-match segmentation yields `/aw/ → ау` and `/aːw/ → ав`, so the reported phrase now renders `рунг лет лав ді`. Exact-head Quality [45775899034](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45775899034) passed 564 Python + 70 subtests; Chromium [45775899044](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45775899044) passed 49 tests. PR #585 remains open.
- Current state: merged generalized Soft path is build-verified but not yet live-updated because Pages deploy failed; adapter correction is verified in PR but awaits merge. Do not claim current live site has these two fixes until a successful main Pages deployment and live smoke check.
