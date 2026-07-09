---
id: core.tote-consolidation
version: 0.1.0
title: Tote Consolidation
license: Apache-2.0
risk_class: medium
maturity: robot_ir
profile: fixed-manipulator
required_capabilities:
  - perception.object
  - manipulation.pick
  - manipulation.place
source_refs:
  - authored:skillir:foundational-commons
---

# Tote Consolidation

## Preconditions
The source and destination totes share an approved consolidation assignment and the destination has capacity.

## Steps
1. Inspect both totes and the next assigned item.
   - action: perceive.inspect
   - observe: tote identities, item identity, and destination capacity are available
   - verify: the assignment matches both totes and sufficient capacity remains
   - on_failure: safety.stop
   - evidence: authored:skillir:tote-consolidation:step-1
2. Pick the assigned item from the source tote.
   - action: manip.pick
   - observe: item identity, grasp state, and neighboring item motion are available
   - verify: the correct item is retained without displacing neighboring items
   - on_failure: safety.stop
   - evidence: authored:skillir:tote-consolidation:step-2
3. Place the item in the destination tote.
   - action: manip.place
   - observe: free space, item pose, and release state are available
   - verify: the item is stable within the destination tote boundary
   - on_failure: safety.stop
   - evidence: authored:skillir:tote-consolidation:step-3

## Success Criteria
The assigned item is stable in the correct destination tote and tote capacity is not exceeded.

## Safe State
Stop motion, preserve tote identities, and retain or place the item in a stable approved location.
