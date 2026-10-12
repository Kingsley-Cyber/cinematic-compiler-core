# F-189 — The decoy is guessed by distance and may come from nowhere

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
high

## Layer
L1.1

## Status
open

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the fifth principal review, S-072 (docs/reports/2026-10-12-principal-review-5.md)
- `decoy()` takes the nearest changed prop within 0.15 m of the actor's pelvis anchor: a trivial effect ("kunai location ground", already true) makes a kunai placed there the decoy; a crouched swap or a decoy lying on the ground is refused
- library/archetypes/ninja_lean.yaml lists the log in its equipment, so the log is carried by A (planner/query_expander.py) and PROP_FIRST_STATE excuses its first place; the log card still offers `hidden`; a plan whose log first appears at the swap passes S04 to S07, against O48's post standing from 0.00
- capabilities reach the S04 packet but no code reads them: an entity whose card lacks `substitution` may substitute

## Description
The decoy is inferred from geometry, not read from what declares it (the archetype's invariant, the card's deploy affordance), and nothing makes it stand in the scene before the swap.

## Impact
The kawarimi is governed by a distance tuned to the golden.

## Proposed Fix
Backlog RV-87: the substitution's decoy is declared (the archetype's invariant names it), stands in the scene from the first beat, and is measured where the actor stood; a substitution needs the capability.

## Owner Ruling
who declares the decoy and whether every decoy stands from the first frame (listed, F-196)

## Related
- RV-87
- F-169
- ADR-O48
- ADR-O12

## Resolution
Open.
