# Design: Local deterministic Khmer IPA engine distilled from a neural teacher

## Intent

Build a browser-local Khmer-to-Ukrainian phonetic engine whose runtime is deterministic and does not load a neural model, call an inference API, or depend on a network service. A neural G2P model is used offline during research and rule/lexicon construction. Its outputs are evidence-bearing candidates, not phonetic truth.

The required processing contract remains:

`Khmer orthography → structural analysis → source-language phonological representation → typed IPA → Ukrainian IPA adaptation → Ukrainian practical orthography`.

The existing Python and JavaScript engines, typed IPA boundary, source registry, and Ukrainian adapter remain the foundation. No parallel path may generate Ukrainian text directly from Khmer graphemes while merely displaying IPA as an audit side output.

## Goals

1. The deployed site runs a deterministic local engine: same NFC input + same engine/data version = same output.
2. Neural inference is an offline teacher/build-time research step only. No ONNX Runtime, model weights, Hugging Face request, or remote inference is required by the final site runtime.
3. The deterministic student is compiled from versioned rules and/or exact-form lexical entries with explicit provenance, profile, status, and uncertainty.
4. The student emits typed IPA. The existing Ukrainian adapter consumes that exact IPA result.
5. Strict, Soft, and Super-soft remain distinct evidence/coverage policies:
   - Strict prioritizes source-supported and independently adjudicated correctness.
   - Soft has wider coverage and may expose explicitly PROVISIONAL model-distilled candidates.
   - Super-soft returns a best-effort candidate for every valid Khmer input accepted by the parser; its 100% result coverage is not an accuracy claim.
   - Accuracy must rank Strict > Soft > Super-soft; result coverage must rank Soft > Strict, with Super-soft at 100%. Measure these properties; never manufacture metrics or count placeholders as complete IPA.
6. Preserve raw source forms, syllable boundaries, tone/length where known, IPA kind, provenance, and uncertainty.

## Non-goals

- Running a neural model for each site visitor.
- Shipping the NCKL training dataset or the MekongPhon training/evaluation corpus.
- Calling a provisional model output SUPPORTED merely because it is non-empty.
- Treating a source-attested dictionary or a model's own test split as independent project IPA gold.
- Replacing the existing Ukrainian adapter or creating a second IPA-to-Ukrainian mapping.
- Merging or deploying this branch before acceptance gates pass.

## Current state and evidence

- PR #578 merged browser-local MekongPhon ONNX inference into main. It is a working research candidate, not the desired final deterministic runtime.
- MekongPhon was compared with the six non-conflicting source-attested IPA examples in `data/khmer/vowel-context-register.json`. Both greedy and beam-4 produced 0/6 exact matches and 44.44% code-point CER. This is not a general accuracy estimate, but it fails the narrow source-concordance gate. MekongPhon is not selected as the primary rule-distillation teacher.
- The NCKL `phonsobon/khmer-G2P` model produces Khmer-script pronunciation respelling with syllable separators, not IPA. On its own word-disjoint NCKL test split, the repository measured 83.16% exact respelling, 4.16% CER, and 93.06% syllable-count accuracy. These are respelling metrics, not IPA accuracy.
- The NCKL model's model card declares MIT for model artifacts. The underlying 2022 NCKL dictionary is copyrighted by NCKL and has no blanket redistribution license in the repository's source record. Do not copy its training rows; retain no generated respellings/IPA in aggregate diagnostics; require rights review before shipping any derived lexicon or rule artifact.
- Khmer Phonemizer 0.0.3 is an existing deterministic IPA candidate (MIT package metadata). Direct source-attested diagnostics are weaker than MekongPhon, but it may work better when given the NCKL model's explicit phonetic respelling and syllable boundaries. This bridge is currently being evaluated on the same 12 source-attested lexical examples as the direct baseline.
- The advertised 29,204-entry Khmer Acoustic Model dictionary cannot be used as a lexicon: the pinned upstream repository contains only a six-line sample, no full dictionary/model package, and conflicting/incomplete data-license declarations.
- Independent adjudicated IPA gold remains 0. Accuracy remains NOT_ASSESSED. The profile equivalence of all external engines remains UNVERIFIED.

## Approaches considered

### A. Keep MekongPhon as the primary neural IPA teacher and compile its outputs

Rejected as the primary path. It outputs IPA directly and can run in the browser, but it failed the six-case source matrix under both greedy and beam-4 decoding. Compiling those outputs would deterministically preserve unverified mismatches and could falsely imply evidence-backed rules.

