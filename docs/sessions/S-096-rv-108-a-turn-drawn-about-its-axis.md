# S-096 — RV-108: a declared turn under a half turn is drawn as the turn it is

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-108 (PLAN-007); finding F-225 (principal review 7); rulings O18 (declared turns), R-18; the source's rule
"Use slerp on all joint rotations. Root positions are exact."; F-053's S-011 reading (a declared turn's angles run
straight)

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-096]

## Plan
Between keys a declared turn's root angles run straight (S-086), which draws a whole flip that a shortest-arc slerp
would undo. But a turn under a half turn has no such need, and from a key at gimbal lock straight angles leave the
turn: B's 8.5 tip (a 90-degree turn about B's side axis, as the prompt prints it) is drawn sweeping 116 degrees and
straying 34 from it, sinking a sole 0.385 m. The class: an interpolation chosen by a declaration rather than by the
turn the keys make.
1. solver/interpolation.py: a declared turn whose angle about its own axis (flip X, spin Y, cartwheel Z) is under a
   half turn is slerped, the shortest arc being that turn; a half turn or more keeps its angles straight.
2. S13's follows edge says the same (`interpolation`: slerp or euler_axis by that rule); the motion graph schema's
   words follow.
3. F-053's S-011 entry revised; the between-keys report re-measured.

Predictions, made before the change (12:29 by the clock):
1. The gate passes before the change: 745 tests (3bcf40f, S-095's chained gate).
2. At most two declared-turn edges across the four examples are under a half turn about their axis, B's 8.5 crash
   among them; only their interpolation changes.
3. B's crash then sinks 0.209 m between keys (the tip), still over 0.15 m, so RV-59c still needs a key mid-fall.
4. No prompt changes (the turn words come from the keys); only the envelopes' edges change.
5. About 748 tests.

## Decisions
- D1 — A declared turn under a half turn about its own axis (flip X, spin Y, cartwheel Z: solver/staff_geometry.py
  TURNS) is slerped between its keys: the shortest arc is that turn, and from a key at gimbal lock straight angles
  leave it. A half turn or more keeps its angles straight, which a slerp would undo. The rule reads each segment, so an
  in-between that splits a whole turn into parts under a half turn draws each part as its arc. Level: interpretation
  (F-053), revising S-011's and S-086's readings.
- D2 — S13's edge says the same (`interpolation`: euler_axis only for a half turn or more), and S-011's graph test
  follows F-225 (ADR-O102), checked from the edge's own Euler change. Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the staged scan, the gate and the commit |
| One gap, right layer | PASS | the declared interpolation and S13's edges (L4c) |
| Predictions written first | PASS | the session file was written at 12:29, before any code |
| Measured, not assumed | PASS | eight turn edges listed before and after; B's crash re-measured (0.209 m, 5 frames); the overlaps (24 frames) |
| Neighbours | PASS | the edge field, the graph schema's words (1.3), the between-keys report, F-053's two readings, the floor term's docstring numbers |
| Tests changed with their data | PASS | the report's pins (24 frames; the crash 0.209 m), S-011's graph test under F-225, one new test |
| Examples | PASS | the fight's and the wizard's envelopes (eight edges); no prompt or plan changed |
| Records | PASS | F-225 resolved; F-053, F-220 noted; map 29 (kernel log); the schema logged; backlog (RV-108 done, RV-59e next); PLAN-007; CHANGELOG; run report |
| Hygiene | see Verification | the staged scan runs first, on the added lines |

## Duration
from 12:29 (the plan) to 12:31 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- solver/interpolation.py (`straight`); compiler/passes/derived/p13_motion.py (the edge's interpolation);
  schemas/graphs/motion_graph.schema.json 1.3
- examples: the fight's and the wizard's envelopes (eight edges)
- tests: test_interpolation.py (pins; one test), test_motion_solver.py (F-225), test_reblock.py (a docstring)
- F-225 resolved; F-053, F-220; kernel/knowledge_map.yaml 29; backlog; PLAN-007; CHANGELOG; run report

## Verification
- before: S-095's chained gate at 3bcf40f: 745 passed
- Prediction 1 held. Prediction 2 failed (eight turn edges are under a half turn, not at most two; the spins among
  them draw the same path either way). Prediction 3 held (0.209 m). Prediction 4 held. Prediction 5 held in part (746:
  two under). Predictions 3.5 of 5.
- the gate on this record (12:31:57): `scripts/verify.sh` exit 0, 746 passed in 78.23 s, docs plane: PASS, check:
  PASS
- the hygiene scan over the staged diff's added lines: 0 hits (run first in the chained commit)
