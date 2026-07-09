---
id: core.fixture-unload
version: 0.1.0
title: Fixture Unload
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

# Fixture Unload

## Preconditions
The fixture cycle is complete, motion is stopped, and unloading is permitted by the cell controller.

## Steps
1. Inspect the fixture and completed part.
   - action: perceive.inspect
   - observe: completion state, part identity, and part pose are available
   - verify: the cycle is complete and the expected part is ready for removal
   - on_failure: safety.stop
   - evidence: authored:skillir:fixture-unload:step-1
2. Pick the completed part from the fixture.
   - action: manip.pick
   - observe: grasp, extraction path, and part retention are available
   - verify: the part clears the fixture and remains stable
   - on_failure: safety.stop
   - evidence: authored:skillir:fixture-unload:step-2
3. Place the part in the designated output location.
   - action: manip.place
   - observe: output location occupancy and release state are available
   - verify: the part is stable in the correct output location
   - on_failure: safety.stop
   - evidence: authored:skillir:fixture-unload:step-3

## Success Criteria
The fixture is empty and the completed part is stable in the designated output location.

## Safe State
Stop outside the fixture hazard zone and do not authorize another cycle.
