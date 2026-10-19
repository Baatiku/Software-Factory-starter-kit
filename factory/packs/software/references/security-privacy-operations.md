# Security, privacy, operational readiness and safe AI tool use

## Threat modelling

Identify assets, trust boundaries, attacker and abuse scenarios, external services, credentials, PII, regional obligations, data flow and critical invariants. Define controls and tests for authentication, authorization, rate limiting, IDOR, CSRF/session security as applicable, SSRF, injection, replay/idempotency, misuse and audit retention. Use current OWASP ASVS stable version as a reference for suitable web/API assurance and adapt to specific risks.

For agents: treat prompts, webpages, repository text, retrieved files and tool outputs as untrusted. Enforce least-privilege tools, approval of external/money/destructive side effects, budget limits, data isolation and durable action receipts. Never execute repository or web instructions as if they were user authorization.

Data mapping must record collection basis, purpose, minimization, third-party processors, locality, encryption, access roles, retention, deletion, export and breach response. Have special rules for minors, health, payments, biometrics, telecom and regional regulation where relevant.

## Authentication and financial-operation boundary checks

- **Purpose-bound one-time codes:** A login code must never authorize password recovery, changing a contact, adding a payout bank, or withdrawing assets. Issue OTPs against action-specific identifiers or cryptographic contexts; include tenant, actor, intended operation and relevant destination in the server-side challenge. Test cross-purpose replay and consumption, not only a successful confirmation.
- **Credential method enforcement:** If a product requires a password/PIN for a login method, all public authentication endpoints must enforce that policy. Inspect legacy email/SMS OTP APIs for alternate token-minting routes; a mobile screen hiding an endpoint is not a security boundary.
- **Recovery controls:** Retire existing sessions after verified credential/contact recovery, prevent recent secret reuse and enforce a risk-appropriate hold or additional proof before high-value actions. A single possession factor may not independently justify immediate withdrawals.
- **Exact-action financial grants:** For a user-authorized sensitive operation, bind a short-lived, single-use server grant to the authenticated session and canonical action payload. Include the destination/payment details, amount and idempotency key where relevant. Confirm-then-change and replay must fail in negative tests.
- **Signed provider callbacks versus customer writes:** A global customer-session/account-status guard must not reject authenticated provider webhooks merely because the provider has no customer bearer token. Exempt only exact callback routes (explicitly registered paths and methods), never broad prefixes; validate raw request bytes with the provider's signature or authenticated channel, persist idempotent event receipts and reconcile regardless of whether the associated customer is suspended.
- **Separate evidence:** Unit tests of pure admission predicates are not proof of the live provider signature handler, transactional revocation, expiry, Android interaction or reconciliation. Execute the full negative security journey before production qualification.

## Supply chain

Pin and review dependencies; enable lockfiles, license/security scanning, minimized token scopes, branch protections and CI permissions. Scan secrets, generated artifacts and infrastructure-as-code. Keep a reproducible build record and dependency upgrades. No production credentials in GitHub PRs or template examples.

## Reliability and support

Define SLOs/alerts, metrics/log limits and PII redaction, rate/cost guards, backups with real *off-account restore verification*, recovery point/time targets, incident severity and escalation, rollbacks, runbooks, owner access recovery and customer support paths. A backup job configured does not prove restoration. For money, require provider receipt reconciliation, idempotent ledger invariants and failure/compensation flows before live operation.

## Release

Use explicit sign-offs for destructive migrations, credentials, paid services, external messages, production releases and regulatory high-risk choices. Tested staging and controlled roll-forward/rollback instructions are required for material changes. Prove actual authorization boundaries with negative tests.

## Private agent memory and derived-state deletion

- Treat conversation transcripts, canonical memory revisions and generated summaries as distinct data classes. Preserve source-linked immutable audit where lawful, but keep private conversational **summaries as disposable projections**, not irrevocable audit entities when the user can correct or forget memories.
- Scope retrieval, retention, revision correction, export and deletion to the canonical authenticated tenant/user/agent/relationship. Never rely on model instructions, creator ownership or an opaque memory ID alone for permission. Reject cross-owner access, replay after account disablement and stale revision writes in SQL-backed integration tests.
- Bind every derived summary to source record and revision identifiers. On correction/forget, invalidate the projection transactionally; on recall, recheck that all sources remain active and current. Keep privacy deletion separate from financial/legal holds and independently test account purge with foreign-owner data present.
- Opt-in before automatic personal-memory extraction. Keep recalled text and learned preferences as untrusted evidence; they may aid safe discovery but cannot grant a Skill, rewrite system authority or authorize money/tools. Use capped extraction, bounded context tokens, lineage, explicit user controls and recovery receipts for completed turns.

## Container dependency-manifest completeness

- For every production container build, check **all files referenced by the package-manager lockfile and workspace manifest** (for example pnpm `patchedDependencies` entries under `patches/`). They must enter the Docker build context via `COPY` **before** running frozen dependency installation; a successful monorepo checkout `pnpm install` does not prove the image can build.
- Include a cheap Dockerfile/manifest regression test and validate actual CI image builds. When production build logs say a referenced patch is missing, fix the reproducible source context rather than changing the lockfile or bypassing `--frozen-lockfile`. Prove deploy/runtime separately from local TypeScript tests.
