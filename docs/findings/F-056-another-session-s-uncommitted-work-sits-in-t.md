# F-056 — Another session's uncommitted work sits in the main folder

<!-- docs-version: 1.0 -->

## Type
risk

## Severity
medium

## Layer
docs

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
—

## Evidence
HANDOFF.md 'Parallel session warning'; ADR-O52

## Description
~/Documents/cinematic-compiler-core holds another session's uncommitted files (scripts/build_knowledge_dag_json.py, scripts/verify_dag_check.py, tests/test_knowledge_dag_check.py, examples/reference_fight/knowledge_dag*.json, one scripts/check.sh line). Its knowledge_dag.json is stale against today's map and prompts.

## Impact
See the description.

## Proposed Fix
Leave untouched (O52); the owner decides whether to keep, refresh or drop it.

## Owner Ruling
ADR-O52

## Related
- PLAN-001

## Resolution
Open.
