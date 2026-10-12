# PLAN-007 — The principal review of 2026-10-11: every gap named, the owner's rulings, the gate

<!-- docs-version: 1.0 -->

## Status
in progress

## Owner
Kingsley (owner); Claude executes

## Created
2026-10-11

## Updated
2026-10-12

## Intent
Close what the first principal review (docs/prompts/principal_review.md, S-035) found, under the no-shortcuts principle
(docs/prompts/no_shortcuts.md) and the anti-reward-hacking clause (AGENTS.md section 18): each gap is fixed at its cause,
named here with a slice, or asked of the owner. The review's verdict: the work matches the plan only partially. The
skeleton is real (layer order, write scopes, sealed authoring, hash logs, recorded rulings), but no prompt is a
deliverable, prompt checks never run at compile, and recent checks passed by exemptions and re-blocks that broke the
moves they measured, several of them the builder's own (F-074 to F-077). The gate is the owner's six conditions (ADR-O98,
CLAUDE.md).

## The owner's rulings (2026-10-11)

| Ruling | In short | Slice |
|---|---|---|
| ADR-O88 | A's limb and head words follow the source's words; each flip a recorded deviation | RV-05 |
| ADR-O89 | An exact-instant miss is not an artefact; re-block B's throw, the palm on the log, the vault hand | RV-02a, RV-02b |
| ADR-O90 | A's supports and holds end at 3.7; the rope dart rests on the ground until 7.5 | RV-06 |
| ADR-O91 | The smoke bursts at 3.7 at A's body; the spent pellet falls and rests | RV-07 |
| ADR-O92 | Hits are camera holds framing both bodies; no playback ramps; no inserts | RV-09 |
| ADR-O93 | The kunai drive holds the kunai in B's shoulder; the catch is a grasp plus a throw | RV-10 |
| ADR-O94 | DAG-excluded rows are N/A; `cinematic compile` refuses a non-deliverable prompt | RV-11 |
| ADR-O95 | "Never mirrored" binds strikes and action beats, not idle guards; no veto of S-034's choices | AS-04 |
| ADR-O96 | The 6.3 cartwheel is a full turn | RV-12 |
| ADR-O97 | Prompts capped at 3,500 characters (Runway) and 1,000 words (BytePlus) | RV-13, RV-13b |
| ADR-O98 | The gate's six conditions | RV-39 |
| ADR-O99 | The principal review and the no-shortcuts principle | this plan |
| ADR-O100 | The anti-reward-hacking clause | F-119 |
| ADR-O107 | O102 confirmed; the finish run pushes each slice and continues | S-045 |

The builder reads O89's "genuine airborne or prop-moving misses" as contacts measured between keys or samples (an
interpolated instant): ADR-O104 (RV-02a), for the owner to confirm.

