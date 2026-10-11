# M9 render plan (owner O45, superseded by O46 the same day)

**Superseded:** the owner's rule O46 (test only what is uncertain and visual) replaces the eight fight renders below
with six 5 s probes and one final full-fight render: [2026-10-11-m9-probes](2026-10-11-m9-probes/README.md).

At most eight renders of the reference fight, one after each slice below. Same model (Seedance 2.0 Mini), same seed,
same length (10 s, as R1-R5) and the same prompt file every time, so each render differs from the one before only by
the slices built in between. There is no baseline render: each render is judged against its own scorecard (what the
frames must show), not against R1-R5, which had no recorded seed. Slices that get no render of their own (verbs and
wording, the y=10 opening, B's active keys, money-shot frame parts, the Laban and momentum checks, genre cards) are
built and checked as usual; their effect shows, unisolated, in the next render. Each render is logged in
[the render log](../render_log.md), bound to the prompt's sha256, with the owner's verdict verbatim and Claude's frame
notes apart.

| Render | After | Scorecard: the frames must show |
|---|---|---|
| T1 | F5.3 strike timing | each hit lands at its pose time (deflect 2.5, knee 4.7, kunai drive 8.5) within 2 frames; the sole meets the blade at 2.5; no beat 0.5 s late |
| T2 | F6.3 grounded pickups | A lands beside the rope dart before taking it (7.5) and beside the kunai before taking it (8.0); one rope line from A's left hand to B, never pulled two ways |
| T3 | F2.1/F2.2, F6.1/F6.2 prop physics and visibility | the kunai flies in an arc and reverses at the deflect without skipping; it rests on the ground 3.4-8.0; the log is not seen before 3.7 |
| T4 | FR.1/FR.3 rotation path | the 5.1 backflip turns once about the lateral axis, inverted near 5.3; the 6.3 cartwheel turns once in the frontal plane; no extra rotation |
| T5 | F5.1/F5.2 world contact | the foot visibly strikes the kunai blade at the printed point; the knee meets B's back |
| T6 | O19 D9 lines (carries the verbs, the opening, B's keys, the money-shot frames) | the story still reads in order with the shorter prompt; A falls in from above the frame; B acts between hits |
| T7 | C10 camera | about 11 shots, hits held with both bodies in frame, no limb close-ups, height or depth changes at least every 2 s |
| T8 | part 3 words | weight and follow-through read: snaps on strikes, settles after, coat and scarf lag |

To fix before T1: which prompt file is rendered every time, and the seed.
