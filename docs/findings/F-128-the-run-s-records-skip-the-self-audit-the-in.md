# F-128 — The run's records skip the self-audit, the interpretation label, typed deviations and commit IDs

<!-- docs-version: 1.0 -->

## Type
drift

## Severity
low

## Layer
all

## Status
resolved

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
RV-45 (S-055): from S-055 an applied session records its self-audit, or the docs plane refuses it
(kernel/docs_plane.py `_session_problems`; tests/test_docs_plane.py's "records its self-audit" break); the session
template asks for the clock time of the predictions and labels a choice no ruling makes "interpretation", to be listed
in F-053, which now carries the run's interpretations; the golden's records are typed deviations DEV-01 to DEV-28 with
their ADRs (examples/reference_fight/deviations.yaml;
tests/test_reference_fight_golden.py::test_every_recorded_deviation_is_typed_and_ruled); commit messages name the gap,
layer, rule, slice and deviation from S-055 on. The eight sessions before (S-046 to S-053) stay without a self-audit:
review 3 recorded it (F-166).
