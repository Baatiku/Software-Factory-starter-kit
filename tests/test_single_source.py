"""Single current Factory verification; no parallel software-only toolkit."""
import importlib.util
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('kit_checker',ROOT/'scripts/check_kit.py')
checker=importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

class SoleFactoryTests(unittest.TestCase):
    def test_single_canonical_kit(self):
        self.assertEqual([], checker.check(ROOT))
    def test_all_packs_loadable(self):
        for p in checker.PROFILES:
            self.assertTrue((ROOT/'.agents/skills'/f'{p}-work/SKILL.md').is_file())
            self.assertTrue((ROOT/'factory/packs'/p/'PLAYBOOK.md').is_file())
    def test_only_current_packaging_and_bootstrap(self):
        self.assertFalse((ROOT/'scripts/bootstrap.py').exists())
        self.assertFalse((ROOT/'scripts/package_skill.py').exists())
        self.assertFalse((ROOT/'.agents/skills/software-factory/SKILL.md').exists())
        self.assertFalse((ROOT/'templates').exists())
        self.assertFalse((ROOT/'references').exists())
    def test_no_outdated_local_installation_instruction(self):
        data=(ROOT/'install/CUSTOM-INSTRUCTIONS.txt').read_text()
        self.assertIn('.agents/skills/work-factory/SKILL.md',data)
        self.assertNotIn('.agents/skills/software-factory/',data)
if __name__ == '__main__':
    unittest.main()
