# S-129 — The fourth check: silhouette, computed at the camera step for every shot

<!-- docs-version: 3.0 -->

## Date
2026-10-13

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
PLAN-009 PM-4, check 4 of 4 (silhouette; at S17, which holds the camera, as ruled)

## Layer
L5.5

## Status
applied

## Commit
the commit whose message names [S-129]

## Plan
1. solver/pose_mechanics.py `silhouette`: each framed body's trunk (pelvis to head) and its hands and feet projected on
   the shot camera's picture plane; an end within the trunk's half width (0.15 m) of a framed trunk is against it.
2. S17's derived block (validators/camera_validator.py `derive`) records it per shot from the packet's body points at
   its first beat; the shot line and the LBN row print it.
3. SILHOUETTE_READABLE (a report): a striking hand or foot against a body other than its target in the shot that
   opens on the strike.

Predictions, made before the change (16:31 by the clock):
1. No packet changes (the camera step's packet already holds each beat's body points): no plan re-binds.
2. Most ends read clear; the UGC shots, close on the hands and the product, have the most against a body.

## Decisions
- D1 — A strike's end against its own target is the contact itself, not a hidden limb; only a third body or the
  striker's own trunk counts. Level: covered.
- D2 — Measured at the shot's first beat (the packet's points), the beat the camera derives from; a strike later in a
  long shot is not judged. Level: covered (reported).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the chained gate commits |
| graft used | PASS | the camera packet's points read through the S-125 map |
| Tests | PASS | four new: a hand on the chest, the flying kick, the clash, the planted strike |

## Duration
from 16:31 to 16:38

## Changes
- solver/pose_mechanics.py; validators/camera_validator.py, validators/pose_checks.py; renderers (prose, anime);
  schemas/graphs/camera_graph.schema.json (logged); examples, checklists, docs/graph_map.md; tests

## Verification
- Prediction 1 held: no plan re-bound.
- Prediction 2 held in part: reference fight 136 clear and 16 against over 22 shots, wizard 73 and 7, live action 20
  and 0, UGC 11 and 5 (the most against for its shot count). No strike is hidden against the wrong body.
