# F-114 — Do R-21, R-23 and R-25 bind render.txt?

<!-- docs-version: 1.0 -->

## Type
question

## Severity
medium

## Layer
L6

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
- render.txt prints holds in frames ("[[5.5,12]]"), angles inside turns and no causal reasons, as the LBN-2.4 format does (ADR-O1, ADR-O55, the owner invariant no_render_compression)
- R-21, R-23 and R-25 are written for every emitted prompt

## Description
Question: do these rules bind LBN-2.4, or only the structured prose?

## Impact
Either the LBN prompts fail three rules by design or the rules need a scope.

## Proposed Fix
None until the owner rules.

## Owner Ruling
the question open

## Related
- PLAN-007
- ADR-O1

## Resolution
Open.
