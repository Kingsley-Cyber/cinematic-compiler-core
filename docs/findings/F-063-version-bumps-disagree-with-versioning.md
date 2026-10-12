# F-063 — Earlier protocol changes took a +0.1 bump, versioning.md says +1.0

<!-- docs-version: 1.0 -->

## Type
drift

## Severity
low

## Layer
docs

## Status
resolved

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
—

## Evidence
- docs/versioning.md (Frozen docs row: "+0.1 for wording; +1.0 for a protocol or rule change")
- docs/docs_log.jsonl seq 15, 16, 19: AGENTS.md 1.1 (step 9, a protocol change), docs/rules.yaml 1.1 (rule R-31),
  AGENTS.md 1.2 (step 1 points to the bootstrap) each took +0.1

## Description
Three earlier frozen-doc changes that altered the protocol or a rule bumped +0.1, against the written rule. Session
S-008 follows the written rule (+1.0 for its protocol and rule changes), so the record now holds both readings.

## Impact
None on behaviour; a reader cannot tell a wording change from a protocol change by the version alone.

## Proposed Fix
The owner picks one reading: keep versioning.md (the past bumps stay as they are; the log is append-only), or
change versioning.md to "+0.1 for an additive change, +1.0 for a breaking one".

## Owner Ruling
none yet

## Related
- PLAN-005
- ADR-O70

## Resolution
ADR-O106 (S-044): docs/versioning.md stands as written; the three earlier +0.1 bumps stay (the log is append-only).
