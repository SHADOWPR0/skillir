# Skill IR

**A portable skill layer between human work instructions and robot-specific
execution.**

Skill IR is an offline-first CLI, open specification, and governed skill commons
for converting manuals and operating procedures into reviewable, robot-neutral
physical skills. It makes the missing engineering explicit: capabilities,
observations, constraints, failure behavior, success criteria, evidence, and the
adapter boundary to a real robot, simulator, controller, or training stack.

Skill IR is deliberately not a “PDF in, autonomous motion out” product. A
document can describe what work should accomplish. Robot demonstrations,
simulation, controls engineering, policy training, safety systems, and target
qualification determine how a particular machine performs it.

## What is useful today

The current `main` branch provides:

- 24 installable skills across 10 operating verticals and 11 functional groups;
- neutral profiles for fixed manipulators, mobile manipulators, mobile load
  carriers, and bimanual humanoids;
- Markdown and PDF-to-review-draft ingestion with source-file hashing;
- deterministic compilation into `urn:skill-ir:v1alpha1` JSON;
- capability-gap, observation, verification, and safety checks;
- an installable skill catalog with search, inspection, and local customization;
- deterministic bundles, digest attestations, and a local registry overlay;
- an adapter contract for proprietary robotics and automation integrations;
- cross-platform tests on Linux, macOS, and Windows.

| If you are a… | Start here |
|---|---|
| Automation developer | Pull a commons skill, compile it, then map its primitives through [the adapter contract](docs/adapter-sdk.md). |
| Robot engineer | Inspect profiles, primitives, preconditions, observations, failure behavior, and success criteria before binding hardware. |
| Operations or process engineer | Ingest a procedure, review the generated draft, and resolve missing physical facts with the robotics team. |
| Platform team | Use private overlays for proprietary manuals and target adapters while keeping the public protocol vendor-neutral. |
| Research team | Use Skill IR as the task, dataset, evaluation, and promotion contract around a simulator or policy-training backend. |

## Mental model

```text
manual / work instruction / checklist
                  |
                  v
       cited, reviewable skill.md
                  |
                  v
     robot-neutral Skill IR + gap report
                  |
          +-------+--------+
          |                |
          v                v
 target adapter       training adapter
 PLC / ROS / BT       dataset / policy / sim
          |                |
          +-------+--------+
                  v
    target bundle + named evidence record
```

The layers stay separate:

1. **Source knowledge** — manuals, procedures, diagrams, and local parameters.
2. **Skill IR** — portable intent, ordered primitive bindings, observations,
   verification, recovery, and success.
3. **Target binding** — robot profile, controller, simulator, dataset, or policy
   adapter.
4. **Evidence** — results tied to an exact skill version, target configuration,
   adapter, environment, and test suite.

## Install from source

The expanded commons and `show`/`pull` commands are currently on `main` and will
ship in the next tagged release.

```bash
git clone https://github.com/SHADOWPR0/skillir.git
cd skillir
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
python -m pip install -e .
skillir doctor
```

For local PDF extraction:

```bash
python -m pip install -e '.[pdf]'
```

Pin a tag or commit for production and repeat qualification after upgrading.

## Five-minute engineering walkthrough

### 1. Discover the commons

```bash
skillir taxonomy
skillir search manufacturing_assembly
skillir search inspection
skillir search cleaning
skillir show core.fixture-load
```

The catalog spans logistics and warehousing, manufacturing and assembly,
inspection and quality, maintenance and field service, facilities and cleaning,
construction and fabrication, agriculture and food handling, service and
hospitality, human assistance, and safety/recovery.

### 2. Pull a skill into an editable workspace

```bash
skillir pull core.component-kitting --out ./component-kitting
skillir compile ./component-kitting
skillir inspect ./component-kitting
```

`pull` copies the complete Markdown source, not a prompt or catalog stub. Edit
the local copy to add authorized tolerances, identifiers, tools, fixtures,
hazards, and recovery requirements.

### 3. Convert an existing procedure

Markdown input works with the dependency-free core:

```bash
skillir ingest ./work-instruction.md \
  --profile fixed-manipulator \
  --out ./work-instruction-skill
```

