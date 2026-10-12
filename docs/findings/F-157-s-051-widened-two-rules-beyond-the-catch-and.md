# F-157 — S-051 widened two rules beyond the catch and the drive

<!-- docs-version: 1.0 -->

## Type
bug

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
- the third principal review, S-054 (docs/reports/2026-10-12-principal-review-3.md)
- compiler/passes/derived/p17_render.py `impact_sync` and validators/prompt_validator.py `_impact_checks` accept any possess that starts on an impact frame: an impact frame added at 0.0, where B merely holds the kunai, now passes
- renderers/prose_renderer.py `strike_contacts` drops any touch on any held prop, so a weapon clash or a disarm kick would not count as a strike

## Description
O93 asked for the catch and the drive; the rules now excuse every grasp and every touch of a held weapon.

## Impact
A wrong impact frame or a real strike can pass unnoticed.

## Proposed Fix
Backlog RV-58: a possess counts on an impact frame only as a catch; a touch of a prop another performer holds is no strike only when the touching part is not a hand or foot; tests at both boundaries.

## Owner Ruling
none needed (O93, O23)

## Related
- PLAN-007
- F-084
- RV-58

## Resolution
Open.
