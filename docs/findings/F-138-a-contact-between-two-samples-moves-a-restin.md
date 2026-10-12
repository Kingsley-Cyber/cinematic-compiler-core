# F-138 — A contact between two samples moves a resting prop unchecked

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
low

## Layer
L1.1

## Status
open

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the second principal review, S-045 (docs/reports/2026-10-12-principal-review-2.md)
- planner/dynamic_beat_validator.py skips a span with a contact strictly between its two samples
- the substitution log moves 0.6 m (z 5.3 to 4.7) at the 3.7 swap with no sample after the contact

## Description
A contact can teleport a resting prop.

## Impact
Prop paths can jump.

## Proposed Fix
Backlog RV-48: a contact that moves a resting prop needs a sample at the contact (or the owner's rule for the swap).

## Owner Ruling
none needed

## Related
- PLAN-007

## Resolution
Open.
