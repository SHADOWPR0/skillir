---
id: core.tote-transfer
version: 0.1.0
title: Tote Transfer
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

# Tote Transfer

## Preconditions
The tote is within the approved load limit and the source, route, and destination are available.

## Steps
1. Inspect the tote and destination assignment.
   - action: perceive.inspect
   - observe: tote identity, grasp features, and destination identifier are available
   - verify: the tote matches the assignment and is within the approved envelope
   - on_failure: safety.stop
   - evidence: authored:skillir:tote-transfer:step-1
2. Pick the tote.
   - action: manip.pick
   - observe: grasp state and load stability are available
   - verify: the tote is retained and stable at transport height
   - on_failure: safety.stop
   - evidence: authored:skillir:tote-transfer:step-2
3. Navigate to the assigned destination.
   - action: nav.goto
   - observe: route clearance, localization, and load stability are available
   - verify: the robot reaches the destination approach zone without losing the load
   - on_failure: safety.stop
   - evidence: authored:skillir:tote-transfer:step-3
4. Place the tote in the destination position.
   - action: manip.place
   - observe: destination occupancy and tote pose are available
   - verify: the tote is stable inside the destination tolerance
   - on_failure: safety.stop
   - evidence: authored:skillir:tote-transfer:step-4

## Success Criteria
The assigned tote is stable at the assigned destination and the route remains incident-free.

## Safe State
Stop in a designated safe zone while maintaining a stable load or stable placed state.
