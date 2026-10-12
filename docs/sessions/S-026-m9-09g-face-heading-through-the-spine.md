# S-026 — M9-09g: the face's heading reads the whole chain (O76, R-34)

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5)

## Gap
Backlog M9-09g (the S-020 single-joint audit); rulings O76, R-34

## Layer
L4d

## Status
applied

## Commit
the commit whose message names [S-026]

## Plan
The audit (S-020) found one whole-body reading built from part of the chain: `solver/quaternion.head_heading` summed
the root's, NK's and HD's yaw and skipped the spine, feeding S14's facial packet and S16's face checks. It now turns
the forward axis through root, Sp, NK and HD and reads its heading; a face within 0.2 of vertical (a body on its back)
has no horizontal heading and keeps the summed reading.

Predictions, made before the change: the live-action and UGC keys (the only ones with faces) have no spine twist, so
no packet and no output changes; a unit test shows a 30-degree spine twist turning the face.

## Decisions
- D1 — The fallback for a near-vertical face is the old summed reading. Why: such a face has no horizontal heading,
  and S16 needs a number; the root's own heading is what the old reading used. Alternatives: the head's up axis.
  Level: interpretation (FACE_LEVEL 0.2; F-053).

## Duration
about 15 minutes

## Changes
- `solver/quaternion.py` (`head_heading`, FACE_LEVEL); `tests/test_motion_solver.py` (one test); backlog (M9-09g done,
  M9-06 next); CHANGELOG; F-053

## Verification
- before: `scripts/verify.sh` exit 0, 622 passed (S-025, 5dc1f9e)
- after: `scripts/verify.sh` exit 0, 623 passed
- The predictions held: the live-action and UGC headings differ by 0.0 (no spine yaw there); no output moved.

## Next
M9-06 (forward kinematics, world contact points, roots at the pelvis: O72).
