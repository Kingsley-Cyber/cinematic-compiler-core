# F-118 — O37 and the genre_profile schema disagree on where genre values live

<!-- docs-version: 1.0 -->

## Type
question

## Severity
low

## Layer
L6

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
- ADR-O37: genre values in the existing per-genre cards plus a new FX card per genre
- schemas/genre_profile.schema.json (O65, draft) holds the camera arc, holds, smear and speedline policy, dust, shake and float in one profile; S-033 used it for body_type

## Description
Question: which governs M9-11's genre values, O37's split cards or the one genre profile?

## Impact
M9-11 cannot start without the answer.

## Proposed Fix
M9-11 blocked on this finding.

## Owner Ruling
the question open

## Related
- PLAN-007
- ADR-O37
- ADR-O65

## Resolution
Open.
