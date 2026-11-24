# Build log — Lao engine contract alignment

- Base: `main` at `1b8649c4b874fbf34a66012d7e02aa1da04fb6da`.
- Branch: `feat/khmer-lao-engine-contract-parity-20261124`.
- PR: [#568](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/pull/568), ready for review, mergeable, not merged.
- Source/test head: `f579e1444fbda2b186fdf8a04dc9f52f7ebc044e`. Later commits update benchmark evidence, audits, handoff and replica artifacts only.
- Latest docs/evidence test head: `79d7ff26e2f7c5905ea4ed6fde903fdbfe81de82`.
- Final branch head at the time of this build-log update: see the PR head; subsequent changes to this file are documentation-only.
- Method: clean-room architecture mapping from the Lao contract; no Lao code, data or phonological values copied.
- TDD: initial Python typed IPA tests were committed before implementation and produced the expected RED failure; CLI tests were likewise added before routing CLI through the engine.
- Local clone: `git clone` could not resolve `github.com` in the local container; all edits were made on the isolated GitHub branch and verified by repository CI. No local test pass is claimed.

## Exact verification

| Workflow | Result | Evidence |
|---|---|---|
| Quality | PASS — 503 Python tests + 70 subtests; web checks, parity, benchmarks and Vite build | [45490428639](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45490428639) |
| Chromium | PASS — 42/42 Playwright tests, including typed IPA details | [45490428728](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45490428728) |
| Pinned upstream Rust segmentation | PASS | [45490428786](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45490428786) |
| External khPOS segmentation benchmark | PASS | [45490428814](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45490428814) |

Parity counts: 129 structural, 38 lexical, 46 consonant/rule and 6 segmentation fixtures. Typed IPA status, segments, boundaries and target result are included in the consonant/rule output parity.

The 39-input benchmark and measured overhead/runner variance are recorded in `docs/research/KHMER-ENGINE-BENCHMARK-2026-11-24.md`. These are engineering coverage and throughput measures, not phonetic accuracy.

## Reconciliation

- PR #519 was inspected and left open/untouched because it is a separate diverged hybrid-inference change (73 commits ahead / 200 behind, non-mergeable).
- No other user branches were deleted or rewritten.
- No main-branch merge, Pages deployment, release tag, or external setting change was performed.
- Independent adjudicated Khmer IPA gold remains empty; pronunciation accuracy remains NOT_ASSESSED.
