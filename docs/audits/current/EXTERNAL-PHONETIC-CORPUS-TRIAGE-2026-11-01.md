# External phonetic corpus/source triage — Khmer — 2026-11-01

## Candidate: MekongPhon (LREC 2026)

**Disposition: high-priority research lead; NOT imported as gold or training data.** The paper reports 1.3 million Khmer orthography–IPA pairs and sub-2% CER on held-out data. These are paper-reported figures, not results independently reproduced by this repository.

- Paper: https://aclanthology.org/2026.lrec-1.129/
- Project: https://github.com/byu-matrix-lab/MekongPhon
- Inspected upstream main commit: `f80f6c1840c4818b51e05f2e00cded4701a5b662`.
- Files include `data/lexicons/khmer_lexicon.csv`, `data/splits/khmer_train.csv`, `data/splits/khmer_eval.csv`, and a 500-sentence qualitative sample.
- The project repository metadata has `license: null`; its tree has no LICENSE/COPYING file. The LREC proceedings page states CC BY-NC 4.0 for proceedings, but that does not automatically license the separate corpus, source lexicon, OPUS data or trained models.
- The documented pipeline scrapes the SEAlang Khmer dictionary (source filter `headley77`), downloads OPUS parallel text, and applies a greedy lexicon transliterator. Sentences with out-of-lexicon tokens are filtered out. Thus the sentence IPA is dictionary-generated, not an independently hand-transcribed sentence-level reference.
- The committed split script uses `random.seed(1234)` and reserves only 100 lexicon lines for evaluation. This is a held-out lexical split, not evidence of independent expert adjudication or robust dialect-balanced coverage.
- The paper's “verified” claim is worth investigating, but the accessible project README/pipeline does not document annotator identities, adjudication protocol, dialect stratification, or data licensing at the per-entry level.

## Candidate: Khmer Acoustic Model / Khmer IPA dictionary

- Repository: https://github.com/chemvatho/Khmer-acoustic-model
- Pinned upstream default-branch commit checked 2026-11-18: `2714994b41ccf875c5b6f6182b48a72f13632dbf` (the only listed branch is `main`; no releases are published).
- Root README claims 29,204 IPA dictionary entries validated by native Khmer linguists; its data-license subsection assigns **CC BY-SA 4.0** to the pronunciation dictionary and MIT to the acoustic model. The root `LICENSE` is MIT and should not be read as overriding that explicit dictionary-data statement.
- `dictionary/README.md` describes a G2P mapping derived from **33,091** dictionary entries and declares **CC BY 4.0** for that mapping. These are differently named/specified data objects; the public files do not establish whether the mapping is a distinct derivative dataset or a different license statement for the same underlying lexicon. Do not flatten this into a single license or choose one by assumption; request author clarification and artifact-specific terms.
- The recursive tree at the pinned commit contains only `dictionary/README.md` and `dictionary/khmer_ipa_sample.dict` in `dictionary/`; the sample is six lines (blob SHA `9dbd64d74194485fbfda69dce41b5129b5fbb8ab`, 144 bytes). There is no `khmer_ipa.dict`, no 29,204- or 33,091-row data artifact, and the releases endpoint is empty. The claimed full dictionary cannot be independently inspected, counted, or reproduced from this public revision.
- The root README also reports 137 hours of audio and alignment metrics, but alignment-boundary metrics are not pronunciation-accuracy metrics.

## Other candidate: Goruut

The source code is MIT, but the corresponding `neurlang/dataset/khmer/central/` lexicon has no declared repository license, and no per-language rights statement was found. Its derived model assets remain blocked pending provenance/license clarification. See `docs/audits/current/GORUUT-ASSET-LICENSE-REVIEW-2026-11-01.md`.

## Acceptance before use

1. Obtain explicit corpus/lexicon/model license terms and provenance for each component (SEAlang, OPUS corpora, dictionary data, derived IPA, model weights).
2. Obtain the MekongPhon paper and inspect annotation/verification protocol, Phnom Penh vs regional dialect profile, IPA conventions and held-out split design.
3. Resolve the Khmer Acoustic Model's CC BY 4.0 vs CC BY-SA 4.0 discrepancy and obtain the complete dictionary with a stable version/digest.
4. Establish whether the 100-word MekongPhon eval split is independently adjudicated; if not, keep it as a comparator split only.
5. Import no rows until each row has a stable source locator, profile, adjudication status and provenance; retain original IPA exactly.

