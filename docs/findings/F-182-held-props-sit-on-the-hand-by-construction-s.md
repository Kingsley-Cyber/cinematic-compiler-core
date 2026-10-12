# F-182 — Held props sit on the hand by construction, so the draw is unmeasured

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
medium

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
- the fourth principal review, S-063 (docs/reports/2026-10-12-principal-review-4.md)
- examples/reference_fight/plans/temporal.json: the volley's 5.1 and 5.5 samples sit on B's forward-kinematics hand point, so CONTACT_WORLD reads 0.004 m for b13_c1, b14_c1 and b14_c4; no sample puts the holstered volley on the thigh, so the hand's reach to the pouch is not measured
- S-061's "0.05 m off the thigh's surface" was measured to the thigh's midpoint: the hand is 0.108 m from the thigh's axis, 0.028 m from its surface, and its own 0.04 m radius overlaps the thigh by 0.012 m (S-063's probe)

## Description
RV-62 placed the drawn volley where the hand is, so the check that would judge the draw cannot fail.

## Impact
The draw from the pouch is asserted, not measured, and the record overstated the clearance.

## Proposed Fix
Backlog RV-68: the holstered volley gets a sample at the thigh pouch and the draw is measured against it; B's arm re-posed so the hand meets the pouch without entering the thigh. S-061 and F-053 corrected.

## Owner Ruling
none needed

## Related
- RV-68
- F-163
- F-105
- ADR-O83

## Resolution
RV-68 (S-066): the volley's 5.1 sample rests at the pouch, on the outer side of B's right thigh a quarter of the way
from the hip, and B's repo 5.1 arm is re-posed (RA [30, -15, 0], RFA [-45, 0, 0]) so the hand meets it from outside the
thigh: CONTACT_WORLD measures the draw at 0.045 m; the golden's draw test pins the sample on the thigh's surface and the
hand outside it (tests/test_reference_fight_golden.py::test_b_draws_the_volley_before_throwing_it).
