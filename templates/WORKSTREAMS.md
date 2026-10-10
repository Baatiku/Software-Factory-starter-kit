# Parallel workstream map

| Scope | Priority | Vertical user outcome | Dependency | Exact owned paths | Protected paths / integrator | Owner/lease | PR and SHA | Source remaining | Blocker / owner / next action | Status |
|---|---|---|---|---|---|---|---|---|---|---|
<!-- TODO: assign actual scopes from complete product plan and reconcile open PRs -->

Rules: one writer per contested path; inspect live main and PRs first; register five-minute exact-path claims with scripts/claims.py (GitHub CAS); expiry never authorizes takeover; never erase unmerged source on lease expiry. Integrate shared auth/schema/router/ledger/build/deploy sequentially. Default to promptly MERGED workstreams, not indefinitely PR_OPEN. Track merge target/SHA and explain holds with a specific conflict, failing test or production-deploy risk. Code merge does not waive separate release proof.

## Milestones and live dispatch

The table is a planning allocation, not live ownership or completion evidence.
Refresh PR source, claims and actual tests before dispatching. Complete customer
milestones before secondary helpers; every necessary guard names its unfinished
parent milestone. Reuse existing implementations and canonical tools.
List dependency contracts explicitly; independent work need not await the entire
integrator. Publish bounded shared-file transfers, available test runners and
one continuing reviewed safe integration baseline. Do not open another per-patch
integration branch without a concrete isolation/conflict reason.

