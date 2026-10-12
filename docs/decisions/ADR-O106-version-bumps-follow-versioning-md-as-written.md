# ADR-O106 — Version bumps follow docs/versioning.md as written

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-12

## Decided By
owner_default

## Scope
docs

## Decision
Answered from the sources under ADR-O101 (finish run 1, S-044), for F-063: docs/versioning.md stands as written. A
frozen doc takes +0.1 for wording and +1.0 for a protocol or rule change; a schema, library card or kernel file takes a
new version with every change. The three earlier protocol and rule changes that took +0.1 (docs log seq 15, 16, 19) and
the logged changes that kept their version stay as they are, since the logs are append-only; from S-044 the gate
refuses a log entry that changes a file without changing its version, and docs/rules.yaml takes 4.0 for R-35.

## Context
F-063: "Three earlier frozen-doc changes that altered the protocol or a rule bumped +0.1, against the written rule."
F-078 (the principal review, S-035): "docs/rules.yaml went 3.0 to 3.1 for the new rule R-35 (S-029), against
docs/versioning.md (+1.0 for a rule change)"; its proposed fix is "rules 4.0; the gate checks that a changed logged file
carries a new version". docs/versioning.md: "Frozen docs ... +0.1 for wording; +1.0 for a protocol or rule change".
Session S-008 followed the written rule.

## Consequences
- docs/rules.yaml 4.0; kernel/docs_plane.py refuses an unbumped change in the schemas, library and kernel logs after
  each log's end at S-044, as it already does for the docs log (owner O64).
- The size of a bump (wording or protocol) stays the author's to choose and the self-audit's to check.

## Alternatives Considered
- Rewrite versioning.md to "+0.1 additive, +1.0 breaking" (F-063's second option): the written rule already serves,
  and S-008 and the review both read it this way.

## Supersedes
—

## Superseded By
—

## Related
- ADR-O64
- F-063
- F-078
- PLAN-007
