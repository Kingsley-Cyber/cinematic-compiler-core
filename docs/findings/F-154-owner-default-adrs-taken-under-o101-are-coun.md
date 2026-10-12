# F-154 — Owner_default ADRs taken under O101 are counted as rulings the owner has not seen

<!-- docs-version: 1.0 -->

## Type
question

## Severity
medium

## Layer
docs

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
- AGENTS.md defines owner_default as a decision the owner saw and did not object to; ADR-O101 lets the run answer questions as owner_default ADRs for the owner to confirm
- S-046 moved two test pins under ADR-O108 (owner_default); ADR-O102 allows a test change where "an owner ruling or the plan's intent" moves its data, ADR-O107 and finish.md say "a ruling"
- the generated owner lists (AGENTS.md section 7, docs/bootstrap/state.md, docs/for_the_owner.md) show no decision awaiting the owner ("0 proposed")

## Description
Accepted owner_default ADRs that the owner never saw read like owner rulings, and test pins have moved under one.

## Impact
The owner cannot see which decisions wait for him, and a test may move on a decision he would strike.

## Proposed Fix
Waits for the owner: does an owner_default ADR count as a ruling for moving a test; confirm or strike O103, O104, O105, O106 and O108. RV-46 lists them in the generated owner lists.

## Owner Ruling
the question open

## Related
- PLAN-007
- ADR-O101
- ADR-O102
- ADR-O107
- ADR-O108
- RV-46

## Resolution
Open.
