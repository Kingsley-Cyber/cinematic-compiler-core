# Principal review 2 (2026-10-12): does the finished work match the plan?

<!-- docs-version: 1.0 -->

The second principal review (docs/prompts/finish.md section 6, after the finish run's first eight slices). Five fresh,
read-only reviewers who did not build the work each took one scope and followed docs/prompts/principal_review.md and
docs/prompts/no_shortcuts.md. The builder checked their heaviest claims against the files (session S-045) before
filing them. The `soul_check_passes` condition of the owner's gate reads this report's verdict.

## Verdict

**Partially.** All five reviewers say "partially"; the golden-and-fight reviewer adds that `fight_works` does not hold
(0 of 20 prompts deliverable, none within the O97 caps).

| Scope | Verdict | Heaviest gap (finding) |
|---|---|---|
| Layers S01-S09 | partially | the declared `invariants`, `constraint` and `coherence` validators never run (F-142; F-019, F-020, F-093); the 37 reference rules reach no scene (F-133) |
| Layers S10-S18 | partially | S18 not built; no prompt deliverable or within the caps (RV-11, RV-13); the S13 author can list its own CONTACT_WORLD exceptions (F-123) |
| Rules and shortcuts | partially; some shortcuts | the run changed tests under its own answer to the owner's question (F-120, answered by the owner: ADR-O107) |
| Decisions and findings | partly honoured | owner_default ADRs taken before the owner saw them; stale records (F-121, F-130) |
| The golden and the fight | partially faithful; partially coherent; fight_works no | the Euler convention renders the source's leans as rolls and its backflip as a front flip (F-143); bodies pass through each other (F-144); fighters face away from their targets (F-145) |

## What matches the plan

- The skeleton: the step order, every pass's write scope, sealed authoring (packet hashes), the causal, state and contact
  checks, deterministic rebuilds (S01-S09).
- The authored steps S11-S17 bind their packets and refuse on any finding; CONTACT_WORLD is strict at exact instants and
  measures releases; world points come from forward kinematics on the genre's body; the rotation checks are real (S10-S18).
- No test was deleted, skipped or weakened to pass; every test change cites a ruling or a plan item (rules and shortcuts).
- The rulings the run built are in the code with tests: O84, O85, O86, O88 (19 of 21 limb flips and 13 head flips), O89 with
  O104, O90 (decisions and findings).
- The checklist is honest: NOT CHECKED blocks delivery and every prompt reads "no".

## Checked by the builder (S-045)

- The exception door is real: S13 passes the authored plan's `contact_world_exceptions` to `refusals`
  (compiler/passes/derived/p13_motion.py); the limit to the owner's source rows is a schema description only.
- The RULES lines "From t to the end" use the beat's end, in the renderer and its checker.
- S03 maps `scene_reference` items to no targets; S07 orders contacts by beat end, not by their instants.
- The prompt prints "2.50 post-contact ... moving down toward B" beside the rule "NOT toward B".
- Under ADR-Q6 the root [20, 90, 0] at 3.0 faces +X with its up axis tilted to (0, 0.94, 0.34), a sideways roll; at
  yaw -180, X from 0 toward -360 tips the up axis to (0, 0.81, -0.59) after a tenth, toward A's front: a front flip.
  Read as turn-then-lean (R = Ry Rx), the same rows lean forward and the flip goes backward.

## Filed

F-120 to F-150 (docs/index/findings.md), each with a slice or an owner question. F-120 and F-121 are answered by the
owner (ADR-O107, below). New backlog slices RV-42 to RV-51; RV-09, RV-15, RV-17, RV-18, RV-21, RV-24, RV-33, RV-35
and RV-36 widened.

## The owner's answer during the review

"O102 confirmed, keep pushing, continue the finish run" (ADR-O107): ADR-O102 is the owner's ruling; the finish run
pushes each slice and continues; rules 5.0 (R-03, R-06, R-30) and finish.md 2.0 record it, and R-06 now keeps any
question whose answer would set aside an owner ruling or an owner invariant for the owner.

## Questions only the owner can answer

1. **ADR-Q6 (F-143).** Q6 says "intrinsic XYZ" and "+X pitch forward, +Y yaw left". On a root turned about Y,
   intrinsic XYZ makes X a sideways roll, so the source's leaning rows tilt sideways and the 5.1 backflip turns as a front
   flip. Keep the label (and re-author those rows) or keep the meaning (X pitches the body forward at any heading,
   R = Ry Rx Rz)?
2. **The source's numbers against its own words (F-148).** The head inside the pillar at 1.1, 1.6 and 7.0; the 4.7 knee
   led by the foot; A facing away at 1.6, 2.0, 5.5-6.3 and 7.0; the 5.9 slide's soles 0.35-0.55 m up under "support=both
   feet"; "arm fwd high" on B's shoulder at 9.0. Bring the numbers to the words, as O18 did for the pickups, or keep
   them as recorded deviations?
3. **O95 against O88 (F-149).** O88's word flips made the action keys at 3.0 and 6.6 mirror-symmetric. Does "never
   mirrored" win there?
4. **ADR-O103 (F-129, F-111).** It keeps two of O88's 21 flips (A's 0.6 hips) to keep the feet on the pillar top, and every
   A head line reads "forward-high". Which frame are limb and head words read in?
5. **ADR-O104, O105, O106.** Confirm or strike (the builder's answers under finish.md section 4).
6. **F-088 (blocks RV-13b).** Which prompts carry the O97 caps, and what may a capped prompt drop, given
   no_render_compression? No prompt can become deliverable until this is answered.
7. **F-099 with F-125.** Does O80 let a vault turn over its planted hands, and how does A's 5.1 backflip, launched from the
   air, meet "grounded support in the prior beat"?
8. **The pre-commit hook.** `make hooks` in the worktree (it writes the shared repository config, O52).

## Next

The run continues with the slices that change what a rendered fight shows and need no ruling: RV-42 (the deflect's one
reading), RV-43 (exceptions from an owner-held list), RV-07 (the smoke at 3.7), RV-49 (no body through another), then
the rest in backlog order. The owner's answers to questions 1 to 4 unblock the source rows' re-authoring.
