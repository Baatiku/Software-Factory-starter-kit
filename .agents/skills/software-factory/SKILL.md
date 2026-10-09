---
name: software-factory
description: Plan, bootstrap, architect, build, or improve software products and apps from a brief idea using evidence-backed competitor research, simplicity-first product scope, complete screen specifications, vendor-neutral technology/cost selection, canonical contracts, safe parallel workstreams, full-story testing, release gates, and a versioned lessons loop. Use when starting or overhauling a product, coordinating multi-agent development, or asking to ship an end-to-end software project.
---

# Software Factory Skill (v0.3)

This is an execution workflow, not permission to invent actions or claim that inaccessible tools were used. Adapt depth to risk and size: simple projects require fewer artifacts.

## Load only relevant references

- Always: references/operating-protocol.md
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
8. Split complete vertical slices by real dependencies, ownership paths and integration capacity; read live PR heads and claim exact paths using a short, visible lease before edits. One owner per high-risk shared path.
9. Implement actual end-to-end behavior with automated tests and realistic recovery. Keep unfinished work in draft PRs with branch/base/head SHAs and evidence; don't substitute chat summaries.
10. One integrator reconciles branches and executes real device/browser/API/DB/provider/auth and restore/rollback tests. Distinguish verified from blocked tests and from simulated output.
11. Guard production and chargeable/destructive/external side effects with explicit permission. Update lessons and templates with versioned changes so future products inherit improvements.

## Stop gates

- **Before parallel UI**: complete actor/screen inventory, navigation, behavior, design states and design review.
- **Before shared integration**: canonical contracts published and conflicting claims resolved.
- **Before release**: real, SHA-specific end-to-end proof; required security, accessibility, data recovery, performance and rollback checks performed.
- **If blocked**: record exact failure/dependency and preserve source. Never relabel unverified work as complete.

Use scripts/bootstrap.py for non-destructive scaffolding and scripts/check.py for structural design/handoff/release-evidence checks. Neither guarantees real-world correctness.
