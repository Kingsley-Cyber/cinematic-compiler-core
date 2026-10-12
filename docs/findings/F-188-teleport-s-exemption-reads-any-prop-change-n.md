# F-188 — TELEPORT's exemption reads any prop change, not the decoy

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
high

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
- the fifth principal review, S-072 (docs/reports/2026-10-12-principal-review-5.md)
- planner/dynamic_beat_validator.py `_teleports`: a substitution that changes any prop exempts its actor's jump; probe: a substitution that changes a kunai 5 m away, with no prop at the actor's anchor (`decoy()` None), lets the actor move 20 m in 0.5 s
- S-064 D3 labelled this "covered (O12)"; O12 says "decoy revealed"; tests/test_dynamic_beat_validator.py's teleport test calls a beat that reveals no decoy one that "reveals a decoy"

## Description
RV-66 narrowed the decoy for S04's swap and S07, and left the actor's own teleport on the old reading.

## Impact
A body can teleport after a substitution that leaves no decoy in its place.

## Proposed Fix
Backlog RV-86: the exemption needs `decoy(before)`; the teleport test's substitution places its decoy, recorded under ADR-O102.

## Owner Ruling
none needed to narrow it (O12's words); listed with F-196

## Related
- RV-86
- F-169
- ADR-O12
- ADR-O48

## Resolution
Open.
