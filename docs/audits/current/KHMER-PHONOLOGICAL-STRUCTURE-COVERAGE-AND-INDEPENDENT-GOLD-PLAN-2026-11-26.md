# Khmer phonological-structure coverage and independent IPA gold plan

**Audit date:** 2026-11-26  
**Base:** main at efc101626bce56dd26c2d4c97b3fe62558b8998a  
**Purpose:** extend productive Khmer G2P by phonological structure, not isolated word additions; establish an independent, profile-controlled audio/IPA evaluation set.

## Executive finding

The deployed engine is a local deterministic runtime with offline neural-teacher distillation. Its generalization is broader than the earlier onset-only fallback, but its generated CV/CVC candidate inventory is not a complete Khmer phonology. The teacher reproduces source labels; it does not independently establish contemporary Phnom Penh pronunciation.

The source-indexed vowel/register register contains **14 lexical cases**: 12 SOURCE_ATTESTED_NOT_GOLD and 2 CONFLICTING_SOURCE_ANALYSES. They represent only three dependent-vowel signs in exact lexical cases. The generated coverage report expects 16 dependent-vowel signs × 2 consonant series = 32 cells; most remain NOT_ESTABLISHED. This is evidence coverage, not a score of the runtime's generated candidate table.

The independent project IPA-gold TSV currently contains only its header; annotation, record and split JSONL files are empty. Independent adjudicated gold = **0** and accuracy remains **NOT_ASSESSED**.

## Keep the layers separate

1. Unicode orthographic parsing identifies bases, shifters, robat, coeng/subscripts, vowels, signs and join controls. It does not decide phonetic syllables or word boundaries.
2. Phonological analysis infers a profile-conditioned onset, nucleus, coda, syllable type and phonological syllable sequence.
3. Phonetic realization preserves aspiration/VOT, vowel quality and quantity, diphthong trajectories, coda-conditioned shortening, glottal realization, and pitch/voice-quality cues where supported.
4. Typed IPA is the adapter boundary. Ukrainian output is generated only from that IPA result.
5. Orthographic romanization remains a separate non-pronunciation lane.

## Productive structure coverage matrix

This is a work specification, not a claim that every combination is legal or evidenced. Orthographic validity, phonological legality and surface pronunciation are separate fields. Do not generate a Cartesian product and treat it as valid Khmer syllables.

| Dimension | Required classes / interactions | Current state | Engine acceptance |
|---|---|---|---|
| Onset base and series | all 33 basic consonants; first/second series; shifter-adjusted series | inventory/series mostly structurally established; phonetic values have source/profile limits | resolve series from full orthographic unit; preserve onset identity, aspiration and implosion |
| Initial clusters | simple onset; coeng clusters; obstruent+/r/ and other licensed sequences; minor-syllable types | partial descriptive evidence; bounded acoustic cluster data exist | parse compositionally; no blanket /r/ deletion; distinguish major/minor syllables |
| Robat | initial and post-subscript positions; cluster and vowel interactions | orthographic structures parsed; phonological realization incomplete | typed structure and source-located rules; abstain on unsupported combinations |
| Dependent vowels | all 16 signs, multi-sign sequences, first/second series and shifter context | 32 base series cells expected; few exact source-located lexical examples | generate only from attested/context-supported rule families |
| Independent vowels | all independent vowel signs and glottal onset behaviour | orthographic inventory known; phonetic coverage partial | keep independent-vowel onset and nucleus distinct |
| Nucleus | monophthongs, diphthongs, short/long, reduced/minor-syllable nuclei | acoustic inventories exist, but no complete lexical cross-table | preserve length and diphthong identity; condition on series, coda, stress and syllable type |
| Coda | oral stops, nasals, lateral, glottal/h-related signs and sign-mediated codas | descriptive inventory exists; interactions incomplete | infer coda separately from trailing orthographic components; model nucleus+coda jointly |
| Nucleus × coda | vowel quality/length before /p,t,k,m,n,ɲ,ŋ,l,h,ʔ/ | partial acoustic evidence; no exhaustive cross-product | no universal vowel-sign lookup; add only supported context-conditioned rules |
| Phonetic syllabification | orthographic chaining vs one/two phonetic syllables; minor syllables | Unicode/phonological descriptions establish non-equivalence | explicit phonological boundaries; do not equate each orthographic unit with a phonetic syllable |
| Register and profile | careful Standard/PPH; colloquial Phnom Penh; speaker/style variation | profile-specific studies exist; coverage uneven | explicit profile input; retain alternatives; no universal colloquial rewrite |
| Prosody | stress, F0, possible pitch phonologization, voice quality | recent bounded PPK evidence; no broad lexical gold | separate phonemic and phonetic outputs; profile-conditioned prosody only |
| Ukrainian target | IPA phones, glides, long vowels, sequences | project target policy; not Khmer evidence | IPA-only mapping; /w/ → в in default Ukrainian mode; Russian compatibility remains separate |

