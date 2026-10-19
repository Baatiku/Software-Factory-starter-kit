# Compatibility and migration to Universal Work Factory 1.0

## Existing v0.4.x software projects
The historical `scripts/bootstrap.py`, `scripts/check.py`, `scripts/claims.py`, `scripts/package_skill.py`, `templates/`, `references/` and `.agents/skills/software-factory/` remain available. Their behavior and existing tests are unchanged; no generated project files are deleted or overwritten automatically. Current code projects may continue using the old workflow until their local instructions are reconciled.

## New projects
Use `python scripts/factory.py init --repo /path/to/existing/project --idea "..." --profile publishing --depth standard`. Available profiles: general, software, publishing, research, automation, design, business, infrastructure, analytics. `auto` is a deterministic lightweight heuristic, NOT an authoritative classifier: ambiguous multi-domain tasks default to general; select the primary profile explicitly and load additional pack docs when appropriate.
`quick` generates only one outcome document plus the portable tool/skill runtime. `standard` adds acceptance and continuation with specialist templates. `high-assurance` also adds risk/approval/recovery records. No automatically created template is proof that planning or delivery occurred.

## Upgrades
Run `python scripts/factory.py upgrade --repo /path/to/project` for a read-only preview. Add `--apply` only after review. The versioned manifest stores SHA-256 of factory-created files; owner-preexisting and locally modified files are preserved. The upgrader does not infer semantic merges, remove old files or migrate old software projects automatically. To adopt the new universal scaffold in an old project, use an isolated test copy, reconcile its existing `AGENTS.md`, source contracts and docs, then explicitly migrate; do not run a destructive replacement.
Generated `.factory/bin/factory.py` can run checks offline, but an upgrade needs the current full kit checkout: use upstream `scripts/factory.py` or pass `--factory-root /path/to/kit`.

## Evidence and safe deployment
`check --gate structure` checks installed files, `delivery` checks placeholders plus evidence, `release` also requires VERIFIED/DELIVERED proof; these are structural checks only. For high-assurance work an approval record is required. Project-specific verification (actual code, article publication, research quality or backup restore) must be run separately. Existing 0.4 legacy release gates remain distinct.

## Portable skills
`python scripts/package_work_factory.py --profile all --output dist/work-factory.zip` builds the universal router plus specialist references. Install only where supported by the actual client; producing an archive does not activate a ChatGPT account-wide skill. The old software ZIP remains available separately. Portable bundles and generated projects should not claim live API access merely because a skill is present.
