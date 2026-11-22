## Dual IPA / romanization route correction — 2026-11-23

- **DONE — visible UI implementation on branch `feat/khmer-visible-dual-transcription-paths-20261123`, based on main `fe870f1b6d138d39bc271362cdda4165c1e3517e`:** moved the two-method switch from the collapsed research drawer to the primary Ukrainian result card, matching the Lao service's interaction pattern. The primary output now changes with the selected method. Method labels are explicitly `За IPA` and `З романізації`; title, explanation and status change with the method. Latin romanization input no longer presents itself as an IPA result.
- **DONE — Python hybrid API implementation:** `HybridKhmerEngine` now retains all validated external candidates and exposes a separate `provisional_candidate` when canonical IPA is unresolved and an external candidate can pass the project's Ukrainian IPA adapter. Canonical deterministic `ipa` / `ukrainian` fields remain unchanged. Candidate provenance, profile, uncertainty, provider identity and IPA kind remain inspectable. No voting, quality ranking or gold promotion is claimed.
- Added a lazy Khmer Phonemizer 0.0.3 adapter (MIT) and pinned optional `phonemizer` extra; added a separate pinned MekongPhon model extra. The MekongPhon Hugging Face model card declares Apache-2.0 for the model weights. This does not grant rights to the separate source corpus; corpus rights and item-level provenance remain independently restricted.
- **BLOCKED — browser-to-hybrid integration:** the public GitHub Pages service is static, local-first and explicitly has no runtime API/server. The Python providers cannot be invoked from the browser without adding and deploying a separate inference backend. This branch does not pretend that the public page now calls external models. The visible selector works between the two existing browser-side routes; the IPA route still uses the current deterministic/lexical browser engine.
- **PARTIAL — linguistic coverage:** current browser IPA derivation still abstains for many dependent-vowel, subscript, coda and complex-syllable patterns. The phonology research matrices document incomplete series × vowel × coda coverage. External candidates are now surfaced by the Python API but are not yet connected to the public static UI.
- **DONE_VERIFIED — Quality:** exact-head Python suite at `3ec4d0120a36c59e83bfe3714847a8fdc4a94aea`: 457 passed, 70 subtests passed; hosted Quality run [45078832071](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45078832071) passed.
- **DONE_VERIFIED — real Khmer Phonemizer smoke:** hosted optional-provider run [45078836057](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45078836057) passed; its uploaded artifact contains the actual IPA and Ukrainian provisional candidate for `កម្ពុជាប្រជាធិបតេយ្យ`. Observed IPA: `kampuciə prɑciətʰɨppaʔtaj`; Ukrainian: `кампутьіє пратьієт'иппатай`. Provider profile match remains UNVERIFIED; tone/stress and profile equivalence are not established.
- **DONE_VERIFIED — MekongPhon model smoke:** hosted optional G2P run [45078836077](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45078836077) passed on the then-current head. The pinned model returned `kampucieprɑcietʰiʔpaʔtay`; the current Ukrainian adapter correctly withheld a complete Ukrainian form because final `y` has no supported mapping. Candidate remains visible with mapping failure; no guess was inserted.
- A follow-up combined-provider workflow now exercises both MekongPhon and Khmer Phonemizer together, preserving both IPA candidates and preferring a candidate that maps completely into Ukrainian. Exact-head run is pending.
- Browser smoke is still running at this checkpoint; record its final exact-head outcome before merge.
- **Acceptance still required:** hosted browser smoke on the latest exact head; inspect the MekongPhon adapter result and failures; decide separately whether to deploy a runtime inference service. Do not claim full website hybrid inference until that backend exists and has passed its own operational/privacy/licensing checks.
- External evidence consulted: Khmer Phonemizer 0.0.3 PyPI record documents its token/phone-list API and MIT license; BYU MATRIX Lab's `byumatrixlab/khmer-ipa` Hugging Face model card declares Apache-2.0 and documents `pron_no_tones` examples. These sources support adapter availability and declared model/package licenses, not accuracy for the project's selected pronunciation profile.

---

## Lao-style unresolved final-output marker — 2026-11-22

- **DONE_VERIFIED — engineering/UI scope:** PR [#508](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/508) merged to `main` as `35866ecf493bdd61e62fe3a7784893a6f94ef8eb`.
- The public canonical Ukrainian field renders `???` for each linguistic unit whose result is not `PROPOSED`; punctuation and numeric literals remain unchanged, and supported neighbouring units remain visible. Per-unit statuses, source provenance and provisional onset hints remain in diagnostics, not the final result. Romanization is unchanged.
- Exact-head Quality [#44956091937](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44956091937) and [#44956095933](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44956095933) passed; browser smoke [#44956095934](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44956095934) passed. Post-merge main Quality [#44956195460](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44956195460), browser smoke [#44956195589](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44956195589), and Pages deployment [#44956195493](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44956195493) passed.
- Python research API internals and their typed diagnostic placeholders are unchanged. No phonological rule, IPA value, evidence label or accuracy claim changed.

---

## Public output levels — post-merge beta verification — 2026-11-21

- **DONE_VERIFIED — engineering/UI scope:** PR [#507](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/507) merged to `main`; merge commit `2dc432a8237ac56da7337c9787a1030890eeb9a3`.
- Public selector: careful / balanced (default) / exploratory. Careful hides per-unit diagnostics; balanced shows per-unit results/statuses and separately labelled PROVISIONAL onset hints; exploratory additionally reveals existing parsed graphemic structure. No new vowel, coda, tone or full IPA is inferred. BGN/PCGN romanization remains independent.
- Exact-head PR checks: Quality #6026 [44952265766](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44952265766) passed, including Python corpus validation, 451 pytest tests (70 subtests), and Node/web checks with output-level regression assertions. Browser #1321 [44952265803](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44952265803) passed production build and Chromium smoke.
- **Main deployment:** Pages #795 [44952354090](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44952354090) passed build, web checks, production build, Chromium, artifact upload, deploy and deployed asset smoke test.
- Live verification: [GitHub Pages](https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System-/) returned HTTP 200 and exposed all three selector options.
- Linguistic limits unchanged: PROPOSED fixtures are not expert gold; independent adjudicated IPA gold remains empty and empirical accuracy remains `NOT_ASSESSED`. External KhmerPhonemizer/Goruut/MekongPhon are not silently promoted or presented as canonical site engines.
- Remaining gates: independent IPA gold / expert adjudication, complete vowel-tone-prosody coverage, manual accessibility review and any claim beyond the labelled beta.

---

## Earlier PR implementation checkpoint (superseded by the post-merge verification above) — 2026-11-21

- Latest code, README and regression-test commit: `57b7950f9a1be19830c8a6e6dd01313a35ac9634` (PR #507); handoff refreshed immediately after it. Branch remains based directly on current `main` with no behind commits.
- Distinct behavior refined: careful hides candidate/unit diagnostics; balanced shows available non-Google / core diagnostic candidates (Khmer: unit-level statuses and explanations); exploratory adds the widest available diagnostics (Burmese: Google candidate if deployed; Khmer: existing onset-only provisional hints).
- **Verification status remains PARTIAL:** no exact-head CI run IDs or local test results are available in this session. Do not merge until the repository test/check, production build and browser workflow pass on this exact head; inspect the rendered site and confirm phonetic/romanization switching.

---

## Public output-level implementation — 2026-11-21

- **PARTIAL — engineering implementation submitted for exact-head verification:** branch `feat/evidence-aware-output-levels-2026-11-21`; base main commit `a07b9660b03daec9bacb17bab1d0f48b85fe4275`; PR #507.
- Added careful, balanced (default), and exploratory presentation levels. The selector changes display only; it does not modify source analysis, IPA evidence, canonical promotion rules, pronunciation profile, or the separate orthographic romanization path.
- Balanced retains the separately labelled existing PROVISIONAL onset hint; exploratory additionally reveals parsed graphemic structure. These hints are not full IPA, and no vowel, coda or tone is inferred. PROPOSED fixture outputs remain proposals, not expert gold.
- README and public UI documentation updated. **Acceptance still pending:** run the repository's exact-head Node/web tests, build, and browser smoke; inspect the live preview and confirm selector behavior for phonetic versus romanization modes. No test result is claimed from the connector's empty workflow-run lookup.
- Readiness unchanged: beta/research prototype; linguistic accuracy remains NOT_ASSESSED and independent IPA gold remains unavailable.

---

## Beta release scope decision — 2026-11-21

The project owner has explicitly chosen to proceed with public beta versions because qualified external specialists will not be available. This supersedes the earlier assumption that human expert annotation/adjudication is a prerequisite for *any* release.

- **Beta is permitted; expert validation is not claimed.** The gold corpus may remain empty and linguistic accuracy must remain null / NOT_ASSESSED.
- Reclassify the absence of annotators, adjudicator and expert-approved convention as **DEFERRED for beta**, not as a blocker to publishing a clearly labelled beta. It remains a blocker to expert-validated or production linguistic claims.
- Preserve all fail-closed behavior. Do not invent IPA, gold labels, accuracy metrics, source permissions or complete contextual rules.
- Beta acceptance requires exact-candidate engineering CI, package/site build, generated-data freshness, browser smoke tests, user-facing limitations, and documented rights for every shipped asset.
- Candidate external corpora with unresolved item-level provenance or license remain excluded. This decision does not authorize their import or redistribution.
- Manual accessibility QA is not a beta engineering gate if clearly disclosed as not performed; automated checks remain required.
- Publication of a GitHub Release or other external announcement still requires a separate owner-authorized action.

Canonical criteria: [docs/BETA-RELEASE-POLICY.md](BETA-RELEASE-POLICY.md). This decision changes release scope only; it does not alter phonological rules, IPA labels, corpus contents, or linguistic evidence.

---

## Engineering gate and corpus-coverage corrections — 2026-11-04

- The shared IPA corpus CLI previously emitted `release_ready: true` after checking only machine-verifiable corpus engineering conditions (adjudicated rows, frozen split minimums, one target-profile signature, one IPA kind and recorded redistributable source rights). It did not evaluate expert approval of the IPA convention, annotator/adjudicator qualifications, blind intake or expert-approved phonological contrast coverage.
- The success payload now reports `engineering_gate_passed: true` and `linguistic_release_readiness: "NOT_ASSESSED_BY_THIS_COMMAND"`. It lists six external acceptance gates not evaluated by this command: versioned expert-approved IPA convention; qualified independent annotators and separate adjudicator; controlled blind annotation/adjudication; expert-approved contrast coverage; independent corpus curator; and independent source-rights/license verification. It no longer emits `release_ready`.
- The engineering gate now separately requires at least **30 distinct adjudicated lexeme groups** by default, in addition to train/dev/test record minima. It reports both the number of distinct adjudicated groups and the configured minimum; repeated records within a single group cannot inflate the group-coverage count. Tests may lower the minimum explicitly for small synthetic fixtures.
- The tag/manual workflow is now named `IPA gold engineering-data gate`, and its minimum-count step explicitly says it is not linguistic release approval.
- Test-first evidence: regression-only commits produced expected Python-test failures on the old implementation (RED runs 41885520797, 41886236752, 41887115621). The final implementation on code-bearing commit `ea5b19cc50dc875c1ca7fdbef334a0ecd88f30f0` has exact-head hosted evidence: 41887446163 + 41887446069; additional push workflow: 41887436748. Exact-head Quality checks and browser smoke passed: Python tests, web checks, production build, and Chromium visible-results smoke.
- Updated `tests/test_ipa_gold_corpus.py` to assert the exact status, six unevaluated gates, absence of the old `release_ready` key, distinct lexeme-group minimums, and positive group minimum validation. No IPA labels, phonological rules, corpus rows, source permissions or generated pronunciation data changed.
- No local checkout or local test execution was available in this connector session; all verification evidence listed here is from hosted GitHub Actions.

## Post-merge handoff audit — 2026-11-04

- The base `main` SHA for this implementation branch was `ba6b90dee1acf00f7c89d3313d71270b713ecca2`. This is an immutable branch-base fact, not a claim that it remains the live `main` head after this implementation PR is merged.
- Previous documentation checkpoint PR #146 had exact head `7c6814fbc6fc26ae4a6479ab4b4edb1c9bac20d4`. Its diff was manually inspected; no CI status/workflow evidence surfaced for that PR head, so its CI remains **NOT VERIFIED**.
- The duplicate follow-up PR #147 was closed unmerged. The replacement implementation PR is #148; it includes the validator, regression tests, workflow-label correction, agent guidance and this handoff update. The branch's code-bearing implementation commit is `1a7474b287a9aa77b1d3ccbfd368d5afac1da15f`; GitHub PR metadata is the source of the eventual merge SHA.
- The exact-head workflow evidence and any still-running steps are recorded in the engineering-gate section above. This document intentionally records immutable branch-base history rather than a self-referential live-main SHA.
- Independent expert-adjudicated IPA gold remains 0; `data/benchmark/gold.tsv` remains header-only; empirical accuracy remains null. The profile confirmation does not substitute for expert convention approval, independent annotators/adjudicator, curator, blind intake, contrast coverage or independently verified source rights.

---


## Exact mainline checkpoint after methodology-gate adoption — 2026-11-04

- Verified `main` head: `a710984637c385797ea800ebd4bc6d7c9b9b5e6f`. The two methodology/completion-gate PRs for this repository are merged; there are no open PRs at this checkpoint. No implementation, linguistic registry, source record, benchmark label, or generated artifact was changed by those PRs.
- Exact-head CI status at checkpoint: Khmer Quality run 41877038265, browser run 41877038233, and Pages deployment run 41877038461 are QUEUED. These runs have not completed; do not record them as successful. Earlier green PR runs are not substitutes for this exact mainline head.
- GitHub branch metadata reports `main` as unprotected (no required status checks). This is a repository governance risk, not changed here; configuring branch protection or rulesets requires an owner decision and is outside this checkpoint.
- Independent expert-adjudicated IPA gold remains 0; `data/benchmark/gold.tsv` remains header-only; empirical accuracy remains null. KHM-GOLD-001 remains BLOCKED (independent adjudicated gold=0; gold.tsv header-only; target profile is already confirmed as contemporary Phnom Penh Khmer, careful citation-form speech (`khmer-pph-careful-citation-v1`); the versioned IPA convention sheet, two independent annotators, third adjudicator, curator, private blind intake and rights-cleared 30 lexeme groups remain required). KHM-PHON-001 and KHM-RLOSS-001 remain PARTIAL; KHM-UI-001 remains PARTIAL pending manual visual, keyboard, assistive-technology and mobile QA. DDD audio and MekongPhon remain candidate evidence only; external dictionary rights/counts remain unresolved.
- Methodology upstream refresh: Unlazy remains at `16671491f6679ad9378f52604d3bc2415b4120c7`; Matt Pocock skills at `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`; Ponytail at `96608e078b2d5ea607c5c3b8b5a54d1c1fba6846`. Superpowers main has advanced to `22f0b463e7a5e579904dd6211a520321035526f7` (v7.0.2), one commit beyond the project's pinned v7.0.1 snapshot. Its delta is primarily harness/platform integration and skill-helper changes; no runtime dependency or unreviewed copy was imported. Keep the existing pinned reference reproducible unless a project-specific adoption is justified.
- Environment boundary: this checkpoint used GitHub's hosted repository/Actions APIs; no local checkout or local test execution was available. Do not claim local pytest/npm/Playwright results.
- Next actionable work: Continue source-located contextual phonology research and organize the controlled human IPA pilot; do not promote generated/source-attested G2P outputs or orthographic transcripts to gold.

---



## External reference evidence review — MekongPhon (2026-11-04)

- Reviewed the LREC 2026 paper, PDF methodology sections, public MekongPhon repository README/data/pipeline code, and the current repository snapshot.
- The seed lexicon is derived from historical dictionary IPA (Kerr 1972 for Lao; Headley 1977 for Khmer). The paper reports a two-author qualitative review of 500 seed entries: 97.2% Lao and 99.2% Khmer; the authors disclose that both reviewers are proficient second-language speakers, not native speakers.
- The sentence-level corpus is expanded by longest-match-first lexicon lookup over OPUS text, so it is not an independently transcribed sentence-level gold set. Its held-out evaluation is dictionary-seeded and must not be conflated with our blind adjudicated gold.
- The GitHub repository snapshot f80f6c1840c4818b51e05f2e00cded4701a5b662 declares no repository license and contains no root LICENSE. The paper's SEALang “Creative Commons open license” wording does not specify a license version. Rights remain UNKNOWN for redistribution/derivative use pending item-level verification.
- Disposition: retain as a candidate secondary lexical reference and optional external diagnostic; do not import into data/benchmark/records.jsonl or gold.tsv as independent gold. The existing human annotation/adjudication gate remains open.
- Primary evidence: https://aclanthology.org/2026.lrec-1.129.pdf; https://github.com/byu-matrix-lab/MekongPhon/tree/f80f6c1840c4818b51e05f2e00cded4701a5b662.
## Post-merge reconciliation — Khmer G2P diagnostic provenance (2026-11-03)

- PR [#129](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/129) is merged into main as **2138f6f10df875591e846c81fae69c7cfde69bb5**; this is the current mainline checkpoint for this change.
- Exact final PR-head checks on c4741aa4a70e228ea8a5b2af42a5657da0ed4629: Quality [41726874329](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41726874329) SUCCESS (172 tests + 60 subtests), browser [41726874307](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41726874307) SUCCESS, optional G2P [41726874306](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41726874306) SUCCESS. The downloaded artifact contains the JSON report, .json.sha256 sidecar, and separate source diagnostic file; 90-day retention.
- The post-merge push-run result was not available through the connected workflow-run query at this checkpoint; no post-merge CI result is claimed. PR-head verification is the available evidence.
- Research boundary unchanged: independent adjudicated Khmer IPA gold remains 0; empirical accuracy remains null.

## Continuation update — external Khmer G2P report provenance and integrity (2026-11-03)

- **KHMER-G2P-PROVENANCE-001 — DONE_VERIFIED (diagnostic reproducibility only):** scripts/benchmark_g2p.py now embeds an inspectable provenance block with exact harness SHA-256, corpus path/hash, engine name/version, Python version/implementation, platform, and clearly named GitHub event SHA/ref/head-ref fields. It writes an adjacent .json.sha256 sidecar and creates parent directories.
- **Test-first evidence:** regression test added first; expected RED [41725130084](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41725130084). Transient integration defects (main output not yet routed through checksum writer; then literal escaped newline) were exposed by CI and corrected.
- **Final exact PR-head verification:** head 54c6a321c894468a7dd1625192a43f15fd806822; Quality [41726222759](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41726222759) SUCCESS (172 tests + 60 subtests); browser [41726222701](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41726222701) SUCCESS; optional Khmer G2P [41726222858](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41726222858) SUCCESS. Downloaded artifact was inspected and contains the JSON report, its SHA-256 sidecar, and the separate source diagnostic file; 90-day retention expires 2027-02-01.
- **Research boundary:** integrity/reproducibility only. Source-attested IPA remains non-gold; independent adjudicated Khmer IPA gold remains 0 and empirical accuracy remains null. No pronunciation rules, source labels, or accuracy values changed.
- **PR:** [#129](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/129), branch head 54c6a321c894468a7dd1625192a43f15fd806822.

## Continuation update — external Khmer G2P report provenance and integrity (2026-11-03)

- **KHMER-G2P-PROVENANCE-001 — DONE_VERIFIED (diagnostic reproducibility only):** scripts/benchmark_g2p.py now embeds an inspectable provenance block with the exact harness SHA-256, corpus path/hash, external engine name/version, Python version/implementation, platform, and GitHub source revision when running in Actions. The report writer emits an adjacent .json.sha256 digest sidecar and creates parent directories.
- **Test-first evidence:** regression test added first; expected RED on [41725130084](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41725130084). A transient integration failure [41725258719](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41725258719) exposed that the main path had not yet routed output through the checksum writer; fixed before final verification.
- **Exact implementation-head verification:** Quality [41725569108](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41725569108) SUCCESS (172 tests + 60 subtests); browser smoke [41725569152](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41725569152) SUCCESS; optional Khmer G2P run [41725569100](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41725569100) SUCCESS. Artifact khmer-phonemizer-raw-output is present and retained until 2027-02-01.
- **Research boundary:** report integrity and reproducibility only. Source-attested IPA remains non-gold; independent adjudicated Khmer IPA gold remains 0 and empirical accuracy remains null. No phonological rules, source labels, or accuracy values changed.
- **PR:** [#129](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/129), branch head 0607f7d2ad2ed481f0b75dcd486a2dcaefa31c6c; pending review/merge at this checkpoint.

## Continuation update — Unicode punctuation token boundaries (2026-11-03)

- **UNICODE-TOKEN-BOUNDARY-001 — DONE_VERIFIED:** browser tokenization now recognizes the Unicode general category `Punctuation`, matching Python's `unicodedata.category(...).startswith("P")` separator contract. Previously, the browser used a hand-maintained punctuation allowlist; punctuation outside it (for example U+3002 IDEOGRAPHIC FULL STOP) could be absorbed into a neighboring Khmer token and incorrectly mark that unit unsupported.
- **Regression:** `tests/web-runtime.test.mjs` exercises `ក។គ`; it checks exact source reconstruction, three distinct units, punctuation status, and that both Khmer neighbors retain their existing IPA/Ukrainian results.
- **PR:** [#126](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/126), squash-merged as `2a2f1c55282e076d6c4e0640d80af1053783bd6b`.
- **Verification on exact PR head `ec38f92efa0a59dd0d887e436a7194ded23c4e23`:** Quality checks [41710399396](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41710399396) SUCCESS; browser smoke [41710399684](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41710399684) SUCCESS. Deterministic web checks and production build also passed in the browser workflow.
- **Scope boundary:** this is a tokenizer parity/source-boundary fix, not a Khmer phonology rule, IPA convention decision, gold-corpus addition, or accuracy result. Independent adjudicated Khmer IPA gold remains 0; empirical accuracy remains null.

# Master execution plan and chat handoff

## Verified mainline checkpoint — Khmer external audio and dictionary research (2026-11-04)

- Current main before this documentation checkpoint: `98e66afecbce5528850e3a6906a8d9522385d3ed`. No open PRs; open human research issue #104 remains.
- PR #134 documented the Khmer Acoustic Model's unreconciled 29,204 vs 33,091 dictionary counts, CC BY-SA 4.0 vs CC BY 4.0 data-license statements, and missing full dictionary in the public tree. Exact-head and post-merge Quality, browser and Pages checks all SUCCESS (runs 41799402432, 41799595059, 41799595047, 41799595094).
- PR #135 registered DDD Khmer ASR Cultural Dataset v3 Part 1: 134.60h, 8 speakers, 13 topics/401 subtopics, CC BY-SA 4.0. PR-head Quality and post-merge Quality/browser/Pages all SUCCESS (41799786264, 41799802512, 41799887156, 41799887167, 41799887180). Use only after profile and share-alike review; city metadata does not establish Phnom Penh.
- PR #137 registered Common Voice 27.0 Khmer: 739 clips/0.98h, 213 validated/0.28h, 15 speakers, 364 validated sentences, accent/gender unreported. CC0-1.0 but no speaker identification or re-hosting/re-sharing. PR-head Quality [41800443113](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41800443113), browser [41800443035](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41800443035), post-merge Quality [41800575946](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41800575946), browser [41800575935](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41800575935), Pages [41800575937](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41800575937) SUCCESS.
- Neither audio corpus supplies IPA. Use provider-hosted clips only, no speaker identification/re-hosting, exact word-span/time locators, profile screening, two blind annotations and third-person adjudication. Independent gold remains 0; accuracy remains null. Issue #104 remains blocked on human convention/recruitment/intake and item-level rights/profile review.


## Khmer Common Voice 27 audio checkpoint — 2026-11-04

- Added source `mozilla-common-voice-khmer-27-2026` to `data/khmer/sources.json`: https://mozilladatacollective.com/datasets/cmu5olr5u00xzmh07pfgl3kuw.
- The provider declares CC0-1.0 but prohibits speaker identification and re-hosting/re-sharing. The release contains 739 clips / 0.98h total, 213 validated / 0.28h, 15 speakers and 4,971 sentences (364 validated); 483 unresolved and 43 invalidated. Accent is blank for the disclosed subset; gender is unreported.
- **KHMER-CV27-AUDIO-001 — PARTIAL.** Candidate secondary audio only. Do not infer Phnom Penh/Standard Khmer from locale; use only validated provider-hosted clips, no mirroring, and retain exact word-span/time locators. Blind IPA double annotation and adjudication remain mandatory.
- Keep this separate from DDD's CC BY-SA 4.0 corpus. Neither dataset supplies IPA. Gold remains 0; accuracy remains null.



## Verified mainline checkpoint — Khmer external-source research (2026-11-04)

- Current main: `ccd24f1f53dda8ccf19dbdbac0766ed4509f99e4` (PR #135). No open PRs at checkpoint.
- PR #134 merged as `09640f83141127eeb5c9d201d96671d243d03019`: recorded the Khmer acoustic-model dictionary's conflicting counts (29,204 vs 33,091), conflicting data-license declarations (CC BY-SA 4.0 vs CC BY 4.0), and absence of a full dictionary/release asset in the visible upstream tree. Exact-head Quality [41799402432](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41799402432) and post-merge Quality [41799595059](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41799595059), browser [41799595047](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41799595047), Pages [41799595094](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41799595094) SUCCESS.
- PR #135 merged as `ccd24f1f53dda8ccf19dbdbac0766ed4509f99e4`: registered DDD Khmer ASR Cultural Dataset v3 Part 1 as a candidate audio source, explicitly not IPA gold. PR-head Quality [41799786264](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41799786264) and [41799802512](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41799802512) SUCCESS; post-merge Quality [41799887156](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41799887156), browser [41799887167](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41799887167), Pages [41799887180](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41799887180) SUCCESS.
- Research boundary: DDD provides audio + orthographic transcripts; the 8 speakers and city metadata do not independently establish Phnom Penh phonology. CC BY-SA obligations and exact word-span/time locators remain to be reviewed before pilot use. The Khmer acoustic dictionary remains blocked for reuse. Independent adjudicated IPA gold remains 0; accuracy remains null.


## Khmer audio-backed pilot lead — 2026-11-04

- Added source `ddd-khmer-asr-cultural-v3-part1-2026` to `data/khmer/sources.json`. The provider listing for Version 3 Part 1 reports 134.60 hours, 8 Cambodia-based native speakers (4F/4M), 13 topics, 401 subtopics, origin-city metadata, CC BY-SA 4.0, attribution requirement and a prohibition on speaker identification.
- **KHMER-DDD-AUDIO-001 — PARTIAL.** This is a useful audio+orthographic-transcript candidate for a specialist-run pilot, not IPA gold. City metadata alone does not prove Phnom Penh speech; sentence recordings require explicit word-span/time locators; share-alike obligations need review before publishing derived IPA.
- Keep Version 3 Part 1's 134.60h/8-speaker figures separate from the broader HF card's 727.94h/12-speaker aggregate until provider manifests reconcile them. No speaker identification, audio mirroring or IPA labels are added.
- Acceptance: approve profile and licensing path, curate exact word spans, complete blind double annotation and third-person adjudication. Gold remains 0; accuracy remains null.



## Khmer external dictionary evidence checkpoint — 2026-11-04

- Rechecked `chemvatho/Khmer-acoustic-model` directly. Root README claims 29,204 IPA dictionary entries under CC BY-SA 4.0; `dictionary/README.md` describes a 33,091-entry G2P mapping under CC BY 4.0. The public Git tree currently contains only a six-line sample dictionary and no release asset with the complete data.
- **KHMER-ACOUSTIC-DICT-001 — PARTIAL / BLOCKED for reuse.** The counts and artifact-specific licenses are unreconciled; a full inspectable dictionary and per-entry provenance are unavailable in the public tree. Do not infer data rights from the MIT code license, and do not treat alignment metrics as IPA accuracy.
- Acceptance: obtain a versioned full dictionary and digest, explicit license for each artifact, target dialect and IPA convention, source provenance, and documented annotator/adjudication protocol. Until then, this remains a research lead only; no IPA gold or accuracy claim is added.

 — Khmer → Ukrainian

## Continuation update — strict JSON constants (2026-11-03)

- **JSON-INPUT-003 — DONE_VERIFIED:** JSONL corpus records and the license registry now reject JavaScript-only constants `NaN`, `Infinity`, and `-Infinity` through the JSON decoder's `parse_constant` hook. Diagnostics retain file and line context.
- **Regression coverage:** invalid constants in a corpus JSONL row and in `licenses.json`.
- **Test-first RED:** [41692662080](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41692662080) — exactly the two new regression tests failed before the parser change.
- **Implementation-head CI:** [41694124825](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41694124825) SUCCESS — 171 Python tests + 60 subtests; 3 browser smoke tests (run 41694138503).
- **Scope boundary:** this enforces RFC-compliant JSON syntax only; no corpus labels, license permissions, or gold records were changed.

## Continuation update — duplicate JSON keys in license registry (2026-11-03)

- **JSONL-INPUT-002 — DONE_VERIFIED:** the standalone `data/benchmark/licenses.json` registry is now parsed with the same duplicate-key rejection as JSONL corpus files. Duplicate top-level `licenses` and nested `redistributable` keys fail with path-qualified diagnostics; this prevents last-key-wins ambiguity in redistribution decisions.
- **Regression coverage:** duplicate top-level and nested license-registry JSON keys. Test-first RED: [41690144835](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41690144835); exact implementation-head CI: [41690306190](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41690306190) SUCCESS — 169 Python tests + 54 subtests; 3 browser smoke tests (run 41690316616).
- **Scope boundary:** no license grant is inferred or changed, and no source records or IPA labels are added. Existing rights evidence requirements remain in force.

## Continuation update — duplicate JSON object-key rejection (2026-11-03)

- **JSONL-INPUT-001 — DONE_VERIFIED:** `scripts/ipa_gold_corpus.py` now rejects duplicate JSON object member names at every nesting level. The parser reports the source path and line number instead of allowing Python's default decoder to silently retain only the last value.
- **Regression coverage:** duplicate top-level `record_id` and nested `orthography.text` keys, using otherwise valid corpus records.
- **Test-first RED:** 41687409282.
- **Exact implementation-head verification:** 41687730383 SUCCESS — 167 Python tests + 54 subtests; 3 browser smoke tests.
- **Scope boundary:** this protects annotation/provenance/profile/split input integrity; no linguistic labels, source data, schemas, or gold rows were added or changed. Independent adjudicated gold remains 0; empirical accuracy remains null.

## Continuation update — strict benchmark TSV validation (2026-11-03)

- **Implementation commit:** `46e7eda242f134a792060c3002992bdea42bdb6c` on `fix/heldout-ipa-benchmark-20261103` (PR #123; subsequent documentation commits follow it).
- **DONE_VERIFIED (input integrity):** `read_tsv()` now rejects duplicate column names, blank header names, and nonblank rows with missing or extra fields. Physically blank lines remain ignored; values are not silently padded, truncated, or rewritten.
- **Regression coverage:** duplicate gold and prediction headers, extra gold fields, and short prediction rows. Test-first RED: [41665735912](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41665735912); focused GREEN after implementation: [41665873021](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41665873021).
- **Scope boundary:** this is TSV/input-integrity hardening only. It does not add IPA labels, change linguistic rules, or establish empirical accuracy. Independent adjudicated gold remains 0 and accuracy remains null.

## Current repository state — 2026-11-03 (post-merge)

- **Mainline integration:** benchmark implementation PR #123 was squash-merged as `0f73d006bfc05f6106a3b1e463c2cc7d6471ffae`; the handoff/register reconciliation PR #124 was squash-merged as `ebd8432b4abacecb50e30bae43ff64c42ac4063b`. No open PRs remained at this checkpoint.
- **Held-out benchmark contract:** gold export preserves `split`, `split_seed`, and `split_version`; adjudicated records without a frozen split fail closed; the scorer defaults to `test`; train/dev/all require explicit diagnostic selection; mixed manifest identities and empty prediction files are rejected.
- **Input integrity:** benchmark TSV headers/row widths, whitespace-only identifiers, duplicate JSON object keys, and non-standard JSON constants are rejected with regression coverage.
- **Post-merge exact-main verification:** Post-merge Quality checks, built-site Chromium browser smoke, GitHub Pages deployment, and deployed-site/runtime-asset smoke all passed on the exact `main` head. [workflow](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41707503253); [browser smoke](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41707503102); [Pages deployment and deployed smoke](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41707503262)
- **Research boundary:** Independent expert-adjudicated Khmer IPA gold remains 0; `data/benchmark/gold.tsv` is header-only; empirical accuracy remains null. Engineering, browser and deployment checks do not establish pronunciation accuracy.

## Current task ledger and blockers

- **DONE_VERIFIED:** deterministic manifest-wide split identity; export/scorer held-out split integrity; strict TSV and JSON input validation; post-merge exact-main engineering verification.
- **PARTIAL:** The consonant-series × dependent-vowel × coda × syllable-context matrix, automatic word segmentation, contextual /r/-loss profile, and Ukrainian correspondences remain incomplete or evidence-limited.
- **BLOCKED:** Approve a profile-specific IPA convention; recruit two qualified independent Khmer phonetic annotators and a separate adjudicator; clear source/audio rights and establish blinded intake.
- **TODO:** Manual visual, keyboard, screen-reader, responsive and mobile QA on the deployed site remains TODO.

## Historical checkpoints (retained for audit; superseded by the current state above)



- **DONE_VERIFIED (engineering):** independent IPA corpus schemas, runtime validation, deterministic split/rights gates, source/evidence documentation, and the exact-head automated engineering checks recorded in the historical entries below. This is not linguistic validation.
- **DONE_VERIFIED (web output hotfix):** PR #108 removed the stale `source-result` DOM write; current `main` no longer dereferences the absent element. Exact-main Quality, Chromium browser smoke, Pages deployment, and deployed-site asset smoke all passed on merge commit `e9894e5726f5f6aa2510d7d3beed69b2d03fb666`. This verifies the UI regression fix and deployment, not pronunciation accuracy. Manual visual, keyboard, screen-reader and mobile QA remain open.
- **PARTIAL:** source-language phonology, IPA conventions, and Ukrainian target adaptation remain bounded by the language-specific evidence matrices and unresolved cases. PR #107 separately narrows the runtime to the selected Phnom Penh careful-citation profile; it must not be conflated with the isolated UI hotfix.
- **BLOCKED:** the 30-lexeme blind pilot cannot start until the IPA convention is approved, two qualified independent annotators and a separate adjudicator are confirmed, rights-cleared source packets are prepared, and blind intake is arranged. See [issue #104](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/104).
- **TODO:** manual visual, keyboard, assistive-technology and mobile QA on the deployed site; automated Chromium tests do not replace this human QA.
- **Next actionable engineering step:** reconcile PR #107 against post-hotfix `main` without reintroducing the removed DOM write; re-run exact-head tests and inspect the full profile diff before any merge. Separately complete manual keyboard, screen-reader and mobile QA. PR #108 is already merged; no release was published.

No local checkout was available; hosted CI is not local test execution, expert adjudication, manual accessibility QA, or proof that the current public URL has redeployed. Preserve fail-closed behavior and do not create IPA/gold labels from model output or unsupported spelling inference.


## Historical records

The dated entries below are retained as audit history. When a historical status or SHA conflicts with this current checkpoint, the active branch ref, completion register, and exact-head workflow run above are authoritative.

## Historical master handoff snapshot — 2026-10-25

**Last updated:** 2026-10-25  
**Repository:** https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-  
**Default branch:** main  
**Last audited base revision:** 6cc30bb48bedb83d86534a5fbff92839e26673dd  
**Latest implementation commits:** 479eda62aa32172bd6799caa324222c0260a7fc9 (style per-unit evidence breakdown), e1a2ba7304e96fe6afb392c74c0bfebd94531c2b (render per-unit IPA/status/source note safely), 117181206a4ec0b7be8c13e44da9c2f3d22367aa (show provisional-result notice), 9f4d583d469988e970c76d0080f32adfa92020f4 (test notice behaviour). Earlier audited revision: 3907ee710bad5c749805ce00d828c272a01838f9. This handoff update itself is a subsequent documentation commit; re-check main before the next code change. Recent implementation commits: 37d8e5dfb17144ed7c673841d2643fb38a9be9a6 (centralize effective register resolver), 7d3abf49720f05ed3f9f832fad22a105932e74bc (parser uses shared resolver), b45ecbd2a3567727db6c47ffbd56be5b75b4b556 (register regression tests), e4ff44656166d82d9dbb2554cf0d471612e37b4c (API status contract tests). Earlier matrix commits: d5686e6a1e4a8e5edbbf212ae7966305bdc6f1f8 and 9b7936c24b7ec584797d9e47aeb835afd670d091. Recheck latest main SHA and Actions runs before further work.

## Mandatory instructions for the next session

1. Read this document first, then docs/audits/2026-10-20-vowel-coverage-matrix.md and docs/audits/2026-10-20-coda-diacritics-matrix.md, docs/repository-audit.md, docs/superpowers/plans/2026-10-05-khmer-repository-finalization.md, docs/validation.md, docs/phonology.md, data/khmer/vowels.json, data/khmer/registers.json, data/khmer/sources.json, src/khmer_ua/parser.py, src/khmer_ua/phonology.py, src/khmer_ua/ipa.py and the related tests.
2. Check current main SHA, recent commits, CI, Pages workflow, and working tree before editing. This handoff's CI evidence refers to the earlier base revision, not necessarily the newest commit.
3. Continue from the first unresolved P0 below. Do not restart the entire audit unless the repository has materially changed.
4. Do not describe this as a complete IPA engine or claim full IPA verification while the vowel/coda/context matrix and adjudicated lexical corpus are incomplete.
5. After each work cycle, update this handoff and the relevant task/matrix statuses with commit SHA, changed paths, exact checks, results, unresolved issues, and the next action.

## Current evidence and state

- The repository is public, default branch main, and the connected GitHub permissions allow reading and writing.
- The latest commit before this audit was 6cc30bb48bedb83d86534a5fbff92839e26673dd (2026-10-09), message: "fix: classify unknown non-Khmer input as unsupported".
- GitHub Actions workflow runs for that base revision: Quality checks run 177 and Pages deployment run 187 both reported completed/success on 2026-10-09. This is historical CI/deployment evidence, not a test of the newer documentation commit or proof of linguistic completeness.
- The commit status API returned no individual statuses and state pending; prefer the actual Actions workflow runs when reporting workflow results.
- docs/audits/2026-10-20-vowel-coverage-matrix.md was initially added in commit 65c474768ef3db9f95573dfe443ee6fc9bcc41d7 and expanded in commit 9b7936c24b7ec584797d9e47aeb835afd670d091. It now indexes representative vowel, register, coda, NIKAHIT/REAHMUK, independent-vowel and orthographic-layout evidence from Unicode 17.0 Chapter 16 and R12A notes updated 2026-04-27. It remains intentionally non-exhaustive and is not an adjudicated IPA corpus.
- Source review confirms R12A's representative register-conditioned examples (ក vs គ; កី vs គី; កា vs គា), coda-sensitive contrasts (លង vs ល្ង), and that NIKAHIT/REAHMUK can affect both coda and nucleus. Unicode 17 is used as orthographic/illustrative evidence, not acoustic validation. Unicode 17.0 itself includes NIKAHIT contrasts (ដំ vs ដម; ពាំ vs ពាម). These are current-version source examples, but not an independently adjudicated gold corpus. The source-specific discrepancy between Unicode 17 Table 16-7 and R12A's simplified inherent-vowel examples is recorded in matrix commit fe38b18; do not flatten it into a universal mapping.
- Firecrawl research search was unavailable because the connected Firecrawl account reported insufficient credits; do not retry that connector this session. The publisher-hosted Chem (2020) PDF was subsequently reviewed: 21 speakers were screened, then 4 Phnom Penh speakers were selected; 61 lexical items were read three times, with formant and duration measurements. The paper explicitly discusses coda effects on vowel quality and length. This is useful acoustic evidence for prioritizing context, not a complete grapheme-to-IPA mapping.
- The previous plan at docs/superpowers/plans/2026-10-05-khmer-repository-finalization.md still has unchecked tasks, including phonological coverage, corpus, and final audit. Do not infer completion from files existing.
- No file named handoff, CITATION.cff, or LICENSE was found in the audited tree. Recheck before release work; this is an inventory observation, not a recommendation to add a license without deciding terms.
- The working web service is explicitly described by README as production-structured but linguistically coverage-limited.

## Architecture findings

### Implemented at structural level
- NFC normalization and parsing of consonants, coeng/subscript sequences, dependent/independent vowel signs, and format controls.
- Consonant series metadata and eligibility lists for MUUSIKATOAN/TRIISAP.
- Explicit parser outcomes for malformed or unsupported input.
- Register-shifter handling and the special ប៉ case in parser.py.
- Evidence/source registry, proposed Ukrainian mapping policy, representative lexical fixtures, adversarial web fixtures, Python and Node test suites, Vite build and Pages workflow.

### Not established as a complete phonological engine
- parser.analyze() returns phoneticization_not_yet_established rather than deriving complete phonetic output.
- resolve_inherent_vowel() deliberately returns a series label, not a deterministic IPA value.
- data/khmer/vowels.json records a short inventory and a few representative contrasts; it does not enumerate all attested vowel-sign × series × coda/context cases.
- The verified lexical corpus is small and uses Wiktionary sources for several items. Unicode representative examples establish orthographic examples but should not automatically be treated as independent acoustic or lexical IPA validation.
- There is no adjudicated gold corpus and no empirical accuracy score.
- A browser screenshot/pixel audit was not confirmed in the previous handoff/context; current responsive/accessibility behaviour still needs a dedicated check.
- The register helper inconsistency has been addressed in commits 37d8e5d and 7d3abf4: phonology.resolve_effective_register() now owns the shifter rules, parser.decompose_khmer_syllable() calls it, and phonology.resolve_register() applies it to a KhmerSyllable. Regression tests cover MUUSIKATOAN on second-series ង, the ប៉ exception, and an ineligible shifter. Python tests passed in Quality run 193 for commit b45ecbd2; the full workflow was still running at the last check. Recheck final run conclusion before calling the work verified.
- The previous deterministic /r/-loss profile was identified as overconfident because primary phonetic research reports variable aspiration, F0, phonation and vowel effects. The guard is merged as `1cbb5abdef1d7b7ac062199bfebdad14d9fe74b2`; exact-head Quality checks [40215678125](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40215678125) passed Python tests, web checks and site build. This is a fail-closed guard, not a complete profile model.

## Prioritized task register

| ID | Task | Priority | Status | Dependencies | Acceptance / verification |
|---|---|---|---|---|---|
| KH-VOW-001 | Expand vowel matrix using attested orthographic patterns, register, vowel sign, coda and profile | P0 | IN_PROGRESS | authoritative source extraction | Every row has source, confidence, IPA status, and test or explicit unresolved status; no arbitrary Cartesian product. PR #41 merged as `08fe98a88f5e3c0c3a21519b6cdc2024992d2f02`; evidence-gate CI [40210193894](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40210193894) passed source/status/conflict validation. Initial source-indexed rows are in matrix commit 9b7936c. |
| KH-VOW-002 | Verify vowel-sign inventories and contextual effects against Unicode + specialist phonology + acoustic literature | P0 | IN_PROGRESS | KH-VOW-001 | Orthographic inventory and R12A contextual descriptions reviewed; acoustic study and unresolved source/version differences still need review. Distinguish orthographic evidence from phonetic evidence. |
| KH-CODA-001 | Add coda-conditioned and syllable-structure cases, including NIKAHIT and REAHMUK | P0 | IN_PROGRESS | KH-VOW-001 | Source-indexed contrasts identified; conservative parser tests now assert that NIKAHIT/REAHMUK preserve structure without fabricating IPA (commit 262cffd). The NIKAHIT pairs are present in Unicode 17.0; independent lexical/phonetic adjudication remains open. |
| KH-IPA-001 | Audit parser-to-IPA API boundary and status semantics | P0 | IN_PROGRESS | matrix + model review | Python API contract tests in e4ff446 separate structural success from phonetic success. Browser shows a visible provisional notice and per-unit evidence breakdown. The unknown/mixed-script guard from PR #35 was merged into `main` as `a4912d520077f3e0df4e7236ae8784d8245354ff`; exact-main CI [40196341065](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40196341065) passed Python tests, web checks and site build. Follow-up PR #37 is now merged as `e39143cf5d880214765fff8f5a237e58d24ab00b`: browser parsing also rejects unknown material inside a Khmer unit, matching Python. Exact-head CI [40197626232](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40197626232) passed. General IPA generation, vowel/coda context coverage, and independent gold remain open; the overall task stays IN_PROGRESS. |
| KH-TEST-001 | Expand independently adjudicated lexical corpus | P0 | IN_PROGRESS | source review | Source-attested examples are now explicitly distinguished from independently adjudicated gold; build a held-out corpus with profile/audio adjudication before scoring |
| KH-REG-001 | Check helper register resolver against shifter-aware parser | P1 | DONE_VERIFIED | code-path review | PR #39 merged as `a0f5f6a272f10d79d5c383bf717363b5e18b053f`. Shared six-case JSON contract is consumed by Python and browser tests; both runtimes agree on effective register, rule ID and structural status for valid, ineligible and multiple shifters. Exact-head CI [40209903755](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40209903755) passed pytest, web checks and build. | The orthographic register resolver is verified. Inherent-vowel IPA quality, the full vowel/coda context matrix, and colloquial phonetics remain separate IN_PROGRESS research tasks. |
| KH-REG-002 | Verify encoded order of Khmer register shifters around visually prebase vowels | P1 | DONE_VERIFIED | Shared Python/browser fixture now tests `ង៉េ` (base + shifter + vowel sign in encoded order) and rejects `ងេ៉` (shifter after vowel sign). PR #51 merged as `123314b3fbb19e016270e7252fc86a933192cb93`; exact-head Quality checks [40222606376](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40222606376) passed. | Unicode 17.0 Chapter 16 says register shifters are encoded immediately after the base consonant; visual prebase placement must not be mistaken for code-point order. This is orthographic structure validation, not IPA gold. Main CI/Pages for the merge is pending as of this checkpoint. |
| KH-SOURCE-002 | Add source locators to all Khmer rule registry records | P1 | DONE_VERIFIED | PR #53 merged as `8c8c2939b44734bd30b7e63419c96c77e13217d4`; each rule now has a section-level locator, unique rule ID and registered source are validated. Exact-head Quality runs [40223685839](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40223685839) and [40223679988](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40223679988) passed. | Source traceability is improved; it does not resolve the full vowel × register × coda IPA matrix or create independent lexical gold. |
| KH-SOURCE-003 | Validate Khmer rule registry provenance and uncertainty contract | P1 | DONE_VERIFIED | PR #55 merged as `b447124dc429e60825e5da48a4feeecd04e54d4f`; exact-head Quality runs [40225032146](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40225032146) and [40225019704](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40225019704) passed. | Added `tests/test_rule_registry_provenance.py` validating unique IDs, source references, HTTPS records, specific locators, allowed statuses and the context-dependent NIKAHIT/REAHMUK contract. This verifies metadata/provenance only; it does not validate pronunciation accuracy. |
| KH-PROFILE-001 | Remove unsupported deterministic /r/-loss guess | P1 | DONE_VERIFIED | primary source review and exact-head CI | Merged as `1cbb5abdef1d7b7ac062199bfebdad14d9fe74b2`. `render_ipa_profile()` now raises an explicit `ValueError` for boundary-marked /CrV/ candidates under `phnom_penh_colloquial`; exact-head Quality run [40215678125](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40215678125) passed Python tests, web checks and site build. This verifies the fail-closed contract only, not colloquial IPA correctness. |
| KH-PROFILE-002 | Include aspirated IPA stop-/r/ onsets in colloquial uncertainty gate | P1 | DONE_VERIFIED | Exact-head Quality CI after regex and regression update | PR [#49](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/49) merged as `86c63af497ecb728eb8df338bd02ace85cf04a44`; optional IPA aspiration marker `ʰ` is now accepted before `r`, with regressions for `pʰrɑː`, `tʰrɑː`, `kʰrɑː`, and `cʰrɑː`. Exact-head Quality runs [40220444930](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40220444930) and [40220435721](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40220435721) passed. This closes a regex bypass only; it does not establish a complete /r/-loss environment model or gold IPA. |
| KH-UI-001 | Browser runtime, mobile viewport, accessibility and visual audit | P1 | IN_PROGRESS | stable engine cases | Added visible PROPOSED caution and per-unit status/evidence notes with safe text-only DOM construction. Still need keyboard/focus and responsive/browser visual audit; verify latest Quality/Pages workflows. |
| KH-REL-001 | License, CITATION.cff, release and Zenodo metadata review | P2 | TODO | authorship/license/data provenance decisions | Metadata accurate, source/data licensing checked, reproducible release archive; no invented author claims |
| KH-DOC-001 | Methodology note: “Khmer-to-Ukrainian Transcription: Register-Conditioned Vowels and Conservative IPA Analysis” | P1 | TODO | KH-VOW-001/002, KH-IPA-001 | Clearly separates orthography, phonology, broad IPA, phonetic profile, Ukrainian proposal and limits |

## Next concrete action

1. Verify Quality/Pages workflows for the latest coda evidence document commits 343e2ef and 84eb28c; the UI baseline Quality run 210 and Pages run 220 both succeeded for commit 66c6a20.
2. Continue KH-CODA-001: independently verify the R12A rhyme table transcription and build lexical examples for REAHMUK contexts, recording variety, gloss, source transcription, and any normalization to project IPA. Keep source-indexed examples distinct from gold adjudication.
3. Continue KH-IPA-001/KH-UI-001: test the per-unit view with long/mixed input, ensure output remains readable on mobile and accessible to screen readers, and confirm no status is lost in aggregate display. Do not treat browser fixture IPA as an independently adjudicated gold corpus.
4. Review docs/phonology.md and data/khmer/vowels.json against the scope of Chem (2020); preserve source-specific discrepancies. Do not add deterministic vowel mappings merely to make the matrix look full.

## Work log

### 2026-10-20 — audit continuation
- Reviewed repository tree and metadata, latest commits, existing implementation plan, repository audit, vowel/register/source data, parser, phonology helper, IPA profile helper, validation documentation, lexical corpus, adversarial corpus, package scripts, and CI workflow.
- Confirmed base revision's Quality checks run 177 and Pages deployment run 187 were successful on 2026-10-09; these are historical and do not validate newer documentation commits.
- Created initial matrix (commit 65c474768ef3db9f95573dfe443ee6fc9bcc41d7), handoff (commit 03e94ced1a2c319c462d53b681a3d61d348e1525), and plan links (commit b045495275b367c69a8e4c4ed8107faeb4724eb2).
- Expanded the evidence matrix with R12A/Unicode 17 source-indexed examples, coda-sensitive patterns, independent-vowel caveats, and source-version limitations (commit 9b7936c24b7ec584797d9e47aeb835afd670d091).
- Reviewed the publisher-hosted Chem (2020) PDF methods/results and added explicit study-design and coda-effect limitations to the matrix (commit d5686e6a1e4a8e5edbbf212ae7966305bdc6f1f8).
- Added tests/test_coda_marks.py (commit 262cffd76064cbb91c4fbeb83a04d38699e8353a) to guard against presenting deterministic IPA for NIKAHIT/REAHMUK before the coda/nucleus analysis is established.
- Updated the matrix to link GAP-004 to the conservative tests (commit bbf23f33263e17bc53264728cb058ee032589e12).
- Centralized effective register resolution in src/khmer_ua/phonology.py and made parser.py use the same helper (commits 37d8e5d and 7d3abf4). Added tests/test_register_resolution.py for a valid MUUSIKATOAN shift, the ប៉ exception, and an ineligible shifter (commit b45ecbd2). Quality run 193 completed successfully.
- Added tests/test_api_contract.py (commit e4ff446) to assert that structural success does not imply IPA success, and that unsupported/mixed input preserves status and never returns fabricated IPA. Quality run 195 passed; subsequent run 203 also passed the full Quality workflow for handoff commit 555a898.
- Browser audit found that an all-PROPOSED result did not show the caution panel, despite fixture values being explicitly provisional. Added getStatusNotice() and made the panel visible for PROPOSED results (commit 117181206a4ec0b7be8c13e44da9c2f3d22367aa). Added Node regression tests for PROPOSED, NOT_ESTABLISHED, INVALID_OR_UNSUPPORTED and ESTABLISHED_STRUCTURE notice semantics (commit 9f4d583d469988e970c76d0080f32adfa92020f4).
- Added a per-unit browser breakdown in commits 32aa0c4, e1a2ba7 and 479eda6. Each non-punctuation unit displays its source, status, IPA, Ukrainian candidate and note; content is inserted with textContent/createElement, not innerHTML. It is intended to expose mixed-input failures instead of presenting only concatenated output. Latest Quality run 209 and Pages run 219 were queued at last check.
- Opened R12A notes updated 2026-04-27, especially sections on registers, vowels, codas, NIKAHIT/REAHMUK, and independent vowels; reviewed Unicode 17 Chapter 16 for script examples and register shifters. Unicode 17.0 now confirms the explicit NIKAHIT contrasts; independent lexical/phonetic adjudication remains open.
- Firecrawl research search could not run because its connected account reported insufficient credits; no retries were made. No local Python/npm tests were run. Check current Actions/Pages runs for commit 9b7936c before claiming the documentation pipeline is green.

### 2026-10-20 — evidence register and external-engine screening
- Re-checked the latest default-branch workflow state before continuing: Quality run #215 and Pages run #225 completed successfully for commit 14ca4c33d06bdab7039a1022f035ca780391c888. These runs predate the current audit additions and do not validate them.
- Added `data/khmer/vowel-context-register.json` (initial commit 85bfac3; source-form correction b834703). It records source-indexed examples with graphemic structure, base series, register/coda context, IPA source, evidence status, limitations, and Ukrainian adaptation left unset where word-level output is not adjudicated. The register deliberately preserves the Unicode 17 / R12A inherent-vowel example discrepancy instead of collapsing it into a universal mapping.
- Added `tests/test_data_integrity.py` checks for registry fields, unique IDs, source references, conservative Ukrainian-output status, and explicit source conflict (commit 91a05c0). These tests have been committed but have not yet been run locally in this session; await the CI run for the new commit.
- Added `docs/audits/2026-10-20-external-phonemizer-audit.md` (commit 5cac544). Public documentation for `khmerphonemizer` describes word tokenization, phoneme-symbol lists, beam search, and optional lexicon use; the displayed symbols are IPA-like, but their complete IPA convention and exact lexicon/data provenance were not established by this source inspection. Treat it as a candidate comparator, not a gold oracle.
- Screened `chemvatho/Khmer-acoustic-model`: README describes a 29,204-entry IPA-labelled dictionary and reports a separate CC BY-SA 4.0 dictionary license while the code/model is MIT. No dictionary data was copied. The repository's exact entry provenance, phonetic convention, and claimed evaluation metrics were not independently reproduced.
- No external tool was installed or executed; no independent benchmark or accuracy figure is claimed. The current audit used public repository/package documentation only. Local Python/npm tests and browser/mobile visual checks were not run.
- Important audit observation: `data/tests/verified-lexical-corpus.json` currently labels six lexically sourced items `WELL_SUPPORTED`, but their cited sources are primarily Wiktionary pages and no entry-level independent adjudication record is present. The existing name/status should be reviewed in a dedicated follow-up; do not infer that these six entries constitute a phonetic gold corpus.
- Next: inspect CI for the registry/test commits; run Python + Node + build if an execution environment becomes available; then tighten the lexical corpus status semantics and audit the broad `/r/-loss` regex in `src/khmer_ua/ipa.py`. Do not add deterministic vowel rules until each context has adequate evidence.

### 2026-10-20 — lexical evidence-status correction and next phonology audit
- Updated all six entries in `data/tests/verified-lexical-corpus.json` from `ipa_status: WELL_SUPPORTED` to `SOURCE_ATTESTED_NOT_INDEPENDENTLY_ADJUDICATED`, adding an explicit evidence note. Their cited Wiktionary/lexical sources remain useful, but no audio-based or independent multi-source adjudication is recorded. Commit: 1e43292f1cb4abe204e7ac18c01e1e246b73995c.
- Added a data-integrity test forbidding those entries from claiming `WELL_SUPPORTED` absent adjudication (commit 8a32dc545d9fe26d125949b11123e90cabd81951). CI is pending/in progress for this change; no local test execution is claimed.
- The existing filename `verified-lexical-corpus.json` is legacy and now overstates its contents. Do not treat the filename as validation; consider renaming it only in a coordinated change that updates all test and runtime references.
- The current /r/-loss profile in `src/khmer_ua/ipa.py` remains a broad regex over IPA-like strings. It has a small unit test for one cluster, but no independently verified environment matrix. Do not expand its scope; audit the valid onset/coda boundaries against primary phonetic sources before modifying it.
- Next: check the newest Quality and Pages runs; inspect whether the new registry/status tests pass. Then audit the /r/-loss transform with explicit positive, negative and boundary examples and keep it labelled profile-level/provisional unless source-backed environments are verified.

### 2026-10-20 — documentation consistency and release metadata
- Corrected the README's overstatement that the small lexical corpus was independently supported: the cited phrase IPA is now described as source-attested but not independently adjudicated. Removed a stale assertion that the current main revision was green without checking its exact workflow SHA (commit 494ff78f2ff1526606f0c66141439d1587585167).
- Reconciled `docs/repository-audit.md` with the actual `src/khmer_ua/ipa.py`: a regex-based Phnom Penh /r/-loss transform is present and has only minimal unit coverage, contrary to older prose that said it had been removed. It remains an open P1 review item; do not treat the transform as fully validated (commit 402b6cef3c89b22c80d4dc44bc9b8ac7fdce83f2).
- Added repository license/citation metadata gaps to the external-tool audit: `pyproject.toml` declares MIT, but no root LICENSE or CITATION.cff was found in the inspected tree. Do not invent a copyright holder or author list; confirm terms before adding metadata (commit c543a8c9599dcee28afa609185ea83bb788f4cf6).
- CI evidence: Quality #219 succeeded for registry validation commit 91a05c0; Quality #220 succeeded for handoff commit b7fe0038. Quality #221 succeeded for the corpus status-only commit 1e43292. At the last check, Quality #222 for the new anti-overclaim test was still in progress, #223 queued for handoff commit 132c6640, and #224/#225 queued for README/repository-audit corrections. These runs do not cover the later commit c543a8c or the final handoff update; recheck exact SHA-specific runs before claiming final green status. Pages #229 succeeded for registry commit 91a05c0; later Pages runs were queued, pending, or cancelled by newer commits.
- No local Python tests, Node tests, Vite build, browser screenshots, mobile viewport tests, or external package execution were performed in this session. Successful GitHub Actions checks are the only execution evidence available here.
- Next priority: inspect the final SHA's workflow results. If CI passes, continue the P1 /r/-loss environment audit and then the P2 license/citation decisions. The P0 lexical gold corpus remains incomplete: source-attested rows are not independently adjudicated and must not be used for accuracy scoring.

### 2026-10-20 — bounded /r/-loss profile audit
- Checked current main workflow state before this cycle: Quality #227 and Pages #237 passed for handoff commit `f28c18a0`. This is the pre-change revision only.
- Found a concrete implementation risk in `src/khmer_ua/ipa.py`: the regex rewrote any matching `CrV` substring, even without a word/syllable boundary. An arbitrary string such as `akra` could therefore be changed although the function has no syllabification context.
- Changed the transformation to operate only at the beginning of the supplied IPA string or after an explicit space, syllable dot, or stress mark; unsegmented medial matches are preserved. Commit: `8949667a4ce91d71558b4896a12effe64ef1d3c1`.
- Expanded `tests/test_ipa.py` with word-initial, explicit-boundary, unsegmented-medial, coda-/r/, profile-preservation, and unknown-profile cases. Commit: `3d5aed8179134f74bbf23229cf153a6ebfb13d70`.
- Updated `docs/phonology.md` to explicitly label the transform a provisional string-level approximation that does not model full F0, phonation, vowel effects, or lexical conditioning. Commit: `c97c9f56a84cf1876930ddf37b7627a8e4ce8cec`.
- Latest workflow check: Quality #228 (fix commit) and #229 (test commit) were queued; Quality #230 for docs commit was queued. Pages #238 was in progress for the fix commit; #239 pending for tests; #240 queued for docs. Do not claim the latest changes passed until runs for the exact current SHA complete.
- No local Python/Node/browser tests were run. New tests are committed but not yet independently executed in this session.
- Interpretation limit: these tests verify conservative implementation boundaries, not the phonetic truth of any lexical /r/-loss example. The exact conditioning environments and full acoustic consequences still need review against primary phonetic studies and a dialect-labelled corpus.
- Next: re-check CI for current SHA, then continue P0 coda/REAHMUK source-indexing and IPA/status API/UI audit. Keep the independently adjudicated lexical corpus as an open P0; do not claim phonetic accuracy from source-cited fixtures.

### 2026-10-20 — NIKAHIT source conflict captured explicitly
- While continuing the coda audit, found a concrete cross-document/source mismatch for the same form ដំ ‘to pound’: the coda matrix records R12A `/ɗɑm/`, while the vowel matrix and Unicode 17.0 example record `/dɔm/`. This affects both onset notation and vowel quality; it must not be flattened into one source-neutral IPA.
- Updated `data/khmer/vowel-context-register.json` row KHV-007 to `CONFLICTING_SOURCE_ANALYSES`, with both verbatim source transcriptions, source IDs, and a no-selection criterion. Project IPA and Ukrainian output remain unset. Commit: `f2e80c41052b029a084e4cc1d4e5f7a1c62c1cf9`.
- Updated the vowel coverage matrix to flag SRC-006/VOW-014 as conflicting and blocked pending reconciliation; added an explicit discussion of the discrepancy. Commit: `e5fde73d8e4a51c1e3df3594c37809b42b821ca4`.
- Added a data-integrity assertion that the registry preserves both source alternatives without choosing one. Commit: `7d19e61204072e6d84eb02016fc63557d2b30edb`.
- Added the same caveat to the coda matrix. Commit: `aba5f13888d5e2a97dcde96ca436d960e28ad92d`.
- CI at the latest check: Quality #232 (registry conflict) queued; #233 (matrix) queued; #234 (test) queued; #235 (latest coda documentation) queued. Pages runs for intermediate commits were cancelled by newer pushes or remained queued/pending. No claim that the latest data tests have passed. Previously completed Quality #227 / Pages #237 were green only for the pre-implementation handoff revision `f28c18a0`.
- No local Python/Node/build/browser execution is available in this pass. This new conflict guard is committed but not yet independently executed.
- Next: check whether Actions actually runs for the latest SHA; if still blocked/queued, inspect workflow reasons before making more rapid pushes. Then continue the REAHMUK lexical evidence inventory and verify the source-specific transcriptions; do not promote these source examples to gold or runtime mappings.



### 2026-10-20 — REAHMUK lexical source inventory continuation

- Reviewed R12A's published character-detail examples for U+17C7 REAHMUK. The page supplies explicit lexical examples for the short-vowel combinations and for series-conditioned forms such as `សេះ` / `នេះ` and `កោះ` / `គោះ`. This is useful source evidence, but it is not independent audio adjudication.
- Added `data/tests/reahmuk-lexical-examples.json` (commit `f576eedf6145134434757c005982cfe5cbd62987`) with 11 source-indexed forms, glosses, verbatim source transcription strings, rhyme patterns, and limitations. The file explicitly warns that the strings are not normalized to project IPA and must not be used as gold labels.
- Added `tests/test_reahmuk_lexical_examples.py` (initial commit `c3b3bf871b333609b3f1277e66853012562bc90e`, assertion correction `74df5fdfad95313940e08ada2f8077f991bd2809`) to check the schema, provenance status, and a few series-sensitive examples.
- Expanded `docs/audits/2026-10-20-coda-diacritics-matrix.md` with the new inventory and its interpretation limits (commit `1f4755080bf10d1f4b820d52abae699e67b1d29f`).
- CI audit found Quality runs `39488178399` (commit `4f7891a`) and earlier runs `39488143676` / `39488125778` failing at “Run Python tests”; downstream Node/build steps were skipped. The API response exposed the failed step but not its traceback, so the precise failing assertion remains unverified. Do not claim tests pass. Inspect the current run/log or reproduce the workflow locally before more implementation changes.
- No local Python/Node test run or browser test was performed in this cycle.
- **Next:** first retrieve the Python failure traceback or run `python -m pytest` locally and fix the earliest failing assertion; then verify all Python tests, Node checks and build on the same commit. After CI is green, adjudicate a small REAHMUK subset against an independent lexical/audio source; keep the remaining source-indexed forms non-gold.


### 2026-10-20 — Python CI failure diagnosed and fixture corrected

- Retrieved the actual GitHub Actions job log for Quality checks run `39488650161`. Result: **54 passed, 1 failed**. The failure was `tests/test_ipa.py::test_phnom_penh_profile_does_not_rewrite_coda_r`.
- Root cause was a malformed test fixture, not evidence that the bounded regex was wrong: the assertion used `ar.kɑː` but expected `ar.kʰɑː`. There is no `r` after `k` in that input, so the implementation correctly left it unchanged.
- Corrected the input to `ar.krɑː` while retaining the expected output `ar.kʰɑː`; this now tests that the coda `r` before the explicit syllable boundary is preserved while the following onset cluster `kr` is transformed. Commit: `64fc5f8a717e91b39f3970ea20bb42c831ed3d46`.
- The fix is test-only; it does not strengthen the phonetic evidence or change engine behavior. Await CI for this commit before claiming the suite is green.


### 2026-10-20 — CI verification after onset-fixture correction

- Quality checks run [#242](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/39488865390) completed **successfully** for commit `64fc5f8a717e91b39f3970ea20bb42c831ed3d46`.
- The job's Python tests, web checks, and site build all completed successfully on that SHA. This resolves the known malformed-fixture failure; it is software-test/build evidence, not independent phonetic validation.
- GitHub Pages deployment run [#252](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/39488865332) was still in progress when checked. Verify its final result separately; do not assume a successful deployment from a successful build.


## Continuation update — 2026-10-21 (coverage audit tooling)

**Branch:** `feat/evidence-gated-coverage-audit-2026-10-21`  
**Starting default-branch commit:** `d06a5da7967032cecb0865ca86e5897d32fb90f7`  
**Latest implementation:** see the branch head and CI run; this section is updated as evidence arrives.

### Task ledger

- **DONE_VERIFIED — repository inspection:** Confirmed the default branch head, current source-indexed evidence registry, sign/consonant/register inventories, vowel and coda matrices, README, Python package, web tests, and CI workflow. Existing data and explicit source conflicts were preserved.
- **DONE_VERIFIED — deterministic inventory and generated artifact:** `scripts/coverage.py` builds `reports/khmer-coverage-audit.json` from canonical data, supports `--check` drift validation, validates required input shapes, counts register records correctly, and gives conflicts precedence over non-conflicting rows. The committed report currently contains 32 dependent-sign × series cells (16 dependent signs × two series), 4 source-attested-not-gold cells, 28 not-established cells, and no conflicts inside this narrow matrix. The source registry separately preserves conflicts KHV-007 and KHV-008. These counts describe evidence coverage, not pronunciation accuracy.
- **DONE_VERIFIED — regression coverage added:** `tests/test_coverage_report.py` checks reproducibility, matrix dimensions/status arithmetic, source conflict preservation, and that unresolved cells do not fabricate IPA. GitHub Actions Quality checks run [39570181898](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/39570181898) passed on implementation/doc commit `d279c60cb89e6d0bca9e0c38eaf747fdb1143d10`: **58 Python tests passed**, web engine/runtime checks passed, and Vite production build passed. The handoff-only follow-up commit is checked again by CI separately.
- **PARTIAL — phonological evidence coverage:** Source-attested examples remain examples, not gold. The report covers only dependent sign × consonant series; inherent vowels and sign combinations with codas, length, syllabification, register shifters, lexical context, and pronunciation profiles remain separate open dimensions.
- **BLOCKED / evidence-limited:** Do not fill missing cells from Unicode names or structural patterns. KHV-007 and KHV-008 preserve non-equivalent source transcriptions and must not be normalized into one project IPA without source-convention, lexical, and profile reconciliation.
- **TODO — linguistic acceptance:** Build a versioned independently adjudicated corpus and complete the full context matrix; acceptance requires each deterministic output to have scoped provenance and regression coverage, while unsupported contexts must remain explicit.
- **TODO — cross-runtime parity:** Verify Python/browser/shared-data behavior for supported and unresolved cases, including malformed input and source-to-IPA-to-Ukrainian boundaries.
- **TODO — /r/ profile:** Expand positive and negative Phnom Penh /r/-loss environments only with validated lexical and phonological evidence; the current string-level transformation remains provisional.
- **PARTIAL — full verification:** Python tests (including report drift check), browser checks, and production build passed in GitHub Actions. The Pages workflow is restricted to pushes to `main`, so this feature branch has not been deployed; no production deployment is claimed. The local container could not resolve `github.com`, so all execution evidence comes from the repository's CI runner, not local commands.

### Evidence and limitations

The inventory script is not a pronunciation engine. It generates no IPA or Ukrainian output, and it does not promote source-indexed evidence to gold. The generated artifact is committed so CI can detect drift. A green software pipeline validates code/data invariants only; it does not prove phonological completeness or empirical accuracy.

### Branch / PR reconciliation

The repository-scoped open-PR query returned no open PRs at the start of this pass. Work remains on the dedicated continuation branch; no PR was merged, no user branch was deleted, and no release was published.


### Current continuation checkpoint

- **Implementation/code verification commit:** `d279c60cb89e6d0bca9e0c38eaf747fdb1143d10`.
- **Handoff/documentation commit:** this section's latest commit on `feat/evidence-gated-coverage-audit-2026-10-21`; consult the branch head for its exact SHA and CI result.
- **Release classification:** research prototype / evidence-limited preview, not release-ready as a complete Khmer-to-Ukrainian transcription engine. Software tests passing do not close GAP-001–GAP-010 or resolve source conflicts.


## Continuation update — 2026-10-21 (coverage dashboard on site)

- **DONE_VERIFIED — site integration:** `system.html` now contains a responsive evidence-coverage dashboard. `src/coverage.js` imports the committed report as a build-time JSON module, renders all 32 dependent-vowel × series cells, shows the four summary counts, preserves source-conflict IDs, and links to the complete machine-readable report. It uses DOM `textContent` rather than inserting report values as HTML. The existing local-first CSP remains unchanged; the dashboard requires no network requests or analytics.
- **DONE_VERIFIED — site regression guard:** `tests/web-engine.test.mjs` asserts the dashboard mount, adapter, status vocabulary, report dimensions, and report link.
- **DONE_VERIFIED — CI on dashboard commit:** Quality checks [run 39598081311](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/39598081311) passed on `976cc5a40c633fee9a43868be980784539172a74`: 58 Python tests, web engine/runtime checks, and Vite production build. An earlier run on intermediate commit `a2c904bee6ef22cd62256e5dd281cdc4fab2b23f` failed because the HTML reference was committed just before the adapter file; the complete subsequent commit passed CI. No unresolved build failure remains at the verified head.
- **DONE_VERIFIED — public deployment (subsequently completed):** PR #1 was merged only after exact-head CI passed and GitHub reported mergeable. The Pages deployment for main commit `7f99f46beb290cfb240ded7438e568f0be0cd4d4` succeeded in run [39598303846](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/39598303846). A follow-up fix then made the linked JSON a public static asset.
- **TODO — linguistics:** Dashboard displays existing evidence only; it does not close the vowel/coda/context matrix, establish a gold corpus, or adjudicate KHV-007/KHV-008. Keep release classification as evidence-limited research preview until those acceptance criteria are met.


## Continuation update — 2026-10-21 (public report asset fix)

- **DONE_VERIFIED — identified and fixed static-asset gap:** Vite only publishes files in its public directory; the dashboard's JSON hyperlink would otherwise target a report file that exists in the repository but is not copied to `dist`. The generator now writes both the canonical report and a byte-identical `public/reports/khmer-coverage-audit.json`; `--check` validates both copies, and a new pytest checks byte identity.
- **DONE_VERIFIED — fix branch CI:** Quality checks [run 39598494026](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/39598494026) passed on `7754524b104269cd7b1069549c7c07b84680bbde`: Python tests, browser checks, and Vite build all passed.
- **DONE_VERIFIED — public asset merged and deployed:** PR #2 was merged at `48a1e2697ad802c31f21b99a404a10d7ab65b45c`. GitHub Pages run [39598640164](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/39598640164) completed successfully, with build and deploy jobs green.


## Final continuation checkpoint — 2026-10-21

- **Live site:** https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System-/system.html#coverage-audit
- **Public JSON asset:** https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System-/reports/khmer-coverage-audit.json
- **Last verified deployed main SHA before this documentation-only checkpoint:** `48a1e2697ad802c31f21b99a404a10d7ab65b45c`.
- **Quality checks:** [run 39598640050](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/39598640050) passed on the deployed main SHA.
- **Pages deployment:** [run 39598640164](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/39598640164) passed on the deployed main SHA.
- **Task ledger:** Dashboard, generated report, public static report copy, drift checks, regression tests, README, and deployment are `DONE_VERIFIED`. Full phonological/context matrix and independently adjudicated lexical gold corpus remain `TODO/BLOCKED` on evidence; KHV-007 and KHV-008 remain unresolved.
- **Release assessment:** Public research preview is deployed; the project is not certified as a complete or universally accurate Khmer-to-Ukrainian transcription engine.


## Continuation update — external Khmer G2P evidence reconciliation (2026-10-24)

- The optional Khmer Phonemizer 0.0.3 smoke run [40091745346](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40091745346) produced 6/6 outputs with 0 runtime errors. Its report records `independent_gold_count: 0` and `accuracy: null`; do not describe this as a 100% benchmark.
- Corrected the source-attested `ខ្ញុំ` entry: the cited Wiktionary page's standard IPA is `/kɲom/`; `k̥ʰñuṃ` is its separate orthographic/phonemic transcription. The previous `/kʰɲom/` value was not supported by that locator. A regression test now guards this distinction. Source: https://en.wiktionary.org/wiki/ខ្ញុំ
- For `ភ្នំពេញ`, the source gives `/pʰnum ˈpɨɲ/`, including a boundary/space and stress marker. The engine's token output omits those marks. This is an unresolved output-convention/representation difference, not an adjudicated phonological error. Source: https://en.wiktionary.org/wiki/ភ្នំពេញ
- Broader phonetic context: Khmer contrasts plain and aspirated stops (https://aclanthology.org/Y16-1.pdf); colloquial Phnom Penh /CrV/ realizations may differ through aspiration, f0 and phonation (https://doi.org/10.1016/j.wocn.2014.02.001). These papers do not independently adjudicate the candidate outputs for these lexical items.
- Dedicated branch: `fix/khmer-g2p-source-ipa-reconciliation-2026-10-24`. Pending CI. Keep external engine disabled in production and retain the evidence status SOURCE_ATTESTED_NOT_INDEPENDENTLY_ADJUDICATED.


## CI reconciliation note — Khmer source IPA fixture (2026-10-24)

- The first quality run on this evidence correction failed exactly where expected after changing the canonical corpus: `tests/test_data.py::test_verified_corpus_and_web_fixtures_agree_on_ipa` found the web fixture still held `/kʰɲom/` while the source-reconciled corpus now holds `/kɲom/`. The run had 67 passing tests and 1 failing test; this was fixture drift, not a runtime/adapter failure.
- Updated `data/tests/web-fixtures.json` to `/kɲom/`, added the separate orthographic transcription field, and clarified the note. The next quality and optional-G2P workflows are queued on head `a1ffffa821e809b638db328b1f23bc6b6a27bef4`; re-check their final conclusions before merge.
- Acceptance remains: full quality suite green, optional smoke successful, corpus and web fixture IPA aligned, accuracy still null / no independent gold.


## Final checkpoint — G2P source IPA reconciliation merged (2026-10-24)

- **Merged PR:** [#11](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/11), merge commit `35ce7142bf71f7e4cdb1acbb44d94d45ef71693a`.
- **Quality verification:** [run 40093054206](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40093054206) passed after the fixture correction, including Python tests, web-engine/runtime checks and site build. The earlier failures are recorded above: the canonical corpus correction first exposed stale JSON and JavaScript fixture expectations; both were aligned with the cited source.
- **Latest raw-output smoke:** [run 40093054099](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40093054099) passed. `khmerphonemizer==0.0.3`, 6/6 outputs, 0 errors; corpus SHA-256 `4b0fafa4a178c0a3e769ddb168f2115cd1fda0c98919c3bc2d731c13cbe6a7f4`; artifact SHA-256 `89eb762a46da84941bf47c7b26d7b18134270bcdede29bc7f1be8bcd60653f89`.
- **Source correction:** current cited Wiktionary standard IPA for `ខ្ញុំ` is `/kɲom/`; `k̥ʰñuṃ` is kept as separate orthographic/phonemic notation. For `ភ្នំពេញ`, source IPA `/pʰnum ˈpɨɲ/` includes stress/boundary information absent from the external phone-token output. No independent gold corpus exists; report still has `independent_gold_count: 0`, `accuracy: null`.
- **Release status:** research preview / partial prototype, not a complete or empirically accuracy-certified Khmer→Ukrainian engine. External engine remains diagnostic-only.


Authoritative readiness checkpoint — 2026-10-24 12:38 UTC

- Current main HEAD: 8e7209df4ec6c05767a8870368b112774681a151.
- Current-main quality checks: DONE_VERIFIED. Run 40093541363 passed; Pages deployment 40093541446 passed.
- Optional G2P smoke: DONE_VERIFIED as raw-output execution only. Run 40093213224 passed with six outputs, zero runtime errors, no independent gold; artifact SHA-256 89eb762a46da84941bf47c7b26d7b18134270bcdede29bc7f1be8bcd60653f89.
- The cited standard IPA for ខ្ញុំ is /kɲom/; k̥ʰñuṃ remains separately labeled as orthographic/phonemic notation. ភ្នំពេញ still requires an explicit convention for stress and syllable boundaries.
- Remaining TODO/BLOCKED: complete vowel/coda/context matrix, adjudicated lexical IPA corpus, source review for unresolved context-sensitive cases KHV-007/KHV-008. Unicode and external G2P output are not substitutes for acoustic or expert-adjudicated phonetic evidence.
- Readiness: research preview is build/test/deploy verified, not a complete or empirically accuracy-certified transcription engine.


## Browser/Python IPA profile parity correction — 2026-10-24

### Finding
The Python profile adapter in `src/khmer_ua/ipa.py` correctly restricts the Phnom Penh colloquial /r/-loss approximation to an explicit word/syllable boundary (`^|[ .ˈˌ]`). The browser adapter in `src/main.js` instead rewrote every matching `CrV` substring, including an unsegmented medial match. That violated the documented conservative boundary rule and made Python/browser behavior diverge.

### Change prepared
- Updated the browser regex to require the same explicit boundary as the Python implementation and preserve the captured boundary and onset.
- Strengthened `tests/web-engine.test.mjs` to require the boundary-aware pattern and replacement.
- Existing Python behavioral tests cover word-initial and explicitly segmented onset clusters, unsegmented medial matches, and coda /r/.

### Verification boundary
- Change is on PR [#14](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/14), based on main `1977822694cb5ce31fc9cb54ab79446605907738`.
- The browser test is a source-guard test; the existing Python tests are the behavioral reference. Quality workflow [40112562271](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40112562271) passed on the exact PR head `6fcd4442746f091159136e0b2b5ec126224c6e1b`: Python tests, web checks, and site build all succeeded. PR #14 merged as `d5245c0d7ab94de9c1774a705da1a3a7a14617f5`; post-merge quality [40113051028](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40113051028) and GitHub Pages deployment [40113051034](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40113051034) both passed on the merged HEAD.
- This fixes implementation parity; it does not validate the underlying linguistic hypothesis or expand the evidence-backed contexts in which the colloquial rule may apply.


## IPA benchmark harness and external engine protocol — 2026-10-24

- Added `scripts/benchmark_ipa.py`, a standard-library-only harness with strict Unicode NFC exact match, code-point Levenshtein CER (diagnostic only), and explicit missing-prediction accounting. Every independently adjudicated gold row remains in each engine's denominator; omitted outputs cannot inflate accuracy.
- Added `data/benchmark/gold.tsv` and `data/benchmark/predictions.tsv` header templates plus `tests/test_benchmark_ipa.py` covering no-gold behavior, adjudication gating, diacritic preservation, missing rows, and mismatches.
- Added `docs/benchmarking-and-external-ipa.md`; linked the existing `data/external-ipa-renderers.json` inventory to the benchmark protocol. External candidates remain optional and disabled by default.
- PR is open; current CI is queued / not yet verified. Do not merge until hosted tests pass. Local GitHub access is unavailable from the current container due network/DNS failure.
- No adjudicated gold corpus was added and no accuracy score is claimed. Candidate engine language support, actual IPA semantics, exact versions, and model/data licensing still require verification. Registry presence and smoke execution are not evidence of accuracy.
- Required next acceptance: run the repository test suite including the new harness tests; inspect all generated-artifact checks; then populate the gold set only with source-located, independently adjudicated pronunciations and rerun all engines against the same held-out set.


## External IPA/G2P and benchmark continuation — 2026-10-24

- Registry and per-language evidence notes: `data/external-ipa-renderers.json` and `docs/benchmarking-and-external-ipa.md`.
- External outputs are diagnostics only unless compared against a versioned, independently adjudicated gold set. Engineering fixtures and source-attested dictionary entries are not automatically gold.
- Shared harness: `scripts/benchmark_ipa.py`; empty templates at `data/benchmark/gold.tsv` and `data/benchmark/predictions.tsv`; tests at `tests/test_benchmark_ipa.py`.
- External comparator provenance audit PR #20 merged as `f5b6de77b30c2e6c65d94f9a31871d7bddf7a5a4`. Khmer Phonemizer 0.0.3 smoke returned 6 outputs without runtime errors; outputs remain unadjudicated and not directly string-comparable to source IPA. Independent gold remains 0.
- Keep IPA adaptation boundary: source spelling → structural parse → source phonology → typed IPA → Ukrainian adapter. Third-party candidates remain optional and disabled in production.
- Current true blocker: a source-located, independently adjudicated language-specific gold corpus with a documented dialect and IPA convention. Do not report accuracy until it exists.


### Verified status as of 2026-10-24

PR #17 merged as `edf625847029bbc3a043a0c01a09115e263164fb`. Latest quality checks and external smoke passed; 72 tests and 22 subtests passed. Khmer Phonemizer 0.0.3: 6 outputs, 0 runtime errors, independent gold=0, accuracy=null. Durable report: `data/benchmark/runs/external-g2p-smoke-2026-10-24.json`; artifact: https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40120003193/artifacts/12569269396.

- Keep IPA adaptation boundary: source spelling → structural parse → source phonology → typed IPA → Ukrainian adapter. Third-party candidates remain optional and disabled in production.
- Current true blocker: a source-located, independently adjudicated language-specific gold corpus with a documented dialect and IPA convention. Do not report accuracy until it exists.


## IPA gold provenance gate — merged 2026-10-24

- PR #21 merged; benchmark scoring now fails closed when an ADJUDICATED row lacks non-empty `gold_ipa`, `source_id`, or `profile`. Regression tests and optional Khmer G2P smoke passed on the merged head. This validates metadata completeness only; it does not validate the phonetic truth of a label.
- Latest successful Khmer Phonemizer 0.0.3 run [40121359605](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40121359605): 6 outputs, 0 runtime errors, 0 independent gold rows, accuracy null. Raw phone-token arrays remain unadjudicated and not directly string-comparable to source IPA without a declared convention.
- Artifact ZIP SHA-256: `3cd5ad913909cd1ff692c192614f354b707f705c1b6a2f1dc7ad971a4baf63a5`.


### Khmer external IPA notation diagnostic — 2026-10-24

- Pinned `khmerphonemizer==0.0.3` run [40128165807](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40128165807) passed with 6/6 outputs and 0 runtime errors. Strict token-join vs source IPA content matches 2/6; a separate notation-only comparison ignoring only slash wrappers, whitespace, syllable dots and stress marks matches 6/6. Aspiration, length, diacritics, tie bars and phone symbols remain significant. These are source-attested comparisons, not accuracy; independent gold count is 0. Artifact ZIP SHA-256: `2cbc7b00d35325e2e97fc98e80efeb9fdfecd477bf5ae5be24c43b6726c33299`.

## Authoritative current-head checkpoint — 2026-10-25

This checkpoint supersedes earlier readiness notes with stale main SHAs or queued-workflow status.

- Current `main`: `cb5331d2b587733180d9a585631dee26d0c370d9`.
- Quality checks [40129501080](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40129501080): `success`; Pages deployment [40129501022](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40129501022): `success`; optional Khmer G2P smoke [40129500995](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40129500995): `success`.
- The evidence registry is synchronized with the latest inspected smoke evidence from run [40128165807](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40128165807): 6 outputs, 0 runtime errors, 0 independent gold, accuracy null. Smoke outputs and notation-normalization agreement remain diagnostics, not adjudicated accuracy.
- Generated report, public report copy, drift checks and software CI are verified. The complete vowel/coda/context matrix, unresolved KHV-007/KHV-008 source-profile reconciliation and independent expert-adjudicated Khmer IPA gold remain PARTIAL/BLOCKED. Do not fill missing evidence from Unicode names or external G2P agreement.

## Latest external-smoke artifact reconciliation — 2026-10-25

- Inspected current-main smoke [40129500995](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40129500995), artifact [12574167928](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40129500995/artifacts/12574167928), SHA-256 `da53268c5d66ba3e2e5682029deb4bd6c2566466fbd920d72a6e3d9cab322f33`. The artifact contains one valid JSON report: khmerphonemizer 0.0.3, 6/6 outputs, 0 runtime errors, corpus SHA-256 `4b0fafa4a178c0a3e769ddb168f2115cd1fda0c98919c3bc2d731c13cbe6a7f4`.
- Source-attested notation diagnostic: 2/6 strict matches, 6/6 after limited normalization of slash wrappers, whitespace, syllable dots and stress only. Do not call this accuracy or gold agreement. Independent gold remains 0; accuracy remains null.
- The external-system registry and benchmarking documentation now reference this latest inspected artifact; earlier run records are retained for provenance.

## Final smoke and trigger-loop checkpoint — 2026-10-25

- After PR #32 narrowed the optional smoke workflow's automatic path filters, current-main smoke [40133705156](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40133705156) passed; inspected artifact [12575459926](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40133705156/artifacts/12575459926), ZIP SHA-256 `ff588e5d6a0e533aa4de7427e4786672f03999c3f7131abb1c89cb828936a677`.
- Report: 6/6 outputs, 0 runtime errors, corpus SHA-256 `4b0fafa4a178c0a3e769ddb168f2115cd1fda0c98919c3bc2d731c13cbe6a7f4`; 2/6 strict source-attested string matches and 6/6 limited notation matches. Independent gold 0, accuracy null.
- Registry and benchmark documentation now point to this final inspected run. Evidence-only updates no longer trigger optional smoke, avoiding a self-referential sequence of new run IDs and registry edits.
- Remaining research blockers unchanged: independently adjudicated Khmer IPA gold, unresolved source/profile conflicts KHV-007/KHV-008, and complete vowel/coda/context evidence. No engine promoted to production.


## Multiple register-shifter uncertainty regression — 2026-10-25

- PR #34: https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/34
- Added a runtime test asserting that a syllable with multiple register shifters returns `EVIDENCE_LIMITED` / `MULTIPLE_REGISTER_SHIFTERS`; wired it into both `npm test` and `npm run check`.
- Verification: Quality checks [40192533827](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40192533827) completed successfully on commit `78ec839322ca3211469ff7c0d46639c0d55eb78c`.
- This verifies conservative parser behavior only. The external G2P diagnostic remains 6/6 outputs with 0 runtime errors, but independent gold remains 0 and accuracy remains null. Complete vowel/coda/context evidence and unresolved source/profile conflicts remain open.


## Unknown-character fail-closed correction — 2026-10-25

- Branch: `fix/khmer-reject-unknown-grapheme-material-20261025`; PR [#35](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/35).
- Defect: `decompose_khmer_syllable` recorded an unknown character as `sign_or_unknown` but continued; if the same unit contained a recognized Khmer base consonant, final status could be `ESTABLISHED_STRUCTURE`. Example: mixed-script input `កx`.
- Test-first evidence: [run 40195870960](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40195870960) failed as expected because `analyze("កx")` returned `ESTABLISHED_STRUCTURE`.
- Fix: the parser now returns `INVALID_OR_UNSUPPORTED`, confidence `0.0`, and source-labeled grapheme diagnostics immediately when a character is not in the known Khmer sign registry. This is a structural rejection, not an IPA rule.
- Verification: post-fix exact-head run [40195885161](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40195885161) **passed** Python tests, web checks and site build.
- Linguistic gate remains open: the general orthography-to-IPA pipeline still intentionally withholds IPA; representative register/vowel examples and acoustic literature are not a complete context-conditioned mapping or independent adjudicated lexical gold. Independent gold count remains 0.


## Post-merge checkpoint — 2026-10-25

- Default branch now contains merge commit `a4912d520077f3e0df4e7236ae8784d8245354ff` for the unknown-character structural guard.
- Exact-main workflow [40196341065](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40196341065) passed Python tests, web checks and site build.
- This closes the specific mixed-script false-positive, not the overall KH-IPA-001 task. IPA mapping, source/profile conflicts, vowel/coda context, and independent gold remain unresolved.


## Browser parity: unknown Khmer material — 2026-10-25

- Follow-up inspection after the Python guard merged found the browser parser still downgraded unknown characters to `EVIDENCE_LIMITED`, allowing a recognized base consonant to lend false structural confidence to mixed-script input.
- The browser now returns `INVALID_OR_UNSUPPORTED` with the unknown characters preserved in diagnostics, matching Python's contract. Runtime regression tests cover `parseSyllable("កx")` and ensure the unknown fragment is not treated as established structure.
- Exact-head CI must pass Python tests, web-engine/runtime tests and build checks before this follow-up is merged. The guard is structural only; the broader IPA mapping and independent gold corpus remain open.


## Browser unknown-character guard merged — 2026-10-25

- PR #37 merged to `main` as `e39143cf5d880214765fff8f5a237e58d24ab00b`.
- Exact-head quality workflow [40197626232](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40197626232) passed. The regression verifies `កx` is `INVALID_OR_UNSUPPORTED` end-to-end in the browser, including unit-level status and output withholding.
- This closes a structural parity defect only. The repository still lacks a general source-orthography-to-IPA engine and independent adjudicated gold; do not mark the full IPA task complete.


## Khmer shared register-shifter parity fixture — 2026-10-25

- Added `data/tests/register-shifter-contract.json` with six structural cases: second-series MUUSIKATOAN, the ប៉→ប exception, first-series TRIISAP, two ineligible shifters, and multiple shifters.
- Python and browser-runtime tests consume the same fixture and assert effective register, exact rule ID and structural status. The fixture deliberately contains no IPA gold labels.
- KH-REG-001 remains IN_PROGRESS until exact-head CI passes; even after that, inherent-vowel quality and colloquial phonetics remain separate research tasks.


## Khmer register-resolver verification — 2026-10-25

- Reviewed the Python parser, `resolve_effective_register`, `resolve_register`, browser `resolveRegister`, and all direct tests/call sites. Both implementations remove ZWNJ for shifter-position calculation and preserve the same eligibility, exception, and fail-closed rules.
- PR #39 merged as `a0f5f6a272f10d79d5c383bf717363b5e18b053f`. Exact-head CI [40209903755](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40209903755) passed pytest, web checks and site build; the browser contract test is wired into `npm run check`.
- KH-REG-001 is DONE_VERIFIED for orthographic register resolution only. This does not validate inherent-vowel IPA or phonetic realization.


## Khmer vowel evidence-registry validation — 2026-10-25

- Added a test for `data/khmer/vowel-context-register.json` that checks unique case IDs, known evidence statuses, registered source IDs, and the rule that source-attested/non-gold rows cannot emit Ukrainian output.
- Conflicting source analyses must keep `ipa=null`, retain at least two source-specific alternatives, and state a selection criterion. This prevents incompatible Unicode/R12A examples from silently becoming one project-wide IPA.
- This validates provenance and withholding contracts, not the correctness of any IPA row. Exact-head CI must pass before merge.


- Post-merge evidence-gate checkpoint: PR #41 merged as `08fe98a88f5e3c0c3a21519b6cdc2024992d2f02`; exact-head CI [40210193894](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40210193894) passed. KH-VOW-001 remains IN_PROGRESS because provenance validation does not adjudicate source disagreements or establish the full vowel/coda/context matrix.


## Research and implementation checkpoint — 2026-10-25

- Reviewed the publisher-hosted author manuscript for Kirby (2014), DOI [10.1016/j.wocn.2014.02.001](https://doi.org/10.1016/j.wocn.2014.02.001), alongside Wayland (2005). The source describes several /r/-loss correlates and multiple colloquial realizations; aspiration-only output is not a uniquely determined result from a broad IPA string.
- Branch `fix/khmer-r-loss-profile-fail-closed-20261025` changes `src/khmer_ua/ipa.py` to reject ambiguous deterministic colloquial rendering; `tests/test_ipa.py` now checks the uncertainty boundary; `docs/phonology.md` records the evidence and limitation.
- This is a correctness guard, not added phonological coverage. The full orthography-to-IPA engine and independently adjudicated corpus remain absent; do not increase readiness based on this change alone.
- Exact-head Quality run [40215678125](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40215678125) passed Python tests, web checks and site build for the merged fail-closed profile guard. No local test result is claimed.


- Next profile task: `TODO` — design an alternatives-aware result contract that can represent multiple colloquial realizations with lexical/profile metadata. Do not re-enable a single deterministic aspiration-only output from a broad IPA string.


## Post-merge current-head checkpoint — 2026-10-25

- Current `main` after the colloquial /r/-loss fail-closed correction is `33778677a776fe8bbd51d8789368daac2cda74d9`.
- Current-main Quality checks [40215767648](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40215767648) and Pages deployment [40215767572](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40215767572) passed. The colloquial profile no longer collapses source-attested variable /r/-loss outcomes into an unsupported single aspiration-only rendering.
- Remaining P0 blockers are still substantive: contextual vowel × register × coda derivation, complete phonological IPA generation, and a source-located independently adjudicated lexical/audio gold set. This checkpoint does not raise measured accuracy; gold accuracy remains unmeasured.


## Khmer target-comparator evidence gate — 2026-10-25

- Target-layer review found that `map_segment(..., mode="compatibility_ru")` silently fell back to the Ukrainian default when a segment lacked a Russian comparator entry. For example, Khmer IPA `i` was returned as Russian compatibility `і`, which is a Ukrainian target choice and not an established Russian comparator mapping.
- Removed the fallback. Missing Russian comparator entries now raise from the strict mapper; `explain_segment` exposes `ru_compatibility: null` and `ru_compatibility_status: NOT_ESTABLISHED` while retaining the Ukrainian candidate separately. Added regression coverage.
- This makes target-policy provenance more honest; it does not establish a new IPA mapping or official Ukrainian/Russian standard. Exact-head Quality checks and site build must pass before merge.


## Post-merge target-comparator checkpoint — 2026-10-25

- The Russian comparator fallback correction merged as `894a2628b20c75f54733adcf49b3242625e2803d` via [PR #47](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/47). The earlier conflicted PR #46 was closed as superseded; its branch was left untouched.
- Exact-head Quality checks [40217188087](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40217188087) passed. The change ensures missing Russian comparator entries are `NOT_ESTABLISHED` rather than silently copied from the Ukrainian mapping.
- This fixes target-policy provenance only. Khmer phonological IPA generation and independent gold remain the primary P0 blockers; no empirical accuracy percentage is claimed.


## Aspirated stop-/r/ uncertainty guard — 2026-10-25

- PR [#49](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/49) merged as `86c63af497ecb728eb8df338bd02ace85cf04a44`.
- The previous `/CrV/` candidate regex did not match IPA forms where the aspiration diacritic `ʰ` occurs between the stop and `r`, allowing such forms to bypass the colloquial uncertainty guard. The pattern now accepts an optional `ʰ` and tests the aspirated sequences `pʰrɑː`, `tʰrɑː`, `kʰrɑː`, and `cʰrɑː`.
- Exact-head Quality runs [40220444930](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40220444930) and [40220435721](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40220435721) passed. This verifies a conservative guard, not a complete colloquial phonetic model.
- The broader alternatives-aware profile result contract, contextual vowel/coda IPA, unresolved source/profile reconciliation and independent expert-adjudicated gold remain open.


## Register-shifter encoded-order checkpoint — 2026-10-25

- PR [#51](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/51) merged as `123314b3fbb19e016270e7252fc86a933192cb93`.
- Extended `data/tests/register-shifter-contract.json`, shared by Python and browser tests, with a valid base + shifter + vowel-sign sequence `ង៉េ` and an invalid shifter-after-vowel sequence `ងេ៉`.
- Primary source: Unicode 17.0.0 Chapter 16, Khmer “Consonant Shifters” and “Ordering of Syllable Components”: https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-16/. It states that shifters are encoded immediately after the base consonant even where vowel glyphs are visually reordered. The new fixture is a structural regression contract, not a lexical IPA label.
- Exact-head Quality checks [40222606376](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40222606376) passed. Post-merge main checks [40222854594](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40222854594) and Pages [40222854484](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40222854484) were queued when this checkpoint was authored; verify before claiming the merged head is green.
- The full contextual vowel/coda/register-to-IPA matrix and independent lexical/audio gold remain open.


## Rule source-locator checkpoint — 2026-10-25

- PR [#53](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/53) merged as `8c8c2939b44734bd30b7e63419c96c77e13217d4`.
- Added explicit section-level locators to each canonical `data/khmer/rules.json` record. Orthographic claims cite Unicode 17.0 §16.4 Khmer; NIKAHIT and REAHMUK cite Richard Ishida’s specialist orthography notes.
- Tests now require unique rule IDs, known source IDs and non-empty, non-pending locators. Exact-head Quality runs [40223685839](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40223685839) and [40223679988](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40223679988) passed.
- This closes a source-traceability gap, not the contextual IPA gap. Independent lexical/audio gold remains unavailable; no accuracy claim is added.


## Rule registry provenance contract — 2026-10-25

- PR [#55](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/55) merged as `b447124dc429e60825e5da48a4feeecd04e54d4f`.
- Added `tests/test_rule_registry_provenance.py` for `data/khmer/rules.json` and `data/khmer/sources.json`. It checks unique IDs, registered sources, HTTPS records, section/table/code-point-level locators, required fields and evidence statuses.
- The test explicitly protects the context-dependent status for NIKAHIT and REAHMUK and ensures the register-shifter record remains a script/register claim rather than a complete contextual IPA mapping.
- Exact-head Quality checks [40225032146](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40225032146) and [40225019704](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40225019704) passed. No local tests are claimed.
- First unresolved P0 tasks remain the full vowel × register × coda/profile matrix, source conflict reconciliation, and independently adjudicated lexical/audio gold. This metadata test does not close those tasks.


## Romanization → IPA → Ukrainian result order — 2026-10-29

- Open draft PR [#57](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/57) adds a separate Khmer romanization card before the existing IPA and Ukrainian candidate cards. The original Khmer text remains available as a later source card.
- Romanization engine: `@gmana/km-translit@0.1.2`, MIT, BGN/PCGN-derived ASCII profile. The package explicitly says it drops diacritics and is **not** a fully conformant BGN/PCGN implementation; UI labels it accordingly. This is a separate orthographic romanization output and does not feed IPA or Ukrainian conversion.
- Exact-head CI for `aed14ec04b123d1aff81a5cd11b59eda35c3b961`: [Quality checks run 40780984225](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40780984225) **passed**. Python tests, Node checks, build, and generated-page checks passed. The added romanization test is included in `npm run check`; there is no dedicated browser automation in this repository.
- Status: UI/engine integration **PARTIAL / CI-PASS**. Independent Khmer pronunciation gold remains unavailable; do not treat the Latin output or the existing research IPA/Ukrainian candidate as normative.
- Next acceptance gates: independently inspect mixed-script/punctuation behavior in a browser; expand source-backed romanization fixtures; retain the profile/license notice; keep this PR draft until the owner approves the intended profile and the remaining language-engine evidence gates are reviewed.


## Publication checkpoint — 2026-10-29

This checkpoint supersedes earlier notes in this handoff saying the romanization PR was open/draft.

- PR #57 was merged to main as 875054f3ff31a2cebabd2d23672843791b746142.
- Exact post-merge Quality checks [40782813125](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40782813125) passed.
- Exact post-merge GitHub Pages deployment [40782813148](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40782813148) passed and reported URL: https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System-/
- Published output order: Khmer romanization → IPA → Ukrainian candidate; the romanization is independent and its upstream profile limitations remain as documented above.
- Remaining linguistic/UI acceptance gates are unchanged: independent Khmer pronunciation gold, broader source-backed romanization fixtures, and manual browser/mobile/accessibility QA. Publication does not mean linguistic completeness.


## Shared Ukrainian target adaptation checkpoint — 2026-10-30

- PR #59 (draft), branch `fix/shared-ukrainian-phonetics-2026-10-30`, applies the common target policy after Khmer IPA: /pʰ tʰ kʰ cʰ/ → п' т' к' ч'; foreign /h/ → г; hard /ɡ/ → ґ; genuine /x/ → х.
- Added explicit target mappings for /t͡s/ → ц, /d͡z/ → дз, /t͡ʃ/ and alveolo-palatal /tɕ/ → ч, /d͡ʒ/ and /dʑ/ → дж, /ʃ/ → ш, /ʒ/ → ж, plus supported palatalized sequences.
- The apostrophe marks aspiration only. It is not an output for /ʔ/ and is not the Ukrainian orthographic apostrophe. Adjacent consonants are not fused into an affricate without a source phonological affricate analysis.
- Updated source-attested lexical practical proposals: `ភាសាខ្មែរ` → `п'ієса к'мае`; `ហើយ` with /h/ → `гаеі`. The Phnom Penh colloquial profile's attested /cʰ/ candidate now outputs ч' rather than neutralizing aspiration.
- Exact-head CI [41076121018](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41076121018) passed Python (82 tests, 25 subtests) and all web checks, including runtime, register-shifter and romanization contracts. Branch head at verification: `677a9191e0614a7c9d9a55a259920689e0d04ec3`.
- Existing PR #58 was left untouched. This PR is still draft and is not merged.

These changes implement project-approved target conventions; they are not a new official Ukrainian standard and do not create new Khmer pronunciation evidence. Existing research blockers remain: contextual vowel/register/coda derivation, complete phonological IPA coverage and independent lexical/audio adjudication. Accuracy remains unmeasured.


## Romanization standard and crosswalk checkpoint — 2026-10-31

- Added [romanization-to-ukrainian-matrix.md](romanization-to-ukrainian-matrix.md) with the standard decision, source citations, initial consonant/subscript and vowel crosswalk, and explicit task ledger.
- Selected BGN/PCGN 1972 as the reference romanization standard. UNGEGN documents its 1972 approval as the UN-recommended Khmer system; the official PCGN guide provides the contextual consonant, subscript, vowel, diacritic and numeral tables.
- Existing @gmana/km-translit 0.1.2 remains a BGN/PCGN-derived ASCII approximation, not the complete standard: it drops diacritics and does not claim full conformance. The current romanization UI is retained but is not upgraded to a full standard implementation by this documentation change.
- Important gap: no independent romanization → Ukrainian syllable adapter exists yet. Do not imply that the romanization card already produces a Ukrainian orthographic-mode result. The current IPA → Ukrainian route remains independent.
- Task statuses: KHM-ROM-STD-001 DONE_VERIFIED (source review); KHM-ROM-ENGINE-001 PARTIAL; KHM-ROM-UA-001 TODO; KHM-ROM-MATRIX-001 PARTIAL; KHM-ROM-TEST-001 TODO; contextual IPA and independent lexical/audio gold remain PARTIAL.
- Branch: work/romanization-matrix-completion-20261031. No runtime code changed in this checkpoint; no new test result is claimed.


## BGN/PCGN Khmer consonant crosswalk checkpoint — 2026-10-31

- Added data/khmer/romanization_ukrainian.csv with the 22 official PCGN 2017 consonant/subscript table rows. Each row carries exact source-unit sequences, BGN/PCGN romanization, Ukrainian candidate/status, official PCGN URL and row-level locator. Row 18 records that ឡ has no subscript form; no extra ឝ row is claimed.
- Added tests/test_romanization_matrix.py. It checks all 22 official row IDs, exact Khmer source-unit sequences, romanization and Ukrainian candidate fields, provenance, locators and evidence statuses. It deliberately does not treat the CSV as a complete vowel/rime inventory.
- Source reconciliation: the first draft used an incorrect row transcription and an ASCII apostrophe. Inspection of the official PCGN 2017 PDF (page 2 table and notes) showed the apostrophe marker is U+2019 and corrected rows include 8/9 (ឋ/ឍ and ថ/ធ), 12/13 (ប and ព), and 18 (ឡ/ល). The data and test now assert the official source, not the earlier draft.
- Exact-head verification: workflow [41229686270](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41229686270) completed successfully: pytest 84 passed / 25 subtests passed; npm run check passed; production build passed.
- KHM-ROM-ONSET-001 is DONE_VERIFIED for the 22-row PCGN consonant/subscript table; this is a bounded consonant-table acceptance, not whole-language romanization coverage. KHM-ROM-MATRIX-001 remains PARTIAL: contextual vowel signs, shortening, anusvara/visarga, diacritics and numerals still need a source-exact data matrix and Ukrainian adjudication.


## Two-method result UI checkpoint — 2026-10-31

- Added an accessible two-button method switch to the service: **Фонетичний** and **За романізацією**. The default remains phonetic.
- The phonetic panel contains IPA, Ukrainian phonetic output, unit-level IPA/UA analysis and phonetic issue notices.
- The romanization panel contains the current BGN/PCGN-derived Latin output and a clearly labelled PARTIAL Ukrainian crosswalk state linked to the canonical research matrix. It does not reuse IPA or the phonetic Ukrainian output as a fallback.
- Test-first RED: workflow [41229998528](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41229998528) failed because the required mode controls/panels did not exist.
- Exact-head GREEN: workflow [41230217547](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41230217547) passed: pytest 84 passed / 25 subtests passed, npm run check and production build.
- The UI now separates the methods, but the Khmer Latin output is still the @gmana ASCII simplifier (diacritics omitted), and the independent syllable-level BGN/PCGN → Ukrainian adapter remains TODO. The romanization tab exposes that limitation rather than pretending it is complete.


## Final repository and Pages checkpoint — 2026-10-31

- Main commit: a351b0f66a608d7b4372e7c7bd0179808488be70 (PR #68, dual-method tabs).
- The final audit register records the source-corrected PCGN 2017 consonant matrix and the separate romanization/phonetic UI contract.
- Main quality workflow [41230505480](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41230505480) passed.
- GitHub Pages deployment [41230505474](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41230505474) succeeded: https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System-/ .
- Final statuses: KHM-ROM-STD-001 DONE_VERIFIED; KHM-ROM-ONSET-001 DONE_VERIFIED; KHM-ROM-ENGINE-001 PARTIAL; KHM-ROM-MATRIX-001 PARTIAL; KHM-ROM-UA-001 TODO; KHM-ROM-TEST-001 PARTIAL; phonetic independent lexical gold BLOCKED (none supplied/adjudicated).
- The website exposes two separate methods, but the romanization route's Ukrainian result is intentionally PARTIAL. Do not call the romanization mode complete until the full context-sensitive source → BGN/PCGN → Ukrainian syllable matrix and adapter are implemented and tested.


## Romanization evidence inventory continuation — 2026-10-31

- User confirmed the two-method contract: orthographic BGN/PCGN romanization → Ukrainian table adapter is independent from phonetic IPA → Ukrainian adaptation; romanization mode is intended to cover the supported orthographic inventory, while phonetic output may be partial/unsupported.
- Added `data/khmer/romanization_vowels_ukrainian.csv` with **37 source-located PCGN table entries**: 12 independent-character rows, 17 dependent-vowel rows, and 8 vowel + anusvara/visarga combinations. The independent-character column is sparse in the shared 22-row table. The data preserves PCGN alternatives, consonant-series/shortening context, candidate Ukrainian values, and explicit `PROPOSED`, `ANALYSIS_DEPENDENT`, or `EVIDENCE_LIMITED` statuses. Rows without an adjudicated target have an empty candidate; no missing value was guessed.
- Added `data/khmer/romanization_marks_numerals.csv` with all 6 PCGN diacritic rows and 10 numeral rows, plus `tests/test_romanization_marks_numerals.py`. These preserve series-changing and silent-mark behavior and map Khmer numerals to Arabic digits.
- Added `tests/test_romanization_vowel_matrix.py` to verify row counts, unique section/row identifiers, official source URL/locators, allowed evidence statuses, and the no-candidate invariant for `EVIDENCE_LIMITED`.
- Existing 22-row consonant/subscript matrix and its tests are preserved. This expands machine-readable evidence; it does **not** implement the PCGN romanization engine or the BGN/PCGN syllable → Ukrainian runtime adapter.
- Status: KHM-ROM-VOWEL-INVENTORY-001 = implementation added, CI verification pending; KHM-ROM-ENGINE-001 remains PARTIAL; KHM-ROM-UA-001 remains TODO; full context-sensitive vowel coverage and independent Khmer IPA gold remain PARTIAL/BLOCKED.
- Branch: `work/romanization-evidence-completion-20261031`. Changes are isolated from `main`; do not mark the new tests DONE_VERIFIED until the exact PR-head workflow passes.


## PCGN vowel-table source correction — 2026-10-31

- Direct inspection of the official PCGN 1972 PDF (pp. 2–4) corrected the shared vowel table inventory: 12 independent-character entries occupy rows 3, 4, 7, and 14–22; 17 dependent-vowel entries occupy rows 1–17; together these span the shared 22-row table. The earlier draft's 13-item independent list was inaccurate and has been replaced.
- Added all six diacritic rows and ten numeral rows in `data/khmer/romanization_marks_numerals.csv`; notes for series-shifting, shortening, `rC`, positional inherent-vowel behavior and silent `◌៍` are retained as contextual rules, not letter substitutions.
- The first CI attempt [41232327611](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41232327611) exposed a missing `source_url` field in the vowel CSV (86 passed, one failed). The source URL has been inserted into all 37 rows; a fresh exact-head run is required before closing this checkpoint.


## Verified Khmer PCGN orthographic inventory — 2026-10-31

- Exact PR-head workflow [41232468242](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41232468242) checked out merge commit `a1ce5ff` containing head `49f595e4ea030c4b4726ed3335c4bf9d22863271` and passed: pytest **87 passed / 25 subtests passed**, `npm run check` passed (engine, runtime, register-shifter, and romanization checks), and Vite production build passed.
- The first failed attempt [41232327611](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41232327611) exposed the omitted source URL in the vowel CSV; all 37 rows now carry the official PCGN PDF URL and row locator. The exact-head verification branch was created from the corrected tree.
- `KHM-ROM-VOWEL-INVENTORY-001` is `DONE_VERIFIED` for the bounded 37-row source inventory; `KHM-ROM-MARKS-NUMERALS-001` is `DONE_VERIFIED` for six diacritic rows and ten numeral rows. `KHM-ROM-MATRIX-001` remains `PARTIAL`; `KHM-ROM-ENGINE-001` remains `PARTIAL`; `KHM-ROM-UA-001` remains `TODO`.
- This does not establish all contextual BGN/PCGN transformations, nor does it complete the syllable-level BGN/PCGN → Ukrainian adapter. Existing @gmana ASCII output still drops diacritics. No new live Pages deployment was needed for these source-data and test changes; existing Pages site remains https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System-/.
- Verification PR: [#71](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/71), branch `verify/romanization-evidence-20261031`. PR #70 contains the earlier attempt and is superseded by #71.


## Post-merge main checkpoint — 2026-10-31

- PR #71 merged by squash as `2b8c9d4869c1fa4f179c3a087057e44bf5ef213b`; this is the main-branch implementation merge SHA for the romanization evidence inventory.
- Exact code-verification workflow [41232468242](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41232468242) passed: 87 Python tests + 25 subtests; web checks and Vite production build passed. The exact code-verification run checked out head `49f595e4ea030c4b4726ed3335c4bf9d22863271`; subsequent changes before merge were documentation-only.
- The bounded source inventory and its tests are now on `main`. The overall orthographic matrix and runtime adapter remain incomplete; see the PARTIAL/TODO statuses above.
- No runtime behavior or Pages build inputs changed in this PR; the already deployed GitHub Pages site remains the existing public service. A new Pages deployment was not necessary for these data/documentation-only changes.


## PCGN composite vowel glyph correction — 2026-10-31

- A second visual inspection of the official PCGN PDF (especially page 4) found that some dependent-vowel and anusvara/visarga source glyphs had been simplified in the first CSV draft. The data now preserves the actual table forms, including preposed-vowel sequences (`េ◌ើ`, `េ◌ឿ`, `េ◌ៀ`, `េ◌ា`, `េ◌ៅ`) and the PCGN composite patterns in rows 3, 7 and 8 of the anusvara/visarga table.
- The implicit-vowel row now uses the PCGN placeholder `◌`, whose note defines it as any Khmer consonant or consonant + subscript, rather than the non-graphemic label `inherent vowel`.
- Extended `tests/test_romanization_vowel_matrix.py` to assert exact source glyph sequences for all 17 dependent-vowel and all 8 anusvara/visarga rows, in addition to the full 22-row numbering, source URL, locators and evidence statuses.
- This is a source-faithfulness correction to the bounded inventory; it does not change the BGN/PCGN romanization values or claim that the context-sensitive engine / Ukrainian adapter is complete. Exact-head CI pending.

- This checkpoint supersedes the earlier 38-row / 13-independent-vowel draft count: the source PDF contains **12** independent-character entries, **17** dependent-vowel entries and **8** anusvara/visarga entries, for **37** machine-readable rows. The full shared PCGN vowel table spans row IDs 1–22 across its independent and dependent columns.
- The diacritic/numeral test now asserts all six exact PCGN mark glyphs and all ten Khmer numeral glyphs, not just their counts.


## Exact-head verification blocker for final PCGN glyph correction — 2026-10-31

- Programmatic branch-content validation confirms 37 vowel/rime rows, all 37 official source URLs, all 37 exact source-glyph + BGN/PCGN value pairs, 16 diacritic/numeral rows, and no Ukrainian candidate on any `EVIDENCE_LIMITED` row.
- The latest exact-head Quality checks run [41233203184](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41233203184) remains `queued` (job 124631488043). A local `git clone`/pytest attempt is blocked by the execution environment's DNS error (`Could not resolve host: github.com`). Therefore the new exact-glyph assertions have **not** been reported as passed.
- The matrix records `KHM-ROM-VOWEL-INVENTORY-001` and `KHM-ROM-MARKS-NUMERALS-001` as `PARTIAL` pending exact-head CI. PR #75 contains the correction and is mergeable; merge does not imply CI passed. Re-run/confirm CI after the runner becomes available before promoting these rows to `DONE_VERIFIED`.


## Final main SHA and merged source correction — 2026-10-31

- The corrected PCGN source glyph inventory and exact-row tests were merged by PR #75 as `5959113931c2e08ac279f4e064fa14a669a96f87`; the subsequent ledger correction PR #76 merged as `799d66f2038053e03b3a1c82d33fec7bbef4bfc8`. This is the main head before this final handoff-only update.
- PR #75's exact-head workflow [41233203184](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41233203184) remains queued. The local clone attempt failed with `Could not resolve host: github.com`; no test pass is claimed for the latest exact-glyph assertions. The matrix correctly leaves the bounded vowel and marks/numerals tasks PARTIAL pending CI.
- Remaining acceptance: exact-head CI green; complete context-dependent BGN/PCGN engine; complete romanization-syllable → Ukrainian table and adapter; broader IPA gold and ambiguity tests. No runtime changes or new Pages deployment were made.


## Exact PCGN glyph inventory verification checkpoint — 2026-10-31

- Current main before this documentation checkpoint: `5f3a9184f61d2e6e559cde30767e8c681a995a68`; matrix status update commit: `37990bcaf9550d6d2d45506ae9f56eb7717c2a2f`.
- Previously queued exact-head workflow [41233203184](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41233203184) is now completed with conclusion `success`. Job `test` (ID `124631488043`) completed all steps successfully: Python dependency setup and tests, Node dependency setup, web checks, and site build.
- Updated `docs/romanization-to-ukrainian-matrix.md`: `KHM-ROM-VOWEL-INVENTORY-001` and `KHM-ROM-MARKS-NUMERALS-001` are now `DONE_VERIFIED` as bounded source-table inventories with exact-glyph/romanization assertions; `KHM-ROM-TEST-001` remains `PARTIAL` because broader mixed-script, punctuation, malformed-unit and ambiguity coverage is still outstanding.
- This CI result verifies the bounded PCGN inventory assertions only. It does **not** establish the complete contextual vowel × consonant-series × shortening × coda matrix, a conformant runtime PCGN engine, a complete Ukrainian syllable adapter, or phonetic IPA coverage.
- No runtime code or Pages build inputs changed; no new deployment is required for this documentation-only update. Existing live site: https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System-/.
- Next implementation priority remains the context-dependent Khmer vowel/rime matrix and a source-aware PCGN engine; do not replace evidence gaps with guessed Ukrainian candidates.


## Final handoff head reconciliation — 2026-10-31

- Audit-register update commit: `a74a33dc77d1180eab32dbe79688442458d65d40`.
- Latest verified mainline documentation commit before this handoff update: `a74a33dc77d1180eab32dbe79688442458d65d40`.
- Matrix, repository audit, and handoff agree that workflow [41233203184](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41233203184) passed exact PCGN glyph and romanization assertions. The bounded inventory tasks are DONE_VERIFIED; the contextual romanization engine, full matrix, Ukrainian syllable adapter and broader adversarial coverage remain open.
- No production runtime or Pages build input changed in this cycle; the prior successful Pages deployment remains the live site evidence.
- Next implementation work must use source-backed contextual PCGN rules and explicit unresolved states. Do not synthesize unsupported Ukrainian candidates or treat the inventory CI as phonetic validation.


## Exact CI log detail and current head — 2026-10-31

- The exact-head workflow [41233203184](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41233203184), job `124631488043`, was inspected at the log level, not only by job conclusion.
- Exact results: `pytest -q` → **87 passed, 25 subtests passed**; `npm run check` → all configured web-engine, runtime, register-shifter and romanization checks passed (including the sample romanization test); `npm run build` → Vite production build succeeded and emitted `index.html`, `system.html`, and the expected asset bundles.
- The CI log contains non-fatal Node `punycode` deprecation and npm install-script warnings; no configured step failed.
- Latest handoff update commit before this section: `27b30e3250c8f8c92899cd50c654b7cca673a32e`. Treat this as a documentation-only checkpoint; no runtime behavior or Pages artifact inputs changed.


## Final audit/handoff synchronization — 2026-10-31

- Repository audit now includes exact CI log counts in commit `c8f9ed80e2ea45f34fa5ac4c86ecf306fc7f0634`.
- Latest verified documentation head before this handoff update: `c8f9ed80e2ea45f34fa5ac4c86ecf306fc7f0634`.
- Exact inventory acceptance evidence: 87 pytest tests + 25 subtests, configured npm checks passed, Vite production build passed. No full linguistic coverage claim is made.
- The master handoff, romanization matrix and repository audit preserve the same remaining acceptance criteria: contextual PCGN rules and engine; independent Ukrainian syllable adapter; wider malformed/mixed-input tests; adjudicated IPA gold. No code or deployment change occurred in this documentation synchronization.


## Open styling PR reconciliation — 2026-10-31

- Rechecked open PR #64 (`design/khmer-layout-20261030`) against current `main` `b4de6b248660b50d320ab24e8d3348fb1226d178`: branch is diverged, 7 commits ahead and 22 behind; merge base is `20e2e6dc296829986e52672d96b8730687aaa42a`. Its changes touch `index.html`, `system.html`, `src/styles/main.css`, and add `tests/test_layout_contract.py`.
- PR #64 remains open and untouched. Do not merge blindly: the CSS and layout-contract test need to be ported onto a fresh branch from current `main`, followed by current Python/web/build and visual/mobile verification. No styling changes were cherry-picked in this checkpoint.
- This is independent from the now-verified PCGN glyph inventory; no new Pages deployment or runtime change is claimed.

 
## Responsive layout merge and verification — 2026-10-31

- PR [#78](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/78) was merged by squash as `3b6e08177f9c90dddb27e787cc7a6deaa015c33e`.
- The PR adds 53 lines of focused responsive CSS overrides in `src/styles/main.css`; existing method-switch, IPA fallback, source-card and status styles were preserved rather than replacing the stylesheet from the diverged PR #64.
- Exact PR-head Quality workflow [41234615041](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41234615041) completed successfully. The sole job passed setup, checkout, Python dependency installation, `pytest -q`, Node dependency installation, `npm run check`, and `npm run build`.
- PR #64 remains open and untouched: its branch is substantially diverged; only the responsive behavior needed here was ported. Do not merge its broader CSS wholesale.
- The merge is UI-only. No Khmer phonological coverage, BGN/PCGN runtime, Ukrainian syllable adapter, or gold IPA corpus is completed by this change. Research prototype status remains unchanged.
- Pages deployment after this merge has not yet been verified. Check the Pages workflow and deployed site before claiming the live site includes this CSS.


## Sentence-level source-preservation regression — 2026-10-31

- Added and merged PR [#80](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/80) as `14113b5d45bbd36e53510b24a6f48f565a54bcd0`.
- The runtime regression passes the supplied Khmer greeting sentence through `convert()` and asserts that the normalized source and the concatenated per-unit source spans are identical, preserving whitespace and punctuation. It also requires an explicit aggregate Ukrainian result or fail-closed marker.
- Exact-head Quality workflow [41238197962](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41238197962) passed Python tests, Node web checks (including the runtime regression), and Vite build.
- This is a segmentation/source-preservation check, not independent IPA gold or a claim that every word in the sentence has an established pronunciation. The aggregate converter remains deliberately fail-closed when any unit is unresolved.
- The latest Pages deployment [41237778259](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41237778259) succeeded for main commit `cb48d4c660d3e7f826c677d871654157914ae59c`; PR #80 adds tests only and does not change the deployed runtime.


### Reconciliation update — open layout PR #64 — 2026-10-31

- Rechecked PR #64 (`design/khmer-layout-20261030`) against current main `6be7a09bb02824cfba2a50f17fdfd16faa5605e8`: diverged, 7 commits ahead and 22 behind; merge base remains `20e2e6dc296829986e52672d96b8730687aaa42a`.
- The branch changes `index.html`, `system.html`, and replaces `src/styles/main.css` wholesale; it also adds `tests/test_layout_contract.py` with assertions coupled to the old CSS implementation. Those exact selectors are not a portable contract for the current stylesheet and need redesign before reuse.
- The responsive layout improvements required for the current interface were already ported in focused PR #78 (`3b6e08177f9c90dddb27e787cc7a6deaa015c33e`) and its exact-head CI passed. No unique engine behavior is present in PR #64.
- PR #64 remains open and untouched; no wholesale CSS replacement or brittle test was ported. The existing IPA/method-switch styles and newer source-aware behavior are preserved.


### Full-sentence fail-closed output contract — 2026-10-31

- PR [#83](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/83) merged as `4a2e29dad27c80f2185db645a3971afe6315e022`.
- The sentence regression now asserts the exact aggregate markers `⟦ВИМОВУ НЕ ВСТАНОВЛЕНО ДЛЯ ЧАСТИНИ ВВОДУ⟧` and `⟦ТРАНСКРИПЦІЮ НЕ ВСТАНОВЛЕНО ДЛЯ ЧАСТИНИ ВВОДУ⟧` for the supplied greeting. This confirms that the engine preserves the input but does not claim a complete IPA or Ukrainian transcription when lexical units are not established.
- Exact-head Quality workflow [41239297284](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41239297284) passed Python tests, Node web/runtime tests, and Vite build.
- This is an explicit expected limitation, not a successful phonetic result. Supporting the sentence requires source-backed contextual phonology and lexical evidence, not weakening the fail-closed rule.

## Full-sentence romanization integration — 2026-10-31

- Main head: \`076ffaa1523afa7cc9ec9b8c2ca8e3a83cea101f\` (PR #89).
- PR #87 added the supplied full Khmer greeting sentence to the romanization test. Exact-head Quality workflow [41240282424](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41240282424) passed: 87 Python tests + 25 subtests, configured Node web/runtime/romanization checks, and Vite build.
- PR #89 merged the bounded UI integration fix: \`src/main.js\` now passes the complete input string to \`khmerToLatin(data.source)\`, rather than manually splitting on whitespace and invoking the library token by token. This follows the package's documented whole-text contract for preserving whitespace and punctuation, and its handling of the Khmer repetition mark \`ៗ\` ([package documentation](https://www.npmjs.com/package/@gmana/km-translit)).
- The exact regression checks that the sample is converted out of Khmer letters/signs while preserving both Khmer sentence stops, spaces, and the exclamation mark. Exact-head Quality workflow [41241149726](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41241149726) passed Python tests, Node web checks, and the Vite production build.
- This does not solve dictionary-based word segmentation inside unspaced Khmer runs; the library explicitly documents that limitation. Nor does it complete conformant BGN/PCGN 1972 contextual romanization or the independent romanization-to-Ukrainian adapter.
- PR #88 was closed as superseded; it used a stale pre-main branch and an incorrectly escaped Unicode test assertion. PR #64 remains open and untouched because its branch is diverged and replaces the stylesheet wholesale.
- No new Pages deployment is claimed. The site remains a research prototype; contextual PCGN coverage, a source-backed Ukrainian syllable adapter, and independently adjudicated phonetic gold remain open.

## Short mixed-text Khmer romanization regression — 2026-10-31

- PR #92 merged as \`99638ea6758d1553f3853d163c4b42ad8fe0741d\`.
- The supplied short sample \`សួស្តី 123! ភាសាខ្មែរ។\` now has an explicit whole-text romanization test. It verifies conversion of Khmer letters and preservation of ASCII digits, spaces, exclamation mark and Khmer sentence-stop punctuation.
- Exact-head Quality workflow [41242382955](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41242382955) passed Python tests, Node web checks and Vite build.
- This is an input-integrity regression, not BGN/PCGN gold or evidence of complete word segmentation/Ukrainian adaptation. No runtime code changed and no new Pages deployment is claimed.


## Native numerals and mixed Latin sentence regression — 2026-10-31

- PR #94 merged as `48e5d6c05d4a6ade8019c853135b7e2f6d655591`. The sample `២០២៦ ABC-42, សួស្តី។` verifies that Khmer numerals remain visible or are rendered as Arabic digits, ASCII digits and Latin text survive, and spaces/comma/Khmer sentence-stop punctuation are preserved while Khmer letters are romanized.
- Exact PR-head Quality workflows [41242836968](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41242836968) and [41242823462](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41242823462) passed Python tests, Node web checks and Vite build.
- Combined with PR #92's ASCII-number short sentence and PR #89's full Khmer greeting sentence, the romanization route now has explicit coverage for spaces, punctuation, native and ASCII numerals, and mixed Latin text. This is input-integrity evidence only; it does not establish the correct BGN/PCGN numeral rendering, word segmentation inside unspaced runs, complete contextual PCGN conformance, or a Ukrainian romanization adapter.


## Main-head verification after Khmer mixed-text regressions — 2026-10-31

- Current `main` head: `1a6921fc75dd011bc8097f6636b8077fc7c59cff`.
- Exact-main Quality workflow [41243972009](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41243972009) completed successfully. Pages workflow [41243971788](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41243971788) also completed successfully; both build and deploy jobs passed, including the deployed-site/runtime smoke test.
- Main has explicit whole-text romanization regressions for the full Khmer greeting, short mixed-script input, ASCII numbers, native Khmer numerals, Latin text, spaces, commas and Khmer sentence-stop punctuation. The application passes the complete input to the romanization library rather than manually tokenizing by whitespace.
- The full greeting's phonetic route intentionally remains fail-closed where source-backed contextual phonology is missing. The romanization library's documented inability to segment dictionary words within unspaced Khmer runs is not repaired by these tests.
- This verifies whole-text input integrity and deployed artifact behavior, not full BGN/PCGN 1972 conformance, Ukrainian romanization adaptation, or independently adjudicated IPA gold.
- Open PR #64 remains untouched: it is a diverged wholesale layout/CSS rewrite; focused responsive improvements were already ported separately in PR #78. Do not merge #64 without a fresh rebase/port and current browser/visual verification.
- Remaining blockers: source-backed contextual PCGN rules/engine, independent syllable-level romanization → Ukrainian adapter, unspaced word segmentation, broader malformed-input parity and independently adjudicated phonetic gold. Research prototype status remains unchanged.


## Post-merge verification for PR #95 — 2026-10-31

- PR #95 merged as `28a9bbb909ca57735ceca92f262c2de9eeb43396`; it synchronizes current whole-text romanization and deployment evidence without changing application code.
- Exact post-merge Quality workflow [41246343908](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41246343908) passed. Pages deployment [41246343845](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41246343845) also passed, including the deployed-site/runtime smoke test. This is the current verified main head.
- The full/short sentence, mixed-script, native/ASCII numeral, whitespace and punctuation tests remain engineering/input-integrity coverage. The phonetic route remains fail-closed for unsupported contexts; this is not full PCGN conformance, word segmentation, Ukrainian adaptation or independently adjudicated IPA gold.
- PR #64 remains open, diverged by 35 commits behind current main and is not merged. Its 7-commit CSS/layout branch is preserved; focused responsive improvements remain in the merged PR #78.


## Whole-message mixed-script segmentation regression — 2026-11-01

- PR [#97](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/97) merged as `72e4644204c879f905ebaa20dddd2d00b6583d32`.
- Added a canonical adversarial case containing Khmer, Latin identifier, ASCII digits, Khmer numerals and punctuation, tab, CRLF, U+200B and an unsupported symbol.
- The test consumes the canonical fixture, requires exact reconstruction from `segment_syllables()`, confirms a supported Khmer example remains structurally established and confirms the unsupported symbol remains locally invalid/unsupported.
- Exact PR-head Quality checks [41289845696](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41289845696) passed: Python tests, web checks and production build.
- The fixture has `ipa: null` and explicit non-phonological provenance; it is structural/source-integrity evidence, not IPA gold or an accuracy benchmark row.


## Goruut comparator research — 2026-11-01

- Task `KHM-G2P-GORUUT-001`: `PARTIAL` (upstream availability/source triage only; runtime execution and quality validation pending).
- Inspected and pinned upstream Goruut commit `b224bde02151f8f86d0fe260804e4ca743bda620`; upstream README advertises Khmer Central, IPA output, word tokens and tone support, but no syllable tokens or tie bars and no number/date normalization. MIT applies to source code; embedded dictionary/model asset licenses remain unaudited.
- Recorded the candidate and limitations in `docs/benchmarking-and-external-ipa.md`, alongside a triage note for Khmer NLP KCC: its advertised G2P tokens are not established as IPA and its downloaded checkpoint/data need separate license review. PR [#98](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/98); exact PR-head CI [41302072416](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41302072416) passed before this handoff-only follow-up commit.
- No Goruut/KCC runtime invocation or output artifact was produced. Independent gold remains 0; no accuracy or winner claim. Next acceptance: run pinned Goruut in isolated optional CI, audit asset provenance, review Khmer register/inherent-vowel/coda/syllable conventions, and score only independent expert-adjudicated IPA.


## Goruut asset licensing reconciliation — 2026-11-01

- Task `KHMER-CENTRAL-G2P-GORUUT-001` remains `BLOCKED` for runtime execution, not merely PARTIAL: the source-code MIT license does not establish rights for the language-specific lexicon/model assets.
- The pinned Goruut source tree contains embedded files under `dicts/khmer/central/`; Goruut's own data-preparation documentation states these model assets derive from a `lexicon.tsv`. The corresponding separate `neurlang/dataset/khmer/central/` lexicon is present, but dataset repo metadata declares no license, root tree has no LICENSE/COPYING, and the README does not allocate a license/provenance to this language.
- No runtime invocation, output artifact, or quality claim is made. Next acceptance: per-language source/provenance and rights for both lexicon and derived weights, then owner-approved usage decision, followed by isolated pinned execution and independent expert IPA adjudication.
- Detailed evidence and exact upstream paths: `docs/audits/current/GORUUT-ASSET-LICENSE-REVIEW-2026-11-01.md`.


## External corpus/source triage — 2026-11-01

- Task `KHM-MEKONGPHON-001`: `PARTIAL` for discovery and evidence triage; external data import / benchmark gold remains `BLOCKED` pending source-specific rights and expert validation.
- MekongPhon LREC 2026 source triage is PARTIAL: the paper reports 1.3M Khmer orthography–IPA pairs; inspected GitHub main `f80f6c1840c4818b51e05f2e00cded4701a5b662` includes lexicon/train/eval files and a documented SEAlang/OPUS lexicon-based sentence conversion pipeline. Import remains BLOCKED: repository license is undeclared; sentence IPA is generated by greedy dictionary lookup with OOV sentences filtered; the committed split script reserves only 100 lexicon lines (seed 1234). A second lead, chemvatho/Khmer-acoustic-model, claims a 29,204-entry native-validated IPA dictionary and CC BY-SA 4.0 in README, but dictionary/README says CC BY 4.0 and the full dictionary is absent from the current tree (only six sample entries). Resolve rights and availability before use. Gold remains 0.
- No external corpus rows, IPA labels, model weights or audio were copied into the repository. No accuracy score or engine ranking is claimed.
- Full source register and acceptance gates: `docs/audits/current/EXTERNAL-PHONETIC-CORPUS-TRIAGE-2026-11-01.md`.


## KHM-GORUUT-RUNTIME-001 — PARTIAL

- Added an optional, test-only HTTP runtime probe for Goruut at pinned upstream commit `b224bde02151f8f86d0fe260804e4ca743bda620`. It explicitly enables `KhmerCentral` in `BuiltinDictLanguages`, builds the upstream Go binary and records raw JSON responses for source-attested lexical probes plus multiword/punctuation cases. `scripts/benchmark_goruut.py` records commit, language, input SHA-256, raw response, tokens and errors; it does not normalize or score IPA. Existing source-attested IPA remains non-gold. Accuracy=null; independent gold=0. Workflow: `.github/workflows/optional-goruut-runtime.yml`; artifact retention 30 days.
- Acceptance: exact-head optional workflow must pass; inspect raw output for language coverage, unknown-word behavior, punctuation, multiword segmentation, malformed/unicode cases and phonetic output consistency. Keep raw data and errors; do not normalize tone/length/diacritics.
- Status remains PARTIAL until runtime artifacts are inspected and language-specific expert gold exists. The test-only CI checkout is not a production dependency or data import.


## KHM-GORUUT-RUNTIME-001 — PARTIAL (runtime executed; not promoted)

- The pinned Goruut runtime was executed with KhmerCentral enabled (Go 1.23.12). Engineering probes returned 8/8 responses; 6 source-attested IPA probes returned 6/6, but only 1/6 was an exact NFC/whitespace concordance (not accuracy/gold). Clear incomplete outputs: `ខ្មែរ` → `kʰr` vs source `kʰmae`; `ភ្នំពេញ` → `pʰɲ` vs `pʰnum ˈpɨɲ`; `ភាសាខ្មែរ` → `pʰiəsaːkʰr` vs `pʰiəsaː kʰmae`. Server log repeatedly reports missing `weights9.bin.zlib`. Do not promote. Full evidence: `docs/audits/current/GORUUT-RUNTIME-EVALUATION-2026-11-01.md`.
- Runtime/build/HTTP availability is verified for the returned probes. Phonetic accuracy, dialect coverage and IPA convention are not verified; independent expert gold remains 0.
- Acceptance to progress: investigate the repeated missing `weights9.bin.zlib` warning and raw outputs; resolve unsupported/empty responses; create a language-specific expert-adjudicated held-out IPA set; rerun and inspect exact artifacts. Production integration remains deferred until those gates pass.


## KHM-GORUUT-RUNTIME-001 — PARTIAL, repeatability evaluated

- Three-repeat re-evaluation: 8/8 engineering outputs and 6/6 source-attested probe outputs were stable across repeats; only 1/6 source-attested IPA rows matched exactly. Stable but incomplete outputs include `ខ្មែរ` → `kʰr` vs `kʰmae` and `ភ្នំពេញ` → `pʰɲ` vs `pʰnum ˈpɨɲ`. Stable execution does not offset the phonetic mismatch. This is not accuracy or gold.
- Production integration remains blocked by insufficient source concordance, missing/unsupported outputs or incomplete phonetic forms. Independent expert gold remains 0.
- Next acceptance: investigate upstream missing-weight warning and language-specific mapping; resolve every no-output and unstable-tone case; commission expert IPA gold; rerun the pinned artifact and retain raw evidence.


## Cross-engine comparator evidence — PARTIAL

- Cross-engine check: khmerphonemizer 0.0.3 returned 6/6 source-attested probes; 2/6 strict IPA strings and 6/6 limited-notation matches. Goruut returned 6/6 stable outputs but only 1/6 strict and 3/6 limited-notation matches. This small source-attested sample favors khmerphonemizer as a comparator, not as proven production phonology. No independent gold exists.
- No external result is accepted as independent gold. Production selection remains blocked pending expert adjudication and repeatable, dialect-scoped validation.


## KHM-GORUUT-RUNTIME-001 — PARTIAL (exact-head evidence recorded)

- Exact PR #101 head `eeeede50447c41df30f866bcbf77f56824b40190` runtime build and HTTP probe passed: [41310808284](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41310808284); artifact SHA-256 `34330aac3be84a438a7bdc181d715f12b745cfe6f7e15edcd4be08dcbfeb52da`.
- Three-repeat results: engineering 8/8 stable; source-attested 6/6 stable; strict concordance 1/6 and limited notation diagnostic 3/6. Stable missing-segment outputs are present; not accuracy, gold=0.
- Missing `weights9.bin.zlib` warning persists; causal relation unknown. Keep as optional comparator only; production promotion rejected.
- Full run evidence and config hash: `docs/audits/current/GORUUT-RUNTIME-EVALUATION-2026-11-01.md`.


## Goruut nondeterminism root-cause finding — Khmer

- The latest artifact had no RandomizationWordsCount / RandomizationWordsChoices metadata on any of the 14 inputs; all 14 were stable across three repetitions. Its problem is different: stable but incomplete dictionary output (e.g. missing vowels), not the homograph-selection instability observed in Lao/Burmese.
- Upstream pinned selector counts homographs and falls back to a random dictionary pronunciation when no preferred entry is selected; response counters are `RandomizationWordsCount` and `RandomizationWordsChoices`. See [selector source](https://github.com/neurlang/goruut/blob/b224bde02151f8f86d0fe260804e4ca743bda620/repo/services/parts_of_speech_selector_service.go#L168-L205).
- Missing `weights9.bin.zlib` is a separate warning; causality is not established.


## KHMER Goruut source-coverage gate — PARTIAL

- Raw runtime evidence was re-analysed using `PrePunct`, `CleanWord`, and `PostPunct`; non-empty phonetic output is not sufficient evidence of complete coverage.
- - Runtime workflow: [41311611360](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41311611360); artifact [13085627015](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41311611360/artifacts/13085627015); ZIP SHA-256 `30988a1aae36261f94319286c0815b184f5effb633527f79d07e6011334d19aa`.
- - Input SHA-256 `3d93a49c0162b5de4374c51d742fab0d2f5f975251c09664faefc9870535df49`; engine `b224bde02151f8f86d0fe260804e4ca743bda620`; Go `1.23.12`; config SHA-256 `d2f19f923da8ca089ba9133465018903263f681b57a1177152ab07f2a284225e`.
- - 97/100 inputs returned at least one phonetic token; 3/100 returned an empty Words array. Of the 97 responses, 96 were stable across three repetitions and one (`ជួត`) was unstable.
- - Source coverage was independently re-analysed from `PrePunct`, `CleanWord`, and `PostPunct`. A row counts complete only if these fields reconstruct the original input after NFC/whitespace removal and no letters, combining marks or numbers are relegated to PrePunct/PostPunct. Result: **70/100 complete**, **27/100 partial**, **3/100 no output**. This is a source-preservation check, not a phonetic correctness score.
- - 27 partial cases include examples where the engine emits only a suffix or prefix as phonetic output and stores remaining Khmer letters in punctuation fields, e.g. `បេះបិទ` → CleanWord `ទ`, PrePunct `បេះបិ`, Phonetic `t`; `ថួន` → CleanWord `ន`, PrePunct `ថួ`, Phonetic `n`. The API's non-empty Phonetic response therefore substantially overstates usable coverage.
- - Strict source-attested concordance: **6/100 (6%)**; limited notation diagnostic: also 6/100. These are not accuracy or gold agreement. The source field is MekongPhon's generated `pron_no_tones`, not independent expert gold.
- - The one unstable input `ជួត` carried `RandomizationWordsCount=1`, `RandomizationWordsChoices=2`; the other 99 did not show that metadata.
- The benchmark harness now has tests for dropped source characters and source letters in punctuation fields; exact-head CI is still pending. No accuracy score or production promotion is claimed.
- Full evidence: `docs/audits/current/GORUUT-RUNTIME-EVALUATION-2026-11-01.md`.


## Owner scope decision — temporary test-only use — 2026-11-01

The repository owner explicitly directed that external Goruut assets may be used for temporary verification and comparison without blocking these tests on license review. Accordingly:

- **Test-only execution:** authorized for this research task; do not stop runtime probes because the external asset license is unresolved.
- **No data/model import:** no Goruut dictionary, model weight, or MekongPhon source row is copied into the product runtime or committed as a corpus by this decision.
- **Production packaging or redistribution:** not authorized by this instruction and remains outside this test-only scope; asset provenance/rights must be revisited before any bundling, redistribution, or production deployment.

This is a project scope decision, not a legal conclusion about the upstream assets.


### Khmer source-coverage repeat-run evidence

## Re-run with source-coverage and randomization counters — 2026-11-01

The updated harness completed on PR branch commit `b9f706473e4e03c6e446254703b7e6e09d863cce`: [runtime workflow 41312379618](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41312379618), artifact [13086660287](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41312379618/artifacts/13086660287), ZIP SHA-256 `dd6934c304e802bf5aabbce2802a92c11855e8a0e3d37d05b7ca7f19b12d41e4`.

- The 100-row MekongPhon report independently reproduces **70 complete / 27 partial / 3 no-output** source-coverage results; 96 outputs were repeat-stable, one was unstable. The unstable word carried dictionary-randomization metadata in all three repetitions.
- Strict source-attested concordance remains 6/100, with 6/100 on the limited notation diagnostic. Accuracy remains null; independent gold remains 0.
- The eight engineering probes that were previously described as 8/8 successful responses are now correctly classified as **3 complete and 5 partial**. All eight had non-empty phonetic output, but five did not preserve the full source word through CleanWord/PrePunct/PostPunct.
- The six-row source-attested sample is 3 complete / 3 partial; its strict 1/6 and notation-only 3/6 matches are not accuracy.

This confirms the coverage gate is functioning on a real 100-row run. The current PR head adds an additional empty-phonetic-token guard and associated tests; final exact-head CI remains pending.



## Final Goruut / Khmer G2P PR #101 reconciliation — 2026-11-01

- Final head `1e9cbfdf4f21514e4f39093d51ea3f923133a90a`: repository checks [41313433562](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41313433562), Khmer G2P [41313433619](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41313433619) and Goruut [41313433641](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41313433641) all **PASS**.
- Khmerphonemizer 0.0.3 returned 100/100 outputs, but 0/100 rows were comparable because the input split provided no source IPA labels. This is an availability result only, not accuracy.
- Goruut 100-row results: 97 outputs, 3 no-output; source coverage 70 complete / 27 partial / 3 unknown; 96 stable / 1 unstable; one randomized dictionary input; strict source-attested concordance 6/100. The eight engineering probes had 3 complete and 5 partial outputs. Accuracy remains null, independent gold=0.
- Artifacts: Khmerphonemizer [13086870731](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41313433619/artifacts/13086870731), SHA-256 `86ef634b67dd60ca121cfe11a8549a42e7ee2e4655447851e91a4eefffb7a1b2`; Goruut [13085864084](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41313433641/artifacts/13085864084), SHA-256 `469bd4f9fc0baa3e8366724e43dfcb802427eca3d70c916be1e98ff6d779583d`. Both downloaded archive hashes matched GitHub's digest.
- Runtime-probe code and exact-head CI are **DONE_VERIFIED**. Goruut production use remains rejected. Khmerphonemizer accuracy and production suitability remain **BLOCKED** until an appropriate source IPA set and independent expert adjudication exist. The `weights9.bin.zlib` warning is unresolved; causality is not established.


## Khmer source-IPA comparator correction — 2026-11-01

The previous addendum's statement that the 100-word MekongPhon split lacked IPA was incorrect. The workflow included `pron_no_tones` under `source_reported_ipa`; the benchmark runner read only `ipa`, silently dropping the reference labels. I added a regression test first and observed the intended failure on [41325025559](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41325025559): 1 failed, 106 passed, 25 subtests. The minimal fix, `source_ipa_from_metadata`, now supports both field names.

Final head `1a0a8190e60d003b2e48ac29da21ce553822130c` passed repository CI [41325152300](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41325152300) and [41325147911](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41325147911), plus optional G2P run [41325147987](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41325147987). Corrected artifact [13091145662](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41325147987/artifacts/13091145662), SHA-256 `b3e2262c5f72d51c770ec88c3cf880387d1aa03ab5bc4beafc85e0551ec1f2f9`, reports 100/100 outputs, 100 comparable source labels, 18 strict matches and 19 limited-notation matches. These are not accuracy: gold=0, accuracy=null.

The earlier 0-comparable count is superseded. The bug was in our report adapter, not absent source data. The fix is a research-harness correction only; no production phonology changed.


## Final Khmer run reconciliation — PR #101

Final-head repository checks [41325417322](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41325417322) and [41325414211](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41325414211), Goruut [41325417330](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41325417330) and corrected Khmerphonemizer [41325417374](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41325417374) all passed. Goruut artifact [13090873861](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41325417330/artifacts/13090873861): 97/100 outputs, 70 complete / 27 partial / 3 unknown, 96 stable / 1 unstable, 6/100 source-attested exact matches. Khmerphonemizer artifact [13091310659](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41325417374/artifacts/13091310659): 100/100 outputs, 100 comparable source labels, 18 strict and 19 limited-notation matches after fixing the dropped `source_reported_ipa` field. Both archive hashes match GitHub digests. These are source concordance only, not accuracy; independent gold=0, accuracy=null.


## Session closeout — 2026-11-01

- PR [#101](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/101) was reviewed and squash-merged into `main` as `211a5273a0bebc8b95bee7c821ec3aa63ebcfa60`; the main branch head was verified to equal that SHA.
- Post-merge quality checks [41326232442](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41326232442) PASS; optional G2P smoke [41326232443](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41326232443) PASS; GitHub Pages build/deploy and deployed-site/runtime smoke test [41326232421](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41326232421) PASS.
- Final PR-head Goruut runtime [41325808140](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41325808140) PASS; artifact [13091003881](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41325808140/artifacts/13091003881), SHA-256 `079c6e56ad178815bba2159ec4720f538b01071a17cb1d030fcf4d024f8696f2`: 97/100 outputs, 70 complete / 27 partial / 3 unknown, 96 stable / 1 unstable, 1 randomized input, 6/100 strict source-attested matches. The 8 engineering probes had 3 complete / 5 partial.
- Corrected Khmerphonemizer 0.0.3 comparison [41325808089](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41325808089) PASS; artifact [13090603852](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41325808089/artifacts/13090603852), SHA-256 `668668bb1a6a3aca45145b0894c83000889695e6d25878d794622fef64e5e5d2`: 100/100 outputs, 100 comparable source labels, 18 strict and 19 limited-notation matches. This follows the test-first fix for the dropped `source_reported_ipa` metadata field (red CI: 1 failed, 106 passed, 25 subtests; final CI passed).
- Goruut test harness and exact-head CI: **DONE_VERIFIED**. Production phonology remains **PARTIAL/BLOCKED**: 27/100 Goruut outputs partial, 3/100 absent; source labels are not independent gold; independent expert Khmer IPA gold remains 0. Khmerphonemizer concordance is diagnostic only. Permanent source-data/model import remains outside the approved test-only scope.
- No local checkout was available; engineering verification is from exact-head and post-merge GitHub Actions. See runtime audit for full evidence and hashes.


## Linguistic completion register — 2026-11-01

- Current verified `main` baseline: `c0a2b33c86791b6546e1158c62043fd23acc1f60`; latest exact-main engineering workflow: https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41326462947 (success). See the linked current audit register for the verified status and next acceptance criteria: [Linguistic completion register](audits/current/LINGUISTIC-COMPLETION-REGISTER-2026-11-01.md).
- Reconfirmed `data/benchmark/gold.tsv` contains only its header. Independent expert-adjudicated lexical IPA gold remains **0**; empirical accuracy remains **null**. No external source-attested labels or engine outputs are promoted to gold.
- The register separates implementable repository work from external expert, primary-source and licensing blockers. Preserve existing canonical plans, registries, tests and generated data; do not create parallel corpora or weaken fail-closed behavior.
- No local checkout was available for this pass. GitHub Actions provide exact-main engineering evidence only; they do not prove linguistic accuracy, manual accessibility QA or legal permissions.
## Current master-matrix status override — 2026-11-01

The following current statuses supersede older checkpoint rows above where they conflict; historical evidence remains preserved.

| Task | Current status | Current acceptance boundary |
|---|---|---|
| KH-TEST-001 | BLOCKED | Gold TSV is header-only; independent expert-adjudicated lexical IPA gold=0; accuracy=null. Requires independent annotation, adjudication, profile and source/audio locators. |
| KH-VOW-001 / KH-VOW-002 | PARTIAL | Orthographic/register inventory exists; full context-dependent vowel/rime/series matrix and acoustic/phonetic adjudication remain open. |
| KH-CODA-001 | PARTIAL | Structural cases and fail-closed behavior exist; full coda-conditioned IPA coverage remains open. |
| KH-IPA-001 | PARTIAL | IPA boundary/status contract exists; complete contextual orthography-to-IPA model and gold remain open. |
| KH-PROFILE-001 / KH-PROFILE-002 | PARTIAL | Fail-closed guards are verified; complete Phnom Penh /r/-loss environment model and expert validation remain open. |
| KH-G2P-001 | DONE_VERIFIED (harness only) | Goruut and Khmerphonemizer comparisons are diagnostic; no accuracy claim or production promotion. |
| KH-ROM-001 | PARTIAL | BGN/PCGN bounded inventory exists; full contextual runtime and independent Ukrainian syllable adapter remain open. |
| KH-UI-001 | TODO | Manual deployed visual, keyboard, screen-reader and mobile QA not evidenced by CI. |
| KH-REL-001 | PARTIAL | Release remains blocked by phonological gold and asset-rights review. |


## IPA gold corpus implementation checkpoint — 2026-11-01

### Current task ledger

| Task | Status | Evidence / remaining acceptance |
|---|---|---|
| IPA-GOLD-SCHEMA-001 | DONE_VERIFIED | Six versioned JSON Schemas; empty JSONL templates; validator and regression tests in exact-head CI |
| IPA-GOLD-DOUBLE-ANNOTATION-001 | PARTIAL | Enforces two distinct annotators and third independent adjudicator; actual blind collection needs qualified human annotators and controlled intake |
| IPA-GOLD-ADJUDICATION-001 | PARTIAL | Agreement/resolved/unresolved semantics and rationale validation implemented; no real adjudicated rows exist |
| IPA-GOLD-SPLIT-001 | DONE_VERIFIED | Deterministic SHA-256 split assignment, preserves frozen assignments, prevents lexeme-group leakage; current manifest empty |
| IPA-GOLD-EXPORT-001 | DONE_VERIFIED | Exports only adjudicated, redistributable rows into existing benchmark TSV; current export has header only |
| IPA-TYPED-BENCHMARK-001 | DONE_VERIFIED | PHONEMIC / PHONETIC_BROAD / PHONETIC_NARROW retained; type mismatch cannot count as exact match |
| IPA-GOLD-RELEASE-GATE-001 | PARTIAL | Tag/manual workflow requires 100/25/25 adjudicated split rows and rights; owner must require the check in release rulesets/procedure |
| KHMER-VOWEL-CONTEXT-001 | PARTIAL | Research workpack requires sign × series × length × coda × profile matrix and source/audio locators |
| KHMER-CODA-001 | PARTIAL | Existing structural cases retained; full coda-conditioned surface IPA and acoustic validation remain open |
| KHMER-R-LOSS-001 | PARTIAL | Wayland & Guion (2005) and Kirby (2014) located; /r/-loss must remain profile/style-conditioned, with matched multi-speaker evidence |
| KHMER-UA-IPA-ADAPTER-001 | PARTIAL | Existing adapter retained; independent expert target review awaits adjudicated surface IPA |

### Evidence boundary

The four JSONL files are empty templates. `gold.tsv` is header-only; independent expert gold=0 and accuracy=null. Wayland & Guion's study describes two Phnom Penh speakers and a specific colloquial /Cr/ environment; it does not justify universal /r/ deletion. No IPA labels were added.

See [IPA gold protocol](docs/ipa-gold-corpus.md), [Khmer phonology workpack](docs/audits/current/PHONOLOGY-RESEARCH-WORKPACK-2026-11-01.md), and [evidence registry](docs/evidence.md).

### Additional rights and export controls

| Task | Status | Acceptance / remaining work |
|---|---|---|
| IPA-GOLD-RIGHTS-001 | DONE_VERIFIED (mechanism) | Approved license registry, per-record rights evidence, rejection of unregistered/non-redistributable licenses; legal verification of future source-specific records remains required |
| IPA-GOLD-PROVENANCE-EXPORT-001 | DONE_VERIFIED | Gold TSV and benchmark rows retain source ID, license ID and rights-evidence locator |
| IPA-GOLD-BLIND-INTAKE-001 | BLOCKED | Requires external controlled intake; public GitHub history cannot provide blind annotation |

The rights registry does not itself grant permission. Each real source still needs its exact license/permission verified by a responsible curator, and share-alike/attribution terms must be honored in distribution.


### 2026-11-01 follow-up — validator and Khmer research evidence

- IPA-GOLD-SCHEMA-001 remains DONE_VERIFIED (mechanism), now with runtime/schema parity checks: closed object properties, mandatory annotation notes, string uncertainty arrays, ISO dates and optional field types.
- IPA-TYPED-BENCHMARK-001 remains DONE_VERIFIED (mechanism): adjudicated gold requires a valid IPA kind; missing/different prediction kinds cannot score as exact matches or enter CER.
- Wayland & Guion (2005) is a two-speaker, 20-item, three-repetition-per-style Phnom Penh study; its /r/-loss findings remain profile- and speech-style-conditioned. Kirby (2014) provides complementary production/perception evidence. Chem & Chem (2020) is a Phnom Penh acoustic vowel source, not yet a complete contextual matrix.
- Independent expert gold remains 0; gold.tsv remains header-only. No IPA entries or universal /r/-loss rule were invented.


### Research artifact — Khmer

- [KHMER vowel × series × coda evidence matrix](docs/audits/current/KHMER-VOWEL-SERIES-CODA-EVIDENCE-MATRIX-2026-11-01.md): specialist ɑ/ɔ-class mappings, Chem (2020) sample/method and coda effects, and missing contextual cells.
- Wayland & Guion's /r/-loss remains restricted to the studied Phnom Penh colloquial profile; no universal deletion rule was introduced.


## 2026-11-01 implementation and verification closeout

- Starting main SHA: c0a2b33c86791b6546e1158c62043fd23acc1f60 (main remains unchanged).
- Implementation branch: feat/ipa-gold-corpus-20261101-review.
- Comprehensive PR: [#103](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/103); PR-head implementation checkpoint SHA: 608d2d92c5e883c095bf0c679b7353bd442ee55c.
- PR CI: [Quality checks](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41337410745) SUCCESS — 136 Python tests + 27 subtests; Khmer register-shifter browser contract, web checks and Vite build passed.
- This branch includes the previous documentation-only PR #102 in full; #102 was closed as superseded after its content was verified in #103. No branch was deleted.
- Legacy PR [#64](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/64) remains open and untouched: it is a divergent legacy CSS/layout patch and was not blindly merged.
- Existing feature branch feat/independent-ipa-gold-corpus-20261101 was left untouched because its history is substantially broader; the narrower review branch is the PR source.
- No local checkout was available; all verification claims above are GitHub Actions evidence, not local command runs.

### Final task ledger

- Corpus schemas/runtime validator, license registry, frozen group-safe splits and typed benchmark: DONE_VERIFIED (implementation and CI only).
- Actual independent expert annotations and adjudicated gold: BLOCKED — no qualified annotators or adjudicated source dataset supplied; gold.tsv remains header-only, gold count 0, accuracy null.
- Full vowel × consonant-series × final matrix and independent /r/-loss replication: PARTIAL/BLOCKED — see the Khmer evidence matrix; Chem's four-speaker Phnom Penh sample and Wayland & Guion's two-speaker /r/-loss sample are profile-limited.
- Release gate: PARTIAL — count, rights, adjudication and split checks exist and fail closed on empty gold; project owner must require the gate in repository rulesets/release procedure, and feature-coverage thresholds require an expert-approved matrix.
- Manual UI/accessibility review: TODO.

**Readiness:** research infrastructure is substantially improved; the language system remains a research prototype, not production/release-ready.


The Khmer evidence matrix now contains the full Ishida phone-to-grapheme mapping table, including stress, coda and final-conditioned variants. Chem's acoustic evidence still does not fill every series × vowel × coda cell, so the language model remains PARTIAL.


## 2026-11-01 final IPA-kind consistency verification

- Added fail-closed cross-annotation consistency: both independent annotations for one record must use the same `ipa.kind`, and a `RESOLVED` adjudicated result must preserve that kind. This prevents phonemic-vs-phonetic representation differences from being misclassified as pronunciation disagreements.
- Regression evidence: both new tests failed against the pre-fix validator on the test-only commit, then passed after the validator change.
- New task `IPA-GOLD-REPRESENTATION-KIND-001`: **DONE_VERIFIED** (mechanism and exact-head CI). Blindness, annotator qualifications and independent adjudicator competence remain external operational evidence, not properties CI can prove.
- Final PR head: `f7f2bf9a471f5fea990c0cf9509d382e3371d17b`; CI run [41338461515](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41338461515) SUCCESS — 139 Python tests + 27 subtests; browser register-shifter contract, web checks and Vite build passed.
- The Khmer matrix remains PARTIAL: full profile × series × stress × coda lexical coverage and an independent broader /r/-loss replication are not available.
- Gold remains zero; `gold.tsv` remains header-only; empirical accuracy remains null. No IPA labels were generated.


## CI action runtime modernization — 2026-11-01

- Status: `DONE_VERIFIED` (CI maintenance only; no Khmer phonology or transcription behavior changed).
- Updated all five workflow files to current Node.js 24-compatible action majors: `actions/checkout@v7`, `actions/setup-python@v7`, `actions/setup-node@v7`, `actions/setup-go@v7`, and `actions/upload-artifact@v7`. Existing Pages actions remain at `configure-pages@v6`, `upload-pages-artifact@v5`, and `deploy-pages@v5`.
- Tested code commit: `61d98b1417a6d0200df4722523e8caeae90269fd`.
- Exact-head verification: [Quality checks 41339636053](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41339636053) SUCCESS; [optional Goruut 41339636042](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41339636042) SUCCESS; [optional G2P smoke 41339636117](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41339636117) SUCCESS.
- Verified workflow coverage: 139 Python tests + 27 subtests, browser register-shifter contract, web checks and Vite production build passed on the exact code commit.
- Local checkout was unavailable; verification evidence is GitHub Actions. The gold corpus remains empty and empirical accuracy remains unmeasured.


## Frozen split-manifest schema parity — 2026-11-01

- Status: `DONE_VERIFIED`.
- Review found that `assign-splits` accepted unknown properties in existing split rows even though the split JSON Schema is closed; the generator could silently discard those fields when rewriting the manifest.
- RED evidence: regression `test_assign_splits_rejects_unknown_properties_in_existing_manifest` failed as expected on test-only commit `3fdfd9559dfc98c43c4c503b9e707f1632ebad07` ([run 41340259859](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41340259859)).
- GREEN implementation: shared `SPLIT_PROPERTIES` is now used by both cross-file validation and `assign-splits`; the generator rejects unknown fields instead of dropping them. Code commit: `64851a4572437d9185b47fcff56bde55e4f092c5`.
- Exact-head verification: [PR Quality checks 41340405233](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41340405233) SUCCESS and [push checks 41340400309](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41340400309) SUCCESS — 140 Python tests + 27 subtests; browser register-shifter contract, web checks and Vite production build passed. Optional Goruut and G2P smoke checks also passed on this head.
- Shared implementation and regression test are byte-identical across Lao, Khmer and Burmese branches. No corpus rows or IPA labels were added; independent gold remains zero and accuracy remains null.


## Product-corpus license eligibility — 2026-11-01

- Status: `DONE_VERIFIED` (policy enforcement; no source corpus or license grant was changed).
- Review found that the license registry accepted `redistributable: true` together with `commercial_use: false/null` or unknown attribution/share-alike terms. That could make a non-commercial or legally incomplete entry eligible for the product corpus if the registry were misconfigured.
- RED evidence: the new runtime and schema-contract tests failed on test-only commit `83cfdc10716eff99f622f5d0e3c9c035bee3b56e` ([run 41340790159](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41340790159)).
- GREEN implementation: a redistributable license must explicitly set `commercial_use: true` and boolean `attribution_required` + `share_alike`; the JSON Schema now encodes the same conditional rule. Code/schema commit: `b3104d6815edb3950e13457f7e04bcb8f5f90145`.
- Exact-head verification: [PR Quality checks 41340930079](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41340930079) SUCCESS and [push checks 41340925788](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41340925788) SUCCESS — 142 Python tests + 31 subtests; browser register-shifter contract, web checks and Vite production build passed. Optional Goruut and G2P smoke diagnostics also passed.
- This is a conservative product-corpus eligibility rule, not a legal opinion about all uses of these licenses. Each real source still needs human rights review. No IPA gold rows were added; independent gold remains zero and accuracy remains null.


## Release-gate threshold validation — 2026-11-01

- Status: `DONE_VERIFIED`.
- Review found that the CLI accepted zero/negative `--min-train`, `--min-dev` and `--min-test` thresholds. That could let an operator weaken a release gate below a meaningful non-empty split requirement.
- RED evidence: the six invalid threshold cases (0 and -1 for each split) failed as expected on test-only commit `888ce85258e0c42b44e082e06023dbcd96401b96` ([run 41341526589](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41341526589)).
- GREEN implementation: all three minimums must be positive integers. Invalid threshold configuration is added to the gate's aggregated findings rather than raised before corpus checks, preserving diagnostics for other blockers. Final code commit: `38aed74299c898461607407b730085e1b70d565d`.
- Exact-head verification: [PR Quality checks 41341743668](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41341743668) SUCCESS — 143 Python tests + 37 subtests; browser register-shifter contract, web checks and Vite production build passed.
- The configured release-gate defaults remain train=100, dev=25, test=25. No gold rows or IPA labels were added; independent gold remains zero and accuracy remains null.


## Controlled IPA gold acquisition checkpoint — 2026-11-01

- Added `docs/ipa-gold-collection-playbook.md` on `feat/ipa-gold-corpus-20261101-review`. This defines a human-led 30-lexeme process pilot, one predeclared pronunciation profile and IPA convention per corpus version, a curator, two blind independent annotators, and a third independent adjudicator. It sets explicit start/pilot-accepted/benchmark-ready gates and distinguishes pilot data from held-out evaluation.
- This is a protocol/documentation deliverable, not evidence that annotators have been recruited or that any IPA gold has been collected. The four JSONL corpus inputs remain empty; no gold labels or accuracy claims were added.
- External source lead: MekongPhon (LREC 2026) reports 367k Lao and 1.3m Khmer orthography–IPA pairs. It is recorded only as a candidate external reference. Its dataset-specific license, variety/profile, IPA convention, provenance, verification method, and overlap with engine development data must be checked before use. The LREC proceedings CC BY-NC-4.0 notice does not establish the dataset license. https://lrec.elra.info/lrec2026-main-129
- Khmer additional lead: chemvatho/Khmer-acoustic-model reports a 29,204-entry IPA dictionary and states dictionary data are CC BY-SA 4.0, distinct from MIT code/model. Per-entry provenance, dialect, IPA consistency, exact version and actual reuse rights still require inspection before importing. https://github.com/chemvatho/Khmer-acoustic-model
- Lao sampling guidance distinguishes Vientiane from other profiles and preserves lexical tone separately from contextual F0 effects; sources include Yanagimura (2013) and EURPhon profiles. Khmer guidance distinguishes Phnom Penh vowel/coda effects and variable /r/-loss. Burmese guidance keeps competing tone/prosody analyses explicit and requires source-table transcription to be independently checked before annotation.
- Current blockers: recruit/confirm two qualified annotators and one independent adjudicator per language; choose and approve target variety/convention; identify rights-cleared pilot lexemes; test a blind intake channel; verify candidate external datasets before use. Burmese additionally needs specialist approval of its prosodic transcription convention and source extraction. These are human/source/rights dependencies, not additional automation tasks.
- No repository test was run for this documentation-only checkpoint; existing CI evidence belongs to the preceding code head. Re-run exact-head CI after the documentation commits before merge.


## External corpus provenance audit — 2026-11-01

- Inspected https://github.com/byu-matrix-lab/MekongPhon. Its pipeline README describes SEAlang frequency lists, IPA scraping, minor lexicon post-processing, OPUS sentence downloads, lexicon train/eval splits, and trie-based sentence conversion from word-level IPA entries. Treat this as a large external orthography–IPA resource and possible comparator, not automatically as independent sentence-level phonetic gold.
- The upstream repository root LICENSE path was not present in the inspected tree. Dataset-specific redistribution permission, source terms, variety, IPA conventions, human verification/correction process, exact data files and overlap with our engine sources remain unverified. Do not import or redistribute any of it until those are resolved. Proceedings CC BY-NC-4.0 and Apache-2.0 model-card licenses do not license the underlying dataset by implication.
- Khmer Acoustic Model dictionary remains a candidate external comparator only; its README states dictionary CC BY-SA 4.0 and claims native-linguist validation, but per-entry provenance, variety, IPA convention and exact version require inspection.
- Burmese audio lead: Oo et al. (LREC 2020) speech corpus is described as 2,528 utterances from 20 female speakers with manual segmentation, plus G2P/normalization grammars. This is not IPA gold; inspect primary source, audio/transcript rights, consent, variety and metadata before considering it as lawful audio material for expert re-transcription.
- No data files were imported and no IPA labels were added. Corpus remains empty and benchmark accuracy remains null.


## Controlled IPA acquisition documentation CI — 2026-11-01

The documentation-only playbook, corpus-guide and handoff changes at the preceding branch head were checked by GitHub Actions. Khmer: Quality checks 41343502985 SUCCESS; optional Khmer G2P smoke 41343502939 SUCCESS; optional Goruut 41343502878 SUCCESS. No language-engine runtime or gold data changed. This validates the repository state, not the linguistic correctness of future annotations. Pages deployment and release-gate workflow were not run.


## Source acquisition update — 2026-11-01

- **Common Voice v27.0 Khmer:** official catalog lists locale `km`, CC0-1.0, MP3 archive 20.23 MB: https://commonvoice.allizom.org/en/datasets. This is sentence audio/transcript, not IPA. The archive size is not a clip/speaker count; exact manifest and regional coverage need inspection.
- **OpenSLR 42 (SLR42):** official resource page https://openslr.org/42 lists Khmer multi-speaker TTS audio and transcript index, CC BY-SA 4.0; the currently available archive is male-speaker only (866 MB). Provider warns that manual QC does not eliminate all transcript errors.
- Both are supplementary contextual audio, not direct citation-form lexical gold. Confirm Phnom Penh profile coverage before use; preserve exact clip/speaker IDs and time intervals, and independently transcribe audio.
- **Khmer Acoustic Model artifact check:** README claims a 29,204-entry IPA dictionary with native-linguist validation and says dictionary data are CC BY-SA 4.0. However, `dictionary/khmer_ipa.dict` was not found at the documented path in the inspected default branch; only `dictionary/khmer_ipa_sample.dict` (six entries) was available. The sample's space-separated representation and missing item-level provenance/variety convention prevent direct use as project gold. It remains a comparator lead pending a reproducible full artifact and method.
- `KHM-GOLD-001` remains `BLOCKED`; independent gold 0 and accuracy `null`. Next acceptance step: inspect Common Voice/OpenSLR manifests for profile and lexical coverage, recruit Phnom Penh experts, and choose a controlled citation-form protocol. No data imported.


## Common Voice v27.0 exact manifest audit — 2026-11-01

Inspected the official release manifest: https://github.com/common-voice/cv-dataset/blob/main/datasets/scripted-speech/cv-corpus-27.0-2026-09-11.json. Khmer: 739 clips; 213 validated; 15 contributor IDs; 0.28 validated hours (0.98 total). No named accent/variant category; gender metadata is entirely unspecified. Manifest locale checksum: `d1c4bb041744fefb1fa60397217b7cd79bfa2ade4510b11ff9863e9a0dc0392d`.

**Decision:** contextual-audio/process-pilot candidate only. Inspect actual transcripts for the 30 required lexical contrasts and obtain specialist Phnom Penh profile approval before sampling. OpenSLR42 adds male-only contextual audio but does not supply IPA. Neither source substitutes for controlled citation-form elicitation. No data/labels imported; gold 0, accuracy null.


## Final exact-head verification — 2026-11-01

Branch `feat/ipa-gold-corpus-20261101-review`, source-audit content commit `9bb02272d9da77126ac80392e840228aef18d18f`. Khmer exact-head CI: Quality checks [41345111255](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41345111255) SUCCESS; optional Goruut [41345111267](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41345111267) SUCCESS; optional Khmer G2P [41345111293](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41345111293) SUCCESS. Core job passed corpus structure validation, Python tests, Node web checks, and production site build.

These checks validate the committed repository and its automated engineering contracts. They do **not** validate the linguistic correctness of future human annotations, create gold labels, or change the release blocker. Gold remains empty and accuracy remains null.


## Follow-up handoff-head CI — 2026-11-01

The subsequent documentation-only handoff/register state at commit `1800ab775ade8e6c2ac1264c4318da69a07a53c1` was also checked on its exact head: Quality checks [41345362797](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41345362797) SUCCESS; optional Goruut [41345362827](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41345362827) SUCCESS; optional Khmer G2P [41345362791](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41345362791) SUCCESS. These runs validate the updated documentation and existing automated checks, not future IPA annotations. Any later branch update must be checked again on its new exact head.


## Open-rights state consistency fix — 2026-11-01

- Code review found that a source could pass corpus validation with `rights_status: OPEN` but `redistributable: false`. The export and release gate would later exclude/reject it, but the canonical record itself was contradictory.
- Added a test-first regression. Test-only commit `8e328d06fb13130d878859ca2c297fb154fc0533` failed as expected in the language CI because validation incorrectly returned success for that contradictory state.
- Added the fail-closed Python validation and matching conditional in `schemas/ipa-gold-record.schema.json`; regression also asserts the schema condition. Exact code/schema head: `e624dd59ce7ae1648cf72262e124764769fbc8a2`.
- Exact-head CI [41347973905](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41347973905) passed: 144 Python tests + 37 subtests; web checks and production build passed; optional Goruut and Khmer G2P smoke benchmark passed.
- No external corpus, restricted source data, IPA label or benchmark record was imported or created. Gold remains 0; `gold.tsv` remains header-only; empirical accuracy remains null.

## Exact current-head verification and handoff reconciliation — 2026-11-01

- Verified default branch `main` at `c0a2b33c86791b6546e1158c62043fd23acc1f60`; work branch `feat/ipa-gold-corpus-20261101-review` at `508ed94460e210ff9cc07cc0eaa7815246ee37b2`. GitHub compare reports **83/84/82 commits ahead respectively and 0 behind** (see the repository's PR compare; no main commits need porting at this checkpoint).
- Exact current-head GitHub Actions core run: [41348224247](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41348224247) — SUCCESS. 144 Python tests + 37 subtests; browser register-shifter contract, web checks and Vite production build passed. Optional Goruut KhmerCentral and Khmer G2P diagnostics passed.
- These are hosted CI results. No local checkout or local test execution is claimed. Optional G2P/Goruut/Epitran checks are diagnostics only and do not establish linguistic correctness.
- The current branch contains the open-rights invariant: `rights_status=OPEN` requires `redistributable=true` in both the Python validator and `schemas/ipa-gold-record.schema.json`, with a regression test.
- Independent expert-adjudicated gold remains **0**; `gold.tsv` remains header-only; empirical accuracy remains **null**. Engineering CI does not close human annotation, profile/convention approval, or linguistic validation gates.
- This entry supersedes earlier handoff statements that described the documentation/code checkpoint as awaiting exact-head CI. The PR description may contain older or superseded SHA references; the branch ref and exact-head run above are authoritative.


## IPA gold nested-record contract hardening — 2026-11-01

- Test-first regression run [41352932018](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41352932018) failed as expected: undeclared fields inside orthography, profile, source and rights_evidence passed runtime validation, and the schema left those objects open.
- Runtime fix and schema closure: unknown properties are now rejected at all four nested boundaries. Exact code/schema head `8d6b2c8184dc27a126dfa11420bc5c821c1afeb6`; exact-head core CI [41353055958](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41353055958) SUCCESS (146 pytest tests + 44 subtests; web checks, register-shifter browser contract and production build passed).
- Engineering-only change: no linguistic rules, IPA labels, gold records, source data or accuracy claims added. Independent expert gold remains 0; accuracy remains null. Hosted CI only; no local checkout was available.


## Cross-repository validator cleanup checkpoint — 2026-11-01

- Methodology review: the repository's pinned references in `AGENTS.md` already capture the relevant practices from Superpowers (test-first changes and evidence-gated verification), mattpocock/skills (clear module seams and behavior-focused tests), and Ponytail (small complete diffs and connected-code review). They remain methodology references, not runtime dependencies; no external skill bundle was copied into the product.
- Removed four consecutive duplicate nested-object validation calls from `scripts/ipa_gold_corpus.py` (orthography, profile, source, and rights_evidence). This removes redundant work without changing the contract. The resulting file has the same blob SHA across all three repositories: `a072297e320b4b91a36c59fc90328b6ff98d2a5f`.
- Code commit: `5c5e14d0458f9afd9c154e36975d86d882b67c0f`. - Core PR CI: https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41354247584 (SUCCESS); core push CI: https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41354242025 (SUCCESS); optional language diagnostics: https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41354247560, https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41354247608 (SUCCESS).
- No schema, source data, linguistic rule, IPA label, or gold row changed. Independent expert-adjudicated gold remains 0; accuracy remains null. The next substantive blocker is still qualified target-variety annotation and adjudication, not more validator scaffolding.


### Upstream methodology review — follow-up 2026-11-02

- **mattpocock/skills v1.3.2**: `d1478fcb140db0b93c0c8df17bcfd311844749d0` (released 2026-10-29). Applied the relevant improvements: standards review reads repository standards and reports separately; spec compliance and repository standards are separate review axes; bug-diagnosis RED evidence must prove the intended mutation changed relevant source; issue/PR tracker operations follow repository templates and ownership boundaries.
- **Superpowers 7.0.1** remains pinned at `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b`; its current workflow guidance reinforces preserving untracked work when worktree cleanup refuses and keeping human-authored report sections genuinely human-authored. The October 20 template changes are included in the reviewed 7.0.1 lineage.
- **Ponytail 5.3.3** remains pinned at `7801d061243d7b753bad0e0b3c057cd250b11755`. Upstream `main` advances to `96608e078b2d5ea607c5c3b8b5a54d1c1fba6846`; the inspected post-pin change only adds a README product/logo mention, not engineering-method guidance, so the method pin remains appropriate.
- No upstream skill bundle, code, dependency, dataset, or runtime integration was copied. These instructions are a selective adaptation, not a claim that third-party tools are installed.


## Exact-head verification — methodology refresh 2026-11-02

- Documentation and agent guidance checkpoint: `73e654b5a592cb84ed29b25b03cb95fb5a7e25e0`.
- [Quality checks 41358627128](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41358627128) completed SUCCESS on this exact commit; full quality-check workflow.
- Optional diagnostic runs [41358627194](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41358627194) and [41358627130](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41358627130) also completed SUCCESS. These diagnostics are not accuracy evidence.
- The current branch has one subsequent documentation-only evidence-register commit; its exact-head CI is recorded in the final session report. No engine, linguistic rules, IPA labels, gold records, datasets, or runtime dependencies were changed.


## Adjudication schema/runtime parity correction — 2026-11-02

- Found a real contract mismatch: `schemas/ipa-gold-adjudication.schema.json` requires `final_ipa` (nullable), but the Python validator used `row.get("final_ipa")` and therefore accepted an omitted key for `UNRESOLVED`.
- Test-first evidence: test-only commit `df23f23c573c8311c7c721b02177b65b44117fd7` failed as intended on exact-head PR CI [41407016954](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41407016954); the runtime returned success for a malformed adjudication and the new regression failed.
- Fix: `dea7008094314b6a1ae88b1b4868e41552cdd54a` now rejects a missing `final_ipa` property for every decision; unresolved cases must explicitly provide `null`. Exact-head PR CI [41407116467](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41407116467) SUCCESS. 147 pytest tests + 44 subtests; web checks and production build passed.
- Optional diagnostic runs: [41407116367](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41407116367), [41407116301](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41407116301) — SUCCESS.
- This is validator/schema parity only. No linguistic rules, IPA labels, gold records or source datasets changed; independent expert gold remains 0 and accuracy remains null.


## Unresolved adjudication positive-path verification — 2026-11-02

- Added explicit positive-path coverage proving that `UNRESOLVED` with a present `final_ipa: null` remains valid; omitted `final_ipa` is rejected by the new runtime guard. Test commit `8111f28c34b7b3d7118d4f428178e4e90591c336`.
- Exact-head PR CI [41407396214](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41407396214) SUCCESS. 148 pytest tests + 44 subtests; web checks and production build passed.
- Optional diagnostic runs: [41407396207](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41407396207), [41407396326](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41407396326) — SUCCESS.
- No linguistic rules, IPA labels, corpus records, datasets or empirical metrics changed. Independent expert gold remains 0; accuracy remains null.


## External G2P benchmark and engine coverage audit — 2026-11-02

A source-backed audit was added at [docs/research/external-g2p-benchmark-and-engine-coverage-2026-11-02.md](research/external-g2p-benchmark-and-engine-coverage-2026-11-02.md). It separates declared engine language support from verified phonological coverage, records language-specific external benchmark resources, defines a reproducible held-out evaluation protocol, and explicitly does not claim a score for this repository. No external engine output was promoted to IPA gold.

Current key findings:
- Epitran and Goruut both declare this language, but both remain comparators only; their public support lists do not establish complete project-profile coverage.
- The audit records engine-specific limitations and the phonological feature inventory that must be evaluated.
- The next step is a pinned, same-input, held-out benchmark with independent expert references and feature-specific metrics; exact model/dataset versions and provenance must be recorded before execution.

No runtime engine benchmark was run in this documentation update. Hosted CI verifies repository engineering, not linguistic correctness or benchmark accuracy.


## External engine smoke evidence — 2026-11-02

Detailed methods, benchmark context, limitations and per-feature acceptance requirements: [external G2P benchmark and engine coverage audit](research/external-g2p-benchmark-and-engine-coverage-2026-11-02.md).

Khmer: khmerphonemizer 0.0.3, 100 source-attested MekongPhon examples, 100 outputs, 18 strict / 19 limited-normalized matches; Goruut 100 rows, 6/100 exact, 97 outputs, 3 failures, 70 complete/27 partial/3 unknown coverage, 27 unphonemized fragments. No independent gold; accuracy=null. Runs: https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41409092574 and https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41409092578.

These are raw-output concordance/coverage diagnostics, not accuracy measurements. All independent gold counts remain zero and accuracy remains null. The missing `weights9.bin.zlib` diagnostic in Goruut's logs is recorded for investigation. Declared language support is not accepted as proof of adequate coverage. No gold labels or production rules were changed based on these runs.


## Benchmark provenance correction — 2026-11-02

Goruut was fetched from upstream source snapshot `b224bde`, not a release tag. The Khmer phonemizer was version 0.0.3. Added the 2019 Khmer G2P paper benchmark (PER 23.2% → 11.1%; WER 69.6% → 51.4%) as separate historical research evidence.

The detailed research audit is authoritative for engine versions, benchmark limitations, and measured diagnostic values. Do not describe the Goruut run as release-pinned; it used the captured upstream source revision stated above.


## Verification checkpoint for the 2026-11-02 external-engine audit

Research audit and completion register are now updated. Last register commit before this handoff update: `85f7537cfa59fe839fad11076f692a70770f1709`.

Quality checks, Khmer G2P diagnostic and Goruut raw-output workflows passed on the same code state before the final register-only documentation commit: https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41409309736, 41409309726, 41409309834.

The commits after those workflow runs changed only research-audit / handoff / completion-register documentation, not executable code. Do not treat hosted diagnostic jobs as gold evaluation: all independent gold counts remain zero. The current review branch remains ahead of `main` and has not been merged.


## Final exact-head CI reconciliation — 2026-11-02

The previously pending final-head hosted workflows have now completed successfully on this repository's recorded review-branch head `86980925a7dc9eda745268b2bd1fb081d1a82713`. Runs: [Quality 41409583877](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41409583877); [Khmer G2P 41409583886](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41409583886); [Goruut 41409583865](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41409583865). All listed jobs and steps report SUCCESS. This closes the CI-status uncertainty from the preceding checkpoint; it does not close linguistic validation or gold-data acceptance.

A follow-up inspection of the pinned Goruut source tree at `b224bde02151f8f86d0fe260804e4ca743bda620` confirms that the language-specific dictionary directories for Lao, Khmer Central and Burmese do not contain `weights9.bin.zlib`; the available language assets include the earlier weight files. Therefore the recurring log warning is consistent with an absent upstream language asset in that snapshot, not evidence that our checkout step failed to fetch an existing file. The server still starts and returns outputs, but the precise model-quality impact of the missing file is not established by this probe. Keep it recorded as an upstream model-bundle coverage limitation; do not patch or synthesize model weights locally.

The current review branch remains ahead of `main` and 0 commits behind; no PR was merged and no release was published. Independent expert-adjudicated gold remains 0; empirical accuracy remains null. All external-engine scores remain diagnostic concordance only.


## Final audit-register correction checkpoint — 2026-11-02

The completion register now supersedes the stale action item to locally recover/fix Goruut `weights9.bin.zlib`: the pinned upstream source tree does not publish that file for the three language bundles. The issue is therefore **BLOCKED (upstream dependency)** pending upstream publication or documentation of the intended fallback, not a project-owned file repair. No synthetic weights or substitute model assets were introduced.

The immediately preceding exact-head verification completed successfully on the pre-register-correction commits; the register correction itself changes documentation only. Previous runs: [Khmer Quality 41411555459](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41411555459); [Goruut 41411555448](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41411555448); [Khmer G2P 41411555592](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41411555592). Current branch commit before this handoff checkpoint: `afe5a2b3becc6438362cd9a11ac47b4bc9dc5698`. The handoff update will trigger fresh branch CI; do not treat these preceding run IDs as verification of the new handoff commit.


## Additional Khmer model and dictionary resources discovered — 2026-11-02

A follow-up source search found [`byumatrixlab/khmer-ipa`](https://huggingface.co/byumatrixlab/khmer-ipa), a 33.6M-parameter BERT encoder–decoder trained from the MekongPhon pipeline, and [`chemvatho/Khmer-acoustic-model`](https://github.com/chemvatho/Khmer-acoustic-model), which reports a 29,204-entry IPA dictionary. The former is a priority neural G2P baseline; the latter is a lexical/forced-alignment resource, not a G2P engine. Its reported F1 values (0.360 phoneme alignment; 0.120 word alignment) are not IPA-generation accuracy. Status: **PARTIAL / BLOCKED for full lexicon coverage**. The README reports 29,204 entries, but `dictionary/khmer_ipa.dict` returned GitHub API 404; only the six-row `dictionary/khmer_ipa_sample.dict` was retrievable. The full lexicon's notation and coverage therefore remain unverified. Pin the model revision/checksum, verify dialect and IPA conventions, audit unusual inventory symbols, and measure lexicon coverage only when the full dictionary is accessible. Retain raw predictions. Gold remains 0; accuracy remains null.


## Main publication reconciliation — 2026-11-02

Supersedes earlier handoff statements that the review branch was still ahead of `main` and unmerged: PR [#103](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/103) was merged into `main` as `b7e0171f77c08a15b0e55a9cb9fd83a001fff4f7`; this was the repository's current `main` tip at reconciliation. Exact-head engineering workflows on the PR head passed: Quality/tests [41414658963](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41414658963), Khmer G2P [41414658924](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41414658924), and Goruut [41414658926](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41414658926). The Pages workflow is configured to deploy from `main` and includes a deployed-site/runtime-asset smoke test. The public deployment result could not be independently inspected from this session, so deployment status remains **BLOCKED (external verification/network access)**, not claimed successful. No frontend source changes were included in this PR. Independent expert-adjudicated gold remains 0 and accuracy remains null; the project is still a research prototype.


## Current-main UI publication — 2026-11-02

The older design PR [#64](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/64) was not merged because its branch had diverged (7 commits ahead / 178 behind current `main`). Its responsive CSS and cache-busting intent were ported onto a fresh branch from the then-current `main`; PR [#105](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/105) was merged as `18ee0ae46cb98725c7f59c0436611fa50e4581bf`. The current-main CI [41424009124](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41424009124) passed the IPA gold-corpus structure validation, Python tests, JS web checks and Vite build. Added responsive layout contract tests for control wrapping, Ukrainian-result priority, narrow-phone status and coverage overflow. The Pages workflow is configured for pushes to `main`; actual deployment completion and public-site smoke-test result remain **BLOCKED (external verification/network/DNS unavailable in this session)**. This UI change improves presentation only and does not improve linguistic accuracy. Independent adjudicated gold remains 0; accuracy remains null; research-prototype status is unchanged.

### Pages smoke-test compatibility follow-up — 2026-11-02

The cache-busted stylesheet URL introduced by the UI polish exposed an overly strict CSS-link extractor in the deployed-site smoke test. Fixed in PR [#106](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/106), merge `7ee049aae9cc7ff571b21eabe18e962627f192a3`; the extractor now accepts an optional query string. PR CI passed (41424681328). The Pages workflow is now compatible with the deployed CSS URL. The post-merge Pages deployment and live-site smoke-test result are still **BLOCKED for independent verification** because external DNS/network access and a workflow-run listing endpoint were unavailable; do not infer deployment success from a merged PR or a successful pull-request CI run.


## Focused scholarly source audit — 2026-11-03

A targeted full-text review in the Undermind workspace and a parallel Consensus synthesis were added to the research evidence base. See the durable [cross-language research note](https://app.undermind.ai/projects/4f071406-bdb4-4fd1-b93f-71b9d5ec661d?path=/Research%20brief%20for%20three%20active%20engineering-research%20repositories%20that%20convert%20L.md) and the [Khmer practical transcription comparison](https://app.undermind.ai/projects/4f071406-bdb4-4fd1-b93f-71b9d5ec661d?path=/Khmer%20Cyrillic%20practical%20transcription%20comparison).

- Chem Vatho (2020), [Standard Khmer vowel system: An acoustic study](https://doi.org/10.61945/cjbar.2020.2.2.3), is a one-page poster. Although 21 speakers were initially recruited, the reported acoustic results concern four Phnom Penh speakers (2 men, 2 women; ages 20–50) reading lexical items. It reports F1/F2 and duration but has unclear/inconsistent timing details, no stated formant normalization, and reported token/measurement gaps. It does not establish a representative standard, consonant system, tone inventory or coda inventory.
- Sakamoto (1968), [The standard Khmer language and its Phnom Penh dialect](https://doi.org/10.20495/tak.6.2_290), relies principally on one Phnom Penh informant born in 1945. It records style-sensitive weak-syllable realization and proposes specific PP/ST correspondences, but these remain largely single-speaker analyses, not population-level rules.
- This reinforces the project's careful-citation profile as a bounded project decision rather than a universally established standard. The four-speaker vowel study does not validate every consonant, register, coda or colloquial process. Keep the removed deterministic colloquial /r/-loss rule removed; do not reintroduce it from general descriptions.
- Consensus identified Khmer G2P studies including Sar & Tan (2019), DOI [10.1016/j.procs.2019.11.140], reporting PER reduction from 23.2% to 11.1% after vowel-tag linguistic features. This is a published system result, not independent gold for this repository; its split, lexicon provenance, profile and rights must be checked in the primary paper before any benchmark reuse. Sok & Adams (2016) describes Thrax-based word transcription, but is not itself evidence that the current project has an adjudicated benchmark.

Independent expert-adjudicated gold remains 0; accuracy remains null. The source audit changes no IPA label or phonology rule. The Khmer browser hotfix is still separate from linguistic research and must be merged/deployed independently before production repair is claimed.


## Post-hotfix integration checkpoint — 2026-11-03

- PR [#108](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/108) merged by squash as `e9894e5726f5f6aa2510d7d3beed69b2d03fb666`.
- The merged change removes exactly one invalid DOM dereference from `src/main.js`; `index.html` intentionally has no `#source-result` element. A post-merge source inspection confirms the render path no longer writes to that absent element.
- Exact `main` push workflows all completed successfully: Quality checks [41641496598](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41641496598), Chromium browser smoke [41641496582](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41641496582), and GitHub Pages build/deploy plus deployed-site smoke [41641496680](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41641496680). The Pages run's build, Chromium production-preview test, deploy and deployed runtime-asset smoke steps all succeeded.
- The PR's exact pre-merge head `e8ef5ea727758c3339d016fb2636c1108e1549f4` also passed Quality [41536753767](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41536753767) and browser [41536753931](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41536753931); all steps in both job summaries succeeded.
- The browser regression covers visible IPA/Ukrainian output for `ក`, withholding mixed unsupported input, and clear/reset. This is UI behavior only; no phonology rule, IPA label, or gold row was introduced.
- PR [#107](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/107) is now 95 commits ahead / 1 behind and reports non-mergeable after the isolated hotfix landed. It contains the same one-line DOM correction plus a broad profile change; do not merge wholesale. Reconcile against new `main`, retain the already-merged hotfix, and re-run all relevant checks.
- Independent adjudicated IPA gold remains 0; empirical accuracy remains `null`. The repository remains a research prototype, not a linguistically validated release.


## Rebased Khmer split-manifest correction — 2026-11-03

- Rebased the substantive changes from prior PR [#109](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/109) onto current `main` after PRs #108 and #111; this branch deliberately excludes the already-merged browser hotfix and does not reintroduce its obsolete DOM write.
- Enforces one manifest-wide `(seed, version)` identity across all lexeme groups, preserves the identity when extending an existing manifest, rejects conflicting and empty explicit CLI overrides, and adds an acceptance test for creating a new versioned manifest from a separate empty `--splits` input.
- Prior exact-head CI [41639679611](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41639679611) succeeded on the original PR head, but this rebased port requires its own exact-head tests before merge.
- No linguistic gold rows or phonological labels are added. Independent adjudicated gold remains 0; accuracy remains `null`.


## Khmer source evidence and benchmark reconciliation — 2026-11-03

- Ported the source registry, references, external-corpus triage, controlled collection playbook, benchmark audit and provenance tests from prior PR [#110](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/110) onto current `main` after PR #112 merged. The IPA corpus protocol was merged carefully: the existing manifest-wide split instructions are preserved and the agreement-metric boundary is added separately.
- The MekongPhon record is an external benchmark lead, not project gold. Kirby's 2015 DataShare items are scoped to the specific audio/supplementary resources and their item-level CC BY 4.0 declarations; Praat TextGrids and measurements are not independent lexical IPA gold. Cucchiarini and Oller/Ramsdell are methodological sources, not Khmer-specific scoring algorithms. Woźnica's multi-region thesis is not treated as Phnom Penh-only evidence.
- Original PR-head Quality workflow [41640011541](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41640011541) succeeded; this clean port requires its own exact-head CI. No external IPA labels imported; independent adjudicated gold remains 0 and accuracy remains `null`.


## Single careful-citation profile integration — rebased 2026-11-03

- Rebased the narrow profile/runtime change onto the latest main after Khmer source-evidence PR #113 merged. This branch excludes the already-merged browser hotfix and all unrelated broad PR #107 changes.
- The service exposes only `khmer-pph-careful-citation-v1`, a bounded project profile for contemporary Phnom Penh careful citation-form speech. The adapter preserves supplied IPA; it does not synthesize colloquial /r/-loss or rewrite /Cr/ clusters.
- The project profile decision is supported as an elicitation target by Chem (2020)'s small formal-reading sample, but it is not a national standard or a claim of full lexical coverage. Independent adjudicated gold remains 0 and accuracy remains `null`.
- Original #114 exact-head Quality and Chromium workflows succeeded, but this rebase requires fresh exact-head checks.


## Khmer agent context and glossary — 2026-11-03

- Added the project glossary, current codebase/data-flow map and issue-tracker instructions, and updated `AGENTS.md` to route future work through the canonical handoff and verified maps.
- The codebase map reflects the current main after the browser hotfix, manifest-wide split fix, source-evidence reconciliation and single careful-citation profile. It distinguishes parser structure, source-language phonology, typed IPA, Ukrainian adaptation, generated browser data and the separate romanization path.
- These are navigation and process aids, not linguistic evidence or a replacement for expert review. No runtime rules or gold labels changed. Exact-head CI required.


## Current repository continuation checkpoint — 2026-11-03

- Verified default branch `main` at `d8419d3099a8047d819a5a71cb5c4ef927db435e`.
- Latest exact-main CI for profile/runtime commit `1dc07f9c43972f547ac7a56adb9ed949155bacf1`: Quality 41646838970 SUCCESS; Chromium 41646838756 SUCCESS; Pages/deployed-site 41646838884 SUCCESS. The subsequent glossary/codebase-map documentation commit is d8419d3.
- PR reconciliation: PRs #107 and #114 were closed without merge as superseded; their profile/runtime/test changes are already byte-identical to main. PRs #108 and #111 were merged earlier. The attempted documentation sync PR #117 was closed because main advanced while the docs-only branch was open; this branch is based on the latest main. No runtime changes are involved.
- Current engineering state: main includes the single operational profile `khmer-pph-careful-citation-v1`, no deterministic colloquial /r/-loss rewrite, the manifest-wide split fix, source-evidence reconciliation, browser hotfix, and project glossary/codebase map. The profile remains a bounded project elicitation decision pending specialist approval and does not establish a complete phonological model.
- Linguistic evidence boundary: independent adjudicated IPA gold remains 0; gold export remains header-only; empirical accuracy remains null. CI verifies engineering behavior only.
- Human/research blockers remain: approve the versioned IPA convention; recruit two qualified independent annotators and a separate adjudicator; establish blinded intake; verify source-specific data rights; collect and adjudicate a profile-specific pilot; complete deployed-site manual keyboard, screen-reader, responsive and mobile QA.
- No gold labels, source-derived IPA guesses, phonological rules, or benchmark scores were created in this checkpoint.


## Upstream methodology reference refresh — 2026-11-03

- `obra/superpowers` current `main` remains `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b`, release v7.0.1. The inspected upstream guidance reinforces protecting untracked work, re-reading evidence rather than treating reruns as proof, bounded waits, and explicit review/finish accounting. Apply relevant practices; do not import the external repository as a runtime dependency.
- `mattpocock/skills` current `main` is `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`; the latest commit adds a software-factory glossary and example runs. The immutable release reference remains v1.3.2 at `d1478fcb140db0b93c0c8df17bcfd311844749d0`; distinguish release pin from current-main snapshot.
- `DietrichGebert/ponytail` current `main` is `96608e078b2d5ea607c5c3b8b5a54d1c1fba6846`, release v5.3.3 at `7801d061243d7b753bad0e0b3c057cd250b11755`. The post-pin upstream change inspected is a README/product-list addition, not a methodology change.
- No upstream skill files were copied into product/runtime code. These are traceable method references only.

## Continuation — held-out IPA benchmark correction (2026-11-03)

- Base `main`: `3809f0de9b77253a08985bb90e18e7308bdda412`; work branch: `fix/heldout-ipa-benchmark-20261103`.
- Finding: the frozen split manifest existed, but the gold TSV export discarded split identity and the scorer included all adjudicated rows. This could allow train/dev examples into a purported independent evaluation.
- Implemented: export now requires a frozen assignment and emits `split`; the gold TSV header includes the field; benchmark validation requires a valid split, defaults to `test`, and supports explicit `--split train|dev|all` for non-held-out diagnostics. Reports identify the selected split and distinguish all adjudicated rows from the scored denominator.
- Exact code/test-head verification: [Quality run 41651903776](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41651903776) SUCCESS on `ca53d628ae9a9ea4696fc85f42cdf59bcedfa2d1`, including Python, web checks and Vite build.
- **IPA-BENCH-SPLIT-001 — DONE_VERIFIED (engineering contract).** Independent expert-adjudicated gold remains 0; `gold.tsv` remains header-only; empirical accuracy remains `null`. No phonetic labels were added.
- Still blocked: two qualified independent annotators, a separate adjudicator, approved IPA convention, controlled blind intake and source-specific rights evidence. Manual visual/keyboard/screen-reader/mobile QA remains TODO.

**Final review:** self-review performed against the complete branch diff and matching implementation across all three repositories (no subagent reviewer is available). The split/export/scoring contract, fail-closed paths, report denominator, tests and docs were inspected; no Critical/Important defect was identified. PR remains open for owner review; no shared-branch merge was performed.

## Frozen split manifest provenance — 2026-11-03

The export and benchmark now preserve and validate the complete frozen split identity, not only the bucket name: `split`, `split_seed`, and `split_version`. Every adjudicated row must carry non-empty seed/version metadata, and the benchmark rejects a TSV that mixes manifest identities. The report exposes the manifest seed/version and selected scoring split. This makes the evaluated test partition traceable to one exact manifest; it does not create linguistic gold or change the current zero-row accuracy status.


## Empty prediction dataset guard — 2026-11-03

A further benchmark review found that a header-only prediction TSV exited successfully and emitted a report with no engine entries. This could be mistaken for a completed evaluation even though no engine had been evaluated. Added a regression test and a fail-closed CLI guard requiring at least one prediction row. The guard runs after gold/split-manifest validation so existing malformed-manifest diagnostics remain specific. This does not change the treatment of missing rows within a named engine: those remain in its denominator. Exact-head verification: RED: [41655188132](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41655188132). Final exact-head quality checks: [41655492141](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41655492141) SUCCESS; browser smoke: [41655491334](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41655491334) SUCCESS. The benchmark guard is DONE_VERIFIED as an engineering input-integrity check; no gold rows or accuracy claims were added.


## Continuation — whitespace-only benchmark identifiers (2026-11-03)

A code review found that truthiness-only identifier checks accepted whitespace-only gold IDs, prediction IDs and engine names. Such values could create visually empty keys and make malformed prediction rows look like a named engine. Validation now rejects identifiers whose trimmed value is empty while preserving non-empty identifiers verbatim for exact matching. Regression tests cover each field separately.

- Test-first RED for whitespace-only gold IDs: [workflow run 41660794382](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41660794382) FAILED on the new regression as expected.
- Test-first RED for prediction engine/ID fields: [workflow run 41662096875](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41662096875).
- Final exact-code-head verification: [workflow run 41662242906](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41662242906) SUCCESS; 164 Python tests + 50 subtests; 3 browser smoke tests passed; browser smoke [41662242611](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41662242611) SUCCESS.
- Verified implementation commit: `02807605a78fee4c7ab25cd51315e4343940a3c1`; exact-code-head CI [workflow run 41662242906](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41662242906) SUCCESS.
- **IPA-BENCH-IDENTIFIERS-001 — DONE_VERIFIED (engineering input-integrity guard).** No linguistic labels, gold records or accuracy claims were added.

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


## One-pass continuation checkpoint — 2026-11-04

- Current default branch: `main`; verified head `9e688e0118382f8e990e8758c53a5c7ec8877a78` (latest commit after PR #138).
- Open PR query on 2026-11-04 returned none. Latest relevant merges: #131–#138. #131–#133 reconcile MekongPhon provenance, scale and dictionary-seeded evaluation limits; #134 records unresolved Khmer Acoustic Model dictionary count/license discrepancies; #135 registers DDD audio candidate constraints; #137 registers Common Voice 27 Khmer audio limits; #136/#138 reconcile merges and verification.
- Exact-head hosted verification for PR #137: Quality checks 41800443113 SUCCESS and Khmer browser smoke 41800443035 SUCCESS. PR #138 is a documentation-only post-merge checkpoint. The current main combined-status endpoint returned no status entries; this is not evidence of a failed or successful main push run.
- Preserved evidence boundary: DDD Part 1 lists 134.60h and 8 speakers under CC BY-SA 4.0 with attribution and no-speaker-identification restrictions; Common Voice 27 reports 739 clips (213 validated; 0.28 validated hours; 15 speakers) but no IPA or reliable accent identification. Neither source is IPA gold. MekongPhon remains dictionary-seeded and dataset rights are unresolved.
- Task ledger: source registrations and provenance reconciliation **DONE_VERIFIED**; independent adjudicated Khmer IPA gold **BLOCKED** (0 records; gold export header-only; accuracy null); expert approval of target variety/profile and IPA convention, two independent annotators, separate adjudicator, item-level rights and blind intake **BLOCKED**; manual keyboard/screen-reader/mobile QA **TODO**.
- Khmer Acoustic Model dictionary remains blocked pending author clarification and an inspectable versioned full corpus; conflicting dictionary counts and CC BY/CC BY-SA statements must not be treated as cleared.
- No runtime phonology or Ukrainian mapping changes were made in the latest source-evidence merges. No orthographic transcript or G2P respelling is promoted to IPA.
- The initial checkpoint commit was documentation-only; a subsequent test-only change now uses Khmer script and a neutral test profile in the IPA-corpus fixtures. Hosted CI results for the final head are recorded separately; local tests were not run in this connector session. Hosted CI evidence above is tied to the exact PR head, not a claim of fresh local verification.


## Hosted verification update — 2026-11-04

- Draft PR #139 exact head `3889739aecf0221c7cf1e26be59f025838a914ed`: Quality checks [41844573271](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41844573271) **SUCCESS** and browser smoke [41844573296](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41844573296) **SUCCESS**.
- Quality job completed IPA gold corpus structure validation, Python tests, web checks and site build. Browser smoke completed successfully.
- This verifies the docs-only PR head and the repository's current CI contract. It does not establish phonological accuracy or clear the Khmer Acoustic Model / MekongPhon rights questions; the evidence and expert-review blockers above remain unchanged.


## Test-fixture correction — 2026-11-04

- Review found that the shared IPA-corpus validator test file used Lao orthography and a Lao-specific profile description even in the Khmer and Burmese repositories. This did not affect production validation, but made the fixtures misleading and weakened language-specific test coverage.
- The test fixtures now use the repository's script (Lao / Khmer / Myanmar), neutral `test-<language>` profile identifiers and `Test fixture (<language>)` variety labels. A regression test asserts the fixture characters fall within the corresponding Unicode block and that profile metadata matches the repository language.
- This is a test-harness correction only. It does not validate language phonology, IPA correctness, or script-specific parser behavior; the production validator still intentionally validates corpus structure rather than imposing a single script restriction on all orthographic records.


## Final test-fixture PR verification — 2026-11-04

- Test and handoff changes were present at head `ff656632cb3323612f5c7f647a069c821aceaa48` when the following hosted checks completed: Quality checks [41847143845](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41847143845) **SUCCESS**; browser smoke [41847143819](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41847143819) **SUCCESS**.
- The successful checks include the language-specific IPA-corpus fixture regression, repository data validation, language-specific Python test suite, web build/reproducibility checks and Chromium browser checks where configured.
- Exact job steps were inspected; every reported step completed with `success`. These are engineering/structural checks, not a linguistic accuracy benchmark. No local tests were run in this connector session.


## External Khmer pronunciation-source research continuation — 2026-11-04

- Created dedicated branch `research/khmer-external-pronunciation-audit-20261104` from main `09f439dc12e078c72a00038c0583b03803ee054a`.
- Added four external resource records to `data/khmer/sources.json`: pinned IPA-Dict Khmer, PhonSobon Khmer G2P, PhonSobon combined pronunciation dictionary, and Chem Vatho's Khmer Acoustic Model. Each record distinguishes source format, scope, provenance, rights and whether it is eligible for gold.
- Extended `docs/audits/current/EXTERNAL-PHONETIC-CORPUS-TRIAGE-2026-11-01.md` with source-level findings and explicit no-import decisions.
- Extended the existing linguistic completion register with `KHMER-EXT-IPA-DICT-001`, `KHMER-EXT-RESP-001`, and `KHMER-ACOUSTIC-DICT-RECHECK-001`.
- Added `test_external_pronunciation_sources_preserve_format_and_rights_boundaries` to `tests/test_data_integrity.py`. It guards against silently reclassifying Khmer-script respelling as IPA, treating non-commercial sources as unrestricted, or treating a missing/contradictory external dictionary as an approved source.
- External research evidence: IPA-Dict's pinned revision `972cd67dd5f96bc5660e28070cde26e3928abcd7` has 3,286 lines in `data/km.txt`; its README attributes Khmer data to aakanee.com and CC BY-NC-SA 4.0. PhonSobon Khmer G2P reports 38,629 pairs / 37,755 unique words and explicitly says the pronunciation field is Khmer-script respelling, not IPA; source content remains NCKL-owned and commercial terms must be checked. The combined dictionary reports 39,110 rows and flags 39 LLM-assisted decisions for native-speaker confirmation. Chem Vatho's current main `2714994b41ccf875c5b6f6182b48a72f13632dbf` claims 29,204 IPA entries but exposes only a six-line sample; root README and dictionary README disagree on CC BY-SA 4.0 vs CC BY 4.0 and on dictionary/mapping counts.
- No external source data were copied; no license was inferred; no IPA or Ukrainian output was fabricated. The IPA-Dict resource is non-commercial/share-alike, PhonSobon resources remain rights-limited/unresolved and Khmer-script respelling, and the acoustic-model dictionary remains blocked pending a full artifact and clarified terms.
- Acceptance boundary: this closes source discovery/triage documentation only. It does not close `KHM-GOLD-001`; independent expert-adjudicated Khmer IPA gold remains 0 and empirical accuracy remains null.
- Validation: pending hosted CI for this branch/PR. No local checkout or local test execution was available through the connector session.


## Final Khmer external-source PR verification — 2026-11-04

- PR #140 head after the regression assertion correction: `3fd741b420eb217f2fe0d24087642dbbf866c687`.
- The first Quality run [41849845861](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41849845861) exposed one test-only case-sensitive assertion mismatch (`NOT project gold` vs the source note's `Not project gold`); 173 tests and 60 subtests passed, one new assertion failed. The assertion was corrected to compare case-insensitively; no source classification or production behavior was changed.
- Corrected-head Quality [41850630303](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41850630303) **SUCCESS**; corrected-head browser smoke [41850630166](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41850630166) **SUCCESS**. The Python suite, web checks, production build and Chromium browser smoke completed successfully.
- Source records continue to distinguish IPA-Dict's non-commercial/share-alike Khmer IPA, PhonSobon's Khmer-script respelling (not IPA), and the incomplete/licensing-conflicted Khmer Acoustic Model dictionary. No third-party data were copied.
- This verifies source-registry and rights-boundary engineering only. Independent expert-adjudicated Khmer IPA gold remains 0; empirical accuracy remains null.
- No local tests were run; hosted CI logs were inspected.


## IPA gold release-gate profile consistency — 2026-11-04

- Found a concrete gap in the shared `scripts/ipa_gold_corpus.py`: the release gate checked adjudicated-record counts, frozen splits and source redistribution rights, but did not enforce the playbooks' one-target-profile / one-IPA-convention requirement. A mixed-variety or mixed-kind corpus could therefore pass the numeric/rights gate and be scored as one benchmark.
- Added regression tests first for mixed profile and mixed IPA kind in each of the three repositories. The first Lao test run failed on both new cases as expected; after adjusting the fixture to populate all three deterministic split buckets, the regression remained targeted. The Khmer and Burmese exact-head runs subsequently passed; final run IDs and merge evidence are recorded below.
- Added shared gate checks: one signature across adjudicated records (`profile.id`, `variety`, `region`, `register`) and exactly one adjudicated IPA kind. Per-record speaker/audio IDs are deliberately excluded from target-profile identity.
- Updated the corpus documentation and completion register. The checks do not replace approved convention sheets, human reviewer qualifications, blind annotation evidence, or language-specific contrast-coverage reports. The gate still does not calculate contrast coverage from free-text phonological metadata.
- No IPA labels, pronunciation rules, Ukrainian mappings, source data, or benchmark scores were added. Independent adjudicated gold remains 0 in all three projects.


## Final release-gate profile guard verification — 2026-11-04

- TDD RED evidence on the pre-fix implementation: Lao [41868595591](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41868595591), Khmer [41868607839](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41868607839), and Burmese [41868623352](https://github.com/ClippyFirst/Burmese-Ukrainian-Phonetic-System-/actions/runs/41868623352). In each repository both new regression cases failed because the old CLI returned `{"release_ready": true, ...}` for a corpus deliberately mixing target profiles and/or IPA kinds despite meeting train/dev/test minimums.
- GREEN after the shared validator fix:
  - Lao Verify [41868752376](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41868752376) **SUCCESS**; 172 Python tests and 4 browser tests passed; data/evidence audit, optional G2P CLI, generated-data reproducibility and Chromium built-site checks also passed.
  - Khmer Quality [41868942150](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41868942150) **SUCCESS**; 176 tests and 60 subtests passed, plus browser runtime contract and site build checks.
  - Burmese tests [41868956132](https://github.com/ClippyFirst/Burmese-Ukrainian-Phonetic-System-/actions/runs/41868956132) **SUCCESS**; 167 tests and 64 subtests passed, generated web data stayed current, npm tests and 54 built-site browser tests passed.
- Final documentation/register/handoff commits also passed their subsequent push CI: Lao [41869194865](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41869194865), Khmer [41869262079](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41869262079), and Burmese [41869342234](https://github.com/ClippyFirst/Burmese-Ukrainian-Phonetic-System-/actions/runs/41869342234). Exact final PR-head runs are tracked in the PRs.
- The Burmese execution status matrix was updated in the same branch. Lao and Khmer have no separate execution-matrix file; their canonical handoff and linguistic completion register were updated.
- This verifies an engineering fail-closed guard only. The CLI still does not calculate language-specific contrast coverage, and human convention approval, blind workflow evidence, expert adjudication and rights review remain required. No linguistic data or rules changed.
- No local checkout/tests were available in this connector session; all test claims above refer to inspected hosted GitHub Actions logs.


## Mainline merge verification — IPA gold release-profile guard — 2026-11-04

- PR #141 merged to `main` as `4ba59abdc389a797c58216e4e155b8b06408c557`; current main was confirmed at the same SHA immediately after merge.
- Exact PR-head verification: [41870121484](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41870121484) **SUCCESS** (177 tests; 60 subtests).
- Exact PR-head browser smoke: [41870121371](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41870121371) **SUCCESS**. Post-merge Quality [41870545200](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41870545200) **SUCCESS** and Pages [41870545069](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41870545069) **SUCCESS**. A duplicate post-merge browser workflow [41870545028](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41870545028) was still installing Chromium at this checkpoint; the exact merged tree had already passed the PR-head browser smoke.
- The branch was based on latest main with zero commits behind at merge; no conflicting PRs were present. The exact diff was reviewed and merged with an expected-head SHA guard.
- The release guard is now on main. Independent expert-adjudicated gold remains 0; this work does not establish phonetic accuracy or benchmark readiness.


## Expert recruitment lead revalidation — 2026-11-04

- Branch: `research/expert-recruitment-leads-20261104`, based on main immediately before this research pass.
- Rechecked official institutional and publication sources for prospective expert reviewers/referral routes; appended a dated, qualification-limited section to `docs/ipa-gold-collection-playbook.md` and added `KHMER-IPA-GOLD-RECRUITMENT-LEADS-001` to the existing completion register.
- Candidate fit is limited to the evidence actually published: no availability, willingness, native target-variety competence, role independence or consent is inferred. No one was contacted. Public institutional emails are included only where published by the institution/research journal.
- The pilot remains blocked on actual recruitment, versioned convention approval, two independent target-variety annotators, separate adjudicator, non-annotating curator, source/item rights and secure blind intake. No IPA labels or gold data were added.
- Hosted CI pending for this branch; no local checkout/tests were available in this connector session.


## Final expert-lead research PR verification — 2026-11-04

- Exact PR head: `f60e682bb423d951cd4c5b5649ecedbe490dbb10`; Quality [41872769175](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41872769175) **SUCCESS** and browser smoke [41872769410](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41872769410) **SUCCESS**. Inspected steps: independent corpus validation, Python suite, deterministic web checks, production build, Chromium install and visible-results smoke all passed.
- The update only improves recruitment evidence. Chem's relationship to his acoustic-model resource is explicitly recorded as a potential conflict; no recruitment, IPA labels, gold data or production phonology changed.
- No local checkout or local tests were available; these results refer only to the hosted GitHub Actions runs linked above.
- The human pilot remains blocked on actual invitations/consent, approved versioned IPA convention, two qualified independent target-variety annotators, separate adjudicator, curator, item-level rights and secure blind intake.


## Agent completion-methodology update — 2026-11-04

- Added the missing Unlazy completion-gate discipline to `AGENTS.md`, pinned to upstream `Leonxlnx/unlazy@16671491f6679ad9378f52604d3bc2415b4120c7`. The update adopts observable acceptance items, evidence-bound manual gates, exact-final-commit re-verification, scoped task decomposition and explicit non-successful handoff for blockers.
- Kept the existing master handoff/status vocabulary and GitHub Actions as canonical. No second ledger framework, Unlazy checker/hooks, runtime dependency, or linguistic behavior was introduced.
- Also retained the existing Superpowers, Matt Pocock and Ponytail methodology references. Their use is constrained by project-specific IPA, source-rights, privacy and fail-closed requirements.
- Documentation PR: #143. Exact-head CI evidence: 41876110596 (Quality SUCCESS), 41876110636 (browser smoke SUCCESS). The PR has been merged to main; post-merge workflow/deployment checks are still being observed where applicable.
- This is an engineering-process improvement only. It does not resolve the external blockers: expert recruitment and approved IPA conventions, independent adjudicated gold, item-level redistribution rights, and controlled blind annotation intake. No people were contacted and no IPA labels or corpus data were added.

## Deterministic rule-engine replacement — 2026-11-11

- Replaced the model-consensus design with RuleBasedKhmerEngine in src/khmer_ua/rule_engine.py; the legacy HybridKhmerEngine name is only a compatibility alias. There is no provider injection, model vote, network call or external runtime in the active engine.
- Runtime path: NFC normalization → Khmer structure/register analysis → exact versioned lexical IPA fixtures or narrowly scoped inherent-vowel rule → longest-match IPA → Ukrainian policy. Unsupported structures are withheld.
- Website copy now explicitly identifies the deterministic local rule path and links to docs/DETERMINISTIC-RULE-ENGINE.md.
- PR [#152](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/152) merged to main as `913e1b2a117022eb3350c3d1957680f0b5db0661` from branch release/deterministic-rule-engine-2026-11-11. Exact main Quality [43018004334](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43018004334), browser smoke [43018004167](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43018004167), and Pages deployment + post-deploy asset smoke [43018004186](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43018004186) all SUCCESS.
- Published service: https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System-/
- Engineering task DONE_VERIFIED; linguistic coverage remains PARTIAL/PROPOSED. Determinism is verified; phonetic correctness beyond the covered rules/lexical fixtures still requires expert-adjudicated Phnom Penh gold.

## Final deterministic-engine verification — 2026-11-11

- Post-merge hardening on main head `7585b49fdaac5480940d2511f48961f7690bf6b5`: legacy factory now rejects external provider injection; execution trace is named `rule_trace`, not a fabricated evidence-rule identifier.
- Exact-head Quality [43019207054](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43019207054), browser smoke [43019207032](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43019207032), and Pages deployment + asset smoke [43019207026](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43019207026) all SUCCESS.
- Live service: https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System-/. The Python rule engine and published browser runtime are deterministic and do not use model consensus.
- Remaining linguistic acceptance: independent adjudicated Phnom Penh IPA gold and expanded contextual vowel/coda coverage; no blanket accuracy claim.


## 2026-11-11 continuation — Ukrainian practical transcription

### Repository state
- Starting default-branch SHA: \`2fe36aa1eb64cc47fb60ab1b37561f40d57202a7\`.
- Verified implementation SHA: \`e7b52ae3921b17fb9d0c400eaad913c8c78d2b50\`.
- Final verification branch: \`feat/khmer-ukrainian-practical-adapter-final-2026-11-11\`.
- Draft PR: [#156](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/156), open, not merged.
- Earlier drafts #154 and #155 were closed as superseded; their branches were retained.
- No main-branch modification and no Pages deployment/publication.

### Implemented
- \`src/khmer_ua/practical.py\` now provides the whole-IPA longest-match adapter \`map_ipa_string()\`; \`RuleBasedKhmerEngine\` calls it after IPA derivation. Unknown IPA withholds the complete practical result.
- \`src/ukrainian-practical.js\` is the shared browser adapter imported by \`src/main.js\`; browser and Python adapter behavior is tested against the same machine-readable policy.
- Policy version: \`2026-11-11.3\`.
- Ukrainian-specific choices: /h, ɦ/ → г; /ɡ/ (ASCII /g/) → ґ as a contrast-preserving project choice; /x/ → х; /w, ʋ/ → в; explicit /t͡s, d͡z, t͡ʃ, d͡ʒ/ → ц, дз, ч, дж; /tɕ, dʑ/ → ч, дж as practical approximations; /cʰ/ → ть'.
- Syllable-initial /j/ + transparent vowel uses Ukrainian я/є/ї/ю/йо; /j/ elsewhere remains й. Russian comparator /w/ → у is not copied into Ukrainian.
- The 2026 Ukrainian Orthography is target-language guidance, not evidence about Khmer phonology. It generally uses г for foreign [g] and permits ґ as imitation in personal names; /ɡ/ → ґ remains an explicit project policy.
- Public system page, README, policy documentation, fixture audit and regression tests were updated. Work was text-only; no audio was used.

### Verification evidence
- Quality workflow [43094688835](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43094688835): SUCCESS; 187 Python tests + 62 subtests; deterministic web checks, policy/data validation and production build passed.
- Browser workflow [43094688837](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43094688837): SUCCESS; Chromium 3/3.
- The browser adapter runtime tests exercise yotation, /w/, affricates, whitespace, and fail-closed unknown IPA.

### Task ledger
| Work item | Status | Evidence / acceptance |
|---|---|---|
| Whole-IPA Python adapter integrated after deterministic IPA | DONE_VERIFIED | \`src/khmer_ua/practical.py\`, \`src/khmer_ua/rule_engine.py\`, quality CI |
| Browser adapter shares the canonical policy and passes runtime mapping tests | DONE_VERIFIED | \`src/ukrainian-practical.js\`, \`src/main.js\`, \`tests/web-engine.test.mjs\`, browser/build CI |
| Ukrainian h/g/x, affricates, /w/ and /j/ target conventions documented | DONE_VERIFIED | \`data/ukrainian/practical-policy.json\`, public \`system.html\`, regression tests |
| Empirical correctness of Khmer IPA → Ukrainian target correspondences | PARTIAL | Rules are explicit and deterministic; independent adjudicated gold is still absent |
| Independent text-only Khmer IPA/Ukrainian gold set | BLOCKED | Requires rights-cleared text lexical sources with provenance plus independent native/expert adjudication; acceptance: non-overlapping held-out set, per-phenomenon labels, adjudication record, CER/PER and coverage/abstention report |
| Audio validation | DEFERRED | Explicitly outside this text-only task |

### Next genuine blocker
Create the independent text-only Khmer IPA/Ukrainian adjudication set. Do not promote the proposed correspondences to validated accuracy claims until that evidence exists.

## Verification refresh — Ukrainian practical transcription, 2026-11-11

- Latest implementation branch: `feat/khmer-ukrainian-practical-adapter-final-2026-11-11`; current PR #156 remains open/draft and unmerged. Main remains unchanged at `2fe36aa1eb64cc47fb60ab1b37561f40d57202a7`.
- The canonical Python adapter, browser adapter and target policy are unchanged at the verified implementation baseline; subsequent changes expanded tests and synchronized README, system/implementation/validation documentation and completion records.
- Expanded adapter checks cover /h, ɦ, ɡ, g, x; explicit affricates; plain consonant sequences; /cʰ/ → ть'; /j/ yotation; whitespace and unsupported IPA. No audio was used or required.
- Exact-head quality run [43095329118](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43095329118) and browser smoke [43095329245](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43095329245) are queued with no jobs started at this refresh. Do not report these final runs as passed.
- The independent text-only Phnom Penh IPA/Ukrainian gold set remains BLOCKED by missing independently sourced and adjudicated text labels. This blocks empirical accuracy claims, not deterministic adapter implementation. Audio annotation is DEFERRED by scope.


## Provisional grapheme IPA fallback — continuation 2026-11-11

- Added `docs/provisional-grapheme-ipa-fallback.md` defining the Lao-style `PROVISIONAL` grapheme → IPA → existing Ukrainian adapter contract, visible `?` uncertainty, Python/browser parity and benchmark separation.
- This is a design/acceptance document only, not an implementation claim. Current Khmer parser/practical adapter still withholds unsupported constructions. Implementation is BLOCKED pending a source-backed, positional Khmer grapheme-to-IPA inventory; no context-free letter readings or vowel/tone guesses may be fabricated.


## Provisional onset fallback implementation — 2026-11-11

- Python and browser now expose a separate PROVISIONAL onset-only IPA preview for unresolved units when the existing parser has a registered base-consonant onset IPA.
- The same IPA → Ukrainian adapter is used; the affected Ukrainian unit receives ?. Canonical ipa/ukrainian remain withheld.
- No vowel, coda, subscript/coeng realization or tone is inferred.
- Python regression and browser source-contract regression were added.
- Status: PARTIAL. Dedicated per-grapheme positional source registry, executed browser parity fixtures, exact-head CI and Chromium verification remain outstanding.
- Exact head at this update: 660915e4ed1f44eab04258957eee39537883aadd. Quality and browser workflows 43099931373 / 43099931284 were queued, not passed.


## Final continuation snapshot — 2026-11-11 23:00 +02:00

- Current PR #156 head: ffeb3ee3a46898f1fdf6ab5ac455972bb59f327a. Draft, open, unmerged. Main baseline remains 2fe36aa1eb64cc47fb60ab1b37561f40d57202a7.
- Implemented Python and browser onset-only PROVISIONAL fallback. It uses registered consonant onset IPA → existing IPA adapter → Ukrainian text plus ?. Canonical fields remain withheld.
- Exact-head CI is NOT verified. Earlier quality/browser runs 43100166075 and 43100166123 were queued on head 30f2dc5ee6be90cd75205c742d73f3af41f1523b; the subsequent status-priority correction is at ffeb3ee3a46898f1fdf6ab5ac455972bb59f327a and no workflow run was returned for that exact head.
- Local test execution was unavailable: public GitHub clone attempt failed because the execution environment could not resolve github.com. No tests are claimed passed on the new fallback.
- Remaining: execute Python/Node/Chromium tests on the exact head; add functional shared Python/browser fixtures; register source-backed positional fallback evidence; expand only where vowel/subscript/coeng evidence is explicit. Keep the independent text-only adjudicated gold set BLOCKED and audio DEFERRED.


## Fallback scope clarification — 2026-11-11

The browser preview is separate from canonical output. The onset-only test fixture is ក្ក (known base plus unresolved coeng/subscript), not កា, which is handled by the existing inherent-vowel rule. Exact-head tests after this correction still need completion.


## Verified implementation result — 2026-11-11

- Code/test head dbdb8beafc3454e6bb0be848011f90fb0dea190b.
- Quality workflow 43101322383 PASS: 189 Python tests, 62 subtests, web checks and production build.
- Browser smoke 43101322537 PASS: deterministic web checks, production build and Chromium visible-result check.
- Browser keeps canonical IPA/Ukrainian withholding intact and shows a separate onset-only preview in per-unit details.
- Linguistic feature remains PARTIAL: positional primary-source registry and functional shared Python/browser parity fixtures remain TODO. Independent adjudicated gold remains BLOCKED; audio DEFERRED.


## Complete Unicode grapheme-accounting sweep — 2026-11-12

- PR [#157](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/157) merged as `e9c9d997e6de1029fd0b8fef9e7b6a9cb0020a4f`.
- Added an exhaustive runtime sweep over every assigned Unicode letter and combining mark (general categories L/M) in Khmer U+1780–17FF and Khmer Symbols U+19E0–19FF. Each tested code point must survive segmentation and appear in the parser's grapheme trace with its exact U+ identifier.
- The sweep exposed an early-return trace-loss defect for malformed U+17D2 COENG. The parser now retains the malformed coeng and all remaining code points as `invalid_sequence_component`; it does not invent a pronunciation.
- Added a negative control for U+17F9, which remains explicitly unsupported rather than receiving synthetic IPA.
- Exact PR-head verification: Quality [43184648039](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43184648039) SUCCESS; browser smoke [43184647978](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43184647978) SUCCESS. These runs cover the exact tested branch head `fcae948d8ae30bc0ad606ef4ae4071fffb68be08`.
- **Status:** structural/input accounting for the tested Unicode L/M set is DONE_VERIFIED. This is not 100% Khmer phonological coverage, 100% IPA coverage, or pronunciation accuracy. Vowel × series × length × coda × profile evidence and independent adjudicated gold remain PARTIAL/BLOCKED. Post-merge main workflows were still running at this documentation checkpoint; no post-merge result is claimed.


## Explicitly unmodelled Khmer letters and lossless trace tail — 2026-11-12

- PR [#159](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/159) merged as `d1d184334c806cd21cf2eb875a9c5151ab9e61b3`.
- Added explicit `unmodeled_letter` inventory records, with no IPA, for U+17A3 KHMER INDEPENDENT VOWEL QAQ, U+17A4 QAA, U+179D SHA and U+179E SSO. They remain unsupported by the selected modern Khmer phonology profile until appropriate evidence exists.
- Fixed a second parser trace-loss path: encountering an unknown or explicitly unmodelled code point now preserves the entire remaining source tail as trace components rather than returning after the first unknown code point.
- Regression coverage includes all four unmodelled letters and a mixed sequence `កxយ`, ensuring later graphemes remain present after the unknown `x`.
- Exact PR-head Quality [43186170402](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43186170402) SUCCESS and browser smoke [43186170525](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43186170525) SUCCESS on `b62b9beef65ccfd546c39b05578d0a9f80f48083`.
- **Status:** explicit inventory classification and lossless tail trace are DONE_VERIFIED. The four letters remain phonologically NOT_ESTABLISHED; no pronunciation has been fabricated. Complete positional Khmer IPA and independent gold remain PARTIAL/BLOCKED.



## Ukrainian romanization-target matrix completion — 2026-11-12

- Base `main` at start: `e249adb736c57501300cb27322eed7ea27ab901a`; task branch: `feat/khmer-romanization-ukrainian-matrix-completion-2026-11-12`.
- Updated `data/khmer/romanization_ukrainian.csv`: all 22 PCGN consonant rows now have an explicit Ukrainian target, including `th → т'`, the contextual romanized outputs `b → б` / `p → п`, and the PCGN glottal marker `’ → ʼ`.
- Updated `data/khmer/romanization_vowels_ukrainian.csv`: all 37 official PCGN vowel/rime rows now have a non-empty target rendering. Contextual alternatives remain visible as alternatives and carry `ANALYSIS_DEPENDENT`; no IPA or pronunciation value was inferred.
- Expanded `tests/test_romanization_matrix.py` and `tests/test_romanization_vowel_matrix.py` to require complete target-column coverage and the project orthographic status/notes.
- Updated `docs/romanization-to-ukrainian-matrix.md` with the target convention and a separate acceptance gate. `KHM-ROM-UA-TARGET-001` is DONE_VERIFIED: exact-head Quality [43221517618](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43221517618) and browser smoke [43221517788](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43221517788) both SUCCESS; push Quality [43221506380](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43221506380) SUCCESS. The final Python suite reported 194 passed + 62 subtests. Runtime adapter `KHM-ROM-UA-001` remains TODO, BGN/PCGN engine `KHM-ROM-ENGINE-001` remains PARTIAL, and contextual syllable resolution remains PARTIAL.
- This is a letter-level rendering of Latin BGN/PCGN strings into Ukrainian, not phonetic transcription. The upstream `@gmana/km-translit` output remains a BGN/PCGN-derived ASCII simplifier and does not yet implement the full contextual standard. No IPA labels, source phonology, gold data, or pronunciation accuracy claims changed.
- No local checkout/runtime was available through this connector session. Exact-head GitHub Actions Quality and browser smoke workflows passed on commit `91736b45c32ad5a812f71b97e7594a2f7a8da1bc`; Quality: 194 Python tests + 62 subtests, Node checks and build; browser smoke also passed. The latest follow-up commits are documentation-only.


## Post-merge mainline verification — romanization target matrix — 2026-11-12

- PR #161 merged into `main` as `6b0d0e75d794165e5eb935192fab0926e1efca39`.
- Mainline Quality [43221967799](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43221967799), browser smoke [43221968144](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43221968144), and Pages deployment [43221967939](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43221967939) all SUCCESS on the merge commit.
- Exact feature-head tests [43221517618](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43221517618) and browser smoke [43221517788](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43221517788) also passed on `91736b45c32ad5a812f71b97e7594a2f7a8da1bc`: 194 Python tests + 62 subtests, Node checks, build and Chromium smoke.
- `KHM-ROM-UA-TARGET-001` is DONE_VERIFIED. `KHM-ROM-UA-001` remains TODO (runtime Latin-to-Ukrainian adapter); `KHM-ROM-ENGINE-001` remains PARTIAL (the upstream ASCII romanizer is not fully conformant with contextual BGN/PCGN 1972). No IPA or pronunciation claim is implied.


## Khmer romanization → Ukrainian runtime adapter — 2026-11-12

- Started from `main` `3930c8055bcbd6f6747336ad7dce09c9f695f31e`; implementation branch `feat/romanization-to-ukrainian-runtime-2026-11-12`; PR [#164](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/164).
- Added `src/khmer-romanization-ukrainian.js` and wired it to the existing `khmerToLatin` output and the separate “За романізацією” panel. It maps the current Latin result to Ukrainian, preserves non-Khmer text and punctuation, and marks unknown Latin fragments `⟦…⟧`.
- Browser regression: `សុខា → Sokha → Сок'а`; phonetic IPA output remains hidden in romanization mode. Matrix token coverage is tested for consonants and vowel forms.
- **Evidence boundary:** npm package `@gmana/km-translit` documents that its ASCII BGN/PCGN-derived profile drops the standard diacritics and is not fully conformant. The adapter therefore reports `PROVISIONAL`; it cannot recover contextual PCGN vowel distinctions lost upstream. This is not a complete PCGN runtime.
- Exact-head Quality [43226337969](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43226337969), browser [43226337956](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43226337956), and push Quality [43226325685](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43226325685) SUCCESS on `1fa869c524bac5effc98411b71e47e458ad584ae`.
- `KHM-ROM-UA-001`: PARTIAL (runtime display adapter works for current ASCII profile; full diacritic/context coverage is blocked by upstream romanizer output loss). `KHM-ROM-UA-TARGET-001`: DONE_VERIFIED. `KHM-ROM-ENGINE-001`: PARTIAL. No IPA or pronunciation claim is made.



Exact-head Quality [43226337969](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43226337969), browser [43226337956](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43226337956), and push Quality [43226325685](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43226325685) SUCCESS on code head `1fa869c524bac5effc98411b71e47e458ad584ae`. Quality: 194 Python tests + 62 subtests; web checks and production build passed; Chromium visible-results smoke passed.


## Khmer romanization runtime — mainline post-merge verification — 2026-11-12

- PR [#164](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/164) merged as `0ba6107a7e5cb09cca44021669a7401fc125eac4`.
- Mainline Quality [43227360792](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43227360792), browser smoke [43227360789](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43227360789), and Pages deployment [43227360801](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43227360801) all SUCCESS.
- The merged implementation remains deliberately PARTIAL/PROVISIONAL: the upstream ASCII romanizer omits PCGN diacritics; this adapter cannot reconstruct lost contextual vowel distinctions. The IPA route remains separate.


## Romanization mainline reconciliation — 2026-11-12

### New research blocker: Cambodian national 1997 profile

The primary 1995/1997 system table is now located in the Ministry's 2023 provisional Gazetteer (pp. vii–viii). Its foreword says the Geography Department used the system and would submit it for consideration/adoption; the Gazetteer is explicitly provisional pending National Commission approval. Cambodia's national report and UNGEGN 2025 report confirm gazetteer use, while PCGN May 2026 says it is not yet consistently implemented. Thus the primary table is no longer a blocker; formal adoption/consistent implementation and reuse rights remain EVIDENCE_LIMITED. The original PDF is copyright © 2023 by the Geography Department; the ODC mirror record states no license for the PDF. Next: obtain formal adoption evidence, resolve reuse rights, independently transcribe/verify the table, and decide whether to add a separate runtime profile. Do not substitute ALA-LC Khmer 1997; it is a different cataloguing profile.


- Current `main`: `a86a59cf082d547563b45374ced9dfb45c5cd8db`.
- Preserved merged sequence: target-matrix completion PR #161 (`6b0d0e75d794165e5eb935192fab0926e1efca39`); matrix synchronization PR #163 (`3930c8055bcbd6f6747336ad7dce09c9f695f31e`); provisional runtime PR #164 (`0ba6107a7e5cb09cca44021669a7401fc125eac4`); post-merge evidence PR #165 (current mainline checkpoint).
- Current-head CI: Quality [43228414756](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43228414756), browser [43228414938](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43228414938), Pages [43228414646](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43228414646): all SUCCESS.
- Current ledger: target matrix DONE_VERIFIED (22 consonant + 37 vowel/rime rows); runtime PARTIAL (independent adapter integrated, provisional); source romanizer PARTIAL (ASCII profile loses PCGN diacritics and contextual vowel distinctions); contextual whole-standard BGN/PCGN implementation remains open.
- Open draft research PR #153 remains untouched. It is a separate G2P/provider integration, not a dependency of the romanization adapter.
- No local checkout was available in this connector-only session; verification cited here is hosted GitHub Actions on exact current `main`. No local pytest/npm/Playwright execution is claimed.

The 2025 UNGEGN Asia South-East Division report (GEGN.2/2025/73/CRP.73, p. 3) confirms the October 2023 national gazetteer also uses the 1997 transcription system: https://unstats.un.org/unsd/ungegn/sessions/4th_session_2025/documents/GEGN.2_2025_73_CRP73_item4a.pdf


## Post-runtime test closeout — 2026-11-12

- Latest implementation mainline commit: `f0485892f5d4b16e5fbe0ded6f8e083d8b044f4b` (PR #167, test execution coverage; merged).
- Corrected a real test-discovery gap: `tests/romanization-ukrainian.test.mjs` is now run by both `npm test` and `npm run check`. Added coverage for all 22 distinct PCGN consonant romanization tokens; the existing suite covers the 33 ASCII vowel candidates, unsupported units, passthrough and status behavior.
- Exact-main Quality [43250158336](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43250158336) and browser smoke [43250158628](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43250158628) passed on the implementation commit. Pages deployment was checked separately in run [43250158415](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43250158415).
- Remaining acceptance: source-matrix→runtime parity for every row, marks/numerals, real-package corpus tests, diacritic-preserving BGN/PCGN, and a separate evidence-gated decision on Cambodia's national 1997 system. Do not promote PROPOSED mappings or provisional output.


## Canonical Khmer romanization matrix → adapter parity — 2026-11-12

- Started from current `main` `c3a4370bb87b7d116b7ca032520cbc0047e6ff33` on branch `test/khmer-romanization-canonical-matrix-parity-2026-11-12`.
- Closed a remaining test drift gap: the consonant adapter test had a hand-maintained 22-row list even though `data/khmer/romanization_ukrainian.csv` is canonical. The test now parses that CSV and executes every row's Latin/target pair, including contextual `b,p` alternatives and the PCGN U+2019 onset marker.
- Existing ASCII vowel candidates remain separately tested; this does not validate the upstream package's lost diacritics, contextual vowel choices, or full BGN/PCGN conformance. Ukrainian values remain project proposals.
- Implementation commit: `68721f396ebfd6817737ea2d0fcd549a5ab8b94d`. Exact-head CI and full suite are pending; do not mark this item DONE_VERIFIED until they pass.
- Status: PARTIAL pending hosted Quality/browser/Pages checks on the exact final PR head.


## Post-merge closeout — canonical Khmer romanization matrix/runtime parity — 2026-11-12

- PR [#170](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/170) merged as `c5c26082abff87ce6224e00a68047620f9d9975f`.
- Exact PR-head Quality workflow [43266798081](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43266798081) **SUCCESS**: gold-corpus structure validation, Python tests, Node web checks and Vite production build.
- Exact PR-head browser smoke [43266797880](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43266797880) **SUCCESS**: deterministic web checks, production build and Chromium visible-results smoke.
- `KHM-ROM-TEST-MATRIX-PARITY-001`: **DONE_VERIFIED** for the bounded 22-row consonant CSV → runtime mapping contract. This does not close `KHM-ROM-ENGINE-001` or the contextual vowel/marks/numerals/real-package whole-message acceptance work.
- Mainline Quality, browser smoke and Pages deployment were queued after merge at runs `43267004981`, `43267004560`, and `43267004404`; their final outcomes must be checked before claiming deployment success.
- No local checkout or local test command was available in this connector-only run. All pass evidence above is from hosted GitHub Actions on the exact PR head.


## Real-package Khmer whole-message → Ukrainian adapter regression — 2026-11-12

- Started from current main `60caa3903c546e6cd8a79a644161c4fe450fd703` on `test/khmer-romanization-whole-message-adapter-2026-11-12`.
- Added a whole-message test using the actual `@gmana/km-translit` dependency and `renderKhmerRomanizationText`, rather than a stub romanizer. The mixed probe covers Khmer numerals, Latin identifier, ASCII digits/punctuation, tab, CRLF and Khmer sentence-stop punctuation; it requires Khmer letters to be converted.
- This is an engineering/source-preservation regression only. It does not adjudicate the romanization or target Ukrainian output and does not resolve missing diacritics, contextual PCGN vowels, marks/numeral rules, or full-standard conformance.
- Code commit: `d1b41a8ada377af413f2dd1c079feb7dbcfaddfa`. Exact-head Quality/browser CI pending; status PARTIAL until those checks pass.


## Post-merge closeout — real-package Khmer whole-message adapter regression — 2026-11-12

- PR [#172](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/172) merged as `054bc8823ba1f109ee102eda5e966edade1c4886`.
- The actual `@gmana/km-translit` dependency is exercised through `renderKhmerRomanizationText` on a mixed whole message. Assertions cover native-or-Arabic numerals, Latin identifier and ASCII digits, comma, tab, CRLF, Khmer sentence-stop punctuation, and no Khmer-letter leakage.
- Exact PR-head Quality [43267521108](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43267521108) and Chromium smoke [43267521498](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43267521498): **SUCCESS**.
- Exact mainline Quality [43267655512](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43267655512), browser smoke [43267655359](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43267655359), and Pages deployment/deployed-site runtime smoke [43267655210](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43267655210): **SUCCESS** on the merged mainline commit.
- `KHM-ROM-TEST-WHOLE-001`: **DONE_VERIFIED**. `KHM-ROM-TEST-001` remains PARTIAL because canonical marks/numerals runtime parity, full source-profile coverage, and diacritic/contextual tests are not yet complete.
- `KHM-ROM-ENGINE-001` remains PARTIAL: upstream ASCII romanizer drops BGN/PCGN diacritics and contextual vowel distinctions. Ukrainian candidates remain project proposals; no linguistic accuracy or expert approval is claimed.
- Mainline at this closeout: `054bc8823ba1f109ee102eda5e966edade1c4886`. No local checkout or local test execution is claimed; all verification above is from exact-head/mainline GitHub Actions.


## Khmer numeral crosswalk runtime fix — test-first — 2026-11-12

- PR [#174](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/174) began with a data-driven test for all ten numeral rows in `data/khmer/romanization_marks_numerals.csv`.
- RED evidence: Quality workflow [43268170106](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43268170106) failed on the intended assertion, row 0: actual native Khmer `០`, expected Arabic `0`; the other nine adapter tests passed.
- Fix: `renderLatinWord` now converts U+17E0–U+17E9 to ASCII digits 0–9 and counts them as mapped units. The actual-package mixed whole-message test now requires `2026`, not merely either native or Arabic digits.
- Implementation commit: `3244bd847c70daffe6549feca845300faa3e61d7`; tightened integration-test commit: `0ba14111793cf16460dc34c25ecf138e0ffcb007`. Exact-head Quality/browser GREEN and post-merge mainline evidence are pending.
- This closes the bounded numeral target crosswalk only; Khmer diacritical mark behavior remains context-dependent and PCGN upstream romanization remains ASCII/diacritic-lossy.


## Post-merge closeout — Khmer numeral crosswalk — 2026-11-12

- PR [#174](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/174) merged as `ae890fdd436aed9c0fab077401e7612153ce2e6a`.
- Test-first RED evidence: exact Quality run [43268170106](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43268170106) failed only the new canonical numeral assertion on row 0 (`'០' !== '0'`); all previous nine adapter tests passed.
- Implementation: `renderLatinWord` maps U+17E0–U+17E9 to ASCII digits 0–9 and increments the mapped count. The actual-package whole-message regression now requires Arabic-digit output.
- Exact PR-head Quality [43268412329](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43268412329) and Chromium smoke [43268412356](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43268412356): **SUCCESS**.
- Exact mainline Quality [43268536002](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43268536002), browser smoke [43268536046](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43268536046), and Pages deployment/deployed-site runtime smoke [43268535985](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43268535985): **SUCCESS**.
- `KHM-ROM-NUMERALS-001`: **DONE_VERIFIED** for the ten numeral rows. `KHM-ROM-TEST-001` remains PARTIAL due unresolved diacritical marks, broader context-sensitive PCGN coverage and full real-package corpus acceptance.
- `KHM-ROM-ENGINE-001` remains PARTIAL: the upstream ASCII romanizer drops BGN/PCGN diacritics and contextual vowel distinctions. Ukrainian candidates remain project proposals, not expert-adjudicated mappings.
- Mainline at this closeout: `ae890fdd436aed9c0fab077401e7612153ce2e6a`. Hosted GitHub Actions evidence only; no local checkout or local test execution is claimed.


## Khmer vowel inventory crosswalk coverage — 2026-11-12

- PR [#177](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/177) merged as `19a36f820625f53c6f50fbbe810bfbd074bb1ee7`.
- Added data-driven test across all **37** canonical PCGN vowel and vowel-coda rows in `data/khmer/romanization_vowels_ukrainian.csv`. Source diacritics are normalized to the ASCII output conventions of the current upstream package; every form must map to one of the row's existing Ukrainian candidates with zero unsupported units.
- Exact PR-head Quality [43275618264](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43275618264): **SUCCESS** (194 Python tests + 62 subtests; 12 Node adapter tests). Exact PR-head Chromium smoke [43275618099](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43275618099): **SUCCESS**.
- This is not a runtime change and not linguistic validation. The test does not adjudicate context-dependent alternatives, reconstruct lost diacritics, establish phonetic accuracy, or promote Ukrainian proposals to approved mappings.
- PR #176's shortened-vowel sequence coverage is also merged as `d4ac59a78447ba84c84e72457d10277706168434`; its exact PR-head Quality [43275112413], browser smoke [43275112515], and post-merge mainline Quality [43275258617], browser smoke [43275258586], and Pages/deployed-site smoke [43275258614] all passed.
- Post-merge mainline checks for #177 all passed on `19a36f820625f53c6f50fbbe810bfbd074bb1ee7`: Quality [43275764929] **SUCCESS**, browser [43275764932] **SUCCESS**, Pages deployment and deployed-site/runtime smoke [43275764931] **SUCCESS**.


## Repository documentation and branch-consolidation pass — 2026-11-15

### Baseline and scope

- Default branch at inspection: `main`, starting head `25cb1f4db5d0c971184f2393751506daa19f8df2`.
- A recursive tree inspection found 149 tracked files. Existing implementation, canonical data, test suites, audit history and research matrices were preserved.
- Created the single active task branch `docs/repository-information-architecture-2026-11-15` from that exact main head.
- This pass is documentation/information-architecture work. It does not change the Khmer linguistic model, IPA labels, Ukrainian correspondences, source data, benchmark rows, dependencies or generated reports.

### Branch and PR reconciliation

- The pre-existing branch inventory contained 40 non-main historical feature, test, research, CI, release and documentation branches (41 refs including main); this pass added one active task branch (42 refs total at follow-up inspection). Comparisons against live `main` show that the historical branch tips are generally diverged, often with many commits behind main. A branch tip is not evidence that its unique patch is still required; several historical feature lines have already been integrated or superseded by later mainline commits.
- At baseline inspection, the pre-existing open PR was draft [#153](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/153); this documentation pass subsequently opened [PR #179](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/179) for the documentation changes. PR #153 `research: benchmark Khmer G2P candidates and integrate evidence-gated hybrid`. Its head `bddb0186c9e62abd57827fa54233ebbfaa0540e2` is 34 commits ahead and 23 behind the inspected mainline in the branch comparison. It is intentionally not merged: it is a research draft, the optional benchmark workflow is manual-dispatch-only, corpus rights remain unresolved, and independent adjudicated IPA gold remains 0. Its diagnostic candidate outputs must not become production IPA authority.
- Merged PRs #157–#178 already account for their corresponding completed branch work on main. The older model-consensus research PRs #150/#151 were closed unmerged and superseded by deterministic-engine PR #152; practical-adapter PRs #154/#155 were closed unmerged and superseded by merged PR #156. No blind multi-branch/octopus merge, force-push, branch deletion, PR closure or repository setting change was performed. This connector session exposes branch creation and ref updates but no branch-delete operation; historical branches remain untouched.

### Documentation changes on the task branch

- Added `docs/README.md` as the central navigation index and repository layout map.
- Added `docs/agents/methodology-references.md` to record the five requested upstream repositories, exact reviewed snapshots, adopted practices and non-adopted material.
- Updated the root README to route readers through the documentation index.
- Updated `AGENTS.md` with one-active-task-branch integration policy and explicit non-destructive reconciliation rules.
- Reconciled `docs/architecture.md` and `docs/agents/codebase-map.md` with current Python, browser, IPA-adapter and separate orthographic-romanization paths.
- Appended this dated audit/handoff record. The existing canonical research matrices and status registers were not rewritten or downgraded.

### Task ledger

| Task | Status | Evidence / acceptance boundary |
|---|---|---|
| Inspect current default branch, tracked tree and key docs | DONE_VERIFIED | Live main SHA and recursive tree inspected; 149 tracked files returned. |
| Inspect branches and open PRs | DONE_VERIFIED | Branch heads compared to main in batches; open PR endpoint returned draft #153. Historical refs preserved. |
| Create one active task branch | DONE_VERIFIED | `docs/repository-information-architecture-2026-11-15` created from the recorded main SHA. |
| Establish central documentation navigation | DONE_VERIFIED | `docs/README.md` committed in `41b88ecdc7545b4f5f60738bc528c6d56e55c5a6`; all 30 relative Markdown links resolve against the exact commit tree. Exact-head Quality and Chromium workflows passed. |
| Reconcile architecture and codebase map | DONE_VERIFIED | `docs/architecture.md` and `docs/agents/codebase-map.md` reconciled against current source entry points/imports; exact-head Quality and Chromium workflows passed. |
| Record upstream engineering/design methodology | DONE_VERIFIED | Five upstream repositories and exact reviewed snapshots documented in `docs/agents/methodology-references.md`; no copied implementation or runtime dependency; exact-head Quality and Chromium workflows passed. |
| Merge all historical branches | DEFERRED | Not safe or technically equivalent to a single clean history: branch tips are divergent, many changes are already on main, and the only open PR is an evidence-limited research draft. No branch-delete operation is exposed. Acceptance requires branch-by-branch unique-diff review and explicit owner authorization for destructive archival/deletion. |
| Merge draft PR #153 | BLOCKED | 34 ahead / 23 behind in comparison; draft research integration; manual-only optional benchmark; source rights unresolved; no independent gold. Acceptance requires updated-base review, resolved rights and scope, exact-head required checks, and explicit research/production boundary. |
| Local Python/Node/build/browser tests | BLOCKED (environment) | No local checkout/shell execution is available through this GitHub connector session. Do not report these as run. Hosted exact-head CI remains the available verification path. |
| Resolve project license file/metadata mismatch | BLOCKED | `pyproject.toml` declares MIT, but the inspected tracked tree has no root `LICENSE`/`COPYING` file and GitHub repository metadata reports `license: null`. Acceptance requires owner confirmation of intended licensing and a canonical license file/metadata alignment; no license was selected or created. |

### Research status deliberately preserved

- Independent expert-adjudicated IPA gold remains 0; empirical accuracy remains null.
- The deterministic local rule engine remains the published phonetic authority; optional external G2P candidates remain diagnostic only.
- The Khmer → Ukrainian orthographic romanization adapter remains provisional/partial where upstream ASCII output loses diacritics and contextual distinctions.
- The Cambodian 1995/1997 national profile remains evidence-limited pending adoption and rights reconciliation.
- Manual visual, keyboard, assistive-technology and mobile QA is not established by automated CI alone.

### Verification and next gate

- Repository API inspection, branch comparisons, source-file inspection and upstream README/snapshot checks were performed through the connected GitHub integration.
- Exact code-bearing commit `41b88ecdc7545b4f5f60738bc528c6d56e55c5a6` was verified by push Quality workflow [43692108930](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43692108930) **SUCCESS**, PR Quality workflow [43692138758](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43692138758) **SUCCESS**, and Chromium browser smoke [43692138745](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43692138745) **SUCCESS**. The Quality job completed gold-corpus structure validation, Python tests, Node web checks and Vite production build; the browser job completed deterministic web checks, production build, Chromium install and visible-results verification.
- The documentation index's 30 relative Markdown links were checked against the exact commit tree; no missing internal targets were found.
- No local pytest, npm, Vite, Playwright or generator command was executed in this environment. Hosted CI is the verification evidence; do not describe it as local execution.
- PR [#179](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/179) carries this documentation batch. Its exact final-head CI results are recorded in the terminal verification section below. No deployment or release was requested.


### License governance blocker — 2026-11-15

The current `pyproject.toml` declares `MIT`, while the inspected repository tree contains no root `LICENSE`, `LICENSE.md` or `COPYING` file and GitHub repository metadata reports `license: null`. This is an unresolved project-owner decision, not permission to assume or publish MIT terms. **Status: BLOCKED.** Acceptance: owner confirms the intended project license, adds the canonical license text, and aligns package/repository metadata. No license file was fabricated or selected in this pass.


### Final branch-head verification — 2026-11-15

- Final documentation branch head after the license-governance note: `aa3dc61ab331ed0e79e1c4430ecd315254f0fb6e` (three commits ahead of baseline main, zero behind).
- On this exact head, push Quality [43692325225](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43692325225) and PR Quality [43692327962](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43692327962) completed **SUCCESS**. The PR Chromium browser smoke [43692327929](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43692327929) was still running when this record was prepared; do not mark browser verification complete until its final conclusion is checked.
- The documentation-only final changes include the license metadata blocker; no license terms were chosen or added.


## Post-merge closeout — documentation information architecture — 2026-11-15

- Documentation PR [#179](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/179) was squash-merged into `main` as `e84d530b0a4355d450ed1f7e2568a2c58ca4e9c4` at 2026-11-15T08:00:39Z.
- The PR head was `db0e1b930d4566f6443b2b3a19fd811269e33adb`. Exact-head push Quality [43692418605](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43692418605), PR Quality [43692421394](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43692421394), and Chromium browser smoke [43692421391](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43692421391) all completed **SUCCESS**.
- The final docs index's 30 relative Markdown links resolved against the exact PR-head tree with zero missing internal targets.
- Mainline workflows triggered by the merge commit: Quality [43692484702], Chromium browser smoke [43692484674], and Pages deployment [43692484691] were running at the time of this closeout. Check their final outcomes before asserting post-merge mainline/deployment verification.
- The task branch has completed its work and PR #179 is closed/merged. Historical branches remain preserved; no branch deletion was available through the connected GitHub integration. PR #153 remains open as an evidence-limited research draft.
- The project-license metadata mismatch remains BLOCKED for owner decision; no license was selected or added.


## Final mainline verification — 2026-11-15

- Main head at this verification: `8b6dd5a597a670e7c3ff7bc440b2a97b4762060e`.
- Quality [43692567616](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43692567616): **SUCCESS**.
- Chromium browser smoke [43692567608](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43692567608): **SUCCESS**.
- GitHub Pages deployment and deployed-site/runtime smoke [43692567615](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43692567615): **SUCCESS**.
- These are hosted mainline checks; no local shell execution is claimed. No runtime or linguistic data changed in the closeout commits.


## Continuation checkpoint — PR #153 patch-level audit — 2026-11-15

### Task ledger update

| Task | Status | Evidence / acceptance boundary |
|---|---|---|
| Recheck live main, PR #153 head, merge base and CI | DONE_VERIFIED | Main `b2743a2c0f0a843eec9acbab538adad5cfa7cad5`; PR head `bddb0186c9e62abd57827fa54233ebbfaa0540e2`; merge base `2fe36aa1eb64cc47fb60ab1b37561f40d57202a7`; compare is 34 ahead / 26 behind, 18 PR paths, 37 mainline paths since merge base. Exact-head Quality 43084554473 SUCCESS; Chromium 43084554830 SUCCESS; optional G2P benchmark 43084554487 SKIPPED. |
| Patch-level PR #153 review | DONE_VERIFIED (review only) | Reviewed all 18 changed paths and focused patches for hybrid API, provider validation, benchmark harness, tests, workflow, and research documentation. Six paths overlap current-main changes. No code was merged or changed. |
| Integrate PR #153 wholesale | BLOCKED | Diverged history, six overlapping paths, changed public API contract, candidate IPA validator gap, unresolved corpus rights/split independence, optional benchmark skipped. Acceptance criteria are listed in `docs/repository-audit.md` under the dated PR #153 reconciliation. |
| Reuse source-attested MekongPhon diagnostic as project accuracy | DEFERRED / NOT PERMITTED | Source concordance against `pron_no_tones` is not independent gold; tone is not evaluated; independent gold=0 and accuracy=null. |

### Exact findings

- PR #153 is still open and draft, with `mergeable=false`; no reviews or comments are recorded.
- The PR replaces the current deterministic compatibility shim with an external-provider wrapper. Its candidate gate accepts arbitrary non-empty strings other than those containing `?`; it does not establish that output is valid, complete, profile-matched IPA. This is a concrete acceptance defect, not a hypothetical race/security concern.
- Provider priorities are correctly documented as execution/display order only, not accuracy or promotion weights.
- The new MekongPhon harness intentionally reports source-attested concordance only and does not call it accuracy. Its manual workflow did not run in the exact-head CI checkpoint.
- Source corpus rights and training/evaluation split independence remain unresolved. The full Khmer acoustic dictionary is absent upstream and its reported counts/licenses conflict.
- Historical branches were not altered. The audit does not authorize bulk merge, force update, or deletion.

### Next genuine blocker

PR #153 should remain a draft until its research-only API boundary, typed IPA validation, six overlapping paths, corpus rights, and split independence are resolved. Independent expert-adjudicated Phnom Penh IPA gold remains 0; do not invent scores or promote source-attested labels. Hosted CI was inspected; no local shell execution is claimed.


## Final continuation checkpoint — historical branch audit — 2026-11-15

- Live main after documentation PR #180: 509a35f0d9899959c08a809d486e9c0e09d5c957.
- All 41 non-main branch refs returned by GitHub search were compared against main. Their tips are divergent because squash-merged task histories are not ancestors of main; do not infer unique work from ahead/behind counts alone. File-level summaries were checked against merged/superseded PR history.
- Spot checks: the unmodelled-letter fix branch's source/sign/test files are exactly identical to main; the numeral runtime branch's adapter file is identical while its tests have evolved; the older grapheme-accounting branch is superseded by later parser/test changes. Romanization and practical-adapter branches are historical task snapshots whose accepted work is already represented by merged PRs. Earlier practical-adapter PRs #154/#155 were superseded by #156; earlier model-consensus PRs #150/#151 were superseded by deterministic-engine PR #152. Old coverage/font/G2P branches are far behind and not safe merge bases.
- No historical branch was deleted or force-updated. Keep current main as the sole integration base; preserve historical refs.
- PR #180 merged as 509a35f0d9899959c08a809d486e9c0e09d5c957. Exact PR-head Quality 43693340334 and Chromium 43693340375 passed. No post-merge mainline run result was exposed by the available commit-run lookup, so no post-merge CI success is claimed.
- PR #153 remains open/draft/BLOCKED: 34 ahead / 26 behind, 18 changed files, six paths overlap main's post-merge-base changes, candidate validation gap, unresolved corpus rights/split independence, and optional benchmark skipped. Independent adjudicated IPA gold=0; accuracy=null.

**Stop point:** all repository-visible branch comparisons and the active research PR's patch review are recorded. Further code integration is not evidence-safe until PR #153's explicit acceptance criteria are met. License metadata remains an owner decision blocker.


## Continuation checkpoint — typed IPA candidate validator — 2026-11-15

### Task ledger

| Task | Status | Evidence |
|---|---|---|
| Add typed candidate object/status and explicit IPA kind | DONE_VERIFIED | PR #182 adds immutable `IPACandidate`, `IPACandidateStatus`, and `validate_ipa_candidate`; package exports updated. |
| Preserve provider output and uncertainty | DONE_VERIFIED | Exact raw IPA string retained; provider id, profile, kind, status and uncertainty are typed fields. PARTIAL requires uncertainty notes. Tests cover tone, length, stress, tie bar and syllable separator preservation. |
| Reject obvious malformed IPA candidate notation/metadata | DONE_VERIFIED (bounded syntax gate) | Rejects empty/non-NFC strings, non-IPA scripts/symbols, orphan combining marks, bad delimiters, unsupported profile/kind/status and missing provider identity. Not a full IPA grammar or phonological validation. |
| Keep published deterministic result unchanged | DONE_VERIFIED | Only IPA module, package exports, tests and architecture docs changed; no external runtime provider added and no deterministic engine behavior changed. |
| Exact-head hosted verification | DONE_VERIFIED | Runtime/test head `a20f1d3f28cbe1a6a5f79cc7554afe4b47265a4a`; subsequent PR head `6f454e114822f765729666dd27d299604431266b` adds only the audit/handoff documentation recorded in this section. Quality run 43694149473 SUCCESS (206 tests + 62 subtests; corpus gate, web checks and build passed); Chromium run 43694149458 SUCCESS (including visible-result verification). |
| Integrate candidate API into PR #153 provider harness | BLOCKED / NOT DONE | PR #153 remains diverged and rights/split-limited. Keep this candidate boundary standalone until its API can be reconciled without changing published deterministic behavior. |

### Verification correction

The first hosted run for this change failed three tests because IPA tone bars U+02E5–U+02E9 are Unicode modifier symbols, not modifier letters. Added the five tone bars explicitly to the IPA symbol set and reran the exact updated head. Final Quality and Chromium workflows both passed. The failed initial attempt is retained here for audit transparency.

### Remaining blockers

- PR #153: unresolved corpus rights, split independence, six overlapping paths and divergent history; keep it open as draft.
- Independent adjudicated Phnom Penh IPA gold: 0; accuracy: null.
- The validator is deliberately a conservative syntax/metadata gate. It does not verify phonological truth, completeness, profile match beyond the declared profile id, source rights, or provider honesty.
- License metadata mismatch and manual accessibility review remain unresolved as previously recorded.


**CI scope note:** the successful Quality and Chromium runs were triggered for the final runtime/test code head before the two documentation-only audit/handoff commits. The GitHub connector exposed no new workflow runs for the later documentation-only head; no additional test run is claimed for those docs-only commits. Post-merge mainline CI is the final verification gate.


## Mainline closeout — typed IPA candidate validator — 2026-11-15

- Starting main before this task: 2f0d9f362e5f82ebb4d3372eae8f8fb4cc2001ba.
- Implementation branch: feat/typed-ipa-candidate-validation-2026-11-15.
- PR [#182](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/182) merged successfully; final main merge commit: c69789b21bffb306497758a1181bef0d36459bd5.
- Exact runtime/test head: a20f1d3f28cbe1a6a5f79cc7554afe4b47265a4a. Quality [43694149473](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43694149473) SUCCESS (206 tests, 62 subtests; corpus structure gate, web checks, build). Chromium [43694149458](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43694149458) SUCCESS (visible result check included).
- The first CI attempt had 3 failures caused by unsupported U+02E5–U+02E9 IPA tone-bar symbols. Added those symbols explicitly; the final runtime/test head passed all checks. Two later commits only appended audit/handoff evidence. No CI run was exposed for the later docs-only PR head; no such run is claimed.
- No external provider, corpus, or model was added. The deterministic engine and output contract remain unchanged. The new typed candidate API is available for future research adapters, but COMPLETE is only provider metadata and is not independent gold or permission to publish output.
- PR #153 remains open/draft/BLOCKED pending API reconciliation, corpus rights, and train/evaluation split independence. Independent adjudicated Phnom Penh IPA gold remains 0; accuracy remains null.
- Existing blockers remain: MIT metadata without a tracked LICENSE file (owner decision), full manual accessibility review, and the linguistic gold-data gate.


## Final mainline checkpoint after PR #183 — 2026-11-15

- Documentation closeout PR [#183](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/183) was squash-merged as df5891a7b9c9cfecde31f2795617b29a44d4b929.
- Exact PR-head Quality [43694397227](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43694397227): **SUCCESS**. The job completed corpus structure validation, Python tests, Node web checks and production build.
- Exact PR-head Chromium smoke [43694397191](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43694397191): **SUCCESS**, including visible-result verification.
- The implementation PR #182 and documentation PR #183 are both merged. Current source implementation was tested on code head a20f1d3f28cbe1a6a5f79cc7554afe4b47265a4a; documentation closeout was tested on PR #183 head baa98c02342f68bcca132618e84c7c5da34a465d. No local shell run is claimed.
- PR #153 remains the next major research blocker. Do not merge its external-provider integration until rights, train/evaluation split independence, API contract reconciliation and its benchmark run are resolved. Independent adjudicated IPA gold remains 0; accuracy remains null.
- The latest main commit at this checkpoint is df5891a7b9c9cfecde31f2795617b29a44d4b929. This handoff update itself is a further documentation-only commit on main.


## MekongPhon diagnostic harness reconciliation — 2026-11-15

- PR #153 was inspected against current main `5e082024b7ae871b1bb95219ea80e5b87502b66e`. Its head is `bddb0186c9e62abd57827fa54233ebbfaa0540e2`; the merge base is `2fe36aa1eb64cc47fb60ab1b37561f40d57202a7`. The branch is 34 commits ahead and 31 behind current main, with 18 changed paths; wholesale integration is unsafe.
- The PR hybrid wrapper is not ported: it accepts arbitrary non-empty IPA-like strings and does not call the new `validate_ipa_candidate` typed boundary. Its `HybridKhmerEngine` also conflicts with the current deterministic compatibility shim. A future provider adapter must construct a typed candidate with explicit profile, IPA kind, status, provider and uncertainty, preserve raw output, and remain non-promoting.
- Ported only the independent, opt-in MekongPhon diagnostic harness, regression tests, manual-dispatch workflow, and source/experiment registry evidence on a branch based on current main. No MekongPhon corpus rows or model weights were copied into this repository. The harness hashes the external corpus, emits source-attested concordance only, stores no source orthography/reference text in its report records, and fixes `independent_gold_count=0` / `accuracy=null`.
- Historical source-attested model run: 100/100 outputs, 64 strict matches, codepoint CER 0.12539184952978055 against `pron_no_tones`; this field omits tone. Training/evaluation split independence remains NOT_ESTABLISHED. This is not project accuracy and does not reproduce or validate the paper's reported under-2% result.
- Corpus rights remain unresolved in the pinned MekongPhon repository snapshot; model-card Apache-2.0 does not resolve training-corpus rights. Future external inference remains manual-dispatch only; no automated model download is part of the published runtime.
- Task ledger: benchmark harness/tests/workflow = PARTIAL pending exact-head hosted CI; research source registry = DONE_VERIFIED as a record of claims and caveats, not source-rights clearance; hybrid provider integration = BLOCKED pending typed adapter and rights; independent IPA gold = BLOCKED pending two blind Phnom Penh-profile annotations plus independent adjudication; training/evaluation disjointness = BLOCKED pending upstream split manifest/checkpoint provenance.
- No local shell, pytest, model inference, or network benchmark was executed in this session. Hosted CI results for the new branch will be recorded after they complete. PR #153 remains open/draft and was not merged or rewritten.


### Exact-head verification and final workflow corrections — 2026-11-15

- Final code/test head: `750a69b75ee7fa846572f63125d675e4557d12cc`.
- Quality [43695488162](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43695488162): **SUCCESS** — 214 Python tests and 64 subtests passed; independent IPA gold corpus structure validation, Node web checks and production build passed.
- Chromium [43695488169](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43695488169): **SUCCESS** — deterministic web checks/build and visible-result Chromium verification; 4 browser tests passed.
- The benchmark harness now fixes the model identifier to the audited model card; only the immutable model revision can be selected. A custom corpus path no longer inherits the default MekongPhon source commit claim: source revision is recorded only for the known default path or when explicitly supplied. Regression tests cover both cases.
- The optional workflow was reduced to `workflow_dispatch` only. A first draft also exported the upstream 100-row orthography/reference corpus as an Actions artifact; that job was removed because the dataset rights are unresolved. The retained job uploads model diagnostic outputs only, not source corpus rows. The workflow was not dispatched in this session.
- No local shell/pytest, model inference, or fresh external benchmark was run. Hosted CI above verifies repository tests/build/browser behavior, not external model performance.
- PR #184 contains the safe harness/data/docs port only; PR #153 remains open/draft and unmerged. Independent adjudicated Phnom Penh IPA gold remains 0, project accuracy remains null, corpus rights and checkpoint split independence remain blocked.


## Mainline closeout — MekongPhon diagnostic harness — 2026-11-15

- PR [#184](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/184) was squash-merged as `66c43e1772a4c871e06e625e80ad43da2d123c85`, based on starting main `5e082024b7ae871b1bb95219ea80e5b87502b66e`.
- Code/test head before merge: `1fa2db6dfe0a4802d6ccb12403a095393cfcd39a`. Exact-head Quality [43695611313](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43695611313) SUCCESS (214 Python tests + 64 subtests; corpus structure validation, web checks, production build); Chromium [43695611252](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43695611252) SUCCESS (4 browser tests, visible-result verification).
- Post-merge main Quality [43695677574](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43695677574) SUCCESS (214 tests + 64 subtests); browser [43695677644](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43695677644) SUCCESS; GitHub Pages build/deploy [43695677607](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43695677607) SUCCESS.
- The optional MekongPhon workflow is manual-dispatch only and was not dispatched. No model inference or new external benchmark was run. Its corpus-exporting job was removed; only model diagnostic outputs are uploaded. No source corpus rows or model weights are committed.
- The benchmark harness is an isolated research diagnostic, not a production provider. The current deterministic engine and typed IPA candidate boundary are unchanged.
- PR #153 remains open/draft/unmerged. Its provider wrapper still bypasses the typed candidate validator and is not ported. Corpus rights and checkpoint train/evaluation split independence remain unresolved. Independent adjudicated Phnom Penh IPA gold remains 0; empirical accuracy remains null.
- No local shell or pytest execution is claimed. This is an engineering-verification closeout only; the repository remains a research platform / partial prototype, not linguistically validated production.


## Continuation — PR #153 selective reconciliation — 2026-11-15

- Current base main at task start: `d4c058b346d51179af85b3f8173af3ecc79b4adb` (PR #184 mainline closeout).
- PR #153 is draft/open and materially diverged: 34 commits ahead / 34 behind relative to current main; its recorded base SHA predates the latest main. Whole-branch merge is rejected as an approach.
- Main already contains the diagnostic benchmark harness and manual-only workflow from PR #184; these were preserved rather than duplicated.
- Selectively ported a new runtime bridge in `feat/typed-ipa-hybrid-bridge-2026-11-15`. It calls the current typed `validate_ipa_candidate` for every external candidate, rejects bare strings and malformed metadata/notation, preserves exact raw IPA, records uncertainty/provenance, and never alters deterministic `ipa`/Ukrainian output. External execution remains explicit opt-in.
- Added eight focused hybrid tests, public factory/adapter exports, a dedicated API contract document, and README/engine-contract updates. Next action: run exact-head hosted Quality + Chromium checks; fix any failures; then submit a small PR against current main.
- Blocked/evidence-limited: no independent adjudicated Phnom Penh IPA gold (0); model train/evaluation split independence not verified; MekongPhon corpus rights unresolved; no external model inference run; no production promotion permitted.


## PR #185 closeout — typed hybrid provider bridge — 2026-11-15

- Starting main: `d4c058b346d51179af85b3f8173af3ecc79b4adb`.
- Implementation branch: `feat/typed-ipa-hybrid-bridge-2026-11-15`.
- PR [#185](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/185) merged successfully; merge commit: `71a0962ef4977aacde29ef016a13e108044d72b7`.
- Final code/test head: `1d93b823fd15f5fe57da527b2afb5cc86a4b8f0b`. Quality [43696684037](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43696684037) SUCCESS (222 tests + 64 subtests, corpus validation, web checks, production build). Chromium [43696684048](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43696684048) SUCCESS (visible-result check).
- First PR-head CI caught two obsolete tests asserting the previous alias-only hybrid API. Updated the tests to assert the new wrapper preserves deterministic output and requires typed providers; the final exact head passed. Initial failed run 43696654577 is retained for transparency.
- PR #184's diagnostic benchmark harness/workflow were reused, not duplicated. PR #153 remains open/draft/diverged; no blind merge. Its old branch still contains overlapping stale changes and is not a clean integration base.
- Remaining blockers: MekongPhon corpus rights unresolved; exact model checkpoint train/evaluation split independence unverified; independent adjudicated Phnom Penh IPA gold 0 and accuracy null; no external model inference run in this task. Keep all external candidate results diagnostic and never promote them to published output.

## Selective PR #153 research-record reconciliation — 2026-11-15

- Rechecked PR #153 against current main. The old runtime and benchmark workflow are superseded by the typed hybrid bridge in PR #185 and the safe manual-only benchmark harness in PR #184; neither old implementation is reintroduced.
- The branch also contained three useful source records absent from the current main registry. Selectively recorded the PhonSobon model and NCKL-derived respelling dataset as auxiliary Khmer-script respelling/syllabification resources (not IPA), and corrected the Khmer Acoustic Model dictionary entry to preserve its conflicting entry counts and CC BY 4.0 vs CC BY-SA 4.0 declarations.
- No third-party dataset rows, weights, code or model assets were copied. PhonSobon dataset rights remain unverified; the Khmer Acoustic Model full dictionary remains unavailable in the inspected pinned tree. Both remain outside runtime and gold.
- Source evidence checked in this continuation: PhonSobon model card and dataset card; Khmer Acoustic Model root README plus the previously pinned dictionary README/tree review. Upstream model/dataset claims are recorded as claims, not independently reproduced measurements.
- Current branch: `research/phon-sobon-and-lexicon-triage-2026-11-15`, based on main `3cdabeb0eaa325ddbf76c40c4d6baf036467828d`. Exact-head CI and documentation checks are pending.
- Acceptance ledger: PhonSobon source record = PARTIAL (recorded, rights-limited, non-IPA); Khmer Acoustic Model dictionary = BLOCKED (full artifact/count/rights conflict); PR #153 whole-branch merge = REJECTED (diverged and contains superseded runtime/workflow changes). Independent adjudicated Phnom Penh IPA gold remains 0; accuracy remains null.

### Additional PR #153 source-record reconciliation — Google TTS and OpenSLR42

- Added the pinned Google Language Resources Khmer lexicon/phonology files as a PARTIAL research lead. The bounded extraction found Latin-script spelling keys in the inspected subset; because the complete lexicon was not inspected, this is not generalized to every row. The feature inventory is not silently normalized to IPA, and Khmer-specific data rights remain unverified.
- Added OpenSLR SLR42 as supporting audio only. The current official page lists a male archive under CC BY-SA 4.0, while the 2018 paper reports 17 female speakers. This discrepancy is recorded as a blocker requiring archive manifest/checksum and speaker-ID reconciliation.
- Neither resource was downloaded, imported, or promoted to gold. These additions complete the remaining source-triage observations from PR #153 that were safe to preserve without copying third-party data or runtime code.

## Completion of PR #153 source-registry reconciliation — 2026-11-15

- The remaining external candidates from PR #153 are now represented in the canonical registries: MekongPhon rule-based baseline (source inspected, not executed; rights unknown), PhonSobon model (Khmer-script respelling, not IPA), and PhonSobon NCKL-derived dataset (respelling/syllabification only; NCKL terms unresolved).
- Historical MekongPhon model diagnostics already existed in the current registry and were preserved, including both pinned 100-row runs. No duplicate run records were added.
- PR #153's stale runtime and duplicated benchmark workflow remain excluded; the current typed bridge and manual-only benchmark harness remain authoritative. All remaining research records are non-runtime and disabled.

## PR #153 selective reconciliation — final mainline closeout — 2026-11-15

- Current `main` head after this work: `34f9dbfd94788d1d1b9b64646354157d4741dfed`.
- PR #187 merged as `1ef8578143bd2a0e9d55a46c0ddef4d0006dc5c3` from exact head `f65b54d5b476f0808b07307ee620b534ec936f29`. Quality [43697879406](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43697879406) SUCCESS (222 tests + 64 subtests; corpus validation, web checks and production build); Chromium [43697879409](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43697879409) SUCCESS.
- PR #188 merged as `34f9dbfd94788d1d1b9b64646354157d4741dfed` from exact head `a5d740a7d1f978b9192e3c8b4402e68f972f81a4`. Quality [43698031836](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43698031836) SUCCESS (222 tests + 70 subtests; corpus validation, web checks and production build); Chromium [43698031838](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43698031838) SUCCESS (4 browser tests). Duplicate Quality run [43698022071](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43698022071) also SUCCESS.
- PR #153 was closed unmerged as superseded after its remaining useful source-triage records were selectively reconciled. Closure comment: `6892169857`. Its source branch was left untouched. The old untyped provider runtime and duplicated benchmark workflow were not merged; current PR #184/#185 implementations remain authoritative.
- Additional branch reconciliation: `docs/repository-information-architecture-2026-11-15` was compared with current main. Its documentation index, AGENTS.md, codebase map and methodology reference were identical; its README/architecture/audit snapshots were older than main. It was left untouched rather than merged or deleted.
- No local shell/pytest or external model inference was performed. All stated engineering verification above is hosted GitHub Actions on exact PR heads.
- Acceptance ledger: external source registry updates = DONE_VERIFIED as documentation/metadata only; PhonSobon use = PARTIAL/rights-limited/non-IPA; MekongPhon rule baseline = PARTIAL/not executed/rights unknown; Khmer Acoustic Model dictionary = BLOCKED; Google TTS lexicon = PARTIAL/format and rights unresolved; OpenSLR42 = PARTIAL/metadata mismatch pending archive manifest.
- Remaining hard blockers: independent adjudicated Phnom Penh IPA gold = 0 and accuracy = null; MekongPhon corpus rights unresolved; checkpoint train/evaluation split independence unverified; full Khmer Acoustic Model dictionary and one authoritative data license unavailable; NCKL terms unresolved for PhonSobon data; Google lexicon's complete script/format and Khmer-specific rights not verified; OpenSLR42 archive manifest/speaker discrepancy unresolved; repository-level MIT declaration has no root `LICENSE` file and requires owner confirmation before adding license text.
- Release assessment: research platform / partial prototype, not linguistically validated production. Hosted engineering green does not close the linguistic, data-rights or manual accessibility gates.

## Phonotactic scope and 2025 PPK pitch research — 2026-11-15

- Added source-backed classification of major-syllable restrictions vs minor-syllable type-A/type-B restrictions using Nacaskul (1978). No final clusters and short-open-nucleus restrictions remain historical source reports pending contemporary profile confirmation; type-specific restrictions are not global bans.
- Added Unicode L2/22-290 and Ding et al. (2018) evidence showing orthographic coeng stacking/chaining and phonetic syllabification are not equivalent. The two-pre-vowel-coeng limit is an orthographic encoding limit, not a phonological onset maximum.
- Added Mam et al. (2025): 50 target words, five native speakers, three repetitions; PPK shows lower F0 for /r>h/ forms and voiced-onset disyllables, suggesting possible pitch phonologization. This is a bounded profile-specific result, not a universal Khmer tone rule. The careful-citation profile remains unchanged.
- A Sak-Humphry (2025) preview excerpt contradicts itself about whether /r/ is an allowed coda; it is recorded but not used to settle the inventory.
- Added a parser regression for the Unicode syllable-chaining example. It checks lossless orthographic trace and explicit `phoneticization_not_yet_established`; no phonological rules or IPA labels were added.
- Acceptance ledger: phonotactic scope = PARTIAL; PPK pitch = PARTIAL; orthographic chaining boundary = DONE_VERIFIED (source contract + regression). The remaining blocker is profile-matched lexical/acoustic adjudication, not an engineering guess.

## Phonotactic scope research closeout — 2026-11-15

- PR #190 merged as `262d16fb755aff952fef42ecb69f8c8a8251df30` from exact head `df79de7d39471f706fb8350e09e557a18c86c097`.
- Exact-head Quality [43698504896](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43698504896) SUCCESS: 223 Python tests + 70 subtests; IPA corpus structure validation, web checks and production build passed. Duplicate Quality [43698495803](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43698495803) also SUCCESS.
- Exact-head Chromium [43698504898](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43698504898) SUCCESS: 4 browser tests.
- The new parser regression verifies lossless trace of the Unicode coeng-chaining example while keeping `phonetic_representation.status = phoneticization_not_yet_established`. This verifies the boundary only; it does not validate a phonetic syllabifier.
- Sources now separate Nacaskul's historical major/minor syllable restrictions, Unicode's orthographic coeng/chaining rules, Ding et al.'s secondary name-romanization description, and Mam et al.'s bounded 2025 PPK F0 results. The Sak-Humphry preview's coda contradiction is recorded but not adopted.
- No new global coda/onset rejection rule, tone label, IPA label or /r/-rewrite was introduced. The current careful-citation profile remains unchanged.
- Statuses: orthographic/phonetic boundary regression = DONE_VERIFIED; phonotactic scope matrix = PARTIAL pending contemporary profile-matched lexical evidence; PPK pitch = PARTIAL pending replication/perception and speaker coverage.
- No local shell/pytest, human IPA adjudication or acoustic reanalysis was performed. Engineering checks are hosted CI only.

## Direct BGN/PCGN romanization input closeout — 2026-11-15

- PR #192 merged as `736b1bc30bc6ccea6eb1d9f3aacd0647c17b848f` from exact head `e790249dee908c46cad5b1846a81e84014d83338`.
- Exact-head Quality [43699528446](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43699528446) SUCCESS: 223 tests + 70 subtests; data/corpus validation, web checks and production build passed.
- Exact-head Chromium [43699528852](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43699528852) SUCCESS: 7 browser tests, including direct diacritic-preserving input, unknown-fragment bracketing and keeping phonetic diagnostics hidden while the romanization mode is active.
- Earlier exact-head failures were retained: [43699140457](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43699140457) exposed a missing ASCII `ie` fallback; [43699450855](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43699450855) exposed a target-alternative grouping issue for shortened vowel forms. Both were corrected; final exact-head checks are green.
- Romanization mode now accepts either Khmer script (existing ASCII romanizer path) or a Latin-only BGN/PCGN 1972 input. Direct input maps the raw diacritic forms in all 37 vowel/rime rows; unknown Latin fragments remain in `⟦…⟧` with PARTIAL status.
- This is orthographic input mapping, not IPA and not semantic translation. Ukrainian candidates remain PROVISIONAL. The direct path cannot reconstruct omitted diacritics or validate arbitrary non-BGN/PCGN romanization. Mixed Khmer+Latin input is not a dedicated mode.
- The Khmer-script source path still uses `@gmana/km-translit` 0.1.2 and therefore loses PCGN diacritics. A complete contextual Khmer-script→BGN/PCGN generator remains PARTIAL.
- No independent Ukrainian standard/adjudication was created. The result is a usable direct-input path with explicit uncertainty, not a claim of complete BGN/PCGN conformance.

## Mixed-script romanization guard closeout — 2026-11-15

- PR #194 merged as `4e1b95f2a1680e7c7363a68b226b0b44778cac74` from exact head `5c09a03d3d45a16001f73781fe7eb7bf7d057826`.
- Exact-head Quality [43709408446](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43709408446) SUCCESS (223 tests + 70 subtests; deterministic web checks and production build passed).
- Exact-head Chromium [43709408411](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43709408411) SUCCESS (9 browser tests).
- An earlier browser run [43709299480](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43709299480) failed because the newly added UI assertions were attached to the Latin-only unknown-fragment test rather than the mixed-script test. The test placement was corrected; exact final-head browser verification passed.
- Direct BGN/PCGN input now brackets Khmer letters/marks in mixed or direct-renderer calls and returns PARTIAL rather than silently passing Khmer characters through. The UI explains the one-format-per-run boundary.
- Khmer numerals still convert to Arabic digits and Khmer punctuation is preserved. UI mode detection now distinguishes Khmer letters/marks from numerals and punctuation.
- Scope: no change to the Khmer-script romanizer, BGN/PCGN crosswalk values, Ukrainian target proposals, IPA pipeline or phonological rules.
- Post-merge workflow query for merge SHA returned no runs; verification is exact PR-head CI only. No local npm/Playwright execution is claimed.
- Repository remains a partial research prototype; Ukrainian candidates are provisional and linguistic/data-rights/accessibility gates remain open.

## Documentation checkpoint — mixed-script guard final mainline — 2026-11-15

- PR #195 merged as `0d1183553a4851eb0c21336f381be3d0f2d0efaf`; it records the implementation and verification from PR #194 in the canonical handoff, audit, completion register and README.
- PR #195 exact-head Quality [43709585653](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43709585653) SUCCESS (223 tests + 70 subtests); Chromium [43709585691](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43709585691) SUCCESS (9 browser tests).
- PR #194 implementation merge: `4e1b95f2a1680e7c7363a68b226b0b44778cac74`; exact-head Quality [43709408446](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43709408446) and Chromium [43709408411](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43709408411) passed.
- Current main at this checkpoint: `0d1183553a4851eb0c21336f381be3d0f2d0efaf`. No open PRs. GitHub's commit-workflow query returned no post-merge runs for the implementation merge; exact PR-head CI is the available evidence.

## Automated accessibility smoke closeout — 2026-11-15

- PR #197 merged as `9452ac70ee16973ac5f0e8bd28201501539409de` from exact head `b0ca05c11d89b83798f4786a291827a20e99b8f9`.
- Exact-head Quality [43709993984](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43709993984) SUCCESS (223 tests + 70 subtests; web checks and production build passed).
- Exact-head Chromium [43709994024](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43709994024) SUCCESS (11 browser tests).
- New browser assertions verify the input's accessible name, method switch group and button names, clear button name, Enter-key activation of the romanization method, and polite live status region.
- This is automated DOM/keyboard smoke coverage only. Manual screen-reader, full keyboard traversal, contrast, zoom/reflow, mobile and assistive-technology review remains PARTIAL and is not claimed complete.


## Exact mainline verification and PR reconciliation — 2026-11-15

- Verified default branch: `main`, head `14c87c275a3dcc599893da19b455b2e853abb630`; PR #198 is merged at this SHA. No open PRs were returned by GitHub at this checkpoint.
- Unlike the earlier checkpoint, post-merge push workflows are now confirmed on this exact main SHA: Quality [43710193628](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43710193628), Chromium [43710193653](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43710193653), and Pages [43710193633](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43710193633) all SUCCESS. Chromium job completed deterministic web checks, production build and visible-results verification. These are hosted workflows; no local checkout or local test command was run.
- PR #153 is confirmed CLOSED, unmerged, and superseded. A fresh comparison against current main reports 34 commits ahead / 48 behind with divergent changes, including an old hybrid runtime and duplicated optional benchmark workflow. Its useful source-triage records were selectively preserved through PRs #187/#188; do not merge or revive its branch. The source branch was left untouched.
- Open issue #104 remains the genuine human acquisition blocker: expert-approved IPA convention, two qualified annotators, independent adjudicator, curator, blind intake, 30 attested lexeme groups, rights review, double annotation and adjudication are still outstanding. No human annotations or gold rows were fabricated.
- The existing release blockers remain: independent adjudicated IPA gold 0 and accuracy null; contextual phonology and Phnom Penh /r/-loss validation incomplete; Khmer-script BGN/PCGN output loses diacritics; Ukrainian romanization targets remain provisional; external corpus/model rights and train/eval independence unresolved; manual accessibility QA remains PARTIAL. Root `LICENSE` remains absent while `pyproject.toml` declares MIT; this is an owner decision, not silently changed.
- Repository branch metadata still reports `main` unprotected. No branch protection, licensing, release or external account setting was changed.
- Readiness: engineering pipeline is green on this exact main SHA, but the repository remains a partial research prototype, not a linguistically validated production release.


## Current-main reconciliation — 2026-11-15 (89e5ba4)

- **Verified current default branch:** `main` at `89e5ba49c7507f60b421119cbae4b63c240ac3c8`. The preceding checkpoint at `14c87c275a3dcc599893da19b455b2e853abb630` is historical, not current.
- **Exact-current-SHA hosted CI:** Quality [43712699599](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43712699599) SUCCESS; Khmer browser smoke [43712699648](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43712699648) SUCCESS; Pages build/deploy [43712699614](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43712699614) SUCCESS. Quality completed IPA corpus structure validation, Python tests, web checks and production build; browser completed deterministic web checks, production build and Chromium visible-results verification. No local shell/test execution is claimed.
- **PR state:** GitHub search returns no open PRs. PR #153 is CLOSED unmerged; comparing its head `bddb0186c9e62abd57827fa54233ebbfaa0540e2` with current main gives 34 commits ahead / 49 behind (diverged). Its stale runtime/workflow are not to be merged; selected research-source records were already preserved through #187/#188. PR #64 is also CLOSED unmerged; no resurrection is warranted without a new, independently identified UI defect.
- **Task ledger:** mainline engineering CI = DONE_VERIFIED (engineering only); PR #153/#64 historical reconciliation = DONE_VERIFIED (review/closure only); independent Khmer IPA gold = BLOCKED (0 adjudicated rows; accuracy null); contextual phonology and PPK pitch = PARTIAL; Khmer-script BGN/PCGN generator = PARTIAL (ASCII upstream path loses diacritics); Ukrainian romanization proposals = PARTIAL/PROVISIONAL; source/model rights and training/evaluation independence = BLOCKED/PARTIAL as recorded; manual accessibility review = PARTIAL.
- **Owner decisions:** root `LICENSE` remains absent while `pyproject.toml` declares MIT; do not add license text without owner confirmation. Main remains unprotected; do not change repository governance settings without authorization.
- **Readiness:** hosted engineering pipeline is green at this exact main SHA. This does not establish phonetic accuracy, legal clearance or human accessibility acceptance. The project remains a partial research prototype, not a validated production release.


## Khmer romanizer output-integrity guard — 2026-11-15

- PR #201 merged as `37a536592a8e462f00997890af63ad232d41a0ae` from exact head `42cb1ee70bc89daf6739af24e296a8e9dbb29a86`.
- The Khmer-script → upstream Latin → Ukrainian path now detects Khmer-script letters/combining marks still present in the upstream romanizer output, brackets each residual character, increments `unsupported`, and returns `PARTIAL`. The direct BGN/PCGN Latin renderer uses the same guard. Khmer punctuation is preserved; numeral handling and romanization mapping rules are unchanged.
- Regression tests cover a residual Khmer combining mark, a residual Khmer letter plus mark, direct Latin input with a Khmer mark, and preservation of Khmer punctuation.
- Exact PR-head Quality [43720084983](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43720084983) SUCCESS (Python tests, web checks, production build); Chromium [43720085021](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43720085021) SUCCESS.
- Exact post-merge main SHA `37a536592a8e462f00997890af63ad232d41a0ae`: Quality [43720186392](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43720186392), Chromium [43720186338](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43720186338), and Pages build/deploy [43720186436](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43720186436) all SUCCESS.
- Acceptance boundary: this is a fail-closed output-integrity guard, not a contextual Khmer → BGN/PCGN romanizer. It does not restore omitted diacritics, establish series/shortening/coda resolution, or upgrade romanization conformance. KHM-ROM-ENGINE-001 and KHM-ROM-TEST-001 remain PARTIAL.
- No local checkout/test execution is claimed. Repository remains a partial research prototype; IPA gold, language validation, legal and manual accessibility gates remain open.


## Final mainline checkpoint after romanizer guard — 2026-11-15

- PR #201 implementation merged as `37a536592a8e462f00997890af63ad232d41a0ae`; PR #202 documentation closeout merged as `1cc833ad1097f6b1ee7c28eb3e7aefb99ad480fb`.
- Verified current `main` at `1cc833ad1097f6b1ee7c28eb3e7aefb99ad480fb`. Post-merge workflows on this exact SHA all SUCCESS: Quality [43720449189](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43720449189), Chromium [43720449188](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43720449188), Pages build/deploy [43720449180](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43720449180). Pages deploy smoke-tested the deployed site and runtime assets.
- PR #202 exact-head Quality [43720352442](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43720352442) and Chromium [43720352370](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43720352370) also SUCCESS. PR #201 exact-head Quality [43720084983] and Chromium [43720085021] passed; see preceding section.
- PR #201 closes only the residual-script output-integrity hole. Khmer-script → BGN/PCGN remains ASCII-derived and loses diacritics; contextual series/shortening/coda logic, matrix mark semantics and broad romanizer parity remain PARTIAL. Ukrainian targets remain project proposals.
- Open PRs: none at the start of this final documentation checkpoint. Open issue #104 remains the external human acquisition blocker; no one was contacted or recruited and no gold IPA data was fabricated.
- Root `LICENSE` remains absent while `pyproject.toml` declares MIT (owner decision). Main remains unprotected; no governance setting was changed.
- No local checkout or local test execution is claimed. Readiness remains partial research prototype, not linguistically validated production.


## PCGN shortened-vowel mark inventory correction — 2026-11-15

- PR #204 adds U+17D0 SAMYOK SANNYA (◌័) to PCGN diacritical-mark row 3 alongside U+17CB BANTOC (◌់). Official PCGN note 5 distinguishes both marks and describes both within shortened-vowel patterns.
- The six PCGN rule categories remain six; the machine-readable inventory now explicitly covers seven Khmer source marks across those categories. No romanization or Ukrainian target was guessed or added.
- Regression coverage was updated in both Python and Node test suites. An intermediate data-only commit correctly triggered a red Python assertion because the old exact-glyph test expected only ◌់; the assertion is being updated to the source-backed two-mark contract. Exact PR-head verification on code/docs SHA `b27b87081819307da5ffe27d55e3cf4521004730`: Quality [43721677822](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43721677822), Chromium [43721677790](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43721677790), and push Quality [43721673728](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43721673728) all SUCCESS. Quality completed corpus validation, Python tests, web checks and production build; Chromium visible-results smoke passed.
- Scope remains inventory-only. Khmer-script → BGN/PCGN contextual generation, series/shortening/coda resolution and Ukrainian target review remain PARTIAL.


## Final mainline checkpoint — PCGN mark inventory correction — 2026-11-15

- Starting main SHA for this batch: `4c6738940e58e152b9ab3f6d95f6c00006243ebc`.
- PR #204, `fix: inventory both PCGN shortened-vowel marks`, merged by squash as `58735a94a8a8f76635f948c2d003d590f26fb0b2`. It adds U+17D0 SAMYOK SANNYA alongside U+17CB BANTOC in PCGN note 5 row 3; Python and Node regressions now assert both source marks. No romanization or Ukrainian target was guessed.
- Final `main`: `58735a94a8a8f76635f948c2d003d590f26fb0b2`.
- Exact-main Quality [43721873111](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43721873111) SUCCESS: corpus structure validation; 224 Python tests + 70 subtests; web checks; production build.
- Exact-main Chromium [43721873141](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43721873141) SUCCESS: 11 browser tests.
- Exact-main Pages [43721873125](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43721873125) SUCCESS: build, browser exercise, deploy and deployed-site/runtime smoke test.
- `KHM-ROM-MARKS-NUMERALS-001` is `DONE_VERIFIED` for bounded inventory only. `KHM-ROM-ENGINE-001` and `KHM-ROM-TEST-001` remain `PARTIAL`; upstream Khmer-script romanization is still ASCII-derived and lossy.
- Open PRs: none. Issue #104 remains open and blocks independent adjudicated IPA gold (0 rows; accuracy null). Root `LICENSE` is still absent while `pyproject.toml` declares MIT (owner decision). Manual accessibility review remains PARTIAL; main protection is not changed.
- No local checkout/tests were run. Repository remains a partial research prototype, not a linguistically validated production release.


## Current mainline reconciliation — 2026-11-15 (post-PR #204)

- Current default branch verified at `6058768ca745fddf9306f66d2e325fbed512b6ec`; this is a documentation-only follow-up to PR #204's merge `58735a94a8a8f76635f948c2d003d590f26fb0b2`. No open PRs were returned; issue #104 remains the open human IPA-pilot blocker.
- Exact-current-SHA hosted workflows all SUCCESS: Quality [43722162644](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43722162644), Chromium [43722162599](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43722162599), Pages [43722162627](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43722162627). These are hosted GitHub Actions results; no local checkout or local tests are claimed.
- README now states the machine-readable inventory correctly: six PCGN diacritic-rule rows cover seven Khmer source marks; note 5 includes both U+17CB BANTOC and U+17D0 SAMYOK SANNYA; ten numeral rows are separate. This is an inventory clarification, not a new runtime rule.
- PR #204 implementation and its Python/Node regressions remain merged and verified. Contextual Khmer-script → BGN/PCGN generation, diacritic recovery, expert review of Ukrainian target proposals, independent IPA gold (0 adjudicated rows; accuracy null), rights review, manual accessibility, and owner decision on absent root LICENSE vs MIT metadata remain unresolved.
- Main remains unprotected. No repository settings, licensing, or release state changed. Readiness remains partial research prototype, not linguistically validated production.


## Exact mainline closeout — PR #206 — 2026-11-15

- PR [#206](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/206) merged by squash as `ab5ade5f0984b32884df9fa5dac5607f927a2ea4`; current `main` verified at that exact SHA. No open PRs at this checkpoint.
- PR-head checks on `58f2d5e4e3e4d2d6a87d03bc331675292636e373`: Quality [43723307784](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43723307784) and Chromium [43723307771](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43723307771) SUCCESS.
- Exact post-merge main checks on `ab5ade5f0984b32884df9fa5dac5607f927a2ea4`: Quality [43728032467](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43728032467), Chromium [43728032424](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43728032424), Pages build/deploy [43728032407](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43728032407) all SUCCESS. Quality includes corpus-structure validation, Python tests, Node web checks and production build; Chromium visible-results smoke and Pages deployed-site build/deploy completed. No local checkout or local test execution is claimed.
- PR #206 corrects only README inventory wording: six PCGN diacritic-rule rows cover seven Khmer source marks (including U+17CB BANTOC and U+17D0 SAMYOK SANNYA under note 5), plus ten numeral rows. It adds no runtime rule, Ukrainian mapping, IPA label or pronunciation claim.
- Preserved boundaries: `KHM-ROM-MARKS-NUMERALS-001` is DONE_VERIFIED for bounded inventory only; `KHM-ROM-ENGINE-001`, `KHM-ROM-UA-001` and `KHM-ROM-TEST-001` remain PARTIAL. The upstream Khmer-script romanizer remains ASCII-derived/lossy; contextual series/shortening/coda resolution and Ukrainian target expert review are not complete.
- Issue #104 remains open: independent adjudicated IPA gold=0 and empirical accuracy=null. Its human gates (approved IPA convention, two qualified annotators, independent adjudicator, curator, blind intake, rights-cleared 30-lexeme pilot) cannot be completed by repository automation. External source rights, root LICENSE vs MIT metadata owner decision, manual accessibility review and unprotected main remain unresolved.
- Readiness: partial research prototype, not linguistically validated or production-ready.


## External contextual romanizer candidate — 2026-11-15

- Inspected `pheasaKhmer/khmer-engine` at `31b72cd4665f69678fc835da2f501771e42f097a`. It provides a useful architecture reference: Khmer cluster parsing, heuristic syllable-boundary inference, series/shifter-aware nucleus selection, and explicit treatment of BANTOC/SAMYOK/ROBAT and codas.
- It is expressly an UNGEGN 2013 implementation, not yet verified rule-for-rule against this project's BGN/PCGN 1972 contract. Some code paths are marked as not present in the tables and inferred from secondary references. Syllable segmentation is heuristic and requires expert adjudication of ambiguous parses.
- License review: engine code MIT; bundled sample lexical/pronunciation data CC BY 4.0 and counts ODC-By 1.0; dependency `pheasa` declares Apache-2.0. No code or data was copied; no dependency was added.
- Disposition: research candidate only. Next engineering gate is a source-by-source BGN/PCGN ↔ UNGEGN rule diff plus a reviewed ambiguity/abstention corpus. It does not supply IPA gold and does not replace the IPA-first phonological path.


## BGN/PCGN ↔ UNGEGN rule-diff checkpoint — 2026-11-15

- Current base/main at start: `4bf66a05c04d419ab9cbf415fafdc78109ddf5c7`.
- Added `docs/audits/current/BGN-PCGN-UNGEGN-RULE-DIFF-2026-11-15.md`, grounded in the official UK PCGN BGN/PCGN 1972 guide, the UNGEGN 2013 Khmer section, Unicode's Khmer character list, and pinned candidate source code.
- Confirmed explicit rule difference: PCGN note 3's neutral subscript list excludes ស; UNGEGN note 3 adds ស. The candidate's `SERIES_NEUTRAL_SUBSCRIPTS` includes ស, therefore it is not PCGN-equivalent in that branch.
- Candidate-only/unsupported extensions recorded: SAMYOK SANNYA before final យ (commented “not given”), YUUKALEAPINTU mapping (commented “not given; Wikipedia”), generic fallback for unlisted vowel+NIKAHIT/REAHMUK combinations, and coda-conditioned eă for kh although the source lists k/ng/h. The weighted syllable-boundary costs are heuristic, not linguistic evidence.
- No code, data, dependency, IPA, Ukrainian mapping or generated artifact imported/changed. Candidate remains research-only; KHM-ROM-ENGINE-001 and KHM-ROM-UA-001 remain PARTIAL; IPA gold remains 0 and accuracy null.
- Next gate: complete a machine-readable row-by-row PCGN table parity diff, then build a project-owned parser with explicit ambiguity/abstention behavior. Do not port candidate heuristics or extrapolations.


## Exact-main verification after BGN/PCGN ↔ UNGEGN rule diff — 2026-11-15

- PR [#209](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/209) merged by squash as `266297fcc296388220ea48c975344f5aa14f097d`; exact `main` head verified at this SHA. No open PRs at this checkpoint.
- PR-head checks on `4f53e5c2f6759d1b188ace3d4fd0d9a4c08e6c42`: Quality [43730475810](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43730475810) SUCCESS and Chromium [43730475809](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43730475809) SUCCESS. Push Quality [43730456889](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43730456889) SUCCESS.
- Exact post-merge main checks on `266297fcc296388220ea48c975344f5aa14f097d`: Quality [43730567132](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43730567132), Chromium [43730567159](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43730567159), Pages build/deploy [43730567118](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43730567118) all SUCCESS. Hosted Quality completed corpus validation, Python tests, Node web checks and production build; browser smoke passed; Pages build, production-site Chromium exercise, deploy and deployed-site smoke passed.
- No local checkout or local test execution is claimed. No runtime code, dependency, corpus, IPA, Ukrainian target or generated artifact changed in PR #209.
- The bounded profile diff is recorded in `docs/audits/current/BGN-PCGN-UNGEGN-RULE-DIFF-2026-11-15.md`. `KHM-ROM-PROFILE-DIFF-001` is DONE_VERIFIED only for textual comparison; `KHM-ROM-ENGINE-001` and `KHM-ROM-UA-001` remain PARTIAL. Issue #104 remains open; adjudicated IPA gold=0 and empirical accuracy=null.
- Readiness remains partial research prototype, not linguistically validated or production-ready.


## PCGN notes 1–11 registry — 2026-11-15

- Added `data/khmer/romanization_pcgn_notes.csv`: all eleven notes from the official BGN/PCGN 1972 guide are now source-located with bounded summaries, exceptions, limitations and `DOCUMENTED_ONLY` status.
- Added `tests/test_romanization_pcgn_notes.py` to assert note count/order, primary-source provenance, the exact PCGN weak-subscript set (five nasals plus y/r/l/v; no ស), both shortened-vowel marks, the k/ng/h coda condition, and the absence of IPA/Ukrainian-gold fields.
- This is not a contextual romanizer implementation. It adds no code path, external dependency, IPA label, Ukrainian target, corpus row or generated pronunciation. Existing row-level CSV parity tests remain the evidence for the 22 consonant, 12 independent-vowel, 17 dependent-vowel, 8 anusvara/visarga, 6 diacritic-rule and 10 numeral table rows.
- The note registry is `DONE_VERIFIED` only as a source-located transcription of the guide's notes; runtime behavior remains `PARTIAL`. Note 3's ambiguous-foot warning and Note 5's contextual mark/coda behavior explicitly prohibit naive context-free mappings.
- Hosted CI must run on the exact PR head and exact post-merge main before this task is marked verified. No local checkout/test execution is claimed in this connector session.
- Next feasible gate: design a parser-facing, typed PCGN analysis record that retains base consonant, foot identity/uncertainty, series source, shifter presence/absence, vowel pattern, shortening mark, coda, syllable position and provenance; keep ambiguous or omitted-mark cases abstaining until source-backed evidence or expert review exists. Do not port UNGEGN heuristics.


## Exact-main verification — PCGN note registry / PR #211 — 2026-11-15

- PR [#211](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/211) merged by squash as `9383385fc3244ff600d0fab254c6488a83d92d7b`; exact current `main` verified at that SHA. No open PRs.
- PR-head `1724dbcff908c34d1854079c9df9e5fe3117db61`: push Quality [43732930991](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43732930991), PR Quality [43732940452](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43732940452), and PR Chromium [43732940449](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43732940449) all SUCCESS.
- Exact post-merge main `9383385fc3244ff600d0fab254c6488a83d92d7b`: Quality [43733051013](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43733051013), Chromium [43733051164](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43733051164), Pages build/deploy [43733051031](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43733051031) all SUCCESS. Quality ran IPA-corpus structure validation, Python tests, Node web checks and production build; Chromium visible-results smoke passed; Pages exercised the production site, configured/deployed Pages and completed its workflow.
- No local checkout or local test execution is claimed. The change adds a source-located documentation registry and Python regression tests only; no runtime, dependency, IPA, Ukrainian target, gold row or generated pronunciation changed.
- `KHM-ROM-PCGN-NOTES-001` is DONE_VERIFIED only for Notes 1–11 documentation and guardrail tests. `KHM-ROM-ENGINE-001` and `KHM-ROM-TEST-001` remain PARTIAL. Issue #104 remains open; adjudicated IPA gold=0 and accuracy=null. Root LICENSE/MIT metadata, source rights, manual accessibility and main protection remain unresolved.
- Readiness remains a partial research prototype, not a linguistically validated production release.


## Typed PCGN orthographic analysis — 2026-11-15

- New isolated module: `src/khmer_ua/pcgn.py`, exported as `analyze_pcgn_orthographic_chunk`.
- New serialized contract: `schemas/pcgn-orthographic-analysis.schema.json`.
- New focused tests: `tests/test_pcgn_orthographic_analysis.py`.
- The typed result preserves base and subscript identities plus their orthographic register labels, register-shifter identities, dependent/independent vowels, both shortening marks, ROBAT/AHSDA/TOANDAKHIAT positions, unresolved source components, NFC/raw forms and source references.
- Deliberate non-decisions are machine-readable: `NOT_PERFORMED` syllable segmentation, `UNRESOLVED` series and coda, `NOT_SELECTED` series source, and null romanization/IPA/Ukrainian. It does not run through the phonological engine and does not change existing IPA-first outputs.
- It accepts a caller-supplied chunk and does not claim to find chunk boundaries. Multiple unstacked consonants remain unassigned. Unknown characters and malformed coeng sequences are preserved and fail closed.
- This is the first parser-facing structural contract, not contextual PCGN rule parity. Next gates: validate schema/serialization in hosted CI; then add source-backed, independently reviewed contextual fixtures before any rule resolver or romanization generation. Do not infer a coda, syllable boundary or omitted shifter.


## Exact-main verification — typed PCGN orthographic analysis / PR #213 — 2026-11-15

- PR [#213](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/213) merged by squash as `18134929554420875b447b1c5128b3b879e3f608`; exact current `main` verified at this SHA. No open PRs.
- PR-head `065e5368cd07f1ecb78f330aefd98d7ea75467cc`: push Quality [43734102361](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43734102361), PR Quality [43734106341](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43734106341), PR Chromium [43734106320](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43734106320) all SUCCESS.
- Exact post-merge main `18134929554420875b447b1c5128b3b879e3f608`: Quality [43734192447](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43734192447), Chromium [43734192457](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43734192457), Pages build/deploy [43734192455](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43734192455) all SUCCESS. Quality ran independent IPA corpus structure validation, Python tests, Node web checks and production build; browser smoke verified visible results; Pages built and exercised the production site and uploaded/deployed the artifact.
- The Python test step passed on the final PR head after the final fail-closed correction for unmodelled Khmer letters. The schema JSON was parsed in the review session; the focused Python tests assert the contract's required fields and abstention constants. No local checkout or local test execution is claimed.
- New runtime scope is strictly structural: raw/NFC text, code-point-preserving tokens, base/foot identity, orthographic register labels, shifter/vowel/shortening/ROBAT/AHSDA/TOANDAKHIAT marks, unresolved source material and provenance. The schema requires `NOT_PERFORMED` syllable segmentation, `UNRESOLVED` series/coda, `NOT_SELECTED` series source, and null romanization/IPA/Ukrainian. It does not feed or alter the IPA-first engine.
- `KHM-ROM-PCGN-STRUCTURE-001` is DONE_VERIFIED for this bounded typed structure/abstention contract. `KHM-ROM-ENGINE-001`, `KHM-ROM-TEST-001` and `KHM-ROM-UA-001` remain PARTIAL: no contextual PCGN series/shortening/coda resolver, no independently reviewed expected-output fixtures, and no expert-adjudicated Ukrainian target set.
- Relevant old branches reviewed: typed-IPA bridge/candidate-validation branches carry core files byte-identical to main; their functionality is already present on main and was not re-ported. The old direct-BGN/PCGN-input branch differs in `src/khmer-romanization-ukrainian.js` and lacks the later residual-Khmer output guard now on main; it was left untouched rather than merged over the safer current implementation. Matrix-completion and romanization-runtime branch matrix files match main; stale branches were not deleted.
- Issue #104 remains open; independent adjudicated IPA gold=0 and empirical accuracy=null. Root LICENSE remains absent while pyproject metadata declares MIT; main remains unprotected. Readiness remains partial research prototype, not linguistically validated production.


## PCGN Note 3 series resolver — 2026-11-15

- Added `resolve_pcgn_series(analysis)` and `PCGNSeriesDecision` in `src/khmer_ua/pcgn.py`, with schema `schemas/pcgn-series-decision.schema.json` and tests `tests/test_pcgn_series_resolution.py`.
- The resolver applies only the PCGN 1972 Note 3 series rule: base if no foot; foot normally; base when the single foot is weak and base is not weak; foot when both are weak. Exact weak set: `ងញណនមយរលវ`; no UNGEGN-only `ស`.
- Preserves the Note 3 ប+foot p-in-â exception as typed metadata `BA_WITH_FOOT_P_IN_A_SERIES`. The parser now rejects a PCGN foot form for ឡ, which the official consonant table says has no subscript form.
- At this checkpoint, shifters were deferred; the later “PCGN Note 2 shifter subset” section records the bounded single-base implementation. Multiple/misplaced shifters, shifters on clusters and BA+TRIISAP still abstain. Multiple feet/bases and unsupported input also abstain. Output remains series metadata only; no vowel, coda, phonetic syllabification, PCGN Latin, IPA or Ukrainian output.
- Next gate: hosted exact-head Quality/Chromium, then exact-main checks; add Note 2 shifter resolution only after a separate source-grounded exception table and tests. Note 5 shortening remains blocked on coda and vowel-pattern parsing.


## Exact-main verification — PCGN Note 3 series resolver / PR #215 — 2026-11-15

- PR [#215](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/215) merged by squash as `357ce7f2a5400ff1643e4f64337009dd18c4113d`; exact current `main` verified at this SHA. No open PRs.
- PR-head `321a7d9ea03b47dae95bc2d7fd95f0c5a2745346`: push Quality [43734733096](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43734733096), PR Quality [43734746708](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43734746708), PR Chromium [43734746686](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43734746686) all SUCCESS.
- Exact post-merge main `357ce7f2a5400ff1643e4f64337009dd18c4113d`: Quality [43734828487](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43734828487), Chromium [43734828491](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43734828491), Pages build/deploy [43734828557](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43734828557) all SUCCESS. Pages includes a separate deploy job and deployed-site/runtime-asset smoke test.
- Python tests, web checks and production build passed on exact PR head and main. No local checkout or local test execution is claimed.
- `KHM-ROM-PCGN-SERIES-001` is DONE_VERIFIED only for Note 3 series selection. `KHM-ROM-PCGN-SHIFTERS-001` now records bounded Note 2 support as PARTIAL. `KHM-ROM-ENGINE-001` remains PARTIAL: cluster shifters, complete vowel/rime selection, coda, Note 5 shortening, syllable segmentation and full PCGN output are not implemented.
- The resolver preserves PCGN's exact weak-foot set (five nasals plus យ/រ/ល/វ, no ស), the ប+foot p-in-â exception, and the no-foot status of ឡ. It abstains on shifters and multiple feet/bases. No IPA or Ukrainian output changed.
- Issue #104 remains open; independent adjudicated IPA gold=0 and empirical accuracy=null. Root LICENSE absent while pyproject metadata declares MIT; main remains unprotected. Research prototype only.


## PCGN Note 2 shifter subset — 2026-11-15

- Extended `PCGNOrthographicAnalysis` with exact source positions for register shifters.
- `resolve_pcgn_series` now applies Note 2 only for one shifter immediately after one base consonant with no foot: TRIISAP U+17CA changes â→ô; MUUSIKATOAN U+17C9 changes ô→â.
- Preserves Note 3's BA + MUUSIKATOAN p-in-â exception. BA + TRIISAP remains unresolved.
- Shifters on clusters, multiple/misplaced shifters, wrong-direction shifters and unsupported structures abstain. No vowel, coda, syllable segmentation, PCGN Latin, IPA or Ukrainian output is generated.
- Updated the analysis and series-decision JSON Schemas and tests for shifter positions, before/after series and typed effects. Exact PR-head and main CI passed.
- This is a bounded subset, not complete Note 2 implementation. Next gates: review shifters on consonant+foot clusters and BA+TRIISAP; then tackle contextual vowel/rime selection and Note 5 only when coda is known.


## Exact-main verification — PCGN Note 2 shifter subset / PR #217 — 2026-11-15

- PR [#217](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/217) merged by squash as `c738075c47c76730aa15e96acea588ad924c829c`; exact current `main` verified at this SHA. No open PRs.
- PR-head `e1bd39fa43e80ae5cd60dc3af2dc850d7b206076`: push Quality [43735335039](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43735335039), PR Quality [43735349944](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43735349944), PR Chromium [43735349863](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43735349863) all SUCCESS.
- Exact post-merge main checks: Quality [43735441278](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43735441278), Chromium [43735441245](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43735441245), Pages build/deploy [43735441621](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43735441621) all SUCCESS. Pages includes a separate deploy job and deployed-site/runtime-asset smoke test.
- The bounded Note 2 subset preserves shifter source positions, pre-/post-shifter series and typed effect. It supports one correctly placed mark after one base with no foot, plus BA+MUUSIKATOAN p-in-â. It abstains on shifter+foot clusters, multiple/misplaced/wrong-direction marks and BA+TRIISAP.
- This is not complete Note 2 or full PCGN romanization. Vowel/rime selection, coda and syllable segmentation, Note 5 shortening, and PCGN Latin output remain PARTIAL. No IPA-first or Ukrainian target behavior changed.
- Issue #104 remains open; adjudicated IPA gold=0 and accuracy=null. Root LICENSE absent vs MIT metadata and unprotected main remain owner/governance blockers. Research prototype only.


## Exact-main verification — PR #218 PCGN Note 2 documentation closeout — 2026-11-15

- PR [#218](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/218) merged by squash as `9420326549d8a327774d0587b6fe19c4b17befcd`; exact current `main` verified at this SHA. No open PRs.
- PR-head `eec944d2393fd78f810fe19c405e0ee5fdeacd99`: push Quality [43735564674], PR Quality [43735576766], PR Chromium [43735576217] all SUCCESS.
- Exact post-merge main checks: Quality [43735662414](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43735662414), Chromium [43735662288](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43735662288), Pages build/deploy [43735662264](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43735662264) all SUCCESS, including deployed-site/runtime-asset smoke.


## Exact-main verification — PR #219 documentation closeout — 2026-11-15

- PR [#219](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/219) merged by squash as `690b44174a8831ac9b08b44786d5ffde43f6d5aa`; exact current `main` verified at this SHA. No open PRs.
- PR-head `d0cf981a7219d0c9ccd615a11b3f62b08dfffe14`: push Quality [43735841295], PR Quality [43735855013], PR Chromium [43735855047] all SUCCESS.
- Exact post-merge main checks: Quality [43735981736], Chromium [43735981714], Pages build/deploy [43735981744] all SUCCESS, including deployed-site/runtime-asset smoke.
- This is documentation-only verification. The Note 2 shifter implementation remains PARTIAL; no linguistic status is upgraded by this PR.


## Exact-main verification — PR #220 — 2026-11-15

- PR [#220](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/220) merged as `8c4784235742cd83c35ce4a2b0bc7831a2b11bb2`; exact current `main` verified at this SHA. No open PRs.
- PR-head push Quality [43736157032], PR Quality [43736168034], PR Chromium [43736167978] all SUCCESS.
- Exact post-merge main Quality [43736256876], Chromium [43736256892], Pages [43736257006] all SUCCESS on this SHA, including deployed-site/runtime-asset smoke.


## Exact-main verification — PR #221 — 2026-11-15

- PR [#221](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/221) merged as `0d9bb90b1451ce9a2452121e30c3864d4cd887f5`; exact current `main` verified at this SHA. No open PRs.
- PR-head push Quality [43736444673], PR Quality [43736456391], PR Chromium [43736456480] all SUCCESS.
- Exact post-merge main Quality [43736548569], Chromium [43736548708], Pages [43736548595] all SUCCESS on this SHA, including deployed-site/runtime-asset smoke.


## Exact-main verification — PR #222 — 2026-11-15

- PR [#222](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/222) merged as `95dd256b515c4a15e28cf80f21e3a53b0f0dfa11`; exact current `main` verified at this SHA. No open PRs.
- PR-head push Quality [43736688182], PR Quality [43736708656], PR Chromium [43736708789] all SUCCESS.
- Exact post-merge main Quality [43736800449], Chromium [43736800513], Pages [43736800469] all SUCCESS on this SHA, including deployed-site/runtime-asset smoke.


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



## PCGN Note 5 — bounded shortened-vowel component — 2026-11-15

Implemented `resolve_pcgn_shortened_vowel(analysis, onset_analysis, coda_class)` and exported `PCGNShortenedVowelDecision`.

The resolver covers only the exact BGN/PCGN 1972 Note 5/table shapes:
- `onset + coda + BANTOC` (table row 1): `á` in â-series, `ó` in ô-series.
- `onset + AA + coda + BANTOC` (row 2): `ă` in â-series; in ô-series `eă` before coda classes `k/ng/h`, otherwise `oă`.
- `onset + SAMYOK SANNYA + coda` (row 2): same row-2 series/coda values.

The onset is passed separately and must match the exact prefix of the full orthographic chunk. The series is resolved from that onset using the existing bounded Notes 2–3 resolver. The coda class is a required caller-supplied enum (`k`, `ng`, `h`, `other`); it is recorded but never inferred from the full chunk. Parser output now retains exact shortening-mark positions.

Regression fixtures include the official guide's examples `បត់ → bát`, `ចាក់ → chăk`, `រ្ពាក់ → rôpeăk`, `មាត់ → moăt`, `ច័ក → chăk`, and `ភ័ព → phoăpv`, plus explicit ô-series k/ng/h conditions and fail-closed malformed/mismatched contexts.

Schema: `schemas/pcgn-shortened-vowel-decision.schema.json`; tests: `tests/test_pcgn_shortened_vowel_resolution.py` and updated `tests/test_pcgn_orthographic_analysis.py`.

Source: BGN/PCGN 1972 Agreement, Vowel Characters table rows 1–2 and Note 5, pp. 2–3: https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.

Status: `KHM-ROM-PCGN-SHORTENING-001 = PARTIAL`. This is a shortened-vowel component only; no coda romanization, complete PCGN syllable, IPA, Ukrainian output, phonetic syllabification, or inferred coda is produced. `KHM-ROM-PCGN-VOWELS-001` and `KHM-ROM-ENGINE-001` remain PARTIAL.


## Exact-main verification — PCGN Note 5 shortened-vowel component / PR #233 — 2026-11-15

- PR [#233](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/233) merged by squash as `cf57045bf6ddf0537e2a5c33a8b2468e8f3f6f2c`; exact `main` verified at this SHA. No open PRs.
- Final PR-head `9bcf7391ce08557ce2fa56e4cbb764568949f952`: push Quality [43751102348], PR Quality [43751107119], PR Chromium [43751107131] all SUCCESS. Quality reports 272 Python tests passed and 70 subtests passed; web checks and production build passed; Chromium visible-results smoke passed.
- An earlier head `754f04d92009f342fb81f97ef9255c9ee7fb5fc1` failed two registry tests because they still required all PCGN notes to remain DOCUMENTED_ONLY. The tests were reconciled to permit Note 5's PARTIAL_COMPONENT_RESOLVER status while retaining the no-IPA/no-gold assertion; final exact-head checks passed.
- Exact post-merge main: Quality [43751266786], Chromium [43751266785], Pages build/deploy [43751266784] all SUCCESS, including production-site Chromium exercise and deployed-site/runtime-asset smoke.
- Linguistic status remains PARTIAL. The resolver returns only a shortened-vowel component and requires caller-supplied onset/coda context; it does not produce a complete syllable, IPA or Ukrainian output.


## PCGN Note 6 — bounded ROBAT component — 2026-11-15

Implemented `resolve_pcgn_robat(analysis, marked_consonant_romanization)` and exported `PCGNRobatDecision`.

The resolver accepts one ROBAT mark at the end of the supplied component chunk, immediately after one modeled unstacked Khmer consonant. The caller must supply that marked consonant's contextual PCGN romanization from the consonant table. The resolver validates the supplied value against the table's romanized consonant inventory and returns only `rC` (for example, the `rm` component in the guide example `ធម៌ → thôrm`).

Schema: `schemas/pcgn-robat-decision.schema.json`; tests: `tests/test_pcgn_robat_resolution.py`. The PCGN source registry now records Note 6 as `PARTIAL_COMPONENT_RESOLVER`.

Source: BGN/PCGN 1972 Agreement, Diacritical Marks table row 4 (p. 4) and Note 6 (p. 5): https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.

Status: `KHM-ROM-PCGN-ROBAT-001 = PARTIAL`. The consonant romanization is caller-supplied; the resolver does not infer syllable boundaries, determine the consonant's series/coda value, romanize the rest of the syllable, or produce IPA/Ukrainian output. ROBAT on foot clusters or non-final component positions abstains.


## Exact-main verification — PCGN Note 6 ROBAT component / PR #235 — 2026-11-15

- PR [#235](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/235) merged by squash as `34ab63ff37023bddcaeaebb0a6ccd838f662c045`; exact `main` verified at this SHA. No open PRs.
- Final PR-head `0d6f1a2b11ab1de94ad9be391c2dd4932142ff77`: push Quality [43751844908], PR Quality [43751851657], PR Chromium [43751851706] all SUCCESS. Quality reports 278 Python tests passed and 70 subtests passed; web checks and production build passed; Chromium visible-results smoke passed.
- An earlier test run failed one registry assertion because the test searched for the exact phrase `not inferred` while the source text said `is inferred`; the registry wording was clarified to `caller-supplied, not inferred`, and final exact-head checks passed.
- Exact post-merge main: Quality [43751965081], Chromium [43751965119], Pages build/deploy [43751965128] all SUCCESS, including production-site Chromium exercise and deployed-site/runtime-asset smoke.
- `KHM-ROM-PCGN-ROBAT-001` remains PARTIAL: only the `rC` component is returned with caller-supplied consonant romanization. No full syllable, IPA or Ukrainian output is produced.


## PCGN Note 7 — bounded AHSDA position effect — 2026-11-15

Implemented `resolve_pcgn_ahsda(analysis, syllable_position, series)` and exported `PCGNAhsdaDecision`.

The resolver accepts one final AHSDA mark immediately after a modeled unstacked consonant, but never infers syllable position:
- Caller-supplied `INITIAL`: the AHSDA mark itself is not romanized; the resolver returns an explicit `MARK_NOT_ROMANIZED_INITIAL` effect and no Latin component.
- Caller-supplied `FINAL`: requires an explicit `â` or `ô` series and returns that vowel component, as Note 7 specifies.

The mark's position and final series are explicit inputs. Unknown position, missing final series, multiple/misplaced marks and non-consonant attachment abstain.

Schema: `schemas/pcgn-ahsda-decision.schema.json`; tests: `tests/test_pcgn_ahsda_resolution.py`. The official examples `ស៏`, `តំណ៏`, and `ពម៏` are used only to test the stated position/series effects, not as a full romanizer.

Source: BGN/PCGN 1972, Diacritical Marks table row 5 (p. 4) and Note 7 (p. 5): https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.

Status: `KHM-ROM-PCGN-AHSDA-001 = PARTIAL`. Syllable position and series are caller-supplied; no complete syllable, IPA or Ukrainian output is produced.


## Exact-main verification — PCGN Note 7 AHSDA component / PR #237 — 2026-11-15

- PR [#237](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/237) merged by squash as `890791a1d8236180c82a39b81bd28b7f772d614c`; exact `main` verified at this SHA. No open PRs.
- Final PR-head `2e3ee353124b1a9cacac64997ceb06720a78370c`: push Quality [43752539333], PR Quality [43752551657], PR Chromium [43752551605] all SUCCESS. Quality reports 284 Python tests passed and 70 subtests passed; web checks and production build passed; Chromium visible-results smoke passed.
- Exact post-merge main: Quality [43752661403], Chromium [43752661392], Pages build/deploy [43752661369] all SUCCESS, including production-site Chromium exercise and deployed-site/runtime-asset smoke.
- `KHM-ROM-PCGN-AHSDA-001` remains PARTIAL: syllable position is caller-supplied; FINAL additionally requires explicit series. The resolver returns only the mark effect/vowel component, not a full syllable, IPA or Ukrainian output.


## PCGN Note 8 — bounded TOANDAKHIAT silent-character component — 2026-11-15

Implemented `resolve_pcgn_toandakhiat(analysis, marked_character)` and exported `PCGNToandakhiatDecision`.

The resolver requires the caller to identify the exact marked consonant grapheme. It accepts exactly one final TOANDAKHIAT mark and verifies that the supplied grapheme matches the immediately preceding modeled unstacked or subscript consonant token. On success it returns only `OMIT_MARKED_CHARACTER`; it does not romanize the marked character or the remainder of the word.

This deliberately does not infer which glyph is silent from a word-level orthographic string. Synthetic structural tests cover unstacked and subscript tokens, missing/mismatched caller identification, misplaced/multiple marks and non-consonant attachment. The guide's lexical examples are source references, not independently adjudicated pronunciation labels.

Schema: `schemas/pcgn-toandakhiat-decision.schema.json`; tests: `tests/test_pcgn_toandakhiat_resolution.py`.

Source: BGN/PCGN 1972, Diacritical Marks table row 6 (p. 4) and Note 8 (p. 5): https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.

Status: `KHM-ROM-PCGN-TOANDAKHIAT-001 = PARTIAL`. Only consonant tokens with explicit caller identification are supported; no full-word romanization, IPA or Ukrainian output is produced.


## Exact-main verification — PCGN Note 8 TOANDAKHIAT component / PR #239 — 2026-11-15

- PR [#239](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/239) merged by squash as `9c615293e3037cb0ccbd9db0820698741bbcd5cf`; exact `main` verified at this SHA. No open PRs.
- Final PR-head `e52b2d5be98a521dfa3c6dc5af846c6c79d42dce`: push Quality [43753171641], PR Quality [43753185515], PR Chromium [43753185496] all SUCCESS. Quality reports 290 Python tests passed and 70 subtests passed; web checks and production build passed; Chromium visible-results smoke passed.
- Exact post-merge main: Quality [43753327251], Chromium [43753327183], Pages build/deploy [43753327232] all SUCCESS, including production-site Chromium exercise and deployed-site/runtime-asset smoke.
- `KHM-ROM-PCGN-TOANDAKHIAT-001` remains PARTIAL: the caller must identify the exact silent consonant grapheme; the resolver returns omission only. No complete word romanization, IPA or Ukrainian output.


## PCGN Note 4 — bounded glottal-onset apostrophe component — 2026-11-15

Implemented `resolve_pcgn_glottal_onset(analysis, word_initial, followed_by_vowel_letter)` and exported `PCGNGlottalOnsetDecision`.

The resolver accepts only the standalone onset carrier `អ`, verifies its â-series using the existing Note 2–3 series resolver, and returns the apostrophe component `’`. The apostrophe is represented as optional only when both explicit caller inputs are true: the carrier is word-initial and it precedes a vowel letter. In all other supported contexts the apostrophe is required.

Schema: `schemas/pcgn-glottal-onset-decision.schema.json`; tests: `tests/test_pcgn_glottal_onset_resolution.py`.

Source: BGN/PCGN 1972, Consonant Characters row 22 and Note 4 (p. 5): https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.

Status: `KHM-ROM-PCGN-GLOTTAL-001 = PARTIAL`. Word position and following-vowel context are caller-supplied; no complete syllable, IPA or Ukrainian output is produced.


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


## BGN/PCGN Note 10 — exact romanization-letter inventory validator — 2026-11-15

Added `validate_pcgn_romanization_characters` and `PCGNRomanizationCharacterInventoryDecision` in `src/khmer_ua/pcgn_unicode.py`, exported through the package API.

The validator accepts basic ASCII Roman letters and the exact modified-letter inventory in BGN/PCGN Note 10, including both decomposed sequences `œ + U+0306` and `Œ + U+0306`. It preserves the input string and codepoint trace exactly; it performs no NFC/NFD normalization, transliteration, IPA conversion or Ukrainian adaptation. Non-letter characters are passed through and explicitly reported as outside this validator's scope. Unlisted Unicode letters/marks are returned as unsupported.

Schema: `schemas/pcgn-romanization-character-inventory-decision.schema.json`; tests: `tests/test_pcgn_romanization_character_inventory.py`. The source registry marks Note 10 `PARTIAL_CHARACTER_INVENTORY`.

Primary source: BGN/PCGN 1972 Agreement, Note 10 (p. 5): https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.

Status: `KHM-ROM-PCGN-UNICODE-001 = PARTIAL`. This is an inventory validator only; it does not generate romanization or establish any IPA/Ukrainian correspondence.


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


## BGN/PCGN vowel characters with anusvara or visarga — bounded table rows 1–8 — 2026-11-15

Implemented `resolve_pcgn_anusvara_visarga(analysis, onset_analysis, coda_character=None)` and `PCGNAnusvaraVisargaDecision` for the eight rows in the official **Vowel Characters with Anusvara or Visarga** table (p. 4).

- The resolver requires a separately supplied onset-only orthographic analysis and derives the â/ô series through the existing Notes 2–3 resolver.
- It maps only the exact source-token sequences in rows 1–8: U+17BB+U+17C6; U+17C6; U+17B6+U+17C6; U+17C7; U+17BB+U+17C7; U+17C1+U+17C7; U+17C4+U+17C7; and U+17B6+U+17C6+U+1784.
- Row 8 additionally requires the caller to identify the final `ង` coda explicitly. The function does not infer syllable boundaries or codas from a word.
- Results are typed vowel/final-component romanization only; `ipa` and `ukrainian` remain null. No complete PCGN syllable, IPA, or Ukrainian output is generated.

Artifacts: `src/khmer_ua/pcgn.py`, package exports in `src/khmer_ua/__init__.py`, schema `schemas/pcgn-anusvara-visarga-decision.schema.json`, tests `tests/test_pcgn_anusvara_visarga_resolution.py`, and auditable source table `data/khmer/romanization_pcgn_anusvara_visarga.csv`.

Primary source: BGN/PCGN 1972 Agreement, p. 4, “Vowel Characters with Anusvara or Visarga”: https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.

Status: `KHM-ROM-PCGN-ANUSVARA-VISARGA-001 = PARTIAL`; `KHM-ROM-PCGN-VOWELS-001` and `KHM-ROM-ENGINE-001` remain PARTIAL. This is not evidence of IPA or Ukrainian transcription accuracy.


## Exact-main verification — PR #249 / PCGN anusvara-visarga table — 2026-11-15

- PR [#249](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/249) merged by squash as `a50f815f993f8fa9b4ae59c5f0f89b8c7717ea6f`; exact current `main` verified at this SHA. No open PRs.
- PR-head push Quality [43760107833], PR Quality [43760141233] and PR Chromium [43760141132] all SUCCESS.
- Exact post-merge main Quality [43760241393], Chromium [43760241451] and Pages build/deploy [43760241464] all SUCCESS, including deployed-site/runtime-asset smoke.
- The implementation covers only PCGN table rows 1–8 for vowels with anusvara/visarga. Row 8 requires caller-identified final NGA; no IPA, Ukrainian output or accuracy claim.

## BGN/PCGN inherent-vowel component — table row 1 — 2026-11-15

Implemented `resolve_pcgn_inherent_vowel(analysis, syllable_position)` and `PCGNInherentVowelDecision` for the â/ô values in row 1 of the official Independent/Dependent Vowel Characters table.

- The caller must explicitly identify the cluster as `NON_FINAL`; the resolver then uses the existing Notes 2–3 series decision to return the inherent `â` or `ô` vowel component.
- `FINAL` position abstains. The guide separately says that a final consonant without a vowel character or TOANDAKHIAT should generally be romanized without a following vowel letter; that broader coda/edge rule is not inferred here.
- Only one base plus at most one modeled foot is accepted. Invalid clusters, explicit vowel signs, special marks and unresolved series abstain.
- Schema: `schemas/pcgn-inherent-vowel-decision.schema.json`; tests: `tests/test_pcgn_inherent_vowel_resolution.py`; source table: `data/khmer/romanization_pcgn_inherent_vowel.csv`; public package exports updated.

Primary source: BGN/PCGN 1972 Agreement, p. 2, Vowel Characters table row 1 and explanatory paragraph: https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.

Status: `KHM-ROM-PCGN-INHERENT-VOWEL-001 = PARTIAL`. This is an onset vowel component only; no final-coda decision, full syllable, IPA or Ukrainian output is generated.


## Exact-main verification — PR #250 / PCGN inherent vowel row 1 — 2026-11-15

- PR [#250](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/250) merged by squash as `62ce69bd17dc64fecfb73e81e22ca10bf97a25ff`; exact current `main` verified at this SHA. No open PRs.
- PR-head push Quality [43760551262], PR Quality [43760562169] and PR Chromium [43760562155] all SUCCESS.
- Exact post-merge main Quality [43760662544], Chromium [43760662582] and Pages build/deploy [43760662587] all SUCCESS, including production-site Chromium exercise and deployed-site/runtime-asset smoke.
- The inherent-vowel resolver covers only PCGN table row 1 for an explicitly caller-identified NON_FINAL onset. FINAL consonant contexts abstain. No full syllable, IPA or Ukrainian output is generated.
- Latest engineering checkpoint does not change the research gate: issue #104 remains OPEN; independent adjudicated IPA gold remains 0 and accuracy remains null. Root LICENSE is still absent and `main` remains unprotected.


## BGN/PCGN consonant table component — rows 1–21 — 2026-11-15

Implemented `resolve_pcgn_consonant(analysis)` and `PCGNConsonantDecision` for the official consonant table rows 1–21.

- The resolver maps one Unicode base consonant and at most one modeled subscript foot to their PCGN Latin consonant components.
- It derives the â/ô series using the existing Notes 2–3 resolver. For row 12, base `ប` is `b` normally and becomes `p` only when the Note 3 BA+MUUSIKATOAN, BA+TRIISAP or BA+foot exception is present; a subscript `ប` is `p`.
- Row 22 `អ` is deliberately delegated to the separate Note 4 glottal-onset resolver, which requires word-position/following-vowel context.
- One base plus one foot only. Multi-foot clusters, unknown characters, unsupported marks and unresolved series abstain. The resolver maps the supplied Unicode character identity; guide cases requiring lexical consultation remain outside this automatic subset.
- Schema: `schemas/pcgn-consonant-decision.schema.json`; tests: `tests/test_pcgn_consonant_resolution.py`; source table: `data/khmer/romanization_pcgn_consonants.csv`; package exports updated.

Primary source: BGN/PCGN 1972 Agreement, Consonant Characters and Subscript Consonant Forms table (pp. 1–2), Note 3 and note following the table: https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.

Status: `KHM-ROM-PCGN-CONSONANTS-001 = PARTIAL`. This is an onset-cluster component only; it does not segment syllables, map vowels/codas, emit IPA or produce Ukrainian output.


## Exact-main verification — PR #251 documentation closeout — 2026-11-15

- PR [#251](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/251) merged as `aab014705bdf90825b922ff69f1c2e7758e56246`; exact `main` verified at this SHA. No open PRs.
- PR-head push Quality [43760857888], PR Quality [43760868532] and PR Chromium [43760868545] all SUCCESS.
- Exact post-merge main Quality [43760984773], Chromium [43760984785] and Pages build/deploy [43760984838] all SUCCESS, including deployed-site/runtime-asset smoke.
- PR #251 was documentation-only and did not promote any linguistic status.


## Exact-main verification — PR #252 / PCGN consonant table rows 1–21 — 2026-11-15

- PR [#252](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/252) merged by squash as `16fbbde6238e03290507056388b539f54622d236`; exact current `main` verified at this SHA. No open PRs.
- Final PR-head push Quality [43761467383], PR Quality [43761473221] and PR Chromium [43761473212] all SUCCESS.
- Exact post-merge main Quality [43761598283], Chromium [43761598359] and Pages build/deploy [43761598332] all SUCCESS, including production-site Chromium exercise and deployed-site/runtime-asset smoke.
- An earlier pre-fix push Quality run [43761223088] failed because the new consonant-decision JSON schema contained malformed JSON. The schema was corrected, parsed successfully, and the final exact PR-head and main checks passed. The CSV row-12 default was also corrected to keep `b` separate from its Note 3 `p` exception.
- The resolver covers rows 1–21 only; row 22 remains delegated to Note 4. It emits onset consonant components only, not a full syllable, IPA or Ukrainian output.


## Exact-main verification — PR #253 / consonant-table verification record — 2026-11-15

- PR [#253](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/253) merged as `df63d6bb94f19d0772c4051d8d27f117a2d6eaf2`; exact mainline CI passed.
- PR-head push Quality [43761762695], PR Quality [43761775856] and PR Chromium [43761775796] all SUCCESS.
- Exact post-merge main Quality [43761865853], Chromium [43761865900] and Pages build/deploy [43761865852] all SUCCESS, including deployed-site/runtime-asset smoke.
- Documentation-only closeout; no linguistic status promotion.

## BGN/PCGN final-consonant no-following-vowel rule — bounded component — 2026-11-15

Implemented `resolve_pcgn_final_consonant(analysis, has_following_vowel_character, has_toandakhiat)` and `PCGNFinalConsonantDecision` for the guide's general rule: a syllable-final consonant not accompanied by a vowel character or TOANDAKHIAT should generally be romanized without a vowel letter following.

- The caller must isolate the final consonant chunk and explicitly confirm both context conditions are false.
- The resolver maps one base plus at most one foot using the PCGN consonant table and returns the consonant component with `following_vowel=""`.
- BA and ALIF final cases abstain because their special Note 3/4 contexts are not resolved by this general rule. Other marks, vowel-bearing forms, multiple bases/feet and unsupported structures also abstain.
- The source says “generally”; the result is labelled `GENERAL_RULE_APPLIED`, not an absolute phonological law.

Artifacts: `schemas/pcgn-final-consonant-decision.schema.json`, `tests/test_pcgn_final_consonant_resolution.py`, `data/khmer/romanization_pcgn_final_consonant.csv`, and public exports in `src/khmer_ua/__init__.py`.

Primary source: BGN/PCGN 1972 Agreement, p. 2, explanatory paragraph following the vowel table: https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.

Status: `KHM-ROM-PCGN-FINAL-CONSONANT-001 = PARTIAL`. No syllable segmentation, complete PCGN word, IPA or Ukrainian output is generated.


## PR #255 closeout — PCGN final-consonant context contract — 2026-11-16

- PR [#255](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/255) merged by squash as `47679154526fa32c5edd9d62ca084de5af4759dd`; exact current `main` verified at this SHA. No open PRs.
- PR-head `8a9056d4b4a9909ee1e46bee62a0d87ab6d06090`: push Quality [43825412435], PR Quality [43825430244] and Chromium [43825430217] all SUCCESS.
- Exact post-merge main: Quality [43825536547], Chromium [43825536580], Pages build/deploy [43825536491] all SUCCESS. Pages included production-site Chromium exercise and deployed-site/runtime-asset smoke.
- The final-consonant resolver now raises `TypeError` unless both caller-supplied context flags are actual booleans; it no longer accepts `None`, numeric or string lookalikes as negative evidence. Regression coverage iterates every supported base character, excluding BA/ALIF which intentionally abstain under the generic rule.
- Scope remains a bounded PCGN component. No syllable segmentation, complete PCGN output, IPA/Ukrainian output or accuracy claim was added. `KHM-ROM-PCGN-FINAL-CONSONANT-001` and `KHM-ROM-ENGINE-001` remain PARTIAL.
- External gate unchanged: issue #104 remains OPEN; independent adjudicated IPA gold remains 0 and accuracy remains null. Root `LICENSE` remains absent; no license choice is made here.


## Documentation closeout — PR #256 — 2026-11-16

- PR [#256](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/256) merged by squash as `dee4881da4cfb01b6da0ff5e857af67cade14cb1`; exact current `main` verified at this SHA. No open PRs.
- PR-head `be23692a11c716e5022e11f6af092bf38b05157b`: push Quality [43825693046], PR Quality [43825710166] and Chromium [43825710160] all SUCCESS.
- Exact post-merge main: Quality [43825806168], Chromium [43825806361] and Pages build/deploy [43825806234] all SUCCESS. Pages included production-site Chromium exercise and deployed-site/runtime-asset smoke.
- Exact-main Quality log: `pytest -q` — 331 passed, 70 subtests passed; `npm run check` and production build passed. The separate Chromium smoke and Pages deployment also passed.
- PR #256 is documentation-only. PR #255's context-type hardening remains an engineering-only improvement; `KHM-ROM-PCGN-FINAL-CONSONANT-001` and `KHM-ROM-ENGINE-001` remain PARTIAL.
- Research gate remains unchanged: issue #104 OPEN, independent adjudicated IPA gold = 0, accuracy = null. Root `LICENSE` is still absent.


## PCGN independent-vowel source registry — 2026-11-16

- Added `data/khmer/romanization_pcgn_independent_vowels.csv` for the exact independent-character rows present in the BGN/PCGN 1972 table: 3, 4, 7, and 14–22.
- Row 7 `ឧ` remains explicitly UNRESOLVED with both source alternatives `ŏ|ŭ`; no lexical/reference selection is made.
- Each row records the table row, source character(s), romanization or alternatives, acceptance boundary, exact page locator and official primary-source URL.
- Added a regression check that the source registry matches `PCGN_INDEPENDENT_VOWEL_ROWS` exactly and preserves the Note 9 ambiguity. No runtime mapping changed; no IPA/Ukrainian output or accuracy claim is added.
- `KHM-ROM-PCGN-INDEPENDENT-VOWELS-001` and `KHM-ROM-ENGINE-001` remain PARTIAL.


## PR #259 closeout — PCGN independent-vowel source register — 2026-11-16

- PR [#259](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/259) merged by squash as `458026f080bca31edeec87c2009245213ab667c7`; exact current `main` verified at this SHA. No open PRs.
- PR-head `e9ced1775d4382a2a7be3bcbc01c5c51c0b34a2f`: push Quality [43826670914], PR Quality [43826697643], Chromium [43826697687] all SUCCESS.
- Exact post-merge main: Quality [43826837012], Chromium [43826837160] and Pages build/deploy [43826837175] all SUCCESS. Pages included production-site Chromium exercise and deployed-site/runtime-asset smoke.
- Exact-main Quality log: `pytest -q` — 332 passed, 70 subtests passed; `npm run check` and production build passed.
- The CSV is a source/evidence register, not a runtime mapping change. Note 9 `ឧ` remains unresolved with alternatives `ŏ`/`ŭ`. `KHM-ROM-PCGN-INDEPENDENT-VOWELS-001` and `KHM-ROM-ENGINE-001` remain PARTIAL.
- The earlier PR #258 was closed without merge because its branch had a stale-base documentation conflict after PR #257; the changes were preserved on a clean branch and merged as PR #259.


## Current repository continuation checkpoint — 2026-11-16

- Live `main` at inspection: `2e005a3e804e878deb66007d857d2d9361c8e4de` (PR #259 exact-main documentation closeout).
- Open PRs: **0**. Exact-main Quality [43827176347](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43827176347), Chromium [43827176391](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43827176391), and Pages deployment [43827176423](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43827176423) all SUCCESS on that exact SHA.
- GitHub branch listing returns 125 refs across two pages: `main` plus 124 non-main historical/task refs. This count is a ref inventory, not a claim that 124 branches are independently mergeable or all contain unique work.
- Sampled branch comparisons against live `main` show divergent historical snapshots, not clean integration candidates. Examples: `feat/pcgn-note2-shifter-resolution-2026-11-15` is 16 ahead/43 behind; `feat/khmer-ukrainian-practical-adapter-verified-2026-11-11` is 29 ahead/109 behind; `feat/typed-ipa-hybrid-bridge-2026-11-15` is 10 ahead/75 behind; `docs/repository-information-architecture-2026-11-15` is 4 ahead/86 behind; and the independent-vowel source-register branch is 12 ahead/3 behind after its work was integrated via PR #259. These tips must not be merged wholesale. The previous historical-branch audit records prior PR integration/supersession; the current sample confirms the same caution still applies.
- No open PRs remain. The active continuation branch for this inventory update is `audit/current-branch-inventory-2026-11-16`; future work should branch from current `main` and use one active task branch at a time.
- The connected GitHub operations available here do not expose branch deletion. No historical branch refs were deleted or force-updated; doing so is not required to keep the source-of-truth execution line on `main`.
- Human research blocker remains unchanged: issue [#104](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/104) is OPEN. IPA gold remains empty (0 independently adjudicated items), accuracy remains null. Expert-approved IPA convention, two qualified annotators, independent adjudicator, curator, blind intake, rights-cleared 30 lexeme groups and completed double annotation/adjudication require real human participation. Do not fabricate or automate these gates.
- Release characterization remains **research foundation + local web service / partial prototype**, not linguistically release-ready. Root `LICENSE` absence vs MIT metadata and unprotected `main` remain owner-level decisions; no settings were changed.


## Exact-main continuation checkpoint — 2026-11-16 12:13 UTC+02:00

This checkpoint supersedes earlier main-SHA and branch-inventory snapshots in this handoff.

- Current default branch: `main` at `46a54d9ce86916af2d18a2322167798d43bce6c8` (PR #261 merged). Open PRs: 0.
- Exact-main GitHub Actions: Quality [43841825031](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43841825031), Khmer browser smoke [43841825019](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43841825019), and Pages build/deploy [43841825034](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43841825034) all SUCCESS on this exact SHA. Quality reports 332 Python tests and 70 subtests; web checks and production build passed. Browser and deployed-site/runtime-asset smoke passed. These are hosted CI results; no local checkout or local test execution is claimed.
- The previous inventory found 125 branch refs (main + 124 non-main). Sampled divergent historical tips were not merged wholesale. The sole integration base remains current `main`; keep one active task branch/PR at a time. Branch deletion is not exposed by the connected GitHub operations, so historical refs remain untouched.
- **Engineering ledger:** CI/site pipeline and existing bounded components are `DONE_VERIFIED` as engineering artifacts only; full PCGN word/syllable segmentation and assembly are `PARTIAL`; full source-orthography → IPA phonology and profile-conditioned vowel/coda coverage are `PARTIAL`; IPA → Ukrainian target policy is implemented but remains project-proposed, not a normative standard; independent expert-adjudicated IPA gold and empirical accuracy are `BLOCKED` (gold count 0; accuracy null); the complete historical branch audit remains `PARTIAL` (inventory and selected comparisons only).
- **PCGN component boundary:** source-backed bounded resolvers exist for consonants, series/shifters, normal and special vowels, shortening, final consonants, ROBAT, AHSDA, TOANDAKHIAT, glottal onset and Note 10 character validation. They intentionally return component decisions and abstain where context is absent. They do not constitute a full PCGN syllable/word romanizer and must not be described as one.
- **Human research gate:** issue [#104](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/104) remains OPEN. Outstanding: expert-approved versioned IPA convention; two qualified independent Khmer annotators; a third independent adjudicator; separate curator; private blind intake; 30 rights-cleared, source-located lexeme groups; locked double annotations; evidence-based adjudication; provenance/rights/schema/blindness validation. No annotations, recruitment or adjudication are claimed.
- **Owner decisions:** root `LICENSE` remains absent despite package/repository metadata indicating MIT; no license was selected. `main` protection remains an owner-level setting; no settings were changed. These are not silently resolved by CI.
- **Next dependency order:** (1) obtain the human convention and recruitment/intake decisions in issue #104; (2) acquire and adjudicate the rights-cleared pilot without leaking held-out items; (3) only then report empirical agreement/accuracy and use gold to validate phonological rules; (4) independently complete the evidence-backed PCGN syllable assembler and its orthographic Ukrainian crosswalk, keeping it separate from IPA transcription; (5) reconcile license metadata and branch protection with the repository owner.
- Readiness: research foundation + deployed engineering prototype; **not linguistically release-ready**. Green CI proves software/deployment checks, not Khmer phonological correctness.


## Live-main refresh after PR #262 — 2026-11-16

- Current `main`: `17657f91f650e4e5f2213bc3546eaefcb7c95202`. PR [#262](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/262) is merged; open PR count is 0.
- Exact-main Quality [43847284065](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43847284065), Khmer browser smoke [43847284004](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43847284004), and Pages build/deploy [43847283928](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43847283928) all completed SUCCESS on this SHA. Quality steps for corpus structure validation, Python tests, web checks and site build passed; Chromium visible-result smoke and Pages deployment completed successfully. These are hosted CI checks, not local test executions.
- Fresh GitHub branch listing: 127 refs total = `main` + 126 non-main refs. All 126 non-main tips had distinct SHAs in the listing. This is a ref inventory only; it is not a full ancestry/content audit and does not imply those tips should be merged. A systematic compare of all 126 refs was not completed in this run; branch-audit status remains PARTIAL. Historical refs are preserved.
- Issue [#104](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/104) remains OPEN (last updated 2026-11-04). The convention sheet, two annotators, independent adjudicator, curator, blind intake and rights-cleared 30-item pilot remain unconfirmed. The corpus remains intentionally empty; accuracy remains unavailable. This is a human research dependency, not a CI defect.
- This checkpoint supersedes earlier branch-count and main-SHA snapshots above. It does not change any linguistic acceptance status. Readiness remains research foundation + deployed engineering prototype, not linguistically release-ready.


## Continuation checkpoint — explicit PCGN open-CV assembly — 2026-11-16

- Base `main`: `956d9a56be2f8d961eb77d194ff5fd61fc4b5b5e`. Dedicated branch: `feat/pcgn-explicit-open-syllable-assembly-2026-11-16`.
- Added `assemble_pcgn_open_syllable` in `src/khmer_ua/pcgn.py`. It joins the existing bounded consonant-onset and dependent-vowel resolvers only when the caller supplies matching onset and complete open-syllable chunks. It verifies the token-prefix relationship and refuses coda-bearing, shortened, independent-vowel, special-mark, Alif, malformed and ambiguous inputs.
- Added JSON Schema `schemas/pcgn-syllable-assembly.schema.json` and focused regression tests `tests/test_pcgn_syllable_assembly.py`. Updated the romanization matrix and linguistic completion register with the bounded scope and source citation.
- Output is BGN/PCGN orthographic Latin only. IPA and Ukrainian remain null; the existing IPA-first engine was not changed. No word segmentation, coda rules, empirical claims, IPA labels or gold records were introduced.
- Exact PR-head hosted verification on `fcc8bf68aff1634eb5a66955099419e98c98a47f`: Quality [43880147090](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43880147090) SUCCESS (338 Python tests + 70 subtests; JSON corpus validation, web checks and production build passed); Chromium [43880147081](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43880147081) SUCCESS; push Quality [43880136584](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43880136584) SUCCESS. The initial test expectations incorrectly assigned the PCGN series for `ថ្ម`; CI exposed this, the expected outputs were corrected against the existing Note 2–3 resolver, and the final exact-head runs passed.
- PR [#264](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/264) squash-merged as `231b8f031ae130828018b18dbdf1c36c6ac47e6a`. The documentation closeout brought exact `main` to `5c17d9b1b0d1bbfc079b6d5811749488ca3daad1`. On that exact SHA, Quality [43880417655](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43880417655), Chromium [43880417532](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43880417532), and Pages build/deploy plus deployed-site/runtime smoke [43880417474](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43880417474) all SUCCESS. Exact-main Quality reports 338 Python tests + 70 subtests passed; web checks, production build and browser smoke passed. No local checkout or local test execution is claimed.
- `KHM-ROM-PCGN-OPEN-CV-001` is DONE_VERIFIED for the bounded explicit open-CV API. `KHM-ROM-ENGINE-001` remains PARTIAL because general syllable parsing, codas and whole-word PCGN output remain incomplete.


## Continuation checkpoint — PCGN Note 5 closed-syllable assembly — 2026-11-16

- Base main at branch creation: `cc13cde53ab1224d6782528591c0a722f80cca77`. Dedicated branch: `feat/pcgn-shortened-closed-syllable-assembly-2026-11-16`.
- Added `assemble_pcgn_shortened_closed_syllable` in `src/khmer_ua/pcgn.py`. It composes existing PCGN onset, Note 5 shortened-vowel and final-consonant resolvers for the three exact Note 5 patterns. Caller-supplied onset/full/coda chunks are cross-checked; caller-supplied coda class is checked against the final consonant's resolved PCGN Latin value before the vowel variant is accepted.
- Added `schemas/pcgn-closed-syllable-assembly.schema.json` and focused tests `tests/test_pcgn_closed_syllable_assembly.py`; updated the matrix and completion register.
- Output is orthographic BGN/PCGN Latin only; IPA and Ukrainian remain null. No automatic syllable/word segmentation, general coda support, phonetic mapping, gold labels or accuracy claims are added. The existing IPA-first engine is unchanged.
- Exact PR-head verification on `027671a579b2b3e210a1c285f412516e6b3772f4`: Quality [43881403475](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43881403475) and Chromium [43881403279](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43881403279) SUCCESS; push Quality [43881383045](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43881383045) SUCCESS (342 Python tests + 70 subtests). PR [#265](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/265) merged as `664c210d957b0666e5ca85032fb49466018cbf78`. Exact-main Quality [43881564395](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43881564395), Chromium [43881564314](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43881564314), and Pages build/deploy [43881564668](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43881564668) all SUCCESS. No local checkout or local test execution is claimed.
- Acceptance is DONE_VERIFIED only for the exact three Note 5 patterns and a single supported final consonant; `KHM-ROM-ENGINE-001` remains PARTIAL.


## Continuation checkpoint — normal dependent-vowel closed-syllable assembly — 2026-11-16

- Base main at branch creation: `664c210d957b0666e5ca85032fb49466018cbf78`. Dedicated branch: `feat/pcgn-normal-dependent-closed-syllable-assembly-2026-11-16`.
- Added `assemble_pcgn_dependent_closed_syllable` in `src/khmer_ua/pcgn.py`. It composes existing series, onset, ordinary dependent-vowel and final-consonant resolvers for explicitly caller-segmented onset + vowel + coda chunks. The implementation verifies that onset and vowel chunks are exact token prefixes of the complete syllable and that the caller's coda is its final token.
- Added `schemas/pcgn-dependent-closed-syllable-assembly.schema.json` and `tests/test_pcgn_dependent_closed_syllable_assembly.py`. The tests exercise all 17 normal dependent-vowel patterns in both â/ô series with a caller-supplied final coda, plus boundary and abstention cases.
- Output remains orthographic BGN/PCGN Latin only; IPA and Ukrainian remain null. No word/syllable segmentation is inferred. Shortened/independent vowels and special marks abstain. The IPA-first engine is unchanged.
- Exact PR-head verification on `6430c271abe1c69a1ed0e533de6cf95f88a98a4a`: Quality [43882269923](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43882269923) and Chromium [43882269991](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43882269991) SUCCESS; push Quality [43882139617](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43882139617) SUCCESS (347 Python tests + 70 subtests). PR [#266](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/266) merged as `84880d6c241bfc22e8e095a7cb90f2d32759ced1`. Exact-main documentation closeout SHA `8df4f5ca146f82d6f8c3892ae686f6f58f7bbaeb` passed Quality [43882558236](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43882558236), Chromium [43882558488](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43882558488), and Pages build/deploy plus deployed-site/runtime smoke [43882558294](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43882558294). Exact-main Quality reports 347 Python tests + 70 subtests passed; web checks, production build and Chromium smoke passed. No local checkout or local test execution is claimed. `KHM-ROM-ENGINE-001` remains PARTIAL.


## Historical branch ancestry inventory closeout — 2026-11-16

- Exact main used for comparison: `44c2168e9b4a3f818ad2259f663792a4fc86229b`.
- Live branch listing: 131 refs total (main + 130 non-main), all non-main tips unique. Systematically compared all 130 non-main refs against exact main; open PR count 0.
- Most historical refs are divergent because of squash merges and retained task snapshots. File-level summaries plus representative content checks found older PCGN, direct-romanization, mixed-script, practical-adapter, coverage and external-IPA branches to be already integrated or stale. The independent-vowel CSV and several test/source files are byte-identical to main. No historical ref was force-updated, deleted or merged wholesale.
- `KHM-BRANCH-AUDIT-001`: ancestry inventory DONE_VERIFIED; complete changed-file and PR-ancestry reconciliation remains PARTIAL. Preserve refs until the owner chooses an archival policy; branch deletion is not exposed by the connected GitHub operations.


## Final continuation closeout — 2026-11-16

- Final verified baseline before this closeout note: `main` `7a8c1b263ec1e8fa5a8a1395908c661ed5311d42`.
- PR #264 (open-CV assembler), #265 (Note 5 shortened closed syllables), and #266 (normal dependent-vowel closed syllables) are merged. No open PRs.
- Exact-main Quality [43884065012](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43884065012), Chromium [43884065118](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43884065118), and Pages build/deploy plus deployed-site/runtime smoke [43884065234](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43884065234) all SUCCESS on `7a8c1b263ec1e8fa5a8a1395908c661ed5311d42`. Quality: 347 Python tests + 70 subtests; web checks and production build passed. Browser smoke: 11/11 passed. Pages deployment and runtime asset smoke passed.
- Historical refs: 131 total (main + 130 non-main), 130/130 ancestry comparisons completed, 130 unique non-main tips, zero open PRs. Full content-level review remains PARTIAL; no historical branch was force-updated, deleted or merged wholesale.
- Linguistic status remains partial prototype: full Khmer syllable/word segmentation and source→IPA phonology are incomplete. Issue #104 is still the hard human blocker: independent expert convention, two annotators, adjudicator, curator, blind intake and 30 rights-cleared lexeme groups. Gold remains 0; accuracy remains null.
- Owner blockers remain: root `LICENSE` absent despite MIT metadata, and branch protection configuration. Neither was changed. No local checkout or local test execution is claimed; all verification above is hosted GitHub Actions evidence.


## Continuation — bounded PCGN Note 4 Alif open-syllable assembly — 2026-11-16

- Base main: 9ba7b97e6d56f75166533f6978cc9586f718c234. Dedicated branch: feat/pcgn-glottal-open-syllable-assembly-2026-11-16.
- Added assemble_pcgn_glottal_open_syllable to compose the existing Note 4 Alif carrier resolver and A-series dependent-vowel resolver for a caller-supplied standalone អ onset plus one open-syllable chunk. It checks exact onset token prefix and permits only the existing supported dependent-vowel token patterns.
- Both Note 4 context flags (word_initial, followed_by_vowel_letter) remain mandatory explicit booleans. Where Note 4 allows an optional apostrophe, both full PCGN spellings are preserved in romanization_options; the implementation does not silently choose the apostrophe-free variant.
- Added schema schemas/pcgn-glottal-open-syllable-assembly.schema.json, tests tests/test_pcgn_glottal_open_syllable_assembly.py, and package exports. Tests exercise all current normal dependent-vowel patterns in the A-series plus boundary/abstention cases.
- Output is bounded BGN/PCGN orthographic Latin only; IPA and Ukrainian remain null. No word segmentation, independent-vowel selection, coda inference, phonetic rule or gold data was added. The IPA-first runtime remains separate.
- PR #267 squash-merged as 6df8c6c176e0098f97a9f4ab1f9583b0bb7caa68. Exact PR-head Quality [43888596780] and Chromium [43888596962] passed on cd1c6fcb33d93e0b1ef0e508207d8139d5d17eb1: 354 Python tests + 70 subtests, JSON corpus validation, web checks, production build and visible-results Chromium smoke all passed. Exact-main Quality [43888801455], Chromium [43888801448], and Pages build/deploy/runtime smoke [43888801373] all SUCCESS on 6df8c6c176e0098f97a9f4ab1f9583b0bb7caa68.
- KHM-ROM-PCGN-ALIF-ASSEMBLY-001 is DONE_VERIFIED for this bounded Note 4 open-syllable API. KHM-ROM-ENGINE-001 remains PARTIAL; no full segmentation or whole-word romanizer is claimed. All verification is hosted GitHub Actions; no local checkout/test run is claimed.

## Exact-main checkpoint after PR #267 — 2026-11-16

- Main: 6df8c6c176e0098f97a9f4ab1f9583b0bb7caa68. PR #267 merged; exact-main Quality [43888801455], Chromium [43888801448], and Pages build/deploy with deployed-site/runtime smoke [43888801373] all SUCCESS. Quality: 354 Python tests + 70 subtests; browser visible-results smoke and deployed runtime smoke passed.
- Open PRs at this checkpoint: 0. Issue #104 remains OPEN; independent adjudicated IPA gold remains 0 and empirical accuracy remains null. Root LICENSE/MIT metadata and branch protection remain owner-level blockers. Repository readiness remains research foundation + deployed engineering prototype, not linguistically release-ready.


## Continuation — bounded PCGN Note 4 Alif dependent-vowel closed syllable — 2026-11-16

- Base main: 52baf5b9a26d8b2054afd9519f2b4187a114ec52. Dedicated branch: feat/pcgn-alif-dependent-closed-syllable-assembly-2026-11-16.
- Added assemble_pcgn_glottal_dependent_closed_syllable to compose the existing Note 4 Alif carrier, A-series normal dependent-vowel, and general final-consonant resolvers for a caller-supplied onset + vowel + one-consonant coda.
- Caller supplies onset-only, onset-plus-vowel, full-syllable, and coda-only chunks plus explicit Note 4 context booleans. Exact token boundaries and component identities are checked; unsupported final contexts abstain. Optional apostrophe spelling is retained as an explicit full-output alternative.
- Added strict schema, focused tests covering every normal dependent-vowel table pattern with a supported coda, package exports and documentation updates. IPA/Ukrainian remain null; no segmentation, coda guessing or phonetic rule is added.
- PR #269 squash-merged as 482ed151dc99d3fd20714a606c9ad25aa209a99e. Exact PR-head Quality [43889912149] and Chromium [43889912018] passed on d975ca398c42dfe5669b770f9529bbcffda79160: 360 Python tests + 70 subtests, JSON corpus validation, web checks, production build and visible-results Chromium smoke all passed. Exact-main Quality [43890093477], Chromium [43890093456], and Pages build/deploy/runtime smoke [43890093482] all SUCCESS on 482ed151dc99d3fd20714a606c9ad25aa209a99e.
- KHM-ROM-PCGN-ALIF-CLOSED-001 is DONE_VERIFIED for this bounded caller-segmented normal dependent-vowel + one supported coda API. KHM-ROM-ENGINE-001 remains PARTIAL. Hosted GitHub Actions only; no local test execution is claimed.

## Exact-main checkpoint after PR #269 — 2026-11-16

- Main: 482ed151dc99d3fd20714a606c9ad25aa209a99e. PR #269 merged; exact-main Quality [43890093477], Chromium [43890093456], and Pages build/deploy with deployed-site/runtime smoke [43890093482] all SUCCESS. Quality: 360 Python tests + 70 subtests; browser visible-results and deployed runtime smoke passed.
- PR #267 (Alif open-syllable adapter) and PR #269 (Alif normal dependent closed-syllable adapter) are merged. Issue #104 remains OPEN; independent adjudicated IPA gold remains 0 and empirical accuracy remains null. Readiness remains engineering/research prototype, not linguistically release-ready.


## Continuation — bounded PCGN Note 4 + Note 5 Alif shortened closed syllables — 2026-11-16

- Base main: 977286115e0e3e7e2325010c9c0a3d08a959b710. Dedicated branch: feat/pcgn-alif-shortened-closed-syllable-assembly-2026-11-16.
- Added assemble_pcgn_glottal_shortened_closed_syllable to compose the existing Note 4 Alif carrier, Note 5 shortened-vowel resolver and general final-consonant resolver for the three exact Note 5 shapes: inherent+BANTOC, AA+BANTOC and SAMYOK+coda.
- Caller supplies the Alif onset, full syllable, coda-only chunk, coda class and explicit Note 4 context booleans. Exact coda token, final-consonant romanization and coda class are cross-checked. Optional apostrophe spelling is retained as a full-output alternative.
- Added strict schema, regression tests for all three Note 5 shapes and abstention cases, package exports and documentation. Orthographic PCGN Latin only; IPA/Ukrainian remain null.
- PR #271 squash-merged as 9957081db4149ff316695273d8dd525985bd34fd. Exact PR-head Quality [43891125460] and Chromium [43891125490] passed on 43d25e026da0ed22ffcb62ec8e810e28e302d5b3: 368 Python tests + 70 subtests, corpus validation, web checks, production build and visible-results Chromium smoke all passed. Exact-main Quality [43891297907], Chromium [43891298013], and Pages build/deploy/runtime smoke [43891297884] all SUCCESS on 9957081db4149ff316695273d8dd525985bd34fd.
- KHM-ROM-PCGN-ALIF-NOTE5-001 is DONE_VERIFIED for the three exact Note 5 patterns with one supported coda and explicit Note 4 context. KHM-ROM-ENGINE-001 remains PARTIAL. Hosted GitHub Actions only; no local test execution is claimed.

## Exact-main checkpoint after PR #271 — 2026-11-16

- Main: 9957081db4149ff316695273d8dd525985bd34fd. PR #271 merged; exact-main Quality [43891297907], Chromium [43891298013], and Pages build/deploy with deployed-site/runtime smoke [43891297884] all SUCCESS. Quality: 368 Python tests + 70 subtests; browser visible-results and deployed runtime smoke passed.
- PR #267, #269 and #271 now cover bounded Note 4 Alif open-CV, ordinary dependent-vowel closed, and Note 5 shortened closed forms. General segmentation, broader codas and full word romanization remain PARTIAL.


## Continuation — bounded PCGN Note 6 ROBAT closed-syllable assembly — 2026-11-16

- Base main: 268be193eb7af2be19740ec3bd0c3dbffd4582f1. Dedicated branch: feat/pcgn-robat-closed-syllable-assembly-2026-11-16.
- Added assemble_pcgn_robat_closed_syllable to compose an explicitly supplied onset, inherent or ordinary dependent vowel, and final consonant bearing ROBAT. It derives the marked coda's PCGN consonant component from a separate bare-coda chunk and composes the existing Note 6 r+C resolver.
- Exact onset/vowel/syllable/coda/bare-coda token relationships are checked. The official Note 6 example (ធម៌ → thôrm) and one dependent-vowel case are covered. This does not infer syllable or word boundaries.
- Added strict schema, focused tests, package exports and project records. Orthographic PCGN Latin only; IPA/Ukrainian remain null.
- PR #273 squash-merged as 4fee1db13201b9e171b08daa1d4a45f73a396b86. Exact PR-head Quality [43892380539] and Chromium [43892380533] passed on e20241966e77957988ecccf72374b51dfd38b736: 372 Python tests + 70 subtests, corpus validation, web checks, production build and visible-results Chromium smoke all passed. Exact-main Quality [43892575946], Chromium [43892575968], and Pages build/deploy/runtime smoke [43892575864] all SUCCESS on 4fee1db13201b9e171b08daa1d4a45f73a396b86.
- KHM-ROM-PCGN-ROBAT-ASSEMBLY-001 is DONE_VERIFIED for the bounded caller-segmented inherent/ordinary-dependent vowel + final ROBAT coda API. KHM-ROM-ENGINE-001 remains PARTIAL. Hosted GitHub Actions only; no local test execution is claimed.

## Exact-main checkpoint after PR #273 — 2026-11-16

- Main: 4fee1db13201b9e171b08daa1d4a45f73a396b86. PR #273 merged; exact-main Quality [43892575946], Chromium [43892575968], and Pages build/deploy with deployed-site/runtime smoke [43892575864] all SUCCESS. Quality: 372 Python tests + 70 subtests; browser visible-results and deployed runtime smoke passed.
- Bounded Note 4 Alif and Note 5 assemblies remain separate from IPA transcription. Note 6 ROBAT composition now has a bounded whole-syllable API for explicit caller-supplied chunks. General segmentation and whole-word PCGN output remain incomplete.


## Continuation — bounded PCGN independent-vowel closed-syllable assembly — 2026-11-16

- Base main: a9ef890bca4b68fcf319a089157309680b0a9e45. Dedicated branch: feat/pcgn-independent-vowel-closed-syllable-assembly-2026-11-16.
- Added assemble_pcgn_independent_vowel_closed_syllable to compose one listed independent-vowel component with one final consonant under the existing generic PCGN no-following-vowel/no-TOANDAKHIAT rule.
- Caller supplies the independent-vowel-only chunk, complete syllable chunk and coda-only chunk. Exact token prefix/suffix and component identities are validated; no segmentation is inferred. All currently mapped independent vowels are tested with a supported coda. Note 9 ឧ remains unresolved and retains its explicit ŏ/ŭ alternatives.
- Added strict schema, focused tests, package exports and in-place project records. Orthographic PCGN Latin only; IPA/Ukrainian remain null. Hosted CI pending.


## Exact-main checkpoint after PR #275 — 2026-11-16

- Main: 0e408e4d2ce18228e7b8327ddc71af5bdb302f72. PR #275 merged; exact PR-head Quality [43910476719] and Chromium [43910476885] passed on f0385ec3846f5ce2a4616f2c65e06142c20e6fe2 (377 Python tests + 70 subtests). Exact-main Quality [43910647111], Chromium [43910647145], and Pages build/deploy/runtime smoke [43910647200] all SUCCESS.
- KHM-ROM-PCGN-INDEPENDENT-CLOSED-001 is DONE_VERIFIED for the bounded listed independent-vowel + one supported final-coda API. Note 9 ឧ remains unresolved with ŏ/ŭ alternatives. KHM-ROM-ENGINE-001 remains PARTIAL: no general word/syllable segmentation, complete PCGN word romanizer or full phonological IPA coverage is claimed.
- Issue #104 remains OPEN; independent adjudicated IPA gold remains 0 and empirical accuracy remains null. Root LICENSE/MIT metadata and main branch protection remain owner-level blockers. Readiness remains research foundation + deployed engineering prototype, not linguistically release-ready. Hosted GitHub Actions only; no local checkout/test execution claimed.


## Exact-main checkpoint — 2026-11-16 evening

- Main: `0c74b5cbc55b269156a15a4694b8f8f2149b78c1` (`docs: verify independent-vowel syllable assembly`). Latest exact-main hosted runs: Quality [43911193804], Chromium [43911193963], and Pages build/deploy/deployed-runtime smoke [43911194149] all SUCCESS. Quality reports 377 Python tests + 70 subtests; corpus validation, web checks, production build and browser checks completed successfully. No local checkout or local tests are claimed.
- PR #269's Alif + ordinary dependent-vowel closed-syllable API remains DONE_VERIFIED at merge `482ed151dc99d3fd20714a606c9ad25aa209a99e`; its exact-main Quality [43890093477], Chromium [43890093456] and Pages/runtime [43890093482] all passed. Later merged work and current main are not regressed by that bounded feature.
- Current open PR count: 0. Issue #104 remains OPEN and is the hard human research gate: convention approval, two independent Khmer annotators, adjudicator, curator, blind intake, rights-cleared 30-item lexeme pilot, independent annotation/adjudication. Gold remains empty; empirical accuracy remains null.
- Engineering status remains partial: bounded PCGN component/syllable adapters are verified individually, but general syllable/word segmentation, complete PCGN word romanization, complete source-phonology-to-IPA coverage and independently reviewed Ukrainian target validation are not complete. Root LICENSE/pyproject MIT reconciliation, branch protection and manual accessibility review remain governance/owner tasks.
- Readiness: research foundation + deployed engineering prototype; not linguistically validated or production-ready. Hosted GitHub Actions only.


## LOC word-division evidence checkpoint — 2026-11-16

- Current main base: `61371ea27d7fce63add2070792d60195f0850e35`. Dedicated research branch: `research/loc-khmer-word-division-2026-11-16`.
- Primary-source reconciliation: LOC 1989 Khmer Note 10 and ALA-LC 1997 Note 10 use the shortest written form that can stand alone; ALA-LC 2013 Note 8 instead says any word can be separated when romanizing. Both distinguish Pali/Sanskrit from other loan-words, whose original-language divisions are retained. BGN/PCGN 1972 Note 9 is a separate ŏ/ŭ independent-vowel ambiguity.
- Added a dedicated evidence/acceptance audit and source-registry records. No runtime segmentation, syllable parsing, IPA, Ukrainian output, corpus or accuracy claims were changed.
- `KHM-ROM-LOC-WORD-DIVISION-EVIDENCE-001` = DONE_VERIFIED (primary-source comparison only). `KHM-ROM-LOC-WORD-SEGMENTATION-001` = BLOCKED/TODO pending explicit profile selection, licensed lexical evidence, loan-word metadata and independent boundary annotation. Longest-match and LaoNLP are not accepted as normative implementations.
- Next feasible work: inspect existing profile selection and lexical-resource governance, then prepare a typed boundary-evidence interface only if it can remain profile-neutral and fail-closed. Do not build a canonical LOC segmenter or claim conformance without the required lexicon and annotation evidence.


## GitHub Pages live-service deployment — 2026-11-16

- Public service: https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System-/
- Hosting decision: GitHub Pages only. No Vercel/Netlify or separate application server is used or authorized for this service.
- Source commit deployed: `8feb14a3cf96fa2e1aafd00ea045d5fddb2e3c4a` (PR #278 squash merge).
- Deployment workflow: `Deploy site to GitHub Pages`, run [43930778763](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43930778763), completed SUCCESS. Build, npm web checks, Vite production build, production Chromium exercise, Pages artifact upload and deployment all succeeded.
- Deployed-runtime smoke succeeded: fetched `/` and `/system.html`; verified the service input element and module script, system page title, and non-empty JS/CSS assets. Workflow resolved the canonical Pages URL above.
- Mainline Quality run [43930778812](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43930778812) completed SUCCESS, including Python tests, web checks and production build.
- The separate browser-smoke workflow [43930778773](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43930778773) was still running its Chromium installation at the time of this record; the Pages workflow itself independently completed its production Chromium exercise successfully.
- Hosting is live, but linguistic readiness is unchanged: this remains a research-grade, evidence-limited prototype. Deployment success is not linguistic validation or empirical accuracy.


## Khmer phonetic-result architecture and partial-output correction — 2026-11-16

**Base:** `main` at `ba54c791ad71b06e99c4255bb93bfd26ae1533bb`.  
**Merged:** PR #280, squash commit `b0157a3b9f43d8c3b9e5623634571ba6cd647151` on `main`.

This change ports architectural patterns from the Lao engine, not Lao phonological rules:

- **KHMER-RESULT-CONTRACT-001 — DONE_VERIFIED (Quality checks run 43937440225):** browser output now exposes a versioned `khmer-phonetic-result/v1` object. Each source unit has its own status, IPA, Ukrainian rendering, profile, structural/phonological/target-policy provenance lanes, and explicit uncertainty. The declared pipeline is source orthography → structural analysis → source phonology → IPA → Ukrainian target adaptation.
- **KHMER-PARTIAL-AGGREGATE-001 — DONE_VERIFIED (Quality checks 43937440225; browser smoke 43937440523):** aggregate IPA and Ukrainian strings preserve supported neighboring results and place explicit unresolved markers only at unsupported units. Overall `complete`, `partial`, and status fields remain separate; a mixed result cannot be mistaken for a complete transcription.
- **KHMER-UNICODE-DIAGNOSTICS-001 — DONE_VERIFIED (Quality checks 43937440225; browser smoke 43937440523):** browser parsing now iterates Unicode code points rather than UTF-16 code units and includes exact U+ code-point diagnostics for unsupported graphemes. The reported visible string `ព្រះរាជាណាចក្រ` is added as a regression: every visible character is present in the orthographic inventory, so lack of a lexical IPA fixture must remain NOT_ESTABLISHED rather than INVALID_OR_UNSUPPORTED. The test also checks lossless grapheme accounting and a supplementary-plane unsupported symbol.
- Existing lexical IPA fixtures, the canonical IPA → Ukrainian policy, uncertainty statuses, and the separate BGN/PCGN romanization route are preserved. No new Khmer pronunciation or Ukrainian candidate has been invented.

**Still PARTIAL / TODO:** the browser tokenizer remains a conservative orthographic-unit heuristic, not a validated Khmer word/syllable segmenter; the complete contextual orthography → IPA engine and vowel/rime/coda matrix remain incomplete; the Python and browser engines emit the same versioned typed-result contract; exact-head cross-runtime contract-shape tests passed; independent adjudicated IPA gold remains 0 and empirical accuracy remains null. Do not transfer Lao syllable or tone rules into Khmer.

**Verification:** implementation merge commit `b0157a3b9f43d8c3b9e5623634571ba6cd647151` was followed by main verification checkpoint `dbbd34a4af8c7d24d139d7d7f2442acf4b5328b0`, which passed Quality checks `43938194107`, Khmer browser smoke `43938194161`, and GitHub Pages deploy `43938194109`. Quality workflow includes Python tests, corpus/schema checks, Node web checks and production build; browser workflow includes deterministic checks, production build and Chromium tests. No local checkout was available, so no local test run is claimed. PR #280 is merged and the GitHub Pages deployment succeeded for the resulting main SHA. Linguistic acceptance separately requires expert-reviewed Khmer segmentation/phonology and the existing double-annotation/adjudication process.


The reported `ព្រះរាជាណាចក្រ` false `Unknown character(s)` state has now been traced to the browser parser's unit assumption: the conservative tokenizer can keep several known Khmer base consonants in one orthographic chunk, but the parser previously treated every post-base consonant outside a COENG pair as unknown. The parser now records every recognized consonant as a consonant grapheme and withholds phonetic output when the chunk cannot be confidently syllabified. This is a structural-recognition correction, not a new pronunciation rule; the absence of a lexical IPA fixture still yields NOT_ESTABLISHED.

The shared `khmer-phonetic-result/v1` payload is specified in `schemas/phonetic-result.schema.json`. Both runtime implementations expose the same unit keys, rule trace, provenance lanes and uncertainty shape; Python and browser tests assert the published contract shape.

## Profile-neutral Khmer word-boundary evidence interface — 2026-11-16

- Added `src/khmer_ua/word_boundaries.py`, package exports and `schemas/word-boundary-evidence.schema.json`.
- `KHM-WORD-BOUNDARY-EVIDENCE-001`: profile-neutral evidence contract; source offsets are Unicode code points; caller-supplied protected cluster spans prevent boundaries from splitting a grapheme cluster; competing candidates remain explicit; every selected adjudicated boundary requires per-boundary adjudicated evidence and a source locator.
- The interface never tokenizes, selects a candidate from longest match, infers loan origin, or claims ALA-LC conformance. Profile ID/version remain paired and optional pending the owner's explicit 1997-vs-2013 decision.
- Acceptance after exact-head CI: DONE_VERIFIED for the evidence container/schema/tests only. Word segmentation remains TODO/EVIDENCE_LIMITED; rights-cleared lexical evidence and independent boundary annotations remain BLOCKED; no word segmentation output has been added to the service.
## Post-merge verification — profile-neutral Khmer boundary evidence — 2026-11-16

- PR #281 merged to `main` as `50ae3538a624cf78781411c08ebcf51f73fcb5c2`.
- Exact-main Quality checks [43940735723], Khmer browser smoke [43940735738], and GitHub Pages build/deploy [43940735610] all SUCCESS on the merge SHA.
- Quality verified Python tests, independent IPA gold corpus structure, Node web checks and production build. Browser smoke verified visible output in Chromium. Pages workflow built the site, exercised the production site in Chromium, deployed it, and verified deployment.
- The change adds only a profile-neutral evidence interface; it does not change segmentation or linguistic outputs. Open PR count after merge: 0.
- The boundary evidence interface is DONE_VERIFIED; profile selection, licensed lexical resources and independently adjudicated boundary data remain TODO/BLOCKED as recorded in the LOC evidence audit.


## Khmer subscript independent-vowel structural support — 2026-11-16

- Starting main: `784d1a14f9464022b42104f5c41b6277464bdcc9`; dedicated branch: `feat/khmer-subscript-independent-vowels-2026-11-16`.
- Source finding: Unicode Standard 18.0.0 Chapter 16 §16.4.1 documents subscript independent vowels and uses `ផ្ឯម` as an orthographic example. The parser accepted COENG only before consonants, so this source-documented structure was rejected as malformed.
- Implementation: `KhmerSyllable.subscript_independent_vowels`; `KhmerGrapheme(kind="subscript_independent_vowel")`; Unicode 18 source registry record; public `khmer_subscript_sequence_spans()` helper with exact-source code-point offsets; regression tests ensure the COENG pair is protected and the phonetic representation remains `phoneticization_not_yet_established`.
- Scope limit: helper spans cover only U+17D2 plus the following modeled consonant/independent vowel. They do not represent complete Khmer grapheme clusters, full orthographic syllables, word boundaries, IPA or Ukrainian output. The feature is structural only.
- Task `KHM-STRUCT-SUBSCRIPT-INDEPENDENT-VOWEL-001` = DONE_VERIFIED after exact PR-head and exact-main CI. No local test execution is claimed; the environment has no repository checkout.
- Post-merge exact-head/main verification is recorded above. The human word-boundary annotation gate in Issue #104 remains independent and open.


### Exact-main verification — Khmer subscript independent-vowel structure — 2026-11-16

- PR [#282](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/282) merged by squash as `dd94f637674ad5ce599ee439584b88b6dba4db1e`; PR head `1988cfb3e7df99873b8c340d8c5676bf0d536231`; starting main `784d1a14f9464022b42104f5c41b6277464bdcc9`.
- Exact PR-head Quality [43946963677] and Chromium [43946963832] passed. Exact-main Quality [43947114555], Chromium [43947114448], and Pages build/deploy/deployed-runtime smoke [43947114535] all SUCCESS on the merge commit.
- Exact-main Quality log: **393 Python tests passed, 70 subtests passed**; independent IPA gold corpus structure validation, Node/web checks and production build passed. Chromium smoke and production-site Chromium exercise passed. Pages deploy and deployed runtime asset smoke passed.
- An initial Quality run failed only because the new test omitted `import pytest`; this was corrected in commit `1988cfb3e7df99873b8c340d8c5676bf0d536231` and all subsequent exact-head/exact-main checks passed. No failures are hidden or counted as successful.
- `KHM-STRUCT-SUBSCRIPT-INDEPENDENT-VOWEL-001 = DONE_VERIFIED`. The helper protects only COENG + following modeled subscript character; full Khmer orthographic syllable segmentation and LOC word segmentation remain unimplemented. Issue #104 remains OPEN and requires human annotation/adjudication. No local test execution is claimed.


## Unicode 18 Khmer orthographic-component scanner — 2026-11-16

- Starting exact main: `aa02c23094f4e9c796e236b46d9a359655d34735`; dedicated branch: `feat/khmer-orthographic-component-scanner-2026-11-16`.
- Primary source: Unicode Standard 18.0.0 Chapter 16 §16.4 gives the Khmer component-order BNF `B {R | C} {S {R}}* {{Z} V} {O} {S}`, defines base, robat, shifter, subscript, dependent vowel, join controls and other signs, and documents examples such as `ខ្ញុំ`, `ច្រើន`, `សង្គ្រាម`, `ហើ្យ`, `សញ្ញា`, `ស៊ី`, `ប៉ី`, `ម៉្ងៃ`, `ប‌៊ីយែរ`, `ផ្ឯម`, `អាយ៌` and `ពត៌មាន`. UAX #29 Revision 49 explains default grapheme-cluster rules and states that Khmer word boundaries require tailoring; it also notes that orthographic-syllable units may require additional tailoring.
- Implementation: new `src/khmer_ua/orthographic_structure.py` and public `scan_orthographic_components()`; typed `KhmerOrthographicComponent/Scan`; schema `schemas/orthographic-components.schema.json`; Python `analyze()` adds a per-unit structural component trace; browser runtime mirrors the same role labels, codepoint offsets and statuses; regression fixtures cover Unicode 18 examples and supplementary-plane offsets.
- The scanner itself remains a lossless component layer, not a syllabifier. The separate Unicode 18 BNF parser now consumes it, validates component order, and returns packed orthographic-syllable alternatives. Neither component spans nor syllable spans infer lexical word boundaries, pronunciation, IPA or Ukrainian output. Do not pass scanner component spans as complete cluster protections to the word-boundary API.
- Task `KHM-ORTHO-COMPONENT-SCAN-001 = DONE_VERIFIED` for the scanner contract. The separate `KHM-ORTHO-BNF-PARSER-001` is now DONE_VERIFIED for Unicode 18 orthographic parsing; LOC word segmentation remains separate.
- No local tests are claimed; the connector session has no local repository checkout. Issue #104 remains open for human phonetic annotation/adjudication.


### Post-merge verification — Unicode 18 Khmer orthographic component scanner — 2026-11-16

- PR [#283](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/283) merged by squash as `bdc15daf6f7c40a6c088e306343a421b9347e9c1`; exact PR head `06255d5140c27b0534395ee19c7087cca8fabd0c`; starting main `aa02c23094f4e9c796e236b46d9a359655d34735`.
- Exact PR-head Quality [43953219338] and Chromium [43953219579] succeeded. Exact-main Quality [43953449784], Chromium [43953449807], and Pages deploy/runtime smoke [43953450103] all succeeded on the merge commit.
- Exact-main Quality log: **402 Python tests passed, 70 subtests passed**; IPA corpus engineering validation, Node/web checks and production build passed. Chromium visible-results smoke passed. Pages production-site Chromium exercise, deploy action and deployed runtime-asset smoke passed.
- `KHM-ORTHO-COMPONENT-SCAN-001 = DONE_VERIFIED` for the component scanner and Python/browser parity contract only. It does not close full BNF parsing, complete orthographic-syllable segmentation, lexical word segmentation, IPA coverage or Issue #104.
- Open PRs: 0. Historical PR #64 was closed unmerged on 2026-11-02; its old CSS snapshot was not merged. Its branch ref remains preserved. Feature branch `feat/khmer-orthographic-component-scanner-2026-11-16` also remains preserved; no branch deletion or force update performed.
- Main after this code merge: `bdc15daf6f7c40a6c088e306343a421b9347e9c1`. The documentation-only reconciliation below may advance main and must receive its own exact-main verification.


## Unicode 18 Khmer orthographic-syllable grammar reconciliation — 2026-11-16

- Reconciled the exact Unicode Standard 18.0.0 §16.4 formula `B {R | C} {S {R}}* {{Z} V} {O} {S}` with Appendix A.2's extended-BNF semantics (braces = optional group; `*` = zero or more). This confirms the existing Python/browser component scanner is not a full parser: it inventories components but does not validate order, derive complete syllable spans, or retain alternative parses.
- Inspected Unicode Technical Note #61, Version 2 (February 2025), §§“Orthographic Syllable Structure”, “Coengs”, “Triisap and Muusikatoan”, “Vowels” and “Signs”. It is explicitly non-normative implementation guidance; it proposes a tighter Modern Khmer structure and separately treats Middle Khmer. Do not conflate it with the Unicode Standard's broader BNF.
- Established the next parser contract: a separate Unicode-18 grammar implementation over the existing scanner, exact code-point spans, lossless reconstruction, all viable parses/packed parse forest (no greedy choice), explicit ambiguity, and separate orthographic vs phonological/word boundaries. A TN #61 v2 Modern Khmer profile may be added only as a separately named non-normative validator.
- New audit: `docs/audits/current/UNICODE-KHMER-ORTHOGRAPHIC-SYLLABLE-GRAMMAR-2026-11-16.md`. Task `KHM-ORTHO-BNF-PARSER-001` remains TODO; source reconciliation is DONE_VERIFIED. No code, IPA, Ukrainian output, corpus labels or generated artifacts changed.
- Main baseline inspected: `567c105ac453ff95f1e2a567b8f5e992bda9d6b0`. Exact-main Quality [43953751661], browser smoke [43953751879] and Pages deploy/runtime smoke [43953751433] all completed SUCCESS on this SHA. This resolves the prior PENDING Pages note from the previous handoff.
- Local clone/test execution was attempted but blocked because this execution environment could not resolve github.com. The docs-only change must receive exact-head hosted CI; no local tests are claimed.


## Unicode 18 Khmer parser and packed-forest completion — 2026-11-16

The source-reconciliation checkpoint above was superseded by implementation. Main commit 8ec4460a0af291dcba10563912f8fcd0c3f784fd contains the canonical Python/browser Unicode 18 §16.4 parser, grammar-role alternatives, packed derivation representation, and rejected component spans/reasons. It builds on the component scanner and the §16.4.1 subscript-independent-vowel primitive.

- Python: src/khmer_ua/orthographic_syllables.py.
- Browser: src/orthographic-syllables.js.
- Schema: schemas/orthographic-syllables.schema.json.
- The parser preserves complete segmentation alternatives and local grammar-role alternatives without Cartesian expansion, exact source text and Unicode code-point offsets, derivation counts, and rejected spans/reasons. Ambiguous results do not select a preferred parse.
- Shared fixtures cover all Unicode 18 Figure 16-3 examples, §16.4.1 shifter and join-control examples, subscript independent vowels, robat, deprecated/discouraged code points, and the repetition sign that remains outside the syllable grammar.
- Exact-main Quality [43963765593] SUCCESS: 417 Python tests + 70 subtests; IPA corpus structural validation, Node/web checks and production build passed. Chromium [43963765334] SUCCESS. Pages deploy/runtime smoke [43963765391] SUCCESS.
- KHM-ORTHO-BNF-PARSER-001 = DONE_VERIFIED. This is orthographic structure only, not phonological syllabification, LOC word segmentation, IPA or Ukrainian output.
- TN #61 v2 source metadata is registered as unicode-tn61-khmer-encoding-structure-v2, with its date/version, independent non-normative status and Unicode Terms of Use limitations. KHM-ORTHO-TN61-MODERN-PROFILE-001 remains TODO / NON_NORMATIVE; no TN61-derived constraints are mixed into the Unicode 18 parser.
- PR #292 was closed as duplicate after equivalent diagnostics were merged independently to main; its branch remains preserved. PR #294 merged as 8ec4460a0af291dcba10563912f8fcd0c3f784fd, adding the TN #61 v2 source-registry entry, provenance test and documentation reconciliation. Exact-main Quality [43963765593] passed 417 Python tests + 70 subtests; Chromium [43963765334] and Pages [43963765391] passed.
- Issue #104 remains OPEN; independent adjudicated IPA gold remains 0. The repository is a research/engineering prototype, not release-ready.
- All cited checks were run by GitHub Actions; no local checkout/test execution is claimed.


## Final post-merge checkpoint — 2026-11-16

- Final main: 8ec4460a0af291dcba10563912f8fcd0c3f784fd.
- PR #294 merged: TN #61 v2 metadata registered with version/date, author/contributors, official landing/PDF URLs, independent non-normative status, Terms of Use URL, and Technical Notes policy URL; provenance test and README/audit/handoff updates merged.
- Exact-main Quality [43963765593] SUCCESS: 417 Python tests + 70 subtests, IPA corpus structural validation, Node/web checks and production build.
- Exact-main Chromium [43963765334] SUCCESS.
- Exact-main GitHub Pages deploy and published-resource smoke [43963765391] SUCCESS.
- PR #286, #288, #289 and #292 were closed as duplicate/superseded; their branches remain preserved. PR #294 is merged. No force-pushes or user-branch deletions were performed.
- KHM-ORTHO-BNF-PARSER-001 = DONE_VERIFIED. TN #61 Modern Khmer profile, LOC word division, phonological syllabification, independent IPA gold and Ukrainian output remain TODO/BLOCKED/EVIDENCE_LIMITED as specified in the registers.
- Issue #104 remains OPEN. Independent adjudicated IPA gold remains 0.
- No local tests were run; all cited verification is from GitHub Actions.

## Full-file audit — Google Khmer TTS lexicon and OpenSLR 42 — 2026-11-16

- Inspected the full archived Google Language Resources `km/data/lexicon.tsv` blob at repository commit `a90601024f07ab7e96c911243324e0adeb16da96` (blob SHA `d399efeca642b1185786b2982374488c525e37c4`; GitHub file metadata 2.71 MB), rather than the earlier bounded sample. The file has **69,415 two-column rows**, **69,405 unique spellings**, 62,179 Khmer-script rows (62,175 unique keys) and 7,236 Latin-script rows (7,230 unique keys).
- Ten spelling keys occur twice and each pair has divergent phonemic transcriptions. Although the header describes an optional third disambiguating label, every actual row has only two columns. Any future comparison must preserve those variants; do not deduplicate or select one reading automatically.
- The lexicon uses 54 distinct phonemic tokens, all present in `km/festvox/phonology.json` (blob SHA `8fb697ff66b09ef0c2a17f17b35600af410a92a9`): 56 phone entries total (30 vowels, 24 consonants, 2 silence phones; the silence labels are unused). The notation includes ASCII digraphs and doubled-vowel length labels and is a project-specific phonemic inventory, not a documented strict IPA convention. This validates internal symbol-set consistency only, not pronunciation accuracy.
- Sodimana et al. (2018), DOI 10.21437/SLTU.2018-14, report 70,671 Khmer lexicon entries; the inspected snapshot has 69,415 rows (1,256 fewer). The paper says words were crawled from Wikipedia/websites, frequency-ranked, manually transcribed by linguists under guidelines and quality-checked, but gives no Khmer-specific guideline, dialect, annotator count, per-entry source locators or error rate.
- Rights: the `lexicon.tsv` file header explicitly declares CC BY 4.0. The companion `phonology.json` has no file-level license header; the repository README says original files are Apache-2.0 unless otherwise noted, while the paper broadly says data are CC BY 4.0 unless otherwise noted. The companion JSON's exact license scope remains unresolved. Do not infer that the two files share a license.
- SLR42 cross-check: the current OpenSLR page and linked LICENSE file declare CC BY-SA 4.0 and list `km_kh_male.zip` as the sole 866 MB male-speaker archive. The 2018 paper's Table 1 reports 17 female speakers, 2,906 files and 3:58:00 at the same SLR42 URL; the paper's general data-license statement says CC BY 4.0 unless otherwise noted. The current provider-specific archive/license declarations conflict with the paper's metadata. The linked LICENSE was inspected, but the 866 MB archive and its internal manifest/license were not downloaded.
- Updated the existing `google-language-resources-km` and `openslr42-khmer-audio` source records, the IPA gold collection playbook, this handoff and the completion register on branch `research/google-khmer-lexicon-full-audit-2026-11-16`. No lexicon, audio, phonological labels or gold records were imported; no engine/runtime behavior changed.
- `KHMER-GOOGLE-TTS-001 = PARTIAL` (full file and symbol inventory audited; profile, convention, provenance and companion-file rights remain unresolved). The lexicon is a candidate lexical/phonemic comparator, **not** independent IPA gold. `KHM-GOLD-001 = BLOCKED`; Issue #104 remains OPEN; independently adjudicated IPA gold remains 0 and empirical accuracy remains null.
- Main at research start: `941fbf0ed01ae79c2a8be0c02f1870b68e19134a` (after PR #296's documentation merge/correction). PR #297 was closed unmerged and its branch remains preserved. The research branch requires exact-head hosted CI; no local tests or dataset imports are claimed.

### Exact PR-head verification — Google Khmer lexicon audit — 2026-11-16

- Pre-closeout research head `8f79b5560a0ebdfc678f8583e053e9de8be691be`, PR #300: Quality [43965204827] SUCCESS — **417 Python tests + 70 subtests**, independent IPA corpus structural validation, Node/web checks and production build. Khmer browser smoke [43965204751] SUCCESS — **12/12 Playwright tests**; visible-result checks passed.
- The five-file change is source-registry/documentation-only. No runtime, generated artifacts, lexicon rows, audio, phonological labels, IPA gold or Ukrainian output changed. JSON source registry parsed during editing. No local repository checkout or local tests are claimed.
- PR #300 remains OPEN; no merge or deployment was performed. The candidate resource remains PARTIAL, not gold. Next blocker is specialist confirmation of phonemic convention/profile and item-level provenance, plus resolution of the paper-vs-snapshot count and companion JSON license; Issue #104 still requires the external human convention/recruitment/blind annotation/adjudication process.

### Pre-follow-up exact-head CI checkpoint — Google Khmer lexicon audit — 2026-11-16

- PR #300 final head: `65bbc704a5bcf6906f5d57841a625e6f9a2b0f29` (six changed files: source registry, master handoff, linguistic completion register, IPA collection playbook, IPA corpus contract and repository audit).
- Exact-head Quality run [43965487859](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43965487859) SUCCESS: `417 passed, 70 subtests passed`; independent IPA corpus structural validation, Node/web checks and production site build passed.
- Exact-head Khmer browser smoke [43965487827](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43965487827) SUCCESS: deterministic web checks, production build, Chromium install and visible-result browser checks all passed. The prior 12/12 Playwright count remains recorded for pre-closeout head `8f79b5560a0ebdfc678f8583e053e9de8be691be`; the final run's job summary confirms successful Chromium checks but its log count was not separately extracted.
- These are hosted PR-head checks only. No main merge, Pages deployment, local checkout or local test run is claimed. PR #300 remains OPEN and mergeable at the time of this checkpoint.
- The final six-file diff is documentation/source-metadata only; no runtime, generated artifact, dataset payload, IPA labels, Ukrainian mapping or gold corpus rows changed. `KHMER-GOOGLE-TTS-001 = PARTIAL`; `KHM-GOLD-001 = BLOCKED`; independent adjudicated gold remains 0 and accuracy remains null.

### Current PR #300 verification boundary — 2026-11-16

- Current head at this checkpoint: `10e579f554f86eb32fa72b14067a24861a2b760e`, 17 commits ahead / 0 behind base `941fbf0ed01ae79c2a8be0c02f1870b68e19134a`; six changed files: source registry, master handoff, completion register, IPA collection playbook, IPA corpus contract and repository audit.
- Exact-head Quality [43965941851] SUCCESS: 417 Python tests + 70 subtests, IPA corpus structural validation, Node/web checks and production build. Exact-head Khmer browser smoke [43965941825] SUCCESS: 12/12 Playwright tests, including visible-result and accessibility-name/keyboard checks.
- The changes after pre-follow-up head `65bbc704a5bcf6906f5d57841a625e6f9a2b0f29` include source-registry and playbook additions for the 2,748-row/16-speaker Festival prompt index, plus the corpus-contract entry; do not describe all subsequent commits as handoff/register/repository-audit-only.
- The six-file diff is source metadata and documentation only. No runtime, test source, generated artifacts, audio/lexicon payload, IPA gold labels or Ukrainian mapping changed. No local checkout/tests, Pages deployment or production deployment are claimed.
- PR #300 remains OPEN and unmerged. No force-push or branch deletion was performed.

 
## Final post-PR #300 mainline checkpoint — 2026-11-16

- PR #300, “research: complete Google Khmer TTS lexicon audit”, merged by squash as **`b60a65179ffbb593fca8f3eb2c07a1c81e6e8489`**. Final PR head was `07608ca77a06eee741f2988f4e8611d5ebb26880`; issue #300 is closed. No force-push or branch deletion was performed.
- Exact-main Quality [43966413597] SUCCESS: **417 Python tests + 70 subtests**, independent IPA corpus structural validation, Node/web checks and production build.
- Exact-main Chromium smoke [43966413730] SUCCESS: **12/12 Playwright tests**, including Khmer input/output, local unsupported-grapheme handling, romanization separation, accessibility names and keyboard activation.
- Exact-main GitHub Pages build/deploy/runtime smoke [43966413612] SUCCESS: production build, Chromium exercise, artifact upload, deploy and published-site/runtime-asset smoke all passed.
- PR #300 changed source metadata and research/acceptance documentation only. No runtime, generated artifact, lexicon/audio payload, IPA gold labels or Ukrainian mappings were changed or imported.
- The pinned Google Khmer lexicon remains `KHMER-GOOGLE-TTS-001 = PARTIAL`, candidate phonemic comparator only. The paper reports 70,671 entries vs 69,415 snapshot rows. The snapshot has 69,405 unique spellings, ten divergent duplicate keys, 54 used tokens matching a 56-phone inventory, and a CC BY 4.0 header on the lexicon file. Companion `phonology.json` rights remain unresolved.
- The companion Festival prompt index has 2,748 utterance records / 16 pseudonymous speaker-ID prefixes and no gender labels. This differs from the paper's 2,906 files / 17 female speakers and the current OpenSLR page's male-only archive. The prompt index is not a manifest; archive version, checksums and speaker mapping remain unresolved.
- Sodimana et al. (2018) full-text review confirms that its word collection, phonemic transcription guidelines and QC description are general across six languages; it does not provide Khmer-specific annotator, variety, notation, QC/agreement or per-entry provenance. Chem (2020) offers a four-speaker Phnom Penh vowel study but explicitly notes that “Standard Khmer” lacks a clear-cut definition; it cannot validate the Google lexicon as project-profile gold.
- Issue #104 has been updated with the full source audit and the additional Festival prompt-index discrepancy. Independent adjudicated IPA gold remains 0; empirical accuracy remains null. `KHM-GOLD-001 = BLOCKED`.
- Research synthesis stored in the Undermind Khmer workspace: `/analysis/google-khmer-lexicon-profile-and-evidence-audit.md`.
- No local checkout or local tests were run; all code/CI verification above is from GitHub Actions.

## Khmer IPA convention draft checkpoint — 2026-11-17

- Main at continuation start was `484ec68feab98d67bbe327df00ccfbdbe3a56512`, which records PR #300's exact-main checks after its merge. Earlier exact-main Quality (417 Python + 70 subtests), Chromium (12/12) and Pages/deployed-site smoke succeeded; see the post-PR #300 checkpoint above.
- The first research branch `research/khmer-ipa-convention-draft-2026-11-17` was based on `b60a65179ffbb593fca8f3eb2c07a1c81e6e8489`; main advanced by PR #302 before its PR was created. Compare showed one commit behind and five ahead, so that PR could not be merged cleanly. Its work is being ported, not force-pushed or discarded, to the v2 branch based on `484ec68...`.
- Added [Khmer IPA convention sheet draft](../ipa-gold/khmer-pph-careful-citation-ipa-v1-draft.md). It is explicitly `DRAFT_NOT_APPROVED`, proposes `PHONETIC_BROAD` for expert consideration, and records conservative evidence boundaries. It is not a gold annotation standard and does not authorize annotation.
- Full-text review: Minegishi (1985), Chem (2020), Sodimana et al. (2018), and Mam et al. (2025), alongside existing Kirby evidence. Minegishi provides a partial series/coda-conditioned mapping and formal-vs-colloquial distinctions; Chem's final acoustic analysis uses four selected Phnom Penh speakers and formal frame reading, measuring F1/F2 and duration but not F0/stress; Mam et al. use five Greater Phnom Penh speakers and a bounded 50-word cluster/disyllable task, reporting possible pitch phonologization rather than a general citation-form tone rule. No paper supplies a complete approved IPA convention for this project profile.
- Added Minegishi 1985 to `data/khmer/sources.json` with exact locators (pp. 43–53, 55–66); linked the draft from the existing playbook and registered `KHM-IPA-CONVENTION-001 = PARTIAL` in the completion register. Issue #104 has a new evidence comment.
- No gold records, IPA labels, model predictions, audio or external lexicon data were added. Runtime, benchmark code and generated artifacts are unchanged. `KHM-GOLD-001 = BLOCKED`; gold=0; empirical accuracy=null.
- Remaining blocker: specialist sign-off by a qualified contemporary Phnom Penh Khmer phonetician/phonologist, independent challenge review, plus two annotators, separate adjudicator, curator, blind intake, rights-cleared 30-item sample. No expert was contacted or recruited. No local checkout/tests are claimed; hosted CI must run on the final PR head before merge.

## Post-merge Khmer IPA convention draft closeout — 2026-11-17

- PR #306 merged by squash as `4d7e7bd045544d2a6d407511679761a7b0b839a1`; source base was `484ec68feab98d67bbe327df00ccfbdbe3a56512`, final PR head `edded0940db171f92a4daeabe485e8d8efb6a8ba`. The merged change is five files, 143 additions / 2 deletions; no runtime, tests, generated artifacts, gold labels, audio or lexical payload changed.
- Exact PR-head Quality [43969775235] SUCCESS: 417 Python tests + 70 subtests, corpus structure validation, Node/web checks and production build. Exact PR-head Chromium [43969775186] SUCCESS: 12/12 Playwright tests.
- The expert-review draft is `docs/ipa-gold/khmer-pph-careful-citation-ipa-v1-draft.md`, status `DRAFT_NOT_APPROVED`. It proposes `PHONETIC_BROAD` but does not authorize annotation. The evidence review is preserved in the Undermind workspace at https://app.undermind.ai/projects/4f071406-bdb4-4fd1-b93f-71b9d5ec661d?path=/analysis/khmer-ipa-convention-v1-evidence-review.md.
- PR #305 was closed as superseded; its branch remains preserved. PR #306 was the clean v2 port from the then-current main and is merged. No force-push or branch deletion occurred.
- `KHM-IPA-CONVENTION-001 = PARTIAL`; `KHM-GOLD-001 = BLOCKED`; no expert was contacted/recruited; two annotators, third adjudicator, curator, private blind intake, rights-cleared 30-item sample and independent adjudication remain outstanding. Gold=0; accuracy=null. No Pages deployment was triggered by this documentation-only merge; prior Pages evidence remains the PR #300 exact-main checkpoint.

 
## Consolidated Khmer external-source audit — 2026-11-17

A single integration branch now reconciles the overlapping evidence from PRs #301, #303 and #304 against the then-current main. It preserves the detailed Headley/SEALang provenance analysis, the MekongPhon dataset-rights and reproducibility analysis, and the Khmer Acoustic Model artifact audit without treating any external resource as project gold.

### Source decisions
- `mekongphon-2026 = EXTERNAL_BASELINE_CANDIDATE`; rights remain `UNKNOWN_BLOCKED_FOR_REUSE_OR_REDISTRIBUTION`. Pinned lexicon: 8,040 rows (8,026 Headley word entries + 10 numerals + 4 punctuation), split 7,940/100. Sentence pairs are dictionary-derived from OPUS, not independently transcribed speech. No root dataset license, per-item source IDs, or reproducible complete pipeline are available. Preserve the 100-item lexical holdout as a dictionary-seeded diagnostic only.
- Headley (1977) is not demonstrated to match the project's contemporary Phnom Penh careful-citation profile. Jenner (1979), DOI 10.15144/PL-C49.431, describes Headley's broad educated-Standard target and phonemic notation with convention-specific limitations. No verified adapter to the project's typed IPA/register contract exists.
- `open-dict-ipa-km-2026 = EXTERNAL_COMPARATOR_NONCOMMERCIAL_ONLY`. Pinned file has 3,286 rows, 3,261 unique spellings, 25 repeated keys (one divergent) and 63 multi-pronunciation rows. Retain alternatives; no project gold status. The third-party Khmer data are identified as CC BY-NC-SA 4.0, unsuitable for unrestricted commercial redistribution.
- `chemvatho-khmer-acoustic-model-2026` and `chemvatho-khmer-pronunciation-dictionary` remain `BLOCKED_SOURCE_INCOMPLETE_RIGHTS_CONFLICT`. The pinned repository contains only a six-line sample dictionary; full dictionary, model archive, audio corpus and manual alignment annotations are absent. README counts (29,204 vs 33,091) and data license declarations (CC BY-SA 4.0 vs CC BY 4.0) conflict; MIT is software-only. No official MFA model registry entry was found. Alignment boundary metrics are not IPA/G2P accuracy.
- No external corpus, model, audio, or lexicon rows were downloaded or imported. No gold labels or Ukrainian mappings changed.

### Integration and verification boundary
The source registry and canonical research docs were consolidated on `research/khmer-source-audit-integration-2026-11-17`, based on main `db02740d57705c08966c87a6b31a5c874c9edc86`. The PR #304 exact-head Quality runs failed because a legacy integrity test still required the literal `3,286-line` phrase in the source scope; the integrated registry preserves that compatibility phrase. The new integration branch must pass exact-head Quality and browser checks before merge. Prior main Quality [43970083315] SUCCESS (417 Python tests + 70 subtests), Chromium [43970082825] SUCCESS, and Pages deploy [43970082889] SUCCESS are exact for the pre-integration main SHA above.

PR #301, #303 and #304 were closed as superseded after PR #307 merged; their branches are preserved. Do not close them until the integration PR has passed and merged. `KHM-GOLD-001 = BLOCKED`: independently adjudicated gold remains 0; empirical accuracy remains null.

 
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

## Continuation — Kirby Phnom Penh audio candidate audit (2026-11-17)

- Starting main: `44d80987dc7efd461cb4e10b0524dc5c2122a9aa`; dedicated branch: `research/khmer-kirby-cluster-audio-audit-2026-11-17`.
- Added source record `kirby2018-cluster-audio` after verifying the University of Edinburgh DataShare record and Kirby (2014) paper. The source declares CC BY 4.0 and contains 10 native Phnom Penh speakers, 79 lexical items, three repetitions, slow/fast blocks, WAV and segmented Praat TextGrid files. The paper describes the first block as slow-and-careful carrier-sentence reading and analyzes 61 cluster items across 35 onset types.
- Added a detailed source dossier and linked it from the IPA collection playbook and corpus contract. The completion register marks `KHM-KIRBY-CLUSTER-AUDIO-001 = PARTIAL`.
- Boundary: this is supporting audio, not IPA gold. The carrier-sentence task is not automatically equivalent to the project's careful-citation profile; the full archive item manifest and checksum have not been verified locally; no audio or labels were downloaded/imported. The slow-careful block and contrast coverage require specialist approval.
- Research is continuing in Undermind: [Khmer Phnom Penh phonetic pilot lexical materials and source locators](https://app.undermind.ai/projects/4f071406-bdb4-4fd1-b93f-71b9d5ec661d?path=/analysis/Khmer%20Phnom%20Penh%20phonetic%20pilot%20lexical%20materials%20and%20source%20locators).
- No experts were contacted. Issue #104 remains open; convention remains `DRAFT_NOT_APPROVED`; gold=0; empirical accuracy=null.

### PR #309 exact-head verification — 2026-11-17

- PR [#309](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/309) head `74622599f6128f34b3ee2fcd19e346b018d399e2`, based on `44d80987dc7efd461cb4e10b0524dc5c2122a9aa`; 7 commits ahead, 0 behind.
- Hosted Quality workflow [44034902245](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44034902245) SUCCESS on exact head. Steps verified: IPA corpus structure validator; **417 Python tests + 70 subtests**; Node web structural/runtime, Unicode 18 parser, romanization and Ukrainian adapter checks; Vite production build.
- This workflow has one Quality job. No Chromium/Playwright or Pages deployment workflow was triggered for this documentation/source-registry-only branch; do not claim browser or deployment verification for PR #309. No local tests were run.
- No runtime, tests, generated files, audio payload, IPA labels, gold records or Ukrainian mappings changed. Main remains at its pre-PR base until merge; no merge performed in this continuation.

## Kirby cluster-audio candidate — merged mainline checkpoint — 2026-11-17

- PR [#309](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/309) squash-merged as `417ddfe598fc70913d9597dc5fb0b4dc7863d515` on main; source branch retained (not deleted).
- Exact PR-head `a4ab13947e4ff060bf66b2b8a5c14ac432ae195c`: Quality [44039162569] SUCCESS (417 Python tests + 70 subtests, corpus validator, Node/web checks, Vite production build); Chromium browser smoke [44039174297] SUCCESS (deterministic web checks, production build, visible-result Chromium exercise). No Pages deployment was triggered/claimed. No local tests.
- Main at merge is `417ddfe598fc70913d9597dc5fb0b4dc7863d515`; post-merge Quality/build/browser checks were queued at the time of this note and must be checked before claiming mainline verification.
- The source is only a supporting audio candidate. Archive has not been downloaded; listed MD5 is provider metadata, not a locally verified checksum. The 79-item manifest has not been enumerated. Slow-careful carrier-sentence reading requires expert approval before use for the project's careful-citation profile.
- Issue #104 remains open. Convention remains `DRAFT_NOT_APPROVED`; no experts contacted/recruited; gold=0; empirical accuracy=null.

### Final post-merge verification and research blocker — 2026-11-17

- Main commit `d529b941e58d5879b1fb3cdc2d54ba0f921bd15d` passed post-merge Quality workflow [44039408344] and Chromium browser smoke [44039408324]. Quality's single job includes `python scripts/ipa_gold_corpus.py validate --language khmer` (reported 0 records / 0 annotations / `NOT_READY_NO_ADJUDICATED_GOLD` as expected), Python test suite, Node web checks and production build. Browser workflow completed deterministic web checks, production build, Chromium install and visible-results exercise. No Pages deploy workflow was triggered by this documentation-only merge. The last repository update in this handoff is this note; re-run checks if further changes are made.
- Undermind deep search `Khmer Phnom Penh phonetic pilot lexical materials and source locators` completed with 42 ranked references. Its summary is based on abstracts/metadata, not full texts: Kirby cluster audio remains the strongest direct Phnom Penh audio candidate; the slow/fast carrier-sentence task is not proven to equal careful citation speech. Kirby tonogenesis audio, Chem 2020, Mam et al. 2025 and dictionaries/course audio are supporting research leads only; no item list from those sources meets the exact orthography + gloss + audio locator + rights + target-profile acceptance gate. No 30-item pilot list was fabricated.
- Attempted direct DataShare archive retrieval from the execution container; DNS resolution failed (`Temporary failure in name resolution`). Thus the 477.8 MB archive could not be downloaded, its provider-listed MD5 could not be independently checked, and the complete 79-item filename manifest remains TODO. This is an environment/network blocker, not evidence that the archive is unavailable. The archive remains available via the DataShare record for a network-enabled follow-up.
- Remaining human blockers are unchanged: expert approval/replacement of the draft convention, independent challenge review, two annotators, separate adjudicator, non-annotating curator, blind intake, profile ruling on carrier-sentence recordings, and approved contrast coverage. Issue #104 remains OPEN; no one contacted; gold=0; accuracy=null.

## Continuation — Kirby 2011 Phnom Penh prosody source audit (2026-11-17)

- Starting main: `10a475a1511d0729dd9d3ee10c3337fe2bd50531`; dedicated branch: `research/khmer-kirby-tonogenesis-audio-audit-2026-11-17`.
- Enriched the two existing source-registry records `kirby2015-audio` (DOI 10.7488/ds/321, 461.93 MB, provider MD5 `8688e68e76e8269b8bbf5d19020a230b`) and `kirby2015-supplementary` (DOI 10.7488/ds/319); no duplicate source records remain. Both DataShare full metadata records state CC BY 4.0.
- DataShare audio metadata says 16 Phnom Penh speakers, WAV/TextGrid and Praat Pitch/Formant/PointProcess files. Kirby (2014) §§3.1–3.2 reports 20 recruited participants (13 female, 21–60), then excludes four who consistently retained /r/ in both conditions, leaving 16 analyzed. This plausibly explains the DataShare count; archive folder membership remains unverified. The paper reports 41 careful/read items × 3 and a separate 15-item colloquial repetition task × 3.
- Supplementary files include anonymised production/perception CSVs, KlattGrid stimuli, plots and R code. They are not IPA gold; synthetic stimuli and perception responses are not natural production tokens.
- Detailed dossier: `docs/ipa-gold/khmer-kirby-tonogenesis-datasets-audit.md`. No archive or CSVs downloaded, no checksum verified locally, no item manifest extracted, no IPA labels or gold rows created. Issue #104 remains open; convention `DRAFT_NOT_APPROVED`; gold=0; accuracy=null.

### Kirby 2011 full-text reconciliation — 2026-11-17

- Full PDF review of Kirby (2014) §§3.1.1–3.2 and Appendix A (printed pp. 8–11, 47) clarifies the apparent 16-vs-20 difference: 20 native Phnom Penh participants were recruited; four consistently produced /r/ in both conditions and were excluded from subsequent analysis, leaving 16 analyzed participants. This plausibly matches the DataShare audio metadata's 16 speakers. Archive folder membership is still not directly confirmed; keep that acceptance step TODO.
- The paper's 41-item Appendix A is in romanized phonological notation with glosses, not Khmer-script orthography. A Khmer assistant confirmed lexical status/meanings/spellings; some items admit alternate spellings. The list was designed for minimal triplets but not perfectly balanced.
- Task distinction: 41 careful/read self-paced items in the carrier sentence [khñom tha: tiət] at normal rate, 3 randomized repetitions; separate 15-item colloquial repetition task with oral Standard Khmer prompts, also 3 repetitions. Paper reports 2,664 segmented tokens, with main analysis focusing on 2,099 obstruent-onset tokens. Its segmentation labels distinguish onset, excrescent vocalism, trill/tap (voiced/voiceless, fricative/approximant subtypes), and rime nucleus/coda.
- This improves the source's relevance to careful/read phonetics but does not make it standalone citation-form elicitation. Do not import IPA labels or use the 41 romanized forms as exact orthographic records.

## PR #310 merge and final verification — 2026-11-17

- PR [#310](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/310) merged by squash as `4d568f712b8ac055809bc01e53ea7d257b79a6a0`; branch `research/khmer-kirby-tonogenesis-audio-audit-2026-11-17` was retained. The merge enriches the existing `kirby2015-audio` and `kirby2015-supplementary` source records; duplicate records were detected during review and removed before merge (registry now 48 entries, 48 unique IDs; exactly one entry per DOI 10.7488/ds/321 and 10.7488/ds/319).
- Final exact PR head: `a4e8f315f3de8d1742ed5018e27be164ed7bb7cb`. Quality [44054481444](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44054481444) SUCCESS: `python scripts/ipa_gold_corpus.py validate --language khmer` returned 0 records, 0 annotations, 0 adjudicated records and `NOT_READY_NO_ADJUDICATED_GOLD` (expected); `pytest -q`: 417 passed + 70 subtests; Node/web checks and Vite production build passed. Chromium [44054481411](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44054481411) SUCCESS: deterministic checks, production build and 12/12 Playwright tests passed.
- Post-merge main commit `4d568f712b8ac055809bc01e53ea7d257b79a6a0`: Quality [44054711288](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44054711288) SUCCESS; Chromium [44054711282](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44054711282) SUCCESS (12 tests); existing automatic GitHub Pages workflow [44054711377](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44054711377) SUCCESS, including Pages deployment and HTTP smoke-tests for the root page, `system.html`, generated JS and CSS at https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System-/ . No Pages settings were changed and no release was published.
- One intermediate CI attempt failed a documentation-contract assertion because the updated source limitations omitted the literal phrase “not an IPA gold”; this was fixed in the source record. The final exact-head Quality and Chromium checks and post-merge mainline checks passed. No local tests were run.
- Archive retrieval remains blocked in the execution container by DNS failure (`Temporary failure in name resolution`); no DataShare audio/CSV archive was downloaded and no provider MD5 was locally verified. No experts contacted. Issue #104 remains OPEN; IPA convention `DRAFT_NOT_APPROVED`; gold=0; empirical accuracy=null.

### Final mainline snapshot after handoff/audit consolidation — 2026-11-17

- Main snapshot before this final handoff note: `b74ed1b03577139ef97ffb45f343398b30677f43`. It contains the merge verification, completion-register update and repository-audit update.
- Exact snapshot Quality [44055115571] SUCCESS: corpus structural validation (`NOT_READY_NO_ADJUDICATED_GOLD`, 0 records/annotations as expected), 417 Python tests + 70 subtests, Node/web checks and Vite build. Chromium [44055115680] SUCCESS (12/12 tests). Existing GitHub Pages workflow [44055115671] SUCCESS, including production browser exercise, deploy and HTTP smoke tests for root, `system.html`, JS and CSS. Public Pages URL: https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System-/ .
- This note is the final handoff consolidation; no code/runtime/data changes. Issue #104 remains OPEN; PR #310 is merged; no open PRs; source branch retained. No local tests, no audio downloads, no expert contacts. The only substantive remaining blockers are archive/token-level evidence and qualified human linguistic approval/annotation.


## Sok & Adams (2016) Khmer phonological G2P source audit — 2026-11-17

- Added source registry entry `sok-adams-2016-phonological` and dossier [`khmer-sok-adams-phonological-principles-audit.md`](ipa-gold/khmer-sok-adams-phonological-principles-audit.md), based on the full ACL Anthology/PACLIC 30 paper (pp. 417–424).
- The paper explicitly separates orthography → phonemic transcription (intended as careful speech) from phonemic → phonetic transcription (rapid/ordinary colloquial speech). It describes series assimilation, vowel modification, syllable grouping, coda changes, cluster-transition aspiration/schwa, sonorant devoicing and minor-syllable reduction. This is a useful architectural precedent, not proof that its rules match the project's contemporary Phnom Penh careful-citation profile.
- Methods: 140 hand-selected validation words; phonemic references drawn from Headley (1997), with phonetic forms manually produced by the authors. The larger 10,110-word comparison is dictionary-derived; 999 compounds and Pali/Sanskrit loans are outside the implemented scope. No independent blind double annotation, adjudication, IAA, recorded-speech test set or reproducible independent split is reported.
- Reported 97.86% / 98.43% scores are author-run results on those data, not project accuracy and not a benchmark against independent speech gold. The paper's tables/notation include apparent OCR/typographic inconsistencies; do not copy phonetic mappings without visual page review and specialist approval.
- Proceedings front matter reserves contributed-paper copyright to the respective authors; no explicit open license for the contribution was verified. Registry rights marked UNKNOWN. No table/dataset payload or PDF copied into repository.
- No runtime, test, corpus, IPA gold, Ukrainian mapping or generated artifact changed. Gold remains 0; empirical accuracy remains null; issue #104 remains open; convention remains `DRAFT_NOT_APPROVED`.


## Internal IPA-kind contract repair — 2026-11-17

- Code review triggered by Sok & Adams' explicit separation of careful phonemic and rapid phonetic stages found that `PhoneticUnitResult` carried an IPA string but no transcription-kind field. External candidates had a `kind`, while the deterministic engine's typed output did not.
- Added additive `ipa_kind` to the typed result and JSON Schema. The deterministic engine now marks linguistic units `UNRESOLVED` until expert convention approval and punctuation `NOT_APPLICABLE`; it does not guess PHONEMIC or PHONETIC_BROAD.
- Added regression assertions for lexical, proposed-rule, punctuation and invalid units. No IPA string, runtime pronunciation rule, Ukrainian mapping, corpus row or gold label changed.
- Acceptance of a concrete IPA kind remains blocked on expert approval of `KHM-IPA-CONVENTION-001`.


## Final continuation checkpoint — Sok & Adams audit + IPA-kind contract — 2026-11-17

- Starting main commit for this continuation: `da47cfc15713d9cf6afb2dcd48d84a50450c79b9`.
- PR [#311](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/311) merged as `10016150244821c1727d06312825aa625f4e1d42`: Sok & Adams (2016) full-text source audit and source-registry record. PR-head Quality [44064387019] SUCCESS (417 Python tests + 70 subtests, corpus structural validation, Node/web checks, Vite build); Chromium [44064386990] SUCCESS (12/12). Exact-main Quality [44064764141], Chromium [44064764016] and Pages deployment/smoke [44064764164] all SUCCESS.
- PR [#312](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/312) merged as `c426d1c3bacd6edb303b2b4977e5b34c09b81620`: additive `ipa_kind` field in Python and browser typed results. Linguistic units now say `UNRESOLVED` and punctuation `NOT_APPLICABLE`; no output IPA string or Ukrainian mapping changed. PR-head Quality [44065466424] SUCCESS (418 Python tests + 70 subtests, corpus structural validation, Node/web checks, Vite build); Chromium [44065466500] SUCCESS (12/12). Exact-main Quality [44065655690] SUCCESS (418 + 70); Chromium [44065655890] SUCCESS (12/12); existing Pages build, production Chromium, deploy and deployed-site/runtime-asset smoke [44065655951] SUCCESS.
- Source registry: 49 entries, 49 unique IDs; Sok & Adams source ID `sok-adams-2016-phonological`, rights UNKNOWN because no explicit open license was verified.
- No local tests were run. All stated test/build/browser/deployment evidence is from the named GitHub Actions runs. No release was published and no Pages settings were changed.
- The only CI warning observed was the existing non-blocking setuptools warning that `project.license` as a TOML table is deprecated. It was not changed in this scope.
- PRs #311 and #312 are merged; no open PRs at this checkpoint. Both working branches are retained. Issue #104 remains OPEN.
- IPA convention remains `DRAFT_NOT_APPROVED`; internal `ipa_kind` remains `UNRESOLVED` for linguistic units pending qualified approval. Independent adjudicated IPA gold remains 0; empirical accuracy remains null; corpus validator correctly reports `NOT_READY_NO_ADJUDICATED_GOLD`.
- Remaining blockers: qualified Phnom Penh Khmer phonetician + independent reviewer for IPA convention; independent annotators/adjudicator and curator for gold; rights-cleared audio/token-level archive inspection and item locators; archive retrieval was not attempted again in this continuation. No Sok & Adams dictionary data or labels were imported.
- Current public site: https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System-/ .


## Full-text Phnom Penh phonetics evidence addendum — 2026-11-17

- Added [the Chem (2020) and Mam et al. (2025) full-text review](ipa-gold/khmer-phonetic-literature-fulltext-review-2026-11-17.md). This records exact speaker/task/sample limitations and printed/PDF page locators, without promoting examples or study outputs to gold.
- Chem's final vowel analysis uses four selected Phnom Penh speakers and 61 formal frame-read items; the complete item list is not published, unfamiliar-word substitutions are not itemized, and the paper's “Standard Khmer” definition and inventory notation require specialist review. It measures F1/F2 and duration, not F0/stress.
- Mam et al. use five Greater Phnom Penh speakers and 50 cluster/disyllable targets in separate PPK/SK frame-reading tasks. The full wordlist is not published; the normalized F0/functional-PC findings support qualified discussion of pitch, not a categorical general tone rule or a complete citation-form IPA convention.
- These findings refine the evidence boundary but do not produce source-exact 30 lexeme groups. The convention remains `DRAFT_NOT_APPROVED`; `ipa_kind=UNRESOLVED`; gold=0; empirical accuracy=null. Issue #104 remains open.
- The repository's current default branch at start of this continuation was `50899bd3a5fd16338039287775fcfb0b9b2568d3`. A fresh branch `research/phonetic-literature-fulltext-review-2026-11-17` was created from that SHA. No local checkout or local tests were possible because DNS resolution for github.com failed in the execution container. No code, runtime rules, gold rows, source permissions or generated artifacts changed.


## Post-merge closeout — full-text Phnom Penh phonetics review — 2026-11-17

- PR [#314](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/314) was squash-merged as `4760964618f05290560372b1ee60b4f7fba8ae72` from exact head `6cbc2e8e515a455611dc3b3c032197129b6b7b26`; base was `50899bd3a5fd16338039287775fcfb0b9b2568d3`, 0 commits behind and 6 commits ahead before merge.
- Exact PR-head Quality [44076405229](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44076405229) SUCCESS: corpus structural validation reported 0 records / 0 adjudicated records and expected `NOT_READY_NO_ADJUDICATED_GOLD`; Python 418 passed + 70 subtests; Node/web checks and Vite production build passed. Chromium [44076405251](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44076405251) SUCCESS: 12/12 Playwright tests.
- This was a documentation/source-audit-only change. No Pages deployment was required or claimed; no runtime, test code, generated artifact, source permission, IPA label, gold row or Ukrainian mapping changed. Local checkout/tests could not run because the execution container could not resolve github.com; hosted PR-head CI supplied the verification evidence.
- The merged literature review records Chem (2020) and Mam et al. (2025) method/sample limitations and confirms neither provides a complete source-exact 30-item pilot list. Issue #104 remains OPEN; IPA convention remains `DRAFT_NOT_APPROVED`; `ipa_kind` remains `UNRESOLVED`; adjudicated gold=0; empirical accuracy=null.
- Additional expert discovery was recorded in issue #104: Dr. Becky Butler (UNC) is a prospective specialist for Khmer phonetic structure, sesquisyllables and diphthongs, but her public record does not establish specific contemporary Phnom Penh careful-citation authority or availability. No one was contacted or recruited.
- Final mainline commit for this closeout: `4760964618f05290560372b1ee60b4f7fba8ae72`. The working branch for PR #314 is preserved; no branches were deleted.


## Mixed-script and Khmer-numeral token boundary correction — 2026-11-17

The supplied real-world paragraph exposed two source-boundary defects: Latin text adjacent to Khmer was absorbed into one Khmer analysis unit, and Khmer digits attached to a Khmer word were treated as malformed orthographic content.

PR #316 (fix/mixed-script-numeral-token-boundaries-2026-11-17) changes the shared Python and browser tokenizers:
- Script transitions now terminate the current run. Adjacent Latin text such as Llenguatge is retained as its own unsupported foreign-script unit; it no longer invalidates the Khmer unit before it or absorbs Khmer text after it.
- Consecutive Unicode numeric characters, including Khmer digits, are isolated as one literal run.
- Numeric literals are preserved unchanged in both display lanes with status NON_LINGUISTIC and ipa_kind: NOT_APPLICABLE. No number reading or pronunciation is inferred.
- Python parser, deterministic engine, browser runtime and typed-result schema share the same local-boundary contract. Regression tests assert exact source reconstruction and preservation of valid neighboring Khmer results.

This is NOT Khmer lexical word segmentation. Spaces and punctuation remain preserved; the orthographic syllable heuristic remains conservative; no LOC word-boundary profile, lexicon, IPA, or gold data was added. Foreign-language text is not translated or assigned Khmer IPA. It remains explicitly unsupported in the Khmer phonetic route.

Task ledger: KHM-MIXED-SCRIPT-NUMERAL-BOUNDARIES-001 = PARTIAL until exact PR-head and post-merge Quality/Chromium/Pages verification succeeds. Linguistic coverage and lexical word segmentation remain separately blocked under Issue #104.

Verification caveat: the first CI passes exposed two stale assertions that expected mixed-script text to invalidate its valid Khmer neighbor, contrary to the repository's local-uncertainty invariant. Those assertions were updated to require local isolation. An intermediate browser run also caught that the tokenizer edit had displaced the register-shifter resolver; the resolver was restored before final verification. Only the latest exact-head runs may be used for acceptance.


## Mixed-script and Khmer-numeral token boundaries — exact PR-head verification — 2026-11-17

PR [#316](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/316) head after regression corrections: `5eb9d23bdadf175fcb40561ff1de26f6f784ad2e`, based on main `0a79df6918e7e4e291ca28f9e758ac0c14acc742` (25 commits ahead, 0 behind at verification).

- Quality [44079138980](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44079138980) SUCCESS: corpus structural validator reports the expected `NOT_READY_NO_ADJUDICATED_GOLD`; Python 422 passed + 70 subtests; `npm run check` and Vite production build passed.
- Chromium [44079138905](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44079138905) SUCCESS: 13/13 Playwright tests, including mixed Latin/Khmer/numeral source-order preservation.
- The first browser run on the earlier head failed because one pre-existing assertion still expected `កx` to erase the valid Khmer neighbor. The assertion was corrected to the local-uncertainty contract; the added mixed-script browser regression then passed on the exact latest head.
- Review also found that U+200C ZERO WIDTH NON-JOINER was classified as an unrelated “other” script and could split a Khmer unit. Both Python and browser script-bucket classifiers now treat ZWNJ as transparent inside the current run; parser and browser-runtime regressions pass.
- Numeric-only input remains `NON_LINGUISTIC`, preserved without a guessed reading, with `ipa_kind=NOT_APPLICABLE`. Foreign-script text remains explicitly unsupported as its own unit. This does not add lexical word segmentation, number reading, translation, IPA, lexical data or gold rows.
- No local tests were run; all verification above is from exact PR-head GitHub Actions. No Pages deployment is claimed before merge.

Task ledger remains PARTIAL until post-merge mainline Quality, Chromium and Pages checks complete. Linguistic coverage and blind-gold acceptance remain separate from this engineering fix; Issue #104 remains OPEN.


## PR #316 post-merge mainline verification — 2026-11-17

PR [#316](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/316) merged by squash as `cca8612e98292ce2ee2f103e12bcce152d4b3416` from exact PR head `56f0dc922f0bf6cf63aabbf09abc1d9c25be7893`. Mainline was 0 commits behind the PR head before merge.

Post-merge workflows on the exact main commit all succeeded:
- Quality [44079454281](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44079454281) SUCCESS: 422 Python tests + 70 subtests; corpus validator returned expected `NOT_READY_NO_ADJUDICATED_GOLD`; Node/web checks and Vite production build passed.
- Chromium [44079454289](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44079454289) SUCCESS: 13/13 Playwright tests.
- Pages [44079454302](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44079454302) SUCCESS: production browser exercise, GitHub Pages deployment and deployed-site/runtime-asset smoke test all passed.

KHM-MIXED-SCRIPT-NUMERAL-BOUNDARIES-001 is now DONE_VERIFIED for structural/output handling. The implementation preserves exact source order across Khmer, foreign-script and numeric runs; foreign text stays locally unsupported; numeric literals pass through as NON_LINGUISTIC with ipa_kind NOT_APPLICABLE; U+200C ZWNJ stays transparent inside Khmer runs. Python, Node/browser and deployed production checks passed.

Scope boundary: this does not implement lexical word segmentation, foreign-language translation, number reading, new Khmer phonology/IPA, or independent gold. Issue #104 remains OPEN; IPA convention remains DRAFT_NOT_APPROVED; ipa_kind remains UNRESOLVED for linguistic units; adjudicated gold=0; empirical accuracy=null. No expert was contacted or recruited. No local tests were run; verification is from the named GitHub Actions runs. No release was published and no Pages settings were changed.

Final mainline commit for this closeout: `cca8612e98292ce2ee2f103e12bcce152d4b3416`. PR #316 is merged; no open PRs remain at this checkpoint. The implementation branch was preserved.

## Expert shortlist revalidation — 2026-11-17

The current candidate screen is documented in [the IPA collection playbook](ipa-gold-collection-playbook.md). Chem Vatho's current CV/profile identifies him as a native Khmer speaker with a 2022–2025 Dr. phil. in Phonetics (University of Cologne), Central Khmer phonetic-reduction dissertation, RUPP linguistics/Khmer teaching, Royal Academy linguistics-committee service, acoustic phonetics and IPA convention-design experience; it lists an Illustration of the IPA for Phnom Penh Khmer as under revision. He is now the strongest candidate for primary target-profile convention review, subject to credential/status confirmation and disclosure that he maintains the Khmer acoustic-model/dictionary resource. He must not solely adjudicate his own resource-derived data.

James P. Kirby is added as a candidate for independent, bounded challenge review of Phnom Penh Khmer /r/-loss, onset F0/VOT, aspiration, phonation, cluster transitions and speech-style distinctions. His LMU profile and peer-reviewed PPK work support this scope; he is not documented as a native Khmer speaker and cannot replace native target-profile authority. Check collaboration/conflicts with Vatho before treating him as independent. Nielson Hul and Becky Butler are not independent of each other because they co-authored a forthcoming Khmer diphthong chapter. Honglada Klaharn is a possible structural/phonological reviewer only; Sothornin Mam a pitch/F0 specialist candidate only. No one was contacted or recruited.

This update changes no convention, runtime IPA, source dataset, rights status, gold record, or accuracy metric. Issue #104 remains OPEN; IPA convention DRAFT_NOT_APPROVED; 30-item pilot BLOCKED; adjudicated gold=0; empirical accuracy=null.


## PR #319 expert shortlist revalidation — post-merge mainline verification — 2026-11-17

PR [#319](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/319) merged by squash as `033e979c06c30aff5569750fae824f90484558ed` from exact head `5c66ee261dec27893e25e9f97e6875d54b58b62c`.

Exact PR-head checks:
- Quality [44081155872](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44081155872) SUCCESS: 422 Python tests + 70 subtests, expected corpus validator state `NOT_READY_NO_ADJUDICATED_GOLD`, Node/web checks and Vite build.
- Chromium [44081155831](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44081155831) SUCCESS: 13/13 Playwright tests.
- A duplicate push-triggered Quality run [44081116226](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44081116226) also completed SUCCESS with the same checks.

Post-merge exact-main checks at `033e979c06c30aff5569750fae824f90484558ed`:
- Quality [44081323278](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44081323278) SUCCESS: 422 Python tests + 70 subtests; expected no-adjudicated-gold validator state; Node/web checks and production Vite build.
- Chromium [44081323386](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44081323386) SUCCESS: 13/13 Playwright tests.
- Pages [44081323295](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44081323295) SUCCESS: production browser exercise, Pages deployment and deployed-site/runtime-asset smoke test.

The expert-shortlist revalidation is DONE_VERIFIED as a research/admin deliverable only: source-backed candidate roles and conflict/independence boundaries are recorded in the playbook and Issue #104. It does not constitute recruitment, consent, convention approval, annotator appointment or adjudication. No one was contacted. No pronunciation rules, IPA labels, external data, source permissions, corpus records, gold labels or accuracy values changed.

Issue #104 remains OPEN. IPA convention DRAFT_NOT_APPROVED; 30-item pilot BLOCKED; two annotators, independent adjudicator, non-annotating curator and private blind intake not recruited/confirmed; adjudicated gold=0; empirical accuracy=null. No local tests were run. No release was published and no Pages settings were changed.

Final mainline checkpoint: `033e979c06c30aff5569750fae824f90484558ed`. PR #319 is merged; no open PRs remained at this checkpoint; Issue #104 remains the sole open issue.


## Final closeout — PR #320 canonical handoff reconciliation — 2026-11-17

PR [#320](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/320) merged by squash as `06d0fc1c38889ea6c02d78f7f3274c835f2744e2`. Exact PR-head Quality [44081681961](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44081681961) SUCCESS: 422 Python tests + 70 subtests, expected `NOT_READY_NO_ADJUDICATED_GOLD`, Node/web checks and Vite production build.

Post-merge checks on the exact main commit `06d0fc1c38889ea6c02d78f7f3274c835f2744e2`:
- Quality [44081774790](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44081774790) SUCCESS: 422 Python tests + 70 subtests, expected no-adjudicated-gold validator state, Node/web checks and Vite build.
- Chromium [44081774743](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44081774743) SUCCESS: 13/13 Playwright tests.
- Pages [44081774768](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44081774768) SUCCESS: production browser exercise, Pages deployment and deployed-site/runtime-asset smoke.

The final source-backed expert shortlist and role/conflict boundaries are documented; candidate-screening task is DONE_VERIFIED only as documentation. No expert outreach, consent, recruitment, convention approval or annotation occurred. Issue #104 remains OPEN; IPA convention DRAFT_NOT_APPROVED; 30-item pilot BLOCKED; adjudicated gold=0; empirical accuracy=null. No local tests were run. No release or Pages settings were changed.

Final mainline checkpoint for this session: `06d0fc1c38889ea6c02d78f7f3274c835f2744e2`. PRs #319 and #320 are merged. No open PRs remain; Issue #104 is the only open issue at this checkpoint.


## Khmer lexical word-segmentation evidence audit — 2026-11-17

The user-supplied sample confirms the already-merged PR #316 fix: adjacent Khmer/Latin/Khmer/numeral runs are isolated and reconstructed without source loss; foreign text stays unsupported and Khmer numerals pass through as NON_LINGUISTIC / NOT_APPLICABLE. The remaining visible limitation is lexical word segmentation, which is distinct from orthographic syllable segmentation and is not implemented by the G2P path.

A new evidence audit is recorded at [KHMER-LEXICAL-SEGMENTATION-EVIDENCE-AUDIT-2026-11-17.md](audits/current/KHMER-LEXICAL-SEGMENTATION-EVIDENCE-AUDIT-2026-11-17.md). Key finding: a 20,000-sentence manually tokenized/POS-tagged ALT/NOVA corpus exists (Kaing et al. 2021; DOI 10.1145/3464378), as does the smaller khPOS corpus. Both are declared CC BY-NC-SA 4.0 in public dataset records; ALT's origin is translated English Wikinews. The NOVA v0.2 guideline §3 defines word tokens as units not further segmentable without loss of meaning and says they correspond to morphemes in most cases; compounds are tokenized into components and marked by shallow bracketing using dictionary and syntactic diagnostics (§5). This is a specific morpheme-level annotation convention, not a universal lexical, orthographic-syllable or phonetic boundary standard. Their conventions, provenance, privacy and non-commercial/share-alike terms must be reviewed before reuse. Tran et al. (2017) is a syllable-database proposal, not a sentence-level lexical word-segmentation benchmark. Sung & Hwang (2016) report F1 0.906 without U+200B on their own manually segmented test data, but no reusable corpus/code release was established.

Task ledger: KHM-MIXED-SCRIPT-NUMERAL-BOUNDARIES-001 remains DONE_VERIFIED. KHM-LEXICAL-WORD-SEGMENTATION-001 is BLOCKED pending an explicit tokenization convention/use decision, license/privacy review, rights-compatible target-relevant corpus, independent double annotation/adjudication, and held-out boundary evaluation. The existing `word_boundaries.py` remains an evidence container and abstains unless exactly one candidate is adjudicated. No lexical segmenter, corpus import, word boundary, pronunciation or IPA claim was added.


## PR #322 exact-main verification and Pages deployment closeout — 2026-11-17

PR [#322](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/322) is merged. The exact main commit is `1cb22c9dfb5ebec539c01544d9e4270b20293b2d`; it is the starting point for this documentation-only verification branch.

All three workflows for that exact main SHA completed successfully:
- Quality [44087269233](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44087269233): `pytest -q` — **422 passed, 70 subtests passed**; shared browser register-shifter contract, web checks and Vite production build passed; corpus validator's `NOT_READY_NO_ADJUDICATED_GOLD` is the expected research gate.
- Chromium [44087269259](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44087269259): **13/13 Playwright tests passed**.
- Pages [44087269174](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44087269174): production browser exercise, artifact upload, deployment and deployed-site/runtime-asset smoke test all passed. The deploy job's final smoke-test step is confirmed SUCCESS.

Current GitHub reconciliation at this checkpoint: `main` remains at the SHA above; no open pull requests; Issue [#104](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/104) remains open as the human IPA-pilot work item. The lexical segmentation evidence audit and `KHM-LEXICAL-WORD-SEGMENTATION-001 = BLOCKED` remain as recorded; no corpus, lexical segmenter, pronunciation rule, IPA label or gold row was added. No local checkout/tests or human accessibility QA are claimed. This closeout records hosted exact-main evidence only; it does not change linguistic release readiness.


## Sok & Adams rule-transfer audit continuation — 2026-11-17

Starting main: 460a3df4476f9f4beba7649909be101ef5331336. Dedicated branch: research/sok-adams-rule-transfer-audit-2026-11-17.

The PACLIC 30 source was visually checked against the ACL Anthology PDF page images (printed pp. 419–422), including Tables 4–6 and §§6.1–7. The audit now separates existing orthographic series/shifter handling from unimplemented cluster-series assimilation, minor-to-major syllable influence, BANTOC-conditioned vowel changes, final sound-change rules, and rapid-speech phonetic transitions. It explicitly prevents PCGN transliteration shortening from being treated as phonological IPA evidence and prevents final trill deletion from being conflated with colloquial onset /r/-loss.

No rule, IPA mapping, Ukrainian output, test fixture, corpus row or generated artifact was changed. The existing code only resolves a bounded orthographic register/shifter layer and returns an inherent-vowel series label; it does not implement the paper's full cluster, cross-syllable or sound-change system. The visual source-review subtask is DONE_VERIFIED; KHM-SOK-ADAMS-RULE-TRANSFER-001 is BLOCKED pending target-profile expert review and item-level positive/negative evidence. The full matrix is in the source audit (docs/ipa-gold/khmer-sok-adams-phonological-principles-audit.md).

The paper's author-run 97.86%/98.43% scores remain non-comparable to project accuracy; its 140-word and dictionary-derived 10,110-word materials remain deferred, not project gold. No table values were copied from the PDF. Current linguistic status remains: IPA convention DRAFT_NOT_APPROVED; linguistic ipa_kind=UNRESOLVED; adjudicated gold=0; empirical accuracy=null; Issue #104 OPEN.

Hosted exact-head CI and post-merge mainline checks are required for this documentation-only update. No local checkout or local tests are claimed. No external expert was contacted and no license or repository setting was changed.


## PR #324 Sok & Adams rule-transfer audit — final verification — 2026-11-17

PR [#324](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/324) was squash-merged as `3f3352e94e993ab54a79c952bf6c1e7f9d187ae6` from branch `research/sok-adams-rule-transfer-audit-2026-11-17`, based on `460a3df4476f9f4beba7649909be101ef5331336`. Its exact-head Quality [44105695150] passed (422 Python tests + 70 subtests; corpus validator returned the expected `NOT_READY_NO_ADJUDICATED_GOLD`; web checks and production build passed), and Chromium [44105694990] passed (13/13 Playwright tests). The duplicate exact-head Quality run [44105669690] also passed. Post-merge mainline Quality [44105872935], Chromium [44105872929] (13/13), and Pages [44105872984] all passed. Pages deployed the exact main SHA and the deployed-site/runtime-asset smoke test passed.

The visual table audit is DONE_VERIFIED as source inspection only. `KHM-SOK-ADAMS-RULE-TRANSFER-001` remains BLOCKED pending qualified contemporary Phnom Penh careful-citation review and item-level positive/negative evidence. No phonological rule, IPA label, corpus row, Ukrainian mapping or generated artifact changed. Issue #104 remains OPEN; IPA convention remains `DRAFT_NOT_APPROVED`; adjudicated gold=0; empirical accuracy=null. No local tests or external expert outreach are claimed.

Final main: `3f3352e94e993ab54a79c952bf6c1e7f9d187ae6`. No open PRs remain at this checkpoint. Repository is engineering/build verified and research-ready as a partial prototype, not linguistically release-ready.


## Shared onset-fallback fixture continuation — 2026-11-17

A dedicated branch `test/khmer-onset-fallback-cross-runtime-fixture-2026-11-17` adds `data/tests/khmer-onset-fallback-fixtures.json` for the unresolved COENG+subscript input `ក្ក`. Both Python and Playwright tests read the same structured case. They assert canonical IPA/Ukrainian abstention remains intact while the separately rendered onset hint is `k` → `к?`, `PROVISIONAL`, position `onset`, rule `KHMER-PREVIEW-ONSET-IPA-V1`. The fixture is explicitly a regression contract, not IPA gold or a new pronunciation rule.

The fallback documentation and completion register were updated. Remaining gates: exact-head hosted Quality/Chromium verification; dedicated per-position evidence registry; and any broader vowel/subscript/coeng hints, which remain disallowed absent independently sourced positional evidence. No production runtime or canonical output changed. No local tests are claimed.


## PR #326 shared onset-fallback fixture — exact-main closeout — 2026-11-17

PR [#326](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/326) was squash-merged as `c345860483b378c66434139b7923a47094875c5a` from `test/khmer-onset-fallback-cross-runtime-fixture-2026-11-17`, based on `0d6e81a58ce514d49d93115c21925441b6acb579`. Exact-head Quality [44111499227] passed: **423 Python tests + 70 subtests**, Node/web checks and production build. Exact-head Chromium [44111513471] passed **14/14 Playwright tests**. The final code-bearing head also passed Quality [44111468114] and Chromium [44111467933] (14/14); the final documentation head Quality [44111513165] passed.

Post-merge mainline Quality [44111679547] passed (**423 Python tests + 70 subtests**, Node/web checks and build). Pages [44111679525] passed, including production browser exercise, deploy and deployed-site/runtime smoke. Main is `c345860483b378c66434139b7923a47094875c5a`; open PR count is 0.

The shared fallback fixture is an engineering regression only: Python checks API-level `null` canonical fields; browser checks rendered NOT_ESTABLISHED markers; both check the separate onset-only `k` → `к?` preview and rule/position provenance. Browser unit detail exposes `data-fallback-rule-id` and `data-fallback-position` for inspection. No new pronunciation rule, IPA label, Ukrainian canonical output, gold record or corpus data was added. The dedicated positional evidence registry remains TODO; broader vowel/subscript/coeng fallback remains blocked pending independently sourced positional rules. IPA convention remains `DRAFT_NOT_APPROVED`; independent adjudicated gold=0; empirical accuracy=null; Issue #104 OPEN. No local tests or human review are claimed.


## Shared onset-fallback parity task acceptance — 2026-11-17

The bounded cross-runtime regression task is now DONE_VERIFIED. PR #326 merged as `c345860483b378c66434139b7923a47094875c5a`; exact-head Quality [44111933616] and Chromium [44111963202] passed, with **423 Python tests + 70 subtests** and **14/14 Playwright tests**. Post-merge mainline at `c345860483b378c66434139b7923a47094875c5a` passed Quality [44111679547], Chromium [44111687227] and Pages [44111679525]. Documentation closeout PR #327 merged as `5a4f97c2c572020829b9c9eff7fad8a3c9d32e0c`; its exact-head Quality/Chromium passed, and final mainline Quality [44112202827], Chromium [44112202856] (14/14) and Pages [44112203152] all passed.

`Browser regression` and `Exact-head CI and Chromium verification` are DONE_VERIFIED for this shared-fixture acceptance only. The broader onset fallback remains PARTIAL: the dedicated per-position evidence registry is still TODO, and vowel/subscript/coeng hints remain excluded absent independent positional evidence. This is not IPA gold; adjudicated gold=0 and empirical accuracy=null. No local tests, external expert review or pronunciation claims are made.

Final main at this checkpoint: `5a4f97c2c572020829b9c9eff7fad8a3c9d32e0c`; open PRs=0; Issue #104 remains OPEN.


## Khmer positional onset evidence registry continuation — 2026-11-17

Starting main: `5afced05c22ffd359e8e9236fbb8a813403cd220`. Dedicated branch: `data/khmer-onset-evidence-registry-2026-11-17`.

Implemented an evidence-only register for the 33 existing consonant onset hints: `data/khmer-positional-onset-evidence.json`; schema: `schemas/khmer-positional-onset-evidence.schema.json`; contract/parity tests: `tests/test_khmer_positional_onset_evidence.py`; audit note: `docs/audits/current/KHMER-POSITIONAL-ONSET-EVIDENCE-REGISTRY-2026-11-17.md`. Every entry identifies the grapheme/code point, onset position, current IPA hint, existing fallback rule ID, specialist-reference row locator, review status and target-profile status. Tests assert exact parity with `data/khmer/consonants.json` and prevent interpreting the registry as canonical or complete coverage.

**Status: KHM-POSITIONAL-ONSET-EVIDENCE-001 = PARTIAL.** The registry is sourced to Richard Ishida's specialist descriptive *Basic consonants* table, not a primary phonetic source. Entries remain `NOT_INDEPENDENTLY_REVIEWED` and `NOT_ADJUDICATED_FOR_PROJECT_PPH_PROFILE`; the registry is not consumed by runtime. Primary phonetic evidence and qualified target-profile review remain blockers. No new pronunciation rule, IPA label, Ukrainian mapping, corpus row or gold record was added. Vowel/subscript/COENG fallback remains blocked. Issue #104 remains OPEN; IPA convention `DRAFT_NOT_APPROVED`; adjudicated gold=0; empirical accuracy=null.

Hosted exact-head Quality/Chromium and post-merge mainline checks are required. This session has no local checkout/test execution. Preserve the strict provisional-only boundary.


## PR #329 positional onset evidence registry — exact-main closeout — 2026-11-17

PR [#329](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/329) was squash-merged as `841bf283eecf13b2e2ccc7f83f02a8c7617c7cdc` from `data/khmer-onset-evidence-registry-2026-11-17`, based on `5afced05c22ffd359e8e9236fbb8a813403cd220`. Exact-head Quality [44118873208] passed (**427 Python tests + 70 subtests**, web checks and production build); exact-head Chromium [44118873039] passed. Final mainline Quality [44119105502] passed (**427 Python tests + 70 subtests**), Chromium [44119105743] passed, and Pages [44119105718] passed build, deploy and deployed-site/runtime smoke. Duplicate exact-head Quality runs [44118865314] and [44118854562] also passed.

The first registry test run exposed an identifier expectation mismatch (`ONSET-1780` versus the test's `ONSET-U+1780`); the test and schema pattern were corrected, and the final exact head passed. Do not count the intermediate failed runs as final verification.

The register contains 33 entries mirrored exactly from `data/khmer/consonants.json`, with per-character locators to Richard Ishida's Basic consonants table. It is an evidence container only: specialist reference, not primary phonetic evidence; all entries remain independently unreviewed and not adjudicated for the project PPH profile; the register is not a runtime dependency. `KHM-POSITIONAL-ONSET-EVIDENCE-001` remains PARTIAL; its schema/register/parity-test subtask is DONE_VERIFIED, but primary phonetic evidence and target-profile review are still required. No new IPA, Ukrainian output, pronunciation rule, gold record or corpus row was added.

Branch reconciliation: `data/pcgn-independent-vowel-source-register-2026-11-16` was not merged because its CSV and test files are byte-identical to the versions already on main; its tip is 12 commits ahead / 97 behind and offers no unique implementation to port. `feat/direct-bgn-pcgn-romanization-input-2026-11-15` was not merged wholesale (24 ahead / 163 behind); its relevant runtime and test files differ from the newer mainline and require a fresh path-level review before any selective reuse. Historical branches remain preserved.

Final main: `841bf283eecf13b2e2ccc7f83f02a8c7617c7cdc`; open PRs=0; Issue #104 remains OPEN. IPA convention remains `DRAFT_NOT_APPROVED`; independently adjudicated IPA gold=0; empirical accuracy=null. No local checkout or local test execution is claimed. Repository remains an engineering-verified research prototype, not linguistically release-ready.

## PR #331 skip-navigation accessibility improvement — exact-main closeout — 2026-11-17

PR [#331](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/331) was squash-merged as `f594b48615a799b13ae19ad4c2c6453512b8c24d` from `a11y/skip-navigation-2026-11-17`, based on `db8596c3dd697727b0075b4142698bbcac7193f2`.

Both `index.html` and `system.html` now expose a first-focusable Ukrainian skip link, visible on keyboard focus, targeting the main landmark with programmatic focus. `src/styles/main.css` styles the focus-visible link, and `tests/browser/site.spec.js` verifies Tab focus, visibility, Enter activation, URL fragment and main-target focus on both pages.

Exact PR-head `0013c41583669503624b5c14cff7dc971f72a484`:
- Quality [44143747834](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44143747834) SUCCESS: **427 Python tests + 70 subtests**, corpus validator's expected `NOT_READY_NO_ADJUDICATED_GOLD`, Node/web checks and Vite production build.
- Chromium [44143747746](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44143747746) SUCCESS: **16/16 Playwright tests**.

Post-merge main `f594b48615a799b13ae19ad4c2c6453512b8c24d`:
- Quality [44144068435](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44144068435) SUCCESS: **427 Python tests + 70 subtests**, web checks and production build.
- Chromium [44144068416](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44144068416) SUCCESS: **16/16 Playwright tests**.
- Pages [44144068336](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44144068336) SUCCESS: production browser exercise, deployment of the exact main SHA, and deployed HTML/JS/CSS smoke checks.

`KHM-UI-SKIP-NAV-001 = DONE_VERIFIED` for the bounded implementation and automated Chromium contract. `KHM-UI-001` remains PARTIAL: no manual screen-reader/assistive-technology review, full keyboard traversal, contrast audit, zoom/reflow or real mobile-device testing is claimed. No local tests were run. No linguistic rules, IPA labels, gold records, source rights or pronunciation outputs changed. Issue #104 remains OPEN; IPA convention `DRAFT_NOT_APPROVED`; adjudicated gold=0; empirical accuracy=null.

## WCAG AA text-contrast regression and palette correction — 2026-11-17

PR [#333](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/333) was squash-merged as `126899c81810750cc1c8a77667340606c10eab20`, from `a11y/wcag-text-contrast-2026-11-17`.

A first browser measurement exposed concrete normal-text contrast failures on the public pages: service eyebrow red on the paper background was **4.24:1** (below 4.5:1), and methodology `.doc .muted` was **3.68:1**. The hint text color was also below threshold at approximately **4.37:1**. The test helper's initial numeric parser defect was corrected before the valid contrast findings were accepted.

The palette was corrected without changing layout or linguistic behavior:
- `--red` changed from `#d92d3a` to `#c12634`, improving red text on paper and white-on-red button contrast.
- `.hint` changed from `#77766f` to `#6d6c65`.
- `.doc .muted` now uses the existing `--muted` token rather than the insufficient `#777d84`.
- Both pages' stylesheet cache keys were refreshed.

Two Playwright tests check representative text/background pairs against WCAG AA's **4.5:1** normal-text threshold. Exact PR head `6ad35d1345872552458d8510cc1a06649e116a5d`: Quality [44149776508] SUCCESS (**427 Python tests + 70 subtests**); Chromium [44149776607] SUCCESS (**18/18 Playwright tests**, including both new contrast checks).

Post-merge main `126899c81810750cc1c8a77667340606c10eab20`: Quality [44150006145] SUCCESS (**427 Python + 70 subtests**); Chromium [44150005996] SUCCESS (**18/18**). Pages [44150006152] SUCCESS: production build, browser exercise, deployment of the exact main SHA and deployed-site HTML/JS/CSS smoke checks all passed.

`KHM-UI-CONTRAST-001 = DONE_VERIFIED` for the specific measured text styles and tested foreground/background pairs only. This is not a complete WCAG audit: all page content, dynamic states, images, non-text contrast, browser zoom, high contrast modes and assistive technologies have not been exhaustively assessed. General `KHM-UI-001` remains PARTIAL. No phonological/IPA/romanization data or linguistic claims changed.


## Final mainline verification after PR #334 — 2026-11-17

PR [#334](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/334) was merged as `a51135d2c65791ae2b433070b71c482a9f49aa40`, based on `126899c81810750cc1c8a77667340606c10eab20`; its documentation branch head was `05aecb1f136c160e03ba8b8ea7dcabee70c58611`. The final post-merge mainline workflows are now verified against the exact merge SHA:

- Quality [44150735242](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44150735242) — SUCCESS: **427 Python tests + 70 subtests**, corpus validator reports the expected `NOT_READY_NO_ADJUDICATED_GOLD`, 24 Node/web tests, and Vite production build.
- Chromium [44150735206](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44150735206) — SUCCESS: **18/18 Playwright tests**, including representative WCAG AA contrast and skip-navigation regressions.
- GitHub Pages [44150735166](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44150735166) — SUCCESS: production browser exercise, artifact upload, deployment of exact SHA `a51135d2c65791ae2b433070b71c482a9f49aa40`, and deployed HTML/JavaScript/CSS smoke checks.

PR #334's exact-head Quality [44150526026] and Chromium [44150526069] also completed successfully on `05aecb1f136c160e03ba8b8ea7dcabee70c58611`; Chromium exercised 18/18 tests. The post-merge mainline evidence above is the release checkpoint. This session used GitHub-hosted repository/Actions evidence; no local checkout or local test execution is claimed.

No linguistic status changed: IPA convention remains `DRAFT_NOT_APPROVED`; independent adjudicated IPA gold remains 0; empirical accuracy remains null; Issue #104 remains OPEN. Accessibility acceptance is limited to the named automated contrast pairs; `KHM-UI-001` remains PARTIAL pending manual screen-reader/assistive-technology review, complete keyboard traversal, zoom/reflow and real-device testing. Repository remains research-ready as an engineering-verified partial prototype, not linguistically release-ready.


## PR #336 exact-main verification and lexical-audit correction closeout — 2026-11-17

PR [#336](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/336) merged as `c4cd8b1a17463f306b7c6dffbaad0f80685e5aa1`; exact PR head was `f5abd6dd14909ff5b89be5b004f023570ba262a7`.

- Exact PR-head Quality [44170618296](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44170618296) SUCCESS: 427 Python tests + 70 subtests; corpus validator correctly reports `NOT_READY_NO_ADJUDICATED_GOLD`; `npm run check` and Vite production build passed.
- Exact PR-head Chromium [44170618297](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44170618297) SUCCESS: 18/18 Playwright tests.
- Post-merge mainline Quality [44170796321](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44170796321) SUCCESS: 427 Python tests + 70 subtests, expected no-adjudicated-gold validator state, `npm run check` and Vite build.
- Post-merge mainline Chromium [44170796376](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44170796376) SUCCESS: 18/18 Playwright tests.
- GitHub Pages [44170796347](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44170796347) SUCCESS: deployed exact main SHA `c4cd8b1a17463f306b7c6dffbaad0f80685e5aa1`; production root, `system.html`, JavaScript and CSS asset smoke checks passed.

This was a documentation/source-interpretation correction only. No runtime segmentation, corpus, IPA, Ukrainian mapping or generated artifact changed. The NICT Khmer NOVA v0.2 guideline now accurately appears as a generally morpheme-level convention with explicit compound handling; it remains distinct from orthographic syllables and project phonetic units. Local clone/test execution was blocked because this environment could not resolve `github.com`; all reported verification is from exact-head and post-merge GitHub Actions.


## Live historical branch inventory refresh — 2026-11-17

Exact `main` at this check: `35a98711902ec70a5a718eb16c6d07c128f978b2`.

- GitHub branch listing pages 1–3 returned **209 refs**: `main` + 208 non-main refs.
- There are **208 unique tip SHAs** across the 209 refs; 207 non-main refs have unique tips, while `data/integrate-positional-onset-evidence-register-2026-11-17` points to the same SHA as `main` (no file diff).
- Open pull requests: **0**. Open issues: **1**, Issue [#104](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/104) (human expert IPA gold pilot).
- Focused content checks in this continuation found the onset evidence registry already integrated through PR #329; PCGN independent-vowel CSV and its parity test are byte-identical to main; the direct BGN/PCGN feature branch is substantially stale and its current files do not justify wholesale porting. Existing parser/adapter research branches remain snapshots, not merge candidates.
- No branch was deleted, force-updated or merged wholesale. One no-diff branch tip equal to main was preserved.

**Status: `KHM-BRANCH-AUDIT-001 = PARTIAL`.** The live ref inventory is refreshed and the duplicate tip is identified, but a complete 208-branch changed-file/commit/PR-ancestry content reconciliation was not performed in this continuation. Earlier 130/130 ancestry comparison records are historical snapshots and must not be read as covering today's 208 non-main refs. Continue with batched compare/content review before claiming full branch-audit completion. Preserve all historical refs pending owner archival policy.

## Selected historical branch content reconciliation — 2026-11-17

A focused content-level pass was performed against exact main `f5c9c70661126b61a23d5435c8c4368215c36746` for the following high-risk non-documentation branches. These are representative dispositions, not a full audit of all 208 non-main refs.

| Branch | Compare to main | Finding / disposition |
|---|---:|---|
| `feat/khmer-subscript-independent-vowels-2026-11-16` | 16 ahead / 62 behind | Older parser lacks current mixed-script/numeral run isolation and orthographic-component scan; tests also lack current per-unit isolation/structure assertions. Not ported. |
| `feat/khmer-packed-parse-forest-2026-11-16` | 6 ahead / 49 behind | Current main's parser, JS adapter, schema and tests extend the branch with rejected-span diagnostics and more Unicode 18 regression coverage. Not ported. |
| `feat/khmer-parser-rejected-spans-2026-11-16` | 5 ahead / 48 behind | Main already contains the rejected-span contract and expanded tests; branch is an earlier snapshot. Not ported. |
| `feat/khmer-unicode18-syllable-parser-2026-11-16` | 3 ahead / 51 behind | Main has the later parser/schema/test state. Not ported. |
| `feat/khmer-orthographic-bnf-parse-forest-2026-11-16` | 22 ahead / 51 behind | Uses the earlier singular `orthographic_syllable.py` path; main's later plural `orthographic_syllables.py` and browser adapter are the integrated implementation. Not ported. |
| `feat/khmer-orthographic-bnf-parser-2026-11-16` | 11 ahead / 52 behind | Same earlier singular-module snapshot; no unique change justified against current main. Not ported. |
| `feat/khmer-ukrainian-practical-adapter-verified-2026-11-11` | 29 ahead / 213 behind | `src/khmer_ua/practical.py` and `data/ukrainian/practical-policy.json` blob SHAs exactly match main. No code to port. |
| `feat/khmer-romanization-ukrainian-matrix-completion-2026-11-12` | 14 ahead / 208 behind | Both romanization Ukrainian CSVs are line-identical to main; its matrix/docs are an older snapshot. No data to port. |
| `feat/direct-bgn-pcgn-romanization-input-2026-11-15` | 24 ahead / 163 behind | Current main has newer residual-Khmer output guard, mixed-script/numeral isolation and broader tests. Not ported wholesale. |
| `data/pcgn-independent-vowel-source-register-2026-11-16` | 12 ahead / 106 behind | CSV and parity test blob SHAs exactly match main; only stale documentation differs. No data/code to port. |
| `data/khmer-onset-evidence-registry-2026-11-17` | 10 ahead / 9 behind | Its registry/schema/test/audit are already integrated through PR #329; no duplicate port. |

The 209-ref inventory from the preceding refresh remains current at this checkpoint. Historical branches remain preserved; no wholesale merge, force-update or deletion was performed.

**Status: `KHM-BRANCH-AUDIT-001 = PARTIAL`.** The table closes only these selected comparisons. Full 208-branch changed-file/commit/PR-ancestry reconciliation remains outstanding and must not be inferred from this representative sample.

## PR #338 exact-main verification — 2026-11-17

PR [#338](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/338) merged as `f5c9c70661126b61a23d5435c8c4368215c36746`. Exact PR-head Quality [44173194420] and [44173216454] passed; Quality reports 427 Python tests + 70 subtests and the expected `NOT_READY_NO_ADJUDICATED_GOLD` validator state. Exact PR-head Chromium [44173216381] passed 18/18. Post-merge mainline Quality [44173400187], Chromium [44173400043] (18/18), and Pages [44173400219] all passed; Pages completed production browser exercise, artifact upload, deployment and deployed-site/runtime asset smoke. No runtime or linguistic behavior changed.
## Final branch inventory and PR #339 mainline closeout — 2026-11-17

After the audit continuation branches were created, a fresh GitHub listing (pages 1–3) returned **212 refs**: `main` + 211 non-main refs, with **212 unique tip SHAs** and no duplicate tips. Open PRs: **0**. Open issues: **1** (Issue #104). This supersedes the 211-ref snapshot immediately preceding the final clean closeout branch; counts are timestamped snapshots.

PR [#339](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/339) merged as `b5a878f33dae74d34754c547580c5a494307cdce`. Exact PR-head Quality [44173798008] and [44173819190] passed (427 Python tests + 70 subtests; expected `NOT_READY_NO_ADJUDICATED_GOLD`); Chromium [44173818953] passed 18/18. Post-merge mainline Quality [44173970460] passed (427 + 70); Chromium [44173970246] passed 18/18; Pages [44173970271] passed production browser exercise, artifact upload, deployment of exact SHA `b5a878f33dae74d34754c547580c5a494307cdce`, and deployed HTML/JS/CSS smoke checks.

PR #340 was closed unmerged as superseded after GitHub reported a squash-merge conflict; its branch remains preserved. Its intended final inventory/verification note is re-applied here from a clean branch based on current main.

No runtime or linguistic behavior changed. `KHM-BRANCH-AUDIT-001` remains PARTIAL: 11 representative historical branches have focused content dispositions, but full content/PR-ancestry review of all 211 non-main refs is not complete. All branches remain preserved.

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


## Continuation — pinned Khmer Phonemizer diagnostic and refreshed historical-ref inventory (2026-11-18)

### Exact mainline checkpoint before this continuation

- Default branch: `main`; base commit: `52b7ae143c2edc0dc34ec87b5e356d4654ea5fb3`.
- Mainline Quality [44257382312](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44257382312), Chromium [44257382268](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44257382268), and Pages deployment [44257382273](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44257382273) all completed SUCCESS on this exact SHA.
- At the next complete branch-list snapshot (GitHub API pages 1–3), the repository had **224 refs, 224 unique tip SHAs**: main plus 223 non-main refs. Prefix counts: `a11y/*` 2, `audit/*` 15, `benchmark/*` 1, `ci/*` 1, `data/*` 4, `docs/*` 97, `feat/*` 50, `fix/*` 14, `release/*` 1, `research/*` 28, `test/*` 10. This is a timestamped inventory snapshot, not proof that every ref has undergone full content/ancestry review.
- Open PRs at the checkpoint: 0; open issues: 1 (#104).

### KHMER-PHONEMIZER-WORKFLOW-001 — DONE_VERIFIED

The historical `ci/khmer-g2p-smoke-2026-10-24` ref contained an optional raw-output smoke workflow. Its script and tests are already present on main, but its old workflow installed the package without a version pin and the historical workflow path has since been repurposed for the separate MekongPhon model diagnostic. Rather than overwrite that workflow or copy the stale configuration, PR [#353](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/353) adds `.github/workflows/optional-khmerphonemizer-smoke.yml` as a separate workflow.

- Pins `khmerphonemizer==0.0.3`; uses Python 3.12 and the repository's current Actions v7 toolchain.
- Runs on relevant pull requests, matching pushes to main, and manual dispatch.
- Executes the existing `scripts/benchmark_g2p.py` and uploads the JSON report plus SHA-256 sidecar.
- The report remains a source-attested diagnostic: independent gold count stays 0 and accuracy stays null. No runtime, pronunciation rule, IPA label or corpus row changes.

Exact PR-head `f73442afa0d37f6de17b4bb9fe779a91d6120ddb` verification:
- Optional raw-output workflow [44259498574](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44259498574) SUCCESS; artifact `khmer-phonemizer-raw-output` uploaded (artifact ID 14406708793; 1,972 bytes; SHA-256 digest `98a7cea015e4166020c321f78217772c73a634baf1557baa6aac0c38ec68335d`).
- Quality [44259498582](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44259498582) SUCCESS.
- Chromium [44259498488](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44259498488) SUCCESS.
- The branch-push Quality run [44259475466](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44259475466) also completed SUCCESS.
- No local checkout or local test execution was available in this connector-only session.

### Remaining branch-family dispositions from the refreshed inventory

- The two `a11y/*` refs are already integrated by PRs [#331](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/331) and [#333](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/333), with their keyboard and contrast checks recorded above in the historical audit. No re-port is needed.
- The new 97th `docs/*` ref is the documentation branch for PR #352; the new 50th `feat/*` ref is the port branch for PR #351. Both are already merged and represented in the current mainline. This updates the earlier 96/49 family counts; it does not reopen those completed family passes.
- The 15 `audit/*` refs were compared against current main. Their changed files are documentation-only (handoff, completion register and/or repository audit); `audit/complete-remaining-branch-families-2026-11-17` is behind-only with no unique commits. The merged PR series #341–#350 contains the corresponding successive audit closeouts. These audit branches remain preserved.
- `benchmark/current-engine-2026-11-11` contains a distinct optional workflow that reads `neurlang/khmer/central/lexicon.tsv` alongside the pinned MekongPhon evaluation split. It was not ported: the branch workflow does not itself establish item-level rights/provenance for the Neurlang lexicon or independent adjudication, and its concordance output cannot be promoted to accuracy. Keep it deferred until those evidence and rights checks are completed.
- The `ci/*` historical workflow is superseded as described above; its useful diagnostic capability is restored in the new pinned workflow without replacing the current MekongPhon workflow.
- Earlier family passes remain: 4 `data/*`, 10 `test/*`, 28 `research/*`, 14 `fix/*`, and 1 `release/*` refs have documented dispositions. The 49 earlier `feat/*` and 96 earlier `docs/*` refs were covered by PRs #347 and #350 respectively; subsequent #351/#352 branches are integrated.

### KHM-BRANCH-AUDIT-001 — PARTIAL

The branch inventory is refreshed to 224 refs / 223 non-main refs, but a full per-file, per-commit and PR-ancestry reconciliation of every historical ref is still not complete. The benchmark workflow remains evidence/rights-limited; all historical refs are preserved. No branch was deleted or force-updated.

### Issue #104 — BLOCKED / human linguistic work

Issue [#104](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/104) remains the sole open issue. The current `data/benchmark/gold.tsv` contains only its header; `annotations.jsonl`, `adjudications.jsonl`, `records.jsonl` and `splits.jsonl` are empty. The issue comments still do not record any expert contact or recruitment. A versioned IPA convention requires expert approval; two independent annotators, a separate adjudicator, a curator, a private blind intake channel, source-rights review and 30 adjudicated items remain outstanding. No accuracy score is available. This cannot be closed by generating synthetic labels or treating source-attested examples as gold.

**Overall state:** research-ready partial prototype, not linguistically release-ready.

 
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


## IPA notation boundary regression and PR #384 closeout — 2026-11-18

- A focused semantic review of the current typed IPA validator found that U+0361/U+035C tie bars were accepted without a following segment (for example `k͡`), and that a second-segment modifier could intervene (`k͡ːa`). The prior state also incorrectly discarded the first segment's availability after an ordinary combining diacritic, rejecting valid structural order such as `t̪͡s`.
- PR [#384](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/384) fixes the notation-state boundary: a tie bar now requires an adjacent second segment letter; trailing, repeated, or interrupted tie bars are rejected; ordinary diacritics before the tie bar remain supported. Added regressions for `k͡`, `/k͡/`, `k͡ːa`, `k͡͡a`, and `t̪͡s`.
- PR #384 merged by squash as `70b381d41f00f89bb94c3694b1c6faa692bfe34d`, based on `411b616df5f69ab337ea15de498b4cf839bf258c`.
- Exact PR-head CI: Quality [44315101232](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44315101232) — SUCCESS; Khmer browser smoke [44315101225](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44315101225) — SUCCESS.
- Exact post-merge main CI on `70b381d41f00f89bb94c3694b1c6faa692bfe34d`: Quality [44315276642](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44315276642) — SUCCESS; Chromium [44315276566](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44315276566) — SUCCESS; Pages build/deploy and deployed-site runtime-asset smoke [44315276557](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44315276557) — SUCCESS.
- Additional semantic reviews: PR #287's Unicode 18 packed parse forest preserves both segmentation and local component-role derivations; PR #185's typed hybrid bridge keeps the deterministic rule engine as the only final IPA/Ukrainian authority and treats external candidates as diagnostics. Both were already integrated; no duplicate implementation was ported.
- Task ledger: IPA tie-bar notation boundary — DONE_VERIFIED; PR #287 parse-role ambiguity review — DONE_VERIFIED; PR #185 typed-provider boundary review — DONE_VERIFIED. The validator remains a notation/metadata gate, not a pronunciation correctness validator.
- No phonological rule, IPA gold label, Ukrainian mapping, corpus row, source dataset, benchmark score or external model result changed. Independent adjudicated gold remains 0 and empirical accuracy remains null. Issue #104, manual accessibility, root-license owner decision and complete historical semantic re-adjudication remain open/partial as previously recorded. No local checkout or local tests were run; all verification cited above is hosted GitHub Actions.
- Repository status remains **research-ready partial prototype**, not linguistically validated or release-ready.


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


## PR #392 — accessibility-name whitespace parsing correction — 2026-11-18

PR [#392](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/392) merged by squash as `9a5da179316c3a40ec159b11c0c936a2c1f9d551`; exact PR head `73c23741313d46533d9285dca6055cf6e34c2151`, base `a71983ebd1e5c3a290153e44b25aa13b969db8b2`. A review of the PR #389 structural accessibility smoke found that the two regex literals intended to split `aria-labelledby` ID references and collapse whitespace were double-escaped, matching a literal backslash-plus-s rather than whitespace. Both expressions now use `\s` as the JavaScript regex whitespace class. This makes multi-ID reference parsing and whitespace normalization behave as intended; it does not turn the helper into a full browser-computed accessible-name implementation.

Exact PR-head Quality [44366919812](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44366919812) — SUCCESS: 432 Python tests + 70 subtests, corpus structural validator, Node/web checks and production build. Exact PR-head Chromium [44366919747](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44366919747) — SUCCESS: 21/21 Playwright tests.

Exact post-merge main checks on `9a5da179316c3a40ec159b11c0c936a2c1f9d551`: Quality [44367112353] SUCCESS; Chromium [44367112434] SUCCESS; GitHub Pages build, production Chromium exercise, deployment and deployed-site/runtime-asset smoke [44367112407] SUCCESS (build and deploy jobs completed).

This is test-only maintenance. No production runtime, IPA or phonological rule, Ukrainian mapping, source evidence, corpus row, gold label, rights status or benchmark result changed. The existing limits of automated accessibility smoke remain: `KHM-UI-001` is PARTIAL pending manual assistive-technology, exhaustive keyboard, zoom/reflow, contrast-context and real-device checks. Issue #104 remains BLOCKED on expert approval/recruitment, independent annotation/adjudication, private blind intake and rights-cleared source items; gold remains 0 and empirical accuracy null. Root license remains BLOCKED on owner decision; full historical semantic review remains PARTIAL; external benchmark integration remains DEFERRED.

Live branch inventory after PR #392: 264 refs / 264 unique tip SHAs (a11y 2, audit 37, benchmark 1, ci 1, data 4, docs 109, feat 50, fix 16, release 1, research 29, test 13, main 1). Open PRs: 0; open non-PR issue: #104 only. No historical branch was deleted or force-updated. No local checkout or local tests were run; all verification cited here is hosted GitHub Actions evidence.


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


## PR #394 — canonical closeout for PR #393 — 2026-11-18

PR [#394](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/394) merged by squash as `855eac7e6dc39a854cc79055c385152a4a32fc49`, with exact PR head `ad1f0d92ff9e809299571e0a1d83f77f9fcf15bd` and base `991d7a1901263743464a41403b3f3936ee33daf1`. It reconciles the three canonical records with PR #393 and its exact-main verification; it changes documentation only.

Exact PR-head Quality [443789... not retained in the run summary] is not claimed here. Exact post-merge mainline checks on `855eac7e6dc39a854cc79055c385152a4a32fc49`:
- Quality [44379052920](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44379052920) — SUCCESS: 432 Python tests + 70 subtests; IPA corpus validator returned the expected `NOT_READY_NO_ADJUDICATED_GOLD`; Node/web checks and Vite production build passed.
- Chromium [44379052839](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44379052839) — SUCCESS.
- GitHub Pages [44379052866](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44379052866) — SUCCESS: production build, Chromium exercise, deployment and deployed-site/runtime-asset smoke.

Live inventory: 266 branch refs / 266 unique tip SHAs; 0 open PRs; Issue #104 is the only open non-PR issue. Historical branches were not deleted or rewritten. No runtime, phonological rule, IPA label, Ukrainian mapping, corpus row, source-rights decision, gold data or benchmark result changed.

Task ledger: PR #394 canonical closeout and exact-main CI — DONE_VERIFIED. Manual accessibility and full historical semantic re-adjudication remain PARTIAL. Independent IPA gold pilot and root-license decision remain BLOCKED; gold = 0 and empirical accuracy = null. External benchmark integration remains DEFERRED pending rights/provenance and an independent evaluation set. Repository remains a research-ready partial prototype, not a linguistically validated or release-ready product.


## PR #395 — canonical closeout for PR #394 — 2026-11-18

PR [#395](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/395) merged by squash as `3e99140e80ba0a0c1654dcd6f367d651350117b5`, with exact PR head `7783454cab3378f324257a4bd704c3528d7629fe` and base `855eac7e6dc39a854cc79055c385152a4a32fc49`. It records PR #394's exact-main evidence in the three canonical documents; documentation only.

PR-head Quality [44389557778](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44389557778), Chromium [44389557809](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44389557809), and push Quality [44389528287](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44389528287) — SUCCESS.

Exact-main checks on `3e99140e80ba0a0c1654dcd6f367d651350117b5`: Quality [44393630260](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44393630260), Chromium [44393630430](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44393630430), and Pages [44393630332](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44393630332) — all SUCCESS. Pages includes production build, Chromium exercise, deployment and deployed-site/runtime-asset smoke.

No production code, linguistic evidence, rights decision, gold data or benchmark result changed. IPA convention remains DRAFT_NOT_APPROVED; independent gold = 0 and empirical accuracy = null. Issue #104 remains BLOCKED on convention approval, independent personnel, blind-intake dry run and 30 source-verified rights-cleared item groups. Root license remains BLOCKED pending owner decision. Manual accessibility and full historical semantic review remain PARTIAL; external benchmark integration remains DEFERRED. Repository remains research-ready partial prototype, not linguistically validated or release-ready.


## PR #397 — expose omitted PCGN shifter uncertainty — 2026-11-18

PR [#397](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/397) merged by squash as `e888c190570acc19b8cf388d1b2a2a58767e6426`, based on `77ddff02fccdf1f2b90c5dcfa2cb92407d0a2850`. The bounded PCGN series resolver now adds the explicit warning `PCGN_NOTE_2_DIACRITICS_MAY_BE_OMITTED_CONSULT_REFERENCE_IF_SERIES_UNCERTAIN` when no shifter is encoded. It preserves the existing graphemic default and does not infer a missing mark or change romanization. Regression tests cover both â/ô defaults and the warning; the PCGN/UNGEGN audit records the source boundary.

PR-head Quality [44395612844](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44395612844), Chromium [44395612835](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44395612835), and push Quality [44395586583](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44395586583) — SUCCESS. Exact-main Quality [44395795606](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44395795606), Chromium [44395795589](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44395795589), and Pages/deployed-site smoke [44395795652](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44395795652) — SUCCESS.

Task ledger: explicit omitted-shifter warning and regression coverage — DONE_VERIFIED. Full PCGN syllable-boundary behavior and end-to-end contextual Khmer-script romanization remain TODO/PARTIAL pending source-backed ambiguity cases, complete row reconciliation and human review. No IPA, pronunciation or Ukrainian output was introduced. IPA convention remains DRAFT_NOT_APPROVED; adjudicated gold = 0 and empirical accuracy = null. Repository remains research-ready partial prototype, not linguistically release-ready.



## PR #399 — correct PCGN shifter code points and BA exception — 2026-11-18

PR [#399](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/399) merged by squash as `8bbdf54bac984165e86b747504ccf7a1e2735741`, based on `725c09a373d0eebb181e3cd3ee02d751e859a3a9`; final PR head `79bacbdef5cd37be94f05d01ea3223644d10d0fb`.

The source registry had the two Khmer register-shifter names attached to the opposite glyphs. It now records TRIISAP as U+17CA (`◌៊`) and MUUSIKATOAN as U+17C9 (`◌៉`). The deeper runtime audit also found a related BA exception defect: the resolver incorrectly treated BA + TRIISAP as a p-in-â exception. PCGN Note 2 exempts BA from TRIISAP's normal â→ô shift; PCGN Note 3's p-in-â exception is BA + MUUSIKATOAN, or BA with a foot. The resolver now preserves BA + TRIISAP in the ô-series (consonant component `b`) and applies the p exception only to the source-supported MUUSIKATOAN/foot cases.

Changed artifacts: `src/khmer_ua/pcgn.py`, `data/khmer/romanization_pcgn_notes.csv`, both PCGN series/consonant decision schemas, their regression tests, and `docs/audits/current/BGN-PCGN-UNGEGN-RULE-DIFF-2026-11-15.md`. The source correction is limited to the orthographic PCGN route; no IPA labels, Ukrainian adaptation, corpus records, source rights, or benchmark values changed.

Verification:
- PR-head Quality [44404900821](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44404900821) — SUCCESS; 435 Python tests + 70 subtests, corpus gate reports expected `NOT_READY_NO_ADJUDICATED_GOLD`, Node/web checks and production build pass.
- PR-head Chromium [44404900673](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44404900673) — SUCCESS; 21/21 Playwright tests.
- Push Quality [44404888463](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44404888463) — SUCCESS.
- Exact-main Quality [44405101264](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44405101264) — SUCCESS; 435 Python tests + 70 subtests and the same expected corpus-gate status.
- Exact-main Chromium [44405101302](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44405101302) — SUCCESS; 21/21.
- Exact-main Pages/deployed-site smoke [44405101273](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44405101273) — SUCCESS; production build, Chromium exercise, deployment and deployed runtime-asset smoke.

Task ledger: shifter-name/codepoint reconciliation and BA+TRIISAP exception correction — DONE_VERIFIED. Complete contextual Khmer-script → PCGN engine and syllable-boundary inference remain TODO/PARTIAL pending source-reviewed ambiguity cases, full table reconciliation and human review. IPA convention remains DRAFT_NOT_APPROVED; independent adjudicated gold = 0; empirical accuracy = null. Issue #104's blind pilot and root repository license remain BLOCKED on external personnel/rights and owner decision. Manual accessibility and historical semantic re-adjudication remain PARTIAL; external benchmark integration remains DEFERRED. No open PRs remain after #399. Repository remains a research-ready partial prototype, not linguistically validated or release-ready.


## PR #401 — cover the explicit PCGN BA + AA shifter cases — 2026-11-19

PR [#401](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/401) merged by squash as `3bbf3f45afb83faf0335dd2f91f869b85f00c5d5`, based on `fc781fa86fa3acb654903560f743d1129428656b`; code/test PR head `0cf4e3a21bc121b4642afafa7f49e365713f7964`.

Added two regression cases in `tests/test_pcgn_series_resolution.py`:
- `ប៊ា`: Note 2's TRIISAP no-shift exception covers BA with AA (បា), not only bare BA.
- `ប៉ា`: Note 3's BA + MUUSIKATOAN p-in-â exception also covers BA with AA.

This closes a test-coverage gap only; the resolver already branches on the BA base and does not reject dependent vowel signs in the series decision. No runtime code, IPA/Ukrainian output, corpus data, rights or benchmark claims changed.

Source: UK BGN/PCGN 1972 Agreement, Notes 2–3, especially Note 2's explicit exception for both BA and BA+AA: https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf

Verification:
- Push Quality [44407401573](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44407401573) — SUCCESS; 437 Python tests + 70 subtests, expected `NOT_READY_NO_ADJUDICATED_GOLD`, Node/web checks and production build.
- PR-head Quality [44407541894](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44407541894) — SUCCESS; 437 tests + 70 subtests.
- PR-head Chromium [44407541887](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44407541887) — SUCCESS; 21/21.
- Exact-main Quality [44407714461](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44407714461) and [44407773406](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44407773406) — SUCCESS; 437 tests + 70 subtests.
- Exact-main Chromium [44407714501](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44407714501) — SUCCESS; 21/21.
- Exact-main Pages/deployed-site [44407714752](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44407714752) — SUCCESS.

Task ledger: BA+AA exception regression coverage — DONE_VERIFIED. Full contextual Khmer-script → PCGN engine and syllable-boundary inference remain TODO/PARTIAL pending complete source-row reconciliation and human-reviewed ambiguity cases. IPA convention remains DRAFT_NOT_APPROVED; independent adjudicated gold = 0; empirical accuracy = null. Issue #104 pilot and root license remain BLOCKED on external personnel/rights and owner decision. Manual accessibility and historical semantic review remain PARTIAL; external benchmark integration remains DEFERRED. Repository remains a research-ready partial prototype, not linguistically validated or release-ready.


## PR #402 — canonical closeout for PR #401 documentation — 2026-11-19

PR [#402](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/402) merged by squash as `92011a62d150917dfc12193471b3fe994212e563` (base `3bbf3f45afb83faf0335dd2f91f869b85f00c5d5`; PR head `d18171b5fb3daa711d5bb699db4ec98d5cc2c26d`). It synchronizes this handoff, the repository audit and the linguistic completion register with PR #401's BA+AA regression coverage. Documentation only; no runtime, test, corpus, IPA, Ukrainian mapping, source-rights or benchmark data changed.

Exact merged-main verification on `92011a62d150917dfc12193471b3fe994212e563`:
- Quality [44478963929](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44478963929) — SUCCESS: 437 Python tests + 70 subtests; expected corpus status `NOT_READY_NO_ADJUDICATED_GOLD`; Node/web checks and production build passed.
- Khmer browser smoke [44478963989](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44478963989) — SUCCESS: 21/21 Playwright tests.
- GitHub Pages [44478963941](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44478963941) — SUCCESS: production build, Chromium exercise, deployment and deployed runtime-asset smoke.

No local checkout or local test execution is claimed; all checks above are hosted GitHub Actions on the exact merged main SHA. Task ledger remains: BA+AA exception regression coverage — DONE_VERIFIED; full contextual PCGN engine and syllable-boundary inference — TODO/PARTIAL; IPA convention DRAFT_NOT_APPROVED and independent gold = 0 (accuracy = null); Issue #104 pilot and root repository license — BLOCKED; manual accessibility and historical semantic review — PARTIAL; external benchmark integration — DEFERRED. Repository remains a research-ready partial prototype, not linguistically validated or release-ready.


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


## PR #443 closeout and PCGN documentation-branch family spot checks — 2026-11-19

PR [#443](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/443) merged by squash as `f9a3dd7fdc813fbf5de8c0e674256c9a6a43ac05`; exact PR head was `40ed62fcf20f48741b0052a9abcf6474caee6069`. All three PR-head checks passed: Quality, Chromium browser smoke, and the second Quality run. Exact-main checks on the merge SHA: Quality [44556021018](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44556021018) — SUCCESS; Pages build/deploy [44556021178](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44556021178) — SUCCESS; Chromium [44556020948](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44556020948) — IN_PROGRESS at last check. Do not claim exact-main browser verification until this run completes.

A further targeted comparison against current `main` reviewed ten retained PCGN documentation refs:

- `docs/pcgn-ba-aa-foot-closeout-2026-11-19`, `docs/pcgn-ba-aa-test-closeout-2026-11-19`, `docs/pcgn-ba-series-vowel-crosslayer-closeout-2026-11-19`, and `docs/pcgn-vowel-fix-closeout-2026-11-19`: each compare changes only canonical documentation (handoff, repository audit, linguistic register, and in two cases the PCGN↔UNGEGN rule-diff document). Their PR #401/#405/#406/#409/#414/#416 checkpoints are superseded by the current mainline source registries, runtime, tests and later closeouts. No unique code, test or source-data change is present to port.
- `docs/pcgn-vowel-note5-verification-closeout-2026-11-19`: documentation-only earlier snapshot of the PCGN Note 5 and dependent-vowel closeouts; later mainline PCGN table, coda-class tests and source registry supersede it.
- `docs/pcgn-candidate-parity-row7-foot-delta-closeout-2026-11-19`, `docs/pcgn-profile-delta-row7-final-closeout-2026-11-19`, `docs/pcgn-row7-and-profile-delta-closeout-2026-11-19`, and `docs/pcgn-row7-source-registry-parity-ci-closeout-2026-11-19`: documentation-only checkpoints for PRs #421/#422/#424/#425/#427/#430. Current main already contains the PCGN-specific `ស` foot behavior, exact row-7 source sequence `េ+ា+ះ`, and row-specific comparison/source-registry parity; the stale candidate-shaped `ោ+ះ` key and superseded parity approaches must not be reintroduced. No code/test path unique to these refs was found.
- `docs/pcgn-ungegn-row-comparison-closeout-2026-11-19`: older comparison/closeout snapshot. Current main's rule-diff and machine-readable comparison already record the profile differences and candidate-only extensions; no unique implementation or evidence needs porting.

The targeted source check confirms `src/khmer_ua/pcgn.py` defines `PCGN_WEAK_SUBSCRIPTS = frozenset("ងញណនមយរលវ")`, excluding `ស`; the current resolver therefore lets `ស` determine the series under PCGN Note 3. The existing structural `គ្ស` regression is documented in the rule-diff. This is already implemented and tested; no runtime patch was warranted. The older branch snapshots that describe the delta as PARTIAL or retain the UNGEGN neutral-set behavior are stale relative to main.

All ten refs changed documentation paths only; no historical branch was merged, deleted or force-updated. This is a targeted content review, not full per-file/commit/PR-ancestry reconciliation of every documentation ref. Fresh paginated inventory after PR #443: **317 refs, 317 unique names, 317 unique tip SHAs, including 139 `docs/*` refs**; no open PRs at inventory time. `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.


### Historical post-merge documentation branch family — PR #206–#259 snapshots

A further 29 retained `docs/post-pr*` refs were compared with current `main`: #206, #209, #211, #213, #215, #217, #218, #219, #220, #221, #222, #223, #224, #226, #228, #230, #231, #233, #235, #237, #239, #241, #243, #245, #247, #250, #252, #255, #256 and #259 (29 refs total). Each compare is limited to canonical handoff, repository-audit and linguistic-register documentation; all except #206 also carry an earlier `docs/romanization-to-ukrainian-matrix.md` snapshot. No source-code or test path appears in these branch diffs.

The matrix snapshots range from 334 to 841 lines, compared with 541 lines on current main. Every inspected branch matrix is a strict line subset of current main except two historical-only statements: #215 describes the then-unimplemented Note 2 shifter abstention, now superseded by later source-backed resolver behavior; #223 records exact-main workflows as still running, an obsolete point-in-time CI status. No branch-only mapping or acceptance rule was found that is absent from the current matrix. These branches are therefore historical checkpoints, not implementation candidates; do not merge their older matrix or status text.

The branch names above are 29 refs; the sweep used changed-path comparisons for all and line-level matrix subset checks for #209–#259. This is not full commit/PR-ancestry reconciliation. Retain all refs unchanged. `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.


## PR #444 closeout and post-merge documentation-ref sample — 2026-11-19

PR [#444](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/444) merged by squash as `e78da940dbff2a07376f6ae9cb0b4cc4cd8b6603`; exact PR head `3d86b3d1779a971eb7f60b591ac08f42087c889a` passed both Quality checks and Chromium browser smoke. Exact-main Quality [44558019475](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44558019475) and Chromium [44558019636](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44558019636) passed; Pages build/deploy [44558019521](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44558019521) was still running at the time of this update.

A further ten historical refs were compared with current main: `docs/post-pr294-mainline-verification-2026-11-16`, `docs/post-pr300-mainline-handoff-2026-11-16`, `docs/post-pr314-mainline-closeout-2026-11-17`, `docs/post-pr316-mainline-closeout-2026-11-17`, `docs/post-pr319-expert-shortlist-closeout-2026-11-17`, `docs/post-pr353-mainline-closeout-2026-11-18`, `docs/pr322-mainline-verification-2026-11-17`, `docs/pr334-final-mainline-verification-2026-11-17`, `docs/pr336-exact-main-closeout-2026-11-17`, and `docs/pr355-post-merge-closeout-2026-11-18`. Every diff is limited to canonical documentation. The #294 branch additionally carries an older Unicode grammar audit snapshot; current main supersedes its parser commit/CI checkpoint and includes the later TN #61 v2 metadata/rights boundary. The #353 branch additionally carries an old benchmarking note claiming a 29,204-entry native-validated CC BY-SA dictionary; current pinned evidence records the 29,204/33,091 count and license-scope conflict, only a six-line public sample, and no full dictionary artifact. That old statement is not safe to re-import. The remaining branches are historical handoff/audit/register snapshots with no unique runtime or test changes.

No code, test, source-registry, corpus, IPA or Ukrainian mapping patch was found in this sample. All refs are retained unchanged. This is targeted content disposition only; complete commit/PR ancestry reconciliation across all historical refs remains **PARTIAL** under `KHM-BRANCH-AUDIT-001`.


### PR closeout documentation refs — #357–#393

Ten additional refs were compared with current main: `docs/pr357-upstream-audit-closeout-2026-11-18`, `docs/pr359-post-merge-closeout-2026-11-18`, `docs/pr362-pr363-postmerge-closeout-2026-11-18`, `docs/pr366-postmerge-closeout-2026-11-18`, `docs/pr367-final-mainline-closeout-2026-11-18`, `docs/pr378-final-mainline-closeout-2026-11-18`, `docs/pr389-accessibility-landmarks-closeout-2026-11-18`, `docs/pr390-closeout-exact-main-2026-11-18`, `docs/pr392-accessibility-whitespace-closeout-2026-11-18`, and `docs/pr393-canonical-closeout-2026-11-18`. Every compare changes only the three canonical documentation files. A line-level check of the handoff file found **zero branch-only lines** for all ten refs: each is a strict historical subset of current main. No source, code, test or evidence port is applicable. This independently confirms that the older upstream-audit and accessibility closeout notes are already represented in the canonical handoff.

Retain these branches unchanged. This is targeted path/content reconciliation, not complete commit/PR ancestry audit. `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.


### Test-branch family reconciliation — 2026-11-19

A targeted compare/content pass covered 25 retained `test/*` refs: the keyboard/responsive, landmark/name, whitespace, grapheme-accounting, IPA display, Khmer numeral, onset-fallback, romanization adapter/matrix/whole-message, vowel alias/crosswalk, BA+AA shifter/vowel, BA+AA+foot Note 3, PCGN candidate-registry parity, exact component sequence, row-7 anchor, `ស`-foot, SAMYOK coda-class, shifter-codepoint, source-sequence parity, and unconverted-mark regression branches. No test-only change in these refs is missing from current main.

Specific dispositions:
- The onset-fallback fixture, browser/Python source paths and regression file are byte-identical between the inspected branch and main.
- The IPA display contract test is byte-identical.
- The old grapheme-accounting parser/test branch is superseded by the current richer structural parser; its old single rejection test is covered by current explicit unit-isolation/unsupported-material tests.
- Old romanization/numeral branches are earlier adapter snapshots; main has the later diacritic-preserving direct-input contract, whole-message API and larger regression suite.
- Old BA/AA integration fixtures contain pre-correction PCGN vowel values (including the earlier row 3/16/17 values); current main has the corrected source rows and CSV/runtime parity. Old candidate-parity tests that require all row keys or all separators to match are superseded by the row-specific rule: row 7 is `VALUE_MATCH_KEY_SHAPE_DIFFERS`, while only rows with identical source component boundaries require exact grouping.
- The `test/pcgn-s-foot-not-neutral`, SAMYOK coda-class and source-sequence parity branch test contents are subsets of current main; one SAMYOK branch is byte-identical. The unconverted-mark port branch has no diff from main.

All historical test refs are retained unchanged. These targeted comparisons establish no missing tests in this sample; they do not complete full commit/PR ancestry reconciliation of all branches. `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.

Correction to the earlier time-bounded status: Pages/deploy run [44558019521](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44558019521) subsequently completed **SUCCESS** on exact main SHA `e78da940dbff2a07376f6ae9cb0b4cc4cd8b6603`. Quality [44558019475] and Chromium [44558019636] on that same SHA were already confirmed **SUCCESS**.


### Early romanization/source-registry documentation refs — 2026-11-19

Ten further refs were compared: `docs/khmer-1997-profile-evidence-reconciliation-2026-11-12`, `docs/phonotactic-research-closeout-2026-11-15`, `docs/khmer-letter-inventory-handoff-2026-11-12`, `docs/khmer-numeral-crosswalk-closeout-2026-11-12`, `docs/khmer-onset-registry-mainline-closeout-2026-11-17`, `docs/khmer-short-vowel-sequence-test-closeout-2026-11-12`, `docs/khmer-vowel-matrix-crosswalk-closeout-2026-11-12`, `docs/khmer-whole-message-adapter-closeout-2026-11-12`, `docs/khmer-romanization-runtime-postmerge-2026-11-12`, and `docs/khmer-romanization-test-closeout-2026-11-12`.

All changes are documentation, except two historical source-registry snapshots. A structural comparison of `data/khmer/sources.json` found 29 source IDs on the #1997 profile branch and **zero IDs absent from current main**; current main has 49 entries, including later Unicode 18, phonetic-source and rights-scope updates. The older romanization matrices (192–248 lines in these refs) are superseded by the 944-line current matrix. Their old claims that the national 1997 profile was merely unlocated or that the adapter handled only ASCII are superseded by the current 2023 provisional Gazetteer evidence boundary and diacritic-preserving direct BGN/PCGN input contract. The old `docs/phonology.md` snapshot has no branch-only lines; current main adds the typed IPA-kind contract. The onset-registry and letter-inventory refs add no unique source IDs or implementation.

No branch-only source ID, runtime rule, test or evidence needs porting. Retain all refs unchanged. This is targeted content/source-ID reconciliation, not full ancestry review; `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.


### Additional PCGN assembly and direct-input documentation refs — 2026-11-19

Ten more refs were compared with current main: `docs/pcgn-alif-assembly-closeout-2026-11-16`, `docs/pcgn-alif-closed-assembly-closeout-2026-11-16`, `docs/pcgn-alif-note5-closeout-2026-11-16`, `docs/pcgn-independent-vowel-assembly-closeout-2026-11-16`, `docs/pcgn-omitted-shifter-mainline-closeout-2026-11-18`, `docs/pcgn-shifter-registry-closeout-2026-11-18`, `docs/pcgn-shortened-mark-mainline-closeout-2026-11-15`, `docs/pcgn-branch-inventory-current-main-2026-11-19`, `docs/direct-romanization-input-closeout-2026-11-15`, and `docs/khmer-fallback-parity-mainline-closeout-2026-11-17`. All diffs touch canonical documentation only, plus older romanization matrix snapshots on six refs.

The four near-current PCGN assembly matrix snapshots (888–932 lines) are strict line subsets of current main's matrix; no branch-only mapping or evidence exists. The old shortened-mark matrix is likewise a subset. The direct-input matrix is an earlier 265-line snapshot; its two branch-only statements are superseded by the current explicit BANTOC/SAMYOK source inventory and expanded glyph/context status. The omitted-shifter, shifter-registry, branch-inventory and fallback-parity refs are historical handoff/audit/register snapshots; no code or test change is unique.

Retain all ten refs unchanged. This extends targeted documentation sampling but does not complete the full historical ancestry audit. `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.


### Repository architecture, deployment and handoff documentation refs — 2026-11-19

Ten further refs were compared: `docs/ipa-validator-merge-closeout-2026-11-15`, `docs/typed-hybrid-bridge-closeout-2026-11-15`, `docs/repository-information-architecture-2026-11-15`, `docs/final-pr320-mainline-closeout-2026-11-17`, `docs/final-site-deployment-handoff-2026-10-21`, `docs/github-pages-live-service-2026-11-16`, `docs/grapheme-accounting-handoff-2026-11-12`, `docs/mark-inventory-and-mainline-reconcile-2026-11-15`, `docs/mixed-script-romanization-closeout-2026-11-15`, and `docs/skip-navigation-closeout-2026-11-17`.

The two IPA/hybrid closeouts, final PR #320 closeout, site-deployment handoff, grapheme-accounting handoff and skip-navigation closeout change only canonical status documentation. The repository-information-architecture branch changes AGENTS/README/docs index/agent maps/architecture as well as status docs, but the inspected AGENTS, docs index, codebase map, methodology references and handoff content are line subsets of current main. Its README has only older romanization/mark wording, its architecture adds two now-superseded scope statements, and its repository-audit adds one stale PR #64 status. The Pages/mark-inventory/mixed-script README variants likewise contain only older wording; their sole branch-only bullet fragments are superseded by the current README and source registry. No unique implementation or active requirement was identified.

Retain these refs unchanged. This is targeted path/content comparison, not full PR/commit ancestry reconciliation. `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.


A final data-level check of the PCGN candidate-parity test branches confirmed the stale row-7 hazard: `test/pcgn-candidate-diff-source-registry-parity-2026-11-19` still has a CSV row with the candidate-shaped `ោ+ះ` and comparison `MATCH`. Current main instead pins the official PCGN `េ+ា+ះ` source sequence and records `VALUE_MATCH_KEY_SHAPE_DIFFERS` against the candidate's `ោះ`. The three later test branches' CSV files are byte-identical to main. This confirms the stale branch must not be ported.


### Exact-main and branch-audit checkpoint refs — 2026-11-19

Ten additional refs were compared: `docs/correct-main-quality-count-2026-11-16`, `docs/current-main-branch-inventory-2026-11-16`, `docs/exact-main-369e0-ci-complete-2026-11-19`, `docs/exact-main-checkpoint-2026-11-16-evening`, `docs/exact-main-research-register-2026-11-16`, `docs/extend-docs-branch-semantic-spot-audit-2026-11-19`, `docs/extend-historical-docs-spot-audit-2026-11-19`, `docs/final-2026-11-19-mainline-ci-and-branch-status`, `docs/final-mainline-checkpoint-1cc833a-2026-11-15`, and `docs/final-mainline-checkpoint-2026-11-15`.

All ten diffs are limited to the canonical handoff, repository audit and/or linguistic completion register. A line-level comparison found **zero branch-only lines** in each handoff snapshot: all content is already present in current main. Their inventory counts, workflow states and checkpoint SHAs are historical point-in-time records and must not be used as current status. No code, source, test or evidence change is unique to these refs. Retain all refs unchanged; this remains targeted content review, not full PR/commit ancestry reconciliation. `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.


### Live inventory after the current audit batch — 2026-11-19

Fresh paginated GitHub inventory: **319 branch refs, 319 unique names, 319 unique tip SHAs; 141 refs use the `docs/*` prefix**. Exactly one PR is open: #445, which carries this documentation-only audit batch. No branches were deleted, rewritten or force-updated. The count is a live inventory, not a completion percentage; `KHM-BRANCH-AUDIT-001` remains **PARTIAL** because not all historical refs have had full semantic and PR/commit-ancestry reconciliation.


## PR #445 closeout and Unicode 18 parser handoff branch reconciliation — 2026-11-19

PR [#445](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/445) merged as `3663ea20e58510a0a36b5c521627fcacf1c4951b`; exact PR head `b27844f3d02e2c38097da40aa3ab2a22aa55592a` passed both Quality checks and Chromium. All three exact-main workflows on merge SHA `3663ea20...` subsequently passed: Quality [44561793874](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44561793874), Pages/deploy [44561793851](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44561793851), and Chromium [44561793861](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44561793861).

Four retained parser handoff/state refs were compared: `docs/khmer-parser-final-handoff-2026-11-16`, `docs/khmer-parser-final-state-2026-11-16`, `docs/khmer-parser-final-state-v2-2026-11-16`, and `docs/khmer-unicode18-parser-final-handoff-2026-11-16`. The first three modify canonical docs only. The Unicode 18 handoff additionally changes `data/khmer/sources.json`, `tests/test_rule_registry_provenance.py`, references, parser/LOC audit notes and the romanization matrix.

The older source registry has 46 entries; its only branch-only identifier is `unicode-tn61-v2`, superseded by current main's `unicode-tn61-khmer-encoding-structure-v2`. Current main's registry has 49 entries and four later sources absent from that snapshot. The branch-only provenance test asserts the old ID; current main tests the canonical renamed ID. No source identity is lost.

The branch's parser/LOC docs describe an earlier component-scanner-only state and mark BNF parsing TODO; current main has the Unicode 18 §16.4 packed parse forest DONE_VERIFIED, exact code-point rejection spans, Python/browser parity, and explicit separation from LOC word division and TN #61 v2. Current tests still cover the `ហើ្យ` vs `ហើយ` boundary contrast, 2^20 packed derivations, parse/segmentation counts and rejected spans. No code, source ID or test needs porting. Retain refs unchanged. This is targeted content review; full historical ancestry audit remains **PARTIAL**.


### Mainline/PCGN closeout and audit-register refs — 2026-11-19

Ten more refs were compared: `docs/mainline-checkpoint-89e5ba4-2026-11-15`, `docs/mainline-ci-closeout-2026-11-15`, `docs/historical-branch-audit-closeout-2026-11-15`, `docs/fix-exact-main-quality-count-2026-11-16`, `docs/record-pcgn-anusvara-assembly-port-2026-11-18`, `docs/record-pr440-mainline-ci-and-branch-audit-2026-11-19`, `docs/pr430-pcgn-parity-closeout-2026-11-19`, `docs/finalize-external-source-audit-2026-11-17`, `docs/final-sok-ipa-kind-verification-2026-11-17`, and `docs/pcgn-robat-closeout-2026-11-16`.

All changes are canonical documentation only; the exact-main quality-count branch has no file diff. Nine handoff snapshots are strict line subsets of current main. The #430 closeout branch has an older PCGN fix-family disposition and 305-ref inventory snapshot; current main contains the same substantive branch dispositions in its later PCGN branch-family closeout, with refreshed 306/308/319-ref inventories. Its old count/status is historical and must not replace the current inventory. The PCGN RoBat matrix snapshot is also a strict subset of current main. No code, test, source or evidence patch needs porting. Retain all refs unchanged; full historical ancestry audit remains **PARTIAL**.


### Data/evidence branch reconciliation — 2026-11-19

The four retained `data/*` refs were compared with current main:
- `data/integrate-positional-onset-evidence-register-2026-11-17` has no diff from main.
- `data/khmer-onset-evidence-registry-2026-11-17` changes the onset evidence JSON, schema, provenance test and audit docs relative to its merge base, but each of those four artifacts is byte-identical to current main. No evidence row or schema/test change is missing.
- `data/pcgn-independent-vowel-source-register-2026-11-16` and `data/pcgn-independent-vowel-source-register-mainline-2026-11-16` both carry CSV and resolver-test blobs byte-identical to current main.

No data, provenance, schema or test patch needs porting. The onset registry remains `PARTIAL_SPECIALIST_REFERENCE_REGISTER` and cannot promote its 33 onset hints to adjudicated IPA or accuracy evidence. Retain all refs unchanged.


## Audit-branch and PCGN candidate-comparison reconciliation — 2026-11-19

- Compared nine retained audit refs against current main: `audit/non-pcgn-fix-semantic-review-2026-11-19`, `audit/complete-feature-and-test-branch-reconciliation-2026-11-17`, `audit/complete-fix-and-release-branch-reconciliation-2026-11-17`, `audit/complete-research-branch-family-reconciliation-2026-11-17`, `audit/reconcile-audit-pr-ancestry-2026-11-18`, `audit/reconcile-data-branch-pr-ancestry-2026-11-18`, `audit/reconcile-feature-pr-ancestry-2026-11-18`, `audit/reconcile-test-branch-pr-ancestry-2026-11-18`, and `audit/reconcile-research-pr-ancestry-2026-11-18`. All three canonical documents on each ref contain zero branch-only lines versus main. These are superseded documentation snapshots; no content needs porting. This does not validate their claimed ancestry coverage independently.
- Inspected `audit/pcgn-ungegn-vowel-row-reconciliation-2026-11-19`, which is 3 commits ahead / 21 behind main and changes the comparison CSV, rule-diff audit, and its test. Its CSV differs from current main only in PCGN anusvara/visarga row 7: the old branch labels it `MATCH`, while current main correctly records `VALUE_MATCH_KEY_SHAPE_DIFFERS` because PCGN source `េ+ា+ះ` and candidate key `ោះ` have matching Latin values but different source structures. The branch's 57-line test predates current main's 127-line test and lacks the row-7 structural-difference assertion and cross-checks against project-owned PCGN registries. Do not merge or port this stale snapshot; current main is more precise.
- `audit/non-pcgn-fix-semantic-review-2026-11-19` was also checked at the three canonical document paths; all branch content is already present on main (zero branch-only lines). Its name does not imply unique implementation changes.
- All reviewed branches remain untouched. This is targeted branch-content reconciliation, not a full PR ancestry or every-commit semantic audit. `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.


### Additional audit-family continuation refs

Nine further audit refs were compared with current main: `audit/continue-pcgn-branch-reconciliation-2026-11-17`, `audit/continue-pcgn-note-and-special-syllable-branch-reconciliation-2026-11-17`, `audit/continue-pcgn-vowel-and-syllable-branch-reconciliation-2026-11-17`, `audit/continue-typed-ipa-and-coverage-branch-reconciliation-2026-11-17`, `audit/closeout-late-docs-branch-family-2026-11-18`, `audit/complete-docs-branch-family-reconciliation-2026-11-17`, `audit/continue-historical-branch-reconciliation-2026-11-17`, `audit/reconcile-benchmark-ci-branch-family-2026-11-18`, and `audit/reconcile-fix-release-branch-family-2026-11-18`. All nine handoff files have zero branch-only lines against main. `audit/complete-remaining-branch-families-2026-11-17` has no diff from main at all. These are superseded audit snapshots; no unique code, test, source or documentation content needs porting. This does not prove their claimed full ancestry coverage. Retain all refs; `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.


## Research-branch snapshot reconciliation and exact-main CI — 2026-11-19

PR [#448](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/448) merged as `47b3be71478c5a6948a2c66c4761cce9310a5fcb`. Exact PR-head Quality and Chromium passed. All four checks on exact merged main also passed: Quality [44565926529](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44565926529), browser [44565926669](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44565926669), Pages/deploy [44565926377](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44565926377) (build + deploy).

A targeted sample of the retained `research/*` family was reconciled:
- Ten source-registry snapshots (#complete-external-G2P, Google lexicon, acoustic-model release, IPA convention v1/v2, Kirby cluster audio, Kirby tonogenesis, source-audit integration, LOC word division, MekongPhon release-rights) each had **zero branch-only source IDs** relative to the current 49-entry `data/khmer/sources.json`. Current main contains later source entries and canonical IDs; no source record needs porting.
- The external IPA renderer branch's schema and registry test are byte-identical to main; its 5.4 KB registry is an older subset of the current 25.8 KB registry. Do not replace the expanded current inventory with it.
- The Khmer hybrid-engine branch carries the earlier v1 adapter and smaller tests. Current main has v2 typed IPA validation, explicit profile/kind/status/uncertainty, provider priority, and strict rejection of bare strings. The old branch's transport-normalization helper and untyped candidate acceptance must not be reintroduced.
- The older benchmark-expansion branch's runner accepts a user-overridable model ID and lacks the later pinned corpus-source-commit argument. Current main's MekongPhon diagnostic harness and tests are byte-identical to the dedicated `research/mekongphon-diagnostic-harness` branch and retain pinned model/source provenance, no raw text in reports, no independent accuracy claim, and optional dependencies.
- The old PCGN note-registry branch has a 10-row snapshot; current main has a larger source-backed registry and test, including later note-specific rows and stronger assertions. The old test also lacks the current per-row acceptance boundary.
- These are stale historical snapshots, not implementation candidates. No code, source IDs, tests or benchmark changes were ported.

This sample does not complete the full 29-ref research branch family review or full PR/commit ancestry audit. All refs remain untouched; `KHM-BRANCH-AUDIT-001` remains **PARTIAL**. Research claims remain evidence-limited: MekongPhon is diagnostic only; IPA gold remains 0 and accuracy null.


## Fix-branch implementation reconciliation — 2026-11-19

A targeted review covered the non-PCGN `fix/*` family:
- `fix/explicit-ipa-kind-in-phonetic-result`: the phonetic-result adapter is byte-identical to main; the branch's rule-engine snapshot predates current `NON_LINGUISTIC` numeric passthrough and associated IPA-kind handling.
- `fix/flag-unconverted-khmer-romanizer-output`: the JavaScript adapter is byte-identical to main.
- `fix/ipa-tie-bar-segment-boundaries`: both IPA implementation and its tests are byte-identical to main.
- `fix/khmer-benchmark-reproducibility`: its 154-line benchmark harness is superseded by the 257-line current provenance-aware diagnostic; current code preserves hashes, environment, and explicit no-gold/no-accuracy boundaries.
- Parser diagnostics/rejection-span refs are older snapshots. Current main has the fuller orthographic parser and test suite, including fail-closed unsupported code points, exact rejected spans for known nonconforming order, ambiguity/parse-count preservation and packed-forest tests. The `fix/khmer-rejected-span-reasons-and-fixtures` test file is byte-identical to main.
- `fix/khmer-typed-partial-phonetic-results` predates current numeric passthrough; its old partial-result path is superseded by current typed result handling.
- `fix/khmer-unmodeled-letter-trace` signs registry and `fix/mixed-script-numeral-token-boundaries` parser/test are byte-identical to main.
- `fix/mixed-script-romanization-guard` is an older output guard; main uses a shared `bracketUnconvertedKhmer` helper at both whole-message and token paths. The older romanization tests are a strict subset of current tests.

No unique accepted implementation or regression test needs porting. These refs remain unchanged. This is targeted blob/test comparison; the full fix/release family and PR ancestry review remains **PARTIAL** under `KHM-BRANCH-AUDIT-001`.


## Feature-branch snapshot reconciliation and correction of historical blob note — 2026-11-19

PR #450 merged as aeb0bfbaabc47d8658527da4c5634fae12e9faec; exact PR-head Quality and Chromium passed. Exact-main Quality, Chromium and Pages/deploy were still running when this note was drafted; do not infer success until their exact-SHA checks complete.

A targeted review covered ten feature refs:
- feat/khmer-unicode18-syllable-parser is an earlier linear/limited parse representation; current main has the packed parse forest, grammar-role ambiguity, and separate parse/segmentation counts.
- feat/typed-ipa-candidate-validation has an older IPA tie-bar validator; current main has explicit pending-tie-bar state and rejects a tie bar without a following segment. feat/typed-ipa-hybrid-bridge hybrid implementation is byte-identical to current main.
- feat/khmer-ukrainian-practical-adapter-final practical adapter and feat/khmer-romanization-ukrainian-matrix-completion Ukrainian matrix are byte-identical to current main.
- feat/khmer-subscript-independent-vowels contains an older parser; current main uses the later orthographic component scanner and mixed-script token boundaries.
- The historical feat/pcgn-anusvara-visarga-syllable-assembly-port and feat/pcgn-explicit-open-syllable-assembly snapshots contain an obsolete BA+TRIISAP p-in-â exception. Current main correctly records the PCGN Note 2 BA+TRIISAP no-shift exception and reserves Note 3 p-in-â for BA+MUUSIKATOAN or BA+foot. Their PCGN source/schema/test snapshots are older, not byte-identical, and must not be ported.

Correction to an earlier repository-audit note (around line 1774): it previously stated that the feat/pcgn-anusvara-visarga-syllable-assembly-port branch's PCGN source/schema/test files were byte-identical to main. A fresh comparison of the current live branch tip disproves that: src/khmer_ua/pcgn.py, its assembly schema and assembly test all differ. The package __init__.py is byte-identical. The old code carries the obsolete BA+TRIISAP p-in-â case; current main supersedes it with the Note 2 no-shift distinction. This is a current-tip correction, not evidence that main lost accepted behavior.

No unique accepted implementation needs porting. All feature refs remain unchanged. Full feature-family semantic/ancestry reconciliation remains PARTIAL under KHM-BRANCH-AUDIT-001.


Correction to the time-bounded CI note above: exact-main checks on aeb0bfbaabc47d8658527da4c5634fae12e9faec subsequently completed successfully. Quality run 44568314352, Chromium run 44568314381, and Pages build/deploy run 44568314462 all report SUCCESS. A later Quality retry 44568901376 also passed. The exact-main gate for PR #450 is therefore DONE_VERIFIED.


### Live branch inventory at PR #451 pre-merge checkpoint — 2026-11-19

Paginated GitHub branch inventory: **325 refs, 325 unique names, 325 unique tip SHAs; 142 docs/* refs**. Prefix counts: a11y 2, audit 44, benchmark 1, ci 1, data 4, docs 142, feat 50, fix 24, release 1, research 29, test 26, plus one unprefixed ref. Exactly one PR was open at this checkpoint: #451. This is a timestamped inventory, not a branch-audit completion claim. KHM-BRANCH-AUDIT-001 remains PARTIAL.


## Audit-branch snapshot reconciliation and PR #451 — 2026-11-19

PR #451 merged as `89a2152b48a73d725fde607f28e503ca274f45f5`; PR head `ec544141a40d8e1a440bdbc37c31b62328f69ee6` had passing Quality and Chromium checks. Exact-main checks for the new merge were still in progress at the time of this entry; do not infer their result from PR-head checks.

A further 14 audit refs were compared with current main: `audit/closeout-late-docs-branch-family-2026-11-18`, `audit/complete-docs-branch-family-reconciliation-2026-11-17`, `audit/continue-historical-branch-reconciliation-2026-11-17`, `audit/continue-pcgn-branch-reconciliation-2026-11-17`, `audit/continue-pcgn-note-and-special-syllable-branch-reconciliation-2026-11-17`, `audit/continue-pcgn-vowel-and-syllable-branch-reconciliation-2026-11-17`, `audit/continue-typed-ipa-and-coverage-branch-reconciliation-2026-11-17`, `audit/current-branch-inventory-2026-11-16`, `audit/final-branch-inventory-closeout-2026-11-17`, `audit/final-session-closeout-2026-11-18`, `audit/post-pr379-live-inventory-closeout-2026-11-18`, `audit/post-pr380-final-verification-closeout-2026-11-18`, `audit/post-pr381-mainline-ci-closeout-2026-11-18`, and `audit/pr153-diff-reconciliation-2026-11-15`. All diffs are limited to canonical documentation. A line-level handoff comparison found zero branch-only lines in all 14 refs; no unique audit result or implementation requires porting. `audit/complete-remaining-branch-families-2026-11-17` is exactly at an ancestor of current main with no file diff.

The distinct `audit/pcgn-ungegn-vowel-row-reconciliation-2026-11-19` branch is not safe to reuse as a current snapshot. Its CSV retains the old PCGN anusvara/visarga row 7 full-`MATCH` classification and its test asserts all eight rows match. Current main correctly classifies row 7 as `VALUE_MATCH_KEY_SHAPE_DIFFERS`: the PCGN source sequence is `េ+ា+ះ`, while the candidate UNGEGN key is `ោះ`; Latin values match, source key shape does not. Current main also has stronger row-specific and source-registry assertions. The branch's older rule-diff note predates the source-sequence correction. No code/test patch should be ported from this stale branch.

PR #451's feature-branch audit note is retained on main: it corrects an earlier inaccurate claim that the live PCGN syllable-assembly feature branch was byte-identical to main. The old branch carries the superseded BA+TRIISAP p-in-â behavior; current main preserves PCGN Note 2 no-shift for BA+TRIISAP and Note 3 p-in-â only for BA+MUUSIKATOAN or BA+foot.

All inspected historical refs remain untouched. These are targeted changed-path/blob checks, not complete commit/PR ancestry review. `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.


### Remaining audit-branch family and optional workflow snapshot — 2026-11-19

Thirteen further audit refs were compared with current main: `audit/pr384-ipa-tie-bar-closeout-2026-11-18`, `audit/pr385-exact-main-closeout-2026-11-18`, `audit/pr387-accessibility-smoke-closeout-2026-11-18`, `audit/reconcile-accessibility-ci-benchmark-docs-2026-11-18`, `audit/reconcile-audit-branch-family-2026-11-18b`, `audit/reconcile-audit-branch-family-2026-11-18`, `audit/reconcile-benchmark-ci-branch-family-2026-11-18`, `audit/reconcile-docs-branch-pr-ancestry-2026-11-18`, `audit/reconcile-fix-release-branch-family-2026-11-18`, `audit/reconcile-research-branch-family-2026-11-18`, `audit/reconcile-selected-historical-branch-content-2026-11-17`, `audit/refresh-branch-inventory-2026-11-17`, and `audit/refresh-live-inventory-and-reconcile-pcgn-port-2026-11-18`. All diffs are canonical documentation only. A line-level handoff check found zero unique lines in 12 refs; the selected-historical branch's only two unique lines are a stale 211-ref/zero-open-PR snapshot and a historical PARTIAL statement. No unique current implementation or audit evidence needs porting.

The `audit/restore-pinned-khmer-phonemizer-smoke-2026-11-18` branch diff lists an added optional workflow, but its workflow blob is byte-identical to current main (`.github/workflows/optional-khmerphonemizer-smoke.yml`, SHA `a89a848d66810225bbcc2cc5c9143b94304a680d`). It is already present on main; no workflow port is needed. This branch also contains only documentation differences in the inspected canonical files.

The remaining audit refs were preserved. The exact-main checks for PR #451 merge SHA `89a2152b48a73d725fde607f28e503ca274f45f5` were still running at this entry; verify before claiming its mainline gate. `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.


## Research-branch family reconciliation — 2026-11-19

A targeted changed-path review covered all 29 retained `research/*` refs. Their code/data/document snapshots were compared against current main where the changed paths indicated a possible implementation or evidence delta.

### Dispositions

- The pinned external IPA renderer registry and schema are already on main; the schema blob is identical, and main's renderer registry is substantially expanded (25,779 chars versus the old 5,457-char snapshot).
- The research branches' external source-registry additions are all subsets of the current 49-entry `data/khmer/sources.json`; a check of 13 source-bearing branches found **zero branch-only source IDs**. Current main includes later Unicode, profile and rights-boundary records.
- The old MekongPhon hybrid/rule-engine snapshots are superseded by the current larger evidence-gated typed IPA adapter and deterministic engine. The old benchmark scripts are superseded by the current pinned implementation; the test snapshot is byte-identical to main in the checked case, while main has additional duplicate-orthography and missing-reference guards.
- The older optional benchmark workflow includes a separate raw Khmer Phonemizer run over 100 upstream MekongPhon evaluation rows, creating a source-attested (not independently adjudicated) corpus. It was not ported: this would add an unadjudicated upstream evaluation corpus and a second model run, while current main already has a manually dispatched, pinned neural diagnostic that emits raw output without copying source corpus rows. No accuracy claim or gold promotion is justified; source rights remain a separate gate.
- The IPA convention draft, Kirby cluster-audio audit, Kirby tonogenesis audit, phonetic literature full-text review and PCGN/UNGEGN research content are present on main as matching blobs where checked.
- The lexical segmentation audit has since been expanded on main with the exact NOVA guideline semantics (word tokens are generally morpheme-level, while compounds use a separate shallow-bracketing convention); its older generic tokenization caution is superseded.
- The Unicode 18 Khmer grammar audit is expanded on main to record the implemented packed BNF parse forest and ambiguity/role assignments. The older branch's TODO parser contract is stale. TN #61 v2 remains separately versioned and non-normative.
- The Sok-Adams audit on main expands the visual table review and explicitly blocks direct rule transfer pending target-profile approval, complete source transcription and rights; the old branch's generic TODO is superseded.
- LOC word-division evidence on main includes the profile-neutral boundary evidence contract and subsequent Unicode structural parser integration. This does not amount to a lexical segmenter or approved LOC profile.

No research branch-only source ID or accepted runtime behavior was identified for porting. Research branches are preserved unchanged. These are targeted blob/content checks, not a full commit/PR-ancestry review; `KHM-BRANCH-AUDIT-001` remains **PARTIAL**. External gold recruitment, IPA convention approval, independent annotation and rights review remain genuine blockers.


## Data and fix branch reconciliation — 2026-11-19

Targeted comparisons covered all four retained `data/*` refs and the current PCGN/Unicode-related `fix/*` family.

- `data/integrate-positional-onset-evidence-register-2026-11-17` is an ancestor with no diff. The positional-onset evidence JSON, schema and test in `data/khmer-onset-evidence-registry-2026-11-17` are byte-identical to current main (827, 233 and 84 lines). Both independent-vowel CSV snapshots are the same 14-line file already on main.
- The row-7 source-pattern fix branch has the same runtime and decision-schema blobs as main. Its sibling comparison test is older; main adds source-registry parity and the `VALUE_MATCH_KEY_SHAPE_DIFFERS` row-7 guard.
- BA/TRIISAP source matrix and dependent-vowel rows 16–17 CSVs are byte-identical to main.
- `fix/pcgn-dependent-i-o-series-2026-11-19` is stale: it gives row 16 O-series `aô` instead of `oŭ`, row 17 `au` instead of `ŏu`, and retains the obsolete two-component row-7 `ោ+ះ` key instead of PCGN's three-component `េ+ា+ះ`.
- `fix/pcgn-final-consonant-context-types-2026-11-16` and `fix/pcgn-omitted-shifter-uncertainty-2026-11-18` retain the superseded BA+TRIISAP p-in-â exception. Current main follows PCGN Note 2 no-shift for BA+TRIISAP and reserves Note 3 p-in-â for BA+MUUSIKATOAN or BA+foot.
- `fix/pcgn-shifter-registry-codepoint-alignment-2026-11-18` also has old dependent-vowel values and the old row-7 key. The shortened-mark inventory and TN #61 source metadata blobs match main.

No code/data/test patch from these refs is missing from current main. All refs remain untouched. This is targeted blob/content evidence, not full branch/PR ancestry reconciliation; `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.


## Feature-branch family reconciliation — 2026-11-19

A changed-path review covered all **50 retained `feat/*` refs**, including the Unicode 18 parser/parse-forest work, rejected-span diagnostics, direct BGN/PCGN input, coverage dashboard, external G2P diagnostics, IPA renderer fallback, practical Ukrainian adapter/matrix, typed IPA validation/hybrid bridge, profile-neutral word-boundary interface, and the PCGN component/note/syllable-assembly branches.

### Current-main dispositions

- Parser/scanner/BNF/packed-forest/rejected-span branches are earlier implementations. Current main contains the Unicode 18 BNF parser, packed grammar-role alternatives, exact offsets, reconstruction, typed rejections and Python/browser parity. The old linear or partial parser snapshots are not port candidates.
- Direct romanization, Ukrainian matrix and practical adapter snapshots are older than current main's diacritic-preserving direct-input and practical IPA-to-Ukrainian contracts. Current tests and data matrices are more complete.
- Typed IPA candidate validation and hybrid bridge snapshots predate the current explicit tie-bar-following-segment validation and evidence-gated typed candidate adapter. The current deterministic rule engine remains the only final-output authority; external results remain diagnostics.
- Coverage report/dashboard and renderer registry snapshots are superseded by current main's internal/public coverage reports, build-time dashboard integration and expanded renderer registry. The checked coverage JSON is byte-identical; main's coverage script includes additional public-report/drift behavior.
- PCGN component, vowel, note and syllable-assembly branches are historical slices of the now-integrated resolver. Current main has broader schemas, source registries, structural assembly contracts and regression coverage. Several old snapshots encode the superseded BA+TRIISAP p-in-â exception and/or pre-correction dependent-vowel values and row-7 key. Do not port those old rules.
- The old `feat/github-pages-hybrid-candidate-shell` uniquely contains `src/hybrid-engine.js`, which is absent from main. The current main has a different Python typed hybrid adapter, and the canonical execution plan does not specify this separate browser-side candidate shell as an acceptance task. It is therefore **DEFERRED** as an unadopted prototype, not silently imported into the Pages runtime.
- The profile-neutral boundary-evidence feature is already represented in main and remains a data contract, not a lexical word segmenter.

No feature branch was merged or rewritten during this review. No unique accepted rule, source row or test gap was identified for porting. This is changed-path/blob reconciliation, not full PR ancestry review. `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.

### Ancillary branch families and final test-ref count — 2026-11-19

The final test-family inventory contains 26 refs, not 25. The additional `test/ui-accessibility-smoke-2026-11-15` branch changes only `tests/browser/site.spec.js`. Its branch-only check for visibly withheld mixed input is superseded by current main's more specific unsupported-grapheme, neighboring-output preservation, mixed-script ordering and direct-romanization mixed-input tests; current main additionally includes WCAG contrast and keyboard smoke coverage. No test needs porting.

Three remaining singleton refs were also dispositioned:
- `benchmark/current-engine-2026-11-11` adds a manual benchmark workflow comparing the deterministic engine with upstream MekongPhon and Neurlang source-reported IPA. The report labels results as source-attested concordance, not gold accuracy. The canonical plan explicitly defers this benchmark pending independent adjudication and source/rights review; do not import the workflow as a release gate.
- `ci/khmer-g2p-smoke-2026-10-24` is an older optional G2P workflow snapshot. Current main has the later pinned manual benchmark workflow and separate optional Khmer Phonemizer raw-output workflow.
- `release/deterministic-rule-engine-2026-11-11` is an older rule-engine release snapshot. Current main has a substantially expanded deterministic engine, typed IPA/uncertainty boundary, tests and documentation; no unique release implementation needs porting.

The browser-side hybrid candidate shell remains DEFERRED as noted above. These dispositions do not close external gold, licensing, IPA-convention or lexical segmentation blockers.


## Fix/test/singleton branch family closeout — 2026-11-19

The full retained `fix/*` inventory (24 refs) was compared by changed path against current main. The non-PCGN fixes cover typed IPA-kind, unconverted romanizer output, tie-bar segment boundaries, benchmark reproducibility, Unicode parser diagnostics/evidence/rejection spans, typed partial results, unmodeled-letter trace, mixed-script numeral boundaries and mixed-script romanization. Existing current-main audit entries already record their dispositions: current code/tests have the richer typed result contract, tie-bar-with-following-segment validation, Unicode 18 packed parser/rejection reasons, source-preserving mixed-script behavior and shared output guard. Their older snapshots do not justify a code port.

The PCGN fix subset was examined directly. The row-7 source-pattern runtime/schema and the BA/TRIISAP, dependent-vowel, shortened-mark and TN #61 source blobs are already present on main. Stale branches retain incorrect row 16/17 O-series values, the obsolete two-component row-7 key, or BA+TRIISAP p-in-â. Main's current Note 2/Note 3 separation and row-specific source-key checks are authoritative. No old fix branch was merged or rewritten.

Correction to the test-family inventory: the 26th branch, `test/ui-accessibility-smoke-2026-11-15`, has only a browser test change. Its old “unsupported mixed input” test is superseded by current tests for unsupported graphemes, preserving neighboring output, mixed-script order and direct-romanization mixed input. Current main adds keyboard/contrast smoke coverage. The full test inventory is therefore 26 refs; the other 25 were previously reconciled in the November 19 test-family entry. No missing regression test was identified in this additional branch.

The three singleton refs were also checked:
- `benchmark/current-engine-2026-11-11` adds a manually dispatched concordance workflow over upstream MekongPhon and Neurlang source-reported IPA. It explicitly labels the output as source-attested, not gold accuracy. The canonical plan defers this comparison pending independent adjudication and rights review; it is not a release gate.
- `ci/khmer-g2p-smoke-2026-10-24` is an older optional workflow snapshot; main has the later pinned manual diagnostic workflow.
- `release/deterministic-rule-engine-2026-11-11` is an older deterministic engine snapshot; main has the expanded rule engine, typed IPA/uncertainty boundary, tests and documentation.

All branches remain preserved. This is targeted changed-path and selected-blob evidence, not complete ancestry reconciliation. `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.


## Data/source-register and PCGN comparison branch reconciliation — 2026-11-19

PR #457 merged as `db5c14b2e8d9b2e499142f462364aa5f0f35cc76`. Exact-main CI on this SHA completed successfully: Quality [44600726100], Pages build/deploy [44600726134], Chromium [44600726314]. PR #457 exact head `3c9a5f1a1450574908bf5e7f77341067c044f0f5` passed both Quality checks and Chromium.

Further checks of the data/evidence branches found no missing implementation:
- `data/integrate-positional-onset-evidence-register-2026-11-17` is an ancestor of main (ahead 0).
- `data/khmer-onset-evidence-registry-2026-11-17`: the positional-onset JSON (33 existing consonant hints), schema and tests are byte-identical to main. The registry is correctly restricted to specialist-reference provenance and `PROVISIONAL_ONSET_PREVIEW_ONLY`; it does not create canonical IPA evidence or full-syllable support.
- `data/pcgn-independent-vowel-source-register-2026-11-16` and its mainline variant: the independent-vowel CSV and resolver test are byte-identical to main. The source row 7 alternative `ŏ|ŭ` remains unresolved without lexical/reference selection; no IPA/Ukrainian output is emitted.
- `audit/restore-pinned-khmer-phonemizer-smoke-2026-11-18`: the optional pinned `khmerphonemizer==0.0.3` workflow is byte-identical to main; no workflow port is needed.

The `audit/pcgn-ungegn-vowel-row-reconciliation-2026-11-19` branch is stale and must not be merged. Its older comparison CSV calls PCGN anusvara/visarga row 7 a full `MATCH`, and its test requires all eight rows to match. Current main correctly records `VALUE_MATCH_KEY_SHAPE_DIFFERS`: PCGN's source sequence is `េ+ា+ះ`, while the pinned UNGEGN candidate key is `ោះ`. Current main also adds a second test that checks every PCGN comparison cell against project-owned source registries and retains the PCGN-vs-UNGEGN Note 3 `ស`-foot distinction. The stale branch omits these safeguards and older source-diff notes. No data, test or runtime changes should be ported from it.

The three audit snapshot branches `audit/reconcile-feature-branch-snapshots-2026-11-19`, `audit/reconcile-fix-branch-snapshots-2026-11-19` and `audit/reconcile-research-branch-snapshots-2026-11-19` contain only canonical documentation; each handoff is a strict subset of current main (zero branch-only lines). The current-main records already supersede them.

The `benchmark/current-engine-2026-11-11` branch contains a unique manual concordance workflow, but its output is source-attested upstream agreement, not independent gold accuracy. It remains DEFERRED pending independent adjudication and source-rights review, as recorded in the existing benchmark gate. The older `ci/khmer-g2p-smoke-2026-10-24` workflow is superseded by the current optional pinned workflow and manual diagnostic. No workflow or external corpus was added.

All historical refs are retained. These are targeted branch/content checks, not complete ancestry reconciliation; `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.


## Exact-main verification and live inventory after PR #458 — 2026-11-19

PR #458 merged by squash as `c4286ccd425627ef0771f87d0a38f594b7335074`. All exact-main checks on that SHA completed successfully: Quality [44602000654], Chromium [44602000538], and Pages build/deploy [44602000536]. PR #458 exact head `dc1356e8ab44674c3db398467a746c03c8e60066` passed both Quality checks and Chromium. No PR remains open at this checkpoint.

A fresh paginated branch inventory returned **332 refs, 332 unique names and 332 unique tip SHAs**. Prefix counts: `docs/*` 149, `audit/*` 44, `feat/*` 50, `research/*` 29, `test/*` 26, `fix/*` 24, `data/*` 4, `a11y/*` 2, plus one each under `benchmark/*`, `ci/*`, `release/*`, and one unprefixed `main`. All historical branches remain preserved; no branch deletion, rewrite or force-push occurred.

The feature, research, fix, test, data and singleton families have targeted changed-path/content dispositions already recorded above. This count refresh does not turn those targeted reviews into a full commit/PR ancestry audit. `KHM-BRANCH-AUDIT-001` remains **PARTIAL**.


## Post-PR #459 mainline checkpoint — 2026-11-19

PR #459 merged by squash as `c0fb6f8efcadf20ff55aec58b1188144707ae52f`. Exact-main Quality [44602788321], Chromium [44602788413], and Pages build/deploy [44602788487] all completed successfully. PR #459 exact head `5268955fb124d601a3b428d2dd2fbb72826b0aa2` passed both Quality checks and Chromium.

A new paginated inventory after the merge reports **333 refs, 333 unique names and 333 unique tip SHAs**: `docs/*` 150, `audit/*` 44, `feat/*` 50, `research/*` 29, `test/*` 26, `fix/*` 24, `data/*` 4, `a11y/*` 2, plus one each under `benchmark/*`, `ci/*`, `release/*`, and unprefixed `main`. There are **0 open PRs** at this checkpoint. No historical branches were deleted or rewritten.

The remaining release blockers are unchanged: no independently adjudicated IPA gold records, IPA convention still draft/unapproved, external source/dataset rights unresolved, Issue #104 still requires human recruitment and blind pilot execution, root license decision belongs to the owner, lexical segmentation and manual accessibility review remain incomplete. The repository remains a research-ready partial prototype, not release-ready. Full historical PR/commit ancestry reconciliation remains **PARTIAL** under `KHM-BRANCH-AUDIT-001`.


## Contextual vowel evidence contract — 2026-11-20

- Dedicated branch: `docs/architecture-runtime-contract-2026-11-20`, based on default-branch HEAD `3f3fc705784be1e6a82a0d3ed81f2a897acbef98`.
- Added `schemas/khmer-vowel-context-register.schema.json` for the canonical `data/khmer/vowel-context-register.json` and `tests/test_khmer_vowel_context_schema.py` for JSON Schema validation plus cross-record source-reference, unique-ID, evidence/status and conflict-withholding invariants.
- Updated the existing vowel-series/coda evidence matrix, architecture and documentation index in place to explain the new machine-checked contract and its strict boundary.
- No new IPA values, lexical records, Ukrainian mappings, source claims, runtime rules, generated coverage artifacts or gold rows were added. Existing source evidence remains SOURCE_ATTESTED_NOT_GOLD or CONFLICTING_SOURCE_ANALYSES.
- The generated coverage report remains only a dependent-vowel-sign × consonant-series inventory. It does not cover the full series × vowel sequence × coda × syllable type × length × stress/harmony/profile matrix. Full contextual coverage remains PARTIAL.
- The schema/test changes have not yet been executed in hosted CI or a local checkout. Exact-head Quality, Chromium and Pages evidence must be checked after the pull request is opened; no test is claimed as passed here.
- Independent adjudicated Khmer IPA gold remains 0; `data/benchmark/gold.tsv` remains header-only; empirical accuracy remains null. The approved IPA convention, qualified independent annotators, separate adjudicator, non-annotating curator, private blind intake, item-level rights and source locators, and 30 distinct adjudicated lexeme groups remain external acceptance gates.
- The existing architecture already separates the deterministic IPA-first route, typed research-only external candidates and the BGN/PCGN orthographic route. Those boundaries were preserved rather than rewritten.


### CI dependency correction — 2026-11-20

- First exact-PR-head Quality run [44721539422](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44721539422) failed during pytest collection: `ModuleNotFoundError: No module named 'jsonschema'`. The base CI installed only `-e . pytest`; the repository had no declared test extra.
- Corrected the project contract: `pyproject.toml` now declares a test-only extra (`pytest>=8,<10`, `jsonschema>=4.20,<5`), and `.github/workflows/ci.yml` installs `-e ".[test]"`. README now documents the same command and confirms JSON Schema is not a runtime dependency.
- This is a dependency declaration/CI correction, not a runtime dependency increase. The failed run remains recorded as FAILED; only a new exact-head run can verify the fix.


- Final pre-CI synchronization also updated `docs/architecture.md` to use the same `pip install -e ".[test]"` setup. Current branch head after the dependency and documentation correction is expected to be rechecked from PR metadata before recording CI evidence; no green rerun is claimed yet.


### Exact-head verification closeout — 2026-11-20

- Corrected test-only dependency declaration after the first Quality failure; no runtime dependency was added.
- Exact head `45fc31321d3628aa5afb61892802a8f9f20b3eb1` passed Quality [44721843510](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44721843510): **446 Python tests + 70 subtests**, web checks and production build.
- The same exact head passed Chromium browser smoke [44721843530](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44721843530), including visible-result verification.
- `KHMER-VOWEL-REGISTRY-SCHEMA-001` is now DONE_VERIFIED for data-integrity validation only. Full contextual vowel/rime coverage remains PARTIAL; gold remains 0 and accuracy null.
- These results apply to `45fc313`. The documentation-only evidence synchronization that follows will create a new head and must receive its own CI before that later head is called green.


## Post-merge verification — PR #461 — 2026-11-20

- PR [#461](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/461) was squash-merged to `main` as commit `0aa943f8490d5ed6043fbc74bd2f15aa7cf57c26`.
- Exact-main Quality run [44723258396](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44723258396) completed SUCCESS: **446 Python tests + 70 subtests**, shared register-shifter contract, web checks and production build. The test-only `jsonschema` extra was installed successfully.
- Exact-main browser smoke [44723258466](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44723258466) completed SUCCESS, including Chromium visible-result verification.
- Exact-main Pages workflow [44723258463](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44723258463) completed SUCCESS: build, Chromium production-site exercise, Pages artifact upload, deployment and deployed-site smoke test all succeeded. Published URL: https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System-/.
- `KHMER-VOWEL-REGISTRY-SCHEMA-001` is DONE_VERIFIED and merged. This closes a registry-integrity engineering task only. The complete contextual phonological vowel matrix remains PARTIAL; independent adjudicated IPA gold remains 0; empirical accuracy remains null.


## Contextual Khmer vowel evidence inventory — 2026-11-20

A separate branch `feat/khmer-contextual-vowel-coverage-2026-11-20` extends the existing `scripts/coverage.py` output instead of creating a parallel phonology engine or new lexical dataset.

- The canonical and public coverage JSON now include `contextual_vowel_evidence` with one source-preserving observation per existing evidence-register case.
- Fields expose dependent-vowel sequence, consonant class, subscripts, register-shifter marker, orthographic coda marker, source transcription, source ID/role and explicit source length marks.
- The report explicitly marks phonological syllable type, phonological coda identity, measured vowel length, stress/harmony and per-case dialect profile as not established where the registry does not contain them.
- It preserves source transcription strings and conflict status; no IPA was synthesized, no missing length mark was interpreted as short, and no orthographic coda was reclassified as a phonological coda.
- Existing registry has 9 rows (7 source-attested-not-gold; 2 conflicting source analyses). Independent adjudicated gold remains 0 and empirical accuracy remains null.
- Added regression assertions for these boundaries and generated report parity. Exact-head full CI is pending on the new PR; no local checkout/test execution was available in the GitHub connector environment.


## Contextual Khmer vowel coverage PR #462 — merged 2026-11-20

- PR #462 merged to `main` as `d4738096ae05cad4e338388bfb93fa05b8855e54`.
- Exact PR head `c40315663855102ee419090148da351343af9441`: Quality [44733384646](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44733384646) SUCCESS (**447 Python tests + 70 subtests**, report freshness, web checks, Vite build); push Quality [44733376120](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44733376120) SUCCESS; Chromium smoke [44733384573](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44733384573) SUCCESS.
- `scripts/coverage.py` now adds a case-level `contextual_vowel_evidence` view, preserving nine existing source-indexed cases, their source conventions and evidence states. The dashboard renders those observations as text.
- The report explicitly leaves profile, phonological syllable type/coda, measured duration, stress/harmony and full cross-product coverage unresolved. It does not infer shortness from absent length marks or generate IPA. No gold rows or runtime phonology rules were added.
- Current pilot blocker remains Issue [#104](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/104): convention approval, qualified annotators/adjudicator/curator, private blind intake, item-level rights and 30 adjudicated lexeme groups.
- Manual accessibility QA is tracked separately in Issue [#463](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/463). Automated smoke is not manual accessibility sign-off.
- Post-merge exact `main` head `a97381b6cd221ccb65cc7d4d118578c3f482eb54` is fully verified: Quality [44734185716](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44734185716) SUCCESS (**447 Python tests + 70 subtests**, including report freshness and dashboard tests); browser [44734185807](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44734185807) SUCCESS; Pages/deploy [44734185684](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44734185684) SUCCESS, including deployed-site smoke.


## Post-merge mainline verification — 2026-11-20

Current exact `main` HEAD: `a97381b6cd221ccb65cc7d4d118578c3f482eb54`.

- Quality [44734185716](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44734185716): SUCCESS — 447 Python tests + 70 subtests; contextual report freshness, schema, web checks and production build.
- Browser smoke [44734185807](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44734185807): SUCCESS — deterministic web checks, Vite build, Chromium visible-results smoke.
- Pages/deploy [44734185684](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44734185684): SUCCESS — production build, Chromium, artifact upload, deployment and public-site/runtime-asset smoke.
- PR #462 is merged; PR-head CI and exact post-merge main CI are both green.
- Remaining research gate: independent adjudicated IPA gold remains 0, empirical accuracy unmeasured; Issue #104 still requires expert convention approval, qualified annotators/adjudicator/curator, private blind intake, item-level rights and 30 adjudicated lexeme groups. Manual accessibility QA is tracked in Issue #463.

## Exact latest mainline verification — 2026-11-20

- Current verified default-branch HEAD at this checkpoint: `e5ea08e9bc0c9828b5da29cbd6ecb06d6e054ee0`.
- Quality [44734864422](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44734864422): SUCCESS.
- Browser smoke [44734864454](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44734864454): SUCCESS.
- Pages/deploy [44734864513](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44734864513): SUCCESS, including deployment and deployed-site smoke.
- This verifies the documentation/evidence synchronization on top of merged PR #462; it does not close the linguistic matrix or gold-data gates.
- Independent adjudicated IPA gold remains 0 and empirical accuracy remains unmeasured. The full source-located contextual matrix still lacks profile, phonological coda/syllable classification, measured duration, stress/harmony and adjudicated lexical coverage. Issue #104 remains the human/source-rights pilot gate; Issue #463 remains manual accessibility QA.

## Exact current-main closeout after contextual evidence dashboard — 2026-11-20

- Verified default-branch HEAD: 0e90dcaf7d76ac1c8ad43dc6496a506af044ecc1.
- Quality [44736142441](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44736142441) SUCCESS: gold-corpus structural validation, Python tests, web checks and production build.
- Browser smoke [44736142257](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44736142257) SUCCESS: deterministic web checks, Vite production build, Chromium installation and visible-results smoke.
- Pages/deploy [44736142183](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44736142183) SUCCESS: production build, Chromium smoke, Pages artifact upload, deployment and public-site/runtime-asset smoke.
- PR #462 contextual evidence dashboard and register changes are merged; there are no open PRs at this checkpoint.
- The nine contextual vowel observations remain seven SOURCE_ATTESTED_NOT_GOLD and two CONFLICTING_SOURCE_ANALYSES. They expose existing source evidence only; they do not fill the full profile × series × vowel × phonological coda × syllable type × measured length × stress/harmony cross-product. No missing length, coda, IPA or tone values were inferred.
- Independent adjudicated IPA gold remains 0; empirical accuracy remains unmeasured. Issue [#104](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/104) remains BLOCKED on expert-approved convention, two independent annotators, separate adjudicator and curator, private blind intake, item-level source rights and 30 adjudicated lexeme groups.
- Manual accessibility QA remains TODO under Issue [#463](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/463); automated browser checks do not constitute human WCAG sign-off.
- This pre-merge branch-status note is superseded by the final merged-main closeout below.


## Final merged-main closeout — 2026-11-20 (supersedes the pre-merge checkpoint above)

- Final default-branch commit: [5293cdcb93b5f4f617e8a9b04d97630a128c4510](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/commit/5293cdcb93b5f4f617e8a9b04d97630a128c4510); PR [#464](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/464) is merged. The earlier 0e90dc checkpoint and “branch is not main” instruction above are historical, superseded states.
- Exact final-commit Quality [44752921914](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44752921914), Chromium [44752921989](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44752921989), and Pages/deploy [44752921857](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44752921857) all SUCCESS.
- The nine contextual vowel observations remain seven SOURCE_ATTESTED_NOT_GOLD and two CONFLICTING_SOURCE_ANALYSES. The full phonological cross-product remains PARTIAL; no missing coda, duration, stress/harmony, IPA or tone values were inferred.
- Gold pilot BLOCKED under [#104](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/104); manual accessibility QA TODO under [#463](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/463). Independent adjudicated gold=0; empirical accuracy unmeasured. No license was selected because that is an owner decision.
- Result: engineering/build/deployment verified; linguistically a research prototype, not release-ready. Connector-hosted CI was verified; no local checkout or local test commands were available in this session.


## Owner-authorized noncommercial licensing — 2026-11-21

The repository owner has confirmed that the project purpose is noncommercial research and scientific knowledge-sharing. This supersedes earlier handoff notes that the root-license decision was still awaiting the owner.

- Original project software code: PolyForm Noncommercial 1.0.0 (LICENSE); Python package metadata now declares SPDX identifier PolyForm-Noncommercial-1.0.0. This replaces the prior MIT declaration in pyproject.toml.
- Original documentation and explanatory prose: CC BY-NC 4.0 (LICENSE-DOCS).
- Third-party software, fonts, models, dictionaries, corpora, recordings and other externally owned material are excluded and remain subject to their own terms.
- The project license does not blanket-license data/; each source-derived observation and dataset retains its own provenance and rights status. Unknown or conflicting rights remain unresolved and do not authorize redistribution.
- PolyForm Noncommercial is not OSI-approved Open Source. Commercial use is not granted by these terms.

Task ledger:
- KHMER-LICENSE-001 — PARTIAL pending PR CI/merge; scope and metadata implementation is in this branch.
- Third-party source-rights clearance — PARTIAL/BLOCKED per item-level evidence; this license change does not close those existing research gates.
- No linguistic data, IPA labels, Ukrainian mappings, runtime rules, or generated artifacts were changed.

The dedicated branch is license/noncommercial-research-2026-11-21; this section records the proposal until its PR is reviewed and merged. No release or legal opinion is implied.


## Final noncommercial license closeout — 2026-11-21

The owner-authorized noncommercial license decision is now merged. PR #466 added the scoped PolyForm Noncommercial 1.0.0 code license and CC BY-NC 4.0 documentation license, and replaced the prior MIT package metadata declaration. PR #467 corrected the final PolyForm definition wording to match the official license text. Merge commits: #466 575447844a0f876d4e361232a25ef18b8bce50af; #467 94bbc0a230aafcfb65d300ea65f097d026c130df.

PR-head verification: #466 Quality 44826318181 and browser 44826318046 SUCCESS; #467 Quality 44826605678 and browser 44826605610 SUCCESS. Exact post-merge mainline Quality/browser/Pages runs on 94bbc0a230aafcfb65d300ea65f097d026c130df are still running at this handoff update and must be checked before calling that SHA fully green.

KHMER-LICENSE-001 — DONE_VERIFIED for the repository-owned software/docs licensing declarations, scope boundaries, and PR-head CI. Third-party/source-data rights remain PARTIAL or BLOCKED per their individual evidence; this project license does not authorize redistribution of items with unknown or conflicting rights. No linguistic records, IPA, runtime rules, or generated artifacts were changed. The repository remains a linguistically partial research prototype, not release-ready.


## Post-merge CI verification — noncommercial license closeout — 2026-11-21

The licensing closeout documentation PR #468 is merged as 493e135ad4787c737931dbad20ea564c528bfd7c. Exact-mainline CI on that SHA is fully green: Quality [44827023495](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44827023495), Chromium browser smoke [44827023488](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44827023488), and Pages build/deploy [44827023602](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44827023602) all SUCCESS. This supersedes the earlier timestamped note that exact-main workflows were still running. KHMER-LICENSE-001 remains DONE_VERIFIED; third-party and item-level data rights remain separately unresolved.


## Original research-data license — 2026-11-21

Owner-authorized noncommercial research reuse now explicitly covers original project-authored datasets, annotations and curated database contributions under CC BY-NC 4.0 (`LICENSE-DATA`), where the maintainers/contributors hold the rights. README, new `THIRD_PARTY_NOTICES.md`, `data/benchmark/licenses.json` and gold-corpus documentation explain the scope and exclusions and distinguish noncommercial research reuse from the stricter commercial/product gold-corpus gate.

KHMER-RESEARCH-DATA-LICENSE-001 — implementation complete on this branch; pending PR-head and post-merge CI. This grant does not clear MekongPhon, Open-Dict, PhonSobon/NCKL, BYU MATRIX, Google Language Resources, OpenSLR, Kirby, Wayland, DDD, Common Voice, Goruut or other third-party resources. Their item-level licenses and restrictions remain controlling. No new corpus rows, IPA labels, lexical data or runtime behavior were added. The gold corpus remains empty and the expert pilot remains blocked pending approved convention, independent annotators/adjudicator, curator and item-level rights checks.


## Research-data license merged and exact-main CI — 2026-11-21

PR #470 merged as `c57e76d11e940aa522f36cfaca205ad654a6425e`. Its PR-head Quality checks [44829570556](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44829570556) and browser smoke [44829570588](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44829570588) both passed. The exact post-merge main SHA `c57e76d11e940aa522f36cfaca205ad654a6425e` is fully green: Quality [44829718697](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44829718697), Chromium [44829718684](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44829718684), and Pages build/deploy [44829718661](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44829718661) all SUCCESS.

KHMER-RESEARCH-DATA-LICENSE-001 — DONE_VERIFIED for repository-owned original research data license scope, benchmark registry distinction and third-party notice inventory. This does not clear external data rights or contributor ownership not evidenced per item. Gold remains empty; expert gold pilot and manual accessibility QA remain outstanding. The repository remains a research prototype, not linguistically release-ready.


## Scholarly citation metadata and final exact-main CI — 2026-11-21

PR #472 merged as `cd54ed9c64fb9cb7132f33b589d7847a14226bde`, adding `CITATION.cff` aligned with package version 0.2.0 and a README citation note. PR-head Quality [44830502365](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44830502365) and browser smoke [44830502500](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44830502500) both passed. Exact post-merge main SHA `cd54ed9c64fb9cb7132f33b589d7847a14226bde` is fully green: Quality [44830768580](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44830768580), Chromium [44830768579](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44830768579), and Pages build/deploy [44830768577](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44830768577) all SUCCESS.

KHMER-CITATION-001 — DONE_VERIFIED. Citation metadata identifies the research prototype, version and noncommercial code license without inventing a DOI or publication. KHMER-RESEARCH-DATA-LICENSE-001 remains DONE_VERIFIED from PR #470. Third-party rights remain item-specific and unresolved where the source registry says so. Gold remains empty; expert gold pilot and manual accessibility QA remain outstanding. This is not linguistic release approval.


## Final exact-main CI after citation closeout — 2026-11-21

The citation/handoff closeout PR #473 merged as `f41699a7ebadec9d85ec7cf7092f972212463f37`. The exact post-merge main SHA is fully green: Quality [44831432729](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44831432729), Chromium browser smoke [44831432822](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44831432822), and Pages build/deploy [44831432731](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44831432731) all SUCCESS. This supersedes the earlier exact-main checkpoint on `cd54ed9c64fb9cb7132f33b589d7847a14226bde`.

The merged main now contains the scoped PolyForm Noncommercial code license, CC BY-NC documentation and original research-data grants, the third-party rights inventory, and CFF citation metadata. These repository-owned licensing and citation tasks are DONE_VERIFIED. Source-specific third-party rights, expert-adjudicated IPA gold and manual accessibility QA remain separate unresolved gates.


## Exact-main CI after final closeout merge — 2026-11-21

PR #474 merged as `5537abb05795291bebc7e528a365a62b34dae18d`. Exact post-merge main CI is fully green: Quality [44831853817](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44831853817), Chromium [44831853698](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44831853698), and Pages build/deploy [44831853709](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44831853709) all SUCCESS. This supersedes the prior exact-main checkpoint on `f41699a7ebadec9d85ec7cf7092f972212463f37`.


## Final mainline CI after all closeout documentation — 2026-11-21

PR #475 merged as `96c2329d627056daececef1848a76cc977051d65`. Exact post-merge main CI is fully green: Quality [44832297432](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44832297432), Chromium [44832297291](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44832297291), and Pages build/deploy [44832297309](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44832297309) all SUCCESS. This supersedes the prior exact-main checkpoint on `5537abb05795291bebc7e528a365a62b34dae18d`.

The final main contains PolyForm Noncommercial code licensing, CC BY-NC documentation and original research-data grants, the scoped third-party rights inventory, and CFF citation metadata. KHMER-RESEARCH-DATA-LICENSE-001 and KHMER-CITATION-001 remain DONE_VERIFIED. Third-party/source-specific rights, expert IPA gold and manual accessibility QA remain separate unresolved gates. No gold labels or runtime rules were added by these closeouts.


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


## Human pilot operations, rights and contextual research — 2026-11-21

- Added [Khmer private blind-intake runbook](research/KHMER-PRIVATE-BLIND-INTAKE-RUNBOOK-2026-11-21.md): separated curator/A/B/C/reviewer roles, independent A-only/B-only submissions, hash-locked packets, adjudication after both locks, independent discrepancy audit, privacy controls and pilot acceptance criteria. This is an operational design only; no private channel or participant recruitment has occurred.
- Added [Khmer third-party rights reconciliation](audits/current/KHMER-THIRD-PARTY-RIGHTS-RECONCILIATION-2026-11-21.md): MekongPhon dataset license remains UNKNOWN; Khmer Acoustic Model dictionary has a CC BY vs CC BY-SA and 33,091 vs 29,204 count conflict; Khmer ALT is CC BY-NC-SA 4.0; khPOS needs privacy/provenance review; Kirby audio rights are not established. No item newly cleared for gold.
- Added [contextual-vowel and lexical-segmentation research update](research/KHMER-CONTEXTUAL-VOWEL-AND-LEXICAL-SEGMENTATION-RESEARCH-UPDATE-2026-11-21.md). It preserves source/profile/task distinctions and does not create new IPA labels or runtime rules. Full contextual matrix remains PARTIAL; lexical segmentation remains BLOCKED pending convention, rights/privacy review and an independently adjudicated boundary pilot.
- KHM-GOLD-PILOT-001 remains BLOCKED (Issue #104): convention approval, two qualified independent annotators, third adjudicator, curator, private workspace, 30 attested rights-cleared groups and completed blind/adjudication flow remain outstanding. Gold=0; accuracy unmeasured.
- KHM-MANUAL-A11Y-001 remains TODO (Issue #463): no human keyboard, screen-reader, zoom/reflow or mobile evidence has been produced.
- PR #477 was merged as 3263116434d37e18fe6b3ae02d63e6d377dda453; exact post-merge Quality, Chromium and Pages/deploy checks succeeded. This verifies engineering, not phonological completeness or accessibility conformance.


## MekongPhon component-level rights audit — 2026-11-21

A deeper upstream inspection is recorded in docs/audits/current/KHMER-THIRD-PARTY-RIGHTS-RECONCILIATION-2026-11-21.md. The MekongPhon repository at f80f6c1840c4818b51e05f2e00cded4701a5b662 has GitHub license=null and no root LICENSE. Its Khmer lexicon is scraped from SEAlang with source=headley77; sentence data combines OPUS NLLB v1, ParaCrawl-Bonus v9 and OpenSubtitles v2024, then uses trie-based lexicon lookup to convert sentences to IPA. The merged sentence data does not preserve per-line source/license provenance. Treat lexicon, each OPUS component, converted data and published weights as UNKNOWN/RESTRICTED pending written permission and source-level license manifests. Do not import MekongPhon into gold or train on it. The paper's public-release statement and Hugging Face model's Apache-2.0 label do not clear the underlying corpus.


## Khmer public beta reproducibility closeout — 2026-11-21

PR #481 merged as `355409a47feb8987cc655ca62dbad41ce8ff043d`. It adds npm lockfile v3 with exact versions, registry tarball URLs, integrity hashes and declared package license metadata; switches Quality, Pages and browser-smoke workflows from floating `npm install` to `npm ci`; records the `@gmana/km-translit` 0.1.2 MIT package metadata and its romanization-only runtime role; updates local install instructions; and adds the operational beta release checklist.

Exact PR-head checks on `0b844a9db0a98a9a75a068f34d2fd1cf279a7020`: Quality [44905815283](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44905815283) SUCCESS; Chromium/browser [44905815288](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44905815288) SUCCESS. Exact post-merge main checks on `355409a47feb8987cc655ca62dbad41ce8ff043d`: Quality [44905912782](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44905912782) SUCCESS; Pages build/deploy [44905912768](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44905912768) SUCCESS; Chromium/browser [44905912797](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44905912797) SUCCESS.

KHM-BETA-REPRODUCIBLE-DEPS-001 — DONE_VERIFIED. This is an engineering/reproducibility improvement only; it does not create IPA labels, gold data, linguistic accuracy, or new source rights. MekongPhon remains excluded. Expert gold and manual accessibility remain deferred/TODO respectively. No GitHub Release was published.


## Final Khmer beta closeout after checklist reconciliation — 2026-11-21

PR #482 merged as `3ba0523a6e90bdba63a7c80693fbbdd2f0b3fdec`. The checklist's previous lockfile-pending statement is removed, the README links the operational beta checklist, and this handoff retains exact post-merge evidence. Exact-main workflows on `3ba0523a6e90bdba63a7c80693fbbdd2f0b3fdec`: Quality [44906297076](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44906297076) SUCCESS; Chromium/browser [44906297035](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44906297035) SUCCESS; Pages build/deploy [44906297037](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44906297037) SUCCESS.

Khmer engineering beta gates are DONE_VERIFIED: exact npm lockfile, `npm ci` in CI/Pages/browser workflows, Python and web checks, production Chromium smoke, Pages deployment and post-deploy HTML/JS/CSS smoke. Linguistic accuracy remains NOT_ASSESSED; gold=0; complete vowel/context and lexical segmentation matrices remain PARTIAL; manual accessibility QA remains TODO. MekongPhon and other unresolved-rights sources remain excluded. No GitHub Release was published.


## Final exact-main beta verification after PR #483 — 2026-11-21

PR #483 merged as `a6347577052ddf70d69364ed7cc90e2ff584ed2a`. Exact-main checks on this SHA all completed successfully: Quality [44906655301](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44906655301) SUCCESS; Khmer browser smoke [44906655362](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44906655362) SUCCESS; Pages build/deploy [44906655377](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44906655377) SUCCESS.

Engineering beta release gates are now verified on main, including reproducible npm installs, production browser smoke and deployed asset smoke. This does not close language-level PARTIAL items (vowel-context matrix, lexical segmentation, independent gold/accuracy) or manual accessibility TODO. No GitHub Release or public announcement was created.


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


## Shared Strict / Soft / Super-soft output vocabulary — 2026-11-22

- PR [#509](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/509) merged to main as `5d2b3e54f050df07eb9d07fdc135c1bd6486f532`.
- The browser's existing internal values `strict`, `balanced`, and `exploratory` are preserved; user-facing labels are now **Strict**, **Soft**, and **Super-soft**.
- The semantics remain distinct: Strict = source-indexed supported proposals only; Soft = partial output with per-unit uncertainty; Super-soft = additional structural/onset research hints. These are disclosure/acceptance levels, not accuracy scores.
- `???` remains the final Ukrainian placeholder for unresolved units. Candidate output does not overwrite the Strict result. No phonological rules, evidence rows, or target mappings were changed by this UI vocabulary update.
- Exact main verification: Quality checks [45002252229](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/45002252229) SUCCESS; Khmer browser smoke [45002252063](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/45002252063) SUCCESS; Pages deployment [45002252084](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/45002252084) SUCCESS.
- Published site: https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System-/.
- Linguistic validation and independently adjudicated IPA gold remain separate release gates; this change makes no accuracy claim.


## UI/UX quick-transcription-first update — 2026-11-22

- **DONE_VERIFIED — merged, tested, and deployed:** PR [#511](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/pull/511) merged; final UI/CSS follow-up on `main` is `1476d939fb0b0de560dc0211d6611e9971e4478e`.
- The Ukrainian practical form is the primary result. Profile and Strict / Soft / Super-soft controls are in a collapsed settings disclosure; IPA, romanization, per-unit status, and detailed explanations are grouped under “Докладний аналіз”. The beta notice is concise by default and expandable.
- Existing engine-facing IDs and `data-method-panel` hooks were preserved. No Khmer phonological rules, IPA values, Ukrainian adaptations, or uncertainty semantics were changed.
- Quality checks [#45062629220](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45062629220), Chromium browser smoke [#45062629118](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45062629118), and GitHub Pages deployment [#45062629122](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45062629122) all passed.


## Provisional Ukrainian candidate for unresolved Khmer input — 2026-11-22

- **Implementation submitted for exact-head verification:** branch `fix/khmer-provisional-pronunciation-candidate-20261122`, based on main `92de8637336d857ec852db95f749f9bfa0fb7b31`.
- When the phonetic engine has no complete IPA-derived Ukrainian output, but the whole Khmer input is renderable by the already-shipped BGN/PCGN-derived romanizer, the primary Ukrainian field now shows that orthographic adaptation as a `PROVISIONAL` candidate without appending `???`. For `កម្ពុជាប្រជាធិបតេយ្យ`, the expected visible candidate is `Кампучеапчеат'іптей`.
- The IPA line remains `⟦NOT_ESTABLISHED⟧`; per-unit uncertainty and evidence provenance are unchanged. The UI status explicitly identifies the candidate as an orthographic-romanization fallback, not an IPA-derived pronunciation. Mixed partially-resolved input and malformed/unrenderable fragments retain local abstention markers.
- Updated the browser regression for the reported phrase and the shared onset-fallback fixture, plus README and deterministic-engine contract. No phonological rule, IPA value, gold label, or accuracy claim was added.
- **Acceptance:** exact-head Node/web tests, production build, Chromium browser suite, and post-merge Pages deployment/smoke must pass. Until then this change is PARTIAL, not DONE_VERIFIED.


### Strict-level boundary follow-up — 2026-11-22

- Follow-up branch `fix/strict-level-romanization-fallback-guard-20261122`, based on merged candidate commit `03866cbc024b4bc9211f1e3d03a76561b43efb46`.
- The provisional orthographic fallback is shown only in Soft and Super-soft. Strict continues to show `???` for unresolved phonetic units, preserving the existing Strict contract.
- Browser regression explicitly switches the reported phrase from Soft → Strict → Soft and checks both behaviors. README and engine contract now state this boundary.
- **Acceptance:** exact-head Quality checks and Chromium browser smoke must pass before merge; Pages deployment must pass after merge.


## Post-merge closeout — provisional Khmer Ukrainian candidate — 2026-11-22

- **DONE_VERIFIED — PR #516:** merged as `03866cbc024b4bc9211f1e3d03a76561b43efb46`. In Soft/Super-soft, fully renderable unresolved Khmer input now receives the BGN/PCGN-derived Ukrainian orthographic candidate without a trailing `???`; status explicitly labels it PROVISIONAL and not IPA-derived. For `កម្ពុជាប្រជាធិបតេយ្យ`, expected candidate: `Кампучеапчеат'іптей`. IPA remains `⟦NOT_ESTABLISHED⟧` and all per-unit uncertainty remains.
- **DONE_VERIFIED — PR #517:** merged as `c9939495943d4fd264eeac34e4a52ba0ed67a4a9`. Strict withholds the orthographic fallback; Soft and Super-soft show it. Browser regression switches Soft → Strict → Soft.
- **Exact-head PR checks:** PR #516 Quality [45074940396](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45074940396) SUCCESS and Chromium [45074940435](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45074940435) SUCCESS. PR #517 Quality [45075099714](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45075099714) SUCCESS and Chromium [45075099754](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45075099754) SUCCESS.
- **Post-merge main verification:** Quality [45075171449](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45075171449) SUCCESS; Chromium [45075171521](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45075171521) SUCCESS; GitHub Pages build/deploy [45075171498](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45075171498) SUCCESS, including production Chromium exercise and deployed site/runtime-asset smoke.
- **Published:** https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System/
- No IPA, phonological rules, benchmark labels, expert-gold rows or accuracy claims were invented. The fallback is an orthographic candidate only; full source-language phonology/IPA coverage remains incomplete and linguistic accuracy remains NOT_ASSESSED.

## Automatic best-effort Ukrainian output — 2026-11-23

- User clarified that selecting Strict/Soft/Super-soft is not an acceptable prerequisite for seeing an approximate candidate. The expected default is: established IPA-derived forms render normally; unresolved but romanizable units automatically receive a provisional Ukrainian candidate; genuinely unrenderable/malformed units retain a local `???`.
- Implemented in `src/main.js`: each unresolved Khmer orthographic unit is independently passed through the existing BGN/PCGN-derived romanizer and Ukrainian orthographic adapter. The candidate is displayed in the primary output and unit diagnostics, with explicit `PROVISIONAL` provenance. This does not fabricate IPA; the unit's IPA and phonetic status remain `NOT_ESTABLISHED`.
- Removed the detail-level gate from the remaining whole-input fallback. The best-effort candidate is now automatic at Strict, Balanced and Exploratory detail levels.
- Extended `schemas/phonetic-result.schema.json` with `ukrainian_kind=ORTHOGRAPHIC_ROMANIZATION_FALLBACK`, keeping it distinct from `IPA_DERIVED` and `UNRESOLVED`.
- Added runtime and browser regression coverage for the reported phrase, all three detail levels, and an unresolved Khmer cluster.
- **DONE_VERIFIED after merge:** PR #518 squash-merged as `360e8fa1c63e23bce3cf234c8ea2f3b50c3d9177`. Exact-head PR Quality [45076517499](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45076517499) and Chromium [45076517545](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45076517545) passed. Post-merge main Quality [45076618364](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45076618364), Chromium [45076618290](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45076618290), Pages build/deploy [45076618274](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45076618274) all passed; the deploy job's `Smoke-test deployed site and runtime assets` passed. Linguistic accuracy remains unmeasured; this is an explicitly provisional orthographic fallback, not a phonetic gold result.
