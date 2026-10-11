# F-066 — What is a key's root position: the pelvis or the ground point?

<!-- docs-version: 1.0 -->

## Type
question

## Severity
high

## Layer
L4c

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
—

## Evidence
- kernel/conventions.yaml (Q6): axes, Euler order and rest pose; nothing on the root position
- examples/reference_fight/envelope.json motion keys on both feet: ninja_lean@b07 y 0.9, @b19 and @b20 y 0.6, @b23
  y 0.7 (the owner's source rows); ninja_broad@b01, @b07, @b19, @b20 y 0
- docs/plans/deconfliction_2026-10-11.md F5.2: "a tolerance (owner value)"

## Description
Forward kinematics (M9-06, O24) needs to know where the root sits on the body. The owner's rows put it at the pelvis;
the repo-authored rows put a standing body's root on the ground. The contact tolerance is reserved for the owner.

## Impact
M9-06 (world contact points, CONTACT_WORLD) and M9-14a (timed kinetic chain, which needs them) cannot be built.

## Proposed Fix
Rule on ADR-O72 (recommended: the pelvis; 0.15 m).

## Owner Ruling
none yet

## Related
- ADR-O72
- ADR-O24
- F-025
- PLAN-003

## Resolution
Open.
