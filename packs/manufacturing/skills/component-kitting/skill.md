---
id: core.component-kitting
version: 0.1.0
title: Component Kitting
license: Apache-2.0
risk_class: medium
maturity: robot_ir
profile: fixed-manipulator
required_capabilities:
  - perception.object
  - manipulation.pick
  - manipulation.place
source_refs:
  - authored:skillir:manufacturing-commons
---

# Component Kitting

## Preconditions
The bill of materials, source bins, kit container, and required quantities are identified and accessible.

## Steps
1. Inspect the open kit assignment and source component.
   - action: perceive.inspect
   - observe: kit identifier, part identifier, source bin, and remaining quantity are available
   - verify: the observed part and source match the next open kit line
   - on_failure: safety.stop
   - evidence: authored:skillir:component-kitting:step-1
2. Pick one assigned component.
   - action: manip.pick
   - observe: part identity, grasp state, and neighboring component motion are available
   - verify: one correct component is retained without disturbing adjacent inventory
   - on_failure: safety.stop
   - evidence: authored:skillir:component-kitting:step-2
3. Place the component in the assigned kit position.
   - action: manip.place
   - observe: kit identifier, target compartment, and release state are available
   - verify: the component is stable in the correct kit compartment
   - on_failure: safety.stop
   - evidence: authored:skillir:component-kitting:step-3
4. Verify the completed kit line.
   - action: verify.match
   - observe: expected and observed part identifiers and quantities are available
   - verify: the kit line is complete or remains explicitly open
   - on_failure: safety.stop
   - evidence: authored:skillir:component-kitting:step-4

## Success Criteria
Every processed kit line contains the correct component and quantity in its assigned compartment.

## Safe State
Stop motion, preserve kit identity, and place any held component in an approved recovery location.
