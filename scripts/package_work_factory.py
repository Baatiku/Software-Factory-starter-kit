#!/usr/bin/env python3
"""Deterministic ZIP for portable universal router and optionally one specialist."""
import argparse
import zipfile
from pathlib import Path
from factory import PROFILES, CORE_FILES

ROOT = Path(__file__).resolve().parents[1]
STAMP = (2026, 10, 19, 0, 0, 0)


def files_for(profile):
    if profile != 'all' and profile not in PROFILES:
        raise ValueError('Unknown pack')
    result = {
        'work-factory/SKILL.md': ROOT / '.agents/skills/work-factory/SKILL.md',
        'work-factory/scripts/factory.py': ROOT / 'scripts/factory.py',
        'work-factory/scripts/claims.py': ROOT / 'scripts/claims.py',
    }
    for name in CORE_FILES:
        result['work-factory/core/' + name] = ROOT / 'factory/core' / name
    for p in PROFILES if profile == 'all' else (profile,):
        result['work-factory/packs/' + p + '/PLAYBOOK.md'] = ROOT / 'factory/packs' / p / 'PLAYBOOK.md'
        result['work-factory/specialists/' + p + '-work/SKILL.md'] = (
            ROOT / '.agents/skills' / (p + '-work') / 'SKILL.md')
    for f in sorted((ROOT / 'factory/templates').glob('*')):
        if f.is_file():
            result['work-factory/templates/' + f.name] = f
    return result


def build(output, profile='all'):
    files = files_for(profile)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, path in sorted(files.items()):
            if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(ROOT):
                raise ValueError('Unsafe source: ' + str(path))
            info = zipfile.ZipInfo(name, date_time=STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return len(files)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--profile', choices=('all',) + PROFILES, default='all')
    p.add_argument('--output', type=Path, default=ROOT / 'dist/work-factory.zip')
    args = p.parse_args()
    print('Packed', build(args.output, args.profile), 'files into', args.output)


if __name__ == '__main__':
    main()
