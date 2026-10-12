# Principal review 8 (2026-10-12): does the finished work match the plan?

<!-- docs-version: 1.0 -->

The eighth principal review (docs/prompts/finish.md section 6, after the finish run's seventh eight slices: RV-59h,
RV-99b, RV-95b, RV-59f, RV-59i, RV-108, RV-59e, RV-59c). Five fresh, read-only reviewers who did not build the work each
took one scope (layers S01-S09, layers S10-S18, rules and shortcuts, decisions and findings, the golden and the fight)
and followed docs/prompts/principal_review.md and docs/prompts/no_shortcuts.md, each in its own extracted copies of the
commits (the worktree was not written). The builder checked their heaviest claims in its own extracted trees (session
S-099) before filing them. While it checked, the owner narrowed the run to significant work (ADR-O110), so this review
files only what changes what a prompt tells the renderer, or a check the run loosened; the rest is listed below and
waits.

## Verdict
**Partially.** All five reviewers say so; none found test tampering (no test deleted, skipped or xfailed; every commit
tree passes at the count its record states: 731, 732, 734, 734, 743, 745, 746, 749, 750). The in-between keys did what
ADR-O109 promised for overlaps: no body passes through another between keys, and nothing was placed on A's rows. But
they were not checked like keys: nothing held B's feet, so B now floats in a span every layer calls grounded, and the
crash's in-between used the 0.15 m allowance meant for the owner's rows. Two of the run's slices fixed their own case
and widened the class (RV-59h, RV-99b). And every prose prompt's legend still parents the legs on the root, against
the owner's ADR-O84.

## Checked by the builder (S-099)
Each claim below was re-run by the builder on trees extracted with `git archive`.
- **B floats** (four reviewers): B@6.45 soles 0.338 and 0.220 m up; B@6.7 0.463 and 0.498 m, the trunk 55.0 degrees
  off vertical; 16 frames from 6.3 to 7.5 with both soles over 0.05 m, none with the keys alone. The acrobat@3.55's
  right sole is 1.444 m up inside S07's open support. Held.
- **B's crash sinks 0.140 m** at 8.625 (the records say "over the floor"); with no allowance the same five commands each
  miss 0.0 and B's lowest point is 0.009 m over the floor. Held.
- **RV-59h loosened CONTACT_WORLD**: a planted touch of B's right hand on A's torso at 8.25 is refused at 871d7ce
  (0.976 m) and excused at 87804d2 (1.112 m, airborne); the wizard's at 4.0 likewise. Held.
- **RV-99b widened the camera floor**: four rules refused at 1380170 pass at 87804d2 (F-233); the foot phrasings pass on
  both. Held.
- **In-between holes**: an in-between of A inside A's vanish and one of B turning against B's declared spin each pass
  S13. Held (latent).
- **RV-108 redrew A's three spins** (1.6-2.0, 4.7-5.1, 5.9-6.3) by 5.2, 2.1 and 12.6 degrees (0.104, 0.043 and 0.212 m),
  where S-096 said they draw the same path. Held.
- **The pickups' negative** (S-093, F-223): with the lean bound weighted, the committed solver reaches 69.90 and 69.86
  degrees from A's own 0.57 m, every other bound met at 8.0 and all but the ankles (as committed) at 7.5. Held: the
  negative was wrong.
- **B's root pops** 9.68 m/s from 8.45 to 8.5 (3.27 before). Held.
- **"A lands squared up facing B"**: A's hips and shoulders face B exactly at 3.0, 3.2 and 3.4. Not reproduced; not
  filed.

## Filed (built next, ADR-O110)
- F-230 (high): B's in-between keys lift it off the ground, sink its crash and name motions they do not make. RV-59j.
- F-231 (high): every prompt's legend hangs the legs from the root; the poses hang them from the spine (ADR-O84). RV-113.
- F-232 (medium): in-between lines print raw angles inside a declared turn. RV-59k (its latent vanish and turn holes
  wait).
- F-233 (high): two checks this run loosened (RV-59h's airborne, RV-99b's negation). RV-59l and RV-99c; F-210 reopened.

## Listed, not filed (they wait, ADR-O110)
- ADR-O109's text against what was built: the re-pose-first precondition was never shown at the joint limits; its
  Alternatives rank loosened contacts after in-betweens, its Decision before them; three in-betweens sit 0.05 s from a
  key, denser than the DAG's densest tier.
- Slices closed short of their titles: RV-59e (B's 7.5 root re-block dropped), RV-99b (hit words from the scene's
  contacts), RV-108 (F-225's "whole turns kept, the rest slerped": four turns of a half turn or more still run every
  angle straight), RV-95b (retitled in its closing commit), RV-59b (narrowed).
- F-223 is a gap, not an owner question (above); F-053 lacks S-095 D2 and S-097 D2 and D4, and its pickup entry says
  80 degrees; S-098 D1 says "covered (O72)" where F-215 is open.
- Two assertions S-097 loosened in tests/test_inbetweens.py (an exact list made a membership; "no other edge carries
  in-betweens" dropped); S-096's unneeded 1e-3 degree tolerance.
- Stale text: knowledge_map.yaml's "[IN-BETWEEN KEYS] block" and "on a frame of its own"; the between-keys report's
  "a declared turn's angles straight"; F-220's "Open."; beat_planning.txt's "at a shared key"; F-229's layer.
- RV-17's planned order refuses the golden's catch-and-throw at 6.6 while F-199 Q2 is open; RV-59g as titled misses
  supports only S06 states (B to 5.1, the acrobat 1.6-2.0), and S04 can time a takeoff only at a beat's start or end.
- The hygiene scan lives only in the builder's procedure, not as a script; every commit's author address is a local
  machine address, which no diff scan sees.

## Questions only the owner can answer
- ADR-O109 (owner_default): confirm or strike, knowing F-230.
- F-088: the in-betweens add 1.1 to 3 KB to prompts already over the caps.
- F-143: should A's turned-lean spins be slerped between keys (RV-108 now draws them so)?
- The commit author address: keep it, or set a no-reply address for future commits (history is not rewritten).

## Next
RV-113, RV-59j, RV-59k, RV-59l and RV-99c (ADR-O110); then the owner renders the prompts and judges them.
