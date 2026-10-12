# F-123 — The S13 author can list its own CONTACT_WORLD exceptions

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
high

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
- the second principal review, S-045 (docs/reports/2026-10-12-principal-review-2.md)
- compiler/passes/derived/p13_motion.py: refusals(rows, document.get("contact_world_exceptions", {})) reads the authored plan
- solver/contact_world.py `refusals` accepts any listed real miss with any reason
- schemas/graphs/motion_plan.schema.json: "only the owner's source rows (ADR-O83), recorded in the golden test" is a description only; only the reference fight's golden test pins the list

## Description
An exception door: a new compile can exempt its own misses.

## Impact
CONTACT_WORLD can be passed by listing the miss (no-shortcuts types 2 and 3).

## Proposed Fix
Backlog RV-43: exceptions come only from an owner-held list in the kernel (the scene's query hash, the contact, the ruling), logged; S13 reads that list and refuses any other.

## Owner Ruling
ADR-O83 (point 2: only the owner's source rows)

## Related
- PLAN-007
- ADR-O83
- ADR-O89

## Resolution
Open.
