# F-058 — Wizard example: the front flip turns before its takeoff and is inverted at the landing key

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
medium

## Layer
L4c

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
—

## Evidence
examples/wizard_vs_acrobat (B 1.20-2.60; prose 'takeoff 1.60' after the turn starts at 1.20; 2.00 key at 180 with 'lands ... in a deep crouch')

## Description
B's run of flip keys starts on the ground at 1.20 (support both feet), so the turn begins before the takeoff at 1.60, and the 2.00 key, whose action says B lands in a deep crouch, is at 180 degrees (inverted).

## Impact
See the description.

## Proposed Fix
FR.3/FR.4 at S13 (backlog M9-05, M9-09) will refuse it; re-author B's keys then.

## Owner Ruling
none yet

## Related
- PLAN-001

## Resolution
Open.
