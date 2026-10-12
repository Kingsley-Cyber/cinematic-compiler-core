# F-232 — In-between lines print raw angles inside a declared turn; an in-between may stand inside its body's vanish

<!-- docs-version: 1.0 -->

## Type
gap

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
- Principal review 8 (S-099, layers S10-S18): the fight's prose prints B@8.75's root as "EulerXYZ [-90, -45, -90]"
  inside B's 8.50-9.00 tip; the wizard example's prints the acrobat@3.55's as "[360, -365.597, 0]" inside "ONE spin ...
  2.60-3.60". ROTATION_ANGLES_PRINTED reads the staff rows only (validators/prompt_validator.py), and the in-between
  lines sit in [MOTION CONTROL] (S-097).
- Planted by the builder on 87804d2: an in-between of A at 4.0, inside A's 3.7-4.4 vanish, 1.5 m off its path:
  `p13_motion.check` returns []; INBETWEEN_SPAN does not read the packet's `vanished`. A planted B@5.3 at rot
  [0, 330, 0] inside B's declared spin from 5.1 to 5.5 (Y 270 to 90) also returns [] (the turn checks read keys only).

## Description
The staff rows print a turning root as mid-turn, so a renderer does not snap to an angle; the in-between lines print
the raw angles. An in-between is not checked against its own body's vanish window or its declared turn's direction.

## Impact
Two live prompts print an orientation the body passes through as if it were held; the vanish and turn holes are
latent (no example carries one).

## Proposed Fix
RV-59k: an in-between line inside its body's declared turn prints its root as mid-turn and ROTATION_ANGLES_PRINTED
reads the in-between lines. INBETWEEN_SPAN reading its entity's vanish window and the turn's one direction across
in-betweens wait (latent; ADR-O110).

## Owner Ruling
none needed

## Related
- ADR-O109
- ADR-O110
- F-230
- RV-59k

## Resolution
open
