# SDD ledger — plan: docs/superpowers/plans/2026-11-25-deterministic-khmer-ipa-engine-plan.md

## Workspace

- Branch: `feat/deterministic-neural-distillation-20261125`
- Base: `8838a1f33b03aa1bad7c045c216305bb3e60e3f9`
- PR: #582 (draft)
- Workspace ruling: the container has no repository checkout and cannot resolve github.com; no native worktree tool is exposed. Use the isolated remote GitHub branch as the workspace and exact-head GitHub Actions as verification. Cost if wrong: no local pre-commit test execution; mitigated by CI on every branch push/PR.
- Current integration policy: do not merge or deploy from this task; keep PR #582 draft until deterministic runtime and evidence gates are met.

## Pre-flight

- Python and browser engines already share a typed IPA boundary and existing Ukrainian adapter.
- The current browser MekongPhon model is optional/provisional and must not overwrite canonical deterministic fields.
- The NCKL model outputs Khmer-script respelling with hyphen syllable boundaries, not IPA.
- The deterministic phonemizer accepts Khmer script and returns IPA; the current experiment tests whether NCKL respelling improves its output.
- No independent IPA gold exists. Source-attested diagnostic results are not accuracy.

## Task 1 — NCKL respelling → deterministic IPA bridge diagnostic

Status: PARTIAL; focused tests passed on an intermediate commit; exact-head model bridge job pending.

- Test-first commit `f1f3bb58bbcd31abd99cbe216a8cfe49f93852fa` added `tests/test_benchmark_nckl_phonemizer_bridge.py` before the implementation.
- Expected RED confirmed in Quality run [45642382335](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45642382335): collection failed because `scripts/benchmark_nckl_phonemizer_bridge.py` did not exist.
- Implementation added in `d0baf521b9e2729ab32c16ae742d066eb7916fbd`; report newline corrected in `980b1408aed0f459a638cda2049a2661965de686`.
- Focused/full Quality test job passed at commit `980b1408aed0f459a638cda2049a2661965de686` in run [45642506251](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45642506251). This is not the current head.
- Branch-gated CI job `nckl-phonemizer-bridge` was added in commit `0635b69b943eaf7d43e92b89ca8472cd4e3b9ece`. It installs the pinned NCKL model and Khmer Phonemizer, runs both direct and bridged pipelines on the same source-attested corpus, and uploads only aggregate metrics and hashes.
- Exact-head bridge result: PENDING. Inspect run [45642540955](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45642540955) and subsequent exact-head runs before updating status.

## Completed diagnostic — MekongPhon teacher gate

Status: DONE_VERIFIED as a diagnostic only; NOT selected as primary teacher.

- Source matrix contains six non-conflicting cases with non-empty IPA.
- Greedy: 0/6 exact; codepoint CER 44.44%.
- Beam-4: 0/6 exact; codepoint CER 44.44%.
- Push run [45641401954](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45641401954) and PR run [45641415788](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45641415788) completed successfully on the diagnostic branch head.
- Interpretation: not an accuracy score; this narrow source-concordance gate fails. Do not distill MekongPhon into production phonological rules.
- Ruling: keep MekongPhon as a research/diagnostic candidate only — it has no exact match on the six available source examples in either decode mode and profile equivalence is unverified. Cost if wrong: a useful model may be excluded due to source/profile convention mismatch; retain the model and report as an optional research candidate rather than deleting it.

## Task 2 — Typed respelling representation

Status: TODO; gated on Task 1 bridge result. No production parser/schema has been added.

## Task 3 — Deterministic respelling-to-IPA adapter

Status: TODO; requires validated NCKL respelling semantics and source-backed contextual mappings. The current 54 R12A mapping observations are explicitly `runtime_eligible=false`; do not promote them directly.

## Task 4 — Offline deterministic-student compiler

Status: BLOCKED / RIGHTS_REVIEW_REQUIRED until source/output rights and profile requirements are established. NCKL model weights are MIT per model card; underlying NCKL dictionary is copyrighted by NCKL and no blanket dataset redistribution license is declared. No NCKL training rows or raw model outputs are copied into the repository.

## Task 5 — Python/browser runtime integration

Status: TODO after Tasks 1–4. No site runtime behavior is changed by this branch so far. Final runtime must use static versioned data and the existing IPA → Ukrainian adapter; no ONNX/model inference dependency.

## Task 6 — Strict/Soft/Super-soft evaluation

Status: BLOCKED because independent adjudicated IPA gold remains 0. Existing user requirement retained: Strict accuracy > Soft > Super-soft; Soft coverage > Strict; Super-soft result coverage 100%. Measure complete IPA, provisional, partial, and unresolved coverage separately.

## Task 7 — Documentation and release gates

Status: PARTIAL. Design, plan, progress ledger, master handoff, repository audit, and deterministic engine doc updated. Exact-head tests, NCKL bridge result, final code review, and release-readiness decision remain pending.

## Rulings

1. Use remote GitHub branch instead of local worktree because the local environment has no checkout and network DNS to github.com fails. Cost: no local verification; mitigate with CI on exact SHAs.
2. Do not promote MekongPhon as primary teacher after 0/6 and 44.44% CER under both greedy and beam-4. Cost: a profile mismatch may explain some differences; preserve as diagnostic candidate, not production teacher.
3. Test NCKL respelling + deterministic IPA phonemizer as an alternate teacher bridge because its own held-out respelling benchmark is materially stronger (83.16% exact, 4.16% CER, 93.06% syllable-count accuracy) and exposes syllable boundaries. Cost: this is not IPA accuracy; bridge and profile must pass independent evaluation.
4. Do not use the advertised 29,204-entry Khmer Acoustic Model dictionary: the pinned repository lacks the full dictionary/model artifacts and its license declarations conflict. Cost: losing a potentially valuable lexicon; revisit only if the complete artifacts and rights are supplied.
5. Do not ship generated NCKL-derived outputs until rights review and independent phonetic validation. Cost: slower coverage expansion; avoids redistributing unlicensed data or presenting unverified pronunciations as supported.

## Latest commands/evidence

- Container inspection: `pwd`, `ls -la`, `git rev-parse --show-toplevel`, `git branch --show-current`; result: no repository checkout.
- Local clone attempt: `git clone --filter=blob:none --no-checkout https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System.git`; blocked by DNS resolution (`Could not resolve host: github.com`).
- Remote GitHub Actions are the only executable repository verification environment in this session.
