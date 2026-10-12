# F-095 — Authoring prompts do not teach their steps' checks, and declared inputs are incomplete

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
medium

## Layer
all

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
—

## Evidence
- the principal review, S-035 (docs/prompts/principal_review.md)
- planner/prompts/kinematic_organization.txt, euler_solving.txt and frame_parts.txt do not mention MOMENTUM_MISSING, CONTACT_WORLD, `contact_world_exceptions` or SHAPE_DIRECTION
- kernel/layer_order.yaml external_inputs leave out libraries S04 reads (combat verbs, body segments, genre profiles) and several S10-S16 read; R-13's read half is unchecked

## Description
Authors learn their step's rules only by failing them, and the layer order understates what each step depends on.

## Impact
Slower, blinder authoring; a library change can move a step's output unannounced.

## Proposed Fix
Backlog RV-20 (blocked: the layer-order edit needs an accepted ADR, R-09).

## Owner Ruling
needs an ADR for the layer-order change

## Related
- PLAN-007

## Resolution
Open.
