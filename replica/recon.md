# Recon: Lao engine architecture applied to the Khmer engine

Scope: engine/result-contract architecture only — not a clone of Lao phonology, Lao source data, or the Lao public UI.
For: maintainers of the Khmer → Ukrainian research prototype.
Date: 2026-11-24

## Sources

| Source | Location | What it establishes |
|---|---|---|
| Lao grapheme IPA preview contract | [Lao docs](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/blob/main/docs/lao-grapheme-ipa-preview.md) | Typed statuses, provisional IPA, one IPA-only target adapter, explicit unknown spans |
| Khmer deterministic engine | [Khmer docs](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/blob/main/docs/DETERMINISTIC-RULE-ENGINE.md) | Existing Khmer parser, lexical rules, profiles, output boundaries |
| Khmer provisional preview | [Fallback contract](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/blob/main/docs/provisional-grapheme-ipa-fallback.md) | Registered onset-only hint and uncertainty limits |
| Khmer hybrid API | [Hybrid contract](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/blob/main/docs/hybrid-engines.md) | External candidates remain separate from canonical output |
| Typed output schema | `schemas/phonetic-result.schema.json` | Machine-readable unit result envelope |
| Existing tests | `tests/`, `scripts/export_rule_output_parity.py` | Python, browser, Worker, schema and cross-runtime behavior |
| Replica-skill | [Jakeschincariol/replica-skill](https://github.com/Jakeschincariol/replica-skill) | Recon → feature matrix → architecture → build → test → parity workflow |

## Core loop

Khmer input → Khmer structural analysis and Khmer phonology → typed IPA result → one IPA-only Ukrainian adapter → Ukrainian practical output with confidence and provenance preserved.

## Engine surfaces

| ID | Surface | Purpose | Acceptance state |
|---|---|---|---|
| S01 | Python `RuleBasedKhmerEngine` | Canonical rule engine and typed per-unit result | Implemented; Quality checks passed |
| S02 | Python typed IPA adapter | Tokenize supplied IPA and adapt only typed IPA | Implemented; Python tests passed |
| S03 | JavaScript engine core | Browser-equivalent result contract | Implemented; web checks passed |
| S04 | Web Worker / client | Run deterministic engine without network access | Existing Worker preserved; contract tests passed |
| S05 | CLI | Expose canonical, provisional and unresolved output | Implemented; CLI tests passed |
| S06 | Browser unit details | Show IPA status, provenance and uncertainty | Implemented; exact-head Chromium smoke pending |
| S07 | JSON schema and parity suite | Keep result shape inspectable and cross-runtime | Implemented; schema and parity checks passed |

## Flows

```
F01 Complete segmental IPA
    Khmer parser/rules → TypedPhoneticResult(UNCERTAIN) → adapt_phonetic_result → Ukrainian output

F02 Registered onset-only hint
    Khmer parser/onset registry → TypedPhoneticResult(PROVISIONAL)
    → same IPA adapter → known onset + ???

F03 No defensible hint
    source unit → TypedPhoneticResult(UNRESOLVED) → ???

F04 Valid IPA but no Ukrainian correspondence
    IPA remains UNCERTAIN → target adapter withholds Ukrainian mapping
    → no invented target correspondence

F05 Orthographic romanization fallback
    independent BGN/PCGN path → separately typed ORTHOGRAPHIC_ROMANIZATION_FALLBACK
    → never enters IPA adapter

F06 Browser execution
    UI → Worker → same JavaScript core → structured-clone-safe typed result
```

## Components

| Component | Responsibility |
|---|---|
| `PhoneticSegment` / `TypedPhoneticResult` | IPA segments, boundaries, length, tone slot, status, provenance and uncertainty |
| `from_ipa` | Parse supplied IPA notation independently of Ukrainian correspondence coverage |
| `from_provisional_ipa` | Keep registered IPA hints provisional and append one explicit unknown region |
| `from_unknown_source_unit` | Represent no defensible IPA hint without guessing |
| `adapt_phonetic_result` | Single IPA-only IPA → Ukrainian target boundary |
| Existing Khmer parser/rules/fixtures | Remain the only source of Khmer structural and phonological facts |
| Existing romanization path | Remains orthographic and separate |
| Existing hybrid provider API | Remains opt-in and non-canonical |

## Data model

```text
TypedPhoneticResult
  phonemic_ipa: string | null
  segments: PhoneticSegment[]
  syllable_boundaries: integer[]
  vowel_length: string | null
  tone_category: null unless explicitly supplied by an accepted source
  tone_contour_ipa: null unless explicitly supplied by an accepted source
  status: SUPPORTED | UNCERTAIN | PROVISIONAL | UNRESOLVED
  provenance: string[]
  uncertainty: string[]

PhoneticSegment
  ipa: string
  kind: vowel | consonant | modifier | boundary | tone | unknown
  provenance: string[]
  certainty: SUPPORTED | UNCERTAIN | PROVISIONAL | UNRESOLVED
```

## Out of scope

- Importing Lao phonological rules, grapheme values, lexica or pronunciation assumptions.
- Expanding Khmer vowel, coda, coeng, register-shifter or tone rules without source-backed evidence.
- Turning BGN/PCGN romanization into IPA.
- Automatically promoting external G2P candidates to canonical output.
- Claiming pronunciation accuracy while the independent adjudicated IPA gold corpus is empty.
- Deploying or publishing a release as part of this architecture PR.

## Size

Seven implementation surfaces, six core flows, one typed result model. Size: M. The difficult parts are confidence preservation, IPA/target separation, and exact Python/JavaScript parity.
