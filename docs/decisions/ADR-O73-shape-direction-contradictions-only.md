# ADR-O73 — SHAPE_DIRECTION refuses only a Shape quality the motion contradicts

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-11

## Decided By
owner

## Scope
L5

## Decision
Owner, in chat, 2026-10-11: "ADR-O73: The check refuses contradictions only. Rewrite the 12 as recorded deviations.
Leave the 24 as-is until M9-10. Unblock M9-09a." The measure follows ADR-O76 (an airborne turn is not judged).

## Context
The agent's proposal the owner ruled on (S-012 to S-018):
Proposed by the agent during autopilot run 1 (S-017), for the owner to rule on:
1. SHAPE_DIRECTION (plan F9.1, owner O31) refuses an Effort interval whose declared Shape quality neither the root's
   path nor the body's form shows while one of them shows the opposite quality (rising against sinking, advancing
   against retreating, spreading against enclosing). An interval that shows neither (a still hold) keeps its
   declared quality as intent.
2. The twelve intervals that contradict their motion in the four examples (F-068) are re-authored to the quality the
   motion shows, as recorded deviations, in the slice that adds the check.
3. The measurement: the root path rises or falls over 0.1 m or travels over 0.1 m along the facing; the form changes
   the arms' elevation or the knees' fold by over 15 degrees, the chest's lean by over 10, or the arms' spread by
   over 0.15 (unit vectors), between the interval's first key and the key at its end.

O31 rules that Laban direction is checked "against both the root's path and the body's form change"; the plan (F9.1)
leaves the measure open. A prototype over the four examples (S-017): 24 of 42 intervals show neither reading of their
declared quality, and 12 show the opposite one. Any SHAPE_DIRECTION check therefore re-authors Effort intervals in
every example; no ruling covers those edits, and M9-10, M9-14b and M9-15d depend on M9-09a (ADR-O71 rule 3).

## Consequences
- Accepting it lets M9-09a land with twelve recorded S15 deviations; the strict reading (refuse "shows neither")
  would re-author 24.
- The measurement thresholds are Claude's; a flip's in-air lean (A at 5.10-5.90) reads as a form change, so some of
  the twelve may be the measure's, not the plan's.
- Until the owner rules, M9-09a is blocked, with M9-10, M9-14b and M9-15d behind it.

## Alternatives Considered
- Strict: refuse an interval whose quality neither reading shows (24 intervals re-authored).
- Advisory: print a mismatch as a finding without refusing (no check in the gate; R-19 cannot pass on it).
- Measure advancing and retreating toward and away from the opponent instead of along the facing (the plan's
  "target"; the single-performer UGC demo has none).

## Supersedes
—

## Superseded By
—

## Related
- F-068
- ADR-O31
- ADR-O71
- PLAN-003
