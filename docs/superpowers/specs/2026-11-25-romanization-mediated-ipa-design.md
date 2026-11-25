# Romanization-mediated IPA candidate path — design

Date: 2026-11-25
Status: APPROVED — first implementation stage delivered; broader phonology remains partial (2026-11-25)
Base: `main` at `e972cd503f3670d08a2fbf0812efdc701513a810`

## Intent

Improve the “Українська через романізацію” mode by using the existing BGN/PCGN-derived romanization as a contextual clue for a **provisional IPA candidate**, then adapting that typed IPA through the existing IPA→Ukrainian target adapter. Keep orthographic romanization distinct from pronunciation and never imply that romanization is IPA.

## Current implementation and constraints

- `src/khmer-romanization-ukrainian.js` renders romanization as Ukrainian orthographic approximations. It is explicitly independent of IPA.
- Khmer text is currently romanized through `@gmana/km-translit` (`khmerToLatin`) before the Ukrainian rendering. The visible browser route strips PCGN diacritics in its profile description (“BGN/PCGN-derived ASCII (diacritics omitted upstream)”).
- The crosswalk is longest-match character/sequence substitution. It is not a positional phonology engine and cannot itself recover distinctions that upstream romanization has discarded.
- `src/khmer-ipa-result.js` and Python's typed IPA model already provide provenance, certainty, uncertainty, partial candidates and a single IPA-only Ukrainian target adapter.
- Main's existing canonical IPA remains `UNCERTAIN` pending independent adjudication. No source in this design promotes a romanization-derived candidate to canonical/gold IPA.
- The research review found that Khmer vowel realization depends on consonant series/register, inherent/dependent vowels, syllable/coda position and coeng clusters. A romanization-only bridge is defensible only where the romanized representation preserves the necessary distinctions; otherwise source orthography/context must remain attached.

## Goals

1. Offer an IPA-mediated Ukrainian candidate in the “through romanization” mode when the contextual romanization path can justify one.
2. Use longest-match tokens and contextual rules, not independent character substitution.
3. Preserve the original Khmer span, romanization, tokenization, rule IDs, candidate alternatives, provenance and uncertainty.
4. Return partial/unknown spans explicitly; do not fill unsupported vowels, codas, tone or dialect details by guesswork.
5. Keep the existing orthographic Ukrainian romanization output available as a separately labelled, non-pronunciation result.
6. Share equivalent typed result semantics across Python and JavaScript/browser paths.

## Non-goals

- Replacing direct Khmer-script IPA analysis as the primary route.
- Claiming PCGN romanization is phonetic transcription or universally reversible.
- Generating narrow phonetic IPA, tone, phonation or dialect detail without suitable evidence.
- Integrating a neural model, server inference endpoint or external API.
- Promoting provisional outputs to supported/canonical IPA or changing gold-corpus labels.

## Approaches considered

1. **Contextual romanization-mediated IPA with retained Khmer context (selected).** Tokenize the actual romanization while retaining aligned source graphemes and positional features; apply only evidenced rules; produce typed provisional IPA and pass it through the existing IPA target adapter. This best matches the requested mode while guarding against information lost in ASCII romanization.
2. Romanization-only deterministic mapping. Simpler, but unsafe where romanization collapses consonant-series, vowel-sign or syllable information; likely to encode hidden guesses as deterministic output.
3. External/neural G2P. Potentially better coverage, but introduces model/runtime, privacy, licensing and deployment decisions beyond this feature.

## Proposed behavior

- Direct IPA remains the preferred source for the canonical result.
- The “Українська через романізацію” path computes the established romanization, then a separate contextual adapter creates a **PROVISIONAL** typed IPA candidate only for rule-covered spans.
- Where direct IPA is complete, the romanization mode may still display its orthographic rendering as such; it must not silently relabel it as IPA.
- Where the bridge cannot justify a segment, the typed result contains an explicit unknown tail/span and Ukrainian output uses the existing unresolved marker convention.
- Candidate provenance identifies the romanization profile, transducer/rule-set version and source alignment. Uncertainty states exactly which contrasts or contexts were lost/unmodeled.
- The UI distinguishes “Українська через IPA (попередня)” from “Українська з романізації (орфографічна; не вимова)” or equivalent clear labels. Existing standalone romanization remains visible.

## Evidence and evaluation

- Build a rule inventory from the repository's PCGN matrices and audited primary descriptions; each executable rule must have source citation, environment, scope and test fixture.
- Do not infer IPA values solely from the Ukrainian romanization crosswalk.
- Add paired fixtures where identical romanized sequences have distinct source contexts, to verify that context is retained and ambiguity is surfaced.
- Evaluate against existing source-attested IPA datasets only as exploratory diagnostics unless the target profile/dialect and licensing are established. No accuracy claim without independent adjudicated gold.
- Report candidate coverage, partial coverage, ambiguity/abstention, PER/CER where valid, exact-word match and Python/JS parity separately.

## Acceptance criteria

- A romanization-derived candidate is always typed `PROVISIONAL` (or `UNRESOLVED`), with non-empty provenance and explicit uncertainty; never `SUPPORTED` or canonical IPA.
- The Ukrainian phonetic candidate is generated only by the existing IPA target adapter; no direct romanization-to-Ukrainian shortcut is used for this mode's pronunciation result.
- Context-sensitive rules retain and test source consonant series, vowel sign/inherent vowel, coeng structure, syllable/coda position and boundaries wherever relevant.
- Lost distinctions produce ambiguity/unknown output rather than silent selection.
- Orthographic romanization remains separately available and clearly labelled as non-pronunciation.
- Python/browser parity, unit tests, production build and relevant CI workflows pass.
- Documentation and master handoff record exact evidence and remaining linguistic blockers.

## Decisions left to implementation

The builder should first verify the exact behavior and licensing of `@gmana/km-translit`, whether it exposes aligned/tokenized output or only a diacritic-stripped string, and whether a safe source-aligned representation can be added without replacing the current romanizer. If alignment cannot be recovered reliably, the bridge must use the original Khmer orthographic structure alongside the romanized sequence rather than pretending the ASCII string is lossless.

## Implementation status — 2026-11-25

The first executable stage is implemented on branch `feat/romanization-mediated-ipa-20261125` (draft PR #572):

- A source-aligned PCGN onset adapter cross-checks the leading romanization token against the original Khmer base consonant and the repository's source-registered onset IPA.
- The resulting typed IPA is always `PROVISIONAL` or `UNRESOLVED`; Ukrainian output uses the existing IPA-only adapter.
- The context-sensitive PCGN BA `b/p` row abstains. Vowels, codas, syllable boundaries, tone and dialect detail remain unresolved.
- The orthographic romanization card remains separately available and explicitly marked “не вимова”.
- Python/JavaScript semantics and all registered onset rules have parity tests. Quality checks passed on `9d5acbb95fbe46df884d1ccc2482eb48d6f6d90e`; Chromium smoke passed 43/43 on the same code head.
- This is a verified partial implementation, not completion of the full contextual G2P acceptance criteria. The vowel model explicitly warns that its representative contrasts are not a complete deterministic orthography-to-IPA matrix. Do not generalize the onset-only inventory into vowel/coda rules without additional evidence and tests.
