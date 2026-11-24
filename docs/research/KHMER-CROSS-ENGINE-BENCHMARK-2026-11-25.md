# Shared Khmer IPA engine benchmark — 2026-11-25

## Executive result

A reproducible CI run evaluated four engines on the same 100-word MekongPhon Khmer held-out lexical split. The project rule engine returned non-empty material for 95/100 inputs, but 94 of those outputs were partial/provisional onset hints. The pinned MekongPhon neural model was the strongest candidate on this small source-attested sample; Khmer Phonemizer was second. Epitran returned something for every word but its string concordance was poor.

**These are source-attested diagnostics, not independent accuracy scores.** The repository's expert-adjudicated Khmer IPA gold remains empty (0 rows); accuracy remains null and no candidate is promoted to canonical IPA.

## Reproducibility

- Repository PR: [#570](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/pull/570)
- Exact code head: 84830e3e8d2fe0c30e555ddef868ac864915fa52
- Shared benchmark workflow: [45499595763](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45499595763) — SUCCESS.
- Full project quality workflow: [45499595556](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45499595556) — SUCCESS.
- Aggregate-only artifact: [14970916634](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45499595763/artifacts/14970916634), SHA-256 d8c5dba103d60ea16604326b85fe508f909e53cc795e383d3925647b753e9509.
- Corpus repository: byu-matrix-lab/MekongPhon, pinned commit f80f6c1840c4818b51e05f2e00cded4701a5b662.
- Evaluation file: data/splits/khmer_eval.csv, 100 unique Khmer orthographies.
- Reference field: pron_no_tones (source-reported IPA without tone).
- Neural model: byumatrixlab/khmer-ipa, pinned revision 20e069d384b240da76320e1569958568c12a54bc.
- Runtime: Python 3.12.16; CPU; PyTorch 2.5.1; Transformers 4.46.3; Khmer Phonemizer 0.0.3; Epitran 1.35.3.
- Scoring: Unicode NFC only. No phone, tone, length, diacritic, syllable-boundary or delimiter normalization. CER is Unicode code-point Levenshtein distance divided by reference code points.
- The CI artifact contains aggregate metrics only; source rows, references and per-word predictions were not saved or redistributed.

## Results — same 100 inputs

| Engine | Non-empty output | Partial / provisional | Strict source matches | Source-attested CER | Mean latency |
|---|---:|---:|---:|---:|---:|
| Project deterministic rules | 95/100 (95.0%) | 94 | 0/100 | 74.61% | 0.632 ms/input |
| Khmer Phonemizer 0.0.3 | 100/100 (100%) | 0 | 18/100 | 25.71% | 2.574 ms/input |
| Epitran 1.35.3 (khm-Khmr) | 100/100 (100%) | 0 | 0/100 | 114.73% | 0.023 ms/input |
| MekongPhon neural | 100/100 (100%) | 0 | 64/100 | 12.54% | 34.897 ms/input |

The project engine's 74.61% CER must be read together with its status counts: it intentionally emitted onset-only/partial output on 94 inputs rather than claiming full IPA. Its zero exact matches therefore do not mean it generated 100 complete but wrong pronunciations. Five inputs had no non-empty IPA preview. The metric makes the missing full-syllable coverage visible.

Epitran illustrates why “it returned a string” is not enough: it had 100% output coverage, but no exact matches and a source-attested CER above 100%.

On this 100-word sample, MekongPhon has the best string concordance (64 exact; 12.54% CER), followed by Khmer Phonemizer (18 exact; 25.71% CER). This is a **candidate ranking for further evaluation only**, not proof that either provider matches the project's careful-citation profile.

## What this says about the current IPA engine

The main bottleneck is not runtime speed or the size of the Khmer character inventory. The current rule engine has a narrow evidence-backed set of full lexical readings and only limited productive phonology. Outside that coverage it preserves a registered onset hint, then marks the rest unresolved. This is an intentional evidence gate, but it is too conservative as the only user-facing result path when a separately labelled approximate candidate is acceptable.

Khmer spelling is not a one-letter/one-sound code. Unicode's Khmer chapter documents two consonant registers, register shifters, inherent vowels and dependent-vowel values that vary with consonant context. The orthographic syllable structure also does not always align with phonological syllables. See [Unicode Chapter 16](https://www.unicode.org/versions/Unicode18.0.0/core-spec/chapter-16/) and [W3C Khmer layout requirements](https://www.w3.org/TR/khmr-lreq/).

## External research and datasets

### MekongPhon — IPA G2P

Shurtz, Richardson & Richardson (LREC 2026) report 1.3 million Khmer orthography–IPA pairs and under 2% CER for a Transformer on their held-out test sets. They also report their linguistically informed transliteration tools outperforming Epitran by 6–71 CER points. Those are the paper's results, not the result of this repository's 100-row diagnostic. The accessible upstream snapshot used here has a 100-row Khmer evaluation file, and its repository snapshot has no declared corpus-data license. The test here is therefore ephemeral, source-attested research only; no dataset rows or model weights were copied into this repository.

Paper: [MekongPhon, LREC 2026](https://aclanthology.org/2026.lrec-1.129/), DOI [10.63317/4bb9rvdshu4z](https://doi.org/10.63317/4bb9rvdshu4z).

### NCKL / PhonSobon Khmer G2P — orthographic pronunciation, not IPA

The phonsobon/khmer-G2P dataset reports 38,629 word-to-pronunciation pairs (37,755 unique words), including a word-disjoint test split of 1,920 pairs / 1,888 unique words. Its targets are Khmer-script pronunciation respellings with syllable separators, not IPA. It is a valuable separate benchmark for syllabification and dictionary-reading recovery, but its scores must not be combined with the IPA CER above. The source is the 2022 NCKL Khmer Dictionary; the dataset card asks users to check NCKL's terms, particularly before commercial use.

Dataset: [phonsobon/khmer-G2P](https://huggingface.co/datasets/phonsobon/khmer-G2P). A 7.5M-parameter model card reports 83.37% best validation word accuracy; that is a validation result, not a held-out test result and not IPA accuracy: [phonsobon/khmer-g2p](https://huggingface.co/phonsobon/khmer-g2p).

### Earlier Khmer G2P research

- Kak et al. (2016), WFST-based Khmer G2P, report 3.49% phoneme error rate and 12.98% word error rate on their test set: [paper PDF](https://ksoky.github.io/static/pdf/wfst_g2p.pdf).
- Sar & Tan (2019) report their linguistic-tag-assisted statistical G2P improving PER/WER from 23.2%/69.6% to 11.1%/51.4%: [paper](https://doi.org/10.1016/j.procs.2019.11.140). The paper has internal count/metric inconsistencies noted in the earlier external-G2P audit; these figures are reported, not reproduced here.
- A 2024 publication reports 6.6% CER for a character-level Khmer G2P model and approximately 7.1% for WFST on its test set: [ACET 2024 proceedings PDF](https://www.idri.edu.kh/wp-content/uploads/2025/04/ACET_2024_Publication.pdf). This is a separate experiment and dataset.

These studies use different datasets, phone inventories, normalization and evaluation protocols. Their numbers are useful reference points, not directly comparable leaderboard entries.

## Recommended engineering direction

1. Keep the deterministic rule engine as the source-traceable canonical path where its evidence supports a complete IPA result.
2. When that path is unresolved, expose a separate **PROVISIONAL IPA candidate** from a neural/external G2P engine rather than replacing the canonical fields or returning only “unresolved”. On this run, MekongPhon is the first candidate to investigate; Khmer Phonemizer is a faster secondary fallback.
3. Preserve provider, model revision, profile match, uncertainty and raw IPA provenance. Never label the candidate SUPPORTED solely because it returned a string or scored well against this source-attested split.
4. Add a separate NCKL respelling/syllabification benchmark; do not convert its Khmer-script target mechanically into IPA.
5. Build the independent 30-item blind IPA pilot and expand it to a profile-stratified test corpus before publishing an accuracy claim.
6. Keep the static public site boundary intact for now: it has no inference backend and its browser CSP blocks network connections. A live neural fallback needs either a local browser model with measured asset/startup costs or an explicitly approved inference backend and privacy design.

## Status

- Shared-engine diagnostic harness: DONE_VERIFIED on PR #570 exact head.
- Four-engine same-input execution: DONE_VERIFIED (100/100 inputs per engine; all four ran).
- Independent IPA gold: BLOCKED / 0 records.
- Pronunciation accuracy: NOT_ASSESSED.
- Production neural fallback: BLOCKED pending profile adjudication, asset/data rights review and browser/runtime architecture decision.
