# F-129 — A's head words read forward-high on every line, also where the source says the head points down

<!-- docs-version: 1.0 -->

## Type
bug

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
- the second principal review, S-045 (docs/reports/2026-10-12-principal-review-2.md)
- examples/reference_fight/prose_mixed.txt: 18 of 18 A lines with a head word print "head forward-high", including 0.0, 0.6, 1.1, 8.5, 9.0 and 9.5 where the source's rows say the head faces or points down; the legend reads "high" as up
- solver/staff_geometry.py reads the head against the chest; F-080 was resolved by sign flips (S-038)

## Description
F-080's head part is not done: a sign flip cannot make a chest-relative word say down.

## Impact
The model reads a raised head where the source wants it lowered.

## Proposed Fix
With F-111 (the frame words are read in) and RV-36; F-080 reads resolved for its limbs only.

## Owner Ruling
with F-111

## Related
- PLAN-007
- F-080
- F-111
- ADR-O88
- ADR-O103

## Resolution
Open.
