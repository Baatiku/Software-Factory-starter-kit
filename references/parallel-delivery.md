# Safe parallel development and GitHub coordination

Multi-window speed is governed by the slowest shared integration bottleneck, not window count. Use a dependency graph and assign independent vertical slices with bounded paths; begin with canonical cross-slice interfaces. Preserve current PR source and historical debt; do not reinvent something already implemented on a draft branch.

## Five-minute exact-path claim

Before editing, inspect current main, open/draft PR touched files, workstream claims and dependency contracts. Publish scope ID, window/owner, exact glob/path list, claim time, expiry/heartbeat, base SHA, current branch/PR, dependency and risk. Recheck claims frequently. The optional `scripts/claims.py` coordinator acquires multiple paths atomically via a dedicated branch and GitHub Contents API blob-SHA compare-and-swap. It rechecks registry conflicts on every retry; only exact file names or directory/** roots are supported.

Protected areas have one integrator: root routing, auth, shared server composition, database migration registry, ledger/financial source, native configs, CI and production deployment. Workstreams propose compositional patches in handoffs rather than silently editing protected files.

## Handoff and collision policy

Each branch keeps an immutable evidence checkpoint: base SHA, head SHA, PR URL, changed paths, requirements/journeys covered, tests actually run, failures, environment, unavailable checks, migration strategy and next integrator steps. Source-done but missing composition is PARTIAL_IMPLEMENTATION. Full source but unrun proof is IMPLEMENTED_UNVERIFIED.

If two PRs overlap, identify semantically equivalent code and current tests, preserve both pending review, elect one canonical contract, and carry forward unique behavior. Never delete because a five-minute lease expired. Merge in dependency order only after executable proof.

## Coordinated claims and stale recovery

- Claim before edits, heartbeat within five minutes, and release after a SHA-specific PR handoff. Multiple owned paths use one registry record.
- Expired claims remain blocking. The original owner can renew or release; another window cannot silently steal work. Stale recovery requires a reviewed registry change after checking live PRs, branch heads and unfinished source.
- Owner names and base SHAs are user-provided fields, not verified GitHub identities. The registry guards cooperating writers only. Direct GitHub writes can bypass it; branch permissions/reviews remain necessary.
- Tokens must use least privilege, remain in secret storage, and never run on untrusted PR code with write permissions.
- CAS retries reject collisions including directory prefix overlaps. This is a single-registry-file GitHub atomicity mechanism, not a cross-repository lock or full distributed authorization system.
- The first release is tested with deterministic simulated collisions. A credentialed live GitHub write/read/heartbeat/release test is still outstanding.

Example usage is in README.md. Record all recovered stale claims in registry history and link the review. Never delete code or PRs on expiry.
