# F-167 — The S04 author never sees the query it plans

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
high

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
- planner/beat_planner.py: the S04 packet carries the scene, entities, props, surfaces, constraints and vocabulary, but not the raw query
- choreography is never extracted (planner/intent_parser.py) and the scene_reference rules are dropped (F-133), so the golden's beats were written from outside the sealed packet
- the declared validators never run: the envelope's validation fields stay null and a query that drops a hinted fighter or the world compiles (RV-18, F-093, F-142)

## Description
Sealed authoring holds for S04's form, not its content: a new query's choreography reaches no author.

## Impact
A new fight cannot be planned from its packet.

## Proposed Fix
Backlog RV-64: the S04 packet carries the query's choreography and the scene_reference rules; with RV-18 the declared validators run.

## Owner Ruling
none needed (R-04, ADR-O62)

## Related
- PLAN-007
- F-016
- F-133
- F-093
- RV-64
- RV-18

## Resolution
Open.
