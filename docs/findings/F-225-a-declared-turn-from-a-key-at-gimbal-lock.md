# F-225 — A declared turn from a key at Y = +-90 degrees is drawn off the turn the prompt prints

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
medium

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
- Principal review 7 (S-090, layers S10-S18; the golden): B's 8.5 key ([0, -90, 0]) declares "flip" only because a
  change of 90 degrees on an axis must be declared (solver/euler_solver.py:10); the net rotation to 9.0 is a 90-degree
  tip about B's side axis (arc 90.0), which the prompt prints ("tips backward 90 degrees about the side-to-side axis",
  prose_mixed.txt:59).
- The straight Euler path the S13 edge declares (euler_axis) sweeps 116.4 degrees and strays up to 33.7 from that tip;
  B's sole sinks 0.385 m on it and 0.209 m on the tip (both measured by the builder on S-089).
- F-053 (S-011): "a flip or cartwheel's inversion is read on linear Euler interpolation between its keys", the repo's
  reading.

## Description
Straight Euler angles draw a turn about one axis only when the turn's change sits on one angle; from a key at gimbal
lock the three angles change together and the drawn path is not the declared turn.

## Impact
B's crash, and any declared turn from such a key, is drawn on a path the prompt does not describe.

## Proposed Fix
RV-108: a declared turn is drawn about its own axis by its net angle (whole turns kept), the rest slerped; F-053's
S-011 reading revised; the between-keys report re-measured, A's flips included.

## Owner Ruling
none needed (F-053's reading is the repo's)

## Related
- F-053
- F-220
- RV-59c
- RV-108

## Resolution
Open.
