# S-001 — M9 step 1: the probe wording rules W1-W4, O48's post and O54's negatives

<!-- docs-version: 1.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5)

## Gap
Backlog M9-01; findings F-031 (GAP-16), F-041 to F-045 (P1-P5), F-037 (AX3), F-038 (AX4)

## Layer
L6

## Status
applied

## Commit
7cc69f8

## Plan
Print the wording the owner's probes showed the model follows (O47-O49) and add one prompt code per rule. Predicted
before the change: on fresh renders BODY_HOLD_FRAMES fires only on the anime camera card's "Hold or freeze ... in one
frame" and HIDDEN_PHRASING only on the reference log's "deployment hidden"; both held. S05 refused the first version of
O48 (a hard cause that changes nothing), so the log card gained the state `standing`.

## Duration
about 2 hours

## Changes
- `renderers/prose_renderer.py`: hit holds, empty hands, turn runs, 'EulerXYZ mid-turn'
- `validators/prompt_validator.py`: BODY_HOLD_FRAMES, EMPTY_HAND_UNSTATED, ROTATION_ANGLES_PRINTED, HIDDEN_PHRASING
- `library/camera_conventions/anime.yaml`, `library/archetypes/ninja_{lean,broad}.yaml`, `library/ontology/objects/substitution_log.yaml` (logged)
- `examples/reference_fight/plans/temporal.json` (O48 post), every example re-bound and rewritten

## Verification
- `scripts/check.sh`: pass (558 tests)
- `make golden`: render.txt changed on purpose for the reference fight only (log track, four negatives; deviation SUBSTITUTION_POST)

## Next
S-002: the docs plane (owner O64-O67), then backlog M9-02 (F5.3 strike timing).
