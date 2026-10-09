"""Regression tests for portable skill ZIP packaging."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("package_skill", ROOT / "scripts/package_skill.py")
packager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packager)

class SkillPackageTests(unittest.TestCase):
    def test_archive_has_self_contained_skill_and_trigger(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "skill.zip"
            count = packager.build(output)
            self.assertGreater(count, 25)
            with zipfile.ZipFile(output) as archive:
                names = archive.namelist()
                self.assertEqual(len(names), len(set(names)))
                self.assertTrue(all(name.startswith("software-factory/") and
                        ".." not in Path(name).parts for name in names))
                for name in ("SKILL.md", "references/operating-protocol.md",
                             "references/screen-design.md", "references/technology-economics.md",
                             "references/parallel-delivery.md", "scripts/claims.py",
                             "scripts/check.py", "templates/PROJECT-CHARTER.md"):
                    self.assertIn("software-factory/" + name, names)
                manifest = archive.read("software-factory/SKILL.md").decode("utf-8")
                self.assertIn("description: Use when", manifest)
                self.assertIn("relative to this SKILL.md directory", manifest)
                self.assertNotIn("Reference paths are relative to this repository root", manifest)
                self.assertTrue(all(z.file_size < 500000 for z in archive.infolist()))
                self.assertIsNone(archive.testzip())

    def test_reproducible_archive_bytes(self):
        with tempfile.TemporaryDirectory() as temporary:
            first = Path(temporary) / "first.zip"
            second = Path(temporary) / "second.zip"
            packager.build(first)
            packager.build(second)
            self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_missing_source_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".agents/skills/software-factory").mkdir(parents=True)
            (root / ".agents/skills/software-factory/SKILL.md").write_text(
                "---\nname: software-factory\ndescription: Use when planning software.\n---",
                encoding="utf-8")
            (root / "references").mkdir()
            (root / "scripts").mkdir()
            (root / "templates").mkdir()
            with self.assertRaises(ValueError):
                packager.build(root / "out.zip", root)

if __name__ == "__main__":
    unittest.main()
