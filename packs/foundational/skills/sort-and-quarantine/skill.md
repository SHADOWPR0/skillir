---
id: core.sort-and-quarantine
version: 0.1.0
title: Sort and Quarantine
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

# Sort and Quarantine

## Preconditions
The item, normal destination, and quarantine destination are assigned and accessible.

## Steps
1. Inspect and classify the item against the acceptance criteria.
   - action: perceive.inspect
   - observe: required item attributes and inspection confidence are available
   - verify: the item is classified as accepted, rejected, or unknown
   - on_failure: safety.stop
   - evidence: authored:skillir:sort-and-quarantine:step-1
2. Pick the classified item.
   - action: manip.pick
   - observe: item identity, grasp state, and retention are available
   - verify: the inspected item is retained in a stable grasp
   - on_failure: safety.stop
   - evidence: authored:skillir:sort-and-quarantine:step-2
3. Navigate to the destination selected by the classification result.
   - action: nav.goto
   - observe: selected destination, route clearance, and load stability are available
   - verify: rejected or unknown items route only to quarantine
   - on_failure: safety.stop
   - evidence: authored:skillir:sort-and-quarantine:step-3
4. Place the item in the selected destination.
   - action: manip.place
   - observe: destination identity, occupancy, and release state are available
   - verify: the item is stable in the classification-appropriate destination
   - on_failure: safety.stop
   - evidence: authored:skillir:sort-and-quarantine:step-4

## Success Criteria
The inspected item is stable in the accepted destination or quarantine according to its recorded result.

## Safe State
Stop in a designated safe zone and retain unknown items under quarantine control.
