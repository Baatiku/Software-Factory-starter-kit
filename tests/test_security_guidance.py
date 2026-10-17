"""Structural regression for the factory's reusable authentication lessons.

This is a guidance contract test, not an authentication or provider e2e test.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SecurityGuidanceTest(unittest.TestCase):
    def test_sensitive_auth_boundary_rules_retained(self):
        guidance = (ROOT / "references" / "security-privacy-operations.md").read_text(
            encoding="utf-8"
        ).lower()
        for principle in (
            "purpose-bound one-time codes",
            "alternate token-minting routes",
            "single-use server grant",
            "exact callback routes",
            "raw request bytes",
            "cross-purpose replay",
        ):
            with self.subTest(principle=principle):
                self.assertIn(principle, guidance)

    def test_change_has_changelog_rationale(self):
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8").lower()
        self.assertIn("one-time code purposes", changelog)
        self.assertIn("guidance-only change", changelog)


if __name__ == "__main__":
    unittest.main()
