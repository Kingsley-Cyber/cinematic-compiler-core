# S-014 — M9-07b: Laban actions printed as qualities (F4.2, O22)

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5), autopilot run 1 (docs/reports/2026-10-11-autopilot-1.md)

## Gap
Backlog M9-07b (split from M9-07; PLAN-003 F4.2); ruling O22

## Layer
L6

## Status
applied

## Commit
the commit whose message names [S-014]

## Plan
The implied guidance ends each Effort span with its Laban action in brackets, "(punch)", and the model reads punch as
a fist (F4.2). O22: the Effort action stays Laban and punch is thrust; the prose prints actions as qualities. The prose
writes "(thrust quality)", "(press quality)" and so on; S15's data keeps its vocabulary, and LBN-2.4 stays as it is.

Predictions, made before the change:
1. The gate passes before the change: 604 tests.
2. All sixteen prose prompts change (every example has Effort actions); "(punch)" becomes "(thrust quality)" in the
   reference fight (8), the wizard (2) and the live-action standoff (1); render.txt does not change.
3. No prompt code fires; no checklist row changes result.
4. 605 tests (one wording test).

## Decisions
- D1 — "punch" prints as "thrust"; the other seven actions keep their Laban names. Why: O22 ("punch = thrust: strong,
  sudden, direct"); press, slash, flick, dab, glide, float and wring have no fist reading. Level: covered (O22).
- D2 — The action is followed by "quality" inside the existing brackets, after the four factors the line already
  lists ("maintain strong weight, sudden time, direct space, bound flow (thrust quality)"). Why: F4.2 ("thrust quality
  (strong, sudden, direct)"); the factors are already on the line, so they are not repeated. Level: covered (F4.2).
- D3 — LBN-2.4 keeps "punch" in its Laban action field. Why: the plan's F4.2 "LBN unchanged unless Q3", and Q3's
  ruling (O55, no reasons in LBN) does not ask for it; the LBN's field is the Laban vocabulary itself. Level: covered.

## Duration
about 15 minutes

## Changes
- `renderers/prose_renderer.py` (LABAN_WORDS; the action as a quality); `tests/test_render.py` (one test)
- outputs: the sixteen prose prompts and the envelopes; checklists (hashes only)
- `docs/rules.yaml` 2.2 (R-27 enforcement; docs log), backlog (M9-07b done, M9-08 next), CHANGELOG, the run report

## Verification
- before: `scripts/verify.sh` exit 0, 604 passed (the pre-commit gate of S-013, 30c3229)
- after: `scripts/verify.sh` exit 0, 605 passed; `make golden`: the sixteen prose prompts changed on purpose; every
  render.txt unchanged
- Prediction 1 held. Prediction 2 held (punch to thrust: 8, 2 and 1; the UGC demo has none). Prediction 3 held.
  Prediction 4 held (605; the first run of the new test failed on a missing import, fixed).

## Next
M9-08 (O21 opening from above in V6's wording).
