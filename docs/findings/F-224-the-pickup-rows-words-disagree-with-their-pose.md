# F-224 — The pickup rows' words disagree with their pose under the printed legend

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
medium

## Layer
L6

## Status
open

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- Principal review 7 (S-090, the golden), re-run by the builder: at 8.0 A's right arm, "side mid ... taking the kunai
  from the ground", points 56 degrees below horizontal; at 7.5 the left arm, "fwd mid ... taking the rope dart from
  the ground", 86 degrees below; the printed legend reads a limb "mid" while within 45 degrees of horizontal
  (prose_mixed.txt:13). Before S-083 both read "fwd low".
- "head facing B" at 7.5: A's face heads -32.6 degrees while B's torso lies at +51.4 degrees from A's head, 84 degrees
  off (61 at review 6).
- S-083 D4 worded the rows in the trunk's frame (DEV-10); F-111 (which frame limb words are read in) waits for the
  owner.

## Description
S-083 worded the pickup rows in the trunk's frame; the legend the prompt prints reads them in the world's, where they
are wrong.

## Impact
The prompt says mid where the arm hangs low, and facing B where the head looks away.

## Proposed Fix
RV-95b: word the rows in the legend's frame until the owner answers F-111, and aim the head at B (RV-15c's check,
RV-103b) or drop "facing B".

## Owner Ruling
F-111 (the frame) is open

## Related
- F-111
- DEV-10
- RV-95b
- RV-15c

## Resolution
Open.
