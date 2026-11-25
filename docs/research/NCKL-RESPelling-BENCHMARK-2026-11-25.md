# NCKL Khmer-script respelling benchmark — 2026-11-25

## Purpose and representation boundary

This is a separate benchmark for the external Khmer G2P model that predicts the NCKL dictionary's **Khmer-script pronunciation respelling**, with hyphens marking syllable boundaries. It is not an IPA task. Its metrics must never be merged with the repository's IPA CER tables, treated as IPA accuracy, or used to promote a typed IPA result.

The dataset card explicitly describes its target as Khmer-script respelling rather than IPA and notes dictionary-only, standard Phnom Penh, isolated-word scope. It also notes that source errors may remain.

## Pinned sources

| Component | Pin | Scope |
|---|---|---|
| Dataset | `phonsobon/khmer-G2P` revision `2733e664ed4d77dee4cc588a130bb4844c9da767` | NCKL Khmer Dictionary 2022 respelling pairs |
| Model | `phonsobon/khmer-g2p` revision `7dbc6c3d1c1f5a9a8763be602fa679f130f20dca` | 7,461,956-parameter character Transformer |
| Model architecture source | `PhonSobon/Khmer-pronunciation` revision `66b526ebd5edbacfeb7178f377de30662d9b30d2` | Upstream inference architecture and tokenizer |
| Target split | `test` | Word-disjoint from train and validation |

Dataset card split sizes: train 34,770 pairs / 33,979 unique words; validation 1,939 / 1,888; test 1,920 / 1,888. The harness verifies the split sizes and checks pairwise word-disjointness before inference.

The model card reports 83.37% validation word accuracy. The PyPI package description reports 83.2% word accuracy and 4.2% character error rate on its test split; those are upstream claims, not this repository's measurements.

## Metrics

- **Output coverage:** unique words with non-empty model output / unique test words.
- **Word exact-match rate:** output equals any source-attested NCKL alternative for that word / unique test words.
- **Character error rate:** minimum Unicode code-point Levenshtein distance to an attested alternative, divided by the selected reference's code-point count. For multiple readings, the minimum-edit alternative is used, matching the upstream evaluator's selection policy.
- **Syllable-count accuracy:** predicted hyphen count matches the selected reference's hyphen count / unique test words.

These are held-out source-attested respelling test metrics for the external model. They are not independent IPA gold and do not measure the repository's IPA engine.

## Rights and retention

The dataset's Hugging Face license label is `other / nckl-khmer-dictionary-2022`. Its card states that the underlying content is © National Council of Khmer Language (NCKL), Royal Academy of Cambodia, and asks users to check NCKL terms before commercial use or redistribution. The model card declares MIT for the model weights.

The workflow fetches the dataset and model ephemerally. It uploads only aggregate metrics and provenance; it does not store source rows, words, references, raw predictions or per-word errors. No NCKL data is committed to this repository. Commercial use or redistribution remains blocked pending direct terms clarification.

## Implementation and verification

- Harness: `scripts/benchmark_nckl_respelling.py`.
- Tests: `tests/test_benchmark_nckl_respelling.py`.
- Optional workflow: `.github/workflows/optional-nckl-respelling-benchmark.yml`.
- Test-first RED: Quality run [45581925948](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45581925948) failed exactly because the harness module did not yet exist (6 expected FileNotFoundError failures; 507 existing tests and 70 subtests passed).
- Final harness/benchmark execution: pending.
- This benchmark is diagnostic research only; no runtime model integration is proposed.
