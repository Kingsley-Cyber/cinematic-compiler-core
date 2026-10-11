# F-003 — The conformance test passed placeholders

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
high

## Layer
all

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
F3

## Evidence
38/84 rows verified (DAG rows M4, all partial rows)

## Description
CAUSAL_LIST_MISSING only checks that each link is listed, not that it states a cause. The same pattern runs through the test: it verifies what the renderer writes, not every DAG requirement.

## Impact
Checklist rows M4, all partial rows cannot pass while this holds.

## Proposed Fix
The per-prompt checklist (M8.10) judges every map row; M4 stays NOT CHECKED until a code catches what the renders saw.

## Owner Ruling
ADR-O6

## Related
- PLAN-002
- docs/reports/2026-10-11-renders-and-dag-adherence.md section 3

## Resolution
Open: no code catches it yet.
