# Principal review 7 (2026-10-12): does the finished work match the plan?

<!-- docs-version: 1.0 -->

The seventh principal review (docs/prompts/finish.md section 6, after the finish run's sixth eight slices: RV-96,
RV-95, RV-100, RV-99, RV-59a, RV-59b, RV-59d, RV-59c). Five fresh, read-only reviewers who did not build the work each
took one scope and followed docs/prompts/principal_review.md and docs/prompts/no_shortcuts.md, each in its own
extracted copies of the commits (the worktree was not written). The builder checked their heaviest claims against the
files (session S-090) before filing them. The `soul_check_passes` condition of the owner's gate reads this report's
verdict.

## Verdict

**Partially.** All five reviewers say "partially"; the golden-and-fight reviewer says the golden is partially faithful
and partially coherent, and that the fight does not work, unchanged since review 6. No test tampering was found: the
rules reviewer re-ran all ten commit trees (each green at the count its record states, 711 to 731) and ran each new
test against its parent's code. But the run parked its own work behind a question the sources answer, filed negative
results it never recorded, closed F-210 on its probes for the fourth time, and loosened two of its own measures (a
landing excused as airborne; test slack).

| Scope | Verdict | Heaviest gap (finding) |
|---|---|---|
| Layers S01-S09 | partially | open supports are never measured between keys, 9 of 16 lift over 0.15 m (F-221); the wizard's landing became a 1.4 s braced descent its shots contradict (F-227) |
| Layers S10-S18 | partially | a landing between keys is excused as airborne (F-222); the camera floor misses the fight's own hits (F-210); a declared turn from a key at gimbal lock is drawn off its printed tip (F-225) |
| Rules and shortcuts | partially; no tampering | RV-59c parked on an unrecorded probe that froze the hips' twist (F-220); S-085 narrowed its own hit list (F-210); S-083's slack and post-solve bound (F-226); commit messages lost their fields |
| Decisions and findings | partially | F-220's option (a) adds and sets nothing aside, so it was the run's to answer (ADR-O109); "covered" on interpretations; F-210 closed on its probes again |
| The golden and the fight | faithful partially; coherent partially; fight works no | the second half unchanged; the pickups lean 74 degrees and their words contradict the legend (F-223, F-224); the 7.0-7.5 span is the repo's to fix |

## What matches the plan

- Review 6's queue was followed: RV-96, RV-95, RV-100 and RV-99, then RV-59 in four parts.
- Every commit tree is green at its stated count; every new test fails on its parent for the reason it claims (new
  capabilities by import); no test was deleted or skipped; KNOWN stays empty; the moved pins moved with typed data
  (DEV-32 to DEV-34).
- Re-blocks re-derive from recorded commands whose goals do not restate their outcome (RV-95, RV-59b).
- The between-keys measure reproduces byte for byte and by the reviewers' own code; the new caches change no number
  (with them stripped, 731 pass).
- Review 6's pickup regressions are closed: the knees off the floor, the hand no support, the crouch at A's own 0.57
  m.
- R-06 held: no owner ruling or source row was set aside.

## Checked by the builder (S-090)

- A's trunk (pelvis to chest) leans 74.0 degrees from vertical at 8.0 and 70.1 at 7.5, where the test's X sums read
  70.0 and 58.6; the 8.0 spine is [40, 70.375, 27.125].
- At 7.5 A's face heads -32.6 degrees and B's torso lies at +51.4 from A's head; A's right arm at 8.0 points 56.1
  degrees below horizontal and the left at 7.5 86.1, both worded "mid".
- B's 7.5 root moved 0.30 m in x removes the overlaps at 7.21-7.42; the post-catch frames 6.625-6.833 remain (0.095
  m).