PDF input uses the optional local document extractor:

```bash
skillir ingest ./equipment-manual.pdf \
  --profile mobile-manipulator \
  --out ./equipment-manual-skill
```

The output is intentionally blocked until a reviewer resolves every
`action: unresolved`, missing success criterion, unknown capability, and local
engineering parameter:

```text
equipment-manual-skill/
  source/
    equipment-manual.pdf      # preserved source
    document.md                # extracted review text
  skill.md                     # cited draft to review
```

Compilation then produces:

```text
build/
  skill.ir.json                # portable machine contract
  gap-report.json              # blockers and warnings
```

### 4. Package reviewed work

```bash
skillir compile ./equipment-manual-skill
skillir simulate ./equipment-manual-skill
skillir pack ./equipment-manual-skill
skillir verify ./equipment-manual-skill/equipment-manual-skill.skillbundle
```

The built-in simulator is a deterministic structural mock. It proves that the
skill and bundle pipeline are reproducible; it does not establish physical
feasibility or hardware safety.

### 5. Keep proprietary knowledge private

Use a private repository or registry overlay for imported manuals, extracted
text, product parameters, target adapters, and deployment evidence. Public
commons skills can be extended without publishing the underlying source:

```bash
skillir publish ./equipment-manual-skill/equipment-manual-skill.skillbundle \
  --registry /secure/private-skill-registry
```

The CLI makes no network call in its default workflow.

## Authoring contract

`skill.md` is the human-review surface. A minimal executable skill looks like:

```markdown
---
id: private.inspect-and-place
version: 0.1.0
title: Inspect and Place
license: Proprietary
risk_class: medium
maturity: reviewed
profile: fixed-manipulator
required_capabilities:
  - perception.object
  - manipulation.pick
  - manipulation.place
source_refs:
  - sha256:<source-document-digest>
---

# Inspect and Place

## Preconditions
The approved object and destination are visible and inside the configured cell.

## Steps
1. Inspect the object and destination.
   - action: perceive.inspect
   - observe: object identity, pose, and destination occupancy are available
   - verify: identity and pose meet the local acceptance criteria
   - on_failure: safety.stop
   - evidence: source:section-4.2
2. Pick the approved object.
   - action: manip.pick
   - observe: grasp state and object retention are available
   - verify: the object remains stable after the verification lift
   - on_failure: safety.stop
   - evidence: source:section-4.3
3. Place the object at the destination.
   - action: manip.place
   - observe: destination pose and release state are available
   - verify: the object is stable inside the configured tolerance
   - on_failure: safety.stop
   - evidence: source:section-4.4

## Success Criteria
The correct object is stable at the destination with no safety-envelope event.

## Safe State
Stop in a collision-free pose and preserve a stable load state when possible.
```

The compiler rejects unknown profiles, unknown primitives, unsupported
capabilities, unresolved actions, missing success criteria, and high-risk skills
without a safe state. It warns when steps lack observation or verification
contracts.

## Commons organization

The library uses a typed hierarchy:

```text
vertical -> skill group -> skill -> primitive bindings
```

Examples:

| Vertical | Groups | Included skills |
|---|---|---|
| Manufacturing and assembly | machine tending, kitting, material handling | fixture load/unload, component kitting, pick-and-place |
| Logistics and warehousing | intralogistics, fulfillment, packaging | order picking, tote transfer, case packing, consolidation |
| Inspection and quality | perception, verification, sorting | object inspection, indicator reading, count check, quarantine |
| Maintenance and field service | asset inspection, tool logistics | condition survey, tool delivery |
| Facilities and cleaning | cleaning, sanitation, waste handling | surface wipe, waste-bin service |
| Construction and fabrication | staging, preparation | material staging plus high-risk reference coverage |
| Agriculture and food handling | grading, handling | produce sorting |
| Service and hospitality | delivery, assistance | tray delivery, shelf replenishment |

Run `skillir taxonomy` for stable identifiers and read
[the Skill Commons architecture](docs/skill-commons.md) before contributing a
new group.

## Maturity is evidence, not branding

