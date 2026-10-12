# F-200 — The source, owner_default ADRs and decided_by as rulings

<!-- docs-version: 1.0 -->

## Type
question

## Severity
medium

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
- O105 and O108 reread the source's words as owner_default; O103 sets aside two of O88's flips, which R-06 now leaves to the owner; deviations cite owner_default ADRs (DEV-18, DEV-23); the logs use agent_fix, which R-28 does not define (F-154, F-180)

## Description
1. Does the source fight count as an owner ruling under R-06? 2. Confirm or strike O103, O104, O105, O106, O108. 3. Must a deviation's ruling be an owner ADR in force? 4. Should the run answer listed questions as owner_default ADRs (finish.md section 4) or as F-053 interpretations? 5. Is agent_fix a decided_by value under R-28? 6. Should partly fixed findings be reopened (S-063) or kept resolved with a note (S-056 D2)?

## Impact
The slices that build the answer wait for it.

## Proposed Fix
The owner's answer; the slices it opens follow.

## Owner Ruling
needed

## Related
- F-154
- F-180
- ADR-O103
- ADR-O105
- ADR-O108
- R-28

## Resolution
Open.
Noted in S-081 (the sixth review): R-33 says a rewrite is recorded 'in the golden test and the session file', ADR-O102
'or' (F-212).
