from __future__ import annotations

import json
import re
import tempfile
import unittest
from importlib import resources
from pathlib import Path

from jsonschema import Draft202012Validator

from skillir.cli import main
from skillir.core import bundle, compile_skill, simulate, verify
from skillir.frontmatter import parse


ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "packs/household-service/skills/inventory-bin-sort/skill.md"


class SkillIrTests(unittest.TestCase):
    def test_local_markdown_links_resolve(self) -> None:
        for document in [ROOT / "README.md", *(ROOT / "docs").glob("*.md")]:
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", document.read_text(encoding="utf-8")):
                if "://" in target or target.startswith("#"):
                    continue
                local = target.split("#", 1)[0]
                with self.subTest(document=document, target=target):
                    self.assertTrue((document.parent / local).resolve().exists())

    def test_public_json_contracts_are_valid_json(self) -> None:
        paths = list((ROOT / "schemas").glob("*.json")) + list((ROOT / "examples").glob("*.json"))
        self.assertGreaterEqual(len(paths), 3)
        for path in paths:
            with self.subTest(path=path):
                json.loads(path.read_text(encoding="utf-8"))

    def test_catalog_and_adapter_examples_validate_against_public_schemas(self) -> None:
        catalog_schema = json.loads((ROOT / "schemas/catalog.v1alpha1.schema.json").read_text(encoding="utf-8"))
        adapter_schema = json.loads((ROOT / "schemas/adapter-manifest.v1alpha1.schema.json").read_text(encoding="utf-8"))
        skill_schema = json.loads((ROOT / "schemas/skill-ir.v1alpha1.schema.json").read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(catalog_schema)
        Draft202012Validator.check_schema(adapter_schema)
        Draft202012Validator.check_schema(skill_schema)
        catalog = json.loads((ROOT / "src/skillir/resources/catalog.json").read_text(encoding="utf-8"))
        adapter = json.loads((ROOT / "examples/adapter-manifest.json").read_text(encoding="utf-8"))
        Draft202012Validator(catalog_schema).validate(catalog)
        Draft202012Validator(adapter_schema).validate(adapter)
        Draft202012Validator(skill_schema).validate(compile_skill(SAMPLE).ir)

    def test_catalog_taxonomy_and_bundled_sources_are_consistent(self) -> None:
        package = resources.files("skillir")
        catalog = json.loads(package.joinpath("resources", "catalog.json").read_text(encoding="utf-8"))
        taxonomy = json.loads(package.joinpath("resources", "taxonomy.json").read_text(encoding="utf-8"))
        entries = catalog["skills"]
        repository_sources: dict[str, str] = {}
        for path in (ROOT / "packs").glob("**/skill.md"):
            source = path.read_text(encoding="utf-8")
            metadata, _ = parse(source)
            repository_sources[metadata["id"]] = source
        identifiers = [entry["id"] for entry in entries]
        self.assertEqual(len(identifiers), len(set(identifiers)))
        installable = [entry for entry in entries if "resource" in entry]
        self.assertGreaterEqual(len(installable), 20)
        active_verticals: set[str] = set()
        active_groups: set[str] = set()
        for entry in entries:
            self.assertTrue(set(entry["verticals"]).issubset(taxonomy["verticals"]))
            self.assertTrue(set(entry["groups"]).issubset(taxonomy["groups"]))
            active_verticals.update(entry["verticals"])
            active_groups.update(entry["groups"])
            if "resource" not in entry:
                continue
            source = repository_sources[entry["id"]]
            metadata, _ = parse(source)
            self.assertEqual(metadata["id"], entry["id"])
            self.assertIn(metadata["profile"], entry["profiles"])
            self.assertEqual(metadata["maturity"], entry["maturity"])
            self.assertEqual(metadata["risk_class"], entry["risk_class"])
        self.assertGreaterEqual(len(active_verticals), 8)
        self.assertGreaterEqual(len(active_groups), 8)

    def test_all_commons_skills_compile_without_blocking_gaps(self) -> None:
        skills = sorted((ROOT / "packs").glob("**/skill.md"))
        self.assertGreaterEqual(len(skills), 10)
        results = {str(skill.relative_to(ROOT)): compile_skill(skill) for skill in skills}
        failures = {path: result.gaps for path, result in results.items() if result.blocked}
        self.assertEqual(failures, {})

    def test_complete_skill_compiles_and_simulates(self) -> None:
        result = compile_skill(SAMPLE)
        self.assertFalse(result.blocked, result.gaps)
        evidence = simulate(result, SAMPLE)
        self.assertEqual(json.loads(evidence.read_text())["status"], "passed")

    def test_unresolved_action_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "skill.md"
            path.write_text(
                "---\nid: test.unresolved\nversion: 0.1.0\ntitle: Test\nlicense: Apache-2.0\nrisk_class: low\nmaturity: reference\nprofile: mobile-manipulator\n---\n\n## Steps\n1. Do a thing.\n\n## Success Criteria\nThe thing is done.\n",
                encoding="utf-8",
            )
            result = compile_skill(path)
            self.assertTrue(result.blocked)
            self.assertIn("action.unresolved", {gap["code"] for gap in result.gaps})

    def test_risk_underclassification_and_undeclared_capability_block(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "skill.md"
            path.write_text(
                "---\nid: test.bad-contract\nversion: 0.1.0\ntitle: Bad Contract\nlicense: Apache-2.0\nrisk_class: low\nmaturity: robot_ir\nprofile: fixed-manipulator\nrequired_capabilities:\n  - perception.object\nsource_refs:\n  - authored:test\n---\n\n## Preconditions\nThe target is visible.\n\n## Steps\n1. Pick it.\n   - action: manip.pick\n   - observe: grasp state is available\n   - verify: the object is retained\n\n## Success Criteria\nThe object is retained.\n",
                encoding="utf-8",
            )
            codes = {gap["code"] for gap in compile_skill(path).gaps}
            self.assertIn("risk.underclassified", codes)
            self.assertIn("capability.undeclared", codes)

    def test_bundle_is_attestable(self) -> None:
        result = compile_skill(SAMPLE)
        simulate(result, SAMPLE)
        artifact = bundle(SAMPLE)
        from skillir.core import attest

        attest(artifact)
        self.assertTrue(verify(artifact))
        artifact.unlink()
        artifact.with_suffix(artifact.suffix + ".attestation.json").unlink()

    def test_cli_search(self) -> None:
        self.assertEqual(main(["search", "handling"]), 0)

    def test_bundled_commons_skill_can_be_pulled_and_compiled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "pick-and-place"
            self.assertEqual(main(["pull", "core.pick-and-place", "--out", str(output)]), 0)
            result = compile_skill(output / "skill.md")
            self.assertFalse(result.blocked, result.gaps)

    def test_taxonomy_command(self) -> None:
        self.assertEqual(main(["taxonomy"]), 0)

    def test_markdown_ingest_creates_reviewable_blocked_draft(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "manual.md"
            source.write_text("# Procedure\n\n1. Move the item.\n", encoding="utf-8")
            output = root / "draft"
            self.assertEqual(main(["ingest", str(source), "--out", str(output)]), 0)
            result = compile_skill(output / "skill.md")
            self.assertTrue(result.blocked)
            self.assertTrue((output / "source" / "document.md").exists())


if __name__ == "__main__":
    unittest.main()
