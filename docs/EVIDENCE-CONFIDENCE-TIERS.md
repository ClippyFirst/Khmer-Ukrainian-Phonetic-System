# Evidence confidence tiers — Khmer beta

**Scope:** Phnom Penh careful-citation project profile. These are categorical evidence tiers, not calibrated probabilities, benchmark scores, or claims of expert validation.

| Tier | Meaning | Runtime treatment |
|---|---|---|
| A | Independently adjudicated, profile-matched gold | Not currently available |
| B | Every output has an exact per-unit locator to a registered pronunciation source, the IPA → Ukrainian adapter succeeds and agrees with the supplied lexical Ukrainian reference (when present), and the source/profile scope is explicit | Display as PROPOSED/PROVISIONAL with the source locator visible; never call canonical or expert-validated |
| C | Experimental or incomplete evidence, unregistered source IDs, no exact locator, compositional hypothesis without a phrase-level source, or unresolved source conflict | Keep visible as a candidate where safe, but do not present as B |
| D | No usable candidate or unsupported/malformed input | Withhold IPA and Ukrainian output |
## Runtime behavior

The B gate now requires both an explicit per-unit `source_locator` and at least one evidence ID registered in `data/khmer/sources.json` as a pronunciation-capable source (`SPECIALIST_REFERENCE`, `PRIMARY_PHONETIC_SOURCE`, or `SECONDARY_LEXICAL_REFERENCE)). A non-empty evidence array alone is insufficient: Unicode examples, unregistered IDs, and compositional guesses remain C.

Current B examples:
- `ក` → /kɑː/ and `គ` → /kɔː/: exact R12A §Consonant registers examples (U+1780/U+1782, lines 237–243) and §Inherent vowels (lines 258–266).
- `ខ្មែរ`, `ភាសា`, `ភ្នំពេញ`, `កម្ពុជា`, `ខ្ញុំ`: exact Wiktionary entry-level standard IPA locators are stored in the fixtures and source registry. The `ភាសា` stress mark is retained.
- `ជាខ្មែរ` is a direct phrase-entry case with standard IPA `/ciə ˈkʰmae/` at permanent Wiktionary revision `oldid=68806374`; it is not the compositional `ភាសាខ្មែរ` fixture and has its own registered locator. The page's orthographic/phonemic form `jāk̥ʰmaer` and WT romanisation `ciə khmae` are stored separately from IPA.
- `ល្ងាច` is a direct lexical entry with standard IPA `/lŋiəc/` at Wiktionary revision `oldid=68625783`; the orthographic/phonemic notation and WT romanisation are kept separate from IPA. The cluster passes the current mechanical adapter as a provisional Ukrainian form.
- `អក្សរខ្មែរ` `/ʔak.ˈsɑː kʰmae/`, `នគរខ្មែរ` `/nɔ.ˈkɔː kʰmae/` and `អក្សរមូល` `/ʔak.ˈsɑː muːl/` are direct standard-IPA entries at permanent Wiktionary revisions `oldid=87132823`, `84887163` and `63698235`. Orthographic/phonemic notation and WT romanisation are preserved separately. The Ukrainian adapter keeps the full length marker in the IPA display but omits post-vocalic `ː` in practical Ukrainian spelling; this is an explicit target-orthography decision, not IPA normalization.

The phrase `ភាសាខ្មែរ` is composed from the separately cited `ភាសា` and `ខ្មែរ` entries, but no direct phrase-level source locator was found; it remains C. The inherent-vowel fallback for `ឆ` remains C: R12A's own consonant-register listings conflict (the Onsets table lists `ឆ` in the ɑ-class at lines 1158–1160, while Basic consonants lists it in the ɔ-class at lines 1181–1187). A source ID without an exact, reconciled locator does not qualify for B.

The browser unit details now show the exact locator for each B-tier item. Aggregate confidence remains the weakest tier among linguistic units, while per-unit tiers identify which parts have source-backed support.

## Measurement boundary

The Phnom Penh IPA convention sheet remains a draft, not expert-approved. The independent adjudicated gold corpus remains empty; accuracy remains null / NOT_ASSESSED. B means source-traceable provisional support under the project's stated profile, not independent expert confirmation or empirical correctness. No gold labels or benchmark rows were created by this change.

## Verification

Implementation branch: research/tier-b-provisional-coverage-2026-11-21, based on main 90f791e9e264ab680e5b871a1d54229d7567b993. Added per-unit and aggregate confidence-tier logic, source provenance for the inherent-vowel rule, browser display labels, and regression tests. Exact-head hosted CI is required before merge; do not infer test success from the presence of tests.
