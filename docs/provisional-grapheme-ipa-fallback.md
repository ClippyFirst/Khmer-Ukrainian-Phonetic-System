# Provisional Khmer grapheme-to-IPA fallback

Status: design contract; implementation pending.

## Purpose

Mirror the Lao hybrid's typed, low-confidence grapheme fallback without weakening the Khmer engine's established orthography-to-IPA path. This is a rendering-coverage feature, not a claim that every grapheme has a context-free pronunciation.

## Required pipeline

Khmer grapheme cluster / recognized positional unit → provisional IPA token(s) → the existing IPA-to-Ukrainian adapter → Ukrainian text with a visible `?` uncertainty marker.

Never map Khmer code points directly to Ukrainian letters. Provisional IPA must be typed `PROVISIONAL`, carry source grapheme, positional role, rule ID and evidence, and must not be counted as supported IPA in benchmarks.

## Eligibility and limits

- Reuse parser-confirmed base-consonant identity and already registered onset IPA hints only.
- A consonant's inherent-vowel class/series must not be inferred from a naked code point when the parser has not established the relevant series.
- Vowel signs, subscripts, coeng, independent vowels, register shifts and diacritics may be emitted as provisional IPA only when a source-backed, positional rule explicitly covers the complete grapheme unit.
- Do not infer tone from incomplete orthographic structure.
- Unknown or non-core signs remain explicit unknown markers; do not silently drop them.
- Keep full-confidence IPA/Ukrainian fields unchanged. Expose fallback separately, e.g. `provisional_ipa`, `provisional_ukrainian`, `fallback_status`, and `fallback_trace`.

## Confidence and rendering contract

- `SUPPORTED`: normal engine path only.
- `UNCERTAIN`: structurally complete IPA with a known uncertainty.
- `PROVISIONAL`: grapheme-position hint, low confidence; append `?` to the Ukrainian rendering of the affected unresolved unit.
- `UNKNOWN`: no registered IPA hint; render `?` only, with the source grapheme preserved in trace.

Provisional values must not be promoted to canonical `ipa`, and must be excluded from IPA accuracy scoring. Browser and Python must return the same text and trace.

## Acceptance

1. Source registry entries for each fallback rule include language variety, grapheme/position, IPA hint, scope, primary source and review status.
2. Parser tests cover consonant series, vowel signs, subscripts/coeng, independent vowels, punctuation, mixed scripts and unknown symbols.
3. Python and browser parity tests cover the same fixtures.
4. Tests assert that unsupported marks remain visible as uncertainty and no tone is invented.
5. Full CI and built-site Chromium tests pass.
6. Report rendering coverage separately from supported IPA coverage and phonetic accuracy.

## Current evidence boundary

The existing engine's partial Khmer parser and the practical IPA adapter are not themselves a source-backed grapheme fallback inventory. Do not manufacture IPA hints from the Ukrainian practical table. Until positional Khmer rules are registered and sourced, unsupported constructions remain `UNKNOWN`.


## Implementation checkpoint — 2026-11-11

A minimal onset-only fallback is now implemented in the Python rule engine and browser engine.

- Reuses the parser's registered base-consonant onset IPA and the existing IPA → Ukrainian adapter.
- Keeps canonical ipa and ukrainian fields withheld when the full unit is unresolved.
- Exposes provisional_ipa, provisional_ukrainian, fallback_status and fallback_trace in Python; browser units carry PROVISIONAL, an onset-only IPA display and a visible ?.
- Does not infer vowel, coda, subscripts, coeng realization or tone.
- Added Python regression for កា and browser source-contract assertions.

Status: PARTIAL, not DONE_VERIFIED. The current hint is an onset-position consonant only, not a full grapheme inventory. The parser's current evidence IDs are reused; a dedicated rule registry with per-entry primary-source locators, explicit positional scope and reviewer status is still required. Browser tests currently assert the fallback contract in source; they do not yet execute a Python/JavaScript parity fixture against identical structured results.

Implementation commits: 61e0246cf34e0319f72c9b04c5926b6e3b3ad1f5 (Python engine), 352c22a55f526877dd136a982b2aa5ac03ff3838 (Python regression), 862aa061726b2bae6296199e4b655334bb6f609a (browser), 660915e4ed1f44eab04258957eee39537883aadd (browser regression). Exact-head CI runs 43099931373 and 43099931284 were queued at the last check; neither is recorded as passed.


## Scope correction — 2026-11-11

The fallback is a separate diagnostic preview, not a replacement for canonical IPA or Ukrainian output. The browser keeps the canonical unresolved marker in the main result and shows the onset-only preview in per-unit analysis details. The regression fixture is a consonant with an unresolved coeng/subscript structure (ក្ក), not ကា: the latter already follows the existing inherent-vowel rule and must not be treated as unresolved.


## Shared Python/browser fallback regression fixture — 2026-11-17

A shared machine-readable fixture now exercises the existing onset-only preview for an unresolved COENG+subscript unit (ក្ក). Python and Chromium tests read the same case. Python asserts the API's intentional `null` canonical fields; the browser asserts the corresponding rendered `NOT_ESTABLISHED` markers. Both assert the separate onset-only `k` → `к?` preview is visibly provisional and carries the same rule ID, exposed as inspectable unit-detail data attributes. This is a cross-runtime contract regression, not a pronunciation gold item and not a new grapheme-to-IPA rule.

Fixture: `data/tests/khmer-onset-fallback-fixtures.json`. Acceptance remains limited to the existing onset hint. The dedicated register now exists at `data/khmer-positional-onset-evidence.json` with a JSON Schema and parity tests. It records the 33 existing consonant onset hints against Richard Ishida's Basic consonants rows. This is a specialist-reference evidence container only: entries are not independently reviewed or adjudicated for the project profile, and the register is not a runtime rule source. Primary phonetic evidence and qualified target-profile review remain outstanding. No unsupported vowel, coda, subscript realization or tone is inferred.


## Primary display correction — 2026-11-24

The user's explicit output contract requires the best supported approximate result to remain visible when a complete pronunciation is unavailable. An onset-only preview is therefore no longer confined to the per-unit diagnostics:

- When the parser identifies a source-backed onset but the full unit cannot be converted to IPA, the primary IPA display shows `/onset/???` and the primary Ukrainian phonetic display shows the IPA-adapted onset followed by `???`.
- The unit retains its parser-derived status (`NOT_ESTABLISHED` or `EVIDENCE_LIMITED`); `complete` remains false. The typed result stores bare onset IPA without display markers and types the Ukrainian value as `IPA_DERIVED_PROVISIONAL`.
- No vowel, coda, subscript realization, syllable boundary, tone or full-word pronunciation is inferred by this fallback.
- If an orthographic BGN/PCGN candidate is also available, it remains separately visible as an orthographic candidate and must never replace the phonetic preview.
- The onset preview is attempted before the orthographic fallback. It applies whenever a valid parsed unit has a registered onset hint but deterministic full-unit IPA is unavailable, including units whose broad structural status remains `ESTABLISHED_STRUCTURE` while syllabification is unresolved.
- If no source-backed onset hint exists, the result remains `???` with the source grapheme and reason preserved.

Regression example: `ពាក់` exposes `/p/???` and `п???`; its separate `Пеак` candidate is labelled BGN/PCGN-derived orthography, not pronunciation. This is a low-confidence onset preview, not a complete or adjudicated IPA transcription.

This correction changes display behavior, not the evidence threshold for full IPA. Provisional hints remain excluded from supported-IPA coverage and accuracy scoring.
