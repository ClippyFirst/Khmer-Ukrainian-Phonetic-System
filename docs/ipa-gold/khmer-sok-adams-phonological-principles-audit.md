# Sok & Adams (2016) — Khmer orthography-to-phonology source audit

**Audit date:** 2026-11-17  
**Primary source:** Makara Sok and Larin Adams, “Phonological Principles for Automatic Phonetic Transcription of Khmer Orthographic Words,” *Proceedings of PACLIC 30*, pp. 417–424.  
**ACL Anthology:** https://aclanthology.org/Y16-3013/  
**PDF:** https://aclanthology.org/Y16-3013.pdf  
**Disposition:** foundational rule-system comparator; not an independently validated benchmark, not project IPA gold, and not an approved source of target-profile rules.

## Why this source matters

The paper explicitly separates two conversion stages:

1. Khmer orthography → phonemic transcription, which the authors describe as representing careful speech.
2. Phonemic transcription → close phonetic transcription, which they describe as approximating rapid/ordinary colloquial speech.

This is a useful architectural precedent for keeping lexical/phonological analysis distinct from contextual phonetic realization. It does not establish that its specific output notation or dialect assumptions match the project's contemporary Phnom Penh careful-citation profile.

## Methods and data provenance

- The authors describe a 1967 fifth-edition Chuon Nath Khmer monolingual dictionary with about 17,000 entries. After cleanup and exclusion of Pali/Sanskrit material, 11,109 native-word entries remained.
- Their syllable grouping covered 10,110 words: 3,969 monosyllables, four disyllabic classes (1,249; 815; 769; 864), 1,963 double-monosyllabic words and 481 double-disyllabic words. Another 999 compounds were left out because their structures were not covered.
- The 140-word validation set was hand-selected to cover cases. Expected phonemic transcriptions were taken from Headley (1997); phonetic transcriptions were manually prepared by the authors. The paper does not describe independent double annotation, blind submission, adjudication, IAA, or a separately held-out speaker sample.
- The 10,110-word experiment compares generated phonemic forms with Headley's dictionary phonemic transcriptions. This is dictionary-derived comparison, not an independent audio-based pronunciation evaluation.
- Pali/Sanskrit loans were excluded from this stage; the conclusion explicitly identifies their pronunciation rules as future work.

## Rule-system findings

### Orthographic representation

The paper proposes an orthographic syllable sequence C(S)(D1)(V)(F)(D2), where C is a consonant, S a coeng/subscript consonant, D1 a series shifter, V a dependent or inherent vowel, F a final consonant, and D2 Bantoc. It notes that the inherent vowel is not written and that coeng may mark a subscript consonant in monosyllables or a syllable break in disyllabic forms.

This is a useful historical computational model, not a replacement for current Unicode 18.0 §16.4 or the repository's existing structural parser. Do not copy this notation as a normative grammar.

### Series assimilation

For onset clusters, the paper says the least-sonorous/strongest consonant determines the cluster series, using the hierarchy unaspirated plosives > aspirated plosives > fricatives > nasals > approximants. It also states that the series of a syllable-final consonant does not affect the preceding vowel's series.

For disyllabic words, the minor syllable's initial consonant may influence the major syllable's series; the paper gives examples of both cross-syllable assimilation and dissimilation. These are rule hypotheses that require comparison with the project's current source-grounded rules and profile; do not treat them as universal without specialist review.

### Vowel modification and sound changes

The paper discusses inherent/dependent vowel selection by consonant series, Bantoc-conditioned vowel modification, final devoicing, unreleased final plosives, implosive devoicing before another consonant, fricative/plosive backing in codas, trill deletion and nasal deletion before another nasal. Its tables contain OCR/typographic inconsistencies and use an idiosyncratic mixture of IPA symbols and ASCII length notation. The tables should be visually checked against the PDF before any rule is transcribed into a formal rule registry.

### Phonemic versus phonetic layer

The second stage adds cluster-transition aspiration and schwa, devoicing of sonorants after aspirated plosives, lack of audible releases for final plosives/nasals, and substantial reduction of minor syllables in rapid colloquial speech. Examples include /rə-/ → [rə-] or [lə-], /də-/ and /sə/ → [tə-], and /bə-/ → [pə-].

These are specifically described as rapid/colloquial realizations. They must not be injected into the careful-citation phonological output. The project should represent them only as a separate profile/context-conditioned phonetic layer if later validated for the intended variety.

## Reported results — interpretation boundary

The paper reports the following author-run results:

- On its hand-selected 140-word validation set, the reported phonemic transcription accuracy rises from 2.14% for character mapping alone to 97.86% after the listed rule stages.
- On its dictionary-derived 10,110-word set, it reports 98.43% overall, with per-syllable-group figures between 96.62% and 99.06%.

These values are **not** transferable to this repository. The 140-word set is hand-selected; the phonemic references are derived from Headley (1997); phonetic forms are author-produced; the larger experiment is also dictionary-derived; and no independent blind annotation or recorded-speech gold evaluation is reported. The paper does not provide a reproducible split or enough item-level data to independently recalculate its headline scores.

## Rights

The PACLIC 30 proceedings front matter (printed p. ii) says contributed-paper copyright is reserved by the respective authors and includes a general all-rights-reserved notice. No explicit open license for this paper was verified. The source is registered for bibliographic and research reference only; do not redistribute its PDF or copy tables/data into the repository absent a valid permission basis.

## Project disposition

