# S-023 — M9-09d: the kunai reverses to -Z at the deflect (F-064, O77)

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5)

## Gap
Backlog M9-09d; finding F-064; ruling O77

## Layer
L1.1

## Status
applied

## Commit
the commit whose message names [S-023]

## Plan
O77: "The golden is correct. The kunai reverses to -Z at 2.5. Fix the render." The post-contact sample takes the
source's own v_post [0.5, -4.0, -3.0]; gravity lands the kunai at 2.70 on [0.6, 0, 4.0] (computed, lesson L-15); the
rest samples (3.4) and A's pickup sample (8.0) move there. The prompts then print "post-contact v[0.5, -4, -3]
moving down along -Z" next to the rule "REVERSES from +Z to -Z".

Predictions, made before the change:
1. PROP_KINEMATICS passes with the landing sample at 2.70 (gravity gives y 0.004 there).
2. Nothing after S04 needs re-binding (no later packet holds the samples) and nothing refuses: A's pickup at 8.0 is
   1.49 m from A's root, inside PROP_KINEMATICS's and AIRBORNE_PICKUP's 2 m reach.
3. The reference fight's five prompts change in the kunai's rows and WHERE line; five tests pin the old numbers.
4. No checklist row changes result.

## Decisions
- D1 — The post velocity is the source's v_post, not a smaller -Z that would keep the landing near A's 8.0 crouch.
  Why: the owner ruled the golden correct, and v_post is the golden's own number. Alternatives: a gentler -Z (lands
  closer to A; not the golden's words). Downstream: A's hand is about 1.4 m from the kunai at 8.0; M9-06's
  CONTACT_WORLD (0.15 m, O72) will need A's pickup pose to reach it. Level: covered (O77).
- D2 — The landing sample sits at 2.70, the gravity instant (0.2006 s after 2.5), replacing the 2.9 sample. Why:
  PROP_KINEMATICS checks flight between samples and does not model the ground, so the flight's last sample is its
  landing. Level: covered (O8, F2.2's samples).

## Duration
about 20 minutes

## Changes
- `examples/reference_fight/plans/temporal.json` (the post velocity; the landing at 2.70; the rest and pickup samples)
- outputs regenerated; tests pinning the old numbers: DEFLECT_PAIR (golden), test_prop_track (two),
  test_dag_conformance (the PROP_VISIBILITY break), test_dynamic_beat_validator (the pair rows), test_kinematic_solver (the reach break)
- F-064 resolved; backlog; CHANGELOG

## Verification
- before: `scripts/verify.sh` exit 0, 620 passed (S-022, 7141adb)
- after: `scripts/verify.sh` exit 0, 620 passed (the first run failed: the pickup-reach break measured to the old
  rest point, 3.36 m; to the new one it is 3.81 m, computed)
- Prediction 1 held. Prediction 2 held (no re-bind, no refusal). Prediction 3 failed on the count: six tests pinned the old numbers, not five (the pickup-reach break too). Prediction 4 held.

## Next
M9-09e (F-065: a prop at rest has support; the pellet falls, O78).
