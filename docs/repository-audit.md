# Repository audit — 2026-10-05

## Identity

The repository is a Khmer → Ukrainian research system. The active implementation is Python/data driven and the target is contemporary Khmer with explicit pronunciation-profile separation.

## Inventory decision

| Area | Classification | Action |
|---|---|---|
| README/docs | CORE/DOCUMENTATION | keep and revise |
| data/khmer | CORE/SUPPORTING DATA | keep; correct provenance |
| data/comparative | RESEARCH EVIDENCE | keep |
| data/ukrainian | CORE | keep as proposed policy |
| src/khmer_ua | IMPLEMENTATION | keep; expose new API |
| tests | VALIDATION | keep and expand |
| schemas | SUPPORTING DATA | keep |
| scripts/coverage.py | SUPPORTING/UTILITY | keep until benchmark generation is implemented |
| git/OS/IDE debris | ARTIFACT | none found in tracked tree |
| foreign-language project content | FOREIGN | none found in tracked tree |
| duplicate authoritative mapping tables | TECHNICAL DEBT | reduced by making data/khmer and data/ukrainian the active sources of truth |

## Historical material

The repository history contains useful milestones: initial foundation; orthographic syllable segmentation fix; data-driven register/rule layer; comparative Cyrillic research; Ukrainian practical target layer. These commits remain useful provenance and are not rewritten away.

## Important audit finding

The previous consonant table attached IPA evidence directly to the Unicode source ID. This was too strong: Unicode establishes script structure, not the complete modern phonetic realization. The active table now cites a specialist orthography/phonology reference for phonetic values while retaining Unicode for orthographic structure.

## No destructive cleanup

No unique research dataset or historical analysis was deleted. The repository was small enough that archiving large historical trees would have added complexity without improving the active research workflow.


## Transcription edge-case audit — 2026-10-06

A focused adversarial review found several practical-layer weaknesses that were too easy to miss in ordinary examples:

- register shifters ៉ / ៊ were parsed as generic signs instead of changing the effective register;
- the exceptional ប៉ construction was not represented as the /p/ realization it encodes;
- /c/ had been mapped to Ukrainian ч even though the source phoneme is conventionally represented as [c], making ть a closer Ukrainian practical approximation;
- /h/ had been mapped to г, which is weaker phonetically than х for the source [h];
- /w/ and /ʋ/ were unnecessarily collapsed in the practical policy;
- the representative /kiə/ example was written as «кіа», which was corrected to «кіє» as a more transparent Ukrainian sequence.

The new adversarial corpus includes ខ្ញុំ, សង្គ្រាម, ហើយ, ស៊ី, សញ្ញា, ច្រើន, ប៉ី and a negative multiple-shifter case. These are regression fixtures, not a claim of complete lexical coverage. The parser now explicitly records register-shifter decisions and flags multiple-shifter structures as EVIDENCE_LIMITED.

External evidence used for this review: Unicode Khmer encoding/register documentation; R12A Khmer orthography notes; and the documented Khmer-Russian practical transcription tradition as a comparator. The Ukrainian layer remains a project proposal and still requires an adjudicated Ukrainian corpus before empirical accuracy can be claimed.


## Final consistency pass — 2026-10-06

The web-facing explanation was re-audited against the canonical Ukrainian policy and the adversarial parser work. A stale system-page table was found and removed: the page now agrees with the policy for /c/ → ть, /cʰ/ → ч, /h/ → х, /ʋ/ → в and /w/ → у. The current `src/khmer_ua/ipa.py` contains a regex-based Phnom Penh /r/-loss profile transformation. Its test coverage is minimal and its environments have not been independently validated against a full source-backed matrix; treat this as provisional and audit before expanding it. This is a remaining inconsistency with earlier documentation that said the transformation had been removed.

The web fixture corpus includes Unicode/R12A representative cases for register shifters, coeng clusters, pre-base vowels, long vowels, repeated nyo, coeng-r and the ប៉ exception, plus a negative multiple-shifter case. For representative Unicode examples, the corpus keeps the Unicode 17 IPA forms even where lexical dictionaries provide alternative phonetic analyses.

The system page and web structural tests now explicitly guard against stale transcription mappings. Academic paragraph-logic review of the updated system page returned no issues.

Pipeline status is revision-specific. Check the latest Quality and Pages workflow runs before asserting a green build; successful CI remains separate from linguistic accuracy validation.


## External IPA and benchmark audit — 2026-10-24

- The Python/browser profile-boundary correction and fail-closed gold-provenance gate are merged; ADJUDICATED rows require non-empty IPA, source_id and profile.
- Khmer Phonemizer 0.0.3 completed 6 probes with 0 runtime errors in [run 40121359605](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/40121359605). The report records raw phone-token arrays, but they are not directly string-comparable to source IPA until tokenization, syllabification, stress and notation conventions are reconciled.
- Independent gold count remains 0 and accuracy is null. Do not promote source-attested but unadjudicated examples into the score denominator. The remaining acceptance gate is a representative, source-located, independently adjudicated Khmer corpus and expert review of the Phnom Penh /r/-loss profile.
- Latest smoke artifact ZIP SHA-256: `3cd5ad913909cd1ff692c192614f354b707f705c1b6a2f1dc7ad971a4baf63a5`.


## Ukrainian target-policy audit — 2026-10-30

**Status: DONE_VERIFIED for the scoped target-policy change; broader Khmer phonology remains PARTIAL.**

- The canonical practical policy now marks aspirated IPA with an ASCII apostrophe after the Ukrainian base consonant, including the existing colloquial /cʰ/ profile.
- /h/ maps to г, /ɡ/ to ґ, and genuine /x/ to х. The policy does not equate foreign /h/ phonetically with Ukrainian /ɦ/.
- Ukrainian affricate mappings include /t͡s/ → ц, /d͡z/ → дз, /t͡ʃ/ and /tɕ/ → ч, /d͡ʒ/ and /dʑ/ → дж. Supported palatalization is kept explicit; sequences are not automatically fused.
- /ʔ/ is not aspiration and does not generate the marker.
- Python tests passed (82 tests, 25 subtests); the complete web check workflow passed in [41076121018](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41076121018).
- Draft PR #59 carries the changes; PR #58 is not modified. No merge or deployment was performed.
- No new pronunciation source or gold label was fabricated. Existing independent lexical/audio adjudication remains absent; this target-policy change does not increase accuracy evidence.


## Final romanization / dual-method audit — 2026-10-31

- PR #65 records BGN/PCGN 1972 as the selected reference profile, supported by UNGEGN and the official PCGN guide. It is not represented as a reversible or official Cambodian national orthography.
- PR #66's first data draft was superseded by PR #67 after direct PCGN 2017 PDF reconciliation. The canonical data file now contains exactly the 22 official consonant/subscript rows, with exact source units and the U+2019 apostrophe marker; row 18 notes that ឡ has no subscript form. Tests validate exact source sequences, romanization values, source locators and uncertainty statuses.
- PR #68 adds separate phonetic and romanization tabs. Phonetic remains IPA-first. Romanization displays the current BGN/PCGN-derived Latin output and an explicit PARTIAL Ukrainian state; no phonetic fallback is permitted.
- Main quality workflow [41230505480](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41230505480) passed on a351b0f66a608d7b4372e7c7bd0179808488be70.
- Pages deployment [41230505474](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41230505474) succeeded at https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System-/ and deployed a351b0f66a608d7b4372e7c7bd0179808488be70.
- Remaining: the @gmana ASCII simplifier is not fully conformant to PCGN 1972; the contextual vowel/shortening/coda/diacritic/numeral matrix is not yet canonical machine-readable data; the independent syllable-level romanization → Ukrainian adapter is not implemented; independent lexical IPA gold remains 0. This is still a research prototype, not a validated production transcription standard.


## Romanization inventory CI reconciliation — 2026-10-31

