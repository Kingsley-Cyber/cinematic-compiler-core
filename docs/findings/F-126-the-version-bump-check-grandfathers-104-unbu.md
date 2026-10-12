# F-126 — The version-bump check grandfathers 104 unbumped changes, six of them this run's

<!-- docs-version: 1.0 -->

## Type
gap

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
- the second principal review, S-045 (docs/reports/2026-10-12-principal-review-2.md)
- kernel/docs_plane.py BUMP_CHECKED_AFTER = {schemas: 125, library: 77, kernel: 55}
- kernel log seq 50-55: this run's map edits at version 1; 35 files' latest version strings also label earlier, different content
- the check sees no size: rules 3.0 to 3.1 for a new rule would still pass

## Description
History is kept, but the files whose present version also names older bytes keep an ambiguous version.

## Impact
A version cannot identify a file's content.

## Proposed Fix
Backlog RV-44: each affected file takes one new version now (a new entry each, history kept), then the cutoff goes.

## Owner Ruling
none needed (ADR-O106)

## Related
- PLAN-007
- F-078
- ADR-O106

## Resolution
Open.
