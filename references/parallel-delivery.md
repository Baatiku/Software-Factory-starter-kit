# Safe parallel development and GitHub coordination

Multi-window speed is governed by the slowest shared integration bottleneck, not window count. Use a dependency graph and assign independent vertical slices with bounded paths; begin with canonical cross-slice interfaces. Preserve current PR source and historical debt; do not reinvent something already implemented on a draft branch.

## Five-minute exact-path claim

Before editing, inspect current main, open/draft PR touched files, workstream claims and dependency contracts. Publish scope ID, window/owner, exact glob/path list, claim time, expiry/heartbeat, base SHA, current branch/PR, dependency and risk. Recheck claims frequently. The optional `scripts/claims.py` coordinator acquires multiple paths atomically via a dedicated branch and GitHub Contents API blob-SHA compare-and-swap. It rechecks registry conflicts on every retry; only exact file names or directory/** roots are supported.

Protected areas have one integrator: root routing, auth, shared server composition, database migration registry, ledger/financial source, native configs, CI and production deployment. Workstreams propose compositional patches in handoffs rather than silently editing protected files.

## Handoff and collision policy

Each branch keeps an immutable evidence checkpoint: base SHA, head SHA, PR URL, changed paths, requirements/journeys covered, tests actually run, failures, environment, unavailable checks, migration strategy and next integrator steps. Source-done but missing composition is PARTIAL_IMPLEMENTATION. Full source but unrun proof is IMPLEMENTED_UNVERIFIED.

If two PRs overlap, identify semantically equivalent code and current tests, preserve both pending review, elect one canonical contract, and carry forward unique behavior. Never delete because a five-minute lease expired. Merge in dependency order after **appropriate executable source/contract proof**; do not require full production-provider or cutover proof merely to integrate compatible code. Fix known code/security failures before merging.

## Merge-first delivery: two separate gates

**Code merge is the default end of each completed workstream, not a PR left waiting indefinitely.** The integrator checks the latest head SHA, changed paths, dependency versions and genuine conflicts, runs the relevant build/unit/contract/negative tests, fixes any real failures, and merges promptly in dependency order. Prefer one short-lived integration branch for colliding work; merge non-conflicting, tested slices directly to main when it is safe. Do not create long stacked PR chains if earlier layers can be integrated now. Refresh branch bases and close superseded PRs only after their unique changes are accounted for.

**A merge does not mean a release.** Production cutover still requires separate real provider/browser/device/backup/security evidence and authorization. Before merging to main, identify *every* automatic deploy trigger (GitHub Actions, Vercel/hosting Git integrations, branch hooks, DB migration/predeploy tasks, etc.). Where main would deploy unfinished software, gate or disconnect automatic production deployments through an approved reversible change first; until then merge into a non-deploying integration branch. Never force-merge an actual code/test failure or security regression simply to clear the PR queue.

**If CI cannot start (runner/account/quota outage):** record the no-step job evidence, run equivalent tests against the exact checkout/SHA using an accessible local/alternate runner, and continue integration on a non-deploying branch when those tests and contract checks pass. If no executable runner is available, label the result unverified and keep the integration change isolated; do not misreport static inspections as passing tests. Production remains blocked until its proof succeeds.

**Integrator accountability:** when a workstream is handed off, identify the next merge target and execute the merge as soon as dependencies are satisfied. A five-minute claim controls edits, not an indefinite veto over review/merge. For each withheld PR, record a concrete failing test/conflict/deployment hazard, owner and next correction rather than a generic “waiting for verification.”

## Coordinated claims and stale recovery

- Claim before edits, heartbeat within five minutes, and release after a SHA-specific PR handoff. Multiple owned paths use one registry record.
- Expired claims remain blocking. The original owner can renew or release; another window cannot silently steal work. Stale recovery requires a reviewed registry change after checking live PRs, branch heads and unfinished source.
- Owner names and base SHAs are user-provided fields, not verified GitHub identities. The registry guards cooperating writers only. Direct GitHub writes can bypass it; branch permissions/reviews remain necessary.
- Tokens must use least privilege, remain in secret storage, and never run on untrusted PR code with write permissions.
- CAS retries reject collisions including directory prefix overlaps. This is a single-registry-file GitHub atomicity mechanism, not a cross-repository lock or full distributed authorization system.
- The first release is tested with deterministic simulated collisions. A credentialed live GitHub write/read/heartbeat/release test is still outstanding.

Example usage is in README.md. Record all recovered stale claims in registry history and link the review. Never delete code or PRs on expiry.
