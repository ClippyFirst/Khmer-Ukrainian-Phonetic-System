# Khmer vowel × consonant-series × coda evidence matrix — 2026-11-01

**Profiles:** modern Standard Khmer is not treated as a single self-evident spoken variety. Phnom Penh acoustic evidence and specialist orthographic mapping are separate evidence layers. This is not an adjudicated lexical corpus.

## 1. Orthographic class and inherent-vowel matrix

Richard Ishida's specialist Khmer Orthography Notes (updated 27 April 2026) describe two consonant classes, ɑ-class and ɔ-class. Khmer is non-tonal; class determines vowel-sign selection, while stress, vowel harmony and register-shifter diacritics may also affect output.

| Orthographic input | ɑ-class output | ɔ-class output | Evidence / qualification |
|---|---|---|---|
| Inherent vowel | /ɑː/ | /ɔː/ | Ishida: ក /kɑː/ vs គ /kɔː/ |
| Base consonant + U+17B8 ី | /əj/ | /iː/ | Explicit Ishida class-comparison example |
| Base consonant + U+17B6 ា | /aː/ | /iə/ | Explicit Ishida class-comparison example |
| U+17B7 ិ | /e/ or /ə/ in specified a-class contexts | /i/; stressed syllables may show following glottal closure | Ishida plain-vowel mappings; context-sensitive |
| U+17B9 ឹ | /ə/ | /ɨ/ | Ishida plain-vowel mappings |
| U+17BA ឺ | /əɨ/ | /ɨː/ | Ishida plain-vowel and rhyme mappings |
| U+17C2 ែ | /ae/ | /ɛː/ | Ishida vowel mappings |
| U+17BC ូ | /ou/ | /uː/ | Ishida vowel mappings |
| U+17C4 ោ | /ao/ | /oː/ | Ishida vowel mappings |
| U+17D0 ័ | /a/ in listed a-class environment | coda-conditioned outcomes include /ɨj/ or /oə̆/ in listed o-class environments | Ishida diphthong/rhyme mappings; not one sign/one sound |

