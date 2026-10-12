# ADR-O81 — M9-06 lands forward kinematics and reports the contact misses before CONTACT_WORLD refuses

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-11

## Decided By
owner

## Scope
L4c

## Decision
Owner, in chat, 2026-10-11: "Option 3 — build it, report misses first. Land forward kinematics, pelvis roots (O72),
and print the world points in the prompt. List every miss as a finding with its distance. Group by: source A rows vs
repo-authored keys; hand/foot vs prop; small misses (<0.3m) vs large (>1.0m); real misses vs measurement artifacts
(airborne, rotating, prop-moving). Turn the refusal on in the following slice once I've seen the list. Also: the
1.4m miss at A's 8.00 pickup (since F-064) is expected. Include it in the list with its cause. Do not re-block yet.
Do not rewrite the source. Do not turn the check on yet. Report back with the miss list before proceeding."

## Context
A prototype (S-027) found 5 of 35 measurable contacts within ADR-O72's 0.15 m, the owner's source A rows among the
misses (up to 1.9 m), so a refusing check would have forced re-blocking the owner's rows against O72.

## Consequences
- Backlog M9-06 splits: M9-06a (forward kinematics, pelvis roots, printed points, the miss report) and M9-06b
  (CONTACT_WORLD refuses; blocked until the owner has reviewed the list).
- The owner's source rows (the reference fight's A keys) are not changed.

## Alternatives Considered
- Re-block every contact (source rows included); re-block repo keys only: not chosen by the owner.

## Supersedes
—

## Superseded By
—

## Related
- ADR-O72
- ADR-O24
- PLAN-003
