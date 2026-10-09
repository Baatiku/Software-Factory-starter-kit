#!/usr/bin/env python3
"""Create a self-contained project scaffold without replacing existing files."""
import argparse
import re
from pathlib import Path


def bootstrap(repo: Path, idea: str, template_root: Path) -> tuple[int, int]:
    repo = repo.resolve()
    template_root = template_root.resolve()
    factory_root = template_root.parent
    if not repo.is_dir():
        raise ValueError("Repository directory does not exist")
    if not idea.strip():
        raise ValueError("Product idea is required")
    if not (factory_root / ".agents/skills/software-factory/SKILL.md").is_file():
        raise ValueError("Factory source is missing its skill")
    if repo == factory_root:
        raise ValueError("Choose a target project, not the factory starter-kit directory")
    created = preserved = 0

    def install(destination: Path, content: str):
        nonlocal created, preserved
        if destination.exists():
            if not destination.is_file():
                raise ValueError(f"Destination exists but is not a file: {destination}")
            preserved += 1
            print("PRESERVED", destination.relative_to(repo))
            return
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
        created += 1
        print("CREATED", destination.relative_to(repo))

    # A project gets its own product documents, not claims of completed research.
    for source in sorted(template_root.iterdir()):
        if not source.is_file():
            continue
        destination = repo / source.name if source.name in {"AGENTS.md", "CONTINUE-HERE.md"} else repo / "docs" / source.name
        text = source.read_text(encoding="utf-8")
        if source.name == "PROJECT-CHARTER.md":
            text = text.replace("{{PROJECT_IDEA}}", idea.strip())
        if source.name == "WORKSTREAMS.md":
            text = text.replace("scripts/claims.py", ".factory/bin/claims.py")
        install(destination, text)

    # Portable skill plus local playbooks: does not depend on this chat's memory.
    for source in sorted((factory_root / "references").glob("*.md")):
        install(repo / ".factory/playbooks" / source.name, source.read_text(encoding="utf-8"))

    source = factory_root / ".agents/skills/software-factory/SKILL.md"
    skill_text = source.read_text(encoding="utf-8")
    skill_text = skill_text.replace("references/", ".factory/playbooks/")
    skill_text = skill_text.replace("scripts/check.py", ".factory/bin/check.py")
    skill_text = skill_text.replace("scripts/claims.py", ".factory/bin/claims.py")
    skill_text = skill_text.replace("scripts/bootstrap.py", "the upstream Software Factory bootstrap script")
    install(repo / ".agents/skills/software-factory/SKILL.md", skill_text)

    # Retain only lean runtime tools; the source kit remains the editable upstream.
    for name in ("check.py", "claims.py"):
        source = factory_root / "scripts" / name
        install(repo / ".factory/bin" / name, source.read_text(encoding="utf-8"))

    changelog = (factory_root / "CHANGELOG.md").read_text(encoding="utf-8")
    match = re.search(r"^## \[(\d+\.\d+\.\d+)\]", changelog, flags=re.M)
    if not match:
        raise ValueError("Factory version not found in CHANGELOG")
    install(repo / ".factory/FACTORY-VERSION", match.group(1) + "\n")
    (repo / "docs" / "workstreams").mkdir(parents=True, exist_ok=True)
    print(f"SCAFFOLD: {created} created, {preserved} preserved; research, design and integration are NOT automatically verified.")
    return created, preserved


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--repo", required=True, type=Path)
    p.add_argument("--idea", required=True)
    args = p.parse_args()
    bootstrap(args.repo, args.idea, Path(__file__).resolve().parents[1] / "templates")


if __name__ == "__main__":
    main()
