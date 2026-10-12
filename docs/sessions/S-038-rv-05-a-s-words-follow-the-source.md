# S-038 — RV-05: A's limb and head words follow the source's words (O88)

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-05 (PLAN-007); finding F-080; rulings O88, O7, O10, O11, O83, O101, O102

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-038]

## Plan
O88 (owner): "Follow the source's words. Flip the 21 limb words and 13 head words. Record each as an R-33 deviation."
Measured on the reference fight's A rows: exactly 21 limb words point the other way to the source's own words (fwd
against back) and 13 lines print "head back-high", all on HD below zero (F-080). A test first: reading the words in
Labanotation's standard cross instead of the trunk frame agrees with the source less (47 of 88 against 67 of 88), so
the cause is the source's numbers, not the frame; the numbers flip (joint X sign), and the printed words follow.

Each flip is checked against its row's other words and physics. Nineteen limb flips are sound. The two at 0.6 (both
hips, "leg back mid") would point A's thighs up and lift the soles 1.27 m off the pillar top, against the same row's
"deep compressed crouch ... both feet on pillar top": those two keep their numbers (ADR-O103, for the owner to
overrule). 1.1's left hip flips to +90, past the anime hip-extension limit, so it is held at +60 (O11, as O10's clamp);
the right hips at 1.1 and 3.0 flip from the source's +90 to -90, which replaces their O10/O11 clamp. A's 3.0 right foot
then reaches the ground, so b06_c3, CONTACT_WORLD's one exception, goes. A's left arm at 6.6 flips, so B's catch
(repo-authored) is re-blocked to the moved elbow.

Predictions, made before the change:
1. The gate passes before the change: 640 tests (fa7643e).
2. After it, A's printed limb words agree with the source's fwd/back on 86 of 88 (the 0.6 hips stay against it) and no
   A line prints "head back-high".
3. CONTACT_WORLD: b06_c3 meets (about 0.13 m) and leaves the exceptions; B's catch (b17_c1, b17_c2) misses after A's
   6.6 arm flips and is re-blocked; no other contact moves past 0.15 m.
4. Only the reference fight's outputs change (render.txt and the four prose prompts); S15 or S16 may refuse a moved
   pose (uncertain).
5. 640 tests; the golden test's A-row deviations (O88 flips, the clamps they replace, the pickups' heads, the empty
   exception set) change, each recorded with O88 (ADR-O102).

## Decisions
- D1 — RV-05 moves ahead of RV-02 and RV-02 splits into RV-02a (exact-instant misses and the re-blocks, after RV-05) and
  RV-02b (releases measured, after RV-03 and RV-06). Why: O88 turns A's arms, which RV-02's re-blocks aim at (A's right
  hand at 3.7 holds the pellet); measuring releases now would refuse the rope dart's 5.9 release, which O90 (RV-06)
  removes, and the UGC glasses' release, which RV-03 re-poses. Level: covered (R-10, finish.md section 5).
- D2 — The flips change the numbers, not the frame the words are read in: reading the words in the standard cross
  agrees with the source less (47 of 88 against 67 of 88). Why: F-080, hypothesis tested before the change. Level:
  covered (O88).
- D3 — The 0.6 hips keep their numbers (ADR-O103). Why: flipped, the soles leave the pillar top and the thighs point
  up, against the same row's "deep compressed crouch ... both feet on pillar top". Level: owner_default ADR under
  O101, for the owner to overrule.
- D4 — A hip flipped past the anime extension limit is held at +60 (1.1's left hip), as O10 clamped before (O11); the
  right hips at 1.1 and 3.0 take the source's magnitude with the flipped sign (-90), which replaces their clamp.
  Level: covered (O11, O10, O88).
- D5 — The golden test's deviation records change with O88: WORD_FLIPS and HEAD_FLIPS replace HIP_CLAMPS; the pickups'
  heads at 7.5 and 8.0 flip; CONTACT_EXCEPTIONS is empty; CATCH_ROOT moves with B's re-block. Why: ADR-O102 (O88 asks for
  the records). Level: covered.
- D6 — B's catch is re-blocked with the least-change solver of S-030 (both hands within 0.06 m of A's moved elbow,
  both soles on the ground). Why: O83 point 1 (the repo side of a miss moves). Level: covered.

## Duration
about 50 minutes

## Changes
- examples/reference_fight/plans/motion.json (A's 19 limb and 13 head flips; B@b17 re-blocked; no exceptions),
  temporal.json (B@b17's anchor); re-bound; outputs and checklists regenerated
- tests/test_reference_fight_golden.py (WORD_FLIPS, HEAD_FLIPS, GROUNDED_PICKUPS heads, CONTACT_EXCEPTIONS, CATCH_ROOT)
- ADR-O103 (new); F-080 resolved; PLAN-007 (RV-02a/RV-02b, order); backlog 13; CHANGELOG

## Verification
- before: `scripts/verify.sh` exit 0, 640 passed (fa7643e)
- after: `scripts/verify.sh` exit 0, 640 passed; only the reference fight's outputs changed; `compiler.rebind` passed with
  no refusal at S13, S15 or S16
- Prediction 1 held. Prediction 2 held (86 of 88; no A head prints back). Prediction 3 held in part: b06_c3 meets at
  0.126 m and B's catch at 0.06 m, but the pellet contact b09_c1 grew from 0.20 to 0.81 m when A's right arm flipped at
  3.7; it is still exempt as prop-moving until RV-02a re-blocks it. Prediction 4 held (nothing refused). Prediction 5
  held (640; the golden test's records changed with O88).

## Next
RV-02a (CONTACT_WORLD per O89, re-blocks against A's final poses).
