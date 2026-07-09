---
id: core.object-inspection
version: 0.1.0
title: Object Inspection
license: Apache-2.0
risk_class: low
maturity: robot_ir
profile: fixed-manipulator
required_capabilities:
  - perception.object
source_refs:
  - authored:skillir:foundational-commons
---

# Object Inspection

## Preconditions
The inspection area is visible, illuminated, and clear of moving equipment.

## Steps
1. Inspect the target object from the designated observation pose.
   - action: perceive.inspect
   - observe: object identity, pose, and visible condition are available
   - verify: the observation meets the local confidence and image-quality thresholds
   - on_failure: safety.stop
   - evidence: authored:skillir:object-inspection:step-1
2. Compare the observation with the expected object description.
   - action: verify.match
   - observe: expected and observed attributes are available
   - verify: every required attribute has a pass, fail, or unknown result
   - on_failure: safety.stop
   - evidence: authored:skillir:object-inspection:step-2

## Success Criteria
The target has an inspection result with no required attribute left unclassified.

## Safe State
Stop motion at the observation pose and report the unresolved attribute.
