# BGN/PCGN 1972 ↔ UNGEGN 2013 rule reconciliation

**Review date:** 2026-11-15  
**Project target:** BGN/PCGN 1972 Khmer romanization, followed by a separate Ukrainian orthographic adaptation.  
**Candidate inspected:** `pheasaKhmer/khmer-engine` at `31b72cd4665f69678fc835da2f501771e42f097a`.  
**Disposition:** research comparison only; no external code, dependency, lexical data, or pronunciation output imported.

## Executive result

UNGEGN 2013 explicitly says that the United Nations system was approved in 1972 (Resolution II/10) and was based on BGN/PCGN 1972, itself a modified SGK 1959 system. This historical relationship makes the UNGEGN report a valuable cross-check, but it does **not** establish that a particular implementation of the later report is a rule-for-rule implementation of the PCGN guide.

The candidate engine is explicitly an UNGEGN 2013 implementation. It is a useful architectural reference for parsing Khmer clusters, inferring syllable boundaries, resolving vowel series, and applying coda-sensitive romanization. It is not a drop-in replacement for the selected BGN/PCGN profile.

The review found one explicit series-resolution difference in the two published notes, plus candidate-specific extensions that the candidate source itself marks as absent from the UNGEGN tables or derived from secondary material. These are sufficient reasons to keep the candidate unadopted until a project-owned BGN/PCGN implementation and test oracle are built.

## Source set and scope

| Source | What it establishes | What it does not establish |
|---|---|---|
| UK PCGN, *Romanization of Khmer (Cambodian), BGN/PCGN 1972 Agreement*, checked October 2017 | Selected project's primary reference tables and notes for consonants, feet, vowels, shortened forms, diacritics and numerals. | Modern speech IPA or Ukrainian target correctness. |
| UNGEGN Working Group, *Current status of UN romanization systems*, version 4.0, September 2013, Khmer section | UN system history and its own tables/notes; explicit relation to BGN/PCGN 1972. | Automatic identity between all PCGN and UNGEGN implementation details. |
| Unicode Khmer character names list | Stable character identity and general sign semantics for shifters, BANTOC, SAMYOK SANNYA, ROBAT, etc. | The romanization values assigned by PCGN. |
| Candidate `khmer-engine` source and tests, pinned above | What that specific implementation actually does and tests. | Conformance to PCGN 1972 or independently adjudicated pronunciation. |
| This repository's PCGN matrices and runtime | Existing source-located inventory and current integration boundary. | A complete contextual Khmer-script → PCGN engine. |

Primary references:

- PCGN guide: https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf
- UNGEGN report: https://unstats.un.org/unsd/ungegn/working_groups/wg5/documents/wgrr4khmer.pdf
- Unicode Khmer names list: https://www.unicode.org/Public/UCD/latest/charts/nameslist/1780/
- Candidate rules: https://github.com/pheasaKhmer/khmer-engine/blob/31b72cd4665f69678fc835da2f501771e42f097a/src/khmer_engine/rules.py
- Candidate syllable parser: https://github.com/pheasaKhmer/khmer-engine/blob/31b72cd4665f69678fc835da2f501771e42f097a/src/khmer_engine/syllables.py
- Candidate character classes: https://github.com/pheasaKhmer/khmer-engine/blob/31b72cd4665f69678fc835da2f501771e42f097a/src/khmer_engine/script.py

## Rule-by-rule comparison

