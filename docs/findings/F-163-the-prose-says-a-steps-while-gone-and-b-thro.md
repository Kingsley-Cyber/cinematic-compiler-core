# F-163 — The prose says A steps while gone and B throws with an empty hand

<!-- docs-version: 1.0 -->

## Type
contradiction

## Severity
medium

## Layer
L6

## Status
open

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the third principal review, S-054 (docs/reports/2026-10-12-principal-review-3.md)
- all four reference prose prompts print "3.70 A: SUPPORT steps left alternating [f:alt]"; the legend says a symbol lasts until the next line (4.40) and RULES say no A body, pose or support in between
- all four print "B's right hand is empty from 2.00 until 6.60" beside "5.50 B ... THROW [DOUBLE BOW + accent: R hand > shuriken volley star 1]"; no draw from the pouch (F-105)

## Description
Two prompt lines contradict others in the same prompt.

## Impact
The model may draw A stepping inside the smoke, or a throw from an empty hand.

## Proposed Fix
Backlog RV-62: the vanishing actor's line prints no support that lasts into the vanish; the volley is drawn into B's hand before 5.5 (with F-105).

## Owner Ruling
none needed

## Related
- PLAN-007
- F-105
- F-081
- RV-62

## Resolution
Open in part (review 4, S-063): the staff line is fixed; the guidance and the never-return case keep the vanished body alive (F-176, RV-70), and the drawn volley sits on the hand by construction (F-182, RV-68).
Before: RV-62 (S-061): A's 3.70 line keeps its key's support for the instant and says it ends there ("then none: A vanishes
here until 4.40"), with no path to where A reappears (renderers/prose_renderer.py; owner O90), and the prompt's
VANISHED_BODY refuses a vanish line that carries either; B draws the volley from the thigh pouch at 5.1 and lets it
go with the 5.5 throw, so B's right hand is empty 2.00-5.10 and 5.50-6.60 (DEV-30, DEV-31;
tests/test_reference_fight_golden.py::test_b_draws_the_volley_before_throwing_it,
tests/test_prose_render.py::test_the_vanishing_actor_s_line_ends_its_support_and_walks_nowhere).