## Gaps
| Gap | Layer | Severity | Status | Fix |
|-----|-------|----------|--------|-----|
| RV-01 | L6 | high | done (S-037) | C12 off CONTACT_WORLD (F-074) |
| RV-02a, RV-02b | L4c | high | done (S-039, S-043) | CONTACT_WORLD per O89 (re-blocks, the vault's hand plant, test hygiene), then releases measured (F-075, F-076, F-079) |
| RV-03 | L1.1 | medium | done (S-041) | the UGC pickup and poses (F-077) |
| RV-04 | docs | medium | done (S-044; the hook is the owner's) | records: versions, logs, hook, stale docs and findings (F-078) |
| RV-05 | L4c | high | done (S-038) | A's words follow the source (F-080) |
| RV-06 | L1.1 | high | done (S-042) | the vanish (F-081) |
| RV-07, RV-08 | L1.1, L2.1 | high | done (S-040, S-048) | the smoke at 3.7 after commits at the contact's instant (F-082, F-061) |
| RV-09 | L5.5 | high | done (S-050) | hits as camera holds (F-083, F-005) |
| RV-10 | L1.1 | high | done (S-051) | the kunai drive and the catch (F-084) |
| RV-11 | L6 | high | done (S-052) | compile refuses non-deliverables; excluded rows N/A (F-085) |
| RV-12 | L6 | medium | done (S-053) | the cartwheel's words (F-087) |
| RV-13, RV-13b | L6 | high | RV-13 done (S-075); RV-13b waits for the owner (F-088) | prompt length (F-088) |
| RV-14a, RV-14b | L4c | high | RV-14a done (S-078); RV-14b waits for the owner (F-148) | every-key body checks (F-089, F-062) |
| RV-15a, RV-15b, RV-15c | L5.5 | high | RV-15a, RV-15b done (S-076, S-077); RV-15c waits for the owner (F-148) | the camera's aim and vertical framing (F-090); the body's aim (F-145) |
| RV-16 | L6 | high | done (S-079) | one laban chain per fighter (F-091) |
| RV-17 | L2.2 | medium | open | one possession model; PROP_TWO_HOLDERS (F-092) |
| RV-18 to RV-41 | various | medium-low | RV-35a done (S-080; RV-35b open); the rest open | F-093 to F-116 and F-016, one slice each (docs/plans/backlog.yaml) |
| RV-42 to RV-54 | various | high-low | RV-42, RV-43, RV-49, RV-45, RV-46, RV-48a, RV-48b done (S-046, S-047, S-049, S-055 to S-058); the rest open | the second review's gaps, F-122 to F-150 (docs/reports/2026-10-12-principal-review-2.md), and F-151 (a body through a prop, RV-54) |
| RV-55 to RV-65 | various | high-medium | RV-57, RV-60, RV-61, RV-62 done (S-059 to S-062); the rest open (RV-55, RV-56, RV-63, RV-64b wait for the owner) | the third review's gaps, F-152 to F-167 (docs/reports/2026-10-12-principal-review-3.md), and RV-65 (RV-20's prompt part) |
| RV-66 to RV-84 | various | high-medium | RV-66 to RV-72 done (S-064 to S-071); the rest open | the fourth review's gaps, F-169 to F-186 (docs/reports/2026-10-12-principal-review-4.md) |
| RV-85 to RV-93, RV-82b | various | high-low | RV-85, RV-86 done (S-073, S-074; F-187 reopened in part, RV-99); the rest open (RV-82b, RV-87 wait for the owner) | the fifth review's gaps, F-187 to F-195 (docs/reports/2026-10-12-principal-review-5.md); its questions F-196 to F-203 |
| RV-94 | L5.5 | medium | open | a moving camera's path (F-204, S-077) |
| RV-95 to RV-105, RV-103a-c, RV-14c, RV-90b | various | high-low | open (RV-90b waits for the owner) | the sixth review's gaps, F-206 to F-218 (docs/reports/2026-10-12-principal-review-6.md); its questions F-211, F-215 |

## Dependencies
- RV-02a after RV-05 (A's final poses); RV-02b after RV-02a, RV-03 and RV-06; RV-07 after RV-08; RV-13b after RV-13 and
  F-088; RV-21 after RV-01; RV-22 after RV-14; RV-35 after RV-02a; RV-39
  after RV-11. PLAN-006's AS-01 and AS-07 follow RV-37 (one strike definition at S04).

## Owner Rulings Needed
- F-088: the caps (which prompts carry them, what a capped prompt drops, whether O97 amends R-16)
- F-099: A's backflip at 5.1 launched from the air (O80's "prior beat")
- F-101: which anime spans keep a declared hang and which are re-timed
- F-108: which of B's two kunai releases is real (answered: ADR-O105, the 2.0 throw)
- F-111: the frame limb and head words are read in
- F-114: whether R-21, R-23 and R-25 bind render.txt
- F-116: whether a moved packet forces re-authoring
- F-117: how F-013 and F-014 close without a fixed seed
- F-118: O37's split cards or the one genre profile (blocks M9-11)
- F-119: how the anti-reward-hacking clause meets R-33 (answered: the owner confirmed ADR-O102, ADR-O107)
- F-143: ADR-Q6's label or its meaning (the source's turned leans and its backflip)
- F-148: the source rows whose numbers contradict their words; F-149: O95 against O88 on two action keys
- F-152: O72's measure for body contacts; F-153: render.txt's deliverability under O1 and O94; F-154: owner_default
  ADRs as rulings (confirm or strike O103 to O106 and O108); F-164: O90's timing; F-165: the pellet's point
