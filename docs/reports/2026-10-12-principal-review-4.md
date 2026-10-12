# Principal review 4 (2026-10-12): does the finished work match the plan?

<!-- docs-version: 1.0 -->

The fourth principal review (docs/prompts/finish.md section 6, after the finish run's third eight slices: RV-45, RV-46,
RV-48a, RV-48b, RV-60, RV-61, RV-62, RV-57). Five fresh, read-only reviewers who did not build the work each took one
scope and followed docs/prompts/principal_review.md and docs/prompts/no_shortcuts.md. The builder checked their
heaviest claims against the files (session S-063) before filing them. The `soul_check_passes` condition of the owner's
gate reads this report's verdict.

## Verdict

**Partially.** Four reviewers say "partially"; the golden-and-fight reviewer says the golden is partially faithful, not
coherent at 5.5-6.3, 8.5-10 and between keys, and that the fight does not work. No test tampering was found. Shortcuts
were found in this run's own slices: checks looser than their claims, and one exemption wider than its label.

| Scope | Verdict | Heaviest gap (finding) |
|---|---|---|
| Layers S01-S09 | partially | the substitution exempts any prop it changes, anywhere, at S04 and S07 (F-169); the rewritten S04 instructions teach F-077's jump (F-170); the S04 and S08 packets lack what their checks read (F-174) |
| Layers S10-S18 | partially | no prompt can become deliverable, whatever F-153's answer: thirty checklist rows have no way to pass (F-178); a hit is found by how a contact is written (F-175); the vanished body lives on in the guidance (F-176) |
| Rules and shortcuts | partially; shortcuts, no test tampering | the substitution's exemption (F-169); held props placed on the hand so the draw reads 0.00 m, and the recorded clearance was wrong (F-182); the records' guards check form (F-180); S-055 and S-056 committed before a gate ran after their last edit (F-181) |
| Decisions and findings | partially | the done-gate has conditions no slice reaches (F-179); "resolved" still means "the part this slice did" in five findings; F-165 missing from the owner lists; RV-33 and RV-27 marked ready though blocked |
| The golden and the fight | faithful partially; coherent no; fight works no | the volley never threatens A (F-102, F-059); the climax has no grip (F-148, F-089); the hit holds lose the bodies, one behind the pillar (F-090, F-184); bodies pass through each other between keys (F-159); takeoffs print a key late (F-183) |

## What matches the plan

- "Before a beat" has one reading now: S06's requirements, S09 and S10 use the same `value_at(..., before=beat)`
  (RV-61); RELEASE_AT_POSE puts the throw on B's 6.6 key as the source flashes it (RV-48a).
- Hits are defined once and judged at S16, the first step that sees contacts and shots, then at S17 and in the prompt
  (RV-57); the camera cards play at normal speed only (RV-60).
- Every test change in the eight slices is an added test, an import, a docstring, or a pin moved with its data and
  recorded; no skip, xfail or tolerance change. Every schema, card and kernel change was bumped and logged.
- The records are candid: corrected claims, held-in-part predictions and interpretations in F-053; no owner question was
  answered by the builder in these slices.

## Checked by the builder (S-063)

- The substitution: `_swapped` exempts any prop the substitution beat changes, at any place, and S07 exempts every prop
  change in a substitution beat (planner/dynamic_beat_validator.py, compiler/passes/mandatory/p07_contact.py).
- The instructions: beat_planning.txt says a resting prop moves on a contact at the second sample; the code refuses that
  move (its F-077 comment). The first-state example says "deployment hidden".
- The draw: B's hand is 0.108 m from the thigh's axis, 0.028 m from its surface, and its own 0.04 m radius overlaps the
  thigh by 0.012 m; S-061 had recorded 0.05 m, measured to the thigh's midpoint. Corrected in S-061 and F-053.
