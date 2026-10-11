# ADR-O71 — Golden and authored-data changes during an autopilot run

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-11

## Decided By
owner_default

## Scope
all

## Decision
During an autopilot run (ADR-O70), after R-17 (fix the check when the golden is internally consistent):
1. A golden or authored-data change covered by an accepted ADR or the approved slice text goes ahead, recorded in the
   golden test with that ADR.
2. An uncovered change goes ahead only when it is a leaf (no `next` or `ready` slice depends on the slice), the
   smallest change that makes the golden agree with its own words or the DAG (keeping the golden's words), and fewer
   than three such changes from the run are waiting on the owner. It is committed in its slice's commit with a
   proposed ADR and `[proposed ADR-Onn]` in the message.
3. Anything else parks the slice: its work is restored, its records are committed (session, proposed ADR, question
   finding, backlog `blocked`), and the run picks the next slice.
The layer order, the rules, a card leaving draft and a render verdict always park.

## Context
Accepted as owner_default: the owner saw this policy in the S-008 report and replied "commit it, Run the autopilot"
without objecting (2026-10-11).

The owner, asked what a run should do with a golden change no ruling covers: "can you decide but plan it based on
meeting my intent and downward effects?" The intent is a run that does not stop, with the owner keeping authority over
the golden (R-17, R-30). The downstream cost differs by dependency: a rejected leaf change is one `git revert` with
nothing built on it; a rejected change that later slices build on unwinds all of them. Nothing leaves the machine
before the owner's push review (R-03), so a proposed change is seen before it is published.

## Consequences
- R-30 ("only the owner approves a change to the golden") is read, for these local commits, as "approved before it
  leaves the machine": the owner rules on each proposed ADR before the push.
- At most three unratified golden changes stand at once, which bounds the rework if the owner rejects them.
- Parked slices also block their dependents; the run report lists them with their questions.

## Alternatives Considered
- Park every uncovered change: nothing unapproved lands, but most of M9 re-authors the reference fight, so the run
  would stall early.
- Make every change and flag it: the run never stalls, but one rejection can unwind a chain of later slices.

## Supersedes
—

## Superseded By
—

## Related
- ADR-O70
- ADR-O59
- R-17
- R-30
