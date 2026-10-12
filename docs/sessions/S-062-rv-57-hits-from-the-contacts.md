# S-062 — RV-57: hits found from the contacts are camera holds at S16, S17 and in the prompt, whatever S17 holds

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-57 (PLAN-007); findings F-155, F-015; rulings O92, R-21, O93, O102

## Layer
L5.5

## Status
applied

## Commit
the commit whose message names [S-062]

## Plan
O92 says hits are camera holds ("Camera hold with both bodies in frame at 2.5, 4.7, 8.5 ... Hits are holds, not
inserts"), but HIT_HOLD judges only the holds S17's author placed on impact frames, so a scene with no authored hold
escapes it, and S16, which ADR-O92 named and which sees the contacts, checks nothing (F-155).
1. One function finds the hits from the contacts (planner/hits.py): a touch on another performer's body; a strike,
   deflect or parry on a prop another performer holds or threw; a catch of another performer's body; a body touched by
   a prop another performer holds that affords stab. Each hit owes a camera hold on every body present then.
2. S16's packet lists the hits, and the camera validator refuses a hit whose shot moves, is a close-up or an insert,
   or leaves out a body present (HIT_HOLD at S16); the S16 instructions say so.
3. S17's `hit_hold`, the prose's "Holds on hits:" and the prompt's HIT_HOLD judge the hits from the contacts as well
   as S17's holds on impact frames. The vertical framing stays RV-15's.

Predictions, made before the change (04:34 by the clock):
1. The gate passes before the change: 680 tests (af06251).
2. The contacts give these hits: the reference fight's 2.5 (A's foot on the kunai B threw), 4.7 (A's knee on B),
   6.6 (B's two catches of A's arm) and 8.5 (B touched by the kunai A holds); the wizard's 3.6 (the acrobat's foot on
   the wizard); none in live action or the UGC. Every shot covering one is already a static hold on both bodies.
3. F-155's probe (the 4.7 hold dropped from S17's frame parts, its shot a handheld whip pan on A alone) passes S16 and
   S17 today; after the change S16 refuses it with HIT_HOLD, and S17 and the prompt do too.
4. The rebind moves exactly the four camera plans (S16's packet gains the hits); no prompt text changes.
5. About 684 tests (680; one hits test; the S16, S17 and prompt probes).

## Decisions
- D1 — A hit is one of four contacts, read from F-155's list: a touch on another performer's body, whatever its verb;
  a strike, deflect or parry on a prop another performer holds, or threw and no one holds; a catch of another
  performer's body; a body touched by a prop another performer holds that affords stab. Level: interpretation
  (F-053).
- D2 — S16's HIT_HOLD judges what S17's did: the shot is static, lists every body present among its subjects (whose
  projection S16 already checks) and is no close-up or insert; the vertical framing stays RV-15's. Level: covered
  (F-155's fix).
- D3 — The holds owed are the hits from the contacts together with S17's holds on impact frames, one per frame, so no
  hit S17 alone found is lost (the wizard's 5.2). Level: covered (F-155: "whatever S17 holds").
- D4 — Hits are judged in every genre, as PLAYBACK_RAMP is; live action and the UGC have none today. Level:
  interpretation (F-053).
- D5 — The S16 instructions name the packet's `hits` and what each owes. Level: covered (F-162's rule: the
  instructions follow the code).
- D6 — Knowledge map 12: three HIT_HOLD locators. Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | PASS | `scripts/verify.sh` exit 0, 684 passed, check: PASS, after the last edit |
| One gap, right layer | PASS | the hits defined once (planner/hits.py) and judged at S16, where the camera is authored, as at S17 and in the prompt |
| Predictions written first | PASS | written 04:34, before any edit; the hits list and F-155's probe measured, the probe with the old S17 kept beside the new |
| New checks fire and stay silent | PASS | the probe (4.7 hold dropped, a whip pan on A alone) passes the old S16 and S17 and is refused by the new; every example's hits were already holds, so nothing else fired |
| Tests changed with their data | PASS | `git diff -- tests`: four tests added (one new file), one import added; no test edited, skipped or deleted |
| Examples | PASS | the four camera plans re-bound (hashes only, twice: the S16 instructions changed after the first); no prompt, checklist or other plan changed |
| Records | PASS | F-155 resolved; F-015 and F-053 noted; map 12 (kernel log); docs/reference rebuilt; backlog (RV-57 done, RV-58 next); PLAN-007; CHANGELOG; run report |
| Hygiene | PASS | the scan before the push |
Claim corrected before the commit: the predictions' time first read 04:39; the clock said 04:34, and the file says so.

## Duration
about 9 minutes by the clock (04:30 to 04:39)

## Changes
- planner/hits.py (new: `hits`, `hold_times`); validators/camera_validator.py (`_hit_holds`); compiler/passes/derived/
  p16_camera.py (the packet's `hits`) and p17_render.py (`hit_hold` over the hold times); renderers/prose_renderer.py
  (the printed holds); validators/prompt_validator.py (the prompt's HIT_HOLD over the hold times)
- planner/prompts/camera_selection.txt (the hits)
- tests: test_hits.py (new), test_camera_solver.py, test_render.py, test_prose_render.py (one test each)
- the four camera plans re-bound; the examples regenerated
- kernel/knowledge_map.yaml 12 (kernel log); F-155 resolved; F-015, F-053 noted; docs/reference rebuilt; backlog;
  PLAN-007; CHANGELOG; run report

## Verification
- before: S-061's gate at af06251: `scripts/verify.sh` exit 0, 680 passed
- after: `scripts/verify.sh` exit 0, 684 passed, check: PASS
- Prediction 1 held. Prediction 2 held exactly (the reference fight's 2.5, 4.7, 6.6 twice and 8.5; the wizard's 3.6;
  none in live action or the UGC). Prediction 3 held (S16 and S17 passed the probe and now refuse it; the prompt too).
  Prediction 4 held (the four camera plans, hashes only). Prediction 5 held (684).
