# Safety and Evidence Policy

Skill IR compiles evidence; it does not certify machinery or replace independent
safety controls.

## Non-negotiable gates

- Preserve source provenance for every safety-critical assertion.
- Block unresolved actions, missing safe states, unknown units, unsupported
  profiles, and missing success criteria.
- Keep motion limits, watchdogs, interlocks, and physical stops outside any
  language-model or skill-interpreter process.
- Quarantine bundles after a changed robot, controller, tool, calibration,
  firmware, source procedure, material environment, incident, or expired approval.
- Never allow a critical-gate force bypass.

## Restricted human-contact extensions

Restricted extensions are disabled by default and distributed separately. They
require adult-only access, specific and revocable consent, independent stop
channels, product-tested contact limits, no recording by default, and qualified
review. The core repository contains policy schemas and synthetic tests only.
