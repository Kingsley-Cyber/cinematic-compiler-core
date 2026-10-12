# F-194 — Records and predictions were written ahead of their evidence

<!-- docs-version: 1.0 -->

## Type
drift

## Severity
medium

## Layer
docs

## Status
open

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the fifth principal review, S-072 (docs/reports/2026-10-12-principal-review-5.md)
- S-065, S-066, S-067 and S-071 wrote "after: exit 0, N passed, check: PASS" before the gate that produced it; self_audit.md asks for evidence produced in the audit
- S-066's predictions repeat a probe's results (the arm's angles, about 0.042 m), so they are measurements counted as predictions held (R-05)
- Durations end at the record's last edit, not at the commit; S-071's start (06:05) lies before S-070's commit (06:06)
- commit titles lost finish.md's "(<rulings>)"; 5159dff names no rule; S-066 named DEV-31 and moved DEV-30's record

## Description
The pace (eight slices in about 47 minutes) put records ahead of what they record.

## Impact
A record can claim a result it has not yet seen.

## Proposed Fix
From S-073: the gate runs first and its output is copied into the record, then the chained gate commits; a number found by a probe is reported as measured, never as a prediction; Duration says where it ends; titles carry their rulings. RV-77 makes the self-audit check the order.

## Owner Ruling
none needed (R-05; self_audit.md)

## Related
- RV-77
- F-180
- F-181

## Resolution
Open.
