# F-234 — A kernel prop rule is applied to every prop, whatever props it names

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
high

## Layer
all

## Status
open

## Reported
2026-10-13

## Reporter
agent

## Legacy ID
—

## Evidence
- S03 (compiler/passes/mandatory/p03_constraint.py) applies a `kernel_prop` rule to every prop in the scene. The UGC
  example's envelope holds `c_k_rules_24` ("FIVE props tracked separately, never merged: kunai, rope_dart, ...")
  applied to the glasses, its only prop; its `reference_labels` name five props the scene does not hold.
- Found when S-117 printed the kernel invariants (ADR-O113): COUNT_CONTRADICTION refused the UGC prompt ("'FIVE
  props' but the scene has 1").

## Description
A rule that names props is the same class as R20's kunai: printed, it invites a prop the scene does not hold.

## Impact
No prompt printed it before S-117. S17 now leaves out any rule whose `reference_labels` name something the scene does
not hold, so no prompt prints it; the envelope still applies it.

## Proposed Fix
R20 next action 1 (S03): a kernel or card rule that names a prop not in the scene is not applied.

## Owner Ruling
—

## Related
- F-230
- ADR-O113

## Resolution
—
