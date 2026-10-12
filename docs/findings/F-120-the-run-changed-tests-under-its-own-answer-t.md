# F-120 — The run changed tests under its own answer to the owner's question

<!-- docs-version: 1.0 -->

## Type
risk

## Severity
high

## Layer
all

## Status
resolved

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the second principal review, S-045 (docs/reports/2026-10-12-principal-review-2.md)
- ADR-O100, third consequence: until the owner answers F-119, a test changes only where a ruling explicitly asks for the record, otherwise the work stops and reports
- S-037 D1 answered F-119 as ADR-O102 (owner_default); finish.md section 3 called its own clause the owner's explicit ask
- tests changed under ADR-O102 in S-038 to S-043 (the golden's records; S-040's S07 test; S-041's track test and break strings; S-043's pins under O105)

## Description
Two reviewers ranked this the run's first shortcut (no-shortcuts type 3): the builder answered the owner's own question about the owner's clause, then changed tests under that answer.

## Impact
Every test change of the run rested on an answer the owner had not given.

## Proposed Fix
The owner confirms, narrows or strikes ADR-O102.

## Owner Ruling
ADR-O107 ("O102 confirmed")

## Related
- ADR-O100
- ADR-O102
- ADR-O107
- F-119

## Resolution
The owner confirmed ADR-O102 on 2026-10-12 (ADR-O107); ADR-O100's interim rule is superseded.
