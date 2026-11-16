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

The initial Note 3-only resolver abstained on shifters. A later bounded Note 2 subset now handles one correctly placed shifter after a single base with no foot; see “PCGN Note 2 register-shifter subset” below. Multiple bases/feet and unsupported structures still abstain. The resolver returns only `â` / `ô` series metadata; it does not choose a vowel, coda, syllable boundary, IPA or Ukrainian form. Schema: `schemas/pcgn-series-decision.schema.json`; tests: `tests/test_pcgn_series_resolution.py`. Primary source: https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf (consonant table and Note 3).


## PCGN Note 3 series resolver — exact-main verification — 2026-11-15

PR #215 merged as `357ce7f2a5400ff1643e4f64337009dd18c4113d`. Exact PR-head push Quality [43734733096], PR Quality [43734746708], PR Chromium [43734746686], and exact-main Quality [43734828487], Chromium [43734828491], Pages [43734828557] all SUCCESS.

This verifies only Note 3's series-source decision and its fail-closed cases. The series result is not a vowel output or a complete romanization. Note 2, Note 5, coda and syllable-position handling remain unresolved; IPA-first and Ukrainian target behavior remain unchanged.


## PCGN Note 2 register-shifter subset — 2026-11-15

The series resolver now implements a bounded subset of Note 2 in addition to Note 3:

- One TRIISAP U+17CA immediately after a single â-series base consonant changes the selected series to ô.
- One MUUSIKATOAN U+17C9 immediately after a single ô-series base consonant changes the selected series to â.
- The PCGN Note 3 BA + MUUSIKATOAN exception is preserved as `p` in â series.

This subset is deliberately limited to a single base with no foot and a shifter immediately after the base. It abstains for shifters on consonant+foot clusters, multiple or misplaced shifters, wrong-direction marks, and BA + TRIISAP. The record carries the shifter's source position, pre-shifter series, resulting series, effect and PCGN source locator. It still emits no vowel or complete romanization.

This is not complete Note 2 coverage. Do not infer omitted shifters. The primary source is the official BGN/PCGN 1972 guide, Notes 2–3: https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.


## PCGN Note 2 shifter subset — mainline checkpoint — 2026-11-15

PR #217 merged as `c738075c47c76730aa15e96acea588ad924c829c`. The PR-head Quality, Python tests and Chromium smoke passed. Exact-main Quality [43735441278], Chromium [43735441245] and Pages [43735441621] were dispatched on this merge SHA; final conclusions are recorded in the master handoff after completion.

The subset applies only to one correctly positioned shifter after one base with no foot: TRIISAP U+17CA changes â→ô, MUUSIKATOAN U+17C9 changes ô→â. BA+MUUSIKATOAN retains p-in-â. Cluster shifters, BA+TRIISAP, multiple/misplaced/wrong-direction shifters abstain. This is series metadata, not a vowel or romanization output.


## Exact-main checkpoint — PR #218 — 2026-11-15

PR #218 merged as `9420326549d8a327774d0587b6fe19c4b17befcd`. Exact PR-head Quality [43735576766], Chromium [43735576217], push Quality [43735564674] passed. Exact-main Quality [43735662414], Chromium [43735662288] and Pages [43735662264] all SUCCESS, including deployed-site/runtime-asset smoke.


## Exact-main verification — PR #219 — 2026-11-15

PR #219 merged as `690b44174a8831ac9b08b44786d5ffde43f6d5aa`. PR-head push Quality [43735841295], PR Quality [43735855013], PR Chromium [43735855047], exact-main Quality [43735981736], Chromium [43735981714] and Pages [43735981744] all SUCCESS, including deployed-site/runtime-asset smoke. No linguistic behavior changed in this documentation-only PR.


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


## BGN/PCGN Note 5 shortened-vowel component — 2026-11-15

