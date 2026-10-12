# F-211 — Must each fighter's laban chain carry its side of the other's beats?

<!-- docs-version: 1.0 -->

## Type
question

## Severity
medium

## Layer
L6

## Status
open

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- S-079 (RV-16) chains each fighter's own actions: B prints 5 moves, ending at the 6.6 catch, against the 2.4 source's
  14 (grappled, pulled, hit by the kunai drive, crash, remain down)
- B's own S13 key names word B's side (rope_dart_wraps_shoulder, dragged_toward_pillar, kunai_in_shoulder,
  slammed_down, remains_down); A's follow the source's rows, which name B's move (B_throws_kunai); S-079 D1's 'no node
  words that side' was wrong for B
- renderers/anime_renderer.py `_laban` says it chains 'as the 2.4 source chains them'

## Description
Under O1 (keep LBN-2.4 unchanged), must a fighter's chain list its side of the other fighter's beats, as the source's
chains do, and from which words?

## Impact
B's chain stops before the climax that happens to B.

## Proposed Fix
The owner's answer; then a slice (a participant's phrase from its own key name or a new S04 field).

## Owner Ruling
needed

## Related
- F-091
- ADR-O1
- RV-16

## Resolution
Open.
