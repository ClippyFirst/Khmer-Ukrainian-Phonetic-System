# Khmer lexical word segmentation: evidence and scope audit — 2026-11-17

## Executive finding

The mixed-script/numeral defect shown by the supplied paragraph is already fixed on `main` by PR #316 and marked `DONE_VERIFIED` in the canonical handoff. The remaining limitation is different: the runtime recognizes conservative Khmer orthographic units, but it does not claim to infer lexical word boundaries in continuous Khmer text.

Do not repair this by splitting every syllable into a word, by splitting on spaces alone, or by adopting an unreviewed longest-match dictionary. Khmer spaces are not reliable word delimiters; tokenization conventions may target surface words, morphemes, compounds, or other units. These are not interchangeable with orthographic syllables used by the G2P pipeline.

## Current repository contract

- `src/khmer_ua/parser.py` and the browser tokenizer preserve source order and isolate script/numeric runs. PR #316 verifies Khmer/Latin/Khmer/numeral boundaries, unchanged numeric passthrough, and ZWNJ transparency.
- `src/khmer_ua/orthographic_syllables.py` and the corresponding browser parser address orthographic structure/syllable units, not a complete lexical segmenter.
- `src/khmer_ua/word_boundaries.py` is an evidence container. It stores candidate boundaries, profile metadata, protected cluster spans and source locators. It deliberately selects boundaries only when exactly one viable candidate is adjudicated; it does not generate word boundaries.
- The current phonetic result must not silently depend on guessed lexical segmentation. Source reconstruction and local uncertainty remain invariants.

## Research findings

### 1. ALT/NOVA is the strongest documented manually tokenized corpus lead

Kaing et al. (2021), “Towards Tokenization and Part-of-Speech Tagging for Khmer: Data and Discussion,” reports a 20,000-sentence Khmer corpus with manual tokenization and POS annotation, and evaluates SVM, CRF, LSTM and LSTM-CRF approaches. The authors conclude that morpheme-level processing is satisfactory for their data, while higher grammatical constituents in compounds/phrases remain difficult. DOI: https://doi.org/10.1145/3464378.

The NICT ALT project publishes the Khmer ALT tokenized/POS-tagged sentences and annotation guidelines. The published license is CC BY-NC-SA 4.0. The SEACrowd mirror identifies the dataset as 20,000 manually tokenized/POS-tagged sentences and carries the same license. The Zenodo record describes Khmer ALT as translations of sampled English Wikinews sentences and records an Academic Research Non-Commercial Limited CC-BY-NC-SA Reference-Type agreement. These facts make it a real research candidate, but not automatically a commercially reusable corpus. The translated-news origin also limits domain representativeness.

Sources:
- https://www2.nict.go.jp/astrec-att/member/mutiyama/ALT/
- https://att-astrec.nict.go.jp/member/mutiyama/ALT/index.html
- https://www2.nict.go.jp/astrec-att/member/mutiyama/ALT/Khmer-annotation-guideline.pdf
- https://www2.nict.go.jp/astrec-att/member/mutiyama/ALT/Khmer-annotation-guideline-supplementary.pdf
- https://zenodo.org/records/3937914
- https://huggingface.co/datasets/SEACrowd/khmer_alt_pos

The Khmer tokenization guideline (version 0.2, December 2016) is more specific than a generic “surface tokenization” label. Section 3 defines a word token as a unit that cannot be further segmented without losing its meaning and says that, because Khmer is highly analytic, words are equal to morphemes in most cases (PDF pp. 2–3). It describes compounds as integrated meanings composed of two or more words; compound components are tokenized separately and the compound relation is marked with shallow bracketing. Section 5 discusses compound identification using Chuon Nath dictionary entries and syntactic insertion diagnostics (PDF pp. 10–11). Therefore NOVA is generally morpheme-level, but its compound/POS annotation convention is not a universal lexical standard and is not interchangeable with orthographic-syllable or phonetic units in this project.

### 2. A second manually segmented corpus exists, but needs separate provenance review

The SEACrowd `khpos` dataset card describes 12,000 sentences and 25,626 manually word-segmented/POS-tagged words, with validation and test sets of 1,000 sentences each. It reports sources including economics, news, politics, student lists and election-committee voter lists. Its declared license is also CC BY-NC-SA 4.0. The inclusion of student/voter-list material requires a privacy/provenance review before any redistribution or model training.

Source: https://huggingface.co/datasets/SEACrowd/khpos

