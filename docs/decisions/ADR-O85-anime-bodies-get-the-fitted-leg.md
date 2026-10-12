# ADR-O85 — Anime bodies get the fitted leg; live action and UGC keep the adult

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
Owner, in chat, 2026-10-11: "Anime bodies get the fitted leg (×1.25, standing pelvis 1.22m, roughly a 2.1m body).
Live-action and UGC keep the 0.98m adult. The card gains an anime body entry. The two anime examples (reference fight,
wizard) use the anime body. The live-action knight and the UGC creator use the 0.98m adult. Small schema change"

## Context
M9-06c (S-029): the leg fitted to the source's grounded A rows (O82) under the trunk reading (O84) is 1.25 times the
draft adult's. PLAN-003 F5.1 already asks for segment lengths "per archetype or body mode"; S-027 had drafted one
adult for every body.

## Consequences
- `library/body_segments.yaml` holds two bodies, `adult` and `anime`, and the genre that uses each;
  `schemas/cards/body_segments.schema.json` follows (version bump, logged).
- S13's packet carries the body of the scene's genre; S04's SURFACE_HEIGHT bound reads that body's standing leg.

## Alternatives Considered
- Every body gets the fitted leg (O82 as written): not chosen.

## Supersedes
—

## Superseded By
—

## Related
- ADR-O24
- ADR-O82
- ADR-O84
- F-070
