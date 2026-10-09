# Experience specification — every screen and interaction before parallel UI

## Screen inventory

List **all** human actors and primary flows: anonymous, onboarded, signed out, blocked, support, admin, creator/provider, and other actual roles. For each, assign stable SC-001 etc identifiers; give entry points, main route, platform variants, capability, owner and acceptance state. Include onboarding, auth, settings, permissions, help, billing, receipts, deletion and failure pathways when applicable.

## Every SC specification must record

- User/role and task; preconditions, entry point, exit and back/deep-link handling.
- Top-to-bottom layout: app bar, content hierarchy, cards/forms/rows, empty spaces, footer/navigation, visual density.
- Exact controls: label, position, enabled/disabled rule, validation, user feedback, confirmation, destructive behavior, accessibility semantics.
- Real data: API/schema/event, auth and permissions, cache/revalidation, error contract, optimistic updates vs server truth, idempotency.
- States: first use, empty, skeleton/loading, partial failure, offline, retry, invalid, rate limited, blocked, denied permission, stale, success, account switching.
- Responsive/mobile/small-device/keyboard/touch/RTL/localization requirements as appropriate.
- Screen-to-screen journey with postcondition and observable verification, not merely a screenshot or an isolated button.
- Wireframe or visual prototype when layout warrants it, with acceptance against approved design tokens rather than arbitrary styling.

## Gates

Every SC identifier in the inventory must have one full specification. Each CORE feature maps to at least one SC and one golden acceptance journey. Trace every journey to technical boundaries, negative cases, tests and code owners. No orphan screens, features or journeys. Screen completeness is not just the presence of matching IDs.

Prefer low cognitive load, familiar conventions and fewer decisions. Use WCAG 2.2 AA as a reference baseline for relevant web UIs; mobile platform accessibility standards also apply. Validate with real devices/assistive technologies when available.
