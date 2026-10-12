# F-121 — The rulebook forbade what the finish run did: per-slice pushes, self-answered questions, unseen owner_default ADRs

<!-- docs-version: 1.0 -->

## Type
contradiction

## Severity
medium

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
- R-03 and ADR-O5 "Nothing is pushed without the owner's word"; R-30 "Only the owner approves a push ... and a change to ... the golden"; R-06 "wait instead of guessing"; R-28 and AGENTS.md section 14: owner_default is a proposal the owner saw
- finish.md sections 3 and 4 grant a push per slice and answers from the sources; eight slices pushed to public main; ADR-O102 to O106 accepted owner_default before the owner saw them

## Description
The records disagreed with the run the owner started.

## Impact
A reader of the rules could not tell what the run was allowed to do.

## Proposed Fix
The owner rules; the rulebook records it.

## Owner Ruling
ADR-O107 ("keep pushing, continue the finish run")

## Related
- ADR-O101
- ADR-O107
- R-03
- R-06
- R-28
- R-30

## Resolution
ADR-O107 (owner, 2026-10-12); rules 5.0: R-03, R-06 and R-30 name the finish run's pushes, answers and recorded golden changes; R-06 keeps a question that would set aside an owner ruling or invariant for the owner; finish.md 2.0 says the same and leaves F-088 to the owner; the owner saw ADR-O102 to O106 listed and objected to none.
