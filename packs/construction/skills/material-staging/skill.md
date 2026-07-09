---
id: core.material-staging
version: 0.1.0
title: Material Staging
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
  - authored:skillir:construction-commons
---

# Material Staging

## Preconditions
The material, quantity, route, staging zone, load limit, and stacking constraints are specified.

## Steps
1. Inspect the material and staging assignment.
   - action: perceive.inspect
   - observe: material identifier, visible condition, pickup pose, and destination are available
   - verify: the material matches the assignment and is within the approved load envelope
   - on_failure: safety.stop
   - evidence: authored:skillir:material-staging:step-1
2. Pick the assigned material unit.
   - action: manip.pick
   - observe: grasp state, load stability, and surrounding clearance are available
   - verify: the material is retained at the approved transport pose
   - on_failure: safety.stop
   - evidence: authored:skillir:material-staging:step-2
3. Navigate to the staging approach zone.
   - action: nav.goto
   - observe: route clearance, localization, and load stability are available
   - verify: the robot reaches the assigned approach zone without load shift
   - on_failure: safety.stop
   - evidence: authored:skillir:material-staging:step-3
4. Place the material in the assigned staging position.
   - action: manip.place
   - observe: zone boundary, support surface, neighboring materials, and release state are available
   - verify: the material is stable and satisfies spacing and stacking constraints
   - on_failure: safety.stop
   - evidence: authored:skillir:material-staging:step-4

## Success Criteria
The correct quantity is stable inside the assigned staging zone without violating load or stacking constraints.

## Safe State
Stop outside active work and travel zones while retaining or placing the load in an approved stable state.
