# F-222 — A landing between keys is excused as airborne

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
high

## Layer
L4c

## Status
open

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- Principal review 7 (S-090, layers S10-S18), re-run by the builder: with the wizard example's landing contacts
  (b08_c2, b08_c3) moved to 5.3 and the 5.2 key's support emptied, the rows read 1.163 and 1.197 m, interpolated and
  airborne, and S13 refuses nothing.
- solver/contact_world.py: between keys `airborne` reads the key before (S-088, F-053), and `artefact` has no distance
  limit.
- ADR-O104: "the actor is airborne or the prop is moving there"; O89: "Only exempt genuine airborne ... misses".

## Description
A support onset (a landing) ends a flight: at its own instant the actor is not airborne, yet S-088's rule marks it
airborne whenever the key before claims no support, so any landing between keys is excused, whatever its miss.

## Impact
A landing drawn 1.2 m off the ground passes S13.

## Proposed Fix
RV-59h: a support onset is never airborne at its own instant; an interpolated contact's exemption reads the support in
force just before it and holds for a touch or a hold, never a landing; a test pins both.

## Owner Ruling
none needed (ADR-O104, O89)

## Related
- F-053
- ADR-O104
- RV-59d
- RV-59h

## Resolution
Open.
