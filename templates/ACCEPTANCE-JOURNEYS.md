# Golden acceptance journeys

For every main user outcome, define:
- Journey ID (J-###), role, prerequisites and expected final state.
- Exact sequence of screen IDs and user actions.
- Cross-layer flow: UI → network → auth/policy → persistent data/provider → readback.
- Failure, denied permission, offline, retry, concurrency, account switch and restart paths.
- Observable checks, automated test ID, devices/regions and evidence location.
- What blocked/not-run/failed tests mean for release.

<!-- TODO: one or more full journeys for each CORE feature; include admin/support and safety routes -->
