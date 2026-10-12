# F-128 — The run's records skip the self-audit, the interpretation label, typed deviations and commit IDs

<!-- docs-version: 1.0 -->

## Type
drift

## Severity
low

## Layer
all

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
- S-037 to S-044 record no self-audit (R-31; finish.md section 5.7)
- S-039 D8 and D9, S-041 D4 and S-043 D3 call choices no ruling made "covered" (R-32 asks for "interpretation")
- no deviation type or ID exists (R-33; no_shortcuts.md); the commit messages leave out the layer, rule and deviation IDs no_shortcuts.md asks for

## Description
The process the plan wants is followed only in part.

## Impact
A reader cannot audit a slice from its records.

## Proposed Fix
Backlog RV-45: a Self-audit section in each session file; interpretations labelled; deviation types and IDs in the golden test; commit messages carry them.

## Owner Ruling
none needed

## Related
- PLAN-007

## Resolution
Open.
