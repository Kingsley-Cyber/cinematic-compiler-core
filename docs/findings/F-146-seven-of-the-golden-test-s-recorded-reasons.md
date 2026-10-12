# F-146 — Seven of the golden test's recorded reasons contradict the data

<!-- docs-version: 1.0 -->

## Type
contradiction

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
- the DEFLECT_PAIR comment: "toward B, as the source's rule says" (the rule says NOT toward B; F-122)
- ROOT_TURNS: "pitches A backward through 360" (a front flip under ADR-Q6; F-143)
- REBLOCKED_SAMPLES' comment: the dart "wrapped on B since 7.6" (it wraps at 8.0); k_rules_18 keeps "A pulled toward B" while A stays crouched and moves 0.30 m
- PULL_ANCHOR's comment and test: the rope "pulls toward the pillar" and "both point to +z", tested on pelvis z only; the rope from the dart to A's hand gains 0.08 m of z over 1.74 m, 44.6 degrees off the pillar
- PELLET's comment: 4.0 is "the source's burst time" (the source bursts at 3.7; F-082)
- SUBSTITUTION_POST's comment: the log is deployed "at the substitution" (it is deployed at 4.0)
- DEFLECT_PAIR pins a kunai falling into the foot (it peaks at 1.93 m at 2.10 s); the deflect changes its vertical speed by 0.04 m/s, against "throws upward ... arrives from below ... DEFLECTED DOWNWARD"

## Description
Records that explain the golden's deviations say things the data do not show.

## Impact
A reader trusts reasons that are false.

## Proposed Fix
Backlog RV-50: each reason corrected, or the data brought to it (the rope's pull measured along the line itself; the wrap at 7.6; the log and the smoke at 3.7 with RV-07; the deflect's kick).

## Owner Ruling
none needed

## Related
- PLAN-007
- F-122
- F-143
- F-082

## Resolution
Open. RV-07 (S-048) corrected PELLET's and SUBSTITUTION_POST's comments with the data (the smoke and the log at
3.7); the rest waits for RV-50.
