# F-137 — S08 never checks the support hand

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
low

## Layer
L2.5

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
- compiler/passes/derived/p08_hand_role.py checks the agent hand only; in memory, clearing the support hand's hold in i01 still passes
- docs/plans/MASTER_PLAN.md: roles hold across the interaction

## Description
A two-handed interaction may name a support hand that holds nothing.

## Impact
Hand roles can contradict the contacts.

## Proposed Fix
Backlog RV-48: the support hand holds or touches the object during its interaction.

## Owner Ruling
none needed

## Related
- PLAN-007

## Resolution
Open.
