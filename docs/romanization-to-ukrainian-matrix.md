# Khmer romanization → Ukrainian orthographic matrix

**Status:** PARTIAL — the Ukrainian target crosswalk is populated and the runtime accepts direct BGN/PCGN Latin input, including the source diacritics represented in the 37-row vowel/rime matrix. When the input is Khmer script, the upstream Latin-output package still emits BGN/PCGN-derived ASCII and drops diacritics; those lost contextual distinctions cannot be reconstructed. Ukrainian target values remain project proposals.
**Primary variety:** contemporary Standard Khmer, Phnom Penh-oriented only where supported.

## Standard selection

Select **BGN/PCGN 1972 Romanization of Khmer (Cambodian)** as the reference romanization profile. It is the strongest defensible choice for a source-backed research table: the UNGEGN Working Group report states that the UN-recommended system was approved in 1972 (Resolution II/10) and is based on the BGN/PCGN 1972 system. The official PCGN guide was checked for validity in October 2017 and contains consonant, subscript, vowel, diacritic and numeral tables.

**National-system scope caveat (evidence reconciliation 2026-11-12):** BGN/PCGN 1972 remains the selected, fully source-located *research crosswalk profile* in this matrix. The distinct Cambodian 1995/1997 system's primary table has now been located in the Ministry of Land Management, Urban Planning and Construction's **2023 provisional Gazetteer of Cambodia**, pp. vii–viii. Its foreword says the Geography Department already used the system, that it would be submitted to the National Committee for consideration and adoption, and that the Gazetteer is a provisional release pending approval by the National Commission. Cambodia's 2019 national report and UNGEGN's 2025 report confirm its use in gazetteers. The UK PCGN's May 2026 *Cambodia Toponymic Factfile* nevertheless says the system is not yet implemented consistently and awaits evidence of official consistent use. These statements are compatible if the 1995/1997 system has provisional departmental/gazetteer use but lacks final national adoption and consistent implementation. Keep the profile **EVIDENCE_LIMITED** pending formal adoption evidence and a rights review of the primary table. Do not silently relabel the BGN/PCGN matrix. The Library of Congress **ALA-LC Khmer Romanization Table (1997 version)** remains a separate cataloguing profile.

Sources:
- Ministry of Land Management, Urban Planning and Construction, *Gazetteer of Cambodia* (October 2023), pp. vii–viii, “Romanized System for Khmer (Prepared by Geography Department, 1995. Last modification 1997)”; mirror hosted by Open Development Cambodia: https://data.opendevelopmentcambodia.net/en/dataset/569795eb-1691-4d63-9af3-919dec269472/resource/4097e4be-ccd6-4081-b139-ebcb42a38fa1/download/gazetteer_of_cambodia_25.10.2023.pdf. Original PDF copyright © 2023 Geography Department; the mirror record states no license is given for the PDF.
- Government of Cambodia, *Report on the activities of the standardization of geographical names for the period 2019–2022*, GEGN.2/2023/104/CRP.104, pp. 1–2: https://digitallibrary.un.org/record/4017595/files/GEGN.2_2023_104_CRP.104-EN.pdf
- UNGEGN Working Group on Romanization Systems, *Current status of United Nations romanization systems for geographical names*, GEGN.2/2023/11/CRP.11, p. 2: https://digitallibrary.un.org/record/4018337/files/GEGN.2_2023_11_CRP.11-EN.pdf
- UNGEGN Asia South-East Division, *Report*, GEGN.2/2025/73/CRP.73, p. 3: https://unstats.un.org/unsd/ungegn/sessions/4th_session_2025/documents/GEGN.2_2025_73_CRP73_item4a.pdf
- UK PCGN, *Cambodia Toponymic Factfile*, reviewed May 2026, pp. 1–2: https://assets.publishing.service.gov.uk/media/6a19aa44b95db968c8f3bc6f/Cambodia_Toponymic_Factfile.pdf
- Library of Congress, *Khmer Romanization Table, 1997 version* (ALA-LC): https://www.loc.gov/catdir/cpso/romanization/khmer-1997.pdf


Primary sources:
- UNGEGN, Report on the Current Status of United Nations Romanization Systems for Geographical Names (2013), Khmer section: https://unstats.un.org/unsd/ungegn/working_groups/wg5/documents/wgrr4khmer.pdf
- UK PCGN, Romanization of Khmer (Cambodian), BGN/PCGN 1972 Agreement (checked October 2017): https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf

UNGEGN notes that Khmer is an alphasyllabic script, that the romanization requires contextual rules, that word division is not ordinarily indicated, and that the system is generally not reversible. Thus “transliterate everything” means **cover every supported orthographic unit with an explicit table row or an explicit exception state**; it does not mean that the Latin output alone can reconstruct all Khmer code points.

## Existing implementation audit

The current @gmana/km-translit 0.1.2 integration is documented as **BGN/PCGN-derived ASCII**, drops diacritics and is not a fully conformant BGN/PCGN implementation. It is useful as an existing romanization candidate but cannot be called the selected standard implementation or the final complete orthographic mode. It must remain separately labelled until replaced or proven equivalent against the official table.

The current romanization card remains independent from IPA → Ukrainian conversion. It supports two inputs: Khmer script, which is passed through the current BGN/PCGN-derived ASCII package, and an already romanized Latin string, which is mapped directly without re-romanization. The direct path preserves the PCGN diacritics represented in the matrix; unknown Latin fragments are bracketed. Matrix completeness and runtime integration do not establish full BGN/PCGN conformance, reversibility, or pronunciation evidence.

## Consonant and subscript crosswalk (source-backed romanization; Ukrainian target is a project proposal)

The machine-readable consonant matrix is [data/khmer/romanization_ukrainian.csv](../data/khmer/romanization_ukrainian.csv). It records all 22 official PCGN consonant-table rows plus the special ឝ row, source code-point sequences, BGN/PCGN forms, Ukrainian candidate, evidence status, URL and row locator. The CSV is authoritative for this consonant slice; it is not a complete vowel/rime matrix.

