# Test plan: Khmer typed IPA architecture parity

Build: `feat/khmer-lao-engine-contract-parity-20261124`  Date: 2026-11-24

| Case | Flow | Type | Expected | Automated evidence |
|---|---|---|---|---|
| F01-H1 | Full segmental IPA | Happy | IPA is segmented, status stays UNCERTAIN, same adapter maps Ukrainian | Python and JS typed adapter tests |
| F01-E1 | Valid IPA without Ukrainian correspondence | Edge | IPA remains UNCERTAIN; Ukrainian adapter returns no invented mapping | Python and JS typed adapter tests |
| F01-E2 | IPA syllable and word boundaries | Edge | Dot/space boundaries remain inspectable | Python and JS typed adapter tests |
| F01-E3 | Affricate, length and tone marks | Edge | Tie bar and length preserved; tone retained without inferred tone category | Python and JS typed adapter tests |
| F02-H1 | Registered onset-only hint | Happy | PROVISIONAL segment(s) + one unknown region; Ukrainian output is onset + ??? | Python and JS typed adapter tests; engine parity |
| F02-E1 | No unresolved positions supplied | Edge | Provisional factory still appends an unknown tail | Python and JS typed adapter tests |
| F03-N1 | No IPA hint | Negative | UNRESOLVED and exactly ??? | Python and JS typed adapter tests |
| F04-H1 | Orthographic fallback exists | Separation | Fallback stays ORTHOGRAPHIC_ROMANIZATION_FALLBACK and typed IPA stays UNRESOLVED | web-engine regression |
| F05-H1 | Browser Worker execution | Integration | Plain typed result crosses Worker boundary | Khmer Worker contract test |
| F06-H1 | CLI analyze / explain | Integration | JSON includes typed result, provenance and uncertainty | `tests/test_cli_phonetic_result.py` |
| F06-H2 | CLI ipa / transliterate | Integration | Partial output remains visible with ???; no-hint case is ??? | `tests/test_cli_phonetic_result.py` |
| F07-H1 | Python ↔ JavaScript engine | Parity | Typed status, segment sequence, boundaries and target result match | `tests/cross-runtime-rule-output-parity.mjs` |
| F08-H1 | Browser detail disclosure | UI | Typed IPA, confidence, provenance and caveats visible in Ukrainian | Chromium browser smoke (exact-head pending) |

## Evidence boundary

The suite validates architecture, deterministic behavior and cross-runtime parity. It does not validate Khmer pronunciation accuracy. The independent adjudicated Khmer IPA gold corpus remains empty; linguistic accuracy remains NOT_ASSESSED.
