# F-101 — Momentum is judged from sparse keys, and every off-arc anime span floats

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
medium

## Layer
L4a

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
- compiler/passes/derived/p11_kinematic.py momentum_findings takes off and lands at the last and first supported keys
- 17 float keys cover all 8 off-arc anime spans (S-021); none was re-timed
- A's opening fall (y 10 at 0 to 8.71 at 0.6) is not judged and needs an upward start; F-036: renders show late takeoffs

## Description
The check passes because spans declare hang time, not because they follow the arc. Question: which anime spans keep a declared hang (O74) and which are re-timed?

## Impact
Long hangs invite the late-takeoff failure the renders showed.

## Proposed Fix
Backlog RV-26 (blocked on the question): the true takeoff and landing; the opening fall judged; each span re-timed or hung.

## Owner Ruling
ADR-O74; the question open

## Related
- PLAN-007
- ADR-O74
- F-036

## Resolution
Open.