- Latest repository head before this audit update: `ec75558c862666f38496cdbc02443e3885bf5202`.
- The exact-head PCGN inventory workflow [41233203184](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41233203184) completed successfully. Its `test` job completed Python tests, web checks and the site build without a failed step.
- The 37-row vowel-source inventory and 16-row marks/numerals inventory now have exact source-glyph/romanization test evidence. Their bounded inventory tasks are `DONE_VERIFIED`; the complete context-dependent vowel/rime matrix and runtime semantics remain `PARTIAL`.
- The broader romanization test task remains `PARTIAL`: mixed-script, punctuation, malformed-unit and ambiguity coverage still requires explicit acceptance tests. The BGN/PCGN runtime implementation and independent romanization → Ukrainian syllable adapter remain incomplete.
- This run does not change phonetic evidence: independent lexical IPA gold remains 0, the contextual source-to-IPA algorithm is incomplete, and no accuracy metric is justified.
- No runtime code or Pages build inputs changed in the inventory/documentation checkpoint. The live Pages deployment evidence remains the earlier successful deployment recorded above; this checkpoint did not trigger a new deployment.
- Next work should prioritize the official PCGN context rules and the source-aware vowel/rime × consonant-series × shortening × coda representation. Ukrainian candidates must remain unassigned where the evidence does not support them.


### Exact workflow log verification detail — 2026-10-31

Workflow [41233203184](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41233203184), job 124631488043, was inspected directly:
- pytest -q: **87 passed, 25 subtests passed**.
- npm run check: all configured web-engine, runtime, register-shifter and romanization checks passed.
- npm run build: Vite production build passed, emitting the service and methodology pages plus asset bundles.
- Non-fatal warnings: Node punycode deprecation and npm install-script advisory. No workflow step failed.
- This is exact-head software verification of the bounded inventory, not evidence of full PCGN contextual coverage or phonetic accuracy.

 
### Responsive layout merge — 2026-10-31

- PR #78 merged as `3b6e08177f9c90dddb27e787cc7a6deaa015c33e`; 53 CSS override lines added to `src/styles/main.css`.
- Exact-head CI [41234615041](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41234615041) passed Python tests, configured web checks and Vite production build.
- Existing IPA/method-switch styling was preserved. PR #64 remains open and unmerged because its branch is diverged and its stylesheet replacement risks regressing newer UI.
- This is UI verification only. Contextual PCGN runtime, complete vowel/rime matrix, independent Ukrainian adapter, and adjudicated phonetic gold remain incomplete. No Pages deployment is claimed here.


### Sentence-level source-preservation regression — 2026-10-31

- PR #80 merged as `14113b5d45bbd36e53510b24a6f48f565a54bcd0`; exact-head Quality CI [41238197962](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41238197962) passed Python tests, Node runtime/web checks, and Vite build.
- The supplied Khmer sentence is now covered by a regression that reconstructs the complete normalized source from rendered engine units, including spaces and punctuation.
- The check does not add IPA or Ukrainian lexical gold. Full contextual Khmer phonology, BGN/PCGN runtime, independent romanization-to-Ukrainian adapter, and adjudicated corpus remain incomplete.
- Pages deployment [41237778259](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41237778259) succeeded on `cb48d4c660d3e7f826c677d871654157914ae59c`; no deployment is attributed to the test-only PR.


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

## Full-sentence Khmer romanization integration — 2026-10-31

