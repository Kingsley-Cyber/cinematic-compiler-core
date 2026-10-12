# ADR-O83 — What CONTACT_WORLD refuses: repo misses re-blocked, source misses kept as exceptions, artefacts exempt

<!-- docs-version: 1.0 -->

## Status
proposed

## Date
2026-10-11

## Decided By
owner_default

## Scope
L4c

## Decision
Proposed by the agent for M9-06b; the owner said "start M9-06b" without ruling on these three points:
1. The repo-authored keys that miss are re-blocked to meet within 0.15 m (rule R-33; the agent recommended this).
2. The source's A rows that miss stay as written and are listed as recorded exceptions in the golden test (ADR-O72
   "update the repo-authored keys to match the source", ADR-O81 "do not rewrite the source"); CONTACT_WORLD does not
   refuse them. The agent gave no recommendation here; this is the default that keeps the owner's rows.
3. A contact flagged as a measurement artefact (the actor airborne or turning, or the prop moving at the instant) is
   reported, not refused (the agent recommended this).

## Context
F-070's miss list; ADR-O82 (calibrate first). These points decide how much of the examples M9-06b rewrites.

## Consequences
- M9-06b refuses only real misses on repo-authored keys and non-excepted source rows.

## Alternatives Considered
- Re-pose the source's A rows (against O72 and O81 unless the owner says so).
- Refuse artefacts too (re-blocks flights and moving props).

## Supersedes
—

## Superseded By
—

## Related
- ADR-O72
- ADR-O81
- ADR-O82
- F-070
