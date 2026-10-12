# F-219 — The body model has no ankle joint: a crouching foot cannot lie flat

<!-- docs-version: 1.0 -->

## Type
gap

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
- solver/forward_kinematics.py: the sole lies 0.1 m along the shin from the ankle (`joints`), so the foot turns with
  the shin; there is no ankle flexion
- S-083 (RV-95): asked to keep the ankles 0.045 m (the foot's radius) over the floor with both soles on it, the 7.5
  solve reached only 0.025 to 0.032 m at every root from 0.39 to 0.57 m; the committed keys hold them at 0.012 (7.5) and
  0.038 m (8.0), so the bound became the model's own convention (the ankle over the floor, the sole the contact point)

## Description
A foot is the shin's extension, so a crouching shin lays its foot almost flat on the floor along the shin's line
rather than standing the foot flat under the ankle.

## Impact
Crouches, kneels and lunges cannot show a flat foot or a raised heel; the foot's capsule grazes the floor in every deep
crouch.

## Proposed Fix
With AS-02 (O87 item 9, the foot set): an ankle joint the keys can set, so a foot can stand flat, on its ball or on its
toes, and the floor checks read the foot's own segment.

## Owner Ruling
none needed (O87 item 9 asks for the foot set)

## Related
- AS-02
- F-206
- F-072

## Resolution
Open.