- Re-run on an extracted e0ec6fe: 9 of 16 floor-support intervals lift their part over 0.15 m between keys (the vault
  hand 2.04 m, the kicking foot 1.48 m, A's right foot 0.93 m at 4.4-4.7).
- The wizard's acrobat at 5.6 has its soles 0.914 m up while c06 says "onto both feet".
- F-220 said the probe commands were in S-087's record; they were not.
- The landing moved to 5.3 with the key before unsupported reads 1.163 and 1.197 m, interpolated and airborne, and S13
  refuses nothing.
- B's crash clears with the committed solver once the hips' twist is free within 120 degrees: deepest 0.141 m at
  8.667, B's left foot 1.011 m up at 9.0.
- "Cut to a close-up as the knee connects." and "... as the elbow drives into the chest." pass the camera floor; "No
  playback ramps." and "Hits are holds, not inserts ..." are refused.
- A's right knee at 7.5 is 0.079628 m; the knee and head tests carry 1e-3 (the head's added in S-083).
- B at 4.4 clears A by 2.95 mm at 4.458, not the 0.3 mm S-087 recorded.
- The DAG's density lines exist as quoted (docs/sources/knowledge_dag_v1.md:253, 257, 259, 261).
- The commit messages from 76da0e5 on carry none of the Gap, Layer, Rules and Slice lines (four each before).
- The wizard's acrobat prints dab for 6.60-7.80 and float for 7.60-8.60.

## Filed

F-221 to F-229 (gaps), with slices RV-59g, RV-59h, RV-95b, RV-108, RV-107, RV-110 and RV-111. F-210 reopened, F-187
and F-160 open in part (RV-99b). F-220 corrected (its title, its evidence, ADR-O104's reach) and answered on the
repo's side by ADR-O109 (owner_default: in-between keys from the DAG's density rules), with RV-59f to build them;
RV-59e and RV-59c are ready again. Noted: F-053 (its late entries moved into its Description; S-084's, S-087's,
S-088's and S-089's interpretations added; S-080's superseded), F-089, F-134, F-206, F-207, F-215. Corrections were
appended to S-083, S-085, S-087, S-088 and S-089.

## The run's practice from S-091

- A negative result that blocks a slice or goes to the owner is recorded like a re-block: its commands, free set and
  bounds in the record, a test where it is cheap. A local search's failure proves no negative.
- A probe's bounds are the rulings' (the joint limits, O72), unless an interpretation stated in F-053 before the solve
  narrows them.
- A slice is done when its title is; one that delivers less is split before it closes, not retitled after.
- A question the sources answer is answered (finish.md section 4): an option that adds and sets nothing aside becomes
  an owner_default ADR that quotes its lines.
- "Covered" only where a ruling makes the choice; otherwise "interpretation", with an F-053 entry (R-32).
- Commit messages carry the Gap, Layer, Rules, Slice and Deviations lines (no_shortcuts.md).
- The staged hygiene scan runs before the gate, and any hit stops the commit.
- A test's tolerance is stated in the test and the record; none the data needs to pass.

## Questions only the owner can answer

ADR-O109 (in-between keys on the repo's side: confirm or strike). F-220 (b) and (d), for whatever B's in-between keys
cannot clear. F-215 (the floor's 0.15 m allowance; its evidence corrected: A's ankles sit 0.012 to 0.022 m over the
floor). F-111 (the frame limb words are read in; the pickup words depend on it, F-224). F-148 (the climax: A's right
hand 0.66, 0.70 and 0.87 m from the kunai at 8.5, 9.0 and 9.5). F-088 (the caps; in-between keys lengthen prompts
already over them). F-200 (typed deviations for the repo's own examples). F-202 Q1 (the volley passes 1.85 m from A at
its closest). Still open from before: F-205, F-211, F-196, F-197, F-152, F-153, F-154, F-164, F-165, F-059, F-143,
F-149, F-099, F-124, F-133, F-055, F-057, F-060.

## Next

RV-59h (a landing is never airborne), RV-99b (the camera floor's words), RV-95b (the pickups judged as drawn), RV-59f
(in-between keys, ADR-O109), RV-108 (a declared turn about its axis), RV-59e (BODY_OVERLAP between keys; B's 7.5 key
first), RV-59c (the floor; B's crash keyed mid-fall), RV-59g (open supports between keys), RV-107 (the wizard's
landing); then RV-97, RV-98, RV-101, RV-103a to RV-103c, RV-17 (F-134's live b11), RV-110, RV-111 and the backlog's
order.
