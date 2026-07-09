---
id: core.indicator-read-and-record
version: 0.1.0
title: Indicator Read and Record
license: Apache-2.0
risk_class: low
maturity: robot_ir
profile: fixed-manipulator
required_capabilities:
  - perception.object
source_refs:
  - authored:skillir:inspection-commons
---

# Indicator Read and Record

## Preconditions
The indicator identifier, expected format, valid range, units, and observation pose are specified.

## Steps
1. Inspect the indicator from the approved observation pose.
   - action: perceive.read_indicator
   - observe: indicator identifier, raw reading, units, confidence, and image evidence are available
   - verify: the reading format and units match the specification
   - on_failure: safety.stop
   - evidence: authored:skillir:indicator-read-and-record:step-1
2. Compare the reading with the allowed range.
   - action: verify.threshold
   - observe: parsed reading, allowed range, units, and confidence are available
   - verify: the result is classified as in-range, out-of-range, or unknown
   - on_failure: safety.stop
   - evidence: authored:skillir:indicator-read-and-record:step-2

## Success Criteria
The indicator has a timestamped reading, units, confidence, evidence reference, and range classification.

## Safe State
Remain outside the equipment hazard boundary and report unreadable or ambiguous indicators.
