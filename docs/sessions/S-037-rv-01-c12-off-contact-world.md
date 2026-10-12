# S-037 — RV-01: C12 loses CONTACT_WORLD and is NOT CHECKED until AS-06 (F-074)

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-01 (PLAN-007); findings F-074, F-119; rulings O99, O101, O102

## Layer
L6

## Status
applied

## Commit
the commit whose message names [S-037]

## Plan
S-030 put CONTACT_WORLD on map row C12 (Stylization layer), whose prompt side only checks that two world points are
printed; C12 turned PASS on the twelve prose prompts of the wizard, live-action and UGC examples with nothing about
stylisation checked (F-074). C12 loses the code and its CONTACT_WORLD locator (CONTACT_WORLD stays on C21, where it
belongs); its note says the prompt side waits on AS-06 (limb-only smear and speedline checks). S-030's verification is
corrected. The run's first question, F-119, is answered first (ADR-O102).

Predictions, made before the change:
1. The gate passes before the change: 640 tests.
2. After it: 640 tests; no test changes; `test_every_code_has_a_break_and_every_map_code_is_real` still passes
   (CONTACT_WORLD stays on C21).
3. C12 moves from PASS to NOT CHECKED on the four prose prompts of the wizard, live-action and UGC examples, and from
   FAIL to NOT CHECKED on all four LBN prompts; the reference fight's prose C12 stays NOT CHECKED; no other row moves.

## Decisions
- D1 — F-119 answered before the first slice, from the sources (ADR-O102): a test changes only where a ruling or the
  plan's intent moves the data it pins, each change recorded with its ruling. Why: finish.md section 4 (a question that
  governs every slice is answered first); ADR-O100, O101, O75. Level: covered (O101's grant; owner_default ADR).
- D2 — C12 keeps its graph-side locator (FRAME_SMEAR at S17) and loses CONTACT_WORLD with its locator; its prompt side
  is NOT CHECKED until AS-06. Why: R-19 (NOT CHECKED is not a pass; a row passes only on codes that check it), F-074.
  Alternatives: keep CONTACT_WORLD as a partial code (the shortcut F-074 names). Level: covered.

## Duration
about 15 minutes

## Changes
- kernel/knowledge_map.yaml (C12; kernel log); the four checklists regenerated
- ADR-O102 (new); F-074 and F-119 resolved; S-030's verification corrected; backlog (RV-01 done, RV-02 next);
  CHANGELOG; docs/reports/2026-10-11-finish-1.md (new)

## Verification
- before: `scripts/verify.sh` exit 0, 640 passed (4232a0c)
- after: `scripts/verify.sh` exit 0, 640 passed; `git diff --stat -- tests` empty; only the C12 rows and the count lines
  of the four checklists changed
- Prediction 1 held. Prediction 2 held. Prediction 3 held (wizard prose 39 to 38 PASS, LBN 49 to 48 FAIL, and the same
  in the live-action and UGC examples; the reference fight's LBN C12 went FAIL to NOT CHECKED).

## Next
RV-02 (CONTACT_WORLD per O89).
