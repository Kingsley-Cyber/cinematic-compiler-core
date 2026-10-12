# S-019 — The owner's rulings O72-O80, rules R-33 and R-34

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5)

## Gap
Backlog D-09; the owner's answers to autopilot run 1 (ADR-O72, O73, O74 and the policy) and to findings F-058,
F-064, F-065, F-067

## Layer
docs

## Status
applied

## Commit
the commit whose message names [S-019]

## Plan
Record the owner's rulings word for word: O72, O73 and O74 accepted; the policy as ADR-O75 (rule R-33, superseding
O71 and carrying its other cases forward); the lean ruling as ADR-O76 (rule R-34); the four finding rulings as
ADR-O77 to O80. The backlog unblocks M9-06, M9-09a and M9-09b and gains M9-09d, M9-09e, M9-09f for the findings
(M9-09c carries F-058's check). The autopilot's section 5 takes R-33.

Prediction: the docs plane and the gate pass (609 tests); AGENTS.md section 5 lists R-33 and R-34; section 7 lists
no proposed ADR.

## Decisions
- D1 — The pasted rulings are recorded as the owner's words (they answer the run report's questions and came from
  the owner in chat). Level: covered (AGENTS.md section 14).
- D2 — R-34 is worded for checks that judge a whole-body quality, not "every check": per-joint checks (JOINT_LIMIT,
  a limb's direction word, a knee's fold for support level) read one joint by design, and the owner's sentence would
  forbid them; ADR-O76 keeps the owner's words and notes the scope. Alternatives: the owner's sentence as the rule.
  Level: interpretation (Claude's, for owner review; F-053).
- D3 — ADR-O75 supersedes O71 and restates O71's other cases, so one ADR governs autopilot data changes. Level:
  covered (the ADR protocol keeps Supersedes and Superseded By consistent).
- D4 — The findings' fixes become backlog slices (M9-09d, M9-09e, M9-09f; F-058 in M9-09c), built after M9-09a and
  M9-09b as the owner asked ("Proceed with M9-09a and M9-09b"); O72's re-authoring lands with M9-06, whose forward
  kinematics gives each pelvis height instead of a hand-picked number (lesson L-15). Level: covered.

## Duration
about 20 minutes

## Changes
- `docs/decisions/ADR-O72`, `O73`, `O74` (accepted), `ADR-O75` to `ADR-O80` (new), `ADR-O71` (superseded)
- `docs/rules.yaml` 3.0 (R-33, R-34), `docs/prompts/autopilot.md` 2.0 (section 5), findings' Owner Ruling fields,
  backlog (version 5; D-09), CHANGELOG

## Verification
- before: `scripts/verify.sh` exit 0, 609 passed (the pre-commit gate of S-018, 6d82e06)
- after: `scripts/verify.sh` exit 0, 609 passed; docs plane PASS; AGENTS.md lists R-33 and R-34 and no proposed ADR.
  The prediction held.

## Next
M9-09a (SHAPE_DIRECTION with the owner's lean ruling).
