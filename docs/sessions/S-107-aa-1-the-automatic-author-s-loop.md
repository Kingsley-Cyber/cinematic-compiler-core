# S-107 — AA-1: the automatic author's loop

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog AA-1 (PLAN-008); ADR-O112

## Layer
all

## Status
applied

## Commit
the commit whose message names [S-107]

## Plan
1. compiler/author.py: run the pipeline; on AuthorRequired hand the packet to a backend; on a refusal route it to the
   step that can fix it (replan_trigger.owning_step), drop the documents written after it, and hand the packet back
   with the findings; stop at the third refusal; log every call.
2. A replay backend (an example's committed plans) and `cinematic author`.

Predictions, made before the change (15:33 by the clock):
1. Replay re-authors each example's envelope byte for byte with one passed call per authored step.
2. A motion document put under the floor once is refused with FLOOR_PENETRATION and passes on its second attempt.
3. 760 tests (seven new).

## Decisions
- D1 — The author sets each document's packet_sha256 and attempt; a model never copies a hash. Level: covered
  (compiler/authoring.py binds the document to the packet).
- D2 — `cinematic author` always writes what it made, deliverable or not (deliverable.txt lists why not), so the
  owner sees the output (ADR-O112, R-29). Level: the owner's instruction.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the chained gate commits |
| Predictions written first | PASS | at 15:33, before the code |
| No model called | PASS | replay only; live backends wait for the owner (AA-2, AA-5) |
| Tests | PASS | tests/test_author.py: four replays, one retry, one exhaustion |
| Records | PASS | backlog; PLAN-008; CHANGELOG |

## Duration
from 15:33 to 15:45

## Changes
- compiler/author.py (new); cli/main.py (`author`); tests/test_author.py (new); docs

## Verification
- Prediction 1 held (four examples, byte for byte). Prediction 2 held. Prediction 3 failed: 759 (six new tests, one
  of them parametrized four ways, so six plus three).
- `cinematic author` on the wizard example: 7 calls, $0.00, prose_mixed.txt identical to the committed prompt.
