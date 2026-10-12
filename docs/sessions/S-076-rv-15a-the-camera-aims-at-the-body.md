# S-076 — RV-15a: the camera aims at the body it frames, and every visible part is in frame vertically

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-15 (split: RV-15a here, RV-15b the insert's detail; PLAN-007); findings F-090, F-145 (moved to RV-15c, D5);
rulings O72, O92

## Layer
L5.5

## Status
applied

## Commit
the commit whose message names [S-076]

## Plan
S-027 moved every root to the pelvis (O72) but S16 still aims 1 m above the root (camera_grammar aim_height_m), and
only the horizontal screen position is judged: the cameras aim over the fighters' heads and parts fall out of frame
(F-090; reviews 1, 3, 4 and 5). The class: where every shot aims, and whether what its scale shows is in its frame.
1. S16's packet carries each slot's body points (forward kinematics of the S13 keys); a shot aims at the centre of the
   points its scale shows (the grammar's visible_parts) of its target (the midpoint of both for `midpoint`).
2. VERTICAL_FRAMING (new, S16): every point a shot's scale shows of each subject projects inside the frame, up and
   down as well as across.
3. Shots it refuses are re-authored in their distance, elevation or lens; the prose changes only where a shot does.
4. RV-15b keeps the inserts' detail aim.

Predictions, made before the change (07:05 by the clock):
1. The gate passes before the change: 699 tests (0e0ce9e).
2. With the aim at the centre of the visible parts, VERTICAL_FRAMING still refuses some shots: between three and ten
   in the reference fight (its low bodies at 6.6, 8.5 and 9.0 among them), fewer than three in each other example.
3. Every example's render.txt changes (it prints the derived camera positions); a prose prompt changes only where a
   shot is re-authored; checklist counts stay.
4. About 701 tests (699, a VERTICAL_FRAMING test, an aim test).

## Decisions
- D1 — The aim is the middle of the extent of the shown points on each axis, not their mean: measured, the mean leans
  toward the arms and hands (six upper-body points against four of the legs) and refused seven of the fight's shots,
  the middle six. Level: interpretation (F-053).
- D2 — A subject's screen x is its pelvis's, O72's root (before: the root lifted by aim_height_m): the centre of its
  shown parts read a reaching hand as the subject's place and refused seven of the fight's placements, the pelvis
  five. Level: interpretation (F-053).
- D3 — A static shot is checked at every beat it lists, from the camera S16 derives at its first; a moving shot at its
  first only, since S16 does not model a camera's path (F-090 stays open for it). Level: interpretation (F-053).
- D4 — Each refused shot was re-authored with the least printed change: the distance (prose does not print it) within
  the scale's frame height, then the placement, then the lens or the angle; two needed a wider scale (the fight's c02
  extreme_wide: A on the pillar's top at 8 m and B below; c19 medium_wide: A on the ground, B standing). The
  live-action shot and reverse shot keep one lens (60 mm at 2.5 m), as authored. Level: covered (plan step 3).
- D5 — RV-15 split: RV-15a (this), RV-15b (an insert's detail, a framed prop, and the camera schemas' `position` text,
  which still reads "target + aim height": one major bump with the insert's aim), RV-15c (F-145's body aim at S13,
  blocked on F-148: it would refuse the golden's own rows, O10). Level: covered (R-06 for RV-15c).
- D6 — The grammar's visible_parts stay what a scale shows: a medium close-up lists both hands, so it must hold hanging
  hands, near its widest frame (1.0 m). Whether it should is the library's question, flagged in F-053. Level:
  interpretation.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the chained gate commits |
| One gap, right layer | PASS | S16 (L5.5) reads S13's keys through its packet; S13 and the motion untouched |
| Predictions written first | PASS | the session file was written at 07:05, before any code |
| New checks fire and stay silent | PASS | before the re-authoring: refusals in 6, 2, 2 and 1 shots; after: none in the four examples; tests: c06's old values refused, a head raised at c11's last beat refused at b14, the courtyard passes |
| Neighbours | PASS, with carriers | contact moments out of their shot's frame (measured from the envelopes): the fight 15 of 28 before, 0 after; the wizard 3 of 7, 0 (2 have no key at their instant); the UGC 1 of 3, 0; the source's "ground level" shots 1.90 and 1.14 m high before, 0.72 and 0.19 m after; c01 still frames A from frame 0 (F-202); inserts, framed props and the schemas' position text (RV-15b); a moving shot's later beats (F-090); F-145 (RV-15c) |
| The step's instructions teach it | PASS | camera_selection.txt: the aim, VERTICAL_FRAMING, the pelvis placement, the remedy (distance, lens, angle) |
| Tests changed with their data | PASS | `git diff -- tests`: two new tests and two assertions in the geometry test; nothing removed or loosened |
| Examples | PASS | sixteen shots re-authored in the four camera plans, rebound; render.txt changes in all four, the prose only at the six shots whose printed fields changed; checklist counts the same |
| Records | PASS | F-090 open in part (RV-15b); F-145 to RV-15c; F-053; map 15 and 16 (kernel log 72, 73); backlog 29; PLAN-007; CHANGELOG; run report |
| Hygiene | see Verification | the scan's count copied below |
Claims corrected before the commit: the kernel log's entry 72 recorded the map at version 15 before its locator was
added (the edit script stopped after the bump); entry 73 records version 16 with it, and no log line was edited. The
first draft of the records counted twelve re-authored shots in the fight and fifteen in all; it is eleven and sixteen.

## Duration
from 07:05 (the plan) to 07:41 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- solver/camera_geometry.py (`screen_xy`); compiler/passes/derived/p16_camera.py (the packet's `points`)
- validators/camera_validator.py (`shown`, the aim, the pelvis's screen x, `_framing`: VERTICAL_FRAMING)
- planner/prompts/camera_selection.txt (S16's instructions)
- tests/test_camera_solver.py (two tests; `screen_xy` in the geometry test)
- the four examples' camera plans (sixteen shots), rebound and regenerated; their checklists; docs/reference rebuilt
- kernel/knowledge_map.yaml 15 and 16 (C10's VERTICAL_FRAMING locator)
- backlog 29 (RV-15a done, RV-15b next, RV-15c blocked); F-090; F-145; F-053; PLAN-007; CHANGELOG; run report

## Verification
- before: S-075's gate at 0e0ce9e: 699 passed
- Prediction 1 held. Prediction 2 held in part: VERTICAL_FRAMING refused six of the fight's shots (c02, c05, c11, c12,
  c19, c20) and two, two and one in the others, as predicted, but of the named instants only 8.5 was among them (with
  8.0); 6.6 and 9.0 passed. Not predicted: the moved aim moved the subjects' screen x, so CAMERA_COMPOSITION refused
  five shots and CAMERA_COUPLING two. Prediction 3 held (render.txt in all four; the prose only at re-authored shots;
  the checklist counts the same). Prediction 4 held (701). Predictions 3.5 of 4.
- `make golden`'s steps: `python -m compiler.examples` exit 0, its three golden test files 32 passed;
  `python -m compiler.rebind` (report) exit 0
- the gate on this record (07:41:25): `scripts/verify.sh` exit 0, 701 passed in 75.07 s, docs plane: PASS, check:
  PASS (the run before it, at 07:39:49, failed one test: docs/index/sessions.md was stale; regenerated)
- the hygiene scan over the staged diff: 0 hits
