# S-083 — RV-95: the pickups re-blocked from a recorded command, every part above the floor

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-95 (PLAN-007); findings F-206, F-110, F-207; rulings O18, O72, O11

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-083]

## Plan
S-080's re-block of A's pickups left the right knee 0.109 m in the floor at 7.5, kept each pickup hand bearing
weight through a throw (7.5 to 8.0) and a leap (8.0 to 8.5), left the pinned words describing the old pose, and
justified a 0.40 m crouch by a search that froze the spine's twist (F-206; review 6). The class: a re-block that keeps
its contact and loses a part of the body, and its record.
1. The shape a pickup must keep, stated before any solve: both soles within 0.02 m of the floor and within 0.15 m of
   their place; the grasping hand within 0.03 m of its prop; every knee 0.08 m (the thigh's radius) and every ankle
   0.045 m (the foot's) over the floor; the other hand 0.3 m up; the head 0.2 m over the pelvis; the trunk (root pitch
   plus spine) leaning 70 degrees or less.
2. The crouch's height: the highest root, from A's own crouch (0.57 and 0.59 m, S-029) down in 0.01 m steps, at which
   solver/reblock.py meets every bound; each solve recorded as its command from the committed key (a62e551), and a test
   re-derives it.
3. The hand is not a support: it grasps the prop at the key and the feet bear the weight, so S-080's four S04 contacts
   and two S11 hand supports go; render.txt and the staff print one support per row.
4. The pinned words (DEV-10) re-written from the new numbers by a stated rule: a limb's direction from its vector, its
   bend in 15-degree steps (bentN).
5. The solver's `above` reads the joints (an ankle) as well as the contact points.

Predictions, made before the change (09:26 by the clock):
1. The gate passes before the change: 714 tests (a62e551, S-082's chained gate).
2. 7.5 meets every bound at a root between 0.50 and 0.57 m.
3. 8.0 needs a root at or below 0.50 m to meet every bound.
4. With the hand supports gone, S11, CONTACT_WORLD's claims and S15's shapes pass, and the prose prints one support on
   A's 7.5 and 8.0 lines.
5. The prose changes on A's 7.0, 7.5, 8.0 and 8.5 lines only (the 7.0 and 8.5 lines print the drop and rise to and from
   the crouch); about 715 tests (714 and a re-derivation test).

## Decisions
- D1 — The bounds were stated before any solve. The ankle bound (0.045 m, the foot's radius) proved unattainable with
  both soles on the floor in this body model, whose foot is the shin's extension: the 7.5 solve held the ankles at
  0.025 to 0.032 m at every root from 0.39 to 0.57 m. It became, after the solve and recorded here, the model's own
  convention: the ankle over the floor, the sole the contact point (CONTACT_WORLD measures the sole). F-219 files the
  foot. Level: interpretation (F-053).
- D2 — The crouch's height is the highest root, searched down from A's own crouch, at which every bound holds: 0.57 m at
  both pickups (8.0 missed at 0.59 m by 0.002 m on the head bound). Level: covered (O18; the procedure in the Plan).
- D3 — A hand grasping its prop at a pickup bears no weight; the feet do. S-080's four S04 contacts and two S11 hand
  supports go, and each row prints one support. At 7.50 that support reads "steps left alternating", which b19's action
  ("A runs to the kunai") and the staff's rule (a performer travelling on its feet to its next key) both say. Level:
  interpretation (F-053).
- D4 — The pinned words (DEV-10) come from the numbers by a rule: bent N is 15 N degrees (the source's "arm fwd high
  bent3" at 45), a limb's direction from the staff's sectors (forward and its diagonals "fwd", back "back", left or
  right "side", place "down" or "up"). Level: interpretation (F-053).
- D5 — The two commands are recorded in tests/test_reblock.py, which runs them from the keys S-080 committed (START, the
  same keys `--from a62e551` reads) and asserts the committed bones; it costs about 20 s of the gate. Level: covered
  (F-207's fix).
- D6 — The solver's `above` reads a joint (an ankle) as well as a contact point. Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the chained gate commits |
| One gap, right layer | PASS | A's two S13 keys with the S04 anchors and S11 supports they rest on |
| Predictions written first | PASS | the session file was written at 09:26, before any solve |
| New behaviour, old behaviour | PASS | the search's table (every root from 0.57 and 0.59 down) and the two recorded commands; the shape test now asserts the knees, the ankles, the 70-degree lean and the feet-only support; the re-derivation test passes |
| Neighbours | PASS | the re-bind ran every step from S04 to S17 (S11's KINEMATIC_SUPPORT, CONTACT_WORLD's claims and pickups, FLOOR_PENETRATION, BODY_OVERLAP, S15's shapes, S16's framing); render.txt prints one support per pickup row; the 7.50 staff words checked against b19's action |
| The step's instructions teach it | PASS | euler_solving.txt says the pose shows the kinematic node's support and the world checks (S-078); nothing new to teach |
| Tests changed with their data | PASS, recorded | GROUNDED_PICKUPS and GROUNDED_DESCRIPTIONS moved with the re-block (DEV-09, DEV-10, typed in RV-100); the AIRBORNE_PICKUP break's search text moved with the support words; the shape test's hand-support assertion turned (the hand is no support, F-206) and its bounds tightened (70 degrees from 80; the knees and ankles added); one new test |
| Examples | PASS | the fight's S04, S11 and S13 plans, rebound; the prose on A's 7.0, 7.5 and 8.0 lines; checklist counts the same |
| Records | PASS | F-206, F-110, F-207 resolved; F-219 new (AS-02); F-205, F-053, F-127 noted; backlog 34 (RV-95 done, RV-100 next); PLAN-007; CHANGELOG; run report |
| Hygiene | see Verification | the scan's count copied below |

## Duration
from 09:26 (the plan) to 09:35 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- solver/reblock.py (`above` reads joints); tests/test_reblock.py (the commands, a re-derivation test, the shape
  test's bounds); tests/test_reference_fight_golden.py (the two pins); tests/test_dag_conformance.py (one break's text)
- examples/reference_fight/plans/temporal.json (A's anchors at b19 and b20 at 0.57; S-080's four hand contacts gone),
  kinematic.json (the feet only), motion.json (the two keys from the recorded commands, their words); every plan
  rebound; the fight regenerated
- F-206, F-110, F-207 resolved; F-219 (new); F-205, F-053, F-127; backlog; PLAN-007; CHANGELOG; run report

## Verification
- before: S-082's chained gate at a62e551: 714 passed
- Prediction 1 held. Prediction 2 held in part: no root met the ankle bound as stated; with it corrected (D1), 7.5
  holds every bound at 0.57 m, the top of the range. Prediction 3 failed: 8.0 holds every bound at 0.57 m, not at or
  below 0.50 (the spine's twist does the reaching). Prediction 4 held. Prediction 5 held in part: the prose changed on
  A's 7.0, 7.5 and 8.0 lines, not 8.5; 715 tests. Predictions 3 of 5.
- the gate on this record (09:35:38): `scripts/verify.sh` exit 0, 715 passed in 96.13 s, docs plane: PASS, check:
  PASS
- the hygiene scan over the staged diff: 0 hits
