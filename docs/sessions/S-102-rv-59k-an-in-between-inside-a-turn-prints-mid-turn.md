# S-102 — RV-59k: an in-between inside a declared turn prints its root as mid-turn

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-59k (PLAN-007); finding F-232; rulings W3 (owner O47), ADR-O109; ADR-O110

## Layer
L6

## Status
applied

## Commit
the commit whose message names [S-102]

## Plan
The staff rows print a root inside a declared turn as "EulerXYZ mid-turn" (W3: probe R13 flipped twice on printed
angles), but the in-between lines in [MOTION CONTROL] print the raw angles, and ROTATION_ANGLES_PRINTED reads only the
staff rows (F-232). The class: every in-between line whose key before declares a turn.
1. An in-between whose key before declares a turn (the turn it carries, solver/interpolation.py) prints its root as
   "EulerXYZ mid-turn" in every mode that prints a root.
2. ROTATION_ANGLES_PRINTED reads the in-between lines too.

Predictions, made before the change (14:21 by the clock):
1. The gate passes before the change: 751 tests (7e99987, S-101's chained gate).
2. Two in-between lines change, in the three modes that print a root: B@8.75 in the fight (inside the 8.5 flip) and
   the acrobat@3.55 in the wizard example (inside the 2.6 spin); the pure staff does not change.
3. Before the change the widened check refuses those two lines in each such mode; after it, nothing.
4. 752 tests.

## Decisions
- D1 — An in-between is inside a declared turn when its entity's key before declares one: the turn it carries, which
  the declared interpolation runs (solver/interpolation.py); one shared reading (`inbetweens_turning`) for the
  renderer and the check. Level: covered (W3, ADR-O109).
- D2 — The line keeps its root position and joints; only the angles become "mid-turn", as on a staff row inside a
  turn (W3). Level: covered (W3).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the chained gate commits |
| Predictions written first | PASS | at 14:21, before the edit |
| The class, not the probe | PASS | every in-between of every example; the check run on the committed prompts refused exactly the two lines in three modes |
| Tests | PASS | one added (the two lines in every mode; their angles planted back are refused) |
| Examples | PASS | six lines: B@8.75 and the acrobat@3.55 in mixed, upgraded mixed and euler heavy |
| Records | PASS | F-232 in progress; backlog 45; CHANGELOG; PLAN-007; run report |
| Hygiene | see Verification | the staged scan runs first in the chained commit |

## Duration
from 14:21 (the plan's predictions) to 14:22 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- renderers/anime_renderer.py: `inbetweens_turning`; renderers/prose_renderer.py: the in-between line's root
- validators/prompt_validator.py: ROTATION_ANGLES_PRINTED reads the in-between lines
- examples: six prompt lines and the two envelopes; tests/test_inbetweens.py (one test)
- docs: F-232; backlog 45; CHANGELOG; PLAN-007; run report

## Verification
- before: S-101's chained gate at 7e99987: 751 passed
- Prediction 1 held. Prediction 2 held (six lines; the pure staff unchanged). Prediction 3 held (refused before in the
  three modes for each line, nothing after). Prediction 4 held (752). Predictions 4 of 4.
- the gate on this record (14:25:29): `scripts/verify.sh` exit 0, 752 passed in 159.73 s, docs plane: PASS, check:
  PASS
- the hygiene scan over the staged diff: 0 hits (run first, and again in the chained commit)
