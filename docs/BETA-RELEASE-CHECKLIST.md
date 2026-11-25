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


## Final exact-main beta verification after PR #486 — 2026-11-21

Latest main SHA: `c836bb80236d2b1d68f68bbda88cacdfe2cdac75`. Exact post-merge Quality [44907687986](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44907687986), browser smoke [44907687995](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44907687995), and Pages build/deploy [44907688074](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44907688074) all SUCCESS. This supersedes the prior exact-main verification at `3bd48fe41411a0378fb37b74a31b1768eb7bb4d8`.


## Final beta verification after PR #487 — 2026-11-21

Latest main SHA: `2f4c0c1ca471b0ddd7444c17bb6d1a696fac9ec4`. Exact post-merge Quality [44908008375](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44908008375), browser smoke [44908008378](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44908008378), and Pages build/deploy [44908008449](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44908008449) all SUCCESS. This supersedes the previous exact-main verification at `c836bb80236d2b1d68f68bbda88cacdfe2cdac75`.


## Final exact-main Khmer beta verification after PR #488 — 2026-11-21

PR #488 merged as `866a5439f75d6f67e61a1781cbfccf8c77d9e9d7`. All three post-merge workflows passed on this exact main SHA: Quality [44908337364](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44908337364) SUCCESS; browser smoke [44908337384](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44908337384) SUCCESS; Pages build/deploy [44908338049](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44908338049) SUCCESS. This supersedes the prior exact-main checkpoint on `2f4c0c1ca471b0ddd7444c17bb6d1a696fac9ec4`.

KHM-BETA-ENGINEERING-001 remains DONE_VERIFIED. The exact mainline build, browser, quality and deploy gates are green. Independent expert gold remains 0 and accuracy null (DEFERRED for beta); vowel/context and lexical segmentation remain PARTIAL/BLOCKED as documented; manual accessibility remains TODO; third-party sources with unresolved rights, including MekongPhon, remain excluded. No new IPA labels, gold rows, linguistic rules or GitHub Release were added.


## Final exact-main verification after PR #491 — 2026-11-21

PR #491 merged as `112dd9a55f0dce1843ecd9ba6be272fa1335d586`, refreshing the visible beta status date and making the research-status notice explicitly distinguish engineering verification from pronunciation accuracy. Exact post-merge Quality [44908801606](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44908801606) SUCCESS; browser smoke [44908801669](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44908801669) SUCCESS; Pages build/deploy [44908801630](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44908801630) SUCCESS on this SHA.

This is the latest verified public beta mainline. Engineering/deployment status DONE_VERIFIED; independent expert IPA gold remains 0 and accuracy null; phonological and lexical segmentation coverage remain PARTIAL; manual accessibility QA remains TODO; uncleared third-party sources remain excluded. No gold data or linguistic claims were added.


## Final exact-main beta verification after methodology-page PR #494 — 2026-11-21

PR #494 merged as `877977a215b06eba2a79d19bf38283f39ffb8371`. It updates the methodology page with the public-beta status snapshot, the engineering-vs-linguistic validation distinction and direct beta policy/checklist links. All exact-main post-merge workflows passed: Quality [44909455274](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44909455274) SUCCESS; browser smoke [44909455237](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44909455237) SUCCESS; Pages build/deploy [44909455234](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44909455234) SUCCESS.

This is the latest verified Khmer public beta mainline. Engineering/deployment DONE_VERIFIED; expert gold=0 / accuracy=null; vowel/context and lexical segmentation PARTIAL; manual accessibility TODO; MekongPhon and other uncleared sources excluded. No IPA labels, gold rows or unsupported rules were added.


## Final Khmer public beta mainline closeout — 2026-11-21

Latest main SHA: `32b16b328f0433e30df6f3b1c4c5f7daa8ae59b5`. PR #495 merged the final exact-main evidence record and the methodology-page beta disclosure. Post-merge Quality [44909748314](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44909748314) SUCCESS (447 Python tests + 70 subtests; web checks/build passed); browser smoke [44909748266](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44909748266) SUCCESS (21 Chromium tests); Pages build/deploy [44909748262](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System-/actions/runs/44909748262) SUCCESS (production Chromium and deployed HTML/JS/CSS smoke).

The README now links the beta checklist and policy; the landing page and methodology page show the 21 November beta status snapshot and distinguish engineering verification from linguistic validation. Engineering beta gate DONE_VERIFIED. Independent expert IPA gold remains 0 and accuracy null; vowel/context and lexical segmentation coverage remain PARTIAL/BLOCKED; manual accessibility remains TODO; MekongPhon and other uncleared third-party sources remain excluded. No IPA labels, gold rows, unsupported runtime rules or GitHub Release were added.


## Superseding beta status — browser-local MekongPhon model (2026-11-25)

This section supersedes the 21 November historical notes above that listed MekongPhon as excluded. PR #578 merged as `520a1592345ccabbf859bc88f024485631306f73`; documentation closeout PR #579 merged as `a23412eb5ec17568d49d65fd86a1d69a94dcce65`.

- The public site now includes a user-triggered, browser-local MekongPhon IPA candidate. It is not an inference API: user text stays in the browser and only same-origin static model/runtime assets are fetched after explicit action.
- The pinned model artifact `byumatrixlab/khmer-ipa` revision `20e069d384b240da76320e1569958568c12a54bc` declares Apache-2.0 in its upstream model-card metadata. The upstream training/evaluation corpus is not copied or redistributed; corpus rights remain unresolved.
- ONNX Runtime Web 1.23.2 is vendored with verified npm integrity and its MIT notice. The shipped INT8 encoder/decoder weights total 35,001,440 bytes; FP32 graphs are validation-only.
- Model output is a separate PROVISIONAL candidate, profile match UNVERIFIED, and never promoted to canonical IPA or gold. Independent expert IPA gold remains 0 and pronunciation accuracy remains NOT ASSESSED.
- Exact-main Quality [45624955916](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45624955916), browser smoke [45624955945](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45624955945), and Pages build/deploy with deployed model/runtime asset smoke [45624955965](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45624955965) all passed. Model-enabled Chromium inference passed 46/46 Playwright tests in [45624434366](https://github.com/ClippyFirst/Khmer-Ukrainian-Phonetic-System/actions/runs/45624434366).

The beta remains research-grade. The model integration closes an engineering/runtime gap; it does not close the independent IPA gold, pronunciation-accuracy, corpus-rights or manual accessibility gates.
