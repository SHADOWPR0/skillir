---
id: core.operator-confirmed-handoff
version: 0.1.0
title: Operator-Confirmed Handoff
license: Apache-2.0
risk_class: high
maturity: robot_ir
profile: humanoid-bimanual
required_capabilities:
  - perception.object
  - manipulation.place
  - interaction.confirm
source_refs:
  - authored:skillir:foundational-commons
---

# Operator-Confirmed Handoff

## Preconditions
The handoff object is approved, the operator is in the designated interaction zone, and a safe retreat path is clear.

## Steps
1. Inspect the object and handoff zone.
   - action: perceive.inspect
   - observe: object identity, operator presence, and interaction-zone clearance are available
   - verify: the correct object and one intended recipient are identified
   - on_failure: safety.stop
   - evidence: authored:skillir:operator-confirmed-handoff:step-1
2. Request explicit readiness confirmation.
   - action: interact.ask_confirm
   - observe: a local readiness response and timeout state are available
   - verify: an affirmative response is received from the intended recipient
   - on_failure: safety.stop
   - evidence: authored:skillir:operator-confirmed-handoff:step-2
3. Present and release the object using the approved handoff behavior.
   - action: tool.handoff
   - observe: recipient contact, load transfer, and robot grasp state are available
   - verify: the recipient supports the object before the robot releases it
   - on_failure: safety.stop
   - evidence: authored:skillir:operator-confirmed-handoff:step-3

## Success Criteria
The intended recipient supports the correct object before release and the robot retreats without contact.

## Safe State
Retain the object, stop motion, increase separation when safe, and request human assistance.
