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


## Final mainline closeout — 2026-11-21

PR #482 merged as `3ba0523a6e90bdba63a7c80693fbbdd2f0b3fdec`. Exact-main Quality [44906297076](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44906297076), Chromium/browser [44906297035](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44906297035), and Pages build/deploy [44906297037](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44906297037) all SUCCESS. The reproducible npm dependency gate remains DONE_VERIFIED.


## Final exact-main beta verification after PR #483 — 2026-11-21

PR #483 merged as `a6347577052ddf70d69364ed7cc90e2ff584ed2a`. Exact-main checks on this SHA all completed successfully: Quality [44906655301](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44906655301) SUCCESS; Khmer browser smoke [44906655362](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44906655362) SUCCESS; Pages build/deploy [44906655377](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44906655377) SUCCESS.

Engineering beta release gates are now verified on main, including reproducible npm installs, production browser smoke and deployed asset smoke. This does not close language-level PARTIAL items (vowel-context matrix, lexical segmentation, independent gold/accuracy) or manual accessibility TODO. No GitHub Release or public announcement was created.


## Final current-main verification — 2026-11-21

Latest main SHA: `192d280890e7f95d67a0486227edd540bfabcb26`. All three exact-SHA post-merge workflows completed successfully: Quality [44906966908](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44906966908), Chromium/browser [44906967032](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44906967032), Pages build/deploy [44906966960](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44906966960). This supersedes the prior exact-main verification at `a6347577052ddf70d69364ed7cc90e2ff584ed2a`.


## Final beta mainline verification after PR #485 — 2026-11-21

Latest main SHA: `3bd48fe41411a0378fb37b74a31b1768eb7bb4d8`. Exact post-merge Quality [44907271893](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44907271893), browser smoke [44907271876](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44907271876), and Pages build/deploy [44907271998](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44907271998) all SUCCESS. This supersedes the earlier exact-main checkpoint at `192d280890e7f95d67a0486227edd540bfabcb26`.
