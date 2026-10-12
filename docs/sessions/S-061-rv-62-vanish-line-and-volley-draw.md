# S-061 — RV-62: the vanishing actor's line ends its support; B draws the volley before throwing it

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-62 (PLAN-007); findings F-163, F-105 (the volley's start); rulings O90, O23, O8, O83, R-33, O102

## Layer
L6

## Status
applied

## Commit
the commit whose message names [S-061]

## Plan
Two lines of the reference prose contradict their own prompt (F-163):
1. "3.70 A: SUPPORT steps left alternating [f:alt]" with "path: left 0.3 m": the renderer reads A's teleport to 4.40
   as a walk, and the legend makes the support last until 4.40 while RULES say A is gone (O90: A's supports end at
   3.7). The vanishing actor's line keeps its key's support for the instant, says it ends there ("then none: A
   vanishes here until 4.40") and prints no travel; the prompt validator's VANISHED_BODY refuses a vanish line that
   carries its support or a path into the vanish.
2. "B's right hand is empty from 2.00 until 6.60" beside the 5.50 throw "R hand > shuriken volley": nothing draws the
   volley from B's thigh pouch (the source's opening, F-105). B draws it at 5.1, B's key in A's backflip beat, where
   the repo's own pose ("arms flung wide", not a source row) is re-posed so the right hand reaches the thigh pouch;
   B's right hand holds the volley until it lets go with the 5.5 throw (on B's key, O23). The volley's card gains the
   flight value `drawn` (holstered, drawn at 5.1, flying at 5.5, embedded at 5.9). Typed deviations: the draw
   (added), the re-posed arm (re-blocked).

Predictions, made before the change (04:24 by the clock):
1. The gate passes before the change: 678 tests (cdce012).
2. Part 1 changes one line in each of the four reference prose prompts (A's 3.70: the support from S11, both feet,
   with its end; no path) and nothing else; the new VANISHED_BODY check refuses today's line in all four.
3. Part 2: a right-arm re-pose alone (RA, RFA) brings B's hand within 0.12 m of the right thigh's surface; S04 to S17
   accept the draw, with the possess at 5.1 and the release at 5.5 both measured at 0.00 m; the prose prints B's
   right hand empty 2.00-5.10 and 5.50-6.60, and the volley's states holstered, drawn 5.10, flying 5.50, embedded
   5.90.
4. Only the reference fight changes (the card is its own); its checklist verdicts stay the same.
5. About 680 tests (678, a vanish-line test, a draw test).

## Decisions
- D1 — The vanishing actor's line keeps its key's support (S11: both feet) for the instant and ends it in words, "then
  none: A vanishes here until 4.40", and prints no travel to where A reappears. Level: covered (O90: A's supports end
  at 3.7); the words are an interpretation (F-053).
- D2 — The prompt's VANISHED_BODY refuses a vanish line whose support lacks that end or that carries a path. Level:
  covered (O90, F-163).
- D3 — B draws the volley at 5.1, its key in A's backflip beat, before the 5.5 throw; the repo's own 5.1 pose (no
  source row) moves only its right arm, RA [15, 0, -5] and RFA [-5, 0, 0], so the hand is at the thigh pouch, 0.05 m
  off the thigh's surface. Level: interpretation (F-053); deviations DEV-30 (added) and DEV-31 (re-blocked).
- D4 — The 5.5 throw keeps its touch (the flick and the impact frame's onset, R-21) and adds the release that ends the
  hold, on B's key (O23); the release goes last among b14's contacts, so the ids the owner's exception list names
  (b14_c2, b14_c3) stay. Level: covered (O23, O83).
- D5 — The volley's draft card gains flight `drawn` (version 2): holstered, drawn at 5.1, flying at 5.5, embedded at
  5.9; b14 requires holder B and flight drawn. Level: interpretation (R-30: the card stays draft).
- D6 — Knowledge map 11: the prompt's VANISHED_BODY locator. Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | PASS | `scripts/verify.sh` exit 0, 680 passed, check: PASS, after the last edit |
| One gap, right layer | PASS | the vanish line in the renderer and its prompt check (L6); the draw in the reference fight's data at S04 and its one pose at S13 |
| Predictions written first | PASS | written 04:24, before any edit; the new check measured on today's prompts before the renderer changed |
| New checks fire and stay silent | PASS | VANISHED_BODY refused today's 3.70 line in all four prompts and passes the new one; the draw test pins the contacts, the pose, the sample and the printed spans |
| Tests changed with their data | PASS | `git diff -- tests`: two tests added and two records (VOLLEY_DRAW, DRAW_POSE) with registry entries; no test edited, skipped or deleted |
| Examples | PASS | only the reference fight changed: A's 3.70 line, B's 5.10 and 5.50 lines, the volley's state machine, the empty-hand spans; verdict counts unchanged (two LBN "cannot pass" counts moved: EMPTY_HAND_UNSTATED 5 to 6, CAUSAL_RULE_MISSING 16 to 17) |
| Records | PASS | F-163 resolved; F-105 and F-053 noted; DEV-30, DEV-31; the card's library log; map 11 (kernel log); docs/reference rebuilt; backlog, PLAN-007, CHANGELOG, run report |
| Hygiene | PASS | the scan before the push |
Claim corrected before the commit: the release first went after the throw's touch, which renumbered b14's contacts and
pointed the owner's exception list at the wrong ones (S13 refused); it now goes last and the list is untouched.

## Duration
about 12 minutes by the clock (04:17 to 04:29)

## Changes
- renderers/prose_renderer.py (the vanish line); validators/prompt_validator.py (VANISHED_BODY on the vanish line)
- library/ontology/objects/shuriken_volley.yaml 2 (flight drawn; library log)
- examples/reference_fight/plans/temporal.json (b13's draw, b14's release and states), motion.json (B's 5.1 right
  arm); the reference fight re-bound (motion, effort, camera, render) and regenerated; deviations.yaml (DEV-30, DEV-31)
- tests: test_prose_render.py (one test), test_reference_fight_golden.py (one test, two records)
- kernel/knowledge_map.yaml 11 (kernel log); F-163 resolved; F-105, F-053 noted; docs/reference rebuilt; backlog
  (RV-62 done, RV-57 next); PLAN-007; CHANGELOG; run report

## Verification
- before: S-060's gate at cdce012: `scripts/verify.sh` exit 0, 678 passed
- after: `scripts/verify.sh` exit 0, 680 passed, check: PASS
- Prediction 1 held. Prediction 2 held (one line in each of the four prompts; the check refused all four before).
  Prediction 3 held (0.05 m off the thigh's surface; both contacts measured at 0.00 m; the spans and states as
  predicted). Prediction 4 held (the reference fight alone; verdict counts the same). Prediction 5 held (680).
