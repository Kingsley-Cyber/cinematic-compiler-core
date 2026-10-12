# S-069 — RV-71a: a hit's hold is still on a steady rig and names its bodies; idiom cards reach the scene's archetypes

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-71 (split: RV-71a here, RV-71b the structured card rules; PLAN-007); findings F-177, F-160; rulings O92,
R-21, R-30

## Layer
L5.5

## Status
applied

## Commit
the commit whose message names [S-069]

## Plan
Review 4 (F-177) found HIT_HOLD's hold to be `movement.kind == static` alone, so a shaky handheld shot passes; the
prompt's HIT_HOLD reads the "t impact: hold with " prefix, not the bodies printed after it; and the camera idiom cards
load by archetype id, so ninja.yaml never reaches the fight's ninja_lean and ninja_broad.
1. A hit's hold is a static shot on a locked or smooth stability (the grammar's still kinds), at S16 and S17.
2. The prompt's HIT_HOLD reads the bodies its hold line names and refuses one that leaves out a body present.
3. An archetype card may name its camera idiom card (`camera_idioms`, archetype_card 1.1); ninja_lean and ninja_broad
   name ninja.
4. RV-71b keeps the rest of F-177: the cards' rules as structured fields in place of the word lists.

Predictions, made before the change (05:52 by the clock):
1. The gate passes before the change: 688 tests (a04f668).
2. Every hit shot in the examples is static on a locked tripod (the reference fight's c05, c11, c16, c20; the
   wizard's c04), so nothing in them is refused; a shaky handheld static c11 is refused at S16 and S17.
3. Today's prompts pass the bodies check; a hold line that names only A is refused.
4. The ninja idioms reach the reference fight's S16 packet, so only its camera plan re-binds (hash only); no prompt
   changes.
5. About 690 tests (688, a stability probe, a printed-bodies probe).

## Decisions
- D1 — A hit's hold is a static shot whose stability is locked or smooth, the grammar's still kinds; floating and shaky
  are not. Level: interpretation (F-053's list via F-177; O92's "camera hold").
- D2 — The prompt's HIT_HOLD reads the labels in the hold line's parentheses and refuses one that leaves out a body
  present (a vanished one is not). Level: covered (O92: "both bodies in frame").
- D3 — An archetype card may name its idiom card (`camera_idioms`, archetype_card 1.1); ninja_lean and ninja_broad
  name ninja (version 2). Logged as agent_fix (R-28). Level: covered (F-177).
- D4 — RV-71 split: RV-71b carries the structured card rules (backlog 27). Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | PASS | `scripts/verify.sh > gate.log && git commit`, after a first gate run read the count |
| One gap, right layer | PASS | S16's and S17's hit checks, the prompt's hold check, the idiom loader (L5.5) |
| Predictions written first | PASS | the session file was written at 05:52 before the code edits |
| New checks fire and stay silent | PASS | the five hit shots pass (locked tripods); a shaky handheld or floating gimbal c04 fails at S16 and S17; a hold naming only A fails ("leaves out B") |
| Tests changed with their data | PASS | `git diff -- tests`: three tests added |
| Examples | PASS | the reference fight's camera plan re-bound (hash only) and its envelope; no prompt or checklist changed |
| Records | PASS | F-177 open in part (RV-71b); schema log (archetype_card 1.1), library log (two cards, agent_fix); backlog 27; PLAN-007; CHANGELOG; run report |
| Hygiene | PASS | the scan over the staged diff before the commit |
Claim corrected before the commit: the first record script stopped at the backlog step (RV-71's status read next, not
ready), after updating F-177 only; the rest was written again.

## Duration
about 5 minutes by the clock (05:51 to 05:56)

## Changes
- validators/camera_validator.py (STILL; the hold's stability), compiler/passes/derived/p17_render.py (the same; its
  docstring), validators/prompt_validator.py (the printed bodies; HIT_HOLD's description), planner/camera_library.py
  (idioms by the archetype's `camera_idioms`)
- schemas/cards/archetype_card.schema.json 1.1; library/archetypes/ninja_lean.yaml, ninja_broad.yaml version 2
- tests: test_camera_solver.py, test_render.py, test_prose_render.py (one test each)
- the reference fight's camera plan re-bound; F-177 noted; backlog 27; PLAN-007; CHANGELOG; run report

## Verification
- before: S-068's gate at a04f668: 688 passed
- after: `scripts/verify.sh` exit 0, 691 passed, check: PASS
- Prediction 1 held. Prediction 2 held (the five shots pass; the shaky c04 is refused at S16 and S17). Prediction 3
  held (today's prompts pass; "leaves out B"). Prediction 4 held (the reference fight's camera plan alone, hash
  only). Prediction 5 held (691, about 690).
