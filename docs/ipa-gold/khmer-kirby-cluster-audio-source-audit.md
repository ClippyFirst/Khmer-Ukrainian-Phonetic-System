# Kirby Phnom Penh cluster-audio source audit

**Audit date:** 2026-11-17  
**Source ID:** `kirby2018-cluster-audio`  
**Disposition:** `SUPPORTING_AUDIO_SOURCE_CANDIDATE` — source and licence metadata verified; item-level pilot selection remains pending.

## Primary source and rights

- DataShare record: [Acoustic transitions in Khmer word-initial clusters: audio recordings](https://datashare.ed.ac.uk/items/0d735b30-f6ef-4e14-b6f0-a6b5a136e240).
- DOI: [10.7488/ds/2454](https://doi.org/10.7488/ds/2454).
- Related study: [Kirby (2014), *Acoustic transitions in Khmer word-initial clusters*](https://lel.ed.ac.uk/~jkirby/docs/kirby2014transitions-preprint.pdf), *Proceedings of the 10th International Seminar on Speech Production*, pp. 230–233.
- DataShare metadata explicitly states **Creative Commons Attribution 4.0 International (CC BY 4.0)**. The original archive is `ISSP2014WavGrid.zip`, 477.8 MB, MD5 `a8efcd0cda1cc44fa400fd118d59c396`. A separate `license.txt` is listed in the repository's license bundle.
- Publisher/creator metadata: University of Edinburgh; James Kirby. Recording location: Phnom Penh, Cambodia. Recording date: January 2013.

The dataset description specifies 24-bit/44.1 kHz audio from **10 native Phnom Penh Khmer speakers (3 female)**, producing **79 lexical items**, three repetitions at two self-selected speech rates. Each speaker directory contains WAV files and segmented Praat TextGrids. The filename structure is `subject-rate-Khmer-orthography-repetition`; the DataShare metadata gives `s1-fast-កណ្ដាល-1` as an example.

## What the related paper establishes

The paper's Methods §2.1 (PDF pp. 1–2) says:
- the first block was read **slowly and carefully** and the second as rapidly as possible;
- each item was embedded in the frame sentence /kñom tha: tiət/ ‘I say again’;
- 61 of the 79 recorded items were analysed as words with 35 onset-cluster types, with rimes of shape C1C2V(V)(C);
- the study analyses the occurrence and acoustic properties of transitional vocoids, not a complete segmental IPA inventory.

The paper names several example lexical items and their source transcriptions/glosses, with locators:
- PDF p. 1, Introduction: /mte:h/ ‘pepper’, /pd@j/ ‘husband’, /ckae/ ‘dog’;
- PDF p. 2, §3.3: /t@k/ ‘granary’, /p@n/ ‘clever’;
- PDF p. 2, Figure 2 discussion: /tka@N/ ‘prosperous’;
- PDF p. 2, Figure 1 caption: /lp1v/ ‘pumpkin’;
- PDF p. 3, Figure 3 caption: /kNaok/ ‘peacock’.

These romanized forms are reproduced only as the paper's own analytical notation, **not converted to IPA**. The PDF text extraction corrupts some Khmer-script glyphs; do not reconstruct those orthographic spellings from the corrupted extraction. The full audio archive's filenames encode the Khmer orthography and must be inspected directly before a source-exact item manifest is made.

## Fit to the project profile

**Why this is a strong candidate:** it is directly tied to Phnom Penh speakers, provides original audio plus time-aligned/segmented TextGrids, gives exact recording conditions and speaker count, and includes a slow-careful reading block. It can support direct listening/acoustic inspection rather than relying on dictionary or model output.

**Why it is not yet accepted for the 30-group pilot:**
1. The task is a carrier-sentence reading experiment, not standalone citation-form elicitation. “Slowly and carefully” is relevant but does not itself prove equivalence to `khmer-pph-careful-citation-v1`.
2. The study is focused on onset clusters; it does not establish complete coverage of consonant series × vowel × length/diphthong × coda × prominence.
3. The paper analyses 61 of 79 items; the full 79-item list has not yet been enumerated or manually checked from the archive.
4. TextGrids provide segmentation/measurement, not independent IPA labels or two-person adjudication.
5. The recording sample dates from 2013. It is direct Phnom Penh evidence, but contemporary-profile acceptance remains a specialist decision.
6. No audio archive was downloaded, unpacked, mirrored, or imported during this audit. No individual speaker is identified.

## Required next steps

1. Obtain/inspect the CC BY 4.0 archive and verify its downloaded checksum against the DataShare MD5.
2. Enumerate all Khmer orthographic filenames and associate each item with the corresponding speaker, rate, repetition, WAV and TextGrid locators. Preserve opaque speaker IDs only.
3. Map the paper's 35 cluster types to the actual archive items; keep the remaining recorded items classified separately until their role is known.
4. Have the target-profile expert decide whether the slow-careful carrier-sentence block is admissible for this pilot or only a supplementary acoustic comparator.
5. Build a candidate coverage table against the project's expert-approved contrasts. Do not select a 30-item set until the IPA convention, profile fit, rights and contrast coverage are approved.
6. Keep both rate conditions separate. Never combine fast and slow tokens as if they were equivalent citation forms.
7. If used, cite Kirby (2014) and the DataShare dataset, preserve CC BY 4.0 attribution, and record exact item/time locators. Do not label the TextGrid tiers as IPA gold unless their actual content is independently inspected and the convention approved.

## Status

- Source existence, descriptive metadata, recording profile, file organization and CC BY 4.0 metadata: **DONE_VERIFIED** from the primary DataShare record and paper.
- Complete item manifest and archive checksum verification: **TODO** (archive not downloaded).
- Fit to the exact careful-citation profile: **BLOCKED** pending specialist ruling.
- Pilot selection and IPA annotation: **BLOCKED** by convention approval, independent annotators/adjudicator, curator, blind intake and contrast-coverage review.
- Project gold contribution: **none**. Gold remains 0; empirical accuracy remains null.

## Primary locators

- DataShare full metadata: https://datashare.ed.ac.uk/items/0d735b30-f6ef-4e14-b6f0-a6b5a136e240/full
- Related study PDF, Methods §2.1: https://lel.ed.ac.uk/~jkirby/docs/kirby2014transitions-preprint.pdf
- CC BY 4.0: https://creativecommons.org/licenses/by/4.0/
