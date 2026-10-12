# S-029 — M9-06c: legs read from the trunk, the segment card calibrated to the source's grounded A rows, re-root (O82)

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5)

## Gap
Backlog M9-06c; finding F-070; rulings O7, O72, O81, O82; rule R-17

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-029]

## Plan
O82: calibrate `library/body_segments.yaml` to the source's grounded A rows, re-root the repo-authored keys, regenerate
the miss report. The owner, 2026-10-11: "their are signs the source poses and repo fwd kin dont agree ,issing by
0.5-0,8m continue".

A probe before any change (the source's 24 A rows from `kernel/sources/lbn-2.3-adv.txt`, knees at +|X| by O7, the
eighteen feet of the nine rows marked "support=both feet" on the ground) showed that no leg length fixes the misses
while the legs hang from the root: the best thigh and shin hit the search's edges (0.30 and 0.80 m) and still leave
the feet 0.29 m off on average, up to 0.42 m. The source's crouches (hip -135, knee 90, root pitch 20, Sp 60 at 9.00)
put the soles level with the pelvis when the hip angle is read from the pelvis; read from the trunk (root then Sp), the
same numbers put them on the ground. With the legs hanging from the trunk, one scale of the draft leg (x1.25: thigh
0.56, shin 0.56, ankle 0.10; standing pelvis 1.22 m) fits all the grounded source feet but the right foot at 3.00
(RUL +90, against the row's own "R: leg fwd mid") with a root-mean-square of 0.18 m; leaving out the slide at 5.90 as
well gives 0.09 m and puts 14 of 15 feet within 0.15 m.

Rival readings, each with its best single leg scale, over the 17 grounded source feet (scratch probe, kept in the
session's notes): legs from the root (now) x1.84, 4 of 17 within 0.15 m; legs from the root with the root read
yaw-first x1.30, 5 of 17; legs from the trunk (root, then Sp; Q6 order) x1.25, 14 of 17; legs from the trunk read
yaw-first x1.12, 11 of 17. The leg frame is the cause, not the Euler order (Q6 stands).

The fork, found before any code changed: the repo's authoring prompt (`planner/prompts/euler_solving.txt`) puts leans
in Sp with the legs planted, which is the pelvis reading; 42 repo-authored keys lean through Sp. Under the trunk
reading their legs swing with the lean unless their hip angles are re-expressed (R_hip' = R_Sp^-1 R_hip), and
re-expressing them changes 47 of the 102 printed leg words (B's "right-back-low" becomes "right-forward-low"). The
calibrated leg (standing pelvis 1.22 m) also fits the anime ninja, while the card is shared by every archetype. No
rule or ruling picks either; asked the owner (2026-10-11) before changing code. The owner ruled (ADR-O84: trunk,
everywhere, the repo's keys re-expressed, R-33 deviations, the authoring rule changed; ADR-O85: anime bodies get the
fitted leg, live action and UGC keep the adult; ADR-O83 accepted) and pointed out that the plan answers: PLAN-003
F5.1 asks for segment lengths "per archetype or body mode" and R-20 settles the convention (lesson L-23).

So: `solver/forward_kinematics.py` hangs the legs from the trunk; the card's leg is scaled to the fit; the
repo-authored keys re-root under the new body (S-027's rule); S04's SURFACE_HEIGHT bound reads the card's standing
leg instead of its fixed 1.2 m; the miss report is written again under a new date-stamped name beside the one the
owner reviewed.

Predictions, made before the change:
1. The gate passes before the change: 627 tests.
2. On the reference fight's measured A ground supports: 3.00 left foot and both feet at 9.00 move within 0.15 m;
   3.00 right foot (the source's RUL +90) and both feet at 5.90 (the slide) still miss; 7.50 (a repo-shaped row,
   M9-03) stays within 0.15 m (uncertain).
3. The repo-authored standing roots rise by about 0.24 m (pelvis 0.98 to 1.22); every example's S04 and S13 plans
   move and the later plans re-bind; S04 or S16 may refuse a moved pose (uncertain).
4. The miss list: from 9 of 33 measured contacts within 0.15 m to about 12-14; the source A ground misses from 6 to
   3; the repo-authored limb-to-prop and limb-to-body misses stay (M9-06b's re-blocking, ADR-O83).
5. The staff words do not change (they read each joint's own rotation); the printed world points change; no prompt
   code fires; no checklist row changes result.
6. About 630 tests (the source-fit test and a chain test added).

## Decisions
- D1 — Asked the owner which leg frame and which bodies before changing code. Why: R-06 as I read it then; the owner
  ruled O84 and O85 and noted that PLAN-003 F5.1 ("per archetype or body mode") and R-20 already answered (lesson
  L-23). Level: covered (O84, O85).
- D2 — The hip joints sit on the pelvis (the root's frame); only the thighs turn with the trunk. Why: anatomy; the
  same fit on the source (its grounded rows bend Sp about X only, which leaves the hip line where it was); a
  re-expressed repo key keeps every point even where Sp twists. Alternatives: the hip joints on the trunk's frame (they
  move up to about 3 cm when Sp twists). Downstream: every leg point. Level: interpretation (F-053).
- D3 — The anime leg is one scale of the adult's: x1.25, rounded to thigh 0.56, shin 0.56, ankle 0.10 (standing
  pelvis 1.22 m), least squares over the 17 grounded source feet other than 3.00's right; the upper body stays the
  adult's. Why: O82 (the source's grounded rows), O85; one parameter keeps the draft's proportions, and only feet
  constrain the leg (the free two-length fit, 0.54 and 0.60, is no better). Level: covered (O82, O85); the method is
  an interpretation (F-053).
- D4 — The card holds `bodies` (adult, anime), each with the `genres` that use it, and a `default` (adult); S13's
  packet carries the genre's body (schema 2.0, card version 2, both logged). Why: O85. Level: covered.
- D5 — 43 keys re-expressed, R_hip' = R_Sp^-1 R_hip in Euler XYZ rounded to 0.01 degree; the script asserted every
  knee and sole within 1 mm of where it was. The owner's 42 counted leans of 5 degrees or more; a UGC key leans less.
  Why: O84 ("preserve their bodies"). Level: covered.
- D6 — The re-root reran S-027's rule with each genre's body: the anime examples' repo-authored roots rose 0.14 to
  0.26 m; live action and UGC moved 0.00 m, which checks D5 (their bodies did not move). Why: O72, O82. Level:
  covered.
- D7 — A's rows at 0.6, 7.5 and 8.0 were re-rooted too (+0.21, +0.26, +0.21): their roots are the repo's (O21's
  landing on the 8 m top, O18's grounded pickups), not the source's, and they sank under the anime body. Poses
  unchanged; the golden test's OPENING and GROUNDED_PICKUPS pins moved with a note; the miss report counts them as
  repo-authored. Alternatives: leave them sunk (M9-06b would then re-block them anyway, O83 point 1). Level: covered
  (O72, O82, O83); which rows count as repo-authored is an interpretation (F-053).
- D8 — SURFACE_HEIGHT's bound is the genre body's standing leg, 0.05 m either way (it was 1.2 m): S04's packet
  carries `standing_leg_m`. Why: R-17 (an anime pelvis over straight legs stands 1.22 m up, above the old bound);
  the leg lives in the card (O85). Level: interpretation (F-053).
- D9 — The new miss list is a new dated report beside the one the owner reviewed. Why: AGENTS.md section 12
  (reports are dated records). Level: covered.
- D10 — The 47 changed leg words are recorded as R-33 deviations in tests/test_leg_frame_rewrites.py and in the
  table below; the source's A rows print no new word. Why: O84 ("Record each as an R-33 deviation"). Level: covered.
- D11 — The source's grounded rows that still miss are pinned with reasons in tests/test_forward_kinematics.py
  (3.00 right: RUL +90 against its own words; 4.00 right: its root at 0.9 where the same pose stands at 1.1, a row
  the repo does not draw, O18; 5.90 both: the slide), for M9-06b's exceptions. Why: O83 point 2. Level: covered.
- D12 — This slice is committed before M9-06b starts, and pushed after M9-06b. Why: the owner's "Then proceed with
  M9-06b ... and push" (working agreements 5; R-02, one slice per commit). Level: covered.

The 47 leg words (R-33 deviations, owner O84):

| Example | Key | Leg | Hip before | Hip now | Word before | Word now |
|---|---|---|---|---|---|---|
| reference_fight | ninja_broad@b01 | right | [-10, 0, -8] | [-20, 0, -8] | right-forward-low | forward-low |
| reference_fight | ninja_broad@b04 | left | [-15, 0, 8] | [-20, 0, 8] | left-forward-low | forward-low |
| reference_fight | ninja_broad@b05 | left | [-30, 0, 8] | [-46.78, 14, 22.43] | forward-low | left-forward-mid |
| reference_fight | ninja_broad@b05 | right | [10, 0, -8] | [-5.32, 19.92, -6.18] | right-back-low | place-low |
| reference_fight | ninja_broad@b06 | left | [-15, 0, 8] | [-20, 0, 8] | left-forward-low | forward-low |
| reference_fight | ninja_broad@b08 | left | [-60, 0, 8] | [-85.17, 1.29, 22.95] | forward-mid | left-forward-mid |
| reference_fight | ninja_broad@b08 | right | [15, 0, -8] | [-10.35, 14.77, -5.34] | right-back-low | right-forward-low |
| reference_fight | ninja_broad@b09 | left | [-60, 0, 8] | [-85.17, 1.29, 22.95] | forward-mid | left-forward-mid |
| reference_fight | ninja_broad@b09 | right | [15, 0, -8] | [-10.35, 14.77, -5.34] | right-back-low | right-forward-low |
| reference_fight | ninja_broad@b10 | left | [-40, 0, 10] | [-75, 0, 10] | forward-low | forward-mid |
| reference_fight | ninja_broad@b10 | right | [20, 0, -10] | [-15, 0, -10] | right-back-low | right-forward-low |
| reference_fight | ninja_broad@b11 | left | [-40, 0, 10] | [-75, 0, 10] | forward-low | forward-mid |
| reference_fight | ninja_broad@b11 | right | [20, 0, -10] | [-15, 0, -10] | right-back-low | right-forward-low |
| reference_fight | ninja_broad@b12 | left | [-10, 0, 10] | [15, 0, 10] | left-forward-low | left-back-low |
| reference_fight | ninja_broad@b12 | right | [10, 0, -10] | [35, 0, -10] | right-back-low | back-low |
| reference_fight | ninja_broad@b13 | left | [-10, 0, 10] | [15, 0, 10] | left-forward-low | left-back-low |
| reference_fight | ninja_broad@b13 | right | [10, 0, -10] | [35, 0, -10] | right-back-low | back-low |
| reference_fight | ninja_broad@b14 | left | [-50, 0, 10] | [-63.43, 14.48, 36.57] | forward-mid | left-forward-mid |
| reference_fight | ninja_broad@b14 | right | [-20, 0, -10] | [-33.69, 25.66, 6.1] | right-forward-low | forward-low |
| reference_fight | ninja_broad@b17 | left | [-40, 0, 10] | [-56.66, -11.31, -6.6] | forward-low | forward-mid |
| reference_fight | ninja_broad@b17 | right | [10, 0, -10] | [-5.32, -19.92, -11.82] | right-back-low | right-low |
| reference_fight | ninja_broad@b19 | left | [-10, 0, 10] | [5.18, -14.94, 11.34] | left-forward-low | left-low |
| reference_fight | ninja_broad@b20 | left | [-35, 0, 10] | [-5, 0, 10] | forward-low | left-forward-low |
| reference_fight | ninja_broad@b20 | right | [-5, 0, -10] | [25, 0, -10] | right-forward-low | right-back-low |
| reference_fight | ninja_broad@b21 | left | [-30, 0, 10] | [-69.72, 9.39, 6.55] | forward-low | forward-mid |
| reference_fight | ninja_broad@b21 | right | [-20, 0, -10] | [-59.62, 8.65, -15.04] | right-forward-low | forward-mid |
| wizard_vs_acrobat | acrobat@b01 | left | [15, 0, 0] | [-10, 0, 0] | back-low | forward-low |
| wizard_vs_acrobat | acrobat@b02 | left | [-95, 0, 8] | [-140, 0, 8] | forward-mid | forward-high |
| wizard_vs_acrobat | acrobat@b02 | right | [-100, 0, -8] | [-145, 0, -8] | forward-mid | forward-high |
| wizard_vs_acrobat | acrobat@b03 | right | [-10, 0, 0] | [0, 0, 0] | forward-low | place-low |
| wizard_vs_acrobat | acrobat@b05 | right | [-75, 0, -10] | [-94.33, 2.5, -39.91] | forward-mid | right-forward-mid |
| wizard_vs_acrobat | acrobat@b06 | left | [-30, 0, 5] | [-10, 0, 5] | forward-low | left-forward-low |
| wizard_vs_acrobat | acrobat@b06 | right | [-60, 0, -15] | [-40, 0, -15] | forward-mid | right-forward-low |
| wizard_vs_acrobat | acrobat@b11 | left | [-40, 0, 8] | [-45, 0, 8] | forward-low | forward-mid |
| wizard_vs_acrobat | acrobat@b13 | left | [-110, 0, 5] | [-145, 0, 5] | forward-mid | forward-high |
| wizard_vs_acrobat | acrobat@b13 | right | [-110, 0, -5] | [-145, 0, -5] | forward-mid | forward-high |
| wizard_vs_acrobat | wizard@b03 | left | [-15, 0, 8] | [-20.28, -9.39, 4.55] | left-forward-low | forward-low |
| wizard_vs_acrobat | wizard@b03 | right | [10, 0, -8] | [5.08, -9.96, -7.12] | right-back-low | place-low |
| wizard_vs_acrobat | wizard@b06 | right | [15, 0, -10] | [30, 0, -10] | right-back-low | back-low |
| wizard_vs_acrobat | wizard@b09 | right | [5, 0, -10] | [0, 0, -10] | right-back-low | right-low |
| wizard_vs_acrobat | wizard@b10 | right | [10, 0, -10] | [5.02, 4.98, -10.44] | right-back-low | right-low |
| wizard_vs_acrobat | wizard@b11 | left | [-15, 0, 10] | [-21.88, -23.4, 0.94] | left-forward-low | forward-low |
| live_action_standoff | knight@b01 | right | [10, 0, -6] | [0, 0, -6] | right-back-low | place-low |
| ugc_glasses_demo | ugc_creator@b01 | left | [-5, 0, 6] | [-25, 0, 6] | place-low | forward-low |
| ugc_glasses_demo | ugc_creator@b01 | right | [-5, 0, -6] | [-25, 0, -6] | place-low | forward-low |
| ugc_glasses_demo | ugc_creator@b02 | left | [-5, 0, 6] | [-10, 0, 6] | place-low | left-forward-low |
| ugc_glasses_demo | ugc_creator@b02 | right | [-5, 0, -6] | [-10, 0, -6] | place-low | right-forward-low |

## Duration
about 150 minutes

## Changes
- `solver/forward_kinematics.py` (the thighs from the trunk; `segments(genre)`, `standing_leg`);
  `library/body_segments.yaml` 2 (adult, anime; library log); `schemas/cards/body_segments.schema.json` 2.0 (schema log)
- `compiler/passes/derived/p13_motion.py` (the genre's body in the packet); `planner/beat_planner.py`
  (`standing_leg_m`); `planner/dynamic_beat_validator.py` (SURFACE_HEIGHT's bound); `planner/prompts/euler_solving.txt`
  (hips from the trunk); `solver/staff_geometry.py` docstring (the chain; its words still read each joint's own
  rotation)
- `docs/rules.yaml` 3.1 (R-35; docs log), AGENTS.md regenerated; ADR-O84, ADR-O85 (new), ADR-O83 accepted
- every example's S13 keys (43 hips re-expressed) and the anime examples' S04 anchors and S13 roots (re-rooted); every
  later plan re-bound; outputs and checklists regenerated (no row changed result)
- `validators/contact_world_report.py` (A's repo-authored roots, the header), `docs/reports/2026-10-11-contact-world-misses-trunk.md`
- tests: `test_forward_kinematics.py` (bodies, the leg frame, the source fit, A's re-rooted rows),
  `test_leg_frame_rewrites.py` (new), and pins that moved with the anime roots: test_render, test_state_pass,
  test_dynamic_beat_validator (the bound), test_reference_fight_golden (OPENING, GROUNDED_PICKUPS)
- F-070, F-053, backlog (M9-06c done, M9-06b next), CHANGELOG, lesson L-23

## Verification
- before: `scripts/verify.sh` exit 0, 627 passed (S-028, ddb0ca4)
- after: `scripts/verify.sh` exit 0, 631 passed (the first runs failed on two long lines, on the test module's old
  `segments()` call, on the docs plane before `make docs`, and on three pins of anime roots and the bound's signature,
  each updated with its reason); `make golden`: every example's outputs changed on purpose (the hips, the roots, the
  printed points)
- Prediction 1 held. Prediction 2 held in part: 3.00's left foot (0.06) and both feet at 9.00 (0.00, 0.07) land;
  3.00's right foot (1.54) and the slide (0.55, 0.35) miss; 7.50 failed (its feet sank 0.21-0.26 m until re-rooted, D7;
  now 0.05 and 0.00). Prediction 3 held in part: the anime roots rose 0.14-0.26 m, not a flat 0.24, and live action and
  UGC did not move (O85, ruled after the prediction); every S04 and S13 plan moved; nothing refused. Prediction 4 held:
  13 of 33 within 0.15 m (9 before), the source's ground misses 6 to 3, the repo-authored limb misses stay. Prediction 5
  failed on the words: 47 leg words changed (the hips' re-expression came with O84, after the prediction); the points
  changed, no prompt code fired, no checklist row changed result. Prediction 6 held: 631.

## Next
M9-06b (F5.2 CONTACT_WORLD refuses over 0.15 m; scope ADR-O83, proposed).
