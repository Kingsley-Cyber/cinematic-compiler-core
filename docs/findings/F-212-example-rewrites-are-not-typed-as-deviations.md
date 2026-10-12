# F-212 — Example rewrites are not typed as deviations

<!-- docs-version: 1.0 -->

## Type
drift

## Severity
medium

## Layer
docs

## Status
resolved

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- S-076 re-authored sixteen shots, S-078 three keys (and the acrobat's words, 'shallow bend' to 'deep bend', which
  S-078's record cites as support without saying it made the change), S-080 two keys, four contacts and two supports;
  each commit says 'Deviations: none'
- examples/reference_fight/deviations.yaml is unchanged across the eight commits; DEV-09 still cites O18, O83, O89
  after S-080's re-block; R-33 says recorded 'in the golden test and the session file', ADR-O102 'in the golden test
  or the session file'
- R-19 (rules 7.1) defines a deliverable without O97's cap, which RV-13 added

## Description
Example data changed by the run's slices is recorded in the session files but not typed in the deviations registry,
and the rules disagree on whether it must be.

## Impact
The owner cannot see the golden's departures in one place.

## Proposed Fix
Backlog RV-100: type S-076's, S-078's and S-080's rewrites in deviations.yaml with their rulings, update DEV-09, R-19
cites O97 and PROMPT_LENGTH; commits name their deviations; R-33's 'and' against O102's 'or' goes to the owner
(F-200).

## Owner Ruling
none needed (R-33)

## Related
- F-180
- F-200
- RV-100
- RV-51

## Resolution
Resolved by RV-100 (S-084): the golden test records S-076's eleven re-authored shots (REAUTHORED_SHOTS, every changed
field) and S-078's lunge (B_LUNGE), each held to the plans by a test and typed in deviations.yaml (DEV-32, DEV-33);
DEV-09 and DEV-10 say what RV-95 did and cite O18, O72 and O11; the registry's header names what it still does not
record (RV-51). R-19 cites O97 and PROMPT_LENGTH (rules 7.2). The wizard, live-action and UGC examples have no source
to depart from; their rewrites stay in the session records. Commits name their deviations from S-083 on. Whether
R-33's 'and' or O102's 'or' binds is the owner's (F-200).
