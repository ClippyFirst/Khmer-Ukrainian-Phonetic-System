# Controlled IPA gold acquisition — Khmer

**Status:** protocol ready for a human pilot; this document admits no gold labels.  
**Scope:** a controlled Khmer pilot followed by a versioned, independently adjudicated benchmark.

## Evidence boundary

A pronunciation from this repository, G2P, romanizer, dictionary, language model, or annotator memory is not gold merely because it is plausible. Keep source evidence, expert judgments, and engine predictions separate. Never seed an annotation with model output or infer complete IPA from spelling alone.

Choose one target profile before sampling. Recommended initial profile: contemporary Phnom Penh Khmer, careful citation forms, with one approved broad-phonemic or broad-phonetic convention. Do not merge regional, rural, diaspora, or colloquial variants into one undifferentiated score.

## Roles and blindness

1. **Curator:** selects lexemes, checks sources/rights, assigns opaque IDs, prepares packets; does not annotate.
2. **Annotators A and B:** independently transcribe identical packets. They see orthography, disambiguating gloss/context, target variety, and source/audio evidence, but never each other's work or engine predictions.
3. **Adjudicator C:** receives both locked submissions only after both arrive; cannot be A or B; records decision and rationale.
4. **Release maintainer:** validates provenance, rights, schema, split integrity, and export.

Use stable pseudonymous IDs in Git. Keep identity mappings and contact details outside the repository. Never place private audio or personal data in public issues or PRs.

## Pilot sampling

Start with **30 lexeme groups** as a process pilot, not an accuracy benchmark. Select attested items to cover, where supported by the chosen profile and sources:

- first/second consonant series and vowel contrasts they condition;
- short/long vowels, diphthongs, and offglides;
- open vs closed syllables and coda classes;
- stress/prominence and mono- vs disyllabic forms;
- onset /r/ environments, with conservative and documented Phnom Penh variants separately profiled;
- NIKAHIT/REAHMUK contexts that may affect nucleus and coda;
- source disagreements and cases marked uncertain by the engine.

Do not generate a theoretical Cartesian product. Every item must be an attested lexeme with an exact source locator. Record selection rationale and uncovered cells. Keep pilot items out of held-out evaluation if used to revise the engine.

## Khmer convention sheet

A source-grounded **expert-review draft** now exists at [docs/ipa-gold/khmer-pph-careful-citation-ipa-v1-draft.md](ipa-gold/khmer-pph-careful-citation-ipa-v1-draft.md). It proposes a single `PHONETIC_BROAD` annotation kind and conservative handling of series, vowels, length, diphthongs, codas, stress, F0, phonation and /r/-loss. Its status is `DRAFT_NOT_APPROVED`; it is not permission to start annotation. A qualified Khmer phonetician/phonologist must approve or replace the proposal, a second reviewer should challenge it, and the version/sign-off evidence must be recorded before any gold collection.

The draft synthesizes Minegishi (1985), Chem (2020), Kirby (2014/2015), Mam et al. (2025), and the limitations of Sodimana et al. (2018). Minegishi gives a systematic but partial account of series-conditioned vowel readings and coda effects, while distinguishing formal/school from colloquial Phnom Penh outcomes: https://doi.org/10.11435/GENGO1939.1985.88_41. Chem's final acoustic sample comprises four selected Phnom Penh speakers and formal frame reading; it measures F1/F2 and duration, not F0 or stress, and does not provide a complete IPA policy: https://doi.org/10.61945/cjbar.2020.2.2.3. Mam et al. compare PPK and Standard Khmer with five Greater Phnom Penh speakers and report possible F0 phonologization in a bounded cluster/disyllable task, not a general citation-form tone rule: https://doi.org/10.21437/TAI.2025-29. Kirby (2014) documents multiple cues associated with colloquial /r/-loss; do not reduce them to one spelling-based replacement: https://doi.org/10.1016/j.wocn.2014.02.001.

The draft explicitly keeps all unsupported values unresolved. It does not define a complete phoneme table and must not be treated as approved merely because it is versioned or committed.

## Candidate external references — do not auto-import

### MekongPhon

