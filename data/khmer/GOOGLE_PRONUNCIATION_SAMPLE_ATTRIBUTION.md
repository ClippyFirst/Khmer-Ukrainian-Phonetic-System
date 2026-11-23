# Google Khmer pronunciation sample — attribution and limits

This project bundles the **3,009-entry sample** at `data/khmer/google-pronunciation-sample.json`.

## Sources and licences

- Khmer spellings and source phonemic strings: Google Inc., *Khmer pronunciation lexicon*, pinned source revision [a90601024f07ab7e96c911243324e0adeb16da96](https://github.com/google/language-resources/tree/a90601024f07ab7e96c911243324e0adeb16da96/km), Copyright 2018 Google Inc., **CC BY 4.0**.
- Word-frequency counts: FineWeb-2 `khm_Khmr` test split, pinned revision [af9c13333eb981300149d5ca60a8e9d659b276b9](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2/tree/af9c13333eb981300149d5ca60a8e9d659b276b9), **ODC-By 1.0**.
- The sample was packaged and normalized by [pheasaKhmer/khmer-engine](https://github.com/pheasaKhmer/khmer-engine), revision `31b72cd4665f69678fc835da2f501771e42f097a`. Its implementation code is MIT-licensed; this project independently implements the Viterbi segmentation routine rather than importing that Python package.
- The sample file blob in the upstream repository is `1bc4f28d6666fa6812b738385447e9c7fc5330f9`.

## What this project uses

Only the word spellings and frequency counts are used by the current segmenter. The phonemic strings are retained as source data for future research but are **not treated as IPA**, are not passed to the IPA-to-Ukrainian adapter, and do not determine the canonical pronunciation result.

The segmenter uses frequency-weighted dictionary matching over Khmer cluster boundaries. Unknown clusters are retained as OOV runs. The canonical output is the lowest-cost **provisional word-boundary candidate**, not a verified linguistic segmentation. Python and JavaScript now also expose up to three distinct n-best paths per unprotected chunk for inspection; registered multi-cluster lexical fixtures are treated as protected spans. Candidate costs are negative-log frequency scores and are not probabilities, confidence values or accuracy estimates. Diagnostic enumeration is capped at 128 orthographic clusters per chunk; longer chunks retain the existing canonical segmentation but omit n-best alternatives.

## Limitations

- The bundled sample has 3,009 entries, not the full 61,980-entry upstream lexicon.
- No independent Khmer segmentation gold corpus has been evaluated in this project; segmentation accuracy is therefore **NOT ASSESSED**.
- A dictionary match does not prove the boundary is correct in a particular context.
- The FineWeb-2 frequencies are web-text frequency counts, not pronunciation evidence or a dialect/profile signal.
- Do not promote dictionary phonemic strings to project IPA or lexical gold without a separately documented conversion and adjudication process.


## Full Google Khmer lexicon rebuild route — 2026-11-23

A reproducible upstream route for the full dictionary has now been located and source-reviewed:

- Upstream builder: [pheasaKhmer/khmer-engine](https://github.com/pheasaKhmer/khmer-engine), pinned repository revision `31b72cd4665f69678fc835da2f501771e42f097a` (MIT code).
- Builder: `scripts/build_data.py`; the exact pinned source is available in the upstream repository. It downloads the Google lexicon and FineWeb-2 test split, checks both against SHA-256 before processing, normalizes spellings with `pheasa`, filters to Khmer runs containing a consonant or independent vowel, then iteratively segments FineWeb text for unigram/bigram counts.
- Google source: `km/data/lexicon.tsv` at `a90601024f07ab7e96c911243324e0adeb16da96`; SHA-256 `b3f2e700d07d6c01a4c8cac5aa2f13b9a66885668ac482cc0c513f73c56495e5`; CC BY 4.0. Upstream README reports 62,179 Khmer-script entries before its normalization/filtering.
- Frequency source: FineWeb-2 `khm_Khmr/test/000_00000.parquet` at `af9c13333eb981300149d5ca60a8e9d659b276b9`; SHA-256 `26ae4e654770b07e24a4ef6b8ef3a01c84076a920f1922ac014364ab411b84f0`; ODC-By 1.0. The upstream builder uses the test split for counts only and does not ship its source text; its README notes Common Crawl terms for the underlying web documents.
- Upstream reports a resulting 61,980-word lexicon after normalization/filtering and a separate bigram table. These are upstream-reported build results, not independently reproduced by this project.

**Retrieval and integrity verification — 2026-11-23:** the pinned raw Google TSV was retrieved over HTTPS (HTTP 200) without byte transformation. Its SHA-256 was independently computed as `b3f2e700d07d6c01a4c8cac5aa2f13b9a66885668ac482cc0c513f73c56495e5`, matching the published upstream checksum. The exact source snapshot is stored unchanged at `data/khmer/google-pronunciation-full.tsv`. Its GitHub blob SHA `d399efeca642b1185786b2982374488c525e37c4` matches the blob SHA returned for the pinned Google source itself, providing an additional byte-identity check. The raw TSV contains 69,415 data rows and 69,405 unique raw spellings before upstream normalization/filtering; these counts are not a replacement for the upstream builder's reported 61,980 normalized entries.

The FineWeb-2 Parquet bytes and the complete upstream build have not yet been executed in this environment. The pinned Parquet response is approximately 90.7 MB and exceeds the available retrieval service's 64 MiB decoded-response limit; the repository execution container has no outbound network/DNS.

**Status:** the Google lexicon retrieval blocker is **RESOLVED** and a pinned, checksum-verified copy is committed. Full frequency-dictionary integration remains **BLOCKED pending byte-preserving retrieval and checksum verification of the FineWeb-2 Parquet file**, execution of the deterministic builder, artifact-size/startup review, and Python/JavaScript parity plus segmentation regression checks. Do not infer missing frequency counts or relabel Google phonemic strings as IPA.


## Full upstream source now bundled

The complete pinned Google source file is now stored unchanged at `data/khmer/google-pronunciation-full.tsv`. It retains Google's original copyright and CC BY 4.0 header. The source was retrieved from the pinned raw URL and added to this repository; the repository's resulting Git blob SHA is `d399efeca642b1185786b2982374488c525e37c4`, matching the source blob SHA returned by GitHub for the pinned upstream file. The Markdown-rendered preview was not used as data; the raw response was used, preserving the TSV tabs.

This closes the source-file acquisition portion only. The full normalized 61,980-word frequency dictionary and bigram table are **not yet built**. The FineWeb-2 Parquet source still needs byte-preserving retrieval and its SHA-256 check, then the pinned upstream builder must run in a network-enabled Python environment. The runtime continues to use the 3,009-entry sample until the generated full dictionary is validated and ported with Python/JavaScript parity. The Google phonemic strings remain upstream phonemic notation, not project IPA.
