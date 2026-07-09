---
id: core.waste-bin-service
version: 0.1.0
title: Waste Bin Service
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
  - authored:skillir:facilities-commons
---

# Waste Bin Service

## Preconditions
The bin type, load limit, approved pickup features, route, destination, and contamination controls are specified.

## Steps
1. Inspect the bin and service assignment.
   - action: perceive.inspect
   - observe: bin identifier, fill state, visible damage, pickup features, and destination are available
   - verify: the bin matches the assignment and remains within the approved handling envelope
   - on_failure: safety.stop
   - evidence: authored:skillir:waste-bin-service:step-1
2. Pick the bin using the approved handling features.
   - action: manip.pick
   - observe: grasp state, load stability, and leakage or deformation indicators are available
   - verify: the bin is retained without visible spill or structural fault
   - on_failure: safety.stop
   - evidence: authored:skillir:waste-bin-service:step-2
3. Navigate to the assigned service destination.
   - action: nav.goto
   - observe: localization, route clearance, and bin stability are available
   - verify: the robot reaches the destination approach zone without spill or route fault
   - on_failure: safety.stop
   - evidence: authored:skillir:waste-bin-service:step-3
4. Place the bin in the assigned destination position.
   - action: manip.place
   - observe: destination boundary, support state, and release state are available
   - verify: the bin is upright and stable inside the destination boundary
   - on_failure: safety.stop
   - evidence: authored:skillir:waste-bin-service:step-4

## Success Criteria
The assigned bin is upright and stable at the correct destination with no visible spill or handling fault.

## Safe State
Stop motion, keep the bin upright when possible, and isolate any suspected spill or damaged container.
