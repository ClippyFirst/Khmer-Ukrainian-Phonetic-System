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
