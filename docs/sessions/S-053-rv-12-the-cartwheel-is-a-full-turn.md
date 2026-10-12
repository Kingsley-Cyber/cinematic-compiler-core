# S-053 — RV-12: the 6.3 cartwheel is a full turn in the words too (O96)

<!-- docs-version: 2.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-12 (PLAN-007); finding F-087; rulings O96, O18, R-17, O102

## Layer
L6

## Status
applied

## Commit
the commit whose message names [S-053]

## Plan
O96 (owner): "Cartwheel is a full turn. Update render.txt." A's 6.3 row carries the source's words "A body rotates
sideways in screen plane one quarter turn" while its keys roll A through 360 degrees (O18), so render.txt and the
prose print both (F-087). The 6.3 key's description says "one full turn", recorded as a rewording in the golden test.

Predictions, made before the change:
1. The gate passes before the change: 662 tests (28284e5).
2. After it render.txt and the four reference prose prompts print "rotates sideways in screen plane one full turn" on
   A's 6.3 row, and no output says "one quarter turn".
3. The golden's rewording table gains the 6.3 entry (ADR-O102 with O96); the plans after S13 re-bind (S16's packet
   carries the keys' descriptions); no check refuses.
4. 662 tests.

## Decisions
- D1 — The words change, not the keys: the 6.3 key's description says "one full turn" (the keys already roll 360, O18).
  Level: covered (O96).
- D2 — The golden's rewording table (WORDS) takes the 6.3 entry beside the rope dart's (ADR-O102 with O96). Level:
  covered.

## Duration
about 3 minutes by the commit times (02:36 to 02:39); it read "about 15 minutes" until RV-46
(S-056) corrected it (F-166)

## Changes
- examples/reference_fight/plans/motion.json (A@b16's description); the plans after S13 re-bound; render.txt and the
  checklist regenerated
- tests/test_reference_fight_golden.py (CARTWHEEL_WORDS)
- F-087 resolved; backlog (RV-12 done, RV-13 next); PLAN-007; CHANGELOG; run report

## Verification
- before: S-052's gate at 28284e5: `scripts/verify.sh` exit 0, 662 passed
- after: `scripts/verify.sh` exit 0, 662 passed, check: PASS; `make golden` passed
- Prediction 1 held. Prediction 2 held in part: render.txt prints "one full turn" and nothing says "one quarter turn",
  but the prose prompts never printed the clause. Prediction 3 held (the effort and camera plans re-bound). Prediction
  4 held (662).

## Next
Principal review 3 (eight slices since review 2), then RV-13.
