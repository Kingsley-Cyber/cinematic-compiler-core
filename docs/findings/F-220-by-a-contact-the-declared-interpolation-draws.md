# F-220 — By a contact the declared interpolation draws one body through the other, and B's crash through the floor

<!-- docs-version: 1.0 -->

## Type
question

## Severity
high

## Layer
L4c

## Status
open

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- S-087 (RV-59b): solver/reblock.py's clearance goal re-posed B's keys at the spans' ends, every support and contact
  part held at its start point, each angle within 45 degrees of its start and the root within 0.15 m: 3.4-3.7 and
  4.4-4.7 cleared (B's left arm at 3.7; B's root 1.1 cm and legs at 4.4); the six others did not (measured on S-087;
  the probe commands are in its record)
- 4.75 (0.102 m): A's left hand enters B's upper back 1/24 s after A's knee meets B's spine at 4.7; B's trunk is held
  at the knee and A's rows are the owner's, so only a 0.11 m gap at the knee would clear it
- 6.375 to 6.583 (up to 0.149 m): A's cartwheel elbow drives in toward B's chest; B's guard clears 6.375 and 6.5 only
  with its arms moved 45 degrees, and 6.583 stays (B's forearm in A's upper arm the frame before the catch)
- 6.625 to 7.42 (up to 0.112 m): B's hands hold A's arm at the 6.6 catch; then A is thrown past B, falls from the 7.0
  push-off and lands crouched at 7.5
- 8.17 to 8.71 (up to 0.065 m): the pull at 8.0, the kunai into B's shoulder at 8.5 (B's torso held at the blade) and
  the crash
- the wizard example's kick at 3.6 (0.111 m at 3.583, 0.098 m at 3.708): the acrobat's foot reaches the wizard's torso
  through it
- bigger re-poses broke a key instead (an overlap at the 8.5 key) or left misses
- S-089 (RV-59c): B's crash from 8.5 to 9.0 sinks the left sole 0.385 m under the floor at 8.75: the declared flip
  runs B's root angles straight while the root drops straight from 1.08 to 0.1 m (a slerp would still sink 0.209 m,
  and a 90-degree change must be declared); re-posing B's legs at 9.0 within 45 degrees (120 tried) leaves 0.217 m,
  and B's legs at 8.5, its feet held on the floor, 0.27 m: the fall needs a key mid-fall or a declared fall path

## Description
Keys 0.3 to 0.5 s apart hold a contact at its key; the interpolation from the key before draws the striking or
gripping limb through the target before it meets the surface, or the two bodies through each other after it. Animation
draws an approach and a recoil around a contact; the keys have neither.

## Impact
BODY_OVERLAP and FLOOR_PENETRATION cannot be refused between keys (RV-59e, RV-59c) while these spans pass through;
the render is told to slerp through them.

## Proposed Fix
Owner question, one of: (a) in-between keys: a declared pose of one entity between two of its keys (no beat, no
contact), checked like a key and printed in the prompt, placed by the re-block solver before and after a contact
(recommended: it adds and sets nothing aside; the prompts grow, and they are over the caps already, F-088); (b) a
contact's two bodies may overlap between keys within a stated number of frames of the contact (setting R-18 aside
there, as ADR-O104 does for a contact's interpolated point); (c) the contacts loosened inside O72's 0.15 m (the knee
0.11 m off the spine at 4.7); (d) A's source rows re-posed.

## Owner Ruling
Option (a) answered on the repo's side by ADR-O109 (owner_default, S-090: in-between keys, from the DAG's density
rules); options (b) and (d) stay the owner's, for whatever B's in-between keys cannot clear

## Related
- PLAN-007
- F-159
- F-089
- F-088
- ADR-O104
- RV-59b
- RV-59e
- RV-59c

## Resolution
Open.
Corrected in S-090 (principal review 7): the title said "no re-pose of a key clears it", which its evidence did not
show. (1) The probe commands are not in S-087's record: S-087's and S-089's probes ran in the scratchpad; S-090's
record lists the ones this finding rests on. (2) The 7.0-7.5 span (7.21 to 7.42, 0.112 m) involves no contact: A falls
from the pillar push-off past B's walk, both keys the repo's; B's 7.5 root moved 0.30 to 0.34 m in x clears it
(reviewers and builder). (3) B's crash clears with the committed solver once the hips' twist is freed within 120
degrees (deepest 0.141 m), at the cost of B's left foot 1.0 m up at 9.0; S-089's 0.217 m held the twist. (4) ADR-O104
exempts a contact's interpolated miss and says nothing of overlaps. (5) The 4.7 knee clears with a 0.11 m gap at the
knee, which O72 allows: option (c) is the run's to take, though it leaves the strike short. ADR-O109 answers option
(a) on the repo's side; RV-59f, RV-59e and RV-59c carry it.
