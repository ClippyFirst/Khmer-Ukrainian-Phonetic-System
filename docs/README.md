# Documentation index

This is the navigation map for the repository. It does not replace the canonical task ledger or source registries.

## Start here

1. [README](../README.md) — project purpose, status, usage and top-level orientation.
2. [Agent instructions](../AGENTS.md) — non-negotiable implementation, linguistic and verification rules.
3. [Architecture](architecture.md) — runtime boundaries and authoritative data ownership.
4. [Codebase map](agents/codebase-map.md) — entry points, call paths and high-risk seams.
5. [Master execution plan and chat handoff](MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md) — canonical task ledger, evidence history, blockers and next work.
6. [Repository audit](repository-audit.md) — inventory decisions and cross-cutting audit findings.

## System specification and methodology

- [Methodology](methodology.md) — research method and evidence hierarchy.
- [System specification](system-specification.md) — system scope and expected behavior.
- [Phonology](phonology.md) — Khmer phonological analysis and open questions.
- [Deterministic rule engine](DETERMINISTIC-RULE-ENGINE.md) — actual engine contract and limitations.
- [Implementation](implementation.md) — implementation details.
- [Validation](validation.md) — engineering and linguistic validation boundaries.
- [Limitations](limitations.md) — unsupported and unresolved cases.
- [Glossary](../GLOSSARY.md) — project terminology.

## Canonical data, matrices and evidence

- [Evidence policy and provenance](evidence.md) — evidence types, source quality and provenance expectations.
- [References](references.md) — source bibliography and research references.
- [Khmer → Ukrainian romanization matrix](romanization-to-ukrainian-matrix.md) — separate orthographic BGN/PCGN-derived route and its partial target crosswalk.
- `data/khmer/sources.json` — machine-readable source registry.
- `data/khmer/*.json` — canonical Khmer orthographic, register and rule registries.
- `data/ukrainian/practical-policy.json` — canonical proposed IPA → Ukrainian target policy.
- `data/khmer/romanization*.csv` — canonical orthographic romanization crosswalk tables.
- `data/tests/` — structural, adversarial and source-attested fixtures; not automatically adjudicated gold.

## Phonetic corpus and external candidates

- [IPA gold corpus protocol](ipa-gold-corpus.md) — record lifecycle, provenance and acceptance rules.
- [IPA gold collection playbook](ipa-gold-collection-playbook.md) — controlled collection and adjudication workflow.
- [Phnom Penh phonetic literature full-text review](ipa-gold/khmer-phonetic-literature-fulltext-review-2026-11-17.md) — source-level limits and locators for Chem (2020) and Mam et al. (2025).
- [Benchmarking and external IPA](benchmarking-and-external-ipa.md) — candidate diagnostics and evaluation boundaries.
- [External IPA renderers](external-ipa-renderers.md) — external tool/resource inventory.
- [Current external corpus triage](audits/current/EXTERNAL-PHONETIC-CORPUS-TRIAGE-2026-11-01.md).
- [Current Khmer vowel × series × coda evidence matrix](audits/current/KHMER-VOWEL-SERIES-CODA-EVIDENCE-MATRIX-2026-11-01.md).
- [Current phonology research workpack](audits/current/PHONOLOGY-RESEARCH-WORKPACK-2026-11-01.md).
- [Current linguistic completion register](audits/current/LINGUISTIC-COMPLETION-REGISTER-2026-11-01.md).

## Audit history and plans

- [Current repository audit](repository-audit.md).
- [Historical audits](audits/) — dated evidence and issue-specific audit snapshots.
- [Research work](research/) — bounded external G2P and engine-coverage investigations.
- [Engineering plans and specifications](superpowers/) — dated plans/specifications retained as project history; they do not supersede the current handoff.
- [Agent operations](agents/) — codebase map, issue-tracker conventions and reviewed methodology references.

## Repository layout

```text
.github/workflows/   CI, browser smoke, Pages and opt-in diagnostic workflows
data/
  benchmark/         annotation, adjudication, split, rights and prediction records
  comparative/       comparative practical-transcription evidence
  khmer/             Khmer source inventories, rules and romanization matrices
  tests/              shared structural, adversarial and lexical fixtures
  ukrainian/          proposed IPA → Ukrainian target policy
docs/
  agents/             agent operating guidance and code navigation
  audits/current/     current evidence matrices and completion register
  research/           bounded research workpacks
  superpowers/        historical plans/specifications
public/reports/       generated report served by the static site
reports/              canonical generated report copy
schemas/              JSON/data contracts
scripts/               validators, generators and benchmark tools
src/                   Python package and browser implementation
tests/                 Python, Node and Playwright regression suites
```

## Source-of-truth rules

- Runtime mapping data lives in the canonical registries, not duplicated UI constants.
- The master handoff is the sole canonical continuation ledger; the completion register is its focused linguistic status companion.
- Dated plans and audit snapshots are historical evidence. Do not edit them to pretend old decisions happened later; append a dated reconciliation to the canonical live documents.
- A test file is not verification evidence until it passes on the exact final code state.
- Generated reports are outputs, not independent source evidence.
