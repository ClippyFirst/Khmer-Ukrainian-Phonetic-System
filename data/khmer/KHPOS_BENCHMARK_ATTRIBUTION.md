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
