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

- [ ] **Step 3: Run all three variants on the same 12 source-attested inputs**
  - Compare direct, split, whole-string and spaced-string output.
  - Store only hashes and aggregate metrics; do not retain raw words, respellings, source IPA or generated IPA.
  - Run focused tests and exact-head CI.
  - If neither whole nor spaced mode improves on direct, close this branch as a failed bridge and do not integrate NCKL.

- [ ] **Step 4: Record the final decision**
  - Mark the diagnostic `DONE_VERIFIED` with exact run/commit.
  - Retain NCKL only as a research candidate; do not call it the primary engine.

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

- [ ] **Step 1: Write failing tests first**
  - Every observed source token exists in the pinned source inventory.
  - Every token is either explicitly mapped or explicitly unresolved.
  - Long vowels map to IPA length marks.
  - Syllable dots are preserved.
  - Multi-character phones are tokenized as one unit.
  - Unknown tokens fail closed.
  - The six R12A examples map exactly.
  - The four source lexical conflicts remain conflicts and are not promoted.
  - `ipa_kind="PHONEMIC"` survives serialization and Ukrainian adaptation.

- [ ] **Step 2: Verify RED**
  - Run focused Python and JavaScript tests; confirm missing parser/schema fails.

- [ ] **Step 3: Add the pinned phonology inventory and evidence-bearing token map**
  - Record Google revision, source URL, CC BY 4.0, source file hash and token evidence.
  - Mark mappings corroborated only when source examples support them; mark the rest provisional.
  - `sil` and `pau` remain non-lexical boundary/silence tokens, not guessed phones.

- [ ] **Step 4: Implement Python and JavaScript adapters**
  - Parse space-delimited phonemic tokens and explicit dot boundaries.
  - Convert only mapped tokens to IPA.
  - Validate the output through the existing IPA boundary.
  - Preserve phonemic kind and candidate status.

- [ ] **Step 5: Run focused tests, source matrix, lexical diagnostic, full Python suite, JS tests and Python/JS parity.**

- [ ] **Step 6: Commit** `feat: add Google phonemic to typed IPA adapter`.

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

- [ ] **Step 1: Write tests** for counts, blank rows, duplicate variants, NFC collisions, deterministic rebuild hash, source attribution, unknown-token rejection, and exact/ambiguous lookup.
- [ ] **Step 2: Verify RED.**
- [ ] **Step 3: Implement the generator** from the already committed TSV; do not duplicate source rows unnecessarily.
- [ ] **Step 4: Generate the lexicon and validate its schema, token inventory, row counts and stable hash.**
- [ ] **Step 5: Integrate exact-form lookup in Python and browser engines.**
  - All unadjudicated Google entries remain PROVISIONAL.
  - Strict mode may use only separately corroborated entries under existing promotion rules.
  - Ambiguous entries return multiple candidates or an explicit ambiguity status.
  - The existing Ukrainian IPA adapter remains the only practical-orthography path.
- [ ] **Step 6: Run Python/JS exact-form, variant, full-message and parity tests.**
- [ ] **Step 7: Commit** `feat: add deterministic Google Khmer phonemic lexicon`.

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

- [ ] **Step 1: Write tests first** for tokenization, source-row filtering, blank rows, duplicate grouping, deterministic splits, no leakage, and token inventory.
- [ ] **Step 2: Verify RED.**
- [ ] **Step 3: Implement the smallest reproducible sequence model** using PyTorch CPU. Reuse MIT upstream architecture only with attribution and corrected phoneme-token target encoding.
- [ ] **Step 4: Train on the filtered Khmer-only Google corpus with fixed seed and word-disjoint splits.**
- [ ] **Step 5: Evaluate on held-out source phonemic labels; publish no IPA accuracy claim.**
- [ ] **Step 6: Save checkpoint/config/data hashes only as a short-lived CI artifact; do not commit weights.**
- [ ] **Step 7: Commit** `feat: train offline Google Khmer phonemic teacher`.

### Task 5: Distill the neural teacher into deterministic rules and OOV tables

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

