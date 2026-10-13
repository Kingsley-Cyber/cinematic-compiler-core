# S-126 — S14's first check: the line of action, computed for every key and printed on its line

<!-- docs-version: 3.0 -->

## Date
2026-10-13

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
PLAN-009 PM-3, check 1 of 4 (owner: "build S14's four checks one at a time: line of action, counterbalance, weight
distribution, silhouette")

## Layer
L4e

## Status
applied

## Commit
the commit whose message names [S-126]

## Plan
1. solver/pose_mechanics.py `line_of_action(points)`: the curve from the head through the chest and the hips to the
   base foot; straight, C or S from the inner points' offsets off the head-to-foot chord; tension, apex, bulge,
   chord, base, inverted.
2. S14 writes one node per S13 key; the prose staff line and the LBN row print it.
3. LINE_OF_ACTION (validators/pose_checks.py): a strike along a straight line is named; measured and printed, not
   refusing (owner: measure first).
4. The owner's four reference frames as number fixtures (tests/pose_references.py, Claude's interpretation; the images
   stay out of the repository), read back by the mechanics.

Predictions, made before the change (15:10 by the clock):
1. The reference frames read back as the owner's stills show them.
2. A standing body reads close to straight.

## Decisions
- D1 — STRAIGHT is 8 % of the chord, not 5 %: a standing body bends about 5 % and every example key read as a C;
  the flying kick's long diagonal reads straight at 7.6 %. Level: covered (an interpretation, PLAN-009 section 8).
- D2 — Inverted means the head 0.15 m or more below the hips: the multiplier's flying kick, laid flat, is not upside
  down. Level: covered.
- D3 — LINE_OF_ACTION is a report (`python -m validators.pose_checks`), the line itself is printed: the examples have
  two strikes along a straight line (reference fight 4.7, wizard 3.6), named, not refused. Level: the owner's ruling.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the chained gate commits |
| graft used | PASS | the S13 key's points read from the graft-built forward kinematics map (S-125) |
| Tests | PASS | tests/test_pose_mechanics.py new (13), the reference frames among them |

## Duration
from 15:10 to 16:00

## Changes
- solver/pose_mechanics.py, validators/pose_checks.py (new); compiler/passes/derived/p14_pose_mechanics.py;
  renderers/prose_renderer.py, renderers/anime_renderer.py; schemas/graphs/pose_mechanics_graph.schema.json 1.1
  (logged); kernel/data_flow.yaml (logged); examples, checklists, docs/graph_map.md; tests/pose_references.py,
  tests/test_pose_mechanics.py

## Verification
- Prediction 1 held: clash (Naruto C 0.126 to the rear foot, Sasuke C 0.386), flying kick (Sasuke straight 0.076,
  upside down, to the kicking foot; Naruto C 0.094), takedown (C, upside down), multiplier (straight, level).
- Prediction 2 held: a standing body is straight; the examples: reference fight 41 C and 1 straight of 42, wizard 17
  and 2, live action 8 C, UGC 4 C.