Current independent, project-owned, expert-adjudicated Khmer gold remains 0. No MekongPhon/Goruut/Khmer-Acoustic-Model accuracy claim is added to this repository.


## Test-only Goruut runtime evaluation

Added an optional, test-only HTTP runtime probe for Goruut at pinned upstream commit `b224bde02151f8f86d0fe260804e4ca743bda620`. It explicitly enables `KhmerCentral` in `BuiltinDictLanguages`, builds the upstream Go binary and records raw JSON responses for source-attested lexical probes plus multiword/punctuation cases. `scripts/benchmark_goruut.py` records commit, language, input SHA-256, raw response, tokens and errors; it does not normalize or score IPA. Existing source-attested IPA remains non-gold. Accuracy=null; independent gold=0. Workflow: `.github/workflows/optional-goruut-runtime.yml`; artifact retention 30 days.

The earlier asset-license blocker applies to copying, redistribution and production integration. The owner has authorized use for testing only; therefore the optional CI probe may check out and execute the pinned upstream source transiently. It does not persist upstream assets, does not bundle them, and does not approve a production dependency. Linguistic gold and accuracy remain unestablished.


## Goruut runtime evidence update — 2026-11-01

The pinned Goruut runtime was executed with KhmerCentral enabled (Go 1.23.12). Engineering probes returned 8/8 responses; 6 source-attested IPA probes returned 6/6, but only 1/6 was an exact NFC/whitespace concordance (not accuracy/gold). Clear incomplete outputs: `ខ្មែរ` → `kʰr` vs source `kʰmae`; `ភ្នំពេញ` → `pʰɲ` vs `pʰnum ˈpɨɲ`; `ភាសាខ្មែរ` → `pʰiəsaːkʰr` vs `pʰiəsaː kʰmae`. Server log repeatedly reports missing `weights9.bin.zlib`. Do not promote. Full evidence: `docs/audits/current/GORUUT-RUNTIME-EVALUATION-2026-11-01.md`.

Testing-only owner authorization was used to execute the pinned upstream source in ephemeral CI. No external asset was copied into the repository or production artifact. Full report: `docs/audits/current/GORUUT-RUNTIME-EVALUATION-2026-11-01.md`.


## Repeatability findings — 2026-11-01

Three-repeat re-evaluation: 8/8 engineering outputs and 6/6 source-attested probe outputs were stable across repeats; only 1/6 source-attested IPA rows matched exactly. Stable but incomplete outputs include `ខ្មែរ` → `kʰr` vs `kʰmae` and `ភ្នំពេញ` → `pʰɲ` vs `pʰnum ˈpɨɲ`. Stable execution does not offset the phonetic mismatch. This is not accuracy or gold.

The three-repeat raw outputs are preserved in workflow artifacts and summarized in `docs/audits/current/GORUUT-RUNTIME-EVALUATION-2026-11-01.md`. Do not treat these results as gold or as a production approval.


## Cross-engine comparison update

Cross-engine check: khmerphonemizer 0.0.3 returned 6/6 source-attested probes; 2/6 strict IPA strings and 6/6 limited-notation matches. Goruut returned 6/6 stable outputs but only 1/6 strict and 3/6 limited-notation matches. This small source-attested sample favours khmerphonemizer as a comparator, not as proven production phonology. No independent gold exists.


## Candidate: Kirby 2015 Phnom Penh acoustic recordings and supplementary data

**Disposition: high-value, rights-documented acoustic research source; NOT imported as lexical IPA gold.**

