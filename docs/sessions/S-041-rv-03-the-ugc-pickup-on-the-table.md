# S-041 — RV-03: the UGC pickup on the table, no resting-prop jump, the UGC poses agree with their words

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-03 (PLAN-007); finding F-077; rulings O101, O102; rules R-17, R-33; after RV-08 (S-040)

## Layer
L1.1

## Status
applied

## Commit
the commit whose message names [S-041]

## Plan
F-077: the glasses rest on the tabletop at [0.25, 0.75, 0.35] at 0.0 and sit at [0.2, 1.1, 0.3] at the 1.5 pickup, so
they leave the table before the hand reaches them; PROP_KINEMATICS lets a resting prop move whenever a contact falls
on its next sample; S-030 then posed the hand to meet the floating glasses, and the re-posed keys no longer match
their words. The query says "Creator holding the glasses", so the creator holds them from the first frame:
1. The pickup is `at: start` (0.0): the right hand takes the glasses where they rest on the table; the 1.5 sample is
   the lift (held at chest height).
2. PROP_KINEMATICS (S04): a prop at rest is still where it rested at the instant a contact takes or strikes it; the
   rest-to-contact jump is refused (a contact strictly between two samples still changes the flight).
3. The UGC keys re-posed to their words, each a recorded deviation: 0.0 "the right hand reaching down for the folded
   glasses" (the hand on them on the table, leaning in); 1.5 "the left fingers swing the temples open" (the left hand
   at the glasses); 3.5 "Both hands raise the open glasses to the face, elbows out" (both hands at the glasses);
   5.5 "the right index finger tapping the frame" (the right hand at the frame on the face).
4. The put-on's left-hand touch names the left temple (each hand on its own temple, as two_hand_symmetric and "slide
   the temples over the ears" say), not the right.

Predictions, made before the change:
1. The gate passes before the change: 642 tests (385153e).
2. With the narrowed rule and the old UGC data, S04 refuses PROP_KINEMATICS on the UGC glasses only (the 1.5 jump);
   the other three examples pass S04 unchanged.
3. After the re-authoring every example compiles; every UGC contact meets within 0.15 m, the pickup at 0.0 on the
   tabletop; only the UGC's outputs change.
4. The UGC prompts print the glasses held from 0.00; the tests pinning the UGC's track and strings move with it (each
   recorded under F-077 and R-17), plus a PROP_KINEMATICS break for the rest jump: about 643 tests.

## Decisions
- D1 — RV-08 first: with the possess at the first frame S07 refused HOLDER_CONTACT (S06 committed the holder at the beat's
  end, F-061); this slice was shelved (git stash), RV-08 landed as S-040, and RV-03 resumed here. Level: covered (R-10).
- D2 — The creator holds the glasses from the first frame: the possess is `at: start` (0.0) where they rest, and the 1.5
  sample is the lift. Why: the query says "Creator holding the glasses" (R-17) and F-077's fix. Alternatives: split b01
  into a reach and a lift (a new beat and key, every later step re-authored); keep the pickup at 1.5 (the 1.5 key holds
  them at chest height). Level: covered (F-077, R-17).
- D3 — PROP_KINEMATICS: a resting prop is where it rests at the instant a contact takes it; the exception for a contact
  at the second sample goes, and a contact strictly between two samples still moves it. Level: covered (F-077).
- D4 — The glasses rest on the creator's right ([-0.25, 0.75, 0.35], was [0.25, 0.75, 0.35]). Why: the right hand picks
  them up; on the left the least-change reach needed a 45-degree spine twist that "Upright at the desk, leaning in" does
  not have (L-26); on the right it is a small lean (Sp 20 to 30). Alternatives: the twist. Level: covered (R-17, R-33).
- D5 — The keys follow their words, each the least change found by the scratch solver: 0.0 the right hand on the
  glasses; 1.5 the left hand at the glasses; 3.5 both hands at the glasses' sides, the elbows out (spread bounded at 20
  degrees or more); 5.5 the right hand at the frame on the face. Level: covered (R-33, F-077).
- D6 — The put-on's left hand takes the left temple (b03_c1, was the right temple): "slide the temples over the ears",
  two_hand_symmetric, each hand on its own temple. Level: covered.
- D7 — Shot c02 is motivated by its unfold beat (b02): its pickup contact moved to 0.0, outside the shot (S16
  CAMERA_MOTIVATION); c01's path rises with the lifting hand instead of drifting down to the desk. Level: covered.
- D8 — Tests moved with the data (ADR-O102): two break strings, the glasses' first span ("held by A R hand"), the
  no-place fixture also drops the contacts (the glasses are held from 0.0); a new PROP_KINEMATICS break test and its map
  locator (kernel log). Level: covered.

## Duration
about 1 hour, with RV-08 between

## Changes
- planner/dynamic_beat_validator.py (the rest rule)
- examples/ugc_glasses_demo/plans/temporal.json (the possess `at: start`, the rest on the right, the left temple),
  motion.json (four keys), camera.json (c01's path, c02's motivation); re-bound; outputs and checklist regenerated
- tests: test_dynamic_beat_validator (new test), test_dag_conformance, test_prop_track
- kernel/knowledge_map.yaml (locator; kernel log); F-077 resolved; backlog 16 (RV-03 done, RV-06 next); lesson L-29;
  CHANGELOG

## Verification
- before: 642 passed at 385153e (S-040's gate)
- after: `scripts/verify.sh` exit 0, 643 passed; `make golden` passed; `compiler.rebind` silent; every UGC contact within
  0.15 m (the pickup 0.06 m at 0.0 on the table); only the UGC's outputs changed; checklist counts unchanged
- Prediction 1 held. Prediction 2 held (S04 refused the UGC glasses only). Prediction 3 held; on the way S07 refused the
  first-frame possess (D1) and S16 the shot's motivation (D7). Prediction 4 held (643 tests).

## Next
RV-06 (the vanish, O90).
