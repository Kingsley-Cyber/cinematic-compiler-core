# ADR-O101 — Finish the repo: work until the plan's soul is built and the fight works

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-11

## Decided By
owner

## Scope
all

## Decision
Owner, in chat, 2026-10-11: "commit it, push it. and im about to reach toekn limit, i need a prompt that will
essentially have you working until the repo is done. ive genuiinely provided you enough information to relay the goal
and intent of the repo, and all questions you have can the original document plan can be used to find the soul of the
repo. as of now the repo is not complete nor is it working, at the end of the day you can add to this repo but you cant
take away from the soul and intent of the plan. you can change things but you are working to intentioally implement
fully the soul of the plan and ensure it works, fully implementation and migrations, youve already done a subagent
analysis of the repo state and have finidings so you know what you need to do or read to fully find a way ahead."

## Context
The first principal review (S-035) found the repo only partly matching its plan; its gaps are PLAN-007 and the
remaining slices of PLAN-003 and PLAN-006. The owner is leaving a standing instruction for the work to continue.

## Consequences
- docs/prompts/finish.md (and `/finish`) carries the run: slice after slice until the gate's six conditions hold (O98),
  each slice committed and pushed after the gate, the self-audit and the hygiene scan.
- Open questions are answered from the plan's own sources (the rulings, the DAG, the owner's source fights and render
  verdicts, the plans, the owner's original documents), each recorded as an ADR Decided By owner_default that the owner
  may overrule; only renders, render verdicts and cards leaving draft wait for the owner.
- Nothing the plan intends may be removed or weakened; changes, additions and migrations are allowed with their
  records. Tests change only where a ruling or the plan's intent moves the data they pin, each a recorded deviation
  (AGENTS.md section 18, F-119).
- The bootstrap's resume step 6 sends a resumed session back into a running finish run.

## Alternatives Considered
- —

## Supersedes
—

## Superseded By
—

## Related
- ADR-O70
- ADR-O98
- ADR-O99
- ADR-O100
- PLAN-007
- F-119
