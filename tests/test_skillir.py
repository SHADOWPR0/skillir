from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from skillir.cli import main
from skillir.core import bundle, compile_skill, simulate, verify


ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "packs/household-service/skills/inventory-bin-sort/skill.md"


class SkillIrTests(unittest.TestCase):
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
