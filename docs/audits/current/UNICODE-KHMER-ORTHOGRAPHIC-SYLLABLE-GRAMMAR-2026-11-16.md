# Unicode Khmer orthographic-syllable grammar reconciliation

**Date:** 2026-11-16  
**Scope:** Modern Khmer structural parsing only. This document does not define phonetic syllables, words, pronunciation, IPA, or Ukrainian output.

## Finding

Unicode Standard 18.0.0, Chapter 16 §16.4, gives the component-order formula:

`B {R | C} {S {R}}* {{Z} V} {O} {S}`

where B is a base character; R is robat; C is a consonant shifter; S is a subscript consonant or independent-vowel sign; V is a dependent vowel; Z is ZWJ or ZWNJ; and O is any other sign. Unicode Standard 18 Appendix A.2 defines braces as optional groups and `*` as zero or more repetitions. This is a real formal ordering contract, not a heuristic boundary rule.

The canonical parser now applies this BNF over the existing lossless `khmer-orthographic-components/v1` scanner. It returns complete orthographic-syllable segmentations and packs local grammar-role alternatives (including repeated-S versus trailing-S assignments) without Cartesian expansion. Exact source text and Unicode code-point offsets are preserved; ambiguity is explicit and no preferred parse is selected.

## Important source distinction

Unicode Technical Note #61, *Khmer Encoding Structure*, Version 2 (Martin Hosken; February 2025) is an implementation guideline, not a normative Unicode Standard annex. It explicitly discusses Modern Khmer separately from Middle Khmer and other languages written in Khmer script. Its Modern Khmer proposal gives a more constrained structure:

`Syllable = Base Robat? Coengs? Shifter? Vowels Modifiers Final?`

with (among other rules) up to two pre-vowel coengs, coeng-ro ordering, a cluster-final shifter, structured vowel positions, at most two non-spacing signs and one spacing final. It also describes syllable chaining: one phonetic syllable boundary can occur within a sequence that is treated as a single orthographic structure in some analyses. The note documents that earlier Unicode, Microsoft and HarfBuzz structures differed and that the proposed encoding order is intended to remove ambiguities.

Do not silently substitute TN #61 for Unicode Standard 18 §16.4, or present the note's proposed Modern Khmer restrictions as normative Unicode requirements. Conversely, do not treat the broad Unicode BNF alone as a complete Modern Khmer validity profile. They are different evidence layers and must remain separately identified in code and output provenance.

## Parser contract and implementation acceptance

1. Preserve the existing scanner as the lossless lexical/component layer; do not duplicate its Unicode inventory.
2. Add a typed parser result with exact source text and half-open Unicode code-point spans. Do not normalize source text implicitly.
3. Implement the Unicode 18 BNF as a distinct grammar/profile, with its terminal categories traceable to the scanner. Braces and repetition must follow Unicode Appendix A.2 semantics.
4. Parse continuous input without greedy commitment. Return all viable orthographic-syllable segmentations (or a packed parse forest with equivalent inspectable alternatives), explicit ambiguity status, and rejected spans/reasons. A single best parse must never be selected without independent evidence.
5. Keep orthographic syllables distinct from phonological syllables. Do not infer word boundaries or use syllable boundaries as lexical boundaries.
6. Add a separately named Modern Khmer TN #61 v2 validation profile only if its exact rule set is transcribed and source-located. Mark it PROPOSED/NON_NORMATIVE; do not merge its constraints into the Unicode 18 grammar.
7. Treat ZWJ/ZWNJ placement, shifter placement, robat/coeng combinations, multiple vowels, modifiers/finals, deprecated code points and Middle Khmer exceptions as explicit profile cases. A generic “other sign” fallback must not make an illegal order appear valid.
8. Maintain Python/browser semantic parity and source reconstruction. Shared fixtures cover Unicode 18 §16.4 and §16.4.1 examples, candidate parse trees, component-role assignments and rejection spans. TN #61 v2 positive/negative cases belong to a separately versioned Modern Khmer profile and must not be used to validate or silently constrain this Unicode 18 parser.
9. Do not generate IPA or Ukrainian output from this parser. Its output is structural evidence only.

## BNF ambiguity and role assignments

The BNF uses `S` both in the repeated `{S {R}}*` group and as a final optional `{S}`. For a base followed by one COENG pair (for example `ក្ក` or the Unicode example `ផ្ឯម`), both productions can consume the same subscript component. In `ផ្ឯម`, the B + COENG + independent vowel + final base sequence therefore has two grammar-role parses for the first orthographic unit, followed by a second base-started unit. The parser must preserve both parse trees (`SUBSCRIPT_CLUSTER` and `TRAILING_SUBSCRIPT`) even though the source spans and syllable boundaries are identical. Choosing one role would silently discard grammar ambiguity. This orthographic parse does not decide the word's single phonological syllable.

## Evidence examples already available

