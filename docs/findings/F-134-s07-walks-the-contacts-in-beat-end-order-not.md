# F-134 — S07 walks the contacts in beat-end order, not by their instants

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
medium

## Layer
L2.2

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
- compiler/passes/mandatory/p07_contact.py `events_of` sorts beats by t + dur; S04 and S06 use the contact's instant
- in memory (the S01-S09 reviewer): a possess at 0.0 in a 2 s beat and a release at 1.0 in a 0.5 s beat give a false CONTACT_RELEASE and an endless hold; a hand holding X that takes Y at 0.5 raises no CONTACT_HAND; S08 and S09 reuse it

## Description
Latent since `at: start` contacts exist.

## Impact
Wrong holds and missed double holds.

## Proposed Fix
Backlog RV-17: sort by (instant, releases first, beat id), with two break tests.

## Owner Ruling
none needed

## Related
- PLAN-007
- F-092

## Resolution
Open.
