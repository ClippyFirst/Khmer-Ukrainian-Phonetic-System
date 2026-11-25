# Deterministic Neural-Distilled Khmer IPA Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace per-request neural inference with a deterministic browser-local Khmer IPA engine whose rules and lexical data were developed with an offline neural teacher and whose IPA flows through the existing Ukrainian adapter.

**Architecture:** Use the NCKL G2P model as a research-time teacher for Khmer-script pronunciation respelling, then use a deterministic phonemizer to map respellings to IPA. If the same-input bridge diagnostic passes, compile approved outputs and contextual decisions into static, versioned rules/lexical data consumed by the existing Python and JavaScript engines. The final runtime loads no model weights and makes no inference request.

**Tech Stack:** Python 3.12, PyTorch CPU + pinned `khmer-g2p` for offline teacher inference, `khmerphonemizer==0.0.3` as a deterministic IPA candidate, existing JavaScript site engine, existing typed IPA adapter, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-11-25-deterministic-khmer-ipa-engine-design.md`

## Global Constraints

- Preserve `Khmer orthography → structural analysis → source phonology/respelling → typed IPA → Ukrainian IPA adaptation → practical Ukrainian orthography`.
- No Ukrainian output may be generated independently from source graphemes while IPA is only an audit side channel.
- The final site runtime must not load NCKL/MekongPhon weights, import ONNX Runtime, call an inference API, or depend on network inference.
- All generated rules/entries carry source/model revision, hashes, target profile, IPA kind, evidence status, uncertainty, and rights status.
- Model outputs and source-attested comparisons are not independent IPA gold; accuracy remains null until expert-adjudicated gold exists.
- Never redistribute NCKL training rows or MekongPhon corpus data without explicit rights evidence.
- Keep source-conflicting analyses separate; no silent pronunciation guesses.
- Strict accuracy must exceed Soft, Soft coverage must exceed Strict, and Super-soft must return a non-empty best-effort result for 100% of accepted Khmer inputs; report complete-IPA and supported-IPA coverage separately.
- Preserve existing Python/JavaScript parity, Ukrainian adapter behavior, and the current deployed main branch until a validated replacement exists.
- Use a dedicated branch; do not merge, deploy, release, or choose a license on the owner's behalf.

## Review Focus

1. **Malformed teacher respelling** (empty syllables, doubled/trailing hyphens, whitespace-only output) — reject or mark unresolved; never silently concatenate invalid syllables.
2. **Multi-syllable boundaries and stress** (hyphens in respelling vs dots/spaces/stress in IPA references) — preserve boundaries and normalize only the explicitly allowed notation markers in diagnostic comparisons.
3. **Register/vowel/coda context** (first/second series, shifters, open/closed syllables, NIKAHIT/REAHMUK) — no context-free vowel-sign mapping; tests must cover contextual variants and unresolved cases.
4. **Unknown lexical forms** (names, compounds, unseen syllable combinations) — use deterministic fallback with explicit uncertainty; never claim full IPA when only onset/partial output exists.
5. **Profile and rights mismatch** (NCKL training data, model-derived outputs, external IPA convention) — block distribution/promotion unless the required rights and profile evidence exist.

---

### Task 1: Complete the NCKL-respelling → deterministic-IPA bridge diagnostic

**Files:**
- Create: `scripts/benchmark_nckl_phonemizer_bridge.py`
- Create: `tests/test_benchmark_nckl_phonemizer_bridge.py`
- Modify: `.github/workflows/ci.yml`
- Read: `data/tests/verified-lexical-corpus.json`
- Read: `scripts/benchmark_nckl_respelling.py`, `scripts/benchmark_g2p.py`

**Interfaces:**
- `phonemize_respelling(respelling: str, phonemizer: Callable[[str], Any]) -> str` splits only at explicit NCKL hyphen boundaries, phonemizes each syllable, and joins IPA syllables with dots.
- `build_report(corpus, respellings, direct_outputs, bridge_outputs, *, model_revision, phonemizer_version, corpus_sha256, runtime=None) -> dict` emits aggregate-only source-attested diagnostics.
- NCKL model revision: `7dbc6c3d1c1f5a9a8763be602fa679f130f20dca`; model output is Khmer-script respelling, not IPA.
- Phonemizer: `khmerphonemizer==0.0.3`.

- [x] **Step 1: Write the failing tests first**
  - `test_respelling_bridge_preserves_model_syllable_boundaries`
  - `test_respelling_bridge_rejects_empty_syllables_and_non_string`
  - `test_source_ipa_comparison_key_removes_notation_only`
  - `test_bridge_report_is_aggregate_only_and_never_accuracy`
  - `test_bridge_report_rejects_misaligned_prediction_maps`

- [x] **Step 2: Verify RED**
  - CI run `45642382335` failed during collection because the script did not exist. This is the expected test-first failure.

- [x] **Step 3: Implement the bridge diagnostic**
  - Run the NCKL model only in CI/offline research.
  - Compare direct Khmer Phonemizer with NCKL respelling split into syllables and passed to the same deterministic phonemizer.
  - Store only hashes, case indices and aggregate metrics; do not store words, source IPA, respellings or generated IPA.

- [ ] **Step 4: Verify GREEN and inspect the exact-head bridge run**
  - Run: `pytest -q tests/test_benchmark_nckl_phonemizer_bridge.py`
  - Run the full `Quality checks` workflow and `nckl-phonemizer-bridge` job on the final branch SHA.
  - Expected: all tests pass; workflow reports direct and bridged source-attested CER/exact counts, with `accuracy=null` and `independent_gold_count=0`.
  - Continue only if bridge output coverage is not lower, exact matches do not decrease, and CER improves by at least 20% relative. Otherwise mark this teacher path non-production and do not integrate it.

- [ ] **Step 5: Record the diagnostic decision**
  - If it passes the screening gate, proceed to Task 2.
  - If it fails, record `BLOCKED` and investigate a different teacher or source-only expansion; do not force a rule promotion.

### Task 2: Define a typed Khmer pronunciation-respelling intermediate representation

**Files:**
- Create: `schemas/khmer-respelling.schema.json`
- Create: `src/khmer_ua/respelling.py`
- Create: `src/khmer-respelling.js`
- Test: `tests/test_khmer_respelling.py`
- Test: `tests/khmer-respelling.test.mjs`

**Interfaces:**
- Python `parse_respelling(raw: str, *, provider: str, revision: str, profile: str) -> KhmerRespelling`.
- JavaScript `parseKhmerRespelling(raw, provenance) -> KhmerRespelling`.
- Shared fields: NFC raw text, ordered syllable array, exact separator/boundary provenance, provider/model revision, target profile, evidence status, uncertainty, and parse errors.
- The respelling representation is explicitly not IPA and cannot be passed directly to the Ukrainian IPA adapter.

- [ ] **Step 1: Write tests** for one syllable, multiple hyphen-delimited syllables, Unicode NFC, leading/trailing/doubled separators, empty input, unsupported characters, and provenance preservation.
- [ ] **Step 2: Run tests and verify expected RED** because the parser/schema do not exist.
- [ ] **Step 3: Implement the smallest Python and JavaScript parsers** from the shared schema; do not infer phonetic values.
- [ ] **Step 4: Run focused tests, full Python tests, JS checks, and cross-runtime structural parity.**
- [ ] **Step 5: Commit** `feat: add typed Khmer pronunciation respelling boundary`.

### Task 3: Build and validate deterministic respelling → IPA adaptation

**Files:**
- Create or modify: `src/khmer_ua/respelling_ipa.py`
- Create or modify: `src/khmer-respelling-ipa.js`
- Modify: `data/khmer/vowel-context-register.json` only when source evidence supports an explicit new record
- Test: `tests/test_respelling_ipa.py`
- Test: `tests/respelling-ipa.test.mjs`

**Interfaces:**
- Python `respelling_to_ipa(value: KhmerRespelling) -> TypedPhoneticResult`.
- JavaScript `respellingToIpa(value) -> TypedPhoneticResult`.
- Output kinds/statuses must be explicit; unknown vowels/codas remain unresolved or provisional, never silently guessed.
- The same typed result must be consumable by the existing Ukrainian adapter.

- [ ] **Step 1: Write tests** for first/second series, shifters, independent/dependent vowels, coda, NIKAHIT, REAHMUK, consonant clusters, syllable boundaries, long vowels, and unsupported combinations.
- [ ] **Step 2: Run focused tests and verify RED.**
- [ ] **Step 3: Inspect the pinned Khmer Phonemizer implementation and its license; port only the deterministic rules required by the validated respelling grammar.** Do not import a Python-only runtime into the browser.
- [ ] **Step 4: Implement the smallest adapter that produces typed IPA and explicit uncertainty.**
- [ ] **Step 5: Run focused tests, existing IPA adapter tests, Python/JS parity, and full-message fixtures.**
- [ ] **Step 6: Commit** `feat: map validated Khmer respelling to typed IPA`.

### Task 4: Build the offline deterministic-student compiler

**Files:**
- Create: `scripts/distill_nckl_rules.py`
- Create: `schemas/deterministic-khmer-ipa-lexicon.schema.json`
- Create: `tests/test_distill_nckl_rules.py`
- Generated output (only after rights gate): `data/khmer/nckl-distilled-ipa-lexicon.json`

**Interfaces:**
- `compile_distilled_lexicon(inputs, respellings, ipa_candidates, provenance) -> dict`.
- The compiler must be deterministic: stable sort, NFC keys, no timestamps in the compiled artifact, canonical JSON, stable SHA-256.
- The compiler must refuse distribution output unless an explicit rights status and rights evidence locator are supplied.
- Entries remain `PROVISIONAL` until source/profile review; teacher agreement is recorded separately from accuracy.
- The artifact contains no raw NCKL training rows.

- [ ] **Step 1: Write failing tests** for stable ordering/hash, duplicate NFC keys, missing outputs, malformed IPA, provenance, rights refusal, exact-form-only lookup, and no accidental generalization.
- [ ] **Step 2: Run tests and verify RED.**
- [ ] **Step 3: Implement the compiler and research-only output mode.**
- [ ] **Step 4: Generate a small research artifact only if the bridge diagnostic passes; do not commit or deploy it while NCKL-derived-output rights remain unresolved.**
- [ ] **Step 5: Validate schema and deterministic rebuild equality.**
- [ ] **Step 6: Commit** `feat: compile evidence-gated deterministic IPA lexicon` only when rights and source acceptance permit it; otherwise record `BLOCKED`.

### Task 5: Integrate the deterministic student into Python and the browser

**Files:**
- Modify: `src/khmer_ua/rule_engine.py`
- Modify: `src/khmer-engine-core.js`
- Modify: `src/main.js`
- Modify: `src/khmer-engine.js` or the existing app entrypoint as needed
- Test: existing engine suites plus new full-message parity fixtures

**Interfaces:**
- Both runtimes use the same versioned deterministic lexicon/rule artifact and return the same typed IPA status, provenance, uncertainty, and Ukrainian adaptation.
- The existing deterministic engine remains the fallback and canonical source-supported path.
- Model-derived entries are a separate provisional layer; they cannot overwrite supported canonical fields without satisfying the promotion policy.

- [ ] **Step 1: Write failing Python and browser tests** for exact lexicon hits, contextual rule hits, unknown words, mixed text, punctuation, spaces, Unicode normalization, and each confidence tier.
- [ ] **Step 2: Verify RED.**
- [ ] **Step 3: Integrate the compiled deterministic student behind the existing engine interface.**
- [ ] **Step 4: Remove neural inference from the primary user flow only after the deterministic path is functional and verified; retain offline research scripts separately.**
- [ ] **Step 5: Run Python/JS structural, lexical, rule, segmentation and full-message parity tests.**
- [ ] **Step 6: Build the static site and verify no ONNX/model assets or model-network requests are required by the production bundle.**
- [ ] **Step 7: Commit** `feat: use deterministic neural-distilled Khmer IPA engine`.

### Task 6: Validate Strict / Soft / Super-soft coverage and accuracy

**Files:**
- Modify: `scripts/ipa_gold_corpus.py` only if schema changes are required
- Modify: existing benchmark scripts and tier policy docs
- Test: frozen independent IPA gold benchmark

- [ ] **Step 1: Confirm lawful, profile-compatible, expert-adjudicated IPA gold exists.** If not, record `BLOCKED`; do not substitute source-attested or model-generated outputs.
- [ ] **Step 2: Freeze train/dev/test manifests and independent adjudication provenance.**
- [ ] **Step 3: Run all three tiers on the same frozen inputs.**
- [ ] **Step 4: Assert Strict accuracy > Soft > Super-soft; Soft coverage > Strict; Super-soft non-empty result coverage = 100%.**
- [ ] **Step 5: Report complete IPA coverage, supported IPA coverage, provisional coverage, partial output and unresolved output separately.**
- [ ] **Step 6: Commit** `test: enforce deterministic engine tier coverage and accuracy policy`.

### Task 7: Close out documentation and release gates

**Files:**
- Update in place: `docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md`
- Update in place: `docs/repository-audit.md`
- Update in place: `docs/DETERMINISTIC-RULE-ENGINE.md`
- Update: `README.md` and `docs/implementation.md` only after runtime behavior is verified

- [ ] **Step 1: Update task ledger with exact statuses and evidence.**
- [ ] **Step 2: Run all repository-defined tests, builds, parity checks, browser tests, schema/data validation and generated-artifact drift checks on the exact head.**
- [ ] **Step 3: Perform a read-only whole-branch code review using the plan/spec and exact base/head SHAs.**
- [ ] **Step 4: Fix Critical/Important findings with RED→GREEN tests and one final full-suite run; ledger Minor findings as deferred.**
- [ ] **Step 5: Report release readiness honestly. Do not merge or deploy without the owner's integration decision.**

---

## Current task ledger at plan creation

- Task 1 diagnostic implementation: PARTIAL; tests have a RED run and the script/workflow exist; exact-head NCKL bridge result pending.
- MekongPhon source-matrix gate: DONE_VERIFIED as a diagnostic; 0/6 exact, 44.44% CER for greedy and beam-4; no rule promotion.
- Tasks 2–7: TODO or BLOCKED by the gates above; no deterministic student is yet integrated into the site.
- Ruling: use the remote GitHub branch as the isolated workspace because this environment has no repository checkout and cannot resolve github.com; GitHub Actions must provide exact-head verification. Cost if wrong: no local pre-commit test execution, mitigated by branch-gated CI.
