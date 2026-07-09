"""The Skill IR command line interface."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from importlib import resources
from pathlib import Path

from . import __version__
from .core import attest, build, bundle, compile_skill, local_publish, profiles, simulate, verify
from .frontmatter import load

EXIT_BLOCKED = 31
EXIT_DEPENDENCY = 20

TEMPLATE = """---
id: example.inventory-bin-sort
version: 0.1.0
title: Inventory Bin Sort
license: Apache-2.0
risk_class: low
maturity: reviewed
profile: mobile-manipulator
required_capabilities:
  - perception.object
  - manipulation.pick
  - manipulation.place
source_refs:
  - authored:example
---

# Inventory Bin Sort

## Preconditions
The workspace is clear, the target bin is visible, and the robot has a safe stop path.

## Steps
1. Inspect the target item and destination bin.
   - action: perceive.inspect
   - observe: item identity and destination bin are visible
   - verify: confidence meets the local profile threshold
   - evidence: authored:example:step-1
2. Pick the target item.
   - action: manip.pick
   - observe: grasp remains stable during lift
   - verify: object is held without slip
   - on_failure: safety.stop
   - evidence: authored:example:step-2
3. Place the item in the destination bin.
   - action: manip.place
   - observe: destination is clear
   - verify: item is inside the destination bin
   - on_failure: safety.stop
   - evidence: authored:example:step-3

## Success Criteria
The target item is in the destination bin, no collision occurs, and every verification passes.

## Safe State
Stop motion, release no load, and wait in the designated safe pose.
"""


def _print_gaps(result) -> None:
    if not result.gaps:
        print("No compiler gaps found.")
        return
    for gap in result.gaps:
        print(f"[{gap['severity']}] {gap['code']}: {gap['message']}")


def _skill_path(value: str) -> Path:
    path = Path(value).expanduser().resolve()
    if path.is_dir():
        path = path / "skill.md"
    return path


def cmd_init(args: argparse.Namespace) -> int:
    root = Path(args.directory).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=args.force)
    target = root / "skill.md"
    if target.exists() and not args.force:
        print(f"Refusing to overwrite {target}; pass --force to replace it.", file=sys.stderr)
        return 1
    target.write_text(TEMPLATE, encoding="utf-8")
    print(target)
    return 0


def _markdown_draft(text: str, source_ref: str, profile: str) -> str:
    numbered = [line.strip() for line in text.splitlines() if line.lstrip()[:1].isdigit() and "." in line]
    steps = numbered or ["1. Review the imported procedure and resolve its physical action mapping."]
    rendered = []
    for line in steps:
        rendered.extend([line, "   - action: unresolved", "   - evidence: " + source_ref])
    return """---
id: draft.imported-procedure
version: 0.1.0
title: Imported Procedure Draft
license: UNRESOLVED
risk_class: low
maturity: reference
profile: """ + profile + """
source_refs:
  - """ + source_ref + """
---

# Imported Procedure Draft

## Preconditions
TODO: establish robot, workcell, tool, and operator preconditions.

## Steps
""" + "\n".join(rendered) + """

