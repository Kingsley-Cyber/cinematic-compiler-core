# F-132 — RULES' 'From t to the end' lines time a change at its beat's end, not at its instant

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
medium

## Layer
L6

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
- renderers/prose_renderer.py and validators/prompt_validator.py build "From t to the end" from the beat's t + dur, not from S06's transition t (RV-08)
- a transition that carries two commits keeps only the later as its t (the wizard's acrobat@b11 to b12: 7.8 and 8.6, kept as 8.6); entity rows are not printed today

## Description
Latent: no example triggers it yet.

## Impact
A change of hands at an at-start contact would be printed late.

## Proposed Fix
Backlog RV-07 (it moves the smoke's commit too): every change carries its own instant, and both sites read it.

## Owner Ruling
none needed (F-061, ADR-O107)

## Related
- PLAN-007
- F-061

## Resolution
Open.
