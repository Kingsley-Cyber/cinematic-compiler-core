# F-158 — The throw releases A at 6.8, off its pose, against O23 and the source

<!-- docs-version: 1.0 -->

## Type
contradiction

## Severity
medium

## Layer
L1.1

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
- ADR-O23: strike, throw and release contacts happen at their key pose (`at: start`); the source's anime fx: "6.6 throw release flash"
- S-051 (RV-10) released A at b17's end, 6.8, where neither fighter has a key, and cut b17 to 6.6-6.8: the timeline's only gap, with no Effort for A over 6.80-7.00 or for B over 6.80-7.50; CONTACT_WORLD does not measure a body's release

## Description
The catch's throw sits between poses.

## Impact
The model reads a throw at an instant no pose shows.

## Proposed Fix
Backlog RV-48 (RELEASE_AT_POSE): b17 back to 6.6-7.0 and the throw released at its start, 6.6, with the catch, as the source flashes it.

## Owner Ruling
none needed (O23, O93)

## Related
- PLAN-007
- F-084
- F-135
- ADR-O23
- RV-48

## Resolution
Open.
