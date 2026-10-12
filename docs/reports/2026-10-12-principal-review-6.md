# Principal review 6 (2026-10-12): does the finished work match the plan?

<!-- docs-version: 1.0 -->

The sixth principal review (docs/prompts/finish.md section 6, after the finish run's fifth eight slices: RV-85, RV-86,
RV-13, RV-15a, RV-15b, RV-14a, RV-16, RV-35a). Five fresh, read-only reviewers who did not build the work each took one
scope and followed docs/prompts/principal_review.md and docs/prompts/no_shortcuts.md. The builder checked their
heaviest claims against the files (session S-081) before filing them. The `soul_check_passes` condition of the owner's
gate reads this report's verdict.

## Verdict

**Partially.** All five reviewers say "partially"; the golden-and-fight reviewer says the golden is partially faithful
and partially coherent, and that the fight does not work, unchanged since review 5. No test tampering was found: the
rules reviewer re-ran all eight commit trees (each green at the count its record states) and ran each new test against
its parent's code (each fails there for the reason it claims). But the run's own slices again closed their probes and
not their classes, and S-080 regressed the pickups it set out to fix.

| Scope | Verdict | Heaviest gap (finding) |
|---|---|---|
| Layers S01-S09 | partially | S-080's pickup hands bear weight through a throw and a leap, and its case for the lower crouch compared unlike searches (F-206); TELEPORT inherits the decoy's distance guess (F-189); S07 depends on list order (F-134) |
| Layers S10-S18 | partially | static shots lose the hit holds' bodies between keys (F-208); a knee 0.109 m in the floor passes FLOOR_PENETRATION (F-206, F-215); the solver's joint order decides its answer (F-207); the camera words pass what RV-60 refused (F-210) |
| Rules and shortcuts | partially; no tampering | the solver's re-derivation claim is circular (F-207); example rewrites untyped under "Deviations: none" (F-212); thresholds set after the solve (F-206); a word list built from review 5's probes (F-210) |
| Decisions and findings | partially | F-090, F-110, F-187, F-160 and F-091 closed on the probe, not the class; VERTICAL_FRAMING refuses O21's opening (F-209); S-074 implemented an open owner question (F-196 Q5) |
| The golden and the fight | faithful partially; coherent partially; fight works no | the volley and the climax unchanged (F-102, F-148); bodies through each other and the floor between keys (F-159); the static holds watch empty air (F-208); repo-authored defects (F-216) |

## What matches the plan

- The queue review 5 set was followed: RV-85, RV-86, RV-13, RV-15a, RV-15b, RV-14a, RV-16, RV-35a.
- R-06 and O10 held where they bit: PROMPT_LENGTH refuses delivery, not conformance; RV-14b, RV-15c and F-205 wait for
  the owner rather than re-blocking source rows.
- Every commit tree is green at its stated count; every new test fails on its parent; no test was deleted, skipped or
  loosened; KNOWN stays empty; the moved pins moved with recorded data.
- Gains at the keys: every shot opens with its subjects in frame and the source's ground-level shots sit at 0.72 and
  0.19 m; B's lunge foot is planted; the pickups no longer crawl; the re-block solver is committed.

## Checked by the builder (S-081)

- c11 and c20, the static holds on the 4.7 knee and the 8.5 drive: at 5.1 A's head projects at y +2.59 and B's at
  +1.86; at 9.0 B's torso at -2.08 (the frame's edge is 1).
- A's right knee at 7.5 sits at y -0.109; FLOOR_PENETRATION's 0.15 m passes it.
- The solver, from the pre-S-080 8.0 key with S-080's goals: exact in the recorded joint order, 28.6 degrees off with the
  order reversed.
- At A's old 0.57 m crouch, with the spine twist free, the 7.5 reach meets the rope dart within 0.031 m at a 66-degree
  lean with both knees above the floor.
- `rule_problems` passes "Cut to a close-up of the face at each contact."; HIT_WORDS lacks kick, punch, lands, contact.
- render.txt's A rows at 7.5 and 8.0 print three supports (the slot's, "grounded" and the pinned words' "both feet").
- O21 rules that "A starts above the frame"; 12 of the 22 cameras stand at z > 6.

## Filed

F-206 to F-218 (gaps, and the questions F-211 and F-215), with slices RV-95 to RV-105, RV-103a to RV-103c, RV-14c and
RV-90b. Reopened in part with carriers: F-090 (RV-97, RV-98, RV-101), F-110 (RV-95), F-187 and F-160 (RV-99), F-091
(F-211); F-127's resolution corrected (RV-96). Noted: F-053, F-088, F-089, F-092, F-097, F-134, F-145, F-155, F-159,
F-172, F-188, F-189, F-194, F-195, F-196, F-197, F-200, F-202, F-205. RV-87 and RV-90b now wait for F-196 and F-197;
RV-14b and RV-15c were split so the repo's parts (RV-14c, RV-103b) are ready. Corrections were appended to S-078 and
S-080.

## The run's practice from S-082

- A re-block is a recorded command run from the pre-re-block key, with goals that do not restate its outcome, and a
  test re-derives it.
- A tolerance is stated with what it lets pass in the examples; one that passes the slice's own data change is a
  question for the owner, not a fix.
- Every example rewrite is typed in deviations.yaml and named in the commit; "Deviations: none" means none.
- A check that reads keys says so, and its class between keys has a carrier.
- A new check is run against the owner's rulings before it lands (O21).

## Questions only the owner can answer

F-148 (the climax: the words against A's arm numbers at 8.5-9.5), F-202 Q1 (the volley) and Q2 (the rope's end: the
FINAL text or the kernel 2.3 source), F-205 (the anime arm; evidence corrected), F-211 (each fighter's laban chain:
actions only or the source's reaction moves, O1), F-215 (the floor: points within 0.15 m, or surfaces), F-196 (the
decoy; S-074 implemented Q5's "yes", pending you), F-197 (a hit's hold: its scale, its length), F-088 (one cap or
both; what a BytePlus word is), F-200 (owner_default ADRs against F-053's interpretations; R-33's "and" or O102's
"or"), F-097 (the pillar's footprint; cameras behind it). F-202 Q3 is answered by O21. Still open from before: F-152,
F-153, F-154, F-164, F-165, F-059, F-143, F-149, F-111, F-099, F-124, F-133, F-055, F-057, F-060.

## Next

The builder's own regressions first: RV-96 (the solver reproducible), RV-95 (the pickups re-blocked with it), RV-100
(the rewrites typed), RV-99 (the camera words' floor); then the fight-breakers RV-59 (between keys, with the floor),
RV-97 (static framing over the window), RV-98 (O21's entrance), RV-101, RV-103a to RV-103c (the repo-authored defects),
RV-17 (pulled forward: one possession model, S07's order); then RV-104, RV-105, RV-14c, RV-37, RV-22, RV-102 and the
rest in backlog order (backlog 33).
