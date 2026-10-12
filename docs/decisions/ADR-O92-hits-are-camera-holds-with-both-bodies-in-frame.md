# ADR-O92 — Hits are camera holds with both bodies in frame; no playback ramps

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-11

## Decided By
owner

## Scope
L5.5

## Decision
Owner, in chat, 2026-10-11, answering the principal review's question 5 (S-035): "Camera hold with both bodies in frame at 2.5, 4.7, 8.5. No playback ramps. Hits are holds, not inserts."

## Context
F-083: the hits at 2.5, 4.7 and 8.5 were 85 mm slow-motion smash-cut inserts and playback ramps sat inside a fixed 10 s, against R-21 and O47 (F-005).

## Consequences
- Backlog RV-09: the three hits are camera holds framing both bodies; no playback speed change in the clip; S16 checks HIT_HOLD and PLAYBACK_RAMP.
- As built (S-050): PLAYBACK_RAMP at S16 and in the prompt; HIT_HOLD at S17 and in the prompt, judging the holds S17 places on impact frames; F-155 (RV-57) moves it to the hits found from the contacts, at S16 (RV-46, S-056).

## Alternatives Considered
- —

## Supersedes
—

## Superseded By
—

## Related
- ADR-O47
- R-21
- F-005
- F-083
- PLAN-007
