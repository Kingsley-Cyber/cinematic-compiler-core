# F-228 — CONTACT_WORLD reads a free prop between its samples on a straight line; S04 reads a gravity arc

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
low

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
- Principal review 7 (S-090, layers S01-S09): S04 holds a free prop between samples to gravity
  (planner/dynamic_beat_validator.py:17-18, 398); solver/contact_world.py `_prop_at` (S-088) runs it straight, and
  S-088 D1 called that "covered (ADR-O104)", which says nothing of a path; F-053 did not list it.
- Latent: no contact in the four examples falls between two samples of its prop.

## Description
Two steps read one prop's path two ways.

## Impact
A contact on a flying prop between samples would be measured against a point the prop never passes.

## Proposed Fix
RV-110: CONTACT_WORLD follows S04's arc for a free prop and the holder's hand for a held one; a test plants each.

## Owner Ruling
none needed

## Related
- ADR-O104
- F-053
- RV-110

## Resolution
Open.
