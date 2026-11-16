# Khmer IPA convention sheet — expert-review draft

**Document ID:** `khmer-pph-careful-citation-ipa-v1-draft`  
**Status:** `DRAFT_NOT_APPROVED` — research synthesis for specialist review; not an annotation authority and not a release gate pass.  
**Target profile:** `khmer-pph-careful-citation-v1` — contemporary Phnom Penh Khmer, careful citation-form speech (project-local profile identifier).  
**Proposed corpus IPA kind:** `PHONETIC_BROAD` (provisional recommendation; requires explicit expert approval before annotation).  
**Prepared:** 2026-11-17

## 1. Purpose and non-goals

This sheet proposes a reproducible *annotation policy* for a small, controlled pilot. It does not claim to supply a complete Khmer phonological grammar, a complete orthography-to-IPA mapping, or a set of gold pronunciations. No IPA value may be inferred solely from a Unicode character, romanization, dictionary token, G2P output, or the annotator's unrecorded intuition.

The pilot profile is deliberately narrow. Do not pool colloquial Phnom Penh, other Cambodian regions, Khmer varieties in Vietnam/Thailand, Western Khmer, diaspora speech, or Standard Khmer reading tasks that are not demonstrated to match the selected profile. Record any elicitation/task mismatch rather than silently relabeling it.

The Unicode 18 orthographic-syllable parser supplies structural analysis only. It does not decide phonological syllables, word boundaries, pronunciations, or IPA. Orthographic transliteration and practical Ukrainian output remain separate downstream tasks.

## 2. Evidence hierarchy and known limits

Use evidence in this order:

1. A consented recording from a speaker verified for the target profile, with task instructions and lexical context preserved.
2. A specialist-reviewed, profile-matched primary phonetic study or rights-cleared audio with sufficient metadata.
3. Multiple independent specialist descriptions that agree on the relevant contrast.
4. Candidate lexicons and model outputs only as *discovery prompts*, never as labels.

### Source-backed observations

- Minegishi's description explains why a vowel sign cannot be mapped independently of the consonant's orthographic series, and why some vowel readings are additionally conditioned by the coda. It distinguishes formal/school pronunciation from colloquial Phnom Penh outcomes for particular contrasts and documents dialect mergers. It is a systematic partial account, not a complete formal G2P algorithm [Min85].
- Chem's acoustic study uses four selected Phnom Penh speakers for its final acoustic analysis, with 61 lexical items read formally three times in a carrier frame. It measures F1/F2 and duration; it does not measure F0 or stress, and it does not provide a complete IPA convention. Its proposed inventory and some duration prose require expert review [Vat20].
- Mam, Pittayaporn & Maspong compare Phnom Penh and Standard Khmer using 50 target words, five Greater Phnom Penh speakers, three repetitions, and F0 trajectories from stressed rimes. The paper reports possible pitch phonologization in PPK, but it is a bounded controlled wordlist study, not a perception study or a complete citation-form transcription policy [Mam25].
- Kirby's work documents the colloquial PPK /r/-loss pathway and associated pitch, aspiration/VOT, breathiness and sometimes vowel-quality cues. These cues must not be collapsed into a categorical spelling-to-[h] rule or imported into the careful-citation profile without direct evidence [Kir14].
- Sodimana et al. describe generic cross-language TTS lexicon/audio procedures but do not specify Khmer-specific dialect, IPA convention, annotator counts, or agreement results [Sod18]. The audited Google lexicon is therefore a phonemic comparator, not strict IPA gold.

### Evidence limitations

The sources do not yet jointly provide an expert-approved, exhaustive, reproducible segment-by-segment transcription convention for this exact profile. In particular, there is no approved complete consonant/vowel/coda table, no profile-specific F0/tone policy, no expert ruling on all series-conditioned allophones, and no blind pilot evidence. All decisions below are proposed conservative defaults for review, not established facts.

## 3. Proposed annotation type and notation

**Proposed type:** `PHONETIC_BROAD`, because the pilot is intended to record the surface pronunciation of a defined careful-reading task, while preserving only phonetic detail supported by the recording and convention. This proposal must be approved or replaced by the Khmer expert panel before any annotation begins.

