# F-227 — The wizard example's landing beat (S-088) is a 1.4 s braced descent its shots do not show

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
medium

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
- Principal review 7 (S-090, layers S01-S09; the golden), re-run by the builder: b08 ("pushes off the cracked pillar
  and drops to both feet") keeps the torso on the pillar and the state "braced" until 6.6; the release and both
  landings fall at 6.6; the root drops 0.95 m at an even speed for 1.4 s (a free fall from the brace lands in about
  0.5 s).
- c06 (5.2-5.6) says "comes off the cracked pillar onto both feet" while the soles are 1.244 m up at 5.2 and 0.914 m
  at 5.6; c08 (from 6.4) says "Both feet drop to the stone".
- planner/prompts/beat_planning.txt (S04) does not say that a contact between keys is measured on the interpolated
  pose; RV-59d taught only euler_solving.txt (S13).
- S-088 D2 called the stretch "covered (O72)"; O72 is a tolerance and does not choose between stretching a beat and
  keying a landing (R-32: an interpretation).

## Description
S-088 moved the landing onto the next key by lengthening the beat, so the push-off happens at the beat's end and the
fall takes 1.4 s.

## Impact
The prompt lands the acrobat twice and slides it down the pillar.

## Proposed Fix
RV-107: the pillar released at the push-off (at: start), the landing keyed where the fall ends (an in-between key,
ADR-O109, or a beat), c06 and c08 re-authored, beat_planning.txt taught RV-59d's measure.

## Owner Ruling
none needed (the example is the repo's)

## Related
- RV-59d
- RV-107
- F-116
- ADR-O109

## Resolution
Open.
