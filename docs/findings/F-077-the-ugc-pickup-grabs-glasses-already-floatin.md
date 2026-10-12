# F-077 — The UGC pickup grabs glasses already floating, and the re-posed hands break their own descriptions

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
medium

## Layer
L1.1

## Status
resolved

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
—

## Evidence
- the principal review, S-035 (docs/prompts/principal_review.md)
- examples/ugc_glasses_demo/plans/temporal.json: the glasses rest on the tabletop at [0.25, 0.75, 0.35] at 0.0 and sit at [0.2, 1.1, 0.3] at the 1.5 pickup (possess with no `at`)
- planner/dynamic_beat_validator.py PROP_KINEMATICS lets a resting prop move when a contact at the second sample picks it up
- S-030 re-posed ugc_creator@b02-b04 (the right hand at [0.14, 1.12, 0.29] at 1.5); the keys still read "Both hands raise ... elbows out" and "the right index finger tapping the frame"; the hand role is two_hand_symmetric over one-handed contacts

## Description
At the pickup instant the glasses are already 0.35 m above the table; S-030's re-block posed the hand to meet them in mid-air instead of fixing the sample, and the re-posed hands no longer match the keys' own words.

## Impact
The model is told the hand takes glasses that float; the poses contradict their descriptions.

## Proposed Fix
Backlog RV-03: the pickup sample on the table (the possess `at: start`, then a lift sample); PROP_KINEMATICS keeps a resting prop still at its pickup instant; the UGC keys re-posed to their descriptions, each a recorded deviation.

## Owner Ruling
none needed (R-17, R-33)

## Related
- PLAN-007
- F-062

## Resolution
RV-03 (S-041, after RV-08): the query's "Creator holding the glasses" holds from the first frame: the possess is `at:
start` (0.0) where the glasses rest on the table, moved to the creator's right so the right hand reaches them leaning
in (on the left the reach needed a 45-degree twist the key's words do not have); the 1.5 sample is the lift.
PROP_KINEMATICS keeps a resting prop where it rests at the instant a contact takes it
(tests/test_dynamic_beat_validator.py::test_a_resting_prop_is_where_it_rests_when_a_contact_takes_it). The keys follow
their words: the hand on the glasses at 0.0, the left fingers at the temples at 1.5, both hands at the glasses with the
elbows out at 3.5, the right index finger at the frame at 5.5; the put-on's left hand takes the left temple, so both
hands carry the glasses through the two-handed put-on. Shot c02 is motivated by its unfold beat; c01 rises with the
lifting hand.
