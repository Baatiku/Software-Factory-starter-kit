# Safe parallel development and GitHub coordination

Multi-window speed is governed by the slowest shared integration bottleneck, not window count. Use a dependency graph and assign independent vertical slices with bounded paths; begin with canonical cross-slice interfaces. Preserve current PR source and historical debt; do not reinvent something already implemented on a draft branch.

## Five-minute exact-path claim

Before editing, inspect current main, open/draft PR touched files, workstream claims and dependency contracts. Publish scope ID, window/owner, exact glob/path list, claim time, expiry/heartbeat, base SHA, current branch/PR, dependency and risk. Recheck claims frequently. Do not treat text leases as atomic locking; enforce single-writer decisions for contested high-risk files or build compare-and-swap GitHub coordination.

Protected areas have one integrator: root routing, auth, shared server composition, database migration registry, ledger/financial source, native configs, CI and production deployment. Workstreams propose compositional patches in handoffs rather than silently editing protected files.

## Handoff and collision policy

Each branch keeps an immutable evidence checkpoint: base SHA, head SHA, PR URL, changed paths, requirements/journeys covered, tests actually run, failures, environment, unavailable checks, migration strategy and next integrator steps. Source-done but missing composition is PARTIAL_IMPLEMENTATION. Full source but unrun proof is IMPLEMENTED_UNVERIFIED.

If two PRs overlap, identify semantically equivalent code and current tests, preserve both pending review, elect one canonical contract, and carry forward unique behavior. Never delete because a five-minute lease expired. Merge in dependency order only after executable proof.
