# Operating protocol

## Inputs and autonomous defaults

Accept a short product idea. Derive likely roles, journeys, business model, admin/back-office, support, privacy, customer onboarding, operations, lifecycle and failure conditions. Use assumptions labelled by confidence and reversibility. Ask the owner only when a consequential unknown affects scope, compliance, irreversible costs, or brand direction. Don't repeatedly ask about routine implementation preferences.

Differentiate product-wide standards from project-specific decisions. Keep the default UX modern, compact, familiar and responsive. Use low-data and low-end-device performance constraints when materially relevant. Simplicity is not removal of security, accessibility or operational support.

## Scale plans proportionately

- Small utility/landing page: brief market scan, main screens, lean stack, tests and deployment checklist.
- Ordinary SaaS/mobile app: explicit feature/screen catalog, real backend/auth/contracts, cost model, security/ops and integrated test map.
- High-impact money, health, identity, telecom, agents or compliance product: deeper threat model, data governance, financial reconciliation/abuse prevention, audit evidence, provider qualification, restore drills and explicit approvals.

Never use complexity classification to erase a legally required control. Record classification and rationale in the charter.

## Source of truth

1. Proven current behavior and executable evidence at a named commit.
2. Canonical current product requirements and recorded owner decisions.
3. Active contracts and accepted ADRs.
4. Historical plans/PRs, reconciled rather than ignored.
5. Unverified memories and speculation, explicitly identified.

An open PR is neither merged nor automatically obsolete. A stale claim is not proof the source can be overwritten. Preserve evidence even when blocked.

## Planning gates

Idea → market and scope → complete experience → architecture/contracts/security/budget → independent workstreams → implementation → integrated verification → staged release → feedback and method improvement.

Plan comprehensively but adapt rapidly with a dated decision log when real evidence changes the answer. Avoid premature architecture commitments before knowing workloads.

## Generated project runtime

A new project includes `.agents/skills/software-factory/SKILL.md`, `.factory/playbooks/**`, `.factory/bin/check.py`, `.factory/bin/claims.py` and `.factory/FACTORY-VERSION`. Read and apply them without requiring chat history. Re-running upstream bootstrap creates missing files but does not silently overwrite customizations or upgrade existing files; review upstream changes consciously.
