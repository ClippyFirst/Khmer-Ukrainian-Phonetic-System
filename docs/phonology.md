# Khmer phonology and pronunciation model

## Scope

The repository distinguishes a descriptive phonetic inventory from a deterministic orthography-to-IPA algorithm. The latter is incomplete and must not be simulated by guesswork.

The current `khmer-pph-careful-citation-v1` profile does not encode lexical tone by default. This is a conservative implementation choice, not a claim that all contemporary Phnom Penh speech is non-tonal: a 2025 five-speaker study reports a categorical high/low F0 grouping in a bounded PPK wordlist, including /r>h/ forms and voiced-onset disyllables, and argues that pitch may be undergoing phonologization. This remains profile-specific and evidence-limited; it is not a license to add a universal Khmer tone rule.

## Consonants

The current inventory includes the 33 basic consonant letters and records their principal onset values separately from orthographic class. Foreign/loanword consonant combinations are kept outside the core 33-letter inventory unless separately evidenced.

## Vowels

The descriptive inventory includes short/long plain vowels and complex vowels. The repository does not equate a vowel sign with one IPA vowel: the same written sign can be realized differently after the two consonant classes/registers. Representative documented contrasts include ក /kɑː/ vs គ /kɔː/, and កី /kəj/ vs គី /kiː/.

Chem & Chem's acoustic study specifically investigates the Phnom Penh dialect as a candidate standard variety and reports systematic differences between first- and second-register vowels, including quality and diphthongization differences.

## Syllable structure

A useful descriptive model permits complex onsets and restricted codas, but the exact constraints depend on syllable type and source profile. Nacaskul (1978) distinguishes major syllables from two minor-syllable types: its /r/-second-member cluster restriction applies to minor type A, while the four-nasal coda restriction applies to minor type B. Neither is a global ban on clusters or codas. Nacaskul also reports no coda clusters in major syllables and no short nuclei in open major syllables; these are historical source-reported generalizations that still need contemporary profile-matched confirmation.

Orthographic syllables and phonetic syllables are not identical. Unicode's Khmer encoding analysis describes coengs as marking both initial clusters and syllable chaining, so a previous phonetic coda may be represented inside the next orthographic unit. Its limit of two pre-vowel coengs is an orthographic encoding limit, not a phonological maximum for onset clusters. Therefore the current parser is a structural foundation, not a complete phonetic syllabifier.

## /r/-loss and emerging Phnom Penh pitch patterns

Colloquial Phnom Penh pronunciation can lose /r/ in relevant onset clusters and show associated aspiration, F0, phonation and vowel effects. This is a profile-level phonetic process, not a global spelling rule. Mam, Pittayaporn & Maspong (2025) extend the evidence by reporting lower F0 for /r>h/ forms and voiced-onset disyllables in a five-speaker PPK sample; they suggest possible phonologization but explicitly leave further work open. The current careful-citation profile and colloquial PPK must remain distinct. See the sources listed in `data/khmer/sources.json` (Wayland 2005; Kirby 2014; Mam et al. 2025).

The previous `render_ipa_profile()` implementation rewrote eligible stop+/r/+vowel strings to a single aspiration-only form. This was too deterministic for the evidence: Kirby (2014) reports multiple correlates of colloquial Phnom Penh /r/-loss, including variable aspiration, F0 contours, phonation and vowel-quality/diphthongization effects; the variants are not selected by an IPA string alone. See Kirby, *Incipient tonogenesis in Phnom Penh Khmer: Acoustic and perceptual studies*, Journal of Phonetics 43 (2014), 69–85, DOI: https://doi.org/10.1016/j.wocn.2014.02.001; Wayland (2005), *Sound changes following the loss of /r/ in Khmer*, Mon-Khmer Studies 35:55–82.

The adapter now fails closed with an explicit `ValueError` when a colloquial-profile input contains a potential onset /CrV/ at a known boundary. It leaves unsegmented matches such as `akra` unchanged and preserves careful/established profiles. This is a safety guard, not a completed colloquial phonetic model. A future alternatives-aware result contract must retain source profile, lexical scope, and competing realizations rather than selecting aspiration as a universal output.

## Glottal stop

The glottal stop is part of the phonetic analysis. In practical Ukrainian output it may be neutralized to zero by project policy, but it remains explicit in the research layer. Independent-vowel constructions commonly involve a glottal onset in pronunciation.

## Open research gap

The next major linguistic artifact should be a versioned matrix:

base series × vowel sign × coda × syllable type × length × stress/profile → phonological vowel → IPA → Ukrainian candidates

That matrix must be built from lexical evidence rather than generated solely from Unicode sign names.


## Phonotactic restrictions: scope before implementation

Do not treat every unusual Khmer letter sequence as a forbidden phonological structure.

- **Major-syllable restrictions (historical source report):** Nacaskul (1978) says major syllables do not have final consonant clusters and that short vowels/short diphthongs do not occur in open syllables. These are candidate phonotactic generalizations, not yet fully reconciled with the selected contemporary profile.
- **Minor-syllable type A:** Nacaskul's restriction that an onset cluster has /r/ in second position, with a short /ə/ or /ɔ/ nucleus and no coda, applies to this minor-syllable type only.
- **Minor-syllable type B:** its single-consonant onset, restricted short nucleus and nasal coda are likewise type-specific.
- **Orthographic stacking:** Unicode L2/22-290 describes up to two pre-vowel coengs in an orthographic unit, but coengs can encode syllable chaining. Ding et al. (2018) also show that phonemic syllables and orthographic units can diverge, including silent etymological stacked letters. These are not direct phonotactic bans.
- **Profile-level prosody:** Mam et al. (2025) report possible PPK pitch phonologization in /r>h/ forms and voiced-onset disyllables. This is not a universal tonal rule and must not be inferred from graphemes alone.

No new phonological rule is enabled by this evidence update. The next acceptance step is a source-located lexical matrix that records major/minor type, onset, nucleus length, coda, profile and evidence status separately.


## Explicit IPA transcription kind

The typed result now includes `ipa_kind` on every unit. The internal engine currently emits `UNRESOLVED` for linguistic units because the project has not approved whether its single scored corpus should be phonemic, broad phonetic or narrow phonetic. It emits `NOT_APPLICABLE` for punctuation. External provider candidates already carry an explicit kind, but that provider declaration does not determine the internal corpus convention. This additive field prevents consumers from silently treating an untyped IPA string as phonemic or phonetic. Changing `UNRESOLVED` to one of the three transcription kinds requires the expert approval recorded in the IPA convention draft; no IPA labels or output strings were changed by this contract repair.
