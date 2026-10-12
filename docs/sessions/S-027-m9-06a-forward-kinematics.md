# S-027 — M9-06a: forward kinematics, roots at the pelvis, printed world points, the miss report (F5.1; O72, O81)

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5)

## Gap
Backlog M9-06a (split from M9-06; PLAN-003 F5.1); findings F-025, F-028, F-062; rulings O24, O72, O81

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-027]

## Plan
O72: a key's root is the pelvis; contacts meet within 0.15 m; repo-authored keys follow the source. O81: land forward
kinematics, the pelvis roots and the printed world points; list every miss, grouped; do not re-block, do not rewrite
the source, do not refuse yet. A draft card of segment lengths (`library/body_segments.yaml`, schema
`schemas/cards/body_segments.schema.json`, logged) feeds `solver/forward_kinematics.py`, which turns a key (root
position and rotation, the eleven joints) into named world points along the Q6 chain (root, Sp, NK, HD, LA, LFA, RA,
RFA, LUL, LL, RUL, RL; at rest upright with the limbs hanging). S13 writes each key's points into the motion graph
(1.1) from its packet's card. The repo-authored keys (everything but the reference fight's A rows) move up to the
pelvis: each supported key's root rises until its lowest supporting foot sole meets its surface's top; airborne keys
move by the offset interpolated between their span's takeoff and landing. Each touch and hold prints the actor's
point and the target's point on its staff line. `solver/contact_world.py` measures every contact and writes the miss
report (docs/reports) and finding F-070.

Predictions, made before the change:
1. At rest the pelvis stands 0.98 m above the soles (thigh 0.45, shin 0.45, ankle 0.08).
2. The repo-authored standing roots rise from 0 to about 0.9-0.98 m; the reference fight's A rows do not change (the
   golden A-rows test passes untouched).
3. Every example's S04 and S13 plans move and later plans re-bind; S16 may refuse a shot framed on the old roots
   (uncertain).
4. After re-rooting, the repo-authored foot supports on the ground meet it by construction; of about 40 measured
   contacts roughly 15-20 meet within 0.15 m; about 8 miss by over 1 m, most limb-to-body and limb-to-prop.
5. The prompts print each touch's two points; no prompt code fires; no checklist row changes result.

## Decisions
- D1 — One draft adult (pelvis 0.98 m over the soles: thigh 0.45, shin 0.45, ankle 0.08; spine 0.50; arm 0.30 + 0.35)
  for every archetype. Why: O24 asks for a segment-length card; per-archetype bodies wait for the owner. Level:
  interpretation (card status draft; F-053).
- D2 — Where a contact part touches: a foot at its sole below the ankle along the shin, a hand at the palm's centre at
  the forearm's end, a leg at the knee, an arm at the elbow, the torso at 0.8 of the spine, the head at its centre.
  Level: interpretation (F-053).
- D3 — The pelvis re-rooting (O72) of the repo-authored keys: a supported key's root rises until its lowest supporting
  sole meets its surface's top (another supporting part keeps 0.1 m above it); a support on a surface with no top (a
  wall) gives no height; an airborne key moves by the offset interpolated between its span's ends. The reference
  fight's A rows (the source) are untouched (ADR-O81). Run once from a scratch script; its first run stopped on the UGC
  demo (no floor) after writing three examples and was restored from git before the second; the wizard's pinned key
  first went underground (a wall read as ground) and was redone. Level: covered (O72), the rule's details
  interpretation (F-053).
- D4 — SURFACE_HEIGHT judges a landing only on the pose at its instant: the acrobat pinned to the stone pillar at 5.20
  (pelvis 1.77 m up its face) lands at 6.40 with no key there, and the check compared that landing with the 5.20
  pose. Why: R-17 (the content is consistent; the check measured the wrong instant). Downstream: one landing (both
  feet at 6.40) is not judged; fourteen are. Level: covered (R-17).
- D5 — The printed points: on each touch or hold of a prop or a body ("R foot at [1.19, 1.41, 4.57], kunai blade at
  [0.5, 1, 4.6]"), as their own item after the bow so no reader of the bows changes; supports on surfaces are not
  printed. Why: F5.1's printed form and O81 ("print the world points in the prompt"). Level: covered (F5.1, O81).
- D6 — Measurement rules for the report: a touch on any surface but a floor is a face (not measurable); flags mark the
  owner's artefacts (airborne, rotating, prop moving); the likely cause is a heuristic. Level: interpretation (F-053).
- D7 — M9-06 split into M9-06a (this) and M9-06b (the refusal, blocked on the owner's review; ADR-O81); backlog 6.
  Level: covered (O81).

## Duration
about 120 minutes

## Changes
- new: `solver/forward_kinematics.py`, `solver/contact_world.py`, `validators/contact_world_report.py`,
  `library/body_segments.yaml` (draft, library log), `schemas/cards/body_segments.schema.json` (schema log),
  `tests/test_forward_kinematics.py`, `docs/reports/2026-10-11-contact-world-misses.md`, ADR-O81, F-070
- `schemas/graphs/motion_graph.schema.json` 1.1 (points; logged); `compiler/passes/derived/p13_motion.py` (the packet
  carries the segments; nodes carry points); `renderers/prose_renderer.py` (the printed points);
  `planner/dynamic_beat_validator.py` (SURFACE_HEIGHT at the onset's pose)
- every example's S04 anchors and S13 roots for the repo-authored keys (pelvis); every later plan re-bound; outputs and
  checklists regenerated
- `kernel/knowledge_map.yaml` C21 note (kernel log); F-053; backlog (version 6); CHANGELOG
- tests pinning repo roots at y 0 now read the pelvis: test_prose_render, test_render, test_state_pass

## Verification
- before: `scripts/verify.sh` exit 0, 623 passed (S-026, 594f2c2; pushed)
- after: `scripts/verify.sh` exit 0, 627 passed (the first run failed three tests that pinned repo-authored roots at
  y 0: B's end state, the wizard's 1.60 key, the acrobat's 0.00 key; each now reads its pelvis height, as O72 intends)
- Prediction 1 held (the soles at y 0 at rest). Prediction 2 held (B's standing roots 0.83-0.96 m; the golden A-rows
  test passes untouched). Prediction 3 held in part: every example's S04 and S13 plans moved and re-bound and S16 did
  not refuse, but S04's SURFACE_HEIGHT refused the wizard's pinned landing (D4). Prediction 4 failed: 9 of 33
  measured contacts meet within 0.15 m, not 15-20; 24 miss, 6 by over 1 m. Prediction 5 held (no prompt finding; no
  row changed result).

## Next
Report the miss list to the owner (O81); M9-06b waits for the owner.