- [ ] **Step 1: Write failing tests** for deterministic ordering/hash, context specificity, conflict preservation, unsupported contexts, and no promotion from teacher agreement alone.
- [ ] **Step 2: Verify RED.**
- [ ] **Step 3: Generate a bounded Khmer orthographic syllable lattice** from existing consonant/register/vowel/sign inventories.
- [ ] **Step 4: Use the offline teacher to label the lattice and extract candidate context rules.**
- [ ] **Step 5: Measure deterministic-student agreement with the teacher on held-out words and separately compare with source IPA evidence.**
- [ ] **Step 6: Keep the student research-only unless independent evidence and rights gates pass.**
- [ ] **Step 7: Commit** `feat: distill neural Khmer phonology into deterministic rules` only when the artifact is reproducible and evidence-gated.

### Task 6: Integrate Strict / Soft / Super-soft policies

**Files:**
- Modify: `src/khmer_ua/rule_engine.py`
- Modify: `src/khmer-engine-core.js`
- Modify: `src/main.js`
- Test: Python and browser tier suites

- [ ] **Step 1: Write failing tests** for exact lexical hits, ambiguous variants, source conflicts, model-distilled OOV rules, unknown names, mixed text, punctuation, Unicode normalization and all three tiers.
- [ ] **Step 2: Verify RED.**
- [ ] **Step 3: Integrate the deterministic lexical/rule layers behind the existing engine interface.**
- [ ] **Step 4: Preserve canonical source-supported results; model-derived rules remain PROVISIONAL and cannot overwrite them.**
- [ ] **Step 5: Enforce accuracy/coverage ordering on one frozen corpus when gold exists.**
- [ ] **Step 6: Verify Super-soft 100% non-empty result coverage while reporting partial/unresolved IPA separately.**
- [ ] **Step 7: Verify the site runtime has no ONNX/model assets or inference/network dependency.**
- [ ] **Step 8: Commit** `feat: integrate deterministic neural-distilled Khmer IPA engine`.

### Task 7: Documentation, code review and release gates

**Files:**
- Update in place: `docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md`
- Update in place: `docs/repository-audit.md`
- Update in place: `docs/DETERMINISTIC-RULE-ENGINE.md`
- Update: `README.md` and `docs/implementation.md` only after runtime behavior is verified

- [ ] **Step 1: Update task ledger with exact statuses, source revisions, hashes, and blockers.**
- [ ] **Step 2: Run all repository-defined tests, builds, schema/data validation, Python/JS parity, browser tests, benchmark, generated-artifact drift and clean-install checks on exact head.**
- [ ] **Step 3: Perform a read-only whole-branch review against the spec and exact base/head SHAs.**
- [ ] **Step 4: Fix Critical/Important findings with RED→GREEN tests and one final full-suite run.**
- [ ] **Step 5: Report release readiness honestly; do not merge or deploy without the owner's integration decision.**

---

## Current task ledger at plan amendment

- NCKL split-syllable bridge: DONE_VERIFIED as a failed diagnostic; 8/12 exact, 6.93% CER versus direct Khmer Phonemizer 11/12 exact, 0.99% CER. Whole/spaced boundary variants pending.
- MekongPhon source-matrix gate: DONE_VERIFIED as a failed diagnostic; greedy and beam-4 both 0/6 exact, 44.44% CER.
- Google phonemic source inventory: PARTIAL; source rows, token inventory, preliminary token map and 6/6 R12A concordance verified; dedicated parser/adapter/tests not yet implemented.
- Google deterministic lexicon generator/integration: TODO.
- Project-owned neural teacher: TODO; training data is available and licensed, but reproducible model training is not yet implemented.
- Deterministic rule distillation: TODO.
- Strict/Soft/Super-soft gold validation: BLOCKED because independent adjudicated IPA gold remains 0.
- Runtime integration and release gates: TODO.
- Workspace ruling: use the isolated remote GitHub branch because the container has no repository checkout and cannot resolve github.com. Exact-head GitHub Actions are the verification source; this means no local pre-commit test execution.
