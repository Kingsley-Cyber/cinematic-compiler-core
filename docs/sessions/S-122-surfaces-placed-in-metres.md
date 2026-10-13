# S-122 — Surfaces placed in metres: every surface has boxes, S04 checks a body reaches the surface it meets, the prompt prints where each is

<!-- docs-version: 3.0 -->

## Date
2026-10-13

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
R20 next action 2 (owner: "proceed with fix #2"): the side pillar; a surface had no place

## Layer
all

## Status
applied

## Commit
the commit whose message names [S-122]

## Plan
1. World cards and the brief's surfaces gain `boxes` (axis-aligned, metres; required); S02 copies them; casting drafts
   must give them (the schema it is handed).
2. S04's packet carries them; SURFACE_REACH refuses a body meeting a surface other than a floor from more than 1.5 m.
3. Floors and tabletops take their top from their boxes; a pillar keeps the top its text names.
4. [SPATIAL ANCHORS] and the LBN axes print every surface's place.

Predictions, made before the change (09:50 by the clock):
1. The examples pass SURFACE_REACH with boxes drawn from their own text and data.
2. Measuring faces would refuse the reference fight's own pillar contacts.

## Decisions
- D1 — Draft boxes are Claude's, drawn from each card's own words and each example's own data (the reference pillar
  from "z=6 from y=0 to y=8", the tabletop from the glasses' rest at y 0.75, the wizard's stone pillar from the
  acrobat's back-first slam); the four world cards are drafts for owner review. Level: covered.
- D2 — A pillar's or wall's top is not stood on unless its text names one: the acrobat's slam into the stone
  pillar's side measured as a landing on its top refused at 0.62 m. Level: covered.
- D3 — Face contacts stay unmeasured (F-235): the reference fight's wall push misses any pillar its text allows; the
  owner rules which is true. Level: the owner's ruling (R-06).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the chained gate commits |
| graft used | PASS | graft grep of every `ax` reader before the edits |
| Tests | PASS | SURFACE_REACH planted; every world surface placed and printed; the casting test's drafted roof takes boxes |

## Duration
from 09:50 to 11:00

## Changes
- schemas (world_card 1.1, brief_nodes 1.2) and four world cards (logged); planner/world_grounder.py,
  planner/beat_planner.py, planner/dynamic_beat_validator.py, planner/prompts/beat_planning.txt;
  renderers/prose_renderer.py, renderers/anime_renderer.py; every example plan re-bound; examples, checklists,
  docs/graph_map.md, kernel/data_flow.yaml (logged); tests; F-235; docs/reports/2026-10-13-graph-inventory.md (every layer and field: writer, readers,
  printed, orphaned; generated from the contract)

## Verification
- Prediction 1 held: every example passes; the planted 5 m slam is refused.
- Prediction 2 held: the reference fight's 0.60 landing sits 0.39 m in front of its pillar and its 7.00 push has one
  foot inside it (F-235).
