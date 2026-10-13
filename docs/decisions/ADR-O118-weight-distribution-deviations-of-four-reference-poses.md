# ADR-O118 — Weight distribution deviations: four reference fight poses kept as the owner's

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-13

## Decided By
owner

## Scope
all

## Decision
Owner, in chat, 2026-10-13 (PLAN-009, answer 2): "Reference b07, b08, b11, b23: check the anime body model first. If
the model causes the 0.16-0.23m misses, fix the model. If the model is correct, record the four as deviations. Do not
touch the source without evidence."

The anime body model was checked first (S-128) and found correct: only its longer legs put the poses' soles on the
ground, and the spine leans forward as the source writes it. The source's legs set both feet, 0.2 m apart, beside the
body, so the centre of mass stands 0.16 to 0.23 m past the support base, over anime's 0.15 m allowance. The four poses
(the lean ninja at b07, b08, b11, b23) are recorded as owner-only deviations in kernel/weight_exceptions.yaml.

## Context
WEIGHT_DISTRIBUTION (PLAN-009 PM-2) refuses a pose S11 calls stable whose centre of mass stands past its support base
by more than the genre's allowance.

## Consequences
- kernel/weight_exceptions.yaml's four entries cite this ruling; an entry naming a pose that is no such miss is refused.
- The source poses are not changed.

## Alternatives Considered
- Re-posing the four at S13: the source is the owner's; no evidence that it is wrong.

## Supersedes
—

## Superseded By
—

## Related
- docs/plans/009-pose-mechanics.md
- docs/sessions/S-128-weight-distribution.md
