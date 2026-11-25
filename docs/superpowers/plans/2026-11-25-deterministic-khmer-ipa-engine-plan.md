# Deterministic Neural-Distilled Khmer IPA Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a browser-local deterministic Khmer-to-Ukrainian phonetic engine from the licensed Google Khmer phonemic lexicon and an offline neural G2P teacher trained on that corpus. The final site runtime loads only static rules/lexicon and never runs a neural model.

**Architecture:** Use the pinned Google Khmer pronunciation lexicon (CC BY 4.0) as the large source-backed phonemic lexical layer. Convert its custom phonemic tokens through an explicit, provenance-aware token-to-IPA adapter. Train a project-owned neural teacher offline with a correct phone-token target tokenizer (not a character-level approximation). Distill validated teacher behavior into static deterministic lexical/context rules. The existing IPA-to-Ukrainian adapter remains the only practical-orthography path.

**Tech Stack:** Python 3.12, PyTorch CPU for offline teacher training, pinned Google source TSV + Festvox phonology inventory, Python/JavaScript shared token map, existing typed IPA result and Ukrainian adapter, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-11-25-deterministic-khmer-ipa-engine-design.md`

## Global Constraints

- Preserve `Khmer orthography → structural analysis → source phonology/phonemic representation → typed IPA → Ukrainian IPA adaptation → Ukrainian practical orthography`.
- Do not generate Ukrainian output independently from source graphemes while displaying IPA only as an audit side channel.
- The final site runtime must not load model weights, import ONNX Runtime, call a model API, or perform neural inference.
- Google source phonemic strings are not already project IPA. Convert through a dedicated, typed, inspectable adapter.
- Preserve the four multi-pronunciation Google lexical entries as candidate arrays; never choose a variant arbitrarily. Preserve blank rows as unresolved.
- Preserve syllable boundaries (`.`), vowel length, phoneme inventory, source row provenance, source revision/hash, IPA kind, status and uncertainty.
- The Google lexicon and phonology inventory are CC BY 4.0; keep attribution with any derivative.
- The external NPanha model repo has MIT code but no committed checkpoint or training TSV. Its reported metrics are not reproducible project evidence. Re-train from the pinned Google source; do not claim its metrics as ours.
- The NCKL model outputs Khmer-script respelling, not IPA. Its split-syllable bridge currently degrades source concordance; keep it as a negative-control diagnostic only unless an alternate boundary mode proves otherwise.
- The MekongPhon direct IPA model failed the six-case source-concordance gate under greedy and beam-4. Do not promote it as the primary teacher.
- Accuracy remains NOT_ASSESSED until independent adjudicated IPA gold exists. Source-attested diagnostic CER and neural teacher/student agreement are not accuracy.
- Strict accuracy > Soft > Super-soft; Soft result coverage > Strict; Super-soft non-empty result coverage = 100%. Report complete IPA, supported, provisional, partial and unresolved coverage separately.
- Preserve the existing Python/JavaScript parity and Ukrainian adapter. Keep main/deployed site unchanged until the replacement is verified.
- Do not merge, deploy, publish a release, or choose a project license on the owner's behalf.

## Review Focus

1. **Token inventory drift:** every non-empty lexicon phone must exist in the pinned Google phonology inventory and the IPA map. Unknown tokens fail validation.
2. **Multi-character phones:** `ph`, `th`, `kh`, `ch`, doubled vowels and diphthongs are single phonemic tokens, not character sequences.
3. **Syllable boundaries and length:** `.` and long-vowel phones must survive tokenization, training, IPA conversion and serialization.
4. **Profile conflicts:** source-attested conflicts in aspiration, glottal stops and vowel length remain explicit; no global normalization that hides them.
5. **Duplicate pronunciations and blank entries:** retain variants; do not silently select or invent pronunciations.
6. **Model split leakage:** all variants of one normalized spelling belong to the same train/dev/test split.
7. **OOV behavior:** deterministic rules must return an explicitly uncertain candidate or unresolved status; never claim complete IPA from a partial onset.

---

### Task 1: Finish the NCKL bridge negative-control diagnostic

**Files:**
- Modify: `scripts/benchmark_nckl_phonemizer_bridge.py`
- Modify: `tests/test_benchmark_nckl_phonemizer_bridge.py`
- Existing CI job: `nckl-phonemizer-bridge` in `.github/workflows/ci.yml`

- [x] **Step 1: Test the split-syllable bridge first**
  - Direct Khmer Phonemizer: 11/12 exact, 0.99% CER.
  - NCKL respelling split into syllables then phonemized separately: 8/12 exact, 6.93% CER.
  - The split-syllable bridge fails the screening gate.

- [x] **Step 2: Add boundary-mode tests before implementation**
  - Whole respelling (hyphens preserved and passed to phonemizer once).
  - Spaces substituted for hyphens and passed to phonemizer once.

- [x] **Step 3: Run all three variants on the same 12 source-attested inputs**
  - Exact diagnostic artifact from run 45653367069: direct Khmer Phonemizer 11/12 exact, 0.99% CER; split-syllable bridge 8/12 exact, 6.93% CER; whole-string and spaced-string variants each 7/12 exact, 6.93% CER.
  - Aggregate-only artifact retained hashes and metrics; no raw words, respellings, source IPA or generated IPA were retained.
  - All three NCKL bridge modes underperform the direct deterministic phonemizer; NCKL is rejected as an engine/teacher bridge and not integrated.

- [x] **Step 4: Record the final decision**
  - Mark the diagnostic `DONE_VERIFIED` as a negative control: run 45653367069, code head `a70f304cba563a78dc87b79bc0177901eda38b8f`.
  - Retain the NCKL model only as a research reference; do not call it the primary engine or use its outputs in the runtime.

### Task 2: Validate the Google phonemic source and define a typed phonemic → IPA adapter

**Files:**
- Create: `data/khmer/google-phonology.json` (pinned source inventory)
- Create: `data/khmer/google-phonemic-to-ipa.json`
- Create: `src/khmer_ua/google_phonemic.py`
- Create: `src/google-phonemic-ipa.js`
- Create: `scripts/validate_google_phonemic_lexicon.py`
- Create: `tests/test_google_phonemic_ipa.py`
- Create: `tests/google-phonemic-ipa.test.mjs`
- Modify: `src/khmer-ipa-result.js` to preserve explicit IPA kind in browser results
- Read: `data/khmer/google-pronunciation-full.tsv`
- Read: pinned Google `km/festvox/phonology.json`

**Source facts to verify in code/tests:**
- Google source commit: `a90601024f07ab7e96c911243324e0adeb16da96`.
- Khmer rows: 62,179; non-empty phonemic outputs: 62,118; empty outputs: 61; unique spellings with non-empty outputs: 62,114; four words have multiple pronunciation variants.
- Distinct observed Khmer phone tokens: 54; all 54 occur in the pinned 56-phone phonology inventory; `sil` and `pau` are unused.
- Preliminary token map: 6/6 R12A vowel-context examples exact; 3/7 source-attested lexical sample exact. These are source-concordance diagnostics, not accuracy.

**Interfaces:**
- Python `parse_google_phonemic(raw: str, mapping: dict) -> GooglePhonemicResult`.
- JavaScript `parseGooglePhonemic(raw, mapping) -> GooglePhonemicResult`.
- The intermediate representation is explicitly `GOOGLE_PHONEMIC`, not IPA.
- The adapter returns IPA with `ipa_kind="PHONEMIC"`, preserves `.` syllable boundaries, and records mapping status/provenance/uncertainty.
- Unknown or unsupported phone tokens return unresolved/partial status; no guessed mapping.
- `ie → iə` is allowed only with the recorded R12A source evidence. Other diphthong mappings remain explicit and provisional unless corroborated.

- [x] **Step 1: Write failing tests first**
  - Every observed source token exists in the pinned source inventory.
  - Every token is either explicitly mapped or explicitly unresolved.
  - Long vowels map to IPA length marks.
  - Syllable dots are preserved.
  - Multi-character phones are tokenized as one unit.
  - Unknown tokens fail closed.
  - The six R12A examples map exactly.
  - The four source lexical conflicts remain conflicts and are not promoted.
  - `ipa_kind="PHONEMIC"` survives serialization and Ukrainian adaptation.

- [x] **Step 2: Verify RED**
  - Run focused Python and JavaScript tests; confirm missing parser/schema fails.

- [x] **Step 3: Add the pinned phonology inventory and evidence-bearing token map**
  - Record Google revision, source URL, CC BY 4.0, source file hash and token evidence.
  - Mark mappings corroborated only when source examples support them; mark the rest provisional.
  - `sil` and `pau` remain non-lexical boundary/silence tokens, not guessed phones.

- [x] **Step 4: Implement Python and JavaScript adapters**
  - Parse space-delimited phonemic tokens and explicit dot boundaries.
  - Convert only mapped tokens to IPA.
  - Validate the output through the existing IPA boundary.
  - Preserve phonemic kind and candidate status.

- [x] **Step 5: Run focused tests, source matrix, lexical diagnostic, full Python suite, JS tests and Python/JS parity.** — Quality run 45653367069 succeeded on code-identical adapter/parser/test files; exact-head rerun remains pending.

- [x] **Step 6: Commit** `feat: add Google phonemic to typed IPA adapter`. — Implemented in the continuation branch.

### Task 3: Generate and integrate the deterministic Google lexical layer

**Files:**
- Create: `scripts/build_google_phonemic_lexicon.py`
- Create: `schemas/google-phonemic-ipa-lexicon.schema.json`
- Create: generated `data/khmer/google-phonemic-ipa-lexicon.json`
- Modify: `src/khmer_ua/rule_engine.py`
- Modify: `src/khmer-engine-core.js`
- Modify: `data/khmer/sources.json`
- Update: `data/khmer/GOOGLE_PRONUNCIATION_SAMPLE_ATTRIBUTION.md`
- Test: `tests/test_google_phonemic_lexicon.py`
- Test: `tests/google-phonemic-lexicon.test.mjs`

**Interfaces:**
- `build_lexicon(source_tsv, token_map) -> canonical JSON`.
- Python and JavaScript lookup return the same ordered candidate array.
- Generated JSON is stable: NFC keys, deterministic sort, canonical serialization, no timestamps, stable SHA-256.
- Every entry retains source ID, source row/hash, IPA kind, status, mapping uncertainty and variant index.

- [x] **Step 1: Write tests** for counts, blank rows, duplicate variants, NFC collisions, deterministic rebuild hash, source attribution, unknown-token rejection, and exact/ambiguous lookup.
- [x] **Step 2: Verify RED.**
- [x] **Step 3: Implement the generator** from the already committed TSV; do not duplicate source rows unnecessarily.
- [x] **Step 4: Generate the lexicon and validate its schema, token inventory, row counts and stable hash.**
- [x] **Step 5: Integrate exact-form lookup in Python and browser engines.**
  - All unadjudicated Google entries remain PROVISIONAL.
  - Strict mode may use only separately corroborated entries under existing promotion rules.
  - Ambiguous entries return multiple candidates or an explicit ambiguity status.
  - The existing Ukrainian IPA adapter remains the only practical-orthography path.
- [x] **Step 6: Run Python/JS exact-form, variant, full-message and parity tests.** — Included in successful Quality run 45653367069; exact-head rerun pending.
- [x] **Step 7: Commit** `feat: add deterministic Google Khmer phonemic lexicon`. — Shards and loader are in the branch.

### Task 4: Train a project-owned neural phonemic teacher from the licensed source

**Files:**
- Create: `scripts/train_google_phonemic_teacher.py`
- Create: `scripts/google_teacher/model.py`
- Create: `scripts/google_teacher/tokenization.py`
- Create: `scripts/google_teacher/data.py`
- Create: `tests/test_google_teacher_data.py`
- Create: `tests/test_google_teacher_tokenization.py`
- Create: branch-gated CI workflow job in `.github/workflows/ci.yml`

**Interfaces:**
- Input tokenizer: NFC Khmer grapheme/codepoint sequence with a documented normalization policy.
- Target tokenizer: space-delimited Google phone tokens plus explicit syllable-boundary token `.`; `ph`, `aa`, `ie`, etc. are atomic target tokens, never split into characters.
- Dataset split: deterministic, word-disjoint train/dev/test; all variants of a spelling stay in one split.
- Training config: pinned seed, architecture, epochs, batch size, optimizer, early stopping and CPU thread count.
- Metrics: phoneme-token error rate, word exact match, syllable-boundary accuracy, output coverage, and confusion matrix. These measure prediction of Google source labels, not IPA accuracy.
- Model/checkpoint is an offline research/build artifact only; never ship it in the browser bundle.

- [x] **Step 1: Write tests first** for tokenization, source-row filtering, blank rows, duplicate grouping, deterministic splits, no leakage, and token inventory.
- [x] **Step 2: Verify RED.**
- [x] **Step 3: Implement the smallest reproducible sequence model** using PyTorch CPU with atomic phone-token targets.
- [x] **Step 4: Train on the filtered Khmer-only Google corpus with fixed seed and word-disjoint splits.**
- [x] **Step 5: Evaluate on held-out source phonemic labels; publish no IPA accuracy claim.** — 84.18% exact, 4.33% PER, 100% source-label coverage.
- [x] **Step 6: Save checkpoint/config/data hashes only as a short-lived CI artifact; do not commit weights.** — Run 45653367069, artifact 15043450562.
- [x] **Step 7: Commit** `feat: train offline Google Khmer phonemic teacher`. — Training code and branch-gated CI job are committed.

### Task 5: Distill the neural teacher into a deterministic OOV syllable lookup table

**Files:**
- Create: `scripts/distill_google_teacher.py`
- Create: `schemas/deterministic-khmer-phonology.schema.json`
- Create: `tests/test_distill_google_teacher.py`
- Generated artifact only after verification: `data/khmer/google-neural-distilled-rules.json`

**Interfaces:**
- `distill_teacher(model, syllable_lattice, evidence, config) -> deterministic rule artifact`.
- Candidate rules include source context, onset/register, vowel, coda, syllable position, teacher revision, support count, held-out teacher agreement, source evidence, profile and uncertainty.
- No rule is promoted merely because it matches the teacher.
- The deterministic artifact must not require the model checkpoint.

- [x] **Step 1: Write failing tests** for deterministic ordering/hash, candidate provenance, conflict preservation and no promotion from teacher agreement alone.
- [x] **Step 2: Verify RED.**
- [x] **Step 3: Generate a bounded Khmer orthographic syllable lattice** from existing consonant/register/vowel/sign inventories.
- [x] **Step 4: Use the offline teacher to label the lattice and extract deterministic candidate rows.**
- [x] **Step 5: Measure deterministic-student agreement with the teacher on held-out words and separately compare with source IPA evidence.** — 2,532 candidates; 63.86% exact, 14.19% PER, 98.4% composition coverage.**
- [x] **Step 6: Keep the student PROVISIONAL and evidence-limited; teacher agreement alone never promotes a candidate to SUPPORTED.**
- [x] **Step 7: Commit** the reproducible distillation script and CI artifact generation. Static browser table is regenerated during the Pages build.

### Task 6: Integrate Strict / Soft / Super-soft policies

**Files:**
- Modify: `src/khmer_ua/rule_engine.py`
- Modify: `src/khmer-engine-core.js`
- Modify: `src/main.js`
- Test: Python and browser tier suites

- [x] **Step 1: Write failing tests** for exact lexical hits, ambiguous variants, source conflicts, neural-distilled OOV candidates, unknown names, mixed text, punctuation, Unicode normalization and all three tiers.
- [x] **Step 2: Verify RED.**
- [x] **Step 3: Integrate the deterministic lexical/rule layers behind the existing engine interface.**
- [x] **Step 4: Preserve Strict source-backed output; Google and neural-distilled candidates remain PROVISIONAL and cannot overwrite tier-B output.**
- [ ] **Step 5: Enforce accuracy/coverage ordering on one frozen corpus when gold exists.**
- [x] **Step 6: Add a Super-soft non-empty display coverage contract while reporting full-IPA coverage separately.**
- [x] **Step 7: Remove the standalone ONNX model from production UI/Pages and retain only a same-origin static JSON candidate table.** Exact-head build/browser checks pending.
- [x] **Step 8: Commit** deterministic tiers, Worker/static table loader, Pages build integration and tests in the continuation branch.

### Task 7: Documentation, code review and release gates

**Files:**
- Update in place: `docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md`
- Update in place: `docs/repository-audit.md`
- Update in place: `docs/DETERMINISTIC-RULE-ENGINE.md`
- Update: `README.md` and `docs/implementation.md` only after runtime behavior is verified

- [x] **Step 1: Update task ledger with exact statuses, source revisions, hashes, and blockers.**
- [ ] **Step 2: Run all repository-defined tests, builds, schema/data validation, Python/JS parity, browser tests, benchmark, generated-artifact drift and clean-install checks on exact head.** — Queued at last status check; no pass claim.
- [ ] **Step 3: Perform a read-only whole-branch review against the spec and exact base/head SHAs.** — Pending exact-head CI and final diff review.
- [ ] **Step 4: Fix Critical/Important findings with RED→GREEN tests and one final full-suite run.** — Pending.
- [ ] **Step 5: Report release readiness honestly; do not merge or deploy without the owner's integration decision.** — No merge/deploy performed.

---

## Current task ledger — updated 2026-11-25

- NCKL split-syllable bridge: PARTIAL / negative control; 8/12 exact and 6.93% CER versus direct Khmer Phonemizer 11/12 exact and 0.99% CER. Whole/spaced boundary variants remain TODO; NCKL is not integrated.
- MekongPhon source-matrix gate: DONE_VERIFIED as a failed promotion diagnostic; greedy and beam-4 both 0/6 exact, 44.44% CER. Its public standalone model UI/ONNX deployment is removed by this continuation; archived research remains.
- Google source inventory and typed phonemic→IPA adapter: DONE_VERIFIED on code-identical files in successful Quality run 45653367069; exact-head rerun pending.
- Google deterministic lexical shards and Python/JS lookup: DONE_VERIFIED on code-identical files in successful Quality run 45653367069; exact-head rerun pending.
- Project-owned neural teacher: DONE_VERIFIED by run 45653367069, artifact 15043450562; held-out source-label metrics 84.18% exact, 4.33% PER, 100% label coverage.
- Neural-to-static OOV syllable distillation: DONE_VERIFIED as a research artifact by run 45653367069; 2,532 candidates, 63.86% exact, 14.19% PER, 98.4% composition coverage. Not gold accuracy.
- Strict/Soft/Super-soft runtime integration: PARTIAL; tier filtering, local Google candidates, static neural table lookup, same-origin Worker/fallback and tests implemented; exact-head CI/Chromium pending.
- Pages static table build/deploy: PARTIAL; cache/train/distill/stage/smoke steps implemented; Pages runs only from main and has not yet deployed this branch.
- Independent pronunciation accuracy/profile equivalence: BLOCKED; adjudicated IPA gold remains 0 and Google source-profile equivalence is unverified.
- Release gates: PARTIAL; Quality/Chromium/benchmarks queued at last check; no merge or deployment.
- Workspace ruling: use the isolated remote GitHub branch because the container has no checkout and cannot resolve github.com. GitHub Actions exact-head runs are the verification source; no local repository test execution.
