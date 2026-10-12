# S-024 — M9-09e: a prop at rest has something under it; the smoke pellet falls (F-065, O78)

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5)

## Gap
Backlog M9-09e; finding F-065; rulings O78, O75 (R-33)

## Layer
L1.1

## Status
applied

## Commit
the commit whose message names [S-024]

## Plan
O78: "The smoke pellet must fall after bursting. Fix the prop physics. Add a check: a prop at rest must have support
or be on a surface." S04 checks PROP_SUPPORT on every resting sample of a free prop: within 0.1 m of a surface's top
(the ground, or a raised top from its world card), or placed by a fact since its last hold (a location, or worn: yes).
The pellet, at rest at A's hand height from 3.70, is thrown down by A's touch and lands where it bursts at 4.00.

Predictions, made before the change:
1. PROP_SUPPORT fires once in the four examples: the pellet at 3.70; the log (standing, location ground), the shuriken
   (in the pillar), the kunai and rope dart (on the ground) and the worn glasses pass.
2. With the pellet's fall the reference fight compiles without re-binding; its five prompts change in the pellet's rows.
3. No checklist row changes result.

## Decisions
- D1 — The pellet bursts as it lands at 4.00: A's touch at 3.70 throws it down at 2.2 m/s (computed so gravity brings
  it to the ground at 4.00, S06's burst time), and it rests on the ground (location ground at 4.00). Why: the owner's
  "fall after bursting" taken literally would leave it 0.3 s in mid-air before the burst, with no hold, which the new
  check refuses; the burst time is the source's. Alternatives: a possess from 3.70 to 4.00 and a fall after (new
  contacts through S07 and S08). Level: interpretation within O78 (F-053), for owner review.
- D2 — "On a surface" is read by height (surfaces have no extent), and a card's worn state is the wearer's support.
  Level: interpretation (F-053).
- D3 — PROP_SUPPORT is a step code (S04) on map row C31; the prompt already prints the rest place (WHERE). Level:
  covered.

## Duration
about 25 minutes

## Changes
- `planner/dynamic_beat_validator.py` (`_prop_support`, SUPPORT_M); `examples/reference_fight/plans/temporal.json`
  (the pellet's throw, landing sample and location); outputs regenerated
- tests: a PROP_SUPPORT test (test_dynamic_beat_validator), PELLET (golden); `kernel/knowledge_map.yaml` C31 (kernel
  log); F-065 resolved; F-053; backlog; CHANGELOG

## Verification
- before: `scripts/verify.sh` exit 0, 620 passed (S-023, 9976f53)
- after: `scripts/verify.sh` exit 0, 622 passed
- Prediction 1 held. Prediction 2 held (no re-bind; five outputs). Prediction 3 held.

## Next
M9-09f (F-067: the query says A falls from y=10, O79).
