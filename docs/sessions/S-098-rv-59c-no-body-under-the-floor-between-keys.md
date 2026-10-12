# S-098 — RV-59c: no body under the floor at any frame between keys

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-59c (PLAN-007); finding F-089; rulings O72 (0.15 m), R-18; ADR-O109

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-098]

## Plan
FLOOR_PENETRATION judges the keys and the in-betweens only; between them B's crash sank a sole 0.209 m until S-097's
in-between at 8.75 held it over the floor. The refusal itself, here. The class: BODY_OVERLAP's twin (RV-59e).
1. S13 refuses a body point more than 0.15 m under the floor at any frame between keys, each body posed by the
   declared interpolation through its keys and in-betweens, a vanished body left out; one refusal per body and span,
   at its deepest frame. The frame walk is shared with BODY_OVERLAP's.
2. The instructions teach it; a test plants the crash without its in-between.

Predictions, made before the change (12:50 by the clock):
1. The gate passes before the change: 749 tests (c768ff0, S-097's chained gate).
2. The check refuses nothing in the four examples.
3. Without B's in-between at 8.75 it refuses B's crash once, about 0.209 m deep near 8.71.
4. No example's data or prompt changes; the motion plans re-bind to the instructions.
5. About 751 tests.

## Decisions
- D1 — FLOOR_PENETRATION between keys: at every frame of the scene's fps strictly inside the keys' range, each body
  posed by the declared interpolation through its keys and in-betweens (a vanished body left out, a body at a key or
  an in-between judged there), its lowest FLOOR_PENETRATION point more than 0.15 m under the floor is refused, once
  per body and span at the deepest frame; the frame walk is shared with BODY_OVERLAP's (`_frames`). Level: covered
  (O72).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the staged scan, the gate and the commit |
| One gap, right layer | PASS | S13's check (L4c) |
| Predictions written first | PASS | the session file was written at 12:50, before any code |
| The check fires and stays silent | PASS | the four examples pass; without B's 8.75 in-between the crash is refused once (0.209 m at 8.708; a test) |
| Neighbours | PASS | BODY_OVERLAP's check now walks the shared frames; floor_penetration.py's and the report's docstrings; knowledge map 31 (a locator; Conservation laws) |
| The step's instructions teach it | PASS | euler_solving.txt: no point under the floor at any key or any frame between keys |
| Tests changed with their data | PASS | one new test; nothing removed |
| Examples | PASS | every motion plan re-bound; no data or prompt changed |
| Records | PASS | F-089 noted; backlog (RV-59c done, RV-59g next); PLAN-007; CHANGELOG; run report |
| Hygiene | see Verification | the staged scan runs first, on the added lines |

## Duration
from 12:50 (the plan) to 12:52 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- compiler/passes/derived/p13_motion.py (`_frames`, `_floor_between_keys`; `_between_keys` on the shared frames);
  planner/prompts/euler_solving.txt; every motion plan re-bound
- tests/test_inbetweens.py (one test); solver/floor_penetration.py, validators/between_keys_report.py (docstrings)
- F-089; kernel/knowledge_map.yaml 31; backlog; PLAN-007; CHANGELOG; run report

## Verification
- before: S-097's chained gate at c768ff0: 749 passed
- Prediction 1 held. Prediction 2 held. Prediction 3 held (0.209 m at 8.708). Prediction 4 held. Prediction 5 held in
  part (750: one under). Predictions 4.5 of 5.
- the gate on this record (12:52:08): `scripts/verify.sh` exit 0, 750 passed in 107.33 s, docs plane: PASS, check:
  PASS
- the hygiene scan over the staged diff's added lines: 0 hits (run first in the chained commit)
