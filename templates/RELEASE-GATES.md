# Evidence-based release gates

Required before release (mark applicable items with real evidence):
- [ ] Scope/design reviewed and main journeys matched to real screen/data contracts.
- [ ] Access controls, security risks, dependencies, secrets and privacy reviewed.
- [ ] CI actually executed and passed on exact commit (not zero-step/no-op).
- [ ] Required end-to-end journeys PASS_REAL with authenticated data readback.
- [ ] Device/browser, accessibility, localization, weak-network and performance checks.
- [ ] For money/data-provider flows: genuine provider qualification, failure/reconciliation and duplicate action checks.
- [ ] Migrations rehearsed; off-account backup restored into a test environment.
- [ ] Observability, cost/budget alerts, support and incident recovery ready.
- [ ] Safe staging → production path and actual rollback documented.
- [ ] Human approval for production, paid, destructive and regulated operations.

<!-- TODO: exact per-item commands, artifacts, SHA, date, risk owner and approved waivers -->

Never mark release-ready solely because a script prints STRUCTURE PASS.