The bounded Note 5 resolver is now implemented as a separate component adapter. It accepts three exact token patterns only: inherent-vowel+BANTOC (row 1), AA+BANTOC (row 2), and SAMYOK SANNYA+coda (row 2). The caller must provide an onset-only analysis that exactly matches the full chunk prefix and an explicit coda class. The resolver applies the existing Notes 2–3 series decision to the onset, then returns only the shortened vowel component: row 1 â/ô = `á/ó`; row 2 â = `ă`; row 2 ô = `eă` before k/ng/h, otherwise `oă`.

The coda class is caller-supplied and is never inferred from the orthographic chunk. The implementation preserves shortening-mark positions, validates exact token order, and abstains on unsupported patterns or mismatched onset context. It does not romanize the coda or generate a complete syllable, IPA, or Ukrainian output.

Source: BGN/PCGN 1972, Vowel Characters table rows 1–2 and Note 5, pp. 2–3: https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.

Status: `KHM-ROM-PCGN-SHORTENING-001 = PARTIAL`; the PCGN syllable engine and IPA-first/Ukrainian adapter remain PARTIAL.


## Exact-main verification — PR #233 / PCGN Note 5 — 2026-11-15

PR #233 merged as `cf57045bf6ddf0537e2a5c33a8b2468e8f3f6f2c`. Final PR-head `9bcf7391ce08557ce2fa56e4cbb764568949f952`: push Quality [43751102348], PR Quality [43751107119], Chromium [43751107131] all SUCCESS (272 tests + 70 subtests; web checks/build/Chromium passed). Exact-main Quality [43751266786], Chromium [43751266785], Pages [43751266784] all SUCCESS, including deployed-site/runtime-asset smoke. Note 5 remains PARTIAL component-only; no IPA/Ukrainian or complete-syllable status promotion.


## BGN/PCGN Note 6 ROBAT component — 2026-11-15

A bounded ROBAT resolver now returns the source-defined `rC` component. It requires exactly one final ROBAT mark immediately after a modeled unstacked consonant, plus an explicit marked-consonant romanization from the PCGN consonant inventory. The resolver validates the supplied consonant value and returns `r` + `C`; it does not infer the consonant's romanization, coda identity, syllable boundary or full syllable.

The official example `ធម៌ → thôrm` is tested at the component boundary: the resolver returns `rm`, not the full word. Unsupported mark placement, multiple ROBAT marks, foot-marked characters and missing/invalid consonant values abstain.

Source: BGN/PCGN 1972, Diacritical Marks table row 4 (p. 4) and Note 6 (p. 5): https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.

Status: `KHM-ROM-PCGN-ROBAT-001 = PARTIAL`; full PCGN syllable assembly and IPA/Ukrainian adapters remain PARTIAL.


## Exact-main verification — PR #235 / PCGN Note 6 — 2026-11-15

PR #235 merged as `34ab63ff37023bddcaeaebb0a6ccd838f662c045`. Final PR-head `0d6f1a2b11ab1de94ad9be391c2dd4932142ff77`: push Quality [43751844908], PR Quality [43751851657], PR Chromium [43751851706] all SUCCESS (278 tests + 70 subtests). Exact-main Quality [43751965081], Chromium [43751965119], Pages [43751965128] all SUCCESS, including deployed-site/runtime-asset smoke. ROBAT remains a PARTIAL `rC` component resolver with caller-supplied consonant value; no IPA/Ukrainian or complete-syllable promotion.


## BGN/PCGN Note 7 AHSDA position effect — 2026-11-15

A bounded AHSDA resolver now requires an explicit syllable position. In `INITIAL` position it records that the mark is not romanized and emits no Latin component. In `FINAL` position it additionally requires an explicit `â` or `ô` series and returns that vowel component. It accepts only one final AHSDA mark immediately after a modeled unstacked consonant.

The resolver does not infer syllable position or series from an orthographic chunk. It does not generate the consonant, coda, complete syllable, IPA or Ukrainian output. Ambiguous/misplaced marks abstain.

Source: BGN/PCGN 1972, Diacritical Marks table row 5 (p. 4) and Note 7 (p. 5): https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.

