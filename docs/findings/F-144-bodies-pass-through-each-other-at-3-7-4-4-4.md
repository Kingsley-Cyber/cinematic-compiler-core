# F-144 — Bodies pass through each other at 3.7, 4.4, 4.7 and 9.0

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
high

## Layer
L4c

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

## Resolution
Open.
