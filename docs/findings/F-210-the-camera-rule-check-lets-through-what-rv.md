# F-210 — The camera rule check lets through what RV-60's word lists refused

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
high

## Layer
L5.5

## Status
open

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- backlog RV-85 (done) promises 'the word lists stay as a floor on the printed rules'; S-073 D3 says no prompt-level
  word list returns; the floor was never built
- S-081 (checked): rule_problems passes 'Cut to a close-up of the face at each contact.' (fast_move, close); the
  reviewers' probes pass 'Push in on the receiver as the kick connects.', 'Whip pan with the punch as it lands.', 'The
  action slows down as the kunai lands.', 'Slo-mo on every kick.'
- planner/camera_library.py HIT_WORDS holds blow, hit, impact, strike, struck (review 5's probe words); TERMS lacks
  'slow(s) down'; no subject or rig words are read

## Description
RV-85 replaced RV-60's word lists with a term check built from review 5's probes; it refuses those probes and lets
ordinary phrasings of the same rules through.

## Impact
A card rule can print a close-up or slow motion on a hit, which O92 forbids.

## Proposed Fix
Backlog RV-99: RV-60's word lists restored as a floor on the printed rules; a hit rule found from what a contact means
(the hits' kinds), not a noun list; subject and rig words read; the probes above as tests.

## Owner Ruling
none needed (O92)

## Related
- F-187
- F-160
- ADR-O92
- RV-99

## Resolution
Open.
