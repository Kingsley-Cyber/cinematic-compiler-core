# F-221 — Open supports are not checked between keys: a supporting part lifts far off its surface before its release

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
- Principal review 7 (S-090, layers S01-S09), re-run by the builder: for each S07 support interval on a floor or a
  top, the part's height over the surface at every frame between keys (interpolation.frames,
  forward_kinematics.points): 9 of 16 floor intervals lift the part more than 0.15 m before its release. The wizard
  example's vault hand 2.04 m (1.2-1.6); the acrobat's kicking right foot 1.48 m (2.6-3.6) and its left foot 1.38 m
  (2.6-4.6); the fight's A right foot 0.93 m (4.4-4.7), A's feet 0.92 m at the slide (5.9-6.3, F-124) and 0.43 m
  before the leap (7.5-8.5). A's feet on the pillar's top fall up to 5 m below it (0.6-1.6).
- The cause: a release lands at its beat's end, and RELEASE_AT_POSE exempts a surface
  (planner/dynamic_beat_validator.py:249).
- docs/sources/knowledge_dag_v1.md:261: the interpolation is "slerp + respect support + Laban".
- RV-59 carried CONTACT_WORLD between keys at review 6; its split (RV-59a to RV-59e) kept a contact with no key at its
  instant (RV-59d) and no open support.

## Description
A support stays open from its onset to its release, but between keys the interpolated body leaves the surface long
before the release, so the prompt says a foot or a hand supports while the body is already in the air.

## Impact
Takeoffs print late: the kick stands on the kicking foot until impact, the vault never plants its hand, the climber's
feet stay on a pillar top they have left.

## Proposed Fix
RV-59g: CONTACT_WORLD measures each open support at every frame between keys (the DAG's 'respect support'), and S04
places a takeoff where the motion leaves its surface (a release before the beat's end, an in-between key where needed,
ADR-O109).

## Owner Ruling
none needed (O72; ADR-O109)

## Related
- F-089
- F-183
- F-124
- RV-59g
- ADR-O109

## Resolution
Open.
