# ADR-O72 — A key's root is the pelvis, and a touch's two points meet within 0.15 m

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
Owner, in chat, 2026-10-11: "ADR-O72: Root position = pelvis. Tolerance = 0.15m. Update the repo-authored keys
to match the source."

## Context
The agent's proposal the owner ruled on (S-012 to S-018):
Proposed by the agent during autopilot run 1 (S-012), for the owner to rule on:
1. A key's root position is the pelvis (the hip centre), as the owner's source writes A's rows (y 0.6 to 0.9 while
   standing or crouched on both feet); the repo-authored anchors at y 0 for standing bodies move up to the standing
   hip height of the new segment-length card, as recorded deviations in each example.
2. CONTACT_WORLD refuses a touch whose limb-end point (forward kinematics, O24) and target point are more than 0.15 m
   apart at the contact time.

M9-06 (F5.1/F5.2, owner O24) computes hand and foot points from the root and the joint angles. The convention
(kernel/conventions.yaml, Q6) fixes axes and the rest pose but not what the root position is, and the data holds both
readings in one scene: reference_fight A at y 0.9 (b07), 0.6 (b19, b20), 0.7 (b23) on both feet, from the source; B at
y 0 on both feet (b01, b07, b19, b20), repo-authored. Forward kinematics on either reading puts the other performer's
feet underground or in the air. The plan names the contact tolerance an owner value ("a tolerance (owner value)").

## Consequences
- Accepting 1 re-authors the S04 anchors and S13 root positions of every repo-authored standing or crouched key in
  the four examples (a deviation per example, ADR-O71 rule 1 once accepted); the owner's A rows stay.
- Accepting 2 lets M9-06 refuse a contact that misses; a looser value lets more authored poses through unchanged.
- Until the owner ruled (2026-10-11, accepted), M9-06 was blocked and M9-14a (which depends on it) waited; M9-06 then
  built forward kinematics and CONTACT_WORLD on it.

## Alternatives Considered
- The root is the ground point under the pelvis: keeps B, moves the owner's A rows (against the source).
- Read the root per key from its support (feet: ground point; airborne: pelvis): two conventions in one field.
- A tolerance of 0.25 m (the prop tolerance, PROP_KINEMATICS): looser; 0.15 m is about a hand's width.

## Supersedes
—

## Superseded By
—

## Related
- F-066
- ADR-O24
- ADR-O71
- PLAN-003
