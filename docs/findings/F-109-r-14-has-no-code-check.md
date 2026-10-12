# F-109 — R-14 has no code check

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
low

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
- docs/rules.yaml R-14 enforced_by: "kernel/layer_order.yaml (reviewed; no code check yet)"

## Description
Whether each state layer writes nodes and edges is reviewed by eye only.

## Impact
A layer could stop writing edges unnoticed.

## Proposed Fix
Backlog RV-34: validators/layer_dependency_validator.py checks R-14.

## Owner Ruling
none needed

## Related
- PLAN-007

## Resolution
Open.
