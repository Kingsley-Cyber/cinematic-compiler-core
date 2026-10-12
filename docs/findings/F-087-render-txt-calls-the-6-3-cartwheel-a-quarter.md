# F-087 — render.txt calls the 6.3 cartwheel a quarter turn while it rolls 360

<!-- docs-version: 1.0 -->

## Type
contradiction

## Severity
medium

## Layer
L6

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
- examples/reference_fight/render.txt, A's 6.3 row: "rotates sideways in screen plane one quarter turn"
- tests/test_reference_fight_golden.py ROOT_TURNS rolls A through 360 after 6.3 (O18)

## Description
The source's words and the golden's roll disagree, and render.txt prints both.

## Impact
The model reads two different cartwheels.

## Proposed Fix
Backlog RV-12 (O96): the 6.3 row's words say a full turn, a recorded rewording.

## Owner Ruling
ADR-O96

## Related
- PLAN-007
- ADR-O96
- ADR-O18

## Resolution
RV-12 (S-053, O96): A's 6.3 key says "A body rotates sideways in screen plane one full turn", as its keys roll it
(O18); render.txt prints it, and the golden records the rewording (tests/test_reference_fight_golden.py
CARTWHEEL_WORDS). The prose prompts never carried the clause.
