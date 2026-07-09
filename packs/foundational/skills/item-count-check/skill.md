---
id: core.item-count-check
version: 0.1.0
title: Item Count Check
license: Apache-2.0
risk_class: low
maturity: robot_ir
profile: fixed-manipulator
required_capabilities:
  - perception.object
source_refs:
  - authored:skillir:foundational-commons
---

# Item Count Check

## Preconditions
The count region is visible and items are sufficiently separated or otherwise countable by the local perception system.

## Steps
1. Inspect the complete count region.
   - action: perceive.inspect
   - observe: region boundary, visible items, and occlusion state are available
   - verify: the entire required region is covered and unresolved occlusion is reported
   - on_failure: safety.stop
   - evidence: authored:skillir:item-count-check:step-1
2. Compare the observed count with the expected count.
   - action: verify.match
   - observe: observed count, expected count, and confidence are available
   - verify: the result is classified as match, mismatch, or unknown
   - on_failure: safety.stop
   - evidence: authored:skillir:item-count-check:step-2

## Success Criteria
The count has a traceable match, mismatch, or unknown result with no hidden unresolved region.

## Safe State
Remain at the observation pose and request a recount when the result is unknown.
