# Render log — owner results

The owner renders; Claude never does. Each entry binds a result to the exact prompt bytes (file at a commit, sha256)
and keeps the owner's verdict apart from Claude's frame notes (contact sheets at 2 fps, cuts by ffmpeg scene
detection > 0.3). n is per entry; no seeds were recorded, so nothing here is a controlled comparison yet.

| # | Date | Prompt | Model / settings | Output file | Owner verdict |
|---|---|---|---|---|---|
| R1 | 2026-10-11 | `examples/reference_fight/prose_mixed.txt` @ 2e08217, sha256 93d68469… | not stated (output 864x496, 24 fps, 10.08 s, with audio) | `R9rRYFe9JaUOvFF2P-SI6_video.mp4` | "hard to even tell whats happening" |
| R2 | 2026-10-11 | `examples/reference_fight/render.txt` (LBN-2.4) @ 2e08217, sha256 20051754… | not stated (same output format as R1) | `CuwwcRGpWmGqJSf7YaVQn_video.mp4` | "more cohesive story, the hits coulve been better same with the knife kick being a key fraame but the evade of the attacks and the rope swings and dance was legit" |
| R3 | 2026-10-11 | `examples/reference_fight/prose_pure_staff.txt` @ 2e08217, sha256 02d2d208… | not stated (same output format) | `1huuOJHSn0-UZ9zc_myu4_video.mp4` | "to many inchoherent scenes in this fight, and the rope was used in both hands but only 1 target. like in two directions like in 6-7sec" |

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

Next tests change one of these at a time, same model and seed.
