"""Test that the factory rejects incomplete/falsely verified projects."""
import importlib.util
import json
import re
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



    def test_completed_minimal_design_is_structurally_accepted(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            bootstrap.bootstrap(p, 'Simple queueing app', ROOT / 'templates')
            docs = p / 'docs'
            for name in checker.REQUIRED:
                if not name.endswith('.md'):
                    continue
                path = docs / name
                value = path.read_text(encoding='utf-8')
                path.write_text(re.sub(r'<!-- TODO.*?-->', 'Reviewed and recorded', value, flags=re.S),
                                encoding='utf-8')
            (docs / 'SCREEN-INVENTORY.md').write_text(
                '| SC-001 | Home | user | / | F-001 | J-001 | ACCEPTED |\n', encoding='utf-8')
            (docs / 'SCREEN-SPECS.md').write_text(
                '## SC-001\nLayout Controls States Data Access Proof\n', encoding='utf-8')
            (docs / 'TRACEABILITY.json').write_text(json.dumps({
                'requirements': [{'id': 'REQ-001', 'scope': 'CORE_NOW', 'screens': ['SC-001'],
                                  'journeys': ['J-001'], 'owners': ['U01'], 'tests': ['T-001']}],
                'screens': [{'id': 'SC-001'}], 'journeys': [{'id': 'J-001'}],
                'workstreams': [{'id': 'U01'}]
            }), encoding='utf-8')
            self.assertEqual([], checker.check(p, 'design'))

    def test_simulated_workstream_verification_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            bootstrap.bootstrap(p, 'test', ROOT / 'templates')
            goodsha = 'a' * 40
            (p / 'docs/workstreams/w1.json').write_text(json.dumps({
                'base_sha': goodsha, 'head_sha': goodsha, 'status': 'VERIFIED_E2E',
                'paths': ['services/api.py'], 'pr': 'https://github.com/example/pr/1',
                'tests': [{'status': 'PASS_SIMULATED', 'command': 'pytest',
                           'commit_sha': goodsha, 'artifact': 'mock-result.txt'}]
            }), encoding='utf-8')
            findings = checker.check(p, 'handoff')
            self.assertTrue(any('VERIFIED CLAIM WITHOUT PASS_REAL' in i for i in findings), findings)


    def test_new_project_contains_local_skill_and_tools(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            created, preserved = bootstrap.bootstrap(p, 'Build a simple project', ROOT / 'templates')
            self.assertGreater(created, 25)
            self.assertEqual(0, preserved)
            skill = (p / '.agents/skills/software-factory/SKILL.md').read_text(encoding='utf-8')
            self.assertIn('.factory/playbooks/screen-design.md', skill)
            self.assertIn('.factory/bin/claims.py', skill)
            self.assertTrue((p / '.factory/playbooks/verification-and-release.md').is_file())
            self.assertTrue((p / '.factory/bin/check.py').is_file())
            self.assertTrue((p / '.factory/bin/claims.py').is_file())
            self.assertRegex((p / '.factory/FACTORY-VERSION').read_text(encoding='utf-8'), r'^\d+\.\d+\.\d+\n
    unittest.main()
)
            self.assertEqual([], checker.check(p, 'scaffold'))

    def test_repeat_scaffold_preserves_customizations_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            custom_skill = p / '.agents/skills/software-factory/SKILL.md'
            custom_skill.parent.mkdir(parents=True)
            custom_skill.write_text('project-specific skill', encoding='utf-8')
            custom_ref = p / '.factory/playbooks/operating-protocol.md'
            custom_ref.parent.mkdir(parents=True)
            custom_ref.write_text('custom playbook', encoding='utf-8')
            created, preserved = bootstrap.bootstrap(p, 'First idea', ROOT / 'templates')
            self.assertGreater(created, 0)
            self.assertGreaterEqual(preserved, 2)
            second_created, second_preserved = bootstrap.bootstrap(p, 'Different idea', ROOT / 'templates')
            self.assertEqual(0, second_created)
            self.assertGreater(second_preserved, preserved)
            self.assertEqual('project-specific skill', custom_skill.read_text(encoding='utf-8'))
            self.assertEqual('custom playbook', custom_ref.read_text(encoding='utf-8'))
            self.assertIn('First idea', (p / 'docs/PROJECT-CHARTER.md').read_text(encoding='utf-8'))

    def test_does_not_scaffold_factory_into_itself(self):
        with self.assertRaisesRegex(ValueError, 'target project'):
            bootstrap.bootstrap(ROOT, 'should fail', ROOT / 'templates')

if __name__ == '__main__':
    unittest.main()
