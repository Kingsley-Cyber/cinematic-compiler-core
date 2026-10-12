# F-071 — A pulls B toward the pillar from the pillar's far side at 8.0

<!-- docs-version: 1.0 -->

## Type
contradiction

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
- examples/reference_fight/plans/temporal.json, beat b20 (8.0): A's anchor [0.11, 0.59, 4.23], B's [1.4, 1.18, 4.7]
- kernel/sources/lbn-2.3-adv.txt: "8.0 ... A PULLS B TOWARD PILLAR with rope dart, B is being dragged toward the
  pillar at z=6"; the golden's rule k_rules_27 (O18): "kunai picked up from ground at 8.0, A crouched by it"

## Description
Since O77 the kunai lands at [0.6, 0, 4.0]; O18 crouches A by it at 8.0, and CONTACT_WORLD (S-030) now puts A's right
hand on it, so A's root sits at z 4.23. B, whom A pulls with the rope dart at the same instant, stands at z 4.7, between
A and the pillar (z 6): a pull drags B toward A, away from the pillar, while the source says B is dragged toward the
pillar. Before S-030 A crouched at z 5.1 (between B and the pillar) and the hand missed the kunai by 1.33 m, the miss the
owner called expected; the same conflict, seen as a miss.

## Impact
The prompt asks for a pull toward the pillar while the bodies are placed for a pull away from it; no check reads a
pull's direction, so nothing refuses it.

## Proposed Fix
Owner's call, one of: B's 8.0 anchor moves to A's far side (z under 4.2, the drag then runs away from the pillar, so
"toward the pillar" is reworded); the kunai's landing moves toward the pillar (against O77's v_post); or the pickup
moves to another instant.

## Owner Ruling
none yet

## Related
- ADR-O18
- ADR-O77
- ADR-O83
- F-064

## Resolution
Open.
