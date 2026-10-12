# F-094 — Replanning cannot reach the step that owns a fix

<!-- docs-version: 1.0 -->

## Type
bug

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
- compiler/replan_trigger.py and cli/main.py: a replan of S08, S10 or S14 raises ValueError (the principal review, S-035 (docs/prompts/principal_review.md))
- failures whose fix lives in S04 (MOMENTUM_MISSING, AIRBORNE_PICKUP, an out-of-reach CONTACT_WORLD miss, IMPACT_CONTACT_SYNC) go back to the failing step's author, who cannot move roots or times
- tests/test_cli.py covers S04 and S06 replans only

## Description
The repair loop breaks for three steps and loops uselessly for upstream causes.

## Impact
A failing compile cannot repair itself.

## Proposed Fix
Backlog RV-19: each refusal names its owning step; the CLI replans every authored step.

## Owner Ruling
none needed

## Related
- PLAN-007

## Resolution
Open.
