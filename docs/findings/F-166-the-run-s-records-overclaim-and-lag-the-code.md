# F-166 — The run's records overclaim and lag the code

<!-- docs-version: 1.0 -->

## Type
drift

## Severity
medium

## Layer
docs

## Status
resolved

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the third principal review, S-054 (docs/reports/2026-10-12-principal-review-3.md)
- CHANGELOG RV-10 says "while A's right hand keeps it" (the hand is 0.66 to 0.87 m from the kunai); CHANGELOG RV-42 says PROMPT_CONTRADICTION refuses "toward X" beside "NOT toward X", but render.txt's A 2.5 row prints "(toward B and ground)"
- F-084 and F-144 are resolved for what their slices did, not for what they found; F-080's resolution claims the 13 head flips (F-129: every A head word prints forward-high)
- S-046 to S-053 record about 7 h 25 min of Duration; their commits span 1 h 43 min
- no self-audit is recorded in S-046 to S-053, though R-03 grants a push only after one; interpretations are labelled covered (R-32) and none reached F-053; F-127 lacks S-049's re-blocks
- stale: AGENTS.md (F-119 open), ADR-O92 (S16), PLAN-007 (RV-33 waiting; Updated), F-148 (RV-51), F-108 (waiting), docs/for_the_owner.md (30 rules; forward kinematics planned), the kernel log's decided_by "owner" for the builder's exceptions file (seq 59; a log line is never edited), the exceptions file's misquote of ADR-O83, validators/contact_world_report.py (the motion plan lists exceptions); F-015 has no live slice; F-055, F-057 and F-060 are missing from the owner's list

## Description
F-128's pattern continued through the run's second eight slices.

## Impact
A reader trusts claims the data does not bear out.

## Proposed Fix
Backlog RV-45 (self-audit sections, F-053, F-127) and RV-46 (each stale record corrected; resolved findings reopened as partial where work remains) now, before the next code slice.

## Owner Ruling
none needed

## Related
- PLAN-007
- F-128
- F-130
- RV-45
- RV-46

## Resolution
RV-45 and RV-46 (S-055, S-056): the self-audit is recorded from S-055 (the docs plane refuses an applied session
without it); F-053 lists the run's interpretations and F-127 S-049's re-blocks; the CHANGELOG's RV-09, RV-10 and RV-42
lines say what holds; F-084, F-144, F-080 and F-083 say what remains and where; S-046 to S-053 carry their Duration by
the commit times; AGENTS.md, ADR-O92, PLAN-007, F-148, docs/for_the_owner.md, the exceptions file's quote of ADR-O83
(and F-124's) and validators/contact_world_report.py are corrected; the owner lists name every owner_default ADR and
the hook (F-168). Kernel log seq 59 keeps its decided_by "owner" (a log line is never edited); seq 64 records the
file's version 2 as agent_fix.