Status: `KHM-ROM-PCGN-AHSDA-001 = PARTIAL`.


## Exact-main verification — PR #237 / PCGN Note 7 — 2026-11-15

PR #237 merged as `890791a1d8236180c82a39b81bd28b7f772d614c`. Final PR-head `2e3ee353124b1a9cacac64997ceb06720a78370c`: push Quality [43752539333], PR Quality [43752551657], PR Chromium [43752551605] all SUCCESS (284 tests + 70 subtests). Exact-main Quality [43752661403], Chromium [43752661392], Pages [43752661369] all SUCCESS, including deployed-site/runtime-asset smoke. AHSDA remains a PARTIAL component resolver; no syllable-position or series inference, full romanization, IPA or Ukrainian output.


## BGN/PCGN Note 8 TOANDAKHIAT silent-character component — 2026-11-15

A bounded omission resolver now accepts one final TOANDAKHIAT mark only when the caller explicitly identifies the marked consonant grapheme and that exact token immediately precedes the mark. It supports modeled unstacked and subscript consonants and returns an explicit `OMIT_MARKED_CHARACTER` decision.

The resolver does not infer which character is silent, does not romanize the remaining word, and does not produce IPA or Ukrainian output. Non-consonant attachment, multiple/misplaced marks and missing/mismatched caller identification abstain.

Source: BGN/PCGN 1972, Diacritical Marks table row 6 (p. 4) and Note 8 (p. 5): https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.

Status: `KHM-ROM-PCGN-TOANDAKHIAT-001 = PARTIAL`.


## Exact-main verification — PR #239 / PCGN Note 8 — 2026-11-15

PR #239 merged as `9c615293e3037cb0ccbd9db0820698741bbcd5cf`. Final PR-head `e52b2d5be98a521dfa3c6dc5af846c6c79d42dce`: push Quality [43753171641], PR Quality [43753185515], PR Chromium [43753185496] all SUCCESS (290 tests + 70 subtests). Exact-main Quality [43753327251], Chromium [43753327183], Pages [43753327232] all SUCCESS, including deployed-site/runtime-asset smoke. TOANDAKHIAT remains PARTIAL; silent character is caller-identified, with omission-only output.


## BGN/PCGN Note 4 glottal-onset component — 2026-11-15

A bounded onset resolver now maps standalone `អ` to the PCGN apostrophe `’`. It returns both apostrophe options only when the caller explicitly states that the carrier is word-initial and followed by a vowel letter; otherwise it requires the apostrophe. The resolver validates the â-series through the existing Notes 2–3 resolver.

No word position or following-vowel context is inferred. The component does not generate a complete syllable, IPA or Ukrainian output.

Source: BGN/PCGN 1972, Consonant Characters row 22 and Note 4 (p. 5): https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.

Status: `KHM-ROM-PCGN-GLOTTAL-001 = PARTIAL`.


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


## BGN/PCGN vowel characters with anusvara or visarga — table rows 1–8 — 2026-11-15

Added a bounded component resolver for the official p. 4 table “Vowel Characters with Anusvara or Visarga”. It consumes an exact full chunk plus a caller-supplied onset-only analysis, resolves the onset series through Notes 2–3, and maps only these eight source rows:

| Row | Exact source sequence after onset | â series | ô series |
|---:|---|---|---|
| 1 | `ុ + ំ` | `om` | `ŭm` |
| 2 | `ំ` | `âm` | `um` |
| 3 | `ា + ំ` | `ăm` | `ŏâm` |
| 4 | `ះ` | `ăh` | `eăh` |
| 5 | `ុ + ះ` | `ŏh` | `ŭh` |
| 6 | `េ + ះ` | `éh` | `éh` |
| 7 | `ោ + ះ` | `aôh` | `ŏăh` |
| 8 | `ា + ំ + ង` | `ăng` | `eăng` |

Row 8 is intentionally stricter: the caller must pass `coda_character="ង"`; the resolver checks that the exact final base token is NGA. It does not infer a coda or syllable boundary. All unlisted combinations, extra marks, mismatched onset prefixes and unsupported structures abstain.

