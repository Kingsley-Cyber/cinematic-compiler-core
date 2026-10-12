# F-002 — No prompt prints the reasons

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
high

## Layer
L6

## Status
resolved

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
F2

## Evidence
Prompt text (DAG rows C6, V7, V8)

## Description
Prose CAUSAL LINKS lists names and arrows only; LBN-2.4 has no causal list (causal edges appear only as camera motivations).

## Impact
Checklist rows C6, V7, V8 cannot pass while this holds.

## Proposed Fix
Print 'Why each link holds:' under CAUSAL LINKS (M8.11).

## Owner Ruling
ADR-O15

## Related
- PLAN-001
- docs/reports/2026-10-11-renders-and-dag-adherence.md section 3

## Resolution
Caught by CAUSE_REASON (the checklist's caught_by; validators/checklist.py FINDINGS).
Review 4 (S-063): the golden's reasons state causes, but CAUSE_REASON, which the checklist reads as catching this, would pass a reason that states none ("The weather is nice and B likes tea."); F-185, RV-75.