- Audio item: https://datashare.ed.ac.uk/items/fe218489-ad49-4986-b175-721cb9959500; DOI 10.7488/ds/321. The DataShare full-item metadata declares CC BY 4.0. It contains 24-bit/44.1 kHz audio from 16 Phnom Penh Khmer speakers recorded in July 2011, with segmented Praat TextGrids. The provider lists a 461.93 MB ZIP and MD5 `8688e68e76e8269b8bbf5d19020a230b`; this checksum has not been independently recomputed because the archive was not downloaded.
- Supplementary item: https://datashare.ed.ac.uk/items/9a9fa51d-ce4f-4685-9e39-af3fd0a436d3; DOI 10.7488/ds/319. Its DataShare full-item metadata also declares CC BY 4.0 and lists anonymised production/perception CSVs, KlattGrid files, Praat-related measurements and R analysis code.
- The linked article (Kirby 2014, *Journal of Phonetics* 43:69–85) compares reading and colloquial Phnom Penh /CrV/ forms and examines VOT, f0, voice quality, vowel quality and /r/ realisation. It is a targeted study, not a full lexical pronunciation dictionary.
- Use reading-condition tokens only for a carefully scoped citation-style acoustic comparison; keep colloquial productions in a separate contextual set. Preserve speaker IDs, task, token, style, recording and TextGrid locators.
- TextGrids provide segmentation, not independent IPA; supplementary CSVs are measurements/response data, not an adjudicated IPA transcription. Do not promote them to gold without two independent IPA annotations and a separate adjudicator.
- The CC BY 4.0 statement is specific to the two DataShare dataset items. It does not license other third-party materials or source dictionaries cited by the article. Attribute Kirby and the University of Edinburgh when reusing the licensed items.

## Acceptance before any pilot use

1. Download only through the official DataShare item; verify the provider MD5 against the downloaded archive and retain the item DOI and file manifest.
2. Inspect the complete file inventory and map each audio/TextGrid to the paper's participant, lexical item, and reading/colloquial condition.
3. Confirm which tokens are suitable for the selected careful-citation profile; exclude colloquial repetitions from the citation-form benchmark.
4. Obtain two blind IPA annotations from qualified Khmer phoneticians and adjudicate disagreements independently. Preserve uncertainty and acoustic cues rather than inferring a single deterministic /r/-loss rewrite.
5. Keep this targeted /CrV/ acoustic subset separate from the full lexical G2P benchmark and from project gold until the normal rights/provenance gates pass.



## Follow-up verification — Khmer Acoustic Model dictionary claims (2026-11-04)

The upstream repository was rechecked directly at its current public default branch: https://github.com/chemvatho/Khmer-acoustic-model.

- The root README reports **29,204 dictionary entries** and says the pronunciation dictionary is **CC BY-SA 4.0**.
- The separately maintained `dictionary/README.md` describes a Khmer G2P mapping derived from a dictionary of **33,091 entries** and declares **CC BY 4.0** for that mapping.
- The current Git tree's `dictionary/` directory contains only `README.md` and a six-line `khmer_ipa_sample.dict`; there is no complete 29,204- or 33,091-entry dictionary in the visible tree, and the repository has no releases carrying one.
- The two README counts and the two data-license declarations are not reconciled by the visible repository. The dictionary README's aggregate grapheme counts also cannot be treated as validated per-entry IPA evidence. Alignment-boundary metrics are not pronunciation accuracy.

**Disposition remains BLOCKED for import or training.** Do not download/import the sample as a gold set, infer that MIT code licensing covers dictionary data, or select one of the two data licenses by assumption. Request from the authors: (1) the exact versioned full dictionary and SHA-256; (2) a single explicit license statement covering each artifact (dictionary, mapping, acoustic model, audio); (3) provenance and dialect/profile/convention; (4) annotation and adjudication protocol and the meaning of “validated by native linguists”; (5) a stable release or archival DOI. Until then this remains a high-value lead, not an approved corpus.

Evidence checked: upstream root README, `dictionary/README.md`, current Git tree and releases endpoint on 2026-11-04. This check does not establish that no private or externally hosted copy exists.


## Candidate audio source — Digital Divide Data Khmer ASR Cultural Dataset (2026-11-04)

The Mozilla Data Collective's Version 3 Part 1 listing reports **134.60 hours**, WAV audio, orthographic transcripts, **8 Cambodia-based native speakers (4 female, 4 male)**, 13 topics and 401 subtopics, with speaker origin-city metadata. It declares **CC BY-SA 4.0**, requires attribution to Digital Divide Data, and forbids attempts to identify speakers: https://mozilladatacollective.com/datasets/cmpdy0si400ldnu07rs6zwql4.

