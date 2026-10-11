# S-004 — M9-03: grounded pickups at 7.5 and 8.0 (AIRBORNE_PICKUP)

<!-- docs-version: 1.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5)

## Gap
Backlog M9-03; findings F-022 (GAP-07), F-007 (F7); ruling ADR-O18

## Layer
L4a

## Status
applied

## Commit
the commit whose message names [S-004]

## Plan
The golden contradicts itself (O18, O59): its rope-dart track says "7.5 A lands near ground rope dart, A picks up rope
dart" and its kunai track "A picks up kunai from ground during crash landing" at 8.0, while A's rows put the body at
y 2.2 and 1.8, in the air. Fix the numbers to the words: A pushes off the pillar at 7.0 (feet touch `at: start`),
lands crouched by the rope dart ([0.4, 0, 3.8]) and takes it at 7.5, runs to the kunai ([0.3, 0, 5.3]) and takes it
crouched at 8.0, then leaps at 8.5 for the aerial kunai drive. Re-author S04 (positions, support contacts and effects,
actions, b19's label, prop samples, b17/b18 reasons), S11 support and cues, S13 crouch-and-reach keys from A's own
crouches at 5.9 and 9.5, and the S16 shot texts. Check at S07, the first step with contacts and support together:
AIRBORNE_PICKUP refuses a possess on a prop resting on a surface while the possessor has no support, or is farther
than the 2 m reach; the same code reads the prompt (a pickup on a NO SUPPORT line). F7 becomes caught.

Predictions, made before the change:
1. On today's data AIRBORNE_PICKUP fires twice, both in the reference fight (rope dart at 7.5, kunai at 8.0); the
   wizard, live-action and UGC examples stay silent (the UGC glasses are taken standing).
2. The prompt code fires on the same two pickups in all four reference prose modes.
3. Re-authoring trips checks at S11 (support vs S06), S13 (joint limits, root equals S04) or S16 (geometry), each
   fixed in its own plan.
4. Only the reference render.txt changes; the golden test needs a recorded deviation for A's rows at 7.5 and 8.0.
5. No checklist row moves to PASS: F7's rows (BIO, T7, C5) keep open gaps (WEIGHT_TRAVEL, OPPOSITION,
   PROP_TWO_HOLDERS).

## Duration
about 1.5 hours

## Changes
- `examples/reference_fight/plans/temporal.json`: b18 pillar touches `at: start`, A's feet land at 7.5 (support, effect
  grounded), b19 renamed rope_dart_regrapple with A at [-0.1, 0.6, 3.2], b20 A at [-0.2, 0.6, 5.1] with the leap at 8.5
  (release, effect airborne); rope dart and kunai samples at their resting places; b17/b18 reasons; actions keep the
  golden's words where they agree (k_rules_17, k_rules_19) and reword two that contradict its tracks (k_rules_18 "AERIAL",
  k_rules_27 "during crash landing")
- `kinematic.json` (A at 7.5 and 8.0 on both feet), `motion.json` (crouch-and-reach keys from A's crouches at 5.9 and
  9.5), `camera.json` (c17-c19 texts; c18 azimuth 64 to 28, c19 -12.5 to 10, the passing angles closest to the
  authored ones, found with S16's own validator); bartenieff, effort and render packets re-bound
- `compiler/passes/derived/p11_kinematic.py`: `resting_pickups`, `pickup_findings` (AIRBORNE_PICKUP);
  `validators/prompt_validator.py` (prompt side); `validators/checklist.py` (F7 caught); `kernel/knowledge_map.yaml` BIO
- tests: S11 break (no support, out of reach), conformance break, golden GROUNDED_PICKUPS and GROUNDED_RULES
- after the self-audit (owner O68, run before the commit): the rope dart's 8.0 sample moved into A's left hand
  ([0.2, 0.9, 4.9], 0.54 m from the root; it had been left 1.44 m away when A moved); the golden test pins A's full 7.5
  and 8.0 descriptions (it had only checked "support=both feet"); the S11 docstring labels its two interpretations;
  finding F-062 (held props are only checked to 2 m)

## Verification
- `scripts/verify.sh` before the change: pass; after: pass (581 tests)
- Predictions: (1) partly wrong at first: the check at S07 also refused the UGC creator, whose support is authored only
  at S11 (no support contacts); the check moved to S11, the first step that knows support for every genre, and then
  fired exactly on the two reference pickups. (2) held: the prompt code refused both pickups in all four modes.
  (3) held at S16 only (c18 composition and axis, c19 framing); S11 and S13 accepted the new keys. (4) held, plus two
  reference rules that had to be reworded (recorded). (5) held: no verdict moved; F7 is marked caught on BIO, T7
  and C5, whose other gaps keep them NOT CHECKED.
- `make golden`: render.txt changed on purpose for the reference fight only (A's rows at 7.5 and 8.0, contacts,
  prop tracks, c17-c19); GROUNDED_PICKUPS and GROUNDED_RULES recorded in the golden test.

- Self-audit (docs/prompts/self_audit.md) before the commit: NOT READY at first (a held prop left behind by my move,
  a weakened golden assertion for two rows, two unlabelled interpretations, the tree mixed with session S-005); all
  four fixed, then committed apart from S-005. Claims corrected: the crouch keys are modelled on A's crouches (same
  knees at 7.5, hips 15-25 degrees shallower, arms authored), not copied; the camera search was on a 2-degree grid.

## Next
M9-03b (carried_by on prop nodes).
