# S-117 — S17 prints the edge graphs: beat order, paths, transitions, contact order, cuts, rule bindings, invariants

<!-- docs-version: 3.0 -->

## Date
2026-10-13

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
ADR-O113 (owner): "Print every edge graph that reaches the render": temporal, contact, kinematic, Bartenieff and
beat-constraint edges, and the rest S17 dropped

## Layer
L6

## Status
applied

## Commit
the commit whose message names [S-117]

## Plan
1. One helper turns the edge graphs into "- " lines, each in the Master Template section it belongs to: beat order and
   paths in the motion control; kinematic and Bartenieff transitions, Effort spans and state transitions in the
   implied guidance; contact order in the causal links; cuts in the camera; rule bindings and kernel invariants in
   the rules.
2. A constraint the prose leaves to LBN-2.4 (O3, root exact) stays out; so does a rule naming a prop the scene does
   not hold (F-234).
3. The camera's shot count skips the "- " lines (validator and test).

Predictions, made before the change (03:20 by the clock):
1. Reach rises by about forty fields in every example.
2. Some check reads a new line as something it is not.

## Decisions
- D1 — The new lines open with "- " so no staff, shot or rule-count check reads them as their own; the shot count in
  `_camera_checks` and in the prose test skips them (ADR-O113 moves the data; ADR-O102). Level: the owner's ruling.
- D2 — Ids print as words with a repeated word said once ("log log is wood" refused by DOUBLED_WORD). Level: covered.
- D3 — A rule whose `reference_labels` name something the scene does not hold is not printed (F-234; R20's kunai
  class). The S03 fix is R20 next action 1. Level: covered.
- D4 — O3 (root exact left to LBN-2.4) is kept over O113 for the omitted constraints; flagged to the owner. Level:
  the owner's ruling (R-06).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the chained gate commits |
| graft used | PASS | graft skeleton and grep of the renderer and validator before the reads |
| Tests | PASS | 774 passed; one shot-count line in tests/test_prose_render.py; the reach floors raised |

## Duration
from 03:20 to 04:30

## Changes
- renderers/prose_renderer.py; validators/prompt_validator.py; tests/test_prose_render.py, tests/test_graph_map.py;
  examples' prompts, envelopes and checklists; F-234

## Verification
- Prediction 1 held: reach 99 to 146 of 220 (reference fight), 87 to 134/199, 79 to 120/204, 129 to 171/285.
- Prediction 2 held: DISCONNECTED_CAMERA_MOTION (the cuts read as shots), ROOT_EXACT_PRESENT (O3), DOUBLED_WORD and
  COUNT_CONTRADICTION (F-234) each fired once and were answered as above.
