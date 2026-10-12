# F-171 — PROP_SUPPORT takes a location word as support at any height

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
medium

## Layer
L1.1

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
- planner/dynamic_beat_validator.py `_prop_support`: any location fact since the prop's last hold counts as support; probe: the spent pellet resting at y 1.1 with "location ground" passes from 4.0, O78's founding case

## Description
The location word stands in for the surface under the prop; F-053 lists the height and worn readings, not this one.

## Impact
A prop may rest in the air with a word under it.

## Proposed Fix
Backlog RV-74: when the location names a surface with a known top, the resting prop lies within 0.1 m of it.

## Owner Ruling
none needed (O78)

## Related
- RV-74
- ADR-O78
- F-053

## Resolution
Open.
