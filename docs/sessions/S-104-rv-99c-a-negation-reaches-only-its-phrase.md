# S-104 — RV-99c: a negation reaches only the phrase it heads, and the feet strike

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-99c (PLAN-007); findings F-233, F-210; ruling O92; ADR-O110

## Layer
L5.5

## Status
applied

## Commit
the commit whose message names [S-104]

## Plan
RV-99b let a negation govern the rest of its clause, so "Push in to a close-up without delay as the blow lands." and
three more rules the floor refused before it passed, and it left the feet out of the striking parts, so the wizard
example's own hit ("the acrobat's foot connects with the wizard's chest") passed with a close-up (F-233). The class:
any negation in a rule, any part that strikes.
1. A negation reaches only the phrase it heads: a noun's ("no", "without", "nor", "instead of") to the next
   preposition or conjunction, a verb's ("not", "never", "avoid") to the next conjunction, either to its clause's end.
2. The feet strike: a foot, boot, toe or sole meeting something or driven into a body is a hit, its landing is not;
   an attack's -ing and -ed forms and "driven" count.

Predictions, made before the change (14:38 by the clock):
1. The gate passes before the change: 753 tests (cf6750f, S-103's chained gate).
2. The four rules RV-99b let through are refused again, and so are the three foot phrasings (the wizard example's own
   hit among them) and "Never cut away and push to a close-up as the knee connects."; O92's own sentences, "no shaky
   texture" and a landing on both feet still pass; the library's cards pass unchanged (no card, no prompt changes).
3. 754 tests.

## Decisions
- D1 — A negation's reach: a noun's ("no", "without", "nor", "instead of") ends at the next preposition or
  conjunction, a verb's ("not", "never", "avoid") at the next conjunction, either at its clause's end. A word after a
  negation's phrase is said: "without delay as the blow lands" names the blow. A gerund after "no" is read as a noun,
  so "No cutting to a close-up" is refused rather than passed (the floor errs toward refusing). Level: interpretation
  (F-210's, Claude's, for owner review).
- D2 — The feet strike with every meeting verb but a landing ("as both feet land" stays a landing); the attacks' -ing
  and -ed forms and "driven" count. Level: covered (owner O92; the wizard example's hit, b05_c2, is a foot).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the chained gate commits |
| Predictions written first | PASS | at 14:38, before the edit |
| The class, not the probe | PASS | review 8's eleven phrasings across the four reviewers refused; O92's sentences, the negated shake, a landing and every library card pass; F-210 stays open (still a word list) |
| Tests | PASS | one added; a docstring revised (test_o92_s_own_words_pass_the_floor: "reaches the phrase it heads") |
| Examples | PASS | none changed |
| Records | PASS | F-233 resolved; backlog 47; CHANGELOG; PLAN-007; run report |
| Hygiene | see Verification | the staged scan runs first in the chained commit |

## Duration
from 14:38 (the plan's predictions) to 14:40 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- planner/camera_library.py: the negation's reach (`_reach`, `said`); FEET and STRIKES; the attacks' forms; "driven"
- tests/test_camera_solver.py: one test, one docstring
- docs: F-233; backlog 47; CHANGELOG; PLAN-007; run report

## Verification
- before: S-103's chained gate at cf6750f: 753 passed
- Prediction 1 held. Prediction 2 held (all eleven refused; the calm rules, O92's sentences and the cards pass; no
  example file changed). Prediction 3 held (754). Predictions 3 of 3; the first gate run failed on three long
  test lines (ruff E501), fixed before this one.
- the gate on this record (14:42:55): `scripts/verify.sh` exit 0, 754 passed in 161.85 s, docs plane: PASS, check:
  PASS
- the hygiene scan over the staged diff: 0 hits (run first, and again in the chained commit)
