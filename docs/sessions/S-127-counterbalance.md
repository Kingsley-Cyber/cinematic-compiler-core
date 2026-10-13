# S-127 — S14's second check: the centre of mass and the counterbalance of every key

<!-- docs-version: 3.0 -->

## Date
2026-10-13

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
PLAN-009 PM-3, check 2 of 4 (counterbalance); the masses (owner: "Source the mass table from Dempster's
anthropometry")

## Layer
L4e

## Status
applied

## Commit
the commit whose message names [S-127]

## Plan
1. library/body_segments.yaml `masses`: seven segments' share of the body and the place of their centre (Dempster via
   Winter, Table 4.1), summing to 1.000.
2. solver/pose_mechanics.py: the centre of mass on the key's joints (forward kinematics); the counterbalance: the nearly
   straight limbs reaching 0.4 m or more from it across the floor, the furthest leading, the limbs 0.25 m or more on
   the other side countering.
3. S14 writes both per key; the staff line and the LBN row print them; COUNTERBALANCE (a report) names a reach no limb
   opposes.

Predictions, made before the change (12:14 by the clock):
1. The two jointed reference figures balance as drawn: Naruto's rear leg leads and his front leg counters; Sasuke's
   kick leads and his arms counter.
2. A standing body's centre of mass sits over its hips with no reach.

## Decisions
- D1 — The head and neck's centre sits at the head joint (Winter: the ear canal); the anime body keeps the adult's
  fractions on its longer legs (an interpretation, in the card's basis). Level: covered.
- D2 — COUNTERBALANCE is opposition (an animation principle), not physics: the trunk already balances a reach and the
  centre of mass counts it; the prompt says "no limb opposes it", never "unbalanced". WEIGHT_DISTRIBUTION is the
  physics (next slice). Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the chained gate commits |
| graft used | PASS | graft skeleton of solver/forward_kinematics.py before the reads |
| Tests | PASS | four new: the standing body, the two reference figures, the named reach |

## Duration
from 12:14 to 12:27 (corrected in S-128 from the commit times; the clock times first written were estimates)

## Changes
- library/body_segments.yaml 6 and schemas/cards/body_segments.schema.json 3.2 (logged); solver/forward_kinematics.py
  `masses`, solver/pose_mechanics.py; compiler/passes/derived/p14_pose_mechanics.py; renderers (prose, anime);
  validators/pose_checks.py; schemas/graphs/pose_mechanics_graph.schema.json 1.2 (logged); kernel/data_flow.yaml
  (logged); examples, checklists, docs/graph_map.md; tests

## Verification
- Prediction 1 held: Naruto leads with the rear leg (0.83 m), countered by the right leg and arm; Sasuke's kick leads
  (1.13 m), countered by both arms.
- Prediction 2 held. COUNTERBALANCE names 30 reaches in the examples (18 reference fight, 8 wizard, 6 live action).