### 3. Published methods are not interchangeable gold data

- Chea et al. (2015), “Khmer Word Segmentation Using Conditional Random Fields,” reports a large manually segmented corpus and annotator strategies, with a CRF outperforming a dictionary maximum-matching baseline. The paper record does not by itself establish redistribution rights for the corpus.
  Source: https://att-astrec.nict.go.jp/member/tei/KhNLP2015-SEG.pdf
- Sung & Hwang (2016), “Ternary Decomposition and Dictionary Extension for Khmer Word Segmentation,” reports 22,726 training tokens and 6,832 manually segmented test tokens. Its proposed dictionary/longest-match method reports F1 0.906 without U+200B and 0.980 with it. The authors identify a small training corpus and do not provide a reusable dataset/code release in the inspected paper. DOI: https://doi.org/10.21219/JITAM.2016.23.2.011.
- Tran, Nguyen & Phan (2017), “Building a Syllable Database to Solve the Problem of Khmer Word Segmentation,” builds a syllable database from 48,947 dictionary entries; it is not a demonstrated sentence-level lexical segmenter. Its target variety is Khmer in Southern Vietnam, not Phnom Penh. The paper reports 92.3% average syllable-division correctness from two expert assessments, not word-boundary F1 or a held-out external benchmark. DOI: https://doi.org/10.48550/arXiv.1703.02166.

## Decision

No lexical segmentation algorithm or lexicon is added in this change. The public corpora are candidate evidence sources, not pre-approved project data. Their non-commercial/share-alike terms may be incompatible with downstream product use; the exact intended use and repository licensing must be reviewed before copying or training on them. The ALT translation-derived domain and NOVA annotation convention must also be assessed for target fit.

Keep the current source-to-IPA-to-Ukrainian path independent of guessed lexical boundaries. If a lexical segmentation feature is later approved, implement it as a separate, optional boundary-analysis layer over preserved source text, with explicit profile/version, boundary evidence, protected grapheme-cluster spans, source locators, and an abstaining/ambiguous state. Do not let proposed boundaries silently rewrite the phonetic pipeline.

## Task ledger

| ID | Status | Evidence | Acceptance criteria / blocker |
|---|---|---|---|
| KHM-MIXED-SCRIPT-NUMERAL-BOUNDARIES-001 | DONE_VERIFIED | PR #316 merged as `cca8612e98292ce2ee2f103e12bcce152d4b3416`; exact mainline Quality [44079454281], Chromium [44079454289], Pages [44079454302] all SUCCESS. | Source-run isolation and literal numeral passthrough only; no lexical segmentation claim. |
| KHM-LEXICAL-WORD-SEGMENTATION-001 | BLOCKED | Existing evidence model in `src/khmer_ua/word_boundaries.py`; ALT/NOVA and khPOS public corpora identified; relevant guidelines and research reviewed. | Before runtime implementation: approve target tokenization convention and intended use; complete license/privacy/provenance review; select rights-compatible, target-relevant data; double-annotate and adjudicate a representative pilot; freeze train/dev/test separation; report boundary precision/recall/F1 and ambiguity/abstention. |
| KHM-ORTHOGRAPHIC-SYLLABLE-PARSER-001 | DONE_VERIFIED for current structural contract; linguistic edge cases remain evidence-limited | Unicode/parser audits and existing parser test suites. | Do not relabel syllable segmentation as lexical word segmentation; remaining unsupported linguistic structures stay explicit. |

## Explicit non-claims

This audit does not assert that the ALT or khPOS corpus is suitable for commercial use, that its tokenization convention matches the project's intended display, that its labels are phonetic gold, or that its published model scores transfer to Phnom Penh careful-citation transcription. No dataset was downloaded, copied into the repository, or used to train a model. No word boundaries were inferred for the user's sample.


## Operational continuation — 2026-11-21

The private blind-intake and discrepancy-review procedure is documented in docs/research/KHMER-PRIVATE-BLIND-INTAKE-RUNBOOK-2026-11-21.md. This does not authorize use of public GitHub for blind submissions and does not imply that a private workspace exists. The 30-item IPA pilot and any separate lexical-boundary pilot require independent annotators, adjudication, item-level rights review and privacy clearance. ALT/NOVA and khPOS remain candidate research resources only; their annotation conventions are not interchangeable with phonological syllables or a universal lexical-word standard. khPOS student/election/voter-list provenance remains a stop condition until reviewed.


## Controlled external tokenizer and cross-corpus experiment — 2026-11-23

