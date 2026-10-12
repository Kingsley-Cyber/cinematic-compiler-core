# S-089 — RV-59c: the floor between keys measured; B's crash needs a key mid-fall (F-220)

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-59c (PLAN-007); finding F-089; rulings O72 (0.15 m), O18, R-18; the source's rule "Use slerp on all joint
rotations. Root positions are exact."

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-089]

## Plan
FLOOR_PENETRATION judges the keys only; between keys (S-086's report) B's crash from 8.5 to 9.0 sinks the left sole
0.385 m under the floor at 8.75 over nine frames, and nothing else in the four examples sinks over 0.15 m. The class:
a key-only check of a motion drawn between keys (BODY_OVERLAP's twin, RV-59e).
1. solver/reblock.py: a floor term (`--floor`): every contact point of the moving body over the floor less 0.15 m
   (FLOOR_PENETRATION's tolerance), by the same margin, at the key's instant and every frame of its two spans.
2. B's crash re-blocked from a recorded command: B's legs at 9.0 (lying, the torso held on the ground, A kept clear),
   each angle within 45 degrees of its start; a test re-derives it.
3. FLOOR_PENETRATION at every frame between keys at S13 (the packet carries the fps and the vanish windows), the
   instructions teaching it, a planted sink refused.

Predictions, made before the change (10:58 by the clock):
1. The gate passes before the change: 730 tests (b6c6778, S-088's chained gate).
2. B's crash clears with B's hips and knees at 9.0 drawn up (the legs bent while B lies), every angle within 45
   degrees of its start, the torso still on the ground and A no nearer B than before.
3. FLOOR_PENETRATION between keys lands at S13 and refuses nothing in the four examples after the re-block; a planted
   sink between keys is refused.
4. No camera shot is re-authored, and B's 9.5 key needs no change.
5. About 734 tests.

## Decisions
- D1 — The re-block solver's floor term: each contact point FLOOR_PENETRATION reads, at the key's instant and every
  frame of its two spans, counted when deeper than the floor less 0.15 m plus the margin (CLEARANCE_M); `--floor`
  takes the scene's floor level. Level: covered (O72, R-18).
- D2 — No re-pose keeps B's crash over the floor (measured, the probes in the scratchpad, not recorded commands): the
  declared flip at 8.5 runs B's root angles straight while the root drops straight from 1.08 to 0.1 m, sinking the
  left sole 0.385 m at 8.75; a slerp would still sink 0.209 m (and a 90-degree change must be declared); B's legs at
  9.0 within 45 degrees leave 0.218 m and within 120 degrees 0.217 m; B's legs at 8.5, the feet and the torso held,
  0.27 m. So nothing is re-blocked, the fall joins F-220 (a key mid-fall or a declared fall path), RV-59c waits for it
  beside RV-59e, and the queue moves on to principal review 7 (eight slices since S-081), then RV-97. Level: question
  (F-220).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the chained gate commits |
| One gap, right layer | PASS | the re-block solver's floor term (L4c); no check lands (F-220) |
| Predictions written first | PASS | the session file was written at 10:58, before any code |
| A term that measures | PASS | a test: the acrobat standing at 7.6 is clear, dropped 0.3 m it is counted; B's crash key is counted |
| Probes before records | PASS | the crash probes ran in the scratchpad; their numbers are in D2 as measured, and none became a recorded re-block |
| Neighbours | PASS | floor_penetration.py's and between_keys_report.py's docstrings; knowledge map 23; F-220's evidence and impact |
| The step's instructions teach it | n/a | no check lands |
| Tests changed with their data | PASS | one new test in tests/test_reblock.py; nothing removed or loosened |
| Examples | PASS | none changed |
| Records | PASS | F-220 widened; F-089 noted; backlog 37 (RV-59c blocked, RV-97 next); map 23 (kernel log); PLAN-007; CHANGELOG; run report |
| Hygiene | see Verification | the scan's count copied below |

## Duration
from 10:58 (the plan) to 11:01 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- solver/reblock.py (`_joints`, POINTS, the floor term, `--floor`); solver/floor_penetration.py and
  validators/between_keys_report.py (docstrings)
- tests/test_reblock.py (one test); kernel/knowledge_map.yaml 23
- F-220 widened (B's crash); F-089 noted; backlog 37; PLAN-007; CHANGELOG; run report

## Verification
- before: S-088's chained gate at b6c6778: 730 passed
- Prediction 1 held. Prediction 2 failed (no re-pose of B's legs at 9.0 clears the crash: 0.218 m left within 45
  degrees). Prediction 3 failed (no check lands; RV-59c waits for F-220). Prediction 4 not judged (nothing re-blocked).
  Prediction 5 failed (731, three under). Predictions 1 of 5.
- the gate on this record (11:01:35): `scripts/verify.sh` exit 0, 731 passed in 72.17 s, docs plane: PASS, check:
  PASS
- the hygiene scan over the staged diff: 0 hits (run first in the chained commit)

## Correction (S-090)
Corrected in S-090 (principal review 7): D2's "within 120 degrees 0.217 m" held the hips' twist frozen; freed, the
committed solver clears the crash (deepest 0.141 m) with B's left foot 1.0 m up at 9.0, so RV-59c was not blocked by
the evidence; D1's "covered (O72, R-18)" for the floor allowance is F-215's question. ADR-O109 answers F-220's option
(a) and RV-59c is ready again.
