# S-095 — RV-59i: every prompt prints the in-between keys

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-59i (PLAN-007); ADR-O109; finding F-220; rulings O9 (named fields), the DAG's density rules
(docs/sources/knowledge_dag_v1.md:253-261: explicit keys, "pair every dense section with clear implied guidance")

## Layer
L6

## Status
applied

## Commit
the commit whose message names [S-095]

## Plan
S-094 let an in-between key stand at S13; no prompt prints one, so a render would never pass through it. The class: a
graph fact the prompts do not carry.
1. The LBN projection (render.txt for the anime, live and UGC cards): an in-between is a row of its actor at its
   instant, in time order, its description marked as an in-between key (no beat, no contact); the coverage counts
   the in-betweens as a group of their own when there are any.
2. The prose modes: an [IN-BETWEEN KEYS] block after the staff (the staff's rule "a symbol lasts until the next line"
   is kept), each in-between with its time, performer and pose words, and Root and Joints in every mode but the pure
   staff; the motion control's density counts them, and says the explicit keys are the staff lines and the
   in-betweens.
3. Nothing prints when no in-between exists, so the examples stay byte for byte.

Predictions, made before the change (12:23 by the clock):
1. The gate passes before the change: 743 tests (8821985, S-094's chained gate).
2. With no in-between in any example, every prompt stays byte for byte.
3. A planted in-between appears in render.txt's actor rows at its instant, in time order, marked as an in-between,
   and the render's coverage counts it; a renderer that skipped it would read incomplete.
4. Each prose mode prints the block with the in-between's time, performer and pose words, Root and Joints in all
   but the pure staff; the motion control's density counts it.
5. About 747 tests.

## Decisions
- D1 — In render.txt an in-between is a row of its actor at its instant (the rows sorted by time only when one
  exists), its description opening "IN-BETWEEN key (no beat, no contact): the interpolation passes through this
  pose"; the coverage counts the in-betweens as a group of their own, present only when there are any, so a
  projection that skips one reads incomplete and the examples' coverage reports stay as they were. Level: covered
  (O9's named fields; ADR-O109).
- D2 — The prose keeps its staff (one line a measure, "a symbol lasts until the next line") and prints the in-betweens
  in their own block after it, each with its time, performer, name and pose words, Root and Joints in every mode but
  the pure staff (whose words carry the movement without numbers); the motion control's density counts them and calls
  the explicit keys "the staff lines and the in-between keys". Level: interpretation (F-053): the block's place and
  form.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the staged scan, the gate and the commit |
| One gap, right layer | PASS | S17's renderers (L6) |
| Predictions written first | PASS | the session file was written at 12:23, before any code |
| Prints when present, silent otherwise | PASS | planted: render.txt's row and coverage, every prose mode's block and density (tests); absent: `compiler.examples --check` clean |
| Neighbours | PASS | the live and UGC cards share the LBN projection; the coverage catches a skipped in-between; knowledge map 28 |
| Tests changed with their data | PASS | two new tests in tests/test_inbetweens.py; nothing removed |
| Examples | PASS | none changed |
| Records | PASS | backlog 41 (RV-59i done, RV-108 next, RV-95c after RV-107 per review 7's queue); PLAN-007; CHANGELOG; run report |
| Hygiene | see Verification | the staged scan runs first, on the added lines |

## Duration
from 12:23 (the plan) to 12:25 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- renderers/anime_renderer.py (`inbetweens`; the coverage group; the actor rows); renderers/prose_renderer.py (the
  [IN-BETWEEN KEYS] block; `_gaps` and the motion control)
- tests/test_inbetweens.py (two tests); kernel/knowledge_map.yaml 28; backlog 41; PLAN-007; CHANGELOG; run report

## Verification
- before: S-094's chained gate at 8821985: 743 passed
- Prediction 1 held. Prediction 2 held. Prediction 3 held. Prediction 4 held. Prediction 5 failed (745: two under;
  two tests carry the four checks). Predictions 4 of 5.
- the gate on this record (12:25:47): `scripts/verify.sh` exit 0, 745 passed in 77.11 s, docs plane: PASS, check:
  PASS
- the hygiene scan over the staged diff's added lines: 0 hits (run first in the chained commit)
