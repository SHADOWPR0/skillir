---
id: core.inventory-bin-sort
version: 0.1.0
title: Inventory Bin Sort
license: Apache-2.0
risk_class: low
maturity: robot_ir
profile: mobile-manipulator
required_capabilities:
  - perception.object
  - manipulation.pick
  - manipulation.place
source_refs:
  - authored:starter-pack
---

# Inventory Bin Sort

## Preconditions
The workspace is clear, target and destination bins are visible, and a safe stop path is available.

## Steps
1. Inspect the target item and destination bin.
   - action: perceive.inspect
   - observe: item identity and destination bin are visible
   - verify: confidence meets the local profile threshold
   - evidence: authored:starter-pack:step-1
2. Pick the target item.
   - action: manip.pick
   - observe: grasp remains stable during lift
   - verify: object is held without slip
   - on_failure: safety.stop
   - evidence: authored:starter-pack:step-2
3. Place the item in the destination bin.
   - action: manip.place
   - observe: destination is clear
   - verify: item is inside the destination bin
   - on_failure: safety.stop
   - evidence: authored:starter-pack:step-3

## Success Criteria
The target item is inside the destination bin, no collision occurs, and every step verification passes.

## Safe State
Stop motion, retain a stable load state, and wait in the designated safe pose.
