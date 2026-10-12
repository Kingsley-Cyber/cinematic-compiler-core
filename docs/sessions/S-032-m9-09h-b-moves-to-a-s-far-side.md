# S-032 — M9-09h: at 8.0 B moves to A's far side, so the rope dart's pull runs toward the pillar (F-071, O86)

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5)

## Gap
Backlog M9-09h; finding F-071; rulings O18, O21, O77, O86; rule R-33

## Layer
L1.1

## Status
applied

## Commit
the commit whose message names [S-032]

## Plan
O86 (owner): "Moving B is the least costly change — it doesn't touch the golden's physics, only the geometry." At 8.0 A
crouches at the kunai, root [0.11, 0.59, 4.23], facing +X; B stands at [1.4, 1.18, 4.7] facing -X, between A and the
pillar (z 6). B's S04 anchor and S13 root move along z only, to [1.4, 1.18, 3.7]: B keeps its pose, facing and height,
stays in front of A, and the rope from B to A's hand now points about 20 degrees toward the pillar; from 8.0 to 8.5 B is
dragged 1.3 m toward the pillar, passing about 1 m beside A. The rope dart's dart, on B's torso since S-030, moves with
B (its 8.0 sample to [1.6, 1.53, 3.7], 1.84 m from A's root, inside the 2 m reach).

Predictions, made before the change:
1. The gate passes before the change: 639 tests.
2. Every step passes after a re-bind: no TELEPORT (B covers 1.04 m from 7.5 and 1.36 m to 8.5 in 0.5 s), CONTACT_WORLD
   still meets b19_c1 (the dart moves with B's torso), the held dart stays inside 2 m; S16 may refuse shot c19 (framed
   on the midpoint of A and B; uncertain), which would need its angle searched with S16's own validator (L-07).
3. Only the reference fight's outputs change: B's 8.00 root and path words, the dart's printed point and its WHERE
   span; no checklist row changes result.
4. 640 tests (one test that the pull runs toward the pillar).

## Decisions
- D1 — B moves along z only, from 4.7 to 3.7: the least move that puts B on A's far side from the pillar (z under 4.23)
  with a pull clearly toward it (about 20 degrees off the x line between them); x, height, pose and facing stay, so
  B still faces A across the rope. Why: O86 ("only the geometry"). Alternatives: z just under 4.23 (a pull about 5
  degrees toward the pillar, barely visible); B on the pillar line behind A (B would cross A's body when dragged).
  Level: covered (O86); the distance is an interpretation (F-053).
- D2 — The dart's 8.0 sample moves with B's torso (S-030 put it there). Why: CONTACT_WORLD on b19_c1. Level: covered.
- D3 — F-071's proposed fix had said the pull would then run away from the pillar and need rewording; it runs toward
  it, as written. The finding is corrected in its resolution. Level: covered.

## Duration
about 20 minutes

## Changes
- `examples/reference_fight/plans/temporal.json` (B's b20 anchor, the dart's 8.0 sample), `motion.json` (B's b20 root);
  re-bound; outputs and checklists regenerated
- `tests/test_reference_fight_golden.py` (PULL_ANCHOR, the moved sample); ADR-O86; F-071 resolved; backlog (M9-09h done,
  M9-10 next); CHANGELOG

## Verification
- before: `scripts/verify.sh` exit 0, 639 passed (S-031, d39663e)
- after: `scripts/verify.sh` exit 0, 640 passed; `make golden`: only the reference fight changed (B's 7.50 and 8.00
  step words, from "steps left-forward" to "steps left", and the dart's printed point)
- Prediction 1 held. Prediction 2 held (every step passed; S16 kept shot c19 as it was). Prediction 3 held (no
  checklist row changed result). Prediction 4 held: 640.

## Next
The owner's ten asymmetric things per beat (ADR to record, map, plan).
