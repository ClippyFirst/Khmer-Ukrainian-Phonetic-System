# Khmer phonology research workpack

**Scope:** Standard Khmer with a separately versioned Phnom Penh colloquial profile. Do not collapse careful Standard Khmer and colloquial Phnom Penh speech into one pronunciation rule.

## Evidence already located

1. Ratree P. Wayland & Susan G. Guion (2005), “Sound changes following the loss of /r/ in Khmer: a new tonogenetic mechanism?”, *Mon-Khmer Studies* 35, 55–82. [Full paper](https://rilca.mahidol.ac.th/documents/PublicationMultimedia/MonKhmer/Vol35/wayland2005sound.pdf), DOI [10.15144/MKSJ-35.55](https://doi.org/10.15144/MKSJ-35.55). The acoustic study compares colloquial and careful-reading C₁rVC(V)C forms and reports /r/ loss, onset aspiration, diphthongization of short/long front [a] to [ea], and falling-rising pitch in its Phnom Penh colloquial data. The authors explicitly describe two speakers; do not generalize their sample to all speakers or all contexts.
2. James P. Kirby (2014), “Incipient tonogenesis in Phnom Penh Khmer: Acoustic and perceptual studies,” *Journal of Phonetics* 43, 69–85, DOI [10.1016/j.wocn.2014.02.001](https://doi.org/10.1016/j.wocn.2014.02.001). [Publisher record](https://www.sciencedirect.com/science/article/pii/S0095447014000163). Reports multiple cues associated with colloquial /r/-loss: f0, aspiration/VOT, breathy voice and vowel-quality change; the study includes production and perception evidence.
3. [Standard Khmer Vowel System: An Acoustic Study](https://zenodo.org/records/3377387) reports register-related vowel differences and Phnom Penh acoustic variation. Treat its inventory and measurements as a source to inspect and reconcile, not as an automatically accepted canonical table.
4. Unicode 17 Chapter 16 documents the orthographic consonant series and Khmer script ordering; it does not establish phonetic realization. [Unicode chapter](https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-16/).

## Required research matrix

| Workstream | Required matrix | Acceptance evidence |
|---|---|---|
| Vowels | Dependent sign × consonant series × short/long × coda × syllable type × pronunciation profile | Exact source/recording locator per cell; phonemic and phonetic values separated |
| Series/register | Onset series × inherent vowel × dependent vowel × context | Reconcile traditional A/O series labels with phonological register analysis; record historical vs synchronic claims |
| Codas | Final grapheme/cluster × phonological coda × surface realization × preceding vowel | Source-backed inventory, contextual allophones and explicit unknowns |
| /r/-loss | Underlying /Cr/ × speech style × speaker × vowel × coda × acoustic cues | Matched careful/colloquial recordings; /r/ presence/absence, VOT, f0, voice quality, formant trajectory |
| Ukrainian target | Adjudicated surface IPA × Ukrainian output | Preserve aspiration, palatality, register-derived vowel differences and uncertainty without inferring them from script alone |

## Highest-risk questions

1. Which vowel-sign × series × coda cells have direct lexical or acoustic evidence, and which are extrapolations?
2. Which register contrasts remain phonemic in the selected Standard Khmer profile, and which are historical or phonetic descriptions?
3. Does Phnom Penh /r/-loss apply only to particular /Cr/ clusters and colloquial styles? The studies show variation; it must be conditioned, not a blanket rewrite.
4. Are f0, aspiration, breathiness and diphthongization jointly present, optional, speaker-specific, or lexically conditioned?
5. Does the coda alter the vowel realization in a way that the current grapheme-level tables miss?

## Execution order

- [ ] Extract the existing dependent-vowel × series coverage report and reconcile every cell with primary phonological/acoustic sources.
- [ ] Expand the matrix to include length, coda and profile; keep `ATTESTED_EXAMPLE`, `CONFLICTING`, `NOT_ESTABLISHED` and `ADJUDICATED_GOLD` distinct.
- [ ] Re-read Wayland & Guion (2005) and Kirby (2014), record sample size, tasks, speech styles, speaker details and acoustic measurements.
- [ ] Build matched /Cr/ and non-/Cr/ lexical sets, with careful and colloquial speech from multiple speakers.
- [ ] Double-annotate narrow phonetic IPA and acoustic cues; adjudicate disputed /r/, aspiration, breathiness, f0 and vowel trajectories.
- [ ] Only then revise the phonology engine and Ukrainian adaptation rows.

**Current status:** PARTIAL. The current coverage report is a grapheme/series evidence inventory, not a complete phonological matrix or accuracy score. Independent lexical gold remains 0. No new Khmer IPA labels are added in this workpack.


## Verified evidence extraction — 2026-11-01

### Independent /r/-loss study: scope and limits

Wayland & Guion (2005), *Mon-Khmer Studies* 35:55–82, [full paper](https://rilca.mahidol.ac.th/documents/PublicationMultimedia/MonKhmer/Vol35/wayland2005sound.pdf), directly compares careful-reading and colloquial Phnom Penh pronunciations. The sample is two male native speakers from Phnom Penh, 20 lexical items beginning with an obstruent + /r/ cluster, and three repetitions of each item in each style. The study measured VOT or affricate frication, F0 at five vowel positions, and F1/F2. It reports colloquial falling–rising F0 contours, increased onset aspiration, and vowel changes including /a, aː/ → [ea] and /ɔː/ → [ɔə] in the examined items. The paper itself cautions that its proposed aerodynamic explanation lacks direct aerodynamic data.

**Implementation boundary:** these findings justify a Phnom Penh colloquial profile with a conditional /Cr/ pathway and separate reading/colloquial outputs. They do not justify deleting every orthographic or underlying /r/, nor a universal Khmer tone rule. The two-speaker, 20-item sample is a research anchor, not sufficient lexical coverage or independent gold for the project.

### Vowel and register evidence

Chem & Chem (2020), “The Standard Khmer vowel system: An acoustic study,” [publisher record](https://www.cjbar.rupp.edu.kh/index.php/cjbar/article/view/36), is an acoustic description focused on Phnom Penh. Its authors note that “standard Khmer” is not sharply defined. Use it to populate source-located vowel measurements only after extracting its actual tables and reconciling short/long vowels, series and coda context; do not convert its abstract into a complete inventory.

Kirby (2014), *Journal of Phonetics* 43:69–85, [DOI](https://doi.org/10.1016/j.wocn.2014.02.001), adds production and perception evidence for f0, aspiration/VOT, voice quality and vowel-quality cues. These are interacting cues, not a licence to encode /r/-loss as a single replacement segment.

**Status update:** /r/-loss evidence is now more precisely scoped and method-documented; independent multi-speaker replication, full vowel × series × length × coda coverage, and IPA adjudication remain PARTIAL/BLOCKED. No Khmer IPA labels or engine rules were added.


### Additional extraction: Chem (2020) full text

The full article is now linked in the source registry. Its methods report 21 native speakers in initial screening (168 lexical items, two repetitions), then four selected Phnom Penh speakers (two female) for acoustic analysis of 61 lexical items, repeated three times in formal reading (pp. 104–105). It reports 21 monophthong categories (10 long, 11 short) and 13 diphthongs (10 long, 3 short; pp. 103–105). It reports coda effects on vowel quality and duration, with closed syllables generally shorter; short diphthongs occur in sample contexts with /-h, -k, -ʔ/ (pp. 108–112).

This materially improves the vowel evidence baseline, but does not fill the complete consonant-series × vowel-sign × coda cross-table. The article itself notes that Standard Khmer is not sharply defined, and the four-speaker sample is not a universal norm. The published transcription and measured tokens remain source evidence, not adjudicated project gold.

See the new [Khmer vowel × series × coda evidence matrix](KHMER-VOWEL-SERIES-CODA-EVIDENCE-MATRIX-2026-11-01.md), which separates Ishida's specialist orthographic mappings from Chem's bounded acoustic sample.


Chem (2020) full-text extraction adds two high-value dialect probes: Standard Khmer /tiɜ/ vs /tiət/ is reported as a single /tiɜ/ in the studied Phnom Penh dialect, and Standard Khmer /eː/ vs /ɛe/ is reported as merged to /eː/ in Phnom Penh (pp. 114–115). The /i/ vowel is discussed as primarily Sanskrit/Pali loan material and was omitted from the acoustic sample. These are profile-specific evidence rows, not universal mergers.


The Khmer matrix now includes the complete phone-to-grapheme mapping table extracted from Ishida's “Vowel sounds mapped to characters” section (all listed plain-vowel and diphthong/rhyme entries, with series and coda conditions). The acoustic series × vowel × coda cross-table remains PARTIAL because Chem's small Phnom Penh sample does not cover every cell.

## Phonotactic restriction classification — 2026-11-15

The current evidence supports a classification of claims, not a new global phonotactic rule set.

| Claim | Correct domain | Source evidence | Status / implementation boundary |
|---|---|---|---|
| No final consonant clusters | Major syllable coda | Nacaskul (1978), pp. 187–188, explicitly contrasts numerous initial clusters with no final clusters | HISTORICAL_SOURCE_REPORTED; contemporary selected-profile lexical confirmation still needed |
| Short vowels and short diphthongs do not occur in open syllables | Major-syllable nucleus/coda relation | Nacaskul (1978), pp. 185, 188–189 | HISTORICAL_SOURCE_REPORTED; do not generalize to every minor syllable or every variety without confirmation |
| A minor type-A onset cluster has /r/ in second position; nucleus short /ə/ or /ɔ/; no final | Minor syllable type A only | Nacaskul (1978), pp. 187–189 | TYPE_SPECIFIC; not a ban on /r/-clusters in major syllables |
| Minor type B has a single-consonant onset, restricted short nucleus and one of four nasal finals | Minor syllable type B only | Nacaskul (1978), pp. 187–190 | TYPE_SPECIFIC; not the language-wide coda inventory |
| Two-consonant onset clusters are common; up to three are reported | Onset structure | Ding et al. (2018), pp. 181–182, in a Khmer name-romanization/NLP study | SECONDARY_DESCRIPTION; approximate cluster count is not an exhaustive inventory or proof that every other sequence is impossible |
| Up to two pre-vowel coengs in an orthographic unit | Orthographic encoding | Unicode L2/22-290, pp. 9–10 | ORTHOGRAPHIC_LIMIT, not a phonological maximum; base + coengs and syllable chaining must be interpreted separately |
| Coeng may represent initial clustering or syllable chaining; orthographic units need not equal phonetic syllables | Orthographic/phonetic boundary | Unicode L2/22-290, pp. 9–10; Ding et al. (2018), pp. 181–183 | STRUCTURAL_ENCODING_FACT; parser output remains orthographic structure and does not claim phonetic syllabification |
| PPK minor disyllable forms CrV/CV/CVN may simplify to C; F0 is lower in /r>h/ forms and voiced-onset disyllables | Profile-specific reduction/prosody | Mam et al. (2025), 50 words, 5 speakers, 3 repetitions | PRIMARY_BUT_BOUNDED; possible pitch phonologization, not a universal tone or segmental rewrite |

### Source reconciliation and contradictions

- Nacaskul's 1978 article is explicitly a historical Cambodian description and uses its own phonetic notation. Its major/minor syllable distinction is useful, but its coda inventory and register claims are not silently promoted to current project rules.
- Unicode L2/22-290 is an orthographic encoding analysis. It documents up to two pre-vowel coengs and chaining; these must not be mistaken for a language-wide phonological onset limit.
- Ding et al. (2018) study 7,658 personal-name romanization instances and explicitly discuss silent etymological stacked letters and phonemic-syllable/orthographic-unit mismatch. Its approximate 80 cluster types are secondary, not an exhaustive phonological survey.
- The publisher preview for Sak-Humphry (2025) contains an internally contradictory coda excerpt: /r/ appears in both the permitted and excluded sets. The preview is recorded as a lead only and is not used to settle the coda inventory.
- Mam et al. (2025) report possible PPK pitch phonologization beyond /r>-h/ forms, including voiced-onset disyllables. The sample is five speakers and 50 words; the authors call for further work. Do not infer tone from spelling or alter the careful-citation profile.

**Implementation decision:** no new global syllable-rejection rule, coda rule, tone label or /r/-rewrite is introduced. The parser's `syllables` are orthographic structural units; `phonetic_representation.status` remains `phoneticization_not_yet_established`.


## Machine-readable reference mapping continuation — 2026-11-24

- Transcribed all 54 rows of Ishida's “Vowel sounds mapped to characters” table (§8 of the canonical evidence matrix) into `reference_mapping_observations` in the canonical vowel-context register.
- The new layer preserves source notation, consonant-class scope and orthographic sequence verbatim, with source ID, locator, scope and explicit `runtime_eligible=false`.
- It is deliberately separate from lexical/context case rows, source IPA fields, coda lexical examples and the deterministic engine. The source table is not an adjudicated Phnom Penh lexical corpus.
- The generated report exposes all 54 mappings as source-reference observations. The 32-cell sign × series coverage summary is unchanged; this extraction does not fill any missing cell by analogy or claim that every class/sign sequence is a universal phonological rule.
- Acceptance: schema-valid, all source IDs resolve, stable unique IDs KHV-MAP-001–054, report mirrors registry exactly, no IPA/UA promotion, canonical/public report byte parity.
- Status: structured reference extraction **PENDING exact-head CI**; runtime contextual phonology remains **PARTIAL**. No new pronunciation accuracy claim.


## Final verification — structured Ishida reference mappings — 2026-11-24

- PR #560 merged into `main` as `1f48334047c3cbadc6d9d4e0a9c9a3fcf419d989`.
- Exact PR-head Quality [45434765907](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45434765907) and Chromium [45434766063](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45434766063) passed; Chromium reported 40/40.
- Exact-main Quality [45435043181](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45435043181), Chromium [45435043196](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45435043196), and Pages build/deploy [45435043183](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45435043183) all passed.
- Live service and methodology pages returned HTTP 200. The deployed coverage report returned HTTP 200 and exposes all 54 `KHV-MAP-001`–`KHV-MAP-054` rows.
- Structured reference extraction: **DONE_VERIFIED**. Runtime contextual phonology remains **PARTIAL**; no IPA, Ukrainian adaptation, deterministic runtime rule, gold label or accuracy claim was added. The 32-cell sign × series status remains unchanged.
