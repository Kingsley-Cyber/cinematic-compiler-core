# F-231 — Every prompt's legend hangs the legs from the root; the poses hang them from the spine (O84)

<!-- docs-version: 1.0 -->

## Type
contradiction

## Severity
high

## Layer
L6

## Status
resolved

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- renderers/prose_renderer.py, the [SPATIAL ANCHORS] frame line: "joints local to their parent (root -> Sp -> arms,
  NK -> HD; root -> legs)".
- kernel/knowledge_map.yaml, C29's note: the legend's parenting "which the solver uses".
- ADR-O84 (owner): "Forward kinematics reads hip angles from the trunk (the spine) in every key"; R-35.
- Principal review 8 (S-099, layers S01-S09): read the legend's way, B's soles sit on the floor at 6.45 (0.002 and
  -0.048 m) and 6.7 (-0.119 and -0.151 m), where forward kinematics puts them 0.22 to 0.5 m up (F-230).

## Description
Since ADR-O84 the legs hang from the spine, but the legend every prose prompt prints still parents them on the root,
so any key with a bent spine prints leg numbers the renderer is told to read in another frame.

## Impact
The renderer is told a different body from the one S13 checked, in every prompt with a leaning key.

## Proposed Fix
RV-113: the legend says root -> Sp -> legs (ADR-O84), C29's note follows, the examples are regenerated.

## Owner Ruling
ADR-O84

## Related
- ADR-O84
- R-35
- F-230
- RV-113

## Resolution
Resolved by RV-113 (S-100): the [SPATIAL ANCHORS] frame line says "joints local to their parent (root -> Sp ->
arms, legs, NK -> HD; the hips sit on the pelvis)", as forward kinematics composes them; C29's note follows (map 32).
The 16 prose prompts change in that line only.