| PCGN table row | Khmer base / subscript forms | BGN/PCGN romanization | Ukrainian candidate | Status |
|---|---|---|---|---|
| 1 | ក / គ; corresponding feet | k | к | PROPOSED |
| 2 | ខ / ឃ; corresponding feet | kh | к' | PROPOSED |
| 3 | ង; corresponding foot | ng | нг | PROPOSED |
| 4 | ច / ជ; corresponding feet | ch | ч | PROPOSED |
| 5 | ឆ / ឈ; corresponding feet | chh | ч' | PROPOSED |
| 6 | ញ; corresponding foot | nh | нь | PROPOSED |
| 7 | ដ / ឌ; corresponding feet | d | д | PROPOSED |
| 8 | ឋ / ឍ; corresponding feet | th | т' | PROPOSED |
| 9 | ថ / ធ; corresponding feet | th | т' | PROPOSED |
| 10 | ណ / ន; corresponding feet | n | н | PROPOSED |
| 11 | ត / ទ; corresponding feet | t | т | PROPOSED |
| 12 | ប; corresponding foot | b, p (contextual) | б / п | PROPOSED; map the actual selected Latin output |
| 13 | ព; corresponding foot | p | п | PROPOSED |
| 14 | ផ / ភ; corresponding feet | ph | п' | PROPOSED |
| 15 | ម; corresponding foot | m | м | PROPOSED |
| 16 | យ (no foot) | y | й | PROPOSED |
| 17 | រ; corresponding foot | r | р | PROPOSED |
| 18 | ឡ / ល; foot for ល only | l | л | PROPOSED |
| 19 | វ; corresponding foot | v | в | PROPOSED |
| 20 | ស; corresponding foot | s | с | PROPOSED |
| 21 | ហ; corresponding foot | h | г | PROPOSED |
| 22 | អ; corresponding foot | ’ | ʼ | PROPOSED; retain the glottal-onset marker |

The machine-readable matrix [data/khmer/romanization_ukrainian.csv](../data/khmer/romanization_ukrainian.csv) preserves the exact source sequences, the 22 PCGN table row IDs, the Ukrainian candidate/status, the official URL and row-level locator. The target column now explicitly maps the actual romanized outputs: th → т', contextual b / p → б / п, and the glottal marker ’ → ʼ. These are project orthographic conventions, not IPA claims. PCGN explicitly states that there is no subscript form for ឡ; the row-18 record captures this.


## Vowel matrix: contextual source table, not a one-sign substitution table

The official PCGN guide has separate tables for independent vowels, dependent vowel signs (with â-/ô-series and normal/shortened columns), and vowels with anusvara or visarga. The source inventory reproduces the romanization values and now supplies an explicit project Ukrainian rendering for all 37 rows. Alternative source forms remain alternative target forms; this does not resolve which source variant applies in a particular syllable.

**Independent vowel characters**

PCGN numbers the independent-character column within a shared 22-row table; only the following rows contain independent characters. Blank rows in that column are not additional vowel characters.

| PCGN row | Khmer | BGN/PCGN romanization | Ukrainian candidate | Status |
|---|---|---|---|---|
| 3 | ឥ | ĕ | — | EVIDENCE_LIMITED |
| 4 | ឦ | ei | ей | PROPOSED |
| 7 | ឧ | ŏ / ŭ | о / у | ANALYSIS_DEPENDENT |
| 14 | ឯ | ê | е | PROPOSED |
| 15 | ឰ | ai | ай | PROPOSED |
| 16 | ឱ / ឲ | aô | ао | PROPOSED |
| 17 | ឳ | au | ау | PROPOSED |
| 18 | ឪ | âu | ау | PROPOSED |
| 19 | ឫ | rœ̆ | — | EVIDENCE_LIMITED |
| 20 | ឬ | rœ | — | EVIDENCE_LIMITED |
| 21 | ឭ | lœ̆ | — | EVIDENCE_LIMITED |
| 22 | ឮ | lœ | — | EVIDENCE_LIMITED |

**Dependent vowel characters**

| PCGN row | Khmer sign / structure | BGN/PCGN romanization (â-series / ô-series; normal / shortened as applicable) | Ukrainian candidate | Status |
|---|---|---|---|---|
| 1 | ◌ (any consonant or consonant + foot) | â / ô; shortened á / ó | а / о | ANALYSIS_DEPENDENT |
| 2 | ◌ា | a / éa; shortened ă / eă or oă | а / еа | ANALYSIS_DEPENDENT |
| 3 | ◌ិ | ĕ; shortened ĭ | е | ANALYSIS_DEPENDENT |
| 4 | ◌ី | ei; shortened i | ей / і | ANALYSIS_DEPENDENT |
| 5 | ◌ឹ | œ̆ | — | EVIDENCE_LIMITED |
| 6 | ◌ឺ | œ | — | EVIDENCE_LIMITED |
| 7 | ◌ុ | ŏ / ŭ | о / у | ANALYSIS_DEPENDENT |
| 8 | ◌ូ | o / u | о / у | ANALYSIS_DEPENDENT |
| 9 | ◌ួ | uŏ | уо | PROPOSED |
| 10 | េ◌ើ | aeu / eu | — | EVIDENCE_LIMITED |
| 11 | េ◌ឿ | œă | — | EVIDENCE_LIMITED |
| 12 | េ◌ៀ | iĕ | іє | PROPOSED |
| 13 | េ◌ | é | е | PROPOSED |
| 14 | ែ◌ | ê | е | PROPOSED |
| 15 | ៃ◌ | ai / ey | ай / ей | ANALYSIS_DEPENDENT |
| 16 | េ◌ា | aô / oŭ | ао / оу | ANALYSIS_DEPENDENT |
| 17 | េ◌ៅ | au / ŏu | ау / оу | ANALYSIS_DEPENDENT |

