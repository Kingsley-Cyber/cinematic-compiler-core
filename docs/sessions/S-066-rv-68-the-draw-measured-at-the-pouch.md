# S-066 — RV-68: the holstered volley rests at the thigh pouch, and the draw is measured against it

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-68 (PLAN-007); findings F-182, F-163, F-105; rulings O8, O72, O83, R-33, O102

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-066]

## Plan
RV-62 (S-061) placed the volley's 5.1 sample on B's hand, so CONTACT_WORLD read the draw at 0.004 m by construction,
and B's hand overlapped the thigh by 0.012 m (F-182, review 4).
1. The volley's 5.1 sample moves to the pouch: on the outer side of B's right thigh, a quarter of the way from the hip
   (the source holsters it "in B right thigh pouch"), where the hand can reach while B recovers in the air.
2. B's repo-authored 5.1 right arm is re-posed so the hand touches the pouch from outside the thigh.
3. The golden's draw test pins the sample on the thigh's surface and the hand against it, measured by the FK.

Predictions, made before the change (05:37 by the clock):
1. The gate passes before the change: 686 tests (bada528).
2. RA [30, -15, 0] and RFA [-45, 0, 0] put B's hand about 0.04 m from the pouch and just outside the thigh (a
   surface gap of about 0.042 m, at least the hand's 0.04 m radius).
3. CONTACT_WORLD measures the draw (b13_c1) at about 0.04 to 0.05 m; b14's two contacts stay at 0.004 m.
4. Only the reference fight changes: B's 5.10 line (its right-arm words and the two points), the volley's 5.10 sample
   in its state machine, the motion plan and the plans re-bound after it; every checklist verdict count stays.
5. The gate stays at 686 tests.

## Decisions
- D1 — The pouch sits on the outer side of B's right thigh a quarter of the way from the hip: at mid-thigh no arm pose
  reaches it without entering the thigh while B, airborne, leans back with the thigh swung forward. Level:
  interpretation (F-053; the source says only "B right thigh pouch").
- D2 — B's repo-authored 5.1 right arm: RA [30, -15, 0], RFA [-45, 0, 0], the hand 0.042 m outside the thigh's
  surface (at least its own 0.04 m radius) and 0.045 m from the pouch. Level: covered (O83: the repo side is
  re-blocked; DEV-31 already records the re-posed arm).
- D3 — The golden's draw test pins the sample on the thigh's surface (within 0.02 m) and the hand outside the thigh and
  within 0.15 m of the pouch, by the FK; its two records (the sample, the angles) move with the data. Level: covered
  (ADR-O102: the pinned data changed with the fix).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | PASS | `scripts/verify.sh > gate.log && git commit`, after a first gate run read the count |
| One gap, right layer | PASS | the reference fight's S04 sample and one S13 pose; no code changed |
| Predictions written first | PASS | the session file was written at 05:37, before the data edits in the same command |
| New checks fire and stay silent | PASS | `contact_world.measure`: b13_c1 0.045 m, b14_c1 and b14_c4 0.004 m |
| Tests changed with their data | PASS | `git diff -- tests`: the draw test's two records moved with the data; three FK assertions added |
| Examples | PASS | the reference fight alone: B's 5.10 line (arm words, the two points), the volley's 5.10 sample; checklist counts 31/0/36/17 as before |
| Records | PASS | F-182 resolved; F-163 and F-053 noted; backlog (RV-68 done, RV-69 next); PLAN-007; CHANGELOG; run report |
| Hygiene | PASS | the scan over the staged diff before the commit |

## Duration
about 3 minutes by the clock (05:34 to 05:37)

## Changes
- examples/reference_fight/plans/temporal.json (the volley's 5.1 sample at the pouch), motion.json (B@b13's right arm
  and description); the reference fight re-bound (motion, effort, camera) and regenerated
- tests/test_reference_fight_golden.py (the draw's records and three FK assertions)
- F-182 resolved; F-163, F-053 noted; backlog; PLAN-007; CHANGELOG; run report

## Verification
- before: S-065's gate at bada528: 686 passed
- after: `scripts/verify.sh` exit 0, 686 passed, check: PASS
- Prediction 1 held. Prediction 2 held (0.042 m outside the thigh, 0.045 m from the pouch). Prediction 3 held (0.045
  m; 0.004 m for b14's two). Prediction 4 held (the reference fight alone; counts unchanged). Prediction 5 held (686).
