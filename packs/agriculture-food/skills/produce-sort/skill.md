---
id: core.produce-sort
version: 0.1.0
title: Produce Sort
license: Apache-2.0
risk_class: medium
maturity: robot_ir
profile: fixed-manipulator
required_capabilities:
  - perception.object
  - manipulation.pick
  - manipulation.place
source_refs:
  - authored:skillir:agriculture-food-commons
---

# Produce Sort

## Preconditions
The produce class, visible grading criteria, destination containers, handling limits, and hygiene state are specified.

## Steps
1. Inspect one produce item against the visible grading criteria.
   - action: perceive.inspect
   - observe: item identity, visible attributes, pose, and inspection confidence are available
   - verify: the item is assigned an accepted, rejected, or unknown grade
   - on_failure: safety.stop
   - evidence: authored:skillir:produce-sort:step-1
2. Pick the inspected item within the handling limits.
   - action: manip.pick
   - observe: item identity, grasp state, and visible deformation are available
   - verify: the item is retained without exceeding the approved handling envelope
   - on_failure: safety.stop
   - evidence: authored:skillir:produce-sort:step-2
3. Place the item in the grade-appropriate destination.
   - action: manip.place
   - observe: destination identifier, occupancy, drop distance, and release state are available
   - verify: accepted items enter the assigned grade container and unknown items enter review
   - on_failure: safety.stop
   - evidence: authored:skillir:produce-sort:step-3

## Success Criteria
Each processed item is traceably placed in its accepted, rejected, or review destination within handling limits.

## Safe State
Stop contact, preserve hygiene controls, and route unknown items to the review destination.
