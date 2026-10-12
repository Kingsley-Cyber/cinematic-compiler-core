# S-042 — RV-06: the vanish: A's supports and holds end at 3.7; the rope dart lies on the ground until 7.5

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-06 (PLAN-007); finding F-081; rulings O90, O18, O86, O89, O101, O102; rules R-17, R-33

## Layer
L1.1

## Status
applied

## Commit
the commit whose message names [S-042]

## Plan
O90 (owner): "End A's supports and holds at 3.7. The rope dart is on the ground at 3.7 until A picks it up at 7.5."
F-081: A's foot supports (3.0) run to their releases at 4.7 and the rope dart's hold (3.0) to 5.9, straight through the
substitution (3.7 to 4.4), while the prompt says A has no body, pose or support then.
1. VANISHED_BODY (S04) also refuses a vanished actor's support or hold that is open inside its vanish window.
2. At 3.7 (the substitution beat's start) A's feet and left hand let go; the rope dart drops from A's left hand
   ([1.18, 1.12, 4.51]) and lands below it at 4.0, beside the spent pellet, and rests there; its holder becomes none at
   3.7 and its location ground at 4.0. A reappears at 4.4 on both feet, as its row says, and leaves the ground at 4.7.
   The 5.9 release and its sample go.
3. A's 7.5 crouch moves with the dart (+0.78 x, +0.71 z), pose and facing kept, so the left hand takes it where it
   rests; B's 7.5 anchor moves to keep A's head facing B without B standing on the dart (the least change, as O86 moved
   B).
4. The words follow (each a recorded deviation): A's rows 4.4 to 6.3 no longer hold the rope dart; the slide's rule
   ("rope dart released at 5.9 during slide") says it was left on the ground when A vanished.

Predictions, made before the change:
1. The gate passes before the change: 643 tests (4e93b1a).
2. The extended VANISHED_BODY refuses the current reference fight (A's supports and hold open across 3.7-4.4) and
   nothing else.
3. After the data change every example compiles; the rope dart's track reads held 3.0-3.7, falling 3.7-4.0, at rest on
   the ground 4.0-7.5, held from 7.5; only the reference fight's outputs change; S16 may refuse the 7.5 shot after B
   moves (uncertain).
4. CONTACT_WORLD: A's new 4.4 supports meet the ground (the source's row is a grounded row that meets) and the 7.5
   pickup meets the dart within 0.15 m.
5. About 645 tests (a VANISHED_BODY break and a should-not-fire); the golden test's records of A's 7.5 crouch, the
   rope dart's words and the reworded rule change with O90.

## Decisions
- D1 — VANISHED_BODY at S04 also refuses a vanished body's support or hold left open inside its window: S04 is the first
  step that sees the contacts and the substitution (R-10). Level: covered (O90).
- D2 — At 3.7, the substitution beat's start, A's feet and left hand let go. Level: covered (O90).
- D3 — The rope dart drops from A's left hand ([1.18, 1.12, 4.51]) at 2.25 m/s and lands beneath it at 4.0, beside the
  spent pellet. Why: "on the ground at 3.7" read with the substitution beat's 0.3 s for the fall; a let-go from rest
  would need a free-fall rule that PROP_KINEMATICS and PROP_SUPPORT do not have (interpretation, labelled here).
  Alternatives: the dart on the ground at the release instant (a 1.1 m jump the rest rule of RV-03 refuses); tossed to
  its old 5.9 spot (a throw no words ask for). Level: covered (O90), the drop speed an interpretation.
- D4 — A reappears at 4.4 on both feet (supports at b11's start), as its row says ("support=both feet"), and leaves the
  ground at 4.7 as before. Level: covered (R-17).
- D5 — The 5.9 release, its sample and effects, and the slide beat's requirement that A holds the dart go. Level:
  covered (O90's consequences).
- D6 — The 7.5 crouch moves with the dart (+0.78 x, +0.71 z), pose and facing kept: A's heading at 7.5 must stay
  between 7.0's -30 and 8.0's 90 degrees without a declared turn. B's 7.5 anchor moves to [1.46, 1.15, 5.0], in front of
  A, so A's head still faces B and B does not stand on the dart (as O86 moved B). Level: covered (O90, O86, O18).
- D7 — Shot c10 becomes a full shot (1.68 m to 3.2 m away) so A's feet show when A reappears (S16 CAMERA_COUPLING).
  Level: covered.
- D8 — The words follow, each recorded in the golden test: A's rows 4.4 to 6.3 stop holding the dart (ROPE_DART_WORDS)
  and the slide's rule says it was left at the substitution (VANISH_RULE); the description check applies a list of
  rewrites per row (OPENING_WORDS kept). Level: covered (O90, R-33, ADR-O102).
- D9 — `_open_contacts` keeps a pair's first opening; a second opening of an open pair is S07's CONTACT_DUPLICATE.
  Level: covered.

## Duration
about 1 hour 15 minutes

## Changes
- planner/dynamic_beat_validator.py (VANISHED_BODY's open supports and holds, `_open_contacts`)
- examples/reference_fight/plans/temporal.json (the vanish's releases and the dart's drop, A's 4.4 supports, the 5.9
  release gone, the slide's rule, 7.5 anchors), motion.json (A's and B's 7.5 roots, A's words 4.4-6.3), camera.json
  (c10 full); re-bound; outputs and checklist regenerated
- tests: test_dynamic_beat_validator (new test), test_reference_fight_golden (ROPE_DART_WORDS, VANISH_RULE, the 7.5
  root, `reworded`), test_dag_conformance (a break string)
- kernel/knowledge_map.yaml (locator and note; kernel log); F-081 resolved; backlog 17 (RV-06 done, RV-02b next);
  CHANGELOG

## Verification
- before: 643 passed at 4e93b1a (S-041's gate)
- after: `scripts/verify.sh` exit 0, 644 passed; `make golden` passed; `compiler.rebind` silent; only the reference
  fight's outputs changed; checklist counts unchanged
- Prediction 1 held. Prediction 2 held (the reference fight alone: both feet and the left hand). Prediction 3 held: the
  dart's WHERE line reads held 3.00-3.70, ballistic 3.70-4.00, at rest on the ground 4.00-7.50, held from 7.50; S16
  refused not the 7.5 shot but c10 (the new 4.4 supports in a medium shot; D7). Prediction 4 held (the 4.4 soles at
  0.01 and 0.058 m; the pickup 0.06 m). Prediction 5 held in part: 644 tests, one new (the should-not-fire run is the
  gate's compile of every example); the golden records changed as predicted.

## Next
RV-02b (releases measured; B's kunai throw re-staged).