- A kunai another performer threw, landing in a body with no verb, is no hit under planner/hits.py.
- CAUSE_REASON passes "The weather is nice and B likes tea." for b01 to b02.
- The checklist marks unselected menus V4 and V5 NOT CHECKED, where ADR-O14 says menus count only where selected; no
  backlog item names V1 to V3, V7, V9 to V13, C8, C11, C18, C20, C22, T10 or STY.
- B's 4.70 line prints both feet and "rising 0.9 m"; its takeoff prints at 5.10.
- S-061's checklist moved C21's CONTACT_WORLD count from 15 to 17, which its self-audit did not say.
- R-28 says only the owner accepts a decision; the logs record `decided_by: owner` for map and card changes the builder
  designed.
- S-055's and S-056's trees (a14f99a, e0a04e7), exported and re-run: both pass the gate.

## Filed

F-169 to F-186 (docs/index/findings.md), each with a slice: RV-66 to RV-84 (RV-64 split into RV-64 and RV-64b, which
waits for F-133). Reopened in part, each naming its carrier: F-084, F-122, F-130, F-136, F-137, F-155, F-160, F-161,
F-162, F-163. F-001 and F-002 stay resolved for the golden; their checklist credit rests on RV-75. F-165 is now a
question; F-117 is high; RV-27 and RV-33 are blocked; RV-39 checks all six conditions. From S-063 a partly fixed
finding reads open with "Open in part" (F-166's own proposed fix; S-056 D2 is reversed and the choice is listed below).

## Questions only the owner can answer

1. **The decoy (F-169).** May a substitution move or change props other than the decoy that takes its actor's place,
   with no hand? RV-66 narrows the exemption to the decoy, the literal reading of O48.
2. **Hits (F-175, F-177).** Beyond a thrown or held blade landing in a body: do a blunt weapon, a grapple, a pin or a
   touch outside combat owe a camera hold, and in a scene of three or more, does the hold frame every body present?
   Is a smash cut, a whip onto the impact frame or a shaky handheld shot a camera hold?
3. **The deliverable (F-178, with F-153 and F-117).** Which checklist rows must pass for a prompt to be a deliverable,
   and which are N/A? How do F-013 and F-014 close without a fixed seed?
4. **O23 and O93.** Is O23's `at: start` literal, or any instant where the actor has a key (the UGC glasses' release at
   b03's end passes)? Did O93 mean B's grasp and throw on one instant at 6.6, as the source flashes it?
5. **The source and owner_default ADRs.** Does the source fight count as an owner ruling under R-06, given O105 and
   O108 reread its words? O103 sets aside two of O88's flips, which R-06 now leaves to you: confirm or strike it.
6. **The records.** Must a deviation's ruling be an owner ADR in force (F-180)? Do R-21's bans bind every genre? Should
   partly fixed findings be reopened (S-063) or kept resolved with a note (S-056 D2)? Does `decided_by: owner` mean
   you decided that change (R-28)? Will you run `make hooks` (F-168, F-181)?
7. **The camera (F-184).** Does a declared turn plane override the 180-degree side for its beat's shot?
8. Still open from earlier reviews: F-152, F-153, F-154, F-164, F-165, F-143, F-148, F-149, F-111, F-088, F-099, F-124,
   F-133, F-055, F-057, F-060; RV-20's layer-order ADR; M9-03a's constraint schema (O61).

## Next

The builder's own shortcuts and overclaims first: RV-66 (the decoy), RV-67 (the instructions), RV-68 (the draw
measured), RV-69 (a thrown blade is a hit), RV-70 (the vanished body everywhere), RV-71 (structured camera rules),
RV-72, RV-73, RV-74, RV-75, RV-76, RV-77. Then RV-58, RV-18, RV-64, RV-13; then the fight-breakers RV-15, RV-14, RV-16,
RV-37, RV-35, RV-59, RV-22; then RV-78 to RV-84 and the rest in backlog order. Every commit from S-064 runs through
`scripts/verify.sh > gate.log && git commit` (F-181).
