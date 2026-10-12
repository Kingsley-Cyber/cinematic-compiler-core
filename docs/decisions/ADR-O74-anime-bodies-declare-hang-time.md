# ADR-O74 — Anime bodies declare their hang time; other genres follow the arc

<!-- docs-version: 1.0 -->

## Status
proposed

## Date
2026-10-11

## Decided By
owner_default

## Scope
L4a

## Decision
Proposed by the agent during autopilot run 1 (S-018), for the owner to rule on:
1. An airborne span (keys with no support between a takeoff key and a landing key) follows one gravity arc through
   its takeoff and landing roots, each airborne root within 0.3 m of it (MOMENTUM_MISSING at S11), unless the span is
   a declared float.
2. In anime only, an airborne key may declare `float: true` in the kinematic plan (stylised hang time, as props may
   float, R-18); the prose says "hangs in the air (stylised, anime)" on those lines.
3. The examples' spans that leave the arc (F-069) are re-authored per span by the owner's choice: a declared float
   (anime) or new timing and heights on the arc.

## Context
Plan F9.2 refuses "an airborne span whose root rises or hangs against gravity without a declared float (anime) or a
push contact". A prototype (S-018) over the four examples: of nine airborne spans, the reference fight's six and the
wizard's three leave the arc through their own takeoff and landing; the bodies stay airborne far longer than their
heights allow (A from 1.10 to 3.00, B from 4.70 to 6.30; a ballistic arc over those spans would rise about 7 m and
3 m). No field declares a body float today, and which span is stylised hang time and which is mistimed is the
owner's choice of content.

## Consequences
- Accepting it adds one optional field (kinematic plan, logged) and lets M9-09b land with each listed span re-authored.
- Without floats, every anime aerial over about 0.9 s would need new timing or new heights.

## Alternatives Considered
- Refuse only a root that rises after takeoff without a launch (weaker: long hangs pass).
- Read every anime span as a float (the check would never fire on anime).

## Supersedes
—

## Superseded By
—

## Related
- F-069
- F-026
- ADR-O71
- PLAN-003
