# S-131 — The re-block solver hands a finding it cannot clear to the model at once, and measures once per round

<!-- docs-version: 3.0 -->

## Date
2026-10-13

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
S-130's solver took 561 s and 312 s on the R20 idea's re-run (29 s before): a finding its repair could not clear was
tried again every round to the round limit, the whole S13 check re-run each time; and each goal re-measured every
contact.

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-131]

## Plan
1. A finding still present after its repair is skipped: the model's, at once.
2. The contact rows are measured once per round, not once per goal.

Predictions, made before the change (19:05 by the clock):
1. The solver's tests pass unchanged.

## Decisions
- D1 — The S-130 claim repair stays; only its looping goes. Level: covered (the owner: "this is your bug, fix it").

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the chained gate commits |
| graft used | PASS | compiler/author.py repair_motion, read in S-130 |
| Tests | PASS | the solver's tests (25) unchanged |

## Duration
from 19:05 to 19:11

## Changes
- compiler/author.py (repair_motion)

## Verification
- Prediction 1 held. The R20 idea's second re-run stopped at S13 on a planning contradiction the solver cannot clear
  (the ninja's right foot strikes the knight at 2.5 and stands on the floor then): R20 next action 3, one part one job.
