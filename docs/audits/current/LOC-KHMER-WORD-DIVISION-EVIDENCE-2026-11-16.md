# ALA-LC Khmer word division: versioned evidence and implementation boundary

**Date:** 2026-11-16  
**Status:** EVIDENCE_RECONCILED; segmentation implementation remains TODO / evidence-limited.

## Finding

The phrase “shortest written form which can stand alone as a word” is present in the Library of Congress's historical Khmer romanization guidance and in the 1997 ALA-LC Khmer table. It is **Note 10**, not Note 9:

- The 1989 *Cataloging Service Bulletin* No. 43, Khmer section, p. 54, Note 10 says Khmer words are not separately written, and in romanization the shortest written form that can stand alone as a word is treated as such. It explicitly extends that treatment to Pali and Sanskrit loan-words; other loan-words retain divisions from their source language.
- The 1997 ALA-LC *Khmer Romanization Table*, pp. 97–98, Note 10 repeats the same shortest-standalone-form rule and the same loan-word distinction.
- The surfaced 2013 ALA-LC *Khmer Romanization Table* has revised wording at **Note 8**: “Any word can be separated when romanizing.” It again says Pali/Sanskrit loans follow this rule and other loan-words are divided according to their original language. This is not identical wording to the 1997 rule. Do not silently treat the 1997 and 2013 versions as a single unchanged algorithm.

## Do not conflate the profiles or note numbers

- BGN/PCGN 1972 **Note 9** concerns the ambiguous romanization of independent vowel ឧ as ŏ or ŭ and reference-source consultation. It is unrelated to word division.
- ALA-LC 1997 **Note 10** is the shortest-standalone-form rule.
- ALA-LC 2013 **Note 8** is the any-word-may-be-separated formulation.
- Cambodia's national 1995/1997 transcription system, BGN/PCGN 1972 and ALA-LC 1997/2013 are distinct profiles. Evidence from one must not be used to fill another's rule table.

## Segmentation-engine implications

Neither LOC note defines a complete machine segmentation algorithm, a lexicon, a POS model, compound decomposition policy, ambiguity ranking, or a complete set of annotated examples. The 1997 rule presupposes evidence about which written form is independently lexical; the 2013 rule still presupposes a defensible word analysis and source-language handling for non-Pali/Sanskrit loans.

A longest-match dictionary segmenter, bidirectional maximal matching, syllable segmenter, or Khmer character-cluster parser is therefore **not by itself proof of conformance**. Such tools may be candidate generators or structural components only. Their outputs need a separately versioned lexicon, provenance, language-of-origin metadata, ambiguity representation and human-reviewed boundaries.

The LaoNLP route previously inspected is not accepted as a drop-in implementation: orthographic syllable segmentation is not word segmentation, and dictionary maximal matching does not establish the LOC lexical criterion or loan-word exception. Keep it as a rejected integration candidate unless a future evaluation demonstrates the required rule behavior on a licensed, independently annotated test set.

## Required acceptance contract before canonical implementation

1. Declare the exact profile/version (at minimum ALA-LC 1997 versus ALA-LC 2013); never use an unversioned “LOC” profile.
2. Preserve source code-point offsets and Khmer grapheme/cluster integrity; do not split inside a Khmer orthographic cluster.
3. Represent word-boundary evidence and uncertainty explicitly. Do not invent boundaries from longest match alone.
4. For ALA-LC 1997, model lexical standalone-form evidence, including whether a form can stand alone; distinguish Pali/Sanskrit loans from other loans.
5. For ALA-LC 2013, support word separation as permitted by Note 8 and preserve original-language divisions for other loan-words; still require lexical evidence for the actual word sequence.
6. Preserve competing analyses when the source does not determine one boundary sequence. Abstain rather than select a convenient segmentation.
7. Keep word segmentation upstream of romanization and separate from syllable parsing, phonological analysis, IPA and Ukrainian adaptation.
8. Add licensed, source-located examples and independently reviewed boundary annotations before claiming conformance or benchmark accuracy.

## Evidence and references

- Library of Congress, *Khmer Romanization Table*, 1997 version, Note 10, pp. 97–98: https://www.loc.gov/catdir/cpso/romanization/khmer-1997.pdf
- Library of Congress, *Khmer Romanization Table*, 2013 version, Note 8, p. 3: https://www.loc.gov/catdir/cpso/romanization/khmer.pdf
- Library of Congress, *Cataloging Service Bulletin*, No. 43, Winter 1989, Khmer Romanization, Note 10, p. 54: https://www.loc.gov/aba/publications/FreeCSB/CSB_043.pdf
- BGN/PCGN 1972, Note 9 (different rule; independent vowel ឧ): https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf
- Mao et al. (2022), “Bi-directional Maximal Matching Algorithm to Segment Khmer Words in Sentence,” *Journal of Information Processing Systems* 18(4), 549–561, DOI: https://doi.org/10.3745/JIPS.04.0250. This is an NLP segmentation method, not a normative interpretation of ALA-LC word division.