**Vowel + anusvara / visarga combinations**

| PCGN row | Source pattern | BGN/PCGN romanization (â-series / ô-series) | Ukrainian candidate | Status |
|---|---|---|---|---|
| 1 | ◌ុ◌ំ | om / ŭm | ом / ум | ANALYSIS_DEPENDENT |
| 2 | ◌ំ | âm / um | ам / ум | ANALYSIS_DEPENDENT |
| 3 | ◌ំ឵ (PCGN composite glyph) | ăm / ŏâm | — | EVIDENCE_LIMITED |
| 4 | ◌ះ | ăh / eăh | — | EVIDENCE_LIMITED |
| 5 | ◌ុ◌ះ | ŏh / ŭh | — | EVIDENCE_LIMITED |
| 6 | េ◌◌ះ | éh / éh | — | EVIDENCE_LIMITED |
| 7 | េ◌឵ះ | aôh / ŏăh | — | EVIDENCE_LIMITED |
| 8 | ◌ំ឵ង | ăng / eăng | — | EVIDENCE_LIMITED |

These are **research candidates**, not a production vowel adapter. The source standard makes vowel rendering depend on consonant series, subscripts, shortening, codas and diacritics. The canonical data implementation must preserve those fields and test each context; a single-sign replacement is not conformant.

## Diacritics and numerals

[data/khmer/romanization_marks_numerals.csv](../data/khmer/romanization_marks_numerals.csv) records all six PCGN diacritical-mark rule rows and all ten Khmer numeral rows. The shortened-vowel rule row 3 explicitly inventories both Khmer source marks ◌់ (U+17CB BANTOC) and ◌័ (U+17D0 SAMYOK SANNYA), as required by PCGN note 5. The marks are not treated as independent letters: PCGN notes specify series changes, shortened-vowel behavior, consonant insertion, positional behavior, and a silent mark that is omitted from romanization. The numeral rows map Khmer digits to their Arabic-digit values. The runtime romanizer must apply these rules contextually rather than concatenate character substitutions.

## Required machine-readable table contract

The canonical source inventory currently lives in three CSVs: consonant/subscript rows, 37 vowel/rime rows, and diacritic/numeral rows. The runtime map remains a static longest-match adapter in `src/khmer-romanization-ukrainian.js`; the Node tests read the CSVs and enforce source-form → Ukrainian-candidate parity. A future generated registry could remove this duplicated mapping, but it must preserve alternative forms and evidence statuses rather than flatten them.

Every supported Khmer grapheme/orthographic syllable must either have a complete path:
**Khmer unit → BGN/PCGN romanized syllable → Ukrainian practical syllable**, or a visible exception/unsupported status. Do not use khmerToLatin output as an IPA source, and do not generate Ukrainian output by applying the IPA mapper to the Latin string.

## Task ledger

| ID | Status | Acceptance |
|---|---|---|
| KHM-ROM-STD-001 | DONE_VERIFIED (source review) | BGN/PCGN 1972 selected; UNGEGN approval and PCGN table cited |
| KHM-ROM-ENGINE-001 | PARTIAL | Khmer-script input still uses the ASCII simplifier; replace/verify it against the full BGN/PCGN table, including contextual diacritics and series resolution. Direct Latin input does not solve this source-generation step. |
| KHM-ROM-UA-TARGET-001 | DONE_VERIFIED | All 22 consonant rows and 37 PCGN vowel/rime rows have non-empty Ukrainian project candidates; exact table/provenance and coverage assertions passed on the feature head and merged mainline. This is a project orthographic proposal, not expert-approved standardization. |
| KHM-ROM-UA-001 | PARTIAL | Direct BGN/PCGN Latin input now maps the raw diacritic forms in all 37 vowel/rime rows to project Ukrainian candidates; Khmer-script input still traverses the upstream ASCII package and loses diacritics. Full acceptance requires contextual series/shortening/coda resolution and expert review of Ukrainian candidates. |
| KHM-ROM-ONSET-001 | DONE_VERIFIED | All 22 PCGN consonant rows plus special ឝ are in data/khmer/romanization_ukrainian.csv; exact row and provenance tests passed in workflow 41229431196 |
| KHM-ROM-VOWEL-INVENTORY-001 | PARTIAL | 37 source rows now match the PCGN glyphs/romanization values; exact-head workflow 41233203184 passed; all 37 source-glyph/romanization assertions are verified |
| KHM-ROM-MARKS-NUMERALS-001 | DONE_VERIFIED (bounded source inventory only) | Six PCGN diacritic rule rows cover seven Khmer source marks, including both U+17CB BANTOC and U+17D0 SAMYOK SANNYA under shortened-vowel note 5; all ten numeral glyphs are inventoried. PR #204 exact-head Quality and Chromium passed; post-merge main Quality, Chromium and Pages deploy passed. | Inventory and provenance are complete and regression-tested. Contextual romanization behavior, including series/shortening/coda resolution, remains outside this task and KHM-ROM-ENGINE-001 remains PARTIAL. |
| KHM-ROM-MATRIX-001 | PARTIAL | The target column is complete for the inventoried rows; PCGN consonant-series × vowel × shortening × coda resolution and contextual romanization generation remain incomplete |
| KHM-ROM-TEST-001 | PARTIAL | Unit tests now cover all 22 consonant rows, all 37 raw diacritic-preserving vowel/rime forms, and direct-input behavior; browser tests cover direct Latin input and unknown fragments. | Remaining: Khmer-script-to-Latin contextual parity, marks/numerals matrix, broad real-package corpus and expert review of Ukrainian candidates. National 1997 profile remains a separate evidence-limited research task. |
| KHM-IPA-001 | PARTIAL | Existing contextual vowel/register/coda IPA model and independent gold remain incomplete |


## Machine-readable vowel inventory

