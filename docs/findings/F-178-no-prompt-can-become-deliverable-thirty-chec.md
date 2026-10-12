# F-178 — No prompt can become deliverable: thirty checklist rows have no way to pass

<!-- docs-version: 1.0 -->

## Type
gap

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
- the fourth principal review, S-063 (docs/reports/2026-10-12-principal-review-4.md)
- `python -m validators.checklist`: 0 of 20 prompts deliverable; each prose prompt has 0 FAIL and 29 to 36 NOT CHECKED rows, and so has the union
- no backlog item names V1 to V3, V7, V9 to V13, C8, C11, C18, C20, C22, T10 or STY (S-063: 0 mentions each); C20, V3, V6, V10, V11 and V13 are `missing` in kernel/knowledge_map.yaml; C1, C2, C9 and C23 wait on render findings F-013 and F-014 that no code catches (F-117: O20 against O46)
- validators/checklist.py marks an unselected menu (V4, V5) NOT CHECKED, while ADR-O14 says "menus count only where selected"; examples/reference_fight/checklist.md reads P3.2-6 N/A ("no code checks it") although S16's CAMERA_AXIS checks the axis (O53)

## Description
The deliverable condition cannot be met by finishing the backlog.

## Impact
`cinematic compile` exits 5 for every scene, and fight_works cannot hold.

## Proposed Fix
Backlog RV-76: unselected menus N/A (O14) and step-enforced rows judged by their step codes; RV-83: a slice for each unsliced row, or the list of rows for the owner to rule N/A.

## Owner Ruling
which rows must pass for a deliverable (listed, with F-153 and F-117)

## Related
- RV-76
- RV-83
- F-153
- F-117
- ADR-O14
- ADR-O53

## Resolution
Open.
