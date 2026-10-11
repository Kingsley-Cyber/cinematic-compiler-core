# Lessons

Gotchas already paid for once. Append a line after a slice that teaches one; never rewrite an old line (add a newer
one that supersedes it).

| # | Lesson | Learned in |
|---|---|---|
| L-01 | zsh does not split an unquoted variable: `for f in $FILES` runs once, and `mkdir -p $DIR/$(dirname $f)` can hit relative paths. Use Python for file lists. | S-004 commit split |
| L-02 | A chain like `cmd && scripts/verify.sh > gate.log` that fails early leaves an old `gate.log`; its PASS is stale. `rm -f gate.log` first and read `exit=` from the same command. | S-004 self-audit |
| L-03 | `git rev-parse --short A B` fails; ask one revision per call. | S-004 self-audit |
| L-04 | `python -m compiler.rebind` (report mode) stops at the first moved packet; use `--write <examples>`. A later step may then refuse the moved data: fix that step's plan, re-bind again. | M8, S-003 |
| L-05 | Put a check where its data is first known for every genre: AIRBORNE_PICKUP at S07 refused the UGC creator, whose support exists only at S11. | S-004 |
| L-06 | Moving a body moves what it holds: re-check held prop samples (the 2 m reach check is loose, F-062). | S-004 self-audit |
| L-07 | When moved bodies break a camera shot, search the angle with S16's own validator for the nearest passing value instead of guessing. | S-004 |
| L-08 | The golden's reference rules reach the render through S04 action texts; rewording an action can drop a kernel item. Keep the golden's words or record a rewording in the golden test. | S-004 |
| L-09 | S05 refuses a hard cause whose source beat changes nothing its target needs (CAUSE_EFFECT): give the cause a real effect (the log's `standing` state). | S-001 |
| L-10 | A docs-plane break test that edits a real backlog slice goes stale when the slice is done; append a made-up item instead. | S-003, S-004 |
| L-11 | After any backlog, finding or session edit, run `make docs` (or `python -m kernel.docs_plane --write`); otherwise the gate reports stale generated files. | S-002 |
| L-12 | Importing a test module outside pytest needs `sys.path.insert(0, "tests")` (conftest). | S-004 re-test |
| L-13 | `.claude/commands/` load only in sessions opened in the repo folder; elsewhere, paste the prompt ("Run the self-audit in docs/prompts/self_audit.md …"). | S-005 |
| L-14 | A release marked `at: start` happens at its beat's first instant; S07 counts the prop as still in the hand then (S06 commits the holder change at the beat's end, F-061). | S-003 |
| L-15 | A hand-typed number in a test can be wrong: compute expected distances in Python before pinning them. | S-004 |
| L-16 | A commit message needs a blank line after its first line; without it git folds the whole body into the subject. Write the message file with the blank line, check `git log -1 --format=%s`. | S-008 |
| L-17 | `python -m compiler.rebind` takes bare example names (`reference_fight`), not paths; with no names it reports every example, and silence means no packet moved. | S-009 |
| L-18 | A knowledge-map `enforced_by` test must name its code in quotes (`tests/test_knowledge_map.py` locators); the generic BREAKS test in test_dag_conformance does not, so point at a test that asserts the code. | S-010 |
| L-19 | `pipeline.run` stops at `until='constraint'` by default: a script that compiles an example to see whether it passes must pass `until='render'` (or use `compiler.examples`), or it never reaches the authored steps. | S-011 |
| L-20 | A `kernel/knowledge_map.yaml` edit changes every checklist's evidence text: run `python -m validators.checklist --write` after it, or test_checklist fails on a stale checklist. | S-011 |
