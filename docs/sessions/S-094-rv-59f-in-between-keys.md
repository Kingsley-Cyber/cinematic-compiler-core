# S-094 — RV-59f: in-between keys at S13 (ADR-O109)

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-59f (PLAN-007); ADR-O109 (owner_default, S-090); findings F-220, F-159; rulings R-18, O72, O18; the DAG's
density rules (docs/sources/knowledge_dag_v1.md:253-261)

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-094]

## Plan
ADR-O109 lets the repo add explicit keys between two of an entity's keys on its own side, where the declared
interpolation draws a body through another or under the floor. S13 holds one key per entity per beat; nothing can
stand between. The construct, here; its printing in every prompt is RV-59i, before RV-59e's first use.
1. The motion plan may carry `inbetweens` (motion_plan 2.1): one entity's pose (pos, rot, bones, a name and a
   description) at an instant strictly between two of its consecutive keys, on a frame of its own; no beat, no
   contact, no anchor.
2. S13 checks each like a key: its span (INBETWEEN_SPAN: between two consecutive keys of its entity, not on a key's
   frame or another in-between's), the kernel joints and their limits, its root's speed to its neighbours (under
   TELEPORT's 25 m/s), the floor at its instant (FLOOR_PENETRATION), and the other bodies there, posed as they are
   (BODY_OVERLAP). Within a declared turn it carries the span's turn.
3. The graph keeps the slots as they are and carries the in-betweens on the follows edge they split (motion_graph
   2.1); solver/interpolation.py, the between-keys report, CONTACT_WORLD and the re-block solver read the keys and the
   in-betweens as one sequence per entity, so the declared interpolation runs through them.
4. The re-block solver places one (`<entity>@<t>` names an in-between, started from the interpolated pose there).
5. No example takes one yet; tests plant them.

Predictions, made before the change (12:09 by the clock):
1. The gate passes before the change: 734 tests (b810414, S-093's chained gate).
2. No example's prompt or checklist changes; only the motion plans re-bind (the plan's schema version).
3. Planted in-betweens are refused for each of: outside its span, on a key's frame, over a joint limit, too fast a
   root, under the floor, through another body; a clean one passes, and the frames around it follow it.
4. The re-block solver places an in-between from a recorded command: on B's 6.3-6.6 span, in a scratch plan, the
   overlaps at 6.375 and 6.5 clear with one in-between near 6.45 (the use itself is RV-59e's).
5. About 742 tests.

## Decisions
- D1 — An in-between key lives in the motion plan's `inbetweens` (entity, t, name, pos, rot, bones, description) and
  on the follows edge it splits (motion_graph 1.2), not as a motion node: the nodes stay one per slot, so the steps
  and renderers that read them are unchanged until RV-59i prints the in-betweens. Level: covered (ADR-O109).
- D2 — Checked like a key at S13: its span (strictly between two consecutive keys of its entity, on a frame no key or
  other in-between holds), the kernel joints and their limits, its root's speed to its neighbours under TELEPORT's 25
  m/s, the floor at its instant and the other bodies there as the declared interpolation poses them (a vanished body
  left out); every refusal names the in-between. It carries the turn of the key before it. Level: interpretation
  (F-053) for the frame rule, the speed figure and the turn; covered (O72, R-18) for the floor and the bodies.
- D3 — The re-block solver names an in-between `<entity>@<t>` and starts it from the interpolated pose there. Measured
  with it: one in-between of B's at 6.45 (B's arms, spine and root free inside the joint limits) clears every frame
  from 6.333 to 6.583 of A's cartwheel elbow, misses 0. Level: covered (ADR-O109).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the staged scan, the gate and the commit |
| One gap, right layer | PASS | S13's plan, check and graph and the readers of its keys (L4c); printing is RV-59i |
| Predictions written first | PASS | the session file was written at 12:09, before any code |
| Each check fires and stays silent | PASS | a clean in-between passes; each of seven plants fails alone (tests/test_inbetweens.py) |
| Neighbours | PASS | CONTACT_WORLD, the between-keys report and the re-block solver read the in-betweens; the knowledge map's KF names INBETWEEN_SPAN (27); the schemas logged (motion_plan 2.1, motion_graph 1.2) |
| The step's instructions teach it | PASS | euler_solving.txt: when to add one, what it carries, how it is checked, never on the source's rows |
| Tests changed with their data | PASS | nine new tests; nothing removed or loosened |
| Examples | PASS | no example takes one; every motion plan re-bound; no prompt or checklist changed |
| Records | PASS | F-053 and F-220 noted; backlog 40 (RV-59f done, RV-59i next); PLAN-007; CHANGELOG; run report |
| Hygiene | see Verification | the staged scan runs first |

## Duration
from 12:09 (the plan) to 12:16 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- schemas/graphs/motion_plan.schema.json 2.1, motion_graph.schema.json 1.2 (schemas log)
- compiler/passes/derived/p13_motion.py (`_inbetweens`, `_inbetween_world`, the packet's fps and vanish windows, the
  edges' in-betweens); solver/interpolation.py (`sequences`, `envelope_keys`); solver/contact_world.py
  (`inbetween_bodies`); solver/reblock.py (in-between slots); validators/between_keys_report.py
- planner/prompts/euler_solving.txt; every example's motion plan re-bound
- tests/test_inbetweens.py (nine tests); kernel/knowledge_map.yaml 27; F-053, F-220; backlog 40; PLAN-007;
  CHANGELOG; run report

## Verification
- before: S-093's chained gate at b810414: 734 passed
- Prediction 1 held. Prediction 2 held. Prediction 3 held (seven plants refused, the clean one passes). Prediction 4
  held (6.333 to 6.583 clear, the frame before the catch included). Prediction 5 held in part (743: one over).
  Predictions 4.5 of 5.
- the gate on this record (12:18:25): `scripts/verify.sh` exit 0, 743 passed in 76.47 s, docs plane: PASS, check:
  PASS
- the hygiene scan over the staged diff: 0 hits on the added lines read without the diff's own plus sign (the first
  scan caught that sign before a pytest decorator, read as an address, and stopped the commit; an address still
  matches with the sign stripped, so the scan reads the content, not the diff's syntax)
