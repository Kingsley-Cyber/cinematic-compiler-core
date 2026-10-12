# S-075 — RV-13: PROMPT_LENGTH: a prompt over 3,500 characters for Runway or 1,000 words for BytePlus is not delivered

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-13 (PLAN-007); finding F-088; rulings O97, O10, O94, R-19, R-06

## Layer
L6

## Status
applied

## Commit
the commit whose message names [S-075]

## Plan
O97: "Cap prompt length now. 3,500 chars for Runway, 1,000 words for BytePlus. Add the check." O10: the golden passes
conformance with nothing set aside, and tests/test_dag_conformance.py keeps KNOWN empty. A conformance finding that
fires on every prompt would set O10 aside (R-06), so the cap is a delivery refusal, as F-088 put it ("the check
refuses every prompt"):
1. validators/prompt_length.py measures a prompt (characters, words) against O97's two caps; with no target named
   (R-16 leaves targets to M7) a prompt must fit one of them (PROMPT_LENGTH).
2. The checklist's deliverable judgment and `cinematic compile`'s refusal (O94) add the cap; the checklist prints each
   prompt's length and which cap it fits; conformance is untouched.
3. Fitting the prompts under the caps stays RV-13b, waiting for the owner's answer in F-088.
Neighbours: the CLI, the checklist's `--gate`, the knowledge map's prompt-bloat row FM6.

Predictions, made before the change (06:57 by the clock):
1. The gate passes before the change: 697 tests (65d77ee).
2. No prompt fits either cap: all twenty are over 3,500 characters and over 1,000 words.
3. The deliverable count stays 0 of 20, each prompt's refusal now names its length; conformance is unchanged (KNOWN
   stays empty); no prompt text changes.
4. The four checklist files gain the length of each prompt; no verdict count changes.
5. About 699 tests (697, a test of the caps, a test of the refusal).

## Decisions
- D1 — O97's cap is a delivery refusal, not a conformance finding: O10 keeps the golden's conformance with nothing set
  aside, and a finding on every prompt would set it aside (R-06). Level: interpretation (F-053; F-088 had said "the
  check refuses every prompt").
- D2 — With no target named (R-16 leaves targets to M7), a prompt must fit one of the two caps; a word is a run of
  non-space characters. Level: interpretation (F-053).
- D3 — The checklist prints each prompt's words and the caps it fits, and its deliverable column and `cinematic
  compile`'s refusal add the cap; the Any column is deliverable only if a prompt fits a cap. Level: covered (O94, R-19).
- D4 — FM6 (prompt bloat) is enforced by PROMPT_LENGTH (knowledge map 14, agent_fix); `problems` returns (code,
  message) pairs, as the other checks do. Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the chained gate commits |
| One gap, right layer | PASS | the delivery judgment (the checklist and `cinematic compile`, L6); conformance untouched |
| Predictions written first | PASS | the session file was written at 06:57, before any code |
| New checks fire and stay silent | PASS | the measure over all twenty prompts: none fits a cap (the closest 11,464 characters, 1,085 words); a 600-word text fits both, a 900-word one fits BytePlus |
| Neighbours | PASS | `cinematic compile` (refusals), `--gate`, the Any column, FM6's map row |
| Tests changed with their data | PASS | `git diff -- tests`: one new file, two tests |
| Examples | PASS | the four checklist.md files gain the words and caps columns; every verdict count the same; no prompt changed |
| Records | PASS | F-088 open in part (RV-13b); F-053; map 14 (kernel log); backlog (RV-13 done, RV-15 next); PLAN-007; CHANGELOG; run report |
| Hygiene | see Verification | the scan's count copied below |
Claim corrected before the commit: the first `problems` returned formatted strings, so the docs plane and the map's
locator rule found no quoted PROMPT_LENGTH; it now returns (code, message) pairs.

## Duration
from 06:56 (the plan) to 07:00 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- validators/prompt_length.py (new); validators/checklist.py (deliverable, the table's words and caps, refusals)
- tests/test_prompt_length.py (new, two tests)
- the four examples' checklist.md; kernel/knowledge_map.yaml 14 (FM6); docs/reference rebuilt
- F-088 noted; F-053; backlog; PLAN-007; CHANGELOG; run report

## Verification
- before: S-074's gate at 65d77ee: 697 passed
- Prediction 1 held. Prediction 2 held (no prompt fits). Prediction 3 held (0 of 20; each refusal names its length;
  KNOWN stays empty; no prompt changed). Prediction 4 held (the four checklists; counts the same). Prediction 5 held
  (699).
- the gate on this record (07:02:14): `scripts/verify.sh` exit 0, 699 passed in 74.39 s, check: PASS
- the hygiene scan over the staged diff: 0 hits
