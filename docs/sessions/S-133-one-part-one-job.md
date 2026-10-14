# S-133 — One part, one job: S04 declares each limb's role and refuses a brief no pose can meet

<!-- docs-version: 3.0 -->

## Date
2026-10-13

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
PLAN-010 Phase 1 (R20 next action 3): the R20 idea's second run died at S13 on a foot that kicked while it stood

## Layer
L1.1

## Status
applied

## Commit
the commit whose message names [S-133]

## Plan
1. beat_plan 1.7: each beat declares `roles` (owner: declared, not inferred), the twins of its contacts (support,
   strike, block, carry); S04 keeps them out of the graph (the contacts carry them).
2. ONE_PART_ONE_JOB: a limb that stands cannot strike or block until released; a limb stands on one thing at a time; a
   push off a surface is a moment; a held prop strikes with its hand.
3. CONSTRAINT_SATISFIABLE: the roles are the contacts' twins, one for one; a strike lands from within 1.5 m (AA-10's
   reach, now at S04).
4. The four examples' beats get their roles from their own contacts; the S04 instruction teaches the three rules.

Predictions, made before the change (19:50 by the clock):
1. The examples pass all three.
2. The R20 idea's second run's beat plan would have been refused at S04.

## Decisions
- D1 — A release at a strike's own instant frees the limb for it (the wizard example's acrobat releases its right
  foot and kicks at 3.6). Level: covered.
- D2 — Roles stay out of the graph: written twice would be an orphan the gate refuses (ADR-O119). Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the chained gate commits |
| graft used | PASS | the S04 validator and pass read through the S-125 map |
| Tests | PASS | tests/test_limb_roles.py (6, 0.02 s): a valid and an invalid case per check |

## Duration
from 19:50 to 19:44

## Changes
- schemas/graphs/beat_plan.schema.json 1.7 (logged); planner/dynamic_beat_validator.py, planner/beat_planner.py,
  planner/prompts/beat_planning.txt; compiler/passes/mandatory/p04_temporal.py; the examples' temporal plans (roles,
  from their contacts: a recorded deviation) and every plan re-bound; examples, checklists; tests

## Verification
- Prediction 1 held after two fixes found on the examples (a surface touch opened a stand; a release at the kick's
  instant was read after it).
- Prediction 2 held by construction: tests/test_limb_roles.py replays it (a foot that kicks while it stands).
