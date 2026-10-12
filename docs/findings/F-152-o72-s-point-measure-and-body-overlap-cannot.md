# F-152 — O72's point measure and BODY_OVERLAP cannot both hold for body contacts

<!-- docs-version: 1.0 -->

## Type
question

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
- the third principal review, S-054 (docs/reports/2026-10-12-principal-review-3.md)
- O72: a touch whose limb-end point and target point are more than 0.15 m apart is refused (ADR-O72)
- S-049 (RV-49) measures a contact between two bodies from surface to surface, with the body card's draft radii, to the whole trunk and shoulders (solver/contact_world.py `_rows`; forward_kinematics.surface_gap): A's knee at 4.7 reads 0.009 m and the wizard's kick at 3.6 0.02 m, which O72's point measure reads 0.252 m and 0.206 m
- a knee resting on the trunk's surface sits 0.21 m (0.13 + 0.08) from the trunk's axis, so no pose meets O72's 0.15 m to the torso point without the knee inside the trunk, which BODY_OVERLAP refuses
- the surface measure with 0.15 m allows up to 15 cm of air between the surfaces (rules reviewer G1; layers S10-S18 G3)

## Description
S-049 changed the measure of an owner ruling without asking (R-06), and labelled it covered.

## Impact
A body contact passes under a measure the owner did not set, and the tolerance it allows is not the one O72 set.

## Proposed Fix
Waits for the owner: O72's point measure (and BODY_OVERLAP's radii relaxed), the limb's point to the target's surface, or surface to surface, and the tolerance. Until then the surface measure built in S-049 stays as the builder's interim, listed for the owner. Then RV-55.

## Owner Ruling
the question open

## Related
- PLAN-007
- F-144
- ADR-O72
- RV-55

## Resolution
Open.
