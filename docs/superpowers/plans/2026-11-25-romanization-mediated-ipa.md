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
- Modify: `tests/romanization-ukrainian.test.mjs`

**Interfaces:**
- Consumes the original Khmer unit, its actual romanized form, and source-registered onset IPA from structural analysis.
- Produces a typed PROVISIONAL IPA result plus an uncertainty/provenance trace, or UNRESOLVED.
- The candidate is accepted only when the leading romanization token is uniquely consistent with the source-unit PCGN consonant class. No vowel IPA is generated in this task.

- [ ] Add failing tests for unique onset confirmation, ambiguous b/p, dropped-diacritic vowel abstention, coeng-only unresolved input, and explicit provenance.
- [ ] Run the focused Node test and record the expected RED result.
- [ ] Implement the adapter using the existing typed IPA constructor and target adapter.
- [ ] Run focused tests and existing typed-IPA tests.

### Task 2: Python parity

**Files:**
- Create: `src/khmer_ua/romanization_ipa.py`
- Modify: `tests/test_romanization_ukrainian.py`
- Modify: `src/khmer_ua/__init__.py`

**Interfaces:**
- Match the JavaScript candidate status, IPA segments, provenance, uncertainty and Ukrainian rendering.
- Consume existing structural analysis and PCGN source-unit mappings; do not create a second phonology inventory.

- [ ] Add failing parity and abstention tests.
- [ ] Run focused pytest to verify RED.
- [ ] Implement the Python adapter with existing `from_provisional_ipa` and `adapt_phonetic_result`.
- [ ] Run focused pytest and full Python tests.

### Task 3: Mode integration and visible distinctions

**Files:**
- Modify: `src/main.js`
- Modify: `src/khmer-engine-core.js` only if the existing per-unit data cannot supply the required alignment.
- Modify: `tests/browser/*` and/or existing browser tests.

- [ ] Keep the separate orthographic romanization card and its “не вимова” label.
- [ ] In romanization mode, show the IPA-mediated Ukrainian candidate when available; otherwise show explicit unknown markers.
- [ ] Keep the direct IPA mode and canonical result untouched.
- [ ] Add browser tests for both output lanes and status/provenance labels.

### Task 4: Evidence, parity, and closeout

**Files:**
- Modify: `docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md`
- Modify: `docs/superpowers/specs/2026-11-25-romanization-mediated-ipa-design.md`
- Create/update: `docs/superpowers/plans/2026-11-25-romanization-mediated-ipa.md`

- [ ] Add JS/Python parity fixtures and ensure romanization never becomes canonical IPA.
- [ ] Run `npm test`, `npm run test:parity`, `npm run test:rule-parity`, `npm run build`, Python tests and browser tests where CI supports them.
- [ ] Record exact checks, results, blockers, commit SHA and remaining evidence-limited contexts.
