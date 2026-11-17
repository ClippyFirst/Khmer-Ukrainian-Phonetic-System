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
