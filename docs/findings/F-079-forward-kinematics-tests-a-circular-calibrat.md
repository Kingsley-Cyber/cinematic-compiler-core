# F-079 — Forward-kinematics tests: a circular calibration check, mislabelled exceptions, a dead clause

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
low

## Layer
L4c

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
- tests/test_forward_kinematics.py test_the_source_grounded_rows_meet_the_ground_under_the_anime_body checks the very rows the anime body was fitted to (S-029)
- its SOURCE_EXCEPTIONS calls four misses "recorded exceptions (ADR-O83 point 2)" while the plan lists only b06_c3; the 5.9 pair pass as artefacts
- test_repo_authored_roots_stand_at_the_pelvis keeps `or key["id"] == "acrobat@b08"`, which no longer matters

## Description
The calibration test can only fail if the card changes, and its comment claims more owner exceptions than exist.

## Impact
A test that proves less than it says.

## Proposed Fix
Backlog RV-02: the fit test labelled as a regression pin; the exceptions named as what they are; the dead clause removed.

## Owner Ruling
none needed

## Related
- PLAN-007
- ADR-O83

## Resolution
RV-02a (S-039): the calibration test is labelled a regression pin; SOURCE_EXCEPTIONS says what the repo does with
each source miss (3.0 flipped by O88, 4.0 not drawn, the 5.9 slide listed as b14_c2 and b14_c3); the dead
`acrobat@b08` clause is gone.
