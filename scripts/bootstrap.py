#!/usr/bin/env python3
"""Copy project starter templates without overwriting existing project files."""
import argparse
from pathlib import Path


def bootstrap(repo: Path, idea: str, template_root: Path) -> tuple[int, int]:
    if not repo.is_dir():
        raise ValueError('Repository directory does not exist')
    if not idea.strip():
        raise ValueError('Product idea is required')
    created = preserved = 0
    for src in sorted(template_root.iterdir()):
        if not src.is_file():
            continue
        destination = repo / src.name if src.name in {'AGENTS.md', 'CONTINUE-HERE.md'} else repo / 'docs' / src.name
        if destination.exists():
            preserved += 1
            print('PRESERVED', destination.relative_to(repo))
            continue
        content = src.read_text(encoding='utf-8')
        if src.name == 'PROJECT-CHARTER.md':
            content = content.replace('{{PROJECT_IDEA}}', idea.strip())
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding='utf-8')
        created += 1
        print('CREATED', destination.relative_to(repo))
    (repo / 'docs' / 'workstreams').mkdir(parents=True, exist_ok=True)
    print(f'SCAFFOLD: {created} created, {preserved} preserved. Research and executable verification NOT performed.')
    return created, preserved


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True, type=Path)
    p.add_argument('--idea', required=True)
    args = p.parse_args()
    bootstrap(args.repo.resolve(), args.idea, Path(__file__).resolve().parents[1] / 'templates')


if __name__ == '__main__':
    main()
