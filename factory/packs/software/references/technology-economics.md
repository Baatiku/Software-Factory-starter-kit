# Stack selection — vendor-neutral, actual total cost

Start with workload: traffic, concurrency, latency, files, data durability, geography, platforms, real-time/offline requirements, compliance, team skills and operational labor. Select architecture before choosing a named vendor.

For every critical provider, compare at least two viable options or document why only one is eligible. Sources should be current official pricing, quotas, limitations, region and acceptable-use docs, with dates and links. Do not let an available plugin or skill privilege the vendor.

Calculate pilot, normal operation and growth: base plans, requests/API tokens, AI inference, webhooks, egress, storage, backups, log retention, third-party transactions, currency fees, VAT/taxes where relevant, redundancy and migration cost. Include worst-case spikes and shutdown/usage caps. Note that free-tier quotas and promotional prices can change.

Decision record: candidate, actual requirement satisfied, region/account eligibility, price units, TCO scenarios, lock-in/export options, support, reliability evidence, security constraints, switch triggers, reason for selection/rejection. Use a simple managed or monolithic architecture when sufficient; separate services only for demonstrated boundaries.

Secrets are only stored in approved secret managers/environment systems; never copied into docs, chat logs, build artifacts or public repos. Real deployment credentials can be a future integration gate, not a reason to fabricate qualification.
