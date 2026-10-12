# ADR-O95 — "Never mirrored" applies to strikes and action beats, not idle guards

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-11

## Decided By
owner

## Scope
L4c

## Decision
Owner, in chat, 2026-10-11, answering the principal review's question 8 (S-035): "\"Never mirrored\" applies to strikes and action beats, not idle guards. The 6 symmetric A rows and 5 mirrored B guards stay. Veto: none."

## Context
F-086: 18 of 73 keys mirror within 5 degrees while PLAN-006 had said "never mirrored"; the owner was also asked to veto S-034's D1, D2, D5 and D6.

## Consequences
- AS-04 refuses a mirror-symmetric key on a strike or action beat (MIRRORED_ACTION), never on an idle guard; A's six symmetric source rows (0.0, 0.6, 2.0, 3.4, 3.7, 5.9) and B's five guards (b04, b06, b07, b15, b16) stay.
- S-034's D1 (hands and feet as words), D2 (the chain from the support to the striking limb), D5 (AS-01 before M9-10) and D6 (the trail authored at S12) stand.

## Alternatives Considered
- —

## Supersedes
—

## Superseded By
—

## Related
- ADR-O87
- F-086
- PLAN-006
