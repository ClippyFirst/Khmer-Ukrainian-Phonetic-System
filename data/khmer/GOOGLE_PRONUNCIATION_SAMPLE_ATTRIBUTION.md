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
