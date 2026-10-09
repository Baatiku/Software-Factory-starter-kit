# Detailed screen specifications

Create one ## SC-### section per accepted screen in SCREEN-INVENTORY.md, ordered as the UI actually appears. Include auth, blocked, loading, empty, offline, error, permission, recovery and confirmation variants.

<!-- TODO: replace this example structure with one real section per screen; remove this placeholder -->

## Example format (replace)
**User goal:** role, preconditions and postcondition  
**Navigation:** deep link, tab, back, keyboard dismissal, exit  
**Layout:** exact header, content, controls, empty space, footer order  
**Controls:** labels, disabled/enabled rule, validation, UI feedback and confirmations  
**States:** loading, blank, offline, denied, rate-limited, expired, retry, success  
**Data:** DTO/API/event, auth, cache, reconciliation, idempotency, reads/writes  
**Access:** authorization, WCAG/mobile accessibility, i18n/RTL and device sizes  
**Proof:** mapped journeys, test IDs, screenshots/assistive/device checks  

A screen drawing without data flow and failure behavior is incomplete.
