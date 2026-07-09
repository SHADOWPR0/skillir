---
id: core.tray-delivery
version: 0.1.0
title: Tray Delivery
license: Apache-2.0
risk_class: medium
maturity: robot_ir
profile: mobile-load-carrier
required_capabilities:
  - perception.object
  - mobility.navigate
source_refs:
  - authored:skillir:service-commons
---

# Tray Delivery

## Preconditions
The tray is secured, destination is confirmed, route is approved, and spill or temperature controls are satisfied locally.

## Steps
1. Inspect the secured tray and delivery assignment.
   - action: perceive.inspect
   - observe: tray identifier, secure-state indicator, and destination identifier are available
   - verify: the tray matches the assignment and reports a secure state
   - on_failure: safety.stop
   - evidence: authored:skillir:tray-delivery:step-1
2. Navigate to the destination waiting zone.
   - action: nav.goto
   - observe: localization, route clearance, tray state, and destination identifier are available
   - verify: the robot reaches the correct zone without tray or route fault
   - on_failure: safety.stop
   - evidence: authored:skillir:tray-delivery:step-2
3. Verify the delivery destination.
   - action: verify.match
   - observe: assigned and observed destination identifiers are available
   - verify: destination identity matches before custody is released
   - on_failure: safety.stop
   - evidence: authored:skillir:tray-delivery:step-3

## Success Criteria
The correct secured tray reaches the verified destination without a route, load, or spill-state fault.

## Safe State
Stop in an approved waiting zone and retain custody of the secured tray.
