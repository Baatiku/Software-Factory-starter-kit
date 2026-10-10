---
name: software-factory
description: Use when someone proposes a software product, mobile app, website, SaaS or AI-agent idea, requests product planning or implementation, asks to finish an unfinished app, requests a feature upgrade to an existing product, or needs coordinated multi-agent development and real release verification.
---

# Software Factory Skill (v0.4.4)

This is an execution workflow, not permission to invent actions or claim that inaccessible tools were used. Adapt depth to risk and size: simple projects require fewer artifacts.

## Load only relevant references

- Always: references/operating-protocol.md and references/owner-defaults.md
- New product discovery: references/research-and-simplicity.md
- Product with visual screens: references/screen-design.md
- Stack/providers: references/technology-economics.md
- Parallel implementation: references/parallel-delivery.md
- Security-sensitive or data-bearing products: references/security-privacy-operations.md
- Acceptance/integration/release: references/verification-and-release.md
- Improvements to this factory: references/continuous-improvement.md

Reference paths are relative to this repository root, not the skill directory. Locate the project root before reading them.

## Default workflow

1. Determine whether this is a new product, current codebase continuation, or narrow change; read actual code/repo before assuming any plan.
2. Research real competitors and substitute solutions; date and link the evidence; learn what to adopt, avoid and differentiate. Do not copy protected visual designs.
3. Discover user groups, critical jobs, safety/financial/privacy obligations, failure states and operational requirements. Categorize CORE NOW, DELIBERATE DIFFERENTIATOR, LATER, EXCLUDE with justification.
4. Specify **all pages and significant interactions** before dispatching parallel UI work. Include layout hierarchy, navigation, forms, buttons, data/state contracts, loading/empty/error/offline/retry/unauthorized/deletion states and mobile/desktop/accessibility coverage. Collect only high-impact ambiguous decisions from the owner in one consolidated review.
5. Research candidate stacks and vendors using latest official pricing and availability; compare current pilot/launch/scale total cost, downtime risk, regional support, portability and maintenance. Avoid premature microservices, expensive managed infra and provider proliferation.
6. Create/maintain canonical architecture, threat and privacy models, contract schemas, design system, requirement→screen→journey→test traceability, budgets, operations, and evidence gates.
7. Run scaffold design check; unresolved placeholders mean NOT READY. A structurally passing check is not a qualitative or operational acceptance.
8. Split complete vertical slices by real dependencies, ownership paths and integration capacity; read live PR heads and use scripts/claims.py to acquire/heartbeat exact-path claims on the target repo before edits; do not steal stale records. One owner per high-risk shared path.
9. Implement real end-to-end behavior with automated tests and realistic recovery. Open scoped PRs with exact SHAs and evidence. **Merge completed, compatible changes promptly**; PR creation alone is not completion. Keep genuinely unfinished work as draft PRs, not an accumulating backlog.
10. One integrator continuously reconciles and **merges dependency-ready PRs** into an integration branch or directly into main when main cannot trigger unsafe production effects; test the unified SHA. Separate **code integration** (appropriate local/contract checks) from **production release** (real device/browser/API/DB/provider/auth and restoration proof). Missing CI runners require alternate executable checks and truthful evidence, not indefinite PR parking; actual failing code must be fixed.
11. Guard production and chargeable/destructive/external side effects with explicit permission. Update lessons and templates with versioned changes so future products inherit improvements.

## Existing-product upgrades and outcome-first dispatch

Recover current main, local improvements, relevant PR heads/files and live ownership before replanning. Classify each requested journey as missing source, disconnected source, source-tested, integrated or externally qualified; allocation-template status is never live completion evidence. Reuse prior implementation and limit reading to affected contracts.

Dispatch complete customer milestones before isolated helpers. Tie necessary hardening to a demonstrated milestone/security blocker; a partial safeguard never completes its parent lane. Elect one canonical verification/cleanup authority rather than creating another tool to avoid a path collision. Identify usable toolchains before assigning verification.

Keep one continuing reviewed safe integration baseline. Publish bounded exact-path composition transfers and delegate non-overlapping review/merge to avoid a root-integrator bottleneck; protected authority remains singular. Dependencies block required contracts, not independent implementation. Every held PR needs exact head, concrete blocker, responsible owner and next executable action. Continue implementable milestone source while external execution remains blocked; never substitute simulations or static checks for repository tests.

Generate these rules through templates/AGENTS.md, CONTINUE-HERE.md, WORKSTREAMS.md and WINDOW-HANDOFF.md. Record delivery_schema_version 1 milestone handoffs with source completeness and blocker assignments; scripts/check.py validates structure only. Existing customized bundles require a reviewed upgrade; bootstrap must not overwrite them.

## Stop gates

- **Before parallel UI**: complete actor/screen inventory, navigation, behavior, design states and design review.
- **Before shared integration**: canonical contracts published and conflicting claims resolved.
- **Before code merge**: inspect current head, conflicts, ownership, applicable executable tests, security and deployment triggers; fix genuine failures. If main can deploy automatically, merge to a protected integration branch until deployment is explicitly gated.
- **Before release**: real, SHA-specific end-to-end proof; required security, accessibility, data recovery, performance and rollback checks performed.
- **If blocked**: record exact failure/dependency and preserve source. Never relabel unverified work as complete.

Use scripts/bootstrap.py for non-destructive scaffolding, scripts/claims.py for GitHub CAS ownership coordination and scripts/check.py for structural design/handoff/release-evidence checks. Neither guarantees real-world correctness.

