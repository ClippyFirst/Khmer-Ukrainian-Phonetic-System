## Progressive IPA recovery and hybrid candidate selection — 2026-11-23

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-PARTIAL-IPA-001 | DONE_VERIFIED (PR-head exact-input behavior) | PR [#557](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/pull/557); test-first red run [45272634271](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45272634271); final-head Quality [45274851046](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45274851046); Chromium [45274851139](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45274851139). | A lexical fixture with withheld full IPA preserves only an independently supported onset candidate. For `ស៊៉ា`, visible IPA is `/s/⟦EVIDENCE_LIMITED⟧`, UA is `с???`; canonical unit status/IPA remain unresolved, and the separate candidate carries source provenance. No vowel/register/coda/tone/full pronunciation is inferred. |
| KHM-HYBRID-CANDIDATE-001 | DONE_VERIFIED (Python API PR-head) | `HybridKhmerEngine` validates typed provider IPA, maps it with the existing Ukrainian adapter, retains mapping failures, and exposes a separate `PROVISIONAL` candidate only when canonical IPA is unresolved. Final-head Quality [45274851046](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45274851046) passed 475 Python tests + 70 subtests and all JS/Python parity/build checks. | First mappable provider is selected; if none maps, first valid IPA remains visible with an explicit mapping failure. Canonical fields are immutable; no provider voting, accuracy ranking or gold promotion. |
| KHM-KHMERPHONEMIZER-001 | DONE_VERIFIED (opt-in provider smoke) | Pinned `khmerphonemizer==0.0.3`, MIT; optional extra and lazy adapter are explicit opt-in. Final-head smoke [45274851079](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45274851079) passed and emitted a typed `PHONETIC_BROAD` / `PARTIAL` candidate with `profile_match=UNVERIFIED`; artifact [14866596624](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45274851079/artifacts/14866596624), SHA-256 `78cc58c41e921081cc9fc07190e112ab0a71cc5b3c95c3db80b3435e9ac239bf`. | Provider smoke proves executable candidate generation only. It does not prove dialect/profile equivalence, tone/stress completeness, accuracy, or expert adjudication. No auto-discovery; callers must opt in. |
| KHM-BROWSER-LIVE-HYBRID-001 | BLOCKED | GitHub Pages is static; browser CSP sets `connect-src 'none'`. No Python/API inference backend exists. The public page cannot invoke the optional Python provider for arbitrary input. | Requires a separately approved backend/privacy and operational design, or a validated local browser model with pinned rights-cleared assets, size/startup evidence, offline behavior and browser parity. Do not transmit user-entered text or relax CSP silently. |
| KHM-PHON-CONTEXT-001 | PARTIAL (unchanged) | Exact lexical fixtures, narrow inherent-vowel rules, and partial onset preservation; broad dependent-vowel × consonant-series × coda × syllable-context matrix remains incomplete. | Context-qualified, source-located rules and positive/negative fixtures; Python/browser parity; specialist review; no grapheme-to-Ukrainian shortcut. |
| KHM-IPA-GOLD-001 | BLOCKED (unchanged) | Independent expert-adjudicated gold remains 0; issue #104 remains open. | Approved versioned IPA convention, two independent annotators, third adjudicator, curator, private blind intake and rights-cleared 30-item pilot. |
 
**Public-service boundary:** the PR changes are not merged to `main` or deployed. Current PR #557 is a draft continuation branch. Public Pages behavior must not be described as having live multi-provider inference. Broad pronunciation accuracy remains **NOT ASSESSED**.

**Development process gate adopted:** reproduce and minimize the exact defect; document root cause; add a failing regression; make the smallest repair; run Python, Node, structural/lexical/rule/segmentation parity, benchmarks, build and Chromium checks; inspect the complete diff; update this register and the master handoff. A passing unit test alone is not release evidence.

---

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
| Python onset-only preview for unresolved Khmer units | PARTIAL | Separate provisional_ipa/provisional_ukrainian/fallback_status/fallback_trace; canonical ipa/ukrainian unchanged. Shared COENG+subscript fixture added in data/tests/khmer-onset-fallback-fixtures.json; Python assertion added. |
| Browser onset-only preview | PARTIAL | Same onset IPA → existing adapter → ? behavior; per-unit PROVISIONAL status. Commit 862aa061726b2bae6296199e4b655334bb6f609a |
| Browser regression | DONE_VERIFIED (bounded shared-fixture contract) | Python and Playwright consume `data/tests/khmer-onset-fallback-fixtures.json`; Python asserts API null canonical fields and the browser asserts rendered NOT_ESTABLISHED markers. Both verify the same provisional onset IPA/UA, status, rule ID and position. Exact-head Quality and Chromium passed; mainline Quality and Chromium passed. |
| Dedicated grapheme-position evidence registry | TODO | Register primary-source locator, profile, exact position, rule ID, scope and reviewer status for each provisional mapping |
| Exact-head CI and Chromium verification | DONE_VERIFIED for shared fixture | PR #326 exact-head Quality [44111933616] and Chromium [44111963202] SUCCESS; post-merge mainline Quality [44112202827] and Chromium [44112202856] SUCCESS. Mainline Pages [44112203152] SUCCESS. |
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
| KHMER-GOOGLE-TTS-001 | PARTIAL (full file audited; profile and rights unresolved) | Full pinned 69,415-row lexicon audit: 69,405 unique spellings (62,175 Khmer-script, 7,230 Latin); 10 duplicate keys each have divergent readings and no third disambiguation label; 54 used phonemic tokens all match the 56-phone inventory. Festival prompt index adds 2,748 utterance rows/16 speaker-ID prefixes without gender labels. Lexicon file header declares CC BY 4.0. Exact-main after PR #300 merge: Quality [43966413597] SUCCESS (417 Python tests + 70 subtests); Chromium [43966413730] SUCCESS (12/12); Pages deploy/runtime smoke [43966413612] SUCCESS. | Resolve 70,671 paper count vs 69,415 snapshot, 2,748/16 prompt-index discrepancy, target variety and phonemic convention, item-level provenance, duplicate semantics and companion phonology.json license. Candidate comparator only, not IPA gold. |
| KHMER-OPENSLR42-001 | PARTIAL (audio lead; metadata discrepancy) | OpenSLR lists a male-speaker archive and linked CC BY-SA 4.0 LICENSE; 2018 paper reports 17 female speakers/2,906 files/3:58:00; pinned Google Festival prompt index has 2,748 rows/16 speaker-ID prefixes and no gender labels. | Obtain archive manifest/checksum, reconcile repository/paper/provider versions and speaker metadata, verify archive-internal license and transcription scope. Audio/transcripts are not IPA gold. |

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


## Exact-main verification — PR #259 — 2026-11-16

PR #259 merged as `458026f080bca31edeec87c2009245213ab667c7`. PR-head push Quality [43826670914], PR Quality [43826697643], Chromium [43826697687], exact-main Quality [43826837012], Chromium [43826837160] and Pages [43826837175] all SUCCESS. Exact-main `pytest -q`: 332 passed, 70 subtests passed; web checks, production build and deployed-site/runtime-asset smoke passed. The new CSV verifies existing independent-vowel runtime rows and preserves Note 9 ambiguity; `KHM-ROM-PCGN-INDEPENDENT-VOWELS-001 = PARTIAL`, `KHM-ROM-ENGINE-001 = PARTIAL`, IPA gold = 0 and accuracy = null remain unchanged. Issue #104 remains OPEN.


## Exact-main engineering and research gate refresh — 2026-11-16

| ID | Status | Current evidence | Remaining acceptance criteria |
|---|---|---|---|
| KHM-ROM-PCGN-COMPONENTS-001 | PARTIAL | Mainline contains source-backed, typed, bounded component resolvers for consonant rows 1–21, Note 2/3 series and shifters, dependent/independent/inherent vowels, anusvara/visarga, shortening, final consonants, ROBAT, AHSDA, TOANDAKHIAT, glottal onset and Note 10 character inventory. Exact-main Quality run [43841825031](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43841825031) passed. | Build evidence-backed syllable segmentation and orchestration; resolve all required context without guessing; cover remaining PCGN table/note environments; validate full-word output against independent source-located examples. Component tests do not complete the engine. |
| KHM-PHON-001 | PARTIAL | Existing deterministic IPA-first engine, profile abstraction, explicit unsupported states and IPA → Ukrainian adapter remain in main; latest exact-main Quality [43841825031](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43841825031) passed. | Complete source-orthography → phonology → typed IPA coverage for supported profile, including syllable segmentation, vowel × series × length × coda interactions and profile-specific variants; each accepted mapping needs source or adjudicated evidence and cross-runtime regression coverage. |
| KHM-GOLD-001 | BLOCKED | Issue [#104](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/104) remains OPEN. Gold JSONL/TSV remains empty/header-only; independently adjudicated gold count = 0; empirical accuracy = null. | Approve versioned IPA convention; recruit two independent qualified Khmer annotators, separate adjudicator and curator; establish private blind intake; select 30 source-located lexeme groups with item-level rights clearance; lock two annotations per item; adjudicate disagreements; pass provenance, rights, duplicate, schema and blindness checks. |
| KHM-ACCURACY-001 | BLOCKED | No independent adjudicated gold items; no accuracy percentage is reported. | Freeze a non-leaking evaluation manifest after pilot; obtain a sufficiently scoped adjudicated test set; run benchmark with pinned engine/corpus versions and publish metrics with uncertainty and scope. |
| KHM-BRANCH-AUDIT-001 | PARTIAL (ancestry inventory DONE_VERIFIED) | Exact-main inventory at `44c2168e9b4a3f818ad2259f663792a4fc86229b`: 131 refs total (main + 130 non-main), all 130 non-main tips unique. Every non-main ref was compared against main (130/130); open PR count 0. File summaries and spot-checks show many docs-only historical checkpoints and divergent snapshots; representative PCGN, direct-romanization, practical-adapter, coverage, external-G2P and registry branches are already integrated or older/less complete. | Finish content-level review of every changed file/commit and reconcile each branch with its merged/superseded PR ancestry. Preserve historical refs: connected operations expose no branch-delete action and no owner archival policy was supplied. Never merge divergent snapshots wholesale. |

### Exact-main verification — PR #261 — 2026-11-16

PR [#261](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/261) merged as `46a54d9ce86916af2d18a2322167798d43bce6c8`. On that exact main SHA, Quality [43841825031](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43841825031), Khmer browser smoke [43841825019](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43841825019), and Pages build/deploy [43841825034](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43841825034) all SUCCESS. Quality reports 332 passed and 70 subtests passed; web checks, production build, Chromium exercise and deployed-site/runtime-asset smoke passed. Hosted CI only; no local test run is claimed. The verification is engineering/deployment evidence, not linguistic validation.

### Readiness classification — 2026-11-16

The repository is a research foundation with a deployed engineering prototype. It is not linguistically release-ready. The current code is not a complete BGN/PCGN Khmer syllable romanizer, the IPA gold corpus is empty, and no empirical accuracy claim is supportable. The human gate in issue #104 and owner decisions on root licensing metadata and main branch protection remain open.


### Live-main verification refresh — PR #262 — 2026-11-16

PR [#262](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/262) merged as `17657f91f650e4e5f2213bc3546eaefcb7c95202`. On this exact main SHA, Quality [43847284065](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43847284065), Khmer browser smoke [43847284004](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43847284004), and Pages build/deploy [43847283928](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43847283928) all SUCCESS. Quality workflow completed corpus structural validation, Python tests, web checks and site build; browser smoke and deployment completed. Hosted CI only.

The latest branch listing has 131 refs (main + 130 non-main), all 130 non-main tips distinct by SHA. All 130 non-main refs have now been compared against exact main `44c2168e9b4a3f818ad2259f663792a4fc86229b`; content-level review of all changed files and complete PR-ancestry disposition remains PARTIAL. No divergent branch was merged wholesale. Issue #104 remains OPEN; no expert convention, recruitment, blind pilot or adjudicated gold was added. Gold remains 0 and empirical accuracy remains null. Linguistic release readiness is not established.


| KHM-ROM-PCGN-OPEN-CV-001 | DONE_VERIFIED (bounded API) | PR [#264](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/264) merged as `231b8f031ae130828018b18dbdf1c36c6ac47e6a`. Exact PR-head Quality [43880147090] and Chromium [43880147081] passed; push Quality [43880136584] passed. 338 Python tests + 70 subtests passed; web checks and production build passed. | Verified only for explicitly caller-segmented open CV chunks using a supported dependent-vowel pattern. Coda-bearing, shortened, independent-vowel, special-mark, Alif and ambiguous cases abstain. No word segmentation, IPA or Ukrainian output. `KHM-ROM-ENGINE-001` remains PARTIAL. |


### Exact-main closeout — PR #264 and documentation checkpoint — 2026-11-16

PR #264 merged as `231b8f031ae130828018b18dbdf1c36c6ac47e6a`. The documentation closeout produced exact main `5c17d9b1b0d1bbfc079b6d5811749488ca3daad1`. On that SHA, Quality [43880417655](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43880417655), Chromium [43880417532](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43880417532), and Pages build/deploy plus deployed-site/runtime smoke [43880417474](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43880417474) all SUCCESS. Quality reports 338 Python tests + 70 subtests passed; web checks and production build passed. This is engineering verification for the bounded open-CV assembler, not full PCGN or linguistic release validation. Hosted CI only.


| KHM-ROM-PCGN-CLOSED-NOTE5-001 | DONE_VERIFIED (bounded API) | PR [#265](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/265) merged as `664c210d957b0666e5ca85032fb49466018cbf78`. Exact PR Quality [43881403475] and Chromium [43881403279] passed; push Quality [43881383045] passed (342 Python tests + 70 subtests). Exact-main Quality [43881564395], Chromium [43881564314] and Pages [43881564668] also passed. | Scope is exactly inherent+BANTOC, AA+BANTOC and SAMYOK+coda with one supported final consonant. Explicit coda class is cross-checked against resolved PCGN coda value. Unsupported coda, mismatched boundaries/class, ambiguous and malformed inputs abstain. No word segmentation, IPA or Ukrainian output. `KHM-ROM-ENGINE-001` remains PARTIAL. |


| KHM-ROM-PCGN-DEPENDENT-CLOSED-001 | DONE_VERIFIED (bounded API) | PR [#266](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/266) merged as `84880d6c241bfc22e8e095a7cb90f2d32759ced1`. Exact PR Quality [43882269923] and Chromium [43882269991] passed; push Quality [43882139617] passed (347 Python tests + 70 subtests). Exact-main Quality [43882558236], Chromium [43882558488] and Pages [43882558294] also passed on `8df4f5ca146f82d6f8c3892ae686f6f58f7bbaeb`. | Caller supplies onset-only, onset+vowel, full-syllable and coda-only chunks. All 17 normal dependent-vowel table patterns are exercised in both series. Only one supported unmarked final consonant is accepted; shortened/independent vowels, special marks, malformed or mismatched boundaries abstain. No word segmentation, IPA or Ukrainian output. `KHM-ROM-ENGINE-001` remains PARTIAL. |


### Exact-main closeout — PR #266 and documentation checkpoint — 2026-11-16

PR #266 merged as `84880d6c241bfc22e8e095a7cb90f2d32759ced1`. On exact main `8df4f5ca146f82d6f8c3892ae686f6f58f7bbaeb`, Quality [43882558236](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43882558236), Chromium [43882558488](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43882558488), and Pages build/deploy plus deployed-site/runtime smoke [43882558294](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43882558294) all SUCCESS. Quality reports 347 Python tests + 70 subtests passed; web checks, production build and Chromium smoke passed. This verifies the bounded normal dependent-vowel closed-syllable assembler, not full PCGN conformance or linguistic release readiness. Hosted CI only.


### Historical branch ancestry inventory — 2026-11-16

Against exact main `44c2168e9b4a3f818ad2259f663792a4fc86229b`, all 130 non-main branch refs were compared (130/130); all tips were unique and there were zero open PRs. This completes the branch-ref ancestry comparison pass, not a full content audit. File-level comparison summaries show many old documentation checkpoints and divergent snapshots. Representative checks found PCGN source tables and independent-vowel registry already identical to main, old parser branches missing newer main tests, practical-adapter branches with identical `practical.py` but older rule-engine snapshots, and external-IPA registry/benchmark branches with older content than main. The three newly completed assembler branches are already merged through PRs #264–#266. No branch was deleted, force-updated or merged wholesale. `KHM-BRANCH-AUDIT-001` remains PARTIAL until all changed content and PR ancestry are reconciled; retain historical refs pending owner archival policy.


### Final repository checkpoint — 2026-11-16

Exact main before this documentation note: `7a8c1b263ec1e8fa5a8a1395908c661ed5311d42`. PRs #264, #265 and #266 are merged; no open PRs. Exact-main Quality [43884065012](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43884065012), Chromium [43884065118](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43884065118), and Pages build/deploy/runtime smoke [43884065234](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43884065234) all SUCCESS. Quality: 347 Python tests + 70 subtests; browser: 11/11 passed. Branch inventory: 131 refs, all 130 non-main refs compared, all tips unique, no open PRs; content-level review remains PARTIAL. Issue #104 remains open with 0 adjudicated gold items and no empirical accuracy score. Root LICENSE/MIT metadata and main branch protection remain owner blockers. Repository remains an engineering/research prototype, not linguistically release-ready. Hosted CI only; no local test execution claimed.


### KHM-ROM-PCGN-ALIF-ASSEMBLY-001 — DONE_VERIFIED (bounded API)

Added assemble_pcgn_glottal_open_syllable for caller-supplied standalone Alif (អ) onset plus one ordinary dependent-vowel chunk. It composes the existing PCGN Note 4 carrier resolver with the A-series dependent-vowel resolver, validates the exact token prefix, and requires explicit boolean word-initial/following-vowel context. If Note 4 permits an optional apostrophe, both spellings are returned as alternatives rather than silently selecting one. Schema and regression tests cover every current normal dependent-vowel pattern in the A-series, optional-apostrophe behavior and abstention boundaries. IPA/Ukrainian remain null; no segmentation or phonetic behavior is claimed.

PR #267 merged as 6df8c6c176e0098f97a9f4ab1f9583b0bb7caa68. Exact PR-head Quality [43888596780] and Chromium [43888596962] passed on cd1c6fcb33d93e0b1ef0e508207d8139d5d17eb1 (354 Python tests + 70 subtests). Exact-main Quality [43888801455], Chromium [43888801448] and Pages build/deploy/runtime smoke [43888801373] all SUCCESS on 6df8c6c176e0098f97a9f4ab1f9583b0bb7caa68. Hosted CI only; no local test execution claimed. KHM-ROM-ENGINE-001 remains PARTIAL.


### KHM-ROM-PCGN-ALIF-CLOSED-001 — DONE_VERIFIED (bounded API)

Added assemble_pcgn_glottal_dependent_closed_syllable for caller-supplied standalone Alif onset, Alif-plus-normal-dependent-vowel chunk, complete syllable, and one unmarked final consonant. It composes the existing Note 4, A-series dependent-vowel and general final-consonant resolvers; validates exact boundaries and component identity; requires explicit Note 4 context booleans; and preserves optional apostrophe spellings as alternatives. Tests cover every current normal dependent-vowel pattern with a supported coda plus malformed/mismatched and unsupported contexts. This is orthographic PCGN Latin only; IPA/Ukrainian remain null.

PR #269 merged as 482ed151dc99d3fd20714a606c9ad25aa209a99e. Exact PR-head Quality [43889912149] and Chromium [43889912018] passed on d975ca398c42dfe5669b770f9529bbcffda79160 (360 Python tests + 70 subtests). Exact-main Quality [43890093477], Chromium [43890093456] and Pages build/deploy/runtime smoke [43890093482] all SUCCESS on 482ed151dc99d3fd20714a606c9ad25aa209a99e. Hosted CI only; no local test execution claimed. KHM-ROM-ENGINE-001 remains PARTIAL.


### KHM-ROM-PCGN-ALIF-NOTE5-001 — DONE_VERIFIED (bounded API)

Added assemble_pcgn_glottal_shortened_closed_syllable for caller-supplied standalone Alif onset, complete Note 5 syllable and one unmarked coda. It composes the existing Note 4 carrier, Note 5 shortened-vowel and generic final-consonant resolvers for the three exact Note 5 patterns: inherent+BANTOC, AA+BANTOC and SAMYOK+coda. The caller supplies and the implementation cross-checks coda class against final PCGN consonant romanization; Note 4 context flags remain explicit and optional apostrophe output remains variant-preserving. Schema/tests added. IPA/Ukrainian remain null; no segmentation or coda inference is claimed.

PR #271 merged as 9957081db4149ff316695273d8dd525985bd34fd. Exact PR-head Quality [43891125460] and Chromium [43891125490] passed on 43d25e026da0ed22ffcb62ec8e810e28e302d5b3 (368 Python tests + 70 subtests). Exact-main Quality [43891297907], Chromium [43891298013] and Pages build/deploy/runtime smoke [43891297884] all SUCCESS on 9957081db4149ff316695273d8dd525985bd34fd. Hosted CI only; no local test execution claimed. KHM-ROM-ENGINE-001 remains PARTIAL.


### KHM-ROM-PCGN-ROBAT-ASSEMBLY-001 — DONE_VERIFIED (bounded API)

Added assemble_pcgn_robat_closed_syllable for caller-supplied onset, onset-plus-inherent/ordinary-dependent-vowel chunk, complete syllable, final consonant+ROBAT chunk, and bare marked-coda consonant. It composes existing PCGN onset, inherent/dependent vowel, consonant-table and Note 6 ROBAT resolvers. Exact token boundaries and marked-consonant identity are validated. Tests cover the official Note 6 example (ធម៌ → thôrm), a dependent-vowel form and abstention boundaries. This remains orthographic PCGN Latin only; IPA/Ukrainian remain null.

PR #273 merged as 4fee1db13201b9e171b08daa1d4a45f73a396b86. Exact PR-head Quality [43892380539] and Chromium [43892380533] passed on e20241966e77957988ecccf72374b51dfd38b736 (372 Python tests + 70 subtests). Exact-main Quality [43892575946], Chromium [43892575968] and Pages build/deploy/runtime smoke [43892575864] all SUCCESS on 4fee1db13201b9e171b08daa1d4a45f73a396b86. Hosted CI only; no local test execution claimed. KHM-ROM-ENGINE-001 remains PARTIAL.


### KHM-ROM-PCGN-INDEPENDENT-CLOSED-001 — DONE_VERIFIED (bounded API)

Added assemble_pcgn_independent_vowel_closed_syllable for one caller-supplied listed independent vowel plus a final consonant. The caller supplies independent-vowel-only, complete-syllable and coda-only chunks; exact token boundaries and component identity are validated. The adapter composes the independent-vowel table resolver with the existing generic final-consonant rule, which is only invoked with explicit negative context for following vowel character and TOANDAKHIAT. All 12 mapped independent-vowel characters are covered with a supported coda. Note 9 ឧ remains unresolved and retains ŏ/ŭ alternatives. Schema/tests added. Orthographic PCGN Latin only; IPA/Ukrainian remain null; no segmentation is inferred.

PR #275 merged as 0e408e4d2ce18228e7b8327ddc71af5bdb302f72. Exact PR-head Quality [43910476719] and Chromium [43910476885] passed on f0385ec3846f5ce2a4616f2c65e06142c20e6fe2: 377 Python tests + 70 subtests, corpus validation, web checks, production build and visible-results Chromium smoke all passed. Exact-main Quality [43910647111], Chromium [43910647145], and Pages build/deploy/runtime smoke [43910647200] all passed. Hosted GitHub Actions only; no local test execution claimed. KHM-ROM-ENGINE-001 remains PARTIAL.


## ALA-LC Khmer word-division evidence reconciliation — 2026-11-16

Primary LOC sources establish a version distinction that must precede segmentation work. The 1989 *Cataloging Service Bulletin* No. 43, Khmer p. 54 Note 10, and the ALA-LC Khmer 1997 table, pp. 97–98 Note 10, state the shortest written form that can stand alone as a word; both include Pali/Sanskrit loans and preserve original-language divisions for other loans. The ALA-LC 2013 table instead states at Note 8 that any word can be separated when romanizing, while retaining the loan-word distinction. The current 2013 wording is not to be silently rewritten as the 1997 algorithm. BGN/PCGN 1972 Note 9 is unrelated: it concerns ឧ = ŏ/ŭ.

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-ROM-LOC-WORD-DIVISION-EVIDENCE-001 | DONE_VERIFIED | Official LOC 1989, 1997 and 2013 primary documents located and compared; detailed audit: [LOC Khmer word-division evidence, 2026-11-16](LOC-KHMER-WORD-DIVISION-EVIDENCE-2026-11-16.md). | Evidence reconciliation only; no segmentation implementation or conformance claim. |
| KHM-ROM-LOC-WORD-SEGMENTATION-001 | BLOCKED / TODO | LOC notes do not provide a machine segmentation algorithm or lexical inventory. LaoNLP syllable splitting/maximal matching is not equivalent to the LOC lexical criterion. | Select a versioned ALA-LC profile, obtain licensed lexicon and independent word-boundary annotations, preserve loan-word language classes and ambiguity, then implement/test. |

No runtime behavior, IPA, Ukrainian output, corpus label or benchmark result changed. The PCGN Note 9 ambiguity remains independent and unchanged.


### KHM-STRUCT-SUBSCRIPT-INDEPENDENT-VOWEL-001 — DONE_VERIFIED (structural scope only)

The Khmer parser now recognizes Unicode Standard 18.0.0 Chapter 16 §16.4.1's documented subscript independent-vowel form (example `ផ្ឯម`). It preserves U+17D2 COENG + U+17AF as a typed `subscript_independent_vowel` grapheme, retains the following consonant in the same orthographic unit, records Unicode 18 provenance, and exposes exact-source code-point spans for the encoded pair. It does not establish IPA, Ukrainian output, complete Khmer syllable segmentation or word boundaries.

PR #282 merged as `dd94f637674ad5ce599ee439584b88b6dba4db1e`. Exact-main Quality [43947114555] passed 393 Python tests + 70 subtests, independent IPA corpus structure validation, Node/web checks and production build; Chromium [43947114448] and Pages deploy/runtime smoke [43947114535] passed. Issue #104 remains OPEN; no independent lexical IPA gold or accuracy score is created by this task.


## Khmer Unicode orthographic-component scan — 2026-11-16

| ID | Status | Evidence / acceptance boundary |
|---|---|---|
| KHM-ORTHO-COMPONENT-SCAN-001 | PARTIAL | New Python/browser component scanner, public API, `khmer-orthographic-components/v1` schema and Unicode 18 example tests on branch `feat/khmer-orthographic-component-scanner-2026-11-16`. It classifies known base letters, subscript pairs, robat, shifters, dependent vowels, join controls and other signs with exact code-point spans. It deliberately withholds ambiguous multiple-base parsing. Acceptance requires exact-head Python/browser CI and main verification; full Unicode BNF parsing, syllable segmentation and word boundaries are not included. |

The scanner is structural only. No IPA labels, Ukrainian outputs, lexical boundaries or gold records were added. Unicode 18 Chapter 16 §16.4 supplies the component inventory/order; UAX #29 Revision 49 supplies default grapheme/word segmentation guidance but does not remove the need for Khmer-specific syllable/word tailoring.


### KHM-ORTHO-COMPONENT-SCAN-001 — DONE_VERIFIED (component scanner scope only)

PR #283 merged as `bdc15daf6f7c40a6c088e306343a421b9347e9c1`. The Python and browser runtimes expose the same `khmer-orthographic-components/v1` roles/statuses and exact Unicode code-point offsets. The scanner identifies modeled bases, COENG subscript pairs, robat, shifters, dependent vowels, join controls and other modeled signs; ambiguous multiple-base spans remain `EVIDENCE_LIMITED`.

Exact PR-head Quality [43953219338] and Chromium [43953219579] succeeded. Exact-main Quality [43953449784] passed 402 Python tests + 70 subtests, IPA corpus engineering validation, Node/web checks and build; Chromium [43953449807] and Pages deploy/runtime smoke [43953450103] succeeded.

Acceptance boundary: this does not complete Unicode BNF sequence validation, full Khmer orthographic-syllable segmentation, word segmentation, pronunciation, IPA coverage or Ukrainian target validation. Independent IPA gold remains 0 and empirical accuracy remains null.


## Unicode 18 Khmer orthographic-syllable parser — 2026-11-16

| Task ID | Status | Scope / acceptance |
|---|---|---|
| KHM-ORTHO-COMPONENT-SCAN-001 | DONE_VERIFIED | Lossless Python/browser component inventory, exact code-point spans and versioned schema; PR #283 and exact-main CI verified. This does not validate the full BNF. |
| KHM-ORTHO-BNF-PARSER-001 | DONE_VERIFIED | Unicode 18 §16.4/Appendix A.2 Python/browser packed parser; all complete segmentation and grammar-role alternatives, exact code-point offsets, source reconstruction, rejected spans/reasons, shared examples; exact-main Quality/Chromium/Pages passed on 8ec4460. |
| KHM-ORTHO-TN61-MODERN-PROFILE-001 | TODO / NON_NORMATIVE | Source metadata registered as unicode-tn61-khmer-encoding-structure-v2. Optional separately versioned Modern Khmer validator; keep distinct from normative Unicode 18 BNF and record its proposed/non-normative status. |

Orthographic parsing does not implement phonological syllabification, LOC word division, IPA or Ukrainian output. The source reconciliation and detailed acceptance contract are in `docs/audits/current/UNICODE-KHMER-ORTHOGRAPHIC-SYLLABLE-GRAMMAR-2026-11-16.md`. TN #61 v2 is registered as non-normative metadata only; no source corpus or gold labels were added.


## Unicode 18 parser post-merge verification — 2026-11-16

KHM-ORTHO-BNF-PARSER-001 is DONE_VERIFIED on main commit 8ec4460a0af291dcba10563912f8fcd0c3f784fd. Exact-main Quality [43963765593] passed 417 Python tests + 70 subtests, IPA corpus structural validation, Node/web checks and production build; Chromium [43963765334] passed; Pages deploy/runtime smoke [43963765391] passed. The Python/browser packed parser preserves complete boundary alternatives and grammar-role derivations, exact code-point offsets, source reconstruction and rejected spans/reasons.

TN #61 v2 is registered as unicode-tn61-khmer-encoding-structure-v2 with its date/version, independent non-normative status and Terms-of-Use limitations. The Modern Khmer validation profile remains TODO; no TN61-derived rules are mixed into the Unicode 18 parser.

## Google Khmer TTS lexicon — full-file evidence checkpoint — 2026-11-16

- The pinned archived Google Language Resources lexicon was fully inspected, not sampled: 69,415 rows, 69,405 unique spellings (62,175 Khmer-script; 7,230 Latin-script). Ten spelling keys each have two divergent readings; every row has two columns despite the header's optional third-label description.
- All 54 phonemic tokens used by the lexicon occur in the companion 56-phone JSON inventory. This is structural symbol-set consistency, not a claim of IPA correctness or independent annotation.
- The lexicon file itself declares CC BY 4.0. The companion phonology JSON's file-level rights remain ambiguous between the repository's Apache-2.0 default and the paper's broad CC BY 4.0 data statement. The paper reports 70,671 entries, not the 69,415 present in the pinned file, and supplies no target dialect or per-item provenance.
- `KHMER-GOOGLE-TTS-001 = PARTIAL`; use only as a candidate phonemic comparator pending profile/convention/provenance/rights review. Do not promote to IPA gold. Issue #104 remains OPEN; gold=0; accuracy=null.

### KHMER-GOOGLE-TTS-001 — exact final-head verification — 2026-11-16

- PR #300 final head `65bbc704a5bcf6906f5d57841a625e6f9a2b0f29`, six source/documentation files only.
- Quality [43965487859] SUCCESS: **417 Python tests + 70 subtests**, independent IPA corpus structural validation, Node/web checks and production build.
- Khmer browser smoke [43965487827] SUCCESS: deterministic web checks, production build and Chromium visible-result checks. No local tests or Pages deployment are claimed.
- This closes the engineering verification for the source audit only. `KHMER-GOOGLE-TTS-001 = PARTIAL` remains so until target-variety/convention, per-item provenance, duplicate semantics, 70,671-vs-69,415 snapshot discrepancy and companion `phonology.json` license scope are resolved. `KHM-GOLD-001 = BLOCKED`; gold=0; accuracy=null; Issue #104 remains OPEN.

### Verification boundary after documentation closeout — 2026-11-16

The last completed hosted checks belong to code-bearing documentation/source-record head `65bbc704a5bcf6906f5d57841a625e6f9a2b0f29`: Quality [43965487859] SUCCESS (417 Python + 70 subtests) and Chromium [43965487827] SUCCESS (12/12 Playwright tests). Three subsequent commits updated only the canonical handoff, linguistic completion register and repository audit; the current PR #300 head is `bac8b70210ca01241bec73b516f55abdc278cb98` (12 commits ahead, 0 behind base `941fbf0ed01ae79c2a8be0c02f1870b68e19134a`). The final three commits do not alter source registry, runtime, test files, generated artifacts or corpus payload. The workflow-run lookup exposed no run associated with `bac8b702...`, so **do not describe the last successful checks as exact-head checks for the current PR head**. PR #300 remains OPEN; compare reports no divergence from base, but GitHub's PR snapshot currently reports `mergeable=false`; no merge was attempted.

 
### Final post-PR #300 mainline verification — 2026-11-16

PR #300 merged as `b60a65179ffbb593fca8f3eb2c07a1c81e6e8489` (final PR head `07608ca77a06eee741f2988f4e8611d5ebb26880`); issue #300 is closed. Exact-main Quality [43966413597] SUCCESS (417 Python tests + 70 subtests, corpus structural validation, Node/web checks and production build); Chromium [43966413730] SUCCESS (12/12 Playwright tests); Pages deploy/runtime smoke [43966413612] SUCCESS.

`KHMER-GOOGLE-TTS-001 = PARTIAL`: source and prompt-index audits are complete, but this resource remains a candidate phonemic comparator, not IPA gold. The 70,671 paper count vs 69,415 lexicon rows and 2,906/17 paper audio metadata vs 2,748/16 Festival prompt index vs current male-only OpenSLR archive remain unresolved. Companion phonology JSON rights, target variety, phonemic convention and per-item provenance remain unresolved.

`KHMER-OPENSLR42-001 = PARTIAL`: archive manifest/checksum and historical-version/speaker reconciliation remain required. `KHM-GOLD-001 = BLOCKED`: independent adjudicated gold remains 0; empirical accuracy remains null. Issue #104 remains OPEN. No local tests or data imports are claimed.

## Khmer IPA convention sheet — evidence synthesis draft — 2026-11-17

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-IPA-CONVENTION-001 | PARTIAL (draft prepared; expert approval blocked) | New [expert-review draft](../../ipa-gold/khmer-pph-careful-citation-ipa-v1-draft.md). Synthesizes Minegishi 1985 (series-conditioned vowels/coda/dialect distinctions), Chem 2020 (four selected PPK speakers, 61 formal frame-read items × 3; F1/F2/duration, no F0/stress), Kirby 2014 (multiple cues in colloquial /r/-loss), and Mam et al. 2025 (five Greater Phnom Penh speakers, 50 words × 3; F0 in stressed rimes; possible PPK pitch phonologization, not a general citation-form tone rule). Source registry includes Minegishi with exact page ranges. | Draft proposes PHONETIC_BROAD but is explicitly NOT_APPROVED. Requires a qualified target-profile Khmer phonetician/phonologist to approve or replace it, second independent review, complete symbol/feature policy and documented sign-off. No annotations may start under this draft. |

## KHM-IPA-CONVENTION-001 — merged expert-review draft — 2026-11-17

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-IPA-CONVENTION-001 | PARTIAL (draft merged; expert approval blocked) | PR [#306](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/306) merged as `4d7e7bd045544d2a6d407511679761a7b0b839a1`. Exact PR-head Quality [43969775235] SUCCESS (417 Python + 70 subtests; corpus structural validation, Node/web checks, production build); Chromium [43969775186] SUCCESS (12/12 Playwright). The draft is `docs/ipa-gold/khmer-pph-careful-citation-ipa-v1-draft.md`; Minegishi 1985 source registered with pp. 43–53 and 55–66 locators. | The sheet remains `DRAFT_NOT_APPROVED`; `PHONETIC_BROAD` is only a proposal. Requires qualified target-profile expert approval/replacement and independent challenge review. No gold labels or annotations created. `KHM-GOLD-001` remains BLOCKED; gold=0; accuracy=null. |

 
### Consolidated external Khmer source audit — 2026-11-17

| ID | Status | Evidence / boundary |
|---|---|---|
| KHMER-MEKONGPHON-001 | PARTIAL | 8,040-row seed lexicon audited (8,026 Headley words + 10 numerals + 4 punctuation); 7,940/100 lexical split; no per-item source IDs; sentence labels are longest-match dictionary pseudo-labels over OPUS, not independent speech transcription. Dataset rights unknown; Headley profile/convention not equivalent to approved contemporary Phnom Penh profile. External comparator only; no import/gold. |
| KHMER-OPEN-DICT-IPA-001 | PARTIAL | 3,286 rows, 3,261 unique spellings, 25 repeated keys (one divergent), 63 multi-pronunciation rows. CC BY-NC-SA 4.0 third-party data; preserve alternatives; comparator only and non-commercial. |
| KHMER-ACOUSTIC-MODEL-001 | BLOCKED | Pinned upstream repo exposes only six-line sample dictionary; full dictionary, model archive, 137-hour audio corpus and manual alignments absent. Conflicting counts (29,204/33,091) and data-license claims (CC BY-SA 4.0/CC BY 4.0); no official MFA model entry. |
| KHM-GOLD-001 | BLOCKED | Independent expert-adjudicated IPA gold remains 0; empirical accuracy remains null. |

No external data/model/audio was imported. No source candidate is promoted to gold. Source metadata is consolidated on the 2026-11-17 integration branch; exact-head CI is pending.

 
## Final consolidated-source merge verification — 2026-11-17

- PR [#307](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/307) merged by squash as `43bdeb27821c9308d9b29b693c2cdbbafb72fa7b` from exact head `bf80a8cd8a96dee2ffae5acf2c6f7d9b38317cd0`, based on `db02740d57705c08966c87a6b31a5c874c9edc86`.
- Exact PR-head Quality [43970804968] SUCCESS: **417 Python tests + 70 subtests**, IPA corpus structural validation, Node/web checks and production build.
- Exact PR-head Chromium [43970804939] SUCCESS: **12/12 Playwright tests**.
- Exact-main Quality [43970986954] SUCCESS: **417 Python tests + 70 subtests**, corpus validation, Node/web checks and production build.
- Exact-main Chromium [43970986386] SUCCESS: **12/12 Playwright tests**.
- Exact-main GitHub Pages [43970986366] SUCCESS: production build, Chromium production exercise, deployment and published-site/runtime-asset smoke.
- PRs #301, #303 and #304 were closed as superseded by #307. Their source branches were intentionally preserved; no force-push or branch deletion occurred. PR #307 leaves no open PRs at this checkpoint.
- Issue #104 remains OPEN. No experts were contacted or recruited. `KHM-IPA-CONVENTION-001` remains PARTIAL / `DRAFT_NOT_APPROVED`; `KHM-GOLD-001` remains BLOCKED, adjudicated gold=0 and empirical accuracy=null.
- Undermind's semantic/deep-search operation could not be continued in this session because its free usage limit was reached; the tool reported reset at 2026-11-16 23:30 UTC (2026-11-17 01:30 Kyiv time). No Undermind search result is claimed for this continuation.
- No local checkout/tests were run. All code/test/build/browser/deployment evidence above is from GitHub Actions. No external data, model weights, audio, IPA labels or Ukrainian mappings were imported.

## Kirby Phnom Penh cluster-audio source — 2026-11-17

| ID | Status | Evidence / acceptance boundary |
|---|---|---|
| KHM-KIRBY-CLUSTER-AUDIO-001 | PARTIAL | Registered [Kirby 2013 audio/TextGrid dataset](../../ipa-gold/khmer-kirby-cluster-audio-source-audit.md), DataShare DOI 10.7488/ds/2454, CC BY 4.0. Primary metadata documents 10 native Phnom Penh speakers, 79 lexical items, 3 repetitions and slow/fast conditions; the 2014 paper analyses 61 cluster items across 35 onset types and describes the first block as slow-and-careful carrier-sentence reading. Strong supporting audio candidate, but not IPA gold. Full archive item manifest/checksum is not yet inspected; carrier-sentence task equivalence to the careful-citation profile and contrast coverage require expert review. No data imported; gold=0; accuracy=null. |

No IPA labels, model outputs, audio payload or Ukrainian mappings were added by this source registration. The 30-item blind pilot remains blocked on convention approval, profile fit, qualified independent annotators/adjudicator, non-annotating curator, private blind intake, rights/locator checks and expert-approved contrast coverage.

## Kirby cluster-audio candidate — merged engineering verification — 2026-11-17

| ID | Status | Evidence / acceptance boundary |
|---|---|---|
| KHM-KIRBY-CLUSTER-AUDIO-001 | PARTIAL | PR [#309](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/309) merged as `417ddfe598fc70913d9597dc5fb0b4dc7863d515`. Exact PR-head Quality [44039162569] SUCCESS (417 Python tests + 70 subtests, IPA corpus validator, Node/web checks, Vite build); Chromium [44039174297] SUCCESS. Source is CC BY 4.0 supporting audio, not IPA gold. Archive not downloaded; listed MD5 not locally verified; 79-item manifest and careful-citation profile equivalence remain open. |

No gold rows, IPA labels, audio payload, model output or Ukrainian mappings were created. Issue #104 remains open; `KHM-IPA-CONVENTION-001 = PARTIAL / DRAFT_NOT_APPROVED`; `KHM-GOLD-001 = BLOCKED`; gold=0; empirical accuracy=null. Post-merge mainline checks are tracked separately from exact PR-head verification.

## Kirby 2011 Phnom Penh tonogenesis datasets — 2026-11-17

| ID | Status | Evidence / acceptance boundary |
|---|---|---|
| KHM-KIRBY-TONOGENESIS-AUDIO-001 | PARTIAL | Enriched existing source record for [2011 audio/TextGrid dataset](../../ipa-gold/khmer-kirby-tonogenesis-datasets-audit.md), DOI 10.7488/ds/321, DataShare CC BY 4.0. DataShare describes 16 Phnom Penh speakers; Kirby (2014) §3.1–3.2 reports 20 recruited participants (13 female, 21–60), 41 careful/read items × 3, separate 15 colloquial items × 3, and four participants excluded from further analysis for retaining /r/ in both conditions, leaving 16 analyzed. This plausibly reconciles the counts, but exact archive folder membership remains unverified. Appendix A provides romanized items/glosses, not Khmer-script forms. Supporting /r/-loss/prosody evidence only, not IPA gold. |
| KHM-KIRBY-TONOGENESIS-SUPP-001 | PARTIAL | Enriched existing source record for [2011 supplementary dataset](../../ipa-gold/khmer-kirby-tonogenesis-datasets-audit.md), DOI 10.7488/ds/319, DataShare CC BY 4.0. Includes anonymised production/perception CSVs, KlattGrid stimuli, plots and R code. Bundle/schema not inspected; natural production measurements must be distinguished from synthetic stimuli and perceptual responses. Not IPA gold. |

No audio or supplementary payload was downloaded/imported, no IPA labels were added, and no 30-item pilot entries were selected. Gold remains 0; empirical accuracy remains null. Specialist approval is still required for profile fit and any use of the reading condition.

## KHM-KIRBY-TONOGENESIS — merge and engineering gate — 2026-11-17

PR #310 merged as `4d568f712b8ac055809bc01e53ea7d257b79a6a0`. Exact PR head passed Quality (417 Python tests + 70 subtests, corpus structural validator, Node/web checks, Vite build) and Chromium (12/12 Playwright tests). Post-merge mainline Quality and Chromium also passed; existing Pages workflow deployed and smoke-tested root page, `system.html`, JS and CSS successfully. This confirms repository/build integrity only, not linguistic validity or profile acceptance.

Source status remains PARTIAL: existing Kirby audio and supplementary records are enriched; archive not downloaded, provider MD5s not locally verified, Appendix A has romanized forms rather than Khmer-script orthography, archive folder membership not inspected, and no item-level token manifest. The likely 20 recruited → 4 excluded → 16 analyzed sample flow plausibly explains DataShare's 16-speaker metadata. No IPA labels or gold rows created. Issue #104 OPEN; convention `DRAFT_NOT_APPROVED`; gold=0; accuracy=null.


## Sok & Adams (2016) rule-system source review — 2026-11-17

| ID | Status | Evidence / acceptance boundary |
|---|---|---|
| KHM-SOK-ADAMS-2016-001 | DONE_VERIFIED (source audit only) | Full PACLIC 30 paper inspected (pp. 417–424); source registry and [dossier](../../ipa-gold/khmer-sok-adams-phonological-principles-audit.md) record two-stage careful-phonemic vs rapid-colloquial-phonetic design, rule families, data provenance, evaluation limits and rights uncertainty. No rules were transferred to runtime. |
| KHM-SOK-ADAMS-RULE-TRANSFER-001 | BLOCKED | Visual source audit and current-code comparison completed; remaining blocker is qualified contemporary Phnom Penh careful-citation review plus source-located, independently supported rule environments. | Transfer only individually approved rules with exact source/page locator, typed phonological-vs-phonetic layer, contemporary PPK evidence, positive/negative regression items and rights basis. |
| KHM-SOK-ADAMS-DATA-REUSE-001 | DEFERRED | The 140-word validation set and 10,110-word dictionary comparison are not independent blind audio gold; no dataset rights or reproducible independent split established. Do not import or benchmark against them as project gold. |

The reported 97.86% and 98.43% values are the paper's own results and do not alter repository accuracy (still null). Independent adjudicated gold remains 0; `KHM-IPA-CONVENTION-001` remains `DRAFT_NOT_APPROVED`; `KHM-GOLD-001` remains BLOCKED.


## Explicit IPA transcription-kind contract — 2026-11-17

| ID | Status | Evidence / acceptance |
|---|---|---|
| KHM-IPA-KIND-001 | DONE_VERIFIED (contract repair) | Added `ipa_kind` to every typed internal phonetic-result unit. Linguistic units are `UNRESOLVED` and punctuation is `NOT_APPLICABLE`; schema and regression tests enforce this. This avoids silently assigning PHONEMIC/PHONETIC_BROAD/PHONETIC_NARROW before convention approval. |
| KHM-IPA-KIND-APPROVAL-001 | BLOCKED | A qualified Phnom Penh Khmer phonetician and independent reviewer must approve one kind and its full symbol/feature policy; only then can the internal value be promoted from `UNRESOLVED`. |

No IPA string, source label, Ukrainian mapping or gold row changed. The kind remains explicitly unresolved; gold=0 and empirical accuracy=null.


## Final mainline verification — Sok & Adams + explicit IPA kind — 2026-11-17

| Work | Status | Evidence |
|---|---|---|
| KHM-SOK-ADAMS-2016-001 | DONE_VERIFIED (source audit only) | PR #311 merged as `10016150244821c1727d06312825aa625f4e1d42`; full PACLIC 30 paper reviewed; source record and dossier committed. PR-head Quality 44064387019 and Chromium 44064386990 SUCCESS; exact-main Quality 44064764141, Chromium 44064764016 and Pages 44064764164 SUCCESS. |
| KHM-IPA-KIND-001 | DONE_VERIFIED (contract repair) | PR #312 merged as `c426d1c3bacd6edb303b2b4977e5b34c09b81620`; Python and browser typed results expose `ipa_kind`; linguistic units UNRESOLVED, punctuation NOT_APPLICABLE. PR-head Quality 44065466424 SUCCESS (418 Python tests + 70 subtests); Chromium 44065466500 SUCCESS (12/12). Exact-main Quality 44065655690, Chromium 44065655890 and Pages 44065655951 SUCCESS. |
| KHM-IPA-KIND-APPROVAL-001 | BLOCKED | Qualified target-profile phonetician and independent reviewer must approve PHONEMIC, PHONETIC_BROAD or PHONETIC_NARROW and full symbol/feature policy before internal kind changes from UNRESOLVED. |
| KHM-GOLD-001 | BLOCKED | Independent adjudicated IPA gold remains 0; empirical accuracy remains null. Requires rights-cleared exact audio/token locators, two independent annotators, adjudicator and non-annotating curator. |

Final main SHA: `c426d1c3bacd6edb303b2b4977e5b34c09b81620`. Source registry: 49 records / 49 unique IDs. No local tests, audio import, IPA gold rows, runtime pronunciation-rule changes or Ukrainian mapping changes were made by the source audit or IPA-kind contract repair. No open PRs; issue #104 remains OPEN; working branches retained.


## Phnom Penh phonetic literature full-text review — 2026-11-17

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-CHEM-2020-FULLTEXT-001 | DONE_VERIFIED (source audit only) | Chem (2020) full text reviewed; four-speaker final sample, 61 formal frame-read items, unreported complete wordlist, non-itemized replacements, F1/F2/duration scope and inventory/notation limitations recorded with page locators in [the audit](../../ipa-gold/khmer-phonetic-literature-fulltext-review-2026-11-17.md). | Supports a bounded acoustic vowel discussion only; not a complete IPA convention or reproducible pilot wordlist. |
| KHM-MAM-2025-FULLTEXT-001 | DONE_VERIFIED (source audit only) | Mam et al. (2025) full text reviewed; five Greater Phnom Penh speakers, 50 targets, PPK/SK frame tasks, normalized F0/functional-PC methods, incomplete wordlist and qualified “may have phonologized” conclusion recorded with locators in [the audit](../../ipa-gold/khmer-phonetic-literature-fulltext-review-2026-11-17.md). | Supports qualified pitch/F0 research only; does not establish a categorical general tone inventory or citation-form tone rule. |
| KHM-PILOT-30-LEXEMES-001 | BLOCKED | Neither paper publishes the complete target wordlist with exact source-exact item/audio locators. | 30 attested groups with exact forms, glosses, locators, contrast rationale and rights; expert-approved convention/profile fit. |
| KHM-IPA-KIND-APPROVAL-001 | BLOCKED | IPA convention remains DRAFT_NOT_APPROVED; runtime `ipa_kind` remains UNRESOLVED for linguistic units. | Written target-profile phonetician approval plus independent challenge review of the complete symbol/feature policy. |
| KHM-GOLD-001 | BLOCKED | Independent adjudicated gold remains 0; empirical accuracy remains null. | Rights-cleared pilot items; two independent annotators; third adjudicator; non-annotating curator; private blind intake; provenance/schema/rights checks. |

No pronunciation rule, IPA label, gold row, source permission, Ukrainian mapping or generated artifact changed in this review.


## PR #314 post-merge verification — 2026-11-17

| Work | Status | Evidence |
|---|---|---|
| KHM-CHEM-2020-FULLTEXT-001 / KHM-MAM-2025-FULLTEXT-001 | DONE_VERIFIED (source audit only) | PR #314 merged as `4760964618f05290560372b1ee60b4f7fba8ae72`; exact-head Quality [44076405229] SUCCESS (418 Python tests + 70 subtests, corpus structural validation, Node/web checks, Vite build); Chromium [44076405251] SUCCESS (12/12). |
| KHM-PILOT-30-LEXEMES-001 | BLOCKED | No source-exact 30-item set; full lists and exact item/audio locators absent from Chem/Mam papers. |
| KHM-IPA-KIND-APPROVAL-001 | BLOCKED | No qualified target-profile sign-off; `ipa_kind` remains UNRESOLVED. |
| KHM-GOLD-001 | BLOCKED | Gold remains 0; empirical accuracy remains null; requires rights-cleared items, two independent annotators, separate adjudicator, curator and private blind intake. |

Final main SHA at this checkpoint: `4760964618f05290560372b1ee60b4f7fba8ae72`. No Pages deployment was required for the documentation-only PR; no local test execution is claimed.


## Mixed-script and Khmer-numeral token boundaries — 2026-11-17

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-MIXED-SCRIPT-NUMERAL-BOUNDARIES-001 | PARTIAL | PR #316 adds Python/browser script-run isolation, numeric-run isolation, NON_LINGUISTIC passthrough with ipa_kind NOT_APPLICABLE, and source-reconstruction regressions. | Exact PR-head and post-merge Quality, Chromium and Pages checks must pass. Foreign-script units remain unsupported; Khmer word segmentation, number reading and foreign-language translation are not implemented. |

The new status is structural/output handling only. It adds no IPA, lexical entries, pronunciation claims, word-boundary decisions or gold-corpus rows. Issue #104 and all human IPA/word-boundary adjudication gates remain open.


## Mixed-script and Khmer-numeral boundaries — 2026-11-17

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-MIXED-SCRIPT-NUMERAL-BOUNDARIES-001 | DONE_VERIFIED | PR #316 merged as `cca8612e98292ce2ee2f103e12bcce152d4b3416`. PR-head Quality [44079343371] and Chromium [44079343343] passed; post-merge Quality [44079454281] passed (422 Python tests + 70 subtests, validator, Node/web checks, Vite build), Chromium [44079454289] passed (13/13), and Pages [44079454302] passed (production browser, deploy and deployed-site/runtime-asset smoke). | Verified structural/output handling only: Khmer, foreign-script and numeric runs stay isolated with exact source reconstruction; foreign text remains unsupported; numbers pass through as NON_LINGUISTIC / NOT_APPLICABLE; U+200C ZWNJ stays within the Khmer run. No lexical segmentation, number reading, translation, IPA or gold data added. |

The initial browser run on the prior PR head failed one stale assertion that expected mixed input to invalidate the valid Khmer neighbor; the assertion was corrected and the latest exact-head browser suite passed. Issue #104 remains OPEN; IPA convention remains DRAFT_NOT_APPROVED; adjudicated gold=0; empirical accuracy=null.


### Post-merge verification — KHM-MIXED-SCRIPT-NUMERAL-BOUNDARIES-001 — 2026-11-17

DONE_VERIFIED at main `cca8612e98292ce2ee2f103e12bcce152d4b3416`. Mainline Quality [44079454281], Chromium [44079454289] and Pages [44079454302] all SUCCESS. Python 422 passed + 70 subtests; Chromium 13/13. The corpus validator's `NOT_READY_NO_ADJUDICATED_GOLD` is the expected research state, not a software failure.

This task's DONE_VERIFIED status applies only to deterministic script/numeral token boundaries and non-linguistic passthrough. It does not close the human linguistic acceptance gates: IPA convention DRAFT_NOT_APPROVED; `ipa_kind` UNRESOLVED for linguistic units; independent adjudicated gold 0; empirical accuracy null; Issue #104 OPEN.

## Expert shortlist revalidation — 2026-11-17

| Candidate | Potential scoped role | Evidence | Limit / conflict |
|---|---|---|---|
| Chem Vatho | Primary Phnom Penh careful-citation IPA convention reviewer | Current CV/profile identifies native Khmer, Dr. phil. in Phonetics (2025), Central Khmer phonetic-reduction dissertation, RUPP Khmer/linguistics teaching, Royal Academy linguistics committee, acoustic phonetics and IPA convention design; Phnom Penh IPA Illustration listed under revision. | Verify credentials/status and profile fit directly. Maintains Khmer acoustic-model/dictionary resource; disclose and exclude him from sole adjudication/independent validation of his own resource-derived items. |
| James P. Kirby | Independent technical challenge reviewer for /r/-loss, F0/VOT, phonation, clusters and style boundaries | LMU profile: phonetics/speech science and Southeast Asian tone/register; peer-reviewed PPK tonogenesis and onset-pitch studies. | Not documented as native Khmer or full-profile authority; check collaboration/conflicts with Vatho before assigning independent status. |
| Nielson Sophann Hul | Scoped laryngeal/implosive review | Cornell profile: PhD work on Khmer acoustic phonetics of laryngeal sounds; heritage Khmer teaching. | Co-authored forthcoming Khmer diphthong chapter with Becky Butler; not independent from her for review-count purposes. |
| Becky Butler | Scoped sesquisyllable/cluster/diphthong review | UNC profile/publications: phonetics/phonology of mainland Southeast Asian languages; Khmer/Bunong sesquisyllable research. | Co-authored forthcoming Khmer diphthong chapter with Nielson Hul; not independent from him. |
| Honglada Klaharn | Structural/phonological challenge only | 2019 Phnom Penh Khmer study reports ten native Phnom Penh speakers over 50; PhD Linguistics metadata. | No inspected evidence of experimental phonetics or IPA-convention expertise. |
| Sothornin Mam | PPK pitch/F0 evidence review | ChulaSEAL summary of 2025 study with five native PPK speakers. | Native-language status and complete convention expertise not established by inspected public sources. |

All are leads only. No outreach, consent or appointment. This update does not satisfy IPA approval, annotator/adjudicator recruitment or pilot acceptance. KHM-IPA-CONVENTION-001 remains DRAFT_NOT_APPROVED; KHM-PILOT-30-LEXEMES-001 and KHM-GOLD-001 remain BLOCKED; adjudicated gold=0; empirical accuracy=null. See [the playbook](../../ipa-gold-collection-playbook.md) for role design and source links.


## Expert shortlist revalidation — DONE_VERIFIED as candidate-screening deliverable — 2026-11-17

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-EXPERT-SHORTLIST-REVALIDATION-001 | DONE_VERIFIED (candidate screen only) | PR #319 merged as `033e979c06c30aff5569750fae824f90484558ed`. Exact-head Quality [44081155872] and Chromium [44081155831] passed; duplicate Quality [44081116226] passed. Post-merge main Quality [44081323278] passed (422 Python tests + 70 subtests, expected corpus validator state, Node/web checks, Vite build); Chromium [44081323386] passed (13/13); Pages [44081323295] passed (production browser, deploy and deployed-site/runtime-asset smoke). Candidate evidence and role/conflict limits are recorded in the playbook and Issue #104. | This status means the public-source shortlist is documented. It does not mean outreach, consent, recruitment, independent-review appointment, IPA approval, annotator recruitment or gold acceptance. No one was contacted. |

Human acceptance gates remain open: IPA convention DRAFT_NOT_APPROVED; 30-item pilot BLOCKED; two annotators, separate adjudicator, non-annotating curator and private blind channel unconfirmed; adjudicated gold=0; empirical accuracy=null. Issue #104 remains OPEN. The Quality validator's `NOT_READY_NO_ADJUDICATED_GOLD` is the expected research state, not a test failure.


## Final session checkpoint — PR #320 and exact-main verification — 2026-11-17

| Work | Status | Evidence |
|---|---|---|
| KHM-EXPERT-SHORTLIST-REVALIDATION-001 | DONE_VERIFIED (candidate screen only) | PR #319 merged `033e979c06c30aff5569750fae824f90484558ed`; PR-head Quality [44081155872], Chromium [44081155831], exact-main Quality [44081323278], Chromium [44081323386] (13/13), Pages [44081323295] all SUCCESS. |
| PR #320 handoff/audit/register closeout | DONE_VERIFIED | PR-head Quality [44081681961] SUCCESS; exact-main Quality [44081774790] SUCCESS (422 Python + 70 subtests), Chromium [44081774743] SUCCESS (13/13), Pages [44081774768] SUCCESS (production browser, deployment and smoke). Final main `06d0fc1c38889ea6c02d78f7f3274c835f2744e2`. |

The corpus validator's `NOT_READY_NO_ADJUDICATED_GOLD` is the expected research state, not a software failure. Human gates remain open: IPA convention DRAFT_NOT_APPROVED, 30-item pilot BLOCKED, no recruited annotators/adjudicator/curator/private blind channel, gold=0, empirical accuracy=null. Issue #104 remains OPEN. No expert outreach or local tests are claimed.


## Khmer lexical word-segmentation evidence review — 2026-11-17

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-LEXICAL-WORD-SEGMENTATION-001 | BLOCKED | ALT/NOVA 20,000-sentence manual tokenization/POS corpus (Kaing et al. 2021, DOI 10.1145/3464378); khPOS 12,000-sentence manually segmented corpus; existing profile-neutral boundary evidence model in `src/khmer_ua/word_boundaries.py`. | Approve tokenization convention and intended use; review CC BY-NC-SA 4.0 / privacy / provenance restrictions; select rights-compatible and target-relevant data; independently double-annotate/adjudicate pilot; report held-out boundary P/R/F1 and abstention. |

Do not confuse word segmentation with orthographic-syllable segmentation or G2P. ALT/NOVA uses a documented morpheme-level surface convention: its v0.2 guide defines word tokens as units not further segmentable without loss of meaning, says they are morphemes in most cases, and treats compounds through separate component tokens plus shallow bracketing. This does not make NOVA boundaries equivalent to orthographic syllables or project phonetic units. ALT is translated from English Wikinews. The khPOS card reports economics/news/politics plus student/voter-list sources, requiring provenance/privacy review. Tran et al. (2017) constructs a syllable database rather than evaluating sentence-level word boundaries; Sung & Hwang (2016) report F1 0.906 without U+200B on their own test set but no reusable release was established. See [the evidence audit](KHMER-LEXICAL-SEGMENTATION-EVIDENCE-AUDIT-2026-11-17.md).

No corpus was copied or used for training. No lexical segmentation was implemented, no boundaries inferred for the user's paragraph, and no phonetic/IPA status changed. KHM-MIXED-SCRIPT-NUMERAL-BOUNDARIES-001 remains DONE_VERIFIED independently.


## PR #322 exact-main verification — 2026-11-17

| Work | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| PR #322 lexical-segmentation evidence audit | DONE_VERIFIED (documentation/evidence audit only) | Merged as `1cb22c9dfb5ebec539c01544d9e4270b20293b2d`. Exact-main Quality [44087269233] SUCCESS: 422 Python tests + 70 subtests, corpus validator, Node/web checks and Vite build; Chromium [44087269259] SUCCESS: 13/13 Playwright; Pages [44087269174] SUCCESS: production Chromium exercise, deployment and deployed-site/runtime smoke. | Audit deliverable and exact-main engineering verification only. It does not implement lexical segmentation or resolve the human linguistic gates. |

Current status remains: KHM-MIXED-SCRIPT-NUMERAL-BOUNDARIES-001 = DONE_VERIFIED; KHM-LEXICAL-WORD-SEGMENTATION-001 = BLOCKED; IPA convention DRAFT_NOT_APPROVED; linguistic ipa_kind UNRESOLVED; independent adjudicated gold = 0; empirical accuracy = null. Issue #104 remains OPEN. No local tests, human accessibility QA, expert outreach, annotation or gold creation are claimed.


## Sok & Adams visual rule-family audit — 2026-11-17

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-SOK-ADAMS-VISUAL-TABLE-AUDIT-001 | DONE_VERIFIED (source inspection only) | ACL Anthology PDF page images for printed pp. 419–422 visually inspected; Tables 4–6 and §§6.1–7 were classified by rule family and processing layer in the source dossier (../../ipa-gold/khmer-sok-adams-phonological-principles-audit.md). | Closes visual verification of the source's table/section layout only. No Khmer table cell values were transcribed into project data. |
| KHM-SOK-ADAMS-RULE-TRANSFER-001 | BLOCKED | Existing runtime resolves bounded orthographic register/shifter context and inherent-vowel series only; it does not implement the paper's cluster assimilation, minor-to-major syllable dependency, BANTOC IPA vowel changes or listed sound-change/rapid-speech rules. The source's historical profile, table notation and lack of independent gold prevent automatic transfer. | Qualified target-profile reviewer must approve each rule family; provide exact source/page locator, typed phonological-vs-phonetic layer, contemporary PPK evidence, positive/negative regression items and rights basis before implementation. |

The audit preserves the paper's §6 orthography-to-phonemic rules separately from §7 rapid/ordinary phonetic transitions. PCGN romanization shortening is not IPA evidence; final trill deletion is not interchangeable with onset /r/-loss. No runtime, test, corpus, IPA or Ukrainian mapping changed. Issue #104 remains OPEN; IPA convention remains DRAFT_NOT_APPROVED; adjudicated gold=0; empirical accuracy=null.


## PR #324 Sok & Adams rule-transfer audit — final verification — 2026-11-17

PR [#324](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/324) was squash-merged as `3f3352e94e993ab54a79c952bf6c1e7f9d187ae6` from branch `research/sok-adams-rule-transfer-audit-2026-11-17`, based on `460a3df4476f9f4beba7649909be101ef5331336`. Its exact-head Quality [44105695150] passed (422 Python tests + 70 subtests; corpus validator returned the expected `NOT_READY_NO_ADJUDICATED_GOLD`; web checks and production build passed), and Chromium [44105694990] passed (13/13 Playwright tests). The duplicate exact-head Quality run [44105669690] also passed. Post-merge mainline Quality [44105872935], Chromium [44105872929] (13/13), and Pages [44105872984] all passed. Pages deployed the exact main SHA and the deployed-site/runtime-asset smoke test passed.

The visual table audit is DONE_VERIFIED as source inspection only. `KHM-SOK-ADAMS-RULE-TRANSFER-001` remains BLOCKED pending qualified contemporary Phnom Penh careful-citation review and item-level positive/negative evidence. No phonological rule, IPA label, corpus row, Ukrainian mapping or generated artifact changed. Issue #104 remains OPEN; IPA convention remains `DRAFT_NOT_APPROVED`; adjudicated gold=0; empirical accuracy=null. No local tests or external expert outreach are claimed.

Final main: `3f3352e94e993ab54a79c952bf6c1e7f9d187ae6`. No open PRs remain at this checkpoint. Repository is engineering/build verified and research-ready as a partial prototype, not linguistically release-ready.


## PR #326 shared onset-fallback fixture — exact-main closeout — 2026-11-17

PR [#326](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/326) was squash-merged as `c345860483b378c66434139b7923a47094875c5a` from `test/khmer-onset-fallback-cross-runtime-fixture-2026-11-17`, based on `0d6e81a58ce514d49d93115c21925441b6acb579`. Exact-head Quality [44111499227] passed: **423 Python tests + 70 subtests**, Node/web checks and production build. Exact-head Chromium [44111513471] passed **14/14 Playwright tests**. The final code-bearing head also passed Quality [44111468114] and Chromium [44111467933] (14/14); the final documentation head Quality [44111513165] passed.

Post-merge mainline Quality [44111679547] passed (**423 Python tests + 70 subtests**, Node/web checks and build). Pages [44111679525] passed, including production browser exercise, deploy and deployed-site/runtime smoke. Main is `c345860483b378c66434139b7923a47094875c5a`; open PR count is 0.

The shared fallback fixture is an engineering regression only: Python checks API-level `null` canonical fields; browser checks rendered NOT_ESTABLISHED markers; both check the separate onset-only `k` → `к?` preview and rule/position provenance. Browser unit detail exposes `data-fallback-rule-id` and `data-fallback-position` for inspection. No new pronunciation rule, IPA label, Ukrainian canonical output, gold record or corpus data was added. The dedicated positional evidence registry remains TODO; broader vowel/subscript/coeng fallback remains blocked pending independently sourced positional rules. IPA convention remains `DRAFT_NOT_APPROVED`; independent adjudicated gold=0; empirical accuracy=null; Issue #104 OPEN. No local tests or human review are claimed.


## Khmer positional onset evidence registry — 2026-11-17

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-POSITIONAL-ONSET-EVIDENCE-001 | PARTIAL | Added `data/khmer-positional-onset-evidence.json`, its JSON Schema, and `tests/test_khmer_positional_onset_evidence.py`. The 33 existing consonant onset hints are recorded with Unicode identity, onset position, fallback rule ID, per-character Basic consonants row locator, and explicit review/profile status. | Closes the evidence-container and inventory-parity portion only. The sole cited source is a specialist descriptive reference, not a primary phonetic source; no entry is independently reviewed or adjudicated for the project Phnom Penh careful-citation profile. Primary phonetic evidence and qualified target-profile review remain required before promotion or positional expansion. |

The registry mirrors `data/khmer/consonants.json`; it is not consumed by runtime and adds no IPA, Ukrainian mapping, gold row, or pronunciation rule. All entries are restricted to `PROVISIONAL_ONSET_PREVIEW_ONLY`. Broader vowel/subscript/COENG fallback remains blocked. IPA convention remains `DRAFT_NOT_APPROVED`; independent adjudicated gold=0; empirical accuracy=null; Issue #104 OPEN.


## PR #329 exact-main verification — 2026-11-17

PR [#329](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/329) merged as `841bf283eecf13b2e2ccc7f83f02a8c7617c7cdc`. Exact-head Quality [44118873208] and Chromium [44118873039] passed; Quality reports **427 Python tests + 70 subtests**. Post-merge mainline Quality [44119105502], Chromium [44119105743], and Pages build/deploy/deployed-site smoke [44119105718] all passed on the exact final main SHA.

Acceptance is DONE_VERIFIED for the registry/schema/inventory-parity test artifact only. `KHM-POSITIONAL-ONSET-EVIDENCE-001` remains PARTIAL because its 33 entries cite a specialist descriptive source rather than primary phonetic evidence and are not independently reviewed or adjudicated for the project PPH profile. The registry is not runtime-consumed and grants only provisional onset-preview use. No canonical IPA/Ukrainian behavior or accuracy claim changes. Issue #104 remains OPEN; adjudicated gold=0; empirical accuracy=null.

## PR #331 skip-navigation closeout — 2026-11-17

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-UI-SKIP-NAV-001 | DONE_VERIFIED (automated keyboard navigation contract) | PR #331 merged as `f594b48615a799b13ae19ad4c2c6453512b8c24d`. Exact-head Quality [44143747834] passed (427 Python + 70 subtests); Chromium [44143747746] passed (16/16). Post-merge Quality [44144068435], Chromium [44144068416] (16/16), and Pages [44144068336] all passed on the exact main SHA. | Both public pages provide a first-focusable skip link, visible on focus and targeting the main landmark. This closes only the implemented keyboard skip-navigation behavior. |
| KHM-UI-001 | PARTIAL | Automated semantics/keyboard smoke plus skip navigation are covered by Playwright; PR #331 adds explicit skip-link tests. | Manual screen-reader/assistive-technology review, complete keyboard traversal, contrast, zoom/reflow and real mobile-device review remain outstanding. |

The skip-navigation task does not establish overall accessibility conformance. Issue #104 remains OPEN; IPA convention remains DRAFT_NOT_APPROVED; adjudicated gold=0; empirical accuracy=null.

## WCAG AA contrast regression — 2026-11-17

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-UI-CONTRAST-001 | DONE_VERIFIED (representative text styles only) | PR #333 merged as `126899c81810750cc1c8a77667340606c10eab20`. Exact-head Quality [44149776508] passed (427 Python + 70 subtests); Chromium [44149776607] passed (18/18). Post-merge Quality [44150006145] passed (427 + 70); Chromium [44150005996] passed (18/18). | Tests assert at least 4.5:1 contrast for selected text/background pairs on both public pages. Corrected eyebrow red, input hint text and methodology muted text. |
| KHM-UI-001 | PARTIAL | Skip navigation and representative contrast checks have automated Chromium coverage. | Full manual screen-reader/assistive-technology review, complete keyboard traversal, comprehensive text/non-text contrast, zoom/reflow and real mobile-device review remain outstanding. |

The contrast task is bounded to the tested selectors and states; it does not claim full WCAG conformance. Pages [44150006152] SUCCESS: production build, browser exercise, exact-main deployment and deployed-site asset smoke checks passed.


## PR #334 exact-main verification — 2026-11-17

| Work | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| PR #334 documentation closeout and final mainline verification | DONE_VERIFIED (documentation/evidence synchronization only) | PR #334 merged as `a51135d2c65791ae2b433070b71c482a9f49aa40`. Exact PR-head Quality [44150526026] and Chromium [44150526069] passed on `05aecb1f136c160e03ba8b8ea7dcabee70c58611`; Chromium: 18/18. Post-merge Quality [44150735242] passed (427 Python tests + 70 subtests, expected `NOT_READY_NO_ADJUDICATED_GOLD`, 24 Node/web tests and Vite build); Chromium [44150735206] passed (18/18); Pages [44150735166] deployed the exact main SHA and passed deployed-site asset smoke checks. | Confirms exact-main engineering/deployment state and records PR #334's closeout. Does not complete general accessibility QA or any linguistic release gate. |

`KHM-UI-CONTRAST-001` remains DONE_VERIFIED for the representative tested text/background pairs only. `KHM-UI-001` remains PARTIAL pending manual screen-reader/assistive-technology review, full keyboard traversal, comprehensive non-text/text contrast, zoom/reflow and real-device review. Issue #104 remains OPEN; IPA convention `DRAFT_NOT_APPROVED`; independent adjudicated gold=0; empirical accuracy=null. No local tests, human annotation, expert recruitment or external review are claimed.


## PR #336 — NOVA tokenization scope correction and exact-main verification — 2026-11-17

| Work item | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| Correct ALT/NOVA tokenization description against NICT guideline v0.2 | DONE_VERIFIED (source audit correction) | PR #336 merged as `c4cd8b1a17463f306b7c6dffbaad0f80685e5aa1`; the guideline §3 describes word tokens as generally morphemes and §5 documents component-token/bracketing treatment of compounds. | Documentation only; does not make NOVA token boundaries a universal lexical, orthographic-syllable or phonetic standard. |
| PR #336 exact-head and post-merge engineering checks | DONE_VERIFIED | PR-head Quality [44170618296] and Chromium [44170618297] SUCCESS; post-merge main Quality [44170796321], Chromium [44170796376], Pages [44170796347] SUCCESS. Quality: 427 Python tests + 70 subtests; Chromium: 18/18. Pages deployed exact main SHA and passed HTML/JS/CSS smoke checks. | No runtime, corpus, IPA or gold data changed. Gold remains 0; empirical accuracy remains null; Issue #104 remains OPEN. |

Local clone/test execution was not possible because `github.com` DNS resolution failed in the execution environment; CI evidence above is the verification source.


## Live branch inventory refresh — 2026-11-17

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-BRANCH-AUDIT-001 | PARTIAL (live inventory refreshed; full content audit outstanding) | GitHub branch listing pages 1–3: 209 refs total (main + 208 non-main), 208 unique tip SHAs total; one non-main ref points to the exact main SHA, leaving 207 distinct non-main tips. Open PRs=0; open issues=1 (#104). | The former 131-ref / 130-comparison snapshot is historical. This refresh did not compare every current branch's ancestry or reconcile every changed file/PR. Continue full content-level review; preserve branches and do not merge divergent snapshots wholesale. |

Focused spot-checks: `data/khmer-onset-evidence-registry-2026-11-17` is already integrated through PR #329; PCGN independent-vowel CSV and test are byte-identical to main; the direct BGN/PCGN feature branch is stale/diverged and was not ported wholesale. No branch was deleted or force-updated. The one no-diff branch at main's SHA was preserved.

## Selected historical branch content reconciliation — 2026-11-17

| Work | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| Live branch inventory | DONE_VERIFIED (inventory only) | 209 refs; 208 unique tip SHAs; one non-main ref points to main's SHA; 0 open PRs; 1 open issue (#104). | Does not complete changed-file/commit/PR-ancestry review. |
| Selected historical branch content triage | PARTIAL | Compared parser/parse-forest, direct BGN/PCGN, practical-adapter, romanization-matrix, PCGN registry and onset-registry branches against main. Parser branches are older snapshots missing current diagnostics/coverage; practical.py/policy and PCGN independent-vowel CSV/test are identical to main; onset registry already integrated by PR #329. | 11 representative branches triaged; remaining historical refs still require full content/PR-ancestry reconciliation. No branches deleted or merged wholesale. |
| PR #338 exact-main inventory documentation | DONE_VERIFIED | PR-head Quality [44173194420] and [44173216454] SUCCESS (427 Python tests + 70 subtests; expected no-gold state); Chromium [44173216381] SUCCESS (18/18). Post-merge Quality [44173400187], Chromium [44173400043], Pages [44173400219] SUCCESS. | Documentation-only; no runtime, source data or IPA behavior changed. |

`KHM-BRANCH-AUDIT-001` remains PARTIAL. The 209-ref count is the current inventory; the 130/130 comparison result in older entries is a historical snapshot, not a current full ancestry pass.
## Final branch inventory and PR #339 closeout — 2026-11-17

| Work | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| Final live branch inventory | DONE_VERIFIED (inventory only) | 212 refs total (main + 211 non-main); 212 unique tip SHAs; 0 open PRs; 1 open issue (#104). | Timestamped after creation of the final clean closeout branch; does not imply full content audit. |
| PR #339 selected historical branch content closeout | DONE_VERIFIED (selected 11-branch sample only) | Exact-head Quality [44173798008], [44173819190] SUCCESS; Chromium [44173818953] SUCCESS (18/18). Post-merge Quality [44173970460], Chromium [44173970246] (18/18), Pages [44173970271] SUCCESS on `b5a878f33dae74d34754c547580c5a494307cdce`. | Branch audit remains PARTIAL; 211 non-main refs are not all content/PR-ancestry reconciled. |
| PR #340 disposition | DONE_VERIFIED (superseded, unmerged) | GitHub reported a squash-merge conflict after PR #339; PR #340 closed unmerged, branch preserved. | Its final note is re-applied from a clean main-based branch. |

`KHM-BRANCH-AUDIT-001` remains PARTIAL. Historical branches were preserved; no wholesale merge, force-update or deletion was performed.

## Continued historical branch content reconciliation — 2026-11-17

A second focused pass compared four additional non-main branches with exact main `1f5792d6047fa8172b2e19acfa5984f744fcf753`. This extends the representative sample from 11 to 15 branches; it does not claim a complete audit of all historical refs.

| Branch | Compare to main | Content evidence and disposition |
|---|---:|---|
| `feat/khmer-ambiguous-parse-forest-2026-11-16` | 3 ahead / 52 behind | Its orthographic parser and schema are an earlier snapshot. Main has the packed parse-forest contract, per-syllable grammar alternatives, derivation/segmentation counts and rejected-span diagnostics. No wholesale port. |
| `feat/khmer-orthographic-component-scanner-2026-11-16` | 20 ahead / 59 behind | Its `src/khmer_ua/orthographic_structure.py` blob SHA is exactly identical to main (`fc545b15d109d1829bf4d264b6576270023cc1fe`). Scanner implementation is already integrated; remaining branch divergence is not a reason to merge the branch. |
| `feat/khmer-external-g2p-harness-2026-10-24` | 3 ahead / 504 behind | Main already contains `scripts/benchmark_g2p.py` and its test, but the current main versions are evolved: report provenance binds harness/corpus/runtime/GitHub metadata; report integrity sidecar and bounded source-IPA notation diagnostics are included; no independent gold or accuracy is fabricated. The older branch harness/test are superseded. |
| `feat/khmer-ukrainian-practical-adapter-final-2026-11-11` | 60 ahead / 215 behind | `src/khmer_ua/practical.py` and `data/ukrainian/practical-policy.json` blob SHAs exactly match main (`6476c3c17267adfc2215de5ffc6fe21d0cea588d` and `2388d93b8ec1f2c5b3b2cfc806acdb67197d8a3c`). Its implementation/policy is already integrated; no port. |

No runtime, phonological, IPA, corpus or Ukrainian mapping changes were made in this audit. All reviewed historical branches remain preserved. `KHM-BRANCH-AUDIT-001` remains PARTIAL: 15 representative branches now have focused dispositions, while the other historical refs still require changed-file/commit/PR-ancestry reconciliation.


## Typed-IPA, coverage and boundary-evidence branch reconciliation — 2026-11-17

A third focused pass compared five additional feature branches with exact main `6b458be57c5a21e178c643352eb9958c240d23c1`. The representative content-review sample is now 20 branches. These comparisons do not constitute a full review of every historical ref.

| Branch | Compare to main | Content evidence and disposition |
|---|---:|---|
| `feat/evidence-gated-coverage-audit-2026-10-21` | 17 ahead / 510 behind | Main has the evolved `scripts/coverage.py` implementation: its deterministic check/write path covers both internal and public coverage reports, while the branch version checks/writes only the internal report. No wholesale port. |
| `feat/ipa-renderer-font-fallback-2026-10-24` | 2 ahead / 506 behind | Its stylesheet is an older compact CSS snapshot. Main has the later tokenized stylesheet and subsequent focus/contrast palette changes; no safe isolated renderer fallback change was demonstrated by the branch-level diff. No port. |
| `feat/profile-neutral-khmer-boundary-evidence-2026-11-16` | 9 ahead / 68 behind | `src/khmer_ua/word_boundaries.py` is byte-identical to main (blob SHA `750cfa6fe561a4a92a67be70e35f842e26bb4f3f`). Boundary evidence container/schema/tests are already integrated; it still does not perform lexical segmentation. |
| `feat/typed-ipa-candidate-validation-2026-11-15` | 12 ahead / 187 behind | `src/khmer_ua/ipa.py` is byte-identical to main (blob SHA `000f521f56de5bacc73ffddecc4a2f7cbbec3667`). Typed candidate validation is already integrated; it does not infer or promote pronunciation. |
| `feat/typed-ipa-hybrid-bridge-2026-11-15` | 10 ahead / 181 behind | `src/khmer_ua/hybrid.py` is byte-identical to main (blob SHA `3adb1adda7f9bbb95ec43c5db850dd2626a3a925`). The external-candidate bridge is already integrated as a diagnostic-only adapter behind typed IPA validation. |

No code, runtime, IPA, pronunciation, corpus or Ukrainian mapping was changed in this audit. All historical refs remain preserved. `KHM-BRANCH-AUDIT-001` remains PARTIAL: 20 representative branches have focused dispositions, but the other historical refs still need complete changed-file/commit/PR-ancestry reconciliation. The profile-neutral boundary evidence module is not a lexical word segmenter; the typed IPA and hybrid modules do not establish adjudicated gold or empirical accuracy.


## BGN/PCGN implementation-branch reconciliation — 2026-11-17

A fourth focused pass compared five BGN/PCGN-related feature branches with exact main `59bdf452f15f440918e83a7c6aa4ac94f95f075f`. The representative branch content-review sample is now 25. These are implementation-history dispositions, not independent linguistic validation of the BGN/PCGN rules.

| Branch | Compare to main | Content evidence and disposition |
|---|---:|---|
| `feat/pcgn-typed-orthographic-analysis-2026-11-15` | 17 ahead / 154 behind | The branch's initial `pcgn.py` module (7,915 bytes) and schema are earlier snapshots; main has the substantially expanded typed orthographic analysis implementation (120,449 bytes), updated schema and broader tests. No wholesale port. |
| `feat/pcgn-note10-letter-inventory-20261115` | 18 ahead / 122 behind | `src/khmer_ua/pcgn_unicode.py` is byte-identical to main (blob SHA `2a1960dc5d54fab122e3f8d3a79d0094e01610b0`). The branch's PCGN notes CSV is an earlier version than main's updated 7,233-byte inventory; no data overwrite. |
| `feat/pcgn-note2-cluster-shifters-2026-11-15` | 10 ahead / 143 behind | Its series-resolution test is an earlier version (6,274 bytes vs 7,401 on main); the shared `pcgn.py` module is substantially evolved on main. No isolated missing rule was established from the branch-level diff; no port. |
| `feat/pcgn-series-resolution-note3-2026-11-15` | 16 ahead / 152 behind | Its orthographic-analysis test is an earlier version (6,105 bytes vs 6,273 on main); the current main module/schema/tests have moved beyond this snapshot. No wholesale port. |
| `feat/pcgn-explicit-open-syllable-assembly-2026-11-16` | 8 ahead / 104 behind | Its open-syllable assembly schema is byte-identical to main (blob SHA `1ae644fb612f45f1f38051480e3fdada6a910a0a`). Its `pcgn.py` (71,015 bytes) is an earlier snapshot than main's 120,449-byte module. No port. |

No PCGN rule, source evidence, IPA, pronunciation, corpus, Ukrainian mapping or runtime behavior was changed. The audit does not resolve any outstanding source interpretation or establish BGN/PCGN compliance. All historical refs remain preserved. `KHM-BRANCH-AUDIT-001` remains PARTIAL: 25 representative branches have focused dispositions, not a complete changed-file/commit/PR-ancestry audit of all historical refs.


## BGN/PCGN vowel and syllable-assembly branch reconciliation — 2026-11-17

A fifth focused pass compared ten additional BGN/PCGN feature branches with exact main `c01879e9326f96be24160e64bfd99fe78d4c2767`. The representative content-review sample is now 35 branches. These are code/schema integration findings only, not expert confirmation of the source's phonological rules.

| Branch | Compare to main | Content evidence and disposition |
|---|---:|---|
| `feat/pcgn-ba-triisap-exception-20261115` | 11 ahead / 125 behind | Its `pcgn.py` is an earlier 44,833-byte snapshot; main has the later 120,449-byte implementation. The PCGN-note and series-decision changes are not justification to replace the newer module wholesale. |
| `feat/pcgn-compound-vowel-subset-2026-11-15` | 10 ahead / 140 behind | Its dependent-vowel decision schema is byte-identical to main (blob SHA `d867242351b7d488202e38390acc7ac381b13fae`). The schema is already integrated. |
| `feat/pcgn-dependent-vowel-subset-2026-11-15` | 9 ahead / 142 behind | Its dependent-vowel resolution test is an earlier version (3,398 bytes vs 4,041 on main); current main retains the evolved test/module. No port. |
| `feat/pcgn-independent-vowel-subset-2026-11-15` | 8 ahead / 138 behind | Main's independent-vowel decision schema is evolved (3,634 bytes vs 1,591 on the branch); no older schema overwrite. |
| `feat/pcgn-inherent-vowel-component-2026-11-15` | 18 ahead / 118 behind | Its `romanization_pcgn_inherent_vowel.csv` is byte-identical to main (blob SHA `90404b215dbc9e736e050d77b4439514c13d8f0e`). Data already integrated. |
| `feat/pcgn-final-consonant-component-2026-11-15` | 14 ahead / 114 behind | Its final-consonant decision schema is byte-identical to main (blob SHA `1b5b4fe93d6289225f9d4c31d10a97b16cd65e6f`). Main's shared PCGN implementation and tests are later. |
| `feat/pcgn-glottal-open-syllable-assembly-2026-11-16` | 9 ahead / 86 behind | Its glottal open-syllable assembly schema is byte-identical to main (blob SHA `f402418fa8dea5b3396c06c6f762574755af5f9b`). Already integrated. |
| `feat/pcgn-independent-vowel-closed-syllable-assembly-2026-11-16` | 11 ahead / 78 behind | Its independent-vowel closed-syllable schema is byte-identical to main (blob SHA `900471e3872ef72adc5ffcc9ad203f727020a326`). Already integrated. |
| `feat/pcgn-shortened-closed-syllable-assembly-2026-11-16` | 8 ahead / 99 behind | Its closed-syllable assembly schema is byte-identical to main (blob SHA `33e4619cf9f7ca4a9822a04b2afac8037e8e04a3`). Already integrated. |
| `feat/pcgn-normal-dependent-closed-syllable-assembly-2026-11-16` | 7 ahead / 98 behind | Its dependent closed-syllable assembly schema is byte-identical to main (blob SHA `e97b27627c71951cc81154f94c083138608c3dcc`). Already integrated. |

No PCGN rule, source evidence, IPA, pronunciation, corpus, Ukrainian mapping or runtime behavior was changed. All branches remain preserved. This audit does not claim BGN/PCGN compliance or independent linguistic adjudication. `KHM-BRANCH-AUDIT-001` remains PARTIAL: 35 representative branches now have focused dispositions; full reconciliation of the remaining historical refs is still outstanding.


## BGN/PCGN rule-note branch reconciliation — 2026-11-17

A sixth focused pass compared five rule-note branches with main at `c01879e9326f96be24160e64bfd99fe78d4c2767`. These branches add source-specific PCGN note decisions; the following verifies repository integration only, not independent correctness of the interpretation.

| Branch | Compare to main | Content evidence and disposition |
|---|---:|---|
| `feat/pcgn-note4-glottal-onset-20261115` | 12 ahead / 128 behind | Its glottal-onset decision schema is byte-identical to main (SHA `ed2b915ef85de8006bcb6497a59e9e07d2d03a6f`); main's shared PCGN module and tests are later. |
| `feat/pcgn-note5-shortening-context-20261115` | 13 ahead / 136 behind | Its shortened-vowel decision schema is byte-identical to main (SHA `9fa5887eff4fefc63efdbc5d040ba0f1299f1c7e`); no older module/test overwrite. |
| `feat/pcgn-note6-robat-component-20261115` | 17 ahead / 134 behind | Its Robat decision schema is byte-identical to main (SHA `be85d67cff8dd2ce79261b08224b45fc3307d078`); implementation is already in the later main PCGN module. |
| `feat/pcgn-note7-ahsda-context-20261115` | 10 ahead / 132 behind | Its Ahsda decision schema is byte-identical to main (SHA `bfcf5d7cd053578a1f9a9bac5d9ca80ea73815c5`); no port. |
| `feat/pcgn-note8-toandakhiat-20261115` | 10 ahead / 130 behind | Its Toandakhiat decision schema is byte-identical to main (SHA `69ac7b0f25d5e1dc7a9c1f0271f4360b78b5a67a`); no port. |

## BGN/PCGN alternatives and special syllable-assembly branch reconciliation — 2026-11-17

A seventh focused pass compared five additional branches with main at `c01879e9326f96be24160e64bfd99fe78d4c2767`.

| Branch | Compare to main | Content evidence and disposition |
|---|---:|---|
| `feat/pcgn-note9-alternatives-20261115` | 9 ahead / 122 behind | Its independent-vowel decision schema is byte-identical to main (SHA `ce7397d501bbe535f5748f242916f29c9cecae7f`); the shared module/test and notes inventory on main are later. |
| `feat/pcgn-anusvara-visarga-table-2026-11-15` | 10 ahead / 120 behind | Its anusvara/visarga decision schema is byte-identical to main (SHA `92d9c5594059d0925b0b7cbef83195821f5951b6`); the source table and implementation are already present on main. |
| `feat/pcgn-anusvara-visarga-syllable-assembly-2026-11-16` | 3 ahead / 79 behind | Its `pcgn.py` is an earlier 119,002-byte snapshot than main's 120,449-byte implementation. No missing change justified replacing or merging the module. |
| `feat/pcgn-alif-dependent-closed-syllable-assembly-2026-11-16` | 8 ahead / 85 behind | Its glottal-dependent closed-syllable schema is byte-identical to main (SHA `bce2295940726075a2e7a8c97d13224ca8979865`). Already integrated. |
| `feat/pcgn-alif-shortened-closed-syllable-assembly-2026-11-16` | 9 ahead / 83 behind | Its glottal-shortened closed-syllable schema is byte-identical to main (SHA `b96adf6a9eca3e6d638a5fcca11a4e32329da8f2`). Already integrated. |

No PCGN rule, source evidence, IPA, pronunciation, corpus, Ukrainian mapping or runtime behavior changed. All historical refs remain preserved. These checks do not establish BGN/PCGN compliance or independent linguistic adjudication. `KHM-BRANCH-AUDIT-001` remains PARTIAL: 45 representative branches have focused dispositions; all remaining historical refs still require reconciliation.


## Completion of the `feat/*` branch-family reconciliation — 2026-11-17

The focused comparison pass now covers all **49 branches** returned by the repository's `feat/*` branch search. This is a family-specific completion checkpoint; it does not complete the repository-wide historical branch audit.

Five final feature branches were dispositioned against main `af28e35f5522dd64ceb78289b02d279a74fa9a2f`:

| Branch | Compare to main | Content evidence and disposition |
|---|---:|---|
| `feat/github-pages-hybrid-candidate-shell-2026-11-15` | 5 ahead / 115 behind | Contains a unique 8,305-byte browser-side `src/hybrid-engine.js` absent from main. Its old `src/main.js` imports that module, but the branch does not contain a dedicated test for it and its UI entrypoint is substantially behind current main. Main already has the Python typed-IPA hybrid diagnostic adapter. Preserve this as a candidate; do not port without a current-entrypoint browser contract proving that provider output remains diagnostic-only and cannot replace deterministic published output. |
| `feat/pcgn-consonant-components-2026-11-15` | 17 ahead / 118 behind | Its consonant-decision schema is byte-identical to main (SHA `d5ca11b4f16e006fd84ef3f2f4c921531b016890`); main's shared PCGN implementation is later. Already integrated; no port. |
| `feat/pcgn-note2-shifter-resolution-2026-11-15` | 16 ahead / 154 behind | Its orthographic-analysis and series-decision schemas and series-resolution tests are earlier than main (2,788 vs 2,913 bytes; 1,345 vs 1,402 bytes; 4,787 vs 7,401 bytes). Main has the evolved shared implementation and regression coverage. No port. |
| `feat/pcgn-robat-closed-syllable-assembly-2026-11-16` | 11 ahead / 82 behind | Its Robat closed-syllable assembly schema is byte-identical to main (SHA `e87cafb871849dccadfa181668dfb537d41f7e3e`). Already integrated; no port. |
| `feat/romanization-to-ukrainian-runtime-2026-11-12` | 12 ahead / 211 behind | Its `src/ukrainian-practical.js` is byte-identical to main (SHA `7d6ac30ca63ac240ef9aa74b7f9f303ec77e67c6`). Its old romanization renderer and tests are superseded by main's expanded diacritic-aware BGN/PCGN renderer, numeral handling, mixed-script guards and matrix-backed tests. No port. |

**Disposition:** all 49 `feat/*` branches have now been compared and assigned a content disposition. The browser-side hybrid candidate is the one explicitly retained for possible future engineering review; all other inspected changes are integrated, superseded or not suitable for wholesale porting. No historical branch was deleted or force-updated.

## Data-branch family reconciliation — 2026-11-17

The four `data/*` refs were checked. The onset-registry integration branch points to the exact main tree; the onset evidence registry itself was already integrated by PR #329; the original PCGN independent-vowel source-register CSV/test are identical to main. The remaining `data/pcgn-independent-vowel-source-register-mainline-2026-11-16` branch is 6 ahead / 112 behind, and its `data/khmer/romanization_pcgn_independent_vowels.csv` is byte-identical to main (blob SHA `ff90ff957367595fefe245a7caa7a7e94a768504`). No data port is required. These evidence containers do not independently approve phonological interpretations.

## Test-branch family reconciliation — 2026-11-17

All ten `test/*` refs were compared with main. Their test-only changes are either byte-identical to main or earlier snapshots of tests now expanded on main; no regression fixture or acceptance assertion was found that justified a port.

| Branch | Compare to main | Content evidence and disposition |
|---|---:|---|
| `test/complete-grapheme-accounting-2026-11-12` | 3 ahead / 218 behind | Its parser test is an older 2,450-byte snapshot; main's parser tests are 7,491 bytes and cover later structure/diagnostic behavior. No port. |
| `test/ipa-display-contract-2026-10-24` | 1 ahead / 509 behind | `tests/test_ipa_display_contract.py` is byte-identical to main (SHA `005d4da8cd84d20bd17ddab1b3b9eeb84a2e590a`). Already integrated. |
| `test/khmer-numeral-crosswalk-runtime-2026-11-12` | 6 ahead / 201 behind | Its romanization adapter test is an older subset; main's 13,109-byte test file includes the numeral crosswalk and later mixed-message/matrix regressions. No port. |
| `test/khmer-onset-fallback-cross-runtime-fixture-2026-11-17` | 16 ahead / 19 behind | The fixture JSON and Python rule-engine test are byte-identical to main (SHAs `40b6bfc516523ae03f9b40b2dfdb48c40706f272` and `5ab81fea14e79d85ec0852b4ba67ca164cf24192`). The browser test file is an earlier snapshot than main's expanded 11,016-byte suite. |
| `test/khmer-romanization-adapter-coverage-2026-11-12` | 2 ahead / 209 behind | Its romanization test is an earlier 2,689-byte subset of main's 13,109-byte test suite. No port. |
| `test/khmer-romanization-canonical-matrix-parity-2026-11-12` | 4 ahead / 205 behind | Its test is an earlier 4,582-byte subset; main includes the expanded canonical matrix and cross-runtime assertions. No port. |
| `test/khmer-romanization-whole-message-adapter-2026-11-12` | 4 ahead / 203 behind | Its test is an earlier 5,508-byte subset; main includes the later mixed-message, numeral and preservation coverage. No port. |
| `test/khmer-vowel-ascii-alias-coverage-2026-11-12` | 2 ahead / 199 behind | Its test is an earlier 6,648-byte subset; main's suite is expanded to 13,109 bytes. No port. |
| `test/khmer-vowel-matrix-runtime-crosswalk-2026-11-12` | 1 ahead / 198 behind | Its test is an earlier 8,210-byte subset; main's suite is expanded to 13,109 bytes. No port. |
| `test/ui-accessibility-smoke-2026-11-15` | 2 ahead / 173 behind | Its browser test is an older 5,639-byte snapshot; main's current browser suite is 11,016 bytes and includes later skip-navigation/contrast and keyboard behavior. No port. |

**Branch-family checkpoint:** all 49 `feat/*`, all 4 `data/*`, and all 10 `test/*` refs have focused comparisons/dispositions. The repository-wide `KHM-BRANCH-AUDIT-001` remains PARTIAL because other branch families (including research, documentation and earlier maintenance/audit refs) have not all undergone equivalent content/PR-ancestry reconciliation. All branches are preserved.


## Research-branch family reconciliation — 2026-11-17

A focused content-level pass compared all 28 `research/*` refs with main `af28e35f5522dd64ceb78289b02d279a74fa9a2f`. The findings below distinguish source/data integration from research conclusions. No research branch was merged wholesale.

| Branch | Compare to main | Content disposition |
|---|---:|---|
| `research/bgn-pcgn-ungegn-rule-diff-2026-11-15` | 5 ahead / 162 behind | Its rule-difference audit document is byte-identical to main (15,012 bytes). No port. |
| `research/complete-external-g2p-registry-2026-11-15` | 6 ahead / 183 behind | Main's external-renderer registry contains the same 15 candidate IDs and later status metadata. No unique candidate or registry row to port. |
| `research/expert-shortlist-revalidation-2026-11-17` | 5 ahead / 27 behind | Its IPA-gold collection playbook is byte-identical to main (42,914 bytes). Shortlist revalidation is already represented. |
| `research/external-ipa-renderers-2026-10-24` | 7 ahead / 512 behind | Its initial 10-entry registry/schema/test work is superseded by main's 15-entry registry and current schema/test files. |
| `research/google-khmer-lexicon-full-audit-2026-11-16` | 21 ahead / 50 behind | Its 46-record source registry is a strict subset of main's 49 records; no source ID is unique to the branch. The main playbook is the later full audit. |
| `research/khmer-acoustic-model-release-audit-2026-11-16` | 26 ahead / 49 behind | Its 46 source records are a strict subset of main's 49; the playbook on main is longer and contains the later artifact/rights audit. No model output is promoted to gold. |
| `research/khmer-engine-benchmark-expansion-2026-11-11` | 72 ahead / 231 behind | Its 15-candidate registry is superseded by main's 15-entry renamed/updated registry; the old combined workflow is superseded by current separate optional G2P/Goruut and pinned MekongPhon workflows. |
| `research/khmer-hybrid-benchmarks-reconciled-2026-11-11` | 34 ahead / 220 behind | Its registry, benchmark and research-doc snapshots are superseded by main's current diagnostic harnesses, tests and evidence-limited reports. No wholesale port. |
| `research/khmer-hybrid-engine-2026-11-11` | 91 ahead / 231 behind | Main contains the current hybrid-engine research documentation and typed-IPA diagnostic bridge; this branch is an older integration snapshot. No port. |
| `research/khmer-ipa-convention-draft-2026-11-17` | 5 ahead / 49 behind | Its draft differs from the current draft only in earlier Kirby cluster-transition wording/citation. The v2 draft is the exact main file; status remains `DRAFT_NOT_APPROVED`. |
| `research/khmer-ipa-convention-draft-v2-2026-11-17` | 7 ahead / 48 behind | Its 14,517-byte IPA convention draft is byte-identical to main. This is still a research proposal, not an approved annotation authority. |
| `research/khmer-kirby-cluster-audio-audit-2026-11-17` | 9 ahead / 42 behind | The 6,187-byte cluster-audio source audit is byte-identical to main; the source registry on main contains the additional Sok-Adams entry. |
| `research/khmer-kirby-tonogenesis-audio-audit-2026-11-17` | 26 ahead / 37 behind | The 9,422-byte tonogenesis dataset audit is byte-identical to main. It remains supporting phonetic evidence, not gold. |
| `research/khmer-lexical-segmentation-evidence-2026-11-17` | 4 ahead / 24 behind | Its lexical-segmentation audit is an earlier 8,094-byte version; main has the expanded 8,641-byte audit and corrected NOVA tokenization scope. No port. |
| `research/khmer-lexical-segmentation-evidence-mainline-2026-11-17` | 2 ahead / 10 behind | Compare reports no changed files against main; no separate content to port. |
| `research/khmer-phonotactic-scope-2026-11-15` | 9 ahead / 181 behind | Its source registry (41 records) is a strict subset of main's 49; main's phonology and source docs are later. No phonological rule is promoted from this branch. |
| `research/khmer-source-audit-integration-2026-11-17` | 7 ahead / 44 behind | Its 47 source records are a strict subset of main's 49; main's IPA corpus/playbook documents are expanded. No missing source ID. |
| `research/khmer-unicode-syllable-grammar-2026-11-16` | 1 ahead / 59 behind | Its grammar audit predates the implemented Unicode 18 packed parser and later mainline verification. TN #61 v2 remains a separate non-normative profile TODO. |
| `research/loc-khmer-word-division-2026-11-16` | 6 ahead / 78 behind | Its LOC word-division audit is an earlier 6,223-byte version; main has a 13,989-byte expanded evidence audit. Lexical segmentation remains blocked pending convention, licensed evidence and adjudication. |
| `research/mekongphon-diagnostic-harness-2026-11-15` | 11 ahead / 189 behind | `scripts/benchmark_mekongphon_model.py` (11,923 bytes), its tests (4,069 bytes) and optional workflow are byte-identical to main. No port. |
| `research/mekongphon-release-rights-audit-2026-11-16` | 10 ahead / 49 behind | Its playbook is an earlier 32,951-byte snapshot; main's 42,914-byte playbook incorporates the detailed pinned-repository and upstream-data-rights audit. Rights for the source lexicon remain unresolved. |
| `research/mekongphon-seed-lexicon-audit-2026-11-16` | 34 ahead / 50 behind | Its playbook is an earlier 32,890-byte snapshot; main includes the expanded 8,040-row reconciliation, train/eval split, pipeline reproducibility and rights caveats. No seed labels are accepted as project gold. |
| `research/pcgn-note-registry-2026-11-15` | 6 ahead / 160 behind | The PCGN note registry and tests are integrated in later mainline CSV/schema/test state. No port. |
| `research/phon-sobon-and-lexicon-triage-2026-11-15` | 11 ahead / 184 behind | Its external corpus triage audit is byte-identical to main; its 35-record source registry is a strict subset of main's 49. |
| `research/phonetic-literature-fulltext-review-2026-11-17` | 6 ahead / 31 behind | Its 7,598-byte Chem/Mam full-text review is byte-identical to main. The evidence limitations remain explicit. |
| `research/sok-adams-khmer-phonology-audit-2026-11-17` | 7 ahead / 34 behind | Its 8,033-byte phonological-principles audit is an earlier snapshot; main has the expanded 13,073-byte review. Rule transfer remains a separate TODO. |
| `research/sok-adams-rule-transfer-audit-2026-11-17` | 5 ahead / 22 behind | Its rule-transfer closeout is an earlier documentation snapshot; no code or evidence absent from the current main audit was identified. |
| `research/ungegn-engine-candidate-review-2026-11-15` | 5 ahead / 163 behind | Its matrix/documentation snapshot is superseded by the current romanization matrix and source audit; no engine or linguistic rule was ported. |

### Research-family evidence boundary

Across the eight inspected `data/khmer/sources.json` research snapshots, every branch source ID is present in main; the branch snapshots contain 35–48 records versus 49 on main. The main registry therefore supersedes these branch versions without dropping a source ID. The external renderer registry likewise retains the 15 candidate concepts from the research branches, with current IDs/statuses.

**Disposition:** all 28 `research/*` refs have focused compare/content dispositions. Their research findings are integrated, superseded by more complete mainline audits, or remain explicitly evidence-limited. No IPA gold, licensed dataset, model accuracy or phonological rule was fabricated or promoted. All research branches remain preserved.


## Fix and release branch-family reconciliation — 2026-11-17

Compared all 14 `fix/*` refs and the single `release/*` ref with main `8a84d6550176975f7c3b07bded513993f821f909`. No branch was merged wholesale.

| Branch | Compare to main | Content evidence and disposition |
|---|---:|---|
| `fix/explicit-ipa-kind-in-phonetic-result-2026-11-17` | 9 ahead / 34 behind | `src/khmer_ua/phonetic_result.py` is byte-identical to main (SHA `1700552ae13b95f992fbad613d5da31e9fd18d42`); the schema and rule engine are later on main. Explicit typed IPA kind is integrated; no port. |
| `fix/flag-unconverted-khmer-romanizer-output-2026-11-15` | 2 ahead / 171 behind | `src/khmer-romanization-ukrainian.js` is byte-identical to main (SHA `e2106a8d5ad952fa31bbc3ade6d3706036422155`). Output guarding is integrated. |
| `fix/khmer-benchmark-reproducibility-2026-10-24` | 3 ahead / 508 behind | Its 5,842-byte benchmark script is superseded by main's 10,704-byte provenance/integrity-aware harness. No port. |
| `fix/khmer-orthographic-parser-diagnostics-v2-2026-11-16` | 17 ahead / 57 behind | Its Python parser, browser parser, schema and tests are earlier snapshots than main's expanded parser/rejected-span contract. No port. |
| `fix/khmer-orthographic-parser-evidence-2026-11-16` | 7 ahead / 58 behind | Its 3,869-byte schema is superseded by main's 6,054-byte schema; parser/test implementations are also older. No port. |
| `fix/khmer-orthographic-parser-rejection-spans-2026-11-16` | 16 ahead / 56 behind | Its parser, browser adapter, schema, provenance registry and tests are earlier than the current main implementation; no unique accepted behavior is missing. |
| `fix/khmer-rejected-span-reasons-and-fixtures-2026-11-16` | 2 ahead / 55 behind | Its focused parser/browser/test changes are incorporated in the later main rejected-span contract. No port. |
| `fix/khmer-typed-partial-phonetic-results-2026-11-16` | 56 ahead / 77 behind | Its typed result module is an earlier 1,607-byte snapshot; main has the expanded 1,797-byte result contract and later rule-engine/schema/tests. No port. |
| `fix/khmer-unmodeled-letter-trace-2026-11-12` | 3 ahead / 218 behind | Its parser (7,014 bytes) is an earlier snapshot than main's 10,689-byte parser and later trace tests. No port. |
| `fix/mixed-script-numeral-token-boundaries-2026-11-17` | 32 ahead / 30 behind | `src/khmer_ua/parser.py` is byte-identical to main (SHA `e63d90894da39ca23eab6d41125886d9700d898d`). Current Python/browser tests and schema are integrated; no port. |
| `fix/mixed-script-romanization-guard-2026-11-15` | 10 ahead / 178 behind | Its romanization adapter (4,326 bytes) is an earlier snapshot than main's 4,438-byte diacritic-aware, numeral-safe renderer and expanded tests. No port. |
| `fix/pcgn-final-consonant-context-types-2026-11-16` | 2 ahead / 117 behind | Its PCGN module (65,380 bytes) is an earlier snapshot than main's 120,449-byte module; tests are likewise older. No port. |
| `fix/pcgn-shortened-vowel-diacritic-inventory-2026-11-15` | 11 ahead / 168 behind | `data/khmer/romanization_marks_numerals.csv` is byte-identical to main (SHA `05ead18e065575eb14230d41ea3afe5dfacb2c22`). Already integrated. |
| `fix/serve-coverage-report-on-pages-2026-10-21` | 6 ahead / 515 behind | `scripts/coverage.py` is byte-identical to main (SHA `9a2032211018b47a095c15d49636c2b1b9243044`); current dual internal/public report generation and published artifact are integrated. |
| `release/deterministic-rule-engine-2026-11-11` | 15 ahead / 232 behind | Its initial rule engine (5,914 bytes) and hybrid shim are superseded by main's 16,220-byte rule engine and typed-IPA hybrid diagnostic implementation. No release branch is treated as a release candidate. |

**Disposition:** all 14 `fix/*` and the single `release/*` refs have focused compare/content dispositions. Current main contains the later versions or exact matching implementation/data. No code, runtime, IPA, pronunciation, corpus or mapping changes were made by this audit. All branches remain preserved.


## Documentation-branch family reconciliation — 2026-11-17

Compared all **96** `docs/*` refs with main `5fbb8352165fe72124214541a00105730d8097a5`. This includes 35 `post-pr*` mainline checkpoints and 61 other documentation closeouts/reconciliation branches. The compare file lists show documentation-only changes, with a small number of README/AGENTS/architecture, source-registry metadata or test-provenance updates; no unintegrated runtime implementation was identified.

Representative content checks confirmed:
- The current master handoff is cumulative and longer than the historical checkpoint branches; inspected older checkpoints contain no unique handoff lines that are missing from main, except a mixed-script closeout note whose implementation and later status are already captured in current main documentation.
- The 35 `post-pr*` branches touch only the master handoff, completion register, repository audit and/or romanization matrix. Their historical CI checkpoints are superseded by later mainline checkpoints.
- The Khmer parser/source-registry handoff branches carry older source-registry snapshots; current main has the larger 49-record source registry. `tests/test_rule_registry_provenance.py` is byte-identical to main.
- The Unicode/LOC parser final-state branches contain earlier verification counts and TODO wording; main records later parser completion and explicitly keeps lexical word division/TN #61 separate.
- The repository-information-architecture branch's `AGENTS.md`, codebase map and methodology references are byte-identical to main; its README/architecture are earlier snapshots than current main.
- The accessibility, romanization, PCGN assembly, parser, mixed-script and source-audit closeout branches are historical documentation snapshots of work already reflected in the current implementation, tests and audit registers.

**Disposition:** all 96 `docs/*` refs have compare/file-scope dispositions. No documentation branch was merged wholesale; no code or source data was copied from a stale checkpoint. All branches remain preserved. This closes the `docs/*` family comparison pass, not the repository-wide branch audit until all other branch prefixes and PR ancestry have been reconciled.


## PCGN anusvara/visarga syllable assembly recovered from a historical branch — 2026-11-18

A focused comparison of `feat/pcgn-anusvara-visarga-syllable-assembly-2026-11-16` against the then-current mainline found a genuinely distinct, bounded assembler that was not present in main. The historical branch was 3 commits ahead / 77 behind and changed only `src/khmer_ua/pcgn.py` and `tests/test_pcgn_anusvara_visarga_syllable_assembly.py`. Its test referred to `schemas/pcgn-anusvara-visarga-syllable-assembly.schema.json`, but that schema was absent from the historical branch.

Rather than merging the stale branch snapshot, the feature was ported onto current main in PR [#351](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/351), merged as `5fc517df5708424dea7a67da36bded581e659145`.

The port adds:
- `PCGNAnusvaraVisargaSyllableAssembly` and `assemble_pcgn_anusvara_visarga_syllable`, composing the existing consonant, series and exact eight-row anusvara/visarga resolvers;
- caller-supplied onset and complete-syllable boundaries, with explicit NGA identification required for table row 8;
- a JSON Schema, package-level exports and tests covering all eight rows in both series plus mismatched-onset, missing/incorrect-coda and malformed/unlisted abstention cases.

Acceptance boundary is deliberately narrow: output is PCGN orthographic romanization only. `ipa` and `ukrainian` remain null; no segmentation is inferred and no phonetic or Ukrainian result is promoted.

Verification:
- PR-head Quality run [44256391593](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44256391593) SUCCESS; Python suite `431 passed, 70 subtests passed`, IPA gold engineering gate reports expected `NOT_READY_NO_ADJUDICATED_GOLD`, web checks and build passed.
- PR-head Chromium run [44256391474](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44256391474) SUCCESS.
- Post-merge mainline Quality [44256579643](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44256579643), Chromium [44256579618](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44256579618), and Pages build/deploy [44256579655](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44256579655) SUCCESS. Mainline Python suite also reports `431 passed, 70 subtests passed`; Pages artifact upload completed.

The historical source branch remains preserved. This is a recovered implementation, not a linguistic gold milestone; IPA convention approval, adjudicated IPA gold, word segmentation and release readiness remain unchanged.


## PCGN feature-branch family content reconciliation — 2026-11-18

Compared the 28 pre-existing `feat/pcgn-*` branches against current main and inspected the source-module declarations for the 28 corresponding historical snapshots. The audit was deliberately content-level rather than treating ahead/behind counts as merge recommendations.

- The 27 other branch snapshots' top-level PCGN classes/functions are all present in the current `src/khmer_ua/pcgn.py` or `src/khmer_ua/pcgn_unicode.py`; their modules are older, narrower snapshots and no wholesale port is warranted.
- The remaining unique declaration was `assemble_pcgn_anusvara_visarga_syllable` from `feat/pcgn-anusvara-visarga-syllable-assembly-2026-11-16`. It is now integrated by PR #351 with the missing schema, package exports and tests; the source branch itself remains untouched.
- Selected data checks confirmed that the PCGN consonant table, final-consonant table and anusvara/visarga table match current main by blob SHA. The main PCGN notes register is newer than the older Note 1–10 branch snapshots.
- All reviewed historical branches remain preserved. No broad merge, branch deletion, force update or unsupported linguistic promotion occurred.

This closes a focused module-declaration reconciliation of the 28-branch PCGN feature family. It does not claim full file-by-file review of every changed test, schema, documentation and PR ancestry across all 28 refs; the repository-wide historical branch audit remains PARTIAL until that wider scope is completed.


## 2026-11-18 continuation — optional Khmer Phonemizer workflow and current ref inventory

- **KHMER-PHONEMIZER-WORKFLOW-001 — DONE_VERIFIED:** PR [#353](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/353) adds a separate `.github/workflows/optional-khmerphonemizer-smoke.yml`, pins `khmerphonemizer==0.0.3`, runs the existing diagnostic script, and uploads JSON plus SHA-256 sidecar. Exact-head raw-output run [44259498574](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44259498574), Quality [44259498582](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44259498582), Chromium [44259498488](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44259498488), and branch-push Quality [44259475466](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44259475466) all SUCCESS. Artifact ID 14406708793; 1,972 bytes. This is execution/provenance evidence only; independent gold remains 0 and accuracy null.
- **Historical ref inventory — refreshed 2026-11-18:** 224 refs, 224 unique tip SHAs, 223 non-main refs. Prefix counts: a11y 2, audit 15, benchmark 1, ci 1, data 4, docs 97, feat 50, fix 14, release 1, research 28, test 10. Open PRs 0 at the base checkpoint; Issue #104 is the sole open issue.
- **a11y branches:** already integrated by PRs #331 and #333; no duplicate port.
- **new docs/feat refs:** the 97th docs ref and 50th feat ref correspond to merged PRs #352 and #351.
- **audit refs:** 15 refs compared to main; changed files are documentation-only, or the ref is behind-only. PRs #341–#350 contain the successive merged closeouts.
- **benchmark/current-engine:** DEFERRED pending item-level rights/provenance review of the Neurlang lexicon and evidence that would permit a properly scoped non-gold diagnostic; do not treat its outputs as accuracy.
- **ci/khmer-g2p-smoke:** historical unpinned workflow not copied. Its script/tests remain on main; the separate pinned workflow in PR #353 restores this diagnostic while preserving the existing MekongPhon workflow.
- **KHM-BRANCH-AUDIT-001 — PARTIAL:** inventory refreshed, but full file/commit/PR-ancestry review of every one of 223 non-main refs remains incomplete.
- **IPA gold — BLOCKED:** Issue #104 remains open. gold.tsv is header-only and the four JSONL annotation/adjudication/record/split files are empty. No expert contact/recruitment is recorded; convention approval, independent annotators/adjudicator, curator, private blind channel, source rights and 30 adjudicated items remain acceptance criteria.
- **Release classification:** research-ready partial prototype; not linguistically release-ready. No new IPA, pronunciation rule, gold label or accuracy score was created.

 
### Live inventory after creating continuation branch (2026-11-18)

The continuation branch for PR #353 adds one new preserved audit ref after the 224-ref baseline snapshot above. The live listing now contains **225 refs and 225 unique tip SHAs** (main + 224 non-main); prefix counts are a11y 2, audit 16, benchmark 1, ci 1, data 4, docs 97, feat 50, fix 14, release 1, research 28, test 10. While PR #353 is open, the live count is 1 open PR (#353) and 1 open issue (#104). This is a separate timestamped inventory snapshot; it does not change the earlier 224-ref snapshot or claim full historical file/ancestry review.


## PR #353 post-merge mainline closeout — 2026-11-18

PR [#353](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/353) is merged into `main` as implementation commit `d887a7f4866b7d19050a0a140db2d96a259ccdfc`.

All post-merge checks on that exact mainline SHA completed SUCCESS:
- Quality [44259925491](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44259925491).
- Chromium browser smoke [44259925384](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44259925384).
- GitHub Pages build/deploy and deployed-site/runtime-asset smoke [44259925382](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44259925382).
- Pinned Khmer Phonemizer raw-output workflow [44259925379](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44259925379), SUCCESS; artifact ID 14407298530, 1,941 bytes, SHA-256 artifact digest `9ad7ec54b67307aa7a248f6ce897ef4f94913770c69bfbf8fc56e574c699c553`.

Final post-merge repository snapshot: 225 refs / 225 unique tip SHAs (main + 224 non-main), 0 open PRs, and 1 open issue (#104). Prefix counts: a11y 2, audit 16, benchmark 1, ci 1, data 4, docs 97, feat 50, fix 14, release 1, research 28, test 10. The active continuation and historical refs remain preserved.

This closes the optional workflow restoration and its post-merge verification. It does not close `KHM-BRANCH-AUDIT-001` (full file/commit/PR-ancestry audit remains PARTIAL), nor Issue #104 (human convention approval, independent annotation/adjudication, rights and 30-item gold pilot remain BLOCKED). Independent adjudicated IPA gold remains 0 and empirical accuracy remains null. No local checkout or local tests were run in this connector-only session.


## Human IPA-gold recruitment gate revalidation — 2026-11-18

- Rechecked Issue [#104](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/104), its 33-comment history, the collection playbook, corpus contract and the Sok & Adams source audit. The latest recorded shortlist identifies Chem Vatho for primary target-profile convention review and James P. Kirby for a bounded independent phonetics challenge, subject to explicit conflict/collaboration checks. These remain leads only; no contact, acceptance or appointment is evidenced.
- Added a recruitment execution kit to the existing playbook: separate draft invitations for primary convention review, independent challenge review and annotator/adjudicator/curator recruitment; a private response/qualification register; conflict/independence checks; and an ordered start gate. These are drafts, not sent messages.
- Reclassified stale playbook TODOs as evidence-backed BLOCKED gates: the documented Khmer Acoustic Model dictionary artifact is unavailable at the inspected path and its entry-count/license claims conflict; convention approval, qualified independent roles, rights-cleared items and private blind intake require external human evidence.
- No IPA labels, source records, corpus rows, splits, benchmark scores, runtime rules or Ukrainian mappings were changed. `data/benchmark/gold.tsv` remains header-only; independent adjudicated gold=0; empirical accuracy=null.
- No external contacts were made and no private contact data was added. This documentation work does not satisfy Issue #104 or change release readiness.


## PR #355 post-merge closeout — 2026-11-18

PR [#355](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/355) merged into `main` as `083f9a64729ae7b01d63555090f10536db0ef242`.

Exact PR-head checks on `749f36633e448259b129a20a406f357ac10e5507` completed SUCCESS before merge:
- Quality [44261845934](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44261845934): corpus-structure validation, Python tests, web checks and production build all passed.
- Chromium browser smoke [44261845844](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44261845844): deterministic web checks, production build, Chromium installation and visible-results verification all passed.

The merge commit is the latest repository commit as of this closeout. No post-merge workflow runs were created for the documentation-only merge; verification evidence is from the exact merged PR head. No local checkout or local tests were performed in this connector-only session.

PR #355 adds invitation drafts and a private response/qualification protocol only. No outreach was sent, no expert or annotator was appointed, no source rights were cleared, and no blind intake was tested. The convention remains `DRAFT_NOT_APPROVED`; Issue #104 remains open; independent adjudicated IPA gold remains 0 and empirical accuracy remains null. This closes the documentation change, not the linguistic pilot or release gate.


## Khmer Acoustic Model upstream artifact recheck — 2026-11-18

- Rechecked the public upstream repository at exact default-branch commit `2714994b41ccf875c5b6f6182b48a72f13632dbf`: only branch `main`, no releases, and no full dictionary file in the recursive tree. The dictionary directory contains only a README and a six-line sample file (blob SHA `9dbd64d74194485fbfda69dce41b5129b5fbb8ab`, 144 bytes).
- Upstream root README advertises 29,204 entries and CC BY-SA 4.0 for the pronunciation dictionary; `dictionary/README.md` describes a mapping derived from 33,091 entries under CC BY 4.0. The root MIT license is software licensing; the README separately assigns MIT to the acoustic model. The two data statements have differently described scopes, but the available repository does not establish whether the mapping is distinct from the underlying lexicon. Do not assume a single license or resolve the count discrepancy by guess.
- Updated the existing external corpus triage, gold collection playbook and benchmark source note with this pinned evidence. No sample rows were copied; no IPA labels, corpus rows, split manifests, runtime rules or accuracy values were changed.
- **Disposition: BLOCKED for import/training.** Required next evidence: full versioned artifact + SHA-256; per-artifact license and redistribution terms; per-entry source provenance; target variety/profile and IPA convention; annotator/adjudication method and meaning of “validated”; author clarification of the 29,204/33,091 counts and CC BY-SA/CC BY scope.
- Issue #104 remains open; independent adjudicated gold remains 0 and empirical accuracy remains null.


## PR #357 post-merge closeout — 2026-11-18

PR [#357](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/357) merged into `main` as `14a0f59a29b58279ce19267f5207c6046fbfe15f`.

Exact PR-head hosted checks on `c5c8849328b802fd560a120cfa52164c85344d4f` completed SUCCESS:
- Quality [44265647506](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44265647506): independent IPA corpus structure validation, Python tests, web checks and production build.
- Chromium browser smoke [44265647507](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44265647507): deterministic web checks, production build, Chromium installation and visible-results verification.

No post-merge workflows were created for this documentation/research-only merge; the recorded checks ran on the exact merged PR head. No local checkout or local tests were performed in this connector-only session.

The source audit remains evidence-limited: upstream public tree lacks the full dictionary; license scope, counts and item provenance need author clarification. The candidate remains blocked for import/training. No IPA gold, source rows, benchmark splits, engine rules or accuracy figures were created. Issue #104 remains open; adjudicated gold=0; empirical accuracy=null.


## Live historical-ref inventory and PCGN port reconciliation — 2026-11-18

- Exact base `main`: `736f86db2fd5a60b35a18fa5ea3691ca20871f6f`. GitHub branch API pages 1–3 (100 entries per page) returned **230 refs and 230 unique tip SHAs**: main plus 229 non-main refs. Prefix counts: a11y 2, audit 16, benchmark 1, ci 1, data 4, docs 101, feat 50, fix 14, release 1, research 29, test 10. No duplicate tip SHA was found. Open PRs: 0; open issues: 1 (#104). This is a point-in-time inventory, not proof of full historical ancestry review.
- Reconciled `feat/pcgn-anusvara-visarga-syllable-assembly-port-2026-11-18` against current main. Its `src/khmer_ua/pcgn.py`, `src/khmer_ua/__init__.py`, `schemas/pcgn-anusvara-visarga-syllable-assembly.schema.json`, and `tests/test_pcgn_anusvara_visarga_syllable_assembly.py` have byte-identical Git blob SHAs on main and the historical branch. The four-commit branch is 16 commits behind main; its reported ahead status does not identify unique implementation. No cherry-pick, merge, or duplicate port is warranted; the branch remains untouched.
- Cross-checked seven other PCGN assembly snapshots (normal dependent closed, shortened closed, explicit open, independent-vowel closed, alif-dependent closed, robat closed, and glottal open): each has its corresponding test and schema path on main. The earlier 28-branch PCGN declaration reconciliation already found their module declarations present on main. This spot check supports preservation rather than wholesale merging; it is not a replacement for full per-file and PR-ancestry audit of every historical ref.
- `KHM-BRANCH-AUDIT-001` remains **PARTIAL**: the live inventory is refreshed and this PCGN port family is reconciled, but all 229 non-main refs have not received complete file-level, commit-level, and PR-ancestry review. No historical branch was deleted or force-updated.
- No runtime, linguistic rules, corpus rows, IPA labels, or benchmark values changed. Independent adjudicated IPA gold remains 0; empirical accuracy remains null; Issue #104 remains the external human-evidence blocker.


## PR #359 post-merge closeout — 2026-11-18

PR [#359](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/359) merged into `main` as `d85081ba687b2003c195a5f7b4f0d78764fc9bc1`.

Exact PR-head checks on `3709c1912d1dad5aa18b7aa97b02e0f761484f7a` completed SUCCESS:
- Quality [44277171387](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44277171387).
- Chromium browser smoke [44277171272](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44277171272); deterministic web checks, production build, Chromium installation and visible-results verification passed.

Post-merge mainline runs on `d85081ba687b2003c195a5f7b4f0d78764fc9bc1`: Quality [44277328871](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44277328871) SUCCESS; Pages build/deploy [44277331001](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44277331001) SUCCESS. Post-merge Chromium smoke [44277328915](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44277328915) was still IN_PROGRESS at this closeout; do not count it as a pass until its run reports SUCCESS.

No runtime, linguistic rules, corpus rows, IPA labels or benchmark values changed. The repository-wide historical branch audit remains PARTIAL, Issue #104 remains open, independent adjudicated IPA gold remains 0 and empirical accuracy remains null. No local checkout or local tests were performed in this connector-only session.


## Research branch-family reconciliation — 2026-11-18

- Refreshed GitHub branch API pages 1–3 at exact main `da8054b893bf664a030ab9562e363c983815d344`: **232 refs / 232 unique tip SHAs** (main + 231 non-main), zero duplicate tips. Prefix counts: a11y 2, audit 17, benchmark 1, ci 1, data 4, docs 102, feat 50, fix 14, main 1, release 1, research 29, test 10. Open PRs: 0; open issue: #104. All historical refs remain preserved.
- Compared **all 29 `research/*` branch tips** to current main using GitHub compare. Every branch diverges; ahead range 1–91 commits and behind range 4–526. This is a compare/changed-file inventory, not a full per-file semantic review of every changed path or PR-ancestry closure.

| Research branch | Ahead | Behind | Disposition |
|---|---:|---:|---|
| `research/bgn-pcgn-ungegn-rule-diff-2026-11-15` | 5 | 176 | Older divergent snapshot; no wholesale merge |
| `research/complete-external-g2p-registry-2026-11-15` | 6 | 197 | Older divergent snapshot; no wholesale merge |
| `research/expert-shortlist-revalidation-2026-11-17` | 5 | 41 | Older divergent snapshot; no wholesale merge |
| `research/external-ipa-renderers-2026-10-24` | 7 | 526 | Older divergent snapshot; no wholesale merge |
| `research/google-khmer-lexicon-full-audit-2026-11-16` | 21 | 64 | Older divergent snapshot; no wholesale merge |
| `research/khmer-acoustic-model-release-audit-2026-11-16` | 26 | 63 | Older divergent snapshot; no wholesale merge |
| `research/khmer-engine-benchmark-expansion-2026-11-11` | 72 | 245 | Older divergent snapshot; no wholesale merge |
| `research/khmer-hybrid-benchmarks-reconciled-2026-11-11` | 34 | 234 | Older divergent snapshot; no wholesale merge |
| `research/khmer-hybrid-engine-2026-11-11` | 91 | 245 | Older divergent snapshot; no wholesale merge |
| `research/khmer-ipa-convention-draft-2026-11-17` | 5 | 63 | Older divergent snapshot; no wholesale merge |
| `research/khmer-ipa-convention-draft-v2-2026-11-17` | 7 | 62 | Older divergent snapshot; no wholesale merge |
| `research/khmer-kirby-cluster-audio-audit-2026-11-17` | 9 | 56 | Older divergent snapshot; no wholesale merge |
| `research/khmer-kirby-tonogenesis-audio-audit-2026-11-17` | 26 | 51 | Older divergent snapshot; no wholesale merge |
| `research/khmer-lexical-segmentation-evidence-2026-11-17` | 4 | 38 | Older divergent snapshot; no wholesale merge |
| `research/khmer-lexical-segmentation-evidence-mainline-2026-11-17` | 2 | 24 | Older divergent snapshot; no wholesale merge |
| `research/khmer-phonotactic-scope-2026-11-15` | 9 | 195 | Older divergent snapshot; no wholesale merge |
| `research/khmer-source-audit-integration-2026-11-17` | 7 | 58 | Older divergent snapshot; no wholesale merge |
| `research/khmer-unicode-syllable-grammar-2026-11-16` | 1 | 73 | Older divergent snapshot; no wholesale merge |
| `research/loc-khmer-word-division-2026-11-16` | 6 | 92 | Older divergent snapshot; no wholesale merge |
| `research/mekongphon-diagnostic-harness-2026-11-15` | 11 | 203 | Older divergent snapshot; no wholesale merge |
| `research/mekongphon-release-rights-audit-2026-11-16` | 10 | 63 | Older divergent snapshot; no wholesale merge |
| `research/mekongphon-seed-lexicon-audit-2026-11-16` | 34 | 64 | Older divergent snapshot; no wholesale merge |
| `research/pcgn-note-registry-2026-11-15` | 6 | 174 | Older divergent snapshot; no wholesale merge |
| `research/phon-sobon-and-lexicon-triage-2026-11-15` | 11 | 198 | Older divergent snapshot; no wholesale merge |
| `research/phonetic-literature-fulltext-review-2026-11-17` | 6 | 45 | Older divergent snapshot; no wholesale merge |
| `research/pin-khmer-acoustic-dictionary-artifact-audit-2026-11-18` | 6 | 4 | Older divergent snapshot; no wholesale merge |
| `research/sok-adams-khmer-phonology-audit-2026-11-17` | 7 | 48 | Older divergent snapshot; no wholesale merge |
| `research/sok-adams-rule-transfer-audit-2026-11-17` | 5 | 36 | Older divergent snapshot; no wholesale merge |
| `research/ungegn-engine-candidate-review-2026-11-15` | 5 | 177 | Older divergent snapshot; no wholesale merge |

### Focused content-level checks and dispositions

- External IPA renderer registry: `data/external-ipa-renderers.json`, its schema, and `tests/test_external_ipa_registry.py` are byte-identical between main and `research/external-ipa-renderers-2026-10-24`; no port required. The later MekongPhon diagnostic branch's workflow is also byte-identical to main.
- External source registry snapshots are stale subsets: the three checked branches have 36 or 46 source entries versus 49 on main, and none contains an ID absent from main. Main has 13, 3 and 3 additional entries respectively. No branch-only source record was identified in these checks.
- PCGN Note registry branch is an older snapshot: both main and branch CSV contain the same 11 note numbers, but branch row text predates the bounded resolvers and explicit unresolved contracts now recorded on main. Main CSV is 7,233 bytes vs 5,455; main test is 6,218 bytes vs 2,092. No old CSV/test overwrite is appropriate.
- The hybrid-engine/benchmark branches contain earlier versions of `hybrid.py` (5,701 bytes vs main 6,971), `rule_engine.py` (5,895 vs 16,220), and `test_hybrid_engine.py` (1,718 vs 4,452). Their mainline counterparts are more developed; no implementation port is indicated by the snapshots.
- The benchmark-expansion branch's 4,461-byte optional workflow is not the current 1,443-byte main workflow. Its extra neural-model job and diagnostic harness are not adopted: source-attested MekongPhon concordance is not independent gold, the data rights remain unresolved, and the existing source audit explicitly defers this path. No model benchmark was run and no score is claimed.
- The PCGN phonotactic-scope branch's `tests/test_parser.py` is an older 4,120-byte snapshot vs 7,491 bytes on main. The IPA convention draft v2 is byte-identical to main. The lexical segmentation mainline branch reports no changed files relative to the compare base at its tip.
- Selected main-vs-branch checks therefore support preserving current mainline implementations and retaining historical refs, not merging old divergent branch tips. Remaining branches still need full changed-file semantic review and PR ancestry reconciliation.

**KHM-BRANCH-AUDIT-001 remains PARTIAL.** Completed in this pass: live inventory refresh, compare results for all 29 research refs, and focused content dispositions for the paths above. Outstanding: equivalent content/ancestry review for all changed paths in these 29 refs and remaining non-research families. No branch was deleted, force-updated or merged wholesale. No runtime, linguistic rules, IPA labels, corpus rows, source rights or benchmark values changed. Independent adjudicated IPA gold remains 0; empirical accuracy remains null; Issue #104 remains open.

## PR #359 post-merge verification correction — 2026-11-18

The previously pending post-merge Chromium run [44277328915](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44277328915) subsequently completed SUCCESS. For main `da8054b893bf664a030ab9562e363c983815d344`, all three post-merge workflows completed SUCCESS: Quality [44277815119](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44277815119), Chromium [44277815233](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44277815233), and Pages build/deploy [44277815127](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44277815127).


## Audit branch-family reconciliation — 2026-11-18

- Refreshed all branch API pages at main `3731a16cbb8553a6d3db9f7fc28708030a187d06`: **233 refs / 233 unique tips** (main + 232 non-main), zero duplicate tip SHAs. Prefix counts: a11y 2, audit 18, benchmark 1, ci 1, data 4, docs 102, feat 50, fix 14, main 1, release 1, research 29, test 10. Open PRs: 0; open issue #104 remains. This inventory includes the merged PR #361 source branch, which is preserved.
- Compared all **18 `audit/*` refs** to current main. The comparison results and focused content dispositions are below. All but the restored phonemizer workflow branch are documentation-only; the workflow branch's `.github/workflows/optional-khmerphonemizer-smoke.yml` is byte-identical to main (blob SHA `a89a848d66810225bbcc2cc5c9143b94304a680d`). No code port is needed. The branch created for PR #361 now has its docs content merged into main; the source branch remains preserved.

| Audit branch | Ahead | Behind | Content disposition |
|---|---:|---:|---|
| `audit/complete-docs-branch-family-reconciliation-2026-11-17` | 3 | 11 | docs-only |
| `audit/complete-feature-and-test-branch-reconciliation-2026-11-17` | 3 | 14 | docs-only |
| `audit/complete-fix-and-release-branch-reconciliation-2026-11-17` | 3 | 12 | docs-only |
| `audit/complete-remaining-branch-families-2026-11-17` | 0 | 10 | no changed files |
| `audit/complete-research-branch-family-reconciliation-2026-11-17` | 3 | 13 | docs-only |
| `audit/continue-historical-branch-reconciliation-2026-11-17` | 3 | 19 | docs-only |
| `audit/continue-pcgn-branch-reconciliation-2026-11-17` | 3 | 17 | docs-only |
| `audit/continue-pcgn-note-and-special-syllable-branch-reconciliation-2026-11-17` | 3 | 15 | docs-only |
| `audit/continue-pcgn-vowel-and-syllable-branch-reconciliation-2026-11-17` | 3 | 16 | docs-only |
| `audit/continue-typed-ipa-and-coverage-branch-reconciliation-2026-11-17` | 3 | 18 | docs-only |
| `audit/current-branch-inventory-2026-11-16` | 2 | 125 | docs-only |
| `audit/final-branch-inventory-closeout-2026-11-17` | 3 | 20 | docs-only |
| `audit/pr153-diff-reconciliation-2026-11-15` | 2 | 208 | docs-only |
| `audit/reconcile-research-branch-family-reconciliation-2026-11-18` | 6 | 0 | PR #361 merged; content now on main |
| `audit/reconcile-selected-historical-branch-content-2026-11-17` | 6 | 21 | docs-only |
| `audit/refresh-branch-inventory-2026-11-17` | 3 | 22 | docs-only |
| `audit/refresh-live-inventory-and-reconcile-pcgn-port-2026-11-18` | 3 | 2 | docs-only |
| `audit/restore-pinned-khmer-phonemizer-smoke-2026-11-18` | 8 | 8 | workflow file byte-identical to main |

- These are branch-tip compare and focused content checks, not a complete per-file semantic review of every changed historical file or full PR ancestry audit. The audit branches mostly carry snapshots of previous inventory/reconciliation reports, not implementation candidates. No audit branch is merged wholesale; no historical branch is deleted or force-updated.
- `KHM-BRANCH-AUDIT-001` remains **PARTIAL**. The research family (29 refs) and audit family (18 refs) now have compare inventories; focused semantic checks cover only selected implementation/data paths. Remaining docs, a11y, ci, benchmark and other historical families still require complete changed-file and PR-ancestry review. No runtime, linguistic rules, IPA labels, corpus rows or benchmark values changed.

## PR #361 post-merge closeout — 2026-11-18

PR [#361](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/361) merged as `3731a16cbb8553a6d3db9f7fc28708030a187d06`.

Exact PR-head checks on `036fabab2606f2b4269088a50e1610bb3cf1f0dd` completed SUCCESS:
- Quality [44282464851](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44282464851).
- Chromium [44282464691](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44282464691).

Post-merge mainline Quality, Chromium and Pages runs were still in progress at this closeout: [44282675127](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44282675127), [44282675115](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44282675115), [44282675129](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44282675129). Update this status only after the runs complete.


## Accessibility, CI, benchmark and recent documentation branch checks — 2026-11-18

- Compared the two `a11y/*`, one `ci/*`, one `benchmark/*`, and 11 selected recent `docs/*` branch tips against main `95f0a69f861294490845425b622832bea49df2ab`. Current live inventory at this base: 233 refs / 233 unique tips (main + 232 non-main); docs family has 102 refs. The earlier docs-family audit covered 96 refs at its historical base; the 11 targeted checks below are supplemental spot checks, not a claim that every one is necessarily among the six net-new docs refs.

| Documentation branch | Ahead | Behind | Scope |
|---|---:|---:|---|
| `docs/ipa-gold-recruitment-execution-kit-2026-11-18` | 4 | 7 | Documentation-only snapshot |
| `docs/pr355-post-merge-closeout-2026-11-18` | 3 | 6 | Documentation-only snapshot |
| `docs/pr357-upstream-audit-closeout-2026-11-18` | 3 | 4 | Documentation-only snapshot |
| `docs/pr359-post-merge-closeout-2026-11-18` | 3 | 2 | Documentation-only snapshot |
| `docs/record-pcgn-anusvara-assembly-port-2026-11-18` | 6 | 10 | Documentation-only snapshot |
| `docs/close-shared-fallback-parity-task-2026-11-17` | 3 | 34 | Documentation-only snapshot |
| `docs/closeout-mixed-script-boundaries-2026-11-17` | 3 | 44 | Documentation-only snapshot |
| `docs/correct-khmer-nova-tokenization-scope-2026-11-17` | 3 | 26 | Documentation-only snapshot |
| `docs/khmer-fallback-parity-mainline-closeout-2026-11-17` | 3 | 35 | Documentation-only snapshot |
| `docs/khmer-onset-registry-mainline-closeout-2026-11-17` | 3 | 32 | Documentation-only snapshot |
| `docs/skip-navigation-closeout-2026-11-17` | 3 | 30 | Documentation-only snapshot |

### Content findings

- `a11y/wcag-text-contrast-2026-11-17`: its `index.html`, `src/styles/main.css` and `tests/browser/site.spec.js` are byte-identical to main. Already integrated; no port.
- `a11y/skip-navigation-2026-11-17`: skip-navigation behavior is present on main, but the branch is an older snapshot. Main's stylesheet uses the later WCAG contrast palette, and main browser tests include the contrast-ratio helper and AA checks absent from the branch test. The branch is not a safe overwrite.
- `ci/khmer-g2p-smoke-2026-10-24`: its 1,145-byte optional workflow uses older actions checkout/setup-python versions and installs `khmerphonemizer` without a version pin. Main has a distinct 1,443-byte optional MekongPhon diagnostic workflow plus the separately pinned `khmerphonemizer==0.0.3` smoke workflow. Do not port the unpinned older workflow.
- `benchmark/current-engine-2026-11-11`: its `.github/workflows/benchmark-current-engine.yml` does not exist on main. Keep DEFERRED: it consumes the Neurlang lexicon alongside the pinned MekongPhon split, but item-level provenance/rights and independent evaluation criteria remain unresolved. No benchmark was run; no accuracy is claimed.
- Prior documentation-family audit covered 96 `docs/*` refs at historical main `5fbb8352165fe72124214541a00105730d8097a5`. The 11 targeted branch comparisons above show documentation-only diffs. No branch was merged wholesale and no stale checkpoint text was copied over main.

**KHM-BRANCH-AUDIT-001 remains PARTIAL.** The a11y/CI/benchmark branch family now has focused dispositions; docs have a prior 96-ref family audit plus 11 targeted follow-up comparisons. A complete current-base content/PR-ancestry reconciliation of every documentation branch and all remaining branch families is still outstanding. All historical refs remain preserved. No runtime, linguistic rules, IPA labels, source records, benchmark data or rights status changed.

## PR #362 post-merge closeout — 2026-11-18

PR [#362](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/362) merged into `main` as `95f0a69f861294490845425b622832bea49df2ab`.

Exact PR-head checks on `08882bbe963429f2f9243ed3dd79b73e01c192f9` completed SUCCESS: Quality [44282811673](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44282811673) and Chromium [44282838244](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44282838244).

Post-merge mainline Quality [44283185333](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44283185333), Chromium [44283185381](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44283185381), and Pages [44283185385](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44283185385) were still IN_PROGRESS at this closeout; do not mark them successful until confirmed.


## PR #362 and #363 closeout; live inventory refresh — 2026-11-18

- PR [#362](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/362) merged as `95f0a69f861294490845425b622832bea49df2ab`. Its exact-head Quality [44282811673](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44282811673) and Chromium [44282838244](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44282838244) both SUCCESS. Post-merge mainline Quality [44283185333](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44283185333), Chromium [44283185381](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44283185381), and Pages [44283185385](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44283185385) subsequently all completed SUCCESS.
- PR [#363](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/363) merged into `main` as `66009beed50a0ffbe4258c4ebf35344669ac3901`. Exact PR-head checks on `2dc45e04facc6cee18ac2fcb990eeb7a663dbbf2`: Quality [44283352910](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44283352910) SUCCESS, Quality [44283379087](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44283379087) SUCCESS, and Chromium [44283378923](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44283378923) SUCCESS.
- Refreshed all three GitHub branch API pages at `main=66009beed50a0ffbe4258c4ebf35344669ac3901`: **235 refs / 235 unique tip SHAs** (main + 234 non-main), zero duplicate tips. Prefix counts: a11y 2, audit 20, benchmark 1, ci 1, data 4, docs 102, feat 50, fix 14, main 1, release 1, research 29, test 10. Open PRs: 0; Issue #104 remains open.
- Post-merge mainline workflows for `66009beed50a0ffbe4258c4ebf35344669ac3901` were still IN_PROGRESS at this closeout: Quality [44283576661](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44283576661), Chromium [44283576328](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44283576328), Pages [44283576129](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44283576129). Do not count these as passes until completed.

No implementation, phonological rule, IPA label, source record, rights decision, benchmark score or gold row changed in PRs #362–#363. Historical refs remain preserved. `KHM-BRANCH-AUDIT-001` remains PARTIAL; independent adjudicated IPA gold remains 0, empirical accuracy remains null, and Issue #104 is the human-evidence blocker.


## Unicode TN #61 v2 source-registry alias reconciliation — 2026-11-18

- Compared `data/khmer/sources.json` on main with the older `docs/khmer-unicode18-parser-final-handoff-2026-11-16` branch. Its only branch-only source ID was `unicode-tn61-v2`; it describes the same title, author, version 2, date, Unicode landing page and PDF already registered on main as `unicode-tn61-khmer-encoding-structure-v2`. This was an identifier alias for the same publication, not a distinct source. No duplicate record was imported.
- Enriched the canonical main record with metadata from the old record and primary publication: year 2025; author affiliation SIL International, NPIC LSDU; official landing page; previous-version URL; and `rights_status=PUBLIC_DISTRIBUTION_PERMISSION_NOT_ESTABLISHED`. The official [TN #61 v2 page](https://www.unicode.org/notes/tn61/tn61-2.html) identifies version 2, 2025-02-06, author M. Hosken, previous version and landing page, and says reproduction/modification/other unpermitted use requires permission. The [PDF title page](https://www.unicode.org/notes/tn61/utn61-Khmer_Encoding_Structure_V2.pdf) identifies Martin Hosken (SIL International, NPIC LSDU) and contributors Norbert Lindenberg and Makara Sok.
- Extended `tests/test_rule_registry_provenance.py` to assert the enriched metadata and rights status. Existing assertions still enforce the canonical ID, non-normative technical-note status, and that TN #61 is not the Unicode Standard and is not implemented by the current parser.
- No TN #61-derived grammar, parser behavior, pronunciation rule, IPA, Ukrainian output, corpus record or gold label was added. TN #61 remains a separately versioned, non-normative research profile; Unicode 18 §16.4 remains the parser's implemented standard basis.


## Documentation-family compare completion and TN #61 metadata closeout — 2026-11-18

- Completed GitHub compare of all **103 current `docs/*` branch tips** against main `66009beed50a0ffbe4258c4ebf35344669ac3901`. Every tip was compared and changed-file lists were reviewed. Most branches are historical documentation/checkpoint snapshots; selected changes touch README/AGENTS/architecture, source-registry metadata, test provenance or the romanization matrix. No documentation branch was merged wholesale. The current compare includes the `docs/pr362-pr363-postmerge-closeout` branch later merged by PR #364.
- Source-registry content review: the `docs/khmer-1997-profile` snapshot (29 entries), parser-source-registry snapshots (46 each), and romanization-test-closeout snapshot (28) are subsets of main's 49 entries with no branch-only source IDs. The Unicode18 parser handoff branch had one extra ID, `unicode-tn61-v2`, which is an alias for main's canonical `unicode-tn61-khmer-encoding-structure-v2`, not a distinct publication. PR #365 enriched that canonical record with the alias snapshot's verified metadata and added regression assertions; it did not create a duplicate source record.
- `tests/test_rule_registry_provenance.py` on main already enforced TN #61's canonical ID, version/date, official URL, non-normative status, rights limitations, and no-parser-implementation boundary. PR #365 extends those assertions to year, affiliation, landing page, previous version and explicit permission-not-established rights status.
- Documentation family compare status: **103/103 tips compared**. This completes the current-base branch-tip compare pass, but not semantic review of every changed documentation line or all PR ancestry. All historical branches remain preserved.

## PR #365 source-registry metadata closeout — 2026-11-18

PR [#365](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/365) merged into `main` as `cb4aa8c1e69d1a4fafcd40f59577bef4fd45f7a5`.

Exact PR-head checks on `114e89e2e8a3ab6ea34f6de2c7899affcb4961a7` completed SUCCESS: Quality [44285305424](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44285305424) and [44285327561](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44285327561), Chromium [44285327565](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44285327565). Post-merge mainline runs on `cb4aa8c1e69d1a4fafcd40f59577bef4fd45f7a5` were still in progress at closeout: Quality [44285486097](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44285486097), Chromium [44285486019](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44285486019), Pages [44285486075](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44285486075).

Current live branch inventory at this closeout: **237 refs / 237 unique tip SHAs** (main + 236 non-main), zero duplicate tips. Prefix counts: a11y 2, audit 20, benchmark 1, ci 1, data 4, docs 103, feat 50, fix 15, main 1, release 1, research 29, test 10. Open PRs: 0. Issue #104 remains open. No runtime, IPA, Ukrainian output, gold labels or accuracy figures changed; the repository remains a research-ready partial prototype, not linguistically release-ready.


## PR #366 post-merge closeout — 2026-11-18

PR [#366](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/366) merged into `main` as `9c11943aeb10746b006a9684df13fe71dc9f6794`.

Exact PR-head checks on `be079196a4008a8beaaf5339a649e336d673aab3` completed SUCCESS: Quality [44285636247](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44285636247) and [44285613505](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44285613505), Chromium [44285636264](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44285636264).

Post-merge mainline checks on `9c11943aeb10746b006a9684df13fe71dc9f6794` all completed SUCCESS:
- Quality [44286018948](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44286018948).
- Chromium [44286018958](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44286018958).
- Pages build, production Chromium exercise, artifact upload and deploy [44286018982](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44286018982).

Live branch inventory at this checkpoint: **238 refs / 238 unique tip SHAs** (main + 237 non-main), zero duplicate tips. Prefix counts: a11y 2, audit 20, benchmark 1, ci 1, data 4, docs 104, feat 50, fix 15, main 1, release 1, research 29, test 10. Open PRs: 0; Issue #104 remains open.

PRs #365–#366 change only source metadata, tests and audit documentation. No TN #61-derived parser grammar, pronunciation rule, IPA, Ukrainian output, corpus row, gold label or accuracy score was introduced. `KHM-BRANCH-AUDIT-001` remains PARTIAL pending full semantic and PR-ancestry reconciliation; human linguistic pilot remains BLOCKED by Issue #104. Repository status remains research-ready partial prototype, not linguistically release-ready. No local checkout or local tests are claimed; verification is hosted GitHub Actions.


## PR #367 final closeout and live ref reconciliation — 2026-11-18

PR [#367](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/367) merged into `main` as `ac1bb5dbdb1245e7045939c3a4f57de2deb59242`.

Exact PR-head checks on `ca5083fdd3287acdb0c0422db99f3d21235703fc` completed SUCCESS: Quality [44286408991](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44286408991), Quality [44286432543](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44286432543), Chromium [44286432417](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44286432417).

Post-merge mainline checks on `ac1bb5dbdb1245e7045939c3a4f57de2deb59242`: Quality [44286626785](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44286626785) SUCCESS; Pages build/deploy [44286626801](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44286626801) SUCCESS. Chromium [44286626936](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44286626936) remained IN_PROGRESS at last check, with deterministic web checks and production build completed and the Chromium installation step still active. The exact merged PR-head Chromium check succeeded; do not mark the post-merge run as success until GitHub reports completion.

Live inventory after creating this closeout branch: **240 refs / 239 unique tips** at the moment before its first commit; the only shared SHA was the expected `main` + new branch base `ac1bb5dbdb1245e7045939c3a4f57de2deb59242`. The closeout commit will give this branch its own tip. Prefix counts: a11y 2, audit 20, benchmark 1, ci 1, data 4, docs 106, feat 50, fix 15, main 1, release 1, research 29, test 10. All pre-existing non-main branch tips remain preserved. Open PRs before this closeout: 0; Issue #104 remains open.

Repository-wide status: research-ready partial prototype, not linguistically release-ready. `KHM-BRANCH-AUDIT-001` remains PARTIAL despite current-base branch-tip compare coverage; full semantic review of every changed path and PR ancestry is still incomplete. Human IPA pilot remains BLOCKED by expert approval/recruitment, rights-cleared items and blind adjudication. Independent adjudicated gold remains 0; empirical accuracy remains null. No local checkout or local tests are claimed; hosted GitHub Actions provide the recorded verification.


## Audit branch-family reconciliation — 2026-11-18

- Refreshed live branch inventory at main `cb21aeff8a8a7d97ea6a11d27766ff3ae8009fe9`: 240 refs / 240 unique tips; 20 `audit/*` branches. All 20 branch tips compared with GitHub compare against this exact main. Ahead range 0–8, behind range 6–216.

| Audit branch | Ahead | Behind | Changed-file disposition |
|---|---:|---:|---|
| `audit/complete-docs-branch-family-reconciliation-2026-11-17` | 3 | 19 | docs only |
| `audit/complete-feature-and-test-branch-reconciliation-2026-11-17` | 3 | 22 | docs only |
| `audit/complete-fix-and-release-branch-reconciliation-2026-11-17` | 3 | 20 | docs only |
| `audit/complete-remaining-branch-families-2026-11-17` | 0 | 18 | no changed files |
| `audit/complete-research-branch-family-reconciliation-2026-11-17` | 3 | 21 | docs only |
| `audit/continue-historical-branch-reconciliation-2026-11-17` | 3 | 27 | docs only |
| `audit/continue-pcgn-branch-reconciliation-2026-11-17` | 3 | 25 | docs only |
| `audit/continue-pcgn-note-and-special-syllable-branch-reconciliation-2026-11-17` | 3 | 23 | docs only |
| `audit/continue-pcgn-vowel-and-syllable-branch-reconciliation-2026-11-17` | 3 | 24 | docs only |
| `audit/continue-typed-ipa-and-coverage-branch-reconciliation-2026-11-17` | 3 | 26 | docs only |
| `audit/current-branch-inventory-2026-11-16` | 2 | 133 | docs only |
| `audit/final-branch-inventory-closeout-2026-11-17` | 3 | 28 | docs only |
| `audit/pr153-diff-reconciliation-2026-11-15` | 2 | 216 | docs only |
| `audit/reconcile-accessibility-ci-benchmark-docs-2026-11-18` | 3 | 6 | docs only |
| `audit/reconcile-audit-branch-family-2026-11-18` | 3 | 7 | docs only |
| `audit/reconcile-research-branch-family-2026-11-18` | 6 | 8 | docs only |
| `audit/reconcile-selected-historical-branch-content-2026-11-17` | 6 | 29 | docs only |
| `audit/refresh-branch-inventory-2026-11-17` | 3 | 30 | docs only |
| `audit/refresh-live-inventory-and-reconcile-pcgn-port-2026-11-18` | 3 | 10 | docs only |
| `audit/restore-pinned-khmer-phonemizer-smoke-2026-11-18` | 8 | 16 | workflow identical to main; docs differ |

### Content disposition

- 19 branches have changed-file lists containing only the three canonical audit/handoff documents: `docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md`, `docs/audits/current/LINGUISTIC-COMPLETION-REGISTER-2026-11-01.md`, and `docs/repository-audit.md`. They are historical audit snapshots, not code/data contributions; no wholesale merge is appropriate.
- `audit/complete-remaining-branch-families-2026-11-17` is fully behind with zero changed files relative to current main.
- The remaining branch `audit/restore-pinned-khmer-phonemizer-smoke-2026-11-18` also changes `docs/benchmarking-and-external-ipa.md` and `.github/workflows/optional-khmerphonemizer-smoke.yml`; the workflow file was fetched from both refs and is byte-identical (1,372 bytes). Its only workflow delta is historical ancestry, not current content. Benchmark documentation differs only by accumulated historical smoke evidence; no executable workflow improvement is missing from main.
- Thus, this family audit identifies no unported executable or data artifact. Historical branches remain preserved. No changes to runtime, IPA, Ukrainian output, corpus, licensing, benchmark scores or gold labels are warranted.

**Audit-family disposition: reviewed at compare/file-list level; semantic content review limited to the non-identical benchmark documentation and exact workflow blob comparison.** Repository-wide `KHM-BRANCH-AUDIT-001` remains PARTIAL because full semantic review and PR-ancestry reconciliation across every branch family are not complete. Issue #104 remains open; independent adjudicated IPA gold = 0 and empirical accuracy = null. No local checkout or local tests are claimed; this pass used GitHub-hosted repository/compare data only.


## Fix and release branch-family reconciliation — 2026-11-18

Compared all **15 `fix/*` refs and the single `release/*` ref** against current main `b2ce7c0b436cf3cdbbe3665ce702b9272e38948a`. All 16 refs diverge; ahead range 2–56, behind range 4–536. No branch was merged wholesale.

| Branch | Ahead | Behind | Content disposition |
|---|---:|---:|---|
| `fix/explicit-ipa-kind-in-phonetic-result-2026-11-17` | 9 | 55 | Historical divergent snapshot; see focused evidence below |
| `fix/flag-unconverted-khmer-romanizer-output-2026-11-15` | 2 | 192 | Historical divergent snapshot; see focused evidence below |
| `fix/khmer-benchmark-reproducibility-2026-10-24` | 3 | 529 | Historical divergent snapshot; see focused evidence below |
| `fix/khmer-orthographic-parser-diagnostics-v2-2026-11-16` | 17 | 78 | Historical divergent snapshot; see focused evidence below |
| `fix/khmer-orthographic-parser-evidence-2026-11-16` | 7 | 79 | Historical divergent snapshot; see focused evidence below |
| `fix/khmer-orthographic-parser-rejection-spans-2026-11-16` | 16 | 77 | Historical divergent snapshot; see focused evidence below |
| `fix/khmer-rejected-span-reasons-and-fixtures-2026-11-16` | 2 | 76 | Historical divergent snapshot; see focused evidence below |
| `fix/khmer-typed-partial-phonetic-results-2026-11-16` | 56 | 98 | Historical divergent snapshot; see focused evidence below |
| `fix/khmer-unmodeled-letter-trace-2026-11-12` | 3 | 239 | Historical divergent snapshot; see focused evidence below |
| `fix/mixed-script-numeral-token-boundaries-2026-11-17` | 32 | 51 | Historical divergent snapshot; see focused evidence below |
| `fix/mixed-script-romanization-guard-2026-11-15` | 10 | 199 | Historical divergent snapshot; see focused evidence below |
| `fix/pcgn-final-consonant-context-types-2026-11-16` | 2 | 138 | Historical divergent snapshot; see focused evidence below |
| `fix/pcgn-shortened-vowel-diacritic-inventory-2026-11-15` | 11 | 189 | Historical divergent snapshot; see focused evidence below |
| `fix/reconcile-unicode-tn61-source-metadata-2026-11-18` | 5 | 4 | Historical divergent snapshot; see focused evidence below |
| `fix/serve-coverage-report-on-pages-2026-10-21` | 6 | 536 | Historical divergent snapshot; see focused evidence below |
| `release/deterministic-rule-engine-2026-11-11` | 15 | 253 | Historical divergent snapshot; see focused evidence below |

### Focused content-level checks

- `fix/flag-unconverted-khmer-romanizer-output`: the executable `src/khmer-romanization-ukrainian.js` is byte-identical to main (4,438 bytes). Its test file is an older snapshot (12,554 vs 13,109 bytes); no runtime port indicated.
- `fix/khmer-benchmark-reproducibility`: its benchmark script (5,842 bytes) and workflow (1,152 bytes) are older than main (10,704 and 1,443 bytes). Preserve main's current harness/workflow; the historical version does not add a missing capability.
- Parser branches: `fix/khmer-orthographic-parser-diagnostics-v2`, `fix/khmer-orthographic-parser-evidence`, `fix/khmer-orthographic-parser-rejection-spans`, and `fix/khmer-rejected-span-reasons-and-fixtures` carry older `orthographic_syllables.py` snapshots (10,986–12,692 bytes vs main 12,711) and older JS/tests; no wholesale port. Their feature areas are represented by the later mainline parser and regression suite.
- `fix/khmer-unmodeled-letter-trace`: `data/khmer/signs.json` is byte-identical to main (4,668 bytes); its `parser.py` is an older 7,014-byte snapshot vs main 10,689 bytes.
- `fix/khmer-typed-partial-phonetic-results`: branch `phonetic_result.py` (1,607 bytes) and `rule_engine.py` (15,587 bytes) are older than main (1,797 and 16,220); current typed partial result behavior is more developed. No branch implementation port.
- `fix/mixed-script-romanization-guard`: branch renderer is an older 4,326-byte snapshot vs main 4,438. `fix/mixed-script-numeral-token-boundaries` contains an older cross-cutting parser/rule-engine implementation; current main has subsequent integration and tests. Do not replace current files with these snapshots.
- `fix/pcgn-final-consonant-context-types`: its PCGN module is an older 65,380-byte snapshot vs main 124,740; its targeted final-consonant test is byte-identical to main (4,953 bytes). No port.
- `fix/pcgn-shortened-vowel-diacritic-inventory`: the data CSV is byte-identical to main (5,255 bytes); the associated implementation/test snapshots are older.
- `fix/reconcile-unicode-tn61-source-metadata`: both `data/khmer/sources.json` and `tests/test_rule_registry_provenance.py` are byte-identical to main (67,497 and 6,167 bytes); the canonical metadata update is already integrated.
- `fix/serve-coverage-report-on-pages`: `scripts/coverage.py` and `public/reports/khmer-coverage-audit.json` are byte-identical to main (9,665 and 12,579 bytes). No deployment or report artifact is missing.
- The release branch is a substantially older rule-engine/runtime snapshot and is not a release candidate; main's current deterministic engine supersedes it.

**Disposition:** focused content checks found no missing implementation requiring port. The exact current main remains authoritative; all historical branches are preserved. This pass is compare-complete for the 16 refs, with selected critical-file blob checks, not a full semantic review of every changed line or PR ancestry. `KHM-BRANCH-AUDIT-001` remains PARTIAL. Issue #104 remains the human-evidence blocker; independent adjudicated IPA gold = 0 and empirical accuracy = null. No runtime, IPA, Ukrainian mapping, corpus, rights or benchmark values changed. No local checkout/tests are claimed; GitHub compare and file-content checks only.


### PR ancestry cross-check for the fix/release family

Queried GitHub's all-state pull-request list by exact head branch for all 16 refs. Each ref has a corresponding PR; 13 PRs are merged, while parser-rejection PRs #288, #289 and #292 are closed unmerged as superseded/duplicate work. Their functional lineage is preserved by merged PR #293, which follows merged PR #291 and ports the remaining rejected-span reason/fixture details onto the latest packed parser. Specifically: #288 was superseded after main preserved both BNF S-production role assignments; #289 was superseded by #292 on a newer packed-parser base; #292 was closed after main independently merged the diagnostics and #293 carried the distinct reason/fixture refinements. No unmerged PR contained a unique surviving implementation absent from main in the checked paths.

PR mapping: #312 explicit IPA kind; #201 unconverted romanizer guard; #9 benchmark reproducibility; #289/#288/#292 rejected-span/parser work (closed unmerged); #293 merged rejection-reason and Unicode fixture continuation; #280 typed partial results; #159 unmodeled-letter trace; #316 mixed-script numeral boundaries; #194 mixed-script romanization guard; #255 PCGN final consonant context; #204 shortened-vowel inventory; #365 TN #61 source metadata; #2 Pages coverage report; #152 deterministic rule engine.


## Benchmark and CI branch-family reconciliation — 2026-11-18

Compared both remaining specialized workflow refs with current main `190b9c3f1096282f9dc0289c55e8731cbcf7e85d`.

| Branch | Ahead | Behind | PR ancestry | Disposition |
|---|---:|---:|---|---|
| `benchmark/current-engine-2026-11-11` | 1 | 243 | No PR found for exact head branch | DEFERRED; do not merge workflow until external dataset rights and provenance are established |
| `ci/khmer-g2p-smoke-2026-10-24` | 2 | 531 | PR #8 merged 2026-10-24 | Superseded by current pinned/manual workflows; no old workflow restoration |

### Evidence and scope

- The benchmark branch contains a unique 6,006-byte `.github/workflows/benchmark-current-engine.yml` absent from main. It checks out MekongPhon and `neurlang/dataset` at pinned commits, then compares the deterministic engine with source-reported IPA from both cohorts. Its own output labels comparisons `SOURCE_ATTESTED_CONCORDANCE_NOT_GOLD`, but the workflow does not resolve item-level rights/provenance for the Neurlang lexicon or provide independent adjudication. It therefore remains DEFERRED; no model score, accuracy or gold claim is accepted. The branch is preserved.
- The CI branch's 1,145-byte `optional-khmer-g2p-benchmark.yml` is the old unpinned `khmerphonemizer` workflow (actions v4, unpinned package). Main's 1,443-byte workflow is now manual-dispatch-only and runs the pinned MekongPhon diagnostic; a separate `optional-khmerphonemizer-smoke.yml` provides the pinned `khmerphonemizer==0.0.3` raw-output smoke with artifact integrity reporting. PR #8's old workflow is therefore superseded, not restored.
- PR #370's fix/release audit and PR #369's audit-family closeout are merged before this checkpoint. All 240 pre-existing branch refs remain preserved; no benchmark branch was executed in this pass.

**Benchmark/CI family disposition:** compare and ancestry checks complete for both refs. The benchmark workflow is explicitly DEFERRED pending rights/provenance; the CI workflow is superseded by current pinned workflows. Repository-wide `KHM-BRANCH-AUDIT-001` remains PARTIAL until remaining all-family PR ancestry and semantic content review are complete. Issue #104 remains open; independent adjudicated IPA gold = 0; empirical accuracy = null. No runtime, IPA, Ukrainian output, corpus, benchmark values or rights decisions changed. No local checkout or local tests are claimed.


## Late documentation-branch additions — 2026-11-18

The earlier documentation-family pass recorded 103 `docs/*` tips. A fresh live inventory now contains 106. Reconciled the three later closeout branches against current main `42dd0cbddf6fce29ddfdc8d8161b830597183a23` and cross-checked a fourth recent documentation branch for its PR ancestry:

| Branch | Ahead | Behind | PR | Disposition |
|---|---:|---:|---:|---|
| `docs/closeout-tn61-source-registry-and-docs-branch-audit-2026-11-18` | 3 | 6 | #366 merged | Historical three-document closeout; represented on main |
| `docs/pr366-postmerge-closeout-2026-11-18` | 3 | 5 | #367 merged | Historical three-document closeout; represented on main |
| `docs/pr367-final-mainline-closeout-2026-11-18` | 3 | 4 | #368 merged | Historical three-document closeout; represented on main |
| `docs/ipa-gold-recruitment-execution-kit-2026-11-18` | 4 | 17 | #355 merged | Recruitment templates and protocol documentation already merged; no outreach or recruitment is implied |

Each changed-file list contains only the canonical handoff, linguistic completion register, repository audit and, for the recruitment-kit branch, the IPA collection playbook. These are merged documentation snapshots; no additional implementation or evidence payload was found to port. This reconciles the three-ref difference between the previous 103-ref docs-family checkpoint and the current 106-ref inventory. No historical ref was changed or deleted.

Documentation family: **106/106 refs now have a recorded compare/content disposition** (103 from the earlier full pass plus these three later closeout refs); the additional recruitment-kit branch was separately verified against PR #355. This is branch-tip and changed-file review, not a claim that every sentence in every historical handoff has been re-adjudicated. The repository-wide audit remains PARTIAL pending complete semantic review and PR ancestry across all remaining families.


## Feature branch current-base and PR-ancestry reconciliation — 2026-11-18

Refreshed the `feat/*` inventory (50 refs) and compared **all 50 branch tips** against exact current main `e0a9c0b9e195e9c0225f1cbfa1b9f3a38fab3221`. Every ref diverges; ahead range 2–60 commits and behind range 30–541. This refreshes the earlier family comparison against an older base; it does not imply that every changed line was re-reviewed in this pass.

Queried all-state PRs by exact head branch for all 50 feature refs:
- **44 branches map to merged PRs**: #1, #5, #7, #156, #161, #164, #182, #185, #192, #213, #215, #217, #224, #226, #228, #230, #233, #235, #237, #239, #241, #243, #245, #247, #249, #250, #252, #254, #264, #265, #266, #267, #269, #271, #273, #275, #281, #282, #283, #285, #287, #290, #291, #351.
- **Three branches map to closed unmerged/superseded PRs**: #154 and #155 were successive drafts superseded by final merged PR #156; #286 was a redundant BNF parse-forest prototype after main independently received the canonical parser, with subsequent grammar-role ambiguity work merged as #287.
- **Three branches have no PR for their exact head branch**: `feat/github-pages-hybrid-candidate-shell-2026-11-15`, `feat/khmer-orthographic-bnf-parser-2026-11-16`, and `feat/pcgn-anusvara-visarga-syllable-assembly-2026-11-16`. The browser hybrid candidate remains explicitly deferred pending a current-entrypoint browser contract; the BNF parser branch is superseded by merged canonical parser work (#285/#287); the distinct PCGN anusvara/visarga assembler was ported with a complete typed/schema/test contract by PR #351, without merging the stale branch snapshot.

This completes the current-base compare and exact-head PR lookup for the 50 feature refs. Existing content-level dispositions remain: current PCGN source declarations are represented in main; the one browser-side hybrid candidate is retained for future review but not adopted; old branch snapshots are not wholesale-merged. No historical branch was deleted or force-updated. No new runtime, phonological rule, IPA, Ukrainian output, corpus row or accuracy result was introduced by this audit.

**Feature family: compare + PR ancestry DONE_VERIFIED; full semantic line-by-line review of all 50 changed-file sets remains PARTIAL.** Repository-wide `KHM-BRANCH-AUDIT-001` remains PARTIAL. Issue #104 remains the independent human-evidence blocker; adjudicated gold = 0 and empirical accuracy = null. No local checkout or local tests are claimed; GitHub compare and PR APIs were used.


## Test branch current-base and PR-ancestry reconciliation — 2026-11-18

Compared all **10 `test/*` refs** against exact current main `ef29315fff75e7829105a84922fc82bd71733e2d`; all diverge, ahead range 1–16 and behind range 47–537. Queried all-state PRs by exact head branch: **all ten map to merged PRs**, with no open or closed-unmerged test-only PR branches.

| Test branch | Ahead | Behind | Merged PR |
|---|---:|---:|---:|
| `test/complete-grapheme-accounting-2026-11-12` | 3 | 246 | #157 |
| `test/ipa-display-contract-2026-10-24` | 1 | 537 | #6 |
| `test/khmer-numeral-crosswalk-runtime-2026-11-12` | 6 | 229 | #174 |
| `test/khmer-onset-fallback-cross-runtime-fixture-2026-11-17` | 16 | 47 | #326 |
| `test/khmer-romanization-adapter-coverage-2026-11-12` | 2 | 237 | #167 |
| `test/khmer-romanization-canonical-matrix-parity-2026-11-12` | 4 | 233 | #170 |
| `test/khmer-romanization-whole-message-adapter-2026-11-12` | 4 | 231 | #172 |
| `test/khmer-vowel-ascii-alias-coverage-2026-11-12` | 2 | 227 | #176 |
| `test/khmer-vowel-matrix-runtime-crosswalk-2026-11-12` | 1 | 226 | #177 |
| `test/ui-accessibility-smoke-2026-11-15` | 2 | 201 | #197 |

Existing content-level review remains applicable: these branches contain earlier snapshots of tests and fixtures already integrated and expanded on main; no missing assertion/fixture was identified for port. The current test suite is newer than the branch snapshots. No test branch was deleted, force-updated or merged wholesale.

**Test family: current-base compare and PR ancestry DONE_VERIFIED; full semantic re-review of every historical test line remains PARTIAL.** No runtime, linguistic rules, IPA, Ukrainian output, corpus, gold labels or accuracy values changed. No local checkout or local tests are claimed.


## Research branch current-base and PR-ancestry reconciliation — 2026-11-18

All **29 `research/*` refs** were refreshed and compared against exact main `ef29315fff75e7829105a84922fc82bd71733e2d` (the base immediately preceding the current documentation-only PR #374). Every branch diverges; ahead range 1–91, behind range 17–539. The compare/file-list inventory was performed for every ref.

| Research branch | Ahead | Behind |
|---|---:|---:|
| `research/bgn-pcgn-ungegn-rule-diff` | 5 | 189 |
| `research/complete-external-g2p-registry` | 6 | 210 |
| `research/expert-shortlist-revalidation` | 5 | 54 |
| `research/external-ipa-renderers` | 7 | 539 |
| `research/google-khmer-lexicon-full-audit` | 21 | 77 |
| `research/khmer-acoustic-model-release-audit` | 26 | 76 |
| `research/khmer-engine-benchmark-expansion` | 72 | 258 |
| `research/khmer-hybrid-benchmarks-reconciled` | 34 | 247 |
| `research/khmer-hybrid-engine` | 91 | 258 |
| `research/khmer-ipa-convention-draft` | 5 | 76 |
| `research/khmer-ipa-convention-draft-v2` | 7 | 75 |
| `research/khmer-kirby-cluster-audio-audit` | 9 | 69 |
| `research/khmer-kirby-tonogenesis-audio-audit` | 26 | 64 |
| `research/khmer-lexical-segmentation-evidence` | 4 | 51 |
| `research/khmer-lexical-segmentation-evidence-mainline` | 2 | 37 |
| `research/khmer-phonotactic-scope` | 9 | 208 |
| `research/khmer-source-audit-integration` | 7 | 71 |
| `research/khmer-unicode-syllable-grammar` | 1 | 86 |
| `research/loc-khmer-word-division` | 6 | 105 |
| `research/mekongphon-diagnostic-harness` | 11 | 216 |
| `research/mekongphon-release-rights-audit` | 10 | 76 |
| `research/mekongphon-seed-lexicon-audit` | 34 | 77 |
| `research/pcgn-note-registry` | 6 | 187 |
| `research/phon-sobon-and-lexicon-triage` | 11 | 211 |
| `research/phonetic-literature-fulltext-review` | 6 | 58 |
| `research/pin-khmer-acoustic-dictionary-artifact-audit` | 6 | 17 |
| `research/sok-adams-khmer-phonology-audit` | 7 | 61 |
| `research/sok-adams-rule-transfer-audit` | 5 | 49 |
| `research/ungegn-engine-candidate-review` | 5 | 190 |

### Exact-head PR ancestry

Queried all-state PRs by exact head branch for all 29 refs:
- **21 merged PRs:** #4, #184, #187, #188, #190, #208, #209, #211, #278, #284, #300, #306, #307, #309, #310, #311, #314, #319, #322, #324, #357.
- **Seven closed unmerged/superseded PRs:** #150, #151, #153, #301, #303, #304, #305. Their outcomes are not treated as merged code: model-consensus/hybrid candidates were replaced by deterministic rules (#152); the IPA convention v1 draft was superseded by v2 (#306); MekongPhon and acoustic-model rights/provenance findings were carried into later source-audit records and Issue #104; the open-dict Khmer lexicon audit remains represented as a non-commercial external comparator in the current source registry and playbook. No source dataset or gold row was imported.
- **One research branch has no PR:** `research/khmer-lexical-segmentation-evidence-mainline-2026-11-17`; its compare against the base reports zero changed files, so it is an ancestry-free branch tip with no unique content delta.

### Disposition and evidence boundary

The 29 branch compare results and PR mappings are now explicit. Existing content-level findings remain: external IPA renderers and diagnostic harnesses are not gold; MekongPhon and the Khmer Acoustic Model remain rights/profile limited; PCGN note registry snapshots are older than main; IPA convention remains draft; lexical segmentation remains evidence-limited. The benchmark/hybrid branches do not authorize model voting or promotion of source-attested output. All historical refs are preserved.

**Research family: current-base compare and PR ancestry DONE_VERIFIED.** This is not a full semantic adjudication of every changed line in every research document/data file; repository-wide `KHM-BRANCH-AUDIT-001` remains PARTIAL for that reason and for other remaining families. Issue #104 remains open; no expert has been contacted or recruited, approved convention remains absent, adjudicated gold = 0 and empirical accuracy = null. No external data, runtime rules, IPA, Ukrainian output or corpus labels changed. No local checkout or local tests are claimed.


## Data branch current-base and PR-ancestry reconciliation — 2026-11-18

Compared all **four \`data/*\` refs** against exact current main \`bce05e599e3202410a1c49ff4a88ec58ae49c06b\` and queried PR ancestry by exact head branch.

| Data branch | Ahead | Behind | PR ancestry | Disposition |
|---|---:|---:|---|---|
| \`data/integrate-positional-onset-evidence-register-2026-11-17\` | 0 | 37 | No PR; zero changed files | Behind-only duplicate tip; no unique content |
| \`data/khmer-onset-evidence-registry-2026-11-17\` | 10 | 46 | #329 merged | Provisional evidence registry/schema/tests are integrated; entries remain explicitly unadjudicated |
| \`data/pcgn-independent-vowel-source-register-2026-11-16\` | 12 | 143 | #258 closed superseded by #259 | Source register/tests carried forward by clean continuation |
| \`data/pcgn-independent-vowel-source-register-mainline-2026-11-16\` | 6 | 142 | #259 merged | CSV register is byte-identical to main; no port |

PR #258 was closed only to avoid stale-base documentation conflict after PR #257; PR #259 preserved the source register and parity tests, while leaving unresolved \`ឧ\` romanization alternatives \`ŏ\`/\`ŭ\` explicitly undecided. PR #329 added the positional onset evidence registry as a specialist-reference container only; its records remain \`NOT_INDEPENDENTLY_REVIEWED\` and \`NOT_ADJUDICATED_FOR_PROJECT_PPH_PROFILE\`. These data registries are not primary phonetic evidence or IPA gold and do not authorize new pronunciation mappings.

**Data family: current-base compare and PR ancestry DONE_VERIFIED.** No data rows, IPA labels, runtime mappings, or gold records were added in this audit. All historical refs are preserved. Repository-wide \`KHM-BRANCH-AUDIT-001\` remains PARTIAL pending full semantic line review and remaining ancestry work. Issue #104 remains open; adjudicated gold = 0; accuracy = null. No local checkout or local tests are claimed.


## Audit branch PR-ancestry closeout — 2026-11-18

Queried all-state PRs by exact head branch for the 20 pre-existing `audit/*` refs covered by the compare/content pass in PR #369. Results:

- **18 refs map to merged PRs:** #180, #261, #338, #339, #341, #342, #343, #344, #345, #346, #347, #348, #349, #350, #353, #359, #361, #362, #363.
- **One ref has a closed unmerged continuation PR:** `audit/reconcile-selected-historical-branch-content-2026-11-17` maps to merged PR #339 and superseded PR #340. PR #340's body states it was closed due to squash-merge ancestry conflict after #339; its final branch-count/verification note was reapplied on a fresh mainline branch. No content is treated as lost or as merged through #340.
- **One ref has no PR:** `audit/complete-remaining-branch-families-2026-11-17`; the compare against current main reported zero changed files and the branch is behind-only.

This completes exact-head PR ancestry mapping for the 20 historical audit branches. Their substantive changed paths remain documentation-only (with the separately verified pinned Khmer Phonemizer workflow byte-identical to main), as recorded in PR #369. The newer audit branches created for the ongoing closeout are handled by their own PRs (#369–#377) and are not part of this 20-ref historical cohort.

**Audit family: compare/content disposition and PR ancestry DONE_VERIFIED for the 20 historical refs.** Repository-wide `KHM-BRANCH-AUDIT-001` remains PARTIAL because complete semantic line review of every historical document and remaining family refs is not complete. No branches were deleted/force-updated. No runtime, linguistic rules, IPA, Ukrainian output, corpus, gold labels or benchmark scores changed. Issue #104 remains open; independent gold=0, accuracy=null.


## Documentation branch PR-ancestry closeout — 2026-11-18

Queried all-state PRs for the full live `docs/*` family: **106 refs**. Results:
- **101 refs have at least one exact-head PR**; **97 refs map only to merged PRs**.
- **Four refs have closed unmerged/superseded PRs:**
  - `docs/closeout-mixed-script-boundaries-2026-11-17` → PR #318, duplicate of merged PR #317's mixed-script verification closeout.
  - `docs/fix-exact-main-quality-count-2026-11-16` → PR #298, no-op duplicate; correction already represented by PR #299 / final checkpoint PR #296.
  - `docs/khmer-unicode18-parser-final-handoff-2026-11-16` → PR #295, duplicate source-registry update superseded by PR #294 to avoid a duplicate TN #61 source ID.
  - `docs/post-pr294-mainline-verification-2026-11-16` → PR #297, stale verification checkpoint superseded by PR #296, which records exact-main Quality, Chromium and Pages success.
- **Five refs have no PR for their exact head branch:** `docs/khmer-parser-final-state-2026-11-16`, `docs/khmer-parser-final-state-v2-2026-11-16`, `docs/khmer-parser-source-registry-and-handoff-2026-11-16`, `docs/khmer-short-vowel-sequence-test-closeout-2026-11-12`, and `docs/post-pr223-mainline-verification-2026-11-15`. Their changed paths are documentation/audit snapshots or an older source-registry/test snapshot. The registry branch has 46 source entries vs main's 49 and no branch-only source IDs; no missing source or test implementation was identified.

Together with the prior 103-ref family compare and the three later closeout comparisons (PR #372), all **106 docs refs** now have compare/content dispositions; this pass resolves PR ancestry for all 106. The four unmerged PRs are explicitly superseded, not counted as completed merges. Five no-PR refs remain preserved as historical refs with no unique executable contribution.

**Documentation family: branch-tip compare/content disposition and PR ancestry DONE_VERIFIED.** This does not claim a sentence-by-sentence re-adjudication of every historical handoff. No historical branch was deleted/force-updated. No runtime, phonological rule, IPA, Ukrainian output, source rights, corpus, gold labels or accuracy values changed. No expert outreach/recruitment is implied; Issue #104 remains open, independent adjudicated gold=0 and empirical accuracy=null. Repository-wide `KHM-BRANCH-AUDIT-001` remains PARTIAL pending final all-family semantic review.


## PR #378 final mainline closeout — 2026-11-18

PR [#378](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/378) merged into `main` as `35b9379d53f18f45992da8f488982c6fdb3e0a16`.

Exact PR-head checks on `2ffe18c983707bb1f009d5261fa5ee4714b2d0ed` completed SUCCESS: Quality [44298834063](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44298834063) and Chromium [44298834170](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44298834170). Post-merge mainline Quality [44299017800](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44299017800) and Chromium [44299017849](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44299017849) completed SUCCESS. Pages deployment [44299017965](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44299017965) was still PENDING at this closeout; do not mark it as passed until GitHub reports completion.

Live GitHub branch inventory immediately after PR #378 merge: **250 refs / 250 unique tip SHAs**. Prefix counts: a11y 2, audit 30, benchmark 1, ci 1, data 4, docs 106, feat 50, fix 15, main 1, release 1, research 29, test 10. Open PRs: 0. Open non-PR issue: #104 only.

### One-pass branch-family ledger

- Current-base compare and PR ancestry are documented for a11y (2), benchmark/CI (2), data (4), docs (106), feature (50), fix/release (16), research (29), test (10), and the 20 historical audit refs. Newly created audit/closeout branches each have their own merged or open PR record.
- The Neurlang/MekongPhon engine benchmark remains DEFERRED pending rights and item-level provenance; the browser-side hybrid candidate remains deferred pending a current browser contract. Historical branches are preserved; no force-push/deletion or wholesale stale-branch merge occurred.
- Repository-wide `KHM-BRANCH-AUDIT-001` remains PARTIAL: branch tips and PR ancestry have broad coverage, but not every changed line across all historical docs/data/code snapshots has undergone full semantic re-adjudication.
- Issue #104 remains the external human-evidence blocker: IPA convention is not approved, no experts were contacted/recruited, independent adjudicated gold remains 0, and empirical accuracy remains null. Root license selection remains an owner decision. Accessibility manual screen-reader/keyboard/device checks remain outstanding.

No runtime, phonological rules, IPA labels, Ukrainian mappings, source data, corpus rows, gold labels or benchmark scores changed in PRs #369–#378. No local checkout or local test run is claimed; verification is from GitHub Actions.

**Repository status:** research-ready partial prototype; not linguistically release-ready.


## PR #379 post-merge and live branch inventory closeout — 2026-11-18

PR [#379](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/379) merged as `04de0609ec490b09e1e44ec948bbe6ded5f59d4a`. Its exact head was `c76d8e5f54115832cca3d392e5342486ec0f18b2`, based on `35b9379d53f18f45992da8f488982c6fdb3e0a16`; the three-commit branch changed only the canonical handoff, linguistic completion register and repository audit. The branch is retained as the 107th live `docs/*` ref.

Post-merge workflows on exact `main` SHA `04de0609ec490b09e1e44ec948bbe6ded5f59d4a` are now all **SUCCESS**:
- Quality checks: [44299543935](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44299543935).
- Chromium browser smoke: [44299543875](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44299543875).
- GitHub Pages build, deploy and deployed-site asset smoke: [44299543884](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44299543884). This resolves the earlier PR #378 checkpoint's pending Pages status; that earlier pending state is historical, not current.

Refreshed live branch inventory after PR #379: **251 refs / 251 unique tip SHAs**. Prefix counts: a11y 2, audit 30, benchmark 1, ci 1, data 4, docs 107, feat 50, fix 15, main 1, release 1, research 29, test 10. Open PRs: 0. Open non-PR issue: #104 only.

### Documentation-family ancestry addendum

The new `docs/pr378-final-mainline-closeout-2026-11-18` branch maps to merged PR #379 (exact head `c76d8e5f54115832cca3d392e5342486ec0f18b2`; base `35b9379d53f18f45992da8f488982c6fdb3e0a16`). Its compare is 3 commits ahead / 0 behind and contains only the three canonical documentation files. Adding it to the prior 106-ref disposition yields **107/107 docs refs reconciled**: 102 with exact-head PRs (98 merged-only; four closed unmerged/superseded) and five with no exact-head PR. No implementation or evidence was missing from this branch.

The two retained a11y branches are not port candidates: PR #331's skip-navigation behavior and tests are present on current main, while its branch is an older snapshot; PR #333's WCAG contrast changes/tests are integrated, and its branch files were recorded as byte-identical to main in PR #363. Current main retains both skip links and representative WCAG AA contrast assertions. This is automated coverage only, not a completed manual accessibility audit.

### Status ledger refresh

- Documentation branch compare/content disposition and exact-head PR ancestry (107 refs): **DONE_VERIFIED**.
- Current-main Quality, Chromium and Pages workflows on `04de0609`: **DONE_VERIFIED** for the checks actually executed by those workflows.
- `KHM-BRANCH-AUDIT-001` full semantic line-by-line review of all historical changed content: **PARTIAL**; ancestry/file disposition does not equal semantic re-adjudication of every historical line.
- `KHM-UI-001` manual accessibility review: **PARTIAL**; screen-reader/assistive-technology review, complete keyboard traversal, comprehensive text/non-text contrast, zoom/reflow and real-device/mobile checks remain outstanding.
- `KHM-GOLD-001` / Issue #104: **BLOCKED**; approved IPA convention, two qualified independent annotators, separate adjudicator, non-annotating curator, private blind intake, rights-cleared 30 lexeme groups and adjudication remain absent. Independent adjudicated gold = 0; empirical accuracy = null.
- Root repository license selection: **BLOCKED (owner decision)**; do not infer permission or add a root license without owner confirmation.
- Neurlang/MekongPhon benchmark integration: **DEFERRED** pending item-level rights/provenance and a valid independent evaluation set.

No runtime, phonological rule, IPA label, Ukrainian mapping, source data, corpus row, gold label or benchmark score changed in PR #379 or this closeout. No historical branch was deleted or force-updated. No local checkout or local tests were run; verification above is from exact-main GitHub Actions runs.
 
**Repository status remains research-ready partial prototype; not linguistically validated or release-ready.**


## PR #380 merge and exact-main verification — 2026-11-18

PR [#380](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/380) merged by squash as `c149f5eb792c6fbb16c1b52b198809c83b4b4bf6`. Its exact PR head was `463635f4e71cef47f780b77d236b5c273be1fe9d`; the three-file change updated only the canonical handoff, repository audit and linguistic completion register. No runtime or linguistic implementation changed.

Exact PR-head verification:
- Quality [44302844364](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44302844364) — SUCCESS; IPA corpus structure validation, Python test suite, Node web checks and Vite production build all completed successfully.
- Chromium [44302844370](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44302844370) — SUCCESS; deterministic web checks, production build and production Chromium smoke completed successfully.

Post-merge verification on exact `main` SHA `c149f5eb792c6fbb16c1b52b198809c83b4b4bf6`:
- Quality [44303007846](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44303007846) — SUCCESS.
- Chromium [44303007883](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44303007883) — SUCCESS.
- GitHub Pages [44303007825](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44303007825) — SUCCESS, including production build, browser exercise, Pages artifact upload/deploy and deployed-site runtime-asset smoke test.

Live branch inventory immediately after PR #380 merge and before this follow-up documentation branch was created: **252 refs / 252 unique tip SHAs**. Prefix counts: a11y 2, audit 31, benchmark 1, ci 1, data 4, docs 107, feat 50, fix 15, main 1, release 1, research 29, test 10. At that snapshot there were **0 open PRs** and Issue #104 was the only open non-PR issue. The 107 documentation refs remain fully reconciled; the new follow-up branch is a separate documentation-only closeout and does not change the 107-ref historical cohort being recorded here.

No local checkout or local test execution is claimed. All test evidence above is from exact PR-head and exact post-merge GitHub Actions runs. The repository remains a research-ready partial prototype, not a linguistically validated release: independent adjudicated IPA gold remains 0 and empirical accuracy remains null; manual accessibility, root-license owner decision and full historical semantic re-adjudication remain open.


## PR #381 and post-merge verification — 2026-11-18

PR [#381](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/381) merged by squash as `06250a7d2c7f0c90487fd519e173538f00d45314`. Exact PR head: `f1bfa4410effb4dfbc8ad0486015dc26e750abd1`. The change records PR #380's final exact-main checks and is documentation-only across the three canonical records.

PR-head CI:
- Quality [44303308051](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44303308051) — SUCCESS: independent IPA gold corpus structural validation, Python tests, Node web checks and production build.
- Chromium [44303307840](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44303307840) — SUCCESS: deterministic web checks, production build and visible-results Chromium smoke.

Post-merge CI on exact `main` SHA `06250a7d2c7f0c90487fd519e173538f00d45314`:
- Quality [44303520032](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44303520032) — SUCCESS.
- Chromium [44303520568](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44303520568) — SUCCESS.
- GitHub Pages [44303520067](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44303520067) — SUCCESS, including production build, Chromium exercise, artifact upload/deployment and deployed-site smoke.

Live branch inventory after PR #381 merge and before this addendum branch: **253 refs / 253 unique tip SHAs**. Prefix counts: a11y 2, audit 32, benchmark 1, ci 1, data 4, docs 107, feat 50, fix 15, main 1, release 1, research 29, test 10. Open PRs: 0. Open issue: #104 only. The 107-ref documentation ancestry cohort remains reconciled as previously recorded; this follow-up branch is an additional audit-family closeout.

Issue #104 was re-read in full. Its target profile remains decided (`khmer-pph-careful-citation-v1`), but all human-dependent acceptance items remain unchecked: approved versioned IPA convention; two independent annotators; separate adjudicator; non-annotating curator; private blind intake; 30 attested, source-located lexeme groups with coverage rationale and item-level rights; independently locked annotations; evidence-based adjudication; provenance/rights/duplicate/schema/blindness checks. Candidate Common Voice material is insufficient to establish the target profile or required coverage; MekongPhon and Khmer Acoustic Model remain candidate-only pending item-level rights/provenance and convention checks. No external resource was imported and no person was contacted or represented as recruited.

Updated task ledger:
- PR #381 documentation closeout and exact-main Quality/Chromium/Pages verification: **DONE_VERIFIED**.
- Automated code/data validation, Python tests, Node checks, production build, Chromium smoke and Pages deploy on exact main: **DONE_VERIFIED** for the stated workflow scope.
- Independent adjudicated IPA pilot / Issue #104: **BLOCKED** on expert recruitment, approved convention, independent roles, blind intake, source selection and rights evidence. Gold remains 0; accuracy remains null.
- Full historical semantic re-adjudication: **PARTIAL**; ancestry/file disposition is not line-by-line semantic review of every historical change.
- Manual accessibility: **PARTIAL**; automated contrast/skip-link coverage does not replace screen-reader, full keyboard, zoom/reflow and real-device checks.
- Root license: **BLOCKED** pending owner decision.
- External benchmark integration: **DEFERRED** pending rights/provenance and a valid independent evaluation set.

No phonological rules, IPA correspondences, Ukrainian mappings, corpus entries, gold labels, benchmark scores or runtime behavior changed. No historical branches were deleted or force-updated. No local checkout or local tests were run; all test evidence is hosted GitHub Actions on exact commits. Repository status remains **research-ready partial prototype**, not linguistically validated or release-ready.


## Final session closeout after PR #382 — 2026-11-18

PR [#382](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/382) merged by squash as **`f4ad2ddf37579273e5a5bf5f68503a9986e0c812`**. PR-head Quality [44304006397](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44304006397) and Chromium [44304006183](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44304006183) both SUCCESS. Exact-main post-merge Quality [44304178800](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44304178800), Chromium [44304178779](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44304178779) and Pages deployment plus deployed-site asset smoke [44304178824](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44304178824) all SUCCESS.

Final verified main commit for this session: `f4ad2ddf37579273e5a5bf5f68503a9986e0c812`. Live branch snapshot after PR #382: **254 refs / 254 unique tip SHAs**, prefix counts: a11y 2, audit 33, benchmark 1, ci 1, data 4, docs 107, feat 50, fix 15, main 1, release 1, research 29, test 10. Open PRs: 0. Open issue: #104 only.

Session outcomes: PRs #380, #381 and #382 merged; all three canonical execution/audit/handoff records updated in place in each documentation batch; exact-main hosted Quality, Chromium and Pages checks verified SUCCESS. The branch inventory and issue acceptance criteria were refreshed. Historical refs were retained; no unrelated branch was deleted or force-updated.

Final task ledger: ancestry/file disposition remains DONE_VERIFIED for the previously reconciled branch cohorts; exact-main hosted engineering CI is DONE_VERIFIED for the listed checks; complete semantic review of every historical diff remains PARTIAL; manual accessibility remains PARTIAL; independent IPA gold pilot remains BLOCKED by missing expert roles, convention approval, blind intake, source/rights clearance and 30 verified lexical groups (gold 0, accuracy null); root license remains BLOCKED on owner decision; external benchmark integration remains DEFERRED pending rights/provenance and a valid independent evaluation set.

No runtime, phonological rules, IPA correspondences, Ukrainian mappings, source data, corpus rows, gold labels or benchmark scores were changed. No experts were contacted, no candidate datasets imported, and no local checkout/local tests were performed. All test results in this closeout are hosted GitHub Actions evidence. **Release status: research-ready partial prototype, not linguistically validated and not release-ready.**


## Engineering verification addendum — IPA tie-bar structure, 2026-11-18

- `KHM-IPA-BOUNDARY-001` — **DONE_VERIFIED (notation structure only)**. PR #384 requires both adjacent segment letters around U+0361/U+035C, rejects dangling/repeated/interrupted tie bars, and retains valid preceding segment diacritics. Regressions: `k͡`, `/k͡/`, `k͡ːa`, `k͡͡a` reject; `t̪͡s` remains accepted.
- PR [#384](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/384) merged as `70b381d41f00f89bb94c3694b1c6faa692bfe34d`. PR-head Quality [44315101232](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44315101232) and browser smoke [44315101225](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44315101225): SUCCESS. Exact-main Quality [44315276642](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44315276642), Chromium [44315276566](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44315276566), and Pages/deployed-site smoke [44315276557](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44315276557): SUCCESS.
- This validator checks notation structure and metadata only. It does not validate Khmer phonological correctness or create IPA gold labels. Independent adjudicated gold remains 0; empirical accuracy remains null.
- The PR #287 parse-forest and PR #185 typed-hybrid reviews were also completed in this continuation; their existing implementations were preserved without duplicate ports.


## PR #385 and exact-main verification — 2026-11-18

PR [#385](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/385) merged by squash as `56796f4f0facb161f2d659bfe8b8d7e9b27d9262`. Exact PR head: `b6ae553598275cb33ab3cd7aadf5a13c32a5e4a6`; base: `70b381d41f00f89bb94c3694b1c6faa692bfe34d`. The PR updates only the canonical handoff, linguistic completion register and repository audit to record the PR #384 tie-bar correction and semantic spot-checks; no runtime or linguistic data changed.

Exact PR-head checks on `b6ae553598275cb33ab3cd7aadf5a13c32a5e4a6`:
- Quality [44315782204](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44315782204) — SUCCESS.
- Khmer browser smoke [44315782121](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44315782121) — SUCCESS.

Exact post-merge mainline checks on `56796f4f0facb161f2d659bfe8b8d7e9b27d9262`:
- Quality [44315928573](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44315928573) — SUCCESS.
- Chromium [44315928755](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44315928755) — SUCCESS.
- GitHub Pages build/deploy and deployed-site runtime-asset smoke [44315928027](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44315928027) — SUCCESS; both build and deploy jobs completed successfully.

Live branch inventory after PR #385: **257 refs / 257 unique tip SHAs**. Prefix counts: a11y 2, audit 35, benchmark 1, ci 1, data 4, docs 107, feat 50, fix 16, main 1, release 1, research 29, test 10. Open PRs: 0. Open non-PR issue: #104 only.

Task ledger: PR #385 documentation closeout and exact-main Quality/Chromium/Pages checks — **DONE_VERIFIED**. The PR #384 tie-bar validator remains a notation/metadata structural check only. Independent adjudicated IPA gold remains 0 and empirical accuracy remains null; Issue #104 remains **BLOCKED** by the unapproved convention, missing independent annotators/adjudicator/curator, private blind intake and rights-cleared source packet. Manual accessibility and complete historical semantic re-adjudication remain **PARTIAL**; root license remains **BLOCKED** on owner decision; external benchmark integration remains **DEFERRED** pending rights/provenance and a valid independent evaluation set.

No local checkout or local tests were run. All verification above is from GitHub Actions on the exact PR head and exact merged main SHA. Repository status remains **research-ready partial prototype**, not linguistically validated or release-ready.


## PR #387 — expanded automated accessibility smoke and exact-main closeout — 2026-11-18

PR [#387](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/387) merged by squash as `61975c0c899d8c4b390204f69c08ef776b1e1da5`, with exact PR head `cd689943bfa130bd2993ab6d42ac0c0e1cc20bb4` and base `c16de68db26ef19fbaa02065bed7a3663bc46bfa`. The single-file test change adds (1) keyboard focus-indicator and Space activation coverage for the example/clear controls after results appear, and (2) document/body horizontal-overflow checks at 320, 375 and 420 CSS pixels on both the service and methodology pages.

Exact PR-head CI:
- Quality [44336489907](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44336489907) — SUCCESS.
- Khmer browser smoke [44336489862](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44336489862) — SUCCESS.

Exact post-merge main CI on `61975c0c899d8c4b390204f69c08ef776b1e1da5`:
- Quality [44336671094](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44336671094) — SUCCESS.
- Khmer browser smoke [44336671217](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44336671217) — SUCCESS.
- GitHub Pages build/deploy [44336671342](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44336671342) — SUCCESS; both build and deploy jobs completed successfully.

The new browser tests improve automated keyboard and narrow-screen regression coverage only. They do not establish full keyboard traversal, screen-reader/assistive-technology compatibility, 200%/400% zoom/reflow, complete contrast coverage, or real-device/mobile behavior. Manual accessibility task `KHM-UI-001` therefore remains **PARTIAL**.

Live branch inventory after PR #387: **259 refs / 259 unique tip SHAs**. Prefix counts: a11y 2, audit 36, benchmark 1, ci 1, data 4, docs 107, feat 50, fix 16, main 1, release 1, research 29, test 11. Open PRs: 0. Open non-PR issue: #104 only.

Task ledger: PR #387 automated keyboard/narrow-screen regression tests and exact-main Quality/Chromium/Pages checks — **DONE_VERIFIED**. Manual accessibility — **PARTIAL**. Full historical semantic re-adjudication — **PARTIAL**. Issue #104 independent IPA gold pilot — **BLOCKED**; approved convention, independent annotators/adjudicator/curator, private blind intake, rights-cleared 30-item packet and adjudication remain external human/evidence gates; gold = 0 and empirical accuracy = null. Root license — **BLOCKED** pending owner decision. External benchmark integration — **DEFERRED** pending rights/provenance and a valid independent evaluation set.

No production runtime, phonological rule, IPA label, Ukrainian mapping, corpus row, source-rights status or benchmark score changed. No local checkout or local test execution is claimed; verification is from exact PR-head and exact post-merge GitHub Actions runs. Repository status remains **research-ready partial prototype**, not linguistically validated or release-ready.


## PR #389 — accessibility landmark and accessible-name smoke — 2026-11-18

PR [#389](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/389) merged by squash as `21092c099e37e47a0f23031c49dc90387ecb464d`, with exact PR head `e9f7cf81a74ec6bd3732036a299a4d379774b4be` and base `c079eb94cf06778db19c165f5786f8b3c30ee433`. The single-file test change checks both public pages for `lang="uk"`, exactly one main landmark, exactly one H1, non-empty accessible-name sources for every button/input/select/textarea and link, and an `alt` attribute on every image. It also asserts the service navigation landmark and labeled textbox remain discoverable by role/name.

Exact PR-head verification:
- Quality [44339619652](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44339619652) — SUCCESS (full Python suite, IPA corpus engineering validator, web checks and production build).
- Chromium [44339619558](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44339619558) — SUCCESS (full Playwright browser suite, including the new accessibility structural checks).

Exact post-merge main verification on `21092c099e37e47a0f23031c49dc90387ecb464d`:
- Quality [44339770085](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44339770085) — SUCCESS.
- Chromium [44339769999](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44339769999) — SUCCESS.
- GitHub Pages production build, Chromium exercise, deployment and deployed-site/runtime-asset smoke [44339769998](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44339769998) — SUCCESS; build and deploy jobs both completed successfully.

Scope boundary: this is automated structural/accessibility-name smoke coverage, not a complete WCAG audit. It does not establish screen-reader compatibility, exhaustive keyboard traversal, 200%/400% zoom/reflow, all contrast contexts, touch target adequacy or real-device behavior. Manual accessibility task `KHM-UI-001` remains **PARTIAL**. No production runtime, phonological rule, IPA label, Ukrainian mapping, corpus row, source-rights status or benchmark score changed.

Live branch inventory after PR #389: **261 refs / 261 unique tip SHAs**. Prefix counts: a11y 2, audit 37, benchmark 1, ci 1, data 4, docs 107, feat 50, fix 16, main 1, release 1, research 29, test 12. Open PRs: 0. Open non-PR issue: #104 only.

Task ledger: PR #389 automated landmark/document-language/accessible-name smoke and exact-main Quality/Chromium/Pages checks — **DONE_VERIFIED**. Manual accessibility — **PARTIAL**. Full historical semantic re-adjudication — **PARTIAL**. Issue #104 independent IPA gold pilot — **BLOCKED**; approved convention, independent annotators/adjudicator/curator, private blind intake, rights-cleared 30-item packet and adjudication remain external human/evidence gates; gold = 0 and empirical accuracy = null. Root license — **BLOCKED** pending owner decision. External benchmark integration — **DEFERRED** pending rights/provenance and a valid independent evaluation set.

No local checkout or local test execution is claimed; verification is from exact PR-head and exact post-merge GitHub Actions runs. Repository remains a research-ready partial prototype, not linguistically validated or release-ready.


## PR #390 — canonical closeout for PR #389 — 2026-11-18

PR [#390](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/390) merged by squash as a2bb1f6e40cd0e9c172fc75249cdc3154d854289, with PR head 8763b1410f9523352f21e08cd746e3c4b3648ba7 and base 21092c099e37e47a0f23031c49dc90387ecb464d. This documentation-only PR reconciles the canonical handoff, repository audit and linguistic completion register with the PR #389 accessibility structural-smoke work and its exact-main CI.

Exact PR-head Quality [44340072047](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44340072047) — SUCCESS.

Exact post-merge main verification on a2bb1f6e40cd0e9c172fc75249cdc3154d854289:
- Quality [44340210799](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44340210799) — SUCCESS.
- Chromium [44340210892](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44340210892) — SUCCESS.
- GitHub Pages build/deploy and deployed-site/runtime-asset smoke [44340211059](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44340211059) — SUCCESS; build and deploy jobs both completed successfully.

The closeout PR itself changed only the three canonical documentation records. Its exact-head Quality [44340047100](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44340047100) — SUCCESS. No runtime, linguistic data or benchmark result changed.

Live branch inventory at the PR #390 mainline checkpoint: **262 refs / 262 unique tip SHAs**. Prefix counts: a11y 2, audit 37, benchmark 1, ci 1, data 4, docs 108, feat 50, fix 16, main 1, release 1, research 29, test 12. Open PRs: 0. Open non-PR issue: #104 only.

Task ledger: PR #389 automated accessibility structural checks — DONE_VERIFIED; PR #390 canonical documentation closeout and exact-main Quality/Chromium/Pages — DONE_VERIFIED. Manual accessibility KHM-UI-001 remains PARTIAL pending screen-reader, exhaustive keyboard, zoom/reflow, complete contrast-context and real-device checks. Full historical semantic re-adjudication remains PARTIAL. Issue #104 independent IPA gold pilot remains BLOCKED by external convention, staffing, blind-intake, rights and adjudication gates; independent gold = 0, empirical accuracy = null. Root license remains BLOCKED pending owner decision. External benchmark integration remains DEFERRED pending rights/provenance and independent evaluation data.

No local checkout or local tests are claimed. Repository remains a research-ready partial prototype, not linguistically validated or release-ready.


## PR #392 — accessibility smoke test regex correction — 2026-11-18

**TEST-ACCESSIBLE-NAME-REGEX-001 — DONE_VERIFIED (test infrastructure only).** The structural accessibility helper in `tests/browser/site.spec.js` had two double-escaped whitespace regexes: multiple `aria-labelledby` ID references were not split, and whitespace normalization did not process actual whitespace. PR [#392](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/392) corrected both; merged main SHA `9a5da179316c3a40ec159b11c0c936a2c1f9d551`.

Exact PR-head Quality [44366919812] SUCCESS (432 Python tests + 70 subtests, corpus structural validation, Node/web checks and production build); Chromium [44366919747] SUCCESS (21/21). Exact-main Quality [44367112353], Chromium [44367112434], and Pages build/deploy [44367112407] SUCCESS.

Scope is strictly test correctness. The helper remains a structural/name-source smoke check, not a full computed accessible-name algorithm or WCAG audit. `KHM-UI-001` remains PARTIAL pending manual screen-reader/assistive-technology, exhaustive keyboard, zoom/reflow, complete contrast and real-device QA. No IPA, phonology, Ukrainian mapping, corpus, gold or benchmark data changed. Issue #104 remains BLOCKED; independent gold = 0 and empirical accuracy = null. Root license remains BLOCKED on owner decision; historical semantic review remains PARTIAL; external benchmark integration remains DEFERRED.


## PR #393 — canonical closeout for PR #392 — 2026-11-18

PR [#393](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/393) merged by squash as `991d7a1901263743464a41403b3f3936ee33daf1`, with exact PR head `0bab97e4b9ca3b3503c61faf3375635581f80ad4` and base `9a5da179316c3a40ec159b11c0c936a2c1f9d551`. It updates the three existing canonical records in place to document PR #392's accessibility-smoke regex correction, its exact-head checks, exact-main checks, and the unchanged research gates. This is documentation-only; it changes no runtime code, phonological rule, IPA label, Ukrainian mapping, corpus row, source-rights decision, gold data or benchmark result.

Exact PR-head Quality [44367427914](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44367427914) — SUCCESS.

Exact post-merge main verification on `991d7a1901263743464a41403b3f3936ee33daf1`:
- Quality [44367546616](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44367546616) — SUCCESS: 432 Python tests + 70 subtests; corpus validator returned the expected `NOT_READY_NO_ADJUDICATED_GOLD`; browser contract checks and production build passed.
- Chromium [44367546812](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44367546812) — SUCCESS: 21/21 Playwright tests.
- GitHub Pages [44367546866](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44367546866) — SUCCESS: production build, Chromium exercise, deployment and published-site/runtime-asset smoke; build and deploy jobs both completed.

Live branch inventory after PR #393: **265 refs / 265 unique tip SHAs**. Prefix counts: a11y 2, audit 37, benchmark 1, ci 1, data 4, docs 110, feat 50, fix 16, main 1, release 1, research 29, test 13. Open PRs: 0; open non-PR issue: #104 only. All historical branches remain untouched; no branch was deleted or force-updated.

Task ledger: PR #392 accessibility-smoke regex correction and PR #393 canonical documentation closeout — **DONE_VERIFIED**. Manual accessibility KHM-UI-001 remains **PARTIAL** pending assistive-technology, exhaustive keyboard, zoom/reflow, complete contrast-context and real-device checks. Full historical semantic re-adjudication remains **PARTIAL**. Issue #104's independent IPA gold pilot remains **BLOCKED**: convention `DRAFT_NOT_APPROVED`, no confirmed appointments or private blind-intake dry run, rights-cleared 30-item packet not established, adjudicated gold = 0 and empirical accuracy = null. Root license remains **BLOCKED** pending owner decision. External benchmark integration remains **DEFERRED** pending rights/provenance and a valid independent evaluation set.

No local checkout or local tests are claimed; all verification above is from GitHub Actions on the exact PR head and exact merged main SHA. Repository remains a research-ready partial prototype, not linguistically validated or release-ready.


## PR #394 — audit closeout — 2026-11-18

PR #394 merged as `855eac7e6dc39a854cc79055c385152a4a32fc49`. Canonical records now include the PR #393 closeout and its exact-main evidence; this entry closes the remaining one-PR documentation lag.

Exact-main verification: Quality [44379052920] SUCCESS (432 Python tests + 70 subtests; corpus state `NOT_READY_NO_ADJUDICATED_GOLD`; web checks/build passed); Chromium [44379052839] SUCCESS; Pages/deployed-site smoke [44379052866] SUCCESS.

Branch audit: 266 refs / 266 unique tip SHAs, no open PRs, Issue #104 only. Spot-checked recent unmerged-looking PCGN, IPA tie-bar and Unicode TN #61 branches; corresponding implementation, tests/schema and canonical source metadata already exist on main. No stale branch was merged, deleted or rewritten.

Classification: documentation closeout and hosted exact-main CI — DONE_VERIFIED. IPA convention approval and independent gold acquisition — BLOCKED (gold 0; accuracy null). Root license decision — BLOCKED. Manual accessibility and full historical semantic review — PARTIAL. External benchmark integration — DEFERRED. No linguistic labels or rights claims were added; project remains research-ready partial prototype, not release-ready.


## PR #395 — audit closeout — 2026-11-18

PR #395 merged as `3e99140e80ba0a0c1654dcd6f367d651350117b5`. Canonical documentation now records PR #394 and its exact-main verification. PR #395 itself is a documentation-only synchronization change.

Exact-main CI on `3e99140e80ba0a0c1654dcd6f367d651350117b5`: Quality [44393630260](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44393630260) SUCCESS; Chromium [44393630430](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44393630430) SUCCESS; Pages/deployed-site smoke [44393630332](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44393630332) SUCCESS.

Classification: canonical PR #394 closeout and exact-main hosted CI — DONE_VERIFIED. Independent IPA gold pilot and root license decision — BLOCKED (approved convention/personnel/rights-cleared packet and owner license decision absent); gold = 0, empirical accuracy = null. Manual accessibility and full historical semantic re-adjudication — PARTIAL. External benchmark integration — DEFERRED. No new phonological labels, source permissions, corpus rows or benchmark scores were introduced. Repository remains research-ready partial prototype, not linguistically release-ready.


## PR #397 — PCGN omitted-shifter uncertainty — 2026-11-18

Merged as `e888c190570acc19b8cf388d1b2a2a58767e6426`. The PCGN series resolver now emits an explicit note-2 warning when no register shifter is encoded, preserving the current graphemic series default while directing reference consultation when the series is uncertain. It does not infer omitted diacritics. Regression tests cover both base-series defaults and warning presence.

Verification: PR-head Quality [44395612844](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44395612844), Chromium [44395612835](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44395612835), push Quality [44395586583](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44395586583), exact-main Quality [44395795606](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44395795606), Chromium [44395795589](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44395795589), Pages [44395795652](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44395795652): all SUCCESS.

Task classification: omitted-shifter uncertainty warning — DONE_VERIFIED. Full PCGN safe syllable-boundary behavior and contextual script-to-romanization engine — TODO/PARTIAL; the project still requires reviewed ambiguity cases and complete source-backed rule coverage. No IPA, pronunciation labels, Ukrainian mappings or corpus records changed.



## PR #399 — PCGN shifter codepoint and BA exception correction — 2026-11-18

Merged as `8bbdf54bac984165e86b747504ccf7a1e2735741` (final PR head `79bacbdef5cd37be94f05d01ea3223644d10d0fb`). Corrected the source registry to map TRIISAP to U+17CA (`◌៊`) and MUUSIKATOAN to U+17C9 (`◌៉`). Fixed a source-backed resolver defect: BA + TRIISAP is exempt from the normal TRIISAP â→ô shift and remains in the ô-series; Note 3's p-in-â exception applies to BA + MUUSIKATOAN or BA + foot. Updated both decision schemas, tests and the PCGN/UNGEGN audit.

Verification: PR-head Quality [44404900821](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44404900821), Chromium [44404900673](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44404900673), push Quality [44404888463](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44404888463), exact-main Quality [44405101264](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44405101264), Chromium [44405101302](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44405101302), Pages [44405101273](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44405101273): all SUCCESS. Quality: 435 tests + 70 subtests; Chromium: 21/21. Corpus gate correctly remains `NOT_READY_NO_ADJUDICATED_GOLD`.

Classification: PCGN shifter codepoint registry and BA+TRIISAP correction — DONE_VERIFIED. Full contextual PCGN engine and syllable-boundary behavior — TODO/PARTIAL. IPA convention DRAFT_NOT_APPROVED; independent gold = 0; empirical accuracy = null. Issue #104 pilot and root license remain BLOCKED; manual accessibility and historical semantic review remain PARTIAL; external benchmark integration remains DEFERRED. No IPA gold, pronunciation claims or rights decisions were added. Repository remains a research-ready partial prototype, not release-ready.


## PR #401 — BA+AA shifter exception regression tests — 2026-11-19

Merged as `3bbf3f45afb83faf0335dd2f91f869b85f00c5d5` (PR head `0cf4e3a21bc121b4642afafa7f49e365713f7964`). Added regression coverage for BA+AA with TRIISAP (`ប៊ា`, Note 2 no-shift exception) and BA+AA with MUUSIKATOAN (`ប៉ា`, Note 3 p-in-â exception). This is test-only; the resolver behavior did not change.

Verification: push Quality [44407401573](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44407401573), PR-head Quality [44407541894](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44407541894), PR Chromium [44407541887](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44407541887), exact-main Quality [44407714461](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44407714461) and [44407773406](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44407773406), Chromium [44407714501](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44407714501), Pages [44407714752](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44407714752): all SUCCESS. Quality: 437 tests + 70 subtests; Chromium: 21/21. Gold gate correctly remains not ready.

Classification: BA+AA exception test coverage — DONE_VERIFIED. Full PCGN engine/boundary inference remains TODO/PARTIAL; IPA convention DRAFT_NOT_APPROVED, independent gold 0, empirical accuracy null; pilot and root license BLOCKED; manual accessibility/history audit PARTIAL; benchmark DEFERRED. Research-ready partial prototype, not release-ready.


## PR #402 — post-merge closeout evidence — 2026-11-19

PR [#402](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/402) merged as `92011a62d150917dfc12193471b3fe994212e563` (head `d18171b5fb3daa711d5bb699db4ec98d5cc2c26d`). This documentation-only PR recorded PR #401's two BA+AA exception regressions in the canonical handoff, audit and this register.

Exact-main CI on `92011a62d150917dfc12193471b3fe994212e563`:
- Quality [44478963929](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44478963929) — SUCCESS: 437 Python tests + 70 subtests, expected `NOT_READY_NO_ADJUDICATED_GOLD`, Node/web checks and production build.
- Chromium [44478963989](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44478963989) — SUCCESS: 21/21.
- Pages/deployed-site [44478963941](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44478963941) — SUCCESS: build, browser exercise, deploy and runtime-asset smoke.

Classification: PR #401 BA+AA exception regression tests and PR #402 canonical documentation closeout — DONE_VERIFIED. This does not complete the contextual PCGN engine or syllable-boundary inference (TODO/PARTIAL), approve the IPA convention, create independent gold (0; accuracy null), clear Issue #104/root-license blockers, or complete manual accessibility/history review. External benchmark integration remains DEFERRED. Repository remains a research-ready partial prototype, not release-ready. No local tests are claimed; verification is hosted CI on exact main.


## PR #405 — PCGN Note 3 BA+AA+foot regression — 2026-11-19

PR [#405](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/405) adds a test-only extension for the exact Note 3 wording that names both ប and បា with a foot. The existing BA+foot resolver behavior was already implemented; the test now checks both `ប្ក` and `ប្កា`, and confirms the latter retains dependent vowel sign `ា` while resolving the BA-with-foot p-in-â exception. No runtime rule, source row, IPA/Ukrainian output, corpus label or benchmark changed.

Exact PR-head commit: `6b4ed2bbd0a575d39fe0865082f854511c32cb4a`.
- Quality PR [44482081471](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44482081471) — SUCCESS: 437 Python tests + 70 subtests; Node/web checks and production build passed.
- Push Quality [44482061657](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44482061657) — SUCCESS: same exact SHA and test counts.
- Khmer browser smoke [44482081280](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44482081280) — SUCCESS: 21/21 Playwright tests.

Task ledger: PCGN Note 3 BA+AA+foot regression coverage — DONE_VERIFIED. Full contextual PCGN engine and syllable-boundary inference remain TODO/PARTIAL; IPA convention remains DRAFT_NOT_APPROVED, independently adjudicated IPA gold = 0 and empirical accuracy = null. Issue #104 pilot and root repository license remain BLOCKED; manual accessibility and historical semantic review remain PARTIAL; external benchmark integration remains DEFERRED. Repository remains a research-ready partial prototype, not linguistically validated or release-ready. Verification above is hosted GitHub Actions; no local checkout or local tests are claimed.


## PCGN BA exception source-matrix and cross-layer regression closeout — 2026-11-19

### PR #406 — source-matrix reconciliation

PR [#406](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/406) merged as `14e82f0799bd16db61ff688716eee94084cc6a7a`. The PCGN consonant registry row for BA now distinguishes the Note 2 TRIISAP no-shift exception from Note 3's p-in-â exceptions for BA+MUUSIKATOAN or BA+foot. The update aligns the consonant matrix with `romanization_pcgn_notes.csv` and the bounded resolver; no runtime or corpus change.

- PR Quality [44482295867](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44482295867) — SUCCESS; push Quality [44482287227](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44482287227) — SUCCESS.
- PR Chromium [44482295873](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44482295873) — SUCCESS, 21/21.
- Exact-main Quality [44482917557](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44482917557), Chromium [44482852867](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44482852867), and Pages [44482852902](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44482852902) — SUCCESS; exact-main Chromium 21/21.

### PR #409 — Note 2/3 series-to-vowel integration test

PR [#409](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/409) merged as `a595d2da733b522ff3b6203a75ffa658b8f602ed`. Added a test-only cross-layer check proving that the dependent-vowel resolver consumes the series decision: `ប៊ា` (BA+TRIISAP) stays in ô-series and maps AA to `éa`; `ប៉ា` (BA+MUUSIKATOAN) stays in â-series and maps AA to `a`. Both outputs remain PCGN romanization components only; the test explicitly asserts no IPA/Ukrainian output. No runtime behavior, source tables, corpus, or gold labels changed.

- PR Quality [44482940446](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44482940446) and [44482954991](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44482954991) — SUCCESS; 438 Python tests + 70 subtests.
- PR Chromium [44482955087](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44482955087) — SUCCESS, 21/21.
- Exact-main Quality [44483093339](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44483093339) — SUCCESS; 438 Python tests + 70 subtests.
- Exact-main Pages [44483093325](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44483093325) — SUCCESS, including production deploy and deployed runtime-asset smoke. Exact-main Chromium [44483093385](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44483093385) was still running its Chromium-install step at the time of this update; PR-head Chromium is green on the identical source tree.

Task ledger: BA+AA+foot Note 3 test coverage, BA consonant source-row reconciliation, and BA+AA shifter-to-dependent-vowel integration coverage — DONE_VERIFIED. Full contextual Khmer-script → PCGN syllable segmentation/romanization remains TODO/PARTIAL. IPA convention remains DRAFT_NOT_APPROVED; independent adjudicated IPA gold = 0; empirical accuracy = null. Issue #104 pilot and root repository license remain BLOCKED; manual accessibility and historical semantic review remain PARTIAL; external benchmark integration remains DEFERRED. Repository remains a research-ready partial prototype, not linguistically validated or release-ready. Hosted GitHub Actions evidence only; no local checkout or local tests are claimed.


## PR #406 exact-main closeout — 2026-11-19

PR [#406](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/406) merged as `14e82f0799bd16db61ff688716eee94084cc6a7a`. Its single source-registry correction clarifies that BA+TRIISAP remains in the ô-series under PCGN Note 2, while Note 3's p-in-â exception applies to BA+MUUSIKATOAN or BA+foot. This reconciles `romanization_pcgn_consonants.csv` with the existing notes registry; no runtime, corpus, IPA or Ukrainian output behavior changed.

The final main commit at verification was `0e6498db53d0a7792fb4810b2ddba9f8b001df92`. All three workflows on that exact SHA succeeded:
- [Quality checks 44483598159](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44483598159) — SUCCESS: 438 Python tests and 70 subtests; IPA corpus structural check, Node/web checks and production build passed. Corpus gate correctly remains `NOT_READY_NO_ADJUDICATED_GOLD`.
- [Khmer browser smoke 44483598168](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44483598168) — SUCCESS, Chromium visible-result checks passed (21/21).
- [Pages/deployed runtime 44483598094](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44483598094) — SUCCESS: production build, Chromium exercise, Pages deployment and deployed runtime-asset smoke all passed.

This supersedes the earlier note that exact-main Chromium was still in progress: it subsequently completed successfully on the final main SHA above. Current task ledger: BA+AA+foot regression, BA source-matrix reconciliation, and BA+AA series-to-dependent-vowel integration — DONE_VERIFIED. Full contextual Khmer-script → PCGN syllable segmentation/romanization remains TODO/PARTIAL. IPA convention remains DRAFT_NOT_APPROVED; independent adjudicated IPA gold = 0 and empirical accuracy = null. Issue #104 pilot and root repository license remain BLOCKED; manual accessibility and historical semantic review remain PARTIAL; external benchmark integration remains DEFERRED. The repository remains a research-ready partial prototype, not linguistically validated or release-ready. Evidence is from hosted GitHub Actions; no local checkout or local tests are claimed.


## PCGN vowel-table corrections and Note 5 SAMYOK coverage — 2026-11-19

### PR #414 — dependent-vowel source reconciliation

PR [#414](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/414) merged as `21c14e05b40bd0b508358c201e1ff8b586ed78a9`. Direct visual comparison with the official UK PCGN 1972 vowel table corrected three dependent-vowel cells:

- Row 3, `ិ`: â-series `ĕ`, ô-series `ĭ` (the prior resolver/test incorrectly used `ĕ` in both series).
- Row 16, `េ+ា`: â-series `aô`, ô-series `oŭ`.
- Row 17, `េ+ៅ`: â-series `au`, ô-series `ŏu`.

The new `data/khmer/romanization_pcgn_dependent_vowels.csv` registers all 16 normal dependent-vowel patterns (table rows 2–17) with source locators, URL and component-only acceptance boundary. A parity test compares the entire registry against `PCGN_DEPENDENT_VOWEL_ROWS`. The resolver continues to consume an explicit series and emits only PCGN romanization components; no IPA/Ukrainian output was added.

### PR #416 — Note 5 SAMYOK coda-class coverage

PR [#416](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/416) merged as `a179384510377a1aa3ca6f142aca62750cbe7531`. Added structural fixtures for SAMYOK SANNYA (`័`) before each supported coda class (`k`, `ng`, `h`, `other`) in both series. They assert â-series `ă` for all classes and ô-series `eă` before `k/ng/h`, otherwise `oă`. These are table-pattern fixtures, not claims of attested lexical items. No runtime behavior changed in PR #416.

### Exact-main verification on `a179384510377a1aa3ca6f142aca62750cbe7531`

- Quality [44485716034](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44485716034) — SUCCESS: 441 Python tests + 70 subtests; IPA corpus structural gate, Node/web checks and production build passed. Corpus status remains `NOT_READY_NO_ADJUDICATED_GOLD`.
- Khmer browser smoke [44485716025](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44485716025) — SUCCESS, 21/21.
- Pages [44485716116](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44485716116) — SUCCESS: build, deployment and deployed runtime-asset smoke passed.

Task ledger: dependent-vowel PCGN table rows 2–17 source transcription and runtime/CSV parity — DONE_VERIFIED; Note 5 SAMYOK coda-class branches — DONE_VERIFIED. Full semantic comparison with the external UNGEGN candidate remains PARTIAL (profile differences must not be flattened); full contextual PCGN segmentation/romanization remains TODO pending human-reviewed ambiguity and source-backed lexical fixtures. IPA convention remains DRAFT_NOT_APPROVED, independent adjudicated IPA gold = 0, accuracy = null. Issue #104 pilot and root repository license remain BLOCKED; manual accessibility/historical semantic review PARTIAL; external benchmark integration DEFERRED. Repository remains a research-ready partial prototype, not linguistically validated or release-ready.

PR reconciliation: earlier duplicate PR #413 was closed unmerged after its SAMYOK test change was carried forward in PR #416; duplicate PR #415 was closed unmerged after its row-3 correction was superseded by the broader PR #414 (which also corrected rows 16–17 and added the full row registry). Their branches were not deleted. Hosted GitHub Actions are the verification source; no local checkout or local test execution is claimed.


## PCGN ↔ UNGEGN candidate vowel-row reconciliation — 2026-11-19

PR [#419](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/419) merged as `0090960bb1558cf98c5ebd424d1f883f33859c8c`. Added the machine-readable comparison `data/khmer/pcgn_ungegn_vowel_profile_comparison.csv` and structural test `tests/test_pcgn_ungegn_vowel_profile_comparison.py`. It compares 17 PCGN normal dependent/inherent rows, 12 independent-vowel entries, three shortened patterns, and eight anusvara/visarga rows against the pinned UNGEGN candidate source `pheasaKhmer/khmer-engine@31b72cd4665f69678fc835da2f501771e42f097a`.

Findings are now evidence-registered:
- All 17 normal dependent/inherent values and all eight anusvara/visarga rows match the pinned candidate values after the PCGN source corrections in PR #414.
- Eleven of twelve independent-vowel entries match; the candidate selects `ŏ` for `ឧ`, while PCGN Note 9 preserves `ŏ` or `ŭ` and calls for reference selection when uncertain.
- The three shortened patterns share the core values, but the candidate also treats `kh` as an `eă` coda trigger; PCGN Note 5 names only `k`, `ng`, and `h`.
- Eight candidate-only extensions are separately listed: four independent-vowel characters absent from the PCGN table, SAMYOK-before-final-Y, YUUKALEAPINTU, generic fallback for unlisted NIKAHIT/REAHMUK combinations, and the extra `kh` branch.

This closes the comparison task only. It does **not** authorize importing the candidate's UNGEGN behavior into the PCGN runtime. The selected profile remains BGN/PCGN 1972; candidate syllabification heuristics and unsupported extensions remain unadopted.

Exact-main verification on `0090960bb1558cf98c5ebd424d1f883f33859c8c`:
- Quality [44486526230](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44486526230) — SUCCESS: 442 Python tests + 70 subtests; IPA corpus structural gate, Node/web checks and production build passed. Corpus remains `NOT_READY_NO_ADJUDICATED_GOLD`.
- Pages [44486526214](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44486526214) — SUCCESS: production build, deployment and deployed runtime-asset smoke.
- Khmer browser smoke [44486526348](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44486526348) was still running the Chromium installation step at documentation time; no browser result is claimed for this SHA here. PR #416's unchanged browser surface passed 21/21, and no runtime/UI files changed in PR #419.

Task ledger: PCGN dependent-vowel rows 2–17 source registry/runtime parity — DONE_VERIFIED; Note 5 SAMYOK coda classes — DONE_VERIFIED; complete PCGN vowel/nucleus row comparison against the pinned UNGEGN candidate — DONE_VERIFIED (comparison only). Full contextual Khmer-script → PCGN segmentation/romanization remains TODO/PARTIAL pending human-reviewed ambiguity cases and source-backed lexical fixtures. IPA convention remains DRAFT_NOT_APPROVED; independent adjudicated IPA gold = 0; accuracy = null. Issue #104 pilot and root repository license remain BLOCKED; manual accessibility/historical semantic review PARTIAL; external benchmark integration DEFERRED. Repository remains a research-ready partial prototype, not linguistically validated or release-ready. Verification is from hosted GitHub Actions; no local checkout or local test execution is claimed.

PR reconciliation: #413/#415 were closed unmerged as superseded by #416/#414; #418 was closed unmerged after its stale documentation branch conflicted with the already-merged #417 closeout. No user branches were deleted or force-updated.


## PCGN profile-delta and anusvara row 7 closeout — 2026-11-19

### PR #421 — PCGN weak-foot delta for ស

PR [#421](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/421) merged as `3088c1588fe6bdd8f15f169632154e0c044f9f4e`. It added a source-backed structural regression for `គ្ស`: under PCGN Note 3, `ស` is not in the weak-foot set, so the foot determines the â-series despite the ô-series base. The resolver already implemented this; no runtime change was needed. The fixture is structural, not an attested lexical item. PR-head Quality [44487165963](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44487165963) — SUCCESS (443 tests + 70 subtests); Chromium [44487166024](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44487166024) — SUCCESS (21/21).

### PR #422 — PCGN anusvara/visarga row 7 exact source pattern

PR [#422](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/422) merged as `653ed8593d6cdb467eb036a35bb8f48cb4a24672`. Visual review of the official PCGN 1972 table row 7 (PDF p. 4) established the source sequence `េ + ា + ះ` (preposed E + AA + REAHMUK). The prior runtime/source CSV incorrectly used the candidate-shaped key `ោ + ះ` while preserving the same Latin values. Runtime, source registry, resolver/assembler tests and decision/assembly schemas now require the exact PCGN sequence; `កេាះ` / `គេាះ` resolve, while the distinct candidate-shaped `កោះ` abstains. The comparison registry marks row 7 as `VALUE_MATCH_KEY_SHAPE_DIFFERS`, not a full key match. PR-head Quality [44487517489](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44487517489) — SUCCESS (443 tests + 70 subtests); Chromium [44487517431](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44487517431) — SUCCESS (21/21). Exact-main Quality [44487673393](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44487673393), Chromium [44487673310](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44487673310) (21/21), and Pages/deployed runtime [44487673472](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44487673472) all succeeded on the merged state.

### PR #424 — PCGN comparison/source-registry parity

PR [#424](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/424) merged as `7d10b273377c8ebf15b731c372af04735d92f10d`. It adds tests cross-checking every dependent, inherent, independent and anusvara/visarga PCGN comparison cell against the project-owned source registries, including the corrected row 7 source sequence. The test explicitly includes inherent row 1 in the combined dependent/inherent section and all dependent rows 2–17. PR-head Quality [44487905158](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44487905158) — SUCCESS (444 tests + 70 subtests); Chromium [44487905013](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44487905013) — SUCCESS (21/21).

### Exact-main verification and CI note

The final code state at PR #424 was `7d10b273377c8ebf15b731c372af04735d92f10d`:
- Quality [44488041871](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44488041871) — SUCCESS: 444 Python tests + 70 subtests; IPA corpus structural check, Node/web checks and production build passed. Corpus remains `NOT_READY_NO_ADJUDICATED_GOLD`.
- Pages/deployed runtime [44488041861](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44488041861) — SUCCESS: production build, Chromium exercise, Pages deployment and deployed runtime-asset smoke passed.
- Standalone exact-main Khmer browser smoke [44488041862](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44488041862) subsequently completed SUCCESS: 21/21 Chromium checks. The exact-main Pages workflow also exercised Chromium and deployed runtime assets successfully.

Documentation-only PR #425 then merged as `369e0f3d0a7a83d38f28f1e81f4990fd74d9cf21`. On that exact SHA, Quality [44488517602](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44488517602) — SUCCESS (444 tests + 70 subtests); standalone Chromium [44488517391](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44488517391) — SUCCESS (21/21); Pages/deployed runtime [44488517747](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44488517747) — SUCCESS (production build, Chromium exercise, deployment and deployed asset smoke).

### PR reconciliation and task ledger

PR #423 was closed unmerged after its stale-base parity test omitted inherent row 1 from the combined rows 1–17 set and initially used the candidate-shaped row 7 key. The corrected source-registry parity test was ported to #424 on current main after #422 fixed the exact PCGN row 7 pattern. No candidate code or data was imported. PR #426 was closed unmerged as superseded by merged PR #427; its documentation details were incorporated into #427. No branches were deleted or force-updated.

DONE_VERIFIED: PCGN Note 2/3 shifter and BA exceptions by exact code point; PCGN dependent-vowel rows 2–17 source registry/runtime parity; PCGN/UNGEGN vowel/nucleus value comparison with candidate-only extensions and key differences explicit; PCGN anusvara/visarga row 7 exact source pattern; PCGN Note 3 `ស` series-determining foot delta; comparison/source-registry parity test. PARTIAL/TODO: parser-key normalization equivalence for different candidate spellings is not assumed; complete contextual Khmer-script → PCGN syllable segmentation/romanization remains TODO pending human-reviewed ambiguity cases and source-backed lexical fixtures. IPA convention remains DRAFT_NOT_APPROVED; independent adjudicated IPA gold = 0 and empirical accuracy = null. Issue #104 pilot and root repository license remain BLOCKED; manual accessibility and historical semantic review remain PARTIAL; external benchmark integration remains DEFERRED. The repository remains a research-ready partial prototype, not linguistically validated or release-ready. Verification is from hosted GitHub Actions; no local checkout or local tests are claimed.


## Exact PCGN row 7 comparison/source-registry parity closeout — 2026-11-19

PR [#430](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/430) merged as `bdcf231d4516e718edc5b50a95a8ae5455a82c89`. The comparison parity test now preserves exact component-boundary equality for PCGN anusvara/visarga rows 1, 5, 6 and 7, where both registries encode the same explicit grouping. Rows 2, 3, 4 and 8 are compared by ordered concatenated code-point sequence because the two registries intentionally group combined Khmer signs differently (notably row 8: comparison `ាំ+ង` vs source components `ា+ំ+ង`). Row 7 additionally asserts the exact source registry and comparison sequence `េ+ា+ះ`, preserving the distinction from the candidate's separate key `ោះ`. This is data-contract parity; no runtime, IPA or Ukrainian behavior changed.

Exact-main verification on `bdcf231d4516e718edc5b50a95a8ae5455a82c89`:
- Quality [44490203200](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44490203200) — SUCCESS: 444 Python tests + 70 subtests; Node/web checks and production build passed.
- Khmer browser smoke [44490203310](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44490203310) — SUCCESS: 21/21 Chromium checks.
- GitHub Pages workflow [44490203147](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44490203147) — SUCCESS: production build, Chromium exercise, Pages artifact upload (artifact 14513255193).

PR reconciliation: #429 was closed unmerged after its initial all-exact-separator assertion failed on the differing representation of combined signs; #430 superseded it with row-specific grouping semantics and merged. PR #431 was closed unmerged as redundant after #430 included the exact row 7 source-registry assertion. All three branches were left intact; none was deleted or force-updated. No open PRs remained at the time of this audit. The only open issue is #104, which still requires human expert approval of the IPA convention, two independent Khmer annotators, a separate adjudicator, a curator, private blind intake, 30 attested rights-cleared lexeme groups, independent annotations and adjudication. Gold remains 0; empirical accuracy remains null.

Task ledger: PCGN vowel comparison/source-registry value parity — DONE_VERIFIED; exact PCGN row 7 source sequence parity — DONE_VERIFIED; row-specific component-boundary representation checks for all eight anusvara/visarga rows — DONE_VERIFIED. Full contextual Khmer → PCGN syllable/word segmentation remains PARTIAL/TODO; IPA convention remains DRAFT_NOT_APPROVED; issue #104 remains BLOCKED on specialist participation and rights-cleared annotated material. Repository remains a research-ready partial prototype, not a linguistically validated release. Verification is hosted GitHub Actions; no local checkout or local test execution is claimed.

 
## PCGN branch-family and live-ref inventory closeout — 2026-11-19

### Current-main review of PCGN fix branches

The current-base compare and targeted blob checks covered the ten PCGN-specific fix/* refs in this inventory. Dispositions:
- fix/pcgn-anusvara-row7-source-pattern-main-2026-11-19 maps to merged PR #422; its current runtime, source CSV and schema blobs match main. The earlier fix/pcgn-anusvara-row7-source-pattern-2026-11-19 ref has no PR, but its runtime, CSV, decision schema and syllable-assembly test blobs are byte-identical to main; its resolver test is an older snapshot and contains no missing accepted implementation.
- fix/pcgn-ba-triisap-source-matrix-main-2026-11-19 maps to merged PR #406; both it and the earlier PR #404 branch have the same consonant source CSV blob as main. PR #404 remains closed unmerged/superseded.
- fix/pcgn-dependent-vowel-series-rows-16-17-2026-11-19 maps to merged PR #414; its full dependent-vowel CSV matches main. The separate PR #415 branch contains the corrected row-3 ô-series ĭ value but still has old row-16/17 values; PR #415 was closed unmerged as superseded by #414.
- fix/pcgn-final-consonant-context-types-2026-11-16, fix/pcgn-omitted-shifter-uncertainty-2026-11-18, fix/pcgn-shifter-registry-codepoint-alignment-2026-11-18, and fix/pcgn-shortened-vowel-diacritic-inventory-2026-11-15 map to merged PRs #255, #397, #399 and #204 respectively. Their branch snapshots are older or their relevant tests/data are already integrated; no unique implementation was ported from the stale tips.

No historical branch was merged wholesale, deleted or force-updated. The review is a targeted PCGN fix-family disposition, not full semantic review of every changed line in every historical branch.

### Live branch inventory snapshot

GitHub branch-list pages 1–4 returned 306 refs with 306 unique names and 306 unique tip SHAs: main plus 305 non-main refs. Prefix counts: a11y 2, audit 38, benchmark 1, ci 1, data 4, docs 130, feat 50, fix 24, release 1, research 29, test 25, plus one unprefixed ref. No duplicate tip SHA was present in this refreshed snapshot. One open PR (#433, the prior-base documentation closeout) was present when the inventory was taken; it is being superseded by this current-base continuation, with its branch preserved.

This does not close repository-wide KHM-BRANCH-AUDIT-001: full changed-file/commit semantic review and complete PR-ancestry reconciliation across all 305 non-main refs remain PARTIAL. The project-owned PCGN source registries and PCGN/UNGEGN comparison/parity checks are DONE_VERIFIED. Contextual PCGN syllable-boundary inference and the full Khmer-script → PCGN engine remain TODO/PARTIAL pending human-reviewed ambiguity cases and source-backed lexical fixtures. IPA convention remains DRAFT_NOT_APPROVED; independent adjudicated IPA gold = 0 and empirical accuracy = null. Issue #104 pilot and root repository license remain BLOCKED; manual accessibility remains PARTIAL; external benchmark integration remains DEFERRED. The repository remains a research-ready partial prototype, not linguistically validated or release-ready. Verification is from hosted GitHub Actions; no local checkout or local tests are claimed.


## Remaining non-PCGN fix-branch triage — 2026-11-19

A fresh live inventory after the prior PCGN branch closeout returned 308 refs, 308 unique names and 308 unique tip SHAs. Prefix counts at this snapshot: `a11y` 2, `audit` 38, `benchmark` 1, `ci` 1, `data` 4, `docs` 132, `feat` 50, `fix` 24, `release` 1, `research` 29, `test` 25, and one unprefixed ref. The count includes retained closed/superseded working refs; it is not a count of active work.

The remaining 14 non-PCGN `fix/*` refs were compared against current main. All are diverged; ahead/behind counts and changed-file counts are recorded below. This is triage metadata only, not a semantic review or permission to merge stale branch tips.

| Branch | Ahead / behind | Changed files |
|---|---:|---:|
| `fix/explicit-ipa-kind-in-phonetic-result-2026-11-17` | 9 / 111 | 9 |
| `fix/flag-unconverted-khmer-romanizer-output-2026-11-15` | 2 / 248 | 2 |
| `fix/ipa-tie-bar-segment-boundaries-2026-11-18` | 3 / 41 | 2 |
| `fix/khmer-benchmark-reproducibility-2026-10-24` | 3 / 585 | 2 |
| `fix/khmer-orthographic-parser-diagnostics-v2-2026-11-16` | 17 / 134 | 9 |
| `fix/khmer-orthographic-parser-evidence-2026-11-16` | 7 / 135 | 5 |
| `fix/khmer-orthographic-parser-rejection-spans-2026-11-16` | 16 / 133 | 10 |
| `fix/khmer-rejected-span-reasons-and-fixtures-2026-11-16` | 2 / 132 | 4 |
| `fix/khmer-typed-partial-phonetic-results-2026-11-16` | 56 / 154 | 12 |
| `fix/khmer-unmodeled-letter-trace-2026-11-12` | 3 / 295 | 3 |
| `fix/mixed-script-numeral-token-boundaries-2026-11-17` | 32 / 107 | 12 |
| `fix/mixed-script-romanization-guard-2026-11-15` | 10 / 255 | 5 |
| `fix/reconcile-unicode-tn61-source-metadata-2026-11-18` | 5 / 60 | 5 |
| `fix/serve-coverage-report-on-pages-2026-10-21` | 6 / 592 | 5 |

The direct head-ref match found in the latest 100-PR listing was PR #384 for the IPA tie-bar branch; it is merged as `70b381d41f00f89bb94c3694b1c6faa692bfe34d`. No PR-head match was found in that listing for the other 13 refs; this does not prove that no historical PR exists or that their commits are unique. No branch was merged, deleted or force-updated in this triage. Before disposition, each remaining ref needs ancestry and per-file semantic comparison against main, especially parser/phonetic-result branches whose ahead counts are large and whose snapshots are far behind.

Task ledger: non-PCGN `fix/*` branch inventory and compare triage — PARTIAL; branch-specific implementation reuse/retirement — TODO pending per-file semantic review. The broader `KHM-BRANCH-AUDIT-001` remains PARTIAL across the 307 non-main refs in this snapshot; do not mark complete from metadata alone. The only open research issue remains #104, blocked on expert IPA convention approval and independent human annotation/adjudication. Gold remains 0; accuracy remains null. Repository remains a research-ready partial prototype, not linguistically validated or release-ready.


## Final mainline checkpoint — 2026-11-19

PR #436 merged as `e254527e8083ed101c5312f83748a01c6552a58b`, recording the 14 non-PCGN `fix/*` branch triage. Its PR-head Quality run [44491769891](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44491769891) succeeded: 444 Python tests + 70 subtests, IPA corpus structural validation, Node/web checks and production build. On exact merged main `e254527e8083ed101c5312f83748a01c6552a58b), Khmer browser smoke [44491922331](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44491922331) succeeded and Pages workflow [44491922541](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44491922541) succeeded (production build and Pages artifact upload). The immediately preceding exact-main commit `f6bc81c22490975fea625d1159c29e4382b3a073` also passed Quality [44491199974], Chromium [44491200084] and Pages [44491200021]. No local checkout or local tests were used.

PR reconciliation: #432, #434 and #436 are merged. #433 and #435 were closed unmerged as superseded by #434; #429 and #431 were closed unmerged as superseded/redundant after #430 merged. Their branches were retained; no branch was deleted or force-updated. At the post-merge check there were no open PRs; Issue #104 was the only open issue.

Final task status: PCGN source-table/runtime parity and PCGN/UNGEGN comparison/source-registry invariants — DONE_VERIFIED; targeted PCGN branch-family triage and non-PCGN `fix/*` branch compare inventory — DONE_VERIFIED as inventory/triage only; repository-wide `KHM-BRANCH-AUDIT-001` — PARTIAL (all non-main refs still need complete semantic review and ancestry reconciliation); contextual Khmer syllable/word segmentation — PARTIAL/TODO pending source-backed ambiguity cases and lexical evidence; IPA convention — DRAFT_NOT_APPROVED; Issue #104 pilot — BLOCKED on expert approval, independent annotators/adjudicator, curator, private blind intake and rights-cleared attested lexeme groups. Independent adjudicated IPA gold = 0; empirical accuracy = null. Manual accessibility/historical semantic review remains PARTIAL; external benchmark integration DEFERRED. Repository is a research-ready partial prototype, not a linguistically validated production release.


## Targeted non-PCGN fix-branch semantic reconciliation — 2026-11-19

Base: exact `main` commit `f0cfa4202caf9724b4f961f298869e42b234c427`. This is a targeted semantic disposition of the 14 non-PCGN `fix/*` refs listed in the preceding inventory, not closure of repository-wide `KHM-BRANCH-AUDIT-001`.

### Disposition

- `fix/explicit-ipa-kind-in-phonetic-result-2026-11-17`: the typed IPA result boundary is already on main. The branch's `phonetic_result.py` is byte-identical to main; its schema, rule-engine, browser and tests are older snapshots. Current main additionally distinguishes `NON_LINGUISTIC` numerals, preserves supported neighbours, and retains explicit unresolved/not-applicable IPA kinds and fallback traces. No port.
- `fix/flag-unconverted-khmer-romanizer-output-2026-11-15`: romanizer implementation is byte-identical to main. The branch test file is a strict subset of current main; main additionally tests unconverted Khmer letters and marks, Khmer punctuation passthrough, direct Latin marks, and BANTOC/SAMYOK inventory. No port.
- `fix/ipa-tie-bar-segment-boundaries-2026-11-18`: IPA implementation and regression test are byte-identical to main. The associated implementation is already merged through PR #384. No port.
- `fix/khmer-benchmark-reproducibility-2026-10-24`: branch harness/workflow are older. Main includes exact harness/corpus/runtime provenance, SHA-256 sidecar output and the later pinned optional MekongPhon diagnostic workflow. No port.
- `fix/khmer-orthographic-parser-diagnostics-v2-2026-11-16`, `fix/khmer-orthographic-parser-evidence-2026-11-16`, `fix/khmer-orthographic-parser-rejection-spans-2026-11-16`, and `fix/khmer-rejected-span-reasons-and-fixtures-2026-11-16`: these are earlier parser/schema/test snapshots. Current main has the later Unicode 18 packed parse forest, per-syllable grammar-role alternatives, derivation and segmentation counts, exact rejected spans/reasons, and expanded Python/browser fixtures. The rejected-span-reasons branch's parser test and browser parser implementation are byte-identical to main. No unique parser implementation to port.
- `fix/khmer-typed-partial-phonetic-results-2026-11-16`: earlier typed-result/rule-engine/browser snapshot. Current main contains the same typed boundary plus later non-linguistic numeric handling, stricter status semantics and expanded cross-runtime tests. No port.
- `fix/khmer-unmodeled-letter-trace-2026-11-12`: the sign inventory is byte-identical to main; branch parser/tests are older. Current main's parser explicitly traces unmodeled characters and preserves the remaining source tail as unsupported rather than dropping it. No port.
- `fix/mixed-script-numeral-token-boundaries-2026-11-17`: Python parser and browser-runtime test are byte-identical to main; branch browser implementation/tests are older. Current main additionally preserves non-linguistic numeral units and their typed status. No port.
- `fix/mixed-script-romanization-guard-2026-11-15`: branch renderer/browser tests are older. Current main uses the stronger unconverted-Khmer guard and tests unsupported mixed input, local unsupported units, neighboring output and source preservation. No port.
- `fix/reconcile-unicode-tn61-source-metadata-2026-11-18`: source registry and provenance test are byte-identical to main. No port.
- `fix/serve-coverage-report-on-pages-2026-10-21`: coverage generator, tests and both generated report copies are byte-identical to main. The public report is present on main. No port.

The separate branch `test/port-unconverted-khmer-mark-romanizer-regressions-2026-11-19` is identical to main at this checkpoint; its Quality run [44493021147](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44493021147) succeeded. The relevant unconverted-mark regression tests are already in main; there is no uncommitted implementation on that branch to port.

### Branch and PR safety

No historical branch was merged, deleted or force-updated. Exact-head PR search found no direct PR match for these 14 branch names except the tie-bar branch's already-merged PR #384. This is not a complete historical PR-ancestry audit. At this checkpoint there are no open PRs.

The refreshed live branch inventory is 312 refs / 312 unique names / 310 unique tip SHAs. The two repeated-tip references are the shared current-main SHA `f0cfa4202caf9724b4f961f298869e42b234c427` on `main`, `test/port-unconverted-khmer-mark-romanizer-regressions-2026-11-19`, and this audit branch; no other repeated tip SHA was found.

### Task ledger

- `KHM-NON-PCGN-FIX-BRANCH-SEMANTIC-TRIAGE-001` — DONE_VERIFIED for the 14 non-PCGN `fix/*` refs' code/data/schema/test dispositions; no unique implementation requires porting.
- `KHM-BRANCH-AUDIT-001` — PARTIAL. The remaining 298 non-main refs still require full per-file semantic review and complete commit/PR ancestry reconciliation; the targeted 14-branch review does not close that repository-wide task.
- Contextual Khmer → PCGN segmentation, IPA convention approval, independent adjudicated IPA gold, manual accessibility review and root repository license retain their prior statuses. Gold remains 0; empirical accuracy remains null. Repository remains a research-ready partial prototype, not release-ready.

Exact-main hosted verification on `f0cfa4202caf9724b4f961f298869e42b234c427`: Quality [44492646955], Khmer browser smoke [44492646961], and Pages/deployed runtime [44492646965] all SUCCESS. No local checkout or local test execution was available in this connector session.


## Historical branch-family sweep — 2026-11-19

A fresh GitHub branch inventory returned 312 refs and 312 unique names (310 unique tip SHAs). Prefix counts: `docs/*` 134, `feat/*` 50, `audit/*` 39, `research/*` 29, `test/*` 26, `fix/*` 24, `data/*` 4, `a11y/*` 2, and one each under `benchmark/*`, `ci/*`, and `release/*`, plus `main`. All 50 feature, 39 audit, 29 research, 26 test, 4 data, 2 accessibility, and the benchmark/CI/release refs were compared with current main. The 134 documentation refs remain for a dedicated semantic-content/ancestry pass; a diff inventory alone does not complete that review.

### Additional semantic findings

- The 39 `audit/*` refs comprise this new audit branch, 36 older documentation-only snapshots, one older PCGN/UNGEGN comparison snapshot, and the old restore-workflow snapshot for PR #353. The PCGN snapshot predates the row-7 correction: it marks every anusvara/visarga row `MATCH`; main correctly records row 7 as `VALUE_MATCH_KEY_SHAPE_DIFFERS` and tests the exact `េ+ា+ះ` sequence against the candidate's distinct `ោះ` key. The PR #353 workflow snapshot is already merged and the pinned `optional-khmerphonemizer-smoke.yml` workflow is present on main.
- The 26 `test/*` refs contain no identified missing regression to port. Current main has stronger or byte-identical counterparts for the Khmer onset fallback fixture, unmodeled-letter/grapheme accounting, romanization guards, keyboard/accessibility smoke, PCGN Note 2/3 BA cases, `ស` foot behavior, SAMYOK coda classes, and source-registry parity. Several PCGN test branches are earlier snapshots: the old candidate-diff test treats all row-7 values as a full match; the old BA+AA vowel expectations predate the official row-3/16/17 corrections; the old accessible-name test contains a double-escaped whitespace regex. Main contains the corrected, stronger tests.
- The four `data/*` refs add no unique current data: the positional-onset JSON/schema/tests and rule-engine integration are byte-identical to main; both independent-vowel source-register snapshots are byte-identical; one integration branch has no diff.
- The 29 `research/*` refs have older source registries and candidate inventories. Main contains the later source records and more complete external-renderer registry. The sole branch-only Google TTS record (`google-km-tts-2018`) is superseded by main's full-file `google-language-resources-km` audit, which distinguishes 69,415 pinned lexicon rows from the paper's 70,671 claim and records the notation, duplicate-key, profile and rights limitations. It is not a Khmer-script IPA gold source.
- The 50 `feat/*` refs are older snapshots of features now represented by main. Targeted code comparisons confirm that the PCGN BA/TRIISAP branch conflates the Note 2 no-shift exception with the distinct Note 3 MUUSIKATOAN/foot exception; main keeps them separate. The parse-forest branches predate the current packed forest and rejected-span diagnostics; the IPA candidate validator predates the current stricter tie-bar checks; the Ukrainian practical adapter and word-boundary evidence files are byte-identical to main. The old hybrid-candidate shell is not restored: the project intentionally uses the deterministic rule engine and does not adopt provider voting.
- The two `a11y/*` refs are older than main's contrast, keyboard, responsive and landmark/name checks. They do not replace the still-required manual accessibility audit.
- `benchmark/current-engine` is not ported: its proposed scorecard compares project output with external non-gold phonetic datasets and reports exact-match/CER metrics without an approved convention or independent adjudication. This remains deferred. The unpinned historical `ci/khmer-g2p-smoke` workflow is superseded by the pinned PR #353 workflow. The `release/*` snapshot contains an older deterministic/hybrid-engine implementation and no release authorization.

No branch in this sweep was deleted, force-updated, or merged. The sweep found no evidence that would justify copying a stale branch snapshot into main. It does not close `KHM-BRANCH-AUDIT-001`: the 134 `docs/*` refs still need semantic review, and commit/PR ancestry is not fully reconciled for every ref. Repository-wide branch audit therefore remains PARTIAL.


## Historical branch-family sweep — 2026-11-19

A fresh GitHub branch inventory returned 312 refs and 312 unique names (310 unique tip SHAs). Prefix counts: `docs/*` 134, `feat/*` 50, `audit/*` 39, `research/*` 29, `test/*` 26, `fix/*` 24, `data/*` 4, `a11y/*` 2, and one each under `benchmark/*`, `ci/*`, and `release/*`, plus `main`. All 50 feature, 39 audit, 29 research, 26 test, 4 data, 2 accessibility, and the benchmark/CI/release refs were compared with current main. The 134 documentation refs remain for a dedicated semantic-content/ancestry pass; a diff inventory alone does not complete that review.

### Additional semantic findings

- The 39 `audit/*` refs comprise this new audit branch, 36 older documentation-only snapshots, one older PCGN/UNGEGN comparison snapshot, and the old restore-workflow snapshot for PR #353. The PCGN snapshot predates the row-7 correction: it marks every anusvara/visarga row `MATCH`; main correctly records row 7 as `VALUE_MATCH_KEY_SHAPE_DIFFERS` and tests the exact `េ+ា+ះ` sequence against the candidate's distinct `ោះ` key. The PR #353 workflow snapshot is already merged and the pinned `optional-khmerphonemizer-smoke.yml` workflow is present on main.
- The 26 `test/*` refs contain no identified missing regression to port. Current main has stronger or byte-identical counterparts for the Khmer onset fallback fixture, unmodeled-letter/grapheme accounting, romanization guards, keyboard/accessibility smoke, PCGN Note 2/3 BA cases, `ស` foot behavior, SAMYOK coda classes, and source-registry parity. Several PCGN test branches are earlier snapshots: the old candidate-diff test treats all row-7 values as a full match; the old BA+AA vowel expectations predate the official row-3/16/17 corrections; the old accessible-name test contains a double-escaped whitespace regex. Main contains the corrected, stronger tests.
- The four `data/*` refs add no unique current data: the positional-onset JSON/schema/tests and rule-engine integration are byte-identical to main; both independent-vowel source-register snapshots are byte-identical; one integration branch has no diff.
- The 29 `research/*` refs have older source registries and candidate inventories. Main contains the later source records and more complete external-renderer registry. The sole branch-only Google TTS record (`google-km-tts-2018`) is superseded by main's full-file `google-language-resources-km` audit, which distinguishes 69,415 pinned lexicon rows from the paper's 70,671 claim and records the notation, duplicate-key, profile and rights limitations. It is not a Khmer-script IPA gold source.
- The 50 `feat/*` refs are older snapshots of features now represented by main. Targeted code comparisons confirm that the PCGN BA/TRIISAP branch conflates the Note 2 no-shift exception with the distinct Note 3 MUUSIKATOAN/foot exception; main keeps them separate. The parse-forest branches predate the current packed forest and rejected-span diagnostics; the IPA candidate validator predates the current stricter tie-bar checks; the Ukrainian practical adapter and word-boundary evidence files are byte-identical to main. The old hybrid-candidate shell is not restored: the project intentionally uses the deterministic rule engine and does not adopt provider voting.
- The two `a11y/*` refs are older than main's contrast, keyboard, responsive and landmark/name checks. They do not replace the still-required manual accessibility audit.
- `benchmark/current-engine` is not ported: its proposed scorecard compares project output with external non-gold phonetic datasets and reports exact-match/CER metrics without an approved convention or independent adjudication. This remains deferred. The unpinned historical `ci/khmer-g2p-smoke` workflow is superseded by the pinned PR #353 workflow. The `release/*` snapshot contains an older deterministic/hybrid-engine implementation and no release authorization.

No branch in this sweep was deleted, force-updated, or merged. The sweep found no evidence that would justify copying a stale branch snapshot into main. It does not close `KHM-BRANCH-AUDIT-001`: the 134 `docs/*` refs still need semantic review, and commit/PR ancestry is not fully reconciled for every ref. Repository-wide branch audit therefore remains PARTIAL.


## Documentation-branch spot reconciliation and exact-main CI — 2026-11-19

A fresh live GitHub branch listing after PR #438 merged returned **312 refs, 312 unique branch names, and 312 unique tip SHAs** (zero duplicate tips). This supersedes the earlier pre-merge inventory snapshot in the preceding section, which recorded 312 refs but 310 unique tips. Current default branch is `main` at `f5faae81078e2828bc069bddda1ec05b95de5ff1`.

A targeted semantic review was made of representative documentation branches whose tips still contain commits not ancestral to current main. Ahead/behind counts alone were not treated as proof of unique content:

- `docs/ipa-gold-recruitment-execution-kit-2026-11-18`: the playbook's invitation templates, private role register and ordered recruitment gate are already present on main. Main's upstream-artifact paragraph is more specific than the branch snapshot. Its remaining differences are stale audit/handoff checkpoint notes; no unique recruitment or corpus change was ported.
- `docs/khmer-parser-source-registry-and-handoff-v2-2026-11-16`: its source registry is an older, materially shorter snapshot than main's current registry; its provenance test has fewer assertions than main; and its parser/LOC/Unicode audit notes carry earlier implementation SHAs and CI counts. No source record, test or parser change was missing from main in the inspected files.
- `docs/post-pr319-expert-shortlist-closeout-2026-11-17` and `docs/historical-branch-audit-closeout-2026-11-15`: their candidate-screen and branch-audit notes are historical checkpoints already superseded by later canonical documentation. The expert shortlist remains candidate screening only; no outreach or appointment is evidenced.
- `docs/current-pcgn-branch-family-inventory-2026-11-19`, `docs/non-pcgn-fix-branch-triage-2026-11-19`, `docs/closeout-tn61-source-registry-and-docs-branch-audit-2026-11-18`, and `docs/final-2026-11-19-mainline-ci-and-branch-status` contain older handoff/register/audit snapshots; the relevant branch-family findings are represented in the canonical current-main audit, with newer or corrected state where applicable.

These are targeted content dispositions, not a complete semantic or commit/PR-ancestry audit of all 134 `docs/*` refs. `KHM-BRANCH-AUDIT-001` therefore remains **PARTIAL**. No historical branch was deleted, force-updated, or merged wholesale; no unsupported IPA or linguistic evidence was added.

Exact-main workflow recheck for `f5faae81078e2828bc069bddda1ec05b95de5ff1`:
- Quality checks run [44501861035](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44501861035): **SUCCESS**.
- Khmer browser smoke run [44501860981](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44501860981): **SUCCESS**.
- GitHub Pages build/deploy and deployed-site/runtime smoke run [44501861093](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44501861093): **SUCCESS**.

At this checkpoint there are **0 open pull requests** and Issue [#104](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/104) remains the sole open issue. Its human acceptance gates remain unmet: approved versioned IPA convention, qualified independent reviewers/annotators/adjudicator/curator, private blind intake, item-level rights-cleared 30-item pilot and adjudication. Gold remains 0 and empirical accuracy remains null. Repository classification remains research-ready partial prototype, not linguistically release-ready.


## Further documentation-branch semantic spot checks — 2026-11-19

Continued the `docs/*` branch reconciliation beyond the representative branches recorded above. Compare metadata was used to identify each branch's changed paths, then content was inspected for branches touching source registries, the romanization matrix, parser/Unicode evidence, phonology, architecture, accessibility and external benchmarks. A branch's ahead count was not treated as evidence of unique implementation.

Additional dispositions:

- `docs/direct-romanization-input-closeout-2026-11-15`: its branch copy of `docs/romanization-to-ukrainian-matrix.md` is a 265-line earlier snapshot versus the current 944-line matrix. It predates later PCGN source rows, explicit profile/exception reconciliation, and subsequent engine/test scope clarifications. The branch-only old paragraphs are superseded; no runtime or matrix content was missing from main.
- `docs/khmer-1997-profile-evidence-reconciliation-2026-11-12`: its `data/khmer/sources.json` has 29 records versus 49 on main. It has no source IDs absent from main. Main contains 20 additional source records and materially fuller provenance/rights/limitations for MekongPhon, Kirby audio/supplementary material, open-dict-data and the Chemvatho acoustic-model lead. Shared MekongPhon and Kirby records have expanded scope and provenance in main. No unique source record or evidence was ported from this old branch.
- `docs/khmer-unicode18-parser-final-handoff-2026-11-16` and `docs/khmer-parser-final-state(-v2)-2026-11-16`: the branch README describes only the earlier component scanner and explicitly says multiple unstacked consonants remain evidence-limited; main now documents the separately implemented Unicode 18 §16.4 parser and packed parse forest while retaining the limits on phonological syllables, lexical word boundaries, IPA and Ukrainian output. Its TN #61 v2 rights caveat is already represented more fully in the main source registry, including `rights_status=PUBLIC_DISTRIBUTION_PERMISSION_NOT_ESTABLISHED`. No parser code or missing source evidence was identified.
- `docs/repository-information-architecture-2026-11-15`: `AGENTS.md`, `docs/agents/codebase-map.md` and `docs/agents/methodology-references.md` are identical to main. The branch README and architecture note are older and omit current Pages-only deployment, typed external IPA candidate safeguards, packed orthographic parse-forest detail, and the newer literature/source index. Main is the more complete state.
- `docs/post-pr353-mainline-closeout-2026-11-18`: its external acoustic-model description predates the mainline pinned-revision audit. Main records the contradictory 29,204/33,091 counts, six-line sample-only tree, absent full artifacts and conflicting data-license statements. No missing benchmark evidence was ported.
- The PCGN closeout family (including `docs/pcgn-ba-aa-foot-closeout-2026-11-19`, `docs/pcgn-ba-series-vowel-crosslayer-closeout-2026-11-19`, `docs/pcgn-candidate-parity-row7-foot-delta-closeout-2026-11-19`, and the row-7/shifter/vowel closeouts) carries earlier versions of the canonical rule-diff, handoff and completion register. Main includes the later source-row corrections, BA/BAa exception tests, dependent-vowel integration, row-7 exact codepoint sequence and the PCGN-vs-UNGEGN comparison. No PCGN runtime or regression change was unique to these documentation branches.
- The many `docs/post-pr*-mainline-*` and `docs/pr*-closeout-*` refs are historical verification snapshots. Their compare results show changes confined to handoff/register/audit and, in some cases, the romanization matrix; the selected snapshots are older than the corresponding current-main evidence. They are retained as history, not merged as competing canonical state.
- `docs/phonotactic-research-closeout-2026-11-15`: its phonology note is superseded by main's typed `ipa_kind` convention boundary, which explicitly leaves linguistic units UNRESOLVED pending expert approval and distinguishes provider declarations from adjudication.

This extends semantic sampling but does **not** complete a line-by-line content review and full commit/PR ancestry reconciliation for every one of the 135 live `docs/*` refs. `KHM-BRANCH-AUDIT-001` remains **PARTIAL**. The historical refs were preserved; no branch deletion, force-push, wholesale merge, new IPA claim or corpus import was performed.

## Exact-main CI confirmation after PR #439 — 2026-11-19

Default branch `main` at `8c166792a180483bc849b122c6b310b4a83eb2c7` has all three required workflows completed successfully:
- Quality checks [44513448213](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44513448213): **SUCCESS**.
- Khmer browser smoke [44513448302](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44513448302): **SUCCESS**.
- GitHub Pages build/deploy [44513448288](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44513448288): **SUCCESS**, including production Chromium exercise, Pages artifact upload/deployment and deployed-site checks.

The repository still has no open pull requests. Issue [#104](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/104) remains open and unchanged; the IPA convention, independent reviewers/annotators/adjudicator/curator, private blind intake, rights-cleared pilot and adjudication remain human blockers. Gold remains 0; empirical accuracy remains null. Current status is research-ready partial prototype, not linguistically release-ready.


## Mainline checkpoint after PR #440 — 2026-11-19

PR [#440](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/440) merged to `main` as `e3837e036584e3c243f098781d7b24f377090663`. The change extends documentation-branch semantic sampling; it does not close the historical branch audit.

Live inventory at the preceding post-merge checkpoint: 314 refs, 314 unique branch names and 314 unique tip SHAs; no open pull requests. The prior targeted semantic review has not yet inspected every one of the 135 `docs/*` refs or fully reconciled each ref's commit/PR ancestry. `KHM-BRANCH-AUDIT-001` remains **PARTIAL**. Historical refs are preserved; no branch deletion, force update or wholesale merge was performed.

Exact-main GitHub Actions for `e3837e036584e3c243f098781d7b24f377090663`:
- Quality checks [44519884661](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44519884661): **SUCCESS**.
- GitHub Pages build/deploy [44519884653](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44519884653): **SUCCESS**.
- Khmer browser smoke [44519884652](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44519884652): first attempt failed during `Install Chromium` (`npx playwright install --with-deps chromium`); checkout, dependency install, deterministic web checks and production build had succeeded. The failed browser job was explicitly re-run as attempt 2 (job retry requested successfully); at the time of this update, attempt 2 is **IN_PROGRESS**, so Chromium verification is not yet claimed.

Issue [#104](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/104) remains open. Its latest recorded state still has no approved versioned IPA convention, no confirmed independent annotators/adjudicator/curator or private blind intake, and no rights-cleared/adjudicated 30-item pilot. Independent adjudicated gold remains **0** and empirical accuracy remains **null**. Root repository licensing still requires the owner's decision; manual accessibility review remains partial. No new IPA, phonological labels, Ukrainian mappings, corpus rows or benchmark scores were introduced.

The repository remains an engineering-verified, research-ready partial prototype, **not linguistically validated or release-ready**. No local checkout or local test execution is claimed; verification evidence above is from hosted GitHub Actions.


## Accessibility documentation-branch spot checks and live inventory — 2026-11-19

A further targeted review compared four retained accessibility closeout refs against current `main`:

- `docs/pr389-accessibility-landmarks-closeout-2026-11-18` changes only the three canonical handoff/audit/register documents. Its record documents the earlier automated structural checks (document language, one main landmark/H1, accessible-name sources and image alt attributes) and explicitly limits their scope; it does not add a unique implementation commit relative to current main.
- `docs/pr392-accessibility-whitespace-closeout-2026-11-18` likewise changes only those canonical documents. Its record describes the regex whitespace parsing correction already in the mainline history; no unique source or test file is introduced by this documentation ref.
- `docs/skip-navigation-closeout-2026-11-17` and `docs/wcag-contrast-closeout-2026-11-17` are documentation-only historical snapshots. Their records describe the skip-link implementation and the bounded text-contrast palette/tests, which are already part of mainline history. The WCAG contrast evidence is limited to the specific tested text/background pairs, not a full WCAG audit.

Disposition: retain all four refs as historical records; do not merge their older canonical snapshots or port duplicate implementation. This is a targeted documentation-branch content review, not full ancestry reconciliation for every docs ref.

Fresh paginated live branch inventory: **315 refs, 315 unique branch names, 315 unique tip SHAs; 137 refs use the `docs/*` prefix**. The inventory includes the current documentation continuation branch/PR #441. This is a live count, not a claim that all 137 documentation branches have been semantically reviewed. `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.


## Mainline PR #441 closeout and additional documentation-branch dispositions — 2026-11-19

PR [#441](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/441) merged by squash as `8c5b4ab223014bb2292a2e45e9b026a6e85757ed`. It synchronizes the canonical handoff, repository audit and linguistic completion register with PR #440's exact-main CI outcome and adds the accessibility documentation-branch spot checks. Its scope is documentation only.

Exact PR #441 head `76fc232792d9f8aac2daf0ba86f765470ae52db8`:
- Quality [44537589136](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44537589136) — **SUCCESS**.
- Khmer browser smoke [44537589184](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44537589184) — **SUCCESS**.
- Additional Quality push run [44537557821](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44537557821) — **SUCCESS**.

The previously failed browser smoke for PR #440's main SHA `e3837e036584e3c243f098781d7b24f377090663` was retried as attempt 2 and then completed **SUCCESS**. Attempt 1 had failed only during Chromium installation; the browser test itself was not reached on that attempt.

Exact current-main verification on `8c5b4ab223014bb2292a2e45e9b026a6e85757ed`:
- Quality [44537942760](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44537942760) — **SUCCESS**.
- GitHub Pages build/deploy [44537942921](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44537942921) — **SUCCESS**.
- Khmer browser smoke [44537942949](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44537942949) — **SUCCESS**.

### Further targeted documentation-ref checks

Six additional historical documentation refs were compared with current main and relevant content inspected:

- `docs/record-pcgn-anusvara-assembly-port-2026-11-18`: documentation-only branch snapshot. Its record describes the eight-row anusvara/visarga syllable assembler already integrated via PR #351, including schema, exports and abstention tests. No unique implementation is absent from main.
- `docs/closeout-tn61-source-registry-and-docs-branch-audit-2026-11-18`: historical checkpoint from an earlier base with 103 docs refs. Its TN #61 alias/source metadata reconciliation is superseded by PR #365 and the current canonical source registry; the alias is represented on main without a duplicate source record. Its old inventory and CI state are not current.
- `docs/romanization-mainline-ledger-reconciliation-2026-11-12`: older branch snapshot that modifies the romanization matrix as well as the three canonical documents. Its branch-only matrix/register statements describe the earlier partial ASCII adapter, old mark/numeral task state and pre-reconciliation national-1997 caveat; current main contains the later matrix, runtime and explicit profile caveat. No unique current implementation or source evidence was identified to port.
- `docs/pr402-postmerge-closeout-2026-11-19` and `docs/pr406-exact-main-closeout-2026-11-19`: documentation-only historical closeouts whose rule/test and exact-main CI records are superseded by later canonical checkpoints already on main. No runtime/test patch is unique to these documentation refs.
- `docs/pr427-exact-main-closeout-2026-11-19`: compare reports the branch is behind current main with no changed files; no port is applicable.

These are content dispositions for the named refs, not a full line-by-line review or ancestry reconciliation of every documentation ref. Retain historical branches; do not merge stale snapshots wholesale or delete/force-update branches.

Latest paginated inventory remains **315 refs / 315 unique names / 315 unique tips**, including **137 `docs/*` refs**. There are no open PRs after #441. `KHM-BRANCH-AUDIT-001` remains **PARTIAL** because the remaining docs refs and complete PR/commit ancestry still require reconciliation.


## PR #442 closeout and next historical documentation-ref sample — 2026-11-19

PR [#442](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/442) merged by squash as `23c41163b5ea5b9cc1b835283b03c7dceddec7d6`. It records the PR #441 closeout, the successful retry of PR #440's Chromium installation attempt, exact-main CI on `8c5b4ab223014bb2292a2e45e9b026a6e85757ed`, and six additional targeted documentation-ref dispositions. Scope is documentation only.

Correction to the previous interim status: Chromium smoke on `e3837e036584e3c243f098781d7b24f377090663` did **not** remain failed. Retry attempt 2 succeeded; the original failure was limited to the Chromium installation step before browser tests began. On the subsequent exact-main SHA `8c5b4ab223014bb2292a2e45e9b026a6e85757ed`, Quality, Pages and Chromium all passed (runs 44537942760, 44537942921 and 44537942949 respectively).

### Further targeted documentation-ref checks

- `docs/accessibility-smoke-closeout-2026-11-15`, `docs/close-shared-fallback-parity-task-2026-11-17`, `docs/closeout-mixed-script-boundaries-2026-11-17`, `docs/historical-branch-audit-closeout-2026-11-15`, `docs/khmer-fallback-parity-mainline-closeout-2026-11-17`, and `docs/sok-adams-rule-audit-mainline-closeout-2026-11-17`: compare results show only older snapshots of the canonical handoff/audit/register documents. Their branch-only implementation/status notes are historical; no source, runtime or test path unique to these refs was identified. Retain as history; do not merge stale snapshots wholesale.
- `docs/correct-khmer-nova-tokenization-scope-2026-11-17`: its lexical-segmentation evidence audit is byte-for-byte line-identical to current main. No port is applicable.
- `docs/ipa-gold-recruitment-execution-kit-2026-11-18`: its playbook contains an older summary of the Chemvatho acoustic-model candidate. Main supersedes that summary with pinned-revision evidence: conflicting 29,204/33,091 counts and CC BY-SA/CC BY statements, only a six-line sample dictionary in the public tree, and no full dictionary or reproducible artifact. The old branch's generic claim that the candidate is a promising 29,204-entry CC BY-SA dictionary is insufficient and potentially misleading; no evidence or recruitment protocol unique to that branch needs porting. Issue #104 still requires actual human recruitment and rights clearance.
- `docs/khmer-canonical-matrix-parity-closeout-2026-11-12`: an older two-file closeout; its changes are historical status prose, with no runtime or source-registry implementation missing from main.
- `docs/pcgn-robat-closeout-2026-11-16`: its romanization matrix is a 921-line earlier snapshot versus 944 lines on main. The current matrix contains later independent-vowel closed-syllable assembly, exact bounded API/schema/tests and the separate Unicode 18 BNF/LOC word-division evidence boundaries. The branch-only lines add no unique current implementation or evidence.

These are targeted content dispositions, not a full line-by-line review or PR/commit ancestry reconciliation of all live documentation refs. Current paginated inventory after PR #442: **316 refs, 316 unique names, 316 unique tips, including 138 `docs/*` refs**. No open PRs. `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.

Exact-main workflows on the new merge SHA `23c41163b5ea5b9cc1b835283b03c7dceddec7d6` were triggered and were still running at the time of this update; do not mark this SHA CI-verified until all three complete successfully.


### Parser/source-registry and romanization historical refs — additional sample, 2026-11-19

- `docs/continue-docs-branch-audit-and-ci-2026-11-19`, `docs/current-pcgn-branch-family-inventory-2026-11-19`, `docs/non-pcgn-fix-branch-triage-2026-11-19`, `docs/finalize-external-source-audit-2026-11-17`, and `docs/final-sok-ipa-kind-verification-2026-11-17`: these compare as older snapshots changing only canonical handoff/audit/register files. They do not introduce source code, tests, or evidence absent from main; retain as historical records.
- `docs/khmer-parser-source-registry-and-handoff-2026-11-16` and its v2 ref: both contain older source-registry snapshots (526 and 526 lines respectively versus 631 on main for the v1 comparison). Main's registry includes more complete pinned-revision evidence and explicit limitations/rights statuses for MekongPhon, Headley-derived material, Kirby audio/research data, OpenSLR and Chemvatho. The old entries' broad claims and shorter limitations are superseded; no source ID or parser rule absent from main was identified in the inspected diff. Their parser/LOC/Unicode evidence documents are historical snapshots; current main retains the later BNF and word-division scope boundaries. The v2 ref also changes README, but its parser status is superseded by current README/mainline records. No code/test port was justified from these historical refs.
- `docs/romanization-postmerge-evidence-2026-11-12`: two-file historical closeout; no unique implementation file in the branch diff.
- `docs/romanization-target-table-sync-2026-11-12`: its only changed matrix is a 298-commit-behind snapshot; current main's 944-line matrix includes subsequent engine/test and PCGN source reconciliation. No branch-only matrix line was needed.
- `docs/romanizer-output-guard-closeout-2026-11-15`: the branch's 277-line matrix is a much earlier snapshot. Main's 944-line matrix adds the full contextual mark inventory (including BANTOC and SAMYOK SANNYA under PCGN Note 5), the bounded direct-input and independent-vowel assembly contracts, and later PCGN/UNGEGN reconciliation. The old matrix contains no unique current rule or test evidence to port.

All these dispositions are targeted, based on changed-path comparison and inspection of the relevant registry/matrix files; they do not complete the full historical branch ancestry audit. Do not copy older source metadata into main or treat upstream corpus claims as permission to import data.


## PCGN documentation-ref spot audit — 2026-11-19

Ten retained PCGN documentation refs were compared with current main. Their changed paths are canonical documentation only; no unique code, tests, source rows, IPA labels, Ukrainian mappings or corpus material were identified for porting. Historical BA+AA/foot, vowel, Note 5, UNGEGN comparison, profile-delta and row-7 closeouts are superseded by the current mainline implementation and source-backed regression evidence.

The current PCGN resolver was checked directly: `PCGN_WEAK_SUBSCRIPTS` excludes `ស`, and the structural `គ្ស` regression records the PCGN-specific series-determining foot behavior. The exact PCGN row-7 sequence remains `េ+ា+ះ`; the UNGEGN candidate's distinct key is not interchangeable. No runtime changes were needed.

PR #443 is merged as `f9a3dd7fdc813fbf5de8c0e674256c9a6a43ac05`. Its PR-head Quality and browser checks passed; exact-main Quality and Pages passed, while exact-main Chromium was still in progress at the time of this update. Inventory: 317 refs / 317 unique names / 317 unique tips / 139 `docs/*` refs. The full historical branch audit remains **PARTIAL**; no linguistic gold, license or external rights status changed.


### Post-merge documentation branch family (#206–#259)

Twenty-nine historical refs in the `docs/post-pr*` family were compared with current main. Changed paths are canonical documentation plus older snapshots of `docs/romanization-to-ukrainian-matrix.md`; no implementation or test files differ. The old matrices are line-subsets of current main apart from superseded status notes: a pre-Note-2 implementation statement on #215 and a stale in-progress CI note on #223. No unique mapping or source-backed rule was found to port. Retain all branches unchanged. This is targeted compare/content evidence only; repository-wide branch/PR ancestry audit remains **PARTIAL**.


## Post-merge documentation branch review — #294–#355

Ten refs (#294, #300, #314, #316, #319, #353, #322, #334, #336 and #355) were compared with current main. All diffs are documentation-only. The #294 Unicode grammar/TN #61 checkpoint is superseded by current parser and rights-scoped metadata records. The #353 benchmark note's 29,204-entry/native-validated/CC BY-SA statement is contradicted by the pinned source audit (29,204 vs 33,091, conflicting license scopes, six-line public sample, no full artifact) and must not be reintroduced. Other closeout refs contain older status/CI snapshots only. No runtime, test, IPA, Ukrainian or corpus change is warranted. `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.


### PR closeout documentation refs (#357–#393)

Ten refs (#357, #359, #362/#363, #366, #367, #378, #389, #390, #392 and #393) were compared. Only canonical docs differ; all handoff content is already present in current main (zero branch-only lines). No code, test or source evidence needs porting. Retain branches; `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.


### Test branch reconciliation

Twenty-six retained test branches covering accessibility, grapheme accounting, IPA display, Khmer numeral/romanization, onset fallback and PCGN regressions were compared with main. No missing test-only change was identified. Onset-fallback source/data/tests and IPA display contract are byte-identical; older grapheme/romanization adapters are superseded by current richer code/tests; stale PCGN vowel fixtures and all-row equality assertions are superseded by corrected source values and row-specific comparison semantics. The `ស`-foot and SAMYOK coda tests are already present. Branches remain unchanged.

Exact-main Pages/deploy on `e78da940dbff2a07376f6ae9cb0b4cc4cd8b6603` subsequently passed (run 44558019521); Quality and Chromium on the same SHA also passed. Repository-wide historical branch audit remains **PARTIAL**.


### Early romanization and source-registry branch review

Ten older refs (#1997 profile, phonotactics, letter inventory, numerals, onset registry, short-vowel, vowel matrix, whole-message, runtime and test closeouts) were compared. The #1997 branch's 29 source IDs are a strict subset of the current 49-entry registry; no source ID is missing. Old matrices/status notes are superseded by the current 944-line matrix, current national-1997 evidence caveat, and diacritic-preserving direct input. The old phonology snapshot has no unique lines; current main includes the typed IPA-kind contract. No code/test/source change is warranted. Retain refs; `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.


### PCGN assembly/direct-input branch sample

Ten refs covering alif assembly, closed syllables, Note 5, independent vowels, shifter uncertainty/registry, shortened marks, inventory, direct romanization input and fallback parity were compared. All are documentation-only. Four near-current matrix snapshots (888–932 lines) are strict subsets of current main; older matrix statements are superseded by current mark inventory and direct-input contract. No unique implementation or source evidence was found. Retain refs; `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.


### Architecture/deployment/handoff docs branch review

Ten refs (#ipa-validator, #typed-hybrid-bridge, #repository-information-architecture, #final PR #320, #site deployment, #Pages live, #grapheme accounting, #mark inventory, #mixed script, #skip navigation) were compared. The repository-information-architecture branch's AGENTS/docs index/agent maps and handoff are subsets of main; README/architecture and PR #64 status lines are outdated. Remaining refs are canonical documentation or older README snapshots only. No unique code/test/source requirement was found. Retain refs; `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.


Data-level verification: the early candidate-diff branch still marks row 7 as candidate-shaped `ោ+ះ` / `MATCH`; main uses PCGN `េ+ា+ះ` / `VALUE_MATCH_KEY_SHAPE_DIFFERS`. Three later parity branch CSVs match main exactly. The stale row is not portable.


### Exact-main/checkpoint branch review

Ten exact-main and branch-audit checkpoint refs were compared. Their handoff files are strict line subsets of current main (zero branch-only lines); diffs affect only canonical status docs. Historical branch counts, SHAs and CI states are not current evidence. No unique code, source or test changes. Retain refs; `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.


Current inventory: 320 refs, 320 unique names/tips, 142 `docs/*` refs; one open PR (#446). This does not close the full branch audit; `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.


## PR #445 and parser handoff closeout

PR #445 merged as `3663ea20e58510a0a36b5c521627fcacf1c4951b`; Quality, Pages and Chromium all passed on exact main. Four parser handoff refs were reconciled. The old `unicode-tn61-v2` ID is superseded by the canonical renamed source ID; current main has the later source records. The old scanner-only/TODO parser state is superseded by the DONE_VERIFIED Unicode 18 packed parse forest, with current tests preserving the orthographic contrast, 2^20 derivations and rejection spans. No code or evidence needs porting. Full branch audit remains **PARTIAL**.


### Mainline/PCGN closeout refs

Ten refs were compared. Changes are canonical documentation only; one exact-main quality-count branch has no diff, and nine handoff snapshots are strict subsets of main. The #430 branch's older PCGN fix-family notes and 305-ref inventory are superseded by the current main PCGN branch-family audit and later 306/308/319-ref counts. No code/test/source change needs porting. Retain refs; `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.


## Audit branch and PCGN comparison snapshot

Nine audit branches have zero branch-only content in the three canonical docs compared with main. The PCGN/UNGEGN row-reconciliation branch is stale: it treats row 7 as a simple match despite different source structures (`េ+ា+ះ` vs `ោះ`) and lacks current source-registry parity tests. Main correctly classifies it as `VALUE_MATCH_KEY_SHAPE_DIFFERS`. No port is warranted; all refs retained. Full historical ancestry review remains **PARTIAL**.


### Additional audit-family branch sample

Nine further audit refs were compared; each handoff file is a strict subset of current main (zero branch-only lines). The `complete-remaining-branch-families` ref has no diff. No implementation or unique documentation content needs porting. Retain refs; `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.


## Research branch sample and exact-main verification

PR #448 merged as `47b3be71478c5a6948a2c66c4761cce9310a5fcb`; exact-main Quality, Chromium and Pages/deploy succeeded (44565926529, 44565926669, 44565926377).

Ten research source-registry snapshots have no source IDs absent from current main's 49-entry registry. The renderer branch has an old smaller registry but current schema/test. The older hybrid branch is superseded by typed v2 IPA candidate validation. The older benchmark runner allows model-ID overrides and lacks current corpus-source pinning; the dedicated MekongPhon diagnostic script/tests match main exactly. The older PCGN note registry is a 10-row subset, superseded by the larger current registry and stronger tests. No code/source/test port is appropriate. Research family audit and full historical ancestry remain **PARTIAL**; no gold/accuracy claim is made.


## Fix-branch sample

Non-PCGN fix refs for typed IPA, romanizer output guards, IPA tie-bar boundaries, benchmark provenance, parser diagnostics/rejection spans, numeric passthrough, unmodeled letters and mixed-script boundaries were compared. Multiple files/tests match main byte-for-byte. Older branches lack current numeric passthrough, richer benchmark provenance, current parser diagnostics and shared Khmer-output guard. No unique accepted code/test change needs porting. Refs remain untouched; full fix/PR ancestry review remains **PARTIAL**.


## Feature-branch review and historical-note correction

Ten feature branches were checked. The Unicode 18 parser and typed IPA candidate branches are older than current packed-forest and tie-bar validation implementations. The typed hybrid bridge, practical adapter and Ukrainian matrix files match main byte-for-byte. The old subscript parser is superseded by the current scanner/tokenizer. Two older PCGN assembly branches incorrectly preserve BA+TRIISAP p-in-â; main applies Note 2 no-shift and Note 3 BA+MUUSIKATOAN/BA+foot exceptions.

Correction: the current live feat/pcgn-anusvara-visarga-syllable-assembly-port branch does not have PCGN implementation/schema/test blobs identical to main (only package exports match). It contains the superseded BA+TRIISAP behavior. Do not port. Full feature-family semantic/ancestry audit remains PARTIAL.


Exact-main verification correction: PR #450 merge SHA aeb0bfbaabc47d8658527da4c5634fae12e9faec later passed Quality 44568314352, Chromium 44568314381 and Pages/build/deploy 44568314462; Quality retry 44568901376 also passed.


### Branch inventory snapshot — 2026-11-19

At the PR #451 pre-merge checkpoint: 325 refs, 325 unique names and tip SHAs, 142 docs/* refs; prefix counts include 44 audit, 50 feat, 29 research, 26 test and 24 fix refs. One PR (#451) was open. KHM-BRANCH-AUDIT-001 remains PARTIAL.


## Additional audit-ref and stale PCGN snapshot disposition

Fourteen audit refs (late-docs, docs-family, historical, PCGN, typed-IPA/coverage, inventory, final-session, PR #379–#381 and PR #153 reconciliation) have only canonical documentation diffs. Their handoff content is already on current main (zero unique lines). One further branch is an ancestor with no diff.

The PCGN/UNGEGN row reconciliation branch is stale: it asserts all eight anusvara/visarga rows are full matches, whereas current main correctly identifies row 7's PCGN sequence `េ+ា+ះ` and distinct candidate key `ោះ` as `VALUE_MATCH_KEY_SHAPE_DIFFERS`. Current main's tests enforce row-specific comparison and source registry parity. Do not port the old test or CSV.

PR #451's feature audit correction is retained: the old PCGN syllable assembly feature ref has a superseded BA+TRIISAP p-in-â exception; main follows PCGN Note 2 no-shift and Note 3 BA+MUUSIKATOAN/BA+foot exceptions. Full branch/PR ancestry review remains **PARTIAL**.


### Final sampled audit refs

Thirteen further audit refs contain only canonical documentation changes. Twelve have zero unique handoff lines; the selected historical snapshot's two unique lines are obsolete inventory/PR-count metadata. The optional Khmer Phonemizer workflow in the restore branch is already byte-identical on main (blob SHA `a89a848d66810225bbcc2cc5c9143b94304a680d`). No branch-only implementation should be ported. Exact-main CI for PR #451's merge SHA was pending at documentation time. `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.


## Research branch disposition

All 29 research refs were included in a targeted changed-path review. The checked source-registry snapshots add no IDs absent from current main's 49-entry registry. The external renderer schema is identical and the current main registry is substantially expanded. Old MekongPhon hybrid and benchmark code is superseded by the current typed, evidence-gated adapter and pinned diagnostic harness; the old workflow's additional raw-output run over 100 upstream source-attested rows was not imported because those rows are not independently adjudicated gold and corpus rights remain unverified.

IPA convention draft, Kirby audio audits, literature review and PCGN/UNGEGN research notes are present on main where checked. Lexical segmentation, Unicode grammar, Sok-Adams and LOC documents are more complete on main than the historical snapshots. Their old TODOs are superseded, but the actual blockers (IPA gold, expert convention approval, licensed lexical evidence and segmentation annotation) remain open.

No unique accepted implementation was found to port. Branches preserved. Full commit/PR ancestry review remains **PARTIAL**.


## Data and fix branch disposition

The positional-onset evidence files and independent-vowel CSV are byte-identical to main. The row-7 source-pattern runtime/schema, BA/TRIISAP source matrix, dependent-vowel CSV, shortened-mark inventory and TN #61 metadata are also already present.

Do not port the stale dependent-I/O resolver (incorrect O-series values for rows 16/17 and old row-7 key) or the BA+TRIISAP p-in-â exception in older final-consonant/omitted-shifter branches. Current main correctly applies PCGN Note 2 no-shift and Note 3 BA+MUUSIKATOAN/BA+foot. Historical refs retained; full branch/PR ancestry audit remains **PARTIAL**.


## Feature branch disposition

Fifty feature refs were reviewed. The parser/BNF/forest, rejected-span, romanization/practical adapter, typed IPA/hybrid, coverage/dashboard, renderer and PCGN component/note/assembly branches are older snapshots of current mainline functionality. Current main has richer Unicode 18 parser semantics, typed IPA validation, expanded source-backed PCGN resolution, and stronger data/test contracts. Stale PCGN branches contain superseded BA+TRIISAP p-in-â behavior and/or incorrect dependent-vowel/row-7 mappings; do not port.

The browser-side `src/hybrid-engine.js` on the old Pages hybrid-candidate-shell branch is not present on main. No acceptance requirement for this separate UI was found in the canonical execution plan; current main's Python typed hybrid adapter is the supported diagnostic boundary. Classify the prototype **DEFERRED**. Profile-neutral boundary evidence is already integrated but does not segment words.

No feature branch altered; full PR ancestry review remains **PARTIAL**.

### Ancillary branch families and final test-ref count — 2026-11-19

The final test-family inventory contains 26 refs, not 25. The additional `test/ui-accessibility-smoke-2026-11-15` branch changes only `tests/browser/site.spec.js`. Its branch-only check for visibly withheld mixed input is superseded by current main's more specific unsupported-grapheme, neighboring-output preservation, mixed-script ordering and direct-romanization mixed-input tests; current main additionally includes WCAG contrast and keyboard smoke coverage. No test needs porting.

Three remaining singleton refs were also dispositioned:
- `benchmark/current-engine-2026-11-11` adds a manual benchmark workflow comparing the deterministic engine with upstream MekongPhon and Neurlang source-reported IPA. The report labels results as source-attested concordance, not gold accuracy. The canonical plan explicitly defers this benchmark pending independent adjudication and source/rights review; do not import the workflow as a release gate.
- `ci/khmer-g2p-smoke-2026-10-24` is an older optional G2P workflow snapshot. Current main has the later pinned manual benchmark workflow and separate optional Khmer Phonemizer raw-output workflow.
- `release/deterministic-rule-engine-2026-11-11` is an older rule-engine release snapshot. Current main has a substantially expanded deterministic engine, typed IPA/uncertainty boundary, tests and documentation; no unique release implementation needs porting.

The browser-side hybrid candidate shell remains DEFERRED as noted above. These dispositions do not close external gold, licensing, IPA-convention or lexical segmentation blockers.


## Fix/test and singleton branch disposition

Twenty-four fix refs were compared by changed path; current main contains the later typed IPA, Unicode parser/rejection, mixed-script and PCGN implementations. Stale PCGN snapshots must not be ported: incorrect O-series values for dependent rows 16/17, the old two-component row-7 key, and BA+TRIISAP p-in-â are superseded by the exact PCGN source sequence and Note 2/3 distinction.

The test family contains 26 refs. The last accessibility smoke branch's mixed-input withholding check is superseded by current main's more specific unsupported-grapheme, partial-result and mixed-script browser tests, plus keyboard/contrast smoke coverage.

The benchmark workflow against MekongPhon/Neurlang is a source-attested concordance diagnostic, not gold accuracy, and remains DEFERRED pending independent gold and rights. The old optional G2P workflow and deterministic engine release snapshot are superseded by current main. Historical branches retained; `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.


## Data/source and PCGN branch checks

Positional-onset registry, schema and tests are byte-identical to main; 33 specialist-reference onset hints remain preview-only and not canonical IPA. PCGN independent-vowel CSV and resolver test are byte-identical to main; Note 9's `ŏ|ŭ` remains unresolved without reference selection. The pinned Khmer Phonemizer smoke workflow is also already in main.

The PCGN/UNGEGN audit branch is stale: it incorrectly treats anusvara/visarga row 7 as a full match and requires all eight rows to match. Current main correctly marks the distinct PCGN sequence `េ+ា+ះ` vs candidate key `ោះ` as `VALUE_MATCH_KEY_SHAPE_DIFFERS`, and adds source-registry parity tests plus the PCGN `ស`-foot distinction. Do not port stale files.

Feature/fix/research audit snapshots contain no branch-only handoff content. The unique current-engine benchmark workflow is DEFERRED pending independent gold/rights; the older G2P smoke workflow is superseded. All refs retained. `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.


## PR #458 exact-main CI and live branch count

PR #458 merge SHA `c4286ccd425627ef0771f87d0a38f594b7335074` passed exact-main Quality (44602000654), Chromium (44602000538) and Pages/deploy (44602000536). Its PR head also passed Quality and Chromium; no open PR remained.

Live branch inventory: 332 refs, 332 unique names and tips — 149 docs, 44 audit, 50 feature, 29 research, 26 test, 24 fix, 4 data, 2 accessibility and four singleton/unprefixed refs. No historical branches were deleted or rewritten. `KHM-BRANCH-AUDIT-001` remains **PARTIAL** because full commit/PR ancestry review is not complete.


## PR #459 exact-main verification and stop-condition status

PR #459 merge SHA `c0fb6f8efcadf20ff55aec58b1188144707ae52f` passed Quality (44602788321), Chromium (44602788413) and Pages/deploy (44602788487). Its exact PR head passed both Quality checks and Chromium.

Live branch inventory: 333 refs, unique names and unique tips; 150 docs, 44 audit, 50 feature, 29 research, 26 test, 24 fix, 4 data, 2 a11y, and four singleton/unprefixed refs. No open PRs at this checkpoint. Branches retained.

Unresolved blockers: independent adjudicated IPA gold, approved IPA convention, human recruitment/blind pilot under Issue #104, external source/data rights, owner decision on root license, lexical segmentation evidence and manual accessibility review. Full historical ancestry review remains **PARTIAL**. The project is a research-ready partial prototype, not release-ready.


## Contextual vowel registry schema — 2026-11-20

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHMER-VOWEL-REGISTRY-SCHEMA-001 | DONE_VERIFIED (data-integrity contract only) | Exact final PR head `45fc31321d3628aa5afb61892802a8f9f20b3eb1`: Quality [44721843510](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44721843510) SUCCESS (446 Python tests + 70 subtests, web checks, production build); Chromium [44721843530](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44721843530) SUCCESS. Schema validates the 9 existing source-indexed cases; tests unique IDs, source references, evidence/status parity, non-gold status and conflict withholding. | This verifies record shape and provenance/status invariants only; it is not phonetic validation or completion of the contextual vowel matrix. |
| KHMER-VOWEL-CONTEXT-MATRIX-001 | PARTIAL | Existing source register and coverage report preserve bounded source examples and the dependent-sign × series inventory. | Full source-located contextual matrix still requires syllable type, coda, length, stress/harmony, profile and phonemic-vs-phonetic distinction; missing cells remain NOT_ESTABLISHED until evidence is supplied. No extrapolation from Unicode structure. |

No new IPA values, gold records, source permissions, Ukrainian mappings or runtime rules were introduced. Independent adjudicated IPA gold remains 0; empirical accuracy remains null.


### KHMER-VOWEL-REGISTRY-SCHEMA-001 CI dependency correction — 2026-11-20

The initial Quality run failed at test collection because `jsonschema` was not installed by the existing CI command. The test-only dependency is now declared in `pyproject.toml` and CI installs the `.[test]` extra. Status remains PARTIAL until the rerun passes Python, web checks and production build on the final PR head. The initial failure is not counted as a successful test.


Exact-head closeout: the initial Quality run failed because `jsonschema` was absent from the test environment; after declaring the test-only `.[test]` extra and updating CI installation, Quality and Chromium both passed on `45fc31321d3628aa5afb61892802a8f9f20b3eb1`. No runtime or linguistic data changed.

## Contextual Khmer vowel coverage inventory — 2026-11-20

| Task | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-VOWEL-CONTEXT-INVENTORY-001 | DONE_VERIFIED (case-level engineering inventory) | New `contextual_vowel_evidence` section in `reports/khmer-coverage-audit.json`, generated from the canonical case registry by `scripts/coverage.py`; matching public report; regression tests in `tests/test_coverage_report.py`. | Exposes only fields explicitly recorded in each source case. Does not establish the full vowel × series × coda × syllable × length × profile cross-product, phonological coda identity, measured duration, stress/harmony or a universal IPA rule. Independent gold remains 0. |
| KHM-VOWEL-CONTEXT-MATRIX-002 | PARTIAL | Existing source registry has nine case rows: seven SOURCE_ATTESTED_NOT_GOLD and two CONFLICTING_SOURCE_ANALYSES. New report makes each row's exact orthographic context and missing dimensions inspectable. | Complete only after source-located examples cover the required dimensions and expert adjudication approves any runtime rules. No new IPA labels or gold rows added. |



## Contextual Khmer vowel coverage — merged PR #462 — 2026-11-20

| Task | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-VOWEL-CONTEXT-INVENTORY-001 | DONE_VERIFIED (engineering inventory) | PR #462 merged as `d4738096ae05cad4e338388bfb93fa05b8855e54`; exact PR-head Quality [44733384646](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44733384646) SUCCESS (447 Python + 70 subtests), push Quality [44733376120](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44733376120) SUCCESS, Chromium [44733384573](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44733384573) SUCCESS. | Case-level evidence view only; no IPA generation, gold labels or empirical accuracy. Full contextual cross-product remains NOT_ESTABLISHED. |
| KHM-VOWEL-CONTEXT-MATRIX-002 | PARTIAL | Existing nine source-indexed rows are visible in canonical/public JSON and the system dashboard. | Requires source-located evidence across profile × series × vowel × phonological coda × syllable type × measured length × stress/harmony and expert review. |
| KHM-MANUAL-A11Y-001 | TODO (human QA) | Issue [#463](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/463) opened with manual keyboard, screen-reader, zoom/reflow, contrast and mobile checklist. | Complete manual test record, fix defects, retest. Do not infer WCAG conformance from CI. |



## Post-merge exact-main verification — 2026-11-20

| Task | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-MAIN-CI-2026-11-20 | DONE_VERIFIED | Exact main HEAD `a97381b6cd221ccb65cc7d4d118578c3f482eb54`: Quality [44734185716](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44734185716) SUCCESS (447 Python tests + 70 subtests), Chromium [44734185807](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44734185807) SUCCESS, Pages/deploy [44734185684](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44734185684) SUCCESS including deployed-site smoke. | Engineering and deployment verification only; no linguistic gold or accuracy evidence. |

## Latest mainline verification — 2026-11-20

| Task | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-MAIN-CI-2026-11-20-B | DONE_VERIFIED | Exact main HEAD `e5ea08e9bc0c9828b5da29cbd6ecb06d6e054ee0`: Quality [44734864422](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44734864422), browser smoke [44734864454](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44734864454), Pages/deploy [44734864513](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44734864513) all SUCCESS. | Engineering/deployment only. Independent gold=0, accuracy null; contextual phonology and manual accessibility QA remain PARTIAL/TODO. |

## Exact current-main verification and remaining acceptance gates — 2026-11-20

| Task | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-MAIN-CI-2026-11-20-CURRENT | DONE_VERIFIED | Exact main HEAD 0e90dcaf7d76ac1c8ad43dc6496a506af044ecc1: Quality [44736142441](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44736142441), Chromium [44736142257](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44736142257), Pages/deploy [44736142183](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44736142183) all SUCCESS. | Engineering/deployment only; no independent pronunciation gold or empirical accuracy. |
| KHM-VOWEL-CONTEXT-MATRIX-002 | PARTIAL | Nine source-indexed observations remain seven SOURCE_ATTESTED_NOT_GOLD and two CONFLICTING_SOURCE_ANALYSES; report/dashboard parity is tested. | Complete source-located coverage for profile × series × vowel × phonological coda × syllable type × measured length × stress/harmony and expert review. |
| KHM-GOLD-PILOT-001 | BLOCKED | Issue [#104](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/104). | Approved convention, two annotators, separate adjudicator and curator, blind intake, rights clearance and 30 adjudicated lexeme groups. |
| KHM-MANUAL-A11Y-001 | TODO (human QA) | Issue [#463](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/463). | Manual keyboard, screen-reader, zoom/reflow, contrast, touch-target and mobile QA; remediate and retest. |


## Final merged-main engineering verification — 2026-11-20

| Task | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-FINAL-MAIN-CI-2026-11-20 | DONE_VERIFIED | Final main [5293cdcb93b5f4f617e8a9b04d97630a128c4510](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/commit/5293cdcb93b5f4f617e8a9b04d97630a128c4510), PR #464 merged. Quality [44752921914](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44752921914), Chromium [44752921989](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44752921989), Pages/deploy [44752921857](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44752921857): SUCCESS. | Engineering and deployment only; gold and manual accessibility gates remain open. |
| KHM-VOWEL-CONTEXT-MATRIX-002 | PARTIAL | Nine source-indexed observations: seven SOURCE_ATTESTED_NOT_GOLD, two CONFLICTING_SOURCE_ANALYSES. | Complete source-located profile × series × vowel × coda × syllable type × measured length × stress/harmony coverage and expert review. |
| KHM-GOLD-PILOT-001 | BLOCKED | Issue #104; independent adjudicated gold=0, empirical accuracy unmeasured. | Approved convention, two annotators, adjudicator, curator, blind intake, item-level rights and 30 adjudicated groups. |
| KHM-MANUAL-A11Y-001 | TODO | Issue #463. | Human keyboard, screen-reader, zoom/reflow, contrast, touch-target and mobile QA with remediation. |
| KHM-LICENSE-OWNER-DECISION | BLOCKED | No repository license; owner decision required. | Owner explicitly selects and approves license. |


## Licensing status — 2026-11-21

KHMER-LICENSE-001 is PARTIAL pending hosted verification and merge. Original code is assigned PolyForm Noncommercial 1.0.0; original docs CC BY-NC 4.0. The Python package metadata has been changed from its previous MIT declaration to the same noncommercial code license. Third-party components and source-specific research data are explicitly excluded. Existing item-level source rights, redistribution permissions and any conflicts remain separate gates. This is a noncommercial licensing choice, not an OSI Open Source grant or a claim that the linguistic prototype is release-ready.


## Licensing closeout — 2026-11-21

KHMER-LICENSE-001 — DONE_VERIFIED. Original code: PolyForm Noncommercial 1.0.0; original docs: CC BY-NC 4.0. The former MIT package metadata was replaced with SPDX PolyForm-Noncommercial-1.0.0. PR #466 merged as 575447844a0f876d4e361232a25ef18b8bce50af; PR #467 merged as 94bbc0a230aafcfb65d300ea65f097d026c130df to align the official license wording. PR-head Quality and browser checks passed on both heads. Exact-main post-merge workflows on the latter SHA were still pending/in progress at this update. Third-party code and item-level research data are expressly excluded; rights-clearance tasks remain open. This is noncommercial licensing, not OSI-approved Open Source or linguistic release approval.


## Exact-main CI evidence — license closeout — 2026-11-21

Post-merge exact main SHA 493e135ad4787c737931dbad20ea564c528bfd7c is fully verified: Quality 44827023495 SUCCESS, browser smoke 44827023488 SUCCESS, Pages build/deploy 44827023602 SUCCESS. The owner-authorized code/docs noncommercial licensing is complete; source-specific third-party/data rights remain separate PARTIAL/BLOCKED gates.


## Research-data license scope — 2026-11-21

KHMER-RESEARCH-DATA-LICENSE-001 — implementation on license branch; PR-head CI pending. Original project-authored research data, annotations and curated database contributions are covered by CC BY-NC 4.0 in `LICENSE-DATA`, only where contributors hold the rights. Third-party source material and mixed-source items remain separately governed; unknown/conflicting rights remain unresolved. Existing product gold export gate still requires commercial redistribution and therefore excludes NC-only sources. No gold rows were added; linguistic acceptance status is unchanged.


## Research-data licensing — merged and verified — 2026-11-21

KHMER-RESEARCH-DATA-LICENSE-001 — DONE_VERIFIED. PR #470 merged as `c57e76d11e940aa522f36cfaca205ad654a6425e`. Original project-authored research data, annotations and curated database contributions are licensed CC BY-NC 4.0 for noncommercial research under `LICENSE-DATA`, only where project contributors hold the relevant rights. README, `THIRD_PARTY_NOTICES.md`, benchmark license registry and corpus documentation now reflect the scope. PR-head Quality/browser passed (44829570556, 44829570588); exact-main Quality 44829718697, Chromium 44829718684 and Pages build/deploy 44829718661 all SUCCESS on the merge SHA. Third-party source rights and any non-project contributor rights remain item-level unresolved gates. NC-only data remains ineligible for the existing commercial/product gold-corpus export gate. No gold rows or IPA labels were added.


## Citation metadata and exact-main verification — 2026-11-21

KHMER-CITATION-001 — DONE_VERIFIED. PR #472 merged as `cd54ed9c64fb9cb7132f33b589d7847a14226bde`, adding CFF 1.2.0 citation metadata for package version 0.2.0 and a README citation note. PR-head Quality/browser passed (44830502365, 44830502500); exact-main Quality 44830768580, Chromium 44830768579 and Pages build/deploy 44830768577 all SUCCESS on the merge SHA. No DOI or publication is claimed. KHMER-RESEARCH-DATA-LICENSE-001 remains DONE_VERIFIED from PR #470; source-specific third-party rights remain separate unresolved gates.


## Final mainline verification — 2026-11-21

Post-PR #473 exact main SHA `f41699a7ebadec9d85ec7cf7092f972212463f37` is fully green: Quality 44831432729 SUCCESS, browser 44831432822 SUCCESS, Pages build/deploy 44831432731 SUCCESS. This confirms the CFF citation metadata and final handoff update are deployed on main. Code/docs/data noncommercial license scope and CFF metadata remain DONE_VERIFIED; external item-level rights and linguistic release gates remain open.


## Final post-merge CI — 2026-11-21

Final exact main SHA `5537abb05795291bebc7e528a365a62b34dae18d` is fully green: Quality 44831853817 SUCCESS, browser 44831853698 SUCCESS, Pages build/deploy 44831853709 SUCCESS. The final handoff and completion register are therefore verified on main after PR #474. Licensing/citation tasks remain DONE_VERIFIED; external rights and linguistic release gates remain open.


## Final exact-main verification — 2026-11-21

Final main SHA `96c2329d627056daececef1848a76cc977051d65` is fully green: Quality 44832297432 SUCCESS, Chromium 44832297291 SUCCESS, Pages build/deploy 44832297309 SUCCESS. This supersedes the earlier checkpoint on `5537abb05795291bebc7e528a365a62b34dae18d`. Research-data licensing and CFF citation metadata remain DONE_VERIFIED; third-party item-level rights and linguistic release gates remain open.


## Final mainline reconciliation — 2026-11-21 (supersedes earlier closeout checkpoints)

- Verified default branch `main` at `0c0f8c911dece85c6e829886916a245540981c76` (PR #476 closeout). Exact-head GitHub Actions checks all completed successfully: Quality/build run [44832847634](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44832847634), Chromium/browser run [44832847820](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44832847820), and Pages build/deploy is included in run [44832847634](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44832847634). Exact-head check-runs `build`, `browser`, and `deploy` completed successfully. This verifies the latest mainline engineering/build/deployment state only.
- Repository-owned software, documentation, and original research-data licensing are DONE_VERIFIED: PolyForm Noncommercial 1.0.0 for original code; CC BY-NC 4.0 for original documentation and qualifying original project-authored research data. CFF citation metadata is present. Third-party and mixed-source rights remain item-specific; unknown/conflicting rights do not authorize redistribution, and NC-only material remains excluded from the commercial/product gold export gate.
- Current open PR inventory: no open PRs were found. No branch was deleted or rewritten.
- KHM-GOLD-PILOT-001 remains BLOCKED under Issue [#104](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/104): independent adjudicated gold=0 and empirical accuracy unmeasured; approved versioned Khmer IPA convention, two qualified independent annotators, separate adjudicator and curator, private blind intake, 30 attested lexeme groups, and per-item source-rights clearance remain outstanding. Candidate resources remain candidate-only until their exact artifacts and rights are verified. No gold labels or runtime rules were fabricated.
- KHM-MANUAL-A11Y-001 remains TODO under Issue [#463](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/463): human keyboard, screen-reader/assistive-technology, 200%/400% zoom, reflow, contrast, touch-target and mobile evidence is still required. Automated browser checks are not a manual WCAG audit.
- KHM-VOWEL-CONTEXT-MATRIX-002 remains PARTIAL: the canonical inventory contains nine source-indexed observations (seven SOURCE_ATTESTED_NOT_GOLD and two CONFLICTING_SOURCE_ANALYSES); full profile × series × vowel × phonological coda × syllable type × measured length × stress/harmony coverage and expert review are not established. Missing cells remain NOT_ESTABLISHED; no interpolation from orthographic structure is permitted.
- Lexical segmentation and other source-specific evidence gates remain PARTIAL/BLOCKED as recorded in the source/evidence registers. Do not promote candidate-only external corpora or forced-alignment resources to independent IPA gold.
- Local checkout and local test execution were unavailable through this GitHub connector session. The statements above rely on exact-commit GitHub Actions check-run metadata, repository files, issue/PR state and branch metadata; no local test command is claimed.

Task ledger: engineering/build/deployment = DONE_VERIFIED; repository-owned code/docs/research-data license and citation declarations = DONE_VERIFIED; third-party item-level rights = PARTIAL/BLOCKED where registered; gold pilot = BLOCKED (human/source-rights); manual accessibility = TODO (human QA); contextual vowel and lexical segmentation evidence = PARTIAL. Overall status: deployed research-ready partial prototype, not linguistically release-ready and not WCAG-conformance-certified.


## Human pilot, rights and research continuation — 2026-11-21

- KHM-GOLD-PILOT-001: BLOCKED. See Issue #104. Runbook exists; no private workspace, recruited roles, approved convention, rights-cleared 30-group sample, blind submissions or adjudication. Gold=0; accuracy unmeasured.
- KHM-PRIVATE-INTAKE-001: PARTIAL. Private blind-intake operational design added; provisioning, access grants, synthetic-data isolation test and actual use are outstanding. Public GitHub is not a blind channel.
- KHM-THIRD-PARTY-RIGHTS-001: PARTIAL/BLOCKED. See 2026-11-21 source reconciliation; MekongPhon UNKNOWN, Khmer acoustic dictionary CONFLICT, ALT/khPOS RESTRICTED with privacy conditions, Kirby audio UNKNOWN.
- KHM-CONTEXTUAL-VOWEL-MATRIX-002: PARTIAL. New research synthesis clarifies evidence strata and missing metadata; no new row is promoted to gold or runtime rule.
- KHM-LEXICAL-WORD-SEGMENTATION-001: BLOCKED. Morpheme/surface-word conventions, domain fit, data rights/privacy and a human boundary pilot remain unresolved.
- KHM-MANUAL-A11Y-001: TODO. Issue #463 remains open pending manual human evidence.


## MekongPhon rights chain — 2026-11-21

- KHM-MEKONGPHON-RIGHTS-001: BLOCKED/UNKNOWN. Direct inspection confirms no root license in the upstream repository; source chain includes SEAlang Headley77 dictionary scraping and OPUS NLLB v1, ParaCrawl-Bonus v9 and OpenSubtitles v2024 monolingual data. The derived IPA sentences are trie-based lexicon conversions, not independent sentence-level human IPA. Require maintainer permission and per-component/item provenance and license manifest before any import, training or redistribution.


## Public beta scope reconciliation — 2026-11-21

The owner explicitly selected public beta delivery without qualified external specialists. This changes release-scope classification, not linguistic evidence:

- **KHM-BETA-ENGINEERING-001 — DONE_VERIFIED:** the shipped Khmer beta has a reproducible npm dependency graph (`package-lock.json`, npm lockfile v3, integrity hashes and declared package license metadata); Quality, Pages and browser workflows use `npm ci`; exact-main Quality, Chromium/browser and Pages/deploy checks passed on `a6347577052ddf70d69364ed7cc90e2ff584ed2a` (runs `44906655301`, `44906655362`, `44906655377`).
- **KHM-GOLD-PILOT-001 — DEFERRED for beta / BLOCKED for expert-validated claims:** independent gold remains 0 and accuracy remains null. No synthetic labels are permitted. The previous expert-pilot requirements remain necessary only if the project later claims expert-validated linguistic accuracy.
- **KHM-MANUAL-A11Y-001 — TODO:** manual keyboard/screen-reader/zoom/reflow/mobile review remains unperformed and must be disclosed; automated Chromium is not WCAG certification.
- **KHM-VOWEL-CONTEXT-MATRIX-002 — PARTIAL:** nine source-indexed observations remain seven SOURCE_ATTESTED_NOT_GOLD and two CONFLICTING_SOURCE_ANALYSES; no missing contexts are interpolated.
- **KHM-LEXICAL-WORD-SEGMENTATION-001 — PARTIAL/BLOCKED:** unresolved segmentation convention, rights/privacy and no human boundary pilot; not a beta engineering blocker because uncertain spans remain explicit.
- **KHM-MEKONGPHON-RIGHTS-001 — BLOCKED/UNKNOWN:** upstream source chain remains uncleared; excluded from runtime, training, gold and redistribution.

Beta acceptance is therefore an engineering/deployment milestone, not a phonological completion claim. No IPA records, runtime phonological rules, gold rows or accuracy metrics were added by this milestone.


## Final current-main verification — 2026-11-21

Latest main SHA: `192d280890e7f95d67a0486227edd540bfabcb26`. All three exact-SHA post-merge workflows completed successfully: Quality [44906966908](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44906966908), Chromium/browser [44906967032](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44906967032), Pages build/deploy [44906966960](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44906966960). This supersedes the prior exact-main verification at `a6347577052ddf70d69364ed7cc90e2ff584ed2a`.


## Final beta mainline verification after PR #485 — 2026-11-21

Latest main SHA: `3bd48fe41411a0378fb37b74a31b1768eb7bb4d8`. Exact post-merge Quality [44907271893](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44907271893), browser smoke [44907271876](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44907271876), and Pages build/deploy [44907271998](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44907271998) all SUCCESS. This supersedes the earlier exact-main checkpoint at `192d280890e7f95d67a0486227edd540bfabcb26`.


## Final exact-main beta verification after PR #486 — 2026-11-21

Latest main SHA: `c836bb80236d2b1d68f68bbda88cacdfe2cdac75`. Exact post-merge Quality [44907687986](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44907687986), browser smoke [44907687995](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44907687995), and Pages build/deploy [44907688074](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44907688074) all SUCCESS. This supersedes the prior exact-main verification at `3bd48fe41411a0378fb37b74a31b1768eb7bb4d8`.


## Final beta verification after PR #487 — 2026-11-21

Latest main SHA: `2f4c0c1ca471b0ddd7444c17bb6d1a696fac9ec4`. Exact post-merge Quality [44908008375](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44908008375), browser smoke [44908008378](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44908008378), and Pages build/deploy [44908008449](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44908008449) all SUCCESS. This supersedes the previous exact-main verification at `c836bb80236d2b1d68f68bbda88cacdfe2cdac75`.


## Final exact-main Khmer beta verification after PR #488 — 2026-11-21

PR #488 merged as `866a5439f75d6f67e61a1781cbfccf8c77d9e9d7`. All three post-merge workflows passed on this exact main SHA: Quality [44908337364](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44908337364) SUCCESS; browser smoke [44908337384](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44908337384) SUCCESS; Pages build/deploy [44908338049](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44908338049) SUCCESS. This supersedes the prior exact-main checkpoint on `2f4c0c1ca471b0ddd7444c17bb6d1a696fac9ec4`.

KHM-BETA-ENGINEERING-001 remains DONE_VERIFIED. The exact mainline build, browser, quality and deploy gates are green. Independent expert gold remains 0 and accuracy null (DEFERRED for beta); vowel/context and lexical segmentation remain PARTIAL/BLOCKED as documented; manual accessibility remains TODO; third-party sources with unresolved rights, including MekongPhon, remain excluded. No new IPA labels, gold rows, linguistic rules or GitHub Release were added.


## Final exact-main verification after PR #491 — 2026-11-21

PR #491 merged as `112dd9a55f0dce1843ecd9ba6be272fa1335d586`, refreshing the visible beta status date and making the research-status notice explicitly distinguish engineering verification from pronunciation accuracy. Exact post-merge Quality [44908801606](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44908801606) SUCCESS; browser smoke [44908801669](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44908801669) SUCCESS; Pages build/deploy [44908801630](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44908801630) SUCCESS on this SHA.

This is the latest verified public beta mainline. Engineering/deployment status DONE_VERIFIED; independent expert IPA gold remains 0 and accuracy null; phonological and lexical segmentation coverage remain PARTIAL; manual accessibility QA remains TODO; uncleared third-party sources remain excluded. No gold data or linguistic claims were added.


## Final exact-main beta verification after methodology-page PR #494 — 2026-11-21

PR #494 merged as `877977a215b06eba2a79d19bf38283f39ffb8371`. It updates the methodology page with the public-beta status snapshot, the engineering-vs-linguistic validation distinction and direct beta policy/checklist links. All exact-main post-merge workflows passed: Quality [44909455274](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44909455274) SUCCESS; browser smoke [44909455237](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44909455237) SUCCESS; Pages build/deploy [44909455234](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44909455234) SUCCESS.

This is the latest verified Khmer public beta mainline. Engineering/deployment DONE_VERIFIED; expert gold=0 / accuracy=null; vowel/context and lexical segmentation PARTIAL; manual accessibility TODO; MekongPhon and other uncleared sources excluded. No IPA labels, gold rows or unsupported rules were added.


## Final Khmer public beta mainline closeout — 2026-11-21

Latest main SHA: `32b16b328f0433e30df6f3b1c4c5f7daa8ae59b5`. PR #495 merged the final exact-main evidence record and the methodology-page beta disclosure. Post-merge Quality [44909748314](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44909748314) SUCCESS (447 Python tests + 70 subtests; web checks/build passed); browser smoke [44909748266](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44909748266) SUCCESS (21 Chromium tests); Pages build/deploy [44909748262](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44909748262) SUCCESS (production Chromium and deployed HTML/JS/CSS smoke).

The README now links the beta checklist and policy; the landing page and methodology page show the 21 November beta status snapshot and distinguish engineering verification from linguistic validation. Engineering beta gate DONE_VERIFIED. Independent expert IPA gold remains 0 and accuracy null; vowel/context and lexical segmentation coverage remain PARTIAL/BLOCKED; manual accessibility remains TODO; MekongPhon and other uncleared third-party sources remain excluded. No IPA labels, gold rows, unsupported runtime rules or GitHub Release were added.

## Tier-B evidence classification implementation — 2026-11-21

- **DONE_VERIFIED (code + hosted tests):** Python rule-engine results now expose per-unit and aggregate A/B/C/D evidence tiers; the browser UI shows the same labels. B requires a source-located proposed/provisional IPA result and a successful IPA → Ukrainian mapping. C covers evidence-limited or unreferenced proposals and onset-only previews; D covers unsupported/unavailable output. A is reserved for independently adjudicated profile-matched gold and is not currently assigned.
- **DONE_VERIFIED (provenance):** the series-based inherent-vowel fallback now carries the existing onset-registry source references while remaining PROPOSED. No new phonetic values or gold labels were added.
- **DONE_VERIFIED (exact-head hosted CI):** branch/PR head 4ce52614211da63fa9bd4b3efeb2438e13e10938; Quality run 44931854471 SUCCESS: independent gold corpus structure check, Python tests, Node dependencies, web checks and site build all passed.
- **Coverage evidence:** 31 existing web fixtures; 27 contain a source locator, 26 contain both IPA and a Ukrainian reference plus a source locator, and four representative contrast fixtures remain unreferenced and therefore C. Runtime B still additionally requires the adapter to succeed. Aggregate tier is the weakest tier among included linguistic units; per-unit tiers remain available.
- **PARTIAL:** contextual vowel-series × consonant-series × coda coverage and lexical segmentation remain incomplete; no general rule is inferred from the representative fixtures.
- **DEFERRED:** expert-approved Phnom Penh IPA convention and independent adjudicated gold. Gold remains empty; accuracy remains null / NOT_ASSESSED.
- PR #497 contains this work. No other open Khmer PR was identified in this review.

## Post-merge verification — 2026-11-21

Tier-B evidence classification PR #497 was squash-merged as b6e0e69638562e93cb5baa324c7295b50faea115. Exact-main Quality run 44933254418 SUCCESS (448 Python tests + 70 subtests); Chromium browser smoke 44933254481 SUCCESS (21 tests); Pages build/deploy 44933254436 SUCCESS, including production Chromium and deployed HTML/JS/CSS smoke. The browser now exposes B/C/D labels per unit and aggregate; A remains unassigned. Independent expert-approved Phnom Penh IPA gold remains empty; measured accuracy remains NOT_ASSESSED. Contextual vowel-series × consonant-series × coda coverage remains PARTIAL.

## Exact-locator tier-B gate — 2026-11-21 (supersedes the earlier evidence-array-only B rule)

- **DONE_VERIFIED (code):** Python and browser confidence tiers now require an exact per-unit `source_locator`, at least one registered pronunciation-capable source ID from `data/khmer/sources.json`, successful IPA → Ukrainian mapping, and agreement with the supplied lexical Ukrainian reference when one exists. A non-empty evidence array alone no longer grants B.
- **B examples:** `ក` /kɑː/ and `គ` /kɔː/ use the exact R12A §Consonant registers and §Inherent vowels examples (U+1780/U+1782, lines 237–243 and 258–266). `ខ្មែរ`, `ភាសា`, `ភ្នំពេញ`, `កម្ពុជា`, and `ខ្ញុំ` use exact Wiktionary Pronunciation > standard IPA locators, now registered individually. Unit details show the locator to the user.
- **C boundaries:** `ភាសាខ្មែរ` is only a compositional phrase hypothesis from two cited component entries; no direct phrase-level locator was found. `ឆ` remains C because R12A's Onsets and Basic consonants lists conflict on its register class. Unicode-only examples and unregistered evidence IDs remain C even when they contain a proposed IPA string.
- **Rights:** Wiktionary's entry text is dual-licensed CC BY-SA 4.0/GFDL per its copyright page. The exact five lexical page records are separately identified in `sources.json` and `THIRD_PARTY_NOTICES.md`; no full page text/audio/media was copied and no repository-wide license was changed.
- **DONE_VERIFIED (exact code checkpoint):** branch commit `8c63558d3fa49532c7bd37b6dbcdf06382f36f29`; Quality run `44935886648` SUCCESS: 448 Python tests + 70 subtests, independent IPA gold structure check, Node web checks and site build all passed.
- **PARTIAL:** only the above locatable units are B. Contextual vowel × series × coda combinations, lexical segmentation, expert-approved Phnom Penh convention and independent gold remain incomplete. The gold corpus remains empty; accuracy remains NOT_ASSESSED.
- **NEXT VERIFICATION:** PR review must run the separate Chromium workflow and, after merge, a main Pages build/deploy plus deployed HTML/JS/CSS smoke. Do not claim deployment from this branch push.

## Post-merge final verification — 2026-11-21

- **DONE_VERIFIED (main):** final runtime/evidence-gate commit `7c47d56b91d132a1ce1c26e8f46e23372a6f5cd2`, following merged PR #498 (exact registered source-locator gate) and PR #499 (Wiktionary historical-IPA and rights caveat correction).
- **DONE_VERIFIED (Quality):** main run `44936590289` SUCCESS — 448 Python tests + 70 subtests, including independent IPA gold-corpus structure validation, source-locator tier tests, Node web checks and site build.
- **DONE_VERIFIED (browser):** main Chromium run `44936590230` SUCCESS — 23 browser tests, including B-tier locator visibility and C-tier phrase/conflict cases.
- **DONE_VERIFIED (deployment):** Pages run `44936590276` SUCCESS — production build, Chromium exercise, GitHub Pages deploy and deployed runtime asset smoke test all passed. Public beta: https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System-/
- **DONE_VERIFIED (diagnostic only):** optional Phonemizer run `44936590367` SUCCESS — 6/6 outputs, 0 failed outputs, 2 strict source-string matches and 6 limited-notation-normalized matches. Independent gold count is 0 and accuracy is null; do not describe these counts as accuracy.
- **Current evidence boundary (after PR #501):** B applies to nine individually source-located units: `ក`, `គ`, `ខ្មែរ`, `ភាសា`, `ភ្នំពេញ`, `កម្ពុជា`, `ខ្ញុំ`, `ជាខ្មែរ`, and `ល្ងាច`. The last two have direct phrase/lexical-entry locators and complete IPA → Ukrainian adapter agreement. `ភាសាខ្មែរ` remains C (compositional phrase without phrase-level source); `ឆ` remains C (R12A internal register-list conflict). No A-tier units or independent gold rows exist.
- **Remaining:** contextual vowel-series × coda coverage, lexical segmentation, independent Phnom Penh IPA convention/adjudication, and independent gold remain PARTIAL/DEFERRED. Accuracy is NOT_ASSESSED.

## Source-attested lexical expansion — 2026-11-21 (PR #501)

- **DONE_VERIFIED on PR branch, exact-head:** added two individually registered Wiktionary sources with direct orthography–IPA entries: `ជាខ្មែរ` /ciə ˈkʰmae/ (phrase-level entry, permanent Wiktionary revision `oldid=68806374`; orthographic/phonemic `jāk̥ʰmaer` and WT romanisation `ciə khmae` kept separate) and `ល្ងាច` /lŋiəc/ (single-syllable onset cluster, permanent revision `oldid=68625783`).
- **IPA → Ukrainian parity:** the current adapter renders `ciə ˈkʰmae` → `тьіє к'мае` and `lŋiəc` → `лнгієть`. The source IPA is retained exactly in the result; the Ukrainian forms remain project proposals, not independently adjudicated.
- **C boundary preserved:** `ភាសាខ្មែរ` remains C because it is only a project composition from separate word entries and has no phrase-level source locator. No rule or gold label was inferred from the new phrase.
- **Rights:** exact source revisions/URLs and attribution were added to `data/khmer/sources.json` and `THIRD_PARTY_NOTICES.md`. The two entries are community-maintained lexical references; page-level CC BY-SA notices are retained with the Wikimedia terms caveat. No embedded media or extended text was copied.
- **Exact-head verification:** Quality run `44938514023` SUCCESS — 449 Python tests + 70 subtests, Node web checks and build. Chromium run `44938514083` SUCCESS — 25 browser tests, including the direct phrase and cluster examples. Optional raw-output diagnostic run `44938514042` SUCCESS; it is not an accuracy measure.
- **DONE_VERIFIED (main):** PR #501 merged as `6235e28ed736b1d8f0c2a046a46bd5d6bd4691a9`. Main Quality run `44938817058` SUCCESS — 449 Python tests + 70 subtests, Node web checks and build. Main Chromium run `44938816871` SUCCESS — 25 browser tests. Pages build/deploy run `44938816928` SUCCESS, including production Chromium exercise and Pages deployment; public beta: https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System-/. Optional raw-output diagnostic `44938816954` SUCCESS, not an accuracy measure. Independent expert-approved Khmer IPA convention and independent gold remain unavailable; gold count 0, accuracy NOT_ASSESSED.

## Permanent phrase-source locator — post-merge verification — 2026-11-21

- **DONE_VERIFIED (main):** PR #503 merged as `bb1d1d5e3054cec7885ad67b46a63d627c15588a`. The direct phrase fixture `ជាខ្មែរ` now uses Wiktionary permanent revision `oldid=68806374` across the source registry, web fixture, lexical corpus, rights notice and evidence documentation.
- **Notation separation:** standard IPA `/ciə ˈkʰmae/` is retained as IPA; the source's orthographic/phonemic `jāk̥ʰmaer` and WT romanisation `ciə khmae` are stored separately. The direct phrase entry remains distinct from the compositional C-tier `ភាសាខ្មែរ`.
- **DONE_VERIFIED (Quality):** main run `44939428627` SUCCESS — 449 Python tests + 70 subtests, Node web checks and build.
- **DONE_VERIFIED (browser):** main Chromium run `44939428671` SUCCESS — 25 browser tests.
- **DONE_VERIFIED (deployment):** Pages build/deploy run `44939428633` SUCCESS, including production Chromium exercise and deployed asset smoke. Public beta: https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System-/
- **Diagnostic only:** raw-output run `44939428592` SUCCESS; it does not measure phonetic accuracy. Independent gold remains empty and accuracy remains NOT_ASSESSED.

## Source-located Khmer lexical coverage expansion — 2026-11-21

- **PARTIAL pending exact-head CI:** added three direct Wiktionary standard-IPA entries with permanent revision locators: `អក្សរខ្មែរ` `/ʔak.ˈsɑː kʰmae/` (`oldid=87132823`), `នគរខ្មែរ` `/nɔ.ˈkɔː kʰmae/` (`oldid=84887163`), and `អក្សរមូល` `/ʔak.ˈsɑː muːl/` (`oldid=63698235`).
- Source registry, web fixtures, lexical corpus, third-party notices and exact-locator tests updated. Each row remains `SOURCE_ATTESTED_NOT_INDEPENDENTLY_ADJUDICATED`; no gold labels were added.
- Python and browser IPA→Ukrainian adapters now explicitly omit only post-vocalic IPA `ː` when rendering practical Ukrainian spelling. The full IPA value remains unchanged in the IPA layer. Length after consonants remains unsupported and is not silently discarded. This target policy is tested in both runtimes.
- These three records increase the per-unit source-attested tier-B inventory from 9 to 12; aggregate confidence is still the weakest linguistic unit, and independent gold remains 0 / accuracy NOT_ASSESSED.
- External MekongPhon remains diagnostic-only: upstream repository snapshot has no root license, the seed lexicon has no item-level source locators, and the generated sentence IPA is dictionary-trie expansion over OPUS text, not independent sentence transcription. No rows or model artifacts were copied.
- **DONE_VERIFIED (main post-merge):** PR #505 merged as `3ba032ed67b3d5d165005b49bf134f18e0605228`. Quality run [44942983400](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44942983400) SUCCESS — 451 Python tests + 70 subtests; browser run [44942983385](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44942983385) SUCCESS — 26 Playwright tests; Pages build/deploy run [44942983387](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44942983387) SUCCESS, including deployed index/system HTML and JS/CSS asset smoke; raw-output diagnostic [44942983415](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44942983415) SUCCESS. Public beta: https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System-/.
- The three new permanent-locator Wiktionary entries are integrated and browser-visible at tier B; IPA preserves vowel length, while the Ukrainian practical adapter explicitly omits post-vocalic `ː` without rewriting the IPA source.
- Independent gold remains empty; empirical accuracy remains NOT_ASSESSED.


## Khmer lexical segmentation external benchmark — 2026-11-23

| ID | Status | Evidence | Acceptance boundary |
|---|---|---|---|
| KHM-LEXICAL-WORD-SEGMENTATION-001 | BLOCKED | Existing profile-neutral boundary evidence model; no approved project tokenization convention or independently adjudicated boundary pilot. | A separate lexical-boundary feature still requires convention approval, item-level rights/privacy review, independent annotation/adjudication and held-out target-relevant evaluation. |
| KHM-LEXICAL-WORD-SEGMENTATION-002 | DONE_VERIFIED (research benchmark only) | PRs #544, #546 and #547 merged. Pinned Rust v0.3.0 source, 61,980-row project word/count dictionary, khPOS OPEN-TEST and ALT/NOVA test split were compared in [workflow 45253514986](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45253514986) (SUCCESS). Quality [45253515015](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45253515015) and Chromium [45253514987](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45253514987) also SUCCESS. | Reproducible segmentation research only; not project IPA gold, not target-profile phonetic accuracy, and not approval of the ALT/NOVA morpheme-oriented boundary convention for the public UI. |
| KHM-LEXICAL-WORD-SEGMENTATION-003 | NO ADOPTION / DEFERRED | Current Viterbi outperformed MinWordsDp/UnigramDp on both test corpora. Full Tagger reached 95.07% khPOS Khmer-word F1 but fell to 63.59% on ALT, below the current engine's 70.15%; HMM/tagger fallback gave no material gain. | Do not ship the external Rust dependency or khPOS-trained model. Reconsider only with rights-cleared target-relevant training data and independent cross-corpus validation. |

The khPOS train/test and ALT corpora are CC BY-NC-SA 4.0. The 12,000-row train split was checksum-pinned; 12 exact NFC-normalized sentence overlaps with either test set were excluded (11,988 training examples retained). HMM and five-epoch tagger models were trained in memory only; no corpus/model artifacts were committed or uploaded. Phrase-level overlap was not measured. The ALT archive is Zenodo record 3937914, MD5 `20d39d8fa1b874b11ec374139fbe5654`; the khPOS source revision is `0211405c145b0a340ad558569bd06c946b2296b4`.

**Phonetic boundary unchanged:** this word-segmentation research does not establish IPA, phonological syllables, Ukrainian adaptation, or pronunciation accuracy. Independent expert-adjudicated IPA gold remains 0; empirical accuracy remains NOT_ASSESSED. Human IPA pilot issue #104 and manual accessibility review issue #463 remain open.


## Full repository audit — 2026-11-23

### KHM-IPA-ROUTE-SEPARATION-001 — DONE_VERIFIED

- The public browser previously placed the method selector inside the collapsed research drawer. More seriously, `src/main.js` substituted a whole-input BGN/PCGN-derived Ukrainian romanization into the primary phonetic result when IPA had no candidate. The live regression `ស៊៉ា` returned IPA `EVIDENCE_LIMITED` but Ukrainian `Са` without the promised unresolved marker.
- The engine also aggregated per-unit `ORTHOGRAPHIC_ROMANIZATION_FALLBACK` values into `canonical_ua`, despite typing those units as non-IPA fallback. This violated the separation contract and made the browser aggregate differ from Python's abstention semantics.
- PR #554 moves the method selector beside the primary result, makes the primary phonetic aggregate contain only IPA-derived units (unresolved runs remain `???`), retains orthographic candidates in typed unit diagnostics, and displays the separate romanization route only after explicit selection.
- Test-first evidence: PR test-only head failed exactly the two new regressions (37 existing Chromium tests passed). Final PR-head Quality [45266670579](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45266670579), Chromium [45266670379](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45266670379) (39/39), and external khPOS benchmark [45266670389](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45266670389) passed. Merged main commit: `f079e7c8862910b0c5ae783975e4997f2dd29be1`. Main Quality [45266981134](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45266981134) passed 472 Python tests + 70 subtests, Node/web checks, 129 structural, 38 lexical, 46 rule-output and 6 segmentation parity cases, benchmarks and build; main Chromium [45266981049](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45266981049) passed 39/39. Pages deployment and deployed-asset smoke [45266981797](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45266981797) passed. Live browser recheck: `ស៊៉ា` (Khmer input) now yields IPA `⟦EVIDENCE_LIMITED⟧` and UA `???`; explicit romanization mode yields `Са` with PROVISIONAL status. `ក្រុងចតុម្មុខ` remains `/kroŋ/ /caʔ.tom.muk/` → `кронг тьатоммук`.
- No new phonological rules, IPA labels, gold records, data imports or external providers were added. Output-route separation is DONE_VERIFIED on main and Pages; broader contextual phonology remains PARTIAL.

### KHM-PHON-CONTEXT-001 — PARTIAL

- Runtime coverage is exact lexical lookup plus a narrow deterministic inherent-vowel path. The full dependent-vowel × consonant-series × coda × syllable-context matrix is not wired into a general rule generator. The 61,980-entry word/count dictionary is segmentation data, not pronunciation data. Unsupported structures are generally withheld; this is preferable to invented IPA, but it does not meet a broad automatic Khmer-to-IPA coverage expectation.
- Acceptance: source-located and context-qualified rules for each promoted vowel/subscript/coda environment; exact positive/negative fixtures; Python/browser parity; independent specialist review; no blanket grapheme-to-Ukrainian shortcut.

### KHM-FIXTURE-PROVENANCE-001 — PARTIAL

- The runtime fixture file contains 38 entries, 37 with IPA. Four `PROPOSED` entries (`កី`, `គី`, `កា`, `គា`) have empty evidence arrays and no source locator. They currently carry only a representative-contrast note and must not be treated as source-verified tier B or gold.
- Acceptance: add exact registered pronunciation-capable source IDs and source locators for the precise orthographic/profile environment, or withhold the IPA/UA values until such evidence is established. Do not invent citations.

### KHM-IPA-GOLD-001 — BLOCKED

- Issue #104 remains open. No independent expert-adjudicated gold exists; `data/benchmark/gold.tsv` remains header-only and accuracy is NOT_ASSESSED.
- Acceptance: approved versioned IPA convention; two independent qualified annotators; third independent adjudicator; non-annotating curator; private blind intake; 30 rights-cleared source-located lexeme groups; two locked annotations and evidence-based adjudication.

### KHM-ACCESSIBILITY-MANUAL-001 — TODO

- Issue #463 remains open. Automated Chromium checks do not replace manual keyboard-only, screen-reader, zoom/reflow, contrast, touch-target and mobile review.
- Acceptance: record browser/OS/device/assistive technology, reproducible findings, fixes and retests; no WCAG conformance claim without completed evidence.

