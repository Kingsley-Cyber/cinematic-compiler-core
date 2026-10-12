# S-077 — RV-15b: an insert aims at its detail, a framed prop is in frame, and the camera schemas name the aim

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-15b (PLAN-007); finding F-090 (the rest of it); rulings O72, O92

## Layer
L5.5

## Status
applied

## Commit
the commit whose message names [S-077]

## Plan
After RV-15a an insert still aims aim_height_m above its target's pelvis: the UGC's c02 ("close on the hands and the
glasses") aims at 1.97 m, over the creator's head, in a frame 0.3 m tall. A prop a shot frames has no position in
S16's packet, so nothing checks it is in frame, and the camera schemas still say the aim is "target + aim height".
The class: what each shot aims at and whether everything it frames is in its frame, for the subjects RV-15a left out
(an insert's detail, a framed prop).
1. S16's packet carries each prop's point at every beat: its sample at that instant, else its grip hand while held,
   else its flight or rest from its last sample; none while carried or unplaced.
2. An insert aims at its detail: a part of its target (forward kinematics, the contact-point names) or a prop; a
   detail that is neither is refused (CAMERA_VOCABULARY). In an insert, the target's place on screen is its detail.
3. VERTICAL_FRAMING also covers an insert's detail and every framed prop with a point; a framed prop's screen x feeds
   the coupling and composition checks as a body's does.
4. The camera node schema's `position` text names the aim; camera, camera_graph and camera_plan go to 2.0 (the
   meaning of `distance_m` changed in RV-15a: docs/versioning.md); S16's packet names camera_plan 2.0.
5. A moving camera's path stays unmodelled: filed as its own finding with a slice, so F-090 can close.

Predictions, made before the change (07:48 by the clock):
1. The gate passes before the change: 701 tests (f5e4992, S-076's chained gate).
2. The UGC's c02 aims at the creator's right hand, between 0.9 and 1.4 m high, from 1.97 m; as authored it passes
   every S16 check (the glasses are in that hand, inside the 0.3 m frame).
3. No other shot is refused: the UGC is the only example that frames a prop (the glasses, in all four shots), and
   the glasses lie inside each of those frames.
4. The envelopes change in all four examples (the camera plans' packet hashes); render.txt only in the UGC (c02's
   camera); no prose prompt changes; checklist counts stay.
5. About 704 tests (701 and three: the insert's aim, a framed prop out of frame, a detail that names nothing).

## Decisions
- D1 — A prop's point at a beat is its sample at that instant (the post one of a pair), else the point of the hand
  that holds it, else its flight from its last sample toward a later one, else its rest at its last sample; a prop
  carried on a body, unplaced, or flying past its last sample has none and is not checked. Level: interpretation
  (F-053).
- D2 — An insert's detail names a part of its target by forward kinematics' contact points (palm, fingers and fist
  read as the hand; chest, back, spine and shoulder as the torso) or a prop; anything else is refused
  (CAMERA_VOCABULARY), and in an insert the target's place on screen is its detail. Level: interpretation (F-053).
- D3 — camera, camera_graph and camera_plan go to 2.0: RV-15a changed what `distance_m` measures from, a meaning
  change (docs/versioning.md); S16's packet names camera_plan 2.0. Level: covered (agent_fix in the schema log).
- D4 — A moving camera's path is its own gap (F-204, RV-94), so F-090 closes; c01's opening stays with the owner
  (F-202). Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the chained gate commits |
| One gap, right layer | PASS | S16 (L5.5): the packet reads the S04 samples, the S07 holds and the S13 keys; nothing upstream changed |
| Predictions written first | PASS | the session file was written at 07:48, before any code |
| New checks fire and stay silent | PASS | the four examples pass; tests: an insert on the wizard's right hand aims at it, a detail "aura" is refused, a framed prop 4 m above the hand is refused |
| Neighbours | PASS | every insert and framed prop in the examples (the UGC's, the only ones); the coupling (an insert's contacts are its detail's) and the faces (an insert on the head) unchanged; render.txt prints the insert's new camera, the prose prints no camera position; the schemas' text and docs/reference; a moving camera's path filed (F-204) |
| The step's instructions teach it | PASS | camera_selection.txt: the insert's detail, the prop points, the places on screen |
| Tests changed with their data | PASS | `git diff -- tests`: two new tests; nothing removed or loosened |
| Examples | PASS | the four camera plans rebound (the packet's instructions and schema id); render.txt only in the UGC; no prose changed; checklist counts the same |
| Records | PASS | F-090 resolved; F-204 and RV-94 new; F-053; map 17 (kernel log); schemas 2.0 (schema log); backlog 30; PLAN-007; CHANGELOG; run report |
| Hygiene | see Verification | the scan's count copied below |

## Duration
from 07:48 (the plan) to 07:53 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- compiler/passes/derived/p16_camera.py (`prop_points`; the packet names camera_plan 2.0)
- validators/camera_validator.py (`framed`, `_detail`, `_place`; an insert's aim; the detail's reference check)
- schemas/camera.schema.json, schemas/graphs/camera_graph.schema.json, schemas/graphs/camera_plan.schema.json (2.0)
- planner/prompts/camera_selection.txt; tests/test_camera_solver.py (two tests)
- the four examples' camera plans rebound and regenerated; the UGC's checklist; docs/reference rebuilt
- kernel/knowledge_map.yaml 17 (C10's note); backlog 30 (RV-15b done, RV-14 next, RV-94 new); F-090 resolved; F-204
  (new); F-053; PLAN-007; CHANGELOG; run report

## Verification
- before: S-076's chained gate at f5e4992: 701 passed
- Prediction 1 held. Prediction 2 held (c02 aims at [0.138, 1.121, 0.287], 1.12 m high; as authored it passes).
  Prediction 3 held (no shot refused in the four examples). Prediction 4 held (the four envelopes; render.txt only
  in the UGC; no prose; the UGC checklist's counts the same). Prediction 5 held in part: the three cases are tested,
  in two tests (the detail that names nothing is an assertion in the insert's test), so 703, not 704. Predictions
  4.5 of 5.
- the gate on this record (07:53:36): `scripts/verify.sh` exit 0, 703 passed in 75.16 s, docs plane: PASS, check:
  PASS
- the hygiene scan over the staged diff: 0 hits
