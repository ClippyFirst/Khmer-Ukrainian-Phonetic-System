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
- PR #64 was closed unmerged on 2026-11-02 because its branch was diverged and its stylesheet replacement was broader than the focused responsive change already merged in PR #78.
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


## Current mainline reconciliation — 2026-11-15 (6058768)

- Current `main`: `6058768ca745fddf9306f66d2e325fbed512b6ec`; PR #204 implementation merge: `58735a94a8a8f76635f948c2d003d590f26fb0b2`. No open PRs.
- Exact-main hosted Quality [43722162644], Chromium [43722162599] and Pages [43722162627] all SUCCESS. No local execution is claimed.
- README inventory wording corrected to six PCGN diacritic-rule rows / seven Khmer source marks / ten numerals. This accurately distinguishes rule categories from individual source marks; no new phonological interpretation or runtime behavior was added.
- Remaining release blockers unchanged: contextual PCGN generation and lossy upstream ASCII romanizer, Ukrainian target expert review, independent IPA gold=0 and accuracy=null (issue #104), external data rights/train-eval independence, manual accessibility, and root LICENSE owner decision. Main remains unprotected. Research prototype only.


## Post-PR #206 exact-main verification — 2026-11-15

- Current `main`: `ab5ade5f0984b32884df9fa5dac5607f927a2ea4`; PR #206 merged. No open PRs.
- Exact-main Quality [43728032467], Chromium [43728032424], and Pages build/deploy [43728032407] all SUCCESS. The Quality workflow completed corpus structure validation, Python tests, Node web checks and production build; Chromium visible-results smoke passed; Pages build, Chromium exercise, upload and deployment passed. Hosted CI only; no local tests claimed.
- README now accurately distinguishes six PCGN diacritic-rule rows from seven source marks and ten numeral rows. No runtime/linguistic behavior changed.
- Remaining blockers: contextual PCGN Khmer-script generation and upstream ASCII information loss; expert review of Ukrainian proposals; issue #104 human IPA pilot (gold=0; accuracy=null); external rights review; root LICENSE owner decision; manual accessibility; main protection owner decision. Research prototype only.


## External contextual romanizer candidate — audit note (2026-11-15)

- Reviewed `pheasaKhmer/khmer-engine` pinned at `31b72cd4665f69678fc835da2f501771e42f097a`. Its UNGEGN 2013 rules and syllable parser may inform future implementation architecture; it is not a verified BGN/PCGN 1972 drop-in.
- Its syllable parser uses weighted heuristics to infer readings that Khmer orthography does not uniquely mark; some romanization entries are explicitly marked as extrapolations. This makes ambiguity handling and expert review mandatory.
- Engine code declares MIT; sample lexical data and counts have separate CC BY 4.0 / ODC-By 1.0 declarations; its Pheasa normalizer dependency declares Apache-2.0. No dependency or external data was imported.
- This reduces uncertainty about a possible implementation approach but does not close `KHM-ROM-ENGINE-001`. No local or external tests were run by this repository during the review. Candidate is not IPA and not gold.


## Audit addendum — BGN/PCGN vs UNGEGN profile delta (2026-11-15)

The pinned candidate engine review now has a primary-source rule diff at `docs/audits/current/BGN-PCGN-UNGEGN-RULE-DIFF-2026-11-15.md`. The key implementation blocker is concrete: PCGN note 3 does not list ស among neutral subscripts, whereas UNGEGN note 3 does, and the candidate's UNGEGN constant includes it. Candidate-specific unlisted forms (SAMYOK + final y; YUUKALEAPINTU) and heuristic coda/syllable rules must not be promoted to PCGN behavior. No runtime was changed. The contextual Khmer-script engine remains PARTIAL.


## Exact-main audit — PR #209 (2026-11-15)

- PR #209 merged as `266297fcc296388220ea48c975344f5aa14f097d`; no open PRs.
- Exact-head PR checks: Quality [43730475810] and Chromium [43730475809] SUCCESS; push Quality [43730456889] SUCCESS.
- Exact post-merge main checks: Quality [43730567132], Chromium [43730567159], Pages [43730567118] all SUCCESS. Quality includes corpus validation, Python tests, Node checks and build; browser smoke and deployed Pages smoke passed.
- The rule-diff is research/documentation only. No code or linguistic claims changed. Contextual PCGN engine remains PARTIAL; independent IPA gold remains 0; root LICENSE/owner decision and manual accessibility review remain open.


## PCGN note registry audit — 2026-11-15

The eleven notes of the official BGN/PCGN guide are now separately registered in `data/khmer/romanization_pcgn_notes.csv`, with source locators and explicit `DOCUMENTED_ONLY` status. A new Python test protects note coverage and the critical Note 3/Note 5 boundaries: the PCGN weak-foot set excludes ស, and the ô-series shortened eă condition is exactly before k/ng/h. It also preserves both BANTOC and SAMYOK SANNYA.

This closes documentation coverage for Notes 1–11 only. It does not establish that the runtime implements those notes, does not resolve ambiguous feet or omitted diacritics, and does not alter IPA or Ukrainian target behavior. The Khmer-script romanizer remains PARTIAL.


## Exact-main verification — PR #211 PCGN note registry — 2026-11-15

PR [#211](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/211) merged as `9383385fc3244ff600d0fab254c6488a83d92d7b`. PR-head push Quality [43732930991], PR Quality [43732940452], and PR Chromium [43732940449] all SUCCESS. Exact-main Quality [43733051013], Chromium [43733051164], and Pages build/deploy [43733051031] all SUCCESS.

The new eleven-note PCGN registry and its regression tests are therefore engineering-verified on exact main. Acceptance remains bounded to documentation and rule-boundary guardrails: it does not implement a contextual Khmer-script romanizer or resolve ambiguous/omitted marks. Issue #104 remains the human IPA-gold blocker; research prototype only.


## Typed PCGN structural analysis — 2026-11-15

A new isolated `src/khmer_ua/pcgn.py` module records source-script structure for a caller-supplied chunk. It retains base/foot identities and orthographic register labels, shifters, vowel signs, both shortening marks, ROBAT, AHSDA and TOANDAKHIAT, code points, unresolved material and provenance. The output schema requires explicit abstention for syllable segmentation, series, series source, coda, romanization, IPA and Ukrainian output.

This improves inspectability and provides a typed boundary for future work, but it does not implement contextual BGN/PCGN rules or resolve any linguistic ambiguity. It deliberately does not reuse the existing phonological parser's heuristic syllable segmentation. Tests and hosted CI are pending on the PR head; do not mark the engine complete until contextual source-backed parity fixtures and expert review exist.


## Exact-main audit — PR #213 typed PCGN orthographic analysis — 2026-11-15

PR #213 merged as `18134929554420875b447b1c5128b3b879e3f608`. Exact-head push Quality [43734102361], PR Quality [43734106341], PR Chromium [43734106320], and exact-main Quality [43734192447], Chromium [43734192457], Pages [43734192455] all SUCCESS.

The new typed analyzer is bounded to orthographic chunk structure and explicit abstention. It does not segment phonetic syllables, select a PCGN series, infer codas, recover omitted marks or emit romanization/IPA/Ukrainian text. The IPA-first runtime is unchanged. This closes a parser-facing structural-contract task only; contextual romanization and linguistic validation remain partial/blocked.


## PCGN Note 3 series resolver — 2026-11-15

A bounded series-selection function now implements the official Note 3 rule over a typed orthographic chunk. It preserves the exact PCGN weak-subscript set (five nasals plus យ/រ/ល/វ; excludes ស), the special ប-with-foot p-in-â exception, and rejects a subscript form for ឡ because the PCGN consonant table says none exists. It abstains when shifters, multiple feet/bases or unsupported material require additional analysis.

The Note 3 function initially returned only series metadata. A subsequent bounded Note 2 subset now handles one correctly placed shifter after a single base with no foot; cluster shifters, BA+TRIISAP and malformed/multiple/misplaced cases still abstain. Vowel mapping, coda detection, Note 5 shortening, syllabification, IPA and Ukrainian output remain unimplemented.


## Exact-main audit — PCGN Note 3 series resolver / PR #215 — 2026-11-15

PR #215 merged as `357ce7f2a5400ff1643e4f64337009dd18c4113d`. PR-head push Quality [43734733096], PR Quality [43734746708], PR Chromium [43734746686], and exact-main Quality [43734828487], Chromium [43734828491], Pages build/deploy [43734828557] all SUCCESS.

The Note 3 resolver is verified for bounded series metadata only. It does not implement shifters, vowel selection, coda/phonetic syllabification, shortened vowels, or romanization. The complete Khmer-script PCGN engine remains PARTIAL. Issue #104 and legal/governance/manual-accessibility blockers remain unchanged.


## PCGN Note 2 shifter subset — 2026-11-15

The Note 3 series resolver now handles the unambiguous single-base subset of Note 2: TRIISAP after an â-series base shifts to ô; MUUSIKATOAN after an ô-series base shifts to â; BA + MUUSIKATOAN retains the Note 3 p-in-â exception. It records the shifter's source position and before/after series. It abstains on clusters, multiple/misplaced or wrong-direction shifters and BA + TRIISAP. This is partial Note 2 coverage, not full romanization. Exact PR-head and exact-main Quality/Chromium checks passed; Pages deployment also passed on exact main.


## PCGN Note 2 shifter subset — PR #217 — 2026-11-15

PR #217 merged as `c738075c47c76730aa15e96acea588ad924c829c`. PR-head push Quality [43735335039], PR Quality [43735349944] and Chromium [43735349863] all SUCCESS. Exact-main Quality [43735441278], Chromium [43735441245] and Pages [43735441621] all SUCCESS on the merge SHA, including deployed-site/runtime-asset smoke.

The bounded single-base Note 2 subset is implemented; full cluster shifter behavior, vowels, codas, syllabification and Note 5 shortening remain incomplete.


## Exact-main checkpoint — PR #218 — 2026-11-15

PR #218 merged as `9420326549d8a327774d0587b6fe19c4b17befcd`. Exact-head push Quality [43735564674], PR Quality [43735576766] and Chromium [43735576217] all SUCCESS. Exact-main Quality [43735662414], Chromium [43735662288] and Pages [43735662264] all SUCCESS, including deployed-site/runtime-asset smoke.


## Exact-main verification — PR #219 — 2026-11-15

PR #219 merged as `690b44174a8831ac9b08b44786d5ffde43f6d5aa`. PR-head push Quality [43735841295], PR Quality [43735855013], PR Chromium [43735855047], and exact-main Quality [43735981736], Chromium [43735981714], Pages [43735981744] all SUCCESS.


## Exact-main checkpoint — PR #220 — 2026-11-15

PR #220 merged as `8c4784235742cd83c35ce4a2b0bc7831a2b11bb2`. PR-head push Quality [43736157032], PR Quality [43736168034], PR Chromium [43736167978] all SUCCESS. Exact-main Quality [43736256876], Chromium [43736256892] and Pages [43736257006] all SUCCESS, including deployed-site/runtime-asset smoke.


## Exact-main checkpoint — PR #221 — 2026-11-15

PR #221 merged as `0d9bb90b1451ce9a2452121e30c3864d4cd887f5`. PR-head push Quality [43736444673], PR Quality [43736456391], PR Chromium [43736456480] all SUCCESS. Exact-main Quality [43736548569], Chromium [43736548708] and Pages [43736548595] all SUCCESS, including deployed-site/runtime-asset smoke.


## Exact-main checkpoint — PR #222 — 2026-11-15

PR #222 merged as `95dd256b515c4a15e28cf80f21e3a53b0f0dfa11`. PR-head push Quality [43736688182], PR Quality [43736708656], PR Chromium [43736708789] all SUCCESS. Exact-main Quality [43736800449], Chromium [43736800513] and Pages [43736800469] all SUCCESS, including deployed-site/runtime-asset smoke.


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


## BGN/PCGN Note 5 implementation audit — 2026-11-15

- Added a typed shortened-vowel component decision with schema and explicit null IPA/Ukrainian fields.
- Only three source-listed shapes are accepted: consonant(+foot) + coda + BANTOC; consonant(+foot) + AA + coda + BANTOC; consonant(+foot) + SAMYOK SANNYA + coda.
- The onset-only analysis must match the full chunk's token prefix; Notes 2–3 series selection is applied to that onset.
- Coda class is explicit caller input (`k`, `ng`, `h`, `other`), not inferred from Khmer orthography. The decision records the coda character and supplied class.
- Output is the shortened vowel component only. No coda romanization, syllable segmentation, complete romanization, IPA or Ukrainian result is claimed.
- Primary source: BGN/PCGN 1972 Vowel Characters table rows 1–2 and Note 5, pp. 2–3. Implementation status PARTIAL pending integration with a verified syllable/coda parser and full romanization adapter.


## Exact-main verification — PR #233 / PCGN Note 5 — 2026-11-15

PR #233 merged as `cf57045bf6ddf0537e2a5c33a8b2468e8f3f6f2c`. Final PR-head `9bcf7391ce08557ce2fa56e4cbb764568949f952`: push Quality [43751102348], PR Quality [43751107119], Chromium [43751107131] all SUCCESS (272 tests + 70 subtests; web checks/build/Chromium passed). Exact-main Quality [43751266786], Chromium [43751266785], Pages [43751266784] all SUCCESS, including deployed-site/runtime-asset smoke. Note 5 remains PARTIAL component-only; no IPA/Ukrainian or complete-syllable status promotion.


## BGN/PCGN Note 6 implementation audit — 2026-11-15

- Added `PCGNRobatDecision` and `resolve_pcgn_robat`, plus a schema and focused regression tests.
- Accepts exactly one ROBAT mark at the end of the supplied component chunk, immediately after one modeled unstacked consonant.
- Requires the caller to supply a PCGN romanized consonant value; validates against the consonant-table inventory and returns only `rC`.
- The `rm` component in `ធម៌ → thôrm` is covered. No full syllable, coda inference, IPA or Ukrainian output is produced.
- Primary source: BGN/PCGN 1972 Diacritical Marks table row 4 (p. 4) and Note 6 (p. 5). Status PARTIAL pending broader structural integration and complete syllable romanization.


## Exact-main verification — PR #235 / PCGN Note 6 — 2026-11-15

PR #235 merged as `34ab63ff37023bddcaeaebb0a6ccd838f662c045`. Final PR-head `0d6f1a2b11ab1de94ad9be391c2dd4932142ff77`: push Quality [43751844908], PR Quality [43751851657], PR Chromium [43751851706] all SUCCESS (278 tests + 70 subtests). Exact-main Quality [43751965081], Chromium [43751965119], Pages [43751965128] all SUCCESS, including deployed-site/runtime-asset smoke. ROBAT remains a PARTIAL `rC` component resolver with caller-supplied consonant value; no IPA/Ukrainian or complete-syllable promotion.


## BGN/PCGN Note 7 implementation audit — 2026-11-15

- Added `PCGNAhsdaDecision` and `resolve_pcgn_ahsda`, with schema and tests.
- Requires exactly one final AHSDA mark after one modeled unstacked consonant.
- Syllable position is explicit caller input. INITIAL records mark omission; FINAL additionally requires explicit `â`/`ô` and returns only that vowel component.
- No syllable segmentation, series inference, complete romanization, IPA or Ukrainian output.
- Primary source: BGN/PCGN 1972 Diacritical Marks table row 5 (p. 4), Note 7 (p. 5). Status PARTIAL.


## Exact-main verification — PR #237 / PCGN Note 7 — 2026-11-15

PR #237 merged as `890791a1d8236180c82a39b81bd28b7f772d614c`. Final PR-head `2e3ee353124b1a9cacac64997ceb06720a78370c`: push Quality [43752539333], PR Quality [43752551657], PR Chromium [43752551605] all SUCCESS (284 tests + 70 subtests). Exact-main Quality [43752661403], Chromium [43752661392], Pages [43752661369] all SUCCESS, including deployed-site/runtime-asset smoke. AHSDA remains a PARTIAL component resolver; no syllable-position or series inference, full romanization, IPA or Ukrainian output.


## BGN/PCGN Note 8 implementation audit — 2026-11-15

- Added `PCGNToandakhiatDecision` and `resolve_pcgn_toandakhiat`, schema and regression tests.
- Requires exactly one final TOANDAKHIAT mark and an exact caller-supplied marked consonant grapheme matching the immediately preceding unstacked/subscript token.
- Returns an omission decision only. It does not infer silent characters, romanize the remaining word, or produce IPA/Ukrainian.
- Synthetic structural tests cover unstacked/subscript consonants and fail-closed contexts; guide examples are not treated as gold.
- Primary source: BGN/PCGN 1972 Diacritical Marks table row 6 (p. 4), Note 8 (p. 5). Status PARTIAL.


## Exact-main verification — PR #239 / PCGN Note 8 — 2026-11-15

PR #239 merged as `9c615293e3037cb0ccbd9db0820698741bbcd5cf`. Final PR-head `e52b2d5be98a521dfa3c6dc5af846c6c79d42dce`: push Quality [43753171641], PR Quality [43753185515], PR Chromium [43753185496] all SUCCESS (290 tests + 70 subtests). Exact-main Quality [43753327251], Chromium [43753327183], Pages [43753327232] all SUCCESS, including deployed-site/runtime-asset smoke. TOANDAKHIAT remains PARTIAL; silent character is caller-identified, with omission-only output.


## BGN/PCGN Note 4 implementation audit — 2026-11-15

- Added `PCGNGlottalOnsetDecision` and `resolve_pcgn_glottal_onset`, with schema and tests.
- Supports only standalone `អ`; the existing Notes 2–3 resolver must confirm â-series.
- Word-initial and following-vowel-letter context are explicit inputs. Apostrophe omission is offered only when both are true.
- Returns an apostrophe component/options only; no complete syllable, IPA or Ukrainian output.
- Primary source: BGN/PCGN 1972 Consonant Characters row 22 and Note 4 (p. 5). Status PARTIAL.


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


## BGN/PCGN vowel + anusvara/visarga implementation audit — 2026-11-15

- Implemented a bounded resolver for the eight rows in the official p. 4 “Vowel Characters with Anusvara or Visarga” table.
- The caller supplies an onset-only analysis; the resolver uses the existing Note 2–3 series decision. Row 8 additionally requires an explicit final `ង` coda identifier.
- Added the decision schema, focused regression tests, package exports and machine-readable source table.
- Unsupported patterns and any unlisted coda/context abstain. The resolver returns only the table component; no IPA or Ukrainian output is synthesized.
- Status: `KHM-ROM-PCGN-ANUSVARA-VISARGA-001 = PARTIAL`; the overall PCGN engine remains PARTIAL.


## BGN/PCGN inherent vowel row 1 implementation audit — 2026-11-15

- Added a bounded row 1 resolver for the inherent `â/ô` vowel component.
- It requires explicit `NON_FINAL` onset context and obtains series from the existing Notes 2–3 resolver.
- FINAL context abstains; the guide's general no-vowel-after-final-consonant statement is not treated as a complete coda parser.
- Added schema, tests, machine-readable row and public package exports.
- Status: `KHM-ROM-PCGN-INHERENT-VOWEL-001 = PARTIAL`; no IPA/Ukrainian output.


## Exact-main verification — PR #249 / PCGN anusvara-visarga table — 2026-11-15

PR #249 merged as `a50f815f993f8fa9b4ae59c5f0f89b8c7717ea6f`. PR-head push Quality [43760107833], PR Quality [43760141233], PR Chromium [43760141132], exact-main Quality [43760241393], Chromium [43760241451] and Pages build/deploy [43760241464] all SUCCESS. The bounded resolver is engineering-verified; PCGN full syllable coverage remains PARTIAL.


## Exact-main verification — PR #250 / PCGN inherent vowel — 2026-11-15

PR #250 merged as `62ce69bd17dc64fecfb73e81e22ca10bf97a25ff`. PR-head push Quality [43760551262], PR Quality [43760562169], PR Chromium [43760562155], exact-main Quality [43760662544], Chromium [43760662582] and Pages build/deploy [43760662587] all SUCCESS. The inherent-vowel component is bounded to caller-identified NON_FINAL onsets; the PCGN engine remains PARTIAL.


## BGN/PCGN consonant table implementation audit — 2026-11-15

- Added bounded consonant-cluster mapping for table rows 1–21: one base and at most one foot.
- Row 12 BA b/p alternation is controlled by the existing Note 3 exception metadata, not guessed from an isolated glyph.
- Row 22 alif remains delegated to the separate Note 4 glottal-onset resolver.
- Added typed decision, schema, source registry, tests and package exports.
- Multiple-foot clusters, unresolved series, unsupported marks and lexical reference cases abstain. This is not a complete PCGN syllable romanizer and emits no IPA/Ukrainian output.


## Exact-main verification — PR #251 — 2026-11-15

PR #251 merged as `aab014705bdf90825b922ff69f1c2e7758e56246`. PR-head push Quality [43760857888], PR Quality [43760868532], PR Chromium [43760868545], exact-main Quality [43760984773], Chromium [43760984785] and Pages [43760984838] all SUCCESS. Documentation-only closeout.


## Exact-main verification — PR #252 / PCGN consonant table — 2026-11-15

PR #252 merged as `16fbbde6238e03290507056388b539f54622d236`. Final PR-head push Quality [43761467383], PR Quality [43761473221], PR Chromium [43761473212], exact-main Quality [43761598283], Chromium [43761598359] and Pages [43761598332] all SUCCESS. The initial malformed-schema failure [43761223088] was corrected and retested. Overall PCGN generation remains PARTIAL.


## BGN/PCGN final-consonant rule implementation audit — 2026-11-15

- Added a bounded final-consonant component resolver for the guide's general no-following-vowel statement.
- Caller must explicitly isolate the final consonant and confirm absence of a vowel character and TOANDAKHIAT.
- One base plus at most one foot is supported; BA/ALIF and all unsupported contexts abstain.
- The guide's qualifier “generally” is retained in the typed status; no complete word or syllable is inferred.
- Added schema, tests, source registry and public exports. Overall PCGN engine remains PARTIAL.


## PR #255 — final-consonant context type guard — 2026-11-16

PR [#255](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/255) merged as `47679154526fa32c5edd9d62ca084de5af4759dd`. Non-boolean caller context values now raise `TypeError` before a PCGN decision can be emitted; tests cover invalid values and every supported base consonant. PR-head push Quality [43825412435], PR Quality [43825430244], PR Chromium [43825430217], exact-main Quality [43825536547], Chromium [43825536580] and Pages [43825536491] all SUCCESS. This is an input-contract hardening only; no linguistic scope/status promotion.


## PR #256 exact-main closeout — 2026-11-16

PR #256 merged as `dee4881da4cfb01b6da0ff5e857af67cade14cb1`. PR-head push Quality [43825693046], PR Quality [43825710166], Chromium [43825710160], exact-main Quality [43825806168], Chromium [43825806361] and Pages [43825806234] all SUCCESS. Exact-main `pytest -q`: 331 passed, 70 subtests passed; `npm run check`, production build, production Chromium exercise and deployed-site/runtime-asset smoke passed. Documentation-only closeout; no linguistic status promotion.


## PCGN independent-vowel table source registry — 2026-11-16

Added `data/khmer/romanization_pcgn_independent_vowels.csv` with source-located rows 3, 4, 7 and 14–22 from the official BGN/PCGN 1972 table. Row 7 keeps `ឧ` unresolved with both `ŏ` and `ŭ` alternatives. A regression test checks exact parity with the runtime mapping and primary source URL. This is traceability/registry work only; no behavior or linguistic acceptance status is promoted.


## PR #259 exact-main closeout — 2026-11-16

PR #259 merged as `458026f080bca31edeec87c2009245213ab667c7`. PR-head push Quality [43826670914], PR Quality [43826697643], Chromium [43826697687], exact-main Quality [43826837012], Chromium [43826837160] and Pages [43826837175] all SUCCESS. Exact-main `pytest -q`: 332 passed, 70 subtests passed; web checks, production build, Chromium exercise and deployed-site/runtime-asset smoke passed. The new independent-vowel CSV is a source registry only; no language behavior or acceptance status changed. PR #258 was closed as superseded due to a stale-base documentation conflict; no work was discarded.


## Current branch inventory refresh — 2026-11-16

Live `main` is `2e005a3e804e878deb66007d857d2d9361c8e4de`; there are no open PRs. Exact-main Quality [43827176347], Chromium [43827176391] and Pages [43827176423] all succeeded.

The repository branch endpoint returns 125 refs (one `main`, 124 non-main). This is a count of retained refs, not 124 merge candidates. Sampled comparisons against current main confirm that many are old divergent snapshots: Note 2 shifter branch 16 ahead/43 behind; practical-adapter verified branch 29 ahead/109 behind; typed-IPA hybrid bridge 10 ahead/75 behind; old repository-information-architecture branch 4 ahead/86 behind. The independent-vowel source-register branch 12 ahead/3 behind has already had its source registry integrated through PR #259. These branch tips are not safe to merge wholesale; use current main as the only integration base.

No open PR remains. The connected GitHub tool surface does not provide branch deletion, and no branch was deleted or force-updated. Keep one active task branch based on main; historical refs remain preserved until an owner chooses an archival/deletion policy. This is consistent with the earlier historical branch comparison closeout, but refreshes its inventory count.

The next hard blocker is human, not engineering: issue #104 remains open; independent adjudicated IPA gold is 0 and accuracy is null. The expert convention, independent annotators/adjudicator, curator, blind intake, source rights and 30-lexeme pilot cannot be completed by repository automation. Root LICENSE/pyproject metadata reconciliation and main branch protection remain owner decisions.


## Systematic historical branch ancestry comparison — 2026-11-16

- Exact `main` at comparison: `44c2168e9b4a3f818ad2259f663792a4fc86229b`.
- Live branch listing: 131 refs total, `main` + 130 non-main; all non-main tips have unique SHAs. Compared every non-main ref against exact main: **130/130**. Open PR count: **0**.
- Comparison results are predominantly `diverged` because the repository uses squash merges and retained historical task snapshots; ahead/behind counts do not by themselves imply unmerged work. Per-branch file summaries were inspected, and high-risk representative files were compared directly.
- Spot checks: PCGN consonant, dependent-vowel, final-coda and independent-vowel source tables/test suites are already present in main; old PCGN branches carry stale versions of `pcgn.py` and note registries. The independent-vowel source-register branches have the exact same CSV as main. Practical-adapter `practical.py` matches main while its historical `rule_engine.py` is older. The old direct-BGN/PCGN and mixed-script runtime files are smaller/older than main; the output-guard fix file matches main. Coverage report JSON and external registry test/schema files match main; historical coverage/benchmark scripts and external-IPA registry data are older. Old parser branch tests omit a newer main test.
- Disposition: no open PR requires action; no historical branch is a safe blanket merge. PRs #264–#266 are merged and their branch refs are retained. Other historical refs remain untouched because the connected GitHub operations do not expose branch deletion and the owner has not supplied an archival policy.
- `KHM-BRANCH-AUDIT-001` remains PARTIAL: ancestry inventory DONE_VERIFIED; complete file-level content/PR-ancestry audit remains outstanding.


## 2026-11-16 continuation — Note 4 Alif syllable adapter

A dedicated branch adds a bounded Alif + ordinary dependent-vowel PCGN open-syllable adapter. It reuses the existing Note 4 and dependent-vowel resolvers, validates caller-supplied boundaries, requires explicit Note 4 context booleans, and preserves optional apostrophe spellings as alternatives. New schema and focused regression tests are present. The result remains PCGN orthographic Latin only; no IPA/Ukrainian path or segmentation is introduced. Acceptance is DONE_VERIFIED for this bounded API: PR #267 merged as 6df8c6c176e0098f97a9f4ab1f9583b0bb7caa68; exact PR-head Quality [43888596780] and Chromium [43888596962], plus exact-main Quality [43888801455], Chromium [43888801448] and Pages [43888801373] all passed. Full PCGN segmentation/word assembly remains PARTIAL; this adapter is not an IPA or Ukrainian transcription path.


## 2026-11-16 continuation — Note 4 Alif closed syllable adapter

A new dedicated branch adds a bounded Alif + normal dependent vowel + one supported final-consonant assembler. It composes existing Note 4, dependent-vowel and final-consonant resolvers, validates caller-supplied boundaries, requires explicit context flags, and preserves the optional apostrophe as an alternative. Tests/schema cover all current normal dependent-vowel patterns with the bounded generic coda rule. This remains PCGN orthographic Latin only; no IPA/Ukrainian output or automatic segmentation is introduced. Acceptance is DONE_VERIFIED for this bounded API: PR #269 merged as 482ed151dc99d3fd20714a606c9ad25aa209a99e; exact PR-head Quality [43889912149] and Chromium [43889912018], plus exact-main Quality [43890093477], Chromium [43890093456] and Pages [43890093482] all passed. Full PCGN segmentation/word assembly remains PARTIAL; this adapter is not an IPA or Ukrainian transcription path.


## 2026-11-16 continuation — Note 4 + Note 5 Alif shortened closed syllable adapter

A dedicated branch adds a bounded Alif + Note 5 shortened-vowel + one supported coda assembler for exactly the three source-listed patterns. It composes existing Note 4, Note 5 and final-consonant resolvers, requires caller-supplied context/coda class, cross-checks the coda class against resolved PCGN romanization, and preserves optional apostrophe output. Schema and focused tests are included. This remains PCGN orthographic Latin only; no IPA/Ukrainian output or automatic segmentation is introduced. Acceptance is DONE_VERIFIED for this bounded API: PR #271 merged as 9957081db4149ff316695273d8dd525985bd34fd; exact PR-head Quality [43891125460] and Chromium [43891125490], plus exact-main Quality [43891297907], Chromium [43891298013] and Pages [43891297884] all passed. Full PCGN segmentation/word assembly remains PARTIAL; this adapter is not an IPA or Ukrainian transcription path.


## 2026-11-16 continuation — Note 6 ROBAT closed-syllable adapter

A dedicated branch adds a bounded ROBAT-coda syllable assembler. It composes existing consonant, inherent/dependent-vowel and Note 6 ROBAT resolvers, uses an explicit bare marked-coda chunk to establish the consonant's PCGN value, and validates all caller-supplied boundaries. The official thôrm example and a dependent-vowel case are tested. No automatic segmentation or IPA/Ukrainian output is introduced. Acceptance is DONE_VERIFIED for this bounded API: PR #273 merged as 4fee1db13201b9e171b08daa1d4a45f73a396b86; exact PR-head Quality [43892380539] and Chromium [43892380533], plus exact-main Quality [43892575946], Chromium [43892575968] and Pages [43892575864] all passed. Full PCGN segmentation/word assembly remains PARTIAL; this adapter is not an IPA or Ukrainian transcription path.


## 2026-11-16 continuation — independent-vowel closed-syllable adapter

A dedicated branch adds a bounded independent-vowel + final-consonant assembler. It composes the listed independent-vowel resolver with the existing generic final-consonant resolver, validates caller-supplied chunk boundaries and preserves Note 9's unresolved ŏ/ŭ alternatives. It is orthographic PCGN Latin only; no IPA/Ukrainian output or automatic segmentation is introduced. Acceptance is DONE_VERIFIED for this bounded API: PR #275 merged as 0e408e4d2ce18228e7b8327ddc71af5bdb302f72; exact PR-head Quality [43910476719] and Chromium [43910476885], plus exact-main Quality [43910647111], Chromium [43910647145] and Pages [43910647200] all passed. The independent-vowel component's Note 9 ambiguity remains unresolved; no IPA/Ukrainian or automatic segmentation is claimed.


## Exact-main verification checkpoint — 2026-11-16 evening

- Exact main SHA: `0c74b5cbc55b269156a15a4694b8f8f2149b78c1`.
- Quality [43911193804], Chromium [43911193963], Pages build/deploy and deployed runtime smoke [43911194149] all SUCCESS. Quality reports 377 Python tests + 70 subtests; corpus validation, web checks, production build and browser checks passed. No local test run is claimed.
- No open PRs. Issue #104 remains OPEN and blocks the first independently adjudicated IPA gold pilot (gold count 0; accuracy null). Recruitment, convention approval, blind intake, rights-cleared source selection and adjudication require human participants.
- Repository remains a deployed engineering/research prototype, not linguistically release-ready. Full segmentation/word romanization, complete IPA coverage, expert-reviewed Ukrainian target policy, root LICENSE/metadata decision, branch protection and manual accessibility review remain incomplete or owner-gated.


## LOC Khmer word-division reconciliation — 2026-11-16

Official LOC sources distinguish historical/versioned word-division formulations: 1989 and ALA-LC 1997 Note 10 specify the shortest written form that can stand alone; ALA-LC 2013 Note 8 says any word can be separated when romanizing. Both preserve original-language division for non-Pali/Sanskrit loans. BGN/PCGN 1972 Note 9 concerns the independent vowel ឧ and is unrelated. ALA-LC notes do not define a complete segmentation algorithm or lexicon; maximal matching and orthographic syllable segmentation are insufficient evidence of compliance. See `docs/audits/current/LOC-KHMER-WORD-DIVISION-EVIDENCE-2026-11-16.md`. Implementation remains blocked/evidence-limited; no runtime change was made.


## Public hosting verification — 2026-11-16

The service is live exclusively on GitHub Pages: https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System-/. Exact deployed source SHA: `8feb14a3cf96fa2e1aafd00ea045d5fddb2e3c4a`. Pages workflow run 43930778763 completed successfully: Vite build, web checks, production Chromium exercise, Pages artifact upload, deploy-pages action, and deployed HTTP smoke checks for both `index.html` and `system.html`, including JS/CSS runtime assets. No alternative hosting platform or application server is used. Linguistic release status remains research-grade/evidence-limited.


## Typed partial-result and Unicode audit — 2026-11-16

- The previous browser aggregate replaced the complete IPA/Ukrainian strings with one global placeholder whenever any unit was unresolved. That contradicted the repository's per-unit integrity requirement and discarded independently usable neighboring results. The adapter now keeps source-aligned local markers and preserves resolved units while setting explicit `complete` / `partial` metadata.
- The browser result now exposes a versioned, provenance-aware `khmer-phonetic-result/v1` contract with distinct structural, phonological and target-policy provenance lanes. Structural Unicode evidence is not treated as pronunciation evidence.
- Browser parsing now iterates Unicode code points and records U+ diagnostics for unsupported code points. The visible spelling `ព្រះរាជាណាចក្រ` is covered by a regression that checks complete structural trace reconstruction and prevents a missing lexical IPA fixture from being mislabeled as malformed Unicode.
- **Engineering status: DONE_VERIFIED for this change set.** Implementation merge commit `b0157a3b9f43d8c3b9e5623634571ba6cd647151` was followed by main verification checkpoint `dbbd34a4af8c7d24d139d7d7f2442acf4b5328b0`, which passed Quality checks `43938194107`, browser smoke `43938194161`, and Pages deploy `43938194109`. The conservative tokenizer remains heuristic; complete Khmer syllable/word segmentation and contextual orthography → IPA are not established. Python and browser emit the same versioned typed-result schema; exact-head cross-runtime contract-shape tests passed. Independent adjudicated IPA gold remains 0; empirical accuracy remains null.


The Python deterministic engine now emits the same `khmer-phonetic-result/v1` schema as the browser, using frozen dataclasses for result, unit and uncertainty records. It preserves punctuation and known lexical fixtures in mixed input, and marks invalid units locally. Its legacy top-level fields remain available for API compatibility.


The reported `ព្រះរាជាណាចក្រ` false `Unknown character(s)` state has now been traced to the browser parser's unit assumption: the conservative tokenizer can keep several known Khmer base consonants in one orthographic chunk, but the parser previously treated every post-base consonant outside a COENG pair as unknown. The parser now records every recognized consonant as a consonant grapheme and withholds phonetic output when the chunk cannot be confidently syllabified. This is a structural-recognition correction, not a new pronunciation rule; the absence of a lexical IPA fixture still yields NOT_ESTABLISHED.

The shared `khmer-phonetic-result/v1` payload is specified in `schemas/phonetic-result.schema.json`. Both runtime implementations expose the same unit keys, rule trace, provenance lanes and uncertainty shape; Python and browser tests assert the published contract shape.

Exact-main verification for the typed-result, partial-output and Unicode changes: Quality checks `43938194107`, Khmer browser smoke `43938194161`, and Pages deploy `43938194109` all succeeded on `dbbd34a4af8c7d24d139d7d7f2442acf4b5328b0`. PR #280 is merged.

## 2026-11-16 — Khmer boundary-evidence interface post-merge checkpoint

PR #281 is merged as `50ae3538a624cf78781411c08ebcf51f73fcb5c2`. Exact-main Quality run `43940735723`, Chromium browser run `43940735738`, and GitHub Pages build/deploy run `43940735610` all succeeded on that SHA. The boundary evidence contract, Python tests, Node checks, production build, browser smoke and Pages deployment are verified. No local test execution is claimed. The interface is evidence-only; no word segmenter or LOC conformance is claimed. The independent profile decision and licensed/adjudicated lexical boundary evidence remain outstanding.


## Khmer subscript independent-vowel parsing — 2026-11-16

The parser now recognizes a documented Khmer structural form that was previously rejected: a subscript independent vowel encoded as U+17D2 COENG plus a modeled independent vowel (Unicode Standard 18.0.0 Chapter 16 §16.4.1, example ផ្ឯម). The parser preserves the pair as one typed grapheme record, exposes exact-source code-point spans for the encoded pair, and records the Unicode 18 structural source. This is not full orthographic-syllable parsing or word segmentation and adds no IPA or Ukrainian output. Acceptance is verified on exact PR head and exact main: PR #282 merged as `dd94f637674ad5ce599ee439584b88b6dba4db1e`; Quality `43947114555`, Chromium `43947114448`, and Pages deploy/runtime smoke `43947114535` all succeeded. Quality: 393 Python tests + 70 subtests. This is structural-only support, not IPA or word segmentation.


## Unicode 18 Khmer orthographic-component scanner — 2026-11-16

The current feature branch adds a lossless component scanner based on Unicode 18 Chapter 16's Khmer component inventory and documented order. It emits source-preserving typed components and code-point spans in both Python and browser runtimes. It intentionally reports multiple un-subscripted base consonants as `EVIDENCE_LIMITED` rather than guessing whether they are codas or new orthographic syllables. This is not yet a full BNF parser, syllabifier, grapheme-cluster segmenter or word segmenter. UAX #29 Revision 49 confirms that Khmer word segmentation requires tailoring; it does not define this project's lexical boundary algorithm. Exact-head CI is pending.


## Exact-main verification — Khmer orthographic component scanner — 2026-11-16

PR #283 merged as `bdc15daf6f7c40a6c088e306343a421b9347e9c1`. Exact-main Quality [43953449784] SUCCESS (402 Python tests + 70 subtests; corpus engineering validation, Node/web checks, production build); Chromium [43953449807] SUCCESS; GitHub Pages deploy and deployed runtime smoke [43953450103] SUCCESS. The scanner is DONE_VERIFIED as a lossless component inventory with Python/browser parity. Full BNF validation and orthographic-syllable segmentation remain PARTIAL/TODO; lexical word segmentation and independent boundary/IPA gold remain evidence-blocked. Open PRs: 0; Issue #104 remains OPEN. Historical PR #64 is CLOSED unmerged; its branch is preserved.


## Unicode 18 orthographic-syllable grammar reconciliation — 2026-11-16

Unicode Standard 18.0.0 §16.4 gives the formal component-order BNF `B {R | C} {S {R}}* {{Z} V} {O} {S}`; Appendix A.2 defines its extended-BNF operators. The merged PR #283 scanner remains correctly scoped as a component inventory, not a complete grammar parser. Unicode Technical Note #61 v2 (February 2025) is a separate non-normative implementation guideline that proposes a tighter Modern Khmer encoding structure and discusses Middle Khmer separately. The parser follow-up must keep these source layers distinct, preserve all viable parses and ambiguity, and avoid conflating orthographic syllables with phonological syllables or lexical words. Detailed source reconciliation and acceptance contract: `docs/audits/current/UNICODE-KHMER-ORTHOGRAPHIC-SYLLABLE-GRAMMAR-2026-11-16.md`. Exact-main baseline `567c105ac453ff95f1e2a567b8f5e992bda9d6b0`: Quality 43953751661, Chromium 43953751879, Pages 43953751433 all SUCCESS. No runtime change in this documentation-only work.


## Unicode 18 Khmer parser completion — 2026-11-16

Main commit 8ec4460a0af291dcba10563912f8fcd0c3f784fd contains the canonical Python/browser Unicode 18 §16.4 packed parser, grammar-role alternatives, exact source offsets and rejected spans/reasons. Exact-main Quality [43963765593] passed 417 Python tests + 70 subtests, IPA corpus structural validation, Node/web checks and production build; Chromium [43963765334] and Pages deploy/runtime smoke [43963765391] passed.

KHM-ORTHO-BNF-PARSER-001 is DONE_VERIFIED for orthographic structure only. LOC word segmentation, phonological syllabification, IPA gold and Ukrainian output remain separate and incomplete. TN #61 v2 is registered as unicode-tn61-khmer-encoding-structure-v2 with non-normative status and Terms-of-Use limitations; its separate Modern Khmer profile remains TODO. PR #292 was closed as duplicate after equivalent diagnostics were merged independently; its branch remains preserved. Issue #104 remains OPEN; independent IPA gold remains 0.

## Google Khmer TTS lexicon and SLR42 evidence audit — 2026-11-16

The archived Google Language Resources Khmer lexicon was inspected in full at pinned commit `a90601024f07ab7e96c911243324e0adeb16da96` (blob `d399efeca642b1185786b2982374488c525e37c4`). It contains 69,415 two-column rows and 69,405 unique spellings: 62,175 unique Khmer-script keys and 7,230 unique Latin-script keys. Ten spelling keys each have two divergent readings, but no third disambiguation column is populated. The 54 phonemic tokens used by the lexicon all appear in its 56-phone companion inventory. This establishes file-internal symbol consistency, not IPA correctness. The paper's 70,671-entry count differs from the inspected snapshot; its transcription guidelines, Khmer variety and per-entry provenance are not supplied. The lexicon file header declares CC BY 4.0; the companion phonology JSON's exact license scope remains unresolved because repository README and paper statements differ.

The OpenSLR SLR42 page and linked LICENSE declare CC BY-SA 4.0 and list a single male-speaker archive. Sodimana et al. (2018) Table 1 reports 17 female speakers for the same SLR42 URL, and the paper's general license statement says CC BY 4.0 unless otherwise noted. The current provider metadata/license and paper metadata therefore need archive-version reconciliation. No external dataset was imported. `KHMER-GOOGLE-TTS-001` remains PARTIAL; `KHM-GOLD-001` remains BLOCKED (Issue #104, gold=0, accuracy=null).

Exact PR-head verification for the Google lexicon audit: Quality [43965204827] SUCCESS (417 Python tests + 70 subtests, IPA corpus structure validation, Node/web checks and production build); Khmer browser smoke [43965204751] SUCCESS (12/12 Playwright tests). This validates repository engineering and the documentation/source-registry change only, not the lexicon's linguistic correctness or suitability as gold. No local tests or dataset imports are claimed.

## Google Khmer TTS lexicon audit — final exact-head checks — 2026-11-16

PR #300 final head `65bbc704a5bcf6906f5d57841a625e6f9a2b0f29` changes six source/documentation files only. Quality [43965487859] SUCCESS: 417 Python tests + 70 subtests, independent IPA corpus structure validation, Node/web checks and production build. Khmer browser smoke [43965487827] SUCCESS: deterministic web checks, production build and Chromium visible-result checks. No runtime/data/gold changes, local tests, main merge or Pages deployment are claimed. PR #300 remains open. The Google lexicon is a candidate phonemic comparator, not IPA gold; companion inventory rights/profile and per-item provenance remain unresolved. Issue #104 remains OPEN; independent gold=0 and accuracy=null.

### Current PR #300 verification boundary — 2026-11-16

At head `10e579f554f86eb32fa72b14067a24861a2b760e` (17 commits ahead/0 behind base `941fbf0ed01ae79c2a8be0c02f1870b68e19134a`), exact-head Quality [43965941851] SUCCESS (417 Python + 70 subtests, corpus structure, Node/web checks and production build) and Khmer browser smoke [43965941825] SUCCESS (12/12 Playwright tests). The six changed files are the source registry, master handoff, linguistic completion register, IPA collection playbook, IPA corpus contract and repository audit. Source-registry/playbook changes include the Google Festival prompt-index finding (2,748 rows/16 speaker-ID prefixes, no gender labels); do not characterize the post-65bbc changes as handoff/register/repository-audit-only. No runtime, test source, generated artifacts, corpus payload, IPA labels or Ukrainian mappings changed. No local tests, main merge, Pages deployment or production deployment are claimed. PR #300 remains OPEN; no force-push or branch deletion was performed.

 
## Final post-PR #300 mainline verification — 2026-11-16

PR #300 merged as `b60a65179ffbb593fca8f3eb2c07a1c81e6e8489` (final PR head `07608ca77a06eee741f2988f4e8611d5ebb26880`); issue #300 closed. Exact-main Quality [43966413597] SUCCESS (417 Python tests + 70 subtests, corpus validation, Node/web checks and production build); Chromium [43966413730] SUCCESS (12/12 Playwright tests); Pages deploy/runtime smoke [43966413612] SUCCESS.

The source-registry and documentation changes do not modify the deterministic runtime, generated artifacts, lexicon/audio payloads, IPA gold or Ukrainian output. The Google lexicon remains a candidate phonemic comparator, not gold. Its 69,415 rows/69,405 unique spellings and ten divergent duplicate keys are fully audited; the 70,671 paper count, exact target variety/convention, per-entry provenance and companion phonology JSON license remain unresolved. The Festival prompt index has 2,748 records/16 speaker-ID prefixes, which does not reconcile with the paper's 2,906/17-female-speaker metadata or the current OpenSLR male-only archive. Issue #104 remains OPEN; adjudicated IPA gold=0 and accuracy=null. No local tests or dataset imports are claimed.

## Khmer IPA convention draft — merged checkpoint — 2026-11-17

PR #306 merged as `4d7e7bd045544d2a6d407511679761a7b0b839a1` (five documentation/source metadata files). Exact PR-head Quality [43969775235] SUCCESS: 417 Python tests + 70 subtests, corpus structural validation, Node/web checks and production build. Exact PR-head Chromium [43969775186] SUCCESS: 12/12 Playwright tests. The new convention sheet remains `DRAFT_NOT_APPROVED`, proposing `PHONETIC_BROAD` only for specialist review. No runtime, generated artifacts, corpus labels or external data changed. No expert was contacted/recruited; KHM-GOLD-001 remains BLOCKED, gold=0, accuracy=null. PR #305 was superseded and closed with its branch preserved.

 
## Consolidated external Khmer source audit — 2026-11-17

The integration branch reconciles PR #301 (Headley/SEALang seed provenance), #303 (MekongPhon rights/reproducibility) and #304 (Khmer Acoustic Model artifacts) without importing external payloads.

- MekongPhon pinned seed: 8,040 rows, 8,040 unique keys; 8,026 Headley word entries + 10 numerals + 4 punctuation. 7,940/100 split is word-level, not sentence-level. The 1.3m sentence pairs reported in the paper are not in the pinned repository and are generated from OPUS text by dictionary longest-match lookup. Rights unknown; no per-row source locator; Headley profile and notation are not approved contemporary Phnom Penh typed IPA. Candidate comparator only.
- open-dict-data/ipa-dict Khmer: 3,286 rows, 3,261 unique spellings, 25 repeated keys (one divergent), 63 multi-pronunciation rows. Third-party Khmer data identified as CC BY-NC-SA 4.0; retain variants; not unrestricted-commercial eligible and not gold.
- chemvatho/Khmer-acoustic-model: only six-line sample dictionary present; advertised full dictionary, model archive, 137-hour audio and manual alignment annotations absent. README reports 29,204 vs dictionary README 33,091; license declarations conflict (CC BY-SA 4.0 vs CC BY 4.0), root MIT covers code. Official MFA model registry lacks `khmer_mfa`. Blocked for import/benchmark/gold.
- PR #304 exact-head Quality failures were due a legacy source-scope assertion requiring `3,286-line`; the integration branch keeps this literal while retaining the expanded row/duplicate/variant audit. Re-run exact-head checks before merge.
- Main at integration start `db02740d57705c08966c87a6b31a5c874c9edc86` passed Quality [43970083315] (417 Python + 70 subtests), Chromium [43970082825] and Pages [43970082889]. Those checks are not evidence for the new integration branch.
- No dataset/model/audio payload, IPA gold labels, Ukrainian mappings or runtime code changed. Independent gold remains 0; accuracy null.

 
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

## Kirby Phnom Penh cluster-audio source audit — 2026-11-17

The University of Edinburgh DataShare record for [Kirby's 2013 Phnom Penh cluster recordings](https://datashare.ed.ac.uk/items/0d735b30-f6ef-4e14-b6f0-a6b5a136e240/full) explicitly declares CC BY 4.0 and identifies 10 native Phnom Penh Khmer speakers, 79 lexical items, three repetitions, two self-selected speech rates, WAV audio and segmented Praat TextGrids. The related Kirby (2014) paper, Methods §2.1, says the first block was read slowly and carefully in a carrier sentence and that 61 items with 35 onset-cluster types were analysed. The archive is 477.8 MB (MD5 `a8efcd0cda1cc44fa400fd118d59c396`).

Disposition: strong supporting audio candidate; not IPA gold and not automatically equivalent to standalone careful citation-form speech. The full item list has not been extracted or checked; the 2014 study's scope does not provide complete series × vowel × coda × prominence coverage. No audio was downloaded/imported. See [the source dossier](ipa-gold/khmer-kirby-cluster-audio-source-audit.md). `KHM-KIRBY-CLUSTER-AUDIO-001 = PARTIAL`; pilot use remains blocked on expert profile ruling, item manifest, contrast coverage and the existing human annotation gates.

## PR #309 exact-head engineering verification — 2026-11-17

PR [#309](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/309), exact head `74622599f6128f34b3ee2fcd19e346b018d399e2`, passed hosted Quality workflow [44034902245](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44034902245): corpus structural validation; 417 Python tests + 70 subtests; Node web checks (including Unicode 18 parser and romanization/Ukrainian adapter checks); production Vite build. The workflow has a single Quality job; no browser/Playwright or Pages deployment check was triggered for this documentation-only change. No local tests were run. This verifies repository integrity/build compatibility, not the linguistic validity of the external audio source. No runtime or gold data changed.

## Kirby source audit merge — 2026-11-17

PR [#309](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/309) was squash-merged as `417ddfe598fc70913d9597dc5fb0b4dc7863d515`. Exact PR-head `a4ab13947e4ff060bf66b2b8a5c14ac432ae195c` passed Quality [44039162569] (417 Python tests + 70 subtests, IPA corpus validator, Node/web checks, Vite production build) and Chromium browser smoke [44039174297] (deterministic checks, production build and visible-result Chromium exercise). No Pages deployment or local tests are claimed. Post-merge mainline checks were queued at the time of this note.

The merged addition registers the CC BY 4.0 Kirby Phnom Penh cluster recordings as a supporting audio candidate only. The archive and MD5 have not been locally verified; exact 79-item manifest and target-profile equivalence remain unresolved. No audio/IPA gold/runtime payload was imported. Gold remains 0 and empirical accuracy null.

## Kirby 2011 Phnom Penh tonogenesis source audit — 2026-11-17

Enriched the existing DataShare source-registry records after verifying indexed primary full-item metadata and Kirby (2014): [audio recordings DOI 10.7488/ds/321](https://doi.org/10.7488/ds/321) and [supplementary data DOI 10.7488/ds/319](https://doi.org/10.7488/ds/319). Both records explicitly state CC BY 4.0. The audio metadata describes 16 Phnom Penh speakers and WAV/TextGrid/Praat analysis files; the paper §§3.1–3.2 reports 20 recruited native Phnom Penh participants (13 female, 21–60), 41 careful/read items and a separate 15-item colloquial repetition task. Four participants who retained /r/ in both conditions were excluded from subsequent analysis, leaving 16 analyzed participants. This plausibly explains the DataShare count, although archive folder membership has not been checked. The supplementary item contains anonymised production/perception CSVs, KlattGrid stimuli and R code. This is supporting evidence for contextual /r/-loss/prosody, not a complete IPA convention, general tone rule or standalone citation-form gold. No archive downloaded; no local MD5 or item manifest verified; no data imported. See [source dossier](ipa-gold/khmer-kirby-tonogenesis-datasets-audit.md).

## PR #310 merge and mainline verification — 2026-11-17

PR [#310](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/310) merged as `4d568f712b8ac055809bc01e53ea7d257b79a6a0`. It enriches the existing Kirby 2011 DataShare source records; no duplicate DOI records remain. Exact PR head `a4e8f315f3de8d1742ed5018e27be164ed7bb7cb` passed Quality [44054481444] (417 Python tests + 70 subtests, corpus validator, Node/web checks, Vite build) and Chromium [44054481411] (12 Playwright tests). Post-merge main commit passed Quality [44054711288], Chromium [44054711282] and the pre-existing automatic Pages deployment + smoke-test workflow [44054711377]. Pages root, `system.html`, generated JS and CSS were fetched and checked successfully. No Pages settings were changed; no release published; no local tests.

The 16-speaker DataShare description is plausibly explained by Kirby (2014)'s 20 recruited participants minus four excluded from subsequent analysis for retaining /r/ in both conditions, leaving 16 analyzed; actual archive folder membership remains unverified. Appendix A is romanized, not Khmer orthography. Audio archive and supplementary CSVs remain undownloaded; checksums are provider-listed only. No IPA gold labels or corpus payload were added. Gold=0; empirical accuracy=null.


## Sok & Adams (2016) Khmer G2P rule baseline — 2026-11-17

The full PACLIC 30 paper is now registered and audited in [the source dossier](ipa-gold/khmer-sok-adams-phonological-principles-audit.md). It describes two distinct stages: orthography-to-phonemic forms intended for careful speech, followed by phonemic-to-phonetic rules for rapid/ordinary colloquial speech. Candidate rule families include onset-cluster series assimilation, minor-to-major syllable series effects, Bantoc-conditioned vowel modification, coda changes, cluster-transition aspiration/schwa and minor-syllable reduction.

The separation of layers is architecturally relevant, but the paper's rule set is not automatically portable to the current contemporary Phnom Penh careful-citation profile. Its 140-word hand-selected validation set uses Headley (1997) phonemic references and author-created phonetic forms; its 10,110-word evaluation is dictionary-derived, with 999 compounds and Pali/Sanskrit loans outside scope. The reported 97.86% and 98.43% are not independent speech-gold benchmark scores. Tables contain notation/OCR inconsistencies that require visual page verification before any proposed rule transfer. The proceedings reserve copyright to the respective authors; no open license was verified. No runtime or corpus changes were made.


## Final continuation audit — 2026-11-17

Two merged PRs extended the repository's evidence and contract without inventing linguistic labels:

- PR #311 registers and audits Sok & Adams (2016), PACLIC 30. It records the paper's two-stage careful phonemic vs rapid colloquial phonetic architecture, dictionary/Headley provenance, 140-word hand-selected validation, excluded compounds and loans, reported-score limitations and unknown redistribution rights. Its scores are not project accuracy and no rules/data were imported.
- PR #312 repairs the typed result contract: both Python and browser runtimes now carry `ipa_kind`; linguistic units remain `UNRESOLVED` pending expert approval and punctuation is `NOT_APPLICABLE`. No IPA strings, Ukrainian mappings or phonological rules changed.

Mainline commit `c426d1c3bacd6edb303b2b4977e5b34c09b81620` passed Quality [44065655690] (418 Python tests + 70 subtests, corpus structural validation, Node/web checks and Vite build), Chromium [44065655890] (12/12 Playwright tests), and Pages [44065655951] (production build/browser, deployment and deployed-site/runtime-asset smoke). PR-head checks also passed for both PRs. The only observed warning is the existing non-blocking deprecated setuptools `project.license` TOML-table format.

Registry has 49 unique source IDs. No open PRs; issue #104 remains open. Both working branches are preserved. IPA convention is still `DRAFT_NOT_APPROVED`; independent adjudicated gold=0; empirical accuracy=null. The repository is engineering/build verified and research-ready as a partial prototype, not linguistically release-ready.


## Full-text Phnom Penh phonetics review — 2026-11-17

A focused full-text review of Chem (2020) and Mam, Pittayaporn & Maspong (2025) is recorded in [the source addendum](ipa-gold/khmer-phonetic-literature-fulltext-review-2026-11-17.md). Chem's final acoustic analysis uses four selected Phnom Penh speakers and 61 formal frame-read items; the full wordlist and token-level replacement history are absent, and its vowel inventory/notation has internal inconsistencies. Mam et al. use five Greater Phnom Penh speakers and 50 cluster/disyllable targets in separate PPK/SK tasks; normalized F0 patterns suggest possible pitch phonologization but do not demonstrate a categorical general tone system. Neither paper supplies a complete source-exact 30-item pilot set or approved IPA convention. No labels, runtime rules, corpus rows or Ukrainian mappings were added. IPA convention remains DRAFT_NOT_APPROVED, gold=0, empirical accuracy=null.


## PR #314 merge and exact-head verification — 2026-11-17

PR [#314](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/314) merged as `4760964618f05290560372b1ee60b4f7fba8ae72`. Exact PR-head Quality [44076405229] SUCCESS (418 Python tests + 70 subtests, corpus structural validation, Node/web checks and Vite build); Chromium [44076405251] SUCCESS (12/12 Playwright tests). Corpus validator correctly reports no adjudicated gold (`NOT_READY_NO_ADJUDICATED_GOLD`). The change is documentation/source-audit only; no Pages deployment was required, no local tests were run (DNS failure to github.com), and no runtime/data/gold/generated artifacts changed. Issue #104 remains open; IPA convention DRAFT_NOT_APPROVED; gold=0; empirical accuracy=null.


## Mixed-script and numeric source-boundary audit — 2026-11-17

The user-supplied Khmer paragraph exposed a tokenizer boundary defect: adjacent Latin text was swallowed by a Khmer run, and Khmer decimal digits attached to a word were sent through Khmer structural validation. The Python and browser tokenizers now isolate script transitions and consecutive Unicode numeric runs. Numeric runs are passed through unchanged as NON_LINGUISTIC with ipa_kind NOT_APPLICABLE; foreign-script runs remain explicit unsupported units. Tests verify source reconstruction and that valid Khmer neighbors retain their local outputs. This is a tokenizer/source-integrity correction, not a lexical segmenter or a new language/phonology capability. Khmer word division, non-Khmer transcription and number reading remain outside the implemented contract.


## Mixed-script and numeric source-boundary correction — exact PR-head checks — 2026-11-17

PR [#316](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/316) latest head `5eb9d23bdadf175fcb40561ff1de26f6f784ad2e` passes Quality [44079138980] (422 Python tests + 70 subtests, expected no-gold validator state, Node/web checks and Vite build) and Chromium [44079138905] (13/13 Playwright tests). The earlier browser failure was a stale assertion that expected the entire mixed input to be invalid; it was updated to assert local preservation, and the new mixed-script/numeral browser test passes.

The script-run correction isolates Khmer, foreign-script and numeric runs while preserving exact concatenation/source order. U+200C ZERO WIDTH NON-JOINER is explicitly transparent within a run; this was added after review identified that treating it as an unrelated script would split a Khmer orthographic unit. Numeric literals are preserved as `NON_LINGUISTIC` with `ipa_kind=NOT_APPLICABLE`; no pronunciation is inferred. Foreign text remains unsupported. No lexical segmentation, translation, pronunciation data, IPA gold, or Ukrainian phonology was added. No local tests or post-merge Pages deployment are claimed yet.


## PR #316 post-merge verification — 2026-11-17

PR [#316](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/316) merged as `cca8612e98292ce2ee2f103e12bcce152d4b3416`. Exact PR-head Quality [44079343371] and Chromium [44079343343] passed; post-merge mainline Quality [44079454281] SUCCESS (422 Python tests + 70 subtests, corpus validator, Node/web checks and Vite build), Chromium [44079454289] SUCCESS (13/13), and Pages [44079454302] SUCCESS (production browser, deployment and deployed-site/runtime-asset smoke test).

The mixed-script/numeral boundary task is DONE_VERIFIED as a structural/output-integrity improvement. Python and browser tokenizers split foreign-script and numeric runs from Khmer orthographic units while preserving source order; numeric literals remain unchanged and are typed NON_LINGUISTIC / NOT_APPLICABLE; foreign-script runs remain unsupported; U+200C ZWNJ is transparent within the current run. No word segmentation, number reading, translation or new phonological claim was introduced.

Linguistic release gates are unchanged: Issue #104 OPEN; IPA convention DRAFT_NOT_APPROVED; linguistic ipa_kind UNRESOLVED; independent adjudicated gold 0; empirical accuracy null. No local tests or external expert engagement are claimed.

## Expert shortlist revalidation — 2026-11-17

Public-source review strengthens the candidate screen without changing any linguistic acceptance status. Chem Vatho's current profile/CV identifies him as native Khmer, Dr. phil. in Phonetics (University of Cologne, 2025), author of a Central Khmer phonetic-reduction dissertation, prior RUPP Khmer/linguistics lecturer and Royal Academy of Cambodia linguistics-committee member; his skills include acoustic phonetics, segmental/prosodic annotation, IPA transcription and convention design, and his profile lists a Phnom Penh Khmer IPA Illustration under revision. He is the strongest candidate for primary target-profile review, but has a conflict to disclose as maintainer of the Khmer acoustic-model/dictionary resource; he must not be sole adjudicator of items from his own resource.

James P. Kirby's LMU profile and peer-reviewed Phnom Penh Khmer studies support a bounded independent technical challenge of /r/-loss, onset F0/VOT, phonation, cluster transitions and speech-style distinctions. Public evidence does not identify him as a native Khmer speaker or as a complete target-profile convention authority. Confirm independence/conflicts with Vatho before assigning the challenge-review role. Nielson Hul and Becky Butler co-authored a forthcoming Khmer diphthong chapter and must not automatically be counted as independent from each other. Honglada Klaharn is only a candidate for structural phonological review; Sothornin Mam only for scoped PPK pitch/F0 review.

Sources: [Vatho profile/CV](https://khmercorpus.com/about-me), [LMU Kirby profile](https://www.phonetik.uni-muenchen.de/~jkirby/about/), [Cornell Hul profile](https://as.cornell.edu/people/nielson-hul), [ChulaSEAL TAI 2025](https://www.arts.chula.ac.th/chulaseal/2025/05/24/chulaseal-at-tai-2025-presenting-southeast-asian-tone-and-intonation-research-in-germany/), [Klaharn et al. (2019)](https://he02.tci-thaijo.org/index.php/Veridian-E-Journal/article/view/170728).

No outreach occurred. This is not recruitment or expert approval. Issue #104 remains OPEN; IPA convention DRAFT_NOT_APPROVED; independent adjudicated gold=0; empirical accuracy=null.


## PR #319 expert shortlist revalidation — exact mainline closeout — 2026-11-17

PR [#319](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/319) merged as `033e979c06c30aff5569750fae824f90484558ed`. Exact PR-head Quality [44081155872] and Chromium [44081155831] passed; duplicate push Quality [44081116226] also passed. Exact post-merge mainline Quality [44081323278] SUCCESS (422 Python tests + 70 subtests, expected `NOT_READY_NO_ADJUDICATED_GOLD`, Node/web checks and Vite build), Chromium [44081323386] SUCCESS (13/13 Playwright), and Pages [44081323295] SUCCESS (production browser, deployment and deployed-site/runtime-asset smoke).

This closes the candidate-screening/documentation task only. Vatho is a strong candidate for primary Phnom Penh careful-citation convention review, with an acoustic-model/dictionary conflict to disclose. Kirby is a candidate for bounded PPK acoustic challenge review, not a native target-profile authority; his independence from Vatho still requires direct conflict screening. Hul/Butler co-authorship means they cannot be counted as independent from each other. No person was contacted or recruited. No IPA convention or data/gold was approved or changed.

Issue #104 remains OPEN; IPA convention DRAFT_NOT_APPROVED; 30-item pilot BLOCKED; adjudicated gold=0; empirical accuracy=null. No local tests were run.


## Final closeout — PR #320 — 2026-11-17

PR [#320](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/320) merged as `06d0fc1c38889ea6c02d78f7f3274c835f2744e2`. Exact PR-head Quality [44081681961] SUCCESS (422 Python tests + 70 subtests, expected corpus validator state, Node/web checks and Vite build). Exact-main Quality [44081774790] SUCCESS (422 + 70 subtests), Chromium [44081774743] SUCCESS (13/13), and Pages [44081774768] SUCCESS (production browser, deploy and deployed-site/runtime-asset smoke).

This is documentation closeout only. Candidate-screening deliverable is DONE_VERIFIED; no expert was contacted or recruited. IPA convention DRAFT_NOT_APPROVED; 30-item pilot BLOCKED; independent adjudicated gold=0; empirical accuracy=null; Issue #104 OPEN. No local tests were run.


## Khmer lexical word-segmentation evidence audit — 2026-11-17

The mixed-script/numeral behavior is already fixed by PR #316; the residual issue in the supplied paragraph is lexical word segmentation, which must not be conflated with orthographic syllable parsing. A dedicated source-backed review is recorded in [KHMER-LEXICAL-SEGMENTATION-EVIDENCE-AUDIT-2026-11-17.md](audits/current/KHMER-LEXICAL-SEGMENTATION-EVIDENCE-AUDIT-2026-11-17.md).

The review identifies ALT/NOVA's 20,000-sentence manual tokenization/POS corpus (Kaing et al. 2021; DOI 10.1145/3464378) and the khPOS corpus as candidate resources, but both are declared CC BY-NC-SA 4.0; ALT is translated from English Wikinews and khPOS metadata mentions student/voter-list sources. Sung & Hwang's F1 0.906 is specific to their own dataset/test setup; Tran et al.'s 92.3% concerns dictionary-entry syllable division, not running-text word boundaries. No corpus was imported or trained on.

KHM-LEXICAL-WORD-SEGMENTATION-001 is BLOCKED pending tokenization convention/use approval, license/privacy/provenance review, rights-compatible corpus selection, independent annotation/adjudication and held-out evaluation. The existing word-boundary evidence model remains profile-neutral and abstaining; no runtime word segmenter is claimed.


## PR #322 exact-main verification — 2026-11-17

PR #322's lexical-segmentation evidence audit is merged as `1cb22c9dfb5ebec539c01544d9e4270b20293b2d`. Exact-main Quality [44087269233] passed (422 Python tests + 70 subtests, corpus structural validator, web checks and Vite build); Chromium [44087269259] passed (13/13 Playwright); Pages [44087269174] passed (production browser exercise, deployment and deployed-site/runtime-asset smoke test).

This verifies the documentation/evidence checkpoint and software workflows only. It does not verify Khmer lexical word segmentation, approve the IPA convention, add independent gold or establish transcription accuracy. KHM-LEXICAL-WORD-SEGMENTATION-001 remains BLOCKED; Issue #104 remains OPEN; adjudicated gold remains 0 and empirical accuracy remains null. No local tests or manual accessibility review are claimed.


## PR #324 Sok & Adams rule-transfer audit — final verification — 2026-11-17

PR [#324](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/324) was squash-merged as `3f3352e94e993ab54a79c952bf6c1e7f9d187ae6` from branch `research/sok-adams-rule-transfer-audit-2026-11-17`, based on `460a3df4476f9f4beba7649909be101ef5331336`. Its exact-head Quality [44105695150] passed (422 Python tests + 70 subtests; corpus validator returned the expected `NOT_READY_NO_ADJUDICATED_GOLD`; web checks and production build passed), and Chromium [44105694990] passed (13/13 Playwright tests). The duplicate exact-head Quality run [44105669690] also passed. Post-merge mainline Quality [44105872935], Chromium [44105872929] (13/13), and Pages [44105872984] all passed. Pages deployed the exact main SHA and the deployed-site/runtime-asset smoke test passed.

The visual table audit is DONE_VERIFIED as source inspection only. `KHM-SOK-ADAMS-RULE-TRANSFER-001` remains BLOCKED pending qualified contemporary Phnom Penh careful-citation review and item-level positive/negative evidence. No phonological rule, IPA label, corpus row, Ukrainian mapping or generated artifact changed. Issue #104 remains OPEN; IPA convention remains `DRAFT_NOT_APPROVED`; adjudicated gold=0; empirical accuracy=null. No local tests or external expert outreach are claimed.

Final main: `3f3352e94e993ab54a79c952bf6c1e7f9d187ae6`. No open PRs remain at this checkpoint. Repository is engineering/build verified and research-ready as a partial prototype, not linguistically release-ready.


## PR #326 shared onset-fallback fixture — exact-main closeout — 2026-11-17

PR [#326](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/326) was squash-merged as `c345860483b378c66434139b7923a47094875c5a` from `test/khmer-onset-fallback-cross-runtime-fixture-2026-11-17`, based on `0d6e81a58ce514d49d93115c21925441b6acb579`. Exact-head Quality [44111499227] passed: **423 Python tests + 70 subtests**, Node/web checks and production build. Exact-head Chromium [44111513471] passed **14/14 Playwright tests**. The final code-bearing head also passed Quality [44111468114] and Chromium [44111467933] (14/14); the final documentation head Quality [44111513165] passed.

Post-merge mainline Quality [44111679547] passed (**423 Python tests + 70 subtests**, Node/web checks and build). Pages [44111679525] passed, including production browser exercise, deploy and deployed-site/runtime smoke. Main is `c345860483b378c66434139b7923a47094875c5a`; open PR count is 0.

The shared fallback fixture is an engineering regression only: Python checks API-level `null` canonical fields; browser checks rendered NOT_ESTABLISHED markers; both check the separate onset-only `k` → `к?` preview and rule/position provenance. Browser unit detail exposes `data-fallback-rule-id` and `data-fallback-position` for inspection. No new pronunciation rule, IPA label, Ukrainian canonical output, gold record or corpus data was added. The dedicated positional evidence registry remains TODO; broader vowel/subscript/coeng fallback remains blocked pending independently sourced positional rules. IPA convention remains `DRAFT_NOT_APPROVED`; independent adjudicated gold=0; empirical accuracy=null; Issue #104 OPEN. No local tests or human review are claimed.


## Shared onset-fallback parity task acceptance — 2026-11-17

The bounded cross-runtime regression task is now DONE_VERIFIED. PR #326 merged as `c345860483b378c66434139b7923a47094875c5a`; exact-head Quality [44111933616] and Chromium [44111963202] passed, with **423 Python tests + 70 subtests** and **14/14 Playwright tests**. Post-merge mainline at `c345860483b378c66434139b7923a47094875c5a` passed Quality [44111679547], Chromium [44111687227] and Pages [44111679525]. Documentation closeout PR #327 merged as `5a4f97c2c572020829b9c9eff7fad8a3c9d32e0c`; its exact-head Quality/Chromium passed, and final mainline Quality [44112202827], Chromium [44112202856] (14/14) and Pages [44112203152] all passed.

`Browser regression` and `Exact-head CI and Chromium verification` are DONE_VERIFIED for this shared-fixture acceptance only. The broader onset fallback remains PARTIAL: the dedicated per-position evidence registry is still TODO, and vowel/subscript/coeng hints remain excluded absent independent positional evidence. This is not IPA gold; adjudicated gold=0 and empirical accuracy=null. No local tests, external expert review or pronunciation claims are made.

Final main at this checkpoint: `5a4f97c2c572020829b9c9eff7fad8a3c9d32e0c`; open PRs=0; Issue #104 remains OPEN.


## Khmer positional onset evidence registry — 2026-11-17

A bounded evidence-container implementation records all 33 current consonant onset hints in `data/khmer-positional-onset-evidence.json`, with schema `schemas/khmer-positional-onset-evidence.schema.json` and parity/non-promotion tests in `tests/test_khmer_positional_onset_evidence.py`. Each record points to the corresponding character row in Richard Ishida's *Khmer (Cambodian) Orthography Notes*, Basic consonants table. That work is PARTIAL: this is a specialist reference, not a primary phonetic source or project-profile adjudication. The register is not a runtime dependency and does not alter the existing provisional hint. Primary phonetic evidence and qualified review remain outstanding; no vowel, coda, cluster, COENG/subscript realization, tone, canonical IPA or Ukrainian output is inferred.


## PR #329 positional onset registry — final verification — 2026-11-17

PR [#329](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/329) was squash-merged as `841bf283eecf13b2e2ccc7f83f02a8c7617c7cdc`. Exact-head Quality [44118873208] passed with **427 Python tests + 70 subtests**, and Chromium [44118873039] passed. Post-merge mainline Quality [44119105502], Chromium [44119105743], and Pages [44119105718] (build, deploy, deployed-site/runtime smoke) all passed. The evidence register contains 33 exact mirrors of existing onset inventory hints; it does not change runtime. Its acceptance is limited to a specialist-reference evidence container and tests. Primary phonetic evidence, project-profile review and independent adjudication remain outstanding. No IPA gold or empirical accuracy is claimed.

## Skip-navigation accessibility improvement — 2026-11-17

PR [#331](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/331) adds a keyboard-first skip link to both public pages. The link is the first focusable element, appears when focused, and targets `main#main-content`; the target receives programmatic focus. Regression coverage exercises Tab, visible focus state, Enter activation, fragment navigation and target focus on both `/` and `/system.html`.

Exact PR-head Quality [44143747834] and Chromium [44143747746] passed (16/16 browser tests). Post-merge main Quality [44144068435], Chromium [44144068416] (16/16), and Pages deployment/deployed-asset smoke [44144068336] passed on `f594b48615a799b13ae19ad4c2c6453512b8c24d`.

This is a bounded keyboard-navigation improvement, not a complete accessibility audit. Manual screen-reader/assistive-technology review, full keyboard traversal, contrast, zoom/reflow and real mobile-device checks remain PARTIAL/TODO. No local tests or human accessibility review are claimed. Linguistic release gates are unchanged: IPA convention DRAFT_NOT_APPROVED, independent adjudicated gold=0, empirical accuracy=null, Issue #104 OPEN.

## WCAG AA text contrast — 2026-11-17

PR #333 adds browser regressions for representative text/background pairs on the service and methodology pages. Initial valid measurements identified eyebrow red at 4.24:1 on paper, methodology muted text at 3.68:1, and input hint text below 4.5:1. The palette was adjusted (`--red: #c12634`, hint `#6d6c65`, methodology muted text uses `--muted`) and both stylesheet cache keys were refreshed.

Exact-head Quality [44149776508] passed (427 Python + 70 subtests); Chromium [44149776607] passed (18/18). Post-merge Quality [44150006145] passed (427 + 70); Chromium [44150005996] passed (18/18). This verifies only the named selectors and computed pairs, not complete WCAG conformance. Post-merge Pages [44150006152] SUCCESS: production build, browser exercise, deployment and deployed-site asset smoke checks passed. General accessibility remains PARTIAL pending manual and broader automated review.


## PR #334 closeout and exact-main release checkpoint — 2026-11-17

PR [#334](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/334) merged as `a51135d2c65791ae2b433070b71c482a9f49aa40`; PR-head `05aecb1f136c160e03ba8b8ea7dcabee70c58611` was based on `126899c81810750cc1c8a77667340606c10eab20`.

Exact PR-head verification: Quality [44150526026] SUCCESS; Chromium [44150526069] SUCCESS (18/18). Post-merge exact-main verification:
- Quality [44150735242] SUCCESS — 427 Python tests + 70 subtests, expected no-adjudicated-gold validator state, Node/web checks (24 tests) and Vite build.
- Chromium [44150735206] SUCCESS — 18/18 Playwright tests.
- Pages [44150735166] SUCCESS — production build/browser exercise, deployment of exact SHA `a51135d2c65791ae2b433070b71c482a9f49aa40`, and deployed HTML/JS/CSS smoke checks.

The PR #334 change is documentation-only. No runtime or linguistic behavior changed. The automated accessibility evidence is bounded to representative contrast selectors and existing keyboard regressions; full accessibility status remains PARTIAL. The repository is engineering/build/deployment verified and research-ready as a partial prototype, not linguistically release-ready. Issue #104 remains OPEN; convention `DRAFT_NOT_APPROVED`; independent adjudicated gold=0; empirical accuracy=null. This checkpoint was verified through GitHub-hosted APIs and workflow logs; no local test run is claimed.


## PR #336 closeout — 2026-11-17

PR [#336](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/336) merged as `c4cd8b1a17463f306b7c6dffbaad0f80685e5aa1`. It corrects the ALT/NOVA description against the primary NICT Khmer tokenization guideline v0.2: the convention is generally morpheme-level, and compounds are tokenized into components with shallow bracketing based on dictionary/syntactic diagnostics. It does not equate NOVA units with orthographic syllables or project phonetic units.

Exact PR-head Quality [44170618296] and Chromium [44170618297] passed (427 Python tests + 70 subtests; 18/18 browser tests). Post-merge mainline Quality [44170796321], Chromium [44170796376], and Pages [44170796347] all passed. Pages deployed the exact main SHA and passed root/system HTML and JS/CSS asset smoke checks. No runtime or data changed; lexical segmentation remains BLOCKED pending target convention, rights/privacy review and independent adjudicated evaluation. No local tests are claimed because GitHub DNS resolution failed in the execution environment.


## Live branch inventory refresh — 2026-11-17

At exact main `35a98711902ec70a5a718eb16c6d07c128f978b2`, GitHub branch listing pages 1–3 returned 209 refs (main + 208 non-main). There are 208 unique tip SHAs total; one non-main branch, `data/integrate-positional-onset-evidence-register-2026-11-17`, points to the exact main SHA, so 207 non-main tips are distinct. Open PRs=0; the only open issue is #104.

Focused checks confirmed the positional-onset registry is already integrated via PR #329, the PCGN independent-vowel CSV and parity test are byte-identical to main, and the direct BGN/PCGN feature branch is stale/diverged. No historical branch was deleted, force-updated or merged wholesale. The no-diff branch was preserved.

`KHM-BRANCH-AUDIT-001` remains PARTIAL: this is a live ref inventory plus focused branch triage, not a full changed-file/commit/PR-ancestry reconciliation of all 208 non-main refs. The previously recorded 131-ref/130-comparison inventory is a historical checkpoint, not the current count. Preserve refs pending an owner archival policy.

## Selected historical branch content reconciliation — 2026-11-17

Focused comparisons against exact main `f5c9c70661126b61a23d5435c8c4368215c36746` found:

- The subscript-independent-vowel parser branch is an older parser/test snapshot; main now includes mixed-script/numeral run isolation and orthographic-component scan coverage.
- The packed-parse-forest and rejected-span branches are older than main's parser/schema/browser contract, which includes explicit `rejected_spans` diagnostics and additional Unicode 18 regression cases.
- The two BNF parser branches use the earlier singular `orthographic_syllable.py` module; main uses the later plural parser plus browser adapter.
- The verified practical-adapter branch's `practical.py` and practical policy JSON are byte-identical to main.
- The Ukrainian romanization matrix branch's two CSV files are line-identical to main.
- The direct BGN/PCGN input branch is 24 ahead / 163 behind and lacks current mixed-script/numeral and residual-script guard work; no wholesale port is justified.
- The PCGN independent-vowel source-register branch's CSV and parity test are byte-identical to main.
- The positional-onset evidence branch was already integrated via PR #329.

These findings support preserving rather than wholesale-merging the selected stale branches. The complete branch audit remains PARTIAL: this is an 11-branch focused content check, not a complete 208-ref content/PR-ancestry reconciliation.

## PR #338 verification — 2026-11-17

PR [#338](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/338) merged as `f5c9c70661126b61a23d5435c8c4368215c36746`. Exact-head Quality [44173194420] and [44173216454] passed (427 Python tests + 70 subtests; expected no-adjudicated-gold validator state); Chromium [44173216381] passed 18/18. Post-merge mainline Quality [44173400187], Chromium [44173400043] (18/18), and Pages [44173400219] all passed, including production browser exercise, deployment and deployed-site/runtime-asset smoke. No runtime or linguistic behavior changed.
## Final branch inventory and PR #339 mainline verification — 2026-11-17

Fresh GitHub listing pages 1–3 after creation of the final clean closeout branch returned 212 refs (main + 211 non-main), 212 unique tip SHAs, 0 open PRs and 1 open issue (#104). This supersedes the 211-ref snapshot from immediately before this final branch was created.

PR [#339](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/339) merged as `b5a878f33dae74d34754c547580c5a494307cdce`. Exact-head Quality [44173798008] and [44173819190] passed (427 Python tests + 70 subtests); Chromium [44173818953] passed 18/18. Post-merge mainline Quality [44173970460], Chromium [44173970246] (18/18), and Pages [44173970271] all passed; Pages deployed the exact SHA and passed deployed-site HTML/JS/CSS smoke.

PR #340 was closed unmerged after a squash-merge conflict; its branch was preserved. The final inventory and closeout note are being reapplied from a clean branch based on current main.

The branch audit remains PARTIAL: 11 representative historical branches have focused content dispositions, but all 211 non-main refs have not undergone complete changed-file/commit/PR-ancestry reconciliation. No branch was deleted, force-updated or merged wholesale.

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
