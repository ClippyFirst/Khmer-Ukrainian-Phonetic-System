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

The paper §3.1.1–3.1.2 reports:
- a 41-item wordlist, constructed to include minimal triplets but not perfectly balanced for segmental content or syllable shape;
- 20 native Phnom Penh Khmer participants (13 female), aged 21–60;
- a production segment comprising a self-paced reading task followed by a repetition task;
- target items in the frame sentence [khñom tha: tiət] ‘I say again’, read at a normal speaking rate; each of the 41 targets appeared three times in randomized order.

The study compares colloquial and reading /CrV/ forms, including VOT/aspiration, F0, F1/F2, voice quality and realization of /r/. It reports substantial variation in /r/ realization, and shows that colloquial forms differ from reading forms on multiple acoustic dimensions. Its perceptual experiments examine F0 and F1/F2 cues; this is not a general demonstration that Phnom Penh Khmer has unrestricted lexical tone.

## Material discrepancy that must remain visible

The paper reports **20 participants**, whereas the associated DataShare audio-recording description reports **16 speakers**. The archive's actual speaker-directory count has not been inspected, so these counts cannot be reconciled from metadata alone. Do not report “20 speakers in the archive,” infer that all 20 participants have WAV files, or assume the 16 archive speakers are a random subset. Resolve this from the archive README/file tree or a source-author clarification before using speaker-level counts or claiming coverage.

## Project-profile fit

**Useful for:** direct acoustic study of Phnom Penh /r/-loss and its possible correlates (F0, aspiration/VOT, voice quality, vowel quality/diphthongization); checking whether /r/ can be realized variably; reading-versus-colloquial contrast evidence; historical comparison with the newer 2013 cluster dataset. The supplementary CSVs may expose aggregate or anonymised measurements that help inspect the original study's evidence, once their schemas and provenance are checked.

**Not sufficient for:** a full source-to-IPA transcription convention; a general tone rule; an exhaustive series × vowel × length/diphthong × coda × stress matrix; an independent 30-item gold corpus; standalone isolated citation-form speech. The production task is framed in a carrier sentence and includes both reading and repetition. The dataset dates from 2011 and the wordlist was deliberately constrained rather than fully balanced.

Do not infer that the paper's IPA-like/phonetic examples are the project's approved transcription convention. Do not treat the supplementary perception CSVs or KlattGrid stimuli as natural speech recordings. Do not auto-convert every written រ to [h], or encode a general tone mark based on /r/ spelling.

## Required next steps

1. Download both DataShare items in a network-enabled environment and verify their provider-listed MD5s.
2. Inspect archive directories and readmes; reconcile the 16-speaker audio description with the paper's 20 participants. Record only opaque subject IDs.
3. Inspect the 41-item wordlist in Appendix A and map exact Khmer orthography, meanings, alternate spellings and item locators to actual WAV/TextGrid tokens. The paper notes a Khmer assistant confirmed lexical status, but the list was not perfectly balanced.
4. Inspect the supplementary bundle's README, CSV schemas, code, and relation between production and perception files; distinguish natural production data, derived measurements, synthetic stimuli and perceptual responses.
5. Obtain a specialist decision on whether the reading condition is sufficiently close to the project's careful-citation target profile; keep colloquial/repetition conditions distinct.
6. Use this source only for evidence-backed /r/-loss and prosodic variant discussion until the target IPA convention is approved and independent annotation is arranged.

## Status

- DataShare item identity, descriptive metadata, stated CC BY 4.0 rights, listed file sizes/checksums: **DONE_VERIFIED** from indexed primary item metadata.
- Study methods and 41-item / 20-participant description: **DONE_VERIFIED** from Kirby (2014) §3.1.1–3.1.2.
- 16-vs-20 archive/participant reconciliation: **BLOCKED** pending archive inspection or author clarification.
- Local archive checksum and item manifest: **TODO** (no files downloaded).
- Target-profile fit and use in the 30-item pilot: **BLOCKED** pending specialist ruling and coverage analysis.
- IPA labels/gold contribution: **none**. No audio or supplementary data imported; gold remains 0 and empirical accuracy remains null.
