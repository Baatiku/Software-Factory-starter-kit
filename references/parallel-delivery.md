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

## Outcome-first dispatch and bounded integration capacity

Prefer continuing substantive feature PRs and completing connected customer journeys before isolated helpers or speculative hardening. A justified security fix remains necessary, but its handoff must name the parent milestone still unfinished. Planned allocation files are templates, not live task completion/ownership registries; dispatch from current claims, PR source and executed evidence.

One canonical qualification tool and domain authority per purpose. Consolidate useful checks from competing helpers rather than create another implementation to avoid a path collision. Keep existing source until every unique behavior/test is accounted for.

Use one continuing reviewed safe integration baseline rather than a new branch for every patch. Verify actual deployment filters: naming a branch integration does not prove no deployment. Publish bounded exact-path composition/test/export transfers and allow authorized non-overlapping source review/merge delegation; protected root/auth/money authority remains singular. Dependencies block their actual contracts, not every independent feature until the whole integrator is finished.

Inspect executable toolchains before dispatch. When unavailable, record exact commands/environment, assign execution to a capable runner/window and continue independent connected source. Do not repeatedly retry zero-step CI or manufacture extra evidence scripts instead of implementing the product. Neither static inspection nor rewritten simulated functions replace repository tests.

For every waiting PR require current head, specific dependency/conflict/failing-or-unavailable command/deploy hazard, accountable owner and next executable correction. “Waiting for integration” alone is not a disposition. Keep integration and release evidence separate; do not force unsafe code through a merge.

## Source closure before environment handoff

For a source-first handoff, finish all implementable feature code and composition in the current environment before requesting the owner's local checkout. Maintain a finite per-milestone checklist with required source item/paths, owner, implementation commit, integration SHA and separate execution result. Missing runners defer only the exact unavailable checks, never missing APIs, client wiring, migrations, adapters or unresolved source conflicts. Inspect permitted alternate execution once; record capability, attempted command/error, assigned runner and reproducible next command. Never claim unrun checks passed or force unsafe source through a merge.

Continue the next essential open checklist item; if the session ends, explicitly transfer remaining items in the same milestone PR. A released lease or microfix is not milestone completion. The integrator publishes one reviewed integration target and exact-head composition queue, using bounded path transfers to avoid indefinite waiting. Before local handoff, all required source must be implemented and integrated; publish one pinned unified SHA plus only genuinely environment-dependent checks and build steps. Preserve unseen local changes for later reconciliation. Source closure is distinct from end-to-end qualification and release.