| Feature | BGN/PCGN 1972 guide | UNGEGN 2013 report | Candidate implementation | Assessment for this project |
|---|---|---|---|---|
| Profile lineage | Modified SGK 1959 system; selected PCGN agreement. | Says UN system was approved in 1972 and based on BGN/PCGN 1972. | Declares UNGEGN 2013 as its `ungegn` style. | Related profiles, not interchangeable by assumption. Keep PCGN as project target. |
| Consonant series | â-series / ô-series are assigned in the consonant table. | Same two-series framework. | `script.py` assigns A/O sets from UNGEGN table I. | Architecture reusable after source table parity review. |
| Subscript-series override | PCGN note 3: a foot determines the following nucleus series, except when the foot is a nasal (ង, ញ, ណ, ន, ម) or យ, រ, ល, វ; then the base consonant determines it. | UNGEGN note 3 lists the same neutral group **plus ស**. | `SERIES_NEUTRAL_SUBSCRIPTS` includes ស. | **Explicit rule delta.** For PCGN, do not treat ស as neutral based solely on the UNGEGN note. Add a source-backed PCGN test before implementing this branch. |
| Subscript ambiguity | PCGN says a reference may be needed to establish which consonant a foot represents; e.g. ្ដ/្ថ can represent different base consonants. | UNGEGN note 3 retains this warning and examples. | Parser uses structural cluster parsing; its series logic reads the chosen subscript. | Parser must preserve ambiguity/provenance; do not silently resolve uncertain foot identity. |
| Weak subscripts and base-series selection | PCGN weak list is the five nasals plus y/r/l/v. | UNGEGN weak list is five nasals plus y/r/l/v/s. | Candidate implements UNGEGN's longer set. | Do not copy this constant unchanged into a PCGN engine. |
| Register shifters | PCGN note 2: TRIISAP ◌៊ (U+17CA) changes â-series to ô-series, except for ប / បា; MUUSIKATOAN ◌៉ (U+17C9) changes ô-series to â-series. Marks may be omitted in source spelling. | UNGEGN note 2 carries the same broad series-switching rule and exceptions. | Candidate maps U+17C9 MUUSIKATOAN to A-series and U+17CA TRIISAP to O-series. | Preserve the exact Unicode identity and direction. A BA+TRIISAP form is not a p-in-â exception; it retains BA's ô-series. |
| ប / បា exception | PCGN note 3: ប with MUUSIKATOAN ◌៉ (U+17C9), and ប / បា with a foot, are romanized p in the â-series. | UNGEGN note 4 carries the corresponding exception. | Candidate emits p for bare ប in multi-consonant onset or with MUUSIKATOAN; subscript handling is separate. | The project resolver now keeps BA+TRIISAP (U+17CA) unshifted in ô-series and applies p-in-â only to BA+MUUSIKATOAN (U+17C9) or BA+foot. Regression tests cover both distinct cases. |
| Dependent vowels | PCGN table separates â-/ô-series and normal/shortened forms. | UNGEGN tables IV/V provide corresponding nucleus and shortened forms. | Candidate has explicit per-series nuclei. | Data shape is reusable; compare every row and source glyph before porting. Do not flatten series or shortened alternatives. |
| Coda-sensitive shortened vowels | PCGN note 5: in ô-series the shortened form is eă before k/ng/h, otherwise oă; â-series uses ă for the specified combinations. | UNGEGN note 6 states eă before k/ng/h, otherwise oă, with corresponding â-series values. | Candidate selects eă for final letters k, kh, ng, h; otherwise oă. | Candidate includes `kh` in its final set; verify against the exact PCGN note, which names k, ng, h. Do not silently expand a closed list without source evidence. |
| BANTOC and SAMYOK SANNYA | PCGN note 5 documents the shortened combinations ◌ា់ and ◌័. | UNGEGN note 6 gives the related shortened combinations and series-dependent values. | Candidate has separate `_AA_BANTOC` and `_SAMYOK` keys. | Core architecture aligns with inventory; exact structural patterns must follow PCGN's documented combinations, not a generic “mark shortens previous vowel” rule. |
| SAMYOK before final យ | PCGN published table/note does not provide a dedicated `SAMYOK + final y` output in the inspected guide. | UNGEGN published table/note does not provide a dedicated value in the inspected report. | Candidate adds `_SAMYOK_Y` and comments “not given”; README notes some forms need native-speaker checking. | **Unspecified extension.** Keep unsupported/uncertain under PCGN unless a primary source or expert adjudication supplies the rule. |
| YUUKALEAPINTU (ៈ) | No dedicated romanization value appears in the inspected PCGN vowel/diacritic tables. | No dedicated value appears in the inspected UNGEGN vowel/diacritic tables. | Candidate maps it to ă/eă and explicitly comments “not given; Wikipedia's table”. | **Secondary-source extrapolation.** Not accepted as PCGN/UNGEGN table behavior. Return an explicit unsupported/evidence-limited result until sourced. |
| NIKAHIT / REAHMUK combinations | PCGN has dedicated anusvara/visarga combinations and series values. | UNGEGN has corresponding Table V combinations and a final-sensitive shortened-vowel rule. | Candidate has explicit common combinations and a fallback that concatenates component vowel values plus m/h for unlisted combinations. | Only explicit table combinations are standard-backed. Generic fallback is a heuristic extension; label it and do not call it PCGN-compliant. |
| ROBAT | PCGN note 6: ◌៌ is romanized rC. | UNGEGN note 7: ◌៌ is romanized r before a consonant. | Candidate appends r at the syllable-level representation. | Core rule appears aligned; verify positioning with PCGN source patterns and ensure it does not become an arbitrary suffix rewrite. |
| TOANDAKHIAT / silent letters | PCGN note 8: the mark on unpronounced characters is not romanized. | UNGEGN note 9: corresponding silent mark is ignored. | Candidate suppresses silent syllables/finals in its `chat` style; its UNGEGN path must be checked independently. | Do not infer that chat-style suppression proves the UNGEGN/PCGN path. Add explicit profile-specific tests. |
| Word and syllable boundaries | PCGN warns that word division is not generally indicated and references may be needed. | UNGEGN states the same and notes romanization is generally not reversible. | Candidate uses Pheasa lexicon word segmentation and weighted Viterbi costs to infer syllable boundaries. | Useful architecture, but inferred segmentation is heuristic, not a normative rule. Preserve n-best/uncertainty or abstain where alternatives remain. |
| Independent vowel alternatives | PCGN explicitly says consult a reference for ŏ/ŭ uncertainty. | UNGEGN note 10 similarly says consult a reference. | Candidate selects ŏ as default for ឧ and has no uncertainty result in the romanized string. | Do not turn a default into certainty. Project API should preserve source uncertainty or emit PARTIAL. |
| IPA | PCGN/UNGEGN tables are romanization systems, not IPA transcriptions. | Same. | Candidate produces romanized Latin strings only. | Never use this output as IPA, phonetic gold, or a pronunciation oracle. |

