# Google Khmer pronunciation lexicon — attribution and limits

This project now bundles the complete pinned Google Khmer source TSV and a reproducibly generated, compact word-frequency table used by the provisional segmenter. The historical 3,009-entry sample remains in the repository as a regression baseline.

## Bundled artifacts

- `data/khmer/google-pronunciation-full.tsv` — complete upstream Google source TSV, including its original copyright and CC BY 4.0 header. Source revision `a90601024f07ab7e96c911243324e0adeb16da96`; Git blob SHA `d399efeca642b1185786b2982374488c525e37c4`, identical to the pinned upstream Git blob.
- `data/khmer/google-pronunciation-full-frequency.json` — runtime table with 61,980 normalized Khmer word/count pairs. It intentionally excludes all source phonemic strings. SHA-256 `a5d901e2ddce5f2370bbaf2f502a264e07127f5e97c395859a983d5a4f16b362`; 1,794,821 bytes (322,154 bytes with deterministic gzip level 9).
- `data/khmer/google-pronunciation-sample.json` — the earlier 3,009-entry attributed sample, retained as a compatibility and regression baseline. The full build preserves all 3,009 sample words with exactly matching counts.

## Sources and licences

- Khmer spellings and source phonemic strings: Google Inc., *Khmer pronunciation lexicon*, pinned source revision [a90601024f07ab7e96c911243324e0adeb16da96](https://github.com/google/language-resources/tree/a90601024f07ab7e96c911243324e0adeb16da96/km), Copyright 2018 Google Inc., **CC BY 4.0**.
- Word-frequency counts: FineWeb-2 `khm_Khmr` test split, pinned revision [af9c13333eb981300149d5ca60a8e9d659b276b9](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2/tree/af9c13333eb981300149d5ca60a8e9d659b276b9), **ODC-By 1.0**. The upstream builder uses the test split for counts; the corpus text itself is not bundled.
- Builder: [pheasaKhmer/khmer-engine](https://github.com/pheasaKhmer/khmer-engine), revision `31b72cd4665f69678fc835da2f501771e42f097a`, MIT-licensed implementation. This repository independently implements the Python and JavaScript Viterbi segmenters; it does not import the upstream runtime package.

## Reproducible build and verification

The pinned upstream `scripts/build_data.py` downloads both source artifacts, verifies their SHA-256 values, normalizes the Google spellings with `pheasa`, filters to Khmer runs containing a consonant or independent vowel, and iteratively segments the FineWeb-2 test split to calculate unigram and bigram counts.

The repository workflow `.github/workflows/full-khmer-lexicon-build.yml` performs that build and validates the runtime dataset. Earlier successful build: [GitHub Actions run 45211131496](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45211131496). The exact-`main` rebuild [45215110513](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45215110513) repeated the pinned download/checksum/build and compared the generated runtime JSON byte-for-byte with the committed file; its 2,556,088-byte artifact is [14837179566](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45215110513/artifacts/14837179566). Exact-main Quality [45215110523](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45215110523) passed 468 Python tests + 70 subtests and all parity/build checks; Chromium [45215110623](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45215110623) passed 36/36 tests; Pages deployment and deployed-asset smoke [45215110531](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45215110531) passed.

Verified build outputs:

| Output | Rows | Bytes | SHA-256 |
|---|---:|---:|---|
| Normalized word lexicon | 61,980 | 2,821,094 | `831350c0ff03c714051bdbeca3b100aa2cef65d6196edcf2d2fa1b57ac9d14e1` |
| Adjacent-word bigrams | 209,330 | 7,243,030 | `fc330cc19482e0a229c4a1c2bcbe3443cca3bacb48ff0b0f99d327682b5c5591` |
| Runtime word/count JSON | 61,980 | 1,794,821 | `a5d901e2ddce5f2370bbaf2f502a264e07127f5e97c395859a983d5a4f16b362` |

The build gate also verified: Google source SHA-256 `b3f2e700d07d6c01a4c8cac5aa2f13b9a66885668ac482cc0c513f73c56495e5`; FineWeb-2 source SHA-256 `26ae4e654770b07e24a4ef6b8ef3a01c84076a920f1922ac014364ab411b84f0`; 3,009/3,009 sample entries preserved; zero missing sample words; zero sample count mismatches. The bigram table is generated and retained in the build artifact for future research, but is not currently used by the runtime Viterbi segmenter.

## Runtime use and separation from IPA

Only word spellings and frequency counts from the compact JSON are used by the segmenter. The full Google TSV retains source phonemic strings for provenance, but neither those strings nor the historical sample phonemic strings are treated as project IPA, passed to the IPA-to-Ukrainian adapter, or used to determine canonical pronunciation.

The segmenter uses frequency-weighted dictionary matching over Khmer cluster boundaries. Unknown clusters remain OOV; registered multi-cluster lexical fixtures remain protected spans. Python and JavaScript expose up to three distinct n-best paths per unprotected chunk. Candidate costs are uncalibrated negative-log frequency scores, not probabilities, confidence values or accuracy estimates. The maximum dictionary word length is 14 orthographic clusters; n-best diagnostics remain bounded to 128 clusters per chunk.

## Limitations

- No independent manually adjudicated Khmer segmentation gold corpus has been evaluated; segmentation accuracy is **NOT ASSESSED**.
- A dictionary match does not prove that a boundary is correct in a particular context. A larger dictionary improves lexical coverage, not demonstrated linguistic accuracy.
- FineWeb-2 frequencies are web-text frequency counts, not pronunciation evidence, stress evidence, or a dialect/profile signal.
- The 209,330 bigram rows are available as a reproducible research artifact but are not yet part of the production segmentation algorithm.
- Do not promote Google phonemic strings to project IPA or lexical gold without a separately documented conversion and adjudication process.