This section supersedes only the earlier statement that no corpus had been used for training. The corpus was later fetched temporarily in a non-commercial research workflow; it was not committed, redistributed, or retained as an artifact.

- Upstream implementation: `Alujack/khmer-tokenizer@f38eae5924d4e41a46fd2204cf6951cdb0dc8908`, Rust core v0.3.0, built from source in CI.
- khPOS train split: 12,000 rows, Git blob SHA-1 `3467e80897f192c4bbdb4b88fed488aaa16a830a`; khPOS OPEN-TEST: 1,000 sentences / 10,778 tokens, Git blob SHA-1 `34cf93f298c06723419212f0f0777f3783537069`.
- ALT/NOVA: Zenodo record 3937914, archive MD5 `20d39d8fa1b874b11ec374139fbe5654`; upstream article-ID-modulo-10 test split: 1,931 sentences / 69,831 tokens. The test split is a morpheme-oriented word-tokenization convention and must not be equated with phonological syllabification or this project's intended UI boundary convention.
- Both corpora are CC BY-NC-SA 4.0. The workflow used temporary files only. Exact NFC-normalized input overlaps with either test set were removed from training (12 rows; 11,988 retained). Phrase-level overlap and shared editorial conventions were not measured.
- The project word/count dictionary (61,980 rows) was used for the MinWordsDp/UnigramDp comparisons. HMM counts and a five-epoch averaged-perceptron tagger were trained in memory; no model or corpus artifact was saved or uploaded.

### Results and interpretation

| Strategy | khPOS Khmer-word F1 | khPOS boundary F1 | ALT Khmer-word F1 | ALT boundary F1 |
|---|---:|---:|---:|---:|
| Current project Viterbi | 79.62% | 91.53% | **70.15%** | **88.52%** |
| Rust MinWordsDp | 78.16% | 90.35% | 69.11% | 87.83% |
| Rust UnigramDp | 78.76% | 90.70% | 69.50% | 88.07% |
| MinWordsDp + HMM | 78.16% | 90.35% | 69.10% | 87.83% |
| UnigramDp + HMM | 78.76% | 90.70% | 69.50% | 88.07% |
| MinWordsDp + tagger fallback | 78.18% | 90.36% | 69.10% | 87.83% |
| UnigramDp + tagger fallback | 78.78% | 90.71% | 69.49% | 88.07% |
| Full Tagger | **95.07%** | **97.86%** | 63.59% | 85.70% |

The full Tagger's in-domain khPOS result is not transferable: it loses 6.56 percentage points against the current project engine on ALT Khmer-only word F1 and 2.82 points on ALT boundary F1. The HMM and tagger fallback configurations provide no material improvement over dictionary segmentation. The current project Viterbi remains the strongest measured baseline on both corpora. The full Tagger's high khPOS score is consistent with domain/annotation-convention dependence and is not evidence of target-profile accuracy.

### Updated task ledger

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-LEXICAL-WORD-SEGMENTATION-001 | BLOCKED | Human convention approval and independent lexical-boundary pilot still absent; corpus experiments above are external benchmark diagnostics only. | Approve a project-specific tokenization convention; complete rights/privacy review; obtain independent double annotation/adjudication and held-out evaluation before any project runtime segmentation feature. |
| KHM-LEXICAL-WORD-SEGMENTATION-002 | DONE_VERIFIED (research benchmark only) | Pinned Rust source, exact corpus/dictionary checksums, KCC integrity, OOV/normalization fixtures, khPOS and ALT metrics; PRs #544, #546, #547 merged; workflow [45253514986](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45253514986) SUCCESS. | Reproducible algorithm comparison only. Does not approve ALT/NOVA or khPOS labels as the project's gold or UI segmentation convention. |
| KHM-LEXICAL-WORD-SEGMENTATION-003 | NO ADOPTION / DEFERRED | External Rust dictionary algorithms and khPOS-trained tagger do not outperform current Viterbi on ALT; the tagger is licensed from CC BY-NC-SA training data and cross-corpus performance is poor. | Do not ship the Rust dependency or trained model. Reconsider only with rights-cleared, target-relevant data and independently adjudicated cross-corpus evidence. |

**No phonetic or IPA claim changed.** The segmentation benchmark is orthogonal to source-to-IPA-to-Ukrainian transcription. Independent expert-adjudicated IPA gold remains 0 and empirical pronunciation accuracy remains NOT_ASSESSED.
