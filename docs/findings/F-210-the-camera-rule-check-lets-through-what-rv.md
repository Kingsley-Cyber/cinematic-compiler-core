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
Resolved by RV-99 (S-085): rule_problems keeps RV-60's word lists as a floor under the fields (slowed playback
anywhere, including slows down, slo-mo and time slows; a close-up, tight shot, ECU, macro or insert on a hit), finds a
hit rule by what a contact does (a blow, hit, impact, strike, contact; strike, deflect, parry, catch; a kick, punch,
slash, stab, chop, jab or headbutt; between hits and a kick-off aside), and refuses a hit rule whose words frame one
body or shake the camera, reading a negation ('no shaky texture') as one. Every rule review 6 found passing is refused
(a test); the library's seventeen rules pass unchanged, so no card and no prompt changed. CAMERA_RULES keeps the
printed rules the card's word for word, so the floor reaches the prompt.
Reopened in S-090 (principal review 7): S-085's plan listed the hit words "kick, punch, knee, elbow, palm" and its
code dropped knee, elbow and palm without a reason; "Cut to a close-up as the knee connects." and "... as the elbow
drives into the chest." pass, while the fight's own hits are the palm at 3.4, the knee at 4.7, the elbow at 6.3 and
the drive at 8.5 (planner/hits.py). The floor also refuses O92's own words ("No playback ramps.", "Hits are holds, not
inserts"): a negation is read only for the shaking words. The proposed fix said "not a noun list". RV-99b carries it
(with F-187 and F-160).