### Anti-shortcut rules

- Do not add isolated words as a substitute for phonological coverage.
- Do not turn Google phonemic labels, teacher predictions, Wiktionary, IPA-Dict or external-engine outputs into adjudicated gold.
- 100% non-empty display coverage is not 100% IPA coverage.
- Orthographic syllable counts are not phonetic syllable counts.
- Keep careful Standard Khmer and colloquial Phnom Penh processes separate.
- Preserve length before IPA longest-match parsing: /aw/ and /aːw/ are distinct; current target mapping keeps /w/ → в, /aw/ → ау, /aːw/ → ав.

## Independent audio and benchmark source triage

### A. Edinburgh DataShare — priority for an independent cluster pilot

James Kirby (2018), “Acoustic transitions in Khmer word-initial clusters: audio recordings, 2013.” DOI: https://doi.org/10.7488/ds/2454

- Dataset record: 24-bit/44.1 kHz audio from 10 Phnom Penh Khmer speakers (3 female), 79 lexical items, three repetitions at two self-selected speech rates; recorded in Phnom Penh in January 2013.
- Segmented Praat TextGrids are included.
- The end-user licence was inspected and is **CC BY 4.0**; attribution and indication of changes are required.
- High-value independent acoustic resource for onset-cluster and intrusive-transition coverage. It is not a complete Khmer pronunciation corpus and does not itself provide adjudicated narrow IPA labels.
- Next: inspect ZIP/TextGrids and item/speaker/rate coverage; annotate broad phonemic and narrow phonetic IPA independently with at least two annotators and adjudication.

### B. OpenSLR SLR42 — broader audio-backed pilot, subject to metadata audit

“High quality TTS data for Khmer,” OpenSLR SLR42.

- Resource page states CC BY-SA 4.0, WAV audio plus line_index.tsv transcriptions and speaker IDs in filenames; manually quality checked; collected by Google.
- The listed Khmer download is a male-speaker archive. Do not infer speaker count, dialect, task or balanced phonological coverage from the summary; inspect archive metadata.
- It contains orthographic transcripts, not IPA. Use for audio-based annotation only after speaker, dialect, style and rights provenance are verified.
- Review ShareAlike compatibility before redistributing derived annotations.

### C. MekongPhon — external reference, not independent gold for this engine

Shurtz, Richardson & Richardson (2026), “MekongPhon: A Large-Scale Parallel IPA Corpus for Lao and Khmer,” LREC 2026. DOI: https://doi.org/10.63317/4bb9rvdshu4z

- Paper reports 1.3 million Khmer orthography–IPA pairs, aligned and verified, and public release of data, code and models.
- Existing project model/benchmark work already uses MekongPhon-related material. Held-out splits are useful source-concordance diagnostics, but must not be called independent project gold or independent of all model exposure without full lineage review.
- Audit exact revision, licence, source dictionaries, dialect/style metadata and train/evaluation lineage. Keep results as SOURCE_CONCORDANCE, not ADJUDICATED_GOLD.

### D. IPA-Dict Khmer — cross-source diagnostic only

