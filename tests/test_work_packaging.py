"""Deterministic ZIP packaging checks without external tools."""
import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
s = importlib.util.spec_from_file_location('pack_work', ROOT / 'scripts/package_work_factory.py')
import sys
sys.path.insert(0, str(ROOT / 'scripts'))
mod = importlib.util.module_from_spec(s)
s.loader.exec_module(mod)


class WorkFactoryPackageTests(unittest.TestCase):
    def test_full_and_single_pack_archives(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'all.zip'
            self.assertGreater(mod.build(p), 30)
            a = p.read_bytes()
            mod.build(p)
            self.assertEqual(a, p.read_bytes())
            with zipfile.ZipFile(p) as z:
                self.assertIsNone(z.testzip())
                self.assertIn('work-factory/SKILL.md', z.namelist())
                self.assertIn('work-factory/packs/analytics/PLAYBOOK.md', z.namelist())
            p2 = Path(d) / 'research.zip'
            mod.build(p2, 'research')
            with zipfile.ZipFile(p2) as z:
                self.assertIn('work-factory/packs/research/PLAYBOOK.md', z.namelist())
                self.assertNotIn('work-factory/packs/software/PLAYBOOK.md', z.namelist())

    def test_unknown_pack_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                mod.build(Path(d) / 'a.zip', 'unknown')


if __name__ == '__main__':
    unittest.main()
