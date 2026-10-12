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

Owner, in chat, 2026-10-11, after S-030: "Anime bodies only. [...] The card gains an anime body (standing pelvis 1.22m,
×1.25 the draft adult). The two anime examples use it. The live-action knight and the UGC creator keep the 0.98m adult.
Schema change: body_segments has two entries (adult, anime). Genre profiles gain a body_type field. The FK solver reads
body_type from the genre profile. No per-key flag. No per-performer frame. Update the card, the schema, and the genre
profiles."

## Context
M9-06c (S-029): the leg fitted to the source's grounded A rows (O82) under the trunk reading (O84) is 1.25 times the
draft adult's. PLAN-003 F5.1 already asks for segment lengths "per archetype or body mode"; S-027 had drafted one
adult for every body.

## Consequences
- `library/body_segments.yaml` holds two bodies, `adult` and `anime` (card 3 then, card 4 since S-033; schema 3.0, logged); each genre profile
  (`library/genre_profiles/<genre>.yaml`, the genre profile cards of `schemas/genre_profile.schema.json`, O65; S-033)
  names its `body_type`: anime for anime, adult for live action and UGC; `solver/forward_kinematics.segments` reads it.
  S-029 had put the genres in the card and S-031 the body type in the modality schemas.
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
