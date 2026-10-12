# F-093 — Declared validators never run, and the envelope records no validation

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
medium

## Layer
all

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
- kernel/layer_order.yaml `validated_by` names coherence (S02), invariants and constraint, which exist only as registered names (validators/layer_dependency_validator.py)
- card `genres` lists are never read, so a ugc_ad-only world could ground an anime scene
- every envelope's validation.schema, .invariants and .layer_dependency are null, while camera_kinematic_coupling says "pass"

## Description
The layer order promises checks that do not run, and the envelope's validation block says nothing about the ones that do.

## Impact
A reader of the envelope cannot tell what was validated.

## Proposed Fix
Backlog RV-18: S02 coherence (a card's genres against the scene's); the validation block records what ran; the constraint run stays M9-03a (blocked on the owner).

## Owner Ruling
none needed

## Related
- PLAN-007
- F-019
- F-020

## Resolution
Open.
