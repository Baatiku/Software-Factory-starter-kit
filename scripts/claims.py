#!/usr/bin/env python3
"""GitHub-backed, compare-and-swap workstream ownership claims.

This provides *atomic updates to one registry file* via GitHub Contents API
blob-SHA preconditions. It cannot police direct Git writes, bypassing agents,
or identify who is authorized to resolve abandoned work.
"""
import argparse
import base64
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

REGISTRY_PATH = ".factory/leases.json"
COORD_BRANCH = "factory/claims"
LEASE_SECONDS = 300
MAX_RETRIES = 6
SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")
REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
PATH_RE = re.compile(r"^[A-Za-z0-9_.@/+ -]+(?:/\*\*)?$")


class ClaimError(Exception):
    pass


class ApiError(ClaimError):
    def __init__(self, status, message):
        super().__init__(f"GitHub HTTP {status}: {message}")
        self.status = status


def timestamp(now=None):
    value = now or dt.datetime.now(dt.timezone.utc)
    return value.astimezone(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_time(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def normalize_path(raw):
    if not isinstance(raw, str):
        raise ClaimError("Paths must be strings")
    path = raw.strip().replace("\\", "/")
    if (not path or path.startswith("/") or path.endswith("/")
            or path in (".", "..") or "//" in path
            or any(part in (".", "..") for part in path.split("/"))
            or not PATH_RE.fullmatch(path)):
        raise ClaimError(f"Unsafe or unsupported path: {raw!r}; use exact paths or directory/**")
    if path.startswith((".git/", ".factory/")) or path in (".git", ".factory"):
        raise ClaimError("Claiming Git internals or the ownership registry is forbidden")
    if "*" in path and not path.endswith("/**"):
        raise ClaimError("Only directory/** wildcards are supported")
    return path


def normalize_paths(paths):
    result = sorted(set(normalize_path(p) for p in paths))
    if not result:
        raise ClaimError("At least one exact file or directory/** path is required")
    if len(result) > 100:
        raise ClaimError("At most 100 paths per workstream; use reviewed directory roots")
    return result


def conflicts(a, b):
    """Exact files and nested directory/** scopes, on segment boundaries."""
    if a == b:
        return True
    a_dir, b_dir = a.endswith("/**"), b.endswith("/**")
    a_root = a[:-3] if a_dir else a
    b_root = b[:-3] if b_dir else b
    return ((a_dir and b_root.startswith(a_root + "/"))
            or (b_dir and a_root.startswith(b_root + "/")))


def new_registry():
    return {"schema_version": 1, "active": [], "history": []}


class GithubContents:
    """All mutations are blob-SHA-guarded contents writes on one coordination branch."""
    def __init__(self, repo, token, branch=COORD_BRANCH):
        if not REPO_RE.fullmatch(repo):
            raise ClaimError("Repository must be owner/name")
        if not token:
            raise ClaimError("GITHUB_TOKEN or GH_TOKEN required; use least-privilege contents:write")
        self.repo, self.token, self.branch = repo, token, branch
        self.root = "https://api.github.com/repos/" + repo

    def request(self, method, suffix, payload=None):
        url = self.root + suffix
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        headers = {
            "Authorization": "Bearer " + self.token,
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "software-factory-claims/0.4",
        }
        if data is not None:
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                raw = response.read()
            return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            # Never print or return credentials or response headers.
            try:
                body = json.loads(exc.read().decode("utf-8"))
                reason = body.get("message", "request failed")
            except (ValueError, UnicodeError):
                reason = "request failed"
            raise ApiError(exc.code, reason) from None
        except urllib.error.URLError as exc:
            raise ClaimError("GitHub network request failed; no ownership change confirmed") from exc

    def ensure_branch(self):
        escaped = urllib.parse.quote(self.branch, safe="/")
        try:
            self.request("GET", "/git/ref/heads/" + escaped)
            return
        except ApiError as exc:
            if exc.status != 404:
                raise
        info = self.request("GET", "")
        default = info["default_branch"]
        base_ref = self.request("GET", "/git/ref/heads/" + urllib.parse.quote(default, safe="/"))
        try:
            self.request("POST", "/git/refs", {"ref": "refs/heads/" + self.branch,
                                               "sha": base_ref["object"]["sha"]})
        except ApiError as exc:
            if exc.status != 422:
                raise
            # Another claimant may have created the branch first.
            self.request("GET", "/git/ref/heads/" + escaped)

    def read(self):
        path = urllib.parse.quote(REGISTRY_PATH, safe="/")
        query = urllib.parse.urlencode({"ref": self.branch})
        try:
            value = self.request("GET", "/contents/" + path + "?" + query)
        except ApiError as exc:
            if exc.status == 404:
                return None, None
            raise
        if value.get("encoding") != "base64" or not value.get("sha"):
            raise ClaimError("GitHub registry response malformed")
        registry = json.loads(base64.b64decode(value["content"]).decode("utf-8"))
        if not isinstance(registry, dict) or registry.get("schema_version") != 1:
            raise ClaimError("Unsupported ownership registry schema; refuse writes")
        if not isinstance(registry.get("active"), list) or not isinstance(registry.get("history"), list):
            raise ClaimError("Corrupt ownership registry; refuse writes")
        return registry, value["sha"]

    def write(self, registry, expected_sha, message):
        payload = {
            "message": message,
            "branch": self.branch,
            "content": base64.b64encode((json.dumps(registry, indent=2, sort_keys=True) + "\n").encode("utf-8")).decode("ascii"),
        }
        if expected_sha:
            payload["sha"] = expected_sha
        self.request("PUT", "/contents/" + urllib.parse.quote(REGISTRY_PATH, safe="/"), payload)


class Coordinator:
    def __init__(self, store, now=None, sleep=None):
        self.store = store
        self.clock = now or (lambda: dt.datetime.now(dt.timezone.utc))
        self.sleep = sleep or time.sleep

    def snapshot(self):
        value, _ = self.store.read()
        return value if value is not None else new_registry()

    def update(self, mutation, message):
        for attempt in range(MAX_RETRIES):
            state, sha = self.store.read()
            state = state if state is not None else new_registry()
            result = mutation(state)
            if result is None:
                return state
            try:
                self.store.write(state, sha, message)
                return result
            except ApiError as exc:
                if exc.status not in (409, 422) or attempt == MAX_RETRIES - 1:
                    raise
                # Retry on changed branch head/content; re-evaluate conflicts on fresh data.
                self.sleep(min(0.1 * (2 ** attempt), 1.0))
        raise ClaimError("Unable to acquire ownership after CAS retries")

    def claim(self, *, owner, scope, paths, branch, base_sha, pr=""):
        for key, value in (("owner", owner), ("scope", scope), ("branch", branch)):
            if not value or not isinstance(value, str) or len(value) > 128:
                raise ClaimError(f"Valid {key} is required")
        if not SHA_RE.fullmatch(base_sha):
            raise ClaimError("base_sha must be a real 40-character commit SHA")
        if pr and not re.fullmatch(r"https://github\.com/[^/]+/[^/]+/pull/\d+", pr):
            raise ClaimError("pr must be a GitHub pull request URL")
        paths = normalize_paths(paths)
        instant = self.clock()
        record = {
            "claim_id": str(uuid.uuid4()), "owner": owner, "scope": scope,
            "paths": paths, "branch": branch, "base_sha": base_sha.lower(),
            "pr": pr, "claimed_at": timestamp(instant),
            "heartbeat_at": timestamp(instant),
            "expires_at": timestamp(instant + dt.timedelta(seconds=LEASE_SECONDS)),
        }

        def mutate(state):
            for existing in state["active"]:
                for old in existing["paths"]:
                    for new in paths:
                        if conflicts(new, old):
                            stale = self.clock() >= parse_time(existing["expires_at"])
                            label = "STALE — REVIEW REQUIRED" if stale else "ACTIVE"
                            raise ClaimError(f"Ownership conflict with {existing['scope']}/{existing['owner']} "
                                             f"({label}, {old} vs {new}). Do not overwrite unmerged work.")
            state["active"].append(record)
            return record

        return self.update(mutate, "factory: claim " + scope + " by " + owner)

    def heartbeat(self, claim_id, owner):
        now = self.clock()
        def mutate(state):
            for entry in state["active"]:
                if entry["claim_id"] == claim_id:
                    if entry["owner"] != owner:
                        raise ClaimError("Only the recorded owner may heartbeat")
                    entry["heartbeat_at"] = timestamp(now)
                    entry["expires_at"] = timestamp(now + dt.timedelta(seconds=LEASE_SECONDS))
                    return dict(entry)
            raise ClaimError("Unknown claim; it may have been released. Recheck live work.")
        return self.update(mutate, "factory: renew " + claim_id)

    def release(self, claim_id, owner, reason):
        if not reason or not reason.strip():
            raise ClaimError("Release requires a reason and recorded handoff")
        now = self.clock()
        def mutate(state):
            for i, entry in enumerate(state["active"]):
                if entry["claim_id"] == claim_id:
                    if entry["owner"] != owner:
                        raise ClaimError("Only claim owner can release via CLI; stale recovery needs reviewed registry PR")
                    outgoing = state["active"].pop(i)
                    outgoing["released_at"] = timestamp(now)
                    outgoing["release_reason"] = reason.strip()
                    state["history"].append(outgoing)
                    return outgoing
            raise ClaimError("Unknown claim; cannot release")
        return self.update(mutate, "factory: release " + claim_id)

    def status(self, paths=None):
        current = self.snapshot()
        at = self.clock()
        sought = normalize_paths(paths) if paths else None
        result = []
        for entry in current["active"]:
            item = dict(entry)
            item["lease_state"] = "STALE_REVIEW_REQUIRED" if at >= parse_time(item["expires_at"]) else "ACTIVE"
            if sought is None or any(conflicts(a, b) for a in sought for b in item["paths"]):
                result.append(item)
        return {"repo": getattr(self.store, "repo", None), "as_of": timestamp(at),
                "active": result, "history_count": len(current["history"])}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", required=True, help="owner/name, with contents:write token")
    p.add_argument("--coord-branch", default=COORD_BRANCH)
    sub = p.add_subparsers(dest="command", required=True)
    claim = sub.add_parser("claim")
    claim.add_argument("--owner", required=True)
    claim.add_argument("--scope", required=True)
    claim.add_argument("--path", action="append", required=True, dest="paths")
    claim.add_argument("--branch", required=True)
    claim.add_argument("--base-sha", required=True)
    claim.add_argument("--pr", default="")
    heartbeat = sub.add_parser("heartbeat")
    heartbeat.add_argument("--owner", required=True)
    heartbeat.add_argument("--claim-id", required=True)
    release = sub.add_parser("release")
    release.add_argument("--owner", required=True)
    release.add_argument("--claim-id", required=True)
    release.add_argument("--reason", required=True)
    status = sub.add_parser("status")
    status.add_argument("--path", action="append", dest="paths")
    args = p.parse_args(argv)
    try:
        store = GithubContents(args.repo, os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN"),
                               branch=args.coord_branch)
        if args.command == "claim":
            store.ensure_branch()
        coord = Coordinator(store)
        if args.command == "claim":
            output = coord.claim(owner=args.owner, scope=args.scope, paths=args.paths,
                                 branch=args.branch, base_sha=args.base_sha, pr=args.pr)
        elif args.command == "heartbeat":
            output = coord.heartbeat(args.claim_id, args.owner)
        elif args.command == "release":
            output = coord.release(args.claim_id, args.owner, args.reason)
        else:
            output = coord.status(args.paths)
        print(json.dumps(output, indent=2, sort_keys=True))
        return 0
    except (ClaimError, ValueError, KeyError) as exc:
        print("OWNERSHIP NOT CHANGED/NOT CONFIRMED: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
