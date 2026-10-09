# Software Factory Starter Kit

**Factory v0.3.0** — a reusable, vendor-neutral engineering workflow developed from lessons learned building Masanawa. Its purpose is to turn a brief product idea into a researched, simple, screen-complete, implementable and verifiable product.

This repository is **a skill and executable planning/coordination starter kit**, not an always-on autonomous service. It cannot create parallel ChatGPT conversations automatically, install account-wide skills, or guarantee releases without actual access and tests. Documentation is never proof that an application works.

## Quick start

1. Read [the factory skill](.agents/skills/software-factory/SKILL.md) and [factory rules](AGENTS.md).
2. In a new repository, run: python path/to/Software-Factory-starter-kit/scripts/bootstrap.py --repo /path/to/new/repo --idea "Your product idea"
3. Have ChatGPT Work/Codex research and *fill* the generated documents. Bootstrap creates intentionally incomplete templates.
4. Run: python path/to/Software-Factory-starter-kit/scripts/check.py --repo /path/to/new/repo --gate design
5. Only start independent UI work after the design gate is complete. Publish exact-path claims and branch handoffs for parallel work.
6. Use Work or another controlled integration executor to verify real user journeys before any release.

## Planning outputs

- Product research: dated competitors (ADOPT/AVOID/DIFFERENTIATE), user jobs, exclusions and proof.
- UX: every screen, navigation, controls, responses, permissions, failure/empty/offline states and realistic wireframes or visual references when appropriate.
- Engineering: requirement IDs, typed API/data contracts, stack comparison, three-scale cost model, security/privacy controls, test map and operating plan.
- Execution: independent vertical slices, one owner per contested path, short leases with recovery, SHA-specific PR handoffs.
- Release: independent execution proof across the real UI → API → auth → database/provider → readback path, staged deployment and rollback, accountable sign-off.
- Improvement: postmortem and lessons register, scoped amendments, backwards-compatible templates and versioned releases.

## Key distinctions

**Scaffold present ≠ researched. Design complete ≠ tested. Code present ≠ integrated. CI configuration ≠ passing CI. Health endpoint ≠ real customer journey.**

A simple brochure site should not receive fintech-level paperwork. A wallet, health or identity platform must receive deeper threat, privacy, integrity and operating controls. Build the simplest sufficient solution, not the largest plan.

## Contents

- [.agents/skills/software-factory/SKILL.md](.agents/skills/software-factory/SKILL.md): skill entry point for supported Codex environments.
- [AGENTS.md](AGENTS.md): repo and generated-project operating instructions.
- [references/](references/): planning, UX, owner defaults, provider-neutral skill audit, threat, verification, parallel work and improvement playbooks.
- [templates/](templates/): starter documents copied without overwriting existing files.
- [scripts/](scripts/): safe bootstrap and evidence-aware structural checks.
- [tests/](tests/): positive/negative regression tests.
- [CONTRIBUTING.md](CONTRIBUTING.md), [CHANGELOG.md](CHANGELOG.md): future improvement process.

## Practical tool use

Use available connected GitHub tools for safe repository operations, Work for multi-step cross-file integration, Codex for code-level implementation, Figma for actual editable design deliverables where available, and provider-specific skills only after evaluating whether that provider suits the project. Never assume an installed vendor skill implies vendor preference.

## Recommended future evolution

Implement a properly authenticated GitHub App that enforces atomic exact-path leases, validates PR ownership and records per-SHA quality evidence. Current five-minute text claims are a coordination protocol, **not an atomic distributed lock**. The registry must not silently treat expired leases as permission to delete existing unmerged work.

## Status

v0.3 is a starter kit: scripts validate structure and internal references, not competitor truth, full UX quality, live CI, device performance or production readiness. See [release requirements](references/verification-and-release.md).
