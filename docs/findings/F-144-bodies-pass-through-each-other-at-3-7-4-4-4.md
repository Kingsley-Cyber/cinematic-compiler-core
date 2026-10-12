# F-144 — Bodies pass through each other at 3.7, 4.4, 4.7 and 9.0

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
high

## Layer
L4c

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
- 3.7: B's trunk axis 0.09 m from A's; 4.4: A's left shin crosses B's right shin (0.02 m apart); 4.7: A's right thigh and shin pass through B's trunk (0.002 and 0.008 m) while CONTACT_WORLD meets the knee to B's torso centre (0.06 m); 9.0: A's right shin through B's right thigh (0.04 m) (the golden-and-fight reviewer, forward kinematics on envelope.json)
- about 4.19 s: B's legs cross the falling substitution log's line 0.07 m off its centre

## Description
No check keeps two bodies, or a body and a prop, from occupying one place; a strike is measured to the target's centre point, not its surface.

## Impact
The model is told to draw limbs through bodies.

## Proposed Fix
Backlog RV-49: an overlap check at S13 (segments as capsules with the body card's widths, drafts for the owner), a strike measured to the target's surface; the poses that fail re-blocked.

## Owner Ruling
none needed (R-18)

## Related
- PLAN-007
- F-089
- RV-14
- F-151

## Resolution
RV-49 (S-049): each segment is a capsule with a draft radius from the body card (library/body_segments.yaml 5);
S13 refuses two bodies whose capsules overlap at an instant both have a key (BODY_OVERLAP, solver/body_overlap.py;
tests/test_forward_kinematics.py::test_no_body_passes_through_another and
tests/test_motion_solver.py::test_each_rule_rejects_its_violation); a contact between two bodies is measured from the
part's surface to the target's (tests/test_forward_kinematics.py::test_a_strike_is_measured_to_the_target_s_surface).
B was re-blocked at 3.4, 3.7, 4.4, 4.7, 6.6, 8.5, 9.0 and 9.5, and the acrobat's kick at 3.6 in the wizard example
(tests/test_forward_kinematics.py::test_every_example_keeps_its_bodies_apart). The second item, a body through a prop
between keys, needs props to have an extent: F-151 (RV-54).