## Task ledger

| Task | Status | Reason / acceptance |
|---|---|---|
| Define a profile-neutral, provenance-bearing boundary-evidence payload | DONE_VERIFIED | `schemas/word-boundary-evidence.schema.json` and `src/khmer_ua/word_boundaries.py`; validates code-point offsets, caller-protected cluster spans, competing candidates and adjudication evidence; never chooses a segmentation. |
| Locate and compare LOC 1989/1997/2013 word-division wording | DONE_VERIFIED | Primary LOC sources checked; note numbering and wording differences recorded above. |
| Select one canonical LOC profile/version for runtime | TODO | Project owner/product decision; require explicit profile selection. |
| Build lexical boundary evidence/lexicon with provenance and loan-word classes | BLOCKED | No reviewed, rights-cleared lexicon or boundary gold set is available. |
| Implement deterministic profile-aware word segmentation | TODO / EVIDENCE_LIMITED | Only after profile and lexical evidence are established; uncertain cases must remain ambiguous. |
| Evaluate LaoNLP or another segmenter as a candidate generator | DEFERRED | No conformance claim; can be reconsidered after a licensed annotated evaluation set exists. |
| Claim LOC-conformant segmentation or empirical accuracy | BLOCKED | No independent boundary annotation/adjudication or held-out test set. |


## Profile-neutral boundary-evidence interface — 2026-11-16

A typed evidence container is now available at `src/khmer_ua/word_boundaries.py`, exported from the package and specified by `schemas/word-boundary-evidence.schema.json`.

The interface deliberately does **not** implement a word segmenter and does not select ALA-LC 1997 or 2013. It records:

- exact source text and Unicode code-point offsets;
- optional paired profile identifier/version (both absent until selected);
- protected orthographic-cluster spans supplied by an upstream reviewed parser;
- one or more competing boundary candidates;
- per-boundary evidence type, source locator, status and loan-language metadata;
- an adjudicated candidate only when each selected boundary has explicit adjudicated evidence.

A boundary inside a protected cluster is rejected. Multiple viable candidates remain AMBIGUOUS. Proposed or unresolved candidates never populate `selected_boundaries`. The module does not infer cluster spans, lexical independence, word origins, or boundaries.

**Acceptance:** `KHM-WORD-BOUNDARY-EVIDENCE-001 = DONE_VERIFIED` after exact-head CI. This closes only the data-contract/interface task. Profile selection, licensed lexical evidence, actual segmentation and independent boundary gold remain open under the ledger above.


## Post-merge verification — 2026-11-16

The profile-neutral evidence interface was merged in PR #281 as `50ae3538a624cf78781411c08ebcf51f73fcb5c2`. Exact-main Quality `43940735723`, browser smoke `43940735738`, and Pages deploy `43940735610` succeeded. This verifies the data contract and its engineering integration only; it does not satisfy the still-open profile-selection, licensed-lexicon, boundary-annotation or segmentation-conformance gates.


## Khmer subscript-pair structure checkpoint — 2026-11-16

Unicode Standard 18.0.0 Chapter 16, section 16.4.1, documents subscript independent-vowel signs and gives `ផ្ឯម` as an orthographic example (base consonant + U+17D2 COENG + U+17AF independent vowel + consonant). The parser previously accepted COENG only when followed by a modeled consonant, incorrectly treating this documented subscript-independent-vowel sequence as malformed.

The parser now records the pair as one `KhmerGrapheme(kind="subscript_independent_vowel")`, retains a separate `subscript_independent_vowels` field, adds the Unicode 18 source locator for this feature, and exposes `khmer_subscript_sequence_spans()` with exact-source Unicode code-point offsets. Those spans cover only the encoded COENG + following-character pair. They are not complete orthographic-syllable spans, and they must not be interpreted as word boundaries. No IPA or Ukrainian value is added; phoneticization remains explicitly not established for the example.

Unicode UAX #29 extended grapheme clusters remain a default text-segmentation model, not a complete Khmer orthographic-syllable grammar. The Unicode Standard's Khmer chapter separately documents the encoding structure and component order. This change therefore adds a narrowly scoped structural primitive and does not claim full grapheme-cluster or syllable segmentation.

