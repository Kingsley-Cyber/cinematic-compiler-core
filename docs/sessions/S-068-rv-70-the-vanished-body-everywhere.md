# S-068 — RV-70: a vanished body is gone from every section of the prompt, and VANISHED_BODY reads them

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-70 (PLAN-007); findings F-176, F-163; rulings O18, O90, R-17

## Layer
L6

## Status
applied

## Commit
the commit whose message names [S-068]

## Plan
RV-62 ended A's support on its 3.70 line, but the implied guidance still prints "A 3.70–4.00: maintain light weight,
sudden time, indirect space, free flow (flick quality)" and that every performer "travels through space between
positions"; a vanish that never returns would print "reappears at its next line", "hold sign to the end" and "hold the
final pose"; the prompt's VANISHED_BODY reads STAFF and RULES only, and passes a travelling support on the vanish line
(F-176, review 4).
1. The source gives A's 3.7 row an Effort for the dissolve itself (LBN-2.4: light, sudden, indirect, free; "in-place
   dissolve"), so S15 keeps A's b09 interval; the guidance prints it as the vanish's quality at its instant ("A at
   3.70: vanishes with ... in place; gone until 4.40"), and clips any other interval at a vanish window.
2. The "travels through space" sentence excepts a vanished performer; a vanish that never returns prints that the body
   does not return, with no hold sign or final-pose line.
3. VANISHED_BODY reads the guidance (a span of the gone performer inside its window) and refuses a travelling support
   on the vanish line.

Predictions, made before the change (05:46 by the clock):
1. The gate passes before the change: 687 tests (1144156).
2. S15's plan does not change; the four reference prose prompts lose "A 3.70–4.00: maintain ..." and gain "A at 3.70:
   vanishes with light weight, sudden time, indirect space, free flow (flick quality), in place; gone until 4.40",
   and their "travels through space" sentence gains the exception.
3. The new checks refuse today's four prompts (the guidance line) and the rules reviewer's probe (a vanish line whose
   support steps), and pass the new prompts.
4. Only the reference fight's prose prompts and envelope change; render.txt and every checklist count stay the same.
5. About 689 tests (687, a prompt test, a test of the never-return wording).

## Decisions
- D1 — S15 keeps A's b09 interval: the source gives the 3.7 row an Effort for the dissolve itself (LBN-2.4: light,
  sudden, indirect, free; "in-place dissolve"). Level: covered (R-17: the source).
- D2 — The guidance prints such an interval as the vanish's quality at its instant, "vanishes with ... in place; gone
  until 4.40", and clips any other interval at a vanish; the generic sentence excepts a gone performer. Level:
  interpretation (F-053).
- D3 — VANISHED_BODY reads the guidance (a span of the gone performer inside its window) and refuses a vanish line whose
  support steps; its sections (READS) include the guidance, so the LBN column's "cannot pass" detail names it. Level:
  covered (O90, F-176).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | PASS | `scripts/verify.sh > gate.log && git commit`, after a first gate run read the count |
| One gap, right layer | PASS | the prose renderer and the prompt check (L6); S15's plan unchanged |
| Predictions written first | PASS | the session file was written at 05:46 before the code edits |
| New checks fire and stay silent | PASS | today's four prompts: "The guidance moves A 3.70–4.00 while it is gone"; the regenerated four pass; the stepping probe fires |
| Tests changed with their data | PASS | `git diff -- tests`: one test added |
| Examples | PASS | the reference fight's four prose prompts (two guidance lines) and envelope; every checklist count the same; the four checklists' LBN detail names [IMPLIED GUIDANCE] |
| Records | PASS | F-176 and F-163 resolved; F-053 noted; backlog (RV-70 done, RV-71 next); PLAN-007; CHANGELOG; run report |
| Hygiene | PASS | the scan over the staged diff before the commit |

## Duration
about 4 minutes by the clock (05:44 to 05:48)

## Changes
- renderers/prose_renderer.py (`vanish_note`; the guidance's vanish and clipping; no hold sign on a vanish line);
  validators/prompt_validator.py (VANISHED_BODY reads the guidance; a stepping vanish support)
- tests/test_prose_render.py (one test)
- the reference fight regenerated; the four checklists
- F-176, F-163 resolved; F-053 noted; backlog; PLAN-007; CHANGELOG; run report

## Verification
- before: S-067's gate at 1144156: 687 passed
- after: `scripts/verify.sh` exit 0, 688 passed, check: PASS
- Prediction 1 held. Prediction 2 held (S15's plan unchanged; the two guidance lines as predicted). Prediction 3 held
  (today's four refused, the probe refused, the new four pass). Prediction 4 held in part: render.txt and every count
  stayed, but all four checklists changed in the LBN column's detail. Prediction 5 held in part: 688, one test.
