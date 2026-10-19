"""Behavior regression for universal profile selection, safe upgrades and proof claims."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('universal_factory', ROOT / 'scripts/factory.py')
fac = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fac)


class UniversalFactoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.project = self.root / 'project'
        self.project.mkdir()

    def test_all_packs_present_and_scaffold_proportional(self):
        for profile in fac.PROFILES:
            p = self.root / profile
            p.mkdir()
            result = fac.init(p, ROOT, 'Create meaningful deliverable', profile)
            self.assertEqual(profile, result['profile'])
            self.assertEqual([], fac.check(p))
            self.assertTrue((p / f'.factory/packs/{profile}/PLAYBOOK.md').is_file())
            self.assertEqual((p / 'docs/EXPERIENCE.md').exists(),
                             'EXPERIENCE.md' in fac.PROFILE_TEMPLATES[profile])
            self.assertLessEqual(len(list((p / 'docs').iterdir())), 6)

    def test_quick_publishing_only_one_work_document(self):
        r = fac.init(self.project, ROOT, 'Write an article', 'publishing', 'quick')
        self.assertEqual('quick', r['depth'])
        self.assertEqual(['WORK-OUTCOME.md'], [p.name for p in (self.project / 'docs').iterdir()])

    def test_auto_route_ties_do_not_fake_confidence(self):
        self.assertEqual('publishing', fac.choose_profile('publish an article'))
        self.assertEqual('automation', fac.choose_profile('create MCP tool'))
        self.assertEqual('general', fac.choose_profile('write an article using MCP'))
        self.assertEqual('general', fac.choose_profile('some unusual task'))

    def test_high_assurance_is_inferred_and_scaffolded(self):
        result = fac.init(self.project, ROOT, 'build wallet', 'software')
        self.assertEqual('high-assurance', result['depth'])
        self.assertTrue((self.project / 'docs/RISK-AND-APPROVALS.md').is_file())
        self.assertTrue((self.project / '.factory/bin/claims.py').is_file())

    def test_user_owned_agents_not_overwritten(self):
        f = self.project / 'AGENTS.md'
        f.write_text('owner-specific rules')
        result = fac.init(self.project, ROOT, 'research study', 'research')
        self.assertEqual(1, result['preserved'])
        self.assertIsNone(fac.load_manifest(self.project)['files']['AGENTS.md'])
        self.assertEqual('owner-specific rules', f.read_text())

    def test_upgrade_dry_run_preserves_customizations(self):
        fac.init(self.project, ROOT, 'research study', 'research')
        local = self.project / 'docs/WORK-OUTCOME.md'
        local.write_text('my edits')
        before = (self.project / '.factory/work-manifest.json').read_bytes()
        plan = fac.upgrade(self.project, ROOT)
        self.assertIn({'path': 'docs/WORK-OUTCOME.md', 'action': 'PRESERVE_LOCAL'}, plan)
        self.assertEqual(before, (self.project / '.factory/work-manifest.json').read_bytes())
        fac.upgrade(self.project, ROOT, apply=True)
        self.assertEqual('my edits', local.read_text())

    def test_upstream_updates_only_unmodified_files(self):
        kit = self.root / 'kit'
        kit.mkdir()
        import shutil
        shutil.copytree(ROOT / 'factory', kit / 'factory')
        shutil.copytree(ROOT / '.agents', kit / '.agents')
        (kit / 'scripts').mkdir()
        shutil.copy(ROOT / 'scripts/factory.py', kit / 'scripts/factory.py')
        (kit / 'factory/tools').mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / 'factory/tools/github_claims.py', kit / 'factory/tools/github_claims.py')
        fac.init(self.project, kit, 'research study', 'research')
        f = kit / 'factory/core/routing.md'
        f.write_text('upstream new')
        expected = {'path': '.factory/core/routing.md', 'action': 'UPDATE'}
        self.assertIn(expected, fac.upgrade(self.project, kit))
        self.assertNotEqual('upstream new', (self.project / '.factory/core/routing.md').read_text())
        fac.upgrade(self.project, kit, apply=True)
        self.assertEqual('upstream new', (self.project / '.factory/core/routing.md').read_text())

    def test_symlink_escape_rejected(self):
        outside = self.root / 'outside'
        outside.mkdir()
        (self.project / '.factory').symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'Symlink'):
            fac.init(self.project, ROOT, 'idea', 'general')
        self.assertEqual([], list(outside.iterdir()))

    def test_reinit_rejected(self):
        fac.init(self.project, ROOT, 'first', 'general')
        with self.assertRaisesRegex(ValueError, 'Already initialized'):
            fac.init(self.project, ROOT, 'second', 'software')

    def test_false_verification_does_not_pass(self):
        fac.init(self.project, ROOT, 'compare providers', 'research')
        f = self.project / '.factory/evidence.json'
        f.write_text(json.dumps({'status':'VERIFIED','proof':[{'result':'PASS_SIMULATED'}]}))
        self.assertIn('VERIFICATION_WITHOUT_REAL_PROOF', fac.check(self.project, 'release'))
        f.write_text(json.dumps({'status':'PLANNED'}))
        self.assertIn('NOT_VERIFIED', fac.check(self.project, 'release'))

    def test_high_assurance_requires_approval_and_code_sha(self):
        fac.init(self.project, ROOT, 'financial wallet', 'software')
        f = self.project / '.factory/evidence.json'
        f.write_text(json.dumps({'status':'VERIFIED', 'proof':[
            {'description':'real run', 'artifact':'receipt', 'method':'test','result':'PASS_REAL'}]}))
        problems = fac.check(self.project, 'release')
        self.assertIn('HIGH_ASSURANCE_APPROVAL_MISSING', problems)
        self.assertIn('CODE_PROOF_WITHOUT_SHA', problems)

    def test_path_traversal_in_manifest_blocked(self):
        fac.init(self.project, ROOT, 'research', 'research')
        m = fac.load_manifest(self.project)
        m['files']['../steal'] = None
        (self.project / '.factory/work-manifest.json').write_text(json.dumps(m))
        self.assertIn('UNSAFE_PATH ../steal', fac.check(self.project))


if __name__ == '__main__':
    unittest.main()
