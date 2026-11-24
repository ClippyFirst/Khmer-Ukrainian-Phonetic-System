# Replica build bug log

All entries below were observed during implementation and fixed before the final exact-head check.

| ID | Severity | Symptom | Root cause | Fix |
|---|---|---|---|---|
| BUG-001 | S2 | Browser typed IPA module did not load | Shared `mapIpa` target adapter import was missing after isolating the typed module | Added explicit import; browser checks rerun |
| BUG-002 | S2 | Long-vowel test merged `ɑː` into one segment | Modifier-letter suffix scanner consumed the length mark | Length marks are now separate typed modifier segments |
| BUG-003 | S2 | External candidate mapping failure reported the entire IPA instead of the exact unsupported tail | Typed adapter withheld output but diagnostic did not retain the legacy unsupported-token detail | Reused raw mapper only for diagnostics, never to produce Ukrainian output |
| BUG-004 | S2 | Orthographic fallback kind disappeared from the phonetic result envelope | Initial integration removed an existing separately typed diagnostic candidate | Restored `ORTHOGRAPHIC_ROMANIZATION_FALLBACK`; typed IPA remains UNRESOLVED and never enters the IPA adapter |
| BUG-005 | S2 | CLI bypassed the deterministic rule engine | Existing CLI called only the structural parser | Routed analyze/ipa/transliterate/explain through `RuleBasedKhmerEngine`; retained structural-only syllables command |
| BUG-006 | S2 | Syllable boundaries were not populated in complete typed IPA | Success branch still used a single start/end pair | Applied parsed boundary positions in both Python and JavaScript |

Open bugs: none known at the current branch head. Final browser and external benchmark workflows must still complete before the UI row is marked DONE_VERIFIED.
