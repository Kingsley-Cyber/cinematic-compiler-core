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
Noted in S-081 (the sixth review): S07 walks a beat's contacts in list order: the golden's b19 with its support listed
after its release is refused (CONTACT_RELEASE), and a second opening of an open support listed after a release passes
(RV-17, pulled forward).
Noted in S-090 (principal review 7): S-083 removed b19's pair; the live instance is b11, whose releases listed before
its at-start supports give CONTACT_RELEASE on b11_c1 and b11_c2, then CONTACT_DUPLICATE on b14_c2 and b14_c3
(p07_contact.lifecycle, reviewer's run). RV-17 carries it.
