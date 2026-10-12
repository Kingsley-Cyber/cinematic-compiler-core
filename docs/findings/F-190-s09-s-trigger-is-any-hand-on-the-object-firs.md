# F-190 — S09's trigger is any hand on the object, first come

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
medium

## Layer
L2.6

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
- compiler/passes/derived/p09_object_state.py: any hand contact in the triggering beat at or before the change counts; probe: the glasses become worn at 5.5 credited to a left-hand tap at 3.5, after the right hand let go
- the UGC render prints "change worn no->yes in b03 by b03_c1 (i02)", the left-hand touch, beside "right_hand does put_on"

## Description
RV-72 closed F-173's class for releases only; S-071 D2 claims a hand that let go earlier is not on the object.

## Impact
A change can be credited to a hand that is not on the object at that instant, or not the interaction's.

## Proposed Fix
Backlog RV-88: the trigger is the interaction's hand on the object at the change's instant (a contact at that instant or a hold across it). F-173 reopened in part.

## Owner Ruling
none needed

## Related
- RV-88
- F-173

## Resolution
Open.
