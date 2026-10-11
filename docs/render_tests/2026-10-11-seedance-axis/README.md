# Seedance axis tests (owner, 2026-10-11)

The owner's five test prompts check whether the video model turns a body on the axis the prompt names, in the repo's
frame (Y up, +Z forward, +X the performer's left; owner decision O32 (Q-L): flip about X, spin about Y, cartwheel about Z,
as MovementXML defines somersault and cartwheel). Prompts are saved verbatim, one file each; renders are logged in
[docs/render_log.md](../../render_log.md) as R6-R10, bound to these files' sha256. The owner renders; Claude reads frames.

| # | File | sha256 | Tests |
|---|---|---|---|
| P1 | `P1_backflip_x.txt` | `a2376c7b2fff5ef3288a331e3d2098e04dcb716995126aedbabe48a1b0c085f7` | flip about X, one full turn, landing at 3.0 |
| P2 | `P2_spin_y.txt` | `93de31654a8cead73fde846468aa7641faa2a3fa23f32db30209988b82765b68` | spin about Y, one full turn, landing at 3.0 facing the same way |
| P3 | `P3_cartwheel_z.txt` | `a26eff90ee7312cb69e898a935180255be3bd3cecbc0be036577624542062a77` | cartwheel about Z, left hand planted, one turn, landing at 3.0 |
| P4 | `P4_backflip_kick_x_limbs.txt` | `85765d344bcad6cec6c6af76e7151d9be3581b58bf89071bf3622b3f140e7406` | flip about X with a left-leg crescent and a right-leg tuck |
| P5 | `P5_money_shot_apex_hold.txt` | `3ae82770f4d2d64159db5d6d2eb5164ff59e358ef1a17d0de620575e3aeb4799` | flip about X, inversion at 1.5 held 3 frames at 0.25×, camera arc 180° |

## How each render is scored

Axis and plane (from the frames: sagittal turn seen from the side for a flip, the body turning front-back-front for a
spin, a wheel in the image plane seen from the front for a cartwheel) · number of rotations · the inverted frame ·
launch and landing times against the prompt · camera against the prompt · anything else that drifted. Frames are read
at 4 fps over the whole clip and at 12-24 fps over the airborne window (`ffmpeg -vf fps=…,tile=…`); hard cuts by scene
detection above 0.3.

## Results (Claude's frame notes; the owner's verdicts go in the render log)

All five renders are 5.088 s, 864×496, 24 fps, with audio and no hard cut; the file names say Seedance 2.0 Mini.

| Render | Axis / plane | Rotations | Launch → landing (asked) | Camera (asked) | Other |
|---|---|---|---|---|---|
| R6 P1 (`…_67406_…`) | backward tucked turn in the sagittal plane (X): as asked | at least one; the body passes vertical about four times (≈1.42, 1.79, 2.0, 2.29 s), so "single" is not confirmed | ≈1.25 → ≈2.5 (0.5 → 3.0) | static side view, as asked | turns to face the camera on landing |
| R7 P2 (`…_69995_…`) | spin about the vertical (Y): front → back (≈1.6-2.3) → front, as asked | one | ≈1.0 → ≈2.75 (0.5 → 3.0) | static front view, as asked | stands on a horizontal log, not flat ground; a cape appears mid-jump |
| R8 P3 (`…_25205_…`) | frontal-plane wheel (Z) in the hand-supported part: one hand down, legs split, ≈1.92-2.08 | two: a handstand-walkover into a one-hand cartwheel (≈1.4-2.25), then an unasked aerial wheel in the frontal plane (≈2.4-3.3) | ≈1.4 → ≈3.4 (0.5 → 3.0) | starts close and reframes wide (asked static front) | which hand plants is not readable |
| R9 P4 (`…_43260_…`) | backward turn in the sagittal plane (X), as asked | one, slow: inverted from ≈1.0 to ≈2.25 | ≈0.5 → ≈2.75 (? → 3.0) | static side view, as asked | one leg extended, one bent while inverted (left/right not readable); daylight forest (the prompt names no set) |
| R10 P5 (`…_32293_…`) | backward flip seen from the front three-quarter, face toward the camera | one | ≈0.75 → ≈3.5 (1.0 → 2.5) | follows and tilts with him; no side view, no 180° arc | clip is 5.09 s (asked 10 s); inverted ≈1.5-3.25 s, about 42 frames (asked 3 frames at 0.25×); lands in a four-point crouch |

## What the five suggest (hypotheses, n = 1 per prompt, seed not controlled)

- **AX1 Axis and plane words were followed** in all five: flips turned in the sagittal plane, the spin about the
  vertical, the cartwheel in the frontal plane. Naming the axis and the plane together reads.
- **AX2 Timing was not.** Launches came 0.25-0.75 s late (except P4) and landings 0.25-1.0 s off. P1-P3 asked for
  2.5 s in the air, an apex near 7.7 m under gravity; the model filled the time with late launches, long inverted
  hangs (P4, P5) or an extra rotation (P3).
- **AX3 "Single" did not hold under long airtime:** P3 turned twice; P1's count is uncertain.
- **AX4 "Time slows … held for 3 frames" became a 1.75 s inverted hang** (P5); P4 hung inverted about 1.2 s unasked.
- **AX5 Camera:** static side and front views held (P1, P2, P4); P3 reframed; "side view, arcs 180°" became a
  following front three-quarter view with no arc (P5).
- **AX6 Length is the platform's setting:** 10 s asked in P5, 5.09 s rendered, like the others.
- Set and costume drift freely (log, cape, daylight forest): the prompts carry no set or costume anchor.

## For the plan (deconfliction FR.1, FR.5, FR.6)

The derived rotation path should keep naming axis and plane (AX1), state launch and landing with a realistic airtime
and "exactly one rotation" (AX2, AX3), give a hold as frames and as seconds of screen time (AX4), and the camera arc
needs its own test wording (AX5). One variable at a time with a fixed seed: e.g. P1 again with launch 1.0 and landing
1.8 (timing only); P5 rescaled to 5 s (length only); P5's camera arc alone, worded as an orbit.
