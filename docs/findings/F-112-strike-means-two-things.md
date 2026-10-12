# F-112 — "Strike" means two things

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
medium

## Layer
L1.1

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
- renderers/prose_renderer.py treats a touch as a strike when its beat holds an S17 impact frame, ignoring S04's verb (b10_c1 has verb "strike" and no impact frame)
- planned checks at S04, S13 and S15 (AS-01, AS-03, M9-14a, M9-14b) key on strikes, which R-13 forbids them to read from S17

## Description
There is no strike definition the earlier steps can see.

## Impact
Strike checks would be placed at the wrong step or read later data.

## Proposed Fix
Backlog RV-37: one definition at S04 (a contact whose verb is a strike verb); S17's impact frames must agree with it; AS-01 follows it.

## Owner Ruling
none needed (R-13)

## Related
- PLAN-007
- PLAN-006

## Resolution
Open.
