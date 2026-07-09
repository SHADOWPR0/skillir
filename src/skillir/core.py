"""Compiler, evidence, bundle, and local catalog primitives for Skill IR."""

from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from dataclasses import dataclass
from datetime import UTC, datetime
from importlib import resources
from pathlib import Path
from typing import Any

from .frontmatter import load
from .skilldoc import parse_steps, section_text

SCHEMA = "urn:skill-ir:v1alpha1"
RISK_CLASSES = {"low", "medium", "high", "critical"}
RISK_RANK = {"low": 0, "medium": 1, "high": 2, "critical": 3}
MATURITY = {
    "reference",
    "reviewed",
    "robot_ir",
    "sim_qualified",
    "hardware_observed",
    "cell_qualified",
    "production_approved",
}


@dataclass
class CompileResult:
    ir: dict[str, Any]
    gaps: list[dict[str, str]]

    @property
    def blocked(self) -> bool:
        return any(gap["severity"] == "block" for gap in self.gaps)


def _resource_json(*parts: str) -> dict[str, Any]:
    ref = resources.files("skillir").joinpath("resources", *parts)
    return json.loads(ref.read_text(encoding="utf-8"))


def profiles() -> dict[str, dict[str, Any]]:
    return _resource_json("profiles", "profiles.json")


def primitives() -> dict[str, dict[str, Any]]:
    return _resource_json("primitives", "core.json")


def _as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if value in (None, ""):
        return []
    return [str(value)]


def compile_skill(path: Path, profile_override: str | None = None) -> CompileResult:
    metadata, body = load(path)
    gaps: list[dict[str, str]] = []
    for key in ("id", "version", "title", "risk_class", "maturity", "license", "profile", "required_capabilities", "source_refs"):
        if not metadata.get(key):
            gaps.append({"severity": "block", "code": "metadata.missing", "message": f"Missing required metadata: {key}."})
    risk = str(metadata.get("risk_class", ""))
    if risk and risk not in RISK_CLASSES:
        gaps.append({"severity": "block", "code": "risk.invalid", "message": f"Unknown risk class: {risk}."})
    maturity = str(metadata.get("maturity", ""))
    if maturity and maturity not in MATURITY:
        gaps.append({"severity": "block", "code": "maturity.invalid", "message": f"Unknown maturity: {maturity}."})

    profile_name = profile_override or str(metadata.get("profile", ""))
    available_profiles = profiles()
    profile = available_profiles.get(profile_name)
    if not profile:
        gaps.append({"severity": "block", "code": "profile.unknown", "message": f"Unknown robot profile: {profile_name or '<none>'}."})
        profile = {"id": profile_name, "capabilities": []}
    profile_capabilities = set(profile.get("capabilities", []))
    declared_capabilities = set(_as_list(metadata.get("required_capabilities")))
    for capability in sorted(declared_capabilities - profile_capabilities):
        gaps.append({"severity": "block", "code": "capability.missing", "message": f"Declared capability {capability} is unavailable on {profile_name}."})

    steps = parse_steps(body)
    if not steps:
        gaps.append({"severity": "block", "code": "steps.missing", "message": "Add a ## Steps section with numbered steps."})
    primitive_catalog = primitives()
    used_capabilities: set[str] = set()
    for step in steps:
        if step.action == "unresolved":
            gaps.append({"severity": "block", "code": "action.unresolved", "message": f"{step.id} needs a physical action mapping."})
            continue
        primitive = primitive_catalog.get(step.action)
        if not primitive:
            gaps.append({"severity": "block", "code": "action.unknown", "message": f"{step.id} references unknown primitive {step.action}."})
            continue
        primitive_risk = str(primitive.get("safety_class", "low"))
        if risk in RISK_RANK and primitive_risk in RISK_RANK and RISK_RANK[primitive_risk] > RISK_RANK[risk]:
            gaps.append({
                "severity": "block",
                "code": "risk.underclassified",
                "message": f"{step.id} uses {step.action} ({primitive_risk}) but the skill is classified {risk}.",
            })
        for capability in primitive.get("requires", []):
            used_capabilities.add(capability)
            if capability not in profile_capabilities:
                gaps.append({"severity": "block", "code": "capability.missing", "message": f"{step.id} requires {capability}, unavailable on {profile_name}."})
        if not step.observe:
            gaps.append({"severity": "warn", "code": "observation.missing", "message": f"{step.id} has no observation contract."})
        if not step.verify:
            gaps.append({"severity": "warn", "code": "verification.missing", "message": f"{step.id} has no verification contract."})

    for capability in sorted(used_capabilities - declared_capabilities):
        gaps.append({"severity": "block", "code": "capability.undeclared", "message": f"Primitive bindings require undeclared capability {capability}."})

    preconditions = section_text(body, "Preconditions")
    success = section_text(body, "Success Criteria")
    safe_state = section_text(body, "Safe State")
    if not preconditions:
        gaps.append({"severity": "warn", "code": "preconditions.missing", "message": "Add explicit preconditions."})
    if not success:
        gaps.append({"severity": "block", "code": "success.missing", "message": "Add measurable success criteria."})
    for section_name, section in (("preconditions", preconditions), ("success", success), ("safe_state", safe_state)):
        if "TODO" in section.upper():
            gaps.append({"severity": "block", "code": "content.todo", "message": f"Resolve TODO content in {section_name}."})
    if risk in {"high", "critical"} and not safe_state:
        gaps.append({"severity": "block", "code": "safe_state.missing", "message": "High-risk skills require a Safe State section."})
    if risk == "critical" and str(metadata.get("human_approval", "")).lower() != "true":
        gaps.append({"severity": "block", "code": "approval.missing", "message": "Critical skills require human_approval: true."})

    ir = {
        "schema": SCHEMA,
        "kind": "Skill",
        "metadata": {
            "id": metadata.get("id", ""),
            "version": metadata.get("version", ""),
            "title": metadata.get("title", ""),
            "license": metadata.get("license", ""),
            "source_refs": _as_list(metadata.get("source_refs")),
        },
        "spec": {
            "risk_class": risk,
            "maturity": maturity,
            "robot_profile": profile_name,
            "required_capabilities": sorted(declared_capabilities),
            "preconditions": preconditions,
            "safe_state": safe_state,
            "success_criteria": success,
            "steps": [step.as_dict() for step in steps],
        },
    }
    return CompileResult(ir=ir, gaps=gaps)


