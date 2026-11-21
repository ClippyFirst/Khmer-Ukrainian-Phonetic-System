# Khmer public beta release checklist
## Public beta release gate

- [ ] Exact candidate SHA has successful Quality, browser smoke, and Pages build/deploy workflows.
- [ ] `npm ci` is used in CI and `package-lock.json` is committed.
- [ ] Python test suite, web tests, production build, coverage-report reproducibility and production Chromium smoke pass on the exact candidate SHA.
- [ ] The live Pages deployment serves both pages and their versioned JavaScript/CSS assets.
- [ ] README and both public pages label the project as a beta and distinguish proposed output from validated facts.
- [ ] Every shipped third-party runtime dependency has a version, integrity hash, declared license, upstream locator and documented role; unclear data/model sources remain excluded.
- [ ] No user text is sent to a server, telemetry provider or analytics endpoint; unsupported units remain visible.
- [ ] Expert gold and measured accuracy are explicitly NOT ASSESSED, not fabricated.
- [ ] Manual accessibility QA is explicitly disclosed as not performed; automated browser smoke is not called WCAG certification.

## Current beta acceptance record — 2026-11-21

This checklist is a beta gate, not a claim that every gate is already satisfied. PR #481 merged as `355409a47feb8987cc655ca62dbad41ce8ff043d`. Exact post-merge main checks all passed on that SHA: Quality [44905912782](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44905912782), Pages build/deploy [44905912768](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44905912768), and production Chromium browser smoke [44905912797](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44905912797). The committed npm lockfile and `npm ci` are now the canonical dependency installation path. The original language-level limitations remain disclosed in `docs/BETA-RELEASE-POLICY.md` and `docs/limitations.md`.

## Commands

```bash
python -m pytest -q
python scripts/coverage.py --check
npm ci --no-audit --no-fund
npm run check
npm run build
npm run test:browser
```

Run the full command set on a clean checkout of the exact candidate commit. Record each command separately. A successful GitHub Actions workflow is valid evidence only for the commands that workflow actually ran.
