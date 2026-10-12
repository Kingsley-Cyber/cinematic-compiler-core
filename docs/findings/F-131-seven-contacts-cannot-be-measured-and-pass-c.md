# F-131 — Seven contacts cannot be measured and pass CONTACT_WORLD without a word

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
medium

## Layer
L4c

## Status
open

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the second principal review, S-045 (docs/reports/2026-10-12-principal-review-2.md)
- reference fight b01_c3 and b09_c2 (no prop sample at the instant), b18_c1 and b18_c2 (the pillar's face); wizard b07_c1 (the pillar's face), b08_c2 and b08_c3 (no key at 6.4)
- solver/contact_world.py marks them not measurable; S13 passes them; RV-14 and RV-22 cover missing keys and the pillar's faces, not a missing sample

## Description
A contact the check cannot see passes as if it met.

## Impact
Holds and landings go unchecked.

## Proposed Fix
Backlog RV-47: a prop's point at a contact interpolated between its samples (or a sample required there); unmeasurable rows reported, and NOT CHECKED in the checklist, never passed.

## Owner Ruling
none needed

## Related
- PLAN-007
- F-089
- F-097

## Resolution
Open.
