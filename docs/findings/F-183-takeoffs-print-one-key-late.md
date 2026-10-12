# F-183 — Takeoffs print one key late

<!-- docs-version: 1.0 -->

## Type
contradiction

## Severity
medium

## Layer
L6

## Status
open

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the fourth principal review, S-063 (docs/reports/2026-10-12-principal-review-4.md)
- the reference prompts print "4.70 B: SUPPORT both feet ... rising 0.9 m", "takeoff 5.10" and "B hangs in the air 5.10–6.30", while the source and RULES lift and launch B at 4.7 and the golden's HANG_SPANS starts B's air at 4.7; A at 8.00 likewise (both feet, rising 0.9 m; takeoff 8.50)

## Description
The staff reads a launch as standing until the next key shows no support.

## Impact
The model holds B on the ground for 0.4 s the source spends in the air.

## Proposed Fix
Backlog RV-81: a key whose root rises past the standing leg before the next key ends its support there and prints the takeoff at it.

## Owner Ruling
none needed (R-17)

## Related
- RV-81
- F-150
- ADR-O74

## Resolution
Open.
