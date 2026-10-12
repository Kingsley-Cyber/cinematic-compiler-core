# F-091 — render.txt's laban chains mix both fighters' moves

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
high

## Layer
L6

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
- examples/reference_fight/render.txt laban.A includes "throw kunai" (B's move); laban.B begins "fall from above>kick off pillar>throw kunai>foot deflect kunai>..." (A's moves)
- renderers/anime_renderer.py writes beat labels into each chain; the owner's 2.3 and 2.4 sources give each fighter his own chain

## Description
The LBN-2.4 laban field, the owner's own format, now tells the model each fighter does the other's moves.

## Impact
Identity of action blurs between A and B.

## Proposed Fix
Backlog RV-16: one chain per fighter from that fighter's own beats, as the 2.4 source writes it.

## Owner Ruling
none needed (ADR-O1)

## Related
- PLAN-007
- ADR-O1

## Resolution
Open.
