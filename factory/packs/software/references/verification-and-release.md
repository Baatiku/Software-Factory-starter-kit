# Evidence-first testing, integration and release

Verification follows the customer story through each relevant boundary: client/UI → network → server/auth/policy → DB or provider → persisted readback → notification/receipt. Use reproducible commands and environment with exact commit SHA.

For each requirement/journey map unit, contract, integration, negative/security and end-to-end checks. Add migration up/down or expand/contract rehearsal, account-switch and denied permission, restart/offline, idempotent retry, cross-tenant isolation, backup restore and low-end performance where relevant.

The test matrix must distinguish:
- NOT_RUN: no execution evidence.
- FAIL: executed and failed, with logs/reproduction.
- PASS_SIMULATED: mocks/emulators used; do not present as external integration.
- PASS_REAL: executed end-to-end with genuine backing dependencies and traceable redacted evidence.
- BLOCKED: exact unavailable runner/provider/device/credential stated.

A passing lint/unit suite never substitutes for actual provider, browser, Android/iOS or DB proof. Source review is not deployment evidence. An HTTP 200 on a health endpoint is not service readiness, database integrity or customer workflow proof.

## Integration gate versus production release gate

**Integration gate (routine code merges):** latest head and dependency checks, relevant executable build/lint/unit/contract/negative tests, collision and security review, and a safe merge target. Preserve SHA-specific results. Merge promptly when these pass; do not demand a real external-provider restoration drill for an isolated non-deploying code merge. True failures block their affected merge until corrected. If GitHub Actions fails with zero executed steps, treat it as CI infrastructure failure, run equivalent exact-SHA tests elsewhere when possible, and merge only to an isolated integration branch if confidence is otherwise justified. Record gaps honestly.

### Execution fallback and explicitly authorized source merges

If GitHub Actions cannot execute jobs, first attempt a checkout and **run the matching tests in the available container**. Check installed Node/Dart/Flutter/database toolchains; when direct GitHub clone fails because the container cannot reach GitHub, use the connected repository tools to continue implementation and test isolated, faithfully reproduced pure modules where possible. Do not claim an isolated test proves the whole checkout.

For a project whose owner explicitly directs **merge-first even when all runners are unavailable**, avoid leaving completed, non-destructive development source perpetually unmerged solely for NOT_RUN checks. Review actual source, latest main, conflicts, permissions, sensitive effects, known failures and reachable fallback checks, then merge compatible source to the approved development target; record the precise unexecuted commands and risk. Never override branch protection, conceal a known failure, claim verification that did not occur, or interpret a merge as permission to erase data, move funds, activate a paid provider or ship an unqualified production release. If an automatic deployment makes main unsafe, gate deployment before the merge or choose a non-deploying target.

**Release gate (production, destructive migrations, paid providers or DNS):** separately requires the full provider/device/browser/accessibility/security/backup/rollback evidence and owner authorization defined below. A merge to main must **not** bypass this gate: audit all Git-connected automatic deployment mechanisms first, not only workflow YAML. If production automation cannot be safely gated, integrate on a non-production branch instead.

Verify only the tested artifact/SHA; re-run impacted checks after merge or deploy SHA changes. Distinguish CI configuration present vs workflows actually running and passing. False-green empty/no-op CI is a fail.

Production gate includes threat/privacy review, dependency/license checks, accessibility, representative device/connection performance, monitoring/cost alerts, backup-and-restore drill, deploy rollback and required user journeys. Allow narrowly scoped waivers only from an accountable human, dated with risk and expiry; do not waive fundamental safety requirements silently.

Automated design, handoff and evidence checkers validate *structure only*. Passing them never changes a PR to VERIFIED_E2E or authorizes a release.
