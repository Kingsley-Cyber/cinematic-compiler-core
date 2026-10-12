# F-176 — The vanished body lives on in other sections of the prompt

<!-- docs-version: 1.0 -->

## Type
contradiction

## Severity
medium

## Layer
L6

## Status
resolved

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the fourth principal review, S-063 (docs/reports/2026-10-12-principal-review-4.md)
- the reference prompts' implied guidance prints "A 3.70–4.00: maintain light weight, sudden time, indirect space, free flow (flick quality)" and "travels through space between positions" while A is gone (S15 covers the gone actor's slot, compiler/passes/derived/p15_effort.py)
- a vanish that never returns prints "vanishes here to the end" beside "the body reappears at its next line" and "hold sign to the end" (renderers/prose_renderer.py)
- validators/prompt_validator.py: VANISHED_BODY reads STAFF and RULES only, and its vanish-line check passes on its own phrase ("SUPPORT steps left alternating [f:alt], then none: A vanishes here until 4.40" passes)

## Description
RV-62 (S-061) fixed the staff line F-163 named; the guidance, the never-return case and the check's reach remain.

## Impact
The model is told to keep moving a body the rules say is gone.

## Proposed Fix
Backlog RV-70: S15 and the guidance skip vanish windows; a vanish that never returns prints no reappearance or hold; VANISHED_BODY reads every section and refuses a travelling support on the vanish line. F-163 reopened in part.

## Owner Ruling
none needed (O90, O18)

## Related
- RV-70
- F-163
- ADR-O90
- ADR-O18

## Resolution
RV-70 (S-068): the guidance prints the vanish's own Effort at its instant ("A at 3.70: vanishes with light weight, sudden
time, indirect space, free flow (flick quality), in place; gone until 4.40", the source's "in-place dissolve") and clips
any other interval at a vanish; the "travels through space" sentence excepts a gone performer; a vanish that never
returns says so and holds no sign or final pose (renderers/prose_renderer.py `vanish_note`); VANISHED_BODY reads the
guidance and refuses a vanish line whose support steps
(tests/test_prose_render.py::test_the_vanished_body_is_gone_from_the_guidance).
