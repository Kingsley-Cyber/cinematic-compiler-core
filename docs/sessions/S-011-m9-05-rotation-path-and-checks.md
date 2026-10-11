# S-011 — M9-05: rotation runs checked at S13 and named in the prompt (FR.1, FR.3)

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5), autopilot run 1 (docs/reports/2026-10-11-autopilot-1.md)

## Gap
Backlog M9-05 (PLAN-003 FR.1 as amended by W3, FR.3); findings F-028, F-058; rulings O32 (axes), O33 (derived
rotation), O38 (a named flip completes in the clip), O47 (W3)

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-011]

## Plan
FR.1 as amended by W3 already prints each turn once ("ONE backflip about the side-to-side axis (sagittal plane), 5.10–5.50;
takeoff 4.70, landing 5.90", M9-01); nothing checks it for turns that no beat names (spins), and S13 never checks a run
of keys as a whole. S13 (`solver/euler_solver.py`) gains three run checks over consecutive keys declaring one turn:
ROTATION_NOT_MONOTONIC (the angle about the turn's axis moves one way through the run), ROTATION_INCOMPLETE (a run a
beat names as a flip or cartwheel ends inside the clip on a whole number of turns, O38), INVERSION_MISSING (where a
flip or cartwheel passes 180 degrees, the root interpolated between its keys is upside down). The prompt gains
ROTATION_PATH_UNSTATED: every turn run, named or not, is written on its first line and continued on the later ones.
The wizard's dodge_flip ends at 180 (inverted) at 9.40 with no landing in the clip; O38 rules it gets its landing key.

Predictions, made before the change:
1. The gate passes before the change: 593 tests.
2. On the four examples' current plans the new S13 checks fire once: ROTATION_INCOMPLETE on the wizard's dodge_flip
   (acrobat, 180 of 360, 8.60–9.40); ROTATION_NOT_MONOTONIC and INVERSION_MISSING fire nowhere.
3. ROTATION_PATH_UNSTATED fires on none of the 16 prose prompts and fires on its break (a spin's words removed).
4. After the O38 re-authoring (the 9.40 land_guard key upright at X 0 on both feet; b12's effects end crouching and
   grounded), the wizard compiles through S17 after a re-bind; S04, S11 and S13 plans change; S16 may refuse a shot
   that relied on the inverted pose (uncertain).
5. The wizard's dodge_flip line reads "ONE backflip about the side-to-side axis (sagittal plane), 8.60–9.40" with its
   takeoff and landing; its render.txt and four prose prompts change; the other examples' outputs do not.
6. No checklist row changes result on the reference fight; on the wizard, rows reading the acrobat's last keys may
   move (uncertain which).
7. About 600 tests.

## Decisions
- D1 — One slice, not split: the S13 checks and the prompt code together. Why: the prompt code checks words M9-01
  already prints from the same turn runs (no new render work), as M9-02 and M9-03 paired a step check with its prompt
  twin; the backlog lists the four codes on one item. Alternatives: split as M9-04 was (that split had S04 schema and
  data work on one side). Level: covered (backlog M9-05).
- D2 — A run is the consecutive keys of one performer declaring the same turn; it ends at the first key that does not
  (the run's last delta reaches that key). Monotonic means one sign of the delta about the turn's axis across the run.
  Why: FR.3's "one sign across a multi-key run" and euler_solver's continuous angles (the delta is the rotation
  performed). Level: covered (FR.3).
- D3 — Complete means within 30 degrees of a whole number of turns (at least one), and the run's last key inside the
  clip. Why: O38; the 30 degrees is the prose's existing FULL_TURN_SLACK (labelled interpretation), moved to
  euler_solver so S13 and the prose share one number. Alternatives: exactly 360 (the reference turns are exact; a
  hand-authored 350 would be refused). Level: interpretation (the slack, already in F-053's list as the prose's).
- D4 — Inversion: at every crossing of 180 + 360k along a flip or cartwheel run, the root interpolated linearly in
  Euler angles between the bracketing keys has its up axis at y <= -0.5 (the existing UPRIGHT threshold). Why: FR.3
  ("a run that passes 180 has its inversion") as amended by W3 (derived and checked, not printed); linear spacing is
  FR.1's stated interpretation. Level: interpretation (Claude's, for owner review; added to F-053).
- D5 — Map: ROTATION_PATH_UNSTATED on M4 (with ROTATION_ANGLES_PRINTED, the other W3 code); the three S13 codes as
  EXT1 locators (root Euler, S13). Why: step codes live in `enforced_by`, prompt codes in `codes`
  (test_dag_conformance); the plan's section 6 names no rows for these codes. Level: interpretation (row choice).
- D6 — O38's landing key is a new hold beat b14 "hold_guard" at 9.80-10.00 with the acrobat's landing key (upright,
  crouched, both feet, at [-1.1, 0, 5.3], yaw -330.945 found with S13's own heading function); land_guard (b13) is
  shortened to 9.40-9.80, becomes an action that continues the flip from the 9.40 apex and lands at its end, with a
  hard cause to b14. Why: O38 ("the wizard's dodge_flip gets its landing key", Q-R: "adding its landing key"); the plan
  calls the 9.40 key the apex ("Apex of the backflip, fully inverted"), so turning it into the landing would break the
  plan's own words. Alternatives: the 9.40 apex key as the landing (planned first; dropped when the data showed the
  apex), a landing key at 10.00 (no slot can start at the clip's end). Downstream: the wizard's S04, S11, S12, S13,
  S15 and S16 plans (one entry each for acrobat@b14; c11 shows b14), re-bound; its outputs. Level: covered (O38;
  ADR-O71 rule 1); the new beat and its values are Claude's interpretation, added to F-053.
- D7 — F-058 (the acrobat's first flip starts turning on the ground before its 1.60 takeoff) stays open for M9-09c.
  Why: none of FR.3's three checks refuses it (that run is monotonic, complete and inverted at 180); the launch check
  is FR.4 (M9-09c, which lists F-058). Level: covered (backlog).

- D8 — The dodge_flip's takeoff now prints at 9.40 (the apex) because b12's foot releases sit at its end; added to
  F-058 for M9-09c, not fixed here. Why: the release timing is FR.4's (the launch check, M9-09c); M9-05 is not a leaf
  (M9-09a, M9-09b, M9-09c, M9-11 and M9-13 depend on it), so an uncovered data change waits (ADR-O71 rule 3); the data
  is unchanged, the prompt only states it plainly now. Alternatives: move the releases to b12's start now (uncovered).
  Level: covered (O71).

## Duration
about 75 minutes

## Changes
- `solver/euler_solver.py`: `turn_runs`, `run_findings`, `_inversion_findings`, FULL_TURN_SLACK (labelled
  interpretation); `renderers/prose_renderer.py` uses that slack; `validators/prompt_validator.py`: ROTATION_PATH_UNSTATED
- `examples/wizard_vs_acrobat/plans/`: temporal (b13 shortened and continuing the flip, b14 hold_guard), kinematic,
  bartenieff, motion (b13 declares the flip; b14 landing key), effort (b14 press), camera (c11 shows b14); re-bound;
  render.json re-bound only; outputs and checklist regenerated
- `kernel/knowledge_map.yaml` (M4 code, EXT1 locators; kernel log), `tests/test_motion_solver.py` (three breaks, one
  prompt test), `tests/test_dag_conformance.py` (one break), `tests/test_dynamic_beat_validator.py` (the zero-length
  hold break moves from b13 to b14, the wizard's hold since D6)
- F-053, F-058, backlog (M9-05 done, M9-06 next), CHANGELOG, lessons L-19, the run report

## Verification
- before: `scripts/verify.sh` exit 0, 593 passed (the pre-commit gate of S-010, a3a2f31)
- after: `scripts/verify.sh` exit 0, 598 passed (the first run failed twice: a stale live-action checklist after the
  map edit, lesson L-20; and a BEAT_TIME break aimed at b13 as the wizard's hold, now b14); `make golden`: the wizard's render.txt and four prose prompts
  changed on purpose (the completed backflip, b14); the other examples unchanged
- Prediction 1 held. Prediction 2 held (one refusal, ROTATION_INCOMPLETE on the dodge_flip; my first check compiled
  only to S03 and showed none: lesson L-19). Prediction 3 held. Prediction 4 changed with D6 (b13 and b14 rather than
  the 9.40 key; six plans, not three); S16 did not refuse. Prediction 5 held in part: the line reads "ONE backflip
  about the side-to-side axis (sagittal plane), 8.60–9.80; takeoff 9.40, landing 9.80" (the takeoff at the apex is
  F-058's, D8). Prediction 6 held (no row changed result on either example). Prediction 7 held roughly: 598, not about 600.

## Next
M9-06 (F5.1/F5.2 world contact points by forward kinematics).
