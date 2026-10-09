"""Deterministic concurrency and safety tests for GitHub CAS ownership registry."""
import datetime as dt
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("factory_claims", ROOT / "scripts" / "claims.py")
claims = importlib.util.module_from_spec(spec)
spec.loader.exec_module(claims)


class FakeStore:
    repo = "Baatiku/example"
    def __init__(self):
        self.state = None
        self.revision = 0
        self.fail_next_write = None
        self.on_race = None
        self.writes = 0

    def read(self):
        return (json.loads(json.dumps(self.state)) if self.state is not None else None,
                str(self.revision) if self.state is not None else None)

    def write(self, state, expected_sha, message):
        self.writes += 1
        if self.on_race:
            callback = self.on_race
            self.on_race = None
            callback(self)
        if self.fail_next_write:
            status = self.fail_next_write
            self.fail_next_write = None
            raise claims.ApiError(status, "simulated contention")
        actual_sha = str(self.revision) if self.state is not None else None
        if expected_sha != actual_sha:
            raise claims.ApiError(409, "stale expected blob")
        self.state = json.loads(json.dumps(state))
        self.revision += 1


class CoordinatorTests(unittest.TestCase):
    def setUp(self):
        self.store = FakeStore()
        self.now = dt.datetime(2026, 10, 9, 12, tzinfo=dt.timezone.utc)
        self.coord = claims.Coordinator(self.store, now=lambda: self.now, sleep=lambda _: None)

    def acquire(self, owner="w1", scope="U01", paths=None):
        return self.coord.claim(owner=owner, scope=scope, paths=paths or ["apps/mobile/**"],
                                branch="work/u01", base_sha="a" * 40)

    def test_disjoint_claims_and_single_atomic_multi_path_record(self):
        first = self.acquire(paths=["apps/mobile/lib/a.dart", "services/gateway/**"])
        second = self.acquire(owner="w2", scope="U02", paths=["docs/design/**"])
        self.assertNotEqual(first["claim_id"], second["claim_id"])
        self.assertEqual(2, len(self.store.state["active"]))
        self.assertEqual(2, len(first["paths"]))
        self.assertEqual("ACTIVE", self.coord.status()["active"][0]["lease_state"])

    def test_exact_and_directory_overlap(self):
        self.acquire(paths=["apps/mobile/**"])
        for requested in (["apps/mobile"], ["apps/mobile/lib/page.dart"],
                          ["apps/mobile/lib/**"], ["apps/mobile/**"]):
            if requested == ["apps/mobile"]:
                # A claimed folder/** does not mean its same-named file.
                self.acquire(owner="folder-file", scope="U03", paths=requested)
            else:
                with self.assertRaisesRegex(claims.ClaimError, "Ownership conflict"):
                    self.acquire(owner="other", scope="U03", paths=requested)
        self.acquire(owner="other", scope="U03", paths=["apps/mobility/**"])

    def test_stale_still_blocks_and_owner_can_renew(self):
        lease = self.acquire()
        self.now += dt.timedelta(seconds=301)
        self.assertEqual("STALE_REVIEW_REQUIRED", self.coord.status()["active"][0]["lease_state"])
        with self.assertRaisesRegex(claims.ClaimError, "STALE"):
            self.acquire(owner="w2", scope="U02")
        updated = self.coord.heartbeat(lease["claim_id"], "w1")
        self.assertEqual("ACTIVE", self.coord.status()["active"][0]["lease_state"])
        self.assertNotEqual(lease["expires_at"], updated["expires_at"])

    def test_another_owner_cannot_heartbeat_or_release(self):
        lease = self.acquire()
        with self.assertRaisesRegex(claims.ClaimError, "Only"):
            self.coord.heartbeat(lease["claim_id"], "hijacker")
        with self.assertRaisesRegex(claims.ClaimError, "Only"):
            self.coord.release(lease["claim_id"], "hijacker", "steal")
        self.assertEqual(1, len(self.store.state["active"]))

    def test_release_is_audited_and_reopens_path(self):
        lease = self.acquire()
        result = self.coord.release(lease["claim_id"], "w1", "Handoff: PR #42")
        self.assertIn("released_at", result)
        self.assertEqual(1, len(self.store.state["history"]))
        self.assertFalse(self.store.state["active"])
        self.acquire(owner="w2", scope="U02")

    def test_single_write_conflict_retries_fresh_snapshot(self):
        self.store.fail_next_write = 409
        self.acquire()
        self.assertEqual(2, self.store.writes)

    def test_concurrent_claim_observed_after_sha_race(self):
        def concurrent_write(store):
            new = claims.new_registry()
            new["active"].append({
                "claim_id": "someone-else", "owner": "w2", "scope": "U02",
                "branch": "work/u02", "paths": ["apps/mobile/**"],
                "claimed_at": claims.timestamp(self.now),
                "expires_at": claims.timestamp(self.now + dt.timedelta(seconds=300))
            })
            store.state = new
            store.revision += 1
        self.store.on_race = concurrent_write
        with self.assertRaisesRegex(claims.ClaimError, "Ownership conflict"):
            self.acquire()
        self.assertEqual(1, len(self.store.state["active"]))
        self.assertEqual("w2", self.store.state["active"][0]["owner"])

    def test_retry_limit_prevents_infinite_conflict(self):
        class AlwaysConflict(FakeStore):
            def write(self, state, expected_sha, message):
                raise claims.ApiError(409, "changed again")
        coord = claims.Coordinator(AlwaysConflict(), now=lambda: self.now, sleep=lambda _: None)
        with self.assertRaises(claims.ApiError):
            coord.claim(owner="w1", scope="U01", paths=["app/**"],
                        branch="test", base_sha="a" * 40)

    def test_bad_paths_refused_without_write(self):
        paths = ["../secrets", "/etc/passwd", "a//b", "a/../b",
                 "a/*.dart", "a/*", ".factory/leases.json", ".git/config",
                 "x\\..\\oops", "a/b/", ""]
        for path in paths:
            with self.subTest(path=path):
                with self.assertRaises(claims.ClaimError):
                    self.acquire(paths=[path] if path else [""])
        self.assertIsNone(self.store.state)

    def test_empty_or_bad_sha_fails(self):
        with self.assertRaisesRegex(claims.ClaimError, "base_sha"):
            self.coord.claim(owner="w1", scope="U01", paths=["app/**"],
                             branch="test", base_sha="main")

    def test_pr_url_validate(self):
        with self.assertRaisesRegex(claims.ClaimError, "pull request URL"):
            self.coord.claim(owner="w1", scope="U01", paths=["app/**"],
                             branch="test", base_sha="a" * 40, pr="https://evil.test/pr/1")

    def test_status_filtered_by_path(self):
        self.acquire(paths=["apps/mobile/**"])
        self.acquire(owner="w2", scope="U02", paths=["services/gateway/**"])
        self.assertEqual(1, len(self.coord.status(["services/gateway/main.ts"])["active"]))

    def test_missing_release_reason_refused(self):
        lease = self.acquire()
        with self.assertRaisesRegex(claims.ClaimError, "reason"):
            self.coord.release(lease["claim_id"], "w1", "")


if __name__ == "__main__":
    unittest.main()
