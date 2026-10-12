# S-039 — RV-02a: CONTACT_WORLD per O89, the repo side of each miss re-blocked

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-02a (PLAN-007); findings F-075, F-076, F-079; rulings O89, O77, O80, O83, O86, O101, O102, O104

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-039]

## Plan
O89: an exact-instant miss is not an artefact. ADR-O104 reads "genuine airborne or prop-moving misses" as contacts
measured between keys or samples; every contact measured today sits at an exact instant, so no miss is exempt. Each
real miss is fixed on its repo-authored side, or listed with its reason when both sides are the owner's source:
1. The kunai's arc (b06_c1, 0.81 m; and the release b05_c1, 0.66 m): the 2.0 release at B's right hand, the deflect at
   2.5 at A's right foot, the velocity between them solved under gravity, O77's v_post kept from the foot; the kunai
   lands at about [1.4, 0, 3.77] at 2.72 and rests there; A's 8.0 pickup re-blocked to it, and B's 8.0 anchor (O86)
   moved so it does not stand on the kunai and stays on A's far side from the pillar (the rope dart's dart with it).
2. The palm on the log (b10_c1, 0.62 m): B's right arm re-posed to the log.
3. B's throw (b14_c1, 1.27 m): the volley's 5.5 sample at B's right hand, its velocity solved to the 5.9 sample.
4. The pellet (b09_c1, 0.81 m): the 3.7 sample at A's right hand, the 4.0 rest beneath it (O91's burst is RV-07).
5. B at A's knee (b12_c1, 0.19 m): B rises on straighter legs to meet the knee.
6. The vault (wizard b02_c1, 1.76 m): the hand plant is a support at the vault's first key (1.2, `at: start`),
   released at 1.6; the acrobat's 1.2 pose re-posed to reach the ground; the launch check accepts a launch whose first
   key stands on the hands only (a vault or handspring), still refusing one that starts turning on its feet.
