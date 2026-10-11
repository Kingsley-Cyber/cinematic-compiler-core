# F-065 — The smoke pellet rests in mid-air from 3.70 to the end

<!-- docs-version: 1.0 -->

## Type
contradiction

## Severity
low

## Layer
L1.1

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
—

## Evidence
- examples/reference_fight/plans/temporal.json: the smoke pellet's only sample, 3.7 p[0.4, 1.1, 4.7] v[0, 0, 0], with a
  touch by A's right hand at 3.7 and no possess; S06 keeps its location unknown and bursts its smoke at 4.0
- every reference-fight prose prompt (S-010): "WHERE: 0.00-3.70 carried by A · 3.70-10.00 at rest at [0.4, 1.1, 4.7]"

## Description
The pellet is touched, not held, at A's hand height and then rests there with no support while its smoke bursts at
4.00; R-18 holds props to gravity. The WHERE line (M9-04b) now prints this span until the end, where before the prompt
printed only the instant "3.70 p[0.4, 1.1, 4.7] at rest".

## Impact
The model is told a pellet hangs 1.1 m up for six seconds after it bursts.

## Proposed Fix
The owner picks: A holds the pellet (a possess at 3.7 and a release at 4.0, smashed at A's feet), or the pellet is
thrown down (a sample with v at 3.7 and a resting sample on the ground). Either re-authors S04 and its contacts (S07,
S08), so the autopilot leaves it (ADR-O71).

## Owner Ruling
none yet

## Related
- F-059
- F-064
- PLAN-003

## Resolution
Open.
