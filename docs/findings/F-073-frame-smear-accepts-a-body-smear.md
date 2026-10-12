# F-073 — FRAME_SMEAR accepts a torso or head smear, against DAG C12

<!-- docs-version: 1.0 -->

## Type
contradiction

## Severity
medium

## Layer
L6

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
—

## Evidence
- compiler/passes/derived/p17_render.py, the FRAME_SMEAR rule: a body smear may name any part the entity declares
- docs/sources/knowledge_dag_v1.md, C12: "smear follows ONLY the declared limb or prop, body does NOT smear"

## Description
FRAME_SMEAR refuses a body smear with no part but accepts `torso` or `head` (both are parts the archetype cards
declare), while the DAG's C12 lets a smear follow only a limb or a prop. The reference fight smears limbs only
(right_leg, left_leg, left_arm), so no example breaks it today. Found by the read-only map of S-034.

## Impact
A plan could smear a fighter's torso and pass, which the DAG and the prose's own ink line ("body does NOT smear") forbid.

## Proposed Fix
PLAN-006 AS-06: a body's smear and speedlines name a limb (an arm or leg or their segments, a hand or a foot).

## Owner Ruling
none needed (R-17: the check is looser than the DAG it enforces)

## Related
- PLAN-006
- ADR-O87

## Resolution
Open.
