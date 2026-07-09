# Skill Commons Architecture

The Skill Commons is a typed library, not a prompt collection. Its organizing
hierarchy is:

```text
vertical -> skill group -> skill -> ordered primitive bindings
```

A vertical describes an operating environment such as manufacturing or
facilities. A group describes a reusable function such as material handling or
inspection. A skill is a reviewable procedure with preconditions, observable
steps, verification, recovery behavior, and measurable success. A primitive is
the smallest adapter-facing action recognized by the compiler.

## Design rules

- Skills may belong to multiple verticals and groups.
- Vertical tags never imply hardware compatibility.
- `robot_ir` means the source compiles against a declared capability profile;
  it does not mean a policy has been trained or tested on hardware.
- High-risk operations require a safe state and remain subject to independent
  safety systems and local review.
- Domain parameters such as force, tolerance, chemistry, temperature, hygiene,
  load rating, and protective state must come from an authorized local source.
  The commons never invents them.
- Proprietary manuals extend the commons through private overlays. Public skill
  sources must not contain private procedures or product data.

## Quality contract

An installable commons entry must have:

1. a unique catalog identifier and bundled Markdown resource;
2. known vertical, group, profile, maturity, and risk identifiers;
3. complete metadata and at least one ordered step;
4. known primitives with capabilities supported by the declared profile;
5. observations and verifications for every step;
6. measurable success criteria and a safe state when risk requires one;
7. deterministic compilation without blocking gaps;
8. explicit provenance and a distributable license.

The catalog regression suite checks these structural claims. Simulation and
hardware evidence are separate records and are required for higher maturity.
