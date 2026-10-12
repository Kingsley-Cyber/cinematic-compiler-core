# Principal review 5 (2026-10-12): does the finished work match the plan?

<!-- docs-version: 1.0 -->

The fifth principal review (docs/prompts/finish.md section 6, after the finish run's fourth eight slices: RV-66,
RV-67, RV-68, RV-69, RV-70, RV-71a, RV-71b, RV-72). Five fresh, read-only reviewers who did not build the work each
took one scope and followed docs/prompts/principal_review.md and docs/prompts/no_shortcuts.md. The builder checked
their heaviest claims against the files (session S-072) before filing them. The `soul_check_passes` condition of the
owner's gate reads this report's verdict.

## Verdict

**Partially.** All five reviewers say "partially"; the golden-and-fight reviewer says the golden is partially faithful,
partially coherent (it fails at 5.5-5.9 and 8.5-10) and that the fight does not work. No test tampering was found: the
rules reviewer re-ran all eight commit trees (each green, at the counts the sessions state) and ran each new test
against its parent's code (each fails there). Shortcuts were found in this run's own slices, and one capability was
weakened.

| Scope | Verdict | Heaviest gap (finding) |
|---|---|---|
| Layers S01-S09 | partially | TELEPORT's exemption still reads any prop change (F-188); the decoy is guessed by distance and may come from nowhere (F-189); the vanished actor's own beat inside its window passes (F-172) |
| Layers S10-S18 | partially | the camera check reads the cards' labels, not the words the prompt prints (F-187); the hit's hold has no duration, a scale that disagrees with the card, and may frame a gone body (F-192); a vanish that never returns still brings the body back (F-193) |
| Rules and shortcuts | partially; shortcuts, no tampering | S-070's replacement is weaker than the word lists it removed (F-187; finish.md section 3, ADR-O102); records and predictions written ahead of their evidence (F-194) |
| Decisions and findings | partially | F-160 and F-177 resolved on a check that cannot see the printed words; review 4's owner questions missing from the owner pages; the backlog put the fight-breakers behind latent checks |
| The golden and the fight | faithful partially; coherent partially; fight works no | the volley never threatens A (F-102, F-059); the climax has no grip (F-148, F-089); the camera loses the action in render.txt (F-090); bodies overlap between keys (F-159); the rope reads taut where the source trails it (F-186) |

## What matches the plan

- The eight slices did what review 4 ordered: the decoy alone is swapped, the draw is measured at the pouch, a thrown
  blade is a hit, the vanished body is gone from the guidance, the hit's hold is still and names its bodies, the camera
  cards carry structured rules, and the hand roles read the holds.
- Every commit's tree is green; every new test fails on its parent's code; every removed test line is a fixture or a
  pinned value that moved with a recorded rule; every schema, card and kernel change was bumped and logged as agent_fix.
- B's re-posed arm at 5.1 is coherent against B's own body and against A (the golden reviewer's FK).

## Checked by the builder (S-072)

- `camera_library.rule_problems` passes "Cut close on the receiver after a blow lands." tagged fast_move with empty asks.
- `_teleports` exempts a substitution that changes any prop; `decoy()` is a separate, narrower rule.
- The prompts print "From 8.50 to the end, rope dart keeps line taut."; the source ends "line trailing to B right
  shoulder".
- The RULES' spatial-continuity line says the body "reappears at its next line" for every substitution.
- The records of S-065, S-066, S-067, S-070 and S-071 wrote their gate counts before the gate that produced them;
  S-066's predictions restate a probe's results.

## Filed

F-187 to F-195 (gaps), each with a slice: RV-85 to RV-93 and RV-82b (the turn-plane part of RV-82, which waits for the
owner). F-196 to F-203 file the owner's open questions as question findings, so the generated owner pages list them.
Reopened in part with carriers: F-130, F-160, F-173, F-177. Appended: F-090 (the opening shot), F-155 (its carriers),
F-169, F-171 (RV-74 now follows RV-54 and RV-22), F-172 (the actor's own beat), F-180, F-186 (the rope, the 5.50
throw printed as a strike, A's location through the vanish).

## The run's practice from S-073 (F-194)

- The gate runs first; its output is copied into the record; the chained `scripts/verify.sh > gate.log && git commit`
  then commits.
- A number found by a probe is reported as measured, never as a prediction.
- Each slice names the class of its finding and checks the neighbouring cases, and its self-audit checks that its
  step's instructions teach the change.
- Duration says where it ends; commit titles carry their rulings.

## Questions only the owner can answer

F-196 (the decoy: who declares it, where it stands, who may substitute), F-197 (hits and holds: what counts, how long,
how wide, which cuts hold, a card's words or its fields), F-198 (which checklist rows must pass for a deliverable),
F-199 (O23's key pose, O93's single instant), F-200 (the source, owner_default ADRs and decided_by as rulings), F-201
(R-21's reach beyond the fight), F-202 (the fight's staging: B's 5.5 position, the rope's end, the opening shot, a
turn plane), F-203 (RV-20's layer-order ADR). Still open from before: F-152, F-153, F-154, F-164, F-165, F-143, F-148,
F-149, F-111, F-088, F-099, F-124, F-133, F-055, F-057, F-060.

## Next

The builder's own shortcuts first, RV-85 (the camera words) and RV-86 (TELEPORT); then RV-13 (PROMPT_LENGTH, which O97
asked for "now"); then the fight-breakers RV-15, RV-14, RV-16, RV-35, RV-59, RV-37, RV-22; then RV-88, RV-89, RV-92,
RV-73, RV-87, RV-90, RV-91, RV-93, RV-75, RV-76, RV-77, RV-58, RV-18, RV-64 and the rest in backlog order.
