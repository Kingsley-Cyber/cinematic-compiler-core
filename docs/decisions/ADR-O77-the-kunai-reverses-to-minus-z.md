# ADR-O77 — The kunai reverses to -Z at the deflect

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-11

## Decided By
owner

## Scope
L1.1

## Decision
Owner, in chat, 2026-10-11: "F-064: The golden is correct. The kunai reverses to -Z at 2.5. Fix the render."

## Context
F-064: the plan's post-contact velocity kept +Z; the source's rule says the deflect reverses it from +Z to -Z.

## Consequences
- The kunai's post-contact sample, its landing and its rest move to -Z (S04), with what depends on them (A's pickup
  at 8.0); recorded in the golden test.

## Alternatives Considered
- Reword the rule instead: rejected by the owner.

## Supersedes
—

## Superseded By
—

## Related
- PLAN-003
