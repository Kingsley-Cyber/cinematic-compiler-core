# S-103 — RV-59l: between keys a body stands on what its last key claims, as S07 changes it

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-59l (PLAN-007); finding F-233; rulings ADR-O104, O89, O72; ADR-O110

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-103]

## Plan
RV-59h (S-091) read "airborne" between keys from S07's support contacts alone, so a body standing on the supports its
keys claim (S11) with no support contact of its own (B's feet, the wizard's, the live-action bodies, the UGC
creator) reads airborne, and any between-keys miss of its touch is excused; at an in-between's own instant the actor's
claim is looked up under an id S11 never wrote, so it reads airborne too (F-233). The class: every contact between
keys or at an in-between.
1. Between keys, and at an in-between's instant, the actor stands on what its last key claims (S11; an in-between
   takes its key's), with S07's onsets added and releases taken away from that key's instant to the contact; it is
   airborne only when nothing is left, and a landing (a support's onset) never is.

Predictions, made before the change (14:30 by the clock):
1. The gate passes before the change: 752 tests (d351176, S-102's chained gate).
2. A touch planted on the wizard example, the wizard's right hand on the acrobat's torso at 4.0 (0.97 m off), reads
   airborne False and is refused; one by the acrobat at its 3.7 in-between reads airborne False.
3. RV-59h's two tests pass unchanged: a landing is never airborne, and the touch after the pillar's release at 5.2
   is still excused.
4. No example's refusals, prompts or envelopes change.
5. 753 tests.

## Decisions
- D1 — "Airborne" between keys starts from the S11 claim of the actor's last key and applies S07's surface onsets and
  releases from that key's instant to the contact: the claim is what the layers say the body stands on at its key,
  and S07 says what changes after. S07 alone (RV-59h) missed every body whose supports only S11 claims; S11 alone
  (before RV-59h) missed the release from the pillar. Level: covered (ADR-O104: "genuine airborne").
- D2 — An in-between claims nothing of its own (S11 writes no node for it), so at its instant and after it the actor
  takes its last key's claim. Level: covered (ADR-O109: no beat, no contact of its own).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the chained gate commits |
| Predictions written first | PASS | at 14:30, before the edit |
| The class, not the probe | PASS | the rule reads every contact between keys or at an in-between; review 8's two plants (the fight's and the wizard's) refused again; RV-59h's two cases unchanged |
| Tests | PASS | one added; none changed |
| Examples | PASS | none changed |
| Records | PASS | F-233 in progress; backlog 46; CHANGELOG; PLAN-007; run report |
| Hygiene | see Verification | the staged scan runs first in the chained commit |

## Duration
from 14:30 (the plan's predictions) to 14:31 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- solver/contact_world.py: `_supported` (for `_open_supports`), the airborne reading in `_rows`, the docstring
- tests/test_motion_solver.py: one test
- docs: F-233; backlog 46; CHANGELOG; PLAN-007; run report

## Verification
- before: S-102's chained gate at d351176: 752 passed
- Prediction 1 held. Prediction 2 held (the wizard's touch refused at 0.966 m, airborne False; the acrobat at 3.7
  airborne False). Prediction 3 held. Prediction 4 held (no example file changed). Prediction 5 held (753). Predictions 5 of 5.
- the gate on this record (14:33:51): `scripts/verify.sh` exit 0, 753 passed in 161.20 s, docs plane: PASS, check:
  PASS
- the hygiene scan over the staged diff: 0 hits (run first, and again in the chained commit)
