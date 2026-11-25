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
| Pin Google Khmer phonemic source and Festvox phone inventory | DONE_VERIFIED | Google source commit `a90601024f07ab7e96c911243324e0adeb16da96`; CC BY 4.0 attribution retained; 62,118 non-empty Khmer rows, 61 blank rows, 62,114 unique spellings, four multi-pronunciation spellings. All 54 observed lexical phone tokens occur in the 56-phone inventory. |
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
