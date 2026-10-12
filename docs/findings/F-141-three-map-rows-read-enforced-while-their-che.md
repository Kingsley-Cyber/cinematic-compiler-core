# F-141 — Three map rows read enforced while their checks are looser than the DAG

<!-- docs-version: 1.0 -->

## Type
contradiction

## Severity
medium

## Layer
L1.5

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
- C27 needs "the partner responds during the action" (docs/sources/knowledge_dag_v1.md); CAUSE_TIMING only forbids a response that starts too early (compiler/passes/mandatory/p05_causal.py)
- R-25 and C6 need a reason that states a cause; CAUSE_REASON checks wording: "B is a broad ninja in grey armor with one pauldron." passes it (in memory)
- T10 cites CONTINUITY_PRESENCE, which passes by construction (F-106)

## Description
A row passes on a check that covers part of it (no-shortcuts type 8).

## Impact
The checklist overstates adherence.

## Proposed Fix
Backlog RV-21: the three rows read partial until their checks cover them; C27's reading answered from the DAG's words.

## Owner Ruling
none needed (R-19)

## Related
- PLAN-007
- F-106

## Resolution
Open.
