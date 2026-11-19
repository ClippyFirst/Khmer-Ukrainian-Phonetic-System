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


## Continuation audit — 2026-11-18: pinned optional phonemizer and branch inventory

The exact mainline base for this continuation was `52b7ae143c2edc0dc34ec87b5e356d4654ea5fb3`; Quality [44257382312](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44257382312), Chromium [44257382268](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44257382268), and Pages [44257382273](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44257382273) all succeeded on that SHA.

A fresh complete branch listing returned 224 refs / 224 unique tip SHAs (main + 223 non-main). Prefix counts: a11y 2; audit 15; benchmark 1; ci 1; data 4; docs 97; feat 50; fix 14; release 1; research 28; test 10. This inventory does not imply every ref has had full file-level and PR-ancestry review.

### Optional Khmer Phonemizer diagnostic

PR [#353](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/353) restores the existing `scripts/benchmark_g2p.py` diagnostic in a separate workflow, pinning `khmerphonemizer==0.0.3`. It deliberately does not overwrite the current MekongPhon workflow. The artifact contains the diagnostic JSON and SHA-256 sidecar; exact-head raw-output [44259498574](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44259498574), Quality [44259498582](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44259498582), Chromium [44259498488](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44259498488), and branch-push Quality [44259475466](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44259475466) passed. Artifact ID 14406708793, 1,972 bytes. The harness's independent gold count remains 0 and accuracy remains null. This is DONE_VERIFIED as optional workflow plumbing only.

### Remaining branch refs and dispositions

- `a11y/*` (2): integrated by PRs #331 and #333; documented keyboard navigation and WCAG AA regression work is already on main.
- `docs/*` (97): the earlier 96-ref family was reconciled by PR #350; the additional docs branch is PR #352 and is merged.
- `feat/*` (50): the earlier 49-ref family was reconciled by PR #347; the additional port branch is PR #351 and is merged.
- `audit/*` (15): compare results show documentation-only changed paths or a behind-only ref. The merged closeout series is PRs #341–#350. These refs are preserved.
- `benchmark/current-engine-2026-11-11`: not ported. Its unique workflow imports a Neurlang Khmer Central lexicon but does not establish item-level rights/provenance or independent adjudication. DEFERRED pending that evidence; no output may be treated as gold or accuracy.
- `ci/khmer-g2p-smoke-2026-10-24`: its old unpinned workflow was not copied. The script/tests are already on main and PR #353 restores the useful diagnostic with a version pin.
- Previously audited families remain documented: data 4, test 10, research 28, fix 14, release 1; all historical refs remain preserved.

### Evidence and release boundary

Issue [#104](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/issues/104) remains the only open issue. `data/benchmark/gold.tsv` is header-only; annotation, adjudication, records and split JSONL files are empty. No expert has been contacted/recruited per the latest issue comments. The convention still requires expert approval; two independent annotators, an independent adjudicator, curator, private blind channel, rights verification and 30 adjudicated items remain open. `KHM-BRANCH-AUDIT-001` remains PARTIAL because a complete file/commit/PR-ancestry audit of all 223 non-main refs is not complete.

**Classification:** research-ready partial prototype; not linguistically release-ready. No phonological claim, IPA label, gold record or accuracy metric was invented.

 
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


## PR #384 — IPA tie-bar notation boundary correction — 2026-11-18

- Semantic review of `src/khmer_ua/ipa.py` found that a tie bar could be left dangling at end of candidate or followed by a modifier instead of the second segment; ordinary combining diacritics before the tie bar also reset the old state and caused false rejection.
- The fix tracks a pending tie-bar requirement separately from the preceding segment state. It rejects `k͡`, `/k͡/`, `k͡ːa` and `k͡͡a`; it accepts the structural sequence `t̪͡s` without rewriting the input.
- PR [#384](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/384) merged by squash as `70b381d41f00f89bb94c3694b1c6faa692bfe34d`. Exact PR-head Quality [44315101232](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44315101232) and browser smoke [44315101225](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44315101225) passed. Exact-main Quality [44315276642](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44315276642), Chromium [44315276566](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44315276566), and Pages deployment/deployed asset smoke [44315276557](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44315276557) passed.
- Scope is strictly notation validation. No source-language phonology, IPA gold, Ukrainian mapping, corpus or benchmark data changed. Do not interpret this gate as pronunciation validation.
- Follow-up semantic spot-checks of PR #287 (Unicode 18 grammar-role ambiguity and packed parse forest) and PR #185 (typed hybrid provider bridge with deterministic final-output authority) found their documented boundaries represented in current main; no duplicate changes were needed.
- Remaining P0 research blocker unchanged: Issue #104 requires an approved convention, independent experts/adjudicator/curator, blind intake, rights-cleared lexical items and adjudication. Gold 0; accuracy null. Manual accessibility and root-license owner decision remain outstanding; full historical semantic review remains PARTIAL.


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

The latest semantic spot-check of `tests/browser/site.spec.js` found two double-escaped JavaScript whitespace regexes in the structural accessibility helper. `aria-labelledby.split(...)` did not split multiple ID references, and whitespace normalization did not collapse actual whitespace. PR [#392](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/392) corrected both patterns; merged main SHA: `9a5da179316c3a40ec159b11c0c936a2c1f9d551`.

Verification: PR-head Quality [44366919812] SUCCESS (432 Python tests + 70 subtests, corpus validator, web checks/build); PR-head Chromium [44366919747] SUCCESS (21/21). Exact-main Quality [44367112353], Chromium [44367112434], and Pages build/deploy plus production browser/deployed-asset smoke [44367112407] all SUCCESS.

Classification: **DONE_VERIFIED** for this narrow test correction. The helper still checks accessible-name sources structurally and does not implement the full Accessible Name and Description Computation algorithm. It is not a full WCAG audit. No runtime or linguistic output/data changed. Manual accessibility remains PARTIAL; Issue #104 remains BLOCKED (adjudicated gold 0; accuracy null); root license remains BLOCKED pending owner decision; full historical semantic re-adjudication remains PARTIAL.


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


## PR #394 — canonical closeout and exact-main verification — 2026-11-18

PR [#394](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/394) merged as `855eac7e6dc39a854cc79055c385152a4a32fc49`. It records the already-merged PR #393 in the canonical handoff, repository audit and linguistic completion register. This follow-up entry records PR #394 itself and prevents the audit trail from stopping one merge behind.

Exact-main Actions on `855eac7e6dc39a854cc79055c385152a4a32fc49`: Quality [44379052920] SUCCESS (432 Python tests + 70 subtests; expected no-adjudicated-gold corpus state; Node/web checks and production build); Chromium [44379052839] SUCCESS; Pages [44379052866] SUCCESS (production build, browser exercise, deployment and published-site/runtime-asset smoke).

Live inventory: 266 refs / 266 unique tip SHAs; 0 open PRs; Issue #104 only. The following historical branches were reviewed as potential unmerged work: `fix/ipa-tie-bar-segment-boundaries-2026-11-18`, `fix/reconcile-unicode-tn61-source-metadata-2026-11-18`, and `feat/pcgn-anusvara-visarga-syllable-assembly-port-2026-11-18`. Their relevant runtime/schema/test/source-registry artifacts are already present on main; no duplicate port was made. Their stale branch tips remain untouched.

No production code or linguistic evidence changed. IPA convention remains DRAFT_NOT_APPROVED; independent gold = 0; empirical accuracy = null. Human recruitment, rights-cleared pilot acquisition and root-license owner decision remain BLOCKED; manual accessibility and historical semantic re-adjudication remain PARTIAL; external benchmark integration remains DEFERRED. No local checkout or local test run is claimed; CI evidence is hosted GitHub Actions.


## PR #395 — canonical closeout and exact-main verification — 2026-11-18

PR [#395](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/395) merged as `3e99140e80ba0a0c1654dcd6f367d651350117b5`; it records PR #394's closeout in the canonical handoff, audit and completion register. This follow-up closes the documentation lag by one merge. It changes documentation only.

Exact PR-head Quality [44389557778](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44389557778), Chromium [44389557809](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44389557809), and push Quality [44389528287](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44389528287): SUCCESS. Exact-main Quality [44393630260](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44393630260), Chromium [44393630430](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44393630430), and Pages/deployed-site smoke [44393630332](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44393630332): SUCCESS.

No runtime or linguistic evidence changed. IPA convention remains DRAFT_NOT_APPROVED; gold = 0; empirical accuracy = null. Independent pilot and root-license decision remain BLOCKED; manual accessibility and historical semantic review remain PARTIAL; external benchmark integration remains DEFERRED. No local checkout or local tests are claimed; verification is hosted GitHub Actions. Repository remains a research-ready partial prototype, not release-ready.


## PR #397 — PCGN omitted-mark uncertainty safeguard — 2026-11-18

PR [#397](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/397) merged as `e888c190570acc19b8cf388d1b2a2a58767e6426`. The series resolver preserves its encoded base/foot decision but now warns that PCGN Note 2 says diacritics are often omitted and a reference source is needed when series is uncertain. The warning is informational: no absent shifter is guessed and no romanization output changes. Added a regression test for both unshifted series defaults. Primary source: UK PCGN, *Romanization of Khmer (Cambodian), BGN/PCGN 1972 Agreement*, introduction and Note 2, pp. 1–3.

PR-head Quality [44395612844](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44395612844), Chromium [44395612835](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44395612835), and push Quality [44395586583](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44395586583): SUCCESS. Exact-main Quality [44395795606](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44395795606), Chromium [44395795589](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44395795589), and Pages/deployed-site smoke [44395795652](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44395795652): SUCCESS.

Classification: warning and regression — DONE_VERIFIED. PCGN boundary inference and full contextual engine — TODO/PARTIAL; human-reviewed ambiguous syllable cases, source-row reconciliation and end-to-end parity remain acceptance requirements. No phonological, IPA, Ukrainian or corpus data changed. No local checkout or local tests are claimed; evidence is hosted GitHub Actions.



## PR #399 — PCGN shifter identity and BA exception correction — 2026-11-18

PR [#399](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/399) merged as `8bbdf54bac984165e86b747504ccf7a1e2735741` (base `725c09a373d0eebb181e3cd3ee02d751e859a3a9`; final PR head `79bacbdef5cd37be94f05d01ea3223644d10d0fb)). The PCGN registry now pairs TRIISAP with U+17CA (`◌៊`) and MUUSIKATOAN with U+17C9 (`◌៉`). The BA exception is corrected in code: TRIISAP does not shift BA under Note 2, while Note 3's p-in-â exception applies to BA + MUUSIKATOAN and BA + foot. The previous BA+TRIISAP p-in-â behavior was unsupported by the guide and has been removed from both decision schemas.

PR-head Quality [44404900821](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44404900821), Chromium [44404900673](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44404900673), push Quality [44404888463](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44404888463), exact-main Quality [44405101264](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44405101264), exact-main Chromium [44405101302](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44405101302), and Pages/deployed-site smoke [44405101273](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44405101273) — all SUCCESS. Quality: 435 Python tests + 70 subtests; browser: 21/21. The independent IPA corpus gate remains correctly `NOT_READY_NO_ADJUDICATED_GOLD`.

Classification: source-registry codepoint correction and BA exception fix — DONE_VERIFIED. Complete contextual PCGN engine and boundary inference — TODO/PARTIAL; requires complete source-row reconciliation and human-reviewed ambiguity cases. No IPA/Ukrainian output, gold labels, source rights or benchmark values changed. Independent IPA gold remains 0 and empirical accuracy null. Repository remains a research-ready partial prototype, not release-ready.


## PR #401 — PCGN BA+AA exception regression coverage — 2026-11-19

PR [#401](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/401) merged as `3bbf3f45afb83faf0335dd2f91f869b85f00c5d5` (base `fc781fa86fa3acb654903560f743d1129428656b`; code/test head `0cf4e3a21bc121b4642afafa7f49e365713f7964)). Added source-backed tests for `ប៊ា` (BA+AA+TRIISAP remains unshifted) and `ប៉ា` (BA+AA+MUUSIKATOAN retains the p-in-â exception), matching PCGN 1972 Notes 2–3. Tests only; no runtime behavior changed.

Push Quality [44407401573](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44407401573), PR Quality [44407541894](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44407541894), PR Chromium [44407541887](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44407541887), exact-main Quality [44407714461](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44407714461) and [44407773406](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44407773406), exact-main Chromium [44407714501](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44407714501), and Pages [44407714752](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44407714752) — all SUCCESS. Quality: 437 Python tests + 70 subtests; browser: 21/21; corpus gate remains `NOT_READY_NO_ADJUDICATED_GOLD`.

Classification: explicit BA+AA Note 2/3 regression coverage — DONE_VERIFIED. Full contextual PCGN engine and boundary inference — TODO/PARTIAL. IPA convention DRAFT_NOT_APPROVED; independent gold = 0; empirical accuracy = null. Rights, recruitment, manual accessibility and historical semantic audit blockers remain unchanged. Research-ready partial prototype, not release-ready.


## PR #402 — post-merge audit closeout — 2026-11-19

PR [#402](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/402) merged by squash as `92011a62d150917dfc12193471b3fe994212e563` (PR head `d18171b5fb3daa711d5bb699db4ec98d5cc2c26d`). It records the PR #401 BA+AA TRIISAP/MUUSIKATOAN regression tests in the canonical project records; no implementation or data changed.

Exact-main checks on `92011a62d150917dfc12193471b3fe994212e563`: Quality [44478963929](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44478963929) SUCCESS (437 Python tests + 70 subtests; expected `NOT_READY_NO_ADJUDICATED_GOLD`; Node/web checks and production build); Chromium [44478963989](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44478963989) SUCCESS (21/21); Pages/deployed-site [44478963941](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44478963941) SUCCESS (build, Chromium, deployment and runtime-asset smoke).

No local checkout/tests are claimed. Current ledger: BA+AA test coverage and canonical PR #402 closeout — DONE_VERIFIED; contextual PCGN engine/boundary inference — TODO/PARTIAL; IPA convention and independent gold — BLOCKED (gold 0; accuracy null); Issue #104 pilot and root license — BLOCKED; manual accessibility/historical semantic review — PARTIAL; external benchmark integration — DEFERRED. Repository remains a research-ready partial prototype, not release-ready.


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


## PR #443 and PCGN documentation-ref reconciliation — 2026-11-19

PR #443 merged as `f9a3dd7fdc813fbf5de8c0e674256c9a6a43ac05`. The exact PR head passed browser smoke and both Quality checks. The exact merge SHA passed Quality and Pages build/deploy; Chromium was still running at the time of this audit update.

Ten PCGN documentation refs were compared with current main. All ten diffs were limited to canonical documentation files; none supplied a unique runtime, test or source-data patch. The BA/AA/foot and vowel closeouts are superseded by the merged Note 2/3 regressions, BA source-row reconciliation, dependent-vowel table/CSV parity, and SAMYOK coda tests. The row-7/profile closeouts are superseded by the exact `េ+ា+ះ` PCGN source sequence, the profile-specific `ស` foot regression, and row-specific source-registry comparison parity. The UNGEGN candidate remains a comparison source only; no candidate-specific behavior should be copied into PCGN.

Current implementation was inspected directly: `PCGN_WEAK_SUBSCRIPTS` excludes `ស`, and the existing structural regression establishes the PCGN series-determining behavior. No runtime change was justified. Retain the historical refs unchanged.

Inventory: 317 branch refs, 317 unique names/tips, 139 `docs/*` refs. No open PRs. This remains a targeted sample; `KHM-BRANCH-AUDIT-001` is still **PARTIAL**, not complete.


### Historical post-merge documentation branches (#206–#259)

Compared 29 retained `docs/post-pr*` refs (#206, #209, #211, #213, #215, #217, #218, #219, #220, #221, #222, #223, #224, #226, #228, #230, #231, #233, #235, #237, #239, #241, #243, #245, #247, #250, #252, #255, #256 and #259) against current main. Their diffs touch only the three canonical status documents and, except for #206, an older romanization matrix snapshot. No source-code or test changes are unique to these refs.

The old matrices (334–841 lines) are superseded by the 541-line current matrix; inspected rows/lines are already present in current main. The only non-subset statements are historical: #215's Note 2 “not implemented” status predates the current resolver, and #223's “workflows running” note is stale CI metadata. Neither requires a port. All branches remain untouched. Full historical branch/ancestry audit remains **PARTIAL**.


## PR #444 and post-merge documentation-ref sample

PR #444 merged as `e78da940dbff2a07376f6ae9cb0b4cc4cd8b6603`. Exact PR-head Quality and browser smoke passed. On exact main, Quality and Chromium passed; Pages build/deploy remained in progress at the time of this update.

Ten further `docs/post-pr*` / `docs/pr*` refs (#294, #300, #314, #316, #319, #353, #322, #334, #336 and #355) were compared. All diffs contain documentation only. #294 includes an obsolete Unicode parser/TN #61 checkpoint, superseded by the current grammar audit and rights-scoped TN metadata. #353 contains a stale assertion that the Khmer Acoustic Model offers a 29,204-entry native-validated CC BY-SA dictionary; current pinned evidence shows conflicting counts and license scopes, a six-line sample only, and no full artifact. Do not port that claim. The remaining refs are superseded status snapshots; no runtime/test patch is unique to them.

No historical refs were changed or deleted. The full historical branch/ancestry audit remains **PARTIAL**.


### PR closeout documentation refs (#357–#393)

Compared ten refs (#357, #359, #362/#363, #366, #367, #378, #389, #390, #392, #393). Each diff changes only the three canonical documentation files. A line-level comparison of the handoff found zero branch-only lines across all ten: their content is already a strict subset of current main. No unique source, runtime, test or evidence needs porting. Historical refs remain untouched; repository-wide branch/PR ancestry reconciliation remains **PARTIAL**.


### Test-branch family (#a11y, grapheme, IPA, romanization, PCGN)

Compared 25 retained test branches spanning accessibility smoke, grapheme accounting, IPA display, Khmer numeral/romanization, onset fallback, direct adapter coverage, PCGN BA/AA/foot exceptions, row parity, exact component boundaries, `ស) foot, SAMYOK coda classes and unconverted marks. No missing test-only implementation was identified. Onset-fallback fixtures/source/tests and the IPA display contract test match main byte-for-byte. Older grapheme/parser and romanization tests are superseded by the richer current parser and adapter suite. PCGN branches with pre-correction dependent-vowel values or overly strict all-row key/separator equality are stale; current main contains corrected PCGN source values and row-specific parity semantics. The `ស`-foot and SAMYOK test content is already present in main. All refs retained unchanged.

Exact-main Pages run 44558019521 later completed SUCCESS on `e78da940dbff2a07376f6ae9cb0b4cc4cd8b6603`, joining the already successful Quality and Chromium runs. Full historical branch ancestry remains **PARTIAL**.


### Early romanization/source-registry documentation refs

Compared ten refs (#1997 profile, phonotactic closeout, letter inventory, numeral crosswalk, onset registry, short-vowel sequence, vowel matrix, whole-message adapter, romanization runtime and test closeouts). Two refs alter the historical source registry; the #1997 branch's 29 IDs are all present in current main's 49-entry registry (zero branch-only IDs). Its old matrix/status claims are superseded by current 2023 provisional Gazetteer evidence and the direct diacritic-preserving BGN/PCGN input contract. The old 192–248-line matrices are superseded by the current 944-line matrix. The old phonology doc has no branch-only lines; main adds the typed IPA-kind contract. No unique source ID, code or test needs porting. Retain branches unchanged; full ancestry audit remains **PARTIAL**.


### PCGN assembly/direct-input documentation refs

Compared ten refs (#alif assembly, closed assembly, Note 5, independent-vowel assembly, omitted shifter, shifter registry, shortened mark, branch inventory, direct romanization input and fallback parity). All changes are canonical docs and older matrix snapshots. The four recent assembly matrices (888–932 lines) and shortened-mark matrix are strict line subsets of current main. The older direct-input matrix contains only two superseded statements about mark inventory/status; current main has explicit BANTOC/SAMYOK and direct diacritic-preserving input. No unique mapping, code or test needs porting. Retain all branches; full audit remains **PARTIAL**.


### Architecture/deployment/handoff documentation refs

Compared ten refs (#ipa-validator, #typed-hybrid-bridge, #repository-information-architecture, #final PR #320, #site deployment, #Pages live service, #grapheme accounting, #mark inventory, #mixed script, #skip navigation). Most are status-document-only. The repository-information-architecture ref additionally changes AGENTS/README/docs index/agent maps/architecture; inspected AGENTS, docs index, codebase map, methodology references and handoff are subsets of current main. Its README/architecture/audit-only additions are older wording and stale PR #64 status. Other README variants likewise contain superseded wording. No unique implementation or requirement needs porting. Retain all branches; full historical ancestry remains **PARTIAL**.


The #candidate-diff test branch's CSV also retains the incorrect candidate-shaped PCGN row-7 key `ោ+ះ` and labels it `MATCH`; current main correctly uses `េ+ា+ះ` and `VALUE_MATCH_KEY_SHAPE_DIFFERS`. Three later parity branches have CSVs byte-identical to main. Do not port the stale row.


### Exact-main / branch-audit checkpoint refs

Ten refs (#correct-main-quality-count, #current-main-branch-inventory, #exact-main-369e0, #exact-main-checkpoint, #exact-main-research-register, #extend-docs-audit, #extend-historical-audit, #final-mainline-status, and two final-mainline checkpoints) were compared. All diffs are canonical status documents only; each handoff snapshot is a strict line subset of current main (zero branch-only lines). Their counts, SHAs and workflow states are historical, not current evidence. No implementation or source/test patch is unique. Retain refs; full ancestry audit remains **PARTIAL**.


Fresh live inventory: 320 refs / 320 unique names / 320 unique tip SHAs, including 142 `docs/*` refs. One open PR (#446) contains this parser handoff documentation batch. No branches were deleted or rewritten. The full historical audit remains **PARTIAL**.


## PR #445 and Unicode 18 parser handoff refs

PR #445 merged as `3663ea20e58510a0a36b5c521627fcacf1c4951b`. Exact PR-head Quality and Chromium passed; exact-main Quality [44561793874], Pages [44561793851] and Chromium [44561793861] also passed on the merge SHA.

Four parser handoff refs were compared. One old source-registry alias `unicode-tn61-v2` is superseded by `unicode-tn61-khmer-encoding-structure-v2`; current main has 49 source entries vs 46 and later sources. The old component-scanner-only/TODO parser status is superseded by the verified Unicode 18 §16.4 packed parse forest. Current tests retain the `ហើ្យ` / `ហើយ` boundary, 2^20 derivation and rejection-span regressions. No missing implementation or evidence to port. Retain branches; full audit remains **PARTIAL**.


### Mainline/PCGN closeout refs

Compared ten refs (#mainline checkpoint, #mainline CI, #historical audit, #exact-main quality count, #PCGN anusvara assembly, #PR440, #PR430, #external-source audit, #Sok IPA kind, #PCGN RoBat). All diffs are canonical docs only; the exact-main quality-count ref has no file diff. Nine handoff snapshots are strict subsets of current main. #430 carries an older PCGN fix-family disposition and 305-ref inventory; main has the later equivalent disposition and refreshed 306/308/319 counts. No unique code, test or source evidence needs porting. Retain refs; full audit remains **PARTIAL**.


### Data/evidence branch refs

Compared all four `data/*` refs. The integrate-onset branch has no diff. The onset-evidence branch's JSON, schema, test and audit doc are byte-identical to current main. Both PCGN independent-vowel branches' CSV and resolver tests are byte-identical to main. No unique data or test needs porting. The onset registry remains a partial specialist-reference register, not adjudicated IPA gold.


## Audit branch and PCGN comparison reconciliation

Nine audit refs (non-PCGN fix semantic review; complete feature/test, fix/release, research family reviews; audit/data/feature/test/research PR-ancestry reviews) were compared at all three canonical docs. Each had zero branch-only lines versus current main; no content needs porting. Their ancestry claims are not independently validated by this content check.

The retained `audit/pcgn-ungegn-vowel-row-reconciliation-2026-11-19` branch is 3 ahead / 21 behind main and carries a stale CSV/test snapshot. It labels PCGN anusvara/visarga row 7 as `MATCH`; current main correctly uses `VALUE_MATCH_KEY_SHAPE_DIFFERS` for PCGN `េ+ា+ះ` versus candidate `ោះ`, retaining value match without asserting source-shape equivalence. Current main's test is larger (127 vs 57 lines) and asserts the structural distinction plus parity with project-owned PCGN source registries. No port is appropriate. Branches remain unchanged; full historical branch/PR ancestry audit remains **PARTIAL**.


### Additional audit-family continuation refs

Nine more audit refs (PCGN continuation, special-syllable continuation, vowel/syllable continuation, typed-IPA/coverage continuation, late-docs, complete-docs, historical continuation, benchmark/CI, and fix/release reconciliation) were checked. All handoff files have zero branch-only lines versus current main. The complete-remaining-branch-families ref has no diff at all. These are superseded audit snapshots; no unique content or implementation needs porting. This does not independently validate their claimed ancestry coverage. Retain refs; full historical audit remains **PARTIAL**.


## Research-branch snapshot reconciliation and exact-main CI

PR #448 merged as `47b3be71478c5a6948a2c66c4761cce9310a5fcb`. Exact PR-head Quality and browser checks passed; exact-main Quality, Chromium and Pages/deploy all passed (runs 44565926529, 44565926669 and 44565926377).

Research-branch checks:
- Ten source-registry snapshots were checked against current `data/khmer/sources.json`; all branch source IDs are subsets of the current 49 IDs. No source record is missing.
- The external IPA renderer branch has schema/test byte-identical to main but an older, smaller registry snapshot.
- The old hybrid-engine branch is superseded by current v2's typed IPA candidate validation and stricter metadata contract; its untyped transport-normalization behavior is not suitable to port.
- The old benchmark-expansion branch permits a model-ID override and lacks the current pinned corpus-source-commit provenance argument. The dedicated MekongPhon diagnostic harness branch's script/tests are byte-identical to current main.
- The old PCGN note registry is a 10-row snapshot; current main has more rows and stronger per-row checks.
No stale branch was merged or rewritten. Full research-family semantic and PR-ancestry review remains **PARTIAL**; gold remains 0, empirical accuracy null, and MekongPhon remains diagnostic-only.


## Fix-branch implementation reconciliation

Reviewed non-PCGN fix refs for explicit IPA kind, unconverted Khmer output, IPA tie-bar boundaries, benchmark reproducibility, orthographic parser diagnostics/rejection spans, typed partial results, unmodeled letters, and mixed-script numeral/romanization guards.

The phonetic-result adapter, IPA implementation/tests, unconverted-output adapter, signs registry, numeral parser/test and rejected-span test are byte-identical to current main where compared. Other branch snapshots are older: rule-engine code predates current numeric passthrough; benchmark script predates current provenance/hashing and no-gold safeguards; parser diagnostics/tests are superseded by the current full test suite; the mixed-script output guard is replaced by a shared current helper. No missing accepted behavior was identified. No branch changed or deleted; full historical fix/PR ancestry audit remains **PARTIAL**.


## Feature-branch snapshot reconciliation and correction

PR #450 merged as aeb0bfbaabc47d8658527da4c5634fae12e9faec; exact PR-head Quality and Chromium passed. Exact-main checks were still running when this entry was drafted.

Ten feature refs were checked. The Unicode 18 parser branch predates the current packed parse forest and role ambiguity representation. The typed IPA candidate branch has an older tie-bar validator; current main explicitly requires a following segment. The typed hybrid bridge, practical Ukrainian adapter and Ukrainian romanization matrix blobs are byte-identical to main. The subscript-independent-vowel branch has an older parser than the current structural scanner and mixed-script tokenizer.

The old PCGN syllable-assembly branches contain an obsolete BA+TRIISAP p-in-â interpretation. Current main follows PCGN Note 2: BA+TRIISAP does not shift series; Note 3 p-in-â applies to BA+MUUSIKATOAN or BA+foot. Their current PCGN source/schema/test blobs differ from main and must not be ported.

Correction: an earlier audit note said the current feat/pcgn-anusvara-visarga-syllable-assembly-port branch blobs were identical to main. Rechecking the live tip shows the PCGN implementation, assembly schema and test are not identical; only package __init__.py is. The branch carries the superseded BA+TRIISAP exception. Main's newer rule and tests are authoritative. Full feature/ancestry audit remains PARTIAL.


CI status correction: exact-main Quality 44568314352, Chromium 44568314381 and Pages/build/deploy 44568314462 later all completed SUCCESS on aeb0bfbaabc47d8658527da4c5634fae12e9faec (Quality retry 44568901376 also SUCCESS). The earlier in-progress note above is historical only.


### Live branch inventory at PR #451 pre-merge checkpoint

Fresh paginated inventory returned 325 refs / 325 unique names / 325 unique tip SHAs, including 142 docs/* refs. Prefix counts: a11y 2, audit 44, benchmark 1, ci 1, data 4, docs 142, feat 50, fix 24, release 1, research 29, test 26, and one unprefixed ref. One PR (#451) was open at the time. Historical branch coverage remains PARTIAL; this count is not a completion percentage.
