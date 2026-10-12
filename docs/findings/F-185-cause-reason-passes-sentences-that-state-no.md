# F-185 — CAUSE_REASON passes sentences that state no cause

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
high

## Layer
L1.2

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
- S-063's probe: for b01 to b02, "A is a lean ninja in a dark coat." and "The weather is nice and B likes tea." pass validators/cause_reason.py (it asks only for enough words that name a performer, prop, surface or action)
- F-001 and F-002 are resolved as caught by CAUSE_REASON, which un-contests rows C6, T9, C21, C26, C27 and V7 (validators/checklist.py)

## Description
The check tests that a reason names something, not that it states why the later beat follows.

## Impact
A causal graph of non-reasons passes, and six rows read as covered.

## Proposed Fix
Backlog RV-75: a reason ties a word of the earlier beat's action, effect or contact to the later beat with a causal link; F-001 and F-002 stay resolved for the golden, and their caught_by rests on this fix.

## Owner Ruling
none needed

## Related
- RV-75
- F-001
- F-002

## Resolution
Open.