MekongPhon (Shurtz et al., LREC 2026) reports 1,314,779 Khmer and 367,388 Lao orthography–IPA sentence pairs (DOI https://doi.org/10.63317/4bb9rvdshu4z; paper: https://aclanthology.org/2026.lrec-1.129.pdf). The Khmer seed lexicon contains 8,026 word–IPA pairs derived from Headley (1977), hosted through SEALang. Two authors manually reviewed a 500-entry sample; they report 4/500 inaccurate (99.2% sample accuracy) and explicitly note that both reviewers are highly proficient second-language speakers, not native speakers. The paper does not establish that the full lexicon is consistently scoped to our proposed Phnom Penh citation-form profile.

**Evidence classification:** useful secondary lexical reference and external G2P diagnostic candidate; **not independent sentence-level pronunciation gold**. The sentence corpus is generated by longest-match-first trie lookup over the seed lexicon and OPUS text (NLLB, Paracrawl, OpenSubtitles), not by independent transcription of the sentences. The paper's held-out test construction uses 100 lexicon entries held out from training, then generates evaluation sentences using the complete lexicon; this is a dictionary-seeded G2P evaluation, not a blind expert-adjudicated pronunciation benchmark for our project. Treat the seed entries as source-attested dictionary IPA requiring profile/convention comparison, not as a substitute for two independent annotators and an adjudicator.

Repository snapshot inspected: https://github.com/byu-matrix-lab/MekongPhon/tree/f80f6c1840c4818b51e05f2e00cded4701a5b662. The repository metadata declares no license (license: null) and has no root LICENSE file. The paper reports that the SEALang homepage describes reuse under a “Creative Commons open license”, but does not identify a version in the cited footnote. This is insufficient to infer rights for redistribution or derivative labels. Keep rights_status=UNKNOWN until the exact source and dataset rights are verified. The LREC proceedings license does not establish the dataset's own license. Do not populate records.jsonl or gold.tsv from MekongPhon without item-level source/profile/rights review.

### Khmer Acoustic Model dictionary

https://github.com/chemvatho/Khmer-acoustic-model reports a 29,204-entry IPA dictionary and native-linguist validation; its README states that dictionary data are CC BY-SA 4.0, distinct from the MIT code/model license. This is promising for external comparison and source discovery, not automatically our gold. Inspect actual dictionary, metadata, exact commit, per-entry provenance, variety/profile, transcription consistency, and rights before using any entry. Do not copy entries just because the repository is public.

## Agreement and reliability reporting

The validator's `AGREEMENT` decision means exact equality of the complete typed IPA object under the corpus's canonical NFC representation, including IPA kind and any supplied syllable-boundary, tone, vowel-length and phonation metadata. It is a strict record-level gate, **not** an inter-annotator reliability coefficient. The current implementation does not calculate an alignment-aware or feature-weighted agreement score.

For the 30-lexeme process pilot, report the exact-object agreement numerator/denominator, counts of `RESOLVED` and `UNRESOLVED` decisions, and a descriptive breakdown of disagreements (segment identity, feature/series, vowel quality/length, coda, syllable boundary, tone, phonation and profile/style). Do not present this small process sample as a stable population reliability estimate.

Cucchiarini (1996) explains why raw percentage agreement is limited for phonetic transcription: it treats symbol matches as all-or-none, is affected by chance agreement, and does not itself specify transcription alignment. Oller and Ramsdell (2006) describe a weighted reliability measure intended to distinguish degrees of phonetic difference. These works motivate careful alignment and feature-sensitive reporting, but the repository does **not** implement either published algorithm. A future project-defined weighted metric remains PARTIAL until experts pre-register the segment/feature inventory, alignment procedure, substitution/deletion/insertion costs, suprasegmental weights (tone, length, phonation), syllable-boundary treatment, uncertainty/alternative policy, and validation against independently adjudicated data. Do not call a future score the Cucchiarini or Oller–Ramsdell measure unless their exact method is reproduced.

## Controlled workflow

1. Curator freezes the pilot list and records source provenance and rights before annotation.
2. Curator generates opaque IDs and two separate packets with identical evidence and conventions, excluding model output and competing IPA.
3. A and B submit separately. Curator timestamps and locks both before either sees the other.
4. C reviews both locked submissions and source packet. C records AGREEMENT, RESOLVED, or UNRESOLVED. RESOLVED requires final IPA and written evidence-based rationale; do not force agreement.
5. Curator validates schema, cross-file links, duplicates, rights, and blindness checklist. Unresolved items remain outside gold.
6. Export only rights-cleared adjudicated items. Keep restricted source material external; store exact locators/checksums where permitted.
7. Freeze a versioned manifest before benchmarking.

## Annotation packet

Include opaque record ID; target profile; orthography and NFC form; gloss/minimal context; source title/provider/version/page/entry/audio locator; rights evidence; lawful audio access and recording context; pseudonymous speaker ID; IPA kind and convention-sheet version; literal IPA, syllable boundaries, tone if relevant, length, phonation, confidence, uncertainty, and comments.

## Acceptance gates

- **Pilot can start:** variety and convention sheet approved; two qualified annotators and independent adjudicator confirmed; rights-cleared packets ready; blind intake dry-run passed.
- **Pilot accepted:** 30 items have two independent submissions; all disagreements adjudicated or explicitly unresolved; provenance/rights complete; blindness evidenced; validation passes.
- **Benchmark-ready:** expanded stratified corpus; frozen train/dev/test manifest; no lexeme leakage; held-out test untouched during tuning; coverage report for series × vowel × stress × coda, with /r/-loss variants separately profiled; rights and reproducibility review passed.

Existing numeric thresholds (100 train / 25 dev / 25 test) are minimum engineering gates, not a statistical sufficiency guarantee. Coverage and independent review remain mandatory.

## Current blockers — revalidated 2026-11-18

- **BLOCKED — convention approval:** the `khmer-pph-careful-citation-v1` convention remains `DRAFT_NOT_APPROVED`. A qualified Khmer phonetician must approve or replace the draft, and an independent reviewer must challenge the scoped acoustic/phonological decisions before annotation starts.
- **BLOCKED — people and role independence:** no candidate has been contacted or confirmed. Two qualified annotators, a distinct adjudicator and a non-annotating curator remain unappointed. Candidate biographies are not recruitment evidence.
- **BLOCKED — private blind intake:** no operational channel or dry-run evidence is recorded. A and B must submit independently and be locked before either submission is exposed to the other or to C.
- **BLOCKED — rights-cleared items:** candidate dictionaries and external audio remain excluded until exact item locators, source terms, rights and permitted uses are verified. MekongPhon and the Khmer Acoustic Model remain candidate-only.
- **BLOCKED — Khmer Acoustic Model artifact:** the inspected default branch did not expose the full dictionary at its documented path; only a small sample was available, and README entry-count/license claims conflict. Obtain the exact artifact, checksum, version, per-entry provenance and written maintainer clarification before considering any row.
- **BLOCKED — 30-item pilot:** no source-rights-cleared list has been approved; no records, annotations, adjudications or gold rows may be created until the preceding gates pass.

The 2026-11-17 expert shortlist revalidation improves candidate-role evidence but records no contact, consent, appointment or approval. The next executable step is human outreach using the templates below; do not mark a gate complete until written acceptance and role/qualification checks are recorded.

## References

- Shurtz, Richardson & Richardson (2026), MekongPhon, LREC 2026: https://lrec.elra.info/lrec2026-main-129
- Khmer Acoustic Model upstream technical repository (not a scholarly 2026 article): https://github.com/chemvatho/Khmer-acoustic-model
- Chem (2020), The Standard Khmer vowel system: https://www.cjbar.rupp.edu.kh/index.php/cjbar/article/view/36
- Kirby (2014), Incipient tonogenesis in Phnom Penh Khmer: https://www.sciencedirect.com/science/article/pii/S0095447014000163


## External IPA resources — repository inspection, 2026-11-01

MekongPhon source repository: https://github.com/byu-matrix-lab/MekongPhon. Its README describes data/ as lexicons, OPUS downloads, sampled sentences and splits. pipeline/README.md describes SEAlang frequency lists → IPA scraping → minor lexicon post-processing → OPUS sentence download → lexicon train/eval split → trie-based lexicon lookup to convert sentences, filtering out-of-lexicon sentences. Therefore its sentence IPA is generated through a word-lexicon lookup pipeline and should not be presumed independent sentence-level phonetic transcription. The root LICENSE path was not present in the inspected repository. No dataset-specific redistribution license was verified. The LREC proceedings CC BY-NC-4.0 notice and the paper's “verified” description do not establish data reuse rights or item-level human adjudication. Do not import/redistribute until exact files, variety, IPA convention, correction/verification process, source terms, split construction and license are verified with the maintainers.

Separate candidate: https://github.com/chemvatho/Khmer-acoustic-model reports a 29,204-entry IPA dictionary and says dictionary data are CC BY-SA 4.0, distinct from the MIT code/model. Its README claims validation by native Khmer linguists, but per-entry source provenance, dialect/profile, transcription conventions and exact release must still be audited. Treat as an external comparator/source-discovery lead, not our gold.


## Audio-source shortlist — reviewed 2026-11-01

These are **audio/transcript candidates**, not IPA gold. Sentence-level recordings provide contextual tokens, not automatically citation-form lexical pronunciations. Keep contextual phonetic evaluation separate from the lexical G2P benchmark.

### Common Voice Scripted Speech 27.0 — Khmer

- Official catalog: https://commonvoice.allizom.org/en/datasets (catalog lists “Common Voice Scripted Speech 27.0 - Khmer”, locale `km`, CC0-1.0, MP3, 20.23 MB).
- Dataset/version documentation: https://github.com/common-voice/cv-dataset/tree/main/datasets/scripted-speech. Scripted Speech consists of contributors reading pre-written sentences, with community validation; the current v27.0 release history is dated 2026-09-11.
- The 20.23 MB value is archive size, not a clip/speaker count. Inspect the v27.0 manifest for validated clips, speaker counts, region metadata and transcript coverage before choosing items.
- No IPA labels are supplied. Do not infer Phnom Penh variety or the first/second-series distribution from the locale label alone.

### OpenSLR 42 — Khmer multi-speaker TTS audio

- Official resource page: https://openslr.org/42 (SLR42). The current page lists only `km_kh_male.zip` (866 MB), explicitly described as male-speaker audio, with WAV files and a TSV line index whose filenames contain speaker IDs. The page says the data were manually quality-checked but may still contain errors.
- Metadata conflict: Sodimana et al. (2018), Table 1, reports 17 **female** speakers, 2,906 audio files and 3:58:00 for Khmer at this same SLR42 URL. The current provider page describes a male archive. Do not assume the current archive is the same speaker set or version as the paper; exact manifest, checksum and speaker IDs need reconciliation.
- Independent repository snapshot check: the pinned Google Language Resources Festival prompt file `km/festvox/txt.done.data` (blob `01ca58b32544bcfd44305b91931baf192cce287d`) contains 2,748 utterance rows across 16 pseudonymous speaker-ID prefixes, with no gender labels. It is not a checksum-backed audio manifest and does not reconcile the paper's 2,906/17 figures or the current male archive.
- Rights conflict: the current OpenSLR page and its linked `LICENSE` file declare CC BY-SA 4.0. The 2018 paper says all data were CC BY 4.0 unless otherwise noted. Treat the current provider's archive-specific CC BY-SA 4.0 declaration as controlling for the currently listed archive pending clarification of historical versions. The linked license was inspected; the 866 MB archive's internal license copy was not downloaded.
- This is a supplementary contextual-audio source, not IPA gold. Preserve speaker IDs as pseudonymous source identifiers; do not treat transcript text or aligner output as phonetic gold. The audio is not a balanced sample for the paper's reported female profile, and neither the current archive nor the paper establishes a Phnom Penh careful-citation profile.

### Google Language Resources — Khmer TTS lexicon and phonology inventory

- Pinned archived source: https://github.com/google/language-resources/tree/a90601024f07ab7e96c911243324e0adeb16da96/km. The repository was archived in 2022. The 2018 paper is Sodimana et al., *A Step-by-Step Process for Building TTS Voices Using Open Source Data and Frameworks for Bangla, Javanese, Khmer, Nepali, Sinhala, and Sundanese*, DOI https://doi.org/10.21437/SLTU.2018-14; full paper: https://storage.googleapis.com/gweb-research2023-media/pubtools/4708.pdf.
- Full-file audit of `km/data/lexicon.tsv` (blob `d399efeca642b1185786b2982374488c525e37c4`; 2.71 MB): **69,415 rows**, **69,405 unique spellings**; 62,179 rows use Khmer script and 7,236 use Latin script (62,175 and 7,230 unique keys respectively). Ten spelling keys each occur twice with divergent pronunciations. The header describes an optional third disambiguating column, but all actual rows have only two columns; preserve the duplicate readings as alternatives rather than deduplicating them.
- The lexicon uses **54 distinct phonemic tokens**, all present in `km/festvox/phonology.json` (blob `8fb697ff66b09ef0c2a17f17b35600af410a92a9`), which contains 56 phone entries (30 vowels, 24 consonants, 2 silence phones; the silence labels are unused in the lexicon). The notation is a project-specific phonemic inventory, including ASCII digraphs and doubled-vowel length labels, not a documented strict IPA convention. The paper reports 70,671 Khmer lexicon entries, 1,256 more than this archived snapshot.
- The paper says lexicon words were crawled from Wikipedia and websites, frequency-ranked, manually transcribed by linguists using guidelines and quality-checked. It does not give the Khmer-specific guideline, annotator count, target variety, per-entry source locators or error rate. The lexicon therefore provides candidate Khmer-script lexical coverage and a phonemic comparator, not independently verified Phnom Penh citation-form IPA gold.
- Rights are file-specific: `km/data/lexicon.tsv` has a file-level CC BY 4.0 header. The companion `phonology.json` has no file-level license header; the repository README says original files are Apache-2.0 unless otherwise noted, while the paper broadly says all data are CC BY 4.0 unless otherwise noted. Keep the companion JSON's exact license scope unresolved until clarified. Attribute the lexicon and indicate changes if any permitted subset is redistributed.
- Decision: candidate lexical/phonemic comparator only. Do not use its pronunciations as project gold or infer the target profile; do not import the full dataset into the project until the 70,671-vs-69,415 version discrepancy, duplicate-key semantics, exact profile/convention, per-entry provenance and companion-file rights are resolved.

### Khmer Acoustic Model dictionary — exact artifact check

- Upstream: https://github.com/chemvatho/Khmer-acoustic-model.
- Its README claims 29,204 IPA dictionary entries and says native Khmer linguists validated them; it states the dictionary data are CC BY-SA 4.0, distinct from the MIT code/acoustic model.
- At the inspected default-branch tree, `dictionary/khmer_ipa.dict` returned 404; only `dictionary/khmer_ipa_sample.dict` was retrievable, containing six entries. Therefore the full 29,204-entry artifact is **not reproducibly available at the documented path in the inspected branch**.
- The six-row sample uses space-separated symbol sequences (for example, `p r a p`), not the project's current typed IPA object contract. The README does not establish the target variety, per-entry source locators, or a complete phonemic/broad/narrow convention. Treat it as a methodology/comparison lead only, not gold.

### Kirby 2015 — Phnom Penh acoustic recordings and supplementary data

- Audio item: https://datashare.ed.ac.uk/items/fe218489-ad49-4986-b175-721cb9959500 (DOI 10.7488/ds/321). DataShare item metadata declares **CC BY 4.0**. The archive is 461.93 MB and contains 24-bit, 44.1 kHz recordings of 16 Phnom Penh Khmer speakers from July 2011, with segmented Praat TextGrids; the provider lists MD5 `8688e68e76e8269b8bbf5d19020a230b`.
- Supplementary item: https://datashare.ed.ac.uk/items/9a9fa51d-ce4f-4685-9e39-af3fd0a436d3 (DOI 10.7488/ds/319), also declared CC BY 4.0. It contains anonymised production/perception CSVs, KlattGrid stimulus files, Praat-related measurements and R analysis code.
- Research fit: this is a valuable acoustic source for the Phnom Penh /CrV/ reading-versus-colloquial contrast and speaker-level variability. For a careful-citation pilot, isolate the reading condition and preserve the original task/style metadata; keep colloquial productions in a separate contextual dataset.
- Limits: this is not a lexical-wide IPA corpus. Praat TextGrids are segmentation, not IPA labels; the CSVs are study measurements/response data, not independent double-annotated IPA. The study's /CrV/ focus does not establish the complete vowel × series × coda × profile matrix or the pronunciation of the full lexicon. Do not convert acoustic measurements or model output into gold without two independent IPA transcriptions and adjudication.
- Rights are item-specific: the DataShare records declare CC BY 4.0 for these two dataset items. Attribute Kirby and the University of Edinburgh; do not infer rights for any other source cited by the article or for third-party material not covered by the item licence.

### Collection decision

For a Phnom Penh lexical G2P benchmark, prioritize controlled citation-form recordings from confirmed Phnom Penh speakers and two blind expert transcriptions. Kirby's DataShare recordings are the strongest located acoustic lead for Phnom Penh /CrV/ style comparison; Common Voice and OpenSLR42 can supply supplementary contextual speech and candidate words. Do not combine reading and colloquial realizations or contextual speech with citation-form labels. The Khmer Acoustic Model dictionary remains a comparator candidate until the full artifact, source provenance and IPA convention can be inspected.


### Exact v27.0 manifest audit

The official Common Voice release manifest has now been inspected: [`cv-corpus-27.0-2026-09-11.json`](https://github.com/common-voice/cv-dataset/blob/main/datasets/scripted-speech/cv-corpus-27.0-2026-09-11.json).

- Khmer locale entry: **739 clips**, **213 validated clips**, **15 contributor/user IDs**, **0.28 validated hours** (0.98 total hours).
- The accent dimension contains no named accent category; the variant dimension is empty. Gender metadata is entirely unspecified in this locale entry.
- Manifest locale checksum field: `d1c4bb041744fefb1fa60397217b7cd79bfa2ade4510b11ff9863e9a0dc0392d`. Manifest file blob SHA: `e401c4a8e923cad5c8baacb6120c095b1e1bd561`.

This is a very small and demographically under-described sample. It may be sufficient to test a 30-token annotation workflow if the validated transcripts contain the required lexical contrasts, but it cannot establish Phnom Penh variety, first/second-series coverage, or speaker-balanced generalization. Specialist profile approval and controlled citation-form recordings remain necessary.



## Recruitment and source leads — reviewed 2026-11-03

These are prospective leads only. No person has been contacted, consented, recruited, or approved as annotator/adjudicator. Publication authorship does not establish availability, independence, or suitability for every annotation role.

### Prospective linguistic reviewer

- Vatho Chem (Royal University of Phnom Penh / Institute of Foreign Languages): the 2020 Phnom Penh Khmer vowel-system acoustic study identifies the author as a lecturer at the Institute of Foreign Languages, Royal University of Phnom Penh, and provides a research contact. The 2026 Khmer acoustic-model project also identifies the author as its maintainer and reports a native-linguist validation process. This is a strong prospective reviewer/source-maintainer lead for the vowel and acoustic evidence, not proof that the full dictionary is independently adjudicated IPA gold or that the author is available to participate. Study: https://www.cjbar.rupp.edu.kh/index.php/cjbar/article/view/36 ; acoustic-model repository: https://github.com/chemvatho/Khmer-acoustic-model

### Newly identified pronunciation resource — restricted candidate, not IPA gold

- The Hugging Face phonsobon/khmer-G2P card describes 38,629 Khmer word-to-pronunciation pairs (37,755 unique words), derived from the National Council of Khmer Language (NCKL) Khmer Dictionary 2022. The pronunciations are Khmer-script respellings with syllable boundaries, not IPA. The card explicitly limits the profile to prescribed Standard/Phnom Penh dictionary pronunciations, lists known source/extraction errors, and says to credit NCKL and check NCKL terms before commercial use. It is useful as a candidate lexeme/source locator and orthographic-pronunciation comparator only, not as IPA gold, not as proof of spontaneous/citation phonetic realization, and not automatically redistributable for this project. https://huggingface.co/datasets/phonsobon/khmer-G2P
- The related dictionary card states that rights in the dictionary content remain with NCKL and asks users to check NCKL terms before commercial use or redistribution. Do not assume the Hugging Face card's metadata label grants a project-wide redistribution right: https://huggingface.co/datasets/phonsobon/khmer-dictionary
- kheng.info reports an online Khmer audio dictionary with over 3,000 recordings, but the reviewed about page does not establish dataset licensing, item-level source rights, target speaker profile, or permission to download/reuse audio. Treat it as a discovery/elicitation lead only: https://kheng.info/about/

### Existing stronger audio lead retained

Kirby's Edinburgh DataShare items (DOIs 10.7488/ds/321 and 10.7488/ds/319) remain the strongest rights-declared Phnom Penh acoustic-study materials identified in this playbook. The CC BY 4.0 item metadata does not turn Praat TextGrids or measurements into IPA labels; use only the reading/citation condition relevant to the target profile and retain source task metadata.

### Immediate unblock sequence

1. Invite a prospective reviewer to review a draft versioned convention sheet covering series/register, vowel quality/length, diphthongs, coda, stress, /r/-loss variants and uncertainty.
2. Ask the reviewer to nominate two independent annotators and a separate adjudicator; confirm role independence and target-variety competence.
3. Use NCKL-derived entries only as candidate lexeme discovery pending written clarification of item-level rights and redistribution; do not copy its respellings into IPA fields.
4. Prefer rights-cleared Kirby reading-condition audio or controlled consented citation-form recordings; prepare 30 candidate groups only after rights/profile review.
5. Test private blind intake before annotation begins.

Status remains BLOCKED for pilot execution: the leads improve recruitment and source discovery but do not constitute recruitment, NCKL permission, adjudicated IPA, or a gold corpus.


## Expert-lead revalidation — 2026-11-04

Two stronger current prospective reviewer leads are now documented. They are not automatically approved as annotators or adjudicators:

- **Nielson Sophann Hul (University of Washington):** the official UW profile describes him as a Khmer linguist specializing in phonetics, heritage language acquisition and Southeast Asian linguistics, with research on implosive consonants, voice quality and sociophonetic variation. Public institutional contact: `nhul@uw.edu`. This is a strong candidate to review the Khmer phonetic convention and advise on reviewer recruitment. The profile does not establish current Phnom Penh target-variety competence, availability, independence or willingness to annotate. https://asian.washington.edu/people/nielson-hul
- **Dr Vatho Chem:** the 2026 University of Cologne project profile identifies him as a phonetician and computational linguist, with a 2025 PhD in Phonetics focused on phonetic reduction in Central Khmer; it also describes extensive Khmer dialect fieldwork and a large speech corpus. His 2020 acoustic study specifically examines the Standard/Phnom Penh Khmer vowel system. Public research contact in that article: `chemvatho@gmail.com`. He is a strong prospective convention reviewer and source expert. Because he maintains a Khmer acoustic-model resource already under source audit, do not use him as the sole adjudicator of any data derived from that resource; declare the relationship and keep annotation/adjudication roles independent. https://cif.uni-koeln.de/projects/revitalizing-and-documenting-koelsch-from-archival-materials-to-an-ai-ready-speech-recognition-and-synthesis-system-chat-like-for-the-endangered-koelsch-dialect ; https://www.cjbar.rupp.edu.kh/index.php/cjbar/article/view/36

The Royal University of Phnom Penh Department of Linguistics is also a credible institutional referral route: its official programme describes postgraduate work in phonetics, phonology, Khmer language and dialect documentation. This is an institutional route, not evidence that any specific faculty member has accepted the project. https://www.rupp.edu.kh/academics/faculties_and_institutes/faculty_of_social_science_and_humanities/department_of_linguistics/ma-Lgs

**Recruitment status:** no one has been contacted, recruited or approved. Obtain explicit confirmation of target-profile competence, IPA expertise, role independence, availability and terms. Two independent annotators, a separate adjudicator and a non-annotating curator remain necessary.

 
## External candidate screening: additional Khmer sources — 2026-11-17

The source registry now records three additional evidence boundaries:

- **MekongPhon / Headley–SEALang:** historical dictionary-derived phonemic candidate only. Preserve the 8,040-row lexicon and its word-level split as source facts, not as an importable corpus. No per-entry provenance, verified dataset license, or approved conversion from Headley's notation to the project IPA/register contract exists. The OPUS sentence pairs are dictionary-generated pseudo-labels, not independent speech annotations.
- **open-dict-data/ipa-dict Khmer:** third-party CC BY-NC-SA 4.0 comparator only. Keep duplicate spellings and all alternative readings. The file's broad phonemic notation is not narrow phonetic gold; the non-commercial/share-alike terms preclude treating it as an unrestricted-release source.
- **Khmer Acoustic Model:** blocked until the full versioned dictionary/model/audio artifacts, checksums, artifact-specific rights, corpus manifest and item-level provenance are supplied. A six-line sample and forced-alignment metrics cannot validate G2P or IPA accuracy.

None of these sources authorizes annotation or import into `records.jsonl` / `gold.tsv`. Candidate comparisons must remain isolated from blind expert pilot/test material and must record source revision, variant policy, profile mismatch and rights status.

## Additional Phnom Penh audio candidate — Kirby cluster recordings (2026-11-17)

The [Kirby 2013 Phnom Penh cluster-audio dataset](https://datashare.ed.ac.uk/items/0d735b30-f6ef-4e14-b6f0-a6b5a136e240) is now registered as `kirby2018-cluster-audio`. Its DataShare metadata states CC BY 4.0 and describes 10 native Phnom Penh speakers, 79 lexical items, three repetitions and two speech-rate conditions, with WAV and segmented Praat TextGrid files. The related 2014 study's first block was read slowly and carefully in a carrier sentence; 61 items with 35 onset-cluster types were analysed.

This is a promising **candidate audio source**, not IPA gold and not yet an approved source for the careful-citation pilot. The carrier-sentence task is not standalone citation-form elicitation; the paper's cluster focus does not establish full contrast coverage; and the 79-item filename list has not yet been enumerated from the 477.8 MB archive. See the [source audit](ipa-gold/khmer-kirby-cluster-audio-source-audit.md) for exact locators, checksum, named paper examples and acceptance boundaries. Do not start annotation or claim profile fit until a qualified reviewer approves the slow-careful condition and a candidate list is mapped to the approved contrast matrix.

## Additional Phnom Penh /r/-loss and prosody evidence — Kirby (2011) datasets (2026-11-17)

Two existing primary DataShare source records have been enriched: [Kirby's 2011 Phnom Penh audio recordings](https://doi.org/10.7488/ds/321) and [supplementary perception/production materials](https://doi.org/10.7488/ds/319). Both DataShare full records state CC BY 4.0. The audio item describes 16 speakers with WAV, segmented Praat TextGrids and Pitch/Formant/PointProcess files. The associated 2014 paper reports 20 recruited native Phnom Penh participants (13 female, ages 21–60); four who retained /r/ in both conditions were excluded from subsequent analysis, leaving 16 analyzed participants. This plausibly explains the DataShare count, although the archive folder membership is not yet verified. The paper reports 41 careful/read items × 3 and a separate 15-item colloquial repetition task × 3. The supplementary item contains anonymised production/perception CSVs, KlattGrid stimuli and R code; perception files/synthetic stimuli are not natural production tokens.

These resources strengthen evidence for contextual variation in /r/-loss, F0, aspiration/VOT, voice quality and vowel quality. They do not define a complete IPA convention or justify a general tone rule; the task is carrier-sentence reading/repetition rather than standalone citation-form elicitation. See [the detailed source audit](ipa-gold/khmer-kirby-tonogenesis-datasets-audit.md). Do not derive labels or a 30-item pilot from these resources until archive contents, speaker counts, token locators, profile fit and the expert-approved contrast matrix are checked.

### Clarification from full Kirby (2014) text — 2026-11-17

The 2011 audio archive's 16-speaker description is plausibly explained by the paper's sample flow: 20 participants were recruited, four who retained /r/ in both conditions were excluded from subsequent analysis, leaving 16 analyzed participants (§3.1.1–3.2). The ZIP folder list has not been inspected, so record this as a likely reconciliation, not a verified identity match. The paper's 41-item Appendix A is romanized phonological notation with glosses, not Khmer-script forms; the paper reports a careful/read self-paced task in a carrier sentence at normal rate and a separate 15-item colloquial repetition task. The reading condition may be relevant to expert review of the target profile, but it is not isolated citation-form elicitation. See the dossier for precise boundaries.


## Sok & Adams (2016) — separate careful phonemic and rapid phonetic layers

Sok & Adams' PACLIC 30 paper ([source dossier](ipa-gold/khmer-sok-adams-phonological-principles-audit.md)) provides a useful precedent for separating orthography-to-phonemic output intended for careful speech from a second phonemic-to-phonetic stage for rapid colloquial speech. Its series-assimilation, vowel-modification and syllable-structure analyses can inform future rule review, but must not be copied directly into the current Phnom Penh careful-citation profile. In particular, aspiration/schwa transitions and minor-syllable reduction are explicitly part of its rapid-speech layer and must not leak into careful citation output.

The paper's 140-word validation is hand-selected and based on Headley (1997) phonemic forms plus author-created phonetic forms; its larger 10,110-word evaluation is dictionary-derived. Its 97.86% / 98.43% figures are not independent project accuracy or IPA gold. The contribution's redistribution rights are unverified. Use it as a rule-system comparator only; do not import its data, labels, or tables.


## Expert shortlist revalidation — current credentials and role separation — 2026-11-17

This is a candidate-screening update only. No person has been contacted, consented, appointed, or approved a convention. Public biographies establish research fit, not availability or willingness.

### Primary target-profile convention reviewer candidate: Chem Vatho

The current first-person CV identifies Chem Vatho as a native Khmer speaker; reports a Dr. phil. in Phonetics from the University of Cologne (2022–2025) for a dissertation on phonetic reduction in Central Khmer; lists an MA in Linguistics and BA in Khmer Literature from the Royal University of Phnom Penh; and describes prior RUPP teaching in Khmer language/civilization and service on the Royal Academy of Cambodia Linguistics Committee. His stated methods include acoustic phonetics, segmental/prosodic annotation, IPA transcription and transcription-convention design. It also lists an Illustration of the IPA for Phnom Penh Khmer as under revision for the Journal of the International Phonetic Association. See his [current CV/profile](https://khmercorpus.com/about-me), the [University of Cologne project biography](https://cif.uni-koeln.de/projects/revitalizing-and-documenting-koelsch-from-archival-materials-to-an-ai-ready-speech-recognition-and-synthesis-system-chat-like-for-the-endangered-koelsch-dialect), and his [2020 Phnom Penh vowel study](https://doi.org/10.61945/cjbar.2020.2.2.3).

**Fit:** strongest currently documented candidate to lead a scoped review of the contemporary Phnom Penh careful-citation IPA convention. Ask whether the under-revision IPA Illustration can be shared for review, its current status and scope, and whether it actually describes the project's selected careful-citation profile rather than a broader or changing Phnom Penh variety. His profile is partly self-reported; credentials and current affiliation should be confirmed directly before appointment.

**Conflict/independence boundary:** Vatho created/maintains the Khmer acoustic-model and pronunciation-dictionary resource. If any of that resource's entries or audio are selected, he must disclose the relationship and must not be the sole adjudicator of those items or be counted as an independent validator of his own labels. Keep external model dictionary content out of project gold unless its exact artifact, provenance, rights and convention are independently cleared.

### Independent phonetics challenge-review candidate: James P. Kirby

The [LMU Munich profile](https://www.phonetik.uni-muenchen.de/~jkirby/about/) identifies Kirby as a linguist/speech scientist working on tone, register, sound change and East/Southeast Asian languages, with a PhD in Linguistics. His [Phnom Penh Khmer tonogenesis study](https://doi.org/10.1016/j.wocn.2014.02.001) and work on onset-F0/VOT interactions include direct evidence about /r/-loss, aspiration, breathiness, pitch and the difference between colloquial and reading pronunciations; his [2018 onset-pitch study](https://doi.org/10.1016/j.wocn.2018.09.009) compares Khmer with tonal languages.

**Fit:** candidate for a bounded independent technical challenge of the PPK acoustic interpretation, /r/-loss, onset-F0, VOT, phonation, cluster-transition and speech-style boundaries. He is not documented as a native Khmer speaker and his published Khmer work is specialized; do not use him as the sole authority for native speaker judgments, the entire segment inventory, or the target convention. Public Edinburgh contact: j.kirby@ed.ac.uk; confirm current preferred contact/affiliation before outreach. No collaboration/conflict with the proposed primary reviewer has yet been ruled out; verify explicitly.

### Other scoped candidates and independence constraints

- **Nielson Sophann Hul:** Cornell's [official profile](https://as.cornell.edu/people/nielson-hul) documents PhD work on Khmer acoustic phonetics of laryngeal sounds and heritage-Khmer teaching. Candidate for a bounded implosive/laryngeal review, not automatically a whole-profile convention authority. His forthcoming Khmer diphthong chapter is co-authored with Becky Butler.
- **Becky Butler:** UNC's official profile and publication list (already linked in Issue #104) support a mainland Southeast Asian phonetics/phonology and Khmer/Bunong sesquisyllable research fit. Candidate for syllable-structure/cluster/diphthong review, not established as a Phnom Penh careful-citation authority. Because she and Hul co-authored a forthcoming chapter, they must not automatically be counted as independent reviewers of each other's work.
- **Honglada Klaharn:** the 2019 [Phnom Penh Khmer linguistics study](https://he02.tci-thaijo.org/index.php/Veridian-E-Journal/article/view/170728) reports data from ten native Phnom Penh speakers over 50 and describes phonology, morphology and syntax. The linked thesis metadata identifies a PhD in Linguistics. Candidate for structural/phonological challenge only; current public evidence does not establish experimental phonetics or IPA-convention expertise.
- **Sothornin Mam:** ChulaSEAL's [TAI 2025 research summary](https://www.arts.chula.ac.th/chulaseal/2025/05/24/chulaseal-at-tai-2025-presenting-southeast-asian-tone-and-intonation-research-in-germany/) documents his PPK pitch study with five native speakers. Candidate for a scoped pitch/F0 evidence review; public evidence inspected here does not establish his native-language status, availability, or authority for the complete segmental convention.

### Proposed role design (not yet accepted by any person)

1. Invite Vatho to consider primary target-profile convention review, with his own resource/data conflicts disclosed.
2. Invite Kirby to consider an independent, narrowly scoped challenge review of PPK phonetic evidence, subject to an explicit collaboration/conflict check and acceptance of the bounded scope.
3. Use Hul/Butler only with their co-authorship relationship disclosed; do not count them as independent from each other.
4. Keep annotators, adjudicator and non-annotating curator as separate people. No reviewer may adjudicate their own annotations or data.

This shortlist reduces uncertainty about whom to approach but does not satisfy any recruitment or acceptance gate. The IPA sheet remains DRAFT_NOT_APPROVED; the 30-item pilot remains blocked; independent adjudicated gold remains 0; empirical accuracy remains null.


## Recruitment execution kit — 2026-11-18

This section turns the existing shortlist into an actionable invitation and response protocol. It is a set of drafts only: **no message has been sent**, and no candidate has accepted or been appointed. Send messages individually, verify the recipient's current preferred contact route first, and do not include private participant data or unreleased audio.

### 1. Primary convention-review invitation — draft

Subject: Request for scoped review of a Phnom Penh Khmer IPA convention draft

Dear [Name],

I am developing a research prototype for Khmer-to-Ukrainian phonetic transcription and am seeking a qualified reviewer for a narrowly scoped, versioned IPA convention. The initial profile is contemporary Phnom Penh Khmer in careful citation-form speech (`khmer-pph-careful-citation-v1`).

Would you be willing to consider reviewing the attached draft, or to recommend an appropriate specialist? The review would focus on whether the proposed broad-phonetic convention is defensible for this exact profile, especially consonant series/register, vowel quality and length, diphthongs, codas, prominence/stress, /r/-related variants, phonation/F0 boundaries and explicit uncertainty handling. Unsupported cells are intentionally left unresolved.

The draft is not approved and no annotation or gold collection will begin until the convention is reviewed. I would welcome corrections or a recommendation to replace the draft entirely. Please also let me know whether the target profile falls within your expertise, your availability, preferred acknowledgement/credit, any fee or institutional requirements, and any relevant conflicts of interest.

This is an exploratory request only; there is no assumption of availability or commitment. I can share the protocol and source dossier for a preliminary scope check.

Thank you,
[Project contact]

### 2. Independent challenge-review invitation — draft

Subject: Independent technical challenge of a Khmer phonetic convention draft

Dear [Name],

I am seeking an independent, bounded technical review of a draft convention for contemporary Phnom Penh Khmer careful citation forms. I would value a critical review of the evidence and assumptions around [specific scope: e.g. /r/-loss, onset F0/VOT, phonation, cluster transitions or diphthongs], including cases where the evidence does not support a categorical rule.

This is not a request to endorse a complete Khmer IPA inventory or to serve as the sole native-speaker authority. The primary convention reviewer and I would disclose relevant collaborations and resource relationships before assigning roles. Would you be willing to review this limited scope, or recommend an independent specialist? Please indicate relevant expertise, availability, conflicts/collaborations, and any terms for the work.

No data will be labelled gold on the basis of this review alone.

Thank you,
[Project contact]

### 3. Annotator / adjudicator / curator recruitment request — draft

Subject: Seeking Khmer IPA annotators and an independent adjudicator for a controlled pilot

Dear [Name],

I am preparing a small, controlled pilot of 30 attested Khmer lexeme groups for contemporary Phnom Penh careful citation speech. The pilot requires two qualified annotators who work independently, a third person to adjudicate only after both submissions are locked, and a curator who does not annotate.

The annotation convention will be versioned and expert-reviewed before work begins. Each item will have a source locator and rights review; annotators will receive identical packets without model predictions or the other annotator's work. Uncertain cases may remain unresolved. We will not ask participants to infer pronunciation from spelling where evidence is insufficient.

Could you advise whether you or a suitable colleague may be interested? Please state your Khmer variety/phonetics/IPA experience, relevant conflicts or shared source relationships, availability, preferred terms, and whether you would be comfortable with the proposed role separation and blind workflow. Participation is not assumed, and no personal details will be published.

Thank you,
[Project contact]

### 4. Response and appointment register — keep outside the public repository

Track each prospective person in a private project log with: candidate pseudonym; date/contact route; response state (`NOT_CONTACTED`, `INVITED`, `DECLINED`, `NO_RESPONSE`, `INTERESTED`, `QUALIFIED_PENDING_CHECK`, `APPOINTED`); target-profile competence evidence; IPA/phonetics qualifications; role accepted; conflicts/collaborations; availability; terms/consent; reviewer independence decision; and the evidence location. Do not publish names, email threads, signatures or personal data in Git.

Do not use `APPOINTED` until the person has explicitly accepted the named role and the curator has documented qualification, availability, conflict and independence checks. One person may not fill annotator A, annotator B and adjudicator roles in combination; the adjudicator must differ from both annotators, and the curator must not annotate.

### 5. Ordered execution gate

1. Send the primary convention-review invitation and independent challenge-review invitation separately; confirm any collaboration/conflict relationship before counting the reviewers as independent.
2. Record written acceptance or decline privately. If the primary reviewer declines, seek another qualified Khmer phonetician rather than silently approving the draft.
3. Only after the convention is approved, recruit and qualify annotators A/B, adjudicator C and a non-annotating curator.
4. Confirm item-level rights and freeze the 30-item source packet. Keep candidate sources out until exact artifacts and terms are verified.
5. Run one non-gold practice item through the private blind channel; capture timestamps/lock evidence and confirm that A cannot see B's work before lock.
6. Begin the 30-item pilot only after all start gates pass. Preserve unresolved cases as unresolved; never force a gold label.

**Current state:** templates prepared; outreach not sent; people not appointed; convention still `DRAFT_NOT_APPROVED`; source rights unresolved; blind intake not tested; gold remains 0 and empirical accuracy remains null.
