# Kirby Phnom Penh incipient-tonogenesis datasets — source audit

**Audit date:** 2026-11-17  
**Disposition:** supporting primary phonetic evidence; not IPA gold and not an approved 30-item pilot source.

## Primary datasets and rights

### Audio recordings (2011)

- Edinburgh DataShare full metadata: https://datashare.ed.ac.uk/items/fe218489-ad49-4986-b175-721cb9959500/full
- DOI: https://doi.org/10.7488/ds/321
- Citation: Kirby, James. (2015). *Incipient tonogenesis in Phnom Penh Khmer: audio recordings, 2011* [sound]. University of Edinburgh.
- Metadata describes 24-bit/44.1 kHz audio of **16 Phnom Penh Khmer speakers**, recorded in Phnom Penh in July 2011, with WAV, segmented Praat TextGrids, and Praat Pitch, Formant and PointProcess files.
- Archive: `items.zip`, 461.93 MB; provider-listed MD5 `8688e68e76e8269b8bbf5d19020a230b`.
- DataShare full metadata explicitly states **Creative Commons Attribution 4.0 International Public License**.

### Supplementary materials (2011)

- Edinburgh DataShare full metadata: https://datashare.ed.ac.uk/items/9a9fa51d-ce4f-4685-9e39-af3fd0a436d3/full
- DOI: https://doi.org/10.7488/ds/319
- Citation: Kirby, James. (2015). *Incipient tonogenesis in Phnom Penh Khmer: supplementary materials, 2011* [dataset]. University of Edinburgh.
- Metadata describes KlattGrid files used to generate perceptual stimuli, anonymised perception and production CSV data, plots and R analysis code. It states there are 10 files in total and separately identifies the audio/TextGrid archive above.
- Listed file examples and provider MD5s:
  - `kuu.zip`, 21.39 KB — `7fd0cfa9c7c595009781c15e5a109bcd`
  - `kaa.zip`, 35.86 KB — `e4e3d795ffaee20ab6f97bad0d3b4fc4`
  - `kuu.csv`, 207.89 KB — `1dde9f31baeea0856dcc8144a14a6b1d`
  - `kaa.csv`, 274.57 KB — `2fcbd576ddb055ad74e94e4a290b4703`
  - `kruuRespBySubject.pdf`, 517.92 KB — `ba794f0c1894ed58d683c5eed6d6d419`
- DataShare full metadata explicitly states **Creative Commons Attribution 4.0 International Public License**.

## Associated peer-reviewed study and methods

Kirby, James P. (2014). *Incipient tonogenesis in Phnom Penh Khmer: Acoustic and perceptual studies*. **Journal of Phonetics 43**, 69–85. DOI: https://doi.org/10.1016/j.wocn.2014.02.001. Public preprint: https://www.pure.ed.ac.uk/ws/files/14181671/kirby2014acoustic_preprint.pdf

The paper §3.1.1–3.2 and Appendix A (printed p. 47) report:
- a 41-item wordlist, constructed to include minimal triplets but not perfectly balanced for segmental content or syllable shape; a Khmer assistant confirmed lexical status, meanings and spellings, while some items admit alternate spellings;
- 20 native Phnom Penh Khmer participants (13 female), aged 21–60;
- a self-paced **careful/read** task followed by a separate colloquial repetition task; reading items were presented in the carrier sentence [khñom tha: tiət] ‘I say again’, at a normal speaking rate, three randomized repetitions each;
- a separate set of 15 targets for colloquial variants, elicited by an oral Standard Khmer prompt and a participant repetition, three randomized repetitions each;
- four participants who consistently retained /r/ in both conditions were excluded from subsequent analysis, leaving 16 analyzed participants;
- 2,664 tokens isolated and segmented; the main analysis focuses on 2,099 tokens with obstruent onsets. The annotation scheme distinguished onset, excrescent vocalism, trill/tap (with voiced/voiceless trill/tap, voiced/voiceless fricative or approximant sublabels), and rime (nucleus/coda where applicable).

This provides a plausible explanation for the DataShare description of 16 speakers: the paper's 20 recruited participants minus four excluded from subsequent analysis equals 16. However, the archive directory list has not been inspected, so it remains unverified that the 16 archived speaker folders are exactly the 16 analyzed participants. Appendix A supplies the 41 items in the paper's romanized phonological notation and glosses, not exact Khmer-script forms. The study compares colloquial and careful/read /CrV/ forms, including VOT/aspiration, F0, F1/F2, voice quality and realization of /r/. Its perceptual experiments examine F0 and F1/F2 cues; this is not a general demonstration that Phnom Penh Khmer has unrestricted lexical tone.

