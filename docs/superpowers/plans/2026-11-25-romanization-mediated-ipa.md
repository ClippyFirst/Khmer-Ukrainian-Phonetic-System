# Romanization-mediated IPA Implementation Plan

> **For agentic workers:** Implement task-by-task with test-first changes and a final branch review.

**Goal:** Add a conservative, contextual romanization-mediated provisional IPA path to the existing “Українська через романізацію” mode.

**Architecture:** Preserve the current BGN/PCGN orthographic output as a separate lane. Add a source-aligned adapter that may expose only consonant-onset IPA already registered for the matching Khmer grapheme and confirmed against the PCGN romanization class; all vowels, codas, syllable roles, and contrasts not resolved by evidence remain explicit unknown spans. Route every phonetic Ukrainian candidate through the existing typed IPA target adapter. Mirror semantics in Python and JavaScript.

**Tech Stack:** JavaScript ES modules, Python, Node test runner, pytest, Vite, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-11-25-romanization-mediated-ipa-design.md`

## Global Constraints
- Direct IPA remains primary; romanization-mediated output is always PROVISIONAL or UNRESOLVED.
- No romanization-to-Ukrainian shortcut may be presented as pronunciation.
- No IPA segment is inferred from the Ukrainian orthographic crosswalk.
- Source graphemes and romanization remain aligned; dropped upstream diacritics are never reconstructed.
- Unknown vowels, codas, syllable roles, tone and dialect details remain unknown.
- No neural model, server, external API, or gold-corpus promotion.

## Review Focus
- Romanization tokens that are ambiguous across source consonant classes must abstain.
- ASCII romanization that lost PCGN diacritics must not recover series or vowel quality.
- Coeng clusters must not be mistaken for independent syllable onsets.
- Mixed Khmer/Latin text and punctuation must preserve alignment.
- Unsupported or empty romanization must yield UNRESOLVED, not an empty or fabricated IPA result.

---

### Task 1: Source-aligned contextual candidate adapter

**Files:**
- Create: `src/khmer-romanization-ipa.js`
- Create: `tests/romanization-ipa.test.mjs`

**Interfaces:**
- Consumes the original Khmer unit, its actual romanized form, and source-registered onset IPA from structural analysis.
- Produces a typed PROVISIONAL IPA result plus an uncertainty/provenance trace, or UNRESOLVED.
- The candidate is accepted only when the leading romanization token is uniquely consistent with the source-unit PCGN consonant class. No vowel IPA is generated in this task.

- [x] Add tests for unique onset confirmation, ambiguous b/p, dropped-diacritic vowel abstention, coeng-only unresolved input, explicit provenance, source locators and source-registered IPA equality.
- [ ] Focused RED was not locally observed: the repository could not be cloned/run locally; tests were committed before adapter implementation.
- [x] Implement the adapter using the existing typed IPA constructor and target adapter.
- [x] Run focused and existing typed-IPA tests in GitHub Actions Quality checks.

### Task 2: Python parity

**Files:**
- Create: `src/khmer_ua/romanization_ipa.py`
- Create: `tests/test_romanization_ipa.py`
- Modify: `src/khmer_ua/__init__.py`

**Interfaces:**
- Match the JavaScript candidate status, IPA segments, provenance, uncertainty and Ukrainian rendering.
- Consume existing structural analysis and PCGN source-unit mappings; do not create a second phonology inventory.

- [x] Add parity and abstention tests for every registered onset mapping plus mismatch/ambiguous cases.
- [ ] Focused RED was not locally observed because local repository execution was unavailable.
- [x] Implement the Python adapter with existing `from_provisional_ipa` and `adapt_phonetic_result`.
- [x] Run focused and full Python tests in GitHub Actions Quality checks.

### Task 3: Mode integration and visible distinctions

**Files:**
- Modify: `src/main.js`
- Modify: `src/khmer-engine-core.js` only if the existing per-unit data cannot supply the required alignment.
- Modify: `tests/browser/*` and/or existing browser tests.

- [x] Keep the separate orthographic romanization card and its “не вимова” label.
- [x] In romanization mode, show the IPA-mediated Ukrainian candidate when available; otherwise show explicit unknown markers.
- [x] Keep the direct IPA mode and canonical result untouched.
- [x] Add browser tests for both output lanes, status labels and switching between Khmer and Latin input.

### Task 4: Evidence, parity, and closeout

**Files:**
- Modify: `docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md`
- Modify: `docs/superpowers/specs/2026-11-25-romanization-mediated-ipa-design.md`
- Create/update: `docs/superpowers/plans/2026-11-25-romanization-mediated-ipa.md`

- [x] Add exact JS/Python semantic parity fixtures for every registered onset rule and ensure romanization never becomes canonical IPA.
- [x] GitHub Actions Quality checks passed: Python tests, `npm run check`, structural/lexical/rule/segmentation parity, benchmarks and Vite build. Browser smoke pending on the latest head.
- [x] Record exact checks and remaining evidence-limited contexts in the master handoff; final SHA and latest browser result remain to be refreshed.

## Current implementation boundary (2026-11-25)

- Implemented and CI-verified so far: contextual onset-only candidate generation. Every IPA onset is cross-checked against the source consonant inventory and PCGN token class; the ambiguous BA b/p row abstains.
- Full contextual vowel, coda, syllabification, register-harmony and dialect adaptation remain **PARTIAL / evidence-limited**. `vowels.json` explicitly says it is not a complete deterministic orthography-to-IPA table. No complete vowel IPA matrix was fabricated.
- The separate orthographic romanization card remains the full BGN/PCGN-derived orthographic output; it is not relabelled as pronunciation.
- Local RED tests were not observed because this session used GitHub-hosted execution rather than a local clone. GitHub Actions Quality checks passed on commit `9d5acbb95fbe46df884d1ccc2482eb48d6f6d90e`; browser smoke for the latest UI-label changes is still running.
