# F-137 — S08 never checks the support hand

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
low

## Layer
L2.5

## Status
resolved

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
Backlog RV-48b: the support hand holds or touches the object during its interaction.

## Owner Ruling
none needed

## Related
- PLAN-007

## Resolution
RV-48b (S-058): a named support hand holds the object at the start of one of the interaction's beats or makes a
contact on it in one, as the agent hand must (HAND_ROLE_SWAP, compiler/passes/derived/p08_hand_role.py;
tests/test_hand_role.py::test_the_support_hand_holds_or_touches_its_object); the S08 instructions say so.