## Participant-count reconciliation — plausible, not yet archive-verified

The DataShare audio description reports **16 speakers**. The paper reports **20 recruited participants**, then states that four participants consistently produced forms containing /r/ in both conditions and were not analyzed further (§3.2, printed p. 10). This makes **16 analyzed participants** and is a plausible explanation for the archive's 16-speaker description. Do not silently rewrite the archive metadata as “20 speakers,” and do not claim that the archive folders are confirmed to be exactly the analyzed subset until the ZIP directory list/README is inspected. Record the distinction as 20 recruited / 16 analyzed / 16 described in the DataShare audio record, with archive membership pending verification.

## Project-profile fit

**Useful for:** direct acoustic study of Phnom Penh /r/-loss and its possible correlates (F0, aspiration/VOT, voice quality, vowel quality/diphthongization); checking whether /r/ can be realized variably; reading-versus-colloquial contrast evidence; historical comparison with the newer 2013 cluster dataset. The supplementary CSVs may expose aggregate or anonymised measurements that help inspect the original study's evidence, once their schemas and provenance are checked.

**Not sufficient for:** a full source-to-IPA transcription convention; a general tone rule; an exhaustive series × vowel × length/diphthong × coda × stress matrix; an independent 30-item gold corpus; standalone isolated citation-form speech. The production task is framed in a carrier sentence and includes both reading and repetition. The dataset dates from 2011 and the wordlist was deliberately constrained rather than fully balanced.

Do not infer that the paper's IPA-like/phonetic examples are the project's approved transcription convention. Do not treat the supplementary perception CSVs or KlattGrid stimuli as natural speech recordings. Do not auto-convert every written រ to [h], or encode a general tone mark based on /r/ spelling.

## Required next steps

1. Download both DataShare items in a network-enabled environment and verify their provider-listed MD5s.
2. Inspect archive directories and readmes; verify whether the 16 folders correspond to the 16 analyzed participants after four of the 20 recruited participants were excluded for retaining /r/ in both conditions. Record only opaque subject IDs.
3. Transcribe Appendix A's 41 romanized item/gloss pairs into a candidate crosswalk, then verify exact Khmer orthography and alternate spellings against the archive filenames or an authoritative lexical source. Record item/page/token locators. The paper notes a Khmer assistant confirmed lexical status, but the list was not perfectly balanced.
4. Inspect the supplementary bundle's README, CSV schemas, code, and relation between production and perception files; distinguish natural production data, derived measurements, synthetic stimuli and perceptual responses.
5. Obtain a specialist decision on whether the reading condition is sufficiently close to the project's careful-citation target profile; keep colloquial/repetition conditions distinct.
6. Use this source only for evidence-backed /r/-loss and prosodic variant discussion until the target IPA convention is approved and independent annotation is arranged.

## Status

- DataShare item identity, descriptive metadata, stated CC BY 4.0 rights, listed file sizes/checksums: **DONE_VERIFIED** from indexed primary item metadata.
- Study methods and 41-item / 20-participant description: **DONE_VERIFIED** from Kirby (2014) §3.1.1–3.1.2.
- Participant-count explanation: **PARTIAL** — paper accounts for 20 recruited participants, 4 excluded from analysis, and 16 analyzed; this plausibly matches DataShare's 16 speakers. Exact archive folder membership remains **TODO** pending ZIP inspection.
- Local archive checksum and item manifest: **TODO** (no files downloaded).
- Target-profile fit and use in the 30-item pilot: **BLOCKED** pending specialist ruling and coverage analysis.
- IPA labels/gold contribution: **none**. No audio or supplementary data imported; gold remains 0 and empirical accuracy remains null.


## Full-text evidence addendum — 2026-11-17

Direct review of the Edinburgh-hosted peer-reviewed preprint clarified the participant count and production protocol. See §3.1.1–3.2 (printed pp. 8–11) and Appendix A (printed p. 47): 20 recruited participants; four retained /r/ in both conditions and were excluded from further analysis; 16 remained in the analyzed sample. The paper reports 2,664 segmented tokens, with the main obstruent-onset analysis using 2,099 tokens. Appendix A lists 41 romanized items with glosses; it does not provide a Khmer-script orthographic inventory. Reading tokens were careful/self-paced, embedded in [khñom tha: tiət] and spoken at a normal rate; a separate 15-item colloquial repetition task used oral Standard Khmer prompts. The DataShare 16-speaker description is therefore plausibly aligned with the analyzed sample, but archive membership is not confirmed until the ZIP tree is inspected.