- Use square brackets `[...]` for the primary broad phonetic transcription.
- Do not mix phonemic slashes `/.../` into the same field. If an underlying phonemic analysis is separately requested, store it in a distinct typed field or note; never silently convert one type into the other.
- Use IPA symbols and combining diacritics only where their values are defined in the approved symbol table. NFC normalization is required; do not let normalization erase meaningful tie bars or diacritics.
- Do not add narrow phonetic detail merely to make a transcription look precise. Mark a detail only when it is audible/measurable and the convention defines it.
- Preserve syllable boundaries as structured boundaries and, when represented in the IPA string, use `.` consistently. Do not equate Unicode orthographic syllable boundaries with phonological syllable boundaries.
- Use primary stress mark `ˈ` only if stress/prominence is reliably identified under the approved task and annotation rule. Do not infer stress from orthographic position, word length, or a generic Khmer stress rule.
- Use length mark `ː` only for a long segment supported by the approved profile convention and token evidence. Do not mix colon, doubled vowels, and breve as competing length encodings. Shortness is unmarked unless the approved convention requires otherwise.
- Do not use tone letters/diacritics for a pitch trace unless the expert panel establishes a contrastive tonal analysis and an explicit mapping from measured contour to tone categories. Keep continuous F0, register/phonation cues and confidence in separate structured metadata when available.
- Use `?` only if explicitly allowed by the corpus schema/convention; otherwise record an unresolved annotation status and a reason in uncertainty notes rather than inserting a question mark into IPA.

## 4. Proposed treatment of key Khmer phenomena

| Phenomenon | Conservative pilot policy | Evidence / decision boundary |
|---|---|---|
| Consonant series / register | Do not encode series as a separate IPA segment. Transcribe the actual onset and vowel quality heard. Record series as an orthographic-analysis feature only when the parser/source evidence supports it. | Series conditions vowel readings; orthographic class labels are not equivalent to modern phonetic voicing [Min85]. Expert must approve exact feature schema and mapping. |
| Inherent vowels and dependent vowel signs | Never assign a vowel from the sign alone. Use the complete orthographic context as a prompt, then verify against audio and approved profile-specific evidence. | Minegishi documents series-conditioned values and coda conditioning; the charts are partial and historically motivated [Min85]. |
| Vowel inventory and quality | Use only the expert-approved symbol inventory. Do not import Chem's full proposed inventory mechanically; resolve its category and transcription inconsistencies first. | Chem's four-speaker acoustic sample and poster/article records do not constitute a complete IPA key [Vat20]. |
| Vowel length | Preserve a long/short contrast only when supported by audio and expert convention; represent long vowels with `ː` if that notation is approved. Do not infer length from spelling alone. | Chem reports duration differences and coda effects but does not define a consistent transcription convention [Vat20]. |
| Diphthongs and offglides | Transcribe a diphthong only when the target is supported as one phonological nucleus by expert analysis; do not convert every formant trajectory into a two-vowel sequence. Keep glide/coda analyses distinct. | Chem notes V1 dominance and unclear short-diphthong trajectories [Vat20]. |
| Codas and checked syllables | Transcribe the audible coda; do not infer a coda from spelling where the source's phonological analysis is unresolved. Keep closure/glottalization distinct from an unwritten segment unless explicitly approved. | Minegishi describes checked-vowel and coda-conditioned cases [Min85]. |
| Onset clusters and transitions | Do not insert a schwa or other vowel for an acoustic transition unless the expert-approved criterion identifies a segmental vowel target. | Kirby's cluster work reports transitions without clear evidence of a distinct gestural target [Kir18]. |
| /r/ and /r/-loss | Do not automatically map written រ to [h]. For this careful-citation profile, annotate [h] only when it is directly present in the recording and the panel confirms that the token belongs to this profile; otherwise retain the audible value or mark unresolved. Keep colloquial /r/-loss as a separate profile/variant, not an unlabelled alternative. | Colloquial PPK /r/-loss is associated with multiple cues and emerging F0 contrasts [Kir14]; this cannot be generalized to every careful citation token. |
| Pitch / F0 | Do not encode F0 as lexical tone in the primary IPA field by default. If measured, preserve a separate F0 contour/measurement and task metadata. | Mam et al. report possible phonologization in controlled PPK wordlist data but do not establish a general tonal inventory or isolated citation-form rule [Mam25]. |
| Phonation / aspiration | Mark only audible, convention-defined broad categories; do not infer breathiness or aspiration from an orthographic series or /r/-loss context. | Kirby documents coupled cues in colloquial /r/-loss; the target careful-citation profile needs direct evidence [Kir14]. |
| Word boundaries | Do not infer words from spaces or orthographic-syllable segmentation alone. Use exact lexical source/context and record boundary uncertainty. | Khmer orthographic syllables, phonological syllables and lexical words are separate units in the project contract. |

