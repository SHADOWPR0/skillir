# Adapter SDK Contract

An adapter binds portable Skill IR primitives to a concrete controller,
robotics middleware stack, behavior tree, motion planner, simulator, dataset
generator, or policy runtime. It does not modify the meaning of the source
skill.

The public core currently supplies only a deterministic mock. Target adapters
may remain private and may be implemented as Python entry points or isolated
JSON-RPC subprocesses.

## Integration sequence

1. Select one commons skill and the closest neutral capability profile.
2. Run `skillir compile` and review every gap and observation contract.
3. Declare the exact primitive IDs supported by the target adapter.
4. Map each primitive to a target operation with units, frames, tolerances,
   timeouts, and failure codes.
5. Implement validation before target compilation.
6. Produce a content-addressed target bundle; do not execute mutable source
   Markdown directly.
7. Exercise the adapter against deterministic conformance fixtures.
8. Emit evidence tied to the skill, adapter, target, environment, and test suite.
9. Require a separate, signed target approval before enabling deployment.

## Manifest

The manifest schema is
`urn:skill-ir:adapter-manifest:v1alpha1`. A minimal example:

```json
{
  "schema": "urn:skill-ir:adapter-manifest:v1alpha1",
  "kind": "AdapterManifest",
  "metadata": {
    "id": "example.workcell-adapter",
    "version": "0.1.0",
    "license": "Proprietary"
  },
  "spec": {
    "skill_ir_versions": ["urn:skill-ir:v1alpha1"],
    "transport": "json-rpc",
    "profiles": ["fixed-manipulator"],
    "primitives": ["perceive.inspect", "manip.pick", "manip.place", "safety.stop"],
    "operations": ["validate", "compile", "simulate"],
    "permissions": {
      "network": false,
      "filesystem": "workspace-only",
      "hardware": false
    },
    "deployment_enabled": false
  }
}
```

Validate manifests against
[`schemas/adapter-manifest.v1alpha1.schema.json`](../schemas/adapter-manifest.v1alpha1.schema.json).

## Required operations

### `validate`

Input:

- compiled Skill IR;
- requested target profile;
- immutable target-configuration identifier.

Output:

- supported and unsupported primitive IDs;
- missing capabilities;
- unresolved frames, units, tools, parameters, or safety limits;
- deterministic diagnostics with stable codes.

Validation must make no hardware motion.

### `compile`

Input is a Skill IR document that passed adapter validation. Output is an
immutable target bundle containing:

- source Skill IR digest;
- adapter and target-configuration versions;
- target program, behavior tree, trajectory reference, or policy reference;
- parameter bindings and coordinate-frame declarations;
- required runtime and safety dependencies;
- rollback artifact or safe-disable procedure.

Compilation must fail closed when units, frames, limits, or required primitive
bindings are absent.

### `simulate`

Input is an immutable target bundle plus a named scenario. Output is an
`EvidenceRecord` containing at minimum:

- skill, adapter, target, scenario, and environment digests;
- seed and runtime versions;
- step outcomes and termination reason;
- safety-envelope events and human interventions;
- raw evidence pointers and reproducibility command.

Simulation evidence is valid only for the named configuration.

### `deploy` (optional)

Deployment is disabled by default. An implementation must require an
independently approved, signed, unexpired target configuration and must expose a
kill switch and rollback path. The adapter may request motion; it may not bypass
hardware interlocks, watchdogs, safety-rated control, or emergency stops.

## Primitive binding table

Keep the mapping explicit and reviewable. For example:

| Skill IR primitive | Target binding | Required target parameters | Failure output |
|---|---|---|---|
| `perceive.inspect` | perception pipeline or inspection routine | sensor frame, region, confidence rule | unavailable, ambiguous, mismatch |
| `manip.pick` | grasp planner and controller sequence | object frame, grasp set, load and lift limits | no grasp, slip, collision, timeout |
| `manip.place` | placement planner and release sequence | target frame, pose tolerance, support rule | occupied, unstable, release fault |
| `nav.goto` | navigation action or fleet mission | map frame, goal tolerance, load envelope | blocked, lost, canceled, timeout |
| `safety.stop` | independent stop request | stop category and acknowledgement timeout | unacknowledged stop |

Do not hide target assumptions in prompt text. Units, frames, limits, tools, and
timeouts belong in typed target configuration.

## Transport rules

Python entry-point adapters execute in-process and are appropriate only when the
dependency and permission boundary is trusted. JSON-RPC adapters should run as
subprocesses with:

- newline-delimited JSON messages;
- unique request IDs;
- explicit protocol and schema versions;
- bounded input and output sizes;
- timeouts and cancellation;
- stderr reserved for logs;
- no implicit network or hardware permission.

Secrets and private manuals must never appear in adapter manifests, public test
fixtures, or evidence summaries.

## Conformance minimum

An adapter is not conformant until tests prove that it:

- rejects an unsupported Skill IR version;
- rejects every unknown primitive;
- rejects missing capabilities, frames, units, and required limits;
- produces deterministic output for identical immutable inputs;
- reports target and dependency versions;
- emits an evidence record for simulation;
- refuses deployment when approval is absent, expired, or mismatched;
- exposes quarantine and rollback behavior.

Training adapters follow the same boundary but compile into dataset,
environment, trainer, evaluation, and policy manifests rather than a direct
controller program.
