# S-058 — RV-48b: the support hand holds or touches its object; the S04 and S08 instructions follow the code

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-48b (PLAN-007); findings F-137 (S08, L2.5), F-135 (its prompt part), F-162; rulings O23, O91, O93,
O102

## Layer
L1.1

## Status
applied

## Commit
the commit whose message names [S-058]

## Plan
Two gaps from reviews 2 and 3:
1. S08 (F-137): a named support hand holds the object at the start of one of the interaction's beats or touches it in
   one of them (HAND_ROLE_SWAP, the code that already guards the agent hand; MASTER_PLAN: roles hold across the
   interaction); planner/prompts/hand_roles.txt says so.
2. The S04 instructions (F-135, F-162): planner/prompts/beat_planning.txt rewritten to the rules S04 to S07 apply to a
   beat plan today (effects and contacts at their beat's end or start, a change of hands at its possess or release,
   catch and throw on a prop or a body, releases on a key, the vanished body, prop samples, PROP_SUPPORT,
   SURFACE_HEIGHT with `standing_leg_m`, the decoy's swap, first places), naming each rule's code. A test keeps the
   instructions complete: every code S04's validator and the S05, S06 and S07 passes emit, and every S08 code, is
   named in its step's instructions. The knowledge map's C21 note follows the code (map 9).
3. Re-bind the examples whose packets move; regenerate them.

Predictions, made before the change (03:49 by the clock):
1. The gate passes before the change: 670 tests (30e97a0).
2. The support-hand rule refuses F-137's case (the right hand's hold cleared from i01's beat) with HAND_ROLE_SWAP and
   passes both UGC interactions as authored (i01's right hand holds the glasses from 0.0; i02's left hand touches them
   at 5.5). No other example has a hand-role plan.
3. The new instructions test fails on today's text: S04's instructions name 3 of the 35 codes S04 to S07 emit
   (PROP_FIRST_STATE, CONTACT_VERB, CAUSE_REASON); S08's name none of its 6.
4. The rebind moves exactly five plans (the four temporal plans, the UGC's hand-role plan); no prompt text, checklist
   or plan content other than packet hashes changes.
5. About 673 tests (670, one S08 test, two instruction tests).

## Decisions
- D1 — A named support hand meets its role as the agent hand does: it holds the object at the start of one of the
  interaction's beats or makes any contact on it in one (HAND_ROLE_SWAP, the code that already locks the roles).
  Level: interpretation ("holds or touches", F-137's fix; listed in F-053).
- D2 — The S04 instructions answer for the codes S05, S06 and S07 emit as well as S04's, since those passes read only
  the beat plan and their refusals are the plan's to fix. Level: interpretation (F-053).
- D3 — tests/test_instructions.py reads each step's codes from its checks' own sources (`_finding(`, `add(`,
  `"code":`), less the passes' contract codes MISSING_INPUT and WRITE_SCOPE, so a new rule fails until it is taught.
  Level: covered (F-162: the instructions follow the code).
- D4 — The S04 instructions close with three later checks its placements meet (BODY_OVERLAP and CONTACT_WORLD at S13,
  IMPACT_CONTACT_SYNC at S17), as advice, not as S04's rules. Level: covered (p17's IMPACT_CONTACT_SYNC: "the fix is
  upstream: the contact's `at` in the S04 plan").
- D5 — C21's note follows the code (knowledge map 9, kernel log, agent_fix). Level: covered (F-162).
- D6 — RV-20 split: its prompt part for S11 to S17 is RV-65 (ready); RV-20 keeps external_inputs, blocked on the
  layer-order ADR; backlog 25. Level: interpretation (F-095 names only the layer order as the block; F-053).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | PASS | `scripts/verify.sh` exit 0, 673 passed, check: PASS, after the last edit |
| One gap, right layer | PASS | the support hand at S08, where roles are checked; the instructions in S04's and S08's packets; the test reads the checks' sources |
| Predictions written first | PASS | written 03:49, before any edit; prediction 3 measured on the old text (3 of 35, 0 of 6), prediction 2 on the old code |
| New checks fire and stay silent | PASS | the old S08 check passed F-137's case and the new one refuses it (HAND_ROLE_SWAP); both UGC interactions pass; the instructions test failed on the old texts and passes now |
| Tests changed with their data | PASS | `git diff -- tests`: one test added to test_hand_role.py, a new tests/test_instructions.py; no test edited, skipped or deleted |
| Examples | PASS | `compiler.rebind --write` moved the four temporal plans and the UGC's hand-role plan; the plans and envelopes changed only in hashes; no prompt, prose or checklist changed |
| Records | PASS | F-135, F-137, F-162 resolved; F-095 and F-053 noted; knowledge map 9 logged; backlog 25; PLAN-007, CHANGELOG, run report |
| Hygiene | PASS | the scan before the push |
Claim corrected before the commit: the vanished body's line said no beat "gives it a contact"; the code refuses the
vanished actor as a contact's side a, so it now says no beat "has it make a contact" (a contact on it is the next
clause).

## Duration
about 12 minutes by the clock (03:45 to 03:57)

## Changes
- compiler/passes/derived/p08_hand_role.py (the support hand; `_on`); planner/prompts/hand_roles.txt (each rule by
  its code)
- planner/prompts/beat_planning.txt (rewritten: the rules S04 to S07 apply to a beat plan, each by its code)
- tests/test_instructions.py (new), tests/test_hand_role.py (one test)
- the four examples re-bound (temporal plans; the UGC's hand-role plan) and regenerated (envelope hashes only)
- kernel/knowledge_map.yaml 9 (C21's note; kernel log); F-135, F-137, F-162 resolved; F-095, F-053 noted; backlog 25
  (RV-48b done, RV-60 next, RV-20 split into RV-20 and RV-65); PLAN-007; CHANGELOG; run report

## Verification
- before: S-057's gate at 30e97a0: `scripts/verify.sh` exit 0, 670 passed
- after: `scripts/verify.sh` exit 0, 673 passed, check: PASS
- Prediction 1 held. Prediction 2 held (the old check returns nothing on F-137's case; the new one HAND_ROLE_SWAP on
  i01). Prediction 3 held exactly (3 of 35; 0 of 6). Prediction 4 held (five plans, hashes only; the wording fix moved
  the four temporal plans again, hashes only). Prediction 5 held (673).
