---
id: core.fixture-load
version: 0.1.0
title: Fixture Load
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

# Fixture Load

## Preconditions
The fixture is stopped, isolated as required, empty, and ready to receive the specified part.

## Steps
1. Inspect the part and fixture state.
   - action: perceive.inspect
   - observe: part identity, part pose, fixture occupancy, and fixture-ready signal are available
   - verify: the part matches the job and the fixture is empty and ready
   - on_failure: safety.stop
   - evidence: authored:skillir:fixture-load:step-1
2. Pick the specified part.
   - action: manip.pick
   - observe: grasp and part retention are available
   - verify: the correct part is retained in a stable grasp
   - on_failure: safety.stop
   - evidence: authored:skillir:fixture-load:step-2
3. Place the part in the fixture.
   - action: manip.place
   - observe: part pose relative to fixture references is available
   - verify: the part is seated within the job tolerance and the gripper is clear
   - on_failure: safety.stop
   - evidence: authored:skillir:fixture-load:step-3

## Success Criteria
The correct part is seated in the ready fixture within the specified pose tolerance.

## Safe State
Stop outside the fixture hazard zone and preserve isolation until the cell controller accepts the load.