### B. Use NCKL neural respelling as an offline teacher, then a deterministic IPA bridge, then compile the student

Selected as the research path, subject to the bridge diagnostic. NCKL provides syllable boundaries and a phonetic Khmer respelling; Khmer Phonemizer supplies a deterministic mapping from that respelling to IPA. The model is used only offline. If the bridge materially improves the same-input diagnostic, expand evaluation, then distill the teacher's orthography-to-respelling behavior into a static lexical/rule artifact. The final browser engine applies deterministic rules and the existing IPA adapter.

Trade-offs: the intermediate representation is not IPA; the IPA bridge/profile needs validation; NCKL data rights require review; model-to-student agreement does not establish linguistic accuracy. The initial bridge comparison is a screening gate only.

### C. Expand the current source-backed rule engine manually without a neural teacher

Retained as the conservative fallback, but not selected as the sole path. It offers the clearest provenance and lowest runtime complexity, but the current source matrix is too small for broad vowel/coda/syllable coverage. It does not meet the requested neural-assisted development direction by itself.

## Chosen architecture

### Offline research/build pipeline

1. Normalize input orthography to NFC and parse structural units using the existing Khmer parser.
2. Run the pinned NCKL G2P model offline to produce Khmer-script pronunciation respelling. Preserve the exact raw output and explicit syllable separators during the build process.
3. Convert each respelled syllable to IPA with a deterministic phonemizer. Treat this as a separate adapter boundary; never assume that a Khmer respelling string is already IPA.
4. Compare the composite output with the repository's source-attested IPA examples and, when available, independent adjudicated IPA gold. Keep source-attested diagnostic metrics separate from accuracy.
5. Learn/compile deterministic exact-form entries and contextual rules only from approved inputs. Every rule/entry records teacher/model revision, source corpus identifier and hash, license/rights status, target profile, IPA kind, evidence status, and uncertainty.
6. Reject or quarantine candidates that fail source/profile checks. Conflicting analyses remain separate rather than being collapsed into one guessed value.

### Final local runtime

- Load only static, versioned JSON/JavaScript rule and lexical artifacts.
- Parse Khmer orthography, apply the compiled deterministic student, produce a typed IPA result, and pass it through the existing IPA-to-Ukrainian adapter.
- No model download, ONNX runtime, API request, stochastic decoding, or external service is allowed in the final runtime.
- Unknown or unsupported cases use the existing controlled fallback with explicit uncertainty. Do not silently guess.

### Candidate status policy

- `SUPPORTED`: only when the evidence registry and target profile support the result under the project's promotion rules.
- `PROVISIONAL`: model-distilled or external candidate not independently adjudicated; provenance and uncertainty are mandatory.
- `PARTIAL`: only part of the phonological result is known; it must not count as complete IPA coverage.
- `UNRESOLVED`: no justified IPA candidate is available.
- A model's confidence/logits, a successful inference, or a teacher/student agreement score never independently upgrades evidence status.

## Decision gate for the current bridge experiment

The NCKL-respelling + deterministic-phonemizer bridge is worth expanding only if, on the same 12 source-attested lexical items:

- its non-empty output coverage is not lower than direct Khmer Phonemizer;
- its source-attested CER improves by at least 20% relative, and its exact-match count does not decrease;
- all results remain labeled source-attested diagnostics, not accuracy.

This is a screening threshold, not a production acceptance criterion. A pass permits a larger evaluation; it does not permit rule promotion. A fail means do not integrate the bridge as the primary engine; retain the existing deterministic core and investigate a different teacher or a source-only expansion.

## Production acceptance criteria

1. A lawful, versioned input corpus and complete provenance/rights record exist for every generated artifact.
2. The target pronunciation profile and IPA kind are explicitly defined and reviewed.
3. The independent adjudicated IPA gold corpus has non-zero coverage and frozen train/dev/test splits; source-attested CER is never relabeled as accuracy.
4. The deterministic student has measured teacher agreement and independent-gold results, with uncertainty and coverage reported separately.
5. Strict/Soft/Super-soft coverage and accuracy ordering are verified on the same frozen corpus.
6. Python and browser implementations have exact structural/lexical/rule parity and pass full-message tests.
7. Browser runtime makes no network request for model weights and imports no ONNX/model inference dependency.
8. Existing Ukrainian IPA adaptation is the sole path to practical Ukrainian orthography.
9. Build, tests, benchmark, generated-artifact drift, and clean-install checks pass on the exact branch head.

## Operational boundaries

