# Skills audit — transferable practices (2026-10-09)

This audit sampled available installed skills as engineering references. Their tools and vendors may not be connected or appropriate for every project. It is not a complete registry of every skill, and pricing/product behavior must be checked when used.

| Skill family reviewed | Portable lesson | Factory adaptation |
|---|---|---|
| Vercel full-story verification | Infer complete user story and test browser → server → data → response | Journey tests and SHA-based evidence rules |
| Vercel bootstrap | Verify environment and authorization before starting migrations | No secret leakage; safe provisioning order |
| Vercel backend architecture | Choose workload before runtime/framework | Vendor-neutral architecture and workload mapping |
| Vercel deployment/CI | Know project/environment/SHA, stage deploy, test and rollback | Release-gate evidence requirements |
| Vercel React best practices | Performance, accessibility, request waterfalls and component boundaries | UI/test/checklist review tailored to chosen frontend |
| Supabase Postgres best practices | Query, connection, RLS, concurrency, indexes and observability | SQL/security/performance obligations where SQL applies |
| Neon database branches | Branch-based or schema-only migration rehearsal | Privacy-safe DB verification |
| Vercel durable agents | Untrusted inputs, tools, sessions, cost and permissions | Approval/least-privilege tool boundaries |

## Not inherited as defaults

Do **not** adopt Vercel, Neon, Supabase, Flutter, React, Firebase, or any framework as an automatic project dependency. Vendor-specific skills often optimize for their platform. Select only after contemporary eligibility, pricing, reliability, skills, maintenance and portability comparisons.

Additional references for reviews:
- OWASP ASVS stable security baseline: https://github.com/OWASP/ASVS
- W3C WCAG 2.2: https://www.w3.org/TR/WCAG22/
- OpenSSF Scorecard supply-chain practices: https://scorecard.dev/

## Future audits

On significant kit updates, re-inspect applicable installed skills and current standards, identify reusable principles, and add evidence-driven improvements with tests. Do not copy third-party skills verbatim or assume runtime features remain unchanged.
