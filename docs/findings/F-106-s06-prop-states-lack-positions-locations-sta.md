# F-106 — S06 prop states lack positions, locations stay stale, two continuity checks cannot fire

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
medium

## Layer
L2.1

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
—

## Evidence
- the principal review, S-035 (docs/prompts/principal_review.md)
- ADR-O8 ("S06 carries them", prop p and v) is not built: every prop state's pos is null
- S06 keeps a held or worn prop's last location (the kunai at the end is embedded, held by A and on the ground; the glasses stay "tabletop" on the face); renderers/prop_samples.py works around it
- CONTINUITY_PRESENCE and CONTINUITY_TRIGGER pass by construction on pipeline input

## Description
The state layer does not hold what O8 put there, so later steps patch around it.

## Impact
Stale states flow into chained clips.

## Proposed Fix
Backlog RV-31: S06 carries prop positions; a held or worn prop's location clears; the continuity checks can fire.

## Owner Ruling
ADR-O8

## Related
- PLAN-007
- ADR-O8

## Resolution
Open.