- Current branch: `feat/deterministic-neural-distillation-20261125`; current PR #582 is draft.
- No merge, Pages deployment, release, license selection, or external rights assumption is authorized by this design.
- The GitHub connector is the available repository workspace. The container has no local checkout and cannot resolve github.com, so local git/worktree execution is unavailable; exact-head GitHub Actions are the verification source. This increases the importance of branch-gated CI and exact SHA recording.

## Decision update — Google phonemic lexicon + retrained neural teacher (2026-11-25)

This decision supersedes the earlier selection of the NCKL-respelling bridge as the primary research path. The NCKL split-syllable bridge scored 8/12 exact and 6.93% CER, while direct Khmer Phonemizer scored 11/12 exact and 0.99% CER on the same 12 source-attested lexical items. The bridge is not promoted. Whole-string and space-separated NCKL boundary variants remain a bounded diagnostic only.

A stronger project-local source has been verified:

- The pinned Google Khmer pronunciation TSV at commit `a90601024f07ab7e96c911243324e0adeb16da96` contains 62,179 Khmer-script rows: 62,118 non-empty phonemic transcriptions, 61 empty transcriptions, 62,114 unique spellings, and four words with multiple pronunciation variants.
- The same source's `km/festvox/phonology.json` defines 56 phones. All 54 distinct phone tokens observed in the non-empty Khmer lexicon are present in that inventory; only `sil` and `pau` are unused.
- A preliminary, explicitly provisional token-to-IPA adapter matches all six non-conflicting R12A vowel-context IPA examples. On the separate source-attested lexical sample, only 3/7 overlapping entries match exactly; four conflicts (aspiration, glottal stop, or vowel length) remain visible and must not be silently normalized away.
- The source attribution file records CC BY 4.0 for the Google pronunciation data. The phonemic strings are not already project IPA; they must pass through a dedicated token-to-IPA adapter.
- The external NPanha neural G2P repository provides MIT-licensed training code but no committed model checkpoint and no committed training TSV. Its reported PER/WER cannot be treated as reproducible project evidence. The project will train its own offline teacher from the pinned Google corpus and use a true phone-token target tokenizer (space-delimited phones plus explicit syllable-boundary tokens), rather than trusting the external repository's missing checkpoint or its character-level tokenizer behavior.

### Selected research/build architecture

1. **Licensed source lexicon:** use the 62,118 non-empty Khmer entries as a versioned phonemic lexical source. Preserve the four multi-pronunciation words as candidate arrays; do not select one arbitrarily. Keep the 61 blank rows unresolved.
2. **Google phonemic → IPA adapter:** map source phone tokens to IPA using the pinned Google phonology inventory plus explicit source-attested cross-checks. Emit `PHONEMIC` typed IPA, preserving `.` syllable boundaries and long-vowel marks. Tokens without defensible mappings remain unresolved or provisional; no unknown token is guessed.
3. **Offline neural teacher:** train a project-owned model on the same CC BY 4.0 source corpus, with word-disjoint deterministic train/dev/test splits and phoneme-token-level target encoding. Record phoneme error rate, word exact match, syllable-boundary accuracy, coverage, seed, config, data hash and checkpoint hash. These are source-label prediction metrics, not independent IPA accuracy.
4. **Deterministic student:** compile the exact lexical source and approved neural-derived syllable/context rules into stable static JSON/JavaScript data. The final site uses only that static artifact and the existing IPA → Ukrainian adapter. The neural checkpoint remains a build/research artifact and is not loaded by site visitors.
5. **OOV policy:** exact lexical hits use the source phonemic candidate and IPA adapter; validated deterministic rules cover compositional cases; model-derived rules remain PROVISIONAL until independently corroborated. Unknowns preserve uncertainty.

### Additional evidence gates

- The Google phonemic token inventory must be fully accounted for by the pinned source phonology inventory; all lexicon rows must parse or be explicitly classified as blank/ambiguous/unsupported.
- The token-to-IPA adapter must pass the six R12A source examples and report the four lexical conflicts without suppressing them. The 6/6 result is a screening check, not accuracy.
- The retrained teacher must be evaluated on a word-disjoint held-out split. The split must group all variants of a spelling together.
- The compiled deterministic student must be compared against the teacher on held-out inputs and independently against any available source IPA. Teacher agreement is not accuracy.
- No generated lexicon/rule artifact is promoted to `SUPPORTED` solely because it is licensed, model-generated, or syntactically valid IPA.
- CC BY 4.0 attribution must accompany any distributed derivative of the Google source. The external NPanha metrics are not used as project benchmark results.
