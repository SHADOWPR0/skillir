---
id: core.asset-condition-survey
version: 0.1.0
title: Asset Condition Survey
license: Apache-2.0
risk_class: medium
maturity: robot_ir
profile: mobile-manipulator
required_capabilities:
  - perception.object
  - mobility.navigate
source_refs:
  - authored:skillir:maintenance-commons
---

# Asset Condition Survey

## Preconditions
The asset list, observation poses, access permissions, and visible inspection criteria are assigned.

## Steps
1. Navigate to the next approved observation pose.
   - action: nav.goto
   - observe: localization, route clearance, asset identifier, and pose identifier are available
   - verify: the robot reaches the correct observation pose without entering an exclusion zone
   - on_failure: safety.stop
   - evidence: authored:skillir:asset-condition-survey:step-1
2. Inspect the visible asset surfaces and indicators.
   - action: perceive.inspect
   - observe: required views, visible condition attributes, and image quality are available
   - verify: every required view is captured or explicitly marked unavailable
   - on_failure: safety.stop
   - evidence: authored:skillir:asset-condition-survey:step-2
3. Compare observations with the inspection criteria.
   - action: verify.match
   - observe: expected and observed visible attributes are available
   - verify: each criterion is classified as pass, fail, or unknown
   - on_failure: safety.stop
   - evidence: authored:skillir:asset-condition-survey:step-3

## Success Criteria
Every assigned asset view has a traceable pass, fail, unknown, or inaccessible result.

## Safe State
Stop at an approved observation or waiting pose and report incomplete coverage.
