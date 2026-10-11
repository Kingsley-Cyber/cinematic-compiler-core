# S-015 — M9-08a: the opening from y 10 onto the 8 m top, and SURFACE_HEIGHT (O21)

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5), autopilot run 1 (docs/reports/2026-10-11-autopilot-1.md)

## Gap
Backlog M9-08a (split from M9-08; PLAN-003 section 9 item 8); finding F-010; ruling O21 (X7)

## Layer
L1.1

## Status
applied

## Commit
the commit whose message names [S-015]

## Plan
O21 (audit X7): the pillar keeps its 8 m top; A starts above the frame at root y=10 and lands with the feet on the top
at y=8 (root about 8.5). The data still starts A at root y 7.5 and lands it at 7.2, below the top it stands on, and
nothing refuses that. S04's packet gains each surface's geometry text from its world card (`ax`, "pillar at z=6 from
y=0 to y=8"; the ground is y=0 by the convention), and S04 checks SURFACE_HEIGHT: when a foot starts bearing weight
on a surface, the performer's root is between the surface's top and a leg's length above it. The reference fight's
b01 and b02 anchors and S13 root positions follow O21, b02's action says y=8, and the golden test records the
deviation.

Predictions, made before the change:
1. The gate passes before the change: 605 tests.
2. With the packet carrying surface tops, SURFACE_HEIGHT fires once on the current data: A's landing on the pillar at
   0.60 (root y 7.2 under the 8 m top). The ground supports of all four examples pass (roots 0 to 0.9 m).
3. After the O21 edit (b01 y 10, b02 y 8.5), S04 passes; S13 refuses until its two root positions follow the anchors;
   S16 may refuse a shot aimed at A's old heights (uncertain; lesson L-07 if it does).
4. The reference prompts' Euler lines at 0.00 and 0.60 and b02's action text change; render.txt changes (root
   positions); the other examples do not.
5. The golden test needs the two A rows recorded as O21's deviation, and b02's action text as a rewording (L-08).
6. No checklist row changes result; about 609 tests.

## Decisions
- D1 — Split M9-08: M9-08a at S04 (O21's data and SURFACE_HEIGHT), M9-08b at the render step (V6's wording); backlog
  4. Why: the backlog's rule (split per step). Level: covered.
- D2 — SURFACE_HEIGHT means: at a foot support's onset on a surface whose top is known, the performer's root (its
  latest anchor) lies between the top (less 0.05 m) and 1.2 m above it. Why: the plan names the code only; X7's defect
  was a root below the top it stands on; a range holds under both readings of the root (ADR-O72: a pelvis 0.5 to 1.0 m
  above, a ground point at 0) without deciding between them. Alternatives: an exact pelvis height (needs ADR-O72).
  Downstream: every foot support in the four examples. Level: interpretation (Claude's, for owner review; F-053).
- D3 — A surface's top comes from its world card's geometry text ("from y=0 to y=8" gives 8), the ground's from the
  convention (y=0); a surface without one is not checked. Why: the card is the declared geometry (S02 already carries
  `ax` on surface nodes); no new field or card edit. Alternatives: a structured `top_y` on the card (a card and schema
  change for one number). Level: interpretation (Claude's, for owner review; F-053).
- D4 — O21's data: b01 A at [0, 10, 3.5], b02 A at [0, 8.5, 5.8], b02's action "both feet on the pillar top at y=8",
  and the two S13 root positions to match. Why: O21's own numbers (root y=10; feet on the top at y=8, root about 8.5).
  Level: covered (O21; ADR-O71 rule 1).
- D5 — The query's literal "A starts ABOVE the frame, falling from y=8" stays in the SCENE line, which now disagrees
  with the root at y 10; recorded as finding F-067 for the owner. Why: the query is the owner's text (never edited);
  O21 quotes "falling from y=10", which the source does not say. Level: covered (AGENTS.md section 1: a discovered
  contradiction is a finding).
- D6 — F-016 (S01 drops the query's literal starts, counts and anchors) stays open: this slice reads surface tops
  from the world card, not from the query. Why: parsing literal anchors is S01's own slice; the backlog listed F-016
  under M9-08 as related. Level: covered (backlog).

## Duration
about 50 minutes

## Changes
- `planner/beat_planner.py` (the packet's surfaces carry `ax`); `planner/dynamic_beat_validator.py` (SURFACE_HEIGHT:
  `_tops`, `_surface_heights`; labelled interpretation)
- `examples/reference_fight/plans/temporal.json` (b01, b02 anchors; b02's action "y=8") and `motion.json` (the two
  roots; b02's description "y=8"); every example's S04 plan re-bound, the reference fight's later plans too; outputs
  and checklists regenerated
- tests: a SURFACE_HEIGHT break and a landing test (test_dynamic_beat_validator); OPENING and OPENING_WORDS (golden)
- `kernel/knowledge_map.yaml` C9 (kernel log); `docs/findings/F-067-*.md`; F-053; backlog (M9-08 split, version 4);
  CHANGELOG; the run report

## Verification
- before: `scripts/verify.sh` exit 0, 605 passed (the pre-commit gate of S-014, ffed2bf)
- after: `scripts/verify.sh` exit 0, 607 passed; `make golden`: the reference fight's render.txt and four prose prompts
  changed on purpose (A's roots at 0.00 and 0.60, b02's words); the other examples' outputs unchanged
- Prediction 1 held. Prediction 2 held (the landing at 0.60, once per foot; every ground support passes). Prediction
  3: S13 was edited with S04, so it never refused; S16 did not refuse; S15's packet moved after the b02 description
  edit and was re-bound (L-04). Prediction 4 held. Prediction 5 held in part: the two rows needed recording and the
  0.60 description's "y=8" too (OPENING_WORDS); the kernel items needed no rewording. Prediction 6 held (no row
  changed result; 607 tests, not about 609).

## Next
M9-08b (the opening in V6's wording).