The pinned Khmer IPA-Dict file is derived from the aakanee.com Khmer-English Dictionary and carries CC BY-NC-SA 4.0. It is useful as a cross-source diagnostic after overlap controls, but is neither audio-adjudicated nor gold for the selected careful Phnom Penh profile. Commercial redistribution remains blocked by its non-commercial licence.

### E. General ASR corpora — audio/transcript only

The Khmer ASR Cultural Dataset is advertised as 37.62 hours of speech-text pairs from 12 speakers. Potentially useful for additional annotation, but dialect, style, item coverage and redistribution rights must be verified from authoritative dataset metadata. ASR transcript alignment does not supply IPA.

## Gold collection protocol

1. Freeze the target profile before annotation. Define careful Phnom Penh/Standard citation as the primary profile; separate colloquial Phnom Penh and other varieties. Record speaker, region, task, rate, date and source where supplied.
2. Build a structure-stratified sample: onset/cluster family, consonant series, vowel sign/sequence, coda, open/closed syllable, major/minor type and relevant interactions. Mark unsupported combinations instead of fabricating examples.
3. Preserve audio and orthography provenance: stable audio URI/hash, time span, orthographic text, segmentation, source licence, attribution and annotation version.
4. Two trained annotators produce phonemic IPA and narrow phonetic IPA separately, with syllable boundaries, length, stress, uncertainty and audible variants. Adjudicate disagreements against audio; preserve raw annotations and adjudicated records.
5. Split before tuning. Hold out lexical items and, where possible, speakers. Keep all repetitions and rates of one lexical item in one split. Record dataset and annotation hashes.
6. Report exact IPA match, PER, CER, syllable-boundary accuracy, onset/nucleus/coda accuracy, length accuracy, coverage/abstention and Ukrainian adaptation separately, by profile and structural cell.
7. A new deterministic rule requires primary source locators or adjudicated audio evidence, positive/negative tests, Python/JavaScript parity and a held-out structural cell. Teacher agreement alone cannot promote a rule.

## Task ledger

| Task | Status | Acceptance evidence |
|---|---|---|
| Unicode orthographic parser and Python/JS parity | DONE_VERIFIED (structural layer only) | Unicode 18 grammar tests; does not establish phonetic syllabification |
| Google teacher and deterministic CV/CVC distillation | DONE_VERIFIED (source-label reproduction only) | Exact-head CI artifacts; metrics remain source-label diagnostics |
| Full vowel × series × coda × syllable-type evidence matrix | PARTIAL | Source-located cases for claimed cells; unresolved cells remain unresolved |
| Productive onset/coeng/robat phonology | PARTIAL | Profile-specific compositional rules, positive/negative tests and independent audio evidence |
| Independent cluster audio pilot | TODO | Edinburgh DataShare files inspected; two independent IPA annotations and adjudication; rights provenance retained |
| Broad independent IPA gold | BLOCKED / TODO | Multi-structure, multi-speaker, profile-controlled, split-independent adjudicated records; current count 0 |
| ASR corpus expansion | BLOCKED pending metadata/licence review | Dataset card, manifest, speaker/dialect metadata and licence verified |
| /w/ Ukrainian target mapping | DONE_VERIFIED | Main policy default /w/ → в; Python regression tests; Russian compatibility mapping separate |
| Empirical pronunciation accuracy and tier ordering | NOT_ASSESSED | Independent held-out adjudicated gold with structure-stratified metrics |

## Immediate next implementation batch

1. Inspect Edinburgh DataShare ZIP and TextGrid structure; derive a manifest of item IDs, speakers, repetitions, rates and cluster families without redistributing audio.
2. Build an annotation template and cluster-balanced pilot; do not auto-generate IPA labels from an existing engine.
3. Inspect SLR42 archive metadata and speaker IDs; retain only rights-cleared manifest statistics until dialect and scope are established.
4. Extend the machine-readable evidence register by structure/environment, not isolated word-to-IPA overrides.
5. Implement productive phonological rules only after annotation and source evidence support them.

**Conclusion:** the deterministic browser engine is deployed and its code path is tested, but the general Khmer phonological model remains a partial research prototype. The next credible advance is a structure-stratified, independently annotated audio gold pilot—not a larger dictionary.
