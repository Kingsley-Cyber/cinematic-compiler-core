# F-159 — Bodies pass through each other between keys

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
- the third principal review, S-054 (docs/reports/2026-10-12-principal-review-3.md)
- solver/body_overlap.py checks only the instants where both bodies have keys; A's keys at 0.6, 1.1 and 7.0 have no B key
- under the prompt's own interpolation (slerp joints, linear root) the fighters overlap in 31 frames over 11 spans: 0.149 m at 6.375 (B's forearm in A's trunk), 0.10 m at 4.75, 0.108 m at 6.75, 0.072 m at 8.46; the wizard's foot is 0.175 m inside the wizard's trunk at 3.57
- body_overlap.py defers points between keys to RV-47, whose scope is contacts and prop samples; tests/test_forward_kinematics.py::test_every_example_keeps_its_bodies_apart says "at any instant"
- the S-049 re-blocks left 4 to 18 mm of clearance at the keys

## Description
F-144 was resolved for the key instants; the paths into the keys still go through the bodies.

## Impact
A strike's approach, the catch and the drive are drawn through a body.

## Proposed Fix
Backlog RV-59, after RV-35 (the re-block solver committed): BODY_OVERLAP along the declared interpolation at the scene's frame rate; the paths re-blocked on the repo-authored side.

## Owner Ruling
none needed (R-18)

## Related
- PLAN-007
- F-144
- F-127
- RV-59
- RV-35
- RV-47

## Resolution
Open.
Noted in S-081 (the sixth review): between keys A and B overlap in 33 frames (deepest 0.149 m at 6.375), A falls
through B's head at 7.21, and B's left sole goes 0.385 m under the floor at 8.75 (RV-59, its title widened to
FLOOR_PENETRATION).
Noted in S-086 (RV-59a): along the declared interpolation (joints slerped, the root straight) the fight's bodies
overlap in 38 frames over eight spans between keys, deepest 0.149 m at 6.375, every span with B's repo keys at one
end; the wizard example's in 5 frames over two spans (docs/reports/2026-10-12-between-keys.md). RV-59b refuses them
and re-blocks B's paths.
Noted in S-087 (RV-59b): the re-block solver's clearance goal cleared 3.4-3.7 and 4.4-4.7 (B's left arm at 3.7, B's
root and legs at 4.4); the six spans left lie by a contact the keys must keep, and the wizard example's two by its
kick: F-220 asks how they clear, and RV-59e refuses after its answer.
Resolved in S-097 (RV-59e): S13 refuses two bodies overlapping at any frame between keys, each posed by the declared
interpolation through its keys and in-betweens; five in-between keys of B's (4.75, 6.45, 6.7, 8.45, 8.75) and two of
the acrobat's (3.55, 3.7), placed from recorded commands with nothing moved on A's rows, clear every span, so the four
examples pass (DEV-35; tests/test_inbetweens.py).
