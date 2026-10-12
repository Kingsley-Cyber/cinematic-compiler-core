# F-165 — The log and the pellet do not follow the source at 3.7

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
- the third principal review, S-054 (docs/reports/2026-10-12-principal-review-3.md)
- the log is deployed at 3.7 by its state, but every WHERE line keeps it "0.00-4.00 at rest ... [0.4, 1, 5.3]"; A's 3.7 touch of it (b09_c2) cannot be measured, 0.90 m from A's hand
- the source deploys the pellet "at current position p[0.4,1.1,4.7]"; the golden bursts it at [1.18, 0.99, 4.85], 0.79 m away, and S06 never gives A the pellet though the records say it leaves A's right hand

## Description
RV-07 moved the states to 3.7, not the props.

## Impact
The swap shows the log arriving only when B's palm lands.

## Proposed Fix
Backlog RV-27 widened: the log at A's place at 3.7; the pellet's point asked of the owner (the source's point or A's hand).

## Owner Ruling
the question open (the pellet's point)

## Related
- PLAN-007
- F-082
- F-102
- RV-27

## Resolution
Open in part: the log takes A's former place at 3.7 (RV-48a, S-057); the pellet's point waits for the owner.
