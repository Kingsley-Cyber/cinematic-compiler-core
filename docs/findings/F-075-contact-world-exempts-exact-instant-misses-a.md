# F-075 — CONTACT_WORLD exempts exact-instant misses as artefacts, and never measures a release

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
high

## Layer
L4c

## Status
resolved

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
RV-02a (S-039, O89, ADR-O104): only a point interpolated between keys or samples, with the actor airborne or the prop
moving, is an artefact; the repo side of each exact-instant miss is re-blocked and the source's slide is listed.
RV-02b (S-043, ADR-O105): CONTACT_WORLD measures a prop's release
(tests/test_forward_kinematics.py::test_a_release_leaves_the_prop_where_the_hand_is); B throws the kunai from A's -Z
side, from B's right hand at 2.0, so it arrives along +Z and goes back down toward B, as the source's rule says.
