# F-091 — render.txt's laban chains mix both fighters' moves

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
high

## Layer
L6

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
- examples/reference_fight/render.txt laban.A includes "throw kunai" (B's move); laban.B begins "fall from above>kick off pillar>throw kunai>foot deflect kunai>..." (A's moves)
- renderers/anime_renderer.py writes beat labels into each chain; the owner's 2.3 and 2.4 sources give each fighter his own chain

## Description
The LBN-2.4 laban field, the owner's own format, now tells the model each fighter does the other's moves.

## Impact
Identity of action blurs between A and B.

## Proposed Fix
Backlog RV-16: one chain per fighter from that fighter's own beats, as the 2.4 source writes it.

## Owner Ruling
none needed (ADR-O1)

## Related
- PLAN-007
- ADR-O1

## Resolution
Open in part, reopened by the sixth review (S-081): B's chain now stops at the 6.6 catch, 5 moves against the 2.4
source's 14; whether a chain carries a fighter's side of the other's beats is the owner's (F-211, O1). S-079 D1's 'no
node words that side' is wrong for B, whose own key names word it; `_laban`'s docstring overclaims 'as the 2.4 source
chains them'.
Resolved by RV-16 (S-079): renderers/anime_renderer.py chains, for each fighter, the beats it acts in, in time order,
then its own efforts, so A's chain in the reference fight lists its 18 moves (from 22) and B's its 5 (from 20, which
opened with A's fall); the wizard example's and the live-action example's chains shrink the same way, and the UGC's
one performer acts in all its beats. Only the laban field of render.txt changed. The 2.4 source's chains also name a
fighter's side of the other's beats ("caught by B", "pulled toward pillar"); the repo has no words for that side (its
key names follow the source's rows, which name the actor's move, "B_throws_kunai"), so the chain lists actions only
(F-053).
