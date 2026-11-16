# Unicode Khmer orthographic-syllable grammar reconciliation

**Date:** 2026-11-16  
**Scope:** Modern Khmer structural parsing only. This document does not define phonetic syllables, words, pronunciation, IPA, or Ukrainian output.

## Finding

Unicode Standard 18.0.0, Chapter 16 §16.4, gives the component-order formula:

`B {R | C} {S {R}}* {{Z} V} {O} {S}`

where B is a base character; R is robat; C is a consonant shifter; S is a subscript consonant or independent-vowel sign; V is a dependent vowel; Z is ZWJ or ZWNJ; and O is any other sign. Unicode Standard 18 Appendix A.2 defines braces as optional groups and `*` as zero or more repetitions. This is a real formal ordering contract, not a heuristic boundary rule.

The initial `khmer-orthographic-components/v1` implementation was a lossless scanner only. It has since been extended by a separate `khmer-orthographic-syllables/v1` parser that validates the Unicode 18 BNF over that inventory, identifies complete orthographic-syllable spans, preserves grammar-role ambiguity in a packed forest, and reports exact rejected spans. The scanner remains a distinct layer.

## Important source distinction

Unicode Technical Note #61, *Khmer Encoding Structure*, Version 2 (Martin Hosken; February 2025) is an implementation guideline, not a normative Unicode Standard annex. It explicitly discusses Modern Khmer separately from Middle Khmer and other languages written in Khmer script. Its Modern Khmer proposal gives a more constrained structure:

`Syllable = Base Robat? Coengs? Shifter? Vowels Modifiers Final?`

with (among other rules) up to two pre-vowel coengs, coeng-ro ordering, a cluster-final shifter, structured vowel positions, at most two non-spacing signs and one spacing final. It also describes syllable chaining: one phonetic syllable boundary can occur within a sequence that is treated as a single orthographic structure in some analyses. The note documents that earlier Unicode, Microsoft and HarfBuzz structures differed and that the proposed encoding order is intended to remove ambiguities.

Do not silently substitute TN #61 for Unicode Standard 18 §16.4, or present the note's proposed Modern Khmer restrictions as normative Unicode requirements. Conversely, do not treat the broad Unicode BNF alone as a complete Modern Khmer validity profile. They are different evidence layers and must remain separately identified in code and output provenance.

## Parser contract to implement

1. Preserve the existing scanner as the lossless lexical/component layer; do not duplicate its Unicode inventory.
2. Add a typed parser result with exact source text and half-open Unicode code-point spans. Do not normalize source text implicitly.
3. Implement the Unicode 18 BNF as a distinct grammar/profile, with its terminal categories traceable to the scanner. Braces and repetition must follow Unicode Appendix A.2 semantics.
4. Parse continuous input without greedy commitment. Return all viable boundary segmentations and local grammar-role alternatives in a packed parse forest, exact derivation counts, explicit ambiguity status, and rejected spans/reasons. A single best parse must never be selected without independent evidence.
5. Keep orthographic syllables distinct from phonological syllables. Do not infer word boundaries or use syllable boundaries as lexical boundaries.
6. Add a separately named Modern Khmer TN #61 v2 validation profile only if its exact rule set is transcribed and source-located. Mark it PROPOSED/NON_NORMATIVE; do not merge its constraints into the Unicode 18 grammar.
7. Treat ZWJ/ZWNJ placement, shifter placement, robat/coeng combinations, multiple vowels, modifiers/finals, deprecated code points and Middle Khmer exceptions as explicit profile cases. A generic “other sign” fallback must not make an illegal order appear valid.
8. Maintain Python/browser semantic parity and source reconstruction. Shared fixtures cover Unicode 18 §16.4 examples, ZWJ/ZWNJ placement, shifters, robat, malformed/unsupported components and explicit grammar ambiguity. TN #61 examples are not silently treated as normative Unicode tests; any TN #61 profile requires its own source-located fixture set and rights review.
9. Do not generate IPA or Ukrainian output from this parser. Its output is structural evidence only.

## BNF ambiguity and role assignments

The BNF uses `S` both in the repeated `{S {R}}*` group and as a final optional `{S}`. For a base followed by one COENG pair (for example `ក្ក` or the Unicode example `ផ្ឯម`), both productions can consume the same subscript component. In `ផ្ឯម`, the B + COENG + independent vowel + final base sequence therefore has two grammar-role parses for the first orthographic unit, followed by a second base-started unit. The parser must preserve both parse trees (`SUBSCRIPT_CLUSTER` and `TRAILING_SUBSCRIPT`) even though the source spans and syllable boundaries are identical. Choosing one role would silently discard grammar ambiguity. This orthographic parse does not decide the word's single phonological syllable.

## Evidence examples already available