- Use as a **supporting rule-system baseline** when comparing the current parser/phonology pipeline.
- Preserve the two-stage distinction: careful phonemic/phonological output is not the same object as rapid colloquial phonetic realization.
- Reconcile each claimed rule against primary linguistic sources, the project's target profile and existing code before implementing anything.
- Do not import its dictionary labels, 140-word list, reported scores or phonetic examples as project gold.
- Do not infer a Khmer IPA convention from its tables; the paper's notation is not a complete, formally specified, profile-approved IPA convention.
- Keep Sanskrit/Pali loans, compounds, lexical exceptions and unsupported structures explicit rather than forcing them through the native monosyllabic/disyllabic rules.

## Status

| Work item | Status | Evidence / acceptance |
|---|---|---|
| Full-text source review | DONE_VERIFIED | ACL Anthology PDF, pp. 417–424 inspected |
| Two-stage architecture relevance | DONE_VERIFIED | §§6–7 explicitly separate careful phonemic and rapid colloquial phonetic conversion |
| Rule transfer to project | TODO | Each rule needs independent source/profile review and regression evidence |
| Reuse of 140-word set or 10,110-word data | DEFERRED | Provenance and independence are insufficient for project gold; rights for data extraction are not established |
| Benchmark use of 97.86% / 98.43% | DEFERRED | Author-run dictionary/hand-selected evaluation is not comparable to the project's independent audio-based gold |
| IPA convention approval | BLOCKED | Requires qualified Phnom Penh Khmer phonetician and independent reviewer |
| Rights for redistribution | BLOCKED | No explicit open license for the contribution verified |

**No runtime rules, corpus rows, IPA labels, generated outputs or Ukrainian mappings were changed by this audit.**


## Visual table verification and rule-transfer disposition — 2026-11-17

The original ACL Anthology PDF was visually inspected on printed pp. 419–422 (PDF pages 3–6), including Tables 4–6 and §§6.1–7. This confirms that the text extraction's Khmer glyph/OCR corruption is material: the tables must not be copied or reconstructed from extracted text alone. The visual review supports the following rule-family inventory, but does not authorize transcription of individual table cells into project data.

| Paper rule family | Paper location / layer | Current repository comparison | Transfer disposition |
|---|---|---|---|
| Consonant manner/series grouping and D1 shifter-modified consonants | Table 4, p. 419; orthographic-to-phonemic preparation | The parser and phonology.py already resolve orthographic base series and a bounded register-shifter environment. This is not the paper's full cluster-series algorithm. | Do not duplicate existing shifter logic. Any additional cluster behavior needs an independent contemporary-profile source and expert review. |
| Series-conditioned vowel mapping | Table 5 and §6, p. 420 | resolve_inherent_vowel deliberately returns an orthographic series label, not an IPA vowel. The current IPA path does not adopt Table 5 as a complete surface-vowel map. | BLOCKED: paper notation, dialect/profile and source inventory are not approved for the selected careful-citation profile. |
| Initial-cluster series assimilation by sonority | §6.1, pp. 420–421; phonological/phonemic stage | Current register resolution does not implement the paper's cluster hierarchy or assign cluster series. | BLOCKED: requires verified phonological syllable/onset parsing, contemporary PPK evidence and expert-reviewed minimal/negative cases. Do not infer from orthographic cluster alone. |
| Minor-to-major syllable series influence and dissimilation | §6.2, pp. 421–422; disyllabic phonological structure | The runtime does not identify lexical words or implement this cross-syllable dependency. The orthographic parser is not a lexical or phonological syllabifier. | BLOCKED: depends on word/syllable analysis and profile-specific evidence; not safe to transfer from the paper's four historical word classes. |
| BANTOC-conditioned vowel modification/shortening | §6.3 and Table 6, p. 422; phonemic transcription stage | Existing PCGN Note 5 shortening resolvers are orthographic romanization components, not evidence that the paper's vowel alternations are correct for contemporary PPK IPA. | Keep layers separate. No IPA vowel rule may be derived from the PCGN resolver; expert review and source-located target-profile examples required. |
| Final devoicing, unreleased finals, implosive devoicing, fricative/plosive backing, trill/nasal deletion, vowel backing | §6.4, p. 422; paper labels these as sound-change rules used in its phonemic transcription | No corresponding source-approved PPK careful-citation IPA rules are implemented by the current register/inherent-vowel helpers. | BLOCKED: each environment needs independent contemporary evidence, a precise typed representation and positive/negative regression items. Final trill deletion must not be conflated with onset /r/-loss. |
| Cluster-transition aspiration, schwa transitions, sonorant devoicing after aspirated stops | §7, p. 422 onward; phonemic-to-phonetic rapid/ordinary speech stage | The project keeps phonological and phonetic layers distinct; no such colloquial transition rules are added to the careful-citation profile. | EXCLUDED from the current careful-citation profile unless a separately versioned speech-style profile is approved and validated. |

### Verified scope and remaining limitation

The visual check closes the source-reading subtask: Table 4–6 placement and the §6/§7 stage distinction were confirmed against page images rather than OCR alone. It does not resolve every symbol in the Khmer-font tables, provide a reusable source dataset, establish the paper's variety as identical to contemporary Phnom Penh careful citation, or create an approved IPA convention. Because the paper's contribution has no verified open data license and its wordlist/phonetic labels are not independent gold, no table values or example transcriptions were copied into runtime, tests, source CSVs or corpus files.

KHM-SOK-ADAMS-RULE-TRANSFER-001 is therefore reclassified from TODO to BLOCKED (evidence/profile approval gate), not marked complete. The completed bounded subtask is KHM-SOK-ADAMS-VISUAL-TABLE-AUDIT-001 = DONE_VERIFIED. A future rule transfer requires a qualified reviewer to approve the target-profile relevance, exact source/page locator, typed phonological-versus-phonetic layer, source/rights basis and positive/negative regression examples for each individual rule.