Unicode 18 Figure 16-3 examples include `ទេ`, `ច្រើន`, `សង្គ្រាម`, `ហើ្យ`, `សញ្ញា`, `ស៊ី`, and `ប៉ី`. §16.4.1 also documents shifter and join-control examples such as `ម៉្ងៃ`, `ម៊្ហែតៗ`, `ប‌៊ីយែរ`, `ប្រតឺងអ‌៊ឹះ`, `ប្រតឺងអ៊ឹះ`, `វ‌ិទូ`, and `វ‍ិទូ`, plus subscript-independent-vowel forms such as `ផ្ឯម`, `ឱ្យ`, `ឱ្ម`, and `ហ្ឫទ័យ`. These are structural fixtures only; the external repetition mark in `ម៊្ហែតៗ` is explicitly unsupported by the syllable parser. The IPA strings printed in the Standard are not a project-adjudicated gold corpus. Unicode 18 Figure 16-3 spells “already” as `ហើ្យ` (U+17A0 U+17BE U+17D2 U+1799), with COENG + YO after the dependent vowel. The un-subscripted spelling `ហើយ` (U+17A0 U+17BE U+1799) instead parses as two orthographic syllables (`ហើ` + `យ`) under the BNF. This contrast is a regression requirement: a consonant after a vowel is not automatically absorbed as a coda; the encoded COENG pair is decisive.

TN #61 v2 §§“Orthographic Syllable Structure”, “Coengs”, “Triisap and Muusikatoan”, “Vowels”, and “Signs” provide the proposed Modern Khmer grammar and constraints. The note's Appendix 2 separately discusses Middle Khmer; those exceptions must not be silently folded into the Modern Khmer profile.

## Task ledger

| Task | Status | Evidence / acceptance |
|---|---|---|
| Lossless component inventory and code-point spans | DONE_VERIFIED | `KHM-ORTHO-COMPONENT-SCAN-001`, PR #283, Python/browser schema and exact-main CI. |
| Reconcile Unicode 18 BNF syntax and TN #61 scope/status | DONE_VERIFIED | This source audit; Unicode Standard 18 Appendix A.2 and Chapter 16 §16.4; TN #61 v2 dated February 2025. |
| Unicode 18 BNF parser and ambiguous parse forest | DONE_VERIFIED | Packed Python/browser parser applies §16.4 and Appendix A.2; retains complete segmentation and grammar-role alternatives, exact offsets/source reconstruction, rejected spans/reasons, and shared Unicode 18 fixtures; exact-main Quality/Chromium/Pages passed. |
| Modern Khmer TN #61 v2 validation profile | TODO / NON_NORMATIVE | Source metadata is registered as `unicode-tn61-khmer-encoding-structure-v2`. Requires a separately versioned profile and source-located review of its constraints/exceptions; cannot be labelled Unicode normative. |
| Phonological syllabification and word segmentation | BLOCKED / SEPARATE | Requires linguistic/lexical evidence and independent annotation; neither grammar supplies a complete lexical word segmenter. |
| IPA gold and empirical accuracy | BLOCKED | Issue #104's independent annotation/adjudication gates remain open; gold remains empty. |

## Primary sources

- Unicode Consortium, *The Unicode Standard, Version 18.0.0*, Chapter 16 §16.4 Khmer: https://unicode.org/versions/Unicode18.0.0/core-spec/chapter-16/
- Unicode Consortium, *The Unicode Standard, Version 18.0.0*, Appendix A.2 Extended BNF: https://unicode.org/versions/Unicode18.0.0/core-spec/appendix-a/
- Unicode Consortium, *About Unicode Technical Notes* (independent/non-normative status and versioning): https://www.unicode.org/notes/about-notes.html
- Unicode Consortium, *Copyright, Terms of Use, and Licenses*: https://www.unicode.org/copyright.html
- Hosken, Martin, with Norbert Lindenberg and Makara Sok (2025-02-06), *Unicode Technical Note #61: Khmer Encoding Structure*, Version 2: https://www.unicode.org/notes/tn61/tn61-2.html and https://www.unicode.org/notes/tn61/utn61-Khmer_Encoding_Structure_V2.pdf; registry ID `unicode-tn61-khmer-encoding-structure-v2`.

## Verification boundary

Parser implementation and rejection diagnostics are now merged in main commit `8ec4460a0af291dcba10563912f8fcd0c3f784fd`. Exact-main Quality [43963765593] passed 416 Python tests + 70 subtests, IPA corpus structural validation, Node/web checks and production build. Exact-main Chromium [43963765334] and Pages deploy/runtime smoke [43963765391] also passed. Local tests were not run; all verification cited here is from GitHub Actions. TN #61 v2 remains a separately scoped non-normative profile TODO; no IPA gold, phonological syllabification or LOC word division was added.


### Implementation completion note — 2026-11-16

The Unicode 18 orthographic parser and its rejection diagnostics are now DONE_VERIFIED on main commit 8ec4460a0af291dcba10563912f8fcd0c3f784fd. The packed forest preserves grammar-role alternatives and derivation counts without expanding the Cartesian product. The Python and browser implementations expose the same typed contract, including rejected_spans with exact Unicode code-point offsets and reasons.

Shared fixtures cover all Figure 16-3 examples, the §16.4.1 shifter and join-control examples, subscript independent vowels, robat, and explicit unsupported/deprecated code points. The external repetition sign in ម៊្ហែតៗ remains outside the modeled syllable inventory and is reported as unsupported rather than swallowed by a generic O fallback.

Exact-main verification:
- Quality [43963765593] SUCCESS: 416 Python tests + 70 subtests; IPA corpus structural validation, Node/web checks, production build.
- Chromium [43963765334] SUCCESS.
- Pages deploy/runtime smoke [43963765391] SUCCESS.

TN #61 v2 source metadata is registered as unicode-tn61-khmer-encoding-structure-v2 with its independent/non-normative status and Unicode Terms of Use limitations. It remains a separate profile TODO and is not used to modify the Unicode 18 parser.
