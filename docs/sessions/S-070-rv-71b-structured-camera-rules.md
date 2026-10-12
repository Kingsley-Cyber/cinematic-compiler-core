# S-070 — RV-71b: the camera cards' rules as structured fields, checked where they are written

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-71b (PLAN-007); findings F-177, F-160; rulings O92, R-21, R-30, O102

## Layer
L5.5

## Status
applied

## Commit
the commit whose message names [S-070]

## Plan
RV-60 judged the camera rules by word lists (validators/prompt_validator.py `camera_rule_problems`), which miss plain
violations (crash zoom, half speed, slow-mo, a close-up one sentence after the blow) and refuse plain rules ("close to
eye level"), and passed the knight idiom that frames the shield arm at a hit (F-177, review 4).
1. Each convention and idiom carries a `trigger` (when it applies: opening, hit, fast_move, turn, airborne, ...) and
   `asks` (scale, movement, playback, subjects), in the grammar's words (camera_convention_card 1.1,
   camera_idiom_card 1.1). planner/camera_library.py refuses a card whose asks leave the grammar, whose playback leaves
   the card's list, or whose hit rule is not a static hold on every body present at an impact scale (O92).
2. The prompt prints the genre card's statements and the check (CAMERA_RULES, new) wants them word for word; the word
   lists go.
3. The knight's shield idiom becomes a hold on both fighters; the anime speed rule says "between hits", so no card
   rule asks for a moving camera at a hit.

Predictions, made before the change (05:59 by the clock):
1. The gate passes before the change: 691 tests (33b4db2).
2. The structured check refuses the knight's shield idiom as written and passes every other rule; after its rewording
   every card passes.
3. CAMERA_RULES passes all sixteen prose prompts and refuses an injected or altered sentence (the struck "Cut close on
   the receiver after a blow lands.", and the reviewers' crash zoom and half speed).
4. The eight anime prose prompts change in one camera rule; the four camera plans re-bind (hashes only); every
   checklist count stays.
5. About 693 tests (691, CAMERA_RULES' break, a loader test; two tests rewritten with the rule they pin).

## Decisions
- D1 — Each rule's trigger and asks are read from its own words (fourteen triggers; asks in the grammar's scale,
  movement and playback words, and one of five subject kinds). Level: interpretation (F-053).
- D2 — The O92 check lives where the rules are written: planner/camera_library.py refuses a card whose hit rule is not
  a static hold on every body present at an impact scale, or whose asks leave the grammar or the card's playback
  (CAMERA_CARD, raised when S16 loads the card). Level: covered (O92, R-21).
- D3 — The prompt prints the genre card's rules and CAMERA_RULES (new code) wants them word for word; the word lists
  and `camera_rule_problems` go, and C10 gains the code (knowledge map 13). Level: covered (F-177's fix).
- D4 — The knight's shield hit becomes "Hold medium-wide on both fighters as the blow meets the shield."; anime's speed
  rule applies "between hits". Level: interpretation (F-053; R-30: drafts).
- D5 — Two tests change with the check they pin (the cards' words became fields; the prompt's words became the card's
  text), each saying so in its docstring. Level: covered (ADR-O102).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | PASS | `scripts/verify.sh > gate.log && git commit`, after a first gate run read the count |
| One gap, right layer | PASS | the camera cards and their loader (S16, L5.5) and the prompt's printed rules |
| Predictions written first | PASS | the session file was written at 05:59 before the schema edits |
| New checks fire and stay silent | PASS | `rule_problems` refuses the old knight wording and passes every current rule; CAMERA_RULES refuses four injected sentences and an altered one, and passes all sixteen prose prompts |
| Tests changed with their data | PASS | `git diff -- tests`: two tests rewritten with the check they pin (D5), one break added, one unused import dropped |
| Examples | PASS | eight anime prose prompts (the speed rule), four camera plans re-bound, two checklists (hashes); every count the same |
| Records | PASS | F-177, F-160 resolved; F-053 noted; schema log (two schemas 1.1), library log (eight cards), kernel log (map 13), all agent_fix; backlog; PLAN-007; CHANGELOG; run report |
| Hygiene | PASS | the scan over the staged diff before the commit |

## Duration
about 5 minutes by the clock (05:58 to 06:03)

## Changes
- schemas/cards/camera_convention_card.schema.json, camera_idiom_card.schema.json 1.1; the three convention cards (3)
  and five idiom cards (2, 2, 3, 2, 2)
- planner/camera_library.py (`rule_problems`, `_checked`); renderers/prose_renderer.py (`camera_rules`);
  validators/prompt_validator.py (CAMERA_RULES; the word lists removed)
- tests: test_camera_solver.py, test_prose_render.py (one test each rewritten), test_dag_conformance.py (one break)
- kernel/knowledge_map.yaml 13; the examples re-bound and regenerated; docs/reference rebuilt
- F-177, F-160 resolved; F-053 noted; backlog; PLAN-007; CHANGELOG; run report

## Verification
- before: S-069's gate at 33b4db2: 691 passed
- after: `scripts/verify.sh` exit 0, 692 passed, check: PASS
- Prediction 1 held. Prediction 2 held (the old knight refused; every current rule passes). Prediction 3 held
  (sixteen prompts pass; the injected and altered sentences are refused). Prediction 4 held (eight anime prompts in one
  rule; four camera plans; counts the same). Prediction 5 held in part: 692, as the loader's test sits inside the
  rewritten card test.
