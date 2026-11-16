## MekongPhon evidence review — 2026-11-04

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHMER-MEKONGPHON-001 | PARTIAL (candidate secondary source; rights unresolved) | LREC 2026 paper and PDF; seed lexicon from historical dictionary IPA; two-author 500-entry sample review (97.2% Lao / 99.2% Khmer); sentence expansion by longest-match-first lookup over OPUS; repository snapshot f80f6c1840c4818b51e05f2e00cded4701a5b662 has no declared license/root LICENSE. | May be used for source-located lexical triage only after profile/convention checks. Not independent sentence-level gold; do not import into gold.tsv. Item-level source and derivative rights must be resolved before redistribution. |

## Post-merge provenance checkpoint — 2026-11-03

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHMER-G2P-PROVENANCE-001 | DONE_VERIFIED (PR-head verified; post-merge push CI not independently surfaced) | PR [#129](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/129) merged as 2138f6f10df875591e846c81fae69c7cfde69bb5. Exact PR-head Quality [41726874329](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41726874329), browser [41726874307](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41726874307), optional G2P [41726874306](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41726874306) all SUCCESS; artifact contents inspected. | Diagnostic report provenance and checksum integrity only; no language accuracy. Gold remains 0; accuracy null. |

## External diagnostic report provenance — 2026-11-03

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHMER-G2P-PROVENANCE-001 | DONE_VERIFIED (diagnostic reproducibility only) | PR [#129](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/129), exact head 54c6a321c894468a7dd1625192a43f15fd806822; RED [41725130084](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41725130084); Quality [41726222759](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41726222759) SUCCESS (172 tests + 60 subtests); browser [41726222701](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41726222701) SUCCESS; optional G2P [41726222858](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41726222858) SUCCESS. Artifact inspected: JSON + .sha256 sidecar + source diagnostic; expires 2027-02-01. | Exact harness SHA-256, corpus hash, engine/version, Python/platform and GitHub event metadata are recorded; report integrity is independently checkable. No linguistic validation: independent adjudicated gold 0; accuracy null. |

## External diagnostic report provenance — 2026-11-03

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHMER-G2P-PROVENANCE-001 | DONE_VERIFIED (diagnostic reproducibility only) | PR [#129](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/129), current head 0607f7d2ad2ed481f0b75dcd486a2dcaefa31c6c; test-first RED [41725130084](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41725130084); exact-head Quality [41725569108](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41725569108) SUCCESS (172 tests + 60 subtests), browser [41725569152](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41725569152) SUCCESS, optional G2P [41725569100](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41725569100) SUCCESS; artifact retained until 2027-02-01. | Report records harness SHA-256, corpus hash, engine/version, Python implementation/version, platform and CI source revision; JSON report has adjacent SHA-256 sidecar. This proves diagnostic provenance/integrity only, not language accuracy or gold agreement. Independent adjudicated gold remains 0; accuracy null. |

# Khmer linguistic completion register — 2026-11-01

**Benchmark implementation merge:** `0f73d006bfc05f6106a3b1e463c2cc7d6471ffae` (PR #123). **Handoff/register reconciliation merge:** `ebd8432b4abacecb50e30bae43ff64c42ac4063b` (PR #124).
**Latest post-merge exact-main evidence:** [engineering verification](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41707503253) SUCCESS; [built-site Chromium smoke](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41707503102) SUCCESS; [Pages/deployed-site smoke](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41707503262) SUCCESS.
**Open pull requests:** none at this checkpoint.
**Research boundary:** Independent expert-adjudicated Khmer IPA gold remains 0; `data/benchmark/gold.tsv` is header-only; empirical accuracy remains null.
**Scope:** continue the existing master handoff; this register does not replace it.

## Unicode/parser contract correction — 2026-11-03

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| UNICODE-TOKEN-BOUNDARY-001 | DONE_VERIFIED | PR [#126](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/126), merge `2a2f1c55282e076d6c4e0640d80af1053783bd6b`; exact-head Quality checks [41710399396](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41710399396) SUCCESS and browser smoke [41710399684](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41710399684) SUCCESS. | Browser punctuation segmentation now uses Unicode general category `P`, matching Python; regression covers U+3002 between two valid Khmer units and verifies exact source preservation plus neighbor status/output. This does not establish Khmer pronunciation or gold accuracy. |

**Research boundary unchanged:** no IPA gold labels were added; independent adjudicated gold remains 0 and empirical accuracy remains null.

## Held-out IPA benchmark integrity — 2026-11-03

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| IPA-BENCH-HELDOUT-001 | DONE_VERIFIED | PR #123 merged as `0f73d006bfc05f6106a3b1e463c2cc7d6471ffae`; exact-main verification [workflow](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41707503253) SUCCESS; browser smoke [workflow](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41707503102) SUCCESS; Pages/deployed-site smoke [workflow](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41707503262) SUCCESS. Export preserves split bucket and frozen manifest seed/version; scoring defaults to held-out test; explicit all-split mode is marked diagnostic; malformed/mixed split metadata and empty predictions fail closed. | Engineering evaluation integrity only. Independent expert-adjudicated Khmer IPA gold remains 0; `data/benchmark/gold.tsv` is header-only; empirical accuracy remains null. No gold rows, IPA labels or accuracy claims were fabricated. |


## Engineering integrity continuation — 2026-11-03

- **TSV-INPUT-001 — DONE_VERIFIED:** benchmark TSV ingestion now rejects duplicate/blank headers and nonblank rows with extra or missing fields; blank physical lines are ignored. Regression cases cover gold/prediction duplicate headers, extra gold cells, and truncated prediction rows.
- **Evidence:** test-first RED [41665735912](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41665735912); focused implementation GREEN [41665873021](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41665873021); implementation commit `46e7eda242f134a792060c3002992bdea42bdb6c`.
- **Acceptance boundary:** input shape is validated before scoring. This does not create adjudicated IPA data or alter language accuracy status (gold 0; accuracy null).

## Strict JSON syntax — 2026-11-03

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| JSON-INPUT-003 | DONE_VERIFIED | Reject `NaN`, `Infinity`, and `-Infinity` in JSONL and license registry inputs. RED 41692662080; implementation CI 41694124825 SUCCESS (171 Python tests + 60 subtests; 3 browser smoke tests (run 41694138503)). | Reject non-standard JSON constants before corpus or rights validation; no linguistic labels or license terms changed. |

## License registry JSON integrity — 2026-11-03

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| JSONL-INPUT-002 | DONE_VERIFIED | Duplicate top-level and nested keys in `licenses.json` rejected. RED 41690144835; implementation CI 41690306190 SUCCESS (169 Python tests + 54 subtests; 3 browser smoke tests (run 41690316616)). | Rights registry cannot silently apply last-key-wins semantics; no license permission is inferred or broadened. |

## JSONL input integrity — 2026-11-03

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| JSONL-INPUT-001 | DONE_VERIFIED | Duplicate top-level and nested JSON object keys are rejected. RED 41687409282; exact implementation-head CI 41687730383 SUCCESS (167 Python tests + 54 subtests; 3 browser smoke tests). | Prevent silent last-key-wins corruption before corpus schema/provenance validation. No linguistic data or accuracy claims added. |

## Evidence-based task ledger

| ID | Status | Work remaining | Acceptance |
|---|---|---|---|
| KHM-GOLD-001 | BLOCKED | No independent expert-adjudicated lexical IPA gold exists; `data/benchmark/gold.tsv` contains only its header. | At least two independent qualified Khmer phonetic annotators, adjudication, dialect/profile and IPA convention fixed, stable source/audio locators; frozen held-out split. |
| KHM-PHON-001 | PARTIAL | Complete context-dependent consonant-series × vowel × coda × syllable analysis and word segmentation. | Every supported combination backed by primary sources or adjudication, with shared Python/browser tests and explicit unsupported states. |
| KHM-RLOSS-001 | PARTIAL | Phnom Penh /r/-loss transformation remains profile-dependent and incompletely validated. | Define exact environment/dialect, test positive and negative minimal pairs against source-located expert labels; otherwise withhold. |
| KHM-ROM-001 | PARTIAL | All 22 consonant and 37 PCGN vowel/rime target rows are populated; PR #164 integrates a separate provisional Latin-to-Ukrainian runtime adapter. The upstream ASCII profile drops PCGN diacritics. | Retain provisional label until a diacritic-preserving/context-aware BGN/PCGN engine covers series, vowel, shortening, coda and shifter environments; keep pronunciation claims separate. |
| KHM-G2P-001 | DONE_VERIFIED (diagnostic harness only) | Goruut has substantial partial coverage; Khmerphonemizer source concordance is not independent accuracy. | No production promotion absent gold and full source coverage; preserve raw outputs and comparator provenance. |
| KHM-UI-001 | PARTIAL | PR #108 is merged; exact-main Chromium coverage, Pages deployment and deployed-site smoke all pass. Manual visual, keyboard, assistive-technology and mobile QA remain open. | Record human keyboard, screen-reader, responsive/mobile and visual results on the deployed site. |
| KHM-WEB-RESULT-RENDER-001 | DONE_VERIFIED | Removed the invalid `#source-result` dereference in PR #108; exact-main Quality [41641496598](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41641496598), Chromium [41641496582](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41641496582), and Pages/deployed smoke [41641496680](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41641496680) all succeeded. | Keep regression tests and Pages browser gate; manual accessibility QA remains tracked under KHM-UI-001. |
| KHM-REL-001 | PARTIAL | Production readiness blocked by lexical gold, contextual phonology and rights for external assets. | All release gates met; no restricted external model/data bundled. |

## Current diagnostic evidence

The latest recorded Goruut 100-row result is 97 outputs, 3 none; 70 complete, 27 partial, 3 unknown/no output; 96 stable, 1 unstable, 1 randomization-flagged input; strict source-attested concordance 6/100. Khmerphonemizer 0.0.3 returned 100 outputs and 100 comparable source labels after the comparator metadata-field correction; 18 strict and 19 limited-notation matches. These are not accuracy. The source IPA labels are generated/source-attested, not independently adjudicated gold. Independent gold remains 0; accuracy remains null.

## Execution order

1. Preserve fail-closed phonetic behavior; romanization must never be used as phonetic fallback.
2. Commission independently double-annotated Khmer lexical/audio IPA, with dialect, register, syllable and source metadata.
3. Complete the contextual orthography-to-IPA matrix, especially inherent vowels, consonant series, codas and syllable boundaries.
4. Validate the Phnom Penh /r/-loss profile separately from the core profile.
5. Finish PCGN contextual romanization and implement its independent Ukrainian syllable adapter.
6. Conduct deployed UI/accessibility QA and asset-rights review.

## External dependencies / blockers

- Qualified Khmer phonetic annotators and adjudicator.
- Permission/provenance for external corpus, dictionary, model and audio resources.
- No local checkout was available to this execution; exact-main GitHub Actions are the engineering evidence. Run documented local release commands in a clean checkout before release.

## Method constraints

Preserve `Khmer orthography → structural/register analysis → Khmer phonology → typed IPA → Ukrainian adaptation`. BGN/PCGN romanization is a separate orthographic route. Source-attested labels, engine agreement and structural fixtures are not gold.

## Open PR reconciliation

PR [#64](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/64) remains open and untouched. Current comparison against `main`: diverged, 7 commits ahead / 46 behind; changes replace the current stylesheet snapshot and add layout-contract tests coupled to that old CSS. The required responsive improvements already exist in focused merged work. Do not merge wholesale; revisit only after a fresh visual audit identifies a concrete missing behavior, then port a minimal change with current-browser tests.


## Independent IPA gold corpus implementation — 2026-11-01

| Task | Status | Evidence / remaining acceptance |
|---|---|---|
| IPA-GOLD-SCHEMA-001 | DONE_VERIFIED | Record, annotation, adjudication, split and license schemas plus cross-file validator |
| IPA-GOLD-DOUBLE-ANNOTATION-001 | PARTIAL | Two distinct annotators enforced; blind intake requires external controlled collection |
| IPA-GOLD-ADJUDICATION-001 | PARTIAL | Agreement/resolved/unresolved logic and feature-complete IPA comparison; no real adjudicated rows |
| IPA-GOLD-RIGHTS-001 | DONE_VERIFIED (mechanism) | Allowlisted licenses, required rights evidence and rejection of unregistered/non-redistributable licenses; source-by-source legal review still required |
| IPA-GOLD-SPLIT-001 | DONE_VERIFIED | Deterministic hash-based, frozen lexeme-group split and leakage checks |
| IPA-GOLD-EXPORT-001 | DONE_VERIFIED | Rights-filtered typed IPA export retaining source/license/evidence locators |
| IPA-TYPED-BENCHMARK-001 | DONE_VERIFIED | Different or missing IPA kind cannot count as an exact match |
| IPA-GOLD-RELEASE-GATE-001 | PARTIAL | Tag/manual workflow requires 100/25/25 adjudicated train/dev/test; owner must require the check in release rulesets/procedure |

**Current gold:** zero independent expert-adjudicated records; `gold.tsv` remains header-only; accuracy=null. The new schemas, fixtures and source-attested literature are not gold labels. No phonetic data was invented.


**Research evidence artifact:** [Khmer vowel × series × coda evidence matrix](KHMER-VOWEL-SERIES-CODA-EVIDENCE-MATRIX-2026-11-01.md). It records the specialist ɑ/ɔ-class mapping, Chem's four-speaker acoustic sample, coda-conditioned effects and explicit missing cross-product cells.


**2026-11-01 closeout:** PR [#103](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/103) is the comprehensive implementation and research-matrix change. PR CI passed 136 Python tests + 27 subtests, the browser register-shifter contract, web checks and Vite build. Main remains at c0a2b33. Gold remains 0; full contextual matrix and expert adjudication remain blocked.


**Expanded matrix status:** Ishida's full specialist phone-to-grapheme mapping table has been extracted into the Khmer matrix. The remaining gap is not missing orthographic mappings but independent lexical/acoustic coverage for every profile × series × stress × coda cell.


## 2026-11-01 final IPA-kind consistency verification

- Added fail-closed cross-annotation consistency: both independent annotations for one record must use the same `ipa.kind`, and a `RESOLVED` adjudicated result must preserve that kind. This prevents phonemic-vs-phonetic representation differences from being misclassified as pronunciation disagreements.
- Regression evidence: both new tests failed against the pre-fix validator on the test-only commit, then passed after the validator change.
- New task `IPA-GOLD-REPRESENTATION-KIND-001`: **DONE_VERIFIED** (mechanism and exact-head CI). Blindness, annotator qualifications and independent adjudicator competence remain external operational evidence, not properties CI can prove.
- Final PR head: `f7f2bf9a471f5fea990c0cf9509d382e3371d17b`; CI run [41338461515](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41338461515) SUCCESS — 139 Python tests + 27 subtests; browser register-shifter contract, web checks and Vite build passed.
- The Khmer matrix remains PARTIAL: full profile × series × stress × coda lexical coverage and an independent broader /r/-loss replication are not available.
- Gold remains zero; `gold.tsv` remains header-only; empirical accuracy remains null. No IPA labels were generated.


## IPA gold split-manifest runtime/schema parity — 2026-11-01

| ID | Priority | Status | Scope / evidence | Acceptance criteria / dependencies |
|---|---|---|---|---|
| KHM-IPA-SPLIT-STRICT-001 | P1 | DONE_VERIFIED | RED test on commit `3fdfd9559dfc98c43c4c503b9e707f1632ebad07` failed as expected; GREEN code commit `64851a4572437d9185b47fcff56bde55e4f092c5`; exact-head CI [41340405233](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41340405233) passed | The split generator and corpus validator share the closed split-field contract; unknown prior-manifest properties are rejected rather than silently dropped. No expert gold is created by this change. |


## Product-corpus license eligibility — 2026-11-01

| ID | Priority | Status | Scope / evidence | Acceptance criteria / dependencies |
|---|---|---|---|---|
| KHM-IPA-LICENSE-ELIGIBILITY-001 | P1 | DONE_VERIFIED | RED tests on `83cfdc10716eff99f622f5d0e3c9c035bee3b56e`; GREEN code/schema commit `b3104d6815edb3950e13457f7e04bcb8f5f90145`; exact-head CI [41340930079](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41340930079) passed | Registry and schema fail closed unless a redistributable product-corpus license explicitly permits commercial use and defines attribution/share-alike obligations. Human source-by-source rights review remains required. |


## Release-gate threshold validation — 2026-11-01

| ID | Priority | Status | Scope / evidence | Acceptance criteria / dependencies |
|---|---|---|---|---|
| KHM-IPA-RELEASE-THRESHOLDS-001 | P1 | DONE_VERIFIED | RED test on `888ce85258e0c42b44e082e06023dbcd96401b96`; GREEN code commit `38aed74299c898461607407b730085e1b70d565d`; exact-head CI [41341743668](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41341743668) passed | All split minimums reject zero and negative values; threshold errors aggregate with other release-gate findings. Default minimums remain 100/25/25. |


## Audio-source review update — 2026-11-01

Two audio candidates are now documented in `docs/ipa-gold-collection-playbook.md`:

- Common Voice Scripted Speech v27.0 Khmer: locale `km`, catalogued CC0-1.0, 20.23 MB MP3 archive (https://commonvoice.allizom.org/en/datasets). Exact clip/speaker counts and regional metadata still require manifest inspection.
- OpenSLR 42 (SLR42): multi-speaker Khmer WAV plus transcript line index, CC BY-SA 4.0, with the currently listed archive containing male-speaker audio only (https://openslr.org/42). The provider says recordings are manually quality-checked but may still contain errors.

Neither provides IPA gold. Both are sentence-context sources; neither proves Phnom Penh citation-form coverage. Use them as supplementary audio only unless the exact speaker/profile metadata supports a narrower claim.

The Khmer Acoustic Model README claims 29,204 IPA entries and native-linguist validation, but the documented full dictionary path `dictionary/khmer_ipa.dict` returned 404 in the inspected default branch; only a six-row sample file was retrievable. Its sample uses space-separated symbol sequences, and the README does not specify a project-compatible typed IPA convention or item-level provenance. Keep it as an external comparator lead, not gold.

Status remains `KHM-GOLD-001 = BLOCKED`: no annotations, annotators or adjudications have been created. Independent gold remains 0 and accuracy remains null.


## Common Voice v27.0 manifest verified — 2026-11-01

The official release manifest `cv-corpus-27.0-2026-09-11.json` has been inspected (https://github.com/common-voice/cv-dataset/blob/main/datasets/scripted-speech/cv-corpus-27.0-2026-09-11.json). Khmer metadata: 739 clips, 213 validated clips, 15 contributor IDs, 0.28 validated hours (0.98 total). No named accent/variant category is supplied; gender metadata is entirely unspecified. Locale checksum in the manifest: `d1c4bb041744fefb1fa60397217b7cd79bfa2ade4510b11ff9863e9a0dc0392d`.

The dataset may be sufficient for a process pilot only if 30 required lexical contrasts occur in validated clips. It cannot establish Phnom Penh variety or speaker balance. OpenSLR42 remains an additional male-only contextual-audio source, not IPA gold. Controlled citation-form recordings and expert profile approval remain required. No data imported; `KHM-GOLD-001` remains `BLOCKED`, gold 0, accuracy null.


## Final exact-head verification — 2026-11-01

Branch `feat/ipa-gold-corpus-20261101-review`, source-audit content commit `9bb02272d9da77126ac80392e840228aef18d18f`. Khmer exact-head CI: Quality checks [41345111255](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41345111255) SUCCESS; optional Goruut [41345111267](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41345111267) SUCCESS; optional Khmer G2P [41345111293](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41345111293) SUCCESS. Core job passed corpus structure validation, Python tests, Node web checks, and production site build.

These checks validate the committed repository and its automated engineering contracts. They do **not** validate the linguistic correctness of future human annotations, create gold labels, or change the release blocker. Gold remains empty and accuracy remains null.


## Follow-up handoff-head CI — 2026-11-01

The subsequent documentation-only handoff/register state at commit `1800ab775ade8e6c2ac1264c4318da69a07a53c1` was also checked on its exact head: Quality checks [41345362797](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41345362797) SUCCESS; optional Goruut [41345362827](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41345362827) SUCCESS; optional Khmer G2P [41345362791](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41345362791) SUCCESS. These runs validate the updated documentation and existing automated checks, not future IPA annotations. Any later branch update must be checked again on its new exact head.


## Open-rights redistributability invariant — 2026-11-01

| Task | Status | Evidence / acceptance |
|---|---|---|
| KHM-IPA-RIGHTS-OPEN-001 | DONE_VERIFIED | A test-first regression rejected a source with `rights_status=OPEN` and `redistributable=false`; the runtime validator and record JSON Schema now both require `redistributable=true` for OPEN. Test-only RED commit: `8e328d06fb13130d878859ca2c297fb154fc0533`. Fix/schema code head: `e624dd59ce7ae1648cf72262e124764769fbc8a2`; exact-head CI run [41347973905](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41347973905) passed: 144 Python tests + 37 subtests; web checks and production build passed; optional Goruut and Khmer G2P smoke benchmark passed. |

This is a consistency/eligibility invariant, not a new legal determination. It does not change source licenses, rights evidence, gold labels or measured accuracy. Independent adjudicated gold remains 0; accuracy remains null.

## Exact current-head engineering checkpoint — 2026-11-01

- Current code checkpoint: `508ed94460e210ff9cc07cc0eaa7815246ee37b2`; exact-head core CI [41348224247](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41348224247) **SUCCESS**. 144 Python tests + 37 subtests; browser register-shifter contract, web checks and Vite production build passed. Optional Goruut KhmerCentral and Khmer G2P diagnostics passed.
- The `OPEN` / `redistributable` consistency regression is present in runtime validation, JSON Schema and tests.
- Independent expert gold remains 0 and accuracy remains null. Human annotation/profile/convention gates remain open; CI is not linguistic validation.

 
## Nested IPA record contract closure — 2026-11-01

| Task | Status | Evidence / acceptance |
|---|---|---|
| IPA-GOLD-NESTED-STRICT-001 | DONE_VERIFIED (engineering contract) | Test-first RED: [run 41352932018](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41352932018); GREEN exact-code-head CI: [run 41353055958](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41353055958). Runtime validator and JSON Schema both reject undeclared fields in `orthography`, `profile`, `source` and `source.rights_evidence`. 146 pytest tests + 44 subtests; web checks, register-shifter browser contract and production build passed. |

This closes only the nested-object shape contract. It does not establish the truth of source metadata, rights determinations, speaker profiles, IPA, or expert adjudication. Independent gold remains 0 and accuracy remains null.


## Validator duplicate-call cleanup — 2026-11-01

| Task | Status | Evidence / acceptance |
|---|---|---|
| IPA-GOLD-DUPLICATE-VALIDATION-001 | DONE_VERIFIED | Removed four consecutive duplicate `reject_unknown_properties` calls from nested `orthography`, `profile`, `source`, and `source.rights_evidence` validation. Code commit: `5c5e14d0458f9afd9c154e36975d86d882b67c0f`; Git blob SHA: `a072297e320b4b91a36c59fc90328b6ff98d2a5f`. - Core PR CI: https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41354247584 (SUCCESS); core push CI: https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41354242025 (SUCCESS); optional language diagnostics: https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41354247560, https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41354247608 (SUCCESS). |

This is dead-code cleanup only: each contract check remains once; no validation rule, schema, IPA value, phonology rule, or corpus row changed. The shared validator remains identical across Lao, Khmer and Burmese. Hosted CI only; no local checkout or local test command is claimed. Independent expert-adjudicated gold remains 0 and empirical accuracy remains null.


## Methodology source refresh — 2026-11-02

| ID | Status | Evidence / acceptance |
|---|---|---|
| ENGINEERING-METHOD-REFRESH-001 | DONE_VERIFIED | Updated `AGENTS.md` and canonical handoff to pin Superpowers 7.0.1, mattpocock/skills current main, and Ponytail 5.3.3. Exact-head CI on methodology commit `bf506e2a34e3a2523678487fdc5148ab019bd493`: [PR Quality checks 41356374055](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41356374055) and [push Quality checks 41356369054](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41356369054) SUCCESS; 146 tests + 44 subtests; [Goruut 41356374057](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41356374057) and [Khmer G2P 41356374080](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41356374080) SUCCESS. No runtime dependencies or copied skill bundles were added. |



## Methodology source refresh follow-up — 2026-11-02

| ENGINEERING-METHOD-REFRESH-002 | DONE_VERIFIED | Updated `AGENTS.md` and canonical handoff to mattpocock/skills v1.3.2 (`d1478fcb140db0b93c0c8df17bcfd311844749d0`); added two-axis review, genuine-RED evidence, template/ownership, and safe worktree-cleanup guidance. Verified documentation checkpoint `73e654b5a592cb84ed29b25b03cb95fb5a7e25e0`: [Quality checks 41358627128](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41358627128) SUCCESS; optional [41358627194](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41358627194) and [41358627130](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41358627130) SUCCESS. | No third-party code, data, skill bundle, or runtime dependency copied. |

## IPA gold adjudication required-field parity — 2026-11-02

| ID | Priority | Status | Scope / evidence | Acceptance criteria / dependencies |
|---|---|---|---|---|
| IPA-GOLD-ADJUDICATION-FINAL-IPA-001 | P1 | DONE_VERIFIED | A test-first regression demonstrated that an `UNRESOLVED` adjudication with the `final_ipa` property omitted was accepted by the Python runtime even though the JSON Schema requires the property (nullable). Test-only RED commit `df23f23c573c8311c7c721b02177b65b44117fd7`; failing exact-head PR CI [41407016954](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41407016954). Runtime fix commit `dea7008094314b6a1ae88b1b4868e41552cdd54a`; exact-head PR CI [41407116467](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41407116467) SUCCESS. 147 pytest tests + 44 subtests; web checks and production build passed. |

The validator now requires the `final_ipa` key to be present for every adjudication. `UNRESOLVED` must supply explicit JSON `null`; `AGREEMENT` and `RESOLVED` still require a typed IPA object. No phonology rules, corpus labels, source data or benchmark scores changed. Optional diagnostic runs: [41407116367](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41407116367), [41407116301](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41407116301). Gold remains 0 and empirical accuracy remains null.


### Unresolved adjudication explicit-null positive-path coverage — 2026-11-02

The regression suite now also proves the valid complementary case: `decision=UNRESOLVED` with an explicitly present `final_ipa: null` is accepted and remains excluded from adjudicated gold. Test commit `8111f28c34b7b3d7118d4f428178e4e90591c336`; exact-head PR CI [41407396214](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41407396214) SUCCESS. 148 pytest tests + 44 subtests; web checks and production build passed. Optional diagnostics: [41407396207](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41407396207), [41407396326](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41407396326) SUCCESS. This does not create IPA labels or change the gold count (still 0) or accuracy (still null).

## External G2P engine coverage audit — 2026-11-02

- **PARTIAL (DONE_VERIFIED diagnostic execution):** Khmer phonemizer 0.0.3 returned 100/100 outputs on a 100-row MekongPhon sample, with 18 strict / 19 limited-normalized matches. Goruut source snapshot `b224bde` achieved 6/100 exact matches, 3 failures, 70 complete / 27 partial / 3 unknown coverage, and 27 unphonemized fragments. See `docs/research/external-g2p-benchmark-and-engine-coverage-2026-11-02.md` and Actions runs 41409092574 / 41409092578.
- **NOT SCORED:** these are source-attested diagnostic concordance counts, not independent gold or accuracy; independent expert-adjudicated IPA gold remains 0.
- **TODO:** investigate series × vowel × coda mismatches and the absent upstream Goruut `weights9.bin.zlib` asset; evaluate MekongPhon model and NCKL-derived Khmer respelling as separate IPA and syllabification baselines.


## Goruut language-bundle asset status correction — 2026-11-02

The previous TODO wording suggesting that this repository can simply recover or fix `weights9.bin.zlib` is superseded. Inspection of the exact upstream Goruut source tree at `b224bde02151f8f86d0fe260804e4ca743bda620` shows no `weights9.bin.zlib` in `dicts/lao/`, `dicts/khmer/central/`, or `dicts/burmese/`; the earlier `weights7` and `weights8` assets are present. This is an upstream language-bundle omission in the pinned snapshot, not a missing project-owned file. Status: **BLOCKED (upstream dependency)**. Acceptance: upstream publishes the asset or documents the expected model-tier fallback, and a controlled same-input comparison plus independent expert IPA gold establishes whether the asset changes relevant language coverage. Do not synthesize weights, download unpinned substitutes, or treat the warning as a failed workflow. See the external-engine research audit and canonical handoff for the evidence.


## Additional Khmer transformer and lexical baseline inventory — 2026-11-02

| ID | Priority | Status | Evidence / acceptance |
|---|---|---|---|
| KHM-MEKONGPHON-TRANSFORMER-001 | P1 | TODO | [`byumatrixlab/khmer-ipa`](https://huggingface.co/byumatrixlab/khmer-ipa) is a 33.6M-parameter BERT encoder–decoder trained from MekongPhon, with 128-token maximum input. Pin immutable revision/checksum, verify variety and IPA conventions, and compare on identical held-out lexical groups with series/register, vowel, length, coda, stress, /r/-loss and boundary diagnostics. Model output is not gold. |
| KHM-ACOUSTIC-LEXICON-001 | P2 | BLOCKED | README reports 29,204 IPA entries, but `dictionary/khmer_ipa.dict` returned GitHub API 404; only the six-entry `dictionary/khmer_ipa_sample.dict` was retrievable. No full lexicon coverage/notation audit can be performed from the sample. Acceptance: publish or expose the full dictionary at a stable inspectable path; then audit notation and orthographic coverage. This is a lexical/forced-alignment resource, not a G2P engine; alignment F1 is not IPA-generation accuracy. |


## Main publication reconciliation — 2026-11-02

Supersedes earlier handoff statements that the review branch was still ahead of `main` and unmerged: PR [#103](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/103) was merged into `main` as `b7e0171f77c08a15b0e55a9cb9fd83a001fff4f7`; this was the repository's current `main` tip at reconciliation. Exact-head engineering workflows on the PR head passed: Quality/tests [41414658963](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41414658963), Khmer G2P [41414658924](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41414658924), and Goruut [41414658926](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41414658926). The Pages workflow is configured to deploy from `main` and includes a deployed-site/runtime-asset smoke test. The public deployment result could not be independently inspected from this session, so deployment status remains **BLOCKED (external verification/network access)**, not claimed successful. No frontend source changes were included in this PR. Independent expert-adjudicated gold remains 0 and accuracy remains null; the project is still a research prototype.


## Current-main UI publication — 2026-11-02

The older design PR [#64](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/64) was not merged because its branch had diverged (7 commits ahead / 178 behind current `main`). Its responsive CSS and cache-busting intent were ported onto a fresh branch from the then-current `main`; PR [#105](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/105) was merged as `18ee0ae46cb98725c7f59c0436611fa50e4581bf`. The current-main CI [41424009124](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41424009124) passed the IPA gold-corpus structure validation, Python tests, JS web checks and Vite build. Added responsive layout contract tests for control wrapping, Ukrainian-result priority, narrow-phone status and coverage overflow. The Pages workflow is configured for pushes to `main`; actual deployment completion and public-site smoke-test result remain **BLOCKED (external verification/network/DNS unavailable in this session)**. This UI change improves presentation only and does not improve linguistic accuracy. Independent adjudicated gold remains 0; accuracy remains null; research-prototype status is unchanged.

### Pages smoke-test compatibility follow-up — 2026-11-02

The cache-busted stylesheet URL introduced by the UI polish exposed an overly strict CSS-link extractor in the deployed-site smoke test. Fixed in PR [#106](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/106), merge `7ee049aae9cc7ff571b21eabe18e962627f192a3`; the extractor now accepts an optional query string. PR CI passed (41424681328). The Pages workflow is now compatible with the deployed CSS URL. The post-merge Pages deployment and live-site smoke-test result are still **BLOCKED for independent verification** because external DNS/network access and a workflow-run listing endpoint were unavailable; do not infer deployment success from a merged PR or a successful pull-request CI run.


## Khmer production browser-output hotfix — 2026-11-03

| ID | Status | Evidence | Remaining acceptance |
|---|---|---|---|
| KHM-WEB-RESULT-RENDER-001 | PARTIAL | On current `main` (`7b0a8f8c8661707afd9f0c58a94e2678789adf86`), `src/main.js` dereferences `#source-result` although `index.html` intentionally has no such element; every non-empty render therefore throws before result panels update. PR [#108](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/108) removes only this stale write and adds three Chromium tests. Exact pre-documentation head `aad9ce32378594c0da6651e7fba757ce0dfe40f0`: Quality checks [41533500652](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41533500652) SUCCESS; browser smoke [41533500956](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41533500956) SUCCESS, 3/3. | Fresh CI must pass on the documentation-updated PR head; merge #108; confirm Pages deployment; exercise non-empty input on the published URL and verify no uncaught browser errors. No production fix is claimed before merge/deploy. |

The automated regression verifies: (1) `ក` visibly renders IPA `/kɑː/` and Ukrainian `ка` with no uncaught page error; (2) mixed unsupported input remains visibly withheld; (3) clear returns to the empty state. This is UI engineering evidence only; it does not alter phonology, IPA labels, gold data, or linguistic accuracy. Independent adjudicated gold remains 0 and accuracy remains null.


## New source-level evidence — Phnom Penh Khmer profile and G2P comparators (2026-11-03)

| ID | Status | New evidence | Acceptance / limitation |
|---|---|---|---|
| KHM-PROFILE-SOURCE-001 | PARTIAL | Chem Vatho (2020), DOI [10.61945/cjbar.2020.2.2.3](https://doi.org/10.61945/cjbar.2020.2.2.3), one-page poster; 21 initially recruited, but acoustic results are from four Phnom Penh speakers (2 men, 2 women; 20–50), with reading tasks. F1/F2 and duration reported; normalization/method details and some measurements are internally unclear. | Supports limited vowel-profile context only. Not a representative dialect sample or evidence for consonants, tone, codas, or a complete G2P. Seek stronger multi-speaker primary studies. |
| KHM-PP-DIALECT-SOURCE-001 | PARTIAL | Sakamoto (1968), DOI [10.20495/tak.6.2_290](https://doi.org/10.20495/tak.6.2_290), principally one Phnom Penh informant; records style-sensitive weak syllable behavior and proposed ST/PP correspondences. | Treat as single-informant descriptive analysis; compare with modern multi-speaker evidence before generalizing. Keep the selected careful-citation profile explicit. |
| KHM-G2P-2019-EVIDENCE-001 | PARTIAL | Sar & Tan (2019), DOI [10.1016/j.procs.2019.11.140](https://doi.org/10.1016/j.procs.2019.11.140), reports PER 23.2% → 11.1% after vowel-tag features. | Comparator only until primary-paper split, profile, lexicon provenance, phoneme convention and rights are inspected. Published PER is not this repository's accuracy. |
| KHM-GOLD-PILOT-001 | BLOCKED | No gold labels or adjudications created by this source audit. | Requires profile-specific lexical sampling, frozen IPA convention, two independent qualified annotators, separate adjudicator, source locators and rights-cleared packets. Gold remains 0; accuracy null. |

No source in this audit licenses deterministic colloquial /r/-loss for the careful-citation profile. No IPA values or production phonology changed.


## Manifest-wide split identity — rebased integration — 2026-11-03

**Status: PARTIAL pending exact-head verification of the rebased port.** Ported PR #109's runtime validator/generator invariant and regression tests onto current `main` after the Khmer browser fix and handoff merges. The implementation must be verified on this clean branch before being marked DONE_VERIFIED.

- One frozen `(seed, version)` pair is enforced across the entire manifest; new groups inherit it; explicit conflicting/empty overrides fail; a new identity requires a separate empty input manifest.
- Original PR-head CI [41639679611](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41639679611) succeeded, but does not verify this rebased branch.
- No IPA gold rows were added; adjudicated gold remains 0 and empirical accuracy remains `null`.


## Khmer source evidence and benchmark reconciliation — 2026-11-03

**Status: PARTIAL pending exact-head verification of the clean port.** Ported the source-registry, references, research audit, collection playbook and provenance-test changes from PR #110 onto latest main, preserving PR #112's manifest-wide split protocol while adding the distinct agreement-metric boundary.

- Original PR-head Quality workflow [41640011541](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41640011541) succeeded; this clean port needs fresh exact-head checks.
- Dataset-item rights remain scoped only to those specific DataShare items. No IPA labels imported; independent gold remains 0 and accuracy remains `null`.


## KHM-PROFILE-001 — rebased single careful-citation profile — 2026-11-03

**Status: PARTIAL pending exact-head verification and specialist approval.** Reapplied the single-profile runtime/UI change to the latest main after source-citation integration. Only `khmer-pph-careful-citation-v1` is accepted; deterministic colloquial /r/-loss rewriting is removed.

- The profile is a bounded project decision, not a universal standard. Chem (2020) supports the careful formal-reading elicitation style but not full lexical coverage.
- Original #114 tests passed; the rebased branch needs fresh exact-head CI. Independent gold remains 0 and empirical accuracy remains `null`.


## KHM-AGENT-CONTEXT-001 — glossary and codebase navigation — 2026-11-03

**Status: PARTIAL pending exact-head CI.** Added `GLOSSARY.md`, `docs/agents/codebase-map.md`, `docs/agents/issue-tracker.md` and updated `AGENTS.md` with current code/data-flow and issue-management guidance.

- The map explicitly distinguishes the IPA-first phonetic path from the separate orthographic route and calls out high-risk seams, generated artifacts and fail-closed contracts.
- Documentation/process change only; no linguistic labels or code behavior changed. Independent gold remains 0; accuracy remains `null`.


## Continuation status sync — 2026-11-03

- Current main: `d8419d3099a8047d819a5a71cb5c4ef927db435e`; profile/runtime exact-main Quality 41646838970, Chromium 41646838756 and Pages/deployed smoke 41646838884 all succeeded. The later commit adds agent glossary/map documentation.
- PRs #107 and #114 were closed without merge because their profile/runtime/test changes are byte-identical to main; #108 and #111 were merged. Stale documentation PR #117 was closed after main advanced; this replacement branch is based on current main.
- Engineering improvements are verified; manual accessibility QA remains partial.
- IPA gold remains 0; empirical accuracy remains null. Annotation staffing, convention approval, rights clearance, blind intake and adjudication remain blocked on external human/evidence dependencies.


## KHM-METHOD-REFRESH-001 — methodology upstream snapshots — 2026-11-03

**Status: DONE_VERIFIED (reference audit).** Rechecked upstream default branches and release pins: Superpowers v7.0.1 at `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b`; mattpocock/skills release v1.3.2 at `d1478fcb140db0b93c0c8df17bcfd311844749d0` and current main snapshot `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`; Ponytail v5.3.3 at `7801d061243d7b753bad0e0b3c057cd250b11755`, with current main `96608e078b2d5ea607c5c3b8b5a54d1c1fba6846` adding only a README/product-list note after the method pin.

- These are methodology references, not runtime dependencies. No upstream skill files were copied into the application.
- Remaining linguistic evidence and rights gates are unchanged; gold 0, accuracy null.

## 2026-11-03 — held-out benchmark split enforcement

| Task | Status | Evidence / remaining acceptance |
|---|---|---|
| IPA-BENCH-SPLIT-001 | DONE_VERIFIED (engineering contract) | Export preserves the frozen group-safe split; scorer defaults to test and requires explicit selection for train/dev/all. Exact-head Quality [41651903776](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41651903776) SUCCESS on `ca53d628ae9a9ea4696fc85f42cdf59bcedfa2d1`. This fixes the evaluation boundary, not linguistic gold. |

Independent gold remains 0 and accuracy remains null. No data labels were fabricated. The split-aware benchmark documentation is in `docs/benchmarking-and-external-ipa.md`.

## Frozen split manifest provenance — 2026-11-03

The export and benchmark now preserve and validate the complete frozen split identity, not only the bucket name: `split`, `split_seed`, and `split_version`. Every adjudicated row must carry non-empty seed/version metadata, and the benchmark rejects a TSV that mixes manifest identities. The report exposes the manifest seed/version and selected scoring split. This makes the evaluated test partition traceable to one exact manifest; it does not create linguistic gold or change the current zero-row accuracy status.


## 2026-11-03 — empty benchmark prediction input

| Task | Status | Evidence / remaining acceptance |
|---|---|---|
| IPA-BENCH-EMPTY-PREDICTIONS-001 | DONE_VERIFIED (engineering guard) | Header-only prediction TSV previously exited 0 and produced an empty `engines` object. Test-first regression failed on all three language repositories; the scorer now rejects an empty prediction dataset after checking gold and frozen split provenance. Missing individual predictions within a named engine remain denominator-counted. RED: [41655188132](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41655188132). Final exact-head quality checks: [41655492141](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41655492141) SUCCESS; browser smoke: [41655491334](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41655491334) SUCCESS. |


## 2026-11-03 — benchmark identifier validation

| Task | Status | Evidence / acceptance |
|---|---|---|
| IPA-BENCH-IDENTIFIERS-001 | DONE_VERIFIED (engineering guard) | Reject whitespace-only gold IDs, prediction IDs and engine names while preserving non-empty identifiers exactly. Test-first RED: gold-ID run 41660794382; prediction-ID/engine run 41662096875. Final exact-code-head CI: 41662242906 SUCCESS (164 Python tests + 50 subtests; 3 browser smoke tests passed). Browser smoke 41662242611 SUCCESS. No linguistic labels or accuracy claims were added. |

## Verified continuation checkpoint — 2026-11-03 (late session)

- Default branch base: `dcaad206805abaacb2079f60e892e37af2477aac`; continuation branch: `docs/current-state-checkpoint-20261103`.
- Latest mainline work retained: Unicode punctuation token-boundary fix (#126; merged as 2a2f1c55282e076d6c4e0640d80af1053783bd6b) and subsequent docs/audit checkpoint.
- Exact-main CI on the recorded default-branch head: Quality 41710756134; browser smoke 41710756111; Pages deploy 41710756094; all listed runs completed with SUCCESS. These are CI checks for the current implementation and deployment, not phonetic validation.
- Open pull requests: none at checkpoint time. No upstream methodology repository was modified; Superpowers, Matt Pocock Skills and Ponytail remain process references only.
- Engineering task ledger: benchmark split provenance, empty-prediction rejection and whitespace-only identifier validation remain **DONE_VERIFIED** as input-integrity safeguards. The recently merged runtime fix is verified by its own regression/CI; no new linguistic rule is inferred from it.
- Linguistic task ledger: independent adjudicated IPA gold remains **0**; gold export remains header-only and empirical accuracy remains `null`. The profile-specific IPA convention, two independent annotators, separate adjudicator, curator/blind intake and item-level rights review remain **BLOCKED** on external human decisions/resources. No labels or source-derived pronunciations were fabricated.
- Manual deployed-site keyboard, screen-reader, responsive and mobile QA remains **TODO**; automated browser checks do not satisfy these acceptance criteria.
- Local test execution was not available in this connector-only session. Verification evidence is the linked GitHub Actions CI on the exact recorded main SHA; do not report local tests as run.


## Research unblock checkpoint — 2026-11-03

- Prospective language-specific expert/researcher leads and additional candidate resources are recorded in docs/ipa-gold-collection-playbook.md with primary-source links and explicit limits.
- These are leads only: no one has been contacted or recruited; no IPA convention has been approved; no rights have been granted; no IPA labels were generated.
- The 30-item pilot remains BLOCKED until the acceptance conditions in the playbook are met. Candidate lexicon entries, phonetic respellings, model outputs, orthographic transcripts and source descriptions are not gold IPA.
- The next external action is to contact a qualified prospective reviewer and request nominations for two independent annotators plus a separate adjudicator; separately complete item-level rights review and blind-intake dry run.


## Khmer acoustic-model dictionary follow-up — 2026-11-04

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHMER-ACOUSTIC-DICT-001 | PARTIAL / BLOCKED for reuse | Current upstream root README says 29,204 dictionary entries and CC BY-SA 4.0; `dictionary/README.md` says 33,091 entries and CC BY 4.0 for its G2P mapping. Current public tree contains only a six-line sample dictionary and no full dictionary or release asset. | Request full versioned dictionary + SHA-256, artifact-specific license clarification, dialect/IPA convention, source provenance and independent annotation/adjudication details. No import, training, gold promotion or license inference until resolved. |


## Khmer audio-backed IPA pilot source — 2026-11-04

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHMER-DDD-AUDIO-001 | PARTIAL (candidate audio source; pilot intake not yet approved) | Mozilla Data Collective Version 3 Part 1 reports 134.60h WAV + transcripts, 8 Cambodia-based native speakers (4F/4M), 13 topics/401 subtopics, origin-city metadata, CC BY-SA 4.0 and no-speaker-identification restriction. Source registered as `ddd-khmer-asr-cultural-v3-part1-2026`. | Verify exact speaker/profile/utterance metadata, select attested word spans with time locators, approve the target profile, review share-alike implications, then commission two blind IPA annotations plus separate adjudication. No IPA labels supplied; no gold import. |


## Post-merge checkpoint — DDD Khmer audio source (2026-11-04)

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHMER-DDD-AUDIO-001 | DONE_VERIFIED (source registry and evidence boundary); pilot use remains PARTIAL/BLOCKED | PR #135 merged as `ccd24f1f53dda8ccf19dbdbac0766ed4509f99e4`. PR-head Quality [41799786264](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41799786264) and [41799802512](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41799802512) SUCCESS; post-merge main Quality [41799887156](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41799887156), browser [41799887167](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41799887167), Pages [41799887180](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41799887180) SUCCESS. | Source record and restrictions verified. Still require profile review, word-span/time locators, CC BY-SA compatibility decision, two blind IPA annotators and adjudicator. No IPA gold added. |

## Post-merge checkpoint — Khmer acoustic dictionary discrepancy (2026-11-04)

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHMER-ACOUSTIC-DICT-001 | DONE_VERIFIED (discrepancy documented); reuse remains BLOCKED | PR #134 merged as `09640f83141127eeb5c9d201d96671d243d03019`; exact-head Quality [41799402432](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41799402432) SUCCESS; post-merge main Quality [41799595059](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41799595059), browser [41799595047](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41799595047), Pages [41799595094](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41799595094) SUCCESS. | The conflicting 29,204/33,091 counts and CC BY-SA 4.0/CC BY 4.0 claims are recorded; full dictionary and author clarification still required. |


## Common Voice 27.0 Khmer audio source — 2026-11-04

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHMER-CV27-AUDIO-001 | PARTIAL (secondary audio lead; profile screening required) | Mozilla provider record: CC0-1.0; 739 clips/0.98h total, 213 validated/0.28h, 15 speakers, 4,971 sentences (364 validated); 483 unresolved, 43 invalidated; accent values blank, gender unreported; no speaker identification or re-hosting/re-sharing. | Use provider-hosted validated clips only; approve target variety, select exact word-span/time locators, then double IPA annotate and adjudicate. No audio mirror or gold import. |


## Post-merge checkpoint — Khmer audio sources and corpus evidence (2026-11-04)

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHMER-ACOUSTIC-DICT-001 | DONE_VERIFIED (discrepancy documented); reuse remains BLOCKED | PR #134 merged `09640f83141127eeb5c9d201d96671d243d03019`; PR-head Quality [41799402432](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41799402432), post-merge Quality [41799595059](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41799595059), browser [41799595047](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41799595047), Pages [41799595094](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41799595094) SUCCESS. | Conflicting counts 29,204/33,091 and CC BY-SA 4.0/CC BY 4.0; no full public dictionary. Reuse blocked pending exact artifact, checksum, rights and provenance. |
| KHMER-DDD-AUDIO-001 | DONE_VERIFIED (source registration); pilot use remains PARTIAL/BLOCKED | PR #135 merged `ccd24f1f53dda8ccf19dbdbac0766ed4509f99e4`; PR-head Quality [41799786264](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41799786264), [41799802512](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41799802512), post-merge Quality [41799887156](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41799887156), browser [41799887167](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41799887167), Pages [41799887180](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41799887180) SUCCESS. | 134.60h Part 1, 8 speakers, CC BY-SA 4.0; city metadata does not establish Phnom Penh. Word-span/time locators and share-alike review required. |
| KHMER-CV27-AUDIO-001 | DONE_VERIFIED (source registration and restrictions); pilot use remains PARTIAL/BLOCKED | PR #137 merged `98e66afecbce5528850e3a6906a8d9522385d3ed`; PR-head Quality [41800424004](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41800424004) and [41800443113](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41800443113), browser [41800443035](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41800443035), post-merge Quality [41800575946](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41800575946), browser [41800575935](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41800575935), Pages [41800575937](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41800575937) SUCCESS. | CC0-1.0 but no speaker identification or re-hosting/re-sharing; 739 clips/0.98h, only 213 validated/0.28h; 15 speakers, no accent/gender data. Not a standalone benchmark. |


## Language-specific IPA test fixtures — 2026-11-04

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHMER-IPA-GOLD-FIXTURE-001 | DONE_VERIFIED | PR [#139](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/139) merged as `ed42f9ebfe617d1278949532ecd3d81fad652f7e`; exact-main Quality [41847860271](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41847860271), browser [41847860415](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41847860415), Pages/deployed-site smoke [41847860699](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41847860699) SUCCESS. | Test fixture now uses Khmer script and neutral test profile; regression asserts Khmer Unicode-block and matching profile metadata. This validates test-fixture integrity only, not phonological rules or IPA accuracy. Gold remains 0; accuracy null. |


## External Khmer pronunciation-source triage — 2026-11-04

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHMER-EXT-IPA-DICT-001 | DONE_VERIFIED (source located and scoped; no import) | Pinned `open-dict-data/ipa-dict` commit `972cd67dd5f96bc5660e28070cde26e3928abcd7`; Khmer file `data/km.txt` (3,286 lines); upstream README attributes Khmer data to aakanee.com Khmer-English Dictionary and CC BY-NC-SA 4.0. Registered as `open-dict-ipa-km-2026`. | External comparator only. Profile, IPA convention and per-entry annotation provenance not established; non-commercial/share-alike restrictions must be reviewed. Not project gold. |
| KHMER-EXT-RESP-001 | DONE_VERIFIED (source located and classified; no import) | PhonSobon Khmer G2P: 38,629 word–pronunciation pairs / 37,755 unique words, split by word; pronunciation is Khmer-script respelling, not IPA. Combined pronunciation dictionary: 39,110 rows and 689 disputed items, including 39 LLM-assisted decisions that require native confirmation. Registered as `phonsobon-khmer-g2p-2026` and `phonsobon-khmer-pronunciation-2026`. | Candidate orthographic/syllabification comparator only; NCKL source rights and commercial/redistribution terms unresolved. No conversion to IPA by assumption. |
| KHMER-ACOUSTIC-DICT-RECHECK-001 | PARTIAL / BLOCKED | Upstream main commit `2714994b41ccf875c5b6f6182b48a72f13632dbf`: README claims 29,204 IPA entries and CC BY-SA 4.0; visible tree has only six sample lines; separate dictionary README says CC BY 4.0 for a 33,091-entry mapping. Registered as `chemvatho-khmer-acoustic-model-2026`. | Obtain full versioned dictionary + digest, reconcile artifact counts and licenses, confirm profile, provenance and annotation/adjudication method. No import. |

**Evidence boundary:** no external data were copied. These source-triage tasks are complete as research records, not as phonological gold. Independent expert-adjudicated Khmer IPA gold remains 0; empirical accuracy remains null.


## IPA gold release-gate profile consistency — 2026-11-04

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| IPA-GOLD-RELEASE-PROFILE-001 | DONE_VERIFIED (engineering guard) | Shared `scripts/ipa_gold_corpus.py` now rejects adjudicated corpora that mix target-profile identity (`id`, `variety`, `region`, `register`) or IPA kinds. New regression tests cover both failures. PR #141 merged as `4ba59abdc389a797c58216e4e155b8b06408c557`; exact PR-head CI [41870121484](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41870121484) SUCCESS; exact PR-head browser smoke [41870121371](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41870121371) SUCCESS; post-merge CI [41870545200](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41870545200) SUCCESS; Pages [41870545069](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41870545069) SUCCESS. | Does not prove profile approval, annotator qualifications, blindness, linguistic contrast coverage, or IPA accuracy. A specialist-reviewed language-specific coverage report remains required before benchmark readiness. |


## Expert recruitment lead revalidation — 2026-11-04

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHMER-IPA-GOLD-RECRUITMENT-LEADS-001 | PARTIAL | The current UW profile verifies Nielson Hul's Khmer phonetics/voice-quality/sociophonetic research and public institutional email; University of Cologne 2026 profile verifies Vatho Chem's 2025 PhD in Phonetics focused on Central Khmer reduction and dialect fieldwork. Both are prospective reviewer leads only; Chem's relationship to his own acoustic-model resource must be disclosed and he must not be sole adjudicator of its data. | No candidate has been contacted, consented, recruited or approved. Close only after two independent qualified target-variety annotators, separate adjudicator, non-annotating curator, conflict checks, secure blind intake and written role/terms confirmation are documented. |

## Deterministic rule engine — 2026-11-11

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHMER-DETERMINISTIC-RULE-ENGINE-001 | DONE_VERIFIED (engineering); linguistic coverage PARTIAL | PR #152 merged as `913e1b2a117022eb3350c3d1957680f0b5db0661`. Exact main Quality [43018004334](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43018004334), browser [43018004167](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43018004167), and Pages + asset smoke [43018004186](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43018004186) SUCCESS; live site: https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System-/. | Deterministic rule contract and publication verified. PROPOSED remains a proposal; expert-adjudicated Phnom Penh IPA gold is still required for correctness/accuracy claims. |

## Final deterministic-engine verification — 2026-11-11

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHMER-DETERMINISTIC-RULE-ENGINE-001 | DONE_VERIFIED (engineering); linguistic coverage PARTIAL | Final main head `7585b49fdaac5480940d2511f48961f7690bf6b5`; exact-head Quality [43019207054](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43019207054), browser [43019207032](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43019207032), Pages + smoke [43019207026](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43019207026) SUCCESS. | Deterministic implementation and publication verified. Independent expert-adjudicated Phnom Penh IPA gold remains necessary for broader correctness/accuracy claims. |


## 2026-11-11 — Ukrainian practical adapter continuation

| Work item | Status | Evidence / acceptance |
|---|---|---|
| Whole-IPA longest-match Python adapter integrated after Khmer IPA | DONE_VERIFIED | \`src/khmer_ua/practical.py\`, deterministic engine; quality CI 43094688835 |
| Shared browser adapter with actual yotation, /w/ and affricate tests | DONE_VERIFIED | \`src/ukrainian-practical.js\`, \`src/main.js\`, \`tests/web-engine.test.mjs\`; browser CI 43094688837 |
| Ukrainian target distinctions /h, ɦ/ → г, /ɡ/ → ґ, /x/ → х | DONE_VERIFIED | Policy v2026-11-11.3; note /ɡ/ → ґ is a project choice, while the 2026 standard generally uses г for foreign [g] |
| /w/ → в, syllable-initial /j/ yotation, affricates and /cʰ/ → ть' | DONE_VERIFIED | Machine-readable policy and regression tests |
| Linguistic accuracy of the proposed practical correspondences | PARTIAL | No independent adjudicated text gold set yet |
| Independent text-only Khmer IPA/Ukrainian gold set | BLOCKED | Requires sourced IPA entries, dialect/profile scope, independent annotation/adjudication and held-out evaluation |
| Audio corpus | DEFERRED | Not required for the current text-only scope |


## Practical adapter verification refresh — 2026-11-11

| Work item | Status | Evidence / acceptance |
|---|---|---|
| IPA → Ukrainian Python/browser mapping contract | DONE_VERIFIED (implementation) | Canonical policy v2026-11-11.3; whole-string longest-match adapter; fail-closed unknown IPA; h/g/x, affricates, aspiration, yotation and /w/ target distinctions |
| Expanded browser policy regression coverage | PARTIAL pending exact-head CI | `tests/web-engine.test.mjs` now exercises spaced IPA, h/g/x, affricates, untied consonant sequences, cʰ, yotation and unknown-segment withholding; exact-head Quality [43095329118](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43095329118) and browser [43095329245](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43095329245) are queued |
| Documentation consistency | DONE_VERIFIED | README, system page, implementation, validation and practical transcription specification aligned; /w/ → в corrected in summary table; sole active profile documented |
| Independent text-only Phnom Penh IPA/Ukrainian gold | BLOCKED | No independently sourced/adjudicated text labels available; acceptance requires a rights-cleared held-out text lexicon with dialect/profile scope, independent IPA annotation/adjudication and error/abstention report |
| Audio validation | DEFERRED | Not required for this text-only task |


## Provisional onset IPA fallback — 2026-11-11

| Work item | Status | Evidence / acceptance |
|---|---|---|
| Python onset-only preview for unresolved Khmer units | PARTIAL | Separate provisional_ipa/provisional_ukrainian/fallback_status/fallback_trace; canonical ipa/ukrainian unchanged; regression for កា. Commit 352c22a55f526877dd136a982b2aa5ac03ff3838 |
| Browser onset-only preview | PARTIAL | Same onset IPA → existing adapter → ? behavior; per-unit PROVISIONAL status. Commit 862aa061726b2bae6296199e4b655334bb6f609a |
| Browser regression | PARTIAL | Source-contract assertions added; not yet an executable cross-runtime parity fixture. Commit 660915e4ed1f44eab04258957eee39537883aadd |
| Dedicated grapheme-position evidence registry | TODO | Register primary-source locator, profile, exact position, rule ID, scope and reviewer status for each provisional mapping |
| Exact-head CI and Chromium verification | BLOCKED pending run | Runs 43099931373 and 43099931284 were queued; neither is verified as passed |
| Full provisional vowel/subscript/coeng fallback | TODO | Only consonant onset hints are implemented; require independently sourced positional evidence before extending |


## Verification result — provisional onset preview, 2026-11-11

| Work item | Status | Evidence |
|---|---|---|
| Python fallback implementation and regression | DONE_VERIFIED (engineering behavior) | Exact code/test head dbdb8beafc3454e6bb0be848011f90fb0dea190b; Quality run 43101322383 PASS: 189 tests + 62 subtests |
| Browser preview wiring and source-contract checks | DONE_VERIFIED (engineering behavior) | Quality run 43101322383 web checks PASS; production build PASS |
| Browser visible-result smoke | DONE_VERIFIED | Chromium run 43101322537 PASS |
| Full positional evidence registry and language-wide fallback | TODO / PARTIAL | Current implementation is onset-only and keeps canonical output fail-closed; exact source locators and position-specific inventory still required |
| Functional Python/browser parity fixture | TODO | Current browser assertions are source-contract checks, not shared structured fixture parity |


## Unicode grapheme accounting sweep — 2026-11-12

| Work item | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHMER-UNICODE-ACCOUNTING-001 | DONE_VERIFIED (structural/input accounting) | PR #157 merged as `e9c9d997e6de1029fd0b8fef9e7b6a9cb0020a4f`; exact-head Quality [43184648039](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43184648039) and browser smoke [43184647978](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43184647978) SUCCESS. Exhaustive sweep covers assigned Unicode L/M code points in U+1780–17FF and U+19E0–19FF. | Every tested code point is losslessly retained and traced. Malformed COENG remains visible as invalid structure. Does not imply phonological/IPA coverage or correctness. |
| KHMER-PHONOLOGY-100-001 | PARTIAL / BLOCKED by evidence | Existing vowel × series report remains first-order only; positional coda/profile cells and independent gold remain incomplete. | Requires source-located vowel × series × length × coda × profile evidence, independent expert adjudication, and held-out gold before expanding canonical IPA rules. |


## Khmer unmodelled-letter inventory and trace preservation — 2026-11-12

| Work item | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHMER-UNMODELLED-LETTERS-001 | DONE_VERIFIED (inventory classification only) | PR #159 merged as `d1d184334c806cd21cf2eb875a9c5151ab9e61b3`; exact-head Quality [43186170402](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43186170402) and browser smoke [43186170525](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43186170525) SUCCESS. U+17A3, U+17A4, U+179D, U+179E are explicitly registered as `unmodeled_letter`. | Explicitly accounted for, not pronounced. No IPA or Ukrainian value is assigned. |
| KHMER-TRACE-TAIL-001 | DONE_VERIFIED (source integrity) | Same PR and exact-head CI; regression `កxយ` preserves all graphemes after the unsupported `x`. | Unknown material no longer truncates the detailed parser trace. |


## BGN/PCGN Latin → Ukrainian target matrix — 2026-11-12

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-UA-TARGET-001 | DONE_VERIFIED | Branch `feat/khmer-romanization-ukrainian-matrix-completion-2026-11-12`; exact-head Quality [43221517618](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43221517618) and browser smoke [43221517788](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43221517788) both SUCCESS; push Quality [43221506380](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43221506380) SUCCESS. The final Python suite reported 194 passed + 62 subtests. All 22 consonant and 37 vowel/rime target rows are populated and covered by tests. | Table coverage verified; project orthographic rendering only, not IPA or expert-approved national standard. Runtime adapter and contextual BGN/PCGN engine remain open. |
| KHM-ROM-UA-001 | TODO | No runtime Latin → Ukrainian adapter integrated. | Separate adapter consumes BGN/PCGN string, preserves source/Latin/UA trace and uncertainty, and does not call IPA adapter. |


## Khmer Ukrainian target matrix — post-merge evidence — 2026-11-12

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-UA-TARGET-001 | DONE_VERIFIED | Merged PR [#161](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/161), merge `6b0d0e75d794165e5eb935192fab0926e1efca39`; mainline Quality [43221967799](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43221967799), browser [43221968144](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43221968144), Pages [43221967939](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43221967939) all SUCCESS. | 22 consonant + 37 vowel/rime target rows are covered. Runtime adapter and full contextual BGN/PCGN engine remain separate open tasks. |


## Khmer romanization Ukrainian runtime adapter — 2026-11-12

| ID | Status | Evidence | Remaining acceptance |
|---|---|---|---|
| KHM-ROM-UA-TARGET-001 | DONE_VERIFIED | 22 consonant + 37 vowel/rime target rows; merged PR #161; prior exact-head matrix CI passed. | No remaining table-row blanks in the inventoried target matrix. |
| KHM-ROM-UA-001 | PARTIAL | PR #164 adds `src/khmer-romanization-ukrainian.js`, app integration, and browser regression `សុខា → Sokha → Сок'а`. Exact-head Quality [43226337969](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43226337969), browser [43226337956](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43226337956), push Quality [43226325685](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43226325685) SUCCESS. | The current upstream ASCII romanizer drops BGN/PCGN diacritics; contextual vowel variants cannot be reconstructed. Need diacritic-preserving source output or a context-aware source-syllable romanizer before full-standard acceptance. |
| KHM-ROM-ENGINE-001 | PARTIAL | Upstream package documents its ASCII profile as BGN/PCGN-derived, with diacritics dropped and non-conformance. | Implement or adopt a validated, diacritic-preserving BGN/PCGN 1972 engine; test all contextual vowel, coda and shifter cases. |

The adapter is intentionally labelled `PROVISIONAL`. It is orthographic Latin-to-Ukrainian rendering, not IPA or pronunciation transcription.



## Khmer romanization runtime — mainline post-merge verification — 2026-11-12

- PR [#164](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/164) merged as `0ba6107a7e5cb09cca44021669a7401fc125eac4`.
- Mainline Quality [43227360792](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43227360792), browser smoke [43227360789](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43227360789), and Pages deployment [43227360801](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43227360801) all SUCCESS.
- The merged implementation remains deliberately PARTIAL/PROVISIONAL: the upstream ASCII romanizer omits PCGN diacritics; this adapter cannot reconstruct lost contextual vowel distinctions. The IPA route remains separate.


## Romanization runtime mainline reconciliation — 2026-11-12

### Cambodian national romanization profile evidence — 2026-11-12

The primary 1995/1997 system table is now located in the Ministry's 2023 provisional Gazetteer (pp. vii–viii). The foreword says the Geography Department used the system and would submit it for consideration and adoption; the edition remained provisional pending National Commission approval. Cambodia's national report and UNGEGN 2025 report confirm gazetteer use, while the UK PCGN May 2026 Factfile says the system is not yet consistently implemented. Treat this as provisional use with formal-adoption/implementation status still EVIDENCE_LIMITED, not as a missing primary table. The PDF is copyright © 2023 by the Geography Department; the ODC mirror record states no license for the PDF. The similarly dated ALA-LC Khmer table is a separate cataloguing system.

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-NATIONAL-1997-001 | EVIDENCE_LIMITED | Primary table located in the 2023 provisional Gazetteer pp. vii–viii; foreword states use by the Geography Department and pending submission/adoption. Cambodia/UNGEGN reports confirm gazetteer use; PCGN 2026 says not consistently implemented. | Confirm formal adoption/consistent implementation and resolve reuse rights; transcribe and independently verify the primary table, then decide whether to add a separate profile. Do not relabel BGN/PCGN 1972 rows. |


| ID | Status | Current evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-UA-TARGET-001 | DONE_VERIFIED | 22 consonant + 37 vowel/rime rows have Ukrainian target candidates; PR #161 merged; exact mainline Quality/browser/Pages checks on `a86a59cf082d547563b45374ced9dfb45c5cd8db` passed: [43228414756](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43228414756), [43228414938](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43228414938), [43228414646](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43228414646). | Table coverage only; all Ukrainian candidates remain project proposals. |
| KHM-ROM-UA-001 | PARTIAL | PR #164 merged as `0ba6107a7e5cb09cca44021669a7401fc125eac4`; separate runtime adapter and UI are live; unknown fragments are visibly withheld and IPA route is separate. | Replace the lossy ASCII romanizer or implement a contextual BGN/PCGN source-syllable path. |
| KHM-ROM-ENGINE-001 | PARTIAL | `@gmana/km-translit` 0.1.2 is documented as BGN/PCGN-derived ASCII and drops diacritics. | Demonstrate full standard-conformant contextual romanization, including series, vowel, shortening, coda and diacritic behavior. |

The phonetic route and its IPA boundary are unchanged. No new IPA labels, gold entries, or accuracy claims were added. Independent expert-adjudicated IPA gold remains 0.

The 2025 UNGEGN Asia South-East Division report further confirms that the October 2023 national gazetteer published by Cambodia's General Department of Cadastre and Geography uses the 1997 transcription system (GEGN.2/2025/73/CRP.73, p. 3). This is later corroboration, not a copy of the primary 1997 specification.


## Khmer romanization adapter test discovery — 2026-11-12

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-TEST-001 | PARTIAL | PR #167 merged as `f0485892f5d4b16e5fbe0ded6f8e083d8b044f4b`; the adapter unit suite is now included in `npm test` and `npm run check`. It asserts all 22 distinct consonant romanization tokens and the 33 ASCII vowel candidates. Exact-main Quality [43250158336](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43250158336) and browser smoke [43250158628](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43250158628) passed. | Add complete source-matrix→runtime parity, real upstream romanizer corpus tests, marks/numerals and contextual diacritic-preserving profile coverage. |

The unit-test discovery gap is closed. This does not resolve the lossy ASCII romanizer, the national 1997 profile blocker, or the proposed status of Ukrainian mappings.

## Auxiliary external source triage — 2026-11-15

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHMER-PHONSOBON-001 | PARTIAL (source recorded; not integrated) | PhonSobon model card reports 83.37% validation word accuracy for a 7.46M-parameter Khmer-script respelling model; dataset card reports 38,629 NCKL-derived respelling pairs and a word-level train/validation/test split. | Auxiliary respelling/syllabification only, never IPA or phonetic gold. NCKL redistribution/derivative/commercial terms must be clarified before data use; no rows or weights copied. |
| KHMER-ACOUSTIC-DICT-001 | BLOCKED | Pinned upstream review reports 29,204 vs 33,091 entry-count conflict, CC BY-SA 4.0 vs CC BY 4.0 data-license conflict, and only a six-entry sample in the inspected tree. | Obtain the full versioned dictionary and digest, reconcile counts and IPA conventions, verify item provenance and receive authoritative data-rights clarification. Alignment metrics do not establish G2P accuracy. |

**Research boundary:** neither candidate adds independent adjudicated IPA gold. Gold remains 0 and empirical accuracy remains null.

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHMER-GOOGLE-TTS-001 | PARTIAL (format and rights unresolved) | Pinned Google Language Resources files recorded; bounded lexicon extraction found Latin-script spelling keys in the inspected subset; companion phone inventory is feature-annotated. | Full-file script audit, Khmer-specific data license, dialect and IPA convention review required. Not accepted as Khmer-script G2P or standard IPA. |
| KHMER-OPENSLR42-001 | PARTIAL (audio lead; metadata discrepancy) | OpenSLR lists a male-speaker archive and CC BY-SA 4.0; 2018 paper reports 17 female speakers, 2,906 files and 3:58:00. | Obtain archive manifest/checksum, reconcile speaker metadata, verify included license and transcription scope. Audio/transcripts are not IPA gold. |

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHMER-MEKONGPHON-RULE-001 | PARTIAL (source inspected, not executed) | Pinned MekongPhon snapshot contains a separate rule-based Khmer-to-IPA baseline. | Verify source rights, dependencies, dialect/IPA convention and typed-candidate behavior before any execution or integration. No source copied. |

## Mainline verification closeout — external source reconciliation — 2026-11-15

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| PR153-RECONCILIATION-001 | DONE_VERIFIED | PR #187 merge `1ef8578143bd2a0e9d55a46c0ddef4d0006dc5c3`; PR #188 merge `34f9dbfd94788d1d1b9b64646354157d4741dfed`; exact-head Quality and Chromium workflows succeeded. PR #153 closed unmerged after selective port. | Engineering/documentation reconciliation only; no phonetic gold or external data rights are created by this work. |
| REPOSITORY-LICENSE-001 | BLOCKED (owner decision) | `pyproject.toml` declares MIT; root `LICENSE` is absent. | Owner must confirm intended project license before the canonical license text can be added. |

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHMER-PHONOTACTIC-SCOPE-001 | PARTIAL | Nacaskul (1978), Unicode L2/22-290 and Ding et al. (2018) are now classified by major/minor syllable type versus orthographic encoding. | Confirm current Phnom Penh profile with lexical and acoustic evidence before implementing global constraints; no exhaustive cluster/coda inventory yet. |
| KHMER-PPK-PITCH-2025-001 | PARTIAL | Mam et al. (2025) reports lower F0 groups for /r>h/ forms and voiced-onset disyllables in a five-speaker PPK sample. | Independent multi-speaker replication, perception evidence and profile-matched lexical data required; no universal tone rule or tone-bearing IPA labels added. |
| KHMER-ORTHOGRAPHIC-CHAINING-001 | DONE_VERIFIED (source contract and regression) | Unicode encoding analysis describes coeng chaining and mismatch between orthographic units and phonetic syllables; parser regression keeps phoneticization withheld. | Structural parser remains orthographic; a future phonetic syllabifier requires separate lexical/prosodic evidence. |

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHMER-ORTHOGRAPHIC-CHAINING-001 | DONE_VERIFIED (engineering boundary) | PR #190 merge `262d16fb755aff952fef42ecb69f8c8a8251df30`; 223 tests + 70 subtests and 4 Chromium tests passed on exact PR head. Parser regression preserves source graphemes and withholds phoneticization. | Verifies lossless structural trace only; does not establish a phonetic syllabifier or pronunciation. |
| KHMER-PHONOTACTIC-SCOPE-001 | PARTIAL | Nacaskul (1978), Unicode L2/22-290 and Ding et al. (2018) claims classified by major/minor type and orthographic vs phonological domain. | Contemporary profile-matched lexical/acoustic coverage and exhaustive cluster/coda inventory remain missing. |
| KHMER-PPK-PITCH-2025-001 | PARTIAL | Mam et al. (2025) bounded five-speaker, 50-word F0 study recorded in source registry. | Independent replication, perception evidence and speaker-balanced lexical coverage required; no universal tone mapping is accepted. |

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-LATIN-INPUT-001 | DONE_VERIFIED (direct-input path) | PR #192 merge `736b1bc30bc6ccea6eb1d9f3aacd0647c17b848f`; 223 tests + 70 subtests and 7 browser tests passed on exact head. Direct Latin BGN/PCGN input covers all 37 raw vowel/rime matrix rows. | Applies to Latin-only input assumed to be BGN/PCGN 1972; unknown fragments are bracketed. Does not reconstruct omitted diacritics or certify arbitrary romanization. |
| KHM-ROM-UA-001 | PARTIAL | Direct BGN/PCGN input is wired to the Ukrainian candidate layer. | Ukrainian targets remain PROVISIONAL; expert review and a defined Ukrainian standard are still required. |
| KHM-ROM-ENGINE-001 | PARTIAL | Direct Latin input is supported; Khmer-script input still uses ASCII @gmana/km-translit and loses diacritics. | A contextual, diacritic-preserving Khmer-script→BGN/PCGN generator and source-profile validation remain open. |
| KHM-ROM-TEST-001 | PARTIAL | Tests cover 22 consonant rows, 37 raw vowel/rime forms, direct input, unknown fragments and browser behavior. | Marks/numerals, broad upstream corpus and contextual Khmer-script romanizer parity remain open. |

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-MIXED-INPUT-001 | DONE_VERIFIED (input guard) | PR #194 merge `4e1b95f2a1680e7c7363a68b226b0b44778cac74`; exact-head Quality 223 tests + 70 subtests and 9 browser tests passed. | Mixed Khmer letters/marks plus Latin input is PARTIAL with explicit brackets; Khmer numerals/punctuation remain preserved. This is input-mode validation, not a romanization or linguistic accuracy claim. |

**Verification checkpoint:** PR #194 implementation merged as `4e1b95f2a1680e7c7363a68b226b0b44778cac74`; PR #195 documentation merged as `0d1183553a4851eb0c21336f381be3d0f2d0efaf`. Exact PR-head Quality and Chromium workflows passed; see the canonical master handoff for run IDs. These checks verify implementation and input handling, not linguistic correctness of Ukrainian target proposals.

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-UI-A11Y-SMOKE-001 | DONE_VERIFIED (automated smoke only) | PR #197 merge `9452ac70ee16973ac5f0e8bd28201501539409de`; exact-head Quality 223 tests + 70 subtests and 11 browser tests passed. | Covers key accessible names, method-switch Enter activation and polite live status. Does not replace manual screen-reader, full keyboard, contrast, zoom/reflow or mobile review. |
| KHM-UI-MANUAL-A11Y-001 | PARTIAL | Hosted Chromium smoke exists; PR #197 added automated semantics/keyboard assertions. | Manual screen-reader, complete keyboard, contrast, zoom/reflow, mobile and assistive-technology audit remains required. |


## Exact-main CI and PR-state checkpoint — 2026-11-15

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| MAINLINE-CI-2026-11-15 | DONE_VERIFIED (engineering CI only) | Main SHA `14c87c275a3dcc599893da19b455b2e853abb630`; post-merge Quality [43710193628](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43710193628), Chromium [43710193653](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43710193653), Pages [43710193633](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43710193633) all SUCCESS. | Hosted engineering/build/deployment checks only; not linguistic accuracy, legal clearance or manual accessibility approval. No local tests claimed. |
| PR153-RECONCILIATION-001 | DONE_VERIFIED (selective source-record preservation) | PR #153 CLOSED unmerged; current comparison is diverged, 34 ahead / 48 behind. Useful source-triage records are already preserved by PRs #187/#188. | Do not merge stale runtime or duplicated benchmark workflow. Source branch left untouched. |
| KHM-UI-MANUAL-A11Y-001 | PARTIAL | Automated smoke is merged and exact-main Chromium is green. | Human screen-reader, full keyboard, contrast, zoom/reflow, mobile and assistive-technology review remains required. |
| KHM-GOLD-001 | BLOCKED | Open issue #104 still requires expert-approved convention, two qualified annotators, independent adjudicator, curator, blind intake, 30 attested groups, rights review and independent adjudication. | No gold/accuracy claim until controlled pilot and validation are complete. |

**Current mainline:** `14c87c275a3dcc599893da19b455b2e853abb630`; no open PRs. Root `LICENSE` is still absent while `pyproject.toml` declares MIT; retain as an owner decision. Repository remains a partial research prototype, not production-ready.


## Current-main evidence ledger — 2026-11-15 (89e5ba4)

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| MAINLINE-CI-2026-11-15-B | DONE_VERIFIED (engineering only) | Current main `89e5ba49c7507f60b421119cbae4b63c240ac3c8`; Quality [43712699599](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43712699599), Chromium [43712699648](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43712699648), Pages [43712699614](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43712699614) all SUCCESS on this exact SHA. | Confirms hosted corpus validation, Python/web tests, production build, Chromium visible-results smoke and Pages deploy; no local execution or linguistic accuracy claim. |
| PR153-RECONCILIATION-002 | DONE_VERIFIED (historical disposition) | PR #153 CLOSED unmerged; current comparison to main: 34 ahead / 49 behind, diverged; safe source triage preserved in #187/#188. | Do not merge its stale runtime or duplicate workflow. |
| PR64-RECONCILIATION-001 | DONE_VERIFIED (historical disposition) | PR #64 CLOSED unmerged; historical CSS snapshot is superseded by focused UI work. | Reopen/reimplement only if a fresh audit establishes a concrete missing UI behavior. |
| KHM-GOLD-001 | BLOCKED | Issue [#104](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/104) remains open; independent adjudicated gold=0; `gold.tsv` remains header-only. | Requires approved IPA convention, two qualified annotators, independent adjudicator, curator, blind intake, rights-cleared 30 lexeme groups and adjudication. |
| KHM-UI-MANUAL-A11Y-001 | PARTIAL | Automated Chromium smoke is green on current main. | Human screen-reader, full keyboard, contrast, zoom/reflow, mobile and assistive-technology review remains outstanding. |
| REPOSITORY-LICENSE-001 | BLOCKED (owner decision) | `pyproject.toml` declares MIT; root `LICENSE` absent. | Owner must confirm intended license before adding canonical license text. |

**Readiness:** engineering pipeline verified green on current main; linguistic accuracy, data/legal rights and manual accessibility gates remain open. Repository is a partial research prototype, not production-ready.


## Romanizer output-integrity regression closeout — 2026-11-15

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-OUTPUT-GUARD-001 | DONE_VERIFIED (fail-closed output guard) | PR #201 merge `37a536592a8e462f00997890af63ad232d41a0ae`; exact-head Quality [43720084983](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43720084983) and Chromium [43720085021](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43720085021) SUCCESS; exact-main Quality [43720186392](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43720186392), Chromium [43720186338](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43720186338), Pages [43720186436](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43720186436) SUCCESS. | Residual Khmer letters/marks after upstream rendering are bracketed and produce PARTIAL; punctuation is preserved. Does not repair lost diacritics or implement contextual PCGN romanization. |
| KHM-ROM-ENGINE-001 | PARTIAL | Output-integrity guard merged; upstream Khmer-script romanizer still emits ASCII-derived output with diacritics omitted. | Contextual consonant-series, shortening, coda and diacritic-preserving Khmer-script → BGN/PCGN generator still required. |
| KHM-ROM-TEST-001 | PARTIAL | New residual-letter/mark regressions added and exact-main CI green. | Full contextual romanizer parity, mark semantics, broad attested corpus and expert review remain open. |

**Current main:** `37a536592a8e462f00997890af63ad232d41a0ae`. This guard improves output honesty, not linguistic coverage or readiness.


## Final mainline checkpoint — 2026-11-15 (PR #201/#202)

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| MAINLINE-CI-2026-11-15-C | DONE_VERIFIED (engineering and deployment only) | Main `1cc833ad1097f6b1ee7c28eb3e7aefb99ad480fb`; Quality [43720449189](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43720449189), Chromium [43720449188](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43720449188), Pages [43720449180](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43720449180) all SUCCESS on exact main. | Hosted Python/web tests, build, Chromium visible-results and Pages deploy/runtime smoke; no local test claim or linguistic accuracy inference. |
| KHM-ROM-OUTPUT-GUARD-001 | DONE_VERIFIED (fail-closed output guard) | PR #201 merge `37a536592a8e462f00997890af63ad232d41a0ae`; documented in PR #202 merge `1cc833ad1097f6b1ee7c28eb3e7aefb99ad480fb`. | Residual Khmer letters/marks bracketed and PARTIAL; punctuation preserved. No repair of diacritic loss or contextual romanization. |
| KHM-ROM-ENGINE-001 | PARTIAL | Khmer-script path still uses ASCII-derived upstream package and loses diacritics. | Contextual consonant-series, shortening, coda and diacritic-preserving generator remain open. |
| KHM-GOLD-001 | BLOCKED | Issue [#104](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/104) remains open; independent adjudicated IPA gold=0; accuracy=null. | Human expert protocol, annotators, independent adjudicator, rights-cleared 30 groups and adjudication required. |

**Current main:** `1cc833ad1097f6b1ee7c28eb3e7aefb99ad480fb`. No open PRs at checkpoint. Project remains a partial research prototype; legal, linguistic and manual accessibility acceptance are outstanding.


## PCGN shortened-vowel mark inventory correction — 2026-11-15

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-MARKS-NUMERALS-001 | PARTIAL (source inventory correction) | PR #204 adds U+17D0 SAMYOK SANNYA (◌័) alongside U+17CB BANTOC (◌់) in PCGN note 5 row 3; regression assertions updated in Python and Node suites. | Six PCGN rule categories now explicitly inventory seven Khmer source marks. This does not implement contextual romanization or assign a new Ukrainian value. Exact PR-head Quality [43721677822](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43721677822), Chromium [43721677790](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43721677790), and push Quality [43721673728](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43721673728) SUCCESS on `b27b87081819307da5ffe27d55e3cf4521004730`. |
| KHM-ROM-ENGINE-001 | PARTIAL | Source mark coverage improved; upstream Khmer-script romanizer still emits BGN/PCGN-derived ASCII and loses contextual diacritics. | Contextual series, shortening, coda and diacritic-preserving generation remain open. |

Official evidence: UK PCGN, Romanization of Khmer (Cambodian), BGN/PCGN 1972 Agreement, note 5: https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.


## Final mainline checkpoint — PCGN mark inventory — 2026-11-15

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| MAINLINE-CI-2026-11-15-D | DONE_VERIFIED (engineering/deployment only) | Main `58735a94a8a8f76635f948c2d003d590f26fb0b2`; Quality [43721873111](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43721873111), Chromium [43721873141](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43721873141), Pages [43721873125](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43721873125) all SUCCESS. | 224 Python tests + 70 subtests, web checks/build, 11 browser tests, Pages deployment and deployed-site smoke. No linguistic accuracy claim. |
| KHM-ROM-MARKS-NUMERALS-001 | DONE_VERIFIED (bounded source inventory only) | PR #204 merge `58735a94a8a8f76635f948c2d003d590f26fb0b2`; six PCGN rule rows, seven source marks including U+17CB and U+17D0, ten numerals; exact-head and exact-main CI green. | Inventory and source provenance are covered. Contextual romanization behavior remains outside this task. |
| KHM-ROM-ENGINE-001 | PARTIAL | Source inventory correction merged; upstream Khmer-script path still uses lossy ASCII-derived output. | Contextual consonant-series, shortening, coda and diacritic-preserving generator remain open. |
| KHM-ROM-TEST-001 | PARTIAL | Regression coverage includes both PCGN shortened-vowel marks; full contextual Khmer-script → BGN/PCGN parity remains absent. | Broad attested corpus, contextual matrix behavior and expert review remain outstanding. |
| KHM-GOLD-001 | BLOCKED | Issue [#104](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/104) open; adjudicated IPA gold=0; accuracy=null. | Requires approved convention, qualified annotators, independent adjudicator, curator, rights-cleared pilot and adjudication. |

**Current main:** `58735a94a8a8f76635f948c2d003d590f26fb0b2`. No open PRs. Project remains a partial research prototype; linguistic, legal and manual accessibility gates are not complete.


## Current-main evidence checkpoint — 2026-11-15 (6058768)

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| MAINLINE-CI-2026-11-15-E | DONE_VERIFIED (engineering/deployment only) | Exact main `6058768ca745fddf9306f66d2e325fbed512b6ec`; Quality [43722162644](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43722162644), Chromium [43722162599](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43722162599), Pages [43722162627](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43722162627) all SUCCESS. | Hosted engineering tests/build/browser/deployment only; no linguistic accuracy claim or local test claim. |
| KHM-ROM-MARKS-NUMERALS-001 | DONE_VERIFIED (bounded source inventory only) | PR #204 merge `58735a94a8a8f76635f948c2d003d590f26fb0b2`; six diacritic-rule rows inventory seven Khmer source marks, plus ten numeral rows. | No contextual romanization implementation or new Ukrainian mapping is implied. |
| KHM-ROM-ENGINE-001 | PARTIAL | Khmer-script path still relies on ASCII-derived upstream output and loses PCGN diacritics. | Contextual series, shortening, coda and diacritic-preserving generation remain open. |
| KHM-GOLD-001 | BLOCKED | Issue [#104](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/104); independent adjudicated gold=0; accuracy=null. | Human convention approval, qualified double annotation, independent adjudication, curator, rights-cleared pilot and blind intake. |

**Current main:** `6058768ca745fddf9306f66d2e325fbed512b6ec`. No open PRs. Root LICENSE/MIT metadata owner decision, source rights and manual accessibility remain open. Research prototype only.


## Exact-main evidence checkpoint — PR #206 closeout (2026-11-15)

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| MAINLINE-CI-2026-11-15-F | DONE_VERIFIED (engineering/deployment only) | Exact main `ab5ade5f0984b32884df9fa5dac5607f927a2ea4`; Quality [43728032467](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43728032467), Chromium [43728032424](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43728032424), Pages [43728032407](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43728032407) all SUCCESS. | Hosted corpus validation, Python/Node checks, build, browser smoke and Pages deployment only; no linguistic accuracy claim and no local test claim. |
| KHM-ROM-MARKS-NUMERALS-001 | DONE_VERIFIED (bounded source inventory only) | PR #204 implementation plus PR #206 README correction; six PCGN rule rows cover seven Khmer marks, plus ten numeral rows. | No contextual romanization behavior or Ukrainian target rule is implied. |
| KHM-ROM-ENGINE-001 | PARTIAL | Khmer-script route still uses ASCII-derived upstream output and loses PCGN diacritics. | Contextual series, shortening, coda and diacritic-preserving generation remain open. |
| KHM-ROM-UA-001 | PARTIAL | Direct romanized-Latin adapter covers the inventoried raw forms, but source-script generation and Ukrainian expert review remain incomplete. | Full contextual pipeline and independent target-convention review. |
| KHM-ROM-TEST-001 | PARTIAL | Inventory/direct-input tests are wired into CI; full contextual Khmer-script parity and broad attested corpus remain absent. | Contextual cases, independently reviewed expected outputs and broad corpus. |
| KHM-GOLD-001 | BLOCKED | Issue [#104](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/104) open; adjudicated IPA gold=0; accuracy=null. | Approved IPA convention, qualified double annotation, separate adjudicator, curator, blind intake, rights-cleared 30-lexeme pilot and adjudication. |

**Current main:** `ab5ade5f0984b32884df9fa5dac5607f927a2ea4`. No open PRs. Root LICENSE/MIT metadata, source rights, manual accessibility and branch protection remain owner/external gates. Research prototype only.


## External implementation candidate — KHM-ROM-ENGINE-001 remains PARTIAL (2026-11-15)

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-ENGINE-CANDIDATE-001 | RESEARCH_CANDIDATE (non-acceptance status) | Inspected `pheasaKhmer/khmer-engine` at `31b72cd4665f69678fc835da2f501771e42f097a`: UNGEGN 2013 rules, explicit cluster/syllable representation, weighted syllable-boundary inference, series/shifter/coda handling, and rule tests. Code MIT; bundled sample data CC BY 4.0 / ODC-By 1.0; `pheasa` dependency Apache-2.0. | Not imported or run here. First compare every relevant rule against BGN/PCGN 1972; review heuristic ambiguities and source-specific extrapolations; define abstention behavior; independently verify rights and target outputs. |
| KHM-ROM-ENGINE-001 | PARTIAL | Existing runtime still depends on ASCII-derived `@gmana/km-translit`; external candidate is not a verified BGN/PCGN implementation. | Contextual, diacritic-preserving source-script romanizer with source-backed parity tests and expert review. |

No code, dependency, corpus row, IPA label, Ukrainian mapping or generated artifact was changed by this research review.


## BGN/PCGN ↔ UNGEGN profile comparison — 2026-11-15

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-PROFILE-DIFF-001 | DONE_VERIFIED (bounded textual rule comparison) | `docs/audits/current/BGN-PCGN-UNGEGN-RULE-DIFF-2026-11-15.md`; PCGN note 3 vs UNGEGN note 3 identifies the neutral-subscript delta (UNGEGN adds ស); candidate code includes ស in its UNGEGN neutral set. Candidate explicitly marks SAMYOK-before-final-y and YUUKALEAPINTU as unlisted/secondary-source extensions and has heuristic fallback/coda rules. | This closes only the bounded comparison. Full vowel table parity, code-point fixture verification, and an ambiguity-aware PCGN implementation remain open. |
| KHM-ROM-ENGINE-001 | PARTIAL | Candidate is UNGEGN 2013, not verified PCGN 1972; no code/dependency/data imported. | Build project-owned contextual PCGN engine and source-located parity tests. |
| KHM-ROM-UA-001 | PARTIAL | Existing direct Latin adapter remains separate; contextual source-script generator is absent. | Consume validated PCGN output; expert review Ukrainian targets. |

No gold/IPA evidence changed: independent adjudicated gold remains 0; empirical accuracy remains null.


## Exact-main verification — BGN/PCGN ↔ UNGEGN rule diff (2026-11-15)

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| MAINLINE-CI-2026-11-15-G | DONE_VERIFIED (engineering/deployment only) | Main `266297fcc296388220ea48c975344f5aa14f097d`; Quality [43730567132](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43730567132), Chromium [43730567159](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43730567159), Pages [43730567118](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43730567118) all SUCCESS. | Hosted engineering, browser and deployment checks only; no linguistic accuracy or local test claim. |
| KHM-ROM-PROFILE-DIFF-001 | DONE_VERIFIED (bounded textual comparison) | PR #209 merge `266297fcc296388220ea48c975344f5aa14f097d`; primary-source comparison at `docs/audits/current/BGN-PCGN-UNGEGN-RULE-DIFF-2026-11-15.md`. | Does not complete a full table parity diff or runtime. |
| KHM-ROM-ENGINE-001 | PARTIAL | Candidate is UNGEGN 2013; explicit series-neutral subscript difference and unlisted extensions documented. | Project-owned contextual PCGN engine with ambiguity/abstention and source-located parity tests. |
| KHM-GOLD-001 | BLOCKED | Issue #104 open; adjudicated IPA gold=0; accuracy=null. | Expert-approved convention, qualified double annotation, independent adjudicator, curator, blind intake, rights-cleared pilot and adjudication. |

No code, corpus, IPA label, Ukrainian mapping or generated artifact changed. Research prototype only.


## PCGN note coverage — 2026-11-15

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-PCGN-NOTES-001 | DONE_VERIFIED (source-located Notes 1–11 documentation and regression guardrails; exact PR-head and main CI passed) | `data/khmer/romanization_pcgn_notes.csv` records Notes 1–11 with primary-source locators; `tests/test_romanization_pcgn_notes.py` checks complete coverage and critical PCGN Note 3/5 constraints. | Does not implement contextual romanization. All note rows remain `DOCUMENTED_ONLY`; ambiguous feet, omitted marks and coda-conditioned forms still require a parser and evidence-aware abstention. |
| KHM-ROM-ENGINE-001 | PARTIAL | Current source-script path still uses lossy ASCII-derived upstream output; PCGN contextual notes are now registered but not executed by a project-owned parser. | Contextual series, shifter, shortening, coda, syllable-position and ambiguity-aware romanization with source-located parity tests. |

No IPA labels, Ukrainian mappings, gold rows or empirical accuracy claims were added. Independent adjudicated IPA gold remains 0; accuracy remains null.


## Exact-main verification — PCGN Notes 1–11 registry — 2026-11-15

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| MAINLINE-CI-2026-11-15-H | DONE_VERIFIED (engineering/deployment only) | Exact main `9383385fc3244ff600d0fab254c6488a83d92d7b`; Quality [43733051013](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43733051013), Chromium [43733051164](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43733051164), Pages [43733051031](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43733051031) all SUCCESS. | Hosted corpus-structure, Python, Node, build, browser and Pages deployment checks; no linguistic accuracy claim. |
| KHM-ROM-PCGN-NOTES-001 | DONE_VERIFIED (source-located Notes 1–11 documentation and regression guardrails) | PR #211 merge `9383385fc3244ff600d0fab254c6488a83d92d7b`; exact-head and exact-main Quality/Chromium/Pages workflows passed. | Does not implement contextual PCGN romanization; each note remains DOCUMENTED_ONLY at runtime. |
| KHM-ROM-ENGINE-001 | PARTIAL | PCGN notes are now machine-readable, but the source-script route still relies on lossy ASCII-derived upstream output. | Project-owned contextual PCGN parser/generator with explicit ambiguity, omitted-mark and abstention behavior. |
| KHM-ROM-TEST-001 | PARTIAL | Existing row-level tests plus Notes 1–11 boundary tests pass in hosted CI. | Contextual Khmer-script parity fixtures with independently reviewed expected romanizations remain absent. |

No IPA labels, Ukrainian target decisions or gold records were added. Independent adjudicated IPA gold remains 0; empirical accuracy remains null.


## Typed PCGN orthographic analysis — 2026-11-15

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-PCGN-STRUCTURE-001 | PARTIAL (implementation pending exact-head CI) | `src/khmer_ua/pcgn.py`, `schemas/pcgn-orthographic-analysis.schema.json`, `tests/test_pcgn_orthographic_analysis.py`. Typed source trace preserves base/subscript identities and orthographic register labels, marks, vowel signs, positions, unknowns and provenance. | No syllable segmentation, effective-series choice, coda inference, diacritic recovery, romanization or IPA. Needs exact-head hosted test/schema verification and reviewed contextual fixtures. |
| KHM-ROM-ENGINE-001 | PARTIAL | A parser-facing structural contract now exists, separate from the IPA-first engine. | Complete contextual PCGN resolver/generator with ambiguity/abstention and source-backed parity fixtures; no guessed readings. |
| KHM-ROM-TEST-001 | PARTIAL | Focused tests cover structure preservation, source-mark typing, abstention, malformed input and schema contract. | Hosted CI must pass; add independent expert-reviewed expected PCGN outputs before behavioral rule coverage is accepted. |

No pronunciation, IPA, Ukrainian target or gold data was added. Independent adjudicated IPA gold remains 0; empirical accuracy remains null.


## Exact-main verification — typed PCGN structural analysis — 2026-11-15

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-PCGN-STRUCTURE-001 | DONE_VERIFIED (typed structural contract and abstention only) | PR #213 merge `18134929554420875b447b1c5128b3b879e3f608`; module `src/khmer_ua/pcgn.py`, schema `schemas/pcgn-orthographic-analysis.schema.json`, tests `tests/test_pcgn_orthographic_analysis.py`; exact-head and exact-main Quality/Chromium/Pages passed. | Does not segment phonetic syllables, select effective series, infer coda/position, recover omitted marks or generate PCGN Latin/IPA/Ukrainian output. |
| KHM-ROM-ENGINE-001 | PARTIAL | Typed orthographic input boundary now exists; contextual rules are still not implemented. | Source-backed PCGN series/shifter/vowel/shortening/coda resolver with ambiguity-aware abstention and reviewed expected outputs. |
| KHM-ROM-TEST-001 | PARTIAL | Structural tests and CI pass; no contextual gold fixtures. | Independently reviewed PCGN romanization fixtures covering valid, ambiguous, omitted-mark and unsupported cases. |
| MAINLINE-CI-2026-11-15-I | DONE_VERIFIED (engineering/deployment only) | Exact main `18134929554420875b447b1c5128b3b879e3f608`; Quality [43734192447], Chromium [43734192457], Pages [43734192455] all SUCCESS. | Hosted structure, Python, web, build, browser and deployment checks; no linguistic accuracy claim. |

Independent adjudicated IPA gold remains 0; empirical accuracy remains null. Issue #104 remains open.


## PCGN Note 3 series resolver — 2026-11-15

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-PCGN-SERIES-001 | DONE_VERIFIED (Note 3 series-source decision and abstention only) | `resolve_pcgn_series`, `PCGNSeriesDecision`, `schemas/pcgn-series-decision.schema.json`, `tests/test_pcgn_series_resolution.py`; exact PCGN weak set and Note 3 source locator encoded. | Note 3 series selection only; Note 2 shifters, vowel forms, coda, syllable segmentation and romanization remain out of scope. |
| KHM-ROM-ENGINE-001 | PARTIAL | Typed structural layer plus bounded Note 3 series decision. | Complete contextual PCGN parsing and generation with ambiguity-aware abstention and source-backed parity fixtures. |

No vowel, IPA, Ukrainian target or gold entry is generated. Independent adjudicated IPA gold remains 0; accuracy remains null.


## Exact-main verification — PCGN Note 3 series resolver — 2026-11-15

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-PCGN-SERIES-001 | DONE_VERIFIED (Note 3 series-source decision and abstention only) | PR #215 merge `357ce7f2a5400ff1643e4f64337009dd18c4113d`; `resolve_pcgn_series`, `PCGNSeriesDecision`, schema `schemas/pcgn-series-decision.schema.json`, tests `tests/test_pcgn_series_resolution.py`; exact-head and exact-main Quality/Chromium/Pages passed. | Does not apply Note 2 shifters, map vowels, infer codas/phonetic syllables, process Note 5 shortening or generate PCGN Latin. |
| KHM-ROM-ENGINE-001 | PARTIAL | Typed structural analysis plus Note 3 series resolver. | Contextual PCGN resolver/generator with shifter, vowel/rime, coda, shortening and ambiguity-aware behavior; source-backed parity fixtures. |
| MAINLINE-CI-2026-11-15-J | DONE_VERIFIED (engineering/deployment only) | Exact main `357ce7f2a5400ff1643e4f64337009dd18c4113d`; Quality [43734828487], Chromium [43734828491], Pages [43734828557] all SUCCESS. | Hosted validation/tests/build/browser/deploy only; no linguistic accuracy claim. |

Independent adjudicated IPA gold remains 0; empirical accuracy remains null. Issue #104 remains open.


## PCGN Note 2 shifter subset — 2026-11-15

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-PCGN-SHIFTERS-001 | PARTIAL (bounded subset implemented; exact-head and exact-main CI passed) | `register_shifter_positions` in typed analysis; `resolve_pcgn_series` supports one correctly placed shifter after a single base with no foot; schema/tests cover TRIISAP â→ô, MUUSIKATOAN ô→â and BA+MUUSIKATOAN p-in-â. | Full Note 2 cluster behavior, BA+TRIISAP, multiple/misplaced shifters and all contextual exceptions remain unresolved. |
| KHM-ROM-PCGN-SERIES-001 | DONE_VERIFIED (Note 3 series-source decision only) | PR #215 exact-head and exact-main CI passed. | Note 2 extension is separately PARTIAL; no vowel or full romanization output. |
| KHM-ROM-ENGINE-001 | PARTIAL | Structural analyzer + Note 3 series + bounded Note 2 subset. | Full contextual PCGN generator, vowel/rime, coda, Note 5 shortening and evidence-backed abstention fixtures. |

No IPA, Ukrainian target or gold data is generated. Independent adjudicated IPA gold remains 0; accuracy remains null.


## PCGN Note 2 shifter subset — PR #217 — 2026-11-15

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-PCGN-SHIFTERS-001 | PARTIAL (bounded subset implemented; exact-head and exact-main CI passed) | PR #217 merge `c738075c47c76730aa15e96acea588ad924c829c`; source-positioned shifters, typed before/after series/effect; exact-head push Quality [43735335039], PR Quality [43735349944] and Chromium [43735349863] SUCCESS. | Full Note 2 on clusters/feet, BA+TRIISAP, multiple/misplaced/wrong-direction marks remains unresolved. Exact-main Quality [43735441278], Chromium [43735441245] and Pages [43735441621] all SUCCESS on merge SHA `c738075c47c76730aa15e96acea588ad924c829c`. |
| KHM-ROM-PCGN-SERIES-001 | DONE_VERIFIED (Note 3 series-source decision only) | PR #215 exact-head and exact-main CI passed. | Note 2 remains separately PARTIAL; no vowel or full romanization output. |

No vowel, IPA, Ukrainian target or gold data is generated. Independent adjudicated IPA gold remains 0; accuracy remains null.


## PR #218 exact-main verification checkpoint — 2026-11-15

The documentation closeout PR #218 is merged as `9420326549d8a327774d0587b6fe19c4b17befcd`. PR-head Quality [43735576766], Chromium [43735576217] and push Quality [43735564674] passed. Exact-main Quality [43735662414], Chromium [43735662288] and Pages [43735662264] all SUCCESS, including deployed-site/runtime-asset smoke; no status promotion depends on this docs-only PR.


## Exact-main verification — PR #219 — 2026-11-15

PR #219 merged as `690b44174a8831ac9b08b44786d5ffde43f6d5aa`. PR-head push Quality [43735841295], PR Quality [43735855013], PR Chromium [43735855047], exact-main Quality [43735981736], Chromium [43735981714] and Pages [43735981744] all SUCCESS. This closes the documentation checkpoint only; KHM-ROM-PCGN-SHIFTERS-001 remains PARTIAL.


## PR #220 exact-main checkpoint — 2026-11-15

PR #220 merged as `8c4784235742cd83c35ce4a2b0bc7831a2b11bb2`. PR-head push Quality [43736157032], PR Quality [43736168034], PR Chromium [43736167978] passed. Exact-main Quality [43736256876], Chromium [43736256892] and Pages [43736257006] all SUCCESS, including deployed-site/runtime-asset smoke; no linguistic status promotion depends on this docs-only PR.


## PR #221 exact-main checkpoint — 2026-11-15

PR #221 merged as `0d9bb90b1451ce9a2452121e30c3864d4cd887f5`. PR-head push Quality [43736444673], PR Quality [43736456391], PR Chromium [43736456480] passed. Exact-main Quality [43736548569], Chromium [43736548708] and Pages [43736548595] all SUCCESS, including deployed-site/runtime-asset smoke; no linguistic status promotion depends on this docs-only PR.


## PR #222 exact-main checkpoint — 2026-11-15

PR #222 merged as `95dd256b515c4a15e28cf80f21e3a53b0f0dfa11`. PR-head push Quality [43736688182], PR Quality [43736708656], PR Chromium [43736708789] passed. Exact-main Quality [43736800449], Chromium [43736800513] and Pages [43736800469] all SUCCESS, including deployed-site/runtime-asset smoke; no linguistic status promotion depends on this docs-only PR.


## PCGN Note 2 — base-plus-foot register shifters — 2026-11-15

The bounded Note 2 resolver now handles one base consonant plus one subscript foot when a single shifter is encoded immediately after the base. The implementation first selects the unshifted cluster series under Note 3, then applies Note 2:

- Note 3's weak-foot rule can select the base series; otherwise the foot normally selects the series.
- TRIISAP changes a selected â-series cluster to ô.
- MUUSIKATOAN changes a selected ô-series cluster to â.
- The supported Unicode order is base + shifter + COENG + foot. Unicode 17.0 §16.4 explicitly requires the shifter immediately after the base even when a subscript follows; the PCGN guide's Note 1 defines the affected unit as a consonant or consonant-plus-foot cluster, and Note 2 defines the series changes.
- BA with a foot plus a shifter, BA+TRIISAP, multiple feet, multiple/misplaced shifters, and wrong-direction shifters remain fail-closed. No unlisted BA combination is inferred.

Regression fixtures include `ថ៊្ម` (base-series selected by a weak foot, then TRIISAP), `ម៊្ហ` (foot-series selection, then TRIISAP) and `គ៉្ង` (base-series selection, then MUUSIKATOAN). These assert series metadata only. No vowel/rime, coda, syllable boundary, PCGN Latin, IPA or Ukrainian output is generated.

Sources:
- BGN/PCGN 1972, Notes 1–3, pp. 2–3: https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf
- Unicode 17.0, Chapter 16.4, Khmer syllabic order and consonant shifters: https://unicode.org/versions/Unicode17.0.0/core-spec/chapter-16/

Status: `KHM-ROM-PCGN-SHIFTERS-001` remains `PARTIAL`; this closes only the bounded one-base/one-foot cases with canonical shifter order. BA+foot interactions, multiple-foot clusters, and complete Note 2 coverage remain unimplemented pending evidence/review.


## Exact-main verification — PCGN Note 2 base-plus-foot shifters / PR #224 — 2026-11-15

- PR [#224](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/224) merged by squash as `51a8cbe1bd313e98bd83f28a347c1ddebadf8845`; exact current `main` verified at this SHA. No open PRs.
- PR-head `51a164e5092096267b78edbd87686c00017353af`: push Quality [43743592248], PR Quality [43743604940], PR Chromium [43743604985] all SUCCESS. Quality includes IPA-gold structure validation, the full Python suite, Node checks and production build.
- Exact post-merge main: Quality [43743697905], Chromium [43743697809], Pages build/deploy [43743697813] all SUCCESS. Pages includes production Chromium exercise, deployment and deployed-site/runtime-asset smoke.
- The resolver now handles one canonical base + one foot cluster: determine the unshifted series by Note 3, then apply Note 2 to the cluster. Canonical Unicode order is base + shifter + COENG + foot. Regression examples cover both series-source paths and both shift directions.
- BA+foot+shifter, BA+TRIISAP, multiple feet/marks, misplaced and wrong-direction shifters remain fail-closed. The output is still series metadata only; no vowel/rime, coda, syllable segmentation, PCGN Latin, IPA or Ukrainian output.
- `KHM-ROM-PCGN-SHIFTERS-001` remains PARTIAL; `KHM-ROM-ENGINE-001` remains PARTIAL. Independent adjudicated IPA gold remains 0 and accuracy null; issue #104 remains open. This does not make the repository production-ready.


## PCGN normal dependent-vowel component subset — 2026-11-15

Added `resolve_pcgn_dependent_vowel(analysis, series_decision)` and `PCGNVowelDecision`. It maps only one ordinary dependent-vowel sign after one base and at most one foot, using the already-resolved Note 2/3 series. The bounded source rows are 2–9 and 13–15 of the official PCGN Independent/Dependent Vowel Characters table:

- U+17B6 AA: â `a`, ô `éa`.
- U+17B7 I: `ĕ` in both series.
- U+17B8 II: â `ei`, ô `i`.
- U+17B9 Y: `œ̆`; U+17BA YY: `œ`.
- U+17BB U: â `ŏ`, ô `ŭ`; U+17BC UU: â `o`, ô `u`.
- U+17BD UA: `uŏ`.
- U+17C1 E: `é`; U+17C2 AE: `ê`; U+17C3 AI: â `ai`, ô `ey`.

The resolver deliberately abstains on independent vowels, compound vowel patterns (rows 10–12 and 16–17), shortening marks/Note 5, NIKAHIT/REAHMUK, ROBAT, AHSDA, TOANDAKHIAT, multiple vowel signs, multiple bases/feet, unresolved series and unsupported tokens. The serialized result is explicitly a **vowel component only**: it does not generate an onset, coda, syllable boundary, complete PCGN syllable, IPA or Ukrainian output.

Schema: `schemas/pcgn-dependent-vowel-decision.schema.json`; tests: `tests/test_pcgn_dependent_vowel_resolution.py`. The public package API exports the resolver and decision type.

Source: BGN/PCGN 1972 Agreement, Independent/Dependent Vowel Characters table, pp. 2–3: https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.

Status: `KHM-ROM-PCGN-VOWELS-001` remains `PARTIAL` (bounded normal dependent-vowel component table only). `KHM-ROM-ENGINE-001` remains `PARTIAL`; no IPA-first or Ukrainian adapter behavior is changed.


## Exact-main verification — PR #225 documentation closeout — 2026-11-15

- PR [#225](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/225) merged as `7c8787efa89b7cba1138e808bad5d83ee021e010`; exact post-merge main checks: Quality [43743936544], Chromium [43743936534], Pages build/deploy [43743936575] all SUCCESS, including deployed-site/runtime-asset smoke.
- PR-head push Quality [43743840052], PR Quality [43743854774] and PR Chromium [43743854739] all SUCCESS.
- This was a documentation-only verification of PR #224; no linguistic status changed.


## Exact-main verification — PCGN normal dependent-vowel component / PR #226 — 2026-11-15

- PR [#226](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/226) merged by squash as `8d02c48d7d3249f3b0cdedd87d59cb266ad19080`; exact current `main` verified at this SHA. No open PRs.
- Final PR-head `9860e7be7536ec1d9f05211dd583b6c75deb4d68`: push Quality [43744359146], PR Quality [43744364426] and PR Chromium [43744364535] all SUCCESS. Python tests: 262 passed, 70 subtests passed. An earlier push run [43744245961] failed only because a schema assertion omitted the permitted `null` enum member; the assertion was corrected and the final exact-head runs passed.
- Exact post-merge main: Quality [43744506093], Chromium [43744506092], Pages build/deploy [43744506121] all SUCCESS, including production Chromium exercise and deployed-site/runtime-asset smoke.
- The new resolver maps only normal dependent-vowel table rows 2–9 and 13–15, conditioned on the resolved Note 2/3 series. It returns the vowel component only. Compound rows 10–12/16–17, independent vowels, shortening/Note 5, coda, special marks and unsupported structures abstain.
- `KHM-ROM-PCGN-VOWELS-001` and `KHM-ROM-ENGINE-001` remain PARTIAL. No IPA, Ukrainian output, gold entries or accuracy claims were added. Issue #104 remains open; independent adjudicated IPA gold remains 0 and accuracy null.


## PCGN compound dependent-vowel patterns — 2026-11-15

Extended `resolve_pcgn_dependent_vowel` to accept the exact source-ordered two-sign patterns in PCGN table rows 10–12 and 16–17, in addition to the single-sign rows 2–9 and 13–15:

- Row 10 `េ + ើ`: â `aeu`, ô `eu`.
- Row 11 `េ + ឿ`: `œă` in both series.
- Row 12 `េ + ៀ`: `iĕ` in both series.
- Row 16 `េ + ា`: `aô` in both series.
- Row 17 `េ + ៅ`: `au` in both series.

The result now retains the ordered source signs as `source_signs`; reversed or unlisted sign sequences abstain. The schema and tests cover all table rows 2–17, including both series values where applicable. The resolver still rejects shortening/Note 5, codas, independent vowels, NIKAHIT/REAHMUK and other special marks, and returns only a vowel component. It does not produce a complete syllable, IPA or Ukrainian output.

Status remains `KHM-ROM-PCGN-VOWELS-001 = PARTIAL`: independent vowels, inherent-vowel/coda cases, shortening, and full syllable assembly remain outside the accepted subset.


## Exact-main verification — PR #227 documentation closeout — 2026-11-15

- PR #227 merged as `bbc71312b2b3f913eed7187775764cd55cbe6c24`; exact-main Quality [43744826124], Chromium [43744826188] and Pages build/deploy [43744826137] all SUCCESS, including deployed-site/runtime-asset smoke.
- PR-head push Quality [43744691628], PR Quality [43744706180] and PR Chromium [43744706164] all SUCCESS.
- Documentation-only; no linguistic status changed.


## Exact-main verification — PCGN compound dependent-vowel patterns / PR #228 — 2026-11-15

- PR [#228](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/228) merged as `025432dd61f39ec07e48b6ab86f07e5a9805eb0b`; exact current `main` verified at this SHA. No open PRs.
- PR-head `afe37e0c1394d8d4d16671308860af721963ab5e`: push Quality [43745154699], PR Quality [43745173699] and PR Chromium [43745173686] all SUCCESS; Python tests 262 passed, 70 subtests passed.
- Exact post-merge main: Quality [43745317983], Chromium [43745317953], Pages build/deploy [43745317999] all SUCCESS, including production Chromium exercise and deployed-site/runtime-asset smoke.
- The resolver now covers normal dependent-vowel rows 2–17, using source-ordered one- or two-sign patterns and the resolved Note 2/3 series. It returns only the vowel component; Note 5 shortening, coda, independent vowels and full syllable assembly remain unsupported.
- `KHM-ROM-PCGN-VOWELS-001` and `KHM-ROM-ENGINE-001` remain PARTIAL. No IPA/Ukrainian outputs, gold records or accuracy claims were added.


## PCGN independent-vowel component subset — 2026-11-15

Added `resolve_pcgn_independent_vowel(analysis)` and `PCGNIndependentVowelDecision`, exported through the public package API. It maps the independent-vowel characters explicitly listed in the BGN/PCGN 1972 table:

- Row 3 ឥ → `ĕ`; row 4 ឦ → `ei`.
- Row 14 ឯ → `ê`; row 15 ឰ → `ai`.
- Row 16 ឱ / ឲ → `aô`; row 17 ឳ → `au`; row 18 ឪ → `âu`.
- Rows 19–22 ឫ / ឬ / ឭ / ឮ → `rœ̆` / `rœ` / `lœ̆` / `lœ`.

PCGN row 7 ឧ remains unresolved as `ŏ` or `ŭ` under Note 9, which directs the user to consult a reference source when uncertain. Unlisted/rare variants and mixed-script or mixed-vowel chunks abstain. Output is an independent-vowel Latin component only; no IPA or Ukrainian output is generated.

Schema: `schemas/pcgn-independent-vowel-decision.schema.json`; tests: `tests/test_pcgn_independent_vowel_resolution.py`. Source: BGN/PCGN 1972 Agreement, Independent/Dependent Vowel Characters table, pp. 2–3, Note 9: https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.

Status: `KHM-ROM-PCGN-INDEPENDENT-VOWELS-001` remains `PARTIAL` (listed independent-vowel forms only). This does not complete PCGN syllable assembly or alter the IPA-first/Ukrainian adapter.


## Exact-main verification — PR #229 documentation closeout — 2026-11-15

- PR #229 merged as `71c91ff5bd84a0066fa791762c5ce71093a001bd`; exact-main Quality [43745602483], Chromium [43745602490] and Pages build/deploy [43745602494] all SUCCESS, including deployed-site/runtime-asset smoke.
- PR-head push Quality [43745471853], PR Quality [43745491299] and PR Chromium [43745491239] all SUCCESS.
- Documentation-only; no linguistic status changed.


## Exact-main verification — PCGN independent-vowel component / PR #230 — 2026-11-15

- PR [#230](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/230) merged as `49c6b828e187600792df952202699bc1656eb98f`; exact current `main` verified at this SHA. No open PRs.
- PR-head `e16054765dce8d9d9f73d8a02b9a2c07aab4b209`: push Quality [43745799434], PR Quality [43745819194] and PR Chromium [43745819155] all SUCCESS; Python tests 266 passed, 70 subtests passed.
- Exact post-merge main: Quality [43745949050], Chromium [43745949072], Pages build/deploy [43745949013] all SUCCESS, including deployed-site/runtime-asset smoke.
- Listed PCGN independent-vowel rows 3, 4 and 14–22 are mapped as orthographic components. Row 7 ឧ remains unresolved under Note 9 (`ŏ` / `ŭ`) until a lexical reference selects an alternative; unlisted/rare variants abstain.
- `KHM-ROM-PCGN-INDEPENDENT-VOWELS-001`, `KHM-ROM-PCGN-VOWELS-001` and `KHM-ROM-ENGINE-001` remain PARTIAL. No IPA/Ukrainian output, gold data or accuracy claim was added.


## Exact-main verification — PR #231 documentation closeout — 2026-11-15

- PR #231 merged as `b459fcbf56628409c8cd1ce8c95645b4b9c1c1a6`; exact-main Quality [43746279657], Chromium [43746279685] and Pages build/deploy [43746279665] all SUCCESS, including deployed-site/runtime-asset smoke.
- PR-head push Quality [43746135830], PR Quality [43746153049] and PR Chromium [43746153043] all SUCCESS.
- Documentation-only; no linguistic status changed.


## BGN/PCGN Note 5 bounded implementation — 2026-11-15

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-PCGN-SHORTENING-001 | PARTIAL | `resolve_pcgn_shortened_vowel`, `PCGNShortenedVowelDecision`, schema `schemas/pcgn-shortened-vowel-decision.schema.json`, parser shortening-mark positions, and tests for rows 1–2 / Note 5. Primary source: BGN/PCGN 1972, Vowel Characters table rows 1–2 and Note 5, pp. 2–3. | Only exact inherent+BANTOC, AA+BANTOC and SAMYOK+coda patterns. Caller supplies onset-only analysis and explicit coda class. Remaining: verified syllable/coda parser, complete PCGN onset/coda romanization and IPA/Ukrainian adapters. |


## Exact-main verification — PR #233 / PCGN Note 5 — 2026-11-15

PR #233 merged as `cf57045bf6ddf0537e2a5c33a8b2468e8f3f6f2c`. Final PR-head `9bcf7391ce08557ce2fa56e4cbb764568949f952`: push Quality [43751102348], PR Quality [43751107119], Chromium [43751107131] all SUCCESS (272 tests + 70 subtests; web checks/build/Chromium passed). Exact-main Quality [43751266786], Chromium [43751266785], Pages [43751266784] all SUCCESS, including deployed-site/runtime-asset smoke. Note 5 remains PARTIAL component-only; no IPA/Ukrainian or complete-syllable status promotion.


## BGN/PCGN Note 6 bounded implementation — 2026-11-15

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-PCGN-ROBAT-001 | PARTIAL | `resolve_pcgn_robat`, `PCGNRobatDecision`, schema `schemas/pcgn-robat-decision.schema.json`, tests `tests/test_pcgn_robat_resolution.py`, and source registry Note 6 status. Primary source: BGN/PCGN 1972, Diacritical Marks table row 4 (p. 4) and Note 6 (p. 5). | Only one final ROBAT after one modeled unstacked consonant; caller supplies its PCGN romanization. Remaining: foot-cluster/other placements, integration with complete coda and syllable parsing, full romanization, IPA/Ukrainian adapters. |


## Exact-main verification — PR #235 / PCGN Note 6 — 2026-11-15

PR #235 merged as `34ab63ff37023bddcaeaebb0a6ccd838f662c045`. Final PR-head `0d6f1a2b11ab1de94ad9be391c2dd4932142ff77`: push Quality [43751844908], PR Quality [43751851657], PR Chromium [43751851706] all SUCCESS (278 tests + 70 subtests). Exact-main Quality [43751965081], Chromium [43751965119], Pages [43751965128] all SUCCESS, including deployed-site/runtime-asset smoke. ROBAT remains a PARTIAL `rC` component resolver with caller-supplied consonant value; no IPA/Ukrainian or complete-syllable promotion.


## BGN/PCGN Note 7 bounded implementation — 2026-11-15

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-PCGN-AHSDA-001 | PARTIAL | `resolve_pcgn_ahsda`, `PCGNAhsdaDecision`, schema `schemas/pcgn-ahsda-decision.schema.json`, tests `tests/test_pcgn_ahsda_resolution.py`, and source registry Note 7 status. Primary source: BGN/PCGN 1972, Diacritical Marks table row 5 (p. 4), Note 7 (p. 5). | Explicit INITIAL/FINAL syllable position; FINAL also requires explicit â/ô series. Returns only mark effect/vowel component. Remaining: integration with verified syllable segmentation and complete romanization, IPA/Ukrainian adapters. |


## Exact-main verification — PR #237 / PCGN Note 7 — 2026-11-15

PR #237 merged as `890791a1d8236180c82a39b81bd28b7f772d614c`. Final PR-head `2e3ee353124b1a9cacac64997ceb06720a78370c`: push Quality [43752539333], PR Quality [43752551657], PR Chromium [43752551605] all SUCCESS (284 tests + 70 subtests). Exact-main Quality [43752661403], Chromium [43752661392], Pages [43752661369] all SUCCESS, including deployed-site/runtime-asset smoke. AHSDA remains a PARTIAL component resolver; no syllable-position or series inference, full romanization, IPA or Ukrainian output.


## BGN/PCGN Note 8 bounded implementation — 2026-11-15

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-PCGN-TOANDAKHIAT-001 | PARTIAL | `resolve_pcgn_toandakhiat`, `PCGNToandakhiatDecision`, schema `schemas/pcgn-toandakhiat-decision.schema.json`, tests `tests/test_pcgn_toandakhiat_resolution.py`, and source registry Note 8 status. Primary source: BGN/PCGN 1972, Diacritical Marks table row 6 (p. 4), Note 8 (p. 5). | Caller identifies exact marked consonant grapheme; resolver verifies immediate token adjacency and returns omission only. Remaining: broader character scope, full-word integration, IPA/Ukrainian adapters. |


## Exact-main verification — PR #239 / PCGN Note 8 — 2026-11-15

PR #239 merged as `9c615293e3037cb0ccbd9db0820698741bbcd5cf`. Final PR-head `e52b2d5be98a521dfa3c6dc5af846c6c79d42dce`: push Quality [43753171641], PR Quality [43753185515], PR Chromium [43753185496] all SUCCESS (290 tests + 70 subtests). Exact-main Quality [43753327251], Chromium [43753327183], Pages [43753327232] all SUCCESS, including deployed-site/runtime-asset smoke. TOANDAKHIAT remains PARTIAL; silent character is caller-identified, with omission-only output.


## BGN/PCGN Note 4 bounded glottal-onset component — 2026-11-15

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-PCGN-GLOTTAL-001 | PARTIAL | `resolve_pcgn_glottal_onset`, `PCGNGlottalOnsetDecision`, schema `schemas/pcgn-glottal-onset-decision.schema.json`, tests `tests/test_pcgn_glottal_onset_resolution.py`, and source registry Note 4 status. Primary source: BGN/PCGN 1972, Consonant Characters row 22 and Note 4 (p. 5). | Standalone `អ` only; â-series is verified through Notes 2–3. Word-initial and following-vowel-letter context are explicit caller inputs; omission is offered only when both are true. Remaining: full syllable assembly, IPA/Ukrainian adapter integration, and word-level context acquisition. |


## Exact-main verification — PR #241 / PCGN Note 4 — 2026-11-15

- PR [#241](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/241) merged by squash as `c1eae2e79feb1e79bfddbe42338c73db73d657ff`; exact current `main` verified at this SHA. No open PRs.
- Final PR-head `710de884976269237975f4d642d5d83f5b1d9ef5`: push Quality [43755446552], PR Quality [43755529961], PR Chromium [43755530039] all SUCCESS. Python 296 passed, 70 subtests passed; web checks and production build passed; Chromium visible-results smoke passed.
- Exact post-merge main: Quality [43755629744], Chromium [43755629808], Pages build/deploy [43755629885] all SUCCESS, including production-site Chromium exercise and deployed-site/runtime-asset smoke.
- Note 4 maps only standalone `អ` to the apostrophe component; word-initial and following-vowel-letter context are caller-supplied, and omission is offered only when both are true. `KHM-ROM-PCGN-GLOTTAL-001` remains PARTIAL. No complete syllable, IPA, Ukrainian output, gold record or accuracy claim was added.


## PCGN Notes 2–3 registry correction and BA+TRIISAP exception — 2026-11-15

- Corrected the source registry: Notes 2 and 3 are `PARTIAL_COMPONENT_RESOLVER`, not `DOCUMENTED_ONLY`, because bounded series/shifter decisions already exist. This is a status correction, not a claim that either note is complete.
- Added the explicit Note 3 `ប` + TRIISAP case: the pre-shifter base series is ô, while the documented BA exception selects the â series and records the p-in-â exception. The result remains typed series metadata only.
- BA+foot with a shifter, multiple/misplaced marks, unsupported clusters and wrong-direction shifters continue to abstain. No vowel, complete PCGN romanization, IPA or Ukrainian output is generated.
- `KHM-ROM-PCGN-SHIFTERS-001` remains PARTIAL; `KHM-ROM-PCGN-SERIES-001` remains DONE_VERIFIED only for the bounded Note 3 series decision.
- Primary source: BGN/PCGN 1972 Agreement, Notes 2–3 (pp. 2–3): https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.


## Exact-main verification — PR #243 / PCGN BA+TRIISAP exception — 2026-11-15

- PR [#243](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/243) merged by squash as `f03c214a262c9665bf154fbbf9196c26d945627b`; exact current `main` verified at this SHA. No open PRs.
- Final PR-head `f2436ec9fadc007e077ac375a7dfdcc269411fae`: push Quality [43756120696], PR Quality [43756201009], PR Chromium [43756200975] all SUCCESS. Python 299 passed, 70 subtests passed; web checks and production build passed; Chromium visible-results smoke passed.
- Exact post-merge main: Quality [43756294903], Chromium [43756294932], Pages build/deploy [43756295043] all SUCCESS, including production-site Chromium exercise and deployed-site/runtime-asset smoke.
- The Note 3 `ប`+TRIISAP exception now records ô as the pre-shifter base series and â as the selected series with the p-in-â exception. Notes 2 and 3 are correctly classified as partial component resolvers. `KHM-ROM-PCGN-SHIFTERS-001` remains PARTIAL; no vowel, complete romanization, IPA, Ukrainian output, gold record or accuracy claim was added.


## Exact-main verification — PR #244 documentation checkpoint — 2026-11-15

- PR [#244](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/244) merged as `7dac519ce6a25aa4ccb36c9feb9a588ca3e5f3fa`; exact-main Quality [43756575098], Chromium [43756575123] and Pages build/deploy [43756575113] all SUCCESS, including deployed-site/runtime-asset smoke.
- PR-head Quality [43756457792], PR Chromium [43756457772] and push Quality [43756446431] all SUCCESS.
- This closes the exact-main documentation checkpoint for PR #243; no linguistic status changed.


## BGN/PCGN Note 10 bounded character inventory — 2026-11-15

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-PCGN-UNICODE-001 | PARTIAL | `validate_pcgn_romanization_characters`, `PCGNRomanizationCharacterInventoryDecision`, schema `schemas/pcgn-romanization-character-inventory-decision.schema.json`, tests `tests/test_pcgn_romanization_character_inventory.py`, and Note 10 source-registry row. Primary source: BGN/PCGN 1972, Note 10 (p. 5). | Validates basic ASCII letters and the exact modified-letter inventory, including decomposed breve sequences; preserves codepoints without normalization. Non-letter characters are not validated. No transliteration, IPA or Ukrainian output. |


## Exact-main verification — PR #245 / PCGN Note 10 character inventory — 2026-11-15

- PR [#245](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/245) merged by squash as `f7c038dc479fa7a52c6ec3267e8e1e60313f6343`; exact current `main` verified at this SHA. No open PRs.
- Final PR-head `107a0c250be3f7ca1868e27f165f876667a4cd9d`: push Quality [43757052464], PR Quality [43757137146], PR Chromium [43757137145] all SUCCESS. Python 306 passed, 70 subtests passed; web checks and production build passed; Chromium visible-results smoke passed.
- Exact post-merge main: Quality [43757257747], Chromium [43757257757], Pages build/deploy [43757257745] all SUCCESS, including production-site Chromium exercise and deployed-site/runtime-asset smoke.
- `KHM-ROM-PCGN-UNICODE-001` remains PARTIAL: Note 10 letter-inventory validation only. No PCGN word/syllable romanization, IPA, Ukrainian output, gold record or accuracy claim was added.


## BGN/PCGN Note 9 — explicit independent-vowel alternatives — 2026-11-15

The independent-vowel decision now exposes `romanization_options=("ŏ", "ŭ")` for standalone `ឧ` while keeping `status="UNRESOLVED"` and `romanization=null`. This makes the exact source alternatives inspectable without selecting one. A lexical/reference source is still required before either value can be accepted. All other listed independent-vowel mappings remain unchanged; mixed or unsupported inputs continue to abstain.

Updated schema: `schemas/pcgn-independent-vowel-decision.schema.json`; tests: `tests/test_pcgn_independent_vowel_resolution.py`. Source registry Note 9 is now `PARTIAL_AMBIGUITY_CONTRACT`.

Primary source: BGN/PCGN 1972 Agreement, Independent/Dependent Vowel Characters table row 7 and Note 9 (pp. 2–3): https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.

Status: `KHM-ROM-PCGN-INDEPENDENT-VOWELS-001` remains PARTIAL. No lexical choice, IPA, Ukrainian output, gold record or accuracy claim is added.


## Exact-main verification — PR #247 / PCGN Note 9 alternatives — 2026-11-15

- PR [#247](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/247) merged by squash as `1b6d6a04921915c4e62387daae70e57c19819cb6`; exact current `main` verified at this SHA. No open PRs.
- Final PR-head `20cb0f2704bef9eb6319fb0c3a38c74740d6fded`: push Quality [43757811370], PR Quality [43757897285], PR Chromium [43757897258] all SUCCESS. Python 308 passed, 70 subtests passed; web checks and production build passed; Chromium visible-results smoke passed.
- Exact post-merge main: Quality [43758011762], Chromium [43758011768], Pages build/deploy [43758011784] all SUCCESS, including production-site Chromium exercise and deployed-site/runtime-asset smoke.
- Note 9 now exposes `("ŏ", "ŭ")` as options for `ឧ` while retaining UNRESOLVED status and no selected romanization. `KHM-ROM-PCGN-INDEPENDENT-VOWELS-001` remains PARTIAL; no lexical selection, IPA, Ukrainian output, gold record or accuracy claim was added.


## BGN/PCGN anusvara/visarga table component — 2026-11-15

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-PCGN-ANUSVARA-VISARGA-001 | PARTIAL | `resolve_pcgn_anusvara_visarga`, `PCGNAnusvaraVisargaDecision`, schema `schemas/pcgn-anusvara-visarga-decision.schema.json`, tests `tests/test_pcgn_anusvara_visarga_resolution.py`, data registry `data/khmer/romanization_pcgn_anusvara_visarga.csv`. Primary source: BGN/PCGN 1972, p. 4, “Vowel Characters with Anusvara or Visarga”. | Exact table rows 1–8 only; onset analysis and â/ô series are caller-contextualized through Notes 2–3. Row 8 requires explicit final NGA. No syllable segmentation, inferred coda, complete PCGN output, IPA or Ukrainian output. |

The implementation is a source-table component resolver, not a pronunciation model. Independent adjudicated IPA gold remains 0 and empirical accuracy remains null.


## BGN/PCGN inherent-vowel row 1 component — 2026-11-15

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-PCGN-INHERENT-VOWEL-001 | PARTIAL | `resolve_pcgn_inherent_vowel`, `PCGNInherentVowelDecision`, schema `schemas/pcgn-inherent-vowel-decision.schema.json`, tests `tests/test_pcgn_inherent_vowel_resolution.py`, source row `data/khmer/romanization_pcgn_inherent_vowel.csv`. Primary source: BGN/PCGN 1972, p. 2, vowel table row 1. | Explicit NON_FINAL onset only; Note 2–3 series selects â/ô. FINAL abstains pending separate final-consonant/coda handling. No complete syllable, IPA or Ukrainian output. |

The component remains PARTIAL and does not change `KHM-ROM-PCGN-VOWELS-001` or `KHM-ROM-ENGINE-001` from PARTIAL.


## Exact-main verification — PR #249 — 2026-11-15

PR #249 merged as `a50f815f993f8fa9b4ae59c5f0f89b8c7717ea6f`. PR-head push Quality [43760107833], PR Quality [43760141233], PR Chromium [43760141132], exact-main Quality [43760241393], Chromium [43760241451] and Pages [43760241464] all SUCCESS. This verifies engineering integration of the eight source-table rows only; no linguistic accuracy or IPA/Ukrainian acceptance is claimed.


## Exact-main verification — PR #250 — 2026-11-15

PR #250 merged as `62ce69bd17dc64fecfb73e81e22ca10bf97a25ff`. PR-head push Quality [43760551262], PR Quality [43760562169], PR Chromium [43760562155], exact-main Quality [43760662544], Chromium [43760662582] and Pages [43760662587] all SUCCESS. `KHM-ROM-PCGN-INHERENT-VOWEL-001` remains PARTIAL by design: only explicit NON_FINAL onset contexts are mapped. Independent adjudicated IPA gold remains 0; accuracy=null; issue #104 remains OPEN.


## BGN/PCGN consonant table component — 2026-11-15

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-PCGN-CONSONANTS-001 | PARTIAL | `resolve_pcgn_consonant`, `PCGNConsonantDecision`, schema `schemas/pcgn-consonant-decision.schema.json`, tests `tests/test_pcgn_consonant_resolution.py`, source registry `data/khmer/romanization_pcgn_consonants.csv`. Primary source: BGN/PCGN 1972, consonant table pp. 1–2 and Note 3. | Rows 1–21 only; one base plus at most one foot. BA b/p depends on explicit Note 3 exception. Row 22 is delegated to Note 4. No syllable segmentation, vowels/coda, IPA or Ukrainian output. |

The resolver preserves Unicode source identity and does not guess cases requiring lexical reference consultation. Overall `KHM-ROM-ENGINE-001` remains PARTIAL.


## Exact-main verification — PR #251 — 2026-11-15

PR #251 merged as `aab014705bdf90825b922ff69f1c2e7758e56246`. PR-head push Quality [43760857888], PR Quality [43760868532], PR Chromium [43760868545], exact-main Quality [43760984773], Chromium [43760984785] and Pages [43760984838] all SUCCESS. Documentation-only closeout; no linguistic status promotion.


## Exact-main verification — PR #252 — 2026-11-15

PR #252 merged as `16fbbde6238e03290507056388b539f54622d236`. Final PR-head push Quality [43761467383], PR Quality [43761473221], PR Chromium [43761473212], exact-main Quality [43761598283], Chromium [43761598359] and Pages [43761598332] all SUCCESS. Earlier Quality [43761223088] failed on malformed JSON in the new schema; correction and subsequent full checks passed. `KHM-ROM-PCGN-CONSONANTS-001` remains PARTIAL by design; no IPA or Ukrainian acceptance is implied.


## BGN/PCGN final-consonant no-following-vowel component — 2026-11-15

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-PCGN-FINAL-CONSONANT-001 | PARTIAL | `resolve_pcgn_final_consonant`, `PCGNFinalConsonantDecision`, schema `schemas/pcgn-final-consonant-decision.schema.json`, tests `tests/test_pcgn_final_consonant_resolution.py`, rule registry `data/khmer/romanization_pcgn_final_consonant.csv`. Primary source: BGN/PCGN 1972, p. 2 final-consonant statement. | Explicit final position and caller-confirmed absence of vowel character/TOANDAKHIAT; one base plus at most one foot. BA/ALIF abstain. “Generally” is preserved as a qualified rule. No syllable segmentation, IPA or Ukrainian output. |


## Exact-main verification — PR #255 / final-consonant context contract — 2026-11-16

PR #255 merged as `47679154526fa32c5edd9d62ca084de5af4759dd`. PR-head push Quality [43825412435], PR Quality [43825430244], Chromium [43825430217], exact-main Quality [43825536547], Chromium [43825536580] and Pages [43825536491] all SUCCESS. The resolver rejects non-boolean caller context and tests all supported base consonants. This does not change `KHM-ROM-PCGN-FINAL-CONSONANT-001 = PARTIAL`, `KHM-ROM-ENGINE-001 = PARTIAL`, independent IPA gold = 0, or accuracy = null. Issue #104 remains OPEN.


## Exact-main verification — PR #256 documentation closeout — 2026-11-16

PR #256 merged as `dee4881da4cfb01b6da0ff5e857af67cade14cb1`. PR-head push Quality [43825693046], PR Quality [43825710166], Chromium [43825710160], exact-main Quality [43825806168], Chromium [43825806361] and Pages [43825806234] all SUCCESS. Exact-main `pytest -q`: 331 passed, 70 subtests passed; `npm run check`, production build, production Chromium exercise and deployed-site/runtime-asset smoke passed. This documentation-only closeout does not change `KHM-ROM-PCGN-FINAL-CONSONANT-001 = PARTIAL`, `KHM-ROM-ENGINE-001 = PARTIAL`, IPA gold = 0 or accuracy = null. Issue #104 remains OPEN.


## PCGN independent-vowel source evidence — 2026-11-16

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-PCGN-INDEPENDENT-VOWELS-001 | PARTIAL | Runtime mapping `PCGN_INDEPENDENT_VOWEL_ROWS`; auditable source register `data/khmer/romanization_pcgn_independent_vowels.csv`; parity/Note 9 test in `tests/test_pcgn_independent_vowel_resolution.py`. Primary source: BGN/PCGN 1972, Independent/Dependent Vowel Characters table, pp. 2–3, Note 9 p. 5. | Rows 3, 4, 7, 14–22 only. `ឧ` retains both `ŏ`/`ŭ` alternatives without selection. Component romanization only; no IPA/Ukrainian output or empirical accuracy claim. |
