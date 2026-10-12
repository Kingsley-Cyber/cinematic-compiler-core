# F-180 — The records' guards check form, and the logs credit the owner with the builder's choices

<!-- docs-version: 1.0 -->

## Type
drift

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
- kernel/docs_plane.py accepts any non-empty Self-audit section; rows restate their claims ("Predictions written first: PASS, written HH:MM"; "Hygiene: PASS" written before the scan), and S-061's audit left out C21's CONTACT_WORLD count moving from 15 to 17
- tests/test_reference_fight_golden.py accepts any existing ADR as a deviation's ruling: DEV-23 cites the superseded ADR-O71, DEV-18 cites O12 for re-blocks no ruling made, DEV-30 and DEV-31 cite O23, O8 and O83 for interpretations, and owner_default ADRs count
- kernel/kernel_log.jsonl seq 65, 68 and 69, library/library_log.jsonl seq 83 and docs/docs_log.jsonl seq 44 record `decided_by: owner` for changes the builder designed (R-28)
- the commit messages of S-058 and S-060 name no R-rule, and S-057's names DEV-29 without its type
- the fifth principal review, S-072: kernel/kernel_log.jsonl seq 67 also records decided_by owner for a builder's design; the owner's questions on rulings and decided_by are F-200

## Description
Each review's finding gets a guard on its form: a section exists, an ADR id is named, a phrase is printed.

## Impact
The records can pass while saying less than they claim.

## Proposed Fix
Backlog RV-77: a deviation's rulings split into those that decide it (owner ADRs in force) and those it serves, interpretations typed as such; each self-audit row names its command or file; the logs say owner only when the owner decided that change (owner_default or agent_fix otherwise). The append-only entries stay; this finding corrects them.

## Owner Ruling
none needed (R-28)

## Related
- RV-77
- F-166
- F-154
- R-28

## Resolution
Open.
