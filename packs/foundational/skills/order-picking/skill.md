---
id: core.order-picking
version: 0.1.0
title: Order Picking
license: Apache-2.0
risk_class: medium
maturity: robot_ir
profile: mobile-manipulator
required_capabilities:
  - perception.object
  - manipulation.pick
  - manipulation.place
  - mobility.navigate
source_refs:
  - authored:skillir:foundational-commons
---

# Order Picking

## Preconditions
The order line, source location, and order tote are assigned and accessible.

## Steps
1. Navigate to the assigned source location.
   - action: nav.goto
   - observe: localization, route clearance, and source identifier are available
   - verify: the robot reaches the correct source approach zone
   - on_failure: safety.stop
   - evidence: authored:skillir:order-picking:step-1
2. Inspect the requested item and quantity.
   - action: perceive.inspect
   - observe: item identifier, visible quantity, and grasp candidates are available
   - verify: the item matches the open order line
   - on_failure: safety.stop
   - evidence: authored:skillir:order-picking:step-2
3. Pick the requested item.
   - action: manip.pick
   - observe: item identity, grasp state, and retention are available
   - verify: the correct item is retained in a stable grasp
   - on_failure: safety.stop
   - evidence: authored:skillir:order-picking:step-3
4. Place the item in the assigned order tote.
   - action: manip.place
   - observe: tote identity, occupancy, and release state are available
   - verify: the item is stable inside the correct tote
   - on_failure: safety.stop
   - evidence: authored:skillir:order-picking:step-4

## Success Criteria
The correct item and quantity are stable in the tote assigned to the open order line.

## Safe State
Stop in a designated safe zone and preserve item-to-order custody information.
