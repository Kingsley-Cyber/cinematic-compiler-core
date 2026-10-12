# F-173 — S08 reads the hands' contacts, not their holds, and S09 credits a release before the change

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
medium

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
- the fourth principal review, S-063 (docs/reports/2026-10-12-principal-review-4.md)
- compiler/passes/derived/p08_hand_role.py: only contacts inside the interaction are checked against the declared hands; probe: a one_hand unfold passes while the right hand holds the glasses throughout (library/role_templates.yaml: the other hand stays off the object)
- compiler/passes/derived/p09_object_state.py: a release before the change's instant counts as a hand on the object; probe: the glasses become worn at 5.5 credited to a release made at 3.5

## Description
The role lock and the trigger check read contacts but not the holds between them.

## Impact
Hand roles and triggers can contradict the holds.

## Proposed Fix
Backlog RV-72: an undeclared hand holding the object at any of the interaction's beat starts is refused; a release counts as the trigger only at the change's instant. F-137 and F-161 reopened in part.

## Owner Ruling
none needed

## Related
- RV-72
- F-137
- F-161

## Resolution
RV-72 (S-071): S08 refuses a hand of the actor holding the object at any of the interaction's beat starts that is
not one of its declared hands (HAND_ROLE_SWAP, compiler/passes/derived/p08_hand_role.py); S09 credits a release as the
trigger only at the change's instant (compiler/passes/derived/p09_object_state.py)
(tests/test_hand_role.py::test_an_undeclared_hand_may_not_hold_the_object,
tests/test_object_state.py::test_a_release_before_the_change_is_no_trigger).