**Disposition: promising audio-backed annotation source, not IPA gold.** It can support a carefully profiled human pilot if speaker origin and actual pronunciation variety are checked; city metadata alone does not prove Phnom Penh speech. The recordings contain prompted cultural-topic sentences, not citation-form lexical items. Curators must select attested words, preserve exact utterance/audio/time-span locators and orthographic context, and keep word-span selection separate from IPA annotation. The CC BY-SA 4.0 share-alike implications for publishing derived IPA must be reviewed before release. Do not attempt speaker identification; do not mirror or redistribute audio outside the provider's terms.

The Part 1 listing's 134.60 hours and eight speakers must not be silently conflated with the broader Hugging Face dataset card's 727.94-hour / 12-speaker aggregate. Treat them as version-specific scopes until the provider's file manifests reconcile them. The corpus contains transcripts, not IPA, so it does not change independent gold=0 or accuracy=null.


## Candidate audio source — Common Voice 27.0 Khmer (2026-11-04)

The exact Mozilla Data Collective record is https://mozilladatacollective.com/datasets/cmu5olr5u00xzmh07pfgl3kuw. It declares **CC0-1.0**, while expressly prohibiting speaker identification and re-hosting/re-sharing. Its 2026-09-11 release has **739 clips / 0.98h total**, of which **213 clips / 0.28h are validated**, from 15 speakers; the text corpus has 4,971 sentences but only 364 validated sentences. 483 clips remain unresolved and 43 are invalidated. Accent is blank for the small reported subset; gender is unreported for all 15 speakers.

**Disposition: small secondary audio lead, not IPA gold.** It is not safe to assume Phnom Penh or Standard Khmer variety from the locale tag. Use only provider-hosted audio and opaque clip/time locators; do not mirror, re-share or attempt speaker identification. Curators must screen only validated clips, determine whether the speaker profile fits the selected project variety, and select attested word spans with exact time ranges. Because the validated audio totals only 0.28h and demographic/variety metadata is sparse, this is not a stand-alone benchmark source.

This is separate from DDD's larger CC BY-SA 4.0 corpus and its own share-alike requirements. The two datasets must not be conflated. Neither source supplies IPA labels; independent gold remains 0.


## Additional Khmer pronunciation resources discovered — 2026-11-04

### Candidate: open-dict-data/ipa-dict Khmer lexicon

**Disposition: useful external phonemic comparator; non-commercial rights; NOT project gold and NOT approved for import.**

- Repository: https://github.com/open-dict-data/ipa-dict
- Pinned upstream revision inspected: `972cd67dd5f96bc5660e28070cde26e3928abcd7` (2026-10-22).
- Khmer file: https://github.com/open-dict-data/ipa-dict/blob/972cd67dd5f96bc5660e28070cde26e3928abcd7/data/km.txt
- The file has 3,286 lines of Khmer orthography-to-IPA entries. The upstream README explicitly says the Khmer data were extracted from the Khmer-English Dictionary at aakanee.com and assigns that third-party data **CC BY-NC-SA 4.0**. The repository's general MIT license does not supersede the source-specific license.
- This is the most directly relevant new lexical IPA comparator found in this pass. It is still not an independent project gold set: the upstream README does not provide per-entry source locators, dialect metadata, annotator identities, adjudication records or an IPA convention profile for Khmer.
- Some entries have multiple slash-delimited alternatives and repeated orthographies; the project must preserve alternatives and inspect normalization/duplicates rather than collapse them silently.

**Acceptance before any use:** review whether non-commercial/share-alike terms are compatible with the intended research and eventual distribution; preserve upstream commit and file hash; inspect IPA symbols and profile; map entries to stable source locators; select a small stratified pilot for two blind Khmer-phonetician annotations and independent adjudication. Do not add its IPA to `gold.tsv` or use it for commercial release without permission/legal review.

### Candidate: PhonSobon Khmer G2P / Khmer pronunciation dictionary

