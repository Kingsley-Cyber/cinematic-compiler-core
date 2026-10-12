# F-001 — The causal graph gives no causes

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
high

## Layer
L1.2

## Status
resolved

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
F1

## Evidence
R4 "nothing warranted", R3/R4 rope pull, owner's "is there a causal graph?" (DAG rows C6, T9, C21, C26, C27; audit X40)

## Description
All 22 reference-fight links read "<beat> leads straight into the next exchange" (19 soft, 3 hard): a timeline. Written by Claude on 2026-10-10 when the example was built from the golden, which has no causal graph. `live_action_standoff` also has placeholders ("The stand-off answers itself" ×3); `wizard_vs_acrobat` and `ugc_glasses_demo` have real reasons.

## Impact
Checklist rows C6, T9, C21, C26, C27; audit X40 cannot pass while this holds.

## Proposed Fix
Real reasons per causal link, checked by CAUSE_REASON (M8.11).

## Owner Ruling
ADR-O15

## Related
- PLAN-001
- docs/reports/2026-10-11-renders-and-dag-adherence.md section 3

## Resolution
Caught by CAUSE_REASON (the checklist's caught_by; validators/checklist.py FINDINGS).
Review 4 (S-063): the golden's reasons state causes, but CAUSE_REASON, which the checklist reads as catching this, would pass a reason that states none ("The weather is nice and B likes tea."); F-185, RV-75.
