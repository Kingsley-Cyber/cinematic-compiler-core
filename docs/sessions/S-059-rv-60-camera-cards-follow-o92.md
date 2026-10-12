# S-059 — RV-60: the camera cards follow O92, and the printed camera rules are checked

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-60 (PLAN-007); finding F-160; rulings O92, R-21, R-30, O102

## Layer
L5.5

## Status
applied

## Commit
the commit whose message names [S-059]

## Plan
The draft camera cards still teach what O92 struck ("Camera hold with both bodies in frame at 2.5, 4.7, 8.5. No
playback ramps. Hits are holds, not inserts."), and the prompts print two of those lines beside the hit holds:
1. library/camera_conventions: anime's "Cut close on the receiver after a blow lands." and live action's "Slow motion
   only around the peak of an action." struck; each card's playback list is [normal], as PLAYBACK_RAMP already
   requires of every shot (card_version 2, library log). live action's description loses its slow-motion clause.
2. library/camera_idioms/ninja.yaml: "Insert on the point of contact, then cut wide." when a blade lands, struck (the
   8.5 lodging is one of O92's holds); found in this slice, same contradiction.
3. The prompt validator reads the printed "Camera rules:" line too: a rule asking for slowed, ramped or frozen
   playback is PLAYBACK_RAMP's; a rule cutting close or to an insert on a blow, hit or impact is HIT_HOLD's.
4. A library test: no camera card lists playback other than normal, and no convention or idiom puts a close-up or an
   insert on a hit (the words are the check's interpretation).
5. Re-bind the camera plans whose packets move; regenerate the examples.

Predictions, made before the change (04:01 by the clock):
1. The gate passes before the change: 673 tests (3cfb984).
2. Before the card change, the new prompt checks refuse exactly the anime prose prompts (reference fight and wizard,
   four each) with HIT_HOLD and the live-action ones (four) with PLAYBACK_RAMP; the UGC prompts and every render.txt
   (no [CAMERA] rules line) pass.
3. After the change, the only prompt text that moves is the "Camera rules:" line of the twelve anime and live-action
   prose prompts (one sentence each); no camera shot, checklist verdict or UGC prompt changes.
4. The rebind moves the camera plan of all four examples (the cards are in S16's packet) and nothing else.
5. About 677 tests (673, two prompt break tests, two library tests).

## Decisions
- D1 — anime's close-up after a blow and live action's slow motion at a peak are struck, and the anime and live-action
  playback lists are [normal]. Level: covered (O92: "No playback ramps. Hits are holds, not inserts."; F-160).
- D2 — The ninja idiom's insert on a landing blade is struck too: found in this slice; a blade landing in a body is one
  of O92's hits (the 8.5 lodging is one of its three holds). Level: interpretation (F-053).
- D3 — The UGC card plays normal only, following PLAYBACK_RAMP's reach to every scene (S-050's reading, listed for the
  owner); its library entry is agent_fix, the three O92 cards' are owner. Level: interpretation (F-053).
- D4 — One function reads a camera rule for both codes, a sentence at a time, by words (slow motion, slowed, ramp,
  freeze; close or insert with blow, hit, impact, strike or contact); the prompt check and the card test share it.
  Level: interpretation (F-053).
- D5 — A rule that negates the words ("no slow motion") is flagged too; rules are written as what to do. Level:
  interpretation (the function's docstring).
- D6 — The knowledge map's C10 gains three locators and a note (map 10); four cards go to version 2 (library log).
  Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | PASS | `scripts/verify.sh` exit 0, 675 passed, check: PASS, after the last edit |
| One gap, right layer | PASS | the camera cards S16 reads (L5.5) and the prompt check of their printed rules; no other layer touched |
| Predictions written first | PASS | written 04:01, before any edit; prediction 2 measured on today's prompts before the cards changed |
| New checks fire and stay silent | PASS | the printed-rules check refused the eight anime and four live-action prose prompts before the card change and none of the sixteen after; the card test refuses each struck sentence |
| Tests changed with their data | PASS | `git diff -- tests`: two tests added, one import line widened; no test edited, skipped or deleted |
| Examples | PASS | the four camera plans re-bound (hashes); twelve prose prompts lose one sentence each; the checklists change only in hashes and sizes, every verdict count the same |
| Records | PASS | F-160 resolved; F-053 lists D2 to D4; four cards at version 2 (library log); map 10 (kernel log); docs/reference/library.md rebuilt; backlog, PLAN-007, CHANGELOG, run report |
| Hygiene | PASS | the scan before the push |
Claim corrected before the commit: the first gate run stopped on docs/reference/library.md, stale after the card
versions moved; `python -m kernel.build_docs` rebuilt it.

## Duration
about 7 minutes by the clock (03:58 to 04:05)

## Changes
- library/camera_conventions/anime.yaml, live_action.yaml, ugc_ad.yaml, library/camera_idioms/ninja.yaml (version 2;
  library log); docs/reference/library.md rebuilt
- validators/prompt_validator.py (`camera_rule_problems`; HIT_HOLD and PLAYBACK_RAMP read the printed camera rules)
- tests/test_prose_render.py, tests/test_camera_solver.py (one test each)
- the four examples' camera plans re-bound; the examples and checklists regenerated
- kernel/knowledge_map.yaml 10 (C10; kernel log); F-160 resolved; F-053 noted; backlog (RV-60 done, RV-61 next);
  PLAN-007; CHANGELOG; run report

## Verification
- before: S-058's gate at 3cfb984: `scripts/verify.sh` exit 0, 673 passed
- after: `scripts/verify.sh` exit 0, 675 passed, check: PASS
- Prediction 1 held. Prediction 2 held exactly (eight anime prompts HIT_HOLD, four live-action PLAYBACK_RAMP, the UGC
  ones and render.txt nothing). Prediction 3 held (one sentence gone from twelve prompts; no shot, verdict or UGC
  prompt moved). Prediction 4 held (the four camera plans). Prediction 5 held in part: 675, as two tests carry the
  four checks.
