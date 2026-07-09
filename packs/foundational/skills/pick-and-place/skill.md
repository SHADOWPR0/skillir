---
id: core.pick-and-place
version: 0.1.0
title: Pick and Place
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

# Pick and Place

## Preconditions
The object and destination are visible, reachable, and inside the approved workspace.

## Steps
1. Inspect the object and destination.
   - action: perceive.inspect
   - observe: object pose and destination occupancy are available
   - verify: the object is graspable and the destination is clear
   - on_failure: safety.stop
   - evidence: authored:skillir:pick-and-place:step-1
2. Pick the object.
   - action: manip.pick
   - observe: grasp state and object motion are available
   - verify: the object is retained after the verification lift
   - on_failure: safety.stop
   - evidence: authored:skillir:pick-and-place:step-2
3. Place the object at the destination.
   - action: manip.place
   - observe: destination pose and release state are available
   - verify: the object is stable inside the destination tolerance
   - on_failure: safety.stop
   - evidence: authored:skillir:pick-and-place:step-3

## Success Criteria
The correct object is stable at the destination and the workspace has no collision event.

## Safe State
Stop in a collision-free pose, retain a stable load when safe, and request assistance.
