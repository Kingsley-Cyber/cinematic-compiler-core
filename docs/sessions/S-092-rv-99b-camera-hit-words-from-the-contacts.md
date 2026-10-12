# S-092 — RV-99b: the camera floor finds a hit by what strikes, and reads a negation in every word

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-99b (PLAN-007); findings F-210 (reopened), F-187, F-160 (principal review 7); rulings O92 ("Camera hold
with both bodies in frame at 2.5, 4.7, 8.5. No playback ramps. Hits are holds, not inserts."), R-21

## Layer
L5.5

## Status
applied

## Commit
the commit whose message names [S-092]

## Plan
S-085's floor finds a hit by a word list built around review 6's probes: it misses the fight's own hits (the knee at
4.7, the elbow at 6.3, the palm, the kunai's drive at 8.5) and refuses O92's own sentences ("No playback ramps.";
"Hits are holds, not inserts"), since only the shaking words read a negation. The class: a check built from the
phrasings a reviewer tried rather than from what a hit is.
1. planner/camera_library.py: a rule speaks of a hit when its words name a contact (blow, hit, impact, strike,
   contact), a combat verb of library/combat_verbs.yaml (a throw aside: it lets go), an attack on a body (kick, punch,
   slash, stab, chop, jab, headbutt, uppercut), or a striking part or a blade meeting something (a knee, an elbow, a
   palm, a fist, a heel, a shin, a forearm, a shoulder, a head; a kunai, a blade, a knife, a sword, a dagger, a dart,
   a spear, a shuriken; followed within a few words by lands, connects, meets, drives, sinks, slams, smashes, rams,
   buries, plunges, pierces, embeds or into).
2. Every floor word and every term is read outside a negation: a match counts unless no, not, never, without, nor,
   avoid or "instead of" stands before it in its clause.
3. The floor's own lists follow the class: playback slowed by any fraction (half, quarter, a third), a camera that
   trembles or rattles, one body by "just" as by "only".
4. Tests: the fight's hits and new phrasings of the class refused; O92's three sentences pass as a hit rule's words;
   the library's cards still pass.

Predictions, made before the change (11:54 by the clock):
1. The gate passes before the change: 732 tests (1380170, S-091's chained gate).
2. The library's seventeen card rules still pass, the wizard's palm ward among them (no landing word near the palms).
3. Every phrasing review 7 found passing is refused, and so are phrasings of the class it did not try (a fist sinking
   into the gut, a heel slamming into the ribs, a blade burying itself in the shoulder).
4. O92's three sentences pass the floor as a hit rule's words.
5. About 735 tests.

## Decisions
- D1 — A rule speaks of a hit when its words name a contact noun, a combat verb of library/combat_verbs.yaml (a throw
  aside: it lets go, and planner/hits.py counts the thrown prop's touch, not the throw), an attack on a body, or a
  striking part or a blade followed within three words by a word of meeting or by "into" and a body part. Feet and
  shoulders are left out of the striking parts: "lands on both feet" is a landing, "over the shoulder into" a camera
  idiom. The lists are the repo's reading of planner/hits.py's kinds (F-053). Level: interpretation (F-053).
- D2 — A negation (no, not, never, without, nor, avoid, instead of) governs the rest of its clause, a clause ending at
  a comma, a stop, a colon, a semicolon or "but"; it applies to every floor word, every camera term and the hit
  words, so "No playback ramps." asks for no ramp and "Cut to a close-up on each hit, no shake." still asks for a
  close-up. Level: covered (O92's own words read as they are written).
- D3 — The floor follows the class: any slowed fraction (half, quarter, a third), a frame that trembles, rattles or
  quakes, one body by "just" as by "only". Level: covered (O92).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the staged scan, the gate and the commit |
| One gap, right layer | PASS | the camera library's card check (L5.5) |
| Predictions written first | PASS | the session file was written at 11:54, before any code |
| The class, not the probes | PASS | the hit finder is built from the combat verbs, the striking parts and the words of meeting; tests add phrasings no reviewer tried (a fist sinking, a heel slamming, a blade burying itself, a parry) and two that must pass (the palm ward, a flyer's landing) |
| Run against the owner's ruling | PASS | O92's three sentences pass as a hit rule's words (a test) |
| Neighbours | PASS | the camera terms read the same negation (F-187); camera_selection.txt names hits from the packet, not words (no change); knowledge map 26 |
| Tests changed with their data | PASS | two new tests in tests/test_camera_solver.py; the 35 there pass unchanged |
| Examples | PASS | none changed (the cards pass; `compiler.examples --check` clean) |
| Records | PASS | F-210, F-187, F-160 resolved again; F-053's S-085 entry superseded; map 26 (kernel log); backlog (RV-99b done, RV-95b next); PLAN-007; CHANGELOG; run report |
| Hygiene | see Verification | the staged scan runs first |

## Duration
from 11:54 (the plan) to 11:57 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- planner/camera_library.py (`hit_words`, `_forms`, `said`, NEGATION, CLAUSE; the floor's lists; `terms`)
- tests/test_camera_solver.py (two tests); kernel/knowledge_map.yaml 26
- F-210, F-187, F-160 resolved again; F-053; backlog; PLAN-007; CHANGELOG; run report

## Verification
- before: S-091's chained gate at 1380170: 732 passed
- Prediction 1 held. Prediction 2 held (every card rule passes, the palm ward among them). Prediction 3 held (review
  7's phrasings and the new ones refused). Prediction 4 held. Prediction 5 held in part (734: one under). Predictions
  4.5 of 5.
- the gate on this record (11:57:08): `scripts/verify.sh` exit 0, 734 passed in 73.15 s, docs plane: PASS, check:
  PASS
- the hygiene scan over the staged diff: 0 hits (run first in the chained commit)
