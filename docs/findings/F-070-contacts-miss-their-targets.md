# F-070 — Most contacts miss their targets by forward kinematics

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
high

## Layer
L4c

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
—

## Evidence
- docs/reports/2026-10-11-contact-world-misses.md (`python -m validators.contact_world_report`, M9-06a, S-027)
- docs/reports/2026-10-11-contact-world-misses-trunk.md (the same, after M9-06c, S-029: hips read from the trunk,
  O84; the anime body, O85)

## Description
With forward kinematics (draft segments) and the repo-authored roots at the pelvis (O72), the four examples' touches,
holds and supports were measured at their instants. Measured 33 contacts: 9 within 0.15 m, 24 misses; 7 not measurable.  ## Misses by group  - Whose pose: repo-authored key: 12, source A row: 12 - Kind: foot or body on a surface: 7, limb to body: 4, limb to prop: 13 - Size: large (>1.0 m): 6, medium (0.3-1.0 m): 15, small (<0.3 m): 3 - Real or measurement artefact: artefact (airborne, prop moving): 2, artefact (airborne, rotating): 2, artefact (prop moving): 2, artefact (rotating): 3, real: 15

After M9-06c (S-029: hips read from the trunk, O84; the anime body's leg fitted to the source, O85; the
repo-authored roots re-rooted): 13 within 0.15 m, 20 misses (13 on repo-authored keys, 7 on the source's A rows);
the source's ground misses fell from 6 to 3 (3.00's right foot, the slide at 5.90).

## Impact
The prompts print two points per contact that are often apart; CONTACT_WORLD (0.15 m, O72) cannot refuse until the
owner has seen the list (ADR-O81).

## Proposed Fix
The owner reviews the report; M9-06b turns the refusal on with the poses re-blocked as the owner rules (the source's A
rows, ADR-O72, are kept unless the owner says otherwise).

## Owner Ruling
ADR-O81 (report first)

## Related
- ADR-O72
- ADR-O81
- F-025
- F-062
- PLAN-003

## Resolution
Open.