Implementation: `resolve_pcgn_anusvara_visarga`, `PCGNAnusvaraVisargaDecision`; schema `schemas/pcgn-anusvara-visarga-decision.schema.json`; regression tests `tests/test_pcgn_anusvara_visarga_resolution.py`; source registry `data/khmer/romanization_pcgn_anusvara_visarga.csv`.

Source: BGN/PCGN 1972 Agreement, p. 4: https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.

Status: `KHM-ROM-PCGN-ANUSVARA-VISARGA-001 = PARTIAL`. The result is a vowel/final component only; it does not emit a complete syllable, IPA or Ukrainian text. `KHM-ROM-PCGN-VOWELS-001` and `KHM-ROM-ENGINE-001` remain PARTIAL.


## BGN/PCGN inherent vowel — table row 1 — 2026-11-15

Added `resolve_pcgn_inherent_vowel(analysis, syllable_position)` for the official table's inherent-vowel row 1:

| Context supplied by caller | Series from Notes 2–3 | Component |
|---|---|---|
| NON_FINAL onset | â | `â` |
| NON_FINAL onset | ô | `ô` |
| FINAL consonant | either | Abstain; final-consonant/coda rule is a separate contextual decision |

The resolver accepts one base and at most one modeled foot, derives series through the existing Note 2–3 resolver, and returns only the inherent-vowel component. It requires an explicit non-final position. The guide says a syllable-final consonant not accompanied by a vowel character or TOANDAKHIAT should generally be romanized without a following vowel; the component resolver does not infer this condition or apply it as a universal rule.

Schema: `schemas/pcgn-inherent-vowel-decision.schema.json`; tests: `tests/test_pcgn_inherent_vowel_resolution.py`; machine-readable row: `data/khmer/romanization_pcgn_inherent_vowel.csv`.

Source: BGN/PCGN 1972 Agreement, p. 2, table row 1 and explanatory paragraph: https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.

Status: `KHM-ROM-PCGN-INHERENT-VOWEL-001 = PARTIAL`; final consonant/coda behavior and complete syllable assembly remain outside this component.


## Exact-main verification — PR #249 / anusvara-visarga table — 2026-11-15

