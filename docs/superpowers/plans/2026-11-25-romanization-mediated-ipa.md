# Romanization-mediated IPA Implementation Plan

> **For agentic workers:** Implement task-by-task with test-first changes and a final branch review.

**Goal:** Add a conservative, contextual romanization-mediated provisional IPA path to the existing “Українська через романізацію” mode.

**Architecture:** Preserve the current BGN/PCGN orthographic output as a separate lane. Add a source-aligned adapter that may expose consonant-onset IPA already registered for the matching Khmer grapheme and confirmed against the PCGN romanization class, plus six exact source-cited representative vowel syllables; all other vowels, codas, syllable roles, and contrasts remain explicit unknown spans. Route every phonetic Ukrainian candidate through the existing typed IPA target adapter. Mirror semantics in Python and JavaScript.

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
- Produces a typed PROVISIONAL IPA result plus an uncertainty/provenance trace, or UNRESOLVED. Six exact vowel fixtures from `vowels.json` are allowed only when both the full Khmer spelling and ASCII romanization match.
- The candidate is accepted only when the leading romanization token is uniquely consistent with the source-unit PCGN consonant class. No vowel IPA is generated in this task.

- [x] Add tests for unique onset confirmation, ambiguous b/p, dropped-diacritic vowel abstention, coeng-only unresolved input, six exact series-vowel fixtures, same-ASCII source distinctions, explicit provenance, source locators and source-registered IPA equality.
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
- [x] In romanization mode, show the IPA-mediated Ukrainian candidate and its IPA string/status when available; otherwise show explicit unknown markers.
- [x] Keep the direct IPA mode and canonical result untouched.
- [x] Add browser tests for both output lanes, status labels and switching between Khmer and Latin input.

### Task 4: Evidence, parity, and closeout

**Files:**
- Modify: `docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md`
- Modify: `docs/superpowers/specs/2026-11-25-romanization-mediated-ipa-design.md`
- Create/update: `docs/superpowers/plans/2026-11-25-romanization-mediated-ipa.md`

- [x] Add exact JS/Python semantic parity fixtures for every registered onset rule and ensure romanization never becomes canonical IPA.
- [x] GitHub Actions Quality checks passed: Python tests, `npm run check`, structural/lexical/rule/segmentation parity, benchmarks and Vite build. Chromium browser smoke passed 44/44 Playwright tests on code head `facfa463bd77b7ac9591b5c13e80a0b54daa96ae`.
- [x] Record exact checks and remaining evidence-limited contexts in the master handoff; latest documented handoff head is `c3b95a28aca9b5135c93cdb7e6083df0ba51900f`; full contextual vowel/coda/syllable work remains partial.

## Current implementation boundary (2026-11-25)

- Implemented and CI-verified so far: contextual onset candidate generation plus six exact series-conditioned vowel exemplars. Every IPA onset is cross-checked against the source consonant inventory and PCGN token class; the ambiguous BA b/p row abstains. The exact vowel fixtures match both original Khmer spelling and the ASCII romanization.
- General vowel mapping beyond the six exact examples, coda, syllabification, register-harmony and dialect adaptation remain **PARTIAL / evidence-limited**. `vowels.json` explicitly says it is not a complete deterministic orthography-to-IPA table. No complete vowel IPA matrix was fabricated.
- The separate orthographic romanization card remains the full BGN/PCGN-derived orthographic output; it is not relabelled as pronunciation.
- Local RED tests were not observed because this session used GitHub-hosted execution rather than a local clone. GitHub Actions Quality checks passed on code head `facfa463bd77b7ac9591b5c13e80a0b54daa96ae`; Chromium passed 44/44 on the same head. Local test execution and RED observation were unavailable in this session.


## Follow-up evidence gate — 2026-11-25

A further review of the 54 R12a reference-mapping observations found that the existing evidence register explicitly marks every one as `runtime_eligible: false` and `SPECIALIST_REFERENCE_MAPPING_NOT_LEXICAL_TOKEN`. The mappings describe orthographic reference values but do not constitute exact lexical/syllable tokens suitable for deterministic runtime lookup. Therefore no additional vowel IPA rules were promoted from that table.

To preserve the distinction between source-described reference mappings and executable fixtures, added regression coverage for 26 observed PCGN romanizations (including `ke`, `koe`, `ku`, `ko`, `key`, `kao`, `kau`, `kou`, `kaeu`, `keu`, `koea`, `kuo`) and two mismatched spellings of the six accepted fixtures. All remain onset-only PROVISIONAL candidates with an explicit unknown vowel tail; no phonemic IPA is manufactured.

- Temporary diagnostic test/file removed after recording the actual `@gmana/km-translit` outputs.
- Python/JS parity includes all 26 negative contexts.
- Quality [45586289529](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45586289529) SUCCESS (516 Python tests + 70 subtests); Chromium [45586289504](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45586289504) SUCCESS (44/44). External khPOS [45586289526](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45586289526), shared held-out benchmark [45586289507](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45586289507), and pinned Rust [45586289555](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45586289555) also SUCCESS on exact head `20b860c01965ea2ea49cca439c26ab57ef351a8e`.
- General vowel/coda/coeng rules remain PARTIAL / evidence-limited; the six source-aligned syllable fixtures remain the only full provisional IPA outputs.

