---
id: core.surface-wipe
version: 0.1.0
title: Surface Wipe
license: Apache-2.0
risk_class: medium
maturity: robot_ir
profile: mobile-manipulator
required_capabilities:
  - perception.object
  - manipulation.pick
  - manipulation.place
  - manipulation.surface_contact
source_refs:
  - authored:skillir:facilities-commons
---

# Surface Wipe

## Preconditions
The surface, approved tool, cleaning agent, contact limits, exclusion zones, and waste destination are specified.

## Steps
1. Inspect the surface, obstacles, and approved cleaning tool.
   - action: perceive.inspect
   - observe: surface boundary, obstacle map, tool identity, and visible soil state are available
   - verify: the surface and tool match the assignment and forbidden contact zones are identified
   - on_failure: safety.stop
   - evidence: authored:skillir:surface-wipe:step-1
2. Pick the approved cleaning tool.
   - action: manip.pick
   - observe: tool identity, grasp state, and tool condition are available
   - verify: the correct tool is retained and ready for contact
   - on_failure: safety.stop
   - evidence: authored:skillir:surface-wipe:step-2
3. Wipe the assigned surface using the approved path and contact envelope.
   - action: manip.wipe
   - observe: tool pose, contact state, force estimate, path coverage, and obstacles are available
   - verify: required coverage is reached without exceeding contact or workspace limits
   - on_failure: safety.stop
   - evidence: authored:skillir:surface-wipe:step-3
4. Place the used tool in the assigned recovery or waste position.
   - action: manip.place
   - observe: destination identity, occupancy, and release state are available
   - verify: the used tool is stable in the correct destination
   - on_failure: safety.stop
   - evidence: authored:skillir:surface-wipe:step-4

## Success Criteria
The assigned surface coverage is complete, contact limits are respected, and the used tool is contained correctly.

## Safe State
Break contact, stop motion, contain the cleaning tool, and preserve any chemical or contamination controls.