Reference: Richard Ishida, [Khmer Orthography Notes](https://r12a.github.io/scripts/khmr/km.html), sections “Consonant registers,” “Post-consonant vowels,” “Diphthongs and rhymes,” “Vowel length,” and “Codas.” The page explicitly identifies stress, vowel harmony and register shifters as additional factors.

## 2. Phnom Penh acoustic vowel inventory: source-reported, not gold

Chem Vatho (2020), “The Standard Khmer vowel system: An acoustic study,” Insight: Cambodia Journal of Basic and Applied Research 2(2), 93–121, [full text PDF](https://www.cjbar.rupp.edu.kh/index.php/cjbar/article/download/36/32), supplies a bounded acoustic dataset.

| Dimension | Reported result | Locator | Limitation |
|---|---|---|---|
| Monophthongs | 21 source-reported categories: 10 long and 11 short | pp. 103–109 | Lexical gaps; some categories omitted from sample |
| Diphthongs | 13 source-reported categories: 10 long and 3 short | pp. 98–105, 110–112 | Earlier analyses differ; retain author's transcription convention |
| Speaker selection | 21 native speakers screened; four selected for acoustic analysis (two female), ages 20–50 | pp. 104–105 | Four-speaker Phnom Penh sample |
| Lexical materials | 168 items in initial screening; final analysis used 61 items, three formal-reading repetitions | pp. 104–105 | Not all phonological contrasts/codas covered |
| Series/register | First-register vowels reported lower/more open and more diphthongized than second-register vowels | abstract and pp. 96–101 | Historical breathy/modal labels are not automatically current phonation |
| Coda effect | Final consonants may modify vowel quality and length; closed syllables generally shorter | pp. 108–112 | No complete coda × series × vowel × length cross-table |
| Short diphthongs | Reported especially in closed contexts such as /-h, -k, -ʔ/ | pp. 110–111 | Source-reported sample, not exhaustive legality rule |

The paper states that “Standard Khmer” has no clear-cut definition and distinguishes Standard Khmer from Phnom Penh speech (pp. 93–96). It reports an acoustic inventory, not a complete lexeme-by-lexeme series × coda matrix. Its IPA-like symbols are the authors' transcription, not project gold.

## 3. Coda inventory and nucleus interaction

| Coda/environment | Evidence-supported statement | State |
|---|---|---|
| Final oral stops /p,t,k/ | Common codas; final realization differs from onset and has no following inherent vowel | SOURCE_REPORTED |
| Final nasals /m,n,ɲ,ŋ/ | Common coda classes; exact preceding-vowel effects need lexical/acoustic rows | SOURCE_REPORTED / PARTIAL |
| Final lateral /l/ | Included among common coda consonants in Ishida's summary | SOURCE_REPORTED |
| U+17C6 ំ | Represents final /-m/ and affects the vowel nucleus | SOURCE_REPORTED |
| U+17C7 ះ | Represents final /-h/ and affects the vowel nucleus | SOURCE_REPORTED |
| U+17CB ់ | Shortens the preceding vowel in the described use | SOURCE_REPORTED |
| Short diphthongs before /-h,-k,-ʔ/ | Reported in Chem's Phnom Penh sample | ACOUSTIC_SAMPLE |
| Every coda × every series × every vowel | No exhaustive source-backed cross-product located | NOT_ESTABLISHED |

Unicode and Ishida describe orthographic representation and mapping logic; Chem supplies a small acoustic sample. Neither source licenses extrapolating all outcomes to every final consonant.

## 4. /r/-loss is a separate profile/style matrix

Wayland & Guion (2005), Mon-Khmer Studies 35:55–82, [full paper](https://rilca.mahidol.ac.th/documents/PublicationMultimedia/MonKhmer/Vol35/wayland2005sound.pdf), compare 20 obstruent+/r/ lexical items from two male Phnom Penh speakers, three repetitions per item in careful-reading and colloquial styles. They report /r/ loss in colloquial tokens, onset aspiration, falling–rising F0 and vowel changes. This supports a conditioned Phnom Penh colloquial pathway, not universal deletion.

Kirby (2014), [Journal of Phonetics DOI](https://doi.org/10.1016/j.wocn.2014.02.001), adds production/perception evidence involving f0, aspiration/VOT, voice quality and vowel quality. Keep cues separate.

## 5. Required future row fields

| Field | Meaning |
|---|---|
| profile | Standard/Phnom Penh/other named variety |
| base_consonant_class | ɑ-class or ɔ-class, including shifter state |
| vowel_sign_sequence | Exact normalized Unicode sequence |
| stress | stressed / unstressed / unknown |
| harmony_context | preceding/following syllable class and trigger |
| nucleus_phonemic | source-backed phonemic value |
| nucleus_phonetic | measured/transcribed surface realization |
| length | short/long and measurement where available |
| coda | phonological coda, distinct from written final grapheme |
| source_locator | page/table/word/audio ID |
| evidence_status | SOURCE_REPORTED, ACOUSTIC_SAMPLE, CONFLICTING, NOT_ESTABLISHED, ADJUDICATED_GOLD |

**Status:** PARTIAL. A class-to-vowel mapping baseline and bounded Phnom Penh acoustic inventory are available. Full contextual cross-table, multi-speaker lexical evidence and independently adjudicated IPA remain outstanding. No gold labels or unverified engine rules were added.


## 6. Dialect-sensitive contrast probes from Chem (2020)

The article provides concrete examples showing why a Phnom Penh matrix cannot be silently generalized to Standard Khmer:

| Contrast | Standard Khmer analysis reported by Chem | Phnom Penh realization reported | Consequence |
|---|---|---|---|
| /tiɜ/ vs /tiət/ | Two vowel distinctions are maintained | One /tiɜ/ realization in the studied PP variety | Profile-specific diphthong/rime mapping |
| /eː/ vs /ɛe/ | Distinct in the Standard Khmer analysis | No distinction in the studied PP variety; both realized /eː/ | Do not reuse PP output for every Standard Khmer lexical item |
| /i/ | Primarily Sanskrit/Pali loan vocabulary in the author's account | Omitted from the acoustic sample because reliable sample words were unavailable | Mark the cell as source-discussed but not acoustically sampled |

The paper also notes that the 61-item sample did not cover every nucleus/context and that some vowel samples were substituted from other words or sentences where lexical familiarity caused gaps (pp. 104–106). These limitations are material to any future training split or gold selection.


## 7. Chem (2020) source-transcribed inventory (verbatim notation)

The article's conclusion lists the following 21 monophthong categories and 13 diphthong categories (pp. 114–115). These are retained in the author's transcription, not normalized to a project IPA convention:

- **Monophthongs (21):** /iː, i, ɨː, ɨ̆, uː, ŭ, eː, e, ɛː, ɛ, aː, a, ɘː, ɘ, oː, o, ɔː, ɔ, ɒː, ɒ, ɜ/.
- **Diphthongs (13):** /iɜ, ɨɜ, uɜ, aɛ, aɜ, aɔ, oa, ɛe, oʊ, ɜɘ, ĭɜ, ŭɜ, ɛ̆a/.

The author classifies 10 long and 11 short monophthongs, and 10 long and 3 short diphthongs. The article also notes that /i/ is primarily associated with Sanskrit/Pali loan vocabulary and was not represented in the acoustic sample. This inventory is therefore SOURCE_REPORTED, while the actual acoustic sample coverage is narrower. It must not be copied into gold.tsv or treated as a universal Standard Khmer inventory without expert reconciliation.


## 8. Expanded Ishida phone-to-grapheme reference table

The following is a structured extraction of Ishida's “Vowel sounds mapped to characters” table (sections “Plain vowels” and “Diphthongs and rhymes,” source lines 501–945). IPA-like values are copied as Ishida's transcription; Unicode code points identify the written sequence. The table is a reference mapping, not a claim that every row is phonemic or acoustically validated in every dialect.

| Ishida transcription | Class | Grapheme sequence / context |
|---|---|---|
| /i/ | ɔ-class | U+17B7; followed by glottal stop in stressed syllables, not unstressed |
| /iː/ | ɔ-class | U+17B8 |
| /ɨ/ | ɔ-class | U+17B9; also independent-vowel forms; 17B9 has a before-1799 exception |
| /ɨː/ | ɔ-class | U+17BA |
| /u/ | ɔ-class | U+17BB; stressed syllables may have following glottal stop |
| /uː/ | ɔ-class | U+17BC |
| /e/ | ɑ-class | U+17B7; stressed syllables may have following glottal stop |
| /eː/ | ɔ-class | U+17C1; stressed syllables may have following glottal stop |
| /o/ | ɑ-class | U+17BB; stressed syllables may have following glottal stop |
| /oː/ | ɔ-class | U+17C4; stressed syllables may have following glottal stop |
| /ə/ | ɑ-class | U+17B7; U+17B9; U+17C1 before palatals |
| /əː/ | ɑ-class | U+17BE |
| /ɛː/ | ɔ-class | U+17C2 |
| /ɔː/ | ɔ-class | inherent vowel |
| /a/ | ɑ-class | U+17D0; or U+17B6 + U+25CC + U+17CB |
| /aː/ | ɑ-class | U+17B6 |
| /ɑ/ | ɑ-class | U+17CB after an inherent a-series vowel |
| /ɑː/ | ɑ-class | inherent vowel |
| /iə/ | ɔ-class; also both classes | U+17B6; or U+17C0 in a/ɔ-class environments |
| /ih/ | ɔ-class | U+17B7 + U+17C7; or U+17C1 + U+17C7 |
| /ɨə/ | both classes | U+17BF |
| /ɨj/ | ɔ-class | U+17D0 + U+1799; or U+17C3 |
| /ɨw/ | ɔ-class | U+17BC + U+179C; or U+17C5 |
| /uə/ | both classes | U+17BD |
| /uə̆/ | ɔ-class | U+17CB after inherent series-2 vowel, before a non-labial final |
| /uə̆h/ | ɔ-class | U+17C4 + U+17C7 |
| /uh/ | ɔ-class | U+17BB + U+17C7 |
| /um/ | ɔ-class | U+17BB + U+17C6; or U+17C6 |
| /ei/ | ɑ-class | U+17C1 |
| /eə̆/ | ɔ-class | U+17D0 before velar finals; or U+17B6 + U+25CC + U+17CB before velar finals |
| /eə̆ʔ/ | ɔ-class | U+17C0 |
| /eh/ | ɑ-class | U+17B7 + U+17C7; U+17C1 + U+17C7; or U+17C2 + U+17C7 |
| /eə̆h/ | ɔ-class | U+17C7 |
| /eə̆ŋ/ | ɔ-class | U+17B6 + U+17C6 + U+1784 |
| /ou/ | ɑ-class | U+17BC |
| /oə̆/ | ɔ-class | U+17D0 before non-velar finals; or U+17B6 + U+25CC + U+17CB before non-velar finals |
| /oə̆m/ | ɔ-class | U+17B6 + U+17C6 before non-velar finals |
| /oh/ | ɑ-class | U+17BB + U+17C7 |
| /om/ | ɑ-class | U+17BB + U+17C6 |
| /əɨ/ | ɑ-class | U+17BA |
| /əj/ | ɑ-class; also ɔ-class | U+17B8; or U+17B7 + U+1799; standalone U+17A5/U+17A6 |
| /əw/ | ɑ-class | U+17BC + U+179C; standalone U+17AA |
| /əh/ | ɑ-class | U+17B9 + U+17C7; or U+17BE + U+17C7 |
| /ɔə/ | ɔ-class | U+17D0 + U+179A |
| /ae/ | ɑ-class | U+17C2; standalone U+17AF |
| /aə/ | ɑ-class | U+17BE |
| /ao/ | ɑ-class | U+17C4; standalone U+17A7/U+17B1/U+17B2 |
| /aj/ | ɑ-class | U+17D0 + U+1799; U+17C3; standalone U+17B0 |
| /aw/ | ɑ-class | U+17C5; standalone U+17B3 |
| /aʔ/ | ɑ-class | U+17C0 |
| /ah/ | ɑ-class | U+17C4 + U+17C7; or U+17C7 |
| /am/ | ɑ-class | U+17B6 + U+17C6; or U+17C6 |
| /ɑm/ | ɑ-class | U+17C6 |
| /ɑŋ/ | ɑ-class | U+17B6 + U+17C6 + U+1784 |

### Interpretation rules and unresolved cells

- Stress is part of the mapping: Ishida explicitly notes following glottal closure for some vowels in stressed syllables but not unstressed syllables.
- Coda-conditioned sequences are not interchangeable: the table distinguishes velar vs non-velar finals, labial vs non-labial finals, and U+17C6 /m/ vs U+17C7 /h/.
- Vowel harmony and register-shifter state can change the expected series; conjunct stacks may cause the following vowel to be determined by the subscript consonant, with listed exceptions.
- The table is a specialist orthographic mapping. Chem's four-speaker Phnom Penh acoustic sample remains a separate evidence layer. No row is promoted to project gold or a deterministic engine rule until the lexical item, profile, coda, stress and source/audio evidence are independently adjudicated.

## 9. Phonotactic scope and prohibited-structure classification

The following claims must remain in separate evidence classes:

| Structure claim | Classification | Evidence | What must not be inferred |
|---|---|---|---|
| Major syllables have no coda clusters | Candidate phonological restriction | Nacaskul (1978), pp. 187–188 | Does not imply all written coeng sequences are onset clusters or that chained codas are absent |
| Short nuclei do not occur in open major syllables | Major-syllable distribution | Nacaskul (1978), pp. 185, 188–189 | Does not automatically apply to minor types or all contemporary profiles |
| Minor A: /r/ only in second cluster position; short /ə, ɔ/; no coda | Minor-type restriction | Nacaskul (1978), pp. 187–189 | Not a global ban on /r/ clusters or short vowels |
| Minor B: single onset; restricted short nucleus; nasal coda | Minor-type restriction | Nacaskul (1978), pp. 187–190 | Not a global coda inventory |
| Up to two coengs before the vowel | Orthographic encoding limit | Unicode L2/22-290, pp. 9–10 | Not a phonological maximum of two onset consonants |
| Coeng chaining can make orthographic units diverge from phonetic syllables | Orthographic/phonetic segmentation distinction | Unicode L2/22-290, pp. 9–10; Ding et al. (2018), pp. 181–183 | Do not treat each Unicode/visual unit as one phonetic syllable |
| PPK low-F0 group includes /r>h/ forms and voiced-onset disyllables | Profile-specific prosodic evidence | Mam et al. (2025), five speakers, 50 words | Not a universal Khmer tone rule and not evidence for a grapheme-to-tone mapping |

The Nacaskul restrictions are historical source reports, not yet independently confirmed for every current Phnom Penh careful-citation environment. The Sak-Humphry 2025 publisher preview is not used to settle codas because its excerpt contradicts itself about /r/. No new vowel/coda matrix cell is promoted to adjudicated gold.


## 10. Machine-checked evidence-register contract — 2026-11-20

The canonical source-indexed example register is `data/khmer/vowel-context-register.json`. Its structural contract is now defined in `schemas/khmer-vowel-context-register.schema.json` and exercised by `tests/test_khmer_vowel_context_schema.py`.

The test checks both schema conformance and cross-record invariants:

- each case ID is unique;
- each `ipa_source` and any explicit alternative source resolves to `sources`;
- `evidence_level` and `status` agree;
- no case is labelled `ADJUDICATED_GOLD`;
- conflicting source analyses keep `ipa` and Ukrainian adaptation null and retain `ukrainian_status = NOT_ESTABLISHED`.

This is a data-integrity gate only. It does not validate the correctness of a source transcription, infer missing vowel values, or promote any source-attested example to a runtime rule. The generated coverage report remains the narrower dependent-sign × consonant-series inventory. The full contextual matrix still needs independently source-located lexical rows for series × vowel sequence × coda × syllable type × length × stress/harmony/profile, specialist review, and eventually independent adjudication.


## 11. Exact-head schema verification — 2026-11-20

The contextual evidence-register schema and tests passed on PR head `45fc31321d3628aa5afb61892802a8f9f20b3eb1`:

- Quality [44721843510](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44721843510): SUCCESS — 446 Python tests + 70 subtests, web checks and production build.
- Chromium [44721843530](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44721843530): SUCCESS.

This closes the schema/integrity subtask only. The report still covers dependent vowel sign × consonant series, not the full contextual matrix. No source evidence, IPA value, lexical label or gold item was added. The canonical completion register records `KHMER-VOWEL-REGISTRY-SCHEMA-001 = DONE_VERIFIED`; the broader contextual matrix remains PARTIAL.


## 9. Machine-readable case-level contextual evidence — 2026-11-20

The generated `reports/khmer-coverage-audit.json` and byte-identical public report now include `contextual_vowel_evidence`, built directly from `data/khmer/vowel-context-register.json`. This adds a case-level view of exact dependent-vowel sequences, base consonant class, subscripts, register-shifter marker, orthographic coda marker, source transcription, source ID/role and explicit length marks.

This extension deliberately does **not** claim to complete the requested cross-product. Current registry rows do not consistently identify spoken profile, phonological syllable type, phonological coda identity, measured vowel duration, stress or harmony context. These remain explicit gaps. An absent IPA length mark is not interpreted as short; an orthographic final sign is not silently converted into a phonological coda; source transcription conventions are preserved verbatim. Conflicting source cases remain null at the single-value IPA field.

The report's `cross_product_assessment.status` is therefore `NOT_ESTABLISHED`. The next data-collection acceptance criterion is to add source-located rows only where the source directly records the relevant context, with source convention/profile and locator preserved. Do not populate cells by analogy. Tests assert these no-inference boundaries and generated-artifact parity.

## Latest mainline verification — 2026-11-20

The source-backed case inventory and dashboard remain integrated. Exact main HEAD `e5ea08e9bc0c9828b5da29cbd6ecb06d6e054ee0` passed Quality [44734864422](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44734864422), browser smoke [44734864454](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44734864454), and Pages/deploy [44734864513](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44734864513). These checks validate engineering reproducibility and deployment, not phonological completeness or transcription accuracy.


## Contextual vowel research continuation — 2026-11-21

See docs/research/KHMER-CONTEXTUAL-VOWEL-AND-LEXICAL-SEGMENTATION-RESEARCH-UPDATE-2026-11-21.md. Chem's Phnom Penh acoustic sample, Minegishi's series/coda analysis, Kirby's cluster and laryngeal work, Mam et al.'s bounded five-speaker/50-word pitch study, Woźnica's geographically uneven 80-speaker sample, and Henderson's non-Phnom-Penh speaker are distinct evidence strata. They must not be collapsed into a single complete vowel inventory or a grapheme-to-tone rule. The contextual matrix remains PARTIAL until source-located lexical rows include profile, task, syllable type, coda, length, stress/harmony and acoustic context. No new IPA or runtime rule is added by this continuation.

## Tier-B source-locator gate — 2026-11-21

The runtime no longer treats any non-empty `evidence` array as sufficient for tier B. B requires a per-unit exact source locator, a registered pronunciation-capable source ID, successful IPA → Ukrainian adaptation and lexical-target agreement when a lexical Ukrainian reference is supplied. Current B units are `ក`, `គ`, `ខ្មែរ`, `ភាសា`, `ភ្នំពេញ`, `កម្ពុជា`, and `ខ្ញុំ`. The phrase `ភាសាខ្មែរ` remains a compositional hypothesis at C; `ឆ` remains C because the R12A page conflicts on its register class. This does not close the wider contextual vowel × series × coda matrix, which remains PARTIAL.

## Post-merge final verification — 2026-11-21

- **DONE_VERIFIED (main):** final runtime/evidence-gate commit `7c47d56b91d132a1ce1c26e8f46e23372a6f5cd2`, following merged PR #498 (exact registered source-locator gate) and PR #499 (Wiktionary historical-IPA and rights caveat correction).
- **DONE_VERIFIED (Quality):** main run `44936590289` SUCCESS — 448 Python tests + 70 subtests, including independent IPA gold-corpus structure validation, source-locator tier tests, Node web checks and site build.
- **DONE_VERIFIED (browser):** main Chromium run `44936590230` SUCCESS — 23 browser tests, including B-tier locator visibility and C-tier phrase/conflict cases.
- **DONE_VERIFIED (deployment):** Pages run `44936590276` SUCCESS — production build, Chromium exercise, GitHub Pages deploy and deployed runtime asset smoke test all passed. Public beta: https://clippyfirst.github.io/Khmer-Ukrainian-Phonetic-System-/
- **DONE_VERIFIED (diagnostic only):** optional Phonemizer run `44936590367` SUCCESS — 6/6 outputs, 0 failed outputs, 2 strict source-string matches and 6 limited-notation-normalized matches. Independent gold count is 0 and accuracy is null; do not describe these counts as accuracy.
- **Current evidence boundary:** B applies to `ក`, `គ`, `ខ្មែរ`, `ភាសា`, `ភ្នំពេញ`, `កម្ពុជា`, and `ខ្ញុំ`, with exact source locators and adapter/lexical-reference agreement. `ភាសាខ្មែរ` remains C (compositional phrase without phrase-level source); `ឆ` remains C (R12A internal register-list conflict). No A-tier units or independent gold rows exist.
- **Remaining:** contextual vowel-series × coda coverage, lexical segmentation, independent Phnom Penh IPA convention/adjudication, and independent gold remain PARTIAL/DEFERRED. Accuracy is NOT_ASSESSED.


## 12. Contextual phonology evidence update — 2026-11-24

This section consolidates the current public-source and full-text review into context dimensions. It deliberately does not turn every finding into a runtime G2P rule. The corresponding machine-readable entries are in `data/khmer/vowel-context-register.json` under `context_dimensions` (PPH-CTX-001–009), validated by the schema and tests.

| Dimension | Evidence and exact scope | Evidence status | Runtime consequence |
|---|---|---|---|
| Consonant class/register × vowel sign | Ishida gives four explicit open-syllable examples: ក /kɑː/, គ /kɔː/, កី /kəj/, គី /kiː/, កា /kaː/, គា /kiə/ (Khmer Orthography Notes, §§Consonant registers/Inherent vowels, lines 235–266). Register shifters are separately described. | SOURCE_ATTESTED_NOT_GOLD; specialist synthesis, not a balanced PP acoustic experiment | Retain exact example fixtures and their source locators. No universal sign×series table is inferred from four examples. |
| Cross-syllable vowel harmony | In two-syllable words, second syllables beginning with ង ញ ណ ន ម យ ឡ ល រ វ may take the first syllable's vowel class; exceptions are explicitly noted (Ishida, §Vowel harmony, lines 247–257). | SOURCE_REPORTED_WITH_EXCEPTIONS | Harmony must be lexical/contextual. Do not permanently rewrite the underlying consonant class or treat the list as exception-free. |
| Stress and weak syllables | Ishida's mapping legend states that several vowels are followed by glottal closure in stressed syllables but not unstressed (lines 491–496 and individual entries 503–615). Many bisyllables have an unstressed first syllable realized as schwa in colloquial speech, but compounds may differ (§Phonetic syllables, lines 201–209). Chem's PP experiment deliberately placed words in a frame to reduce sentence-stress effects, but reports unnatural word stress and lexical gaps (2020, pp. 104–106). | SOURCE_REPORTED_NOT_EXPERIMENTALLY_VERIFIED for the broad rule; bounded PP method evidence | Stress and lexical/prosodic structure are required inputs for a surface-phonetic layer. Do not inject schwa or glottal closure from spelling alone. |
| Coda marks and coda place | U+17C6 / U+17C7 represent /-m/ and /-h/ and affect the nucleus; U+17CB shortens the preceding vowel (Ishida, §§Nikahit and reahmuk, lines 325–347). Some ɔ-class U+17D0 rhymes are explicitly split by velar vs non-velar finals (/eə̆/ vs /oə̆/, lines 777–826). | SOURCE_REPORTED_CONTEXT_DEPENDENT | Nucleus and coda must be analyzed jointly; these examples justify explicit context fields, not a complete coda×vowel cross-product. |
| Open vs closed syllable / duration | Chem (2020) reports 21 speakers screened, then four selected Phnom Penh speakers (two female), 61 lexical items, three formal-reading repetitions (pp. 104–105). Closed syllables are usually shorter; coda can modify vowel quality/length; short diphthongs are reported in closed /-h, -k, -ʔ/ contexts (pp. 108–112). | BOUNDED_ACOUSTIC_SAMPLE | Treat closure as a material conditioning factor. Do not create coda-specific deterministic outputs without item-level matched evidence. |
| Profile-specific vowel mergers | Chem reports Standard Khmer /tiɜ/ vs /tiət/ but a single /tiɜ/ in the sampled PP variety; likewise /eː/ vs /ɛe/ are reported merged as /eː/ in PP (2020, pp. 98–100, 114–115). The paper stresses that “Standard Khmer” is not sharply defined and PP speech varies. | BOUNDED_PROFILE_SPECIFIC_REPORT | Keep these as profile-specific lexical probes, not global phoneme mergers. |
| Colloquial /r/-loss and vowel cues | Wayland & Guion (2005) compare careful and colloquial speech for 20 obstruent+/r/ items from two male PP speakers, three repetitions per item/style. Their sampled colloquial forms show /r/-loss, aspiration, F0 and vowel changes (Mon-Khmer Studies 35, pp. 55–82; DOI 10.15144/MKSJ-35.55). | BOUNDED_STYLE_SPECIFIC_ACOUSTIC_SAMPLE | A colloquial profile must be separate and conditioned. Never delete every written/underlying /r/ or transfer these outcomes into careful citation speech. |
| Pitch and syllable structure | Mam, Pittayaporn & Maspong (2025) use 50 words, five native speakers (2M/3F, ages 20–25), three repetitions in PPK and SK. F0 is measured on the stressed rime. PPK shows a lower group for r>h onsets and voiced-onset disyllables; authors interpret the separation as possible phonologized high/low pitch (pp. 139–143, §§2–4; DOI 10.21437/TAI-2025-29). | RECENT_BOUNDED_PROSODIC_EVIDENCE | Keep F0/pitch in a separate prosodic profile layer. The study does not measure vowel formants or voice quality and does not license a general grapheme-to-tone rule. |
| Orthographic vs phonetic syllable/coda parse | Unicode L2/22-290 (§§Orthographic Syllable Structure/Coengs, pp. 9–10) describes coeng as onset cluster or syllable chaining; Ishida documents unmarked vowel absence and ambiguous parses (lines 1095–1115). | ORTHOGRAPHIC_STRUCTURE_ESTABLISHED_PHONETIC_PARSE_CONTEXTUAL | Resolve lexical segmentation and coda role before vowel realization. Ambiguous parses remain unresolved. |

### Source quality and conflict controls

- **Chem (2020) is useful but bounded.** Its abstract itself says Standard Khmer is not sharply defined (pp. 93–96); the four-speaker acoustic sample is small and selected, and the authors note unnatural stress, lexical familiarity gaps and substituted samples (pp. 104–106). Some reported duration values/units are internally inconsistent (pp. 111–115). We therefore use its reported context effects and dialect probes as source evidence, not gold labels or calibrated duration thresholds.
- **Do not collapse register, phonation and tone.** Ishida describes the consonant-class mechanism as vowel selection, not tone (lines 235–246). Chem reports first-register vowels as lower/more open and more diphthongized in its PP sample (pp. 114–115), but this is not an automatic instruction to add breathy-voice diacritics. Mam (2025) specifically measures F0 and finds pitch grouping; it does not measure vowel formants or voice quality.
- **Do not collapse PPK and Standard Khmer.** Chem's reported PP mergers are sample- and profile-specific. Wayland & Guion and Mam address colloquial PPK effects, while the engine's current selected profile is careful citation speech. A future colloquial profile must be versioned separately.
- **Do not transfer An Giang or Western Khmer rules.** The An Giang 2026 comparison and Western Khmer register studies are separate dialect evidence; they do not fill PPK cells.
- **IPA convention remains a separate decision.** Preserve source notation verbatim in evidence records. A source's /ɜ/, [ə], /iɜ/ or pitch notation must not be silently normalized into project phonemic IPA without a declared convention and profile.

### Ranked next engineering/research actions

1. Extend the existing source-indexed registry with exact lexical rows for the contexts already described above (especially 17C6/17C7/17CB, series-2 17D0 before velar vs non-velar codas, and stress-conditioned glottal closure). Keep IPA null where the source gives only a rule description without a specific word/token.
2. Add positive and negative runtime tests for structure/context detection (coda identity, syllable type, stress unknown, harmony trigger/exception, careful vs colloquial profile) without enabling unsupported IPA output.
3. Only promote a context rule after at least one exact lexical source locator plus independent profile review; a single descriptive table is not enough for a universal rule.
4. Keep PPK F0/pitch as an explicit optional phonetic/prosodic annotation dimension. Before deterministic tonal output, require perception evidence and broader speaker/lexical coverage.
5. Build a future matched PP corpus across vowel × series × coda × syllable type × stress/style; record speaker metadata, token counts, raw audio locators and both phonemic and narrow phonetic transcription.

**Current status:** the contextual matrix is now more explicit and source-indexed (nine dimensions), but remains **PARTIAL**. This update improves evidence coverage and testability; it does not add any new deterministic vowel/coda/tone rule to the runtime, does not alter Ukrainian adaptation, and does not establish corpus-wide accuracy.
