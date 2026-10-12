# F-100 — Hip limits read trunk-relative hips against anatomical ranges

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
medium

## Layer
L4c

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
- library/joint_limits.yaml hip ranges (anatomical, against the pelvis) applied by JOINT_LIMIT to LUL and RUL, which O84 reads from the trunk
- the acrobat's re-expressed hips (-140, -145) pass only through the anime +30

## Description
A lean now eats into the hip's range; the same lean in live action would be refused.

## Impact
Valid poses refused, or anime poses passing only by the allowance.

## Proposed Fix
Backlog RV-25: JOINT_LIMIT checks the hip against the pelvis (the trunk reading composed back).

## Owner Ruling
ADR-O84, ADR-O11

## Related
- PLAN-007
- ADR-O84
- ADR-O11

## Resolution
Open.
