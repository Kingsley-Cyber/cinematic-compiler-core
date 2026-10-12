# S-086 — RV-59a: bodies measured between keys, along the declared interpolation

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-59 (PLAN-007); findings F-159, F-089; rulings R-18, O72, the source's rule "Use slerp on all joint
rotations. Root positions are exact."

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-086]

## Plan
BODY_OVERLAP, FLOOR_PENETRATION and the claimed supports are judged at the keys only, 42 instants of the fight's 240
frames; between them A and B overlap in about 33 frames, A falls through B's head at 7.21 and B's sole goes 0.385 m
under the floor at 8.75 (F-159, F-089; review 6). The class: a check that reads the keys of a motion the prompt tells the
model to interpolate.
1. solver/interpolation.py: an entity's pose at any instant between two of its keys, as the source declares it: every
   joint slerped; the root's position linear (its positions are exact only at keys); the root's rotation slerped, or,
   across a declared turn, its Euler angles carried linearly along the turn (the S13 edge's euler_axis).
2. A measure first, at every frame of the scene's fps: the deepest overlap of each pair of bodies, and each body's
   lowest point against the floor, between keys.
3. From the measure, the checks at frames where they hold on the examples' repo-authored paths, and the paths
   re-blocked; whatever only an owner can move (A's source rows), or only a new key can fix, is filed.

Predictions, made before the change (09:54 by the clock):
1. The gate passes before the change: 718 tests (cf74e03, S-085's chained gate).
2. Between keys in the reference fight, A and B overlap in 20 to 45 frames (review 6 counted 33 with its own model),
   each span with B's repo-authored keys or carried poses at one end.
3. Between keys a body sinks more than 0.15 m under the floor in at most three spans in the four examples, B's crash
   (8.5 to 9.0) among them, and in none of A's source spans.
4. A straight root between a standing key and a lying one sweeps the feet under the floor whatever the keys, so B's
   crash needs a key between them (a new beat) or a declared fall path: filed, not re-blocked here.
5. About 722 tests.

## Decisions
- D1 — The declared interpolation between two keys: every joint slerped (the source's words); the root's position
  straight from key to key (exact only at the keys); its rotation slerped, or across a declared turn (flip, spin,
  cartwheel) its Euler angles straight (the S13 edge's euler_axis). A slerped rotation is read back as Euler angles
  that keep it; at Y = +-90 degrees, where X and Z share one axis, the whole turn is read as X. The lock's tolerance
  (|sin Y| within 1e-10 of 1) lets pass a rotation 0.0008 degrees off the lock read with Z = 0: under 0.015 mm per
  metre of limb. Level: interpretation (F-053) for the straight root.
- D2 — The frames are the scene's, at its fps, strictly between an entity's consecutive keys, a vanished body's window
  left out (O18); a body at a key is its key, and two bodies both at their keys are S13's to judge, not counted again.
  A span is "source rows" when both its keys are the owner's rows. Level: covered (O18, R-18).
- D3 — Measure before refusing: refusing now would refuse the golden (38 overlap frames, B's crash), and each needs B's
  keys re-blocked or a key between, so RV-59 splits: RV-59a (this), RV-59b (the overlaps refused and B's paths
  re-blocked; a contact with no key measured on the interpolated pose) and RV-59c (the floor between keys, B's crash).
  No example changes here. Level: covered (finish.md; the golden stays green).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the chained gate commits |
| One gap, right layer | PASS | the motion layer's measure between keys (L4c); no step's data changed |
| Predictions written first | PASS | the session file was written at 09:54, before any code |
| A pose lands on its keys | PASS | a test checks every span of the four examples at both its keys to a micrometre (float noise only); it found the first read-back losing the X angle at Y = +-90 degrees (A's root, 20 spans), fixed (an unrounded quaternion, the lock read as X) before the measure was recorded |
| The measure fires and stays silent | PASS | measured: the fight's eight overlapping spans and B's crash, the wizard's two spans; the live and UGC examples clean |
| Neighbours | PASS | BODY_OVERLAP's and FLOOR_PENETRATION's docstrings point to the report; knowledge map 20 (Conservation laws said "points between keys (RV-59) have no check"); solver/quaternion.py gives the unrounded quaternion |
| The step's instructions teach it | n/a | nothing is refused yet; RV-59b and RV-59c teach their checks |
| Tests changed with their data | PASS | tests/test_interpolation.py new (six tests); nothing removed or loosened |
| Examples | PASS | none changed |
| Records | PASS | F-159, F-089 noted; F-053; map 20 (kernel log); backlog 35 (RV-59a done, RV-59b next, RV-59c ready); PLAN-007; CHANGELOG; run report |
| Hygiene | see Verification | the scan's count copied below |

## Duration
from 09:54 (the plan) to 10:05 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- solver/interpolation.py (new: pose, frames, the slerp and its Euler read-back); solver/quaternion.py (unit_quaternion)
- validators/between_keys_report.py (new) and docs/reports/2026-10-12-between-keys.md (generated)
- solver/body_overlap.py and solver/floor_penetration.py (docstrings point to the report)
- tests/test_interpolation.py (six tests); kernel/knowledge_map.yaml 20
- F-159, F-089 noted; F-053; backlog 35; PLAN-007; CHANGELOG; run report

## Verification
- before: S-085's chained gate at cf74e03: 718 passed
- Prediction 1 held. Prediction 2 held (38 frames in eight spans, each with B's repo keys at one end). Prediction 3
  held (one span, B's crash; none of A's). Prediction 4 not judged (whether a re-pose alone keeps B's feet over the
  floor is RV-59c's first measure). Prediction 5 held in part (724: two over). Predictions 3.5 of 5.
- the gate on this record (10:05:25): `scripts/verify.sh` exit 0, 724 passed in 99.11 s, docs plane: PASS, check:
  PASS
- the hygiene scan over the staged diff: 0 hits
