# S-016 — M9-08b: the opening from above in V6's wording (F-010)

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5), autopilot run 1 (docs/reports/2026-10-11-autopilot-1.md)

## Gap
Backlog M9-08b (split from M9-08); finding F-010 (render F10); rulings O21, O51 (V6 sets the opening's wording), R19

## Layer
L6

## Status
applied

## Commit
the commit whose message names [S-016]

## Plan
Renders R1, R2, R4 and R5 started A on the pillar top (F10). Probe V6 (O51) kept A off the pillar at the start in R19
with two sentences: "A's feet touch the pillar top at 0.60, not earlier" (RULES) and "no A standing on the pillar at
the start" (NEGATIVES), with A dropping in feet first. The renderer derives every entrance from the data: a
performer whose first line is airborne and whose first support is its feet on a raised top (a surface whose top,
from its world card, is above the ground). RULES gain "<A> starts in the air above the <surface>, drops in feet
first, and its feet touch the <surface> top at <t>, not earlier." and NEGATIVES "no <A> standing on the <surface> at
the start". The prompt code ENTRANCE_UNSTATED refuses a prompt without them; F10 is then caught (checklist).

Predictions, made before the change:
1. The gate passes before the change: 607 tests.
2. One entrance in the four examples: the reference fight's A onto the wooden pillar at 0.60; the other examples have
   none, so their prompts do not change.
3. The reference fight's four prose prompts gain one RULES line and one negative; render.txt does not change.
4. ENTRANCE_UNSTATED fires on no prompt and on its break; F-010 resolves (F10's caught_by), and the checklist's F10
   column reads caught; no row changes result unless a row reads F10's codes (C9 gains one: it stays PASS on the
   prose prompts).
5. About 609 tests.

## Decisions
- D1 — An entrance: the performer's first line has no support and its first support onset is a foot on a surface
  whose top lies above the ground (SURFACE_HEIGHT's tops). Why: V6's case in data terms, with no name or example in
  the code. Alternatives: read "ABOVE FRAME" from the beat's words (only the golden says it). Level: interpretation
  (Claude's, for owner review; F-053).
- D2 — The wording keeps V6's two sentences that R19 followed (the touch "not earlier" and the negative) and its
  "drops in feet first"; it leaves out V6's "not visible before 0.20" (W4 bans hidden or not-visible wording for
  props, R-24) and "never stands on the ground" (true in the 5 s probe, false in the fight). Why: O51 (V6 sets the
  wording) and R19's frames. Level: covered (O51, R19), the two cuts are Claude's (F-053).
- D3 — The top-of-surface helper moves into `dynamic_beat_validator.surface_tops` and serves S04 and the renderer.
  Why: one rule for what a top is. Level: covered.
- D4 — ENTRANCE_UNSTATED goes on map rows M1 and C9, the rows F10's checklist entry names. Level: covered (checklist).

## Duration
about 30 minutes

## Changes
- `planner/dynamic_beat_validator.py` (`surface_tops`, shared); `renderers/prose_renderer.py` (`entrances`, the
  RULES line, the negative); `validators/prompt_validator.py` (ENTRANCE_UNSTATED, `_entrance_checks`)
- `validators/checklist.py` (F10 caught by ENTRANCE_UNSTATED); `kernel/knowledge_map.yaml` (M1, C9; kernel log)
- tests: a break (test_dag_conformance) and an entrance test (test_render)
- outputs: the reference fight's four prose prompts; checklists; F-010 resolved; F-053; backlog; CHANGELOG; the run
  report

## Verification
- before: `scripts/verify.sh` exit 0, 607 passed (the pre-commit gate of S-015, 2fe3b5e)
- after: `scripts/verify.sh` exit 0, 609 passed (the first run failed: test_checklist pinned M1 as NOT CHECKED while
  F10 was uncaught; the pin now reads PASS, F10 caught); `make golden`: the reference fight's four prose prompts
  changed on purpose (one rule, one negative); render.txt and the other examples unchanged
- Prediction 1 held. Prediction 2 held. Prediction 3 held. Prediction 4 failed in one place: catching F10 moved row M1 (intent first) from NOT CHECKED to PASS on the
  reference fight's four prose prompts (Pure 30 to 31 PASS), which I did not predict; C9 stays NOT CHECKED (F13).
  Prediction 5 held (609).
- tests: `tests/test_checklist.py` M1's pin moves from NOT CHECKED to PASS (F10 caught), as this slice intends.

## Next
M9-09a (F9.1 Laban direction against path and form).
