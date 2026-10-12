# ADR-O86 — At 8.0 B moves to A's far side, so the pull runs toward the pillar

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-11

## Decided By
owner

## Scope
L1.1

## Decision
Owner, in chat, 2026-10-11, on F-071: "O77 is a real ruling (the kunai reverses to −Z). O21 is a real ruling (A starts
at y=10). Moving B is the least costly change — it doesn't touch the golden's physics, only the geometry."

## Context
F-071: since O77 the kunai lands at [0.6, 0, 4.0] and A crouches by it at 8.0 (O18, CONTACT_WORLD), at z 4.23; B stood
at z 4.7, between A and the pillar (z 6), so the rope dart's pull ran away from the pillar while the source says B is
dragged toward it.

## Consequences
- B's 8.0 anchor and key move to A's far side from the pillar, pose and facing unchanged; the rope dart's dart, on B's
  torso, moves with B (backlog M9-09h).

## Alternatives Considered
- Move the kunai's landing toward the pillar (against O77): not chosen.
- Move the pickup to another instant: not chosen.

## Supersedes
—

## Superseded By
—

## Related
- ADR-O18
- ADR-O21
- ADR-O77
- F-071
