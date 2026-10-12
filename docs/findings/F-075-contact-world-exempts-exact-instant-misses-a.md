# F-075 — CONTACT_WORLD exempts exact-instant misses as artefacts, and never measures a release

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
2026-10-11

## Reporter
agent

## Legacy ID
—

## Evidence
- the principal review, S-035 (docs/prompts/principal_review.md)
- solver/contact_world.py `artefact`: the actor airborne or turning, or any prop velocity above 1e-9; `MEASURED` = touch, possess, support
- docs/reports/2026-10-11-contact-world-after-m9-06b.md: 8 of 9 misses exempt, among them B's throw at 5.5 (1.27 m), B's palm on the log at 4.0 (0.62 m) and the vault hand at 2.0 (1.76 m), all on repo-authored data
- the kunai's release point sits 0.66 m from B's hand (the principal review, S-035 (docs/prompts/principal_review.md))

## Description
The artefact flags (S-027 D6, applied in S-030) exempt a miss whenever the actor is airborne or turning or the prop moves, yet the key, the prop sample and the contact share one instant, so nothing about the measurement is uncertain. Release contacts (throws) are not measured at all.

## Impact
No throw, knock or airborne strike can be refused; the prompts print hands and feet up to 1.8 m from what they strike.

## Proposed Fix
Backlog RV-02 (O89): exempt only genuine airborne or prop-moving misses (read as a contact measured between keys or samples, for the owner to confirm); re-block B's throw, the palm on the log and the vault hand; measure releases; each source exact-instant miss gets its repo side moved or a listed exception with its reason.

## Owner Ruling
ADR-O89

## Related
- PLAN-007
- ADR-O83
- ADR-O89
- F-070

## Resolution
In part. RV-02a (S-039, O89, ADR-O104): only a point interpolated between keys or samples, with the actor airborne or
the prop moving, is an artefact, and no contact measured today is one; B's throw, the palm on the log, the vault hand,
the kunai's deflect, the pellet and B at A's knee are re-blocked on their repo-authored side; the source's slide at
5.9 is listed (ADR-O83 point 2). Open for RV-02b: releases are not measured, and the kunai's 2.0 sample still sits off
B's hand; there B's hand is on A's side of A's 2.5 foot, so a throw from it would fly back toward B: B's throw needs
re-staging with B's track (F-108, RV-33).
