---
id: core.tool-delivery
version: 0.1.0
title: Tool Delivery
license: Apache-2.0
risk_class: high
maturity: robot_ir
profile: humanoid-bimanual
required_capabilities:
  - perception.object
  - manipulation.pick
  - manipulation.place
  - mobility.navigate
  - interaction.confirm
source_refs:
  - authored:skillir:maintenance-commons
---

# Tool Delivery

## Preconditions
The tool, recipient, route, approved grasp, protective state, and handoff zone are specified.

## Steps
1. Inspect and verify the requested tool.
   - action: perceive.inspect
   - observe: tool identifier, visible condition, protective state, and grasp features are available
   - verify: the tool matches the request and is in its approved transport state
   - on_failure: safety.stop
   - evidence: authored:skillir:tool-delivery:step-1
2. Pick the tool using the approved transport grasp.
   - action: manip.pick
   - observe: grasp state, tool orientation, and protective state are available
   - verify: the tool is retained in the specified safe orientation
   - on_failure: safety.stop
   - evidence: authored:skillir:tool-delivery:step-2
3. Navigate to the recipient waiting zone.
   - action: nav.goto
   - observe: localization, route clearance, tool orientation, and recipient zone are available
   - verify: the robot reaches the correct zone while maintaining the transport envelope
   - on_failure: safety.stop
   - evidence: authored:skillir:tool-delivery:step-3
4. Request readiness and complete the approved handoff.
   - action: interact.ask_confirm
   - observe: intended recipient identity, readiness response, and timeout are available
   - verify: affirmative readiness is received before presentation
   - on_failure: safety.stop
   - evidence: authored:skillir:tool-delivery:step-4
5. Transfer the tool to the intended recipient.
   - action: tool.handoff
   - observe: recipient support, tool load transfer, and robot grasp state are available
   - verify: the recipient supports the tool before release
   - on_failure: safety.stop
   - evidence: authored:skillir:tool-delivery:step-5

## Success Criteria
The verified recipient supports the correct tool before release and the robot retreats without contact.

## Safe State
Retain the tool in its approved transport orientation, stop motion, and request human assistance.
