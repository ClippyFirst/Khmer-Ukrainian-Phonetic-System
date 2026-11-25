# NCKL Khmer-script respelling benchmark — 2026-11-25

## Purpose and representation boundary

This is a separate benchmark for the external Khmer G2P model that predicts the NCKL dictionary's **Khmer-script pronunciation respelling**, with hyphens marking syllable boundaries. It is not an IPA task. Its metrics must never be merged with the repository's IPA CER tables, treated as IPA accuracy, or used to promote a typed IPA result.

The dataset card explicitly describes its target as Khmer-script respelling rather than IPA and notes dictionary-only, standard Phnom Penh, isolated-word scope. It also notes that source errors may remain.

## Pinned sources

| Component | Pin | Scope |
|---|---|---|
| Dataset | `phonsobon/khmer-G2P` revision `2733e664ed4d77dee4cc588a130bb4844c9da767` | NCKL Khmer Dictionary 2022 respelling pairs |
| Model | `phonsobon/khmer-g2p` revision `7dbc6c3d1c1f5a9a8763be602fa679f130f20dca` | 7,461,956-parameter character Transformer |
| Inference package | `khmer-g2p==0.1.0` (PyPI, MIT) | Package exposes `KhmerG2P(..., revision=...)`, so the Hub model revision is pinned explicitly |
| Target split | `test` | Word-disjoint from train and validation |

Dataset: [phonsobon/khmer-G2P](https://huggingface.co/datasets/phonsobon/khmer-G2P). Model: [phonsobon/khmer-g2p](https://huggingface.co/phonsobon/khmer-g2p). Upstream source: [PhonSobon/Khmer-pronunciation](https://github.com/PhonSobon/Khmer-pronunciation). Dataset card split sizes: train 34,770 pairs / 33,979 unique words; validation 1,939 / 1,888; test 1,920 / 1,888. The harness verifies the split sizes and checks pairwise word-disjointness before inference.

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
- Final Quality [45582195369](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45582195369): SUCCESS — full Python, JS, parity, deterministic benchmark and build suite.
- Initial NCKL inference [45582195410](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45582195410) SUCCESS using the upstream GitHub source checkout. That run is superseded for final provenance because the GitHub source repository has no standalone license file. The final benchmark must be rerun using the MIT-licensed PyPI package below; do not use the initial artifact as final evidence.

## Measured result

Final MIT-package inference [45582973744](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45582973744) succeeded using `khmer-g2p==0.1.0` and the pinned Hub model revision. Aggregate artifact [15006794082](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45582973744/artifacts/15006794082) was inspected; ZIP SHA-256 `915727bce6e27d28b2191f116ba6e8dc03fd0004c21d1c53e9b67e8709146f1e`; JSON SHA-256 `3fde5453bb9a739ea55ab4b7510716671898b7c3ddd5fb145410bb7cc7ec27fc`. The archive contains only aggregate JSON and its checksum sidecar, with no row-level records.

| Metric | Final result |
|---|---:|
| Reference pairs | 1,920 |
| Unique test words | 1,888 |
| Output coverage | 100% (1,888/1,888) |
| Word exact matches | 1,570 / 1,888 |
| Word exact-match rate | 83.16% |
| Character edits | 803 / 19,298 reference code points |
| Character error rate | 4.16% |
| Syllable-count accuracy | 93.06% (1,757/1,888) |

The final MIT-package run reproduces the upstream PyPI-reported test results to one decimal place (83.2% exact / 4.2% CER). The earlier GitHub-source-checkout run is superseded and not used as final evidence. These metrics concern NCKL Khmer-script respelling only; no IPA accuracy was measured.
- This benchmark is diagnostic research only; no runtime model integration is proposed.
