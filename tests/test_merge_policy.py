"""Policy regression tests: code integration must not be confused with production release."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class MergeFirstPolicyTests(unittest.TestCase):
    def test_skill_has_separate_code_merge_and_release_gates(self):
        skill = read(".agents/skills/software-factory/SKILL.md")
        self.assertIn("Before code merge", skill)
        self.assertIn("Before release", skill)
        self.assertIn("Merge completed, compatible changes promptly", skill)
        self.assertIn("production release", skill)

    def test_parallel_delivery_prefers_merge_but_never_unsafe_main(self):
        guide = read("references/parallel-delivery.md")
        self.assertIn("Merge-first delivery", guide)
        self.assertIn("Code merge is the default", guide)
        self.assertIn("If CI cannot start", guide)
        self.assertIn("automatic deploy trigger", guide)
        self.assertIn("non-deploying integration branch", guide)
        self.assertIn("Never force-merge an actual code/test failure", guide)
        self.assertNotIn("Merge in dependency order only after executable proof.", guide)

    def test_release_evidence_remains_mandatory(self):
        guide = read("references/verification-and-release.md")
        self.assertIn("Integration gate versus production release gate", guide)
        self.assertIn("A merge to main must", guide)
        self.assertIn("off-account backup restored", read("templates/RELEASE-GATES.md"))
        self.assertIn("Human approval for production", read("templates/RELEASE-GATES.md"))

    def test_bootstrap_inherits_merge_first_without_overwriting_customizations(self):
        spec = importlib.util.spec_from_file_location("factory_bootstrap_merge", ROOT / "scripts/bootstrap.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            module.bootstrap(project, "Safe integration sample", ROOT / "templates")
            agent = (project / "AGENTS.md").read_text(encoding="utf-8")
            guide = (project / ".factory/playbooks/parallel-delivery.md").read_text(encoding="utf-8")
            self.assertIn("integrating its compatible tested changes", agent)
            self.assertIn("Merge-first delivery", guide)
            self.assertEqual("0.4.3", (project / ".factory/FACTORY-VERSION").read_text().strip())
            module.bootstrap(project, "Other idea", ROOT / "templates")
            self.assertIn("Merge-first delivery", (project / ".factory/playbooks/parallel-delivery.md").read_text())

if __name__ == "__main__":
    unittest.main()
