# F-064 — The kunai deflect keeps +Z against the golden's own "+Z to -Z"

<!-- docs-version: 1.0 -->

## Type
contradiction

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
- kernel/sources/lbn-2.3-adv.txt, kunai row at 2.5: "DIRECTION REVERSED from +Z to -Z and downward, v_post[0.5,-4.0,-3.0]";
  its row at 4.0 lands the kunai "near pillar p[0.3,0.1,5.5]" (the pillar is at z 6, so the landing needs +Z)
- examples/reference_fight/plans/temporal.json, b05 and b06 (S-009): pre-contact v [-1.4, -3.46, 0.2], post-contact
  v [-0.5, -0.54, 1.75], landing at [0.3, 0, 5.3] at 2.9

## Description
The source contradicts itself at the deflect (a -Z velocity after the foot, a landing toward the pillar at +Z). The
repo's plan kept the landing and gave the kunai a +Z post velocity, so the printed pair shows no reversal in z, and the
foot's "stamp it back down" slows the fall (v_y -3.46 to -0.54) instead of driving it down. The pre/post pair (F2.2,
S-009) makes this visible in every prompt.

## Impact
The model reads a rule that says the kunai reverses to -Z next to velocities that keep +Z.

## Proposed Fix
The owner picks which wins: the words (re-author the post velocity and the landing near B, which moves the rest point
and A's grounded pickup at 8.0, an S11 and S16 cascade) or the samples (reword the rule as a deflect down toward the
pillar). Not a leaf change, so the autopilot does not make it (ADR-O71).

## Owner Ruling
ADR-O77

## Related
- F-059
- PLAN-003
- ADR-O71

## Resolution
Owner O77: the golden is right. The kunai leaves A's foot at 2.5 with the source's v_post [0.5, -4.0, -3.0]
(reversing +Z to -Z), lands at 2.7 on [0.6, 0, 4.0] and rests there until A takes it at 8.0 (M9-09d, S-023; the
golden test records it).
