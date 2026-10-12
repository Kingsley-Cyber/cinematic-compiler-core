# F-078 — Records drift: versions, logs, the commit hook, stale documents and findings

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
2026-10-11

## Reporter
agent

## Legacy ID
—

## Evidence
- the principal review, S-035 (docs/prompts/principal_review.md)
- docs/rules.yaml went 3.0 to 3.1 for the new rule R-35 (S-029), against docs/versioning.md (+1.0 for a rule change)
- kernel/knowledge_map.yaml stays version 1 through every logged change; library and kernel log entries marked changed keep their versions
- kernel/schema_log.py's kernel file list leaves out kernel/layer_order.yaml, which the docs say to log there
- core.hooksPath is unset in the worktree, so the pre-commit gate is not active
- docs/layer_dependency.md (version 1.4, old step numbers) is linked from README.md; ADR-O82 still calls O83 proposed, ADR-O85 says card 3 (now 4), ADR-O72 and O73 still say "until the owner rules"; F-066 and F-028 are open though answered and built; PLAN-004's gap table lists F-018 as open; F-015's fix is a standing practice

## Description
The records the next session trusts disagree with the repo in small ways that add up.

## Impact
A session navigates by stale facts; a version bump that should flag a rule change does not.

## Proposed Fix
Backlog RV-04: rules 4.0; the gate checks that a changed logged file carries a new version; the kernel log covers layer_order.yaml; `make hooks` in the worktree; the stale documents and ADR texts corrected; F-066, F-028 and F-015 closed.

## Owner Ruling
none needed; F-063 still asks which versioning reading the owner wants (until then the written rule holds)

## Related
- PLAN-007
- F-063
- F-066
- F-028
- F-015

## Resolution
Open.
