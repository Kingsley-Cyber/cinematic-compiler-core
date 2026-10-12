# F-074 — C12 passes on a check that does not measure stylisation

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
high

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
- kernel/knowledge_map.yaml row C12: codes [CONTACT_WORLD] since S-030
- examples/{wizard_vs_acrobat,live_action_standoff,ugc_glasses_demo}/checklist.md row C12: PASS on all four prose prompts (NOT CHECKED before e5c1682)
- docs/sessions/S-030-m9-06b-contact-world.md, Verification: "on the prose prompts C12 stays NOT CHECKED" (true of the reference fight only)

## Description
S-030 put CONTACT_WORLD on row C12 (Stylization layer) because the plan's section 6 lists it there, but the prompt side of CONTACT_WORLD only checks that two world points are printed. C12 therefore turned PASS on twelve prose prompts while nothing about stylisation (smear, speedlines, the physics-break exception) is checked, and FRAME_SMEAR is itself looser than C12 (F-073). S-030 reported the prose prompts as unaffected.

## Impact
A DAG row reads as passed when its requirement is unchecked (R-19; no-shortcuts type 8).

## Proposed Fix
Backlog RV-01: CONTACT_WORLD comes off C12 (it stays on C21); C12 is NOT CHECKED until AS-06's limb-only smear and speedline checks cover it; S-030's verification line is corrected.

## Owner Ruling
none needed (R-19)

## Related
- PLAN-007
- F-073
- ADR-O99

## Resolution
Open.
