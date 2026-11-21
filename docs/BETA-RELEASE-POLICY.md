# Khmer beta release policy

**Release channel:** public beta (not a linguistically validated production standard)  
**Scope:** the currently implemented, explicitly supported input structures and pronunciation profiles only.

## Why beta is the right release target

The project will not wait indefinitely for external specialists who are unavailable. It may be released as a usable beta provided that engineering verification is separated from linguistic validation. Lack of annotators is not a reason to invent gold labels, infer accuracy, or silently widen phonological coverage.

## Beta promises

- The application runs using the repository's documented installation or published static-site workflow.
- Supported and unsupported inputs are distinguished; unsupported or incomplete structures fail closed rather than being silently dropped or guessed.
- The source-to-target pipeline and the separation between phonetic transcription and orthographic romanization are documented.
- Automated tests, generated-artifact checks, build checks and browser smoke checks are green on the exact release candidate commit.
- Every external data/model dependency used in the shipped runtime has a documented source, version and rights basis; uncleared candidate corpora are not bundled or redistributed.
- The UI and README visibly identify the output as a beta proposal and explain that pronunciation, dialect and lexical coverage may be incomplete.

## Explicit non-promises

- No claim of expert approval, official Ukrainian standard status, comprehensive coverage, or measured linguistic accuracy.
- No claim that a source-generated IPA label or agreement between G2P engines is adjudicated gold.
- No unsupported pronunciation is guessed merely to increase the number of successful outputs.
- No third-party dataset is copied into project gold or redistributed without item-level rights clearance.

## Beta acceptance gates

| Gate | Required evidence | If unmet |
|---|---|---|
| Engineering | Exact-HEAD CI green; package/site build and generated-data checks pass | Do not call that commit beta-ready |
| Runtime safety | Unsupported cases remain explicit; Python/browser contract tests pass where both runtimes exist | Keep affected forms withheld |
| Data and rights | Shipped assets have documented provenance and license; uncertain candidate data excluded | Exclude the asset |
| User-facing disclosure | README and app explain beta/provisional scope and limitations | Do not publish beta notice |
| Accessibility | Automated browser checks pass; manual QA status disclosed honestly | Label manual accessibility QA as not performed |
| Linguistic validation | Expert-adjudicated gold and measured accuracy | **Not a beta prerequisite**; show as not assessed |

## User-facing status vocabulary

- **SUPPORTED (beta):** the implementation has an explicit rule path and automated regression coverage. This is not a claim of expert validation.
- **PARTIAL / PROVISIONAL:** some structure is recognized, but one or more required phonetic features or contextual rules are unresolved.
- **UNSUPPORTED / NOT_ESTABLISHED:** the system withholds a result rather than guessing.
- **NOT VALIDATED:** no independent expert gold or measured accuracy is available.

## Deferred research (not a beta blocker)

- Independent expert annotation and adjudication.
- Gold-corpus construction and accuracy measurement.
- Completion of all contextual phonological inventories.
- Manual screen-reader, keyboard-only and mobile accessibility review.

## Release procedure

1. Update the beta status and known limitations in README and the master handoff.
2. Run all required workflows on the exact candidate commit; do not substitute older green runs.
3. Inspect generated artifacts and confirm no uncleared data/model assets entered the build.
4. Publish a beta release only after the repository owner explicitly authorizes publication.
5. Preserve this policy and record any later linguistic validation as a separate evidence milestone.
