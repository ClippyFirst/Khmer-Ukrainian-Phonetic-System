# Khmer contextual vowels and lexical segmentation: research continuation — 2026-11-21

**Status:** literature synthesis and evidence gaps updated; full matrix and runtime lexical segmentation remain PARTIAL/BLOCKED. No new IPA gold or runtime rule is introduced.

## Contextual vowels: what the sources support

The current evidence base must remain stratified by source, dialect/profile, task and evidence type:

1. **Chem (2020), Phnom Penh acoustic study.** This is a direct Phnom Penh vowel-acoustics source, but the study uses a small selected speaker sample (four speakers in the current repository audit) and formal frame-reading. Its reported inventory and its acoustic sample coverage are not interchangeable: the article itself notes gaps/substitutions in the sample. Treat its transcriptions as source-reported evidence; do not turn the full listed inventory into a complete phonemic inventory or gold.
2. **Minegishi (1985).** Useful for series-conditioned vowel readings and coda effects, but formal/school and colloquial outcomes must be kept distinct. A source mapping is not automatically a modern Phnom Penh careful-citation phonetic realization.
3. **Kirby (2014/2015/2018).** The evidence concerns incipient tonogenesis, /r/-loss, laryngeal cues, cluster transitions and onset-F0 perturbation. These results do not justify a general grapheme-to-tone mapping. Transition vowels in clusters may be predictable phonetic states without a distinct vowel target; do not automatically parse them as phonological vowels.
4. **Mam et al. (2025).** The five-speaker, 50-word study reports possible F0 phonologization in a bounded cluster/disyllable task. This is a profile/task-specific hypothesis, not a universal tone inventory or citation-form rule.
5. **Woźnica (2013).** The broad 80-speaker study is geographically uneven and only two participants are listed as Phnom Penh in the thesis audit. It challenges overconfident regional generalizations but does not establish a modern, balanced Phnom Penh citation-form target by itself.
6. **Henderson (1952).** A carefully documented speaker description with examples checked against a second Cambodian speaker, but the speaker was born in Kompong Chhnang, not Phnom Penh. Useful comparative evidence, not direct Phnom Penh gold.

## Minimum fields for each contextual-vowel observation

Do not extend a matrix with a naked grapheme-to-IPA pair. Each row should include:

- exact orthographic sequence and Unicode code points;
- lexeme and lexical/morpheme segmentation with evidence;
- consonant series/register-shifter and full onset stack;
- dependent/independent vowel signs and inherent-vowel status;
- phonological syllable type, coda class and exact coda evidence;
- source transcription exactly as printed, with transcription system and page/table locator;
- profile, speaker count, region, age/sex where reported, register and elicitation task;
- phonetic/acoustic measures and audio locator when available;
- stress/prominence, position in word/phrase, connected-speech context;
- evidence class (SOURCE_ATTESTED, ACOUSTICALLY_MEASURED, CONFLICTING, NOT_ESTABLISHED);
- source license, recording/annotation rights and redistribution status;
- independent expert review and adjudication state.

Missing values stay NOT_ESTABLISHED. A source's lack of a length mark is not proof of shortness; orthographic coda marks are not necessarily phonological coda identity; vowel transitions are not automatically separate segments.

## Lexical segmentation: keep three layers separate

- **Unicode/orthographic units:** grapheme clusters and orthographic syllable parsing.
- **Phonological syllables:** structure inferred from a target profile and phonological evidence.
- **Lexical/morphemic boundaries:** word segmentation under a declared annotation convention.

The existing parser handles conservative orthographic structure; the existing word-boundary evidence container abstains unless a unique candidate is adjudicated. Keep that boundary. ALT/NOVA's 20,000-sentence manual corpus uses a morpheme-oriented tokenization convention, including separate compound components and shallow bracketing; it is not a universal surface-word standard. khPOS is another manual resource but its source mixture includes student/election/voter-list material, so privacy/provenance review is mandatory. Published segmentation scores and dictionary matching results are not portable accuracy claims for Phnom Penh or this repository.

## Research actions and decisions

- Continue to use data/khmer/vowel-context-register.json as a source-indexed observation register, not a gold table.
- Expand only with exact source-located examples after inspecting the original page/table/audio and recording profile/task fields.
- Add no contextual IPA value from a G2P engine, romanizer or inferred grapheme mapping.
- Do not add a runtime lexical segmenter until tokenization convention, domain, source rights, privacy and human boundary pilot are approved.
- For any future segmenter, preserve source text and expose boundary alternatives/abstention separately from the IPA-first conversion pipeline.