def build(result: CompileResult, skill_path: Path) -> Path:
    build_dir = skill_path.parent / "build"
    build_dir.mkdir(exist_ok=True)
    (build_dir / "skill.ir.json").write_text(json.dumps(result.ir, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = {"blocked": result.blocked, "gaps": result.gaps}
    (build_dir / "gap-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return build_dir


def simulate(result: CompileResult, skill_path: Path) -> Path:
    if result.blocked:
        raise ValueError("Simulation is blocked until every blocking compiler gap is resolved.")
    build_dir = build(result, skill_path)
    evidence = {
        "schema": SCHEMA,
        "kind": "EvidenceRecord",
        "skill_id": result.ir["metadata"]["id"],
        "skill_version": result.ir["metadata"]["version"],
        "adapter": "mock",
        "simulator": "deterministic-mock",
        "status": "passed",
        "step_count": len(result.ir["spec"]["steps"]),
        "safety_violations": 0,
        "human_interventions": 0,
        "reproducibility_seed": 0,
    }
    evidence_path = build_dir / "evidence.mock.json"
    evidence_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return evidence_path


def bundle(skill_path: Path, output: Path | None = None) -> Path:
    build_dir = skill_path.parent / "build"
    ir_path = build_dir / "skill.ir.json"
    if not ir_path.exists():
        raise ValueError("Compile the skill before packaging it.")
    output = output or skill_path.parent / f"{skill_path.parent.name}.skillbundle"
    files = [skill_path, ir_path, build_dir / "gap-report.json"]
    evidence = build_dir / "evidence.mock.json"
    if evidence.exists():
        files.append(evidence)
    manifest = {"schema": SCHEMA, "kind": "SkillBundleManifest", "files": []}
    for file in files:
        digest = hashlib.sha256(file.read_bytes()).hexdigest()
        manifest["files"].append({"path": file.name if file.parent == skill_path.parent else f"build/{file.name}", "sha256": digest})
    manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file in files:
            member = file.name if file.parent == skill_path.parent else f"build/{file.name}"
            info = zipfile.ZipInfo(member, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, file.read_bytes())
        info = zipfile.ZipInfo("manifest.json", date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(info, manifest_bytes)
    return output


def attest(bundle_path: Path) -> Path:
    digest = hashlib.sha256(bundle_path.read_bytes()).hexdigest()
    path = bundle_path.with_suffix(bundle_path.suffix + ".attestation.json")
    payload = {
        "schema": SCHEMA,
        "kind": "DigestAttestation",
        "artifact": bundle_path.name,
        "sha256": digest,
        "signature_type": "digest-only",
        "note": "Use an OCI/Sigstore release workflow for cryptographic publication signatures.",
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def verify(bundle_path: Path) -> bool:
    attestation = bundle_path.with_suffix(bundle_path.suffix + ".attestation.json")
    if not attestation.exists():
        return False
    payload = json.loads(attestation.read_text(encoding="utf-8"))
    return payload.get("sha256") == hashlib.sha256(bundle_path.read_bytes()).hexdigest()


def local_publish(bundle_path: Path, registry: Path) -> Path:
    registry.mkdir(parents=True, exist_ok=True)
    target = registry / bundle_path.name
    shutil.copy2(bundle_path, target)
    attestation = bundle_path.with_suffix(bundle_path.suffix + ".attestation.json")
    if attestation.exists():
        shutil.copy2(attestation, registry / attestation.name)
    return target
