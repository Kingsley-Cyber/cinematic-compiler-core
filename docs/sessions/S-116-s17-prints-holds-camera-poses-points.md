# S-116 — S17 prints the hold frames, the camera's place and aim, each pose's description and its world points

<!-- docs-version: 3.0 -->

## Date
2026-10-13

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
ADR-O113 (owner): stop thinning the data (camera world position and aim, hold frame counts, per-limb world points,
each pose's description)

## Layer
L6

## Status
applied

## Commit
the commit whose message names [S-116]

## Plan
1. The genre block prints every S17 hold with its frame count; a hit's camera hold carries its frames.
2. Each shot's line prints the camera's distance and side, its world position and aim, focus, blur, composition,
   intent, movement quality, relation to the action and rig.
3. Each staff line prints its key's pose description; the euler-heavy mode prints every key's per-limb world points.
4. BODY_HOLD_FRAMES now refuses a hold printed without its frames (O47's clause superseded); HIT_HOLD reads a hold
   with its frames.

Predictions, made before the change (02:45 by the clock):
1. The prose reads about ten more graph fields in every example.

## Decisions
- D1 — Every field goes inside a Master Template section (STACKED_GRAPHS refuses others): holds in the genre block
  and on the camera's hit holds, the camera's fields on its shot line, the pose on its staff line, the points as a
  block of the mode that prints numbers (O13: the five prompts are one prompt's fragments). Level: covered.
- D2 — BODY_HOLD_FRAMES keeps its code and turns to the owner's rule (the code is named by the backlog and the
  checklist); its planted test and HIT_HOLD's take the new wording (ADR-O113 moves the data; ADR-O102). Level: the
  owner's ruling.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the chained gate commits |
| graft used | PASS | graft skeleton of the prose renderer before the reads |
| Tests | PASS | the hold wording in two planted cases and three prose tests; the reach floors raised |

## Duration
from 02:45 to 03:15

## Changes
- renderers/prose_renderer.py; validators/prompt_validator.py; tests/test_dag_conformance.py, tests/test_graph_map.py;
  examples' prompts, envelopes and checklists

## Verification
- Prediction 1 held: reach 89 to 99 (reference fight), 76 to 87, 68 to 79, 119 to 129.
