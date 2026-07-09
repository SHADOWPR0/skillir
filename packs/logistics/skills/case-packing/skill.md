---
id: core.case-packing
version: 0.1.0
title: Case Packing
license: Apache-2.0
risk_class: medium
maturity: robot_ir
profile: fixed-manipulator
required_capabilities:
  - perception.object
  - manipulation.pick
  - manipulation.place
source_refs:
  - authored:skillir:logistics-commons
---

# Case Packing

## Preconditions
The case, packing pattern, product, and allowed quantity are identified and the case is supported and open.

## Steps
1. Inspect the product, case, and next packing position.
   - action: perceive.inspect
   - observe: product identifier, case identifier, occupancy, and target position are available
   - verify: product and case match the active packing assignment and capacity remains
   - on_failure: safety.stop
   - evidence: authored:skillir:case-packing:step-1
2. Pick one product unit.
   - action: manip.pick
   - observe: product identity, grasp state, and product condition are available
   - verify: one correct, visibly intact unit is retained
   - on_failure: safety.stop
   - evidence: authored:skillir:case-packing:step-2
3. Place the unit in the next packing position.
   - action: manip.place
   - observe: target position, neighboring units, and release state are available
   - verify: the unit is stable and does not exceed the case boundary
   - on_failure: safety.stop
   - evidence: authored:skillir:case-packing:step-3
4. Verify the case contents against the packing assignment.
   - action: verify.match
   - observe: expected and observed product identifiers and quantities are available
   - verify: contents match the current packing state or a discrepancy is reported
   - on_failure: safety.stop
   - evidence: authored:skillir:case-packing:step-4

## Success Criteria
The case contains the specified product and quantity in the approved pattern without visible damage.

## Safe State
Stop motion and preserve the association between the product, case, and packing assignment.
