# F-218 — The checklist's Any row can call deliverable what no single prompt is

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
low

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
- validators/checklist.py: the Any row is 'yes' when the union of the five columns passes every row and some prompt
  fits a cap; one all-PASS prompt over the caps and a different short prompt make it 'yes' (the S10-S18 reviewer's
  synthetic probe)

## Description
The Any row joins a row verdict from one prompt with a length from another.

## Impact
Latent: no prompt is deliverable today.

## Proposed Fix
Backlog RV-105: the Any row is deliverable only when one prompt is.

## Owner Ruling
none needed

## Related
- F-088
- RV-105

## Resolution
Open.