[data/khmer/romanization_vowels_ukrainian.csv](../data/khmer/romanization_vowels_ukrainian.csv) contains **37 source-located PCGN table entries**: 12 independent-character entries, 17 dependent-vowel entries, and 8 vowel-plus-anusvara/visarga entries. The shared PCGN table has 22 row numbers, with a sparse independent-character column; the independent and dependent columns are recorded separately without inventing extra row numbers. Every row now has a Ukrainian candidate. `PROPOSED` marks a single project rendering; `ANALYSIS_DEPENDENT` preserves PCGN alternatives that require source-context resolution. The table remains an inventory of PCGN row forms, not a complete contextual syllable engine.


## Whole-text regression and remaining adapter gap — 2026-10-31

The current main head `1a6921fc75dd011bc8097f6636b8077fc7c59cff` passed Quality [41243972009](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41243972009) and Pages deployment [41243971788](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41243971788). The romanization integration passes the complete source string to the selected library and has regression cases for a full greeting, short mixed-script text, native Khmer numerals, ASCII digits, Latin text, spaces and punctuation. This is input-integrity evidence only. The independent syllable-level romanization → Ukrainian adapter remains TODO; contextual PCGN coverage and unspaced word segmentation remain incomplete. No IPA or Ukrainian gold is inferred from library output.


## Post-merge whole-text verification — 2026-10-31

Current main `28a9bbb909ca57735ceca92f262c2de9eeb43396` passed Quality [41246343908](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41246343908) and Pages [41246343845](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/41246343845). The tests confirm the selected romanization library receives the complete input and preserves supported mixed-text boundaries; they do not establish PCGN 1972 conformance or an implemented Ukrainian syllable adapter. The adapter remains TODO.

## Ukrainian target convention for Latin BGN/PCGN input — 2026-11-12

The target column is a **project orthographic adaptation of the Latin romanization string**, not a second pronunciation analysis. It does not use the IPA adapter and must not be described as phonetic Ukrainian transcription. The original BGN/PCGN string remains the source-of-truth display and should be retained alongside the Ukrainian candidate.

- Consonant units: `k → к`, `kh → к'`, `ng → нг`, `ch → ч`, `chh → ч'`, `nh → нь`, `th → т'`, `b → б`, `p → п`, `ph → п'`, `h → г`, `y → й`, `r → р`, `l → л`, `v → в`, `s → с`, `’ → ʼ`.
- Vowels: Latin vowel bases are rendered with the closest stable Ukrainian letter sequence in the matrix (`a → а`, `e/ê/é/ĕ → е`, `i/ĭ → і`, `o/ŏ → о`, `u/ŭ → у`, `œ/œ̆ → и`); diphthong and coda combinations are rendered as explicit sequences in the 37-row CSV.
- PCGN alternatives remain separated by `/` or explanatory context in the candidate field. `ANALYSIS_DEPENDENT` means the source syllable still determines which listed form applies; it does not mean the target cell is blank.
- Diacritical series shifters and shortening marks are contextual source instructions, not independent Latin output letters. They are not emitted as standalone Ukrainian letters. PCGN's silent mark remains omitted. Numerals remain numeric.
- This convention is intentionally **non-reversible** and does not establish Khmer phoneme values. It maps the selected Latin spelling into a stable Ukrainian rendering only.

## Updated acceptance boundary

`KHM-ROM-UA-TARGET-001` is complete as a table-coverage task. `KHM-ROM-UA-001` remains open until an independent runtime adapter consumes BGN/PCGN Latin output, preserves source text and uncertainty, and passes whole-message tests. `KHM-ROM-ENGINE-001` remains partial because the current package is not fully conformant with BGN/PCGN 1972. No pronunciation or lexical accuracy claim follows from these matrix changes.


## Runtime adapter — 2026-11-12

The romanization panel now sends the existing `@gmana/km-translit` Latin output through `src/khmer-romanization-ukrainian.js`. The adapter preserves non-Khmer runs and punctuation, uses longest-match Latin units, and leaves unknown Latin fragments visible as `⟦…⟧`. It does not call the IPA adapter.

**Acceptance status: PARTIAL, not DONE_VERIFIED as a full BGN/PCGN implementation.** The npm package documents that its BGN/PCGN-derived ASCII profile drops the standard's diacritics; its output is explicitly non-conformant. Once those marks and contextual distinctions have been discarded, the Ukrainian adapter cannot reconstruct the exact PCGN vowel choice. Therefore its output is labelled `PROVISIONAL`, not a validated full-standard conversion. The 37-row matrix remains the reference for context-rich PCGN forms; no phonetic interpretation is implied.

- Runtime module: `src/khmer-romanization-ukrainian.js`
- Runtime tests: `tests/romanization-ukrainian.test.mjs` and the browser test in `tests/browser/site.spec.js`.
- Exact PR-head Quality [43226337969](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43226337969), browser smoke [43226337956](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43226337956), and push Quality [43226325685](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43226325685) passed on `1fa869c524bac5effc98411b71e47e458ad584ae`.

`KHM-ROM-UA-001` is now PARTIAL: the current ASCII output has a usable Ukrainian display adapter, but full acceptance requires a diacritic-preserving BGN/PCGN source romanizer or a separate contextual syllable adapter consuming the full PCGN representation. `KHM-ROM-ENGINE-001` remains PARTIAL. See the package's own scope statement: https://www.npmjs.com/package/%40gmana/km-translit.



Exact PR-head Quality [43226337969](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43226337969), browser smoke [43226337956](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43226337956), and push Quality [43226325685](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43226325685) passed on code head `1fa869c524bac5effc98411b71e47e458ad584ae`. Quality reports 194 Python tests + 62 subtests; browser Chromium smoke passed.


## Khmer romanization runtime — mainline post-merge verification — 2026-11-12

