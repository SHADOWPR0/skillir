# Skill IR Roadmap

Skill IR is building a universal skill foundry for physical machines: a governed
commons of reusable job knowledge and a CLI pipeline that converts private
manuals, procedures, demonstrations, and evidence into trainable, portable
robot skill packages.

The project will keep one distinction explicit:

- **Skill IR describes what must be done.** It carries intent, prerequisites,
  ordered steps, constraints, expected observations, recovery behavior, and
  success criteria.
- **A policy learns how a particular embodiment does it.** Motor behavior comes
  from demonstrations, simulation, robot telemetry, training, evaluation, and
  supervised hardware trials—not from document text alone.

## Product surfaces

### 1. The Skill Commons

A large public library of small, composable, robot-neutral skills. The commons
will favor primitives and foundational procedures that can be assembled into
larger jobs instead of opaque monolithic tasks.

Initial catalog families:

- perceive, locate, inspect, measure, identify, count, and verify
- approach, align, grasp, release, carry, hand off, and place
- push, pull, turn, press, insert, remove, fasten, loosen, and torque
- open, close, latch, unlatch, load, unload, sort, stage, and palletize
- cut, drill, sand, grind, dispense, coat, clean, wipe, and polish
- fixture setup, tool selection, tool change, calibration, and shutdown
- machine tending, assembly, packaging, warehouse, maintenance, and inspection
- mobile navigation, docking, charging, obstacle handling, and load transport
- human-aware interaction, handover, confirmation, pause, and safe retreat
- recovery primitives for dropped objects, blocked paths, bad grasps, missing
  parts, tool faults, and uncertain observations

Every catalog entry will include provenance, required capabilities, parameter
schema, hazards, expected observations, termination conditions, recovery paths,
test fixtures, maturity level, and compatible embodiment classes.

The commons is not a dump of unverified Markdown. Catalog maturity will be
visible and machine-readable:

1. `draft` — structurally valid but not reviewed
2. `reviewed` — source-grounded and human-reviewed
3. `robot_ir` — compiled against at least one capability profile
4. `sim_qualified` — passes a reproducible simulator evaluation suite
5. `hardware_observed` — has supervised real-robot evidence
6. `cell_qualified` — approved for a specific controlled deployment envelope

### 2. The Knowledge Compiler

Organizations must be able to bring their existing operational knowledge
without rewriting it by hand. The CLI will ingest:

- Markdown procedures and structured templates
- text and scanned PDFs with OCR
- diagrams, tables, warnings, tolerances, and inspection criteria
- maintenance manuals, work instructions, standard operating procedures,
  training materials, checklists, and troubleshooting guides
- future video demonstrations, transcripts, images, CAD references, and sensor
  traces

The compiler will produce cited skill drafts, not unsupported autonomy claims.
It will preserve page and section provenance, expose uncertainty, identify
conflicts and missing physical facts, generate capability-gap reports, and route
ambiguous or safety-critical claims to human review.

Private source material will remain private by default. A private overlay may
extend public primitives without publishing source documents, proprietary
parameters, product details, or deployment evidence.

### 3. The Training Bridge

Skill IR will turn an approved skill into a `TrainingSpec` that defines:

- robot embodiment and capability profile
- observation contract and sensor modalities
- state and continuous or discrete action spaces
- task stages, resets, randomization, and scenario generation
- success, failure, intervention, and recovery labels
- safety envelope, forbidden actions, and termination conditions
- baseline controller and candidate training recipes
- train, validation, and held-out test split policy
- promotion, quarantine, rollback, and retraining rules

The target workflow is:

```text
documents + demonstrations
        -> cited Skill IR
        -> reviewed TrainingSpec
        -> teleoperation and simulation episodes
        -> versioned robot dataset
        -> baseline and candidate policies
        -> held-out simulation evaluation
        -> supervised hardware trials
        -> signed PolicyBundle
        -> monitored deployment and new failure data
```

Training backends will be plugins. Skill IR will not force every physical task
through one model family:

- deterministic industrial jobs may compile to task graphs, motion planners,
  calibrated controllers, and learned perception
- variable manipulation may use behavior cloning, action-chunking transformers,
  diffusion policies, or vision-language-action fine-tuning
- locomotion and contact-rich foundational control may use reinforcement
  learning in high-throughput simulation
- mobile material handling may combine navigation, scheduling, perception,
  planning, and conventional safety-rated control
- hybrid recipes may use a planner for long-horizon sequencing and learned
  policies only for uncertain physical interactions

