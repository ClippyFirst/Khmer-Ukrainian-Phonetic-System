# Codebase map — Khmer → Ukrainian

**Purpose:** navigation and data-flow map for the current `main` snapshot. This file is not a claim that the full Khmer phonological engine or Ukrainian standard is complete.

## Entry points

| Surface | Entry point | Responsibility |
|---|---|---|
| Python library | `src/khmer_ua/__init__.py` | Public exports and version identifiers |
| Python CLI | `src/khmer_ua/cli.py` | Command-line interface |
| Deterministic engine | `src/khmer_ua/rule_engine.py` | Bounded lexical/rule analysis and IPA-to-Ukrainian mapping |
| Browser application | `index.html` → `src/main.js` | Local web service |
| System explanation | `system.html` | User-facing methodology and limits |
| Orthographic romanization | `@gmana/km-translit` → `src/khmer-romanization-ukrainian.js` | BGN/PCGN-derived Latin output and separate Ukrainian orthographic adapter |

## Python data flow

```text
Python API / CLI
  ├─ normalize.normalize_khmer
  ├─ parser.analyze
  │    ├─ orthographic segmentation and grapheme decomposition
  │    └─ phonology.resolve_effective_register
  ├─ RuleBasedKhmerEngine.analyze
  │    ├─ exact versioned lexical fixture lookup
  │    ├─ bounded, explicitly supported rule path
  │    └─ explicit unresolved / provisional status where coverage is absent
  └─ practical.map_ipa_string
       └─ longest-match IPA → Ukrainian policy adapter
```

`ipa.render_ipa_profile` validates a supplied IPA string against the currently supported profile and preserves it. It does not derive complete Khmer IPA from orthography. The practical adapter consumes IPA; do not add a parallel Khmer-grapheme-to-Ukrainian phonetic shortcut.

`HybridKhmerEngine` and `create_hybrid_engine` remain compatibility exports, but `src/khmer_ua/hybrid.py` documents that the former provider-voting ensemble was removed. External candidates belong to optional diagnostics and must not override the deterministic published result.

## Browser data flow

```text
index.html
  └─ src/main.js
       ├─ canonical Khmer registries + lexical/web fixtures
       ├─ Unicode normalization and orthographic tokenization
       ├─ consonant / coeng / sign / register-shifter structure
       ├─ bounded fixture/rule-backed phonetic presentation
       │    └─ src/ukrainian-practical.js (IPA → Ukrainian)
       └─ separate romanization mode
            ├─ @gmana/km-translit (Khmer → Latin)
            └─ src/khmer-romanization-ukrainian.js (Latin → Ukrainian)
```

Keep the two routes separate. The romanization adapter is not a fallback when phonetic IPA is unknown. Preserve mixed text, separators and punctuation and expose unsupported fragments locally rather than suppressing valid neighbours.

## Canonical data ownership

- Khmer script/structure: `data/khmer/consonants.json`, `signs.json`, `vowels.json`, `registers.json`, `rules.json`.
- Source provenance: `data/khmer/sources.json` and current audit matrices.
- Ukrainian phonetic target: `data/ukrainian/practical-policy.json`.
- BGN/PCGN-derived orthographic crosswalk: `data/khmer/romanization_ukrainian.csv`, `romanization_vowels_ukrainian.csv`, `romanization_marks_numerals.csv`.
- Test fixtures: `data/tests/`; benchmark and gold lifecycle: `data/benchmark/`.
- Generated coverage report: `scripts/coverage.py` → `reports/khmer-coverage-audit.json` and `public/reports/khmer-coverage-audit.json`.

## High-risk seams

1. Unicode normalization, grapheme boundaries, coeng/subscript order and register-shifter eligibility.
2. Python/browser structural parity and exact preservation of source spans/separators.
3. Vowel sign × consonant series × length × coda × pronunciation profile; do not infer uncovered IPA.
4. Phnom Penh /r/-loss and other style-conditioned variation; no blanket rewriting.
5. Longest-match IPA mapping, including affricates and unsupported sequences.
6. Lossy ASCII romanization and contextual BGN/PCGN distinctions.
7. Gold-corpus provenance, split integrity, expert convention approval and rights verification.

## Commands

```bash
python -m pytest -q
npm run check
npm run build
npm run test:browser
python scripts/coverage.py --check
```

Run the full relevant suite after changes, not just a focused test. If local execution is unavailable, record that fact and cite exact-head hosted workflow evidence instead.
