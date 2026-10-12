# Principal review 3 (2026-10-12): does the finished work match the plan?

<!-- docs-version: 1.0 -->

The third principal review (docs/prompts/finish.md section 6, after the finish run's second eight slices: RV-42, RV-43,
RV-07, RV-49, RV-09, RV-10, RV-11, RV-12). Five fresh, read-only reviewers who did not build the work each took one
scope and followed docs/prompts/principal_review.md and docs/prompts/no_shortcuts.md. The builder checked their
heaviest claims against the files (session S-054) before filing them. The `soul_check_passes` condition of the owner's
gate reads this report's verdict.

## Verdict

**Partially.** All five reviewers say "partially"; the golden-and-fight reviewer adds that `fight_works` does not
hold, and the rules reviewer that shortcuts were found, none of them test tampering.

| Scope | Verdict | Heaviest gap (finding) |
|---|---|---|
| Layers S01-S09 | partially | the declared validators never run and the S04 packet carries no query, so a new query's choreography reaches no author (F-167, RV-18); RV-07 split "before a beat" between S06 and S10 (F-161) |
| Layers S10-S18 | partially | bodies pass through each other between keys (F-159); HIT_HOLD judges only the holds S17 placed (F-155); the kunai sits on the point CONTACT_WORLD measures, 0.21 m from B's shoulder, and A's "holding" hand is 0.66-0.87 m from it |
| Rules and shortcuts | partially; shortcuts, no test tampering | RV-49 changed O72's point measure to a surface gap without asking (F-152); the new checks are tight on the reference fight and looser for a new one (F-155, F-156, F-157); no self-audit recorded in eight pushed slices (F-166) |
| Decisions and findings | partially | render.txt cannot pass the Master Template rows, so no compile can emit (F-153); "resolved" has come to mean "the part this slice did" (F-166) |
| The golden and the fight | partially faithful; partially coherent; fight_works no | between-key overlaps, cameras aimed above the bodies (F-090), the empty grip at the climax (F-148); F-143, F-148 and F-145 still shape most of 1.6-2.5, 4.7-7.0 and 8.5-10 s |

## What matches the plan

- The skeleton holds: step order, write scope, sealed packets, deterministic rebuilds (S01-S09, S10-S18).
- The owner's rulings O91, O92, O93, O94, O96 and O107 are in the code with tests; A's source numbers were never
  touched (checked commit by commit); every test change cites a ruling or the plan's intent (ADR-O102), and every new
  check has a break that fires.
- The exception door is shut (RV-43); bodies have volume and overlap nowhere at the keys (RV-49); hits are static holds
  with both bodies named, no slow motion (RV-09); `cinematic compile` refuses a non-deliverable, exit 5 (RV-11).
- The records are candid about what each slice left (F-150, F-151, the slips in S-049 and S-050).

## Checked by the builder (S-054)

- Every anime prose prompt prints the anime card's "Cut close on the receiver after a blow lands." beside the hit holds
  (library/camera_conventions/anime.yaml).
- The kunai and the rope dart keep "location ground" in S06 from 3.0 and 4.0 to the end while A holds them, so RULES
  print "From 3.00 to the end, kunai keeps location ground" beside "From 8.00 to the end, kunai keeps holder A".
- The sessions' Duration fields (S-046 to S-053) add to about 7 h 25 min; their commits span 1 h 43 min.
- ADR-O23 puts throws and releases at their key pose; the source flashes the throw at 6.6; RV-10 released A at 6.8.
- ADR-O90's words put the rope dart on the ground at 3.7; the data drops it with an invented speed to land at 4.0.
- The envelope's validation fields (schema, invariants, layer_dependency) stay null; only camera_kinematic_coupling is
  written, as "pass".
- S10 reads a beat's snapshot as the state before it, and since RV-07 that snapshot includes the beat's own at-start
  effects.

## Filed

F-152 to F-167 (docs/index/findings.md), each with a slice or an owner question. New backlog slices RV-55 to RV-64
(RV-55, RV-56 and RV-63 wait for the owner); RV-27, RV-45, RV-46 and RV-48 widened; RV-33 now follows RV-52. F-144,
F-084, F-083 and F-080 stay resolved for what their slices did; F-159, F-148, F-155, F-160 and F-129 carry the rest,
and RV-46 corrects their texts.

## Questions only the owner can answer

1. **O72's measure (F-152).** O72 measures a contact from the limb's point to the target's point within 0.15 m; with
   bodies that have volume, no knee can rest on a back and be within 0.15 m of the torso point. Which measure (point to
   point with BODY_OVERLAP relaxed, the limb's point to the target's surface, or surface to surface as built since
   S-049) and which tolerance?
2. **render.txt and O94 (F-153).** LBN-2.4 stays unchanged (O1) and fails the Master Template's layout rows; compile
   refuses unless all five prompts are deliverables. Are its layout rows N/A, is deliverability judged on the union of
   the five fragments (O13), or must render.txt pass?
3. **Owner_default ADRs (F-154).** Does one count as a ruling for moving a test? Confirm or strike O103, O104, O105,
   O106 and O108.
4. **Three details.** O90: is the rope dart on the ground at 3.7 (your words) or does it fall from A's hand to land
   near 4.18 (F-164)? The pellet: does it burst at the source's p[0.4,1.1,4.7] or at A's hand (F-165)? The climax:
   keep the kunai's distance from A's hand as F-148's question, or re-block B to A's hand where it can reach?
5. Still open from reviews 1 and 2: F-143 (ADR-Q6's label or meaning), F-148, F-149, F-111 with O103, F-088 (the O97
   caps), F-099 with F-125, and F-055, F-057 and F-060; `make hooks`.

## Next

The run continues with its records first (RV-45: a self-audit section in every session, F-053 and F-127 brought up to
date; RV-46: the stale and overclaimed records corrected), then the contradictions that need no ruling (RV-48: the
throw on its pose and the S04 instructions; RV-60: the camera cards; RV-61; RV-62), the tightenings (RV-57: hits from
the contacts; RV-58), RV-18 and RV-64 (the validators run; the S04 packet carries the query), then RV-13 (O97's check)
and the rest in backlog order.
