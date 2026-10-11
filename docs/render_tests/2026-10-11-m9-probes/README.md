# M9 probes (owner O46, 2026-10-11)

The owner's rule: test a change only if it is **uncertain** (the model might not respect it) **and visual** (it changes
what the render shows) and cannot be verified without a render; build everything else and move on. These six 5 s
prompts are the uncertain, visual parts of M9, written by hand in the wording the compiler will print once the
matching fix is built; a probe that passes fixes that wording as the target, a probe that fails changes the fix before
it is built. No fixed seed exists, so one render per probe; a borderline result gets one more. Renders go in
[the render log](../../render_log.md) bound to these sha256 values, the owner's verdict verbatim, frame notes apart.

| Probe | File | sha256 | Question | Scorecard (frames must show) | Fixes it informs |
|---|---|---|---|---|---|
| V1 | `V1_deflect_on_time.txt` | `8616c8a9dba4d8b621fc8011d9bb99a48c305a651d1a0ab520fb64a8e12a867c` | Do one time per hit, the sole-on-blade wording, a world contact point and a stated arc make the deflect land on time and the kunai reverse, fall and rest? | contact at 1.50 within 2 frames; sole visibly on the blade; kunai reverses, hits the ground near 1.80, then never moves; one kunai; both fighters in frame; no punch | F5.3, F5.1/F5.2, F4.1/F4.2, F2.1/F2.2 |
| V2 | `V2_substitution_hidden_log.txt` | `1af26b56bdcb3ebc6c1930284c796b17678988048211fce5a6e1810cd11a517b` | Does a prop stated as hidden stay hidden, and does a printed reason make the substitution read as caused? | no log before 2.50; smoke burst and log at 2.50; B's palm hits the log; A unseen 2.50-3.50, then behind B; B's charge plainly comes first | F6.1, CAUSE_REASON (M8.11), VANISHED_BODY (M8.12e) |
| V3 | `V3_backflip_one_rotation.txt` | `26439dd523a06553bf73c4eea4a90b78607581234b3db25913d20ff273fc7338` | With a realistic airtime and quarter-turn angles printed, does the model do exactly one flip about the lateral axis on time? | takeoff near 1.00 and landing near 1.80 (within 3 frames); exactly one rotation; inverted near 1.40; no twist | FR.1/FR.3 (axis tests AX2, AX3) |
| V4 | `V4_apex_hold.txt` | `2a012a574dda01689bf75682cbd250fb8ad3781254c45eef13c69836f34a674f` | Does 'freeze for exactly 3 frames (0.125 s)' give a short hold instead of a long hang? | the inverted hold lasts about 3 frames (no more than 0.2 s); then one rotation completes; landing near 1.93 | FR.6 (axis test AX4) |
| V5 | `V5_hit_held_both_bodies.txt` | `2a5006070e95e1d216b54fb8abf10700127ef974d0814a68fa097176d68d552c` | Will the camera hold a hit with both bodies in frame and then crane up, without cutting to a close-up? | both fighters in frame at 1.00; a short hold; no knee insert; the camera rises from about 1.10; no cut | C10, F8.1 |
| V6 | `V6_opening_from_above.txt` | `707dacf8a732e050cdc0816a78bed52a9bd7998259ffdf0dd8d8e9b9fae47c8e` | Does a framing on the pillar top keep A out of frame at 0.00 and bring A in from above? | A not visible at 0.00; A enters from the top edge near 0.20; feet land on the pillar top near 0.60 | O21 opening (finding F10) |

## Built without a render (certain, or not visual)

| Slice | Why no probe |
|---|---|
| F6.3 grounded pickups | removes a contradiction (picking things off the ground while airborne); certain |
| F2.2 pre/post samples, F6.2 rest persistence, F3.1 contact surface | carried inside V1's wording |
| F4.3/F4.4 B's active keys | choreography content; judged in the final full-fight render |
| F9.1 Laban direction, F9.2 momentum, FR.4 launch, FP.1 Bartenieff-to-pose, counts, limbs, rotation checks | compiler-internal checks, verified by tests |
| FR.7 genre cards, FR.2 limb paths, F4.5 chain timing, F4.6 callbacks (after Q-G) | data and checks; their wording rides in the final render |
| O19 D9 lines, C10 camera as a whole, part 3 words (curves, materials, line of action) | visual and uncertain, but only judgeable on the whole fight: the one full-fight render after the build |

Total: six 5 s probes now, one 10 s full-fight render at the end.

## Results (R11-R15, 2026-10-11; Claude's frame notes, owner verdicts in the render log)

| Probe | Render | Result | What the frames show |
|---|---|---|---|
| V1 deflect on time | R11 `…_12469_…` | FAIL | sole meets the kunai near 1.25 (6 frames early) and stays pressed against B's hand about 1 s; a kunai falls near 1.8-2.2 while B still holds another (two kunai) |
| V2 hidden log, substitution | R12 `…_03930_…` | FAIL on the question | the log stands as a post from 0.00; smoke near 1.5 (asked 2.50); B's palm splinters the log; the log falls near 4.0-4.5; A reappears near 4.5 in front of B |
| V3 one backflip | R13 `…_80206_…` | FAIL | two turns about the lateral axis (2.0-2.55, 2.55-3.1); launch 1 s late; landing near 3.1 (asked 1.80) |
| V4 apex hold | R14 `…_02134_…` | FAIL | the inverted pose freezes about 0.85 s (≈21 frames, asked 3); landing near 2.5 (asked 1.93) |
| V5 hit held with both bodies, crane | R15 `…_52436_…` | PASS | knee on B's lower back near 0.85; both bodies in frame (B's shoulder clipped at times); no knee close-up; brief pause on the hit; camera rises from about 2.0 to a high view; B stays down |
| V6 opening from above | — | not rendered | — |

What this settles (hypotheses, n = 1, no seed; they decide the printed wording, not the checks):
- **P1 Holds in frames are stretched:** every frame-count hold so far became 0.85-1.75 s (R10, R11, R14).
- **P2 Naming a hidden prop draws it:** "exists but is NOT visible before 2.50" put the log on screen from 0.00 (R12),
  as R1-R5 drew the log early.
- **P3 Words do not cap the rotation count:** quarter-turn angles and "exactly ONE" still gave two flips (R13; R8 and
  R6 also over-rotated).
- **P4 The camera wording works:** "hold with BOTH bodies in frame, no close-up, then crane up" rendered as written
  (R15). C10's wording can follow V5.
- **P5 A released prop needs an empty hand stated:** B was never told the hand is empty after the throw and held a
  second kunai (R11).

## Follow-up probes (one variable each where possible)

| Probe | File | sha256 | Changes from | Question |
|---|---|---|---|---|
| V1b | `V1b_deflect_empty_hand.txt` | `c1f85e4600998f2960db92c2a2dcae71b6bc20242de91289e66ea1e0dfd62654` | V1: the hold line removed, B's empty hand stated | one kunai, and a tap instead of a press? |
| V2b | `V2b_log_unmentioned.txt` | `c0b09df4c9ffd967ae3b81bcea5a74b97470e32ad7e82f2b291fc28412a386db` | V2: the log is not named anywhere before 2.50 | does silence keep it hidden? |
| V3b | `V3b_backflip_plain.txt` | `7c07df8f54b6b8f843ed40e4906bb3e17bc83721a1d3cf4abfbaaaca0effbe45` | V3: the angle list and turn speed removed | does a plain "one backflip" give one flip? |
