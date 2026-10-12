# F-193 — A vanish that never returns still brings the body back

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
medium

## Layer
L6

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
- END_STATE_MISSING asks an end state of every performer; the RULES' spatial-continuity line says the body "reappears at its next line"; only `vanish_note(None)` is tested, no compiled scene
- compiler/passes/derived/p15_effort.py accepts an Effort interval across a vanish; probe: A's b09 and b11 intervals merged pass S15 and the prompt then fires EFFORT_UNDECLARED

## Description
RV-70 fixed the cases the golden reaches.

## Impact
A scene whose body vanishes for good, or whose Effort spans the vanish, compiles into a contradiction.

## Proposed Fix
Backlog RV-91: S15 refuses an interval across a vanish (R-10); a body gone to the end keeps no end state and the RULES say it does not return; a compiled test scene.

## Owner Ruling
none needed (O90)

## Related
- RV-91
- F-176
- ADR-O90

## Resolution
Open.
