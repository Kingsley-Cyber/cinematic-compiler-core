# F-198 — Which checklist rows must pass for a prompt to be a deliverable

<!-- docs-version: 1.0 -->

## Type
question

## Severity
high

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
- the fifth principal review, S-072 (docs/reports/2026-10-12-principal-review-5.md)
- F-178: thirty rows cannot pass; sixteen have no slice; C1, C2, C9 and C23 wait on render findings (F-117)
- F-153: render.txt's deliverability under O1 and O94

## Description
Which rows must pass, and which are N/A, for a prompt to be a deliverable; how F-013 and F-014 close without a fixed seed (O20 against O46); whether render.txt must be deliverable at all.

## Impact
The slices that build the answer wait for it.

## Proposed Fix
The owner's answer; the slices it opens follow.

## Owner Ruling
needed

## Related
- F-178
- F-153
- F-117
- ADR-O14
- ADR-O94

## Resolution
Open.
