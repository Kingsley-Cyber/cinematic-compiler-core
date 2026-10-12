# F-072 — A forearm's twist prints as a fold

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
low

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
- solver/staff_geometry.py `fold_word` and `bend_degrees`: the lower segment's whole rotation angle is read as its bend
- library/joint_limits.yaml: LFA/RFA Y allows plus or minus 80 degrees ("forearm pronate/supinate")

## Description
The staff prints a forearm's fold from the angle of its whole rotation, so a pure 80-degree pronation (LFA [0, 80, 0])
would print as "lower arm folded 75" though the elbow does not bend. No key twists a forearm today, so no prompt prints
it wrongly yet. Found by the read-only map of the ten asymmetric things (S-034).

## Impact
A key that turns a palm (PLAN-006 AS-02 reads the palm's facing from this twist) would tell the model the elbow bends.

## Proposed Fix
Read the fold from the X (flexion) part of the lower segment's rotation only; AS-02 reads the Y twist as the palm's
facing.

## Owner Ruling
none needed

## Related
- PLAN-006
- ADR-O87

## Resolution
Open.
