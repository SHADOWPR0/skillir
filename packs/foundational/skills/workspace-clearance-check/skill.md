---
id: core.workspace-clearance-check
version: 0.1.0
title: Workspace Clearance Check
license: Apache-2.0
risk_class: low
maturity: robot_ir
profile: fixed-manipulator
required_capabilities:
  - perception.object
source_refs:
  - authored:skillir:foundational-commons
---

# Workspace Clearance Check

## Preconditions
The robot remains stopped and the complete controlled workspace can be observed.

## Steps
1. Inspect the controlled workspace and exclusion zones.
   - action: perceive.inspect
   - observe: workspace boundary, expected fixtures, people, and unexpected objects are available
   - verify: every required zone has a current observation or an explicit unknown state
   - on_failure: safety.stop
   - evidence: authored:skillir:workspace-clearance-check:step-1
2. Compare observed occupancy with the approved workspace state.
   - action: verify.match
   - observe: approved and observed occupancy states are available
   - verify: the workspace is classified as clear, blocked, or unknown
   - on_failure: safety.stop
   - evidence: authored:skillir:workspace-clearance-check:step-2

## Success Criteria
Every required zone is classified and only a clear result permits a downstream task to proceed.

## Safe State
Keep the robot stopped and prevent downstream motion authorization.
