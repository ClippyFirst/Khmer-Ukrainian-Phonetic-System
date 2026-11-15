# Architecture

## Product contract

This repository is a research-grade Khmer → Ukrainian system with two deliberately separate output routes:

1. **Phonetic route:** Khmer orthography → Unicode normalization → structural analysis → source-language phonological interpretation → IPA / explicitly typed phonetic result → Ukrainian target adaptation → Ukrainian practical orthography.
2. **Orthographic romanization route:** Khmer orthography → the selected BGN/PCGN-derived Latin romanizer → a separately labelled Ukrainian orthographic rendering.

The second route is not a pronunciation engine. Latin romanization must never be used to infer IPA, consonant register, vowel quality, tone, aspiration or other phonetic facts. Neither route may silently convert unsupported input into a confident result.

The Ukrainian practical layer is a project proposal, not an official Ukrainian national standard. The operational pronunciation profile currently selected by the Python IPA adapter and deterministic engine is `khmer-pph-careful-citation-v1`.

## Runtime topology

### Python research API

- `src/khmer_ua/normalize.py` — Unicode normalization.
- `src/khmer_ua/parser.py` — Khmer structural parsing and orthographic-unit analysis.
- `src/khmer_ua/phonology.py` — effective consonant-series/register resolution and bounded structural rules; structural resolution is not a complete source-to-IPA model.
- `src/khmer_ua/ipa.py` — selected-profile preservation plus a typed, syntax-checked IPA candidate boundary. It preserves provider output, notation kind, provider identity and uncertainty; it does not generate pronunciation or promote candidates to published output.
- `src/khmer_ua/practical.py` — the canonical IPA-to-Ukrainian longest-match adapter.
- `src/khmer_ua/rule_engine.py` — deterministic lexical-fixture and narrowly supported rule path. Unsupported combinations remain explicit; provisional onset previews are not complete IPA.
- `src/khmer_ua/hybrid.py` — compatibility import path. The former provider-voting ensemble is removed; external candidates are not promoted to published output.
- `src/khmer_ua/cli.py` — command-line entry point.

Public exports are listed in `src/khmer_ua/__init__.py`. Do not infer broader capability from a function name or a compatibility alias.

### Browser service

- `src/main.js` — browser entry point, data loading, orthographic tokenization, structural parsing, evidence/fixture handling and UI state.
- `src/ukrainian-practical.js` — IPA-to-Ukrainian browser adapter.
- `src/khmer-romanization-ukrainian.js` — separate BGN/PCGN-derived Latin-to-Ukrainian orthographic adapter.
- `src/styles/main.css` — shared presentation.
- `index.html` — service interface.
- `system.html` — explanation of the proposed system.

The browser imports canonical Khmer/Ukrainian registries and test fixtures. Keep its externally visible status semantics aligned with Python where the contracts overlap. The real `@gmana/km-translit` dependency is used only by the orthographic romanization route.

## Data and evidence ownership

| Location | Authority / purpose |
|---|---|
| `data/khmer/*.json` | Khmer orthographic inventory, consonants, signs, vowels, registers, rules and source registry |
| `data/comparative/` | Comparative practical-transcription evidence |
| `data/ukrainian/practical-policy.json` | Proposed Ukrainian IPA adaptation policy |
| `data/ukrainian/practical_correspondence.csv` | Structured target correspondences / supporting matrix |
| `data/khmer/romanization*.csv` | Source-located BGN/PCGN-derived orthographic crosswalks and Ukrainian proposals |
| `data/tests/` | Reusable structural, lexical and adversarial fixtures; not automatically IPA gold |
| `data/benchmark/` | Benchmark records, annotations, adjudications, splits, licenses and predictions |
| `data/external-ipa-renderers.json` | Candidate external resources and renderers; not runtime authority |
| `schemas/` | Machine-readable contracts for data and benchmark records |
| `reports/`, `public/reports/` | Generated coverage report and deployed copy; generated from canonical source data |
| `docs/audits/current/` | Current evidence matrices, source triage and completion register |

Do not duplicate canonical mappings in UI code or explanatory tables without a clear human-readable purpose and a parity test. Generated reports must be regenerated using their documented scripts and checked for drift.

## Research and trust boundaries

- Unicode and orthographic structure do not establish a word's complete phonetic realization.
- A source-attested lexical example is not an independently adjudicated gold label.
- External G2P output is a diagnostic candidate, not a vote and not the final IPA authority.
- The typed candidate boundary validates notation and metadata only. A provider's COMPLETE assertion is not adjudication, gold status, phonological correctness or permission to publish a result.
- IPA notation kind, pronunciation profile, provider/source provenance, uncertainty and data rights must remain explicit. Preserve tone, length, stress and syllable boundaries as supplied; never silently normalize or repair provider output.
- No empirical accuracy percentage is valid while independent adjudicated gold is absent.
- BGN/PCGN-derived ASCII output can lose diacritics and contextual distinctions; a downstream Ukrainian adapter cannot reconstruct information that upstream output discarded.
- Preserve every source unit or mark it unsupported/uncertain. Preserve separators, punctuation, mixed scripts and Unicode normalization semantics according to the tested API contract.

## Verification topology

- Python: `python -m pytest -q`.
- Browser/Node: `npm run check` (or `npm test`; currently the package scripts share the same Node test list).
- Build: `npm run build`.
- Browser automation: `npm run test:browser`.
- Generated coverage artifact: `python scripts/coverage.py --check`.
- Gold corpus engineering gate: use the documented `scripts/ipa_gold_corpus.py` commands and workflow; passing its engineering checks is not linguistic release approval.

Read `AGENTS.md`, the master handoff and [the codebase map](agents/codebase-map.md) before modifying a runtime path. A green engineering suite does not establish phonetic accuracy, expert adjudication, manual accessibility review or release readiness beyond the checks it actually runs.
