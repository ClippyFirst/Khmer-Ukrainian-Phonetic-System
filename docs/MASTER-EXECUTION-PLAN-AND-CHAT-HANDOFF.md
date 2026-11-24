# Master execution plan and chat handoff — 2026-11-24

## Current continuation: Lao engine architecture alignment — 2026-11-24

- Repository: `ClippyFirst/Khmer-Ukrainian-Phonetic-System`.
- Starting `main`: `1b8649c4b874fbf34a66012d7e02aa1da04fb6da`.
- Working branch: `feat/khmer-lao-engine-contract-parity-20261124`.
- PR: [#568](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/pull/568), ready for human review; exact-head workflows passed; no merge was performed.
- Reference architecture: `ClippyFirst/Lao-Ukrainian-Phonetic-System`, especially `docs/lao-grapheme-ipa-preview.md`.
- Final source/test head: `f579e1444fbda2b186fdf8a04dc9f52f7ebc044e`. Subsequent commits through `fbfe2ae68c1376a3ba5a6634bc79790cb4cf687a` update documentation, benchmark evidence and handoff registers only. This handoff refresh is also documentation-only.
- Local clone was unavailable because the container could not resolve `github.com`. Repository edits were made directly on this isolated GitHub branch. No local test pass is claimed.
- No deployment, release tag, main-branch merge or external setting change was performed.

### Implemented architecture

1. Added `TypedPhoneticResult` and `PhoneticSegment` without replacing the existing public `PhoneticResult` envelope.
2. Added typed statuses `SUPPORTED`, `UNCERTAIN`, `PROVISIONAL`, `UNRESOLVED`; current Khmer lexical proposals remain `UNCERTAIN`, not promoted to `SUPPORTED`.
3. Added source-independent IPA tokenization preserving segment sequence, syllable boundaries, length marks, tone symbols, certainty, provenance and uncertainty.
4. Added one IPA-only Ukrainian target adapter for complete and provisional phonetic results. It does not read Khmer graphemes or romanization.
5. Provisional onset IPA remains `PROVISIONAL`, carries `phonemic_ipa=null`, and always retains one explicit unknown tail; the adapter maps the known run and returns `???` for the remainder.
6. Valid IPA with no Ukrainian target correspondence remains valid IPA; the target value is withheld instead of guessed.
7. Preserved the separate `ORTHOGRAPHIC_ROMANIZATION_FALLBACK` candidate and the opt-in, non-canonical external-provider contract.
8. Integrated Python engine, JavaScript core, Worker output, CLI, UI unit details and `schemas/phonetic-result.schema.json`.
9. Added replica-skill recon, feature matrix, architecture, test plan, bug log and build log under `replica/`.

### Verification ledger

| Check | State | Evidence |
|---|---|---|
| Test-first RED for typed IPA model | DONE_VERIFIED | Initial PR-head Quality failure was the expected missing-module failure |
| Test-first RED for CLI contract | DONE_VERIFIED | Initial CLI tests failed because CLI still called structural parser only |
| Python suite | DONE_VERIFIED | 503 passed + 70 subtests in latest successful Quality run [45490428639](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45490428639) |
| Browser deterministic checks | DONE_VERIFIED | Latest Quality run [45490428639](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45490428639); web engine, runtime, Worker, typed IPA adapter and CLI tests passed |
| Python/JavaScript parity | DONE_VERIFIED | 129 structural, 38 lexical, 46 consonant/rule and 6 segmentation fixtures passed; typed IPA fields are included in rule-output parity |
| Benchmarks and Vite build | DONE_VERIFIED | Quality run [45490428639](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45490428639) |
| Exact-head Chromium smoke | DONE_VERIFIED | [45490428728](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45490428728) passed 42/42 Playwright tests, including typed IPA detail disclosure |
| Exact-head pinned Rust comparison | DONE_VERIFIED | [45490428786](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45490428786) passed |
| External khPOS comparison | DONE_VERIFIED | [45490428814](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45490428814) passed |\n| Linguistic accuracy | NOT_ASSESSED | Independent adjudicated IPA gold corpus remains empty |

### Task ledger

| Task | Status | Acceptance boundary |
|---|---|---|
| `KHM-LAO-ENGINE-CONTRACT-001` | DONE_VERIFIED | Typed result model, shared adapter, Python/JS parity, CLI, schema and uncertainty output; no language-rule transfer |
| `KHM-PROVISIONAL-OUTPUT-001` | DONE_VERIFIED on prior main | Existing onset-first primary output and separate orthographic fallback preserved |
| `KHM-PHON-CONTEXT-001` | PARTIAL | Full contextual vowel/coda/series/length matrix remains incomplete |
| `KHM-IPA-GOLD-001` | BLOCKED | Independent gold has 0 entries; two annotators and adjudicator still required |
| Pronunciation accuracy | NOT_ASSESSED | No gold denominator |
| Manual accessibility audit | DEFERRED | Outside this architecture change |

### PR and branch reconciliation

- PR #568 is this isolated architecture continuation; all exact-head automated workflows passed. It is ready for human review; no merge was performed. The PR is mergeable and based directly on the unchanged starting `main`.
- PR #519 remains open and untouched. It is a separate, diverged hybrid-inference change (73 commits ahead / 200 behind, reported non-mergeable); do not merge blindly.
- Historical branches were not deleted or rewritten.
- No public deployment or formal release was requested or performed.

---

## Prior task record — provisional output and benchmark (historical)

- Repository: `ClippyFirst/Khmer-Ukrainian-Phonetic-System`
- Starting `main` for the provisional-output task: `422023d03283648bea9ca59ef0ea01caedf41698`.
- Final `main`: `fff886dfaca8979387dc6cacbd7417a89020a407`.
- Implementation branch: `feat/khmer-provisional-output-benchmarks-20261124`.
- [PR #566](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/pull/566) merged by squash; final merge commit above.
- Hosting: [GitHub Pages public service](https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System/).
- Methodology: [system page](https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System/system.html).
- No formal release tag was created.

## User-requested outcome: non-blocking output

The primary browser output no longer needs to suppress all useful material when full canonical IPA is unavailable.

1. If the source registry supports the onset, display an onset-only IPA-derived Ukrainian hint followed by `???`.
2. If no onset IPA hint is available but a BGN/PCGN-derived orthographic candidate exists, display that candidate followed by `???`, explicitly typed as `ORTHOGRAPHIC_ROMANIZATION_FALLBACK`.
3. If neither candidate exists, display `???`.

The browser visibly distinguishes `IPA_DERIVED_PARTIAL` from `ORTHOGRAPHIC_ROMANIZATION_FALLBACK`; the latter is explicitly **not IPA and not a pronunciation claim**. `display_status=PROVISIONAL` is separate from canonical `status`, `canonical_ipa`, and `canonical_ua`. The separate romanization mode remains separate. Unknown material is not silently deleted or guessed.

The Python reference engine preserves source-registered onset-only previews on withheld lexical fixtures and marks these as partial. It does not turn an orthographic fallback into IPA. Python/JavaScript parity tests cover shared onset fallback fixtures.

## Verified engineering benchmark

Quality run [45474564623](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45474564623), PR code head `ccb40414d85fde0a0d9b7c6ef9de285f9f7d5f2a):

| Measure | JavaScript core | Python engine |
|---|---:|---:|
| Runtime | Node v24.22.3 | Python 3.12.16 |
| Unique NFC inputs | 39 | 39 |
| Warm-up / measured batches | 5 / 25 | 5 / 25 |
| Median batch latency | 1.3028 ms | 5.2737 ms |
| Throughput | 29,934.7 inputs/s | 7,395.16 inputs/s |
| Complete / partial / unresolved | 37 / 2 / 0 | 37 / 2 / 0 |

Observed Node/Python ratio: 4.05× in this CI environment. This is not a browser-device latency guarantee or a pronunciation-accuracy score.

Tokenizer stress: 8,000 code points, 61,980 dictionary entries, 7.65 ms median, 1,046,065 code points/s, source preservation PASS. The external khPOS and pinned upstream Rust comparisons passed. These assess segmentation only.

Full benchmark and limitations: [KHMER-ENGINE-BENCHMARK-2026-11-24.md](research/KHMER-ENGINE-BENCHMARK-2026-11-24.md).

## Exact final-main verification

All workflows below completed successfully on final main commit `fff886dfaca8979387dc6cacbd7417a89020a407`:

- [Quality checks — 45474856164](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45474856164): Python suite, web checks, structural/lexical/consonant/segmentation parity, engine benchmark, tokenizer benchmark and production build.
- [Chromium browser smoke — 45474855979](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45474855979): PASS.
- [External khPOS segmentation benchmark — 45474855939](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45474855939): PASS.
- [Pinned upstream Rust comparison — 45474856176](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45474856176): PASS.
- [GitHub Pages deployment and live smoke test — 45474855848](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45474855848): PASS. The workflow fetched the deployed home page, methodology page, JavaScript and CSS assets successfully and exercised the production site in Chromium.

Local tests were not run in this session because the local clone/network route was unavailable; GitHub Actions executed the listed checks.

## Task ledger

| Task | Status | Boundary |
|---|---|---|
| `KHM-PROVISIONAL-OUTPUT-001` | DONE_VERIFIED | Main browser UI exposes onset-first partial output, then typed orthographic fallback, then `???`; Chromium passed |
| `KHM-ENGINE-BENCHMARK-001` | DONE_VERIFIED | Shared 39-input Python/Node benchmark, runtime versions, throughput and output coverage recorded |
| Tokenizer stress benchmark | DONE_VERIFIED | 8,000-code-point stress case; source preserved |
| External segmentation comparisons | DONE_VERIFIED | khPOS and pinned upstream Rust comparisons passed |
| `KHM-PHON-CONTEXT-001` | PARTIAL | Full profile × consonant series × vowel × coda × syllable type × length × tone/stress coverage is not established |
| `KHM-IPA-GOLD-001` | BLOCKED | Independent adjudicated IPA gold corpus has 0 entries; issue #104 requires two annotators and an adjudicator |
| Pronunciation accuracy | NOT_ASSESSED | No gold denominator exists; benchmark coverage is not accuracy |
| Manual accessibility audit | DEFERRED | Retained as previously scoped |

## PR and branch reconciliation

- PR #566 was reviewed against current main, had no merge conflicts or review-blocking comments, passed all four PR-head workflows, and was squash-merged.
- PR #519 remains open and untouched. It is a separate hybrid-inference change, currently diverged and reported non-mergeable; do not merge blindly. Reconcile its diff against current main before any future reuse.
- Historical branches were not deleted or rewritten.
- No formal release was created.

## Next genuine research blockers

1. Build a profile-compatible lexical/audio cross-product across consonant series, vowels, codas, syllable shape, length and tone/prosody.
2. Curate independent IPA gold with two annotators and a third adjudicator under issue #104; only then measure held-out pronunciation accuracy.
3. Continue specialist review of the provisional phonological rules and Ukrainian adaptation. Never promote romanization candidates to IPA or infer unsupported vowel/coda/tone values.

**Release assessment:** public beta is deployed and the engineering path is verified. This remains a research-ready partial prototype, not a linguistically validated G2P product.
