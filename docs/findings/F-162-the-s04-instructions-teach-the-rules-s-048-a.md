# F-162 — The S04 instructions teach the rules S-048 and S-051 changed

<!-- docs-version: 1.0 -->

## Type
contradiction

## Severity
medium

## Layer
L1.1

## Status
open

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the third principal review, S-054 (docs/reports/2026-10-12-principal-review-3.md)
- planner/prompts/beat_planning.txt: "effects and contacts commit at t + dur" (an effect may say `at: start` since S-048) and "catch, throw and disarm name a prop" (a catch and a throw may name a body since S-051)
- the knowledge map's C21 note says an impact frame needs a touch or support onset

## Description
The packet's instructions contradict the code.

## Impact
The next S04 author is taught the old rules.

## Proposed Fix
Backlog RV-48b ("the S04 prompt rewritten"): the instructions and notes follow the code; RV-20 keeps only its layer-order part.

## Owner Ruling
none needed

## Related
- PLAN-007
- F-135
- RV-48b
- RV-20

## Resolution
Open in part (review 4, S-063): the instructions name every code, but two of their sentences teach what the code refuses (F-077's jump, "deployment hidden") and the test checks names only; F-170, RV-67.
Before: RV-48b (S-058): planner/prompts/beat_planning.txt teaches the rules S04 to S07 apply to a beat plan today (an
effect's and a contact's `at`, a change of hands at its possess or release, a catch and a throw on a prop or a body,
releases on a key, the vanished body, prop samples, the decoy's swap, first places) and names each one's code;
tests/test_instructions.py fails when a code S04 to S07 emit, or one S08 emits, is missing from its step's
instructions. C21's note follows the code (knowledge map 9). RV-20's prompt part for S11 to S17 is RV-65; RV-20 keeps
external_inputs.
