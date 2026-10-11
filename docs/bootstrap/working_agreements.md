# Working agreements with the owner

How the owner (Kingsley) wants the work done, from the owner's own words in the sessions. The formal rules are in
[../rules.md](../rules.md); these are the habits around them.

## Talking to the owner

- Answer first, in plain English, short. Tables and numbered steps; no walls of text.
- The owner is not a terminal user: give one command per `bash` block, and do the running yourself.
- When the owner asks a question in the middle of a task ("how many slices are left?"), answer it before going on.
- Ask only where the DAG, the rules or a ruling are silent or contradict each other, in one line each, with a
  recommended option. Otherwise act (ADR-S4).

## Every slice

1. Read the state (bootstrap, AGENTS.md, indexes); run the gate before changing anything.
2. Write the session file with numbered predictions before the change.
3. Build at the layer that owns the data; add the check, its break tests and a should-not-fire run.
4. Gate, `make docs`, then the self-audit (`/self-audit`). Report which predictions held and which failed, plainly.
5. Show the diff. Commit only on "commit it"; push only on "push it". "Commit it, then start X" approves that one
   commit and the start of X, not a push. An autopilot run (`/autopilot`, ADR-O70) is the exception for commits:
   the owner's invocation is the "commit it" for each slice that clears the gate and the self-audit, for that run
   only. It never covers a push.
6. One slice per commit; never mix two sessions' work in one commit.
7. Log every decision with its reason in the session file's Decisions section (R-32): covered (cite the rule or
   ruling), interpretation (labelled in the code, added to F-053) or the owner's call (a proposed ADR).

## Always

- Never render and never call a paid model API: the owner renders and sends the video; log it verbatim with
  Claude's frame notes apart.
- Graft and graphify before reading files; read only the lines you need.
- Every owner ruling becomes an ADR in `docs/decisions/` (the next free number is in [state.md](state.md)).
- Test the uncertain, build the certain (ADR-O46): a render probe only for what is uncertain and visual.
- The repo is the source of truth; a memory or a summary is a claim to check.
