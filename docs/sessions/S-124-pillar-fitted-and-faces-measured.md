# S-124 — The pillar fitted to the fight's feet; contacts with a surface's face are measured

<!-- docs-version: 3.0 -->

## Date
2026-10-13

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
F-235; owner, 2026-10-13: "move the pillar to fit the feet. The fight is the truth; the backdrop serves it. Re-author
the pillar's box to match the reference fight's foot positions. Record as a deviation. Turn on side measurement."

## Layer
all

## Status
applied

## Commit
the commit whose message names [S-124]

## Plan
1. CONTACT_WORLD measures every contact and claimed support on a surface but a floor to the nearest point of its
   boxes (outside, or out through the nearest face from inside); S13's packet carries the boxes.
2. Fit the reference pillar's box to its feet.
3. What no box can fit, record as the owner's exception.

Predictions, made before the change (12:50 by the clock):
1. One box fits the 0.60 landing and the 1.10 run down the face.
2. No box fits the 7.00 wall push's two feet with those.

## Decisions
- D1 — The box x -0.3 to 0.3, z 5.3 to 5.95, y 0 to 8: the 0.60 feet on its top (0.002 m), the 1.10 feet on its face
  (0.10, 0.01 m); its back face at the source's "z=6", whose text stays. Level: the owner's ruling.
- D2 — The 7.00 push's feet stand 1.4 m apart and 1.2 m from the 1.10 feet; a pillar wide enough for both swallows
  the earlier contacts. They are kept as the owner's exceptions under this ruling (the recorded deviation), as the
  O83 source misses are. Level: the owner's ruling, reported.
- D3 — Tests: the contact-exceptions set and its ruling check, and the pickup test's line that the pillar's face is
  not measured, follow the change (ADR-O102). Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the chained gate commits |
| graft used | PASS | graft skeleton of solver/contact_world.py before the edits |
| Tests | PASS | three test lines follow the change |

## Duration
from 12:50 to 13:40

## Changes
- solver/contact_world.py; library/worlds/bamboo_courtyard_pillar.yaml (logged); kernel/contact_world_exceptions.yaml
  (logged); motion and temporal plans re-bound; examples, checklists; kernel/data_flow.yaml; tests; F-235 resolved

## Verification
- Prediction 1 held: 0.002, 0.002, 0.10, 0.01 m.
- Prediction 2 held: 1.09 and 0.59 m; the wizard's back-first slam meets its pillar at 0.056 m.
