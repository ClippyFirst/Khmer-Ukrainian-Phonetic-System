# Khmer positional onset evidence registry

Status: `PARTIAL_SPECIALIST_REFERENCE_REGISTER`.

The machine-readable register at `data/khmer-positional-onset-evidence.json` records the 33 existing consonant onset hints already present in `data/khmer/consonants.json`. Each entry identifies its Unicode character, onset-only position, current IPA hint, fallback rule ID, specialist-reference locator, and review/profile status.

## Evidence scope

The current source is Richard Ishida's *Khmer (Cambodian) Orthography Notes*, specifically the **Basic consonants** table and the row for each character. This is a specialist descriptive reference, not a primary acoustic study and not independent adjudication for the project's Phnom Penh careful-citation profile. The registry therefore explicitly marks every entry `NOT_INDEPENDENTLY_REVIEWED` and `NOT_ADJUDICATED_FOR_PROJECT_PPH_PROFILE`.

The register mirrors existing inventory values; it does not introduce or independently validate any IPA value. It is not consumed by the runtime. Tests enforce exact parity with `consonants.json` so the evidence record cannot silently drift from the current onset inventory.

## Strict use boundary

- Allowed use: the existing separate `PROVISIONAL_ONSET_PREVIEW_ONLY` path.
- Not allowed: canonical IPA/Ukrainian promotion, accuracy or supported-coverage scoring, coda/cluster realization, vowel or tone inference, or complete-syllable output.
- This source does not establish the pronunciation of subscripts, COENG clusters, codas, vowels, or tone.
- A primary phonetic source, qualified target-profile review, and independent adjudication remain required before promotion or expansion.

## Acceptance status

- Registry and schema: implemented.
- Inventory parity and non-promotion contract tests: implemented.
- Primary phonetic evidence and target-profile adjudication: outstanding.
- Broader vowel/subscript/COENG fallback: still blocked.

This closes only the evidence-container portion of the previously TODO positional registry. The overall positional evidence task remains PARTIAL, not DONE_VERIFIED.

## Exact-locator confidence gate — 2026-11-21

The browser and Python confidence tiers now require an exact per-unit source locator plus an evidence ID registered in `data/khmer/sources.json` with a pronunciation-capable status. The R12A examples for U+1780 `ក` /kɑː/ and U+1782 `គ` /kɔː/ are locatable at §Consonant registers, lines 237–243, and §Inherent vowels, lines 258–266. These two examples can reach B as provisional outputs; this does not promote the full 33-row consonant registry.

The R12A page has an internal class-list conflict for `ឆ`: the Onsets table places it in the ɑ-class (lines 1158–1160), while Basic consonants places it in the ɔ-class (lines 1181–1187). The existing `ឆ` inherent-vowel fallback remains C and is not used as a B example pending reconciliation. The broader positional onset registry remains PARTIAL.
