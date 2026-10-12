# F-127 — Re-block values come from a solver outside the repo

<!-- docs-version: 1.0 -->

## Type
risk

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
- the second principal review, S-045 (docs/reports/2026-10-12-principal-review-2.md)
- S-030 D6, S-038 D6, S-039 D4 and D8, S-041 D5, S-043 D3: least-change values from a scratch optimiser that is not committed
- the values are pinned in tests/test_reference_fight_golden.py (REBLOCKED_ROOTS, GROUNDED_PICKUPS)
- S-039 eased B's lean from 35 to 20 degrees at 4.0 against the source's "B off balance"; F-110 names the pattern for the pickups only
- S-049 (RV-49) re-blocked B at 3.4, 3.7, 4.4, 4.7, 6.6, 8.5 and 9.0-9.5 and the wizard's acrobat at 3.6 with a second
  scratch optimiser (capsule non-penetration with a 0.01 m clearance, contact goals at the surfaces, soles kept at
  their heights), also not committed; its values are pinned in REBLOCKED_ROOTS, the leg-word records and B's end
  state; S-050 (RV-09) chose the hit shots' distances and azimuths by trial against S16's checks (principal
  review 3, S-054)

## Description
Nobody can re-derive the recorded values or see the constraints that kept each move's meaning.

## Impact
Re-blocks cannot be checked or repeated.

## Proposed Fix
Backlog RV-35 widened: the optimiser committed as a tool that derives a key under stated move-keeping constraints, the recorded values re-derived with it; F-110 covers every re-block.

## Owner Ruling
none needed

## Related
- PLAN-007
- F-110

## Resolution
Open in part: solver/reblock.py (RV-35a, S-080) is the committed solver: the least squared change to the listed joint
components that meets stated goals inside stated bounds, with a CLI; it re-derives S-078's three re-blocks from their
goals (within 0.125 degrees) and derived S-080's pickups. Open: the re-blocks recorded from S-030 to S-049 and the
camera values chosen by trial in S-050 and S-076 (S-076's search lives in a scratch file), re-derived with committed
tools (RV-35b).
