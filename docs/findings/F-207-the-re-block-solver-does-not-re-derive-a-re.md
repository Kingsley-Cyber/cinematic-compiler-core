# F-207 — The re-block solver does not re-derive a re-block from its record

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
high

## Layer
L4c

## Status
open

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- S-081: from the pre-S-080 8.0 key and S-080's recorded goals the solver lands exactly in the recorded joint order
  and 28.6 degrees off with the order reversed (checked); the 7.5 key comes no closer than 29.6 degrees in 26 readings
  of its record (rules reviewer)
- tests/test_reblock.py and F-127's resolution 're-derive' S-078's keys with each outcome's own sole height as the
  goal; with independent goals (the sole on the floor) the solver gives LUL -38.5 where S-078 committed -70.17;
  S-078's values are hand steps of exactly 15 degrees
- solver/reblock.py's docstring says the solve stays inside the genre's joint limits; neither solve() nor the CLI
  loads them; the CLI parses no goal weight and starts from the current, already re-blocked key

## Description
The committed solver is a coordinate pattern search whose answer depends on the order of its free joints, and its
records omit the start state, the order and the weights, so a recorded re-block cannot be re-derived; the claim that
it re-derives S-078 is circular.

## Impact
Re-blocks stay unrepeatable, the class F-127 was filed for.

## Proposed Fix
Backlog RV-96: an order-independent search (the best move among all free components at each step), the genre's joint
limits as default bounds, the CLI taking a start key, weighted goals and its free set, every re-block recorded as that
command and re-derived by a test from the pre-re-block key; S-078's three values re-derived from independent goals or
recorded as hand choices.

## Owner Ruling
none needed

## Related
- F-127
- F-206
- RV-96
- RV-35b

## Resolution
Open.
