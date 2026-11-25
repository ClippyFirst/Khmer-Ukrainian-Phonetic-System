# Shared Khmer IPA engine benchmark — 2026-11-25

## Executive result

A reproducible CI run evaluated four engines on two Khmer IPA sources: a 100-word MekongPhon lexical evaluation split and a 1,509-word IPA-Dict cross-source subset after filtering overlaps with the visible MekongPhon train/eval files. The project rule engine returned non-empty material for 95/100 inputs in the first set (94 partial/provisional onset hints) and 881/1,509 in the second (858 partial/provisional). The pinned MekongPhon neural model had the lowest source-attested CER on both sets; Khmer Phonemizer was second. Epitran returned strings for every word but had poor concordance.

**These are source-attested diagnostics, not independent accuracy scores.** The repository's expert-adjudicated Khmer IPA gold remains empty (0 rows); accuracy remains null and no candidate is promoted to canonical IPA.

## Reproducibility

- Repository PR: [#570](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/pull/570)
- Initial 100-word benchmark code head: 84830e3e8d2fe0c30e555ddef868ac864915fa52.
- Final two-source benchmark code/test head: 7a9f081795bcfcc5bc4c0b7d55179828cbe2a898 (subsequent commits on PR #570 update documentation/registers only).
- Shared benchmark workflow: [45499595763](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45499595763) — SUCCESS.
- Full project quality workflow: [45500823635](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45500823635) — SUCCESS.
- Chromium browser smoke: [45500823563](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45500823563) — SUCCESS.
- Two-source/four-engine benchmark: [45500823688](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45500823688) — SUCCESS; aggregate-only artifact [14971017765](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45500823688/artifacts/14971017765), SHA-256 a58d45ff1fac02aca2d9a6ff04779a16e738afc1992cc67b0bb02e78ed59b3e9.
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

## Results — external IPA-Dict cross-source subset

Source: [open-dict-data/ipa-dict](https://github.com/open-dict-data/ipa-dict), Khmer file data/km.txt at commit 972cd67dd5f96bc5660e28070cde26e3928abcd7. The source file has 3,286 rows and 3,261 unique orthographies. It is derived from the aakanee.com Khmer-English Dictionary; its Khmer data retain CC BY-NC-SA 4.0 terms. File SHA-256: d125b5ec03f661b0f02af47efebac3e018bd435b605b0a3dc8444570f910ef2a.

To reduce direct training leakage, the harness excluded 1,732 orthographies overlapping the visible MekongPhon train file and 20 overlapping its visible eval file. The remaining set contains 1,509 unique forms; 24 forms have multiple source-listed IPA alternatives. Scoring accepts any listed alternative and uses the best normalized code-point edit ratio among alternatives. No source words, references or per-word predictions are saved in the artifact.

| Engine | Non-empty output | Partial / provisional | Strict source matches | Source-attested CER | Mean latency |
|---|---:|---:|---:|---:|---:|
| Project deterministic rules | 881/1,509 (58.38%) | 858 | 0/1,509 | 83.41% | 0.542 ms/input |
| Khmer Phonemizer 0.0.3 | 1,509/1,509 (100%) | 0 | 81/1,509 (5.37%) | 33.40% | 0.289 ms/input |
| Epitran 1.35.3 (khm-Khmr) | 1,509/1,509 (100%) | 0 | 0/1,509 | 114.50% | 0.021 ms/input |
| MekongPhon neural | 1,509/1,509 (100%) | 0 | 218/1,509 (14.45%) | 14.52% | 31.705 ms/input |

This second source changes the interpretation materially. MekongPhon still has the best CER, but its exact-match rate drops from 64% on the 100-word MekongPhon evaluation split to 14.45% on this external dictionary source. This indicates strong source/profile sensitivity and means the model must be presented as approximate, not as a universal Khmer pronunciation oracle. Its full training corpus may include data beyond the visible 7,940-row train/8,041-row lexicon snapshot, so excluding visible overlaps does **not** prove absence of all model-training leakage.

The project's deterministic engine has lower coverage on this broader lexical set (58.38%) and still no exact full-word matches; 858 outputs are partial/provisional. This confirms the main weakness is productive coverage, especially full syllable/vowel/coda generation, not throughput. Khmer Phonemizer is a substantially better low-latency fallback than the current rule-only output, but its CER is more than twice MekongPhon's on this set. Epitran again has 100% output coverage but poor source concordance.

Both IPA sources are source-attested dictionaries, not independently adjudicated project gold. The IPA-Dict source is a different dictionary, but dialect and transcription-convention equivalence with the target remains unverified. The model may have seen additional data beyond the accessible MekongPhon snapshot. These scores are therefore cross-source diagnostics only; accuracy remains NOT_ASSESSED.

## What this says about the current IPA engine

The main bottleneck is not runtime speed or the size of the Khmer character inventory. The current rule engine has a narrow evidence-backed set of full lexical readings and only limited productive phonology. Outside that coverage it preserves a registered onset hint, then marks the rest unresolved. This is an intentional evidence gate, but it is too conservative as the only user-facing result path when a separately labelled approximate candidate is acceptable.

Khmer spelling is not a one-letter/one-sound code. Unicode's Khmer chapter documents two consonant registers, register shifters, inherent vowels and dependent-vowel values that vary with consonant context. The orthographic syllable structure also does not always align with phonological syllables. See [Unicode Chapter 16](https://www.unicode.org/versions/Unicode18.0.0/core-spec/chapter-16/) and [W3C Khmer layout requirements](https://www.w3.org/TR/khmr-lreq/).

## External research and datasets

### MekongPhon — IPA G2P

Shurtz, Richardson & Richardson (LREC 2026) report 1.3 million Khmer orthography–IPA pairs and under 2% CER for a Transformer on their held-out test sets. They also report their linguistically informed transliteration tools outperforming Epitran by 6–71 CER points. Those are the paper's results, not the result of this repository's 100-row diagnostic. The accessible upstream snapshot used here contains a 100-row Khmer evaluation file and a visible train split of 7,940 entries (8,041 lexicon-file lines including header), far smaller than the 1.3-million-pair scale reported in the paper. The repository snapshot has no declared corpus-data license. The test here is therefore ephemeral, source-attested research only; no dataset rows or model weights were copied into this repository.

Paper: [MekongPhon, LREC 2026](https://aclanthology.org/2026.lrec-1.129/), DOI [10.63317/4bb9rvdshu4z](https://doi.org/10.63317/4bb9rvdshu4z).

### NCKL / PhonSobon Khmer G2P — orthographic pronunciation, not IPA

The phonsobon/khmer-G2P dataset reports 38,629 word-to-pronunciation pairs (37,755 unique words), including a word-disjoint test split of 1,920 pairs / 1,888 unique words. Its targets are Khmer-script pronunciation respellings with syllable separators, not IPA. It is a valuable separate benchmark for syllabification and dictionary-reading recovery, but its scores must not be combined with the IPA CER above. The source is the 2022 NCKL Khmer Dictionary; the dataset card asks users to check NCKL's terms, particularly before commercial use.

Dataset: [phonsobon/khmer-G2P](https://huggingface.co/datasets/phonsobon/khmer-G2P). A 7.5M-parameter model card reports 83.37% best validation word accuracy; that is a validation result, not a held-out test result and not IPA accuracy: [phonsobon/khmer-g2p](https://huggingface.co/phonsobon/khmer-g2p).

### NCKL / PhonSobon — Khmer-script respelling benchmark (separate task)

The NCKL-derived `phonsobon/khmer-G2P` corpus is evaluated on its own word-disjoint test split, separately from all IPA benchmarks. It contains 1,920 test pairs / 1,888 unique words, with multiple accepted readings grouped by word. Targets are Khmer-script pronunciation respellings with hyphen syllable boundaries, not IPA.

Pinned dataset revision: `2733e664ed4d77dee4cc588a130bb4844c9da767`. Pinned model revision: `7dbc6c3d1c1f5a9a8763be602fa679f130f20dca` (7,461,956 parameters; model card declares MIT). Inference uses the MIT-licensed PyPI package [`khmer-g2p==0.1.0`](https://pypi.org/project/khmer-g2p/0.1.0/) and passes the immutable model revision explicitly. The unlicensed upstream GitHub source checkout was removed.

Our harness reports output coverage, exact match against any NCKL alternative, code-point CER, and syllable-count accuracy. These are source-attested NCKL respelling metrics only. They cannot be compared with IPA CER, used as IPA accuracy, or promoted to the project's independent IPA gold.

Rights: the dataset card uses the custom `other / nckl-khmer-dictionary-2022` label and states that the underlying dictionary remains © NCKL; it asks users to check NCKL terms before commercial use or redistribution. The optional workflow downloads data ephemerally and uploads aggregate metrics only. Commercial use and redistribution remain blocked pending NCKL terms clarification.

Implementation: `scripts/benchmark_nckl_respelling.py`; tests `tests/test_benchmark_nckl_respelling.py`; workflow `.github/workflows/optional-nckl-respelling-benchmark.yml`; methodology `NCKL-RESPelling-BENCHMARK-2026-11-25.md`. Final Quality [45582973468](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45582973468) passed (513 tests, 70 subtests); final MIT-package inference [45582973744](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45582973744) passed. Aggregate artifact [15006794082](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45582973744/artifacts/15006794082) inspected and checksum verified.

Final measured results: 1,888 unique words, 1,920 reference pairs, 1,888 non-empty outputs (100% coverage), 1,570 exact matches (83.16%), 803 character edits / 19,298 reference code points (4.16% CER), and 1,757 correct syllable counts (93.06%). Batched CPU inference took 70.80 seconds (batch size 64; 37.50 ms per word amortized across batches on the GitHub runner; not single-request latency). The initial GitHub-source-checkout run is superseded and excluded from final evidence.

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
- Four-engine same-input execution: DONE_VERIFIED on both sources (100 MekongPhon words and 1,509 non-overlapping IPA-Dict forms; all four engines ran).
- Independent IPA gold: BLOCKED / 0 records.
- Pronunciation accuracy: NOT_ASSESSED.
- Production neural fallback: BLOCKED pending profile adjudication, asset/data rights review and browser/runtime architecture decision.
