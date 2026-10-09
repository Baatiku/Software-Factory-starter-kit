"""Test that the factory rejects incomplete/falsely verified projects."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bootstrap = load('factory_bootstrap', ROOT / 'scripts' / 'bootstrap.py')
checker = load('factory_check', ROOT / 'scripts' / 'check.py')


class FactoryTests(unittest.TestCase):
    def test_kit_has_required_files(self):
        self.assertEqual([], checker.check(ROOT, 'kit'))

    def test_bootstrap_preserves_existing_and_is_not_design_ready(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / 'AGENTS.md').write_text('original', encoding='utf-8')
            bootstrap.bootstrap(p, 'Build a simple queueing app', ROOT / 'templates')
            self.assertEqual('original', (p / 'AGENTS.md').read_text(encoding='utf-8'))
            self.assertIn('Build a simple queueing app', (p / 'docs/PROJECT-CHARTER.md').read_text(encoding='utf-8'))
            self.assertEqual([], checker.check(p, 'scaffold'))
            self.assertTrue(checker.check(p, 'design'))
            self.assertTrue(checker.check(p, 'release'))

    def test_screen_and_traceability_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            bootstrap.bootstrap(p, 'test', ROOT / 'templates')
            f = p / 'docs/SCREEN-INVENTORY.md'
            f.write_text('| SC-001 | Home | user | / | CORE | draft |\n', encoding='utf-8')
            g = p / 'docs/SCREEN-SPECS.md'
            g.write_text('## SC-002\nLayout Controls States Data Access Proof\n', encoding='utf-8')
            findings = checker.check(p, 'design')
            self.assertTrue(any('ONE-TO-ONE' in i for i in findings), findings)

    def test_handoff_requires_real_shas(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            bootstrap.bootstrap(p, 'test', ROOT / 'templates')
            (p / 'docs/workstreams/w1.json').write_text(json.dumps({'base_sha':'latest','head_sha':'main','status':'VERIFIED_E2E','paths':['foo'],'tests':['pass'],'pr':'https://github.com/example'}), encoding='utf-8')
            findings = checker.check(p, 'handoff')
            self.assertTrue(any('HANDOFF MISSING COMMIT SHAS' in i for i in findings), findings)


if __name__ == '__main__':
    unittest.main()