## Candidate source priorities

| Priority | Source | Why useful | Immediate gate |
|---|---|---|---|
| 1 | Chem (2020) | Direct Phnom Penh vowel acoustics | Inspect exact full-text tables and sample limitations; no audio redistribution assumed |
| 1 | Kirby cluster audio/TextGrids | Direct Phnom Penh cluster transitions and speaker variation | Verify exact item list, task, license and consent |
| 1 | Mam et al. (2025) | Recent bounded F0/cluster/disyllable evidence | Inspect full paper/materials; do not generalize beyond five speakers/50 words |
| 2 | Minegishi (1985) | Series/coda contextual analysis | Separate formal/school and colloquial readings |
| 2 | ALT/NOVA | Manual morpheme-oriented segmentation guideline and corpus | NC-SA terms; translated-news domain; not IPA gold |
| 2 | khPOS | Manual word segmentation corpus | Privacy/source review of voter/student-list origins before any use |
| 3 | Woźnica (2013), Henderson (1952) | Broad comparative dialect and older description | Do not relabel as contemporary Phnom Penh careful-citation data |

## Acceptance boundary

The existing contextual evidence schema/integrity checks are engineering-complete. The broad contextual vowel matrix is still PARTIAL: source rows do not consistently cover profile × series × nucleus × coda × syllable type × length × stress/harmony. Lexical segmentation remains BLOCKED pending an approved unit/convention, rights/privacy clearance and independently adjudicated boundary pilot. No new gold or accuracy claim is made.


## Full-text verification of two key Phnom Penh studies — 2026-11-21

### Chem (2020): exact sample and acoustic limits

Full-text review confirms that the final acoustic sample is **four native Phnom Penh speakers (two men, two women), ages 20–50**. A preceding conversational observation stage involved 21 speakers and 168 items; that is not the final acoustic sample. The final task included 61 lexical items read formally three times, with a prompt equivalent to “this word is read as …”. The principal vowel measures are duration, F1 and F2. The study reports 21 monophthong and 13 diphthong categories, but explicitly notes missing/substituted vowel samples and difficulty with unfamiliar items. Closed syllables are usually shorter than open syllables, and coda closure can make the nucleus boundary difficult to locate. The poster discusses register-related vowel differences but does not clearly establish a controlled statistical analysis of consonant series as an experimental factor. These limitations prevent treating its full inventory as a complete modern phonemic/phonetic inventory or gold table. DOI: https://doi.org/10.61945/cjbar.2020.2.2.3.

### Mam, Pittayaporn & Maspong (2025): bounded F0 evidence

Full-text review confirms **five native Greater Phnom Penh speakers (two men, three women), ages 20–25**, familiar with both PPK and Standard Khmer. The 50-word task crossed four onset types (r>h, voiced, voiceless stop, nasal) with cluster and disyllable structures. Each target was shown in Khmer orthography in a carrier sentence; PPK was elicited before Standard Khmer, with three repetitions per target. The analysis focuses on F0 trajectories of stressed rimes, with automated segmentation manually corrected, CREPE extraction and functional PCA. The paper reports higher F0 for cluster than disyllabic words in both varieties and larger onset-related separation in PPK. It explicitly treats the interpretation as possible phonologization, notes that the r>h disyllable stressed syllables had a single /r/ onset, and calls for more items to test Cr clusters. It does not include a perception test establishing lexical tone. DOI: https://doi.org/10.21437/TAI.2025-29.

**Consequence:** these studies justify keeping coda, syllable structure, elicitation, onset type and profile as separate evidence dimensions. They do not justify generalizing a pitch rule or filling missing contextual matrix cells. No new IPA value or runtime rule is added.

## Additional lexical-source search — 2026-11-21

An Undermind follow-up search for additional Modern Khmer lexical entries with directly paired orthography and standard IPA found no further candidates that met the full item-level gate (exact entry/revision locator, transcription convention, profile caveat, rights evidence, and adapter coverage). MotàMot, MekongPhon and open-source TTS resources remain leads requiring direct full-text/source-entry and rights inspection; they were not used to infer IPA or create fixtures. This is a negative result from the available search records/metadata, not proof that no further qualifying source exists.

The only additions in PR #501 are the two directly checked Wiktionary entries `ជាខ្មែរ` (permanent revision `oldid=68806374`) and `ល្ងាច` (permanent revision `oldid=68625783`). No additional candidates were promoted, and no independent gold or accuracy claim was created.
