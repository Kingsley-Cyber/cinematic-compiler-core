# F-127 — Re-block values come from a solver outside the repo

<!-- docs-version: 1.0 -->

## Type
risk

## Severity
medium

## Layer
all

## Status
open

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the second principal review, S-045 (docs/reports/2026-10-12-principal-review-2.md)
- S-030 D6, S-038 D6, S-039 D4 and D8, S-041 D5, S-043 D3: least-change values from a scratch optimiser that is not committed
- the values are pinned in tests/test_reference_fight_golden.py (REBLOCKED_ROOTS, GROUNDED_PICKUPS)
- S-039 eased B's lean from 35 to 20 degrees at 4.0 against the source's "B off balance"; F-110 names the pattern for the pickups only

## Description
Nobody can re-derive the recorded values or see the constraints that kept each move's meaning.

## Impact
Re-blocks cannot be checked or repeated.

## Proposed Fix
Backlog RV-35 widened: the optimiser committed as a tool that derives a key under stated move-keeping constraints, the recorded values re-derived with it; F-110 covers every re-block.

## Owner Ruling
none needed

## Related
- PLAN-007
- F-110

## Resolution
Open.