### Important source-reading caution

The PDFs use Khmer glyphs and diacritics in embedded fonts; extracted text may render some marks ambiguously. The comparison above relies on the published note wording and visible PDF pages, and uses Unicode's character-name list to distinguish U+17C9 from U+17CA. Any future executable mark rule must cite both the original PCGN glyph/example and the exact Unicode code point. Do not derive code-point identity from a text extraction alone.

## Candidate architecture: what can be reused conceptually

1. **Explicit structural objects.** Its `Cluster` separates base, subscripts, shifter, dependent vowel and signs; its `Syllable` separates onset, nucleus, finals, robat and silent material. This is preferable to flattening Khmer into a code-point replacement map.
2. **Separate parsing from romanization.** `syllables.py` infers spoken syllables from written clusters, then `rules.py` applies the romanization profile. Preserve that boundary if independently implemented.
3. **Context-aware series and codas.** The engine represents series and chooses coda-conditioned shortened vowels explicitly.
4. **Regression fixtures.** Official report examples are useful source-located tests when their profile and expected output are checked against the PCGN guide.

These are design patterns only. The candidate parser's weighted costs (`_LEFT_OPEN_COST`, `_SPLIT_AFTER_VOWEL_COST`, `_DOUBLED_ONSET_COST`, etc.) are engineering preferences, not linguistic facts. A single best path is not evidence that the reading is uniquely determined. The current repository should not copy these costs or treat the candidate's output as adjudicated expected output.

## Candidate extensions and unsupported cases

