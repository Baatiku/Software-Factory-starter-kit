"""Exercise generated upgrade rules, milestone validation and portable skill propagation."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]

def load(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT / file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

bootstrap = load("outcome_bootstrap", "scripts/bootstrap.py")
checker = load("outcome_check", "scripts/check.py")
packager = load("outcome_package", "scripts/package_skill.py")

class OutcomeDeliveryTests(unittest.TestCase):
    def bootstrap(self, project):
        with contextlib.redirect_stdout(io.StringIO()):
            return bootstrap.bootstrap(project, "Upgrade an existing appointment app", ROOT / "templates")

    def partial(self):
        return {
            "delivery_schema_version": 1, "milestone_id": "booking",
            "journeys": ["J-001"], "source_complete": False,
            "remaining_source": ["Connect booking API and client readback"],
            "blocked_actions": [{"reason": "Runner unavailable", "owner": "build-window",
                                "next_action": "Run named exact-head tests"}],
            "status": "PARTIAL_IMPLEMENTATION",
        }

    def test_new_project_inherits_customer_milestones_and_blocker_ownership(self):
        with tempfile.TemporaryDirectory() as d:
            project = Path(d)
            self.bootstrap(project)
            for name in ("AGENTS.md", "CONTINUE-HERE.md", "docs/WORKSTREAMS.md",
                         "docs/WINDOW-HANDOFF.md", ".agents/skills/software-factory/SKILL.md"):
                text = (project / name).read_text()
                self.assertIn("milestone", text, name)
            for name in ("AGENTS.md", "CONTINUE-HERE.md", "docs/WORKSTREAMS.md",
                         "docs/WINDOW-HANDOFF.md"):
                self.assertIn("next", (project / name).read_text().lower(), name)
            self.assertIn("bounded", (project / "AGENTS.md").read_text())
            self.assertIn("canonical", (project / "CONTINUE-HERE.md").read_text())
            self.assertEqual("0.4.4", (project / ".factory/FACTORY-VERSION").read_text().strip())
            self.assertEqual([], checker.check(project, "scaffold"))

    def test_repeat_bootstrap_preserves_customized_upgrade_rules(self):
        with tempfile.TemporaryDirectory() as d:
            project = Path(d)
            self.bootstrap(project)
            (project / "AGENTS.md").write_text("custom current journey policy")
            created, preserved = self.bootstrap(project)
            self.assertEqual(0, created)
            self.assertGreater(preserved, 0)
            self.assertEqual("custom current journey policy", (project / "AGENTS.md").read_text())

    def test_partial_guard_cannot_claim_source_complete_or_verified(self):
        handoff = self.partial()
        handoff["status"] = "IMPLEMENTED_UNVERIFIED"
        self.assertIn("DELIVERY PARTIAL SOURCE MISCLASSIFIED", checker.check_delivery_handoff(handoff))
        handoff["source_complete"] = True
        self.assertIn("DELIVERY COMPLETE WITH SOURCE REMAINING", checker.check_delivery_handoff(handoff))

    def test_blocker_needs_owner_and_next_executable_action(self):
        handoff = self.partial()
        handoff["blocked_actions"] = [{"reason": "Waiting for integration"}]
        self.assertIn("DELIVERY BLOCKER MISSING REASON/OWNER/NEXT ACTION",
                      checker.check_delivery_handoff(handoff))

    def test_valid_partial_and_legacy_handoffs_remain_compatible(self):
        self.assertEqual([], checker.check_delivery_handoff(self.partial()))
        self.assertEqual([], checker.check_delivery_handoff({"status": "PARTIAL_IMPLEMENTATION"}))

    def test_delivery_validation_is_used_by_existing_handoff_gate(self):
        with tempfile.TemporaryDirectory() as d:
            project = Path(d)
            self.bootstrap(project)
            handoff = self.partial()
            handoff.update(base_sha="a"*40, head_sha="b"*40, paths=["src/booking.py"],
                           pr="https://github.com/example/project/pull/1", tests=[{"status": "NOT_RUN"}])
            handoff["blocked_actions"] = [{"reason": "Waiting"}]
            (project / "docs/workstreams/booking.json").write_text(json.dumps(handoff))
            self.assertTrue(any("DELIVERY BLOCKER" in issue for issue in checker.check(project, "handoff")))

    def test_packaged_skill_includes_outcome_policy_and_updated_templates(self):
        with tempfile.TemporaryDirectory() as d:
            output = Path(d) / "factory.zip"
            packager.build(output)
            with zipfile.ZipFile(output) as archive:
                self.assertIn("v0.4.4", archive.read("software-factory/SKILL.md").decode())
                self.assertIn("Dispatch complete customer milestones",
                              archive.read("software-factory/SKILL.md").decode())
                self.assertIn("source_complete",
                              archive.read("software-factory/templates/WINDOW-HANDOFF.md").decode())
                self.assertIn("check_delivery_handoff",
                              archive.read("software-factory/scripts/check.py").decode())

if __name__ == "__main__":
    unittest.main()

