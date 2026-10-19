# Universal Work Factory

**One actively maintained toolkit · version 1.0.1** for developing software, research, news/content publishing, automation and agents, design, business operations, infrastructure and analytics. The factory is a repository of **executable project tooling, modular skills, tested coordination, and reusable methods**, not a continuously running hosted agent or a modification of your ChatGPT account.

## Start

For an existing empty or partially created project directory:

```bash
python scripts/factory.py init --repo ./project --idea "Build a publishing workflow" --profile publishing
python scripts/factory.py check --repo ./project --gate structure
python scripts/factory.py upgrade --repo ./project              # preview only
python scripts/factory.py upgrade --repo ./project --apply      # reviewed update
python scripts/check_kit.py                                     # validate the kit itself
python -m unittest discover -s tests -v
python scripts/package_work_factory.py --profile all --output dist/work-factory.zip
```

Profiles: `general`, `software`, `publishing`, `research`, `automation`, `design`, `business`, `infrastructure`, `analytics`. Pick the primary profile explicitly when several apply; load additional playbooks as needed. `--profile auto` uses a conservative keyword heuristic, not a model or a complete intent classifier. Depth: `quick`, `standard` or `high-assurance`. Small tasks should be completed directly without creating project paperwork.

## Single source of truth

- [Work router](.agents/skills/work-factory/SKILL.md) and [nine domain skill entries](.agents/skills/), including the general route.
- [Universal core](factory/core/) for routing, execution, evidence, security, coordination and improvement.
- [Eight specialist packs](factory/packs/) plus the general pack. Software's detailed playbooks are now under [factory/packs/software/references](factory/packs/software/references).
- [Adaptive bootstrap/check/upgrade CLI](scripts/factory.py), [GitHub CAS coordination tool](factory/tools/github_claims.py), [portable packaging](scripts/package_work_factory.py), [tests](tests/), [evaluation](factory/EVALUATION.md), and [migration guidance](factory/MIGRATION.md).
- [ChatGPT setup and account capability notes](install/CHATGPT-SETUP.md) and [custom-instruction snippet](install/CUSTOM-INSTRUCTIONS.txt).

## Project principles

Research peers and alternatives with dated evidence; identify what to borrow, improve and omit. For software, specify all screens, journeys and interactions before parallel UI work. Use current provider comparisons and total cost; choose simple, maintainable, portable solutions. Build complete outcomes with scoped permissions, real tests and honest evidence; coordinate source ownership and merge compatible, tested work promptly, while separately gating production. Record lessons that generalize; do not import product-specific architecture as universal policy.

The `init` command **never overwrites existing files**. `upgrade` previews changes by default, updates only unchanged factory-owned files when applied and preserves local modifications. Structural checks are not proof of a working application, published article, data report or live deployment.

## ChatGPT installation

Skill creation/upload is account and workspace dependent. This repository cannot install itself into ChatGPT or modify ChatGPT memory. For accounts with Skills access, follow [ChatGPT setup](install/CHATGPT-SETUP.md) using the CI-generated `work-factory.zip`. For other accounts, place the short [custom instruction](install/CUSTOM-INSTRUCTIONS.txt) into Settings → Personalization; ChatGPT can read this repository through a connected GitHub tool when available. ZIP creation does not equal installation.

## Scope of cleanup

Only the current universal skill, packs, templates, tests and packaging are maintained. Previous starter scaffolds and duplicate installation files have been retired from this repository's current tree. Git commit history and project-owned copies in other repositories are intentionally not rewritten.