| Maturity | Meaning |
|---|---|
| `reference` | Coverage or research reference; may not be installable. |
| `reviewed` | Source-grounded and reviewed, but not capability-bound. |
| `robot_ir` | Compiles against at least one declared capability profile. |
| `sim_qualified` | Passed a named, reproducible simulator suite. |
| `hardware_observed` | Has supervised evidence on an identified robot configuration. |
| `cell_qualified` | Approved inside a specific controlled deployment envelope. |
| `production_approved` | Organization-specific approval with monitoring and rollback. |

Most public commons entries are `robot_ir`. They are useful engineering
starting points, not pretrained robot policies.

## Connecting an automation or robotics stack

An adapter binds portable primitives such as `perceive.inspect`, `manip.pick`,
`nav.goto`, or `manip.wipe` to a target system. That target can be a behavior
tree, robotics middleware node, motion planner, PLC-controlled cell, digital
twin, simulator, dataset generator, or learned policy runtime.

Every adapter must declare:

- supported Skill IR versions and primitive identifiers;
- capability profiles and target-specific limits;
- permissions, network behavior, and dependency licenses;
- `validate`, `compile`, and `simulate` behavior;
- the exact conditions under which deployment is allowed;
- conformance results, monitoring, quarantine, and rollback behavior.

Start with [the adapter SDK contract](docs/adapter-sdk.md). Keep hardware limits,
interlocks, watchdogs, emergency stops, and safety-rated control independent of
the Skill IR interpreter and any learned policy.

## Training robots

Skill IR is the task and evidence contract around training. The planned bridge
will add `TrainingSpec`, episode and dataset manifests, LeRobot/RLDS export,
trainer plugins, simulator adapters, evaluation suites, policy manifests, and
promotion records.

The intended loop is:

```text
reviewed Skill IR
  -> embodiment-specific observation/action contract
  -> teleoperation and simulation episodes
  -> versioned dataset with held-out splits
  -> baseline and candidate policy training
  -> simulation regression
  -> supervised hardware trials
  -> signed, monitored PolicyBundle
```

See [the roadmap](ROADMAP.md) for the release sequence. Do not use mock evidence
as training or deployment evidence.

## Repository map

```text
src/skillir/                    CLI, compiler, bundle, and packaged resources
src/skillir/resources/          catalog, taxonomy, profiles, and primitives
packs/                          canonical public skill Markdown
schemas/                        Skill IR and catalog JSON Schemas
docs/                           specification, commons, adapter, and safety docs
examples/                       adapter and integration examples
tests/                          compiler, catalog, packaging, and CLI regressions
restricted/                     policy boundaries; no enabled restricted skills
```

Generated `build/`, dataset, model, video, and binary artifacts are not source
files and should remain outside Git or in a content-addressed registry.

## Development and verification

```bash
python -m pip install -e '.[dev]'
python -m unittest discover -s tests
python -m pytest
python scripts/check_neutrality.py
python -m build
```

CI repeats core tests on Python 3.11 and 3.13 across Linux, macOS, and Windows,
then compiles, simulates, and packages a reference skill.

## Current boundaries

- PDF extraction creates a review draft; it does not recover every diagram,
  tolerance, warning, or page-level relationship reliably.
- Scanned-document OCR provenance and visual review tooling remain roadmap work.
- The core includes a deterministic mock adapter, not a live robot driver.
- The commons does not supply local force, torque, temperature, chemistry,
  hygiene, load, calibration, or protective-equipment parameters.
- No checked-in skill claims universal safety, certification, or compatibility
  with unnamed hardware.
- Restricted human-contact extensions are disabled and distributed separately;
  they are not the focus of the public commons.

Read [the specification](docs/spec.md), [Skill Commons architecture](docs/skill-commons.md),
[adapter contract](docs/adapter-sdk.md), [safety policy](docs/safety.md),
[roadmap](ROADMAP.md), and [contribution guide](CONTRIBUTING.md) before building a
target integration.

## License

Apache-2.0. Contributors must have the right to distribute every submitted
source, derivative, dataset reference, and asset. Proprietary manuals and local
deployment evidence belong in private overlays.
