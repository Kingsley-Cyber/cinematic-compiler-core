# F-115 — Two gate conditions have no check: soul_check_passes, fight_works

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
high

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
- ADR-O98 (the gate in CLAUDE.md)
- scripts/verify.sh checks tests, logs, the docs plane and the golden only

## Description
The owner's gate now names a soul check and a working fight; nothing reads either.

## Impact
The gate can pass while the fight does not work.

## Proposed Fix
Backlog RV-39: soul_check_passes reads the latest principal review's recorded verdict; fight_works reads an owner render verdict (docs/renders/) bound to the deliverable prompt's sha256 (R-29).

## Owner Ruling
ADR-O98

## Related
- PLAN-007
- ADR-O98
- ADR-O99

## Resolution
Open.
