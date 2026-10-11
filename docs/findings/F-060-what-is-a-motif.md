# F-060 — What is a motif?

<!-- docs-version: 1.0 -->

## Type
question

## Severity
low

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
schemas/motif.schema.json (DRAFT); the owner's docs-plane request named a motif schema and a "Motif library" plan

## Description
The owner asked for `schemas/motif.schema.json` and showed a "Motif library" plan, but no plan, decision or data in
the repo defines a motif. The draft schema guesses: a reusable choreographic pattern (ordered beat skeletons with
roles and relative timing) plus the callbacks that echo an earlier beat (O50).

## Impact
The schema validates nothing until a motif is defined; building a motif library without a definition would be a guess.

## Proposed Fix
The owner defines a motif (and whether the library feeds S04 authoring as templates); the schema leaves draft then.

## Owner Ruling
none yet

## Related
- PLAN-005
- ADR-O65
- ADR-O50

## Resolution
Open.