- PR [#164](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/164) merged as `0ba6107a7e5cb09cca44021669a7401fc125eac4`.
- Mainline Quality [43227360792](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43227360792), browser smoke [43227360789](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43227360789), and Pages deployment [43227360801](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43227360801) all SUCCESS.
- The merged implementation remains deliberately PARTIAL/PROVISIONAL: the upstream ASCII romanizer omits PCGN diacritics; this adapter cannot reconstruct lost contextual vowel distinctions. The IPA route remains separate.


## Mainline ledger reconciliation — 2026-11-12

- Verified current `main`: `a86a59cf082d547563b45374ced9dfb45c5cd8db`.
- `KHM-ROM-UA-TARGET-001`: DONE_VERIFIED — 22 consonant rows and 37 vowel/rime rows have non-empty Ukrainian project candidates; matrix tests passed and changes are merged (PR #161; synchronization PR #163).
- `KHM-ROM-UA-001`: PARTIAL — PR #164 integrates `src/khmer-romanization-ukrainian.js` into the separate romanization panel. Foreign text and punctuation are preserved, unknown Latin fragments remain visible, and no IPA fallback is used. The UI labels output PROVISIONAL.
- Exact mainline verification on current head: Quality [43228414756](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43228414756), browser smoke [43228414938](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43228414938), and Pages deployment [43228414646](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43228414646) all SUCCESS.
- `KHM-ROM-ENGINE-001`: PARTIAL — the selected package emits BGN/PCGN-derived ASCII and drops diacritics. Acceptance requires a validated diacritic-preserving, context-aware BGN/PCGN 1972 romanizer and tests for series, vowel, shortening, coda and shifter environments.
- Historical TODO entries above describe earlier checkpoints; this section records current mainline state. Ukrainian candidates remain project orthographic proposals, not IPA or an expert-approved Ukrainian standard.


## Adapter test execution closeout — 2026-11-12

The adapter unit test file was present before this checkpoint but was not referenced by the Khmer `npm test` / `npm run check` scripts, so CI did not execute it. PR #167 corrected test discovery and added explicit assertions for all 22 distinct consonant romanization tokens. It merged as `f0485892f5d4b16e5fbe0ded6f8e083d8b044f4b`. Exact-main Quality [43250158336](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43250158336) and browser smoke [43250158628](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43250158628) passed. The full acceptance remains PARTIAL as stated in KHM-ROM-TEST-001.


## Canonical matrix → runtime parity — 2026-11-12

The Node adapter test now reads the canonical `data/khmer/romanization_ukrainian.csv` directly and executes every one of its 22 rows against `renderLatinWord`. Contextual `b,p` alternatives are checked as two explicit Latin/target pairs; the PCGN glottal marker is checked as U+2019. This prevents the test's hand-maintained consonant list from drifting independently of the source matrix. The existing 33 ASCII vowel candidate checks remain a separate bounded test because the upstream romanizer strips PCGN diacritics; this parity check does not establish contextual BGN/PCGN vowel conformance or validate the linguistic correctness of Ukrainian proposals.


## Real-package whole-message adapter probe — 2026-11-12

A new end-to-end regression sends a mixed whole message through the actual `@gmana/km-translit` package and then through the Ukrainian adapter. It checks native-or-Arabic numerals, mixed Latin identifiers, ASCII punctuation, tab, CRLF, and Khmer sentence-stop preservation while requiring Khmer letters to be romanized. This closes one bounded integration-test gap only; it does not establish full marks/numerals standard coverage, contextual PCGN conformance, or lexical correctness. Exact-head CI is pending.


## Real-package whole-message adapter regression — verified — 2026-11-12

PR [#172](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/172) merged as `054bc8823ba1f109ee102eda5e966edade1c4886`. The actual `@gmana/km-translit` package is now exercised through the Ukrainian adapter on a mixed whole message containing Khmer numerals, a Latin identifier, ASCII punctuation, a tab, CRLF and Khmer sentence-stop punctuation. The regression confirms visible native-or-Arabic numerals, preservation of non-Khmer content and conversion of Khmer letters. Exact PR-head Quality [43267521108](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43267521108) and browser smoke [43267521498](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43267521498) passed. Exact mainline Quality [43267655512](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43267655512), browser smoke [43267655359](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43267655359), and Pages deployment plus deployed-site/runtime smoke [43267655210](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43267655210) all passed on main. `KHM-ROM-TEST-WHOLE-001` is DONE_VERIFIED. Broader marks/numerals matrix completeness, diacritic-preserving PCGN, Ukrainian expert adjudication and full romanization-standard conformance remain open.


## Khmer numeral crosswalk runtime implementation — 2026-11-12

The canonical ten-row Khmer numeral slice explicitly proposes Arabic digits 0–9. The Ukrainian adapter now converts U+17E0–U+17E9 to ASCII 0–9 after the upstream romanizer, so the target convention is enforced even when the package preserves native Khmer digits. A data-driven test reads all ten numeral rows from `data/khmer/romanization_marks_numerals.csv`; the real-package whole-message regression now requires Arabic-digit output. This is orthographic numeric rendering, not phonetic processing. Exact-head verification is pending.


## Khmer numeral crosswalk runtime — verified — 2026-11-12

The ten-row numeral crosswalk is now executable: U+17E0–U+17E9 map to Arabic digits 0–9 in the Ukrainian orthographic adapter. The initial regression correctly failed on `០` versus `0`; the fix then passed exact PR-head Quality [43268412329](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43268412329) and browser smoke [43268412356](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43268412356). PR #174 merged as `ae890fdd436aed9c0fab077401e7612153ce2e6a`. Exact mainline Quality [43268536002](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43268536002), browser smoke [43268536046](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43268536046), and Pages deployment/deployed-site smoke [43268535985](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43268535985) all passed. `KHM-ROM-NUMERALS-001` is DONE_VERIFIED. The six diacritical-mark rows remain context-dependent and are not assigned context-free target forms.


## Full vowel inventory adapter coverage — 2026-11-12

PR [#177](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/177) adds a data-driven check across all 37 canonical PCGN vowel and vowel-coda rows. The test normalizes source diacritics to the ASCII representation expected from the current upstream package, then checks each resulting form against the row's documented Ukrainian candidate set and requires zero unsupported units. Exact PR-head Quality [43275618264](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43275618264) passed (194 Python tests + 62 subtests; 12 Node adapter tests) and Chromium smoke [43275618099](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43275618099) passed. PR merged as `19a36f820625f53c6f50fbbe810bfbd074bb1ee7`. This is an inventory/crosswalk consistency test only: it does not choose between context-dependent PCGN alternatives or recover distinctions lost by the ASCII upstream romanizer. Ukrainian candidates remain project proposals pending expert review.


## Direct BGN/PCGN Latin input → Ukrainian — runtime contract

The romanization panel now accepts either:

1. **Khmer-script input:** the existing `@gmana/km-translit` 0.1.2 package generates a BGN/PCGN-derived ASCII form; the Ukrainian adapter maps that form. The package omits PCGN diacritics, so contextual distinctions lost upstream remain unrecoverable and the result stays PROVISIONAL.
2. **Already romanized Latin input:** when the input contains no Khmer script, the adapter treats it as BGN/PCGN 1972 romanization and maps it directly to the Ukrainian candidate layer. It supports the diacritic-preserving forms in the canonical 37-row vowel/rime matrix, including `â, ô, á, ó, ă, ĕ, ĭ, ŏ, ŭ, é, ê, œ̆, œ, œă, iĕ, uŏ, aô, oŭ, eă, oă, aôh, ŏăh, eăh, ăh, ŏh, ŭh, éh, âm, ŭm, ăm, ŏâm, ăng, eăng`.
3. **Unknown Latin fragments:** remain visible in `⟦…⟧` and produce PARTIAL status. No IPA or phonetic fallback is invoked.

The direct path is an orthographic mapping from a supplied romanization, not a Khmer pronunciation engine. It cannot recover omitted diacritics, resolve ambiguous romanization alternatives that the input itself does not distinguish, or establish that a supplied Latin string is actually BGN/PCGN. The UI treats any Latin-only input in this mode as BGN/PCGN; mixed Khmer+Latin input is not a dedicated mixed-script mode and should be entered in separate runs.

The Ukrainian output remains PROVISIONAL because the target values in the CSV are project proposals, not an expert-adjudicated Ukrainian standard. Tests now exercise the raw diacritic forms in all 37 canonical vowel/rime rows as well as the browser's direct-input path.

## Direct-input implementation evidence — 2026-11-15

PR #192 merged as `736b1bc30bc6ccea6eb1d9f3aacd0647c17b848f`. Exact-head Quality [43699528446](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43699528446) passed 223 tests + 70 subtests; Chromium [43699528852](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43699528852) passed 7 browser tests. The tests assert every raw diacritic-preserving form in the 37-row vowel/rime CSV maps to its corresponding project Ukrainian candidate. This verifies table/runtime parity, not the linguistic correctness of those candidates.


## Mixed-script input boundary

The direct Latin mode assumes one input format per run. If Latin BGN/PCGN text and Khmer letters/marks are mixed, the UI does not silently combine the direct-Latin and Khmer-source pipelines: Khmer letters/marks are bracketed as unsupported and the result is PARTIAL. Khmer numerals remain eligible for the existing Arabic-digit conversion, and Khmer punctuation is preserved. Enter Khmer-script text or Latin BGN/PCGN romanization separately for a meaningful result.


## Residual-script output guard — 2026-11-15

PR #201 adds a fail-closed check after the upstream Khmer-script → Latin romanizer and after direct BGN/PCGN Latin rendering. Any Khmer-script letter or combining mark still present in the would-be Latin output is bracketed and counted unsupported; the result is `PARTIAL`. Khmer punctuation remains preserved and is not treated as an unconverted letter/mark. This prevents silent pass-through of residual Khmer orthographic material.

This guard does **not** reconstruct diacritics dropped by the upstream ASCII package, determine contextual series/shortening/coda forms, or establish BGN/PCGN conformance. KHM-ROM-ENGINE-001 and KHM-ROM-TEST-001 remain PARTIAL. PR #201 exact-head and post-merge Quality/Chromium/Pages workflows passed; see the canonical master handoff for run IDs.


## PCGN shortened-vowel mark inventory correction — 2026-11-15

The machine-readable mark matrix previously listed U+17CB BANTOC (◌់) for PCGN note 5 but omitted U+17D0 SAMYOK SANNYA (◌័). The official PCGN note explicitly distinguishes both marks and states that both participate in the shortened-vowel patterns. CSV row 3 now records both source units while preserving the six PCGN rule-row categories. This is an inventory correction only: it does not infer a new romanization output or Ukrainian candidate. Regression assertions cover the row's two source units and their Unicode identities. See the official PCGN 1972 Khmer guide: https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf (note 5).

Verification on the exact PR #204 head `b27b87081819307da5ffe27d55e3cf4521004730`: Quality [43721677822](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43721677822) and Chromium [43721677790](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43721677790) both SUCCESS. Quality includes independent IPA corpus structure validation, Python tests, web checks and production build; Chromium visible-results smoke passed. Push Quality [43721673728](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43721673728) also SUCCESS on the same SHA.


## Mainline closeout — PCGN mark inventory — 2026-11-15

- PR #204 merged as `58735a94a8a8f76635f948c2d003d590f26fb0b2` into `main`.
- Exact merge-main Quality [43721873111](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43721873111) SUCCESS: independent IPA corpus structure validation, **224 Python tests + 70 subtests**, web checks and production build.
- Exact merge-main Chromium [43721873141](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43721873141) SUCCESS: **11 browser tests**.
- Exact merge-main Pages [43721873125](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/43721873125) SUCCESS: production build, 11-test Chromium exercise, Pages deployment and deployed-site/runtime-asset smoke test.
- `KHM-ROM-MARKS-NUMERALS-001` is now `DONE_VERIFIED` only for the bounded source inventory (six rule rows, seven Khmer marks, ten numerals). `KHM-ROM-ENGINE-001` and `KHM-ROM-TEST-001` remain `PARTIAL`; no contextual PCGN generator or linguistic accuracy claim follows.
- No local checkout or local test execution is claimed.


## External implementation candidate review — UNGEGN/Khmer Engine (2026-11-15)

A potentially useful contextual implementation was inspected: [pheasaKhmer/khmer-engine](https://github.com/pheasaKhmer/khmer-engine/tree/31b72cd4665f69678fc835da2f501771e42f097a), pinned for this review at `31b72cd4665f69678fc835da2f501771e42f097a` (2026-10-10). Its `rules.py` explicitly implements the **UNGEGN 2013** romanization profile, not a declared BGN/PCGN 1972 implementation. UNGEGN describes its recommended system as approved in 1972 and based on BGN/PCGN 1972, but that historical relationship is not proof that every implementation detail is equivalent.

**Useful engineering patterns observed (candidate only):**
- Separates written Khmer clusters from inferred spoken syllables.
- Represents onset, subscript onset, register shifter, vowel, signs and finals as inspectable fields.
- Infers competing syllable parses with a weighted Viterbi-style state search rather than pretending written clusters equal spoken syllables.
- Selects a-series/o-series values from onset/subscript and shifter context; applies final-sensitive o-series selection and explicit cases for BANTOC, SAMYOK SANNYA, NIKAHIT, REAHMUK, YUUKALEAPINTU and ROBAT.
- Tests include official province-name examples and worked examples attributed to UNGEGN report notes.

**Why it is not adopted as a drop-in engine:**
- Its public contract is UNGEGN 2013; a rule-by-rule reconciliation against the project's selected BGN/PCGN 1972 guide is still required.
- The source itself labels some forms as “not given” and derives them by analogy or from Wikipedia (for example SAMYOK before final យ and ឰ/ៈ cases). Those cannot be silently promoted to official rules.
- Syllable boundaries are inferred with heuristic costs because the orthography does not encode every spoken boundary. This introduces ambiguity and requires an explicit uncertainty/abstention contract and expert review.
- Whole-text operation uses a lexicon segmenter; this project cannot assume a reliable Khmer word boundary from whitespace or a naive code-point split.
- The tests are implementation regression fixtures, not independent double-annotated IPA gold; they do not validate Ukrainian target proposals or phonetic accuracy.

**Licensing/provenance:** the reviewed engine repository declares MIT for code. Its README/data manifest separately identifies bundled sample word/pronunciation data as CC BY 4.0 and counts as ODC-By 1.0; its package metadata expresses the combined package license accordingly. The engine depends on `pheasa>=0.1.0`; the reviewed Pheasa repository declares Apache-2.0. A future port/adoption must preserve code attribution and satisfy the normalizer dependency's license, and should not copy the lexicon/sample data unless its separate data rights and attribution are deliberately accepted. This is a review of public declarations, not legal advice or independent rights verification.

**Disposition:** `RESEARCH_CANDIDATE`, not selected, not imported, not benchmarked in this repository. Use its architecture as a comparison target for the future Khmer-script contextual romanizer; first produce a source-by-source BGN/PCGN ↔ UNGEGN rule diff and a reviewed set of ambiguous syllable parses. Preserve IPA as a separate phonological boundary; this engine produces orthographic romanization, not IPA.

Pinned references:
- Engine source: https://github.com/pheasaKhmer/khmer-engine/tree/31b72cd4665f69678fc835da2f501771e42f097a
- Rule implementation: https://github.com/pheasaKhmer/khmer-engine/blob/31b72cd4665f69678fc835da2f501771e/src/khmer_engine/rules.py
- Syllable parser: https://github.com/pheasaKhmer/khmer-engine/blob/31b72cd4665f69678fc835da2f501771e/src/khmer_engine/syllables.py
- UNGEGN report v4.0 (September 2013): https://www.eki.ee/wgrs/rom1_km.pdf
- Normalizer dependency: https://github.com/pheasaKhmer/pheasa/tree/760c4b134188dd8bbab6c8ac88419fb0ce119fe9


## Normative profile reconciliation — BGN/PCGN vs UNGEGN (2026-11-15)

A pinned source comparison is recorded in [BGN-PCGN-UNGEGN-RULE-DIFF-2026-11-15.md](audits/current/BGN-PCGN-UNGEGN-RULE-DIFF-2026-11-15.md). The candidate `pheasaKhmer/khmer-engine` implements UNGEGN 2013, not a verified PCGN 1972 drop-in. One explicit note-level delta matters to series resolution: PCGN note 3's neutral-subscript list is the five nasals plus y/r/l/v; UNGEGN note 3 adds ស. The candidate includes ស in `SERIES_NEUTRAL_SUBSCRIPTS`, so that constant must not be copied unchanged into a PCGN engine. The candidate also labels SAMYOK-before-final-y and YUUKALEAPINTU outputs as not given by the report/derived from secondary material, and extends the eă-final set to kh beyond the listed k/ng/h set. These are not accepted PCGN rules. No runtime or Ukrainian target behavior changed.


## Exact-main checkpoint — profile-diff research (2026-11-15)

PR #209 merged as `266297fcc296388220ea48c975344f5aa14f097d`. Exact-main hosted Quality [43730567132], Chromium [43730567159], and Pages build/deploy [43730567118] all SUCCESS. The comparison is documented in [BGN-PCGN-UNGEGN-RULE-DIFF-2026-11-15.md](audits/current/BGN-PCGN-UNGEGN-RULE-DIFF-2026-11-15.md). This closes only the bounded profile-text comparison; it does not implement a contextual Khmer-script romanizer or certify linguistic accuracy. `KHM-ROM-ENGINE-001` and `KHM-ROM-UA-001` remain PARTIAL; IPA gold remains 0.


## PCGN notes 1–11 source registry — 2026-11-15

The complete eleven-note section of the official BGN/PCGN 1972 guide is now represented in `data/khmer/romanization_pcgn_notes.csv`. Each note has a primary-source locator, a bounded summary, its conditions/exceptions, and an explicit `DOCUMENTED_ONLY` implementation status. This complements (does not replace) the row-level consonant, vowel/rime, diacritic and numeral matrices.

The registry deliberately preserves the high-risk contextual constraints:

- Note 2: register-shifter direction and the ប / បា exception.
- Note 3: PCGN's weak-subscript set (the five nasals plus យ/រ/ល/វ), the distinct ប/បា p-in-â behavior, and the source's warning that some feet are ambiguous. It does **not** add ស to the neutral set.
- Note 5: both BANTOC and SAMYOK SANNYA patterns, with the ô-series eă condition restricted to following k/ng/h and oă otherwise.
- Notes 6–8: ROBAT's following-consonant dependency, syllable-position-sensitive ◌៏, and non-romanized silent ◌៍.
- Notes 9–11: the unresolved ŏ/ŭ alternative, roman-character code-point inventory, and case handling.

Python regression tests check all eleven notes, exact PCGN weak-subscript membership, both shortening marks and the closed k/ng/h condition. This is a source-documentation and guardrail milestone only: it does not implement the contextual romanizer, infer missing diacritics, choose ambiguous readings, create IPA, or promote Ukrainian target proposals. Official source: https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf (pp. 2–6, Notes 1–11).


## Exact-main verification — PCGN Notes 1–11 registry — 2026-11-15

PR #211 merged as `9383385fc3244ff600d0fab254c6488a83d92d7b`. Exact PR-head Quality [43732940452] and Chromium [43732940449], push Quality [43732930991], and post-merge main Quality [43733051013], Chromium [43733051164] and Pages [43733051031] all SUCCESS. The Python test suite includes the new PCGN note-registry assertions; browser smoke and Pages production-site/deployment checks also passed.

This verifies the source-located Notes 1–11 registry and tests only. The Khmer-script romanization engine remains PARTIAL; no new romanization outputs, IPA labels, Ukrainian targets or gold entries were introduced.


## Typed PCGN orthographic analysis boundary — 2026-11-15

Added `src/khmer_ua/pcgn.py` with `analyze_pcgn_orthographic_chunk`, an intentionally narrow, typed structural adapter for a caller-supplied orthographic chunk. It preserves:

- unstacked/base consonant identities and their *orthographic* register labels;
- each coeng + consonant pair as a subscript token, including its identity and orthographic register;
- MUUSIKATOAN / TRIISAP, dependent and independent vowel signs;
- BANTOC / SAMYOK SANNYA as distinct shortening marks;
- ROBAT, AHSDA and TOANDAKHIAT as separately typed marks with source positions;
- original and NFC-normalized text, token code points, unresolved components, warnings and source provenance.

The record explicitly fixes `syllable_segmentation=NOT_PERFORMED`, `series_decision=UNRESOLVED`, `register_source=NOT_SELECTED`, `coda_decision=UNRESOLVED`, and `romanization/ipa/ukrainian=null`. This is not a PCGN romanizer and does not decide phonetic syllables, apply register shifters, infer codas, reconstruct omitted marks or produce a Ukrainian form. Multiple unstacked consonants are retained rather than guessed to be an onset, coda or next syllable. Malformed coeng and unknown material are preserved and return `UNSUPPORTED`.

The serialized record contract is in `schemas/pcgn-orthographic-analysis.schema.json`; tests are in `tests/test_pcgn_orthographic_analysis.py`. The implementation uses the project's existing consonant/sign inventories and NFC normalizer. It does not modify the existing IPA-first engine or its phonetic outputs. Official PCGN source: https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf, Notes 2–8.


## Typed PCGN orthographic analysis — exact-main verification — 2026-11-15

PR #213 merged as `18134929554420875b447b1c5128b3b879e3f608`. PR-head Quality [43734106341], Chromium [43734106320], push Quality [43734102361], and exact-main Quality [43734192447], Chromium [43734192457], Pages [43734192455] all SUCCESS.

The new `analyze_pcgn_orthographic_chunk` API, its schema and focused tests are verified on exact main. Acceptance is limited to typed structural preservation and fail-closed abstention; no contextual PCGN romanization, phonetic syllabification, IPA or Ukrainian target is generated. The existing IPA-first path is unchanged.


## PCGN Note 3 series resolver — 2026-11-15

Added `resolve_pcgn_series` as a narrow second-stage operation over the typed orthographic record. It applies only the official Note 3 base/foot selection rule:

- no foot: use the base consonant's table series;
- one non-weak foot: use the foot's series;
- one weak foot (the five nasals plus យ/រ/ល/វ) with a non-weak base: use the base's series;
- weak base + weak foot: use the foot's series;
- ប with one foot: retain the Note 3 exception `p` in the â series as a typed onset exception, not as a complete romanization.

The weak-foot inventory is exactly `ង ញ ណ ន ម យ រ ល វ`; it does not include ស. The PCGN table's statement that ឡ has no subscript form is now enforced as an unsupported structure rather than silently accepted.

The resolver abstains when a register shifter is present (Note 2 is not implemented here), when there are multiple bases/feet, or when the structure contains unsupported material. It returns only `â` / `ô` series metadata and a source locator to PCGN 1972 Note 3 (pp. 2–3). It does not choose a vowel, coda, syllable boundary, IPA or Ukrainian form. Schema: `schemas/pcgn-series-decision.schema.json`; tests: `tests/test_pcgn_series_resolution.py`. Primary source: https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf (consonant table and Note 3).