The candidate source explicitly marks:
- SAMYOK SANNYA before final យ as “not given” and uses a custom key;
- YUUKALEAPINTU as “not given” and obtains its value from Wikipedia;
- some unlisted vowel + NIKAHIT / REAHMUK combinations by concatenating component values;
- the syllable boundary model as a weighted preference search.

Those behaviors must remain separate from the standards-backed table. For this project, an unsupported case should produce a typed PARTIAL/UNSUPPORTED result with source text and reason, not a plausible-looking romanization silently presented as official.

## Porting and acceptance plan

| Step | Status | Acceptance evidence required |
|---|---|---|
| Pin and inspect the PCGN guide and UNGEGN report | DONE_VERIFIED (this review) | Exact primary URLs and note/table locators above. |
| Identify the PCGN vs UNGEGN series-neutral subscript delta | DONE_VERIFIED (textual comparison) | PCGN note 3 vs UNGEGN note 3; explicit difference is inclusion of ស in UNGEGN neutral list. |
| Reconcile every PCGN vowel/nucleus row against the candidate table | PARTIAL | Machine-readable row-by-row diff with exact Khmer glyphs and values; no unresolved OCR/font ambiguities. |
| Verify all shifter and ប exceptions by exact code point and PCGN example | PARTIAL | Tests for U+17C9/U+17CA, both series directions, ប/បា exceptions, and omitted-mark uncertainty. |

Implementation note (2026-11-18): the bounded series resolver now emits an explicit warning when no shifter is encoded: PCGN Note 2 says Khmer diacritics are frequently omitted and directs users to consult a reference source when the series is uncertain. This warning does not infer a missing mark or change the graphemic series result; the complete source-context and lexical uncertainty task remains PARTIAL.
| Specify PCGN-safe syllable-boundary behavior | TODO | Human-reviewed ambiguity cases; preserve alternatives or abstain; no heuristic costs copied without evidence. |
| Implement project-owned contextual PCGN engine | TODO | Diacritic-preserving Khmer-script → PCGN output; typed unsupported results; parity against the PCGN guide and reviewed lexical fixtures. |
| Ukrainian adaptation | PARTIAL | Consume only validated PCGN output; retain source/romanization provenance; expert review of Ukrainian target convention. |
| IPA and empirical pronunciation validation | BLOCKED | Separate approved IPA convention and independent human annotation/adjudication under issue #104. |

## Disposition

- Keep `pheasaKhmer/khmer-engine` as `RESEARCH_CANDIDATE`; do not add it as a dependency.
- Do not import its bundled lexical sample or counts. Its code and data have separate license declarations; the engine README/metadata identifies MIT code, CC BY 4.0 pronunciation lexicon data and ODC-By 1.0 counts; its Pheasa dependency declares Apache-2.0. Rights review of the exact dependency and every data item would still be required before adoption.
- Do not change the selected profile from BGN/PCGN 1972 to UNGEGN 2013.
- Keep `KHM-ROM-ENGINE-001` PARTIAL and `KHM-ROM-UA-001` PARTIAL.
- Keep independent adjudicated IPA gold at 0 and empirical accuracy null.
- This review does not change runtime behavior, pronunciation labels, Ukrainian candidates, source corpora, or benchmark data.


## Regression coverage update — PCGN Note 3 BA+AA+foot (2026-11-19)

The guide's Note 3 explicitly names both bare BA (`ប`) and BA+AA (`បា`) with a foot. PR #405 extends the existing BA+foot test to both `ប្ក` and `ប្កា`, asserting the AA sign remains structurally recognized and the series resolver continues to select the documented p-in-â exception. This is test coverage for an existing bounded resolver, not a new contextual romanization rule.

Exact PR-head CI on `6b4ed2bbd0a575d39fe0865082f854511c32cb4a`: Quality [44482081471](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44482081471) SUCCESS (437 tests + 70 subtests); push Quality [44482061657](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44482061657) SUCCESS; browser [44482081280](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44482081280) SUCCESS (21/21).
