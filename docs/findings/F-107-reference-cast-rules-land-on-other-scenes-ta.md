# F-107 — Reference-cast rules land on other scenes' targets at S03

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
medium

## Layer
L1.5

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
- compiler/passes/mandatory/p03_constraint.py applies kernel reference rules word for word: in the UGC envelope "no duplicated kunai" and "FIVE props" land on the glasses, "no extra fighters beyond A and B" and "TWO fighter identities" on the single creator
- renderers/anime_renderer.py corrects them at S17; the S04 packet shows the raw text to its author

## Description
A fix made at S17 for data that is wrong at S03.

## Impact
Authors read rules that do not fit their scene.

## Proposed Fix
Backlog RV-32: S03 fills reference-cast rules per scene.

## Owner Ruling
none needed (R-10)

## Related
- PLAN-007

## Resolution
Open.
