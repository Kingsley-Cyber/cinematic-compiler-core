# ADR-O82 — Calibrate the segment card to the source's rows, then turn CONTACT_WORLD on

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-11

## Decided By
owner

## Scope
L4c

## Decision
Owner, in chat, 2026-10-11, after reviewing the miss list (F-070, docs/reports/2026-10-11-contact-world-misses.md):
"push it, then calibrate the card and start M9-06b."

## Context
The miss list showed six of the source's A feet hovering 0.49-0.78 m above the ground: the source's root heights and
leg angles disagree under the draft adult (standing pelvis 0.98 m). The agent recommended calibrating
library/body_segments.yaml to the source's own grounded rows before any refusal. ADR-O81's condition (the owner sees
the list first) is met.

## Consequences
- Backlog M9-06c: calibrate the card to the source's grounded A rows; the repo-authored roots re-root to the new
  pelvis height; the miss report is regenerated.
- M9-06b (CONTACT_WORLD refuses) follows M9-06c; its three open points are ADR-O83 (proposed).

## Alternatives Considered
- Keep the draft adult: not chosen.

## Supersedes
—

## Superseded By
—

## Related
- ADR-O81
- ADR-O83
- F-070
