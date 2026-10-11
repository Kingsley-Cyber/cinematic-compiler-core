# Render log — owner results

The owner renders; Claude never does. Each entry binds a result to the exact prompt bytes (file at a commit, sha256)
and keeps the owner's verdict apart from Claude's frame notes (contact sheets at 2 fps, cuts by ffmpeg scene
detection > 0.3). n is per entry; no seeds were recorded, so nothing here is a controlled comparison yet.

| # | Date | Prompt | Model / settings | Output file | Owner verdict |
|---|---|---|---|---|---|
| R1 | 2026-10-11 | `examples/reference_fight/prose_mixed.txt` @ 2e08217, sha256 93d68469… | not stated (output 864x496, 24 fps, 10.08 s, with audio) | `R9rRYFe9JaUOvFF2P-SI6_video.mp4` | "hard to even tell whats happening" |
| R2 | 2026-10-11 | `examples/reference_fight/render.txt` (LBN-2.4) @ 2e08217, sha256 20051754… | not stated (same output format as R1) | `CuwwcRGpWmGqJSf7YaVQn_video.mp4` | "more cohesive story, the hits coulve been better same with the knife kick being a key fraame but the evade of the attacks and the rope swings and dance was legit" |
| R3 | 2026-10-11 | `examples/reference_fight/prose_pure_staff.txt` @ 2e08217, sha256 02d2d208… | not stated (same output format) | `1huuOJHSn0-UZ9zc_myu4_video.mp4` | "to many inchoherent scenes in this fight, and the rope was used in both hands but only 1 target. like in two directions like in 6-7sec" |
| R4 | 2026-10-11 | `examples/reference_fight/prose_euler_heavy.txt` @ e500831, sha256 c6b45bf5… | not stated (same output format) | `-rqKOdMfebgEVfQ-ZFO2h_video.mp4` | "he substituted but nothing warranted this , and the last attachment scene with ropes didnt make much sense, im starting to see a theme? is their a causal graph?" |
| R5 | 2026-10-11 | `examples/reference_fight/prose_upgraded_mixed.txt` @ e500831, sha256 6930500f… | not stated (same output format) | `fFaqcNFufnR0qg90a9q6h_video.mp4` | "the last render is about the same its more cohesive story, but the choreography sucks. upgraded." |
| R6 | 2026-10-11 | `docs/render_tests/2026-10-11-seedance-axis/P1_backflip_x.txt` (owner's axis test), sha256 a2376c7b… | Seedance 2.0 Mini (from the file name; the number in the name may be the seed, unconfirmed); 864x496, 24 fps, 5.09 s, with audio | `Ninja_jumping_backflip_67406_Seedance_20_Mini.mp4` | none given yet (the owner asked for the analysis) |
| R7 | 2026-10-11 | `docs/render_tests/2026-10-11-seedance-axis/P2_spin_y.txt` (owner's axis test), sha256 93de3165… | Seedance 2.0 Mini (from the file name; the number in the name may be the seed, unconfirmed); 864x496, 24 fps, 5.09 s, with audio | `Ninja_jumping_backflip_69995_Seedance_20_Mini.mp4` | none given yet (the owner asked for the analysis) |
| R8 | 2026-10-11 | `docs/render_tests/2026-10-11-seedance-axis/P3_cartwheel_z.txt` (owner's axis test), sha256 a26eff90… | Seedance 2.0 Mini (from the file name; the number in the name may be the seed, unconfirmed); 864x496, 24 fps, 5.09 s, with audio | `Ninja_jumping_backflip_25205_Seedance_20_Mini.mp4` | none given yet (the owner asked for the analysis) |
| R9 | 2026-10-11 | `docs/render_tests/2026-10-11-seedance-axis/P4_backflip_kick_x_limbs.txt` (owner's axis test), sha256 85765d34… | Seedance 2.0 Mini (from the file name; the number in the name may be the seed, unconfirmed); 864x496, 24 fps, 5.09 s, with audio | `Ninja_jumping_backflip_43260_Seedance_20_Mini.mp4` | none given yet (the owner asked for the analysis) |
| R10 | 2026-10-11 | `docs/render_tests/2026-10-11-seedance-axis/P5_money_shot_apex_hold.txt` (owner's axis test), sha256 3ae82770… | Seedance 2.0 Mini (from the file name; the number in the name may be the seed, unconfirmed); 864x496, 24 fps, 5.09 s, with audio | `Ninja_jumping_backflip_32293_Seedance_20_Mini.mp4` | none given yet (the owner asked for the analysis) |

## Claude's frame notes

**R1 (prose, Mixed mode).** 13 cuts; between 2.0 and 5.1 s about one every 0.3 s, several to prop or limb
close-ups. Readable: pillar and moon, A leaping off the pillar, kunai flight and deflect spark (as close-ups), B's
charge, smoke burst, B catching A (6.5), A on the pillar with the rope line (7.0–7.5), kunai drive flash (8.0), crash
and the end tableau (8.5–9.5: A crouched on B, rope in A's left hand, three shuriken in the pillar, log on the
ground). Lost: the log strike, knee from behind, backflip, slide and cartwheel elbow (about 3.7–6.3 s). The log lies on
the ground from 0.5 s; A starts standing on the pillar top instead of falling from above.

**R2 (LBN-2.4).** 2 cuts; one mostly continuous camera. Most beats read in order but about 0.5–1 s late (shuriken
volley at about 6.0 vs 5.5, slide about 6.5 vs 5.9, cartwheel about 7.0 vs 6.3); evades, rope swings and the
cartwheel read well (owner agrees). The foot deflect shows as a kunai-only close-up with sparks at about 2.0 (A's foot
not in frame); the kunai drive is not distinct. The log lies on the ground from about 1.5 s; A starts crouched on the
pillar top.

**R3 (prose, pure staff).** 4 hard cuts by detection, but many framing changes (close-ups of B at 3.0, 3.5 and 5.5;
inserts at 2.0 and 8.0). Better than R1: A falls from above the frame at 0.0; the palm on the log with smoke (3.5),
reappearance behind B (4.0), shuriken throw (5.5), handstand at the pillar base (6.0), B catching A (6.5) and the end
tableau read. The foot deflect became an insert of a hand driving a kunai into the ground with sparks (2.0). At about
7.5 A stands with both arms out, rope running from both hands in two directions while only B is the target. The prompt
asks airborne A, between 7.0 and 8.0, to snatch the rope dart with the left hand, throw it to wrap B, take the kunai
from the ground with the right hand and pull B toward the pillar (audit X2/X3: ground pickups while airborne), and its
rope-dart track says "8.00 p[0.4, 1.3, 4] held by A" with the dart on B: nothing says it is one line from A's left
hand to B.

**R4 (prose, Euler-heavy).** 2 hard cuts. The foot deflect reads at last (1.5–2.0: A's sole meets the kunai with
sparks, a close-up of foot and blade). A appears holding a kunai at 0.0 (the kunai is B's) and holds the rope dart in
both hands at 2.5. The smoke burst comes as B charges (3.0) but nothing on screen threatens A first; the substitution
looks unmotivated (owner). Knee impact (4.0), A going under and over B (4.5–5.0), shuriken passing over A (6.0), A
thrown into the pillar (6.5) read. At 7.5–8.0 A stands on the ground far from the pillar pulling the rope while B flies
sideways against the pillar: the pull has no visible purpose (owner: "didn't make much sense"). Kunai drive flash
(8.5) and the end tableau read.

**R5 (prose, Upgraded Mixed).** 1 hard cut; one continuous camera. The set drifts: a wooden deck and a gate-like
crossbeam replace the courtyard and its single pillar. The foot deflect reads (2.0, sole and blade). Readable: B's
charge (3.0), smoke at the log (4.0), A's kick landing on B with sparks (4.5), the shuriken throw over sliding A (6.0),
A on the pillar with the rope line to B (8.0), the end tableau. The middle (5.0-7.5) is a muddle of close-ups and
grappling at the pillar; the end appears to show four shuriken in the pillar (exactly three asked).

**The causal graph behind R1-R5.** The reference fight's 22 causal links are placeholders written when it was built
from the golden (2026-10-10, which has no causal graph): every reason reads "<beat> leads straight into the next
exchange"; 19 soft, 3 hard: a timeline, not causes. live_action_standoff's reasons are also placeholders ("The
stand-off answers itself"). And neither prompt prints the reasons: the prose CAUSAL LINKS line lists names and arrows
only, LBN-2.4 has no causal list. The conformance check passed because CAUSAL_LIST_MISSING only asks that each link
is listed, not that it gives a cause (the DAG's audit X40: temporal edges labelled causal).

**R6-R10 (the owner's Seedance axis tests).** Per-render notes, the scoring method and the prompts are in
[the suite's README](render_tests/2026-10-11-seedance-axis/README.md). In short: R6 backflip in the sagittal plane
(X) from a static side view, launch about 0.75 s late, landing about 0.5 s early, rotation count uncertain (the body
passes vertical about four times); R7 one spin about the vertical (Y) from a static front view, on a log instead of
flat ground, a cape appears; R8 a handstand-walkover into a one-hand cartwheel in the frontal plane (Z), then an unasked
aerial wheel, landing about 0.4 s late, framing not static; R9 backflip in the sagittal plane with one leg extended and
one bent, inverted hang about 1.2 s; R10 a 5.09 s clip for a 10 s prompt, the flip seen from the front three-quarter
(not the side), inverted about 1.75 s instead of 3 frames, no camera arc.

## What the renders suggest (hypotheses, not proven)

- H1 — Prose camera lines read as hard cuts. Both prompts carry the same 21-shot camera plan; the prose writes each
  shot as "cut to …" and the model cut 13 times, while LBN's terse `cam` rows produced 2 cuts.
- H2 — Strikes are planned as inserts. The 2.5 deflect, 4.7 knee and 8.5 kunai drive are each "smash cut to insert"
  on the striking limb, so the hit is shown without the target: the owner's "hits could've been better" and "knife
  kick as a key frame".
- H3 — Props listed from t = 0 are drawn from t = 0. Both prompts name the substitution log up front without saying
  it is hidden until 3.7.
- H4 — Two-handed airborne pickups split the rope (R3). The 7.0-8.0 window gives A's hands opposite jobs while
  airborne (rope to B, kunai from the ground), and a rope dart wrapped on B while "held by A" is never written as one
  line between them.
- R1 and R2 start A on the pillar top; R3 starts A falling from above the frame, as asked.
- H5 — No reasons reach the model (R4, and the theme across R1-R4). Substitution without a threat, a rope pull without
  a purpose, a log present before it is needed: the prompts say what happens, never why.

- AX1-AX6 (axis tests R6-R10): the axis and plane words were followed in all five; timing, rotation counts under a
  long airtime, the short inverted hold and the camera arc were not; the clip length is the platform's setting (see
  the suite README).

Next tests change one of these at a time, same model and seed.
