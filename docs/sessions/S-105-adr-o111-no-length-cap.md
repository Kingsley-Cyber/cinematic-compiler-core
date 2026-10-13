# S-105 — ADR-O111: no length cap on a prompt (owner)

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Owner instruction in chat (ADR-O111); finding F-088; rule R-19

## Layer
L6

## Status
applied

## Commit
the commit whose message names [S-105]

## Plan
The owner asked to remove whatever makes the prompts shorten to 3,500 characters. That is O97's PROMPT_LENGTH
(validators/prompt_length.py), which refused delivery of every example prompt in `cinematic compile` and the
checklist's deliverable column.
1. Record the instruction as ADR-O111 (owner), superseding O97's caps.
2. Remove PROMPT_LENGTH and both caps (the 1,000-word cap refused the same prompts); R-19 says so.

Predictions, made before the change (15:02 by the clock):
1. `cinematic compile` on the wizard example still exits 5, its refusals naming only checklist rows, no length.
2. No prompt changes; the four checklist.md tables lose their "Fits a cap" column.

## Decisions
- D1 — Both caps go, not only the 3,500 characters: the 1,000-word cap refused the same prompts, so keeping it would
  keep the shortening. Level: the owner's instruction (ADR-O111).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the chained gate commits |
| Owner rulings respected | PASS | ADR-O111 recorded verbatim; ADR-O97 superseded |
| Tests | PASS | tests/test_prompt_length.py replaced by one test that a long prompt is not refused (ADR-O102: the ruling moves the data) |
| Examples | PASS | prompts unchanged; checklist.md tables regenerated |
| Records | PASS | ADR-O111; ADR-O97 superseded; F-088 resolved; R-19 (rules 7.3, docs log); map (kernel log); backlog |

## Duration
from 15:02 to 15:08

## Changes
- validators/prompt_length.py removed; validators/checklist.py; tests/test_prompt_length.py
- docs/rules.yaml 7.3; kernel/knowledge_map.yaml; docs/plans/backlog.yaml; ADR-O111, ADR-O97, F-088
- examples/*/checklist.md

## Verification
- Prediction 1 held (exit 5, refusals list only FAIL and NOT CHECKED rows). Prediction 2 held.
