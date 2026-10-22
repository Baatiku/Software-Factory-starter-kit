# Market research, product selection and ruthless simplicity

For each product class research multiple verifiable alternatives: ideally two established, one lean challenger, one adjacent substitute. Never fabricate usage/reviews/prices. Date findings and link sources; explicitly label missing or weak evidence.

Inspect: primary user job, navigation, time-to-value, onboarding, pricing, core flow, forced registration, support, mobile/performance, security/privacy, cancellation, retention, unnecessary steps, failure handling, overlooked market needs and regional constraints.

Output a competitor comparison containing ADOPT / AVOID / DIFFERENTIATE with evidence. Distinguish competitive absence (verified missing feature) from personal inference. Do not clone exact competitors' copyrighted copy/layout/assets.

Score each feature: essential user outcome, compliance/safety obligation, measurable differentiation, frequency, implementation/operating burden, opportunity cost and effect on the main user flow. Four outcomes: CORE NOW, DIFFERENTIATOR NOW, LATER, EXCLUDE. Write explicit exclusions so they do not creep back in through parallel agents.

Prefer feature subtraction, shared patterns and one intuitive navigation over accumulating tabs, nested menus, controls and configuration. Avoid one-off frameworks for trivial problems. Provide an accepted thin first release with full working vertical slices, not a gigantic disconnected mock.

## Benchmarking existing UI against decoded competitor references

An existing implementation may be **redesigned** when a competitor's more familiar layout reduces user effort. Preserve executable auth/data/payment/permission contracts, not historical screen geometry. Compare screen-by-screen: hierarchy and route/back, controls, main journey, 320dp/200%/RTL/screenreader behavior, loading/empty/offline/unknown/denied/retry states and deep-link/account-switch recovery. Flag where functionality already exists so it is improved rather than duplicated. Trace each proposed change into the canonical screen inventory and existing phased roadmap before reworking shared components.

Evidence confidence ladder: actual decoded layout/manifest/resource identifier proves only the component or declaration is present, not its runtime interactions; secondary component indexes and decompiler READMEs can be wrong; official published product behavior can corroborate user-facing patterns, not the sampled binary's hidden payment engine. Never claim a DEX/Wasm/Java/backend engine was analyzed when it was not committed or inspected. For fintech, do not transplant other providers' KYC tiers, price examples, PIN-keypad safety claims, fake badges, clipboard harvesting, proprietary assets or settlement semantics. Verify existing policy/exchange rate and independently authorized provider/readback first.

Implement the smallest connected high-impact screen replacement after the comparison, and exercise its negative-state transitions and narrow-device layout. Mark remaining reference-inspired changes explicitly open; a screenshot or XML name is not end-to-end acceptance.