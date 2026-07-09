---
id: core.point-to-point-delivery
version: 0.1.0
title: Point-to-Point Delivery
license: Apache-2.0
risk_class: medium
maturity: robot_ir
profile: mobile-load-carrier
required_capabilities:
  - perception.object
  - mobility.navigate
source_refs:
  - authored:skillir:foundational-commons
---

# Point-to-Point Delivery

## Preconditions
The load is secured by an approved mechanism and the destination and route are assigned.

## Steps
1. Inspect the secured load and destination assignment.
   - action: perceive.inspect
   - observe: load identifier, secure-state indicator, and destination identifier are available
   - verify: the load matches the assignment and reports a secure state
   - on_failure: safety.stop
   - evidence: authored:skillir:point-to-point-delivery:step-1
2. Navigate to the destination approach zone.
   - action: nav.goto
   - observe: localization, route clearance, and load secure state are available
   - verify: the robot reaches the assigned zone without a safety or load fault
   - on_failure: safety.stop
   - evidence: authored:skillir:point-to-point-delivery:step-2
3. Verify the destination before releasing custody.
   - action: verify.match
   - observe: assigned and observed destination identifiers are available
   - verify: the observed destination matches the assignment
   - on_failure: safety.stop
   - evidence: authored:skillir:point-to-point-delivery:step-3

## Success Criteria
The correct secured load arrives at the correct destination with no route or load fault.

## Safe State
Stop in the nearest approved waiting zone and retain custody of the load.
