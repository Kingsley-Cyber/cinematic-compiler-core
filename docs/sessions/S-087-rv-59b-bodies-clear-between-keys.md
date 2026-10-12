# S-087 — RV-59b: the re-block solver clears paths between keys; two of B's spans re-blocked, the rest filed

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-59b (PLAN-007); finding F-159 (F-220 filed); rulings R-18 (no body through another), O72, O18; the source's
rule "Use slerp on all joint rotations. Root positions are exact."

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-087]

## Plan
BODY_OVERLAP judges the keys only; along the declared interpolation (S-086, RV-59a) the fight's bodies overlap in 38
frames over eight spans, each with B's repo keys at one end, and the wizard example's in 5 frames over two spans, both
sides repo keys (docs/reports/2026-10-12-between-keys.md). The class: a key-only check of a motion drawn between keys.
1. solver/reblock.py gets a clearance goal (`--clear <entity>`): the key's two spans, posed along the declared
   interpolation (solver/interpolation.py), keep every capsule of the moving body clear of the other body's at every
   frame, by a margin stated before any solve: 0.01 m, room for the angles' rounding to three places (the check itself
   allows no depth). The CLI reads the scene's other keys, beats, fps and vanish windows from the example.
2. B's paths, and the wizard example's, re-blocked from recorded commands run from the keys at 76da0e5: at each span,
   one key on the repo side, the overlapping limb's joints freed, the key's own contact points kept as goals from the
   contact's target; a test re-derives them. A's source rows do not change.
3. BODY_OVERLAP at every frame between keys at S13 (p13_motion: the packet carries the fps and the vanish windows),
   the step's instructions teaching it, and a planted overlap between keys refused.
4. The contact with no key at its instant (CONTACT_WORLD on the interpolated pose; the wizard's landing at 6.4) is a
   separate gap: RV-59d.

Predictions, made before the change (10:13 by the clock):
1. The gate passes before the change: 724 tests (76da0e5, S-086's chained gate).
2. Every one of the ten spans clears with one key re-posed per span on the repo side, at most ten keys in all, no
   component moved more than 45 degrees, and no A source row changed.
3. No re-posed key breaks another check at its key (contacts, supports, floor, shapes), and no camera shot is
   re-authored.
4. After the re-blocks the new check refuses nothing in the four examples, and it refuses a planted overlap between
   keys.
5. About 730 tests.

## Decisions
- D1 — The clearance goal reads the key's instant and every frame of its two spans, the moving body and the others
  posed along the declared interpolation, a vanished body left out but a body at its own key always in (as S13 judges
  it, a substitution's start included); its cost is each overlapping pair's squared depth plus CLEARANCE_M (0.01 m,
  stated before any solve), weighed like a goal. The margin is a goal, not a bound: B at 4.4 clears by 0.3 mm, where
  holding its feet outweighed the rest. Level: covered (R-18; F-159's proposed fix).
- D2 — A root component (`pos.x`, `pos.z`) counts a centimetre as a degree and is bound in metres; a re-blocked root
  moves its S04 anchor with it (temporal.json), as MOTION_POS requires. The speed-ups change no number a check reads:
  a rotation matrix and a slerp are kept once computed, and the clearance composes each chain once (held to forward
  kinematics within 2 micrometres by a test) and passes over a frame the body cannot reach. Level: covered.
- D3 — A re-block holds at its start point every part the key's contacts and S11 supports name, and keeps each freed
  angle within 45 degrees of its start and a root component within 0.15 m (set in the probes, before the recorded
  solves). Probed that way, eight of the ten spans lie by a contact whose hold leaves no clearing re-pose (the knee at
  4.7, the elbow and the catch at 6.3-6.6, the throw and the landing to 7.5, the pull, the drive and the crash 8.0-9.0,
  the wizard example's kick at 3.6; bigger moves broke a key, an overlap at the 8.5 key). So only 3.4-3.7 and 4.4-4.7
  are re-blocked; how the rest clear is the owner's question (F-220: in-between keys recommended), and BODY_OVERLAP
  between keys waits for it (RV-59e). RV-59's contact with no key is RV-59d. Level: question (F-220).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the chained gate commits |
| One gap, right layer | PASS | the re-block solver and B's repo keys (L4c); the check waits for F-220 (RV-59e) |
| Predictions written first | PASS | the session file was written at 10:13, before any code |
| A re-block re-derives | PASS | a test runs both recorded commands from the keys at 76da0e5 (PATH_START) and gets the committed keys; the goals are the start's held points, not the outcome |
| The re-blocked paths clear | PASS | a test measures both keys' spans with no margin: overlapping before, clear after |
| A refusal the solve missed | PASS | the first 3.7 solve left A out at its own key (the substitution's start) and S13 refused it (B's upper arm 0.013 m in A's head); the clearance now counts a key at its instant and the command was run again |
| Neighbours | PASS | body_overlap.py's and between_keys_report.py's docstrings; knowledge map 21; REBLOCKED_ROOTS's 4.4 entry moves with B_PATHS (DEV-18 re-blocked again, DEV-34) |
| The step's instructions teach it | n/a | no check lands; euler_solving.txt's "the root stays the slot's pos" holds (the anchor moved with it) |
| Tests changed with their data | PASS | four new tests in tests/test_reblock.py; the report's pin from 38 to 29 frames (this slice's re-blocks); REBLOCKED_ROOTS's 4.4 entry (DEV-34); nothing loosened |
| Examples | PASS | the fight's 3.7 and 4.4 keys and B's 4.4 anchor; outputs regenerated; the camera plan only re-bound; deviations.yaml 3 (DEV-34, B_PATHS) |
| Records | PASS | F-220 filed; F-159 noted; backlog 36 (RV-59b done, RV-59d next, RV-59e blocked); map 21 (kernel log); PLAN-007; CHANGELOG; run report |
| Hygiene | see Verification | the scan's count copied below |

## Duration
from 10:13 (the plan) to 10:40 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- solver/reblock.py (the clearance goal, root components, solve_key, the composed capsules); solver/interpolation.py
  (a slerp kept); solver/quaternion.py (a rotation matrix kept)
- examples/reference_fight: B's left arm at 3.7, B's root and legs at 4.4 (motion.json) and B's 4.4 anchor
  (temporal.json); outputs regenerated; deviations.yaml 3 (DEV-34)
- tests/test_reblock.py (four tests); tests/test_reference_fight_golden.py (B_PATHS; REBLOCKED_ROOTS at 4.4);
  tests/test_interpolation.py (29 frames)
- docs/reports/2026-10-12-between-keys.md regenerated; F-220 new; F-159 noted; backlog 36; kernel/knowledge_map.yaml
  21; PLAN-007; CHANGELOG; run report

## Verification
- before: S-086's chained gate at 76da0e5: 724 passed
- Prediction 1 held. Prediction 2 failed (two of the ten spans clear with one key re-posed; eight lie by a contact,
  F-220). Prediction 3 held for the two re-blocked keys (no other check broke at them once the 3.7 solve counted A's
  key; the camera plan only re-bound). Prediction 4 failed (no check lands; RV-59e waits for F-220). Prediction 5
  held in part (728: two under). Predictions 2.5 of 5.
- the gate on this record (10:42:47): `scripts/verify.sh` exit 0, 728 passed in 72.73 s (99 s on S-086: forward
  kinematics now keeps its rotation matrices), docs plane: PASS, check: PASS
- the hygiene scan over the staged diff: 0 hits (the first scan's 2 were `+@functools.lru_cache` lines read as an
  address; the decorator is now `@lru_cache`)
