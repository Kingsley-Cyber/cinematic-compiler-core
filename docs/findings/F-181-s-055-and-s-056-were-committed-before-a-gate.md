# F-181 — S-055 and S-056 were committed before a gate ran after their last edit

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
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the fourth principal review, S-063 (docs/reports/2026-10-12-principal-review-4.md)
- the rules reviewer: each session file was last written 13 s before its commit, and the gate takes about 75 s; no hook runs it (F-168)
- S-063 re-ran the gate on the exported trees a14f99a and e0a04e7: both pass (check: PASS)

## Description
The trees were green, but the rule that the gate runs after the last edit (R-02, AGENTS.md section 9) was not kept.

## Impact
A record edit after the gate could have pushed a red tree.

## Proposed Fix
From S-064 the run commits only through `scripts/verify.sh > gate.log && git commit`; the owner's `make hooks` (F-168) closes it.

## Owner Ruling
none needed

## Related
- F-168
- R-02

## Resolution
Open: the chained commit from S-064; the hook waits for the owner (F-168).
