# ADR-O87 — The compiler records ten asymmetric things per beat; the schema is a concept map

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-11

## Decided By
owner

## Scope
all

## Decision
Owner, in chat, 2026-10-11: "The compiler must record ten asymmetric things per beat: per-limb poses (not symmetric),
an asymmetry flag, the kinetic chain order, the limb path, the lead limb, the contact point per limb, the smear per
limb, the speedlines per limb, the hand and foot orientation, and the follow-through per limb — because Naruto fights
are never mirrored, the force travels through a chain, the lead limb strikes and the trail balances, and if any of
these isn't declared, the renderer invents it and the fight looks like a dance instead of a fight."

The owner's table (pasted with the message):

| # | What | Field |
|---|---|---|
| 1 | Per-limb poses | body.left_arm, body.right_arm, body.left_leg, body.right_leg |
| 2 | Asymmetry flag | body.symmetry |
| 3 | Kinetic chain order | body.kinetic_chain |
| 4 | Limb path | limbs.<limb>.path |
| 5 | Lead limb | strike.lead, strike.trail |
| 6 | Contact points per limb | contact.source_part, contact.target_part |
| 7 | Limb-specific smear | anime.smear[].limb |
| 8 | Limb-specific speedlines | anime.speedlines[].limb |
| 9 | Hand and foot orientation | body.left_hand, body.right_foot |
| 10 | Follow-through per limb | follow_through.<limb> |

The owner's framing (pasted with the message), in short: the schema is a concept map, not a checklist or a contract;
it says what the compiler must know, not the exact shape of every file. Record what is real; where a field does not
fit the beat, add a field or reinterpret the one there is; never force a beat into the schema.

## Context
Recorded after S-032. Each item is mapped against the repo (where it lives, its step, its checks, its slice) in the
plan this ruling opens; items the repo already records keep their fields under the concept's name.

## Consequences
- Every beat's pose data carries the ten things; a missing one is a gap with a backlog slice.
- Field names follow the concept, not the table's spelling, where the repo already holds the concept.

## Alternatives Considered
- —

## Supersedes
—

## Superseded By
—

## Related
- R-20
- ADR-O22
- ADR-O24
- ADR-O84