Unicode 18 Figure 16-3 examples include `ទេ`, `ច្រើន`, `សង្គ្រាម`, `ហើ្យ`, `សញ្ញា`, `ស៊ី`, and `ប៉ី`; the shared regression set also covers `ខ្ញុំ`. §16.4.1 also documents subscript-independent-vowel forms such as `ផ្ឯម` and subscripted vowels attached to independent-vowel bases. These must be represented as structural examples only; the IPA strings printed in the Standard are not a project-adjudicated gold corpus. Unicode 18 Figure 16-3 spells “already” as `ហើ្យ` (U+17A0 U+17BE U+17D2 U+1799), with COENG + YO after the dependent vowel. The un-subscripted spelling `ហើយ` (U+17A0 U+17BE U+1799) instead parses as two orthographic syllables (`ហើ` + `យ`) under the BNF. This contrast is a regression requirement: a consonant after a vowel is not automatically absorbed as a coda; the encoded COENG pair is decisive.

TN #61 v2 §§“Orthographic Syllable Structure”, “Coengs”, “Triisap and Muusikatoan”, “Vowels”, and “Signs” provide the proposed Modern Khmer grammar and constraints. The note's Appendix 2 separately discusses Middle Khmer; those exceptions must not be silently folded into the Modern Khmer profile.

## Task ledger

| Task | Status | Evidence / acceptance |
|---|---|---|
| Lossless component inventory and code-point spans | DONE_VERIFIED | `KHM-ORTHO-COMPONENT-SCAN-001`, PR #283, Python/browser schema and exact-main CI. |
| Reconcile Unicode 18 BNF syntax and TN #61 scope/status | DONE_VERIFIED | This source audit; Unicode Standard 18 Appendix A.2 and Chapter 16 §16.4; TN #61 v2 dated February 2025. |
| Unicode 18 BNF parser and packed ambiguous parse forest | DONE_VERIFIED | Python/browser parser and versioned schema; exact code-point offsets and source reconstruction; explicit repeated/final-S role ambiguity; packed local alternatives and exact derivation counts; rejected spans/reasons. Exact-main commit `d773dd7f0bcc0b6ab0f7a241e2b7b9857e2aef72`: 416 Python tests + 70 subtests, Node/web checks, Chromium smoke, production build and Pages deployment/runtime smoke all SUCCESS. |
| TN #61 v2 source registry and rights traceability | DONE_VERIFIED | `unicode-tn61-v2` records official version/date/authors/scope and Unicode Terms of Use restrictions; reference-only, with no copied prose or sample implementation. |
| Modern Khmer TN #61 v2 validation profile | TODO / NON_NORMATIVE | Requires a separately versioned profile and full source-located transcription of its regex constraints and exceptions; cannot be labelled Unicode normative. Public reuse of note content is not established; obtain permission before reproducing any content/sample implementation. |
| Phonological syllabification and word segmentation | BLOCKED / SEPARATE | Requires linguistic/lexical evidence and independent annotation; neither grammar supplies a complete lexical word segmenter. |
| IPA gold and empirical accuracy | BLOCKED | Issue #104's independent annotation/adjudication gates remain open; gold remains empty. |

## Primary sources

- Unicode Consortium, *The Unicode Standard, Version 18.0.0*, Chapter 16 §16.4 Khmer: https://unicode.org/versions/Unicode18.0.0/core-spec/chapter-16/
- Unicode Consortium, *The Unicode Standard, Version 18.0.0*, Appendix A.2 Extended BNF: https://unicode.org/versions/Unicode18.0.0/core-spec/appendix-a/
- Hosken, Martin, with Norbert Lindenberg and Makara Sok (February 2025), *Unicode Technical Note #61: Khmer Encoding Structure*, Version 2: https://www.unicode.org/notes/tn61/utn61-Khmer_Encoding_Structure_V2.pdf

## Verification boundary

The parser is implemented and exact-main verified. `parse_count` is an exact decimal derivation count; `segmentation_count` counts distinct boundary paths. Local grammar-role alternatives are packed per syllable, avoiding Cartesian expansion; a 20-unit regression verifies 2^20 derivations without expanding the full product. A cap of 128 distinct boundary segmentations returns `EVIDENCE_LIMITED` with a diagnostic span and no selected parse. Unknown/malformed characters are rejected with code-point spans and reasons. The parser implements Unicode Standard 18 §16.4 only; TN #61 v2 remains a separate non-normative profile. No IPA, phonological syllabification, LOC word segmentation or Ukrainian output is created. Exact-main `d773dd7f0bcc0b6ab0f7a241e2b7b9857e2aef72`: Quality `43962887689` SUCCESS (416 Python tests + 70 subtests, Node/web checks and production build); Chromium smoke `43962887588` SUCCESS; Pages deploy and deployed-runtime smoke `43962887592` SUCCESS. No local checkout was available; verification cited here is hosted GitHub Actions.
