# S-043 — RV-02b: CONTACT_WORLD measures releases; B's kunai throw re-staged

<!-- docs-version: 2.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-02b (PLAN-007); findings F-075, F-108; rulings O89, O77, O23, O101, O102, O105 (new)

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-043]

## Plan
F-075's last part: CONTACT_WORLD never measures a release, so a thrown prop may leave from anywhere; the kunai's 2.0
sample sits 0.66 m from B's hand. S-039 found why it cannot simply move there: B's hand at 2.0 is on A's side of A's
2.5 foot, so a throw from it flies back toward B. The source's rule says the kunai comes in along +Z, toward A, and
goes back along -Z, toward B and the ground: B throws from A's -Z side.
1. F-108 answered first (ADR-O105): the kunai leaves B's hand once, at 2.0.
2. CONTACT_WORLD measures a prop's release: the prop's sample at the release instant against the releasing part.
3. B's throw re-staged: B steps to A's -Z side by 1.6 ([1.4, 1.19, 3.3], facing A on the pillar), throws at 2.0 from
   [1.77, 1.14, 2.97] facing between A and A's 2.5 foot, and watches at 2.5 ([1.77, 1.19, 3.0]); the pose is kept and
   turned; the kunai's 2.0 sample sits at B's right hand, its velocity solved to A's foot, so it arrives along +Z and,
   deflected (O77), lands in front of B ("toward B and ground").
4. The measured releases: the kunai (2.0), the rope dart (3.7), the UGC glasses (5.5).

Predictions, made before the change:
1. The gate passes before the change: 644 tests (6db3d60).
2. With releases measured and the old data, CONTACT_WORLD refuses the kunai's release at 2.0 only (0.66 m); the rope
   dart's at 3.7 and the glasses' at 5.5 meet.
3. After the re-staging every example compiles; the kunai's track reads "2 ... moving up toward A" (or along +Z) and the
   pre-contact "moving down along +Z"; S16 may refuse the 2.0 shot after B moves (uncertain).
4. Only the reference fight's outputs change in text; every example's envelope may change (the S13 packet carries the
   releases).
5. About 646 tests (a release break, a should-not-fire); the golden test records B's re-staged anchors and the kunai's
   2.0 sample with O105 and O89.

## Decisions
- D1 — F-108 answered first (ADR-O105): the kunai leaves B's hand once, at the 2.0 throw; the 0.5 line is the windup.
  Why: the rules, the camera, A's 2.0 row and B's Laban line name one throw, at 2.0; a 0.5 release along -Z flies away
  from A. Level: owner_default ADR under O101, for the owner to confirm.
- D2 — CONTACT_WORLD measures a release of a prop, not a part leaving a surface: a takeoff's key is already in the air,
  and a support is measured while it holds. Level: covered (F-075's fix).
- D3 — B is re-staged on A's -Z side at 1.6, 2.0 and 2.5, pose kept and turned (yaw 340, 347, 320 degrees, each step
  under 90), so the throw leaves B's hand toward A, arrives along +Z and is deflected back down toward B, the source's
  rule. Alternatives: B farther along +X facing -X (the kunai would arrive along -X, against "from +Z"); the 2.0 sample
  left off the hand (F-075's shortcut). Level: covered (O105, O77, R-17).
- D4 — The kunai's 2.0 sample sits at B's right hand ([1.19, 1.88, 3.45]), its velocity solved to A's foot
  ([0.2, 0.95, 1.98]) and the pre-contact velocity from gravity. Level: covered.
- D5 — Every S13 packet carries the releases, so the examples were re-bound. Level: covered.
- D6 — Tests: the deflect pair's text in two tests and the golden's records (B's three anchors, the kunai's 2.0 sample)
  move with O105; a new release break test and its map locator (kernel log). Level: covered (ADR-O102).

## Duration
about 50 minutes

## Changes
- solver/contact_world.py (releases of props measured)
- examples/reference_fight/plans/temporal.json, motion.json (B at 1.6, 2.0, 2.5; the kunai's 2.0 sample); every
  example re-bound (S13's packet); outputs and checklists regenerated
- tests: test_forward_kinematics (new test), test_reference_fight_golden, test_dynamic_beat_validator
- kernel/knowledge_map.yaml (locator, note; kernel log); ADR-O105 (new); F-075 resolved; F-108 answered in part (RV-33
  ready); PLAN-007; backlog 18 (RV-02b done, RV-04 next); CHANGELOG

## Verification
- before: 644 passed at 6db3d60 (S-042's gate)
- after: `scripts/verify.sh` exit 0, 645 passed; `make golden` passed; `compiler.rebind` silent; no CONTACT_WORLD
  refusal in any example; checklist counts unchanged
- Prediction 1 held. Prediction 2 held (the kunai's release at 0.667 m only; the rope dart 0.007, the glasses 0.118).
  Prediction 3 held: the kunai's lines read "moving up toward A", "moving down along +Z" and, after the deflect,
  "moving down toward B"; S16 refused nothing. Prediction 4 held in part: the UGC's prose changed too (its release now
  prints both points). Prediction 5 held in part: 645 tests, one new; the golden records changed as predicted.

## Correction (S-046)
D3 and the Verification credit "the source's rule" for the kunai going back toward B. The source's rules say
"NOT toward B"; its A row and its B and kunai tracks say "toward B and ground". The prompts then printed "moving down
toward B" beside "NOT toward B" (F-122); ADR-O108 settles the reading (S-046).

## Next
RV-04 (records: versions, logs, the hook, stale docs and findings).
