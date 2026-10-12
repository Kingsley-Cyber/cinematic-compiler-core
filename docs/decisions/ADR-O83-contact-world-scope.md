# ADR-O83 — What CONTACT_WORLD refuses: repo misses re-blocked, source misses kept as exceptions, artefacts exempt

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-11

## Decided By
owner

## Scope
L4c

## Decision
Owner, in chat, 2026-10-11: "Then proceed with M9-06b: re-block the repo-authored misses, keep the source misses as
exceptions (calibrated to the trunk reading), exempt the artifacts, and push."

The three points as the agent proposed them, now ruled:
1. The repo-authored keys that miss are re-blocked to meet within 0.15 m (rule R-33).
2. The source's A rows that still miss under the trunk reading (ADR-O84) and the anime body (ADR-O85) stay as
   written and are listed as recorded exceptions in the golden test; CONTACT_WORLD does not refuse them.
3. A contact flagged as a measurement artefact (the actor airborne or turning, or the prop moving at the instant)
   is reported, not refused.

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
- ADR-O89
- ADR-O104