- PR #87 merged as \`7d058faaf02ebf542fedc8b186d11a88c5318ec4\`; exact-head Quality CI [41240282424](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41240282424) passed Python (87 + 25 subtests), Node checks and Vite build.
- PR #89 merged as \`076ffaa1523afa7cc9ec9b8c2ca8e3a83cea101f\`; exact-head Quality CI [41241149726](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41241149726) passed the same configured gates.
- Runtime now passes the whole input directly to \`khmerToLatin\`; test coverage checks the exact greeting sentence, full conversion of Khmer letters/signs, and preservation of spaces, \`!\`, and both \`។\` punctuation marks. The package documents whole-text whitespace/punctuation handling and repetition-mark behavior: https://www.npmjs.com/package/@gmana/km-translit.
- The test does not claim word segmentation inside unspaced Khmer runs, complete PCGN 1972 conformance, or an independent Ukrainian adapter. Those remain PARTIAL/TODO; independent lexical IPA gold remains 0.
- PR #88 was closed as superseded due its stale base and incorrectly escaped regex. PR #64 remains open and unmerged; no CSS replacement was ported. No post-merge Pages deployment is claimed.

## Short Khmer mixed-text romanization regression — 2026-10-31

- PR #92 merged as \`99638ea6758d1553f3853d163c4b42ad8fe0741d\`; exact-head Quality workflow [41242382955](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41242382955) passed Python, Node web checks and Vite build.
- The short sample \`សួស្តី 123! ភាសាខ្មែរ។\` verifies that ASCII digits, spaces, \`!\` and Khmer \`។\` survive the whole-text romanizer while Khmer letters convert. Tests only; no runtime or Pages input changed. Not linguistic gold.


## Native numerals and mixed Latin preservation — 2026-10-31

- PR #94 merged as `48e5d6c05d4a6ade8019c853135b7e2f6d655591`; exact PR-head Quality checks [41242836968](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41242836968) and [41242823462](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41242823462) passed.
- `២០២៦ ABC-42, សួស្តី។` verifies preservation or explicit Arabic rendering of Khmer numerals, ASCII digits, Latin text, spaces, comma and Khmer sentence-stop punctuation while converting Khmer letters. This is not PCGN numeral gold or proof of complete word segmentation/UA adaptation.
- PR #92 covers ASCII-number mixed text; PR #89 covers a full greeting sentence. Tests only; no runtime or Pages input changed.


### Main-head CI and Pages verification — 2026-10-31

- Current main `1a6921fc75dd011bc8097f6636b8077fc7c59cff` passed Quality workflow [41243972009](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41243972009) and Pages deployment [41243971788](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41243971788). The deploy job's deployed-site/runtime smoke test passed.
- Whole-text romanization coverage on main includes full/short sentences, native and ASCII numerals, Latin mixed text, whitespace and Khmer punctuation. The phonetic route continues to withhold unsupported contextual analyses rather than substituting romanization or guesses.
- PR #64 remains open and unmerged because its branch is diverged and its stylesheet replacement is broader than the focused responsive change already merged in PR #78.
- These checks establish software/build/deployment integrity, not full PCGN conformance or independent pronunciation accuracy. The Ukrainian romanization adapter and independent IPA gold remain incomplete.


### Post-merge PR #95 main and Pages verification — 2026-10-31

- PR #95 merged as `28a9bbb909ca57735ceca92f262c2de9eeb43396`. Exact-main Quality [41246343908](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41246343908) and Pages deployment [41246343845](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41246343845) passed; deployed-site/runtime smoke test succeeded.
- This is documentation-only synchronization. Whole-text romanization regression coverage remains bounded engineering evidence; contextual PCGN implementation and the independent syllable-level Ukrainian adapter remain incomplete.
- PR #64 remains open and untouched; current compare is 7 commits ahead / 35 behind, with changes limited to the old layout/CSS snapshot and its test.


## Whole-message mixed-script segmentation regression — 2026-11-01

- PR [#97](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/97) merged as `72e4644204c879f905ebaa20dddd2d00b6583d32`.
- Added a canonical adversarial case containing Khmer, Latin identifier, ASCII digits, Khmer numerals and punctuation, tab, CRLF, U+200B and an unsupported symbol.
- The test consumes the canonical fixture, requires exact reconstruction from `segment_syllables()`, confirms a supported Khmer example remains structurally established and confirms the unsupported symbol remains locally invalid/unsupported.
- Exact PR-head Quality checks [41289845696](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41289845696) passed: Python tests, web checks and production build.
- The fixture has `ipa: null` and explicit non-phonological provenance; it is structural/source-integrity evidence, not IPA gold or an accuracy benchmark row.


## Current-head reconciliation — 2026-11-01

- Audit baseline: `c0a2b33c86791b6546e1158c62043fd23acc1f60`; exact-main CI: Quality 41326462947; Pages 41326462993; latest check completed successfully.
- The canonical gold TSV currently has a header only. Independent adjudicated IPA gold = 0; accuracy is not measured and must remain null.
- Current language-specific unresolved tasks and acceptance criteria are recorded in [LINGUISTIC-COMPLETION-REGISTER-2026-11-01.md](audits/current/LINGUISTIC-COMPLETION-REGISTER-2026-11-01.md). This register does not replace historical audit evidence.
- CI success is limited to configured engineering checks. It does not establish expert phonetic correctness, production readiness, manual accessibility QA or rights to redistribute third-party assets.


## Independent IPA gold corpus audit — 2026-11-01

The repository now has a standard-library JSONL validator, five versioned JSON Schemas, a source-license registry, independent annotation/adjudication records, deterministic split manifests, a typed IPA export into the existing benchmark and a tag/manual gold release gate. The corpus files remain empty and `gold.tsv` remains header-only. This is infrastructure completion, not scientific completion: independent expert gold=0, accuracy=null, and production readiness remains blocked.

Blind annotation cannot be guaranteed in a public Git repository. Two submissions must be collected separately in a controlled channel and merged only after both are locked. Every future source still requires a human-verified license/permission locator; a registry entry is not itself a grant of rights.


## 2026-11-01 closeout

The independent IPA gold-corpus implementation and Khmer evidence matrix are in [PR #103](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/103). PR CI passed 136 Python tests + 27 subtests, browser register-shifter contract, web checks and Vite build. The source-backed matrices do not establish every vowel × series × coda cell; independent gold remains 0. Main was not changed. Legacy PR #64 remains untouched.


## CI action runtime audit — 2026-11-01

All five workflows now use current Node.js 24-compatible action majors. Exact-head checks passed: [Quality checks 41339636053](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41339636053), [Goruut 41339636042](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41339636042), and [G2P smoke 41339636117](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41339636117). CI maintenance does not establish phonological accuracy or expert gold.


## PR integration reconciliation — 2026-11-03

- PR #108 merged the browser result-rendering hotfix; exact-main Quality, Chromium and Pages/deployed-site smoke passed.
- PR #112 merged the manifest-wide split identity invariant and separate-manifest acceptance; exact PR-head Quality/browser checks passed, followed by exact-main Quality, browser and Pages/deployed-site smoke.
- PR #113 merged source registry, external corpus triage, bibliography and provenance-test updates; exact PR-head Quality and browser checks passed.
- PR #115 merged the single careful-citation profile and removed deterministic colloquial /r/-loss rewriting; exact PR-head Quality and browser checks passed, followed by main Quality, Chromium and Pages/deployed-site smoke.
- PR #116 merged the glossary, codebase map and agent guidance. PRs #107 and #114 were superseded by these scoped integrations; neither broad profile branch was merged wholesale.
- Independent adjudicated IPA gold remains 0 and empirical accuracy remains null. CI verifies engineering and deployed assets, not pronunciation accuracy or manual accessibility.


## Romanization implementation audit — mainline 2026-11-12

### Standard-scope correction: Cambodian national 1997 profile

The Cambodian national report to UNGEGN (GEGN.2/2023/104/CRP.104) says the national romanized writing system is based on the 1997 transcription system instead of the 1972 transliteration system; the UNGEGN Working Group's status report (GEGN.2/2023/11/CRP.11) corroborates that replacement. The project BGN/PCGN 1972 matrix is still a valid, fully source-backed research crosswalk, but it must not be represented as the current national Cambodian system. The primary 1997 national specification is not yet available in the inspected sources. The similarly dated ALA-LC Khmer 1997 table is a distinct library-cataloguing profile, not a substitute. Track this as EVIDENCE_LIMITED pending primary-source retrieval and a profile decision.


The current orthographic romanization path is integrated end to end for the available source output: BGN/PCGN-derived ASCII Latin → separate Ukrainian orthographic adapter. The 22-row consonant target matrix and 37-row vowel/rime target matrix are populated and tested. PR #164 added the adapter; PR #165 records post-merge evidence. Current main is `a86a59cf082d547563b45374ced9dfb45c5cd8db`; exact-head Quality [43228414756](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43228414756), browser [43228414938](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43228414938), and Pages [43228414646](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43228414646) passed.

Acceptance remains PARTIAL: the current `@gmana/km-translit` ASCII profile drops BGN/PCGN diacritics, so the Ukrainian adapter cannot reconstruct contextual distinctions already lost upstream. The output is correctly marked PROVISIONAL. This orthographic route does not use IPA. Draft G2P PR #153 remains open and untouched; it is not a dependency of this work. No pronunciation accuracy, IPA gold, or official Ukrainian-standard claim is made.

The 2025 UNGEGN Asia South-East Division report (GEGN.2/2025/73/CRP.73, p. 3) confirms the October 2023 Cambodian national gazetteer uses the 1997 transcription system: https://unstats.un.org/unsd/ungegn/sessions/4th_session_2025/documents/GEGN.2_2025_73_CRP73_item4a.pdf


## Test-discovery audit — 2026-11-12

The Khmer orthographic adapter's unit test file existed but was omitted from both `npm test` and `npm run check`; browser smoke covered only a single example. PR #167 fixed this by wiring the unit suite into both commands and asserting every distinct PCGN consonant romanization token. It merged as `f0485892f5d4b16e5fbe0ded6f8e083d8b044f4b`. Exact-main Quality [43250158336](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43250158336) and browser [43250158628](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43250158628) passed. Remaining coverage limitations are recorded in KHM-ROM-TEST-001.


## Evidence conflict update — Cambodian 1997 transcription system — 2026-11-12

The Cambodia national report (GEGN.2/2023/104/CRP.104) and UNGEGN 2025 regional report (GEGN.2/2025/73/CRP.73) say national gazetteers used the 1997 transcription system. The UK PCGN's May 2026 *Cambodia Toponymic Factfile* (pp. 1–2) says the system has not yet been implemented consistently and awaits evidence of consistent official use. The 2023 Gazetteer primary table is now located (pp. vii–viii); its foreword states departmental use but provisional status pending formal National Commission approval. The statements are compatible as provisional use versus consistent national implementation. Keep KHM-ROM-NATIONAL-1997-001 EVIDENCE_LIMITED until formal adoption evidence and source reuse rights are resolved. BGN/PCGN 1972 remains the project's current source-located research profile; ALA-LC 1997 remains a distinct cataloguing profile.


## Primary Khmer 1995/1997 table located — 2026-11-12

The Ministry's *Gazetteer of Cambodia* (October 2023), pp. vii–viii, contains the “Romanized System for Khmer” table labelled “Prepared by Geography Department, 1995. Last modification 1997”. The foreword states that the system had been used by the Geography Department, would be submitted to the National Committee for consideration/adoption, and that this Gazetteer is a provisional release pending National Commission approval. This reconciles the Cambodia/UNGEGN gazetteer-use reports with PCGN's May 2026 statement that the system is not yet implemented consistently: provisional departmental use is documented, but formal adoption/consistent nationwide implementation remains unproven. Original PDF copyright © 2023 by the Geography Department; ODC's record says no license is given for the PDF. Keep KHM-ROM-NATIONAL-1997-001 EVIDENCE_LIMITED until adoption evidence and reuse rights are resolved. Do not relabel BGN/PCGN 1972 rows.


## Khmer romanization matrix/runtime parity — 2026-11-12

A second test-discovery gap was identified after the adapter suite was wired into `npm test`: the consonant test still duplicated all 22 source rows as a hard-coded array. That could pass while the canonical CSV changed independently. The test now parses `data/khmer/romanization_ukrainian.csv` and exercises each row's romanization/target pair, including both contextual `b,p` alternatives and the U+2019 marker. This is a source-of-truth parity safeguard, not linguistic adjudication. Vowel coverage remains limited to the 33 ASCII candidates that the current upstream package can emit; diacritic/contextual PCGN output is still lost upstream.


## Post-merge Khmer romanization matrix/runtime parity verification — 2026-11-12

PR #170 merged as `c5c26082abff87ce6224e00a68047620f9d9975f`. Exact-head Quality workflow [43266798081](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43266798081) passed the Python suite, Node web checks and Vite build; exact-head browser workflow [43266797880](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43266797880) passed Chromium visible-results smoke. The bounded canonical 22-row consonant matrix/runtime parity test is now DONE_VERIFIED. This does not resolve upstream PCGN diacritic loss, contextual vowel/rime coverage, Ukrainian expert adjudication or IPA gold. Mainline Quality/browser/Pages checks were queued after merge and remain separately tracked until completed.


## Khmer real-package whole-message adapter coverage — 2026-11-12

The test suite now includes a regression that exercises the actual `@gmana/km-translit` package through the Ukrainian orthographic adapter on a mixed whole message. It checks visible native/Arabic numerals, mixed Latin identifier, ASCII punctuation, tab, CRLF and Khmer sentence-stop preservation, while ensuring Khmer letters do not leak into the Latin-output route. This is a bounded software integration probe, not evidence of complete PCGN marks/numerals coverage or Ukrainian linguistic accuracy. Exact-head CI remains pending.


## Khmer real-package whole-message adapter verification — 2026-11-12

PR #172 merged as `054bc8823ba1f109ee102eda5e966edade1c4886`. The new regression exercises the actual `@gmana/km-translit` package through the Ukrainian adapter and verifies native-or-Arabic numerals, mixed Latin text, ASCII punctuation, tab, CRLF and Khmer sentence-stop preservation. Exact PR-head Quality [43267521108] and browser smoke [43267521498] passed. Mainline Quality [43267655512], browser smoke [43267655359], and Pages deployment/deployed-site smoke [43267655210] all passed on the merge commit. This closes only the bounded real-package whole-message engineering regression; full PCGN conformance and linguistic accuracy remain PARTIAL/EVIDENCE_LIMITED.


## Khmer numeral matrix/runtime discrepancy — 2026-11-12

A data-driven test against `data/khmer/romanization_marks_numerals.csv` exposed that the adapter passed native Khmer digits through unchanged although the canonical target matrix proposes Arabic digits. The RED run was exact and localized: Quality workflow [43268170106](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43268170106) failed only the new numeral assertion (`'០' !== '0'`); the preceding 9 adapter tests passed. The adapter now maps U+17E0–U+17E9 to 0–9 and increments the mapped count. The real-package mixed-message regression now requires `2026`. Exact GREEN CI remains pending.


## Khmer numeral crosswalk implementation verification — 2026-11-12

The adapter now maps all ten Khmer numeral code points U+17E0–U+17E9 to Arabic digits 0–9. The RED regression in [43268170106](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43268170106) failed on the expected native-versus-Arabic mismatch; after the implementation, exact PR-head Quality [43268412329] and browser smoke [43268412356] passed. PR #174 merged as `ae890fdd436aed9c0fab077401e7612153ce2e6a`. Exact mainline Quality [43268536002], browser smoke [43268536046], and Pages deployment/deployed-site smoke [43268535985] passed. The numeral slice is DONE_VERIFIED; contextual diacritical-mark handling and full BGN/PCGN conformance remain open.


## Khmer vowel matrix executable crosswalk coverage — 2026-11-12

PR #177 (`19a36f820625f53c6f50fbbe810bfbd074bb1ee7`) adds a data-driven adapter test for all 37 independent-vowel, dependent-vowel and vowel/coda rows. The test converts PCGN diacritic forms to the ASCII aliases expected from the existing upstream dependency and verifies that each result belongs to the row's Ukrainian candidate set without unsupported fragments. Exact PR-head Quality [43275618264] passed (194 Python tests + 62 subtests and 12 Node adapter tests); browser smoke [43275618099] passed. This verifies inventory consistency only, not contextual vowel selection, phonetic correctness, or PCGN standard conformance. Upstream diacritic loss remains a runtime limitation.


## Repository information architecture and branch reconciliation — 2026-11-15

- Inspected the live default branch `main` at `25cb1f4db5d0c971184f2393751506daa19f8df2`, its recursive tracked tree (149 files), the current documentation/data/code layout, recent commits, workflow-run inventory, and all branches returned by the repository branch endpoint.
- The documentation was already substantial but lacked a single navigational entry point. Added `docs/README.md` as the index; it points to, and does not replace, the canonical master handoff, architecture, current completion register, source registry or matrices.
- Reconciled the architecture and codebase map with the current implementation: Python parsing, deterministic lexical/rule engine, supplied-IPA validation and longest-match Ukrainian adapter; browser structural/fixture path; and the independent BGN/PCGN-derived romanization path. Clarified that the former hybrid provider-voting ensemble is removed and external candidates are diagnostic only.
- Recorded the five requested engineering/design repositories as pinned methodology references in `docs/agents/methodology-references.md`. No third-party code, skill pack, design database, runtime dependency or linguistic evidence was imported.
- Branch comparison showed historical branch tips are generally diverged from current `main`, including branches whose implementation was subsequently integrated through other PRs. At baseline inspection the pre-existing open PR was draft #153; this documentation pass opened PR #179. PR #153's research branch is not a safe blanket merge. No octopus merge, force update or branch deletion was performed. A single active task branch was created from the exact current `main` head.
- Environment limitation: the connected GitHub interface supports repository inspection and file/commit writes, but not a local checkout or local shell execution in this run. Do not claim local tests/builds were run; exact-head hosted checks must be checked separately.

**Disposition:** documentation/navigation and branch policy are updated on the dedicated task branch. Linguistic completion, independent IPA gold, full BGN/PCGN conformance and manual accessibility review remain outside this documentation-only change and retain their existing status.


### Exact-head verification closeout — 2026-11-15

- Documentation branch commit `41b88ecdc7545b4f5f60738bc528c6d56e55c5a6` passed push Quality [43692108930](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43692108930), PR Quality [43692138758](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43692138758), and Chromium browser smoke [43692138745](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43692138745).
- Quality covered corpus-structure validation, Python tests, Node web checks and Vite production build. Browser smoke covered deterministic web checks, production build and Chromium visible-results verification.
- The new documentation index's 30 relative Markdown links were resolved against the exact commit tree; zero missing internal targets.
- PR #179 is reported mergeable/clean. Local shell execution was unavailable; the evidence above is hosted CI, not a local test run.


## License metadata mismatch — owner decision required — 2026-11-15

The package metadata in `pyproject.toml` declares MIT, but the inspected tracked tree contains no root `LICENSE`, `LICENSE.md` or `COPYING` file and GitHub repository metadata reports `license: null`. This is a governance inconsistency. **BLOCKED:** the repository owner must confirm the intended license, add its canonical text and align package/repository metadata. No license was selected or generated by this audit.


### Branch and PR disposition detail — 2026-11-15

The pre-existing inventory contained 40 non-main branches. Their tips were compared against main. PR history confirms that the recent romanization, grapheme-accounting and crosswalk branches associated with merged PRs #157–#178 are already integrated; they should not be merged a second time. Model-consensus research PRs #150/#151 were closed unmerged and superseded by deterministic-engine PR #152. Earlier practical-adapter PRs #154/#155 were closed unmerged and superseded by merged PR #156. Draft research PR #153 remains open and evidence-limited. The documentation branch is a separate, single active task branch. Historical refs remain preserved because the connected interface does not expose a branch-delete operation and no destructive archival was requested.


## Documentation PR #179 merge — 2026-11-15

The documentation/information-architecture batch was merged to `main` by squash commit `e84d530b0a4355d450ed1f7e2568a2c58ca4e9c4` (PR #179). Exact PR-head Quality and Chromium smoke passed on `db0e1b930d4566f6443b2b3a19fd811269e33adb`: runs 43692418605, 43692421394 and 43692421391. The docs index has 30 validated relative links and no missing targets. Mainline Quality, browser and Pages workflows triggered by the merge were still running at closeout; their final state is tracked separately. The license metadata inconsistency remains an owner decision blocker.


### Final mainline verification — 2026-11-15

Main commit `8b6dd5a597a670e7c3ff7bc440b2a97b4762060e` passed Quality [43692567616], Chromium browser smoke [43692567608], and Pages deployment/deployed-site smoke [43692567615]. All conclusions were SUCCESS. This is hosted CI evidence, not a local test run.


## PR #153 patch-level reconciliation against current main — 2026-11-15

- Rechecked live main at `b2743a2c0f0a843eec9acbab538adad5cfa7cad5` and PR #153 head `bddb0186c9e62abd57827fa54233ebbfaa0540e2`. The merge base is `2fe36aa1eb64cc47fb60ab1b37561f40d57202a7`; the branch is **34 commits ahead / 26 behind**, status `diverged`, with 18 changed files. PR metadata remains open + draft + `mergeable=false`. There are no submitted reviews or PR comments.
- The current-main side contains 26 commits since the merge base and changes 37 paths. Six paths overlap the PR's changed-file set: `README.md`, `data/khmer/sources.json`, `docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md`, `docs/audits/current/LINGUISTIC-COMPLETION-REGISTER-2026-11-01.md`, `src/khmer_ua/__init__.py`, and `tests/test_rule_engine.py`. This confirms a non-trivial rebase/reconciliation requirement; do not merge the branch wholesale.
- Exact current PR-head hosted checks: Quality run [43084554473](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43084554473) **SUCCESS**; Chromium browser smoke [43084554830](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43084554830) **SUCCESS**; optional G2P benchmark [43084554487](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43084554487) **SKIPPED**. Combined commit status returned no status entries. No local checkout or local shell tests were available.

### Patch-level disposition

| Area | Finding | Disposition |
|---|---|---|
| `src/khmer_ua/hybrid.py`, package exports, rule-engine tests | PR replaces the current compatibility shim (where `HybridKhmerEngine` aliases the deterministic rule engine and injected providers are rejected) with an external-candidate wrapper and optional provider factories. Current main explicitly documents that external G2P execution is not part of this public API. | **Do not merge as-is.** Any future candidate harness must live behind an explicitly research-only boundary and must not silently change the published API contract. |
| Candidate validation | `_candidate` rejects empty output and literal `?`, but otherwise accepts arbitrary non-empty strings as complete IPA; it does not validate IPA symbols, typed status values, profile, or completeness. | **Acceptance gap.** Add a real typed IPA validation boundary and negative tests before considering reuse. Preserve raw provider output and uncertainty. |
| Provider ordering | Priorities determine execution/display order only; the code and tests do not use them as accuracy weights or promotion authority. | **Conceptually acceptable**, but only after API and validation reconciliation. |
| MekongPhon benchmark harness | New script computes Unicode-codepoint edit distance against upstream `pron_no_tones`, hashes source labels, omits source orthography/reference text from report records, and explicitly reports independent gold=0 / accuracy=null. | **Research-only / PARTIAL.** The metric is source-label concordance, not accuracy; it omits tone by construction. Keep outputs out of gold and production decisions. |
| Optional workflow | Benchmark job is manual-dispatch only and the exact-head optional run was skipped. | **Not runtime-verified in this checkpoint.** Do not claim the new model benchmark ran in this CI cycle. |
| MekongPhon source and model | The PR records a pinned model revision and a pinned upstream corpus snapshot, while explicitly noting unresolved corpus rights and unverified split independence. | **BLOCKED for repeatable project evaluation or data reuse** until rights and split provenance are independently resolved. The model card's code/model license does not settle corpus-data rights. |
| Khmer acoustic dictionary | PR records missing full dictionary and conflicting upstream entry counts/data-license declarations. | **BLOCKED; do not import or redistribute.** |
| Research documentation and registries | Some source metadata and diagnostic findings are useful, but several docs and registries overlap current-main edits and the PR's handoff contains stale base/head claims. | Reconcile item-by-item only after primary-source verification; do not copy stale handoff state. |

### Decision and acceptance criteria

**PR #153 remains BLOCKED and open as a draft; no branch, PR, or code was modified by this audit.** Reconsider only after (1) rebasing onto current main and resolving the six overlapping paths, (2) preserving the current deterministic published-output contract, (3) implementing typed IPA/profile/completeness validation for any candidate adapter, (4) resolving corpus rights and documenting train/evaluation split independence, and (5) obtaining exact-head Quality/browser evidence plus an explicitly dispatched benchmark run where rights permit. Independent Phnom Penh-profile adjudicated gold remains 0; empirical accuracy remains null.


## Historical branch comparison closeout — 2026-11-15

- Compared all **41 non-main branch refs** returned by the repository branch search against live main. Every tip is divergent rather than a clean ancestor because the repository has used squash merges and branch snapshots; ahead/behind counts alone therefore do not establish unmerged code. The compare endpoint returned per-branch file-level change summaries, which were reconciled against merged/superseded PR history.
- Recent romanization, grapheme-accounting, parser, numeral and adapter task branches associated with merged PRs #157–#178 are historical snapshots, not candidates for wholesale merge. Spot-checked blob identity confirms the fix/khmer-unmodeled-letter-trace branch's data/khmer/signs.json, src/khmer_ua/parser.py and tests/test_parser.py are byte-identical to current main. The test/khmer-numeral-crosswalk-runtime branch's runtime adapter is also byte-identical to main; its test file has since evolved on main. The older test/complete-grapheme-accounting parser/test blobs differ from current main and are superseded by later parser/test changes; do not cherry-pick that snapshot.
- The feat/khmer-romanization-ukrainian-matrix-completion, feat/romanization-to-ukrainian-runtime, and associated test/closeout branches are stale task snapshots whose implementation path is represented by merged mainline PRs; matrix/runtime changes should be made against current main only, not by merging their branch tips.
- The practical-adapter branches (feat/khmer-ukrainian-practical-adapter*) contain overlapping historical implementation and documentation; earlier PRs #154/#155 were superseded by #156. The deterministic-engine research branches (research/khmer-hybrid-engine-2026-11-11, research/khmer-engine-benchmark-expansion-2026-11-11) are superseded by the deterministic-engine integration and the later evidence-gated draft #153. The older coverage, font-fallback and external-G2P branches are hundreds of commits behind and are not safe integration bases.
- No historical branch was force-updated or deleted. The available connected GitHub operations did not expose a branch-delete operation. Preserve refs; use current main for all future implementation.

### PR #180 merge closeout

Documentation-only PR [#180](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/180) was squash-merged as 509a35f0d9899959c08a809d486e9c0e09d5c957. Its exact PR-head Quality [43693340334](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43693340334) and Chromium browser smoke [43693340375](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43693340375) both passed. The commit-run lookup did not expose post-merge mainline runs; this record does not claim that such mainline runs passed. PR #153 remains open, draft, and blocked as detailed above.


## Typed IPA candidate boundary — 2026-11-15

- Implemented in PR [#182](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/182), branch `feat/typed-ipa-candidate-validation-2026-11-15`, runtime/test head `a20f1d3f28cbe1a6a5f79cc7554afe4b47265a4a` (the subsequently updated PR head contains documentation-only audit/handoff additions).
- Added immutable `IPACandidate`, `IPACandidateStatus`, and `validate_ipa_candidate`; exported from the package API. Candidate metadata requires the selected Phnom Penh careful-citation profile, one of PHONEMIC / PHONETIC_BROAD / PHONETIC_NARROW, COMPLETE / PARTIAL, and a non-empty provider identifier. PARTIAL requires explicit uncertainty notes.
- The notation gate accepts Latin/Greek IPA segment letters, modifier letters, combining diacritics, IPA tone-bar symbols, click symbols, digits and a bounded set of IPA separators; it rejects unsupported scripts/symbols, orphan combining marks, malformed outer delimiters and non-NFC strings. It preserves the exact provider string, including tone, length, stress and syllable notation. This is a conservative notation check, not a complete IPA grammar, phonological validation, source verification or accuracy judgment.
- No external provider is executed, no candidate is automatically converted to gold, and the deterministic engine's output contract is unchanged.
- Exact-head Quality [43694149473](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43694149473): **SUCCESS**; Python suite: **206 passed, 62 subtests passed**; corpus-structure gate, web checks and production build completed successfully.
- Exact-head Chromium smoke [43694149458](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43694149458): **SUCCESS**, including visible-result verification.
- First CI attempt exposed three test failures because IPA tone-bar characters U+02E5–U+02E9 are Unicode modifier symbols (category Sk), not modifier letters; the gate was corrected to recognize the five IPA tone bars as explicit IPA symbols and the exact-head CI was rerun successfully.
- PR #153 remains separate and blocked by corpus rights/split provenance and its own diverged API patch. This PR addresses the candidate notation/metadata acceptance gap without importing its model, data, or provider runtime. Independent adjudicated IPA gold remains 0; accuracy remains null.


**CI scope note:** the successful Quality and Chromium runs were triggered for the final runtime/test code head before the two documentation-only audit/handoff commits. The GitHub connector exposed no new workflow runs for the later documentation-only head; no additional test run is claimed for those docs-only commits. Post-merge mainline CI is the final verification gate.


## Typed IPA validator integration closeout — 2026-11-15

- PR [#182](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/182) was squash-merged into main as c69789b21bffb306497758a1181bef0d36459bd5. Its source/test head before documentation-only follow-up was a20f1d3f28cbe1a6a5f79cc7554afe4b47265a4a.
- Exact code-head Quality [43694149473](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43694149473) passed: 206 tests, 62 subtests, independent IPA gold corpus structure validation, web checks and production build. Exact code-head Chromium smoke [43694149458](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43694149458) passed, including visible-result verification.
- Documentation-only audit/handoff commits were added after that code-head CI. No additional workflow run was exposed for the final docs-only PR head; the code head itself was tested. The merge commit is recorded above; no post-merge push-run success is claimed by the available connector.
- The PR #153 candidate-validation gap is now addressed by a standalone, typed, non-promoting validator on main. PR #153 itself remains open/draft and blocked by its diverged provider API, corpus rights and split-independence evidence. No MekongPhon model or corpus data was imported.
- The validator does not establish IPA phonological correctness, completeness, independent adjudication, or source redistribution rights. Independent adjudicated gold remains 0 and empirical accuracy remains null.


## PR #153 reconciliation and safe research-harness port — 2026-11-15

### Reconciliation
- Current main: `5e082024b7ae871b1bb95219ea80e5b87502b66e`.
- PR #153: open/draft, head `bddb0186c9e62abd57827fa54233ebbfaa0540e2`, base SHA `2fe36aa1eb64cc47fb60ab1b37561f40d57202a7`; current-main comparison is 34 ahead / 31 behind with 18 changed paths.
- Its `src/khmer_ua/hybrid.py` is incompatible with the current API and bypasses `validate_ipa_candidate`: it accepts arbitrary provider strings/dicts and treats any non-empty candidate without "?" as acceptable. Do not merge this runtime.
- Its documentation and data updates include useful research observations, but current main already contains newer versions of several PhonSobon, Google, and Khmer Acoustic Model records. Only the missing MekongPhon model record and its two historical diagnostic runs were selectively reconciled.
### Safe port
- Branch: `research/mekongphon-diagnostic-harness-2026-11-15`, based on current main.
- Port scope: pinned external benchmark script, tests, manual-only GitHub Actions workflow, MekongPhon source record, external candidate record, historical report checksums and caveats.
- No corpus rows, model weights, third-party implementation code, or provider runtime were copied. No external candidate is enabled by default or promoted to gold.
### Acceptance ledger
| Task | Status | Acceptance boundary |
|---|---|---|
| PR #153 patch/history reconciliation | DONE_VERIFIED (review) | Current-main diff and overlapping API contract reviewed; no blind merge |
| MekongPhon benchmark harness and tests | PARTIAL | Exact-head Quality CI and code review still required |
| Historical diagnostic provenance | DONE_VERIFIED (registry only) | 100 outputs, 64 strict source-attested matches, CER 12.539% on no-tone labels; independent gold 0, accuracy null |
| Typed provider adapter | BLOCKED | Must use `IPACandidate` / `validate_ipa_candidate`; explicit profile/kind/status/provider/uncertainty; preserve raw output |
| Corpus rights | BLOCKED | Rights holder must clarify license for pinned corpus revision; model license alone is insufficient |
| Train/evaluation disjointness | BLOCKED | Need checkpoint training-data manifest or independently verifiable split provenance |
| Independent Phnom Penh IPA gold | BLOCKED | Blind double annotation and adjudication, with tone/length/coda/syllable boundaries explicitly represented |


## PR #184 — final safe MekongPhon diagnostic harness verification — 2026-11-15

- Branch `research/mekongphon-diagnostic-harness-2026-11-15`, based directly on `main` at `5e082024b7ae871b1bb95219ea80e5b87502b66e`.
- Final code/test head `750a69b75ee7fa846572f63125d675e4557d12cc`: Quality [43695488162](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43695488162) SUCCESS (214 Python tests + 64 subtests; corpus structure gate, web checks, production build); Chromium [43695488169](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43695488169) SUCCESS (4 browser tests including visible-result verification).
- The benchmark script now records the source commit only when the default pinned corpus path is used or the caller explicitly supplies a revision. The model identifier is fixed to the audited BYU MATRIX model; report metadata cannot silently claim another model ID.
- The optional workflow is manual-dispatch only. The initial corpus-exporting Khmer Phonemizer job was removed before final verification because it uploaded source orthography/reference rows while corpus redistribution rights remain unresolved. The remaining job downloads the pinned external corpus only at explicit dispatch and uploads model diagnostic output, not source rows. No workflow dispatch/model inference occurred in this session.
- The report remains explicitly source-attested: 100/100 historical outputs, 64 strict matches, CER 12.539% on `pron_no_tones`; no tone evaluation, independent gold 0, accuracy null, training/evaluation split independence not established.
- PR #153's provider runtime was not ported because it bypasses `validate_ipa_candidate` and conflicts with the current compatibility API. PR #153 remains open/draft. PR #184 is the separate safe port; merge only after final docs-head CI.
- No local shell execution is claimed. Rights, split independence, typed provider adapter and independent Phnom Penh IPA adjudication remain BLOCKED.


## PR #184 mainline merge and verification — 2026-11-15

- Squash merge: PR #184 → `66c43e1772a4c871e06e625e80ad43da2d123c85`; starting main `5e082024b7ae871b1bb95219ea80e5b87502b66e`.
- Exact PR-head Quality [43695611313](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43695611313) and Chromium [43695611252](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43695611252) both SUCCESS. Python: 214 passed, 64 subtests passed. Browser: 4 passed including visible-result verification.
- Post-merge main Quality [43695677574](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43695677574), browser [43695677644](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43695677644), and Pages build/deploy [43695677607](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43695677607) all SUCCESS.
- PR #184 ported the pinned diagnostic runner, tests, manual-only neural benchmark workflow, and source/experiment evidence. It did not port the old HybridKhmerEngine provider runtime. The benchmark model is fixed to the audited model ID; custom corpus paths cannot silently inherit the default source revision. The workflow does not export source corpus rows.
- No optional workflow dispatch, external model inference, local shell, or local pytest execution occurred. Hosted CI verifies code/tests/build/browser/deploy only.
- PR #153 remains open/draft; no blind merge or branch rewrite. Independent gold remains 0, accuracy null, MekongPhon corpus rights unresolved, and train/evaluation split independence not established. The engine is not linguistically production-ready.


## PR #153 reconciliation — typed hybrid bridge — 2026-11-15

- PR #153 was compared against main: its head `bddb0186c9e62abd57827fa54233ebbfaa0540e2` is 34 commits ahead and 34 behind; the PR base SHA is `2fe36aa1eb64cc47fb60ab1b37561f40d57202a7`. Do not merge the branch wholesale.
- Reused existing mainline work instead of duplicating it: PR #184 already ported the pinned MekongPhon diagnostic harness, tests, manual-only workflow, and rights/provenance evidence. The PR #153 copy of `scripts/benchmark_mekongphon_model.py`, its benchmark tests, and the workflow changes were therefore not re-imported.
- Ported the useful hybrid runtime concept as a fresh implementation on top of the current main: `HybridKhmerEngine`, explicit provider injection, deterministic provider ordering, MekongPhon lazy adapter, command adapter, and failure isolation. Crucially, every candidate now passes through the shared typed IPA validator; bare string providers are rejected; PARTIAL requires uncertainty; raw IPA is retained; the deterministic final result cannot be overridden.
- Added `tests/test_hybrid_engine.py` for parity, typed boundary enforcement, malformed notation, missing uncertainty, provider order, failure isolation and factory exports. Added `docs/hybrid-engines.md` and updated README and deterministic-engine contract.
- Branch: `feat/typed-ipa-hybrid-bridge-2026-11-15`; based on main commit `d4c058b346d51179af85b3f8173af3ecc79b4adb`. Hosted CI is required before merge; no local execution is claimed.
- Not ported: old branch-wide edits to rule-engine tests/aliases that conflict with the current public API; duplicated benchmark harness/tests/workflow; model/data registry changes already superseded by PR #184. External model inference was not run. MekongPhon source rights and exact checkpoint train/eval split independence remain unresolved; independent adjudicated IPA gold remains 0 and accuracy null.


## PR #185 mainline integration — 2026-11-15

- PR [#185](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/185) selectively ported the hybrid runtime contract from draft PR #153 and merged into main as `71a0962ef4977aacde29ef016a13e108044d72b7`.
- Exact final source/test head: `1d93b823fd15f5fe57da527b2afb5cc86a4b8f0b`. Quality [43696684037](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43696684037) SUCCESS: 222 Python tests + 64 subtests; corpus validation, web checks and production build passed. Chromium [43696684048](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43696684048) SUCCESS, including visible-result verification.
- Hybrid provider candidates now pass the shared typed IPA validator. Bare strings, malformed notation and unsupported metadata are rejected; PARTIAL candidates require uncertainty; raw IPA and provenance are retained; deterministic IPA/Ukrainian output is not overridden. External adapters remain explicit opt-in and research-only.
- The benchmark runner/manual workflow from PR #184 were reused; duplicate versions in PR #153 were not re-imported. PR #153 remains open/draft and diverged; it was not merged wholesale.
- No external inference or local shell execution occurred. Corpus rights, checkpoint train/eval split independence and independent profile-matched IPA gold remain unresolved (gold 0; accuracy null). This merge does not make the engine linguistically production-ready.

## Mainline reconciliation closeout — PR #153 and external source triage — 2026-11-15

### Merged changes and verification

- PR #187 selectively added PhonSobon model/dataset records as non-IPA respelling resources, corrected the Khmer Acoustic Model dictionary count/license conflict, and recorded Google Language Resources and OpenSLR42 evidence boundaries. Merge: `1ef8578143bd2a0e9d55a46c0ddef4d0006dc5c3`. Exact-head Quality [43697879406](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43697879406) SUCCESS (222 tests + 64 subtests); Chromium [43697879409](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43697879409) SUCCESS.
- PR #188 completed the external candidate registry for the MekongPhon rule-based baseline and PhonSobon resources, preserving historical diagnostic runs and updating the research/benchmark docs. Merge: `34f9dbfd94788d1d1b9b64646354157d4741dfed`. Exact-head Quality [43698031836](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43698031836) SUCCESS (222 tests + 70 subtests); Chromium [43698031838](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43698031838) SUCCESS (4 tests).
- PR #153 was closed unmerged after comparison and selective reconciliation. Its old untyped hybrid runtime was superseded by PR #185; the safe benchmark harness was already in PR #184. No third-party data rows, model weights or source code were copied from #153.
- The documentation branch `docs/repository-information-architecture-2026-11-15` was reviewed. Shared index/agent files matched main; the branch's README, architecture and audit snapshots were older. It remains untouched.

### Current task ledger

| Task | Status | Evidence / remaining acceptance |
|---|---|---|
| PR #153 reconciliation | DONE_VERIFIED (review and selective port) | Safe source records ported in #187/#188; incompatible runtime/workflow excluded; original PR closed unmerged |
| PhonSobon model/dataset | PARTIAL | Source records and scope documented; output is Khmer-script respelling, not IPA; NCKL terms must be clarified before data use |
| MekongPhon rule-based baseline | PARTIAL | Source inspected and registered; not executed; pinned snapshot lacks declared root license and output/profile compatibility is unverified |
| Khmer Acoustic Model dictionary | BLOCKED | Entry count and CC BY 4.0/CC BY-SA 4.0 conflict; full dictionary absent from inspected tree |
| Google Language Resources | PARTIAL | Bounded extraction only; Latin-script keys in inspected subset; full lexicon and Khmer-specific data rights not verified |
| OpenSLR42 audio | PARTIAL | Current official page lists male archive while 2018 paper reports female speakers; manifest/checksum and speaker metadata reconciliation required |
| Repository LICENSE | BLOCKED (owner decision) | `pyproject.toml` declares MIT but root `LICENSE` is absent; do not add license text without owner confirmation |
| Independent Phnom Penh IPA gold | BLOCKED | Adjudicated gold remains 0; acceptance requires rights-cleared, profile-matched, blind double annotation and independent adjudication |
| MekongPhon training/eval independence | BLOCKED | Checkpoint training-data manifest or independent split provenance is unavailable |
| Manual accessibility review | PARTIAL | Hosted Chromium smoke is green; manual keyboard, assistive-technology, mobile and visual audit is not evidenced |

The repository remains a research platform / partial prototype. No empirical phonetic accuracy is claimed.

## Phonotactic and PPK pitch evidence reconciliation — 2026-11-15

- Added source records for Nacaskul (1978), Unicode L2/22-290, Ding et al. (2018), Mam et al. (2025), and the Sak-Humphry (2025) publisher preview.
- The evidence now distinguishes major-syllable restrictions, minor type-A/type-B restrictions, and orthographic coeng constraints. Nacaskul's no-coda-cluster and short-open-nucleus claims remain historical source reports pending current-profile confirmation; minor-type restrictions are not global.
- Unicode's two-pre-vowel-coeng limit is explicitly orthographic, not a phonological onset maximum. Coeng chaining and silent/etymological stacked letters can cause orthographic units to diverge from phonetic syllables.
- Mam et al. (2025) provides bounded PPK F0 evidence (50 words, five speakers, three repetitions) consistent with possible pitch phonologization for /r>h/ forms and voiced-onset disyllables. This is profile-specific and not implemented as a universal tone rule.
- The Sak-Humphry publisher preview's coda excerpt is internally contradictory about /r/; it is recorded as a lead but excluded from the accepted coda inventory.
- Added a parser regression that preserves the Unicode syllable-chaining example while keeping `phonetic_representation` explicitly unestablished. No IPA labels or global phonotactic rules were added.

## Phonotactic research and orthographic/phonetic boundary — closeout 2026-11-15

- PR #190 merged as `262d16fb755aff952fef42ecb69f8c8a8251df30`. Exact-head Quality [43698504896](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43698504896) SUCCESS (223 tests + 70 subtests); Chromium [43698504898](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43698504898) SUCCESS (4 tests).
- Nacaskul (1978) is recorded as a historical source for major vs minor syllable types. Its minor type-A /r/ cluster and type-B nasal-coda restrictions are explicitly type-specific, not global bans. Its major-syllable coda and open-nucleus generalizations remain historical reports pending current-profile confirmation.
- Unicode L2/22-290 and Ding et al. (2018) support a strict separation between orthographic units and phonetic syllables: coengs can encode chaining, silent/etymological stacks occur, and the two-pre-vowel-coeng encoding limit is not a phonological onset maximum.
- Mam et al. (2025) reports bounded PPK F0 evidence in 50 words and five speakers, including low-F0 patterns for /r>h/ forms and voiced-onset disyllables. This supports a profile-specific research hypothesis, not a universal Khmer tone rule. The careful-citation profile is unchanged.
- The parser regression preserves the cited Unicode example and keeps phoneticization withheld. No new engine rule or IPA label was added.

## Direct BGN/PCGN Latin input — 2026-11-15

- PR #192 merged as `736b1bc30bc6ccea6eb1d9f3aacd0647c17b848f`. Exact-head Quality [43699528446](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43699528446) SUCCESS (223 tests + 70 subtests); Chromium [43699528852](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43699528852) SUCCESS (7 browser tests).
- The romanization mode accepts direct Latin-only BGN/PCGN 1972 input with the diacritics represented in all 37 vowel/rime matrix rows. Unknown Latin fragments are bracketed and produce PARTIAL; the UI makes the one-format-per-run assumption explicit.
- The Khmer-script path remains ASCII-derived and loses PCGN diacritics upstream. The new direct path does not reconstruct omitted diacritics or validate arbitrary romanization systems.
- Ukrainian target mappings remain project proposals/PROVISIONAL; this is not IPA, pronunciation inference or semantic translation. No release-readiness claim is made.
- Two failed intermediate CI heads were fixed and retained: missing ASCII `ie` fallback and incorrect test grouping for shortened variants that share target candidates. Final exact-head Quality and browser checks passed.

## Mixed-script romanization guard — 2026-11-15

- PR #194 merged as `4e1b95f2a1680e7c7363a68b226b0b44778cac74`. Exact-head Quality [43709408446](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43709408446) SUCCESS (223 tests + 70 subtests); Chromium [43709408411](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43709408411) SUCCESS (9 browser tests).
- Mixed Khmer+Latin direct input no longer silently passes Khmer letters/marks through: they are bracketed and result status is PARTIAL. UI asks users to run Khmer-script and Latin BGN/PCGN inputs separately.
- Khmer numerals still convert to Arabic digits and Khmer punctuation remains preserved; UI mode detection distinguishes letters/marks from numerals and punctuation.
- No change to BGN/PCGN mapping, Ukrainian proposals, IPA or phonological rules. Post-merge CI was not returned for merge SHA; exact PR-head checks are the verification evidence.

## Final mainline checkpoint — 2026-11-15

- Current main before this documentation checkpoint: `0d1183553a4851eb0c21336f381be3d0f2d0efaf`. No open PRs.
- PR #194 merged implementation as `4e1b95f2a1680e7c7363a68b226b0b44778cac74`; exact-head Quality [43709408446] and Chromium [43709408411] passed.
- PR #195 merged documentation as `0d1183553a4851eb0c21336f381be3d0f2d0efaf`; exact-head Quality [43709585653] passed (223 tests + 70 subtests), Chromium [43709585691] passed (9 tests).
- Mixed-script handling is verified as an input guard only. Ukrainian mapping values remain provisional. No new phonological claim or accuracy score is made.
- Post-merge CI was not returned for PR #194 merge SHA; do not substitute PR-head CI for a post-merge run.

## Automated accessibility smoke — 2026-11-15

- PR #197 merged as `9452ac70ee16973ac5f0e8bd28201501539409de`. Exact-head Quality [43709993984] SUCCESS (223 tests + 70 subtests); Chromium [43709994024] SUCCESS (11 browser tests).
- Automated checks cover the input accessible name, method switch group/button names, clear button name, keyboard activation with Enter, and the polite live status region.
- Manual screen-reader, complete keyboard traversal, contrast, zoom/reflow, mobile and assistive-technology review remains PARTIAL. Automated browser smoke is not a substitute for human accessibility QA.


## Post-merge mainline verification — 2026-11-15

The current `main` head is `14c87c275a3dcc599893da19b455b2e853abb630`. PR #198 records the automated accessibility smoke closeout. Post-merge push workflows on this exact SHA are now confirmed: Quality [43710193628](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43710193628), Chromium [43710193653](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43710193653), and Pages [43710193633](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43710193633) all SUCCESS. The Chromium job includes deterministic web checks, production build and visible-results verification. These are hosted GitHub Actions results; no local test execution is claimed.

PR #153 is CLOSED unmerged and superseded. Current comparison is diverged (34 commits ahead / 48 behind); its old runtime and duplicate benchmark workflow are not to be merged. Useful research source records were selectively reconciled through PRs #187 and #188. No open PRs were present at this checkpoint.

No release status upgrade follows from green engineering CI: independent adjudicated IPA gold remains 0, accuracy remains null, romanization and Ukrainian targets remain provisional/partial, data rights and human accessibility review remain open. `main` is still unprotected; no governance setting was changed.


## Current-main reconciliation — 2026-11-15 (89e5ba4)

- Current `main`: `89e5ba49c7507f60b421119cbae4b63c240ac3c8` (supersedes the historical `14c87c2…` checkpoint below).
- Exact-SHA hosted CI: Quality [43712699599](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43712699599), Khmer browser smoke [43712699648](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43712699648), Pages [43712699614](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43712699614): all SUCCESS. Quality included corpus structure validation, Python tests, web checks and build; browser included Chromium visible-results verification. No local test run is claimed.
- No open PRs. PR #153 is CLOSED unmerged; current comparison is diverged, 34 ahead / 49 behind. Its safe source-triage content remains selectively represented by #187/#188; old runtime and duplicate workflow remain excluded. PR #64 is CLOSED unmerged; its old CSS snapshot is not merged.
- Current release blockers are unchanged: independent adjudicated IPA gold=0 (accuracy=null); context/profile phonology and PPK pitch remain PARTIAL; Khmer-script BGN/PCGN generation loses diacritics; Ukrainian romanization targets are provisional; source/model rights and train/eval independence are unresolved; manual accessibility QA remains PARTIAL.
- Root `LICENSE` is absent while `pyproject.toml` says MIT: owner decision required. `main` is unprotected per branch metadata; no governance change was made.
- Classification: engineering CI DONE_VERIFIED; language validation PARTIAL/BLOCKED; research prototype only, not production-ready.


## Khmer romanizer output-integrity guard — 2026-11-15

- PR #201 merged as `37a536592a8e462f00997890af63ad232d41a0ae`; exact PR head `42cb1ee70bc89daf6739af24e296a8e9dbb29a86` passed Quality [43720084983] and Chromium [43720085021]. Post-merge exact-main Quality [43720186392], Chromium [43720186338] and Pages [43720186436] all SUCCESS.
- Residual Khmer-script letters and combining marks emitted by the upstream Khmer→Latin package are now bracketed and counted unsupported in both the Khmer-script path and direct BGN/PCGN Latin path. Status becomes PARTIAL; Khmer punctuation remains untouched.
- This closes a result-integrity hole (unconverted script was previously allowed through with no unsupported count). It does not fix the upstream ASCII/diacritic loss or implement contextual PCGN rules. KHM-ROM-ENGINE-001 and broad romanization coverage remain PARTIAL.
- No phonological or Ukrainian mapping rules changed; no accuracy or conformance claim is added.


## Final mainline checkpoint after PR #201/#202 — 2026-11-15

- Current `main`: `1cc833ad1097f6b1ee7c28eb3e7aefb99ad480fb`. PR #201 implementation merge `37a536592a8e462f00997890af63ad232d41a0ae`; PR #202 documentation merge `1cc833ad1097f6b1ee7c28eb3e7aefb99ad480fb`.
- Exact-main post-merge Quality [43720449189], Chromium [43720449188] and Pages build/deploy [43720449180] all SUCCESS. Pages included deployed-site/runtime-asset smoke. Exact PR #202 head Quality [43720352442] and Chromium [43720352370] passed.
- Residual Khmer letters/marks from upstream romanizer output now produce bracketed PARTIAL output; Khmer punctuation is preserved. This is an output guard only. ASCII diacritic loss and contextual BGN/PCGN conformance remain unresolved.
- Issue #104 remains open for expert IPA convention, annotators, adjudicator, curator, blind intake, rights-cleared 30-item pilot and adjudication. No recruitment/contact or fabricated data.
- No open PRs at this checkpoint. Root `LICENSE` absent vs MIT metadata remains an owner decision; main remains unprotected.
- Status: engineering CI/deployment DONE_VERIFIED on exact main; language/data/legal/manual-accessibility gates remain PARTIAL/BLOCKED. Research prototype, not production-ready.


## PCGN shortened-vowel source-mark inventory correction — 2026-11-15

PR #204 corrects the mark matrix: PCGN note 5 distinguishes U+17CB BANTOC (◌់) and U+17D0 SAMYOK SANNYA (◌័), but the previous row represented only BANTOC. Both are now recorded under the same shortened-vowel rule category; the six PCGN rule rows remain six. Python and Node regression assertions cover the two-mark row. This changes source inventory only, not runtime romanization or Ukrainian mapping. Contextual Khmer-script PCGN generation remains PARTIAL. Official source: https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf (note 5).

Exact PR #204 head `b27b87081819307da5ffe27d55e3cf4521004730` passed Quality [43721677822] and Chromium [43721677790]; push Quality [43721673728] also passed. The initial data-only intermediate commit failed the stale exact-mark assertion, which was updated in both Python and Node suites; the final PR-head runs are green.


## Mainline closeout — PCGN mark inventory — 2026-11-15

- PR #204 merged to `main` as `58735a94a8a8f76635f948c2d003d590f26fb0b2`; current main verified at the same SHA; no open PRs.
- Exact-main Quality [43721873111], Chromium [43721873141], and Pages deployment [43721873125] all SUCCESS. Quality: 224 Python tests + 70 subtests, corpus structure validation, web checks and build. Chromium: 11 browser tests. Pages: production exercise, deployment and deployed-site/runtime smoke.
- The six PCGN diacritic rule categories now explicitly inventory seven Khmer source marks, including U+17CB BANTOC and U+17D0 SAMYOK SANNYA under shortened-vowel note 5. `KHM-ROM-MARKS-NUMERALS-001` is DONE_VERIFIED for inventory only; contextual romanization remains PARTIAL.
- Issue #104 remains open; adjudicated IPA gold=0 and accuracy=null. External data rights/train-eval independence, root LICENSE owner decision, and manual accessibility review remain unresolved. No local test execution is claimed. Readiness remains partial research prototype, not production-ready.
