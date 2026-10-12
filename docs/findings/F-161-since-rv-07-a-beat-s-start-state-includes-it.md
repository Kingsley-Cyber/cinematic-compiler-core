# F-161 — Since RV-07 a beat's start state includes its own at-start effects in S10

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
- the third principal review, S-054 (docs/reports/2026-10-12-principal-review-3.md)
- solver/prop_state_machine.py: a snapshot at a beat's start includes the beat's own at-start effects, while REPLAY_REQUIRES reads before them
- compiler/passes/derived/p10_affordance.py reads that snapshot as the state before the interaction: marking UGC b02's temples=open as at: start passes S04 and S06 and S10 refuses "unfold needs [folded] before, found open"; the converse lets an effect meet its own precondition
- compiler/passes/derived/p09_object_state.py drops each change's instant, so OBJECT_STATE_TRIGGER can credit a hand that arrives after the change

## Description
S06 and S10 read "before a beat" two ways.

## Impact
Latent: an at-start effect can satisfy or break its own beat's precondition.

## Proposed Fix
Backlog RV-61: S10 reads the state before the beat's own effects, as S06's requirements do; S09 carries each change's instant.

## Owner Ruling
none needed

## Related
- PLAN-007
- F-132
- RV-61

## Resolution
Open.
