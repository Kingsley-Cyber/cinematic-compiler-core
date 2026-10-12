# S-091 — RV-59h: a landing is never airborne at its own instant

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-59h (PLAN-007); finding F-222 (principal review 7); rulings ADR-O104 ("the actor is airborne or the prop
is moving there"), O89 ("Only exempt genuine airborne ... misses"), O72

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-091]

## Plan
S-088 read "airborne" between keys from the key before: a span that starts with no claimed support is in the air, so
any contact inside it, a landing included, is excused however far it misses (a landing 1.2 m up passes S13, F-222). A
support's onset ends a flight; at its own instant the actor is not airborne. The class: an exemption that reads a
state the contact itself changes.
1. solver/contact_world.py: between keys, the actor is airborne only when no support of its own is open just before
   the contact's instant (S07's intervals: a support onset opens a part on a surface, a release closes it), and a
   support onset (a landing) is never airborne; at a key nothing changes (an exact instant is never exempt).
2. The S13 instructions say so; S-088's test, which pinned the loose rule, follows F-222; a planted touch in the air
   stays excused.
3. F-053's S-088 entry marked superseded.

Predictions, made before the change (11:48 by the clock):
1. The gate passes before the change: 731 tests (871d7ce, S-090's chained gate).
2. No contact in the four examples is measured between keys, so no example's CONTACT_WORLD rows or prompts change;
   only the motion plans re-bind to the new instructions.
3. The planted landing at 5.3 is refused even when the span starts in the air; a planted touch at 5.3, after the
   pillar is let go, is excused as airborne.
4. No other check or test changes.
5. About 732 tests.

## Decisions
- D1 — Between keys the actor is airborne only when no support of its own is open just before the contact's instant,
  read from the contacts in time order (a support's onset opens a part on a surface, a release closes it; a contact at
  the instant itself does not count), and a support's onset is never airborne: it ends the flight it lands. At a key
  the rule is unchanged (an exact instant is never exempt). Level: covered (ADR-O104's "airborne there", O89's
  "genuine airborne"); it supersedes S-088's reading in F-053.
- D2 — S-088's test pinned the loose rule; it now asserts the landing stays refused with the key's claim emptied,
  under F-222 (ADR-O102: a test follows a recorded finding). Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the staged scan, the gate and the commit |
| One gap, right layer | PASS | CONTACT_WORLD's exemption at S13 (L4c) |
| Predictions written first | PASS | the session file was written at 11:48, before any code |
| New rule fires and stays silent | PASS | measured: the planted landing at 5.3 refused with and without the key's claim; a planted touch at 5.3 after the pillar's release excused (1.16 m, airborne); the examples' rows unchanged (none lies between keys) |
| Neighbours | PASS | the turning flag still reads the key before (a declared turn spans its keys); F-134's same-instant ordering applies to the open supports too (RV-17) |
| The step's instructions teach it | PASS | euler_solving.txt: excused only while no support is open just before it, never at a landing |
| Tests changed with their data | PASS | S-088's test follows F-222 (D2); one new test; nothing removed |
| Examples | PASS | every motion plan re-bound; no prompt or checklist changed |
| Records | PASS | F-222 resolved; F-053's S-088 entry superseded; map 25 (kernel log); backlog (RV-59h done, RV-99b next); PLAN-007; CHANGELOG; run report |
| Hygiene | see Verification | the staged scan runs first |

## Duration
from 11:48 (the plan) to 11:49 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- solver/contact_world.py (`_open_supports`; the airborne flag between keys); planner/prompts/euler_solving.txt
- tests/test_motion_solver.py (S-088's test under F-222; one new test); every example's motion plan re-bound
- F-222 resolved; F-053; kernel/knowledge_map.yaml 25; backlog; PLAN-007; CHANGELOG; run report

## Verification
- before: S-090's chained gate at 871d7ce: 731 passed
- Prediction 1 held. Prediction 2 held (no example's rows or prompts changed; the motion plans re-bound). Prediction
  3 held. Prediction 4 held. Prediction 5 held (732). Predictions 5 of 5.
- the gate on this record (11:49:42): `scripts/verify.sh` exit 0, 732 passed in 71.29 s, docs plane: PASS, check:
  PASS
- the hygiene scan over the staged diff: 0 hits (run first in the chained commit)