7. The slide (b14_c2, b14_c3: A's soles 0.55 and 0.35 m over the ground at 5.9): both sides the source's, listed with
   their reason (O83 point 2).
8. F-079: the forward-kinematics tests say what they prove.

Predictions, made before the change:
1. The gate passes before the change: 640 tests (c40054b).
2. With no exemption and before any re-block, S13 refuses CONTACT_WORLD on 7 reference contacts and 1 wizard contact.
3. After the re-blocks every example compiles; the reference fight has two listed exceptions (the slide) and no other
   miss; the wizard has none; S16 may refuse the 8.0 shot after A and B move (uncertain, L-07).
4. The reference fight's and the wizard's outputs change; live action and UGC do not.
5. About 643 tests (a hand-launch test, a feet-launch break, an interpolation test); the golden test's records of the
   kunai's arc, the pellet, the volley, A's 8.0 pickup, B's 8.0 anchor and the exceptions change with O89 (ADR-O102).

## Decisions
- D1 — ADR-O104: a genuine artefact is a point interpolated between keys or samples while the actor is airborne or the
  prop moves; contact rows carry `interpolated` (false for every contact measured today); a turn alone never exempts.
  Why: O89's words; every measured contact has a key and a sample at its instant. Alternatives: keep the instant
  flags (what O89 rules out). Level: owner_default ADR under O101, for the owner to confirm.
- D2 — The kunai's deflect pair sits at A's right foot (the source's pose; the samples are the repo's); O77's v_post is
  kept, so the kunai lands at 2.72 on [1.4, 0, 3.77] and rests there. The 2.0 sample stays off B's hand, moved along z
  only (4.5 to 4.3) so the throw arrives along +Z as the rule says ("REVERSES from +Z to -Z"). Why: plan item 1 put it
  at B's hand, and the prompt then printed "moving up toward B": B's hand at 2.0 is on A's side of A's 2.5 foot, so a
  throw from it flies back toward B (L-26). Alternatives: the sample at B's hand (the throw reverses); B moved to a
  throwing distance now (B's whole 1.6-3.4 track moves: RV-02b with F-108 and RV-33 own it). Level: covered (O89,
  O77, R-17); the release and B's staging a named slice (RV-02b, F-075 kept open).
- D3 — The 8.0 tableau moves with the kunai's landing (+0.8 x, -0.23 z): A's crouch at it, pose kept; B's anchor, so O86's
  geometry holds (A's z 4.0 over B's 3.47); the dart on B's torso. Why: physics fixes the landing; A's 8.0 row and B's
  anchor are repo-authored (O18, O86). Alternatives: move A only (B would stand on the kunai); re-pose B. Level:
  covered (O86, O18, O89).
- D4 — The palm on the log: B's palm meets the log's own point (the source puts the log at A's root, p[0.4,1.1,4.7]; the
  post's centre stands at 1.0) within 0.1 m, B a step to its left (z 4.7 to 5.0), the lean eased from 35 to 20
  degrees, the arm extended, the root raised to 1.09 so the lower sole stays on the ground. Why: an arm-only re-block
  folds the arm down to the log and S15 refused the interval's rising Shape (SHAPE_DIRECTION): the palm would descend
  (L-26); lowering Sp dipped a sole 1.7 cm (L-27). Alternatives: the arm alone (refused, and it breaks the rising
  palm); measuring the post along its height (not needed once the palm meets the log's point). Level: covered (O89).
- D5 — The pellet leaves A's right hand at 3.7 and rests beneath it at 4.0. Why: O89; the samples are the repo's; O91's
  burst at A's body is RV-07. Level: covered.
- D6 — The volley leaves B's right hand at 5.5, its velocity solved to the 5.9 sample; its aim at A stays F-102's
  (RV-27). Level: covered.
- D7 — B rises to A's knee at 4.7 on straighter legs, both soles on the ground; the source puts the knee on B's spine
  at y=1.6. Level: covered.
- D8 — The vault hand (F-076): the plant is a support at the vault's first key (1.2, `at: start`), released at 1.6
  (`at: start` of b03); the acrobat dives onto the right hand with the feet off the ground (pelvis 0.56, Sp 75, the
  legs tucked); the run-in ends grounded and the vault requires it; the launch check accepts a first key on the hands
  alone and still refuses one on a foot. Why: F-076's fix; O80 ("a launch requires grounded support in the prior
  beat"). A root pitch was refused by MOTION_AXIS (the root must turn 90 degrees to 1.6), and Sp 110 with the pelvis
  at 0.89 turns the body backward from 1.2 to 1.6 (root plus Sp: 110 to 80; L-27). Alternatives: a touch while
  airborne (F-076's shortcut); the hand and the feet at the first key (F-058's pattern). Level: covered (O89, O80).
- D9 — The source's slide at 5.9 (b14_c2, b14_c3) is listed in contact_world_exceptions with its reason. Why: both sides
  are the source's; the owner's M9-06b ruling keeps the source's misses (ADR-O83 point 2). Level: covered.
- D10 — Tests changed as recorded deviations (ADR-O102), each with O89 in its comment: the golden test (DEFLECT_PAIR,
  PELLET, GROUNDED_PICKUPS 8.0, REBLOCKED_SAMPLES, REBLOCKED_ROOTS new, PULL_ANCHOR, CONTACT_EXCEPTIONS); the
  forward-kinematics tests (the pickup's target and printed point; F-079's labels; the dead clause); the motion
  tests (the artefact test re-pinned, a hand-launch test added); the release count and at-start contacts (6, the
  vault's two); three break strings; the deflect rows; FILLER_BEAT's break also empties b03's contacts (b03 now
  lifts the vault hand); the pickup distance (4.64 m); the kunai's spans (2.72); B@b12 joins RE_POSED, which now
  checks each re-posed key's words instead of skipping them. Nothing skipped or weakened. Level: covered (ADR-O102).
- D11 — validators/contact_world_report.py labels a miss an artefact by the new rule; a report after RV-02a is written.
  Level: covered.

## Duration
about 3 hours

## Changes
- solver/contact_world.py (`interpolated`, `artefact`); solver/euler_solver.py (`_hand_launch`, `_launch_findings`)
- examples/reference_fight/plans/temporal.json, motion.json (the kunai's arc and rest, the pellet, the volley, B at 4.0,
  4.7 and 8.0, A at 8.0, the dart at 8.0, the slide's exceptions); examples/wizard_vs_acrobat/plans/temporal.json,
  kinematic.json, motion.json (the vault's plant and release, the run-in's support, acrobat@b02); re-bound; outputs
  and checklists regenerated
- tests: test_reference_fight_golden, test_forward_kinematics, test_motion_solver, test_contact_pass,
  test_dag_conformance, test_dynamic_beat_validator, test_kinematic_solver, test_prop_track, test_leg_frame_rewrites
- kernel/knowledge_map.yaml (C21 note, the hand-launch locator; kernel log); validators/contact_world_report.py;
  docs/reports/2026-10-11-contact-world-after-rv-02a.md
- ADR-O104 (new); ADR-O83 related; F-076 and F-079 resolved; F-075 updated (open for RV-02b); backlog 14 (RV-02a done,
  RV-02b carries B's throw, RV-03 next); lessons L-26, L-27; CHANGELOG

## Verification
- before: 640 passed at c40054b (S-038's gate; the tree held only this slice's new files)
- after: `scripts/verify.sh` exit 0, 641 passed, docs plane PASS; `make golden` 26 passed; `compiler.rebind` silent;
  `contact_world.measure`: 33 contacts measured, 31 within 0.15 m, the 2 misses the slide's listed exceptions;
  `git status`: only the reference fight's and the wizard's outputs changed
- Prediction 1 held. Prediction 2 held (7 reference refusals, 1 wizard). Prediction 3 held: every example compiles,
  the reference fight lists the slide and nothing else misses, the wizard has none, S16 refused nothing; on the way,
  S15 refused the arm-only palm (D4) and S13 the pitched vault (D8). Prediction 4 held. Prediction 5 held in part: 641
  tests, not about 643 (one new test function; the interpolation checks went into the re-pinned test); the golden
  records changed as predicted, plus B's 4.0 and 4.7 roots.

## Next
RV-03 (the UGC pickup on the table).
