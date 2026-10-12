# F-217 — Testing an exported commit imports the live worktree's modules

<!-- docs-version: 1.0 -->

## Type
risk

## Severity
medium

## Layer
all

## Status
open

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the rules reviewer, S-081: the venv's editable finder resolves modules missing from an exported tree to the live
  worktree; test_the_caps_are_the_owner_s passed on 65d77ee, which has no prompt_length.py
- self_audit.md's 're-run the new test on the commit before' is exposed to the same leak

## Description
A test run on an old or exported tree can pass by importing today's code.

## Impact
A self-audit can certify a test against its parent wrongly.

## Proposed Fix
Backlog RV-104: a script runs a commit's tests in an exported tree with an isolated path (no editable finder), and
self_audit.md names it.

## Owner Ruling
none needed

## Related
- F-180
- RV-104
- RV-77

## Resolution
Open.
