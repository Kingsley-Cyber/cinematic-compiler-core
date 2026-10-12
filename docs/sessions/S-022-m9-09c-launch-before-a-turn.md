# S-022 — M9-09c: an airborne turn launches at its first key from grounded support (FR.4, O80)

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5)

## Gap
Backlog M9-09c (PLAN-003 FR.4); finding F-058; rulings O80, O75 (R-33)

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-022]

## Plan
O80: "The wizard must land before launching. Fix the beat. Add a check: a launch requires grounded support in the
prior beat." S13's turn runs (M9-05) gain AIRBORNE_WITHOUT_LAUNCH: a flip or cartwheel run that goes airborne starts
airborne at its first key, with grounded support at a key before it; a turn that stays on the ground (B's tip at
8.50) needs no launch. The wizard's vault (1.20) and dodge flip (8.60) started turning on the ground; their takeoff
moves to their first key.

Predictions, made before the change:
1. The check fires twice: the acrobat's vault at 1.20 and dodge flip at 8.60 (F-058); the reference fight passes (A's
   flips start in the air after a launch, B's tip stays on the ground).
2. After the fix the wizard compiles; its turn lines read "takeoff 1.20" and "takeoff 8.60".
3. No checklist row changes result; about 620 tests.

## Decisions
- D1 — The takeoff effect sits on the beat before each flip (the acrobat's run_in ends airborne at 1.20; the
  wizard's slicing bolt ends with the acrobat airborne at 8.60, its own cause "The acrobat flips away from the bolt"),
  the flips require the air, the dodge flip's foot releases happen at its start, and S11 has no support at 1.20 and
  8.60. Why: S06 commits effects at a beat's end and S11 allows only the state in force at a slot, so a takeoff at a
  beat's start is the end of the beat before it. Alternatives: start each flip's rotation one key later (re-authors
  the rotation and the inversion). Level: covered (O80, R-33); the beats chosen are Claude's (F-053).
- D2 — A turn run whose keys all have support (a tip, a roll) is not a launch. Why: O80 speaks of a launch; B's
  backward tip at 8.50 is a fall on the ground. Level: interpretation (F-053).
- D3 — The hang lines (S-021) start at the first airborne key, not at the last supported one, as the turn lines do.
  Why: a staff symbol lasts until the next line, so the body leaves the ground at the first NO SUPPORT line;
  S-021's "A hangs 1.10-3.00" included half a second on the pillar. Level: covered (the staff's own convention).
- D4 — AIRBORNE_WITHOUT_LAUNCH is a step code (S13) on map row BIO; no prompt code, since the turn and support lines
  already print the takeoff. Level: covered (FR.4 places it at S13).

## Duration
about 40 minutes

## Changes
- `solver/euler_solver.py` (`_launch_findings`); `renderers/prose_renderer.py` (hang lines from the first airborne key)
- `examples/wizard_vs_acrobat/plans/temporal.json` (b01 and b11 end with the acrobat airborne; b02 and b12 require the
  air; b12's foot releases at its start) and `kinematic.json` (no support at 1.20 and 8.60); later plans re-bound;
  outputs and checklists regenerated
- `tests/test_motion_solver.py` (a break), `tests/test_contact_pass.py`, `tests/test_kinematic_solver.py` (D1's
  consequences); `kernel/knowledge_map.yaml` BIO (kernel log); F-058 resolved; F-053;
  backlog; CHANGELOG

## Verification
- before: `scripts/verify.sh` exit 0, 619 passed (S-021, d573fd6)
- after: `scripts/verify.sh` exit 0, 620 passed (the first run failed twice: test_contact_pass asserted every wizard
  contact at its beat's end, now it names the dodge flip's two releases at its start; the support-change test's slot no
  longer has a change in progress, so it builds one on a copy of the packet; both follow from D1)
- Prediction 1 held (the vault and the dodge flip; nothing else). Prediction 2 held after a second try: moving only the
  support to none was refused by S11 (S06 still grounded at those slots), so the takeoff effects moved to the beats
  before (D1). Prediction 3 held (620; no row changed result).

## Next
M9-09d (F-064: the kunai reverses to -Z, O77).