Initial interoperable dataset targets are
[LeRobotDataset](https://huggingface.co/docs/lerobot/lerobot-dataset-v3) and
[RLDS](https://github.com/google-research/rlds). Initial trainer integrations
will target LeRobot-compatible imitation-learning policies and optional
foundation-model adapters. Initial simulation adapters will target an open,
versioned interface that can be implemented for Isaac Lab, MuJoCo, or other
robotics environments.

### 4. Qualification and deployment

Training loss is not deployment evidence. A policy must be evaluated against
the exact `TrainingSpec` and compared with a simple or scripted baseline.

Qualification suites will cover:

- held-out objects, layouts, backgrounds, lighting, operators, and task variants
- perturbations, occlusions, stale or missing sensors, and partial completion
- success rate, intervention rate, recovery rate, latency, and completion time
- collision, force, velocity, workspace, and other safety-envelope violations
- stability across seeds, checkpoints, simulator settings, and hardware runs
- regressions against every previously qualified skill in the target bundle

A deployable `PolicyBundle` will bind the exact model checkpoint,
pre/post-processing, observation and action mappings, robot profile, dataset
digest, evaluation evidence, runtime adapter, monitoring contract, and rollback
artifact. Independent safety controllers, watchdogs, and emergency stops remain
outside the learned policy.

Production systems will not silently learn in place. New failures,
interventions, and demonstrations create a versioned candidate dataset and a
new policy candidate that must pass the same regression and promotion gates.

## Planned CLI

The following commands are roadmap targets, not claims about the current
release:

```bash
# Knowledge to reviewed robot-neutral skill
skillir ingest work-instruction.pdf
skillir review work-instruction-skill/
skillir compile work-instruction-skill/ --profile fixed-manipulator

# Skill to demonstrations and datasets
skillir train-spec work-instruction-skill/
skillir record work-instruction-skill/ --adapter <robot-or-simulator>
skillir dataset build work-instruction-skill/ --format lerobot
skillir dataset validate work-instruction-skill/

# Dataset to qualified policy
skillir train work-instruction-skill/ --recipe act
skillir eval work-instruction-skill/ --suite held-out
skillir shadow work-instruction-skill/ --adapter <robot>
skillir promote work-instruction-skill/ --stage hardware-observed
skillir quarantine work-instruction-skill/ --reason <incident>

# Portable release and discovery
skillir policy pack work-instruction-skill/
skillir publish work-instruction-skill/ --registry <registry>
skillir search "align and insert"
skillir compose assembly-job --from locate,grasp,align,insert,verify
```

## Core training records

The protocol will add stable, inspectable records rather than hiding the
training lifecycle inside a backend:

- `TrainingSpec` — observations, actions, scenarios, metrics, and safety limits
- `EpisodeManifest` — synchronized trajectory, task stage, intervention, result,
  provenance, consent, and license metadata
- `DatasetManifest` — episode selection, lineage, schema, split policy, and digest
- `PolicyManifest` — recipe, code revision, parameters, checkpoint, and runtime
  requirements
- `EvalSuite` and `EvalReport` — reproducible scenarios, baselines, metrics,
  dispersion, failure taxonomy, and raw evidence pointers
- `PromotionRecord` — approver, target embodiment, deployment envelope, expiry,
  rollback artifact, and signed evidence digest

Plugin contracts will include `RecorderAdapter`, `DatasetExporter`,
`TrainerBackend`, `SimulatorAdapter`, `PolicyRuntime`, and `SafetyMonitor`.

## Release sequence

### v0.1 — shipped foundation

- Markdown-to-Skill IR compiler
- capability-gap report, mock evidence, deterministic bundle, local registry
- neutral profiles, starter catalog, public schemas, and safety boundaries

### v0.2 — Skill Commons and document intelligence

- expand the catalog from starter examples into composable foundational skills
- publish catalog schema, maturity states, provenance, and contribution tests
- pinned offline PDF/OCR extraction with page, table, diagram, and warning
  provenance
- interactive review and explicit uncertainty resolution
- source-change impact analysis and versioned private overlays
- demonstration-plan and `TrainingSpec` generation
- first complete reference skill: inventory bin sorting

### v0.3 — Training Bridge

- `EpisodeManifest`, `DatasetManifest`, and recorder adapter contracts
- teleoperation, simulator, and autonomous-rollout episode ingestion
- LeRobotDataset and RLDS export with deterministic validation
- leakage-resistant dataset split tooling by scene, object, environment, and
  operator
- baseline, behavior-cloning, and action-chunking training recipes
- trainer plugin SDK, reproducible run manifests, and checkpoint packaging

### v0.4 — simulation and hardware qualification

- simulator adapter and conformance suite
- seeded perturbation, held-out scenario, and regression-suite generation
- `EvalSuite`, `EvalReport`, `PolicyManifest`, and `PromotionRecord`
- shadow mode, supervised hardware trial capture, quarantine, and rollback
- PolicyBundle exporter with runtime pre/post-processing and adapter bindings
- first compiler-to-policy reference implementation for inventory bin sorting

### v0.5 — universal registry and ecosystem

- OCI registry publishing and cryptographic release attestations
- public catalog API, dependency resolution, composition, and compatibility
  search
- private registry overlays and access-controlled evidence
- adapter certification kit for robots, simulators, trainers, and runtimes
- public reproducibility dashboard and evidence leaderboard
- occupational expansion packs maintained through governed contributions

### v1.0 — trusted public protocol

- stable Skill IR, training-record, and bundle schemas with migration policy
- reproducible external pilots across multiple robot classes and training stacks
- independent adapter implementations and conformance results
- durable governance for the commons, security response, licensing, and quality
- end-to-end document-to-qualified-policy workflow with no proprietary backend
  required

## First proof

The first vertical slice will use the existing inventory-bin-sort skill and a
simulated fixed manipulator. It will establish a scripted baseline, collect
demonstrations, export a standard dataset, train an imitation policy, evaluate
held-out objects and layouts, package the resulting policy, and record every
artifact needed to reproduce or reject the promotion.

This deliberately starts smaller than a full humanoid deployment. Once the
compiler-to-policy loop is measurable and reproducible, the same protocol can
expand to mobile manipulation, bimanual work, warehouse operations,
manufacturing, maintenance, and other manual job families without changing the
meaning of qualification.

## Non-goals

- claiming that PDF extraction directly produces safe robot motion
- treating attractive simulated behavior as proof of hardware readiness
- mixing proprietary source material into the public commons
- shipping untraceable datasets or policies without source and license metadata
- allowing a learned policy to bypass independent hardware safety systems
- publishing numeric performance promises without reproducible evidence