- G2P dataset: https://huggingface.co/datasets/phonsobon/khmer-G2P
- Combined dictionary: https://huggingface.co/datasets/phonsobon/khmer-pronunciation-dictionary
- The G2P card reports **38,629 word–pronunciation pairs / 37,755 unique words**, split by word into 34,770 train, 1,939 validation and 1,920 test rows. The pronunciation field is Khmer-script respelling with syllable separators, **not IPA**. The source is the 2022 Khmer Dictionary of the National Council of Khmer Language (NCKL), Royal Academy of Cambodia.
- The combined dictionary reports 39,110 rows and describes 689 disputed words: 650 judge decisions and 39 Claude-assisted confirmations that the dataset author says should be confirmed by a native speaker.
- These are valuable orthographic/syllabification comparators and possible sources for word-list discovery. They do not close the IPA evidence gap. The dataset cards say NCKL retains rights and direct users to check terms, including before commercial use; no blanket redistribution permission for this project is established.

**Disposition:** no import into the IPA gold corpus. Consider only a separate, rights-cleared orthographic-respelling benchmark or candidate-list generator. Keep the original spelling, respelling, alternatives, split provenance and cleaning history distinct from IPA.

### Recheck: Chem Vatho et al. Khmer Acoustic Model

- Current public upstream main inspected at commit `2714994b41ccf875c5b6f6182b48a72f13632dbf`.
- Root README claims 29,204 IPA dictionary entries validated by native Khmer linguists and declares the pronunciation dictionary CC BY-SA 4.0.
- The visible repository tree contains only `dictionary/khmer_ipa_sample.dict` (six lines), not the claimed complete dictionary. The separate `dictionary/README.md` describes a 33,091-entry G2P mapping and declares CC BY 4.0. The artifact count and data-license statements remain inconsistent.
- The repository's MIT code license does not resolve the separate data terms. A README assertion is not a substitute for access to the actual versioned dictionary, digest, provenance and artifact-specific license.

**Disposition remains BLOCKED for import.** Request the full dictionary, SHA-256, artifact-specific rights statement, provenance, dialect/IPA convention, and details of the claimed native-speaker validation and adjudication.

### Current evidence decision

| Resource | Useful as | Rights / format | Gold status |
|---|---|---|---|
| ipa-dict Khmer | External lexical IPA comparator | CC BY-NC-SA 4.0 source data; exact profile and annotation protocol not established | NOT GOLD |
| PhonSobon Khmer G2P | Orthographic respelling / syllabification comparator | NCKL source rights; Khmer-script respelling, not IPA | NOT IPA GOLD |
| PhonSobon combined dictionary | Candidate lexical list and alternate-reading discovery | Research/non-commercial source constraints; some decisions need native confirmation | NOT GOLD |
| Khmer Acoustic Model | Potential IPA dictionary and audio-model lead | Full dictionary unavailable in visible tree; CC BY 4.0 vs CC BY-SA 4.0 conflict | BLOCKED |

The four records are now in `data/khmer/sources.json` with explicit scope, source revision where available, format and rights status. No external rows were copied into project data. Independent expert-adjudicated Khmer IPA gold remains **0**; empirical accuracy remains **null**.

## Auxiliary NCKL respelling and blocked IPA lexicon candidates — 2026-11-15

### PhonSobon Khmer G2P

