# F-142 — The declared `invariants` validator has no definition and no slice

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
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the second principal review, S-045 (docs/reports/2026-10-12-principal-review-2.md)
- kernel/layer_order.yaml declares `validated_by: [schema, invariants, constraint]` on S02-S09; ADR-O62: "the declared validators run after every layer that declares them"
- compiler/pipeline.py runs none of them; no module defines `invariants` (F-019, F-020 and F-093 name the run, not the definition)

## Description
A validator the layer order promises does not exist.

## Impact
The layer order overstates what runs.

## Proposed Fix
Backlog RV-18 widened: define `invariants` from the kernel's invariants (kernel/invariants.yaml) and run every declared validator after its step, recording the result in the envelope.

## Owner Ruling
ADR-O62

## Related
- PLAN-007
- F-019
- F-020
- F-093

## Resolution
Open.
