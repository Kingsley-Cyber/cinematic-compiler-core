# F-116 — Rebinding re-stamps hashes instead of forcing re-authoring

<!-- docs-version: 1.0 -->

## Type
question

## Severity
medium

## Layer
all

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
—

## Evidence
- the principal review, S-035 (docs/prompts/principal_review.md)
- compiler/rebind.py copies a moved packet's hash into its plan after scripted edits (S-027, S-029, S-030, S-032)
- downstream plans were re-stamped without being re-read (the camera after O72 moved every root); the M2 row's note says a moved plan must be re-authored

## Description
The packet guard (R-04) proves a plan matches its packet's hash, not that its author saw the new packet. Question: should a moved packet show its diff and need the author's re-confirmation, or a fresh authoring, before its plan is re-sealed?

## Impact
Upstream changes pass downstream unexamined.

## Proposed Fix
Backlog RV-40 (blocked on the question).

## Owner Ruling
the question open

## Related
- PLAN-007

## Resolution
Open.
