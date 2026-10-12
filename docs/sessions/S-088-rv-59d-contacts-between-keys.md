# S-088 — RV-59d: a contact with no key at its instant measured on the interpolated pose

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-59d (PLAN-007); finding F-089; rulings O72 (0.15 m), O89 and ADR-O104 (an interpolated point's miss is an
artefact only while the actor is airborne or the prop moves); the source's rule "Use slerp on all joint rotations.
Root positions are exact."

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-088]

## Plan
CONTACT_WORLD reads a contact on the actor's key at the contact's instant; a contact with no key there is "not
measurable" (the wizard example's landing at 6.4 between the acrobat's keys at 5.2 and 6.6), so ADR-O104's
interpolated artefact has never been exercised. The class: a contact at an instant the keys do not sample.
1. solver/contact_world.py: an actor or a body target with no key at the contact's instant, but keys on both sides,
   is posed along the declared interpolation (solver/interpolation.py) and measured there, the row marked
   interpolated. Airborne there (ADR-O104) when the key before claims no support (S11): the span starts in the air;
   rotating when the key before declares a turn. Interpretation (Claude's): the key before decides, since nothing
   else states the support between keys.
2. The neighbours: a prop contact between two samples of its prop, and the instructions (euler_solving.txt) on what a
   contact between keys meets.
3. Whatever the new rows refuse in the examples is fixed on the repo side or filed.

Predictions, made before the change (10:49 by the clock):
1. The gate passes before the change: 728 tests (d2c650c, S-087's chained gate).
2. In the four examples exactly two contacts have no key at their instant and keys on both sides: the wizard
   example's landing feet at 6.4 (b08_c2, b08_c3); both become measurable, marked interpolated.
3. Both feet miss the ground by more than 0.15 m at 6.4, the pose being six sevenths of the way from the pillar brace
   (feet 1.24 m up) to the lunge; the key before claims the torso on the pillar, so they are not airborne and
   CONTACT_WORLD refuses them; the fix is to the wizard example's data (the landing at a key), not to the check.
4. No row of the reference fight, the live standoff or the UGC demo changes; no prop contact falls between two
   samples of its prop.
5. About 731 tests.

## Decisions
- D1 — A contact between two of its actor's keys (or of a body target's) is measured on the pose the declared
  interpolation gives at its instant, and a prop between two samples is read straight between them; the row is then
  interpolated, so ADR-O104's artefact applies to it. Between keys the actor is airborne when the key before claims no
  support (S11) and turning when that key declares a turn: nothing else states the support between keys (the S06
  state at 6.4 also reads "braced"). A contact outside the keys or the samples stays unmeasured. Level:
  interpretation (F-053) for the airborne rule; covered (ADR-O104) for the rest.
- D2 — The wizard example's landing (b08, "pushes off the cracked pillar and drops to both feet") lasts 1.4 s, not
  1.2, so its contacts land at 6.6, where the acrobat's lunge key stands on both feet (0.116 and 0.004 m); the beat's
  other numbers and its wording are unchanged. The example is the repo's (no source rows), so no deviation registry
  covers it; the change is recorded here and in the CHANGELOG. Level: covered (O72; the data, not the check).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the chained gate commits |
| One gap, right layer | PASS | CONTACT_WORLD in S13's measure (L4c) and one repo example's beat length |
| Predictions written first | PASS | the session file was written at 10:49, before any code |
| New check fires and stays silent | PASS | measured: the landing back at 6.4 is refused at S13 (0.275 and 0.181 m) and excused once the span starts in the air (a test); the fight, live and UGC rows keep their measures |
| Neighbours | PASS | a prop between its samples (ADR-O104 names both; none in the examples, a unit test); a body target between its keys; the knowledge map 22 (CONTACT_WORLD's note); contact_world.py's docstring no longer says every contact sits at an exact instant |
| The step's instructions teach it | PASS | euler_solving.txt: a contact between keys is measured on the interpolated pose, excused only while the span starts in the air or its prop moves |
| Tests changed with their data | PASS | two new tests in tests/test_motion_solver.py; nothing removed or loosened |
| Examples | PASS | the wizard example's b08 at 1.4 s (its outputs regenerated); every example's motion plan re-bound to the new instructions |
| Records | PASS | F-089 and F-053 noted; map 22 (kernel log); backlog (RV-59d done, RV-59c next); PLAN-007; CHANGELOG; run report |
| Hygiene | see Verification | the scan's count copied below |

## Duration
from 10:49 (the plan) to 10:54 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- solver/contact_world.py (`_between`, `_prop_at`; `plan_bodies` carries the pose; the rows' interpolated, airborne
  and turning flags); planner/prompts/euler_solving.txt
- examples/wizard_vs_acrobat/plans/temporal.json (b08 lasts 1.4 s) and its outputs; every example's motion plan
  re-bound
- tests/test_motion_solver.py (two tests); kernel/knowledge_map.yaml 22
- F-089 and F-053 noted; backlog; PLAN-007; CHANGELOG; run report

## Verification
- before: S-087's chained gate at d2c650c: 728 passed
- Prediction 1 held. Prediction 2 held (b08_c2 and b08_c3 only, interpolated). Prediction 3 held (0.275 and 0.181 m,
  not airborne, refused at S13; the beat moved, not the check). Prediction 4 held (no other row's measure changed; the
  unmeasured rows now say "at or around"; no prop contact lies between two samples). Prediction 5 held in part (730:
  one under). Predictions 4.5 of 5.
- the gate on this record (10:54:33): `scripts/verify.sh` exit 0, 730 passed in 71.91 s, docs plane: PASS, check:
  PASS
- the hygiene scan over the staged diff: 0 hits (the chained commit now runs the scan first and stops on a hit)
