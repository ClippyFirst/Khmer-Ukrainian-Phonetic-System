# Evidence confidence tiers — Khmer beta

**Scope:** Phnom Penh careful-citation project profile. These are categorical evidence tiers, not calibrated probabilities, benchmark scores, or claims of expert validation.

| Tier | Meaning | Runtime treatment |
|---|---|---|
| A | Independently adjudicated, profile-matched gold | Not currently available |
| B | Every output has an exact per-unit locator to a registered pronunciation source, the IPA → Ukrainian adapter succeeds, and the source/profile scope is explicit | Display as PROPOSED/PROVISIONAL with the source locator visible; never call canonical or expert-validated |
| C | Experimental or incomplete evidence, unregistered source IDs, no exact locator, compositional hypothesis without a phrase-level source, or unresolved source conflict | Keep visible as a candidate where safe, but do not present as B |
| D | No usable candidate or unsupported/malformed input | Withhold IPA and Ukrainian output |
## Runtime behavior

The existing lexical fixtures with source locators and a successful IPA → Ukrainian mapping are now explicitly labelled tier B at both unit and aggregate levels. The series-based inherent-vowel fallback now retains the onset registry's actual source references rather than returning an empty evidence list; it remains PROPOSED and is not promoted to canonical or gold status.

A fixture without a source locator (for example, a representative contrast probe) is tier C even if it has an IPA string. Onset-only previews and evidence-limited structures are also C. Unsupported input is D. Aggregate confidence is the weakest tier among the linguistic units, while each unit keeps its own tier so a mixed input can still show which portions are B.

## Measurement boundary

The Phnom Penh IPA convention sheet remains a draft, not expert-approved. The independent adjudicated gold corpus remains empty; accuracy remains null / NOT_ASSESSED. B means source-traceable provisional support under the project's stated profile, not independent expert confirmation or empirical correctness. No gold labels or benchmark rows were created by this change.

## Verification

Implementation branch: research/tier-b-provisional-coverage-2026-11-21, based on main 90f791e9e264ab680e5b871a1d54229d7567b993. Added per-unit and aggregate confidence-tier logic, source provenance for the inherent-vowel rule, browser display labels, and regression tests. Exact-head hosted CI is required before merge; do not infer test success from the presence of tests.