## Success Criteria
TODO: define observable completion criteria.
"""


def _extract_pdf(source: Path) -> str:
    try:
        from docling.document_converter import DocumentConverter  # type: ignore[import-not-found]
    except ImportError as exc:
        raise RuntimeError("PDF ingestion requires the optional extra: pipx install 'skillir[pdf]'.") from exc
    converter = DocumentConverter()
    result = converter.convert(source)
    return result.document.export_to_markdown()


def cmd_ingest(args: argparse.Namespace) -> int:
    source = Path(args.source).expanduser().resolve()
    if not source.is_file():
        print(f"Source does not exist: {source}", file=sys.stderr)
        return 10
    out = Path(args.out).expanduser().resolve() if args.out else source.with_suffix("").with_name(source.stem + "-skill")
    if out.exists() and any(out.iterdir()) and not args.force:
        print(f"Refusing to overwrite non-empty directory {out}; pass --force to continue.", file=sys.stderr)
        return 1
    (out / "source").mkdir(parents=True, exist_ok=True)
    try:
        if source.suffix.lower() == ".pdf":
            text = _extract_pdf(source)
        else:
            text = source.read_text(encoding="utf-8")
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        return EXIT_DEPENDENCY
    shutil.copy2(source, out / "source" / source.name)
    source_ref = f"sha256:{__import__('hashlib').sha256(source.read_bytes()).hexdigest()}"
    (out / "source" / "document.md").write_text(text, encoding="utf-8")
    (out / "skill.md").write_text(_markdown_draft(text, source_ref, args.profile), encoding="utf-8")
    print(out / "skill.md")
    print("Draft created. Resolve every unresolved action and TODO before compile can pass.")
    return 0


def cmd_compile(args: argparse.Namespace) -> int:
    path = _skill_path(args.skill)
    if not path.exists():
        print(f"Skill file does not exist: {path}", file=sys.stderr)
        return 10
    try:
        result = compile_skill(path, args.profile)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 10
    build_dir = build(result, path)
    _print_gaps(result)
    print(build_dir / "skill.ir.json")
    return EXIT_BLOCKED if result.blocked else 0


def cmd_simulate(args: argparse.Namespace) -> int:
    path = _skill_path(args.skill)
    try:
        result = compile_skill(path, args.profile)
        evidence = simulate(result, path)
    except (ValueError, FileNotFoundError) as exc:
        print(exc, file=sys.stderr)
        return EXIT_BLOCKED
    print(evidence)
    return 0


def cmd_pack(args: argparse.Namespace) -> int:
    path = _skill_path(args.skill)
    try:
        result = compile_skill(path, args.profile)
        if result.blocked:
            _print_gaps(result)
            return EXIT_BLOCKED
        build(result, path)
        artifact = bundle(path, Path(args.output).resolve() if args.output else None)
        attestation = attest(artifact)
    except (ValueError, FileNotFoundError) as exc:
        print(exc, file=sys.stderr)
        return EXIT_BLOCKED
    print(artifact)
    print(attestation)
    return 0


def cmd_publish(args: argparse.Namespace) -> int:
    artifact = Path(args.bundle).expanduser().resolve()
    if not artifact.exists() or not verify(artifact):
        print("Bundle is missing or its digest attestation does not verify.", file=sys.stderr)
        return 1
    target = local_publish(artifact, Path(args.registry).expanduser().resolve())
    print(target)
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    artifact = Path(args.bundle).expanduser().resolve()
    ok = artifact.exists() and verify(artifact)
    print("verified" if ok else "verification-failed")
    return 0 if ok else 1


def cmd_inspect(args: argparse.Namespace) -> int:
    path = _skill_path(args.skill)
    result = compile_skill(path, args.profile)
    print(json.dumps({"ir": result.ir, "gaps": result.gaps, "blocked": result.blocked}, indent=2, sort_keys=True))
    return 0


def _catalog_entries() -> list[dict[str, object]]:
    catalog = json.loads(resources.files("skillir").joinpath("resources", "catalog.json").read_text(encoding="utf-8"))
    return list(catalog["skills"])


def cmd_taxonomy(_: argparse.Namespace) -> int:
    taxonomy = json.loads(resources.files("skillir").joinpath("resources", "taxonomy.json").read_text(encoding="utf-8"))
    print("VERTICALS")
    for identifier, item in taxonomy["verticals"].items():
        print(f"{identifier}\t{item['title']}")
    print("\nSKILL GROUPS")
    for identifier, item in taxonomy["groups"].items():
        print(f"{identifier}\t{item['title']}")
    return 0


def _catalog_skill(skill_id: str) -> tuple[dict[str, object] | None, str]:
    entry = next((item for item in _catalog_entries() if item.get("id") == skill_id), None)
    if entry is None:
        return None, f"Unknown catalog skill: {skill_id}. Run `skillir search <query>` first."
    resource_path = entry.get("resource")
    if not isinstance(resource_path, str):
        return None, f"{skill_id} is a coverage reference, not an installable skill."
    packaged = resources.files("skillir").joinpath(*resource_path.split("/"))
    if packaged.is_file():
        return entry, packaged.read_text(encoding="utf-8")
    repository = Path(__file__).resolve().parents[2]
    matches = []
    for candidate in repository.glob("packs/**/skill.md"):
        metadata, _ = load(candidate)
        if metadata.get("id") == skill_id:
            matches.append(candidate)
    if len(matches) == 1:
        return entry, matches[0].read_text(encoding="utf-8")
    return None, f"Bundled source for {skill_id} is unavailable; reinstall Skill IR from a complete wheel."


def cmd_search(args: argparse.Namespace) -> int:
    query = args.query.lower()
    hits = [entry for entry in _catalog_entries() if query in json.dumps(entry).lower()]
    for hit in hits:
        print(f"{hit['id']}\t{hit['title']}\t{hit['maturity']}\t{hit['risk_class']}")
    return 0 if hits else 1


def cmd_show(args: argparse.Namespace) -> int:
    entry, content = _catalog_skill(args.skill_id)
    if entry is None:
        print(content, file=sys.stderr)
        return 1
    sys.stdout.write(content)
    return 0


def cmd_pull(args: argparse.Namespace) -> int:
    entry, content = _catalog_skill(args.skill_id)
    if entry is None:
        print(content, file=sys.stderr)
        return 1
    root = Path(args.out or args.skill_id.replace(".", "-")).expanduser().resolve()
    target = root if root.suffix.lower() == ".md" else root / "skill.md"
    if target.exists() and not args.force:
        print(f"Refusing to overwrite {target}; pass --force to replace it.", file=sys.stderr)
        return 1
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    print(target)
    return 0


def cmd_profiles(_: argparse.Namespace) -> int:
    for name, profile in profiles().items():
        print(f"{name}\t{profile['title']}")
    return 0


def cmd_doctor(_: argparse.Namespace) -> int:
    print("core: ready")
    try:
        import docling  # type: ignore[import-not-found]
        print("pdf: ready")
    except ImportError:
        print("pdf: missing (install skillir[pdf])")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="skillir", description="Compile human procedures into evidence-backed physical skills.")
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="Create a complete editable skill workspace.")
    init.add_argument("directory")
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=cmd_init)
    ingest = sub.add_parser("ingest", help="Convert a Markdown file or PDF into a cited skill draft.")
    ingest.add_argument("source")
    ingest.add_argument("--out")
    ingest.add_argument("--profile", default="mobile-manipulator")
    ingest.add_argument("--force", action="store_true")
    ingest.set_defaults(func=cmd_ingest)
    create = sub.add_parser("create", help="Guided alias for ingest.")
    create.add_argument("source")
    create.add_argument("--out")
    create.add_argument("--profile", default="mobile-manipulator")
    create.add_argument("--force", action="store_true")
    create.set_defaults(func=cmd_ingest)
    for name, func, help_text in (
        ("compile", cmd_compile, "Compile a skill into Skill IR and a gap report."),
        ("simulate", cmd_simulate, "Run the deterministic mock simulator."),
        ("pack", cmd_pack, "Create a deterministic .skillbundle and digest attestation."),
        ("inspect", cmd_inspect, "Print a compiled Skill IR and its gaps."),
    ):
        command = sub.add_parser(name, help=help_text)
        command.add_argument("skill")
        command.add_argument("--profile")
        if name == "pack":
            command.add_argument("--output")
        command.set_defaults(func=func)
    publish = sub.add_parser("publish", help="Publish a verified bundle to a local registry overlay.")
    publish.add_argument("bundle")
    publish.add_argument("--registry", required=True)
    publish.set_defaults(func=cmd_publish)
    verify_cmd = sub.add_parser("verify", help="Verify a local digest attestation.")
    verify_cmd.add_argument("bundle")
    verify_cmd.set_defaults(func=cmd_verify)
    search = sub.add_parser("search", help="Search the bundled skill commons.")
    search.add_argument("query")
    search.set_defaults(func=cmd_search)
    show = sub.add_parser("show", help="Print a bundled commons skill as Markdown.")
    show.add_argument("skill_id")
    show.set_defaults(func=cmd_show)
    pull = sub.add_parser("pull", help="Copy a bundled commons skill into an editable workspace.")
    pull.add_argument("skill_id")
    pull.add_argument("--out")
    pull.add_argument("--force", action="store_true")
    pull.set_defaults(func=cmd_pull)
    taxonomy = sub.add_parser("taxonomy", help="List supported verticals and skill groups.")
    taxonomy.set_defaults(func=cmd_taxonomy)
    profile_cmd = sub.add_parser("profiles", help="List neutral robot capability profiles.")
    profile_cmd.set_defaults(func=cmd_profiles)
    doctor = sub.add_parser("doctor", help="Check optional runtime capabilities.")
    doctor.set_defaults(func=cmd_doctor)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))
