# F-138 — A contact between two samples moves a resting prop unchecked

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
low

## Layer
L1.1

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
- planner/dynamic_beat_validator.py skips a span with a contact strictly between its two samples
- the substitution log moves 0.6 m (z 5.3 to 4.7) at the 3.7 swap with no sample after the contact

## Description
A contact can teleport a resting prop.

## Impact
Prop paths can jump.

## Proposed Fix
Backlog RV-48a: a contact that moves a resting prop needs a sample at the contact (or the owner's rule for the swap).

## Owner Ruling
none needed

## Related
- PLAN-007

## Resolution
RV-48a (S-057): a contact between two samples moves a resting prop only by taking hold of it; any other needs a
sample at its instant (PROP_KINEMATICS); a substitution swaps its decoy into its new place at its start (O12, O48;
`_swapped`, an interpretation in F-053), so the log takes A's former place at 3.7 with a sample there, and A's hand
touch of it went (it missed by 0.8 m once measurable; S07 lets a substitution change its decoy without a hand)
(tests/test_dynamic_beat_validator.py::test_a_contact_between_two_samples_does_not_move_a_resting_prop,
tests/test_reference_fight_golden.py::test_the_log_takes_a_s_place_at_the_swap).
