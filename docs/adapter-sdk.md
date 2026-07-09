# Adapter SDK

An adapter binds `SkillIR` to a concrete execution, simulation, or training
environment without changing the portable skill.

Every adapter manifest declares:

- supported Skill IR versions;
- supported primitive IDs and capability profiles;
- requested permissions and network behavior;
- adapter, model, and dependency licenses;
- deterministic conformance-test results.

Adapters may be Python entry points or JSON-RPC subprocesses, allowing teams to
keep proprietary hardware integrations private and in their preferred language.

## Required operations

1. `validate(skill, profile)` returns unsupported primitives and capabilities.
2. `compile(skill, profile)` creates a target-specific bundle.
3. `simulate(bundle, scenario)` returns an `EvidenceRecord`.
4. `deploy(bundle)` is optional and must require an independently approved,
   signed, unexpired target configuration.

The public core provides only a deterministic mock adapter. It never establishes
that a skill is deployable to a proprietary system.
