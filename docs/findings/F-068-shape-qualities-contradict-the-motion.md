# F-068 — Twelve Effort intervals declare a Shape quality their motion contradicts

<!-- docs-version: 1.0 -->

## Type
question

## Severity
medium

## Layer
L5

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
—

## Evidence
- the S-017 prototype (ADR-O73's measure) over the four examples' envelopes: 24 of 42 intervals show neither reading
  of their declared quality; these 12 show the opposite and not the declared one:
- knight@b02-b03 (2.50-6.50) declared retreating; root change [0, 0, 0.2]; form change {'elev': 0.0, 'spread': 0.0, 'knees': 0.0, 'lean': 0.0}
- ninja_lean@b03-b04 (1.10-2.00) declared advancing; root change [0.2, -2.0, -0.9]; form change {'elev': 30.0, 'spread': 0.0, 'knees': 30.0, 'lean': -30.0}
- ninja_broad@b06-b07 (2.50-3.40) declared sinking; root change [0.0, 0, 0.1]; form change {'elev': 46.32, 'spread': -0.13, 'knees': 12.5, 'lean': 20.0}
- ninja_lean@b13-b14 (5.10-5.90) declared retreating; root change [0.0, -1.6, -0.2]; form change {'elev': -45.0, 'spread': 0.0, 'knees': 60.0, 'lean': 70.0}
- ninja_broad@b15-b16 (5.90-6.60) declared sinking; root change [1.2, 0, 0.3]; form change {'elev': 38.74, 'spread': -0.33, 'knees': -65.0, 'lean': -15.0}
- ninja_lean@b15 (5.90-6.30) declared sinking; root change [-0.1, 0.9, -0.3]; form change {'elev': 45.0, 'spread': 0.0, 'knees': -30.0, 'lean': -60.0}
- ninja_broad@b17 (6.60-7.00) declared enclosing; root change [0.8, 0, -0.5]; form change {'elev': -32.14, 'spread': 0.51, 'knees': 0.0, 'lean': -30.0}
- ninja_lean@b18 (7.00-7.50) declared advancing; root change [-0.6, -2.2, -2.7]; form change {'elev': -22.5, 'spread': 0.0, 'knees': 45.0, 'lean': 5.0}
- ninja_broad@b19-b21 (7.50-9.00) declared retreating; root change [0.6, 0, 1.3]; form change {'elev': 11.98, 'spread': 0.17, 'knees': -17.5, 'lean': 15.0}
- ugc_creator@b01 (0.00-1.50) declared advancing; root change [0, 0, 0]; form change {'elev': 6.4, 'spread': 0.04, 'knees': 0.0, 'lean': -15.0}
- acrobat@b05 (2.60-3.60) declared enclosing; root change [-0.4, 0, 0.7]; form change {'elev': 14.26, 'spread': 0.26, 'knees': -72.5, 'lean': -40.0}
- acrobat@b12-b13 (8.60-9.80) declared retreating; root change [-2.1, 0, 0.3]; form change {'elev': -113.77, 'spread': 0.17, 'knees': 55.0, 'lean': 35.0}

## Description
The Effort plans declare a Shape quality per interval without any check; measured against the root's path and the
body's form (O31), a quarter of them say the opposite of what the bodies do.

## Impact
SHAPE_DIRECTION (M9-09a) cannot land without re-authoring Effort intervals that no ruling covers; the prompts print
"shape rising" on bodies that sink.

## Proposed Fix
Rule on ADR-O73 (recommended: refuse contradictions only; re-author these twelve).

## Owner Ruling
ADR-O73

## Related
- ADR-O73
- ADR-O31
- F-029
- PLAN-003

## Resolution
Open.
