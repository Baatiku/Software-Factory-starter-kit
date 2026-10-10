# Workstream handoff (one per active implementation branch)

**Scope:** <!-- TODO -->  
**PR:** <!-- TODO -->  
**Base SHA:** <!-- TODO -->  
**Head SHA:** <!-- TODO -->  
**Status:** PARTIAL_IMPLEMENTATION / IMPLEMENTED_UNVERIFIED / VERIFIED_E2E / DEPLOYED_VERIFIED

## Exact files and protected paths
<!-- TODO -->

## Implemented end-to-end behavior
<!-- TODO: backend, data, auth, UI, state/retries, security and observable readback -->

## Tests executed and results
<!-- TODO: commands, environment, PASS/FAIL, real vs simulated, evidence pointers -->

## Tests not executed and genuine blockers
<!-- TODO: device, secrets, CI, provider credentials, DB restore, timeouts -->

## Integration and rollback
<!-- TODO: canonical contracts, unresolved PR overlap and migration steps -->

## Merge completion
<!-- TODO: MERGED (commit SHA and branch) / READY_TO_MERGE (target and tests) / BLOCKED (specific conflict, failure or unsafe deployment trigger). Do not equate a code merge with a release. -->

## Next owner and dependencies
<!-- TODO -->

## Customer milestone and continuation

Name the parent customer milestone and journey IDs, what the customer can now
do, missing connected source, toolchain execution owner, and integration baseline.
A guard/helper handoff must continue or transfer its unfinished parent milestone.
For each blocked PR/check name exact head, concrete blocker, responsible owner and
next executable action. Do not write only “waiting for integration”.

Save machine-readable delivery metadata in docs/workstreams/<milestone>.json.
Use delivery_schema_version 1 for new handoffs; base/head/paths/tests/pr/status
remain required. This structural record is not proof of real functionality.

```json
{
  "delivery_schema_version": 1,
  "milestone_id": "M-001",
  "journeys": ["J-001"],
  "source_complete": false,
  "remaining_source": ["Connect authoritative API and client readback"],
  "blocked_actions": [
    {
      "reason": "Required Flutter runner is unavailable",
      "owner": "named continuing verification window",
      "next_action": "Run exact-head Flutter analyzer and named tests"
    }
  ],
  "base_sha": "replace with exact base SHA",
  "head_sha": "replace with exact head SHA",
  "paths": ["replace with actual owned path"],
  "pr": "replace with actual PR URL",
  "status": "PARTIAL_IMPLEMENTATION",
  "tests": [{"command": "replace with actual command", "status": "NOT_RUN"}]
}
```

