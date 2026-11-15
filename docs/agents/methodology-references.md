# Adopted engineering and design references

**Review date:** 2026-11-15  
**Purpose:** record which practices from the five requested upstream repositories are adopted, how they are constrained by this project's research contract, and what is deliberately not imported.

These repositories are methodology references. They are not runtime dependencies, source-language authorities, IPA sources, or permission to copy third-party code/data into this repository.

## Reference register

| Upstream | Snapshot reviewed | Practices used here | Explicit non-adoption |
|---|---|---|---|
| [Leonxlnx/unlazy](https://github.com/Leonxlnx/unlazy) | `16671491f6679ad9378f52604d3bc2415b4120c7` | Acceptance ledger before substantial work; runnable, explicit gates; rerun relevant checks on the final state; report only supported outcomes. | No copied gate runner, hooks, templates or runtime dependency. Do not treat an agent-written status line as test evidence. |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | `d643997c82e94742dd3bee43210b0198e8bbba3d` | Structured UI direction, information hierarchy, responsive layout, typography, contrast, interaction states and accessibility checks as design-review prompts for the web service. | No wholesale import of its style/rule catalogue, generated assets, CLI, or design database. UI polish must not obscure uncertainty or imply linguistic confidence. |
| [obra/superpowers](https://github.com/obra/superpowers) | `22f0b463e7a5e579904dd6211a520321035526f7` | Test-first regression work, explicit problem/acceptance criteria, small implementation steps, root-cause debugging, review and full-suite verification. | No imported agent harness, helper scripts, plugins or SDD runtime. A separate design-approval ceremony is not added when the owner has explicitly authorized autonomous execution. |
| [mattpocock/skills](https://github.com/mattpocock/skills) | `5863806dd4e15c63174bee4e7515a4256792ecfa` | Small composable practices; behavior-focused tests; clear interfaces and test seams; source-backed research; keep project-specific instructions concise. | No wholesale skill pack or duplicate process framework. Existing `AGENTS.md`, master handoff and test architecture remain authoritative. |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | `96608e078b2d5ea607c5c3b8b5a54d1c1fba6846` | Trace actual entry points and data flow; inspect the surrounding code, not only a diff; protect trust boundaries, data preservation and accessibility; test parser/branching behavior; disclose skipped checks and residual risk. | No copied implementation or agent runtime. Apply only the engineering/audit practices relevant to this repository. |

## Precedence and conflict resolution

1. User-approved project scope and the repository's explicit research contract.
2. `AGENTS.md`, the canonical master execution plan/handoff, and current completion/audit registers.
3. Existing schemas, source registries, canonical data and executable tests.
4. The upstream practices listed above, only where compatible.

In particular, none of these engineering references can authorize an IPA guess, promote source-attested examples to independent gold, resolve data licensing, or turn a proposed Ukrainian spelling into an official standard.

## How to apply the practices

For each substantial task:

1. State the observable acceptance criteria and status using `DONE_VERIFIED`, `PARTIAL`, `TODO`, `BLOCKED` or `DEFERRED`.
2. Trace the real code/data path and identify the canonical source of truth before editing.
3. Add a regression that fails for the intended reason when practical; then implement the smallest complete correction.
4. Run the complete relevant project suite and generators; inspect generated-artifact drift.
5. Recheck the exact final commit and report commands, workflow evidence, unavailable checks and residual uncertainty.
6. For UI changes, review hierarchy, keyboard/focus behavior, contrast, responsive behavior, visible status/uncertainty and screen-reader semantics. Do not claim manual QA unless it was performed.

## Change control

This register records reviewed upstream snapshots, not a promise to track every upstream commit. Refresh a reference only when a change materially affects an adopted practice. Record the new exact commit and the changed practice; do not automatically import upstream updates.
