# F-084 — The kunai drive and the catch print as instant strikes, and the kunai floats over the downed B

<!-- docs-version: 1.0 -->

## Type
contradiction

## Severity
high

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
- prose_mixed.txt lines 103-104: "B after the 6.60 strike" and "B after the 8.50 strike": "one instant contact, the limb does not stay on the target"
- contact b21_c1 is "touch ninja_broad torso -> kunai blade"; A's right hand has no contact at 8.5
- the kunai's 9.0 sample [1.0, 1.3, 5.2] rests 1.2 m above B, who lies at y 0.1 (torso [1.4, 0.1, 5.3]); A's "holding" hand is 0.6 m away; the source says "kunai stays in B shoulder NOT released" and "B right shoulder" (the golden says torso)

## Description
The climax's held kunai and the catch are notated as strikes that leave the target at once, and the kunai's samples after 8.5 do not follow B.

## Impact
The climax shows a kunai hanging in the air and a catch that does not hold.

## Proposed Fix
Backlog RV-10 (O93): at 8.5 A's right hand drives and holds the kunai in B's right shoulder to the end; at 6.6 B grasps A's arm and throws; neither prints as an instant strike.

## Owner Ruling
ADR-O93

## Related
- PLAN-007
- ADR-O93
- ADR-O22

## Resolution
RV-10 (S-051, O93): from 8.5 the kunai is embedded (an effect at the drive's start) and its samples sit at B's torso
point (the shoulder has no part of its own) at 8.5, 9.0, 9.5 and 10.0, while A's right hand keeps it (holder A to the
end); B's torso meets the blade at 8.5, which no longer counts as B's strike (a body struck by a blade another
performer holds); B's hands take A's left arm at 6.6 (possess, catch) and let go at 6.8 (release, throw), so b17 runs
6.6-6.8. Neither prints as an instant strike (tests/test_reference_fight_golden.py
::test_the_kunai_drive_holds_the_kunai_in_b_and_the_catch_grasps_then_throws). A's right hand stays 0.6 to 0.7 m above
the kunai at 8.5 and 9.0-10 under the source's own arm numbers: F-148, the owner's question.
