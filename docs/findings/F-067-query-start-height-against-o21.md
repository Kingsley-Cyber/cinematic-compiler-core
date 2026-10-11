# F-067 — The query says "falling from y=8"; O21 starts A at y=10

<!-- docs-version: 1.0 -->

## Type
contradiction

## Severity
low

## Layer
L0

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
—

## Evidence
- examples/reference_fight/request.json and kernel/sources/lbn-2.3-adv.txt: "A starts ABOVE the frame, falling from y=8"
  (the pillar's top is y=8)
- docs/decisions/ADR-O21-*.md: "A starts above the frame at root y=10 ('falling from y=10')"
- every reference-fight prose prompt (S-015): the SCENE line quotes the query; the staff starts A at root y=10

## Description
O21 moved A's start above the 8 m top so A falls onto it, and quotes the source as "falling from y=10", which the
source does not say. The query is the owner's text and stays as written, so each prompt now says "falling from y=8"
in its first line and starts A at y 10 in the staff.

## Impact
A reader meets two start heights; R19 suggests the model follows the staff's later wording (V6), but it is untested
on the full fight.

## Proposed Fix
The owner picks: keep the query as is (the SCENE line is the owner's request), or correct the query to "falling from
y=10" for the reference example; M9-08b prints V6's wording either way.

## Owner Ruling
none yet

## Related
- ADR-O21
- F-010
- F-016

## Resolution
Open.
