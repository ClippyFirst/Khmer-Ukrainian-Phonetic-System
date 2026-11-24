# Khmer runtime and segmentation benchmark — 2026-11-24

## Scope

This run verifies that the deterministic Khmer engines return usable partial output rather than suppressing an entire input when full IPA is unavailable. It also measures the JavaScript and Python implementations on the same input set.

The benchmark is an engineering throughput and output-availability test. It is **not** a phonetic-accuracy benchmark: the independent, adjudicated IPA gold corpus still contains 0 entries, so pronunciation accuracy remains `NOT_ASSESSED`.

## Deterministic Python ↔ JavaScript core

Source: `npm run bench:engine` in Quality workflow [45469711688](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45469711688), PR head `0d53d301331d33c5877299f8cbd730bfe85c84bc`.

| Measure | JavaScript core | Python engine |
|---|---:|---:|
| Runtime | Node v24.22.3 | Python 3.12.16 |
| Unique NFC inputs | 39 | 39 |
| Warm-up batches | 5 | 5 |
| Measured batches | 25 | 25 |
| Median batch latency | 1.3028 ms | 5.2737 ms |
| Throughput | 29,934.7 inputs/s | 7,395.16 inputs/s |
| Complete | 37 | 37 |
| Partial | 2 | 2 |
| Unresolved | 0 | 0 |

The common input set is the union of:

- `data/tests/web-fixtures.json`
- `data/tests/verified-lexical-corpus.json`
- `data/tests/khmer-onset-fallback-fixtures.json`

The Node-hosted JavaScript core processed this set about 4.05× faster than Python in this CI run. This ratio is environment-specific and is not a browser-device latency guarantee.

Coverage counts mean that the engine returned a complete or explicitly partial result. They do not mean that a `PROPOSED` result is expert-validated or acoustically correct. Both engines returned 37 `PROPOSED` cases, one `NOT_ESTABLISHED` case with an onset-only preview, and one `EVIDENCE_LIMITED` case with an onset-only preview.

## Browser tokenizer stress

Source: `npm run bench:tokenizer`, same Quality run [45469711688](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45469711688).

- Input: 8,000 Khmer code points.
- Dictionary: 61,980 entries.
- Median: 7.65 ms.
- Throughput: 1,046,065 code points/s.
- Source preservation: PASS.
- Inserted candidate boundaries: 7,999.

This is a deterministic tokenizer stress test, not a segmentation-accuracy result or a universal device latency guarantee.

## Independent segmentation comparisons

- [External khPOS segmentation benchmark — run 45469711811](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45469711811): PASS.
- [Pinned upstream Rust Khmer segmentation comparison — run 45469711685](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45469711685): PASS.

These are segmentation evaluations, not pronunciation or IPA validation. The pinned Rust workflow's ephemeral HMM/tagger training is research-only and non-commercial; models are trained in memory only and no redistributable model artifact is produced.

## Browser behavior verification

- [Chromium browser smoke — run 45469711820](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45469711820): PASS, including the visible-result assertion in Chromium.
- The test specifically checks an unsupported independent vowel: IPA remains `⟦NOT_ESTABLISHED⟧`, while the main Ukrainian field shows the separately typed orthographic fallback ending in `???` and the UI states that it is not a pronunciation claim.
- Onset-only IPA previews take precedence over orthographic fallback when the source-registered onset is known. Vowels, codas, tones and full syllables are not inferred from an orthographic candidate.

## Interpretation and remaining limits

- The user-visible output no longer needs to be all-or-nothing: known neighboring material and source-registered onsets survive, and unknown material is marked with `???`.
- The orthographic fallback is explicitly not IPA and is never promoted into `canonical_ipa` or `canonical_ua`.
- Python and JavaScript coverage is aligned on this 39-input engineering corpus, but this is not an independently adjudicated pronunciation corpus.
- Full contextual Khmer phonology, tone/length/coda interactions, independent IPA gold data and accuracy measurement remain `PARTIAL` / `NOT_ASSESSED`.

## Relation to the Lao implementation

The Lao repository's grapheme-preview and stress-benchmark reports were used as a behavioral reference: retain partial output, type its uncertainty, measure latency and coverage separately, and avoid claiming accuracy without held-out gold. The Khmer corpus and phonology differ, so Lao benchmark scores are not treated as directly comparable targets.


## Typed IPA contract overhead — 2026-11-24

Source: latest successful exact-source/docs-head Quality workflow [45490428639](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45490428639), branch `feat/khmer-lao-engine-contract-parity-20261124`, docs-evidence head `79d7ff26e2f7c5905ea4ed6fde903fdbfe81de82`. The implementation source/test head is `f579e1444fbda2b186fdf8a04dc9f52f7ebc044e`; subsequent commits are documentation and evidence-register updates only.

| Measure | JavaScript core | Python engine |
|---|---:|---:|
| Runtime | Node v24.22.3 | Python 3.12.16 |
| Unique NFC inputs | 39 | 39 |
| Warm-up / measured batches | 5 / 25 | 5 / 25 |
| Median batch latency (run 45490428639) | 1.5012 ms | 7.8004 ms |
| Throughput (run 45490428639) | 25,980.01 inputs/s | 4,999.74 inputs/s |
| Complete / partial / unresolved | 37 / 2 / 0 | 37 / 2 / 0 |
| Same-source-head repeat (45489728897) | 1.4829 ms | 8.6119 ms |
| Second same-source-head repeat (45489719057) | 1.4772 ms | 9.1197 ms |

Compared with the earlier main-branch measurement (1.3028 ms JS; 5.2737 ms Python), the latest docs-evidence-head run is 15.2% higher in the JS median and 47.9% higher in the Python median. Repeated runs on the same source/test head vary (Python 7.8004–9.1197 ms; JS 1.4772–1.5012 ms), showing CI runner variance. These are microbenchmarks, not a controlled before/after experiment; runner contention and environment noise may contribute, so the figures must not be attributed wholly to typed segmentation. Absolute throughput remains approximately 26.0k / 5.0k fixture inputs per second, or 0.20 ms per fixture in the Python batch. The measured overhead is recorded for future profiling; no speculative optimization was added without a controlled repeat or evidence of user-visible latency. The Node/Python speed ratio is 5.20× in the latest run.

Tokenizer stress on run 45490428639: 8,000 code points, 61,980 dictionary entries, 6.74 ms median, 1,187,391 code points/s, source preserved. This is a stress microbenchmark, not a segmentation-accuracy measure.

Coverage and throughput remain engineering measures. The input corpus is not adjudicated IPA gold; pronunciation accuracy remains NOT_ASSESSED.
