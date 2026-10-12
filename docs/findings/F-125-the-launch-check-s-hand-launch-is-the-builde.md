# F-125 — The launch check's hand launch is the builder's widening; an all-supported flip run skips its end key

<!-- docs-version: 1.0 -->

## Type
risk

## Severity
medium

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
- the second principal review, S-045 (docs/reports/2026-10-12-principal-review-2.md)
- solver/euler_solver.py `_hand_launch` (S-039) accepts a first key on the hands alone, for any turn run
- O80: "The wizard must land before launching ... a launch requires grounded support in the prior beat"; O89 asks to re-block the vault hand, not to widen a check; F-099 / RV-24 wait on the owner; S-039 D8 called it covered
- euler_solver `_launch_findings` skips a run whose keys are all supported, though the run leaves out its end key: a 360-degree flip between two grounded keys passes with no airborne key

## Description
The hand launch is an interpretation that accepts any hands-only launch; the skip lets a named flip turn on the ground.

## Impact
A launch the owner never ruled on passes; a flip can be authored as a roll.

## Proposed Fix
Backlog RV-24 (with F-099): the hand launch is labelled an interpretation and tied to a beat whose action plants the hands (a vault or a handspring); a run is judged with its end key.

## Owner Ruling
with F-099 (O80's words)

## Related
- PLAN-007
- ADR-O80
- F-076
- F-099

## Resolution
Open.