**Task ledger update:** `KHM-STRUCT-SUBSCRIPT-INDEPENDENT-VOWEL-001 = DONE_VERIFIED` after exact PR-head and exact-main hosted Python/quality, browser, and Pages checks. The existing profile-neutral word-boundary interface can consume the returned spans as protected intervals, but still does not infer lexical boundaries.

**Primary source:** Unicode Standard 18.0.0, Chapter 16, §16.4.1, Khmer Subscript Consonants and Subscript Independent Vowel Signs: https://www.unicode.org/versions/Unicode18.0.0/core-spec/chapter-16/ . The Unicode chapter describes COENG + following code point as a single unit for most processing purposes. The implementation protects only that two-code-point pair.


**Post-merge verification:** PR #282 merged as `dd94f637674ad5ce599ee439584b88b6dba4db1e`. Exact-main Quality [43947114555] succeeded (393 Python tests + 70 subtests, corpus validation, Node/web checks and production build); Chromium [43947114448] succeeded; Pages build/deploy and deployed-runtime smoke [43947114535] succeeded. This closes only the structural subscript-independent-vowel task. The word-segmentation evidence blockers and Issue #104 remain open.


## Unicode 18 orthographic component scan — 2026-11-16

The repository now has a component inventory in `src/khmer_ua/orthographic_structure.py`, mirrored by the browser runtime and serialized as `khmer-orthographic-components/v1`. It identifies base letters, COENG subscript pairs, robat, register shifters, dependent vowels, join controls and other modeled signs with exact code-point offsets. Unicode 18 Chapter 16 §16.4 is the primary source for the component roles and order; UAX #29 Revision 49 is registered separately for default grapheme and word boundary behavior.

**Current parser boundary:** the scanner remains the lossless component layer; the canonical Unicode 18 §16.4 parser now validates component order and returns packed orthographic-syllable alternatives with exact code-point spans. Ambiguous grammar-role assignments are preserved, and unsupported ordering is not repaired heuristically. These are orthographic-syllable candidates, not lexical words, phonological syllables or LOC boundaries. They are not automatically inserted into the word-boundary interface as protected clusters; that requires explicit profile selection and review.

**Task ledger:** `KHM-ORTHO-COMPONENT-SCAN-001 = DONE_VERIFIED`; `KHM-ORTHO-BNF-PARSER-001 = DONE_VERIFIED` for Unicode 18 structural parsing and packed alternatives; LOC profile selection, lexical word segmentation and the human evidence gate in Issue #104 remain open.


**Exact-main evidence:** PR #283 merged as `bdc15daf6f7c40a6c088e306343a421b9347e9c1`. Exact PR-head Quality [43953219338] and Chromium [43953219579] succeeded. Exact-main Quality [43953449784] passed 402 Python tests + 70 subtests, independent IPA corpus structure validation, Node/web checks and production build; Chromium [43953449807] succeeded; Pages deploy and deployed runtime smoke [43953450103] succeeded. No local test execution is claimed.


## Unicode 18 orthographic-syllable parser — post-merge status — 2026-11-16

The complete Unicode 18 §16.4 parser is merged in main as 8ec4460a0af291dcba10563912f8fcd0c3f784fd. It builds on the component scanner and subscript-independent-vowel primitive, retains complete segmentation alternatives and local grammar-role alternatives in a packed forest, reports derivation counts, preserves source text/code-point offsets, and includes rejected component spans/reasons. Python and browser implementations share the schema contract.

Exact-main verification: Quality [43963765593] passed 417 Python tests + 70 subtests, IPA corpus structural validation, Node/web checks and production build; Chromium [43963765334] passed; Pages deploy/runtime smoke [43963765391] passed.

This closes only Unicode orthographic-syllable parsing. It does not select ALA-LC 1997 or 2013, infer lexical independence, classify loan words, choose LOC boundaries, or create a segmenter. The profile-neutral word-boundary evidence interface remains separate; the parser's syllable spans may be candidate protected intervals only after explicit profile selection and review. Licensed lexical evidence, adjudicated word boundaries and held-out evaluation remain blocked.


## Final parser/handoff verification — 2026-11-16

PR #296 merged the final handoff as 1cecfa86e098fb3e96a7a55954010840f28ddb84. Exact-main Quality [43964140244] passed 417 Python tests + 70 subtests; Chromium [43964140341] passed; Pages deploy/runtime smoke [43964140290] passed. This verifies the current parser and documentation state only. The Unicode parser returns orthographic-syllable candidates; LOC lexical word boundaries still require a separately selected profile, reviewed protected-cluster policy, licensed lexical evidence, adjudicated examples and held-out evaluation. Issue #104 remains OPEN.