The [model card](https://huggingface.co/phonsobon/khmer-g2p) describes a 7.46M-parameter character-level Transformer that predicts NCKL Khmer-script respelling with hyphenated syllable boundaries. Its reported 83.37% validation word accuracy at epoch 150 is an upstream validation claim; no test score is reported there and it has not been reproduced by this project.

The associated [dataset card](https://huggingface.co/datasets/phonsobon/khmer-G2P) reports 38,629 word–respelling pairs / 37,755 unique words, split 34,770 / 1,939 / 1,920. It derives from the Khmer Dictionary 2022 of the National Council of Khmer Language (NCKL), Royal Academy of Cambodia. The dataset card identifies the terms as `nckl-khmer-dictionary-2022`, requests NCKL attribution and says to check NCKL terms before commercial use.

**Disposition: AUXILIARY RESPELLING / SYLLABIFICATION ONLY — NOT IPA, NOT PHONETIC GOLD.** The output is Khmer-script respelling, not IPA. It must not be substituted into the IPA-first runtime or used as a phonetic benchmark. No dataset rows or model weights are copied. Redistribution and commercial/derivative use remain blocked pending authoritative NCKL terms.

### Khmer Acoustic Model pronunciation dictionary

The pinned upstream review reports conflicting dictionary counts and data-license declarations: root README says 29,204 entries and CC BY-SA 4.0, while `dictionary/README.md` says 33,091 entries and CC BY 4.0. The inspected tree at `2714994b41ccf875c5b6f6182b48a72f13632dbf` contains only `dictionary/khmer_ipa_sample.dict` (144 bytes), not the advertised full dictionary. Published MAE/F1 values are forced-alignment metrics, not G2P or transcription accuracy.

**Disposition: BLOCKED.** Do not ingest or redistribute the sample as a complete lexicon. Require the complete versioned dictionary and digest, reconciled counts, item-level provenance, dialect/IPA convention and an authoritative data-license statement. The registry now preserves this conflict rather than presenting CC BY-SA 4.0 as settled.

No source rows were added to project data. Independent adjudicated Phnom Penh IPA gold remains 0; empirical accuracy remains null.

## Google Language Resources and OpenSLR42 reconciliation — 2026-11-15

### Google Language Resources Khmer lexicon and phonology

The archived [Google Language Resources repository](https://github.com/google/language-resources/tree/a90601024f07ab7e96c911243324e0adeb16da96/km) contains a Khmer TTS lexicon and a feature-annotated phonology JSON. The pinned files are `km/data/lexicon.tsv` (2,845,315 bytes; blob `d399efeca642b1185786b2982374488c525e37c4`) and `km/festvox/phonology.json` (6,707 bytes; blob `8fb697ff66b09ef0c2a17f17b35600af410a92a9`). The JSON describes a feature inventory with length labels such as doubled vowels; it is not a self-sufficient declaration of the project's standard IPA convention.

A bounded extraction of the large lexicon previously found Latin-script spelling keys and custom phonemic sequences in the inspected subset. The full 2.8 MB file was not inspected, so this does not prove that every row is Latin-script. The repository root says Apache-2.0 applies unless otherwise noted and some datasets are CC BY 4.0; the Khmer-specific rights for these exact files remain to be verified.

**Disposition: PARTIAL FORMAT REVIEW / NOT APPROVED FOR KHMER-SCRIPT G2P.** Do not treat the paper's lexicon-size claim as a count of Khmer-script word–IPA pairs. Reconsider only after a full script/format audit, exact data-rights review and dialect/phone-convention reconciliation.

Primary references: [Sodimana et al. 2018](https://www.isca-archive.org/sltu_2018/sodimana18_sltu.html); [archived Google repository](https://github.com/google/language-resources).

### OpenSLR SLR42 Khmer speech corpus

The [current OpenSLR SLR42 page](https://openslr.org/42/) lists a single 866 MB archive, `km_kh_male.zip`, and identifies it as male-speaker Khmer speech. It declares CC BY-SA 4.0 and describes audio plus a TSV transcription index. In contrast, Table 1 of the [2018 source paper](https://www.isca-archive.org/sltu_2018/sodimana18_sltu.pdf) reports 17 female speakers, 2,906 files and 3:58:00 for Khmer.

**Disposition: SUPPORTING AUDIO ONLY / METADATA DISCREPANCY.** The currently listed male archive must not be assumed to be the same speaker set as the paper's female-speaker table. The resource has text transcripts, not IPA labels or independent phonetic gold. Before annotation, obtain the archive manifest and checksum, inspect speaker IDs, reconcile the paper/page mismatch, and verify the archive's included license. No audio was downloaded or imported in this continuation.

No external audio or lexicon rows were copied. Independent adjudicated Phnom Penh IPA gold remains 0; accuracy remains null.


## Pinned upstream artifact recheck — 2026-11-18

The GitHub API tree, root README, dictionary README, root LICENSE, sample dictionary, releases endpoint and commit history were inspected at upstream main `2714994b41ccf875c5b6f6182b48a72f13632dbf`. The full dictionary remains unavailable in the public tree; the two README counts (29,204 vs. 33,091) and differently scoped data-license statements (dictionary CC BY-SA 4.0 vs. G2P mapping CC BY 4.0) remain unresolved. The six-line sample is not a gold corpus and was not copied. The external source remains candidate-only / BLOCKED for import or training pending exact full artifact, SHA-256, source provenance, profile/convention, artifact-specific rights and author clarification.
