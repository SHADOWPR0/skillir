---
id: core.shelf-replenishment
version: 0.1.0
title: Shelf Replenishment
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

# Shelf Replenishment

## Preconditions
The replenishment item and shelf location are assigned, visible, reachable, and approved for access.

## Steps
1. Inspect the item and shelf assignment.
   - action: perceive.inspect
   - observe: item identifier, shelf identifier, and destination occupancy are available
   - verify: the item matches the shelf assignment and sufficient space is available
   - on_failure: safety.stop
   - evidence: authored:skillir:shelf-replenishment:step-1
2. Pick the assigned item.
   - action: manip.pick
   - observe: grasp and item retention are available
   - verify: the correct item is held in a stable grasp
   - on_failure: safety.stop
   - evidence: authored:skillir:shelf-replenishment:step-2
3. Navigate to the shelf approach zone.
   - action: nav.goto
   - observe: localization, route clearance, and load stability are available
   - verify: the robot reaches the approved shelf approach pose
   - on_failure: safety.stop
   - evidence: authored:skillir:shelf-replenishment:step-3
4. Place the item at the assigned shelf position.
   - action: manip.place
   - observe: item pose, neighboring items, and release state are available
   - verify: the item is stable, correctly oriented, and within the shelf boundary
   - on_failure: safety.stop
   - evidence: authored:skillir:shelf-replenishment:step-4

## Success Criteria
The assigned item is stable in the correct shelf position without disturbing neighboring items.

## Safe State
Stop outside the shelf interaction zone and report any unresolved placement obstruction.