PR [#249](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/249) merged as `a50f815f993f8fa9b4ae59c5f0f89b8c7717ea6f`. PR-head push Quality [43760107833], PR Quality [43760141233], PR Chromium [43760141132], exact-main Quality [43760241393], Chromium [43760241451] and Pages build/deploy [43760241464] all SUCCESS. The PR adds only bounded PCGN table rows 1–8; it does not produce IPA/Ukrainian output or complete the PCGN engine.


## Exact-main verification — PR #250 / inherent vowel row 1 — 2026-11-15

PR [#250](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/250) merged as `62ce69bd17dc64fecfb73e81e22ca10bf97a25ff`. PR-head push Quality [43760551262], PR Quality [43760562169], PR Chromium [43760562155], exact-main Quality [43760662544], Chromium [43760662582] and Pages build/deploy [43760662587] all SUCCESS. The new resolver remains a bounded NON_FINAL inherent-vowel component; it does not implement final consonant/coda handling, complete syllable assembly, IPA or Ukrainian output.


## BGN/PCGN consonant table — bounded rows 1–21 — 2026-11-15

Added `resolve_pcgn_consonant(analysis)` for one base plus at most one subscript foot, mapping source Unicode consonant identity to the official PCGN consonant-table Latin component.

- Rows 1–11 and 13–21 use the source table's consonant values.
- Row 12 `ប` returns `b` normally; it returns `p` only for the Note 3 BA+MUUSIKATOAN, BA+TRIISAP or BA+foot exception. A subscript `ប` maps to `p`.
- Row 22 `អ` is not duplicated here; it is delegated to `resolve_pcgn_glottal_onset` under Note 4.
- The resolver obtains series from Notes 2–3, returns base and foot separately plus their concatenated consonant-cluster component, and abstains on multiple feet, unsupported marks and unresolved context. It maps supplied Unicode character identities only; lexical cases requiring external reference consultation are not guessed.

Artifacts: `PCGNConsonantDecision`, schema `schemas/pcgn-consonant-decision.schema.json`, tests `tests/test_pcgn_consonant_resolution.py`, source table `data/khmer/romanization_pcgn_consonants.csv`.

Source: BGN/PCGN 1972 Agreement, pp. 1–2: https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.

Status: `KHM-ROM-PCGN-CONSONANTS-001 = PARTIAL`. No complete syllable, vowel/coda output, IPA or Ukrainian output is generated.


## Exact-main verification — PR #251 — 2026-11-15

PR #251 merged as `aab014705bdf90825b922ff69f1c2e7758e56246`. PR-head push Quality [43760857888], PR Quality [43760868532], PR Chromium [43760868545], exact-main Quality [43760984773], Chromium [43760984785] and Pages [43760984838] all SUCCESS, including deployed-site/runtime-asset smoke. Documentation-only; no language behavior changed.


## Exact-main verification — PR #252 / PCGN consonant components — 2026-11-15

PR [#252](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/pull/252) merged as `16fbbde6238e03290507056388b539f54622d236`. Final PR-head push Quality [43761467383], PR Quality [43761473221], PR Chromium [43761473212], exact-main Quality [43761598283], Chromium [43761598359] and Pages [43761598332] all SUCCESS. Initial push Quality [43761223088] caught malformed schema JSON; corrected schema and final checks passed. The resolver maps rows 1–21 only and delegates row 22 to Note 4.


## BGN/PCGN final-consonant no-following-vowel rule — 2026-11-15

Added `resolve_pcgn_final_consonant(analysis, has_following_vowel_character, has_toandakhiat)` for the guide's general statement that a syllable-final consonant without a vowel character or TOANDAKHIAT should generally have no vowel letter after it.

The caller must isolate the final consonant chunk and explicitly supply both negative context conditions. The resolver accepts one base and at most one foot, maps them through the consonant table, and returns `following_vowel=""`. It does not find syllable boundaries or infer coda identity. BA and ALIF final contexts abstain for separate Note 3/4 handling; vowel-bearing, TOANDAKHIAT, multi-base/foot and unsupported cases also abstain.

Schema: `schemas/pcgn-final-consonant-decision.schema.json`; tests: `tests/test_pcgn_final_consonant_resolution.py`; source rule: `data/khmer/romanization_pcgn_final_consonant.csv`.

Source: BGN/PCGN 1972 Agreement, p. 2: https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.

Status: `KHM-ROM-PCGN-FINAL-CONSONANT-001 = PARTIAL`; the source's “generally” qualifier is preserved, and the resolver emits no complete syllable, IPA or Ukrainian output.


## Exact-main verification — PR #255 / PCGN final-consonant input contract — 2026-11-16

PR #255 merged as `47679154526fa32c5edd9d62ca084de5af4759dd`. PR-head push Quality [43825412435], PR Quality [43825430244], PR Chromium [43825430217] and exact-main Quality [43825536547], Chromium [43825536580], Pages [43825536491] all SUCCESS. Final-consonant context flags now require actual booleans; exhaustive base-character tests were added. `KHM-ROM-PCGN-FINAL-CONSONANT-001` remains PARTIAL and emits no IPA/Ukrainian result.


## Exact-main verification — PR #256 documentation closeout — 2026-11-16

PR #256 merged as `dee4881da4cfb01b6da0ff5e857af67cade14cb1`. PR-head push Quality [43825693046], PR Quality [43825710166], Chromium [43825710160], exact-main Quality [43825806168], Chromium [43825806361] and Pages [43825806234] all SUCCESS. Exact-main Quality ran `pytest -q` (331 passed, 70 subtests passed), `npm run check` and the production build; Chromium smoke and deployed-site/runtime-asset smoke also passed. No language behavior changed in this docs-only PR.


## PCGN independent-vowel source registry — 2026-11-16

The independent-vowel resolver now has an auditable CSV source register for BGN/PCGN 1972 table rows 3, 4, 7 and 14–22. All mapped entries match the existing runtime constant; Note 9 row 7 (`ឧ`) retains unresolved alternatives `ŏ|ŭ`. The new test checks row-by-row parity and the official source URL. This does not change `KHM-ROM-PCGN-INDEPENDENT-VOWELS-001 = PARTIAL`; no IPA/Ukrainian output is generated.


## Exact-main verification — PR #259 PCGN independent-vowel source register — 2026-11-16

PR #259 merged as `458026f080bca31edeec87c2009245213ab667c7`. PR-head push Quality [43826670914], PR Quality [43826697643], Chromium [43826697687], exact-main Quality [43826837012], Chromium [43826837160] and Pages [43826837175] all SUCCESS. Exact-main Python: 332 passed, 70 subtests passed; web checks, production build and deployed-site smoke passed. The CSV records source table rows 3, 4, 7 and 14–22; Note 9's `ឧ` remains unresolved. No IPA or Ukrainian result was added.


## Bounded PCGN open-CV assembly — 2026-11-16

A new `assemble_pcgn_open_syllable` adapter composes the existing source-located PCGN onset-consonant and ordinary dependent-vowel component resolvers for one explicitly supplied open CV syllable. The caller supplies both an onset-only chunk and the complete syllable chunk; the implementation verifies that the onset tokens are an exact prefix and that the remaining tokens are only a supported dependent-vowel pattern. It then applies the existing Note 2–3 series resolver and concatenates the two already-resolved PCGN Latin components.

This bounded addition does **not** discover syllable or word boundaries in running Khmer text, infer codas, process independent or shortened vowels, ROBAT/AHSDA/TOANDAKHIAT, or resolve the Alif carrier. Those inputs abstain. The result retains source text and component/table provenance and explicitly sets IPA and Ukrainian output to null: this is PCGN orthographic romanization, not a phonetic or Ukrainian transcription path. The existing IPA-first runtime remains separate and unchanged.

- API: `src/khmer_ua/pcgn.py::assemble_pcgn_open_syllable`.
- Contract: `schemas/pcgn-syllable-assembly.schema.json`; regression coverage: `tests/test_pcgn_syllable_assembly.py`.
- Primary source: BGN/PCGN 1972, Consonant Characters and Subscript Consonant Forms table (pp. 1–2), Note 3, and Independent/Dependent Vowel Characters table (pp. 2–3): https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.
- Status: `DONE_VERIFIED` for this bounded API. PR #264 merged as `231b8f031ae130828018b18dbdf1c36c6ac47e6a`; exact-head Quality [43880147090] and Chromium [43880147081] passed, with push Quality [43880136584] also passing. Quality reports 338 Python tests + 70 subtests; web checks and production build passed. `KHM-ROM-ENGINE-001` remains PARTIAL because no general syllable segmentation, coda assembly or whole-word romanizer is claimed.


## Bounded PCGN Note 5 closed-syllable assembly — 2026-11-16

A second bounded assembler, `assemble_pcgn_shortened_closed_syllable`, composes the existing onset, Note 5 shortened-vowel and final-consonant resolvers for the three exact PCGN Note 5 shapes: inherent+BANTOC, AA+BANTOC, and SAMYOK SANNYA+coda. The caller supplies onset-only, full-syllable and coda-only chunks plus the Note 5 coda class. The implementation checks exact token boundaries, requires one unmarked final consonant, and cross-checks the supplied coda class against its resolved PCGN romanization (`k`, `ng`, `h`, or `other`) before selecting the `eă`/`oă` branch.

Coda-bearing syllables outside those exact Note 5 shapes, unsupported final consonants (including BA and ALIF under the current final-consonant resolver), malformed chunks, inconsistent coda classes and all ambiguous structures abstain. This remains orthographic BGN/PCGN Latin output only; it does not infer word boundaries or generate IPA/Ukrainian output.

- API: `src/khmer_ua/pcgn.py::assemble_pcgn_shortened_closed_syllable`.
- Contract: `schemas/pcgn-closed-syllable-assembly.schema.json`; tests: `tests/test_pcgn_closed_syllable_assembly.py`.
- Primary source: BGN/PCGN 1972, Notes §5 and the shortened-vowel entries in the vowel table: https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.
- Status: `DONE_VERIFIED` for the bounded Note 5 API. PR #265 merged as `664c210d957b0666e5ca85032fb49466018cbf78`; exact PR-head Quality [43881403475] and Chromium [43881403279], push Quality [43881383045], and exact-main Quality [43881564395], Chromium [43881564314] and Pages [43881564668] all passed. General syllabification, other coda patterns and whole-word romanization remain incomplete.


## Bounded PCGN normal dependent-vowel closed-syllable assembly — 2026-11-16

The new `assemble_pcgn_dependent_closed_syllable` composes the existing Note 2–3 series, consonant-onset, normal dependent-vowel and final-consonant resolvers. The caller supplies four explicit chunks: onset-only, onset-plus-vowel, complete syllable, and coda-only. Exact token-prefix and final-token relationships are checked before the components are concatenated. The regression suite exercises all 17 normal dependent-vowel table patterns in both series against an explicit final consonant.

Only normal dependent-vowel forms and one unmarked final consonant are accepted. Independent/shortened vowels, special marks, Alif, unsupported codas, malformed chunks and mismatched caller boundaries abstain. This remains BGN/PCGN orthographic Latin output; no word segmentation, IPA or Ukrainian output is generated.

- API: `src/khmer_ua/pcgn.py::assemble_pcgn_dependent_closed_syllable`.
- Contract: `schemas/pcgn-dependent-closed-syllable-assembly.schema.json`; tests: `tests/test_pcgn_dependent_closed_syllable_assembly.py`.
- Primary source: BGN/PCGN 1972, consonant/subscript and dependent-vowel tables, pp. 1–3: https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.
- Status: `DONE_VERIFIED` for the bounded normal dependent closed-syllable API. PR #266 merged as `84880d6c241bfc22e8e095a7cb90f2d32759ced1`; exact PR-head Quality [43882269923] and Chromium [43882269991], plus push Quality [43882139617], passed (347 Python tests + 70 subtests). Exact-main Quality [43882558236], Chromium [43882558488] and Pages [43882558294] also passed on `8df4f5ca146f82d6f8c3892ae686f6f58f7bbaeb`. `KHM-ROM-ENGINE-001` remains PARTIAL pending general segmentation, broader coda patterns and whole-word output.


## Bounded PCGN Note 4 Alif open-syllable assembly — 2026-11-16

Added assemble_pcgn_glottal_open_syllable to compose the source-located Note 4 Alif carrier component with a normal dependent-vowel component for one caller-supplied open syllable. The caller supplies the standalone Alif onset chunk, complete syllable chunk, and explicit boolean word-initial/following-vowel context. Exact onset-token prefix and dependent-vowel-only tail checks are required. The existing Note 4 optional-apostrophe condition is retained as two output alternatives when applicable; neither alternative is silently discarded.

- API: src/khmer_ua/pcgn.py::assemble_pcgn_glottal_open_syllable.
- Contract: schemas/pcgn-glottal-open-syllable-assembly.schema.json; tests: tests/test_pcgn_glottal_open_syllable_assembly.py.
- Primary source: BGN/PCGN 1972, Consonant Characters row 22 and Note 4 (p. 5), plus Independent/Dependent Vowel Characters table (pp. 2–3): https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.
- Boundary: orthographic PCGN Latin only. IPA and Ukrainian remain null; no word segmentation, coda handling or phonetic transcription is generated.
- Status: DONE_VERIFIED for this bounded API. PR #267 merged as 6df8c6c176e0098f97a9f4ab1f9583b0bb7caa68. PR-head Quality [43888596780] and Chromium [43888596962] passed (354 Python tests + 70 subtests); exact-main Quality [43888801455], Chromium [43888801448], and Pages [43888801373] all passed, including deployed-site/runtime smoke. KHM-ROM-ENGINE-001 remains PARTIAL.


## Bounded PCGN Note 4 Alif dependent-vowel closed-syllable assembly — 2026-11-16

Added assemble_pcgn_glottal_dependent_closed_syllable to compose the Note 4 Alif carrier, normal A-series dependent-vowel and general final-consonant components for one caller-supplied closed syllable. Caller supplies onset-only, onset-plus-vowel, full-syllable and coda-only chunks, as well as explicit boolean Note 4 word-position/following-vowel context. Exact token boundaries and source-component identity are checked. Only one unmarked final consonant supported by the existing generic final resolver is accepted; special/unsupported coda contexts abstain. Optional apostrophe spelling remains an explicit full-output alternative when Note 4 allows it.

- API: src/khmer_ua/pcgn.py::assemble_pcgn_glottal_dependent_closed_syllable.
- Contract: schemas/pcgn-glottal-dependent-closed-syllable-assembly.schema.json; tests: tests/test_pcgn_glottal_dependent_closed_syllable_assembly.py.
- Primary source: BGN/PCGN 1972, Consonant Characters row 22 and Note 4 (p. 5), Independent/Dependent Vowel Characters table (pp. 2–3), and final-consonant no-following-vowel rule (p. 2): https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.
- Boundary: orthographic PCGN Latin only. IPA/Ukrainian remain null; no word segmentation or coda inference is generated.
- Status: DONE_VERIFIED for this bounded API. PR #269 merged as 482ed151dc99d3fd20714a606c9ad25aa209a99e. PR-head Quality [43889912149] and Chromium [43889912018] passed (360 Python tests + 70 subtests); exact-main Quality [43890093477], Chromium [43890093456], and Pages [43890093482] all passed, including deployed-site/runtime smoke. KHM-ROM-ENGINE-001 remains PARTIAL.


## Bounded PCGN Note 4 + Note 5 Alif shortened closed-syllable assembly — 2026-11-16

Added assemble_pcgn_glottal_shortened_closed_syllable for the three exact Note 5 shortened closed-syllable patterns with the Note 4 Alif carrier: inherent+BANTOC, AA+BANTOC and SAMYOK+coda. Caller supplies the Alif onset, complete syllable, one-consonant coda, explicit coda class and Note 4 context flags. The adapter cross-checks the coda token and its resolved PCGN Latin value against the supplied class. Optional apostrophe spelling is preserved as an explicit alternative. Unsupported coda contexts and all other shapes abstain.

- API: src/khmer_ua/pcgn.py::assemble_pcgn_glottal_shortened_closed_syllable.
- Contract: schemas/pcgn-glottal-shortened-closed-syllable-assembly.schema.json; tests: tests/test_pcgn_glottal_shortened_closed_syllable_assembly.py.
- Primary source: BGN/PCGN 1972, Consonant Characters row 22 and Note 4 (p. 5), shortened-vowel table rows 1–2 and Note 5, and final-consonant no-following-vowel rule (p. 2): https://assets.publishing.service.gov.uk/media/5ab4e25aed915d78bc23451e/ROMANIZATION_OF_KHMER.pdf.
- Boundary: orthographic PCGN Latin only. IPA/Ukrainian remain null; no word segmentation or coda inference is generated.
- Status: DONE_VERIFIED for the three exact Note 5 patterns with one supported coda and explicit Note 4 context. PR #271 merged as 9957081db4149ff316695273d8dd525985bd34fd. PR-head Quality [43891125460] and Chromium [43891125490] passed (368 Python tests + 70 subtests); exact-main Quality [43891297907], Chromium [43891298013], and Pages [43891297884] all passed, including deployed-site/runtime smoke. KHM-ROM-ENGINE-001 remains PARTIAL.
