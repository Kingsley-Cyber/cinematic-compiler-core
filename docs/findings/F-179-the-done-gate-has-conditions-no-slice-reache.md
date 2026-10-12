# F-179 — The done-gate has conditions no slice reaches

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
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the fourth principal review, S-063 (docs/reports/2026-10-12-principal-review-4.md)
- docs/prompts/finish.md: fight_works asks for a new fight compiled end to end from a new query and render probes prepared for the owner; no backlog item plans either (the run report: "Render probes to run: none yet")
- RV-39 adds soul_check_passes and fight_works to the gate; nothing checks layer_order_matches_plan, rules_match_dag or no_shortcuts_survive

## Description
Finishing every planned slice would still leave three of the owner's six conditions unchecked and one untried.

## Impact
The run cannot reach done.

## Proposed Fix
Backlog RV-79 (a second fight from a new query through every step), RV-80 (render probes prepared for the owner, with F-015's; no render, R-29) and RV-39 widened to the six conditions.

## Owner Ruling
none needed (O98)

## Related
- RV-39
- RV-79
- RV-80
- ADR-O98
- F-015

## Resolution
Open.
