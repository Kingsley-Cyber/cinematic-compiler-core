# F-076 — The vault starts airborne to pass the launch check, and its hand plant lands 1.76 m up

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
medium

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
- S-022 (commit 7141adb): acrobat@b02's support emptied to pass AIRBORNE_WITHOUT_LAUNCH
- examples/wizard_vs_acrobat: contact b02_c1 (touch, right hand, ground) has no `at`, so it falls at the beat's end, 2.0, where the acrobat is inverted at y 1.83 and the hand at 1.76
- tests/test_motion_solver.py test_contact_world_spares_a_listed_exception_and_an_artefact pins b02_c1 as the model artefact (S-030)

## Description
The beat says "plants the right hand and vaults". S-022 removed the vault's support so the launch check passed; the hand plant then fell at the beat's end, in mid-air, and S-030's test named that miss an artefact.

## Impact
A rewrite made to pass one check created a contradiction the next check exempted (no-shortcuts types 1 and 2).

## Proposed Fix
Backlog RV-02: the hand plant is a support at its own instant (`at: start`) and the launch is from the hand; the launch check accepts a hand-supported launch; the test is re-pinned.

## Owner Ruling
ADR-O89 ("re-block ... the vault hand")

## Related
- PLAN-007
- ADR-O80
- ADR-O89
- F-075

## Resolution
RV-02a (S-039, O89, O80): the hand plant is a support at the vault's first key (1.2, `at: start`), released at 1.6;
the acrobat dives onto the planted right hand with the feet off the ground (pelvis 0.56 m, spine 75 degrees, the
hand 0.065 m over the ground); the run-in ends grounded and the vault beat requires it; the launch check accepts a
first key that stands on the hands alone and still refuses one on a foot
(tests/test_motion_solver.py::test_a_vault_launches_from_its_planted_hand); the artefact test is re-pinned.
