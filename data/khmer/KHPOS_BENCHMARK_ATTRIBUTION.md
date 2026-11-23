# khPOS OPEN-TEST benchmark — attribution and limits

## Source

- Corpus: [khPOS — Khmer Part-of-Speech Corpus](https://github.com/ye-kyaw-thu/khPOS), draft release 1.0.
- Citation: Ye Kyaw Thu, Vichet Chea and Yoshinori Sagisaka (2017), “Comparison of Six POS Tagging Methods on 12K Sentences Khmer Language POS Tagged Corpus”, ONA 2017, Phnom Penh.
- Pinned repository revision: `0211405c145b0a340ad558569bd06c946b2296b4`.
- Evaluated file: `corpus-draft-ver-1.0/data/OPEN-TEST.word`.
- Git blob SHA-1: `34cf93f298c06723419212f0f0777f3783537069`.
- File contains 1,000 sentences and 10,778 whitespace-delimited gold tokens. The companion `OPEN-TEST` and `OPEN-TEST.tag` files have 1,000 lines and matching per-line token counts.
- License declared by the upstream repository: **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**.

## Distribution policy

The corpus is **not** committed to this repository, copied into the website, or uploaded as a CI artifact. The benchmark script fetches only the pinned `OPEN-TEST.word` file into a temporary directory, verifies its Git blob SHA-1, evaluates it, and deletes the temporary copy. Only aggregate metrics are printed. This workflow is intended solely for non-commercial research evaluation with attribution; it does not grant permission to redistribute the corpus or use it commercially.

## Benchmark method

- Reconstruct the unsegmented surface by concatenating gold tokens after NFC normalization.
- Remove the corpus's annotation joiners `~`, `_` and `^` from token surfaces, but keep each marked token as **one** gold token. They are annotation notation, not Khmer orthographic characters.
- Score only boundaries between adjacent Khmer word tokens. Punctuation, numbers and non-Khmer tokens are retained in the reconstructed input but their boundaries are not included in the word-boundary metric.
- Report corpus-level boundary precision, recall and F1, plus exact sentence segmentation on sentences containing at least one gold boundary.
- Run both the canonical Python engine and browser JavaScript engine against the same input; the workflow fails if their aggregate counts differ.

## Limitations

- khPOS is a manually segmented external benchmark, but its target variety, annotation adjudication protocol and compound-token policy are not identical to this project's contemporary Phnom Penh careful-citation profile.
- The corpus spans news, economics, politics, student lists and voter lists. Possible overlap between these source texts and the FineWeb-2 frequency-training corpus has not been ruled out.
- A benchmark score measures agreement with this particular published annotation convention. It is not universal Khmer segmentation accuracy, expert-adjudicated project gold, IPA accuracy or pronunciation validation.
- Keep the project status `NOT ASSESSED` for target-profile segmentation accuracy until a rights-cleared, profile-matched and independently adjudicated benchmark is available.

## Reproduction

```bash
python scripts/evaluate_khpos.py
```

The command downloads the pinned open test file, verifies the Git blob SHA-1, runs Python and JavaScript parity evaluation, prints aggregate metrics, and removes the temporary corpus copy.


## Measured result — 2026-11-23

The exact pinned benchmark completed successfully in [GitHub Actions run 45220729721](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45220729721). Both the Python engine and browser JavaScript tokenizer returned identical aggregate counts:

| Metric | Result |
|---|---:|
| Sentences | 1,000 |
| Raw gold tokens | 10,778 |
| Khmer gold word tokens | 10,068 |
| Sentences with at least one gold boundary | 999 |
| Gold boundaries | 8,752 |
| Predicted boundaries | 9,538 |
| True-positive boundaries | 8,370 |
| False-positive boundaries | 1,168 |
| False-negative boundaries | 382 |
| Boundary precision | 87.75% |
| Boundary recall | 95.64% |
| Boundary F1 | 91.53% |
| Exact sentence segmentations | 487 / 999 (48.75%) |

This is a useful external agreement measurement, not target-profile segmentation accuracy. Precision is lower than recall, so the current system tends to introduce too many boundaries relative to this corpus. The score must not be generalized beyond this dataset's annotation convention, and possible overlap with FineWeb-2 source texts remains unknown. The project's target-profile segmentation accuracy stays `NOT ASSESSED`.


## Extended word-level evaluation — 2026-11-23

The evaluator now reports exact token-span precision/recall/F1 in addition to the original Khmer-only boundary metric. A token is correct only when both its start and end match one gold token span.

- **All-token word-level:** includes punctuation and non-Khmer tokens, matching the complete 10,778-token inventory: 10,778 gold, 11,578 predicted, 9,002 true positives, 2,576 false positives, 1,776 false negatives; precision 77.75%, recall 83.52%, F1 **80.53%**; exact sentence matches 486/1,000.
- **Khmer-only word-level:** excludes punctuation and non-Khmer tokens: 10,068 gold, 10,871 predicted, 8,336 true positives, 2,535 false positives, 1,732 false negatives; precision 76.68%, recall 82.80%, F1 **79.62%**; exact sentence matches 487/1,000.
- **Khmer-only boundary-level (the original metric):** 8,752 gold boundaries, 9,538 predicted, 8,370 true positives, 1,168 false positives, 382 false negatives; precision 87.75%, recall 95.64%, F1 **91.53%**; exact sentence matches 487/999 sentences with at least one gold boundary.

The Python and JavaScript evaluators now match **exactly for every sentence**, not just aggregate totals. The per-sentence prediction signature is SHA-256 `fd345cc72b5fea63854bec556cd0df4bbcd83fd2f3149d6ec50b271c09b5d4f5`. Verification: [PR run 45224355067](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45224355067); merged-main rerun is tracked separately in the canonical handoff.

### Published comparison and limits

Wen et al. (2024), [*UnifiedCut: A Simple and Efficient Neural Model for Thai, Burmese and Khmer Word Segmentation*](https://doi.org/10.3390/app142311435), report on the khPOS open test set word-level P/R/F1 of 96.9/97.3/97.1% for KhPOS and 98.3/98.7/98.5% for UnifiedCut. The paper defines word-level precision and recall by exact correctly segmented words and uses the PyThaiNLP benchmark module. Our all-token metric is the closest available comparison because it includes the full 10,778-token inventory, but it is **contextual rather than a strict reproduction**: the exact handling of annotation markers, punctuation, normalization and evaluator versions may differ. The Khmer-only 79.62% metric is a separate project diagnostic, not the paper's reported all-token score. Do not compare the 91.53% boundary F1 to the paper's word-level F1.

The large gap is a useful warning that this deterministic dictionary segmenter is still a provisional baseline, not a substitute for a contextual statistical model or expert review. None of these scores measures pronunciation, IPA correctness, or segmentation accuracy for the project's contemporary Phnom Penh careful-citation profile. That target-profile accuracy remains **NOT ASSESSED**.
