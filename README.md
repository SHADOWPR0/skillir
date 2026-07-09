# Skill IR

**Compile human know-how into evidence-backed physical skills.**

Skill IR is an offline-first CLI and open specification for turning a manual, Markdown procedure, or future multimodal source into a reviewable robot-neutral skill, a capability-gap report, simulation evidence, and a portable skill bundle.

It is deliberately not a "PDF in, autonomous motion out" claim. A human procedure becomes deployable only after the missing physical facts are named, reviewed, bound to a robot capability profile, tested, and packaged with evidence.

```bash
pipx install 'skillir[pdf]'
skillir create maintenance-manual.pdf --profile humanoid-bimanual
skillir compile maintenance-manual-skill/
skillir simulate maintenance-manual-skill/
skillir pack maintenance-manual-skill/
```

## What it produces

```text
source material
  -> cited SourceDocument
  -> human-reviewable InstructionIR
  -> robot-neutral SkillIR
  -> capability binding and Embodiment Gap Report
  -> simulation / hardware EvidenceRecord
  -> signed-release-ready .skillbundle
```

The human-readable source is `skill.md`; the machine contract is `urn:skill-ir:v1alpha1` JSON. Every serious claim can carry source references, risk classification, explicit success criteria, a safe state, and a recovery path.

## Fast local demo

```bash
PYTHONPATH=src python3 -m skillir compile packs/household-service/skills/inventory-bin-sort/
PYTHONPATH=src python3 -m skillir simulate packs/household-service/skills/inventory-bin-sort/
PYTHONPATH=src python3 -m skillir pack packs/household-service/skills/inventory-bin-sort/
PYTHONPATH=src python3 -m skillir search handling
```

## Product boundaries

- Markdown explains a skill; it is not motor control.
- The compiler blocks unresolved actions, unknown profiles, missing success criteria, and high-risk skills without a safe state.
- The default runtime is local and makes no network calls. Remote drafting is an explicit, future provider plugin.
- Generic robot profiles and adapters are public. Target-specific deployment integrations belong in private plugins.
- `sim_qualified` means evidence passed for a named simulator/configuration, not that a skill is universally safe or certified.

## Included now

- Dependency-free Markdown compiler and deterministic mock simulator
- Neutral humanoid, mobile-load-carrier, fixed-manipulator, and mobile-manipulator profiles
- Capability-aware primitive catalog
- Reproducible local bundles and digest attestations
- Starter catalog, pack, schemas, adapter contract, contribution rules, and safety policy
- Optional PDF ingestion through a locally installed document-extraction extra

## Roadmap

1. Harden source-grounded PDF ingestion, OCR, visual provenance, and interactive review.
2. Add adapter conformance for behavior trees, robotics middleware, dataset export, world-model evaluation, and OCI distribution.
3. Build the public catalog, private registry overlays, signed OCI releases, and evidence leaderboard.

See [the specification](docs/spec.md), [adapter contract](docs/adapter-sdk.md), [safety policy](docs/safety.md), and [contributing guide](CONTRIBUTING.md).
