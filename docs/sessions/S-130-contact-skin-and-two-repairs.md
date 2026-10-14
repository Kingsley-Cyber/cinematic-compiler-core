# S-130 — Contacts with a surface measured from the skin; the solver repairs a lifted support and a beat-end contact

<!-- docs-version: 3.0 -->

## Date
2026-10-13

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
The R20 idea re-run (R21 attempt) stopped at S13 on five CONTACT_WORLD misses; three were the checker's, two the
solver's (owner: "go ahead and fix")

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-130]

## Plan
1. CONTACT_WORLD measures a part meeting a surface from its skin (its capsule's radius off the bone's axis; a sole is
   already the foot's underside), as body to body (RV-49): a key's claimed supports and the contacts both.
2. The re-block solver repairs a claimed support off its surface (it skipped them: "<slot>:<part>" names no contact):
   the part goes onto the surface's nearest point, its skin on it.
3. The solver repairs a contact on the key at the contact's own instant (a contact at its beat's end is the next
   beat's key; it re-posed the beat's first key, which has no contact then).

Predictions, made before the change (18:31 by the clock):
1. The failed run's knight torso (0.20 m) and arm (0.19 m) misses measure 0.07 and 0.14 m: under 0.15.
2. The examples pass unchanged.

## Decisions
- D1 — The skin, not a looser tolerance: a tolerance would pass the real misses too (F-233's lesson). Level: covered.
- D2 — The 1.08 m kick was not a routing gap: its anchors were in reach, so AA-10 rightly did not send it to S04; the
  solver posed the wrong key. Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the chained gate commits |
| graft used | PASS | solver/contact_world.py and compiler/author.py repair_motion read through the S-125 map |
| Tests | PASS | tests/test_contact_skin.py new (3): the skin, the lifted foot, the beat-end strike |

## Duration
from 18:31 to 18:38

## Changes
- solver/contact_world.py (skin, surface_miss), compiler/author.py (repair_motion); examples, checklists; tests

## Verification
- Prediction 1 held by construction (0.20 - 0.13 = 0.07; 0.19 - 0.05 = 0.14), and the planted lifted foot (0.213 m) is
  repaired to no finding.
- Prediction 2 held: 833 passed.