- F-055, F-057 and F-060: open since before the run
- From review 4 (S-063): whether a substitution may move or change props other than its decoy without a hand (F-169); what counts as a hit beyond a thrown or held blade (F-175); whether a smash cut, a whip onto the impact frame or a shaky handheld shot is a camera hold (F-177); which checklist rows must pass for a deliverable (F-178, with F-153 and F-117); a declared turn plane against the 180-degree side (F-184); O23's `at: start` read literally or as any key of the actor; O93's grasp and throw on one instant at 6.6; whether the source counts as a ruling under R-06 (O105, O108); whether a deviation's ruling must be an owner ADR in force; R-21's reach to every genre; partly fixed findings reopened (S-063) or kept resolved (S-056 D2); `decided_by: owner` (R-28); O103 sets aside two of O88's flips, which R-06 now leaves to the owner
- F-124 (the 5.9 slide's exception) and F-133 (the scene_reference rules; RV-64b waits for it)
- From review 5 (S-072), filed as question findings: F-196 to F-203; RV-27 and RV-64b wait too
- RV-20: an ADR for the layer-order edit; RV-38: the owner's review of draft values and F-053
- From review 6 (S-081): F-205 (the anime arm, evidence corrected), F-211 (each fighter's chain under O1), F-215 (the
  floor's allowance), F-196 Q5 (S-074's reading, pending) and Q1-Q3 (RV-87 waits), F-197 Q3 (RV-90b waits), F-202 Q2
  (the rope's end); F-202 Q3 is answered by O21 (RV-98)

## Critical Path
1. Step 3, the builder's own shortcuts first (only on the owner's "go"): RV-01, then RV-05 (O88 moves A's arms that
   RV-02a's re-blocks aim at), RV-02a, RV-03, RV-06, RV-02b, RV-04
2. The owner's rulings: RV-05, RV-06, RV-08, RV-07, RV-09, RV-10, RV-11, RV-12, RV-13
3. The fight-breakers that need no ruling: RV-14, RV-15, RV-16, RV-17, RV-37, RV-35, RV-22
4. The rest in backlog order: RV-18, RV-19, RV-21, RV-23, RV-25, RV-27 to RV-32, RV-34, RV-39, RV-41
5. Then PLAN-006 (AS-01 to AS-07) and PLAN-003's remaining M9 slices
After review 3 (S-054): RV-45 and RV-46 (the records) first, then RV-48a, RV-48b, RV-60, RV-61, RV-62, RV-57, RV-58, RV-18,
RV-64 and RV-13, then the rest in backlog order.
After review 4 (S-063): the builder's own shortcuts and overclaims first, RV-66, RV-67, RV-68, RV-69, RV-70, RV-71a,
RV-71b, RV-72, RV-73, RV-74, RV-75, RV-76, RV-77; then RV-58, RV-18, RV-64, RV-13; then the fight-breakers RV-15, RV-14,
RV-16, RV-37, RV-35, RV-59, RV-22; then RV-78 to RV-84 and the rest in backlog order.
After review 5 (S-072): RV-85 and RV-86 (the builder's own shortcuts), then RV-13, then the fight-breakers
RV-15, RV-14, RV-16, RV-35, RV-59, RV-37, RV-22, then RV-88, RV-89, RV-92, RV-73, RV-87, RV-90, RV-91,
RV-93, RV-75, RV-76, RV-77, RV-58, RV-18, RV-64 and the rest in backlog order (backlog 28).
After review 6 (S-081): the builder's own regressions first, RV-96, RV-95, RV-100, RV-99; then the fight-breakers RV-59,
RV-97, RV-98, RV-101, RV-103a to RV-103c, RV-17; then RV-104, RV-105, RV-14c, RV-37, RV-22, RV-102 and the rest in
backlog order (backlog 33).
6. Waiting on the owner: RV-13b, RV-14b, RV-15c, RV-20, RV-24, RV-26, RV-36, RV-40, RV-52, RV-53, RV-55, RV-56, RV-63,
   RV-82b, RV-87, RV-90b (and RV-33, which follows RV-52); the owner's own: RV-38

## Verification
- Each slice: `scripts/verify.sh` and `make golden`, its predictions reported, the self-audit recorded (RV-45); tests
  change only where a ruling or the plan's intent moves the data they pin, each change recorded (ADR-O102, confirmed
  in ADR-O107); a principal review every eight slices and before the next release (O98's soul_check_passes).

## Changelog
- 2026-10-11 — Created from the first principal review (S-035) and the owner's rulings O88 to O100.
- 2026-10-11 — RV-02 split into RV-02a and RV-02b; RV-05 moved ahead of them (S-038).
- 2026-10-11 — RV-01, RV-05 and RV-02a done (S-037 to S-039); ADR-O104 answers O89's "genuine"; RV-02b also re-stages
  B's kunai throw (S-039).
- 2026-10-12 — RV-08, RV-03, RV-06 and RV-02b done (S-040 to S-043); ADR-O105 answers F-108.
- 2026-10-12 — RV-04 done (S-044); the second principal review (S-045): F-120 to F-150, RV-42 to RV-53; ADR-O107.
- 2026-10-12 — RV-42, RV-43, RV-07 and RV-49 done (S-046 to S-049); F-151 and RV-54 (a body through a prop) filed.
- 2026-10-12 — RV-09 done (S-050): hits are camera holds, no playback ramps.
- 2026-10-12 — RV-10 done (S-051): the kunai drive holds the kunai in B; the catch grasps then throws.
- 2026-10-12 — RV-11 done (S-052): excluded rows N/A; cinematic compile refuses non-deliverables.
- 2026-10-12 — RV-12 done (S-053): the cartwheel is a full turn in the words.
- 2026-10-12 — Principal review 3 (S-054): verdict partially; F-152 to F-167, RV-55 to RV-64.
- 2026-10-12 — RV-45 done (S-055): self-audit sections enforced; typed deviations DEV-01 to DEV-28.
- 2026-10-12 — RV-46 done (S-056): the stale and overclaimed records corrected.
- 2026-10-12 — RV-48 split; RV-48a done (S-057): S04's latent checks; the 6.6 throw on its pose; the log's swap.
- 2026-10-12 — RV-48b done (S-058): S08's support hand; the S04 and S08 instructions name every rule their plans
  must meet (tests/test_instructions.py); RV-20 split: its prompt part for S11 to S17 is RV-65.
- 2026-10-12 — RV-60 done (S-059): the camera cards follow O92; the printed camera rules are checked.
- 2026-10-12 — RV-61 done (S-060): "before a beat" read one way by S06, S09 and S10; S09 carries instants.
- 2026-10-12 — RV-62 done (S-061): the vanish line ends A's support; B draws the volley at 5.1.
- 2026-10-12 — RV-57 done (S-062): hits come from the contacts; S16 holds the camera on each.
- 2026-10-12 — Review 4 (S-063): verdict partially; F-169 to F-186 filed with RV-66 to RV-84; RV-27, RV-33 blocked; RV-64 split.
- 2026-10-12 — RV-66 done (S-064): a substitution exempts only its decoy, the prop at its actor's anchor.
- 2026-10-12 — RV-67 done (S-065): the S04 instructions and the validator teach F-077's rule and O48's log.
- 2026-10-12 — RV-68 done (S-066): the volley waits at the thigh pouch; the draw is measured at 0.045 m.
- 2026-10-12 — RV-69 done (S-067): a prop another performer threw is a hit when it touches a body, whatever the verb.
- 2026-10-12 — RV-70 done (S-068): the vanished body is gone from the guidance too; VANISHED_BODY reads it.
- 2026-10-12 — RV-71 split; RV-71a done (S-069): a hit's hold on a still rig, naming its bodies; ninja idioms reach the fight.
- 2026-10-12 — RV-71b done (S-070): the camera cards' rules as structured fields; the prompt prints them word for word.
- 2026-10-12 — RV-72 done (S-071): S08 reads the holds; S09 credits a release only at the change.
- 2026-10-12 — Review 5 (S-072): verdict partially; F-187 to F-195 with RV-85 to RV-93, questions F-196 to F-203; the queue rebalanced toward the fight.
- 2026-10-12 — RV-85 done (S-073): a camera rule's words ask only what its fields ask; a rule about a hit is a hit rule.
- 2026-10-12 — RV-86 done (S-074): TELEPORT's exemption reads the decoy.
- 2026-10-12 — RV-13 done (S-075): PROMPT_LENGTH refuses delivery of a prompt over both of O97's caps; fitting waits (RV-13b).
- 2026-10-12 — RV-15a done (S-076): the camera aims at the body it frames; VERTICAL_FRAMING; RV-15 split (15b inserts and props, 15c body aim, blocked).
- 2026-10-12 — RV-15b done (S-077): an insert aims at its detail; a framed prop is in frame; camera schemas 2.0; F-090 resolved; F-204 and RV-94 filed.
- 2026-10-12 — RV-14a done (S-078): FLOOR_PENETRATION; every claimed support measured at every key; RV-14b (held and embedded props) waits for F-148; the table above brought up to date.
- 2026-10-12 — RV-16 done (S-079): each fighter's laban chain lists the beats it acts in; F-091 resolved.
- 2026-10-12 — RV-35a done (S-080): A's pickups crouch with one hand down; solver/reblock.py committed; F-110 resolved; F-205 (the anime arm) for the owner; RV-35b open.
- 2026-10-12 — Review 6 (S-081): verdict partially, no tampering; F-206 to F-218 with RV-95 to RV-105; F-090, F-110, F-187, F-160, F-091 reopened in part; RV-96 next.
- 2026-10-12 — RV-96 done (S-082): the re-block solver is order-independent, bound by the joint limits, and re-derivable from its printed command.
- 2026-10-12 — RV-95 done (S-083): the pickups re-blocked from recorded commands at A's own 0.57 m, every knee over the floor, the hand no support; F-206, F-110, F-207 resolved; F-219 (the ankle) filed.
- 2026-10-12 — RV-100 done (S-084): S-076's shots and S-078's lunge typed (DEV-32, DEV-33), DEV-09 and DEV-10 updated, R-19 cites O97; F-212 resolved.
- 2026-10-12 — RV-99 done (S-085): RV-60's word lists are a floor in the card check, and a hit rule is found from what a contact does; F-210, F-187, F-160 resolved.
- 2026-10-12 — RV-59a done (S-086): poses between keys along the declared interpolation, measured and reported (38 overlap frames in the fight, one sink: B's crash); RV-59b next, then RV-59c.
- 2026-10-12 — RV-59b done (S-087): the re-block solver keeps a key's spans clear; B re-blocked at 3.7 and 4.4 (29 overlap frames left, all by a contact); F-220 asks how those clear, RV-59e (the check) waits for it; RV-59d next.
- 2026-10-12 — RV-59d done (S-088): a contact between keys is measured on the interpolated pose; the wizard example's landing moves to its 6.6 key; RV-59c next.
- 2026-10-12 — RV-59c measured (S-089): the re-block solver keeps a span over the floor, but no re-pose keeps B's crash there; RV-59c waits for F-220 with RV-59e; RV-97 next, after principal review 7.
- 2026-10-12 — Principal review 7 (S-090): partially, no tampering; F-221 to F-229 filed, F-210 reopened; F-220 corrected and its option a taken as ADR-O109 (in-between keys); RV-59c and RV-59e ready again behind RV-59f; RV-59h next.
- 2026-10-12 — RV-59h done (S-091): a landing between keys is never airborne; F-222 resolved; RV-99b next.
- 2026-10-12 — RV-99b done (S-092): the camera floor finds a hit by what strikes and reads a negation in every word; F-210, F-187, F-160 resolved again; RV-95b next.
- 2026-10-12 — RV-95b done (S-093): the pickups re-solved with every bound S-083 stated; the knees and head held without slack, the lean (70.2, 71.2 degrees) and the ankles asked (F-223, F-215); F-226 resolved; F-224 split to RV-95c; RV-59f next.
- 2026-10-12 — RV-59f done (S-094): in-between keys stand at S13 (motion_plan 2.1, motion_graph 1.2), checked like keys; one of B's at 6.45 clears A's cartwheel elbow (measured); RV-59i (the prompts print them) next.
- 2026-10-12 — RV-59i done (S-095): every prompt prints the in-between keys at their instants (render.txt's rows, the prose's block, the density); RV-108 next.
- 2026-10-12 — RV-108 done (S-096): a declared turn under a half turn is slerped between keys; B's crash is the printed tip (0.209 m under, not 0.385); F-225 resolved; RV-59e next.
- 2026-10-12 — RV-59e done (S-097): S13 refuses a body through another at any frame between keys; five in-betweens of B's and two of the acrobat's clear every span; F-159 and F-220 resolved; RV-59c next.
