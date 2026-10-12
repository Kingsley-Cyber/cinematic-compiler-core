# S-054 — Principal review 3: five read-only reviewers, their gaps filed as F-152 to F-167

<!-- docs-version: 2.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
finish.md section 6 (a review after eight slices: RV-42, RV-43, RV-07, RV-49, RV-09, RV-10, RV-11, RV-12); findings
F-152 to F-167 (new)

## Layer
all

## Status
applied

## Commit
the commit whose message names [S-054]

## Plan
Run docs/prompts/principal_review.md with five fresh, read-only reviewers who did not build the work (layers S01-S09,
layers S10-S18, rules and shortcuts, decisions and findings, the golden and the fight); check their heaviest claims
against the files; file every gap as a finding with a slice, or as a question for the owner where its answer would set
aside an owner ruling (R-06); write the verdict (docs/reports/2026-10-12-principal-review-3.md); continue.

Predictions: none were written before the reviewers ran (the third session in a row without them, F-128, F-166); the
next code slice writes them first.

## Decisions
- D1 — The heaviest claims checked before filing: the anime card's "cut close" rule in every anime prose prompt; S06's
  "location ground" for the held kunai and rope dart; the sessions' Duration fields against the commit times; O23 and
  the source's 6.6 throw flash against the 6.8 release; O90's words against the dropped dart; the envelope's null
  validation fields; S10 reading a snapshot that includes the beat's own at-start effects. Each held. Level: covered
  (finish.md section 6).
- D2 — Three gaps go to the owner because their answers would set aside or reread an owner ruling (R-06): O72's measure
  (F-152), render.txt's deliverability under O1, O13 and O94 (F-153), owner_default ADRs as rulings (F-154); and two
  details of the owner's words (O90's timing in F-164, the pellet's point in F-165). Until the owner answers, the
  surface measure built in S-049 stays as the builder's interim, named in F-152 and in the run report's owner list.
  Level: covered (R-06).
- D3 — The others are filed with slices that need no ruling, and the order puts the records first (RV-45, RV-46), as
  three reviewers asked: the run kept F-128's pattern through eight pushed slices. Level: covered.
- D4 — F-144, F-084, F-083 and F-080 stay resolved for what their slices did; F-159, F-148, F-155, F-160 and F-129 carry
  what remains, and RV-46 rewrites their resolutions to say so. Level: covered.
- D5 — The rules reviewer's claim that ADR-O108 is missing from the run report's owner list does not hold (item 3 lists
  it); the generated owner lists do omit every owner_default ADR awaiting confirmation (F-154, RV-46). Level: covered.

## Self-audit
- Did a reviewer's claim go unfiled? Each gap in the five reports maps to a finding (F-152 to F-167), an existing
  finding (F-090, F-105, F-106, F-127, F-128, F-131, F-133, F-143, F-145, F-148, F-150), or the review report.
- Did the builder settle anything the owner should? No code or data changed in this session.
- The heaviest claims were re-measured or re-read, not trusted (D1).

## Duration
about 32 minutes (02:39 to 03:11 by the clock), most of it the reviewers' parallel runs

## Changes
- docs/reports/2026-10-12-principal-review-3.md (new); F-152 to F-167 (new); backlog 23 (RV-55 to RV-64; RV-27, RV-45,
  RV-46, RV-48 widened; RV-33 after RV-52; RV-45 next); PLAN-007; CHANGELOG; run report

## Verification
- before: S-053's gate at 515166a: `scripts/verify.sh` exit 0, 662 passed
- after: `scripts/verify.sh` exit 0, 662 passed, check: PASS (no code or data changed)

## Next
RV-45 (each slice's records: a self-audit section, interpretations labelled; F-053 and F-127 brought up to date).
