# S-128 — S14's third check: weight distribution, refusing from the start (the pose follows S11)

<!-- docs-version: 3.0 -->

## Date
2026-10-13

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
PLAN-009 PM-1/PM-2, check 3 of 4 (WEIGHT_DISTRIBUTION; owner: refuses early, to S13; allowances anime 0.15 m,
live_action 0.05 m, ugc_ad 0.10 m)

## Layer
L4e

## Status
applied

## Commit
the commit whose message names [S-128]

## Plan
1. solver/pose_mechanics.py `weight_distribution`: the support base (the parts S11 names, a trunk along pelvis to
   chest, each spread a half foot), each support's share, the centre of mass's margin inside it.
2. S14 reads S11's supports and words (depends on kinematic); refuses a stable pose past the genre's allowance
   (genre profiles' com_allowance_m), routed to S13 (compiler/author.py ROUTES).
3. The examples it refuses, ruled by the owner one by one.

Predictions, made before the change (12:27 by the clock):
1. Some example poses stand past their feet.
2. Live action passes (the tightest allowance, the plainest poses).

## Decisions
- D1 — The owner's rulings on the eight refusals (2026-10-13):
  - wizard acrobat b02: one-hand support (S11 already names the right hand alone); re-posed at S13, the planting arm
    28.6 degrees back so the hand lands under the shoulders (the centre of mass 0.12 m past it);
  - UGC creator b01: leans less (the spine 30.1 to 26 degrees; 0.064 m past the feet, the hand 3 cm off);
  - reference b07, b08, b11, b23: the anime body is not the cause (only its legs put the soles on the ground; the
    spine leans forward as written; the source's legs set both feet beside the body), so they are recorded
    deviations, kernel/weight_exceptions.yaml (owner-only, refused if one names a pose that is no miss);
  - reference b15: "sliding, no support": the 5.9 landing (S04 b14's two foot supports, their release, the grounded
    effect) is gone, and with it the two CONTACT_WORLD exceptions for its floating soles;
  - reference b20: "right hand + left foot": at 8.0 the right foot lifts and the right hand takes the ground (S04
    b19, b20; S11). This overrides O18/R-34's "the hand is no support" for this pose.
  Level: the owner's rulings.
- D2 — A trunk support spans the pelvis to the chest: a body on its back lies along it (the broad ninja's b22, b23
  stood 0.24 m past one point before). Level: covered.
- D3 — The session records of S-126 and S-127 carried estimated clock times; their durations are corrected from the
  commit times. Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the chained gate commits |
| graft used | PASS | the motion and kinematic plans read through the S-125 map |
| Tests | PASS | five new; three pinned lines follow the owner's rulings (the 8.0 support, the 7.50 support words, the contact exceptions) |

## Duration
from 12:27 to 12:45 and from 16:08 to 16:35 (the owner's rulings between)

## Changes
- solver/pose_mechanics.py, compiler/passes/derived/p14_pose_mechanics.py, compiler/author.py ROUTES,
  planner/genre_profile.py; renderers (prose, anime); kernel/weight_exceptions.yaml (new), kernel/schema_log.py,
  kernel/contact_world_exceptions.yaml 4, kernel/layer_order.yaml 1.10, MGRAPH-1.4 (logged); schemas (pose mechanics
  1.3, genre profile 0.3, envelope; logged); three genre profiles (logged); example plans (reference temporal and
  kinematic, wizard motion, UGC motion) re-bound; examples, checklists, docs/graph_map.md; tests

## Verification
- Prediction 1 held: eight poses refused (reference six, wizard one, UGC one); all four examples pass after the
  rulings.
- Prediction 2 held.
