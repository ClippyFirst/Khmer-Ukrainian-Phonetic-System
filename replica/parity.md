# Replica parity report — 2026-11-24

## Scope

The replicated object is the Lao engine's architecture and result-output contract, applied to the existing Khmer engine. This is not a visual clone of the Lao website and does not transfer Lao linguistic content.

## Weighted feature parity

The feature matrix contains 11 `must` items and 3 `should` items. Using the replica-skill weighting (must = 3, should = 2; partial = half credit):

- Must-have features: 11/11 complete.
- Should-have features: 3/3 complete.
- Weighted score: 39/39 = **100%**.
- Layout/pixel parity: not applicable; no Lao UI layout was cloned. Only the existing Khmer unit-detail UI was extended to disclose typed IPA confidence/provenance/uncertainty.

## Evidence

- Quality [45490428639](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45490428639): 503 Python tests + 70 subtests, web checks, typed result parity, benchmark and production build.
- Chromium [45490428728](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45490428728): 42/42 Playwright tests; includes the typed IPA detail disclosure.
- Pinned Rust segmentation [45490428786](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45490428786): PASS.
- External khPOS segmentation [45490428814](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45490428814): PASS.
- Python/JavaScript parity counts: 129 structural, 38 lexical, 46 consonant/rule and 6 segmentation fixtures.

## Preserved differences

- Khmer structural and phonological rules remain Khmer-specific.
- BGN/PCGN orthographic fallback remains separate from phonetic IPA.
- External G2P candidates remain opt-in and non-canonical.
- No tone inference was introduced.
- Independent Khmer IPA gold remains empty; pronunciation accuracy is NOT_ASSESSED.

## Verdict

Architecture and behavior feature parity for the agreed scope is complete and verified. The repository remains a research-ready partial prototype rather than a linguistically validated production G2P system.
