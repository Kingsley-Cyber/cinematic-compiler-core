# S-044 — RV-04: the records agree with the repo: versions, logs, stale documents and findings

<!-- docs-version: 2.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-04 (PLAN-007); findings F-078, F-063, F-066, F-028, F-015; rulings O52, O64, O101, O106 (new)

## Layer
docs

## Status
applied

## Commit
the commit whose message names [S-044]

## Plan
F-078: the records the next session trusts disagree with the repo in small ways. Fixes, each against the written rule
(docs/versioning.md):
1. F-063 answered first (ADR-O106): versioning.md stands as written; past bumps stay (the logs are append-only).
2. docs/rules.yaml 3.1 to 4.0: R-35 (S-029) was a rule change and took +0.1.
3. The gate refuses a schema, library or kernel log entry that changes a file without changing its version, from each
   log's present end (the history before stays as written: 36 schema, 21 library and 47 kernel entries, this run's
   own map edits among them); the docs log already has this check (O64).
4. The kernel log covers kernel/layer_order.yaml, as versioning.md says; the knowledge map takes version 2.
5. Stale documents: README points to docs/layer_order.md; docs/layer_dependency.md says it is superseded; ADR-O72,
   O73, O82 and O85 stop saying "until the owner rules", "proposed" and "card 3".
6. Findings answered and built are closed: F-066 (O72; the pelvis root and 0.15 m since M9-06), F-028 (forward
   kinematics, the rotation path and the launch check are built), F-015 (the insert wording is the standing practice),
   F-063 (ADR-O106), F-078 itself; PLAN-004's table shows F-018 resolved.
7. The pre-commit hook (`make hooks`) writes core.hooksPath into the repository config that this worktree shares with
   ~/Documents/cinematic-compiler-core, which O52 keeps the agent from editing: it goes to the owner.

Predictions, made before the change:
1. The gate passes before the change: 645 tests (61e15cb).
2. With the new check, a log entry that changes a kernel file without a version bump after the cutoff is refused, and
   the repo's own logs pass (their violations are before the cutoffs).
3. No example output changes; the checklists may change only in evidence text (the map's version and notes).
4. 646 tests (one break test for the new check).

## Decisions
- D1 — F-063 answered first (ADR-O106): docs/versioning.md stands as written. Level: owner_default ADR under O101.
- D2 — docs/rules.yaml 4.0, as the written rule asks for R-35. Level: covered (ADR-O106).
- D3 — The bump check covers the schemas, library and kernel logs from each log's end at S-044; the 36, 21 and 47
  earlier changes that kept their version stay as written. Alternatives: check from the first entry (it would refuse
  history the append-only logs cannot change). Level: covered (F-078's fix, O64's rule).
- D4 — The library log reads a file's `version` when it has no `card_version`: 18 library files were logged as None.
  A latent bug found while building D3. Level: covered.
- D5 — The kernel log covers kernel/layer_order.yaml (created at 1.7); the knowledge map takes version 2. Level:
  covered (docs/versioning.md).
- D6 — README points to docs/layer_order.md; docs/layer_dependency.md carries a superseded banner and stays as history;
  ADR-O72, O73, O82 and O85 lose their stale phrases (records only; no decision changes). Level: covered.
- D7 — F-066 and F-028 are closed (built). F-015 stays open: the docs plane resolves a render finding only when a
  checklist code catches it, and none does yet (F-078 had proposed closing it). Level: covered (the gate's rule).
- D8 — The pre-commit hook goes to the owner: `make hooks` writes core.hooksPath into the repository config the
  worktree shares with ~/Documents/cinematic-compiler-core, which O52 keeps the agent from editing. Level: covered
  (O52).

## Duration
about 45 minutes

## Changes
- kernel/docs_plane.py (the bump check over every log), kernel/schema_log.py (layer_order.yaml in the kernel log; a
  library file's `version`); docs/rules.yaml 4.0 (docs log); kernel/knowledge_map.yaml version 2 and
  kernel/layer_order.yaml (kernel log)
- README.md, docs/layer_dependency.md, ADR-O72, O73, O82, O85; ADR-O106 (new)
- tests/test_docs_plane.py (new test)
- F-078, F-063, F-066, F-028 resolved; PLAN-004, PLAN-007; backlog 19 (RV-04 done, RV-07 next); CHANGELOG; the run
  report's owner list

## Verification
- before: 645 passed at 61e15cb (S-043's gate)
- after: `scripts/verify.sh` exit 0, 646 passed, docs plane PASS; every log verifies; no example output changed
- Prediction 1 held. Prediction 2 held (the break test's unbumped kernel change is refused; the repo's logs pass).
  Prediction 3 held. Prediction 4 held (646).

## Next
The principal review (finish.md section 6: eight slices since the run began), then RV-07.
