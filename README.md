# Khmer → Ukrainian Phonetic-Graphemic Correspondence System

Research-grade reference implementation for developing a **Ukrainian practical system for transmitting Khmer in Ukrainian Cyrillic**.

> **Status: PUBLIC BETA — NOT EXPERT-VALIDATED.** The repository distinguishes established script facts, linguistic analyses, project decisions and unresolved cases. The service exposes supported beta phoneticizations and marks uncovered forms instead of silently guessing. Automated checks do not establish pronunciation accuracy. No independent expert-adjudicated gold corpus or measured linguistic accuracy is claimed. See the [beta release policy](docs/BETA-RELEASE-POLICY.md).

## What this project is

The active research pipeline is:

**Khmer orthography → graphemic structure → phonology → surface phonetics / IPA → Ukrainian target → Ukrainian orthography**

It is **not** a Khmer character-to-character transliterator and it is not primarily a Khmer romanization converter.

The practical Ukrainian layer is a project proposal. It is not an official Ukrainian national standard.

The shared Ukrainian target conventions are maintained in the canonical [foreign IPA → Ukrainian adaptation policy](https://github.com/ClippyFirst/Ukrainian-Phonetic-Inventory/blob/main/docs/foreign-target-adaptation.md). This Khmer adapter applies the aspiration apostrophe and distinguishes /h/ → г, /ɡ/ → ґ and /x/ → х; it also preserves Ukrainian affricate and palatalization sequences where the source IPA supports them.

## Live service — GitHub Pages only

**[Open the Khmer → Ukrainian web service](https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System-/)**

**[Public beta release checklist](docs/BETA-RELEASE-CHECKLIST.md)** · [Beta release policy](docs/BETA-RELEASE-POLICY.md)

The public static service is hosted exclusively on GitHub Pages. Deployment is performed by `.github/workflows/pages.yml` from `main`; the workflow builds with Vite, runs web checks and production Chromium smoke tests, uploads the `dist/` artifact, deploys with `actions/deploy-pages`, and verifies both public HTML pages plus their JavaScript and CSS assets. No Vercel, Netlify, external application server, runtime API, analytics or telemetry is used.

## Web service

The system page now includes an evidence coverage dashboard generated from `reports/khmer-coverage-audit.json`. It exposes the dependent-vowel × consonant-series inventory and clearly distinguishes source-attested examples from unresolved cells and source conflicts. The dashboard is an evidence-status view, not a pronunciation-accuracy score.

The repository now contains the two-page public web layer:

- `index.html` — the Khmer → Ukrainian service.
- `system.html` — explanation of the author's practical transcription system.

The visual direction is intentionally based on **Cambodia's blue, red and white national palette**, used as controlled accents within an editorial, typographic research-tool design. The structure follows the user's established Chinese service pattern while keeping Khmer-specific linguistic logic independent.

The primary Ukrainian result has two visibly selectable methods, following the Lao service:

1. **За IPA** — Khmer orthography → structural/phonological analysis → IPA → Ukrainian adaptation.
2. **З романізації** — Khmer orthography or supplied BGN/PCGN Latin → romanization → Ukrainian orthographic rendering.

The selector is beside the main result and works without opening the research drawer. These are separate pipelines: the romanization path is not presented as pronunciation, and an unresolved IPA result does not silently switch methods.

The browser service is:

- static and local-first;
- free of runtime API dependencies;
- free of analytics/telemetry;
- Unicode-safe for Khmer and Ukrainian;
- explicit about `PROPOSED`, `EVIDENCE_LIMITED` and `NOT_ESTABLISHED` states;
- backed by the repository's research policy rather than duplicated UI-only correspondence tables.

## Scope

Primary variety: contemporary Standard Khmer, with Phnom Penh-oriented pronunciation where evidence supports it.

The project separates:

- orthographic structure;
- phonological interpretation;
- phonetic/IPA realization;
- pronunciation profiles;
- practical Ukrainian representation;
- established lexical forms.

## Current methodology

The repository follows the research architecture established for the broader Asian-language → Ukrainian project family:

1. reconstruct source orthography;
2. identify the source phonological structure;
3. model contextual phonetic realization;
4. compare existing practical transcription traditions;
5. derive Ukrainian candidates from the Ukrainian target inventory;
6. select practical Ukrainian spellings using explicit constraints;
7. validate against a provenance-bearing corpus.

Russian Khmer practical transcription is a **comparator**, not a template for Ukrainian. Serbian and Bulgarian evidence is retained only at the strength actually established.

## Current Ukrainian policy

Examples of the proposed practical target layer:

| Khmer IPA | Ukrainian default | Russian-compatible alternative |
|---|---|---|
| /p/ | п | — |
| /pʰ/ | п' | пх |
| /t/ | т | — |
| /tʰ/ | т' | тх |
| /k/ | к | — |
| /kʰ/ | к' | кх |
| /c/ | ть | ть |
| /cʰ/ | ть' | ч / тьх |
| /ɲ/ | нь | нь |
| /ŋ/ | нг | нг |
| /r/ | р | — |
| /ʋ/ | в | — |
| /w/ | в | у |
| /h/ | г | х |
| /ɡ/ (ASCII /g/) | ґ | г |
| /x/ | х | х |
| /ʔ/ | ∅ | context-dependent |
| /t͡s, d͡z, t͡ʃ, d͡ʒ/ | ц, дз, ч, дж | comparator-only where documented |

These are **project decisions**, not claims of official Ukrainian usage. Aspiration is retained in the research/IPA layer and marked in practical Ukrainian output with an apostrophe (e.g. к', т', п').

## Vowels

Khmer has a substantially richer vowel system than Ukrainian, and a written vowel sign can have different realizations after first- and second-series consonants. The repository therefore does not use a simple sign → vowel-letter table.

The current evidence-backed vowel model records:

- first/second-series inherent vowels;
- short/long vowel distinctions;
- complex vowels;
- series-conditioned realization;
- vowel harmony as an analysis-dependent factor;
- stress/reduction as a pronunciation-profile factor;
- coda effects such as NIKAHIT and REAHMUK.

The complete lexical vowel-sign × context → IPA matrix is still an open research task.

A reproducible first-order evidence inventory is available via `python scripts/coverage.py`. It writes both `reports/khmer-coverage-audit.json` and the byte-identical `public/reports/khmer-coverage-audit.json` deployed by GitHub Pages, enumerating each dependent vowel sign × consonant-series cell and separating source-attested examples from conflicting or not-established cells. This report is deliberately conservative: an attested example is **not gold data**, and the report does not infer IPA from Unicode structure. Alongside the first-order sign × series audit, it now exposes source-indexed case observations for dependent-vowel sequence, consonant class, subscripts, orthographic coda markers, explicit source length marks and source/profile metadata. Missing phonological syllable type, measured length, stress, harmony and profile remain explicitly NOT_ESTABLISHED; no Cartesian context cells or IPA outputs are inferred. Run `python scripts/coverage.py` after changing the canonical evidence register and review the generated diff. CI checks that the committed report is reproducible via `python scripts/coverage.py --check` and `tests/test_coverage_report.py`.

## Repository structure

- `data/khmer/` — Khmer orthographic and phonological evidence.
- `data/comparative/` — Russian/Serbian/Bulgarian/Ukrainian comparative material.
- `data/ukrainian/` — proposed Ukrainian target policy.
- `data/tests/` — provenance-bearing validation cases.
- `schemas/` — machine-readable schemas.
- `src/khmer_ua/` — implementation.
- `tests/` — regression tests.
- `docs/` — methodology, system specification, implementation, validation and references.
- `index.html` / `system.html` — static web service.

## Web development

The web layer is dependency-light and uses native browser APIs. Exact npm dependency versions and integrity hashes are committed in `package-lock.json`; use `npm ci` for reproducible installs. The included structural check can be run with:

`npm ci` followed by `npm test` and `npm run build`

The structural web test verifies the two-page architecture, canonical research-data imports, explicit unresolved states, and the absence of duplicated linguistic mapping tables in the browser adapter. The production build is generated with Vite.

The web requirements are frozen in:

- `docs/superpowers/specs/2026-10-05-khmer-web-service-requirements.md`

## Python package

Install the package and its test-only dependencies in a Python 3.11+ environment with `pip install -e ".[test]"`, then run the research test suite with `pytest`. JSON Schema validation remains a test-only dependency and is not imported by runtime modules.

The public API exposes:

- `analyze()`
- `render_ipa_profile()`
- `map_segment()`
- `map_sequence()`
- `map_ipa_string()` — whole-IPA longest-match adapter used by the deterministic engine
- `explain_segment()`

The current research parser intentionally returns an explicit NOT ESTABLISHED state instead of inventing IPA where the complete source-language analysis is not implemented.

## Research status

Implemented:

- Unicode normalization;
- conservative Khmer grapheme parsing;
- coeng/subscript recognition, including the structurally distinct subscript-independent-vowel form;
- consonant class/register metadata;
- independent/dependent vowel recognition;
- structural Unicode validation;
- comparative Cyrillic research layer;
- proposed Ukrainian practical target layer;
- pronunciation-profile abstraction;
- evidence registry and provenance-bearing test corpus;
- two-page static web service;
- conservative browser adapter with explicit unresolved states;
- Cambodia-oriented visual design system;
- structural web tests.

Still not established as a complete linguistic engine:

- complete orthography-to-IPA conversion for every Khmer vowel combination;
- corpus-calibrated Ukrainian candidate ranking;
- empirical accuracy;
- a normative Ukrainian Khmer transcription standard.

Accordingly, the web service is **production-structured but linguistically coverage-limited**. It must not be marketed as a complete automatic Khmer transliterator until the full orthography → IPA matrix and adjudicated corpus are completed.

## Documentation map

Start with the [documentation index](docs/README.md). It explains where authoritative requirements, architecture, evidence, research matrices, implementation notes, validation procedures and agent guidance live.

The canonical continuation and task ledger is [docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md](docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md). The index is navigation, not a replacement for that ledger.

## Documentation

- [Documentation index](docs/README.md)

- `docs/methodology.md`
- `docs/phonology.md`
- `docs/system-specification.md`
- `docs/comparative-cyrillic-systems.md`
- `docs/ukrainian-practical-transcription.md`
- `docs/implementation.md`
- `docs/validation.md`
- `docs/evidence.md`
- `docs/references.md`
- `docs/limitations.md`
- `docs/repository-audit.md`
- `docs/superpowers/specs/2026-10-05-khmer-web-service-requirements.md`

## Research integrity

No accuracy percentage is reported without an adjudicated gold-standard corpus.

When evidence is insufficient, the system records **EVIDENCE LIMITED**, **ANALYSIS DEPENDENT**, **DIALECT DEPENDENT**, or **NOT ESTABLISHED** rather than fabricating a result.


## Latest transcription-audit status — 2026-11-11

The current implementation includes explicit handling for Khmer register shifters (៉ / ៊), the exceptional ប៉ construction, coeng-based clusters and adversarial regression fixtures. The canonical Ukrainian policy currently proposes /c/ → **ть**, /cʰ/ → **ть'** (palatal stop + aspiration, not an affricate), /h/ → **г**, /ɡ/ (ASCII alias /g/) → **ґ**, /x/ → **х**, /ʋ/ → **в** and /w/ → **в**. Explicit affricates map /t͡s/ → **ц**, /d͡z/ → **дз**, /t͡ʃ/ → **ч** and /d͡ʒ/ → **дж**; /tɕ/ and /dʑ/ use ч and дж as practical approximations. Syllable-initial /j/ + vowel uses Ukrainian я/є/ї/ю/йо where transparent; otherwise /j/ is й. Aspiration is marked with an apostrophe; /ʔ/ does not trigger this marker. These remain project-specific decisions, not an official Ukrainian standard.

The whole-IPA longest-match adapter is now the single implementation used by the deterministic engine. It preserves IPA as the boundary, maps affricates before their component symbols, and withholds unsupported sequences. The web explanation and browser adapter have been synchronized with the policy. The browser does not silently invent Phnom Penh /r/-loss phonetics or complete vowel IPA where the research engine has not established them.

Quality checks and static deployment are continuously checked by GitHub Actions; consult the latest run for the exact revision before relying on pipeline status. A green build does not constitute linguistic accuracy evidence. No empirical accuracy percentage is claimed.


## Latest lexical-coverage pass — 2026-10-06

The public service's previous `ភាសាខ្មែរ` → `NOT_ESTABLISHED` result was a **coverage gap**, not evidence that the pronunciation was unknown. Cited lexical references report the phrase as **[pʰiəsaː kʰmae]**. The repository stores this as source-attested evidence, not an independently adjudicated gold label: no audio-based or independent multi-source adjudication is recorded. The Ukrainian practical form **п'ієса к'мае** remains explicitly PROPOSED.

The Ukrainian policy was also extended for /ae/, and the browser adapter now distinguishes a corpus-defined lexical Ukrainian form from a mechanical segment-by-segment rendering. This prevents the UI from silently presenting a different practical spelling merely because a phrase contains context-dependent or complex Khmer vowels.


## Adversarial long-input handling — 2026-10-06

The browser adapter evaluates long Khmer inputs **per orthographic unit** rather than assigning one global fallback to the entire input.

- established lexical fixtures remain visible inside mixed/adversarial text;
- unsupported units are marked locally as `NOT_ESTABLISHED`;
- malformed Unicode sequences are marked locally as `INVALID_OR_UNSUPPORTED`;
- `EVIDENCE_LIMITED` is propagated to the overall status without suppressing valid neighboring results;
- lexical Ukrainian overrides are checked against the canonical IPA → Ukrainian policy and cannot silently contradict it;
- misplaced Khmer register shifters are explicitly flagged rather than treated as ordinary vowel/consonant data.

This behaviour is a deliberate research-integrity requirement: one unresolved case must not hide evidence-backed results elsewhere in the same test input.


## External IPA renderers and G2P candidates

The research registry records external pronunciation engines, IPA dictionaries, and Unicode IPA display fonts without treating unvalidated output as ground truth. See [`docs/external-ipa-renderers.md`](docs/external-ipa-renderers.md) and the machine-readable [`data/external-ipa-renderers.json`](data/external-ipa-renderers.json). These are candidate inventories only; no third-party engine is enabled by default, and the ClippyFirst IPA → Ukrainian adapter remains the sole target adaptation boundary.


## Two output methods

The service separates the phonetic IPA-first route from the orthographic romanization route. The romanization tab accepts either Khmer script (via the existing BGN/PCGN-derived ASCII package) or an already romanized BGN/PCGN Latin input with diacritics, then applies a separate provisional Ukrainian orthographic crosswalk. Unknown fragments remain explicit; mixed Khmer+Latin input is marked PARTIAL and should be entered in separate runs; the mode never falls back to IPA. See the [romanization → Ukrainian research matrix](docs/romanization-to-ukrainian-matrix.md) for the profile, source tables and unresolved rows.


## Machine-readable BGN/PCGN orthographic tables

- [`data/khmer/romanization_ukrainian.csv`](data/khmer/romanization_ukrainian.csv) — 22 consonant/subscript rows.
- [`data/khmer/romanization_vowels_ukrainian.csv`](data/khmer/romanization_vowels_ukrainian.csv) — 37 source-located independent/dependent vowel and anusvara/visarga rows.
- [`data/khmer/romanization_marks_numerals.csv`](data/khmer/romanization_marks_numerals.csv) — 6 PCGN diacritic-rule rows covering 7 Khmer source marks (including both U+17CB BANTOC and U+17D0 SAMYOK SANNYA under note 5), plus 10 numeral rows.

These files separate source romanization from Ukrainian target proposals and preserve explicit evidence statuses. They are research tables, not proof that the runtime BGN/PCGN engine or romanization → Ukrainian syllable adapter is complete.

## Independent IPA gold corpus

The project uses a provenance-backed, double-annotated IPA gold workflow. See [the corpus protocol](docs/ipa-gold-corpus.md) and [the language-specific phonology research workpack](docs/audits/current/PHONOLOGY-RESEARCH-WORKPACK-2026-11-01.md). The corpus is currently empty by design; no phonetic accuracy claim is available until expert adjudication is complete.

## Deterministic rule engine

The phonetic web path and Python API are deterministic and local: versioned lexical IPA fixtures plus conservative Khmer register/structure rules feed the explicit IPA → Ukrainian policy. No neural inference, external G2P process, network request, or model-voting step participates in phonetic output. Unsupported combinations are withheld. When the IPA-first analysis cannot establish a complete Khmer result but the existing BGN/PCGN-derived romanizer can render an individual orthographic unit, the primary Ukrainian field automatically offers that unit's orthographic adaptation as a `PROVISIONAL` candidate without requiring a mode switch or appending `???`. This applies at every detail level. Each candidate is visibly identified as an orthographic-romanization fallback, not an IPA-derived pronunciation. The IPA field and per-unit phonetic diagnostics retain `NOT_ESTABLISHED`; malformed or unrenderable fragments keep local `???` markers. A whole-input fallback remains as a secondary safety net when per-unit alignment is unavailable. Provisional onset hints remain separately labelled and are never promoted to canonical IPA. See [the deterministic engine contract](docs/DETERMINISTIC-RULE-ENGINE.md). This guarantees repeatability, not universal linguistic correctness; PROPOSED results remain proposals pending independent adjudication.

Python entry point: `from khmer_ua import RuleBasedKhmerEngine`.

## Live service

GitHub Pages: https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System-/

The published phonetic path uses the deterministic local rule engine; the separate romanization mode is not used as a pronunciation fallback.


## Research-only typed IPA candidates

The optional Python `HybridKhmerEngine` collects explicitly injected external IPA candidates through the shared typed validator. Bare provider strings are rejected; raw IPA, profile, kind, status, uncertainty and provenance are retained. External candidates never replace the deterministic engine's published result. No providers or model dependencies run by default. See [the typed hybrid API contract](docs/hybrid-engines.md).


The Khmer-script romanization path now brackets any Khmer letters or combining marks that remain in the upstream Latin output and marks the result PARTIAL; Khmer punctuation is preserved. This is an output-integrity safeguard only: it does not restore omitted PCGN diacritics or make the upstream ASCII romanizer contextually conformant.


### Khmer subscript independent-vowel structure — 2026-11-16

The structural parser recognizes a Unicode-encoded subscript independent vowel after U+17D2 COENG (for example, the Unicode Standard 18.0.0 Chapter 16 orthographic example ផ្ឯម). It records the sequence as `subscript_independent_vowel`, preserves its two code points and exposes `khmer_subscript_sequence_spans()` for exact-source code-point protection. This is a structural parsing improvement only: it does not establish pronunciation, IPA, Ukrainian output, or lexical word boundaries. See the [Unicode 18 Khmer structure source](https://www.unicode.org/versions/Unicode18.0.0/core-spec/chapter-16/) and the current [LOC word-division evidence audit](docs/audits/current/LOC-KHMER-WORD-DIVISION-EVIDENCE-2026-11-16.md).


### Unicode 18 Khmer orthographic-component scanner and syllable parser — 2026-11-16

The Python and browser runtimes now expose a lossless component scan for Khmer orthography. It identifies modeled bases, COENG+subscript pairs (including subscript independent vowels), robat, register shifters, dependent vowel signs, format controls and other modeled signs, with exact Unicode code-point offsets. The payload schema is `schemas/orthographic-components.schema.json` (`khmer-orthographic-components/v1`).

The component inventory is consumed by a separate Unicode 18 §16.4 parser in `src/khmer_ua/orthographic_syllables.py`, mirrored by `src/orthographic-syllables.js`. The packed parse forest retains all complete orthographic-syllable segmentation alternatives and local grammar-role alternatives without Cartesian expansion; it preserves exact source text, Unicode code-point offsets, derivation counts and rejected spans/reasons. Ambiguous results do not select a preferred parse. This is **orthographic structure only**: it does not establish phonological syllables, lexical word boundaries, pronunciation, IPA or Ukrainian output. UAX #29 default grapheme clusters are not a substitute for Khmer orthographic-syllable grammar, and Khmer word segmentation needs separate tailoring, profile selection and lexical evidence. The Unicode 18 parser is not a TN #61 Modern Khmer validator; TN #61 v2 remains a separately scoped non-normative research profile. See Unicode 18 Chapter 16 §16.4 and UAX #29 Revision 49.


## Project license and research reuse (2026-11-21)

- Original project software code is licensed under **PolyForm Noncommercial 1.0.0**; see [LICENSE](LICENSE). The license permits noncommercial research, modification and redistribution, and has a separate permission for educational institutions and public research organizations regardless of funding source.
- Original documentation and explanatory prose are licensed under **CC BY-NC 4.0**; see [LICENSE-DOCS](LICENSE-DOCS).
- Original project-authored research datasets, annotations and curated database contributions are licensed for noncommercial research under **CC BY-NC 4.0**; see [LICENSE-DATA](LICENSE-DATA). This covers only material the maintainers/contributors have rights to license, not source material embedded in or derived from third-party resources.
- Third-party software, fonts, models, dictionaries, corpora, recordings, source quotations and mixed-source records retain their own rights and notices. Unknown or conflicting rights do not authorize redistribution; consult [third-party notices](THIRD_PARTY_NOTICES.md) and the source registries before reuse.
- The IPA gold benchmark's existing `redistributable` registry flag remains a stricter product-corpus eligibility gate: NC-only material is not eligible for a commercial/product release. This does not cancel the separate noncommercial research grant under `LICENSE-DATA`.
- PolyForm Noncommercial is not an OSI-approved Open Source license. Commercial use of project code or original project data is not granted; contact the rights holder for separate permission.


## Citation

If you use this research prototype, cite the repository and identify the exact commit or version used. Citation metadata is provided in [CITATION.cff](CITATION.cff) and can be used by GitHub's citation interface.

## Evidence confidence tiers

The beta labels source-traceable proposed outputs as B, experimental or incomplete cases as C, unsupported cases as D, and reserves A for independently adjudicated profile-matched gold. These are categorical evidence labels, not probabilities or accuracy scores. Per-unit and aggregate tier behavior is described in [Evidence confidence tiers](docs/EVIDENCE-CONFIDENCE-TIERS.md). The gold corpus remains empty and accuracy remains NOT_ASSESSED.

## Public output detail levels (2026-11-21)

The phonetic interface provides three presentation levels. **Careful** displays the main result and uncertainty summary while hiding per-unit diagnostic cards; **Balanced** (default) shows per-unit results, statuses, explanations and separately labelled existing PROVISIONAL onset hints; **Exploratory** additionally reveals the parser's existing graphemic structure where available. These are display differences, not new phonological analyses. The level changes presentation only: it never changes the phonological analysis, invents vowels/codas/tone, promotes PROVISIONAL output to canonical IPA, or converts PROPOSED records into expert gold. The existing pronunciation profile remains a separate selector. The romanization path remains orthographic and independent of phonetic fallback.
