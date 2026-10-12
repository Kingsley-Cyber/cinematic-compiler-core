# F-233 — Two checks this run loosened: a standing body reads airborne between keys; a negation swallows a hit

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
high

## Layer
all

## Status
open

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- RV-59h (S-091): between keys `airborne` now reads only S07's support contacts (solver/contact_world.py `_rows`), and
  a body standing on the supports its keys claim (S11) has none: B's feet, the wizard's, both live-action bodies and
  the UGC creator. Planted by the builder: B's right hand touching A's torso at 8.25 is refused at 871d7ce (airborne
  False, 0.976 m) and excused at 87804d2 (airborne True, 1.112 m); the wizard touching the acrobat's torso at 4.0 is
  refused at 0.967 m and excused at 0.966 m.
- RV-99b (S-092): a negation governs the rest of its clause (planner/camera_library.py), so four rules refused at
  1380170 pass at 87804d2: "Push in to a close-up without delay as the blow lands.", "Cut close with no warning on each
  impact.", "Cut without hesitation to slow motion as the knee lands.", "Hold medium on both without a cut and let the
  frame shake on impact.". On both trees "Cut to a close-up as the foot slams into the chest." passes; the wizard
  example's own hit is the acrobat's foot (b05_c2), and the striking parts leave the feet out.

## Description
Each slice closed its own case and widened the class: RV-59h fixed a landing read as airborne and made every
S11-supported body airborne between keys; RV-99b let O92's own sentences pass and let any hit rule with a negation in
its clause pass.

## Impact
No example's prompt changes, but CONTACT_WORLD excuses any between-keys miss by a standing body, and the camera floor
lets a close-up, slow motion or a shaking frame on a hit through, against ADR-O104 and O92.

## Proposed Fix
RV-59l: between keys an actor is airborne only when the key before claims no support (S11) and no S07 support is
open, never at a landing (RV-59h's rule kept). RV-99c: a negation governs only the phrase it heads, so the four
refusals return while O92's own sentences pass; the striking parts include the feet. F-210 is reopened: its fix ("not
a noun list") is still undelivered.

## Owner Ruling
ADR-O104, O92

## Related
- F-210
- F-222
- ADR-O104
- RV-59h
- RV-99b
- RV-59l
- RV-99c

## Resolution
open
