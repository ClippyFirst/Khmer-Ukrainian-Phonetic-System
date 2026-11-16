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
| Locate and compare LOC 1989/1997/2013 word-division wording | DONE_VERIFIED | Primary LOC sources checked; note numbering and wording differences recorded above. |
| Select one canonical LOC profile/version for runtime | TODO | Project owner/product decision; require explicit profile selection. |
| Build lexical boundary evidence/lexicon with provenance and loan-word classes | BLOCKED | No reviewed, rights-cleared lexicon or boundary gold set is available. |
| Implement deterministic profile-aware word segmentation | TODO / EVIDENCE_LIMITED | Only after profile and lexical evidence are established; uncertain cases must remain ambiguous. |
| Evaluate LaoNLP or another segmenter as a candidate generator | DEFERRED | No conformance claim; can be reconsidered after a licensed annotated evaluation set exists. |
| Claim LOC-conformant segmentation or empirical accuracy | BLOCKED | No independent boundary annotation/adjudication or held-out test set. |