## 5. Annotation record and uncertainty protocol

For every pilot item, the curator must supply the exact source locator, rights decision, target profile, elicitation prompt, orthography, gloss/context, audio locator/checksum, speaker pseudonym, recording/task condition, and coverage rationale. The annotators receive identical packets but never each other's work or system predictions.

Each annotator must:
- transcribe independently in the approved single IPA kind;
- distinguish directly audible evidence from lexical/contextual inference;
- identify uncertain segments and the reason (audio quality, lexical identity, series-conditioned analysis, syllable boundary, vowel category, coda, /r/-variant, pitch/phonation, or other);
- avoid forced completion; unresolved segments remain unresolved;
- record confidence without using confidence as a substitute for evidence.

The adjudicator sees both locked annotations only after submission, records the disagreement, cited evidence, decision and rationale, and may preserve the item as unresolved. The curator does not annotate. Do not place identity mappings, contact details or private recordings in public GitHub issues/PRs.

## 6. Required expert decisions before approval

The sheet cannot be approved by repository maintainers alone. A Khmer phonetician/phonologist with demonstrated competence in contemporary Phnom Penh careful speech must decide and sign off:

1. Whether `PHONETIC_BROAD` is the right single corpus kind, or whether the pilot should instead be phonemic.
2. The complete approved IPA segment inventory and symbol table, with exact source/examples for every contrast in scope.
3. How the target careful-citation profile treats consonant series, vowel quality/length, diphthongs, codas and checked syllables.
4. Whether and how to represent stress/prominence, F0, register, phonation, aspiration and /r/-loss; which are separate metadata versus IPA diacritics.
5. What counts as a phonological diphthong versus a vowel-plus-glide or cluster transition.
6. Which tokens are excluded or assigned a separate profile, and how variants/unresolved readings are represented.
7. Whether the 30 lexeme groups provide adequate contrast coverage for a process pilot.

Approval must include reviewer identity under a private project record, affiliation/qualification evidence, date, version, exact changed sections, and explicit acceptance of the limitations. A second qualified reviewer should independently challenge the proposed policy. The project must not mark the sheet approved until that evidence exists.

## 7. Decision and status

- This is a **draft proposal**, not an approved convention.
- No gold annotation may begin under this sheet until expert sign-off, two annotators, a separate adjudicator, a non-annotating curator, private blind intake, item rights and the 30-item packet are all ready.
- No IPA gold rows, source data or model predictions are created by this document.
- `KHM-GOLD-001` remains `BLOCKED`; gold count remains 0; empirical accuracy remains null.

## References

- [Min85] Minegishi, Makoto. 1985. “Modern Khmer Orthography and Its Dialects.” *Gengo Kenkyu* 88: 41–67. DOI: https://doi.org/10.11435/GENGO1939.1985.88_41.
- [Vat20] Chem, Vatho. 2020. “The Standard Khmer Vowel System: An Acoustic Study.” *Insight: Cambodia Journal of Basic and Applied Research* 2(2): 93–121. DOI: https://doi.org/10.61945/cjbar.2020.2.2.3.
- [Mam25] Mam, Sothornin, Pittayawat Pittayaporn & Sireemas Maspong. 2025. “Phonologization of Pitch in Phnom Penh and Standard Khmer for Cluster and Disyllabic Words.” DOI: https://doi.org/10.21437/TAI.2025-29.
- [Kir14] Kirby, James P. 2014. “Incipient tonogenesis in Phnom Penh Khmer: Acoustic and perceptual studies.” *Journal of Phonetics* 45: 69–85. DOI: https://doi.org/10.1016/j.wocn.2014.02.001.
- [Kir18] Kirby, James P. 2018. “Acoustic transitions in Khmer word-initial clusters.” Supplementary materials/audio: https://doi.org/10.7488/DS/2454.
- [Sod18] Sodimana, Keshan Sanjaya et al. 2018. “A Step-by-Step Process for Building TTS Voices Using Open Source Data and Frameworks for Bangla, Javanese, Khmer, Nepali, Sinhala, and Sundanese.” DOI: https://doi.org/10.21437/SLTU.2018-14.
