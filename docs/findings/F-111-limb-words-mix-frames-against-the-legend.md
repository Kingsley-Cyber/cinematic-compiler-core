# F-111 — Limb words mix frames against the legend

<!-- docs-version: 1.0 -->

## Type
question

## Severity
medium

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
- solver/staff_geometry.py reads limbs in the trunk's frame (the legs since O84), the head in the chest's and the body against gravity; the legend says "mid while within 45 degrees of horizontal"
- at 1.1 the right leg prints "back-mid" while it points up in the world; a vertical support leg under a 20-degree lean prints "forward-low" (UGC 0.00)

## Description
The words describe directions relative to different frames, while the legend promises one. Question: should limb and head words read against gravity (Labanotation's standard cross of axes) while the hips are still read from the trunk for the body's geometry (O84)?

## Impact
The model misreads limb directions.

## Proposed Fix
Backlog RV-36 (blocked on the question).

## Owner Ruling
the question open

## Related
- PLAN-007
- ADR-O84

## Resolution
Open.
