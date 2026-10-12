# F-069 — Nine airborne spans hang longer than gravity allows

<!-- docs-version: 1.0 -->

## Type
question

## Severity
medium

## Layer
L4a

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
—

## Evidence
- the S-018 prototype (ADR-O74's arc) over the four examples' envelopes (S11 support, S13 roots); these keys sit
  more than 0.3 m off the arc through their span's takeoff and landing roots:
- ninja_broad@b13 at 5.10: root y 1.0, the arc from the takeoff and landing keys gives 2.35 (airborne 4.70-6.30)
- ninja_broad@b14 at 5.50: root y 0.8, the arc from the takeoff and landing keys gives 3.14 (airborne 4.70-6.30)
- ninja_broad@b15 at 5.90: root y 0, the arc from the takeoff and landing keys gives 2.35 (airborne 4.70-6.30)
- ninja_lean from 0.00: airborne run without a takeoff or landing key (ninja_lean@b01)
- ninja_lean@b04 at 1.60: root y 3.2, the arc from the takeoff and landing keys gives 6.99 (airborne 1.10-3.00)
- ninja_lean@b05 at 2.00: root y 2.5, the arc from the takeoff and landing keys gives 7.21 (airborne 1.10-3.00)
- ninja_lean@b06 at 2.50: root y 1.5, the arc from the takeoff and landing keys gives 5.28 (airborne 1.10-3.00)
- ninja_lean@b12 at 4.70: root y 1.4, the arc from the takeoff and landing keys gives 2.77 (airborne 4.40-5.90)
- ninja_lean@b13 at 5.10: root y 2.2, the arc from the takeoff and landing keys gives 3.61 (airborne 4.40-5.90)
- ninja_lean@b14 at 5.50: root y 1.8, the arc from the takeoff and landing keys gives 2.89 (airborne 4.40-5.90)
- ninja_lean@b16 at 6.30: root y 1.5, the arc from the takeoff and landing keys gives 2.95 (airborne 5.90-7.50)
- ninja_lean@b17 at 6.60: root y 1.8, the arc from the takeoff and landing keys gives 3.69 (airborne 5.90-7.50)
- ninja_lean@b18 at 7.00: root y 2.8, the arc from the takeoff and landing keys gives 3.3 (airborne 5.90-7.50)
- ninja_lean@b21 at 8.50: root y 1.5, the arc from the takeoff and landing keys gives 1.88 (airborne 8.00-9.00)
- acrobat@b03 at 1.60: root y 1.2, the arc from the takeoff and landing keys gives 1.96 (airborne 1.20-2.60)
- acrobat@b04 at 2.00: root y 1.0, the arc from the takeoff and landing keys gives 2.35 (airborne 1.20-2.60)
- acrobat@b07 at 4.60: root y 1.2, the arc from the takeoff and landing keys gives 3.51 (airborne 3.60-5.20)
- acrobat@b13 at 9.40: root y 1.0, the arc from the takeoff and landing keys gives 1.57 (airborne 8.60-9.80)

## Description
The examples' aerial spans were authored before any momentum check; their timing and heights do not fit one gravity
arc, and nothing declares a stylised hang.

## Impact
MOMENTUM_MISSING (M9-09b) cannot land without re-authoring spans no ruling covers; renders show late takeoffs and
floating bodies (F-036, R6-R19: aerial events about 0.75-2.7 s late).

## Proposed Fix
Rule on ADR-O74 (recommended: anime declares hang time per span; other genres follow the arc).

## Owner Ruling
ADR-O74

## Related
- ADR-O74
- F-026
- F-036
- PLAN-003

## Resolution
Open.
