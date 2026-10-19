#!/usr/bin/env python3
"""Portable, dependency-free universal work bootstrap, audit and safe upgrade tool.
Structural/evidence checks are never a substitute for real execution.
"""
import argparse
import hashlib
import json
import os
import re
import tempfile
from pathlib import Path

VERSION = '1.0.0'
PROFILES = ('general', 'software', 'publishing', 'research', 'automation',
            'design', 'business', 'infrastructure', 'analytics')
DEPTHS = ('quick', 'standard', 'high-assurance')
STATUS = ('PLANNED', 'PARTIAL', 'IMPLEMENTED_UNVERIFIED', 'VERIFIED', 'DELIVERED')
CORE_FILES = ('routing.md', 'execution.md', 'evidence.md', 'security.md',
              'coordination.md', 'improvement.md')
PROFILE_TEMPLATES = {
    'general': (),
    'software': ('EXPERIENCE.md', 'ARCHITECTURE.md', 'TEST-PLAN.md'),
    'publishing': ('EDITORIAL-PLAN.md', 'SOURCES.md'),
    'research': ('SOURCES.md',),
    'automation': ('AUTOMATION-CONTRACT.md', 'TEST-PLAN.md'),
    'design': ('EXPERIENCE.md',),
    'business': ('COSTS-AND-RISKS.md',),
    'infrastructure': ('OPERATIONS.md', 'TEST-PLAN.md'),
    'analytics': ('DATA-CONTRACT.md',),
}
HIGH_ASSURANCE = ('RISK-AND-APPROVALS.md', 'RECOVERY.md', 'ACCEPTANCE.md')
AUTO_HINTS = {
    'software': ('app', 'website', 'code', 'software', 'flutter', 'frontend', 'backend', 'api'),
    'publishing': ('news', 'article', 'publish', 'editorial', 'newsletter', 'blog'),
    'research': ('research', 'compare', 'study', 'investigate', 'analysis'),
    'automation': ('mcp', 'agent', 'workflow', 'automate', 'scheduler', 'webhook'),
    'design': ('design', 'logo', 'brand', 'poster', 'interface'),
    'business': ('business', 'proposal', 'marketing', 'campaign', 'sales'),
    'infrastructure': ('cloud', 'deploy', 'hosting', 'server', 'database', 'backup'),
    'analytics': ('dataset', 'dashboard', 'analytics', 'metrics', 'spreadsheet'),
}
RISK_WORDS = ('payment', 'wallet', 'custody', 'medical', 'health data', 'identity',
              'financial', 'production database', 'delete accounts')


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def choose_profile(idea):
    text = idea.lower()
    words = set(re.findall(r'[a-z0-9-]+', text))
    scores = {key: sum(1 for hint in hints if (hint in words if ' ' not in hint else hint in text))
              for key, hints in AUTO_HINTS.items()}
    winner = max(scores.values())
    matches = [p for p, s in scores.items() if s == winner and s > 0]
    return matches[0] if len(matches) == 1 else 'general'


def choose_depth(idea, requested):
    if requested != 'auto':
        return requested
    lowered = idea.lower()
    return 'high-assurance' if any(word in lowered for word in RISK_WORDS) else 'standard'


def paths_for(profile, depth):
    names = ['WORK-OUTCOME.md']
    if depth != 'quick':
        names += ['ACCEPTANCE.md', 'CONTINUE-HERE.md']
        names += PROFILE_TEMPLATES[profile]
    if depth == 'high-assurance':
        names += HIGH_ASSURANCE
    return tuple(dict.fromkeys(names))


def safe(root, rel):
    if Path(rel).is_absolute() or any(x in ('', '.', '..') for x in Path(rel).parts):
        raise ValueError('Invalid destination path: ' + str(rel))
    parent = root
    for part in Path(rel).parts:
        parent = parent / part
        if parent.is_symlink():
            raise ValueError('Symlink destination forbidden: ' + str(rel))
    return parent


def write_new(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open('xb') as f:
            f.write(data)
        return True
    except FileExistsError:
        return False


def atomic_replace(path, data):
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix='.factory-stage-')
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(data)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def source(root, rel):
    path = root / rel
    if not path.is_file() or path.is_symlink():
        raise ValueError('Factory source missing: ' + str(path))
    return path.read_bytes()


def source_bundle(factory_root, profile, depth, idea):
    if profile not in PROFILES or depth not in DEPTHS:
        raise ValueError('Unknown profile or depth')
    bundle = {}
    for name in paths_for(profile, depth):
        data = source(factory_root, 'factory/templates/' + name)
        bundle['docs/' + name] = data.replace(b'{{IDEA}}', idea.encode('utf-8'))
    bundle['AGENTS.md'] = source(factory_root, 'factory/templates/AGENTS.md')
    bundle['.agents/skills/work-factory/SKILL.md'] = source(
        factory_root, '.agents/skills/work-factory/SKILL.md')
    bundle['.agents/skills/' + profile + '-work/SKILL.md'] = source(
        factory_root, '.agents/skills/' + profile + '-work/SKILL.md')
    for name in CORE_FILES:
        bundle['.factory/core/' + name] = source(factory_root, 'factory/core/' + name)
    bundle['.factory/packs/' + profile + '/PLAYBOOK.md'] = source(
        factory_root, 'factory/packs/' + profile + '/PLAYBOOK.md')
    if profile == 'software':
        for name in ('screen-design.md', 'research-and-simplicity.md',
                     'technology-economics.md', 'parallel-delivery.md',
                     'verification-and-release.md', 'security-privacy-operations.md'):
            bundle['.factory/packs/software/references/' + name] = source(
                factory_root, 'references/' + name)
    bundle['.factory/bin/factory.py'] = source(factory_root, 'scripts/factory.py')
    if profile in ('software', 'automation', 'infrastructure'):
        bundle['.factory/bin/claims.py'] = source(factory_root, 'scripts/claims.py')
    return bundle


def manifest(profile, depth, idea, files):
    return {'schema': 1, 'factory_version': VERSION, 'profile': profile,
            'depth': depth, 'idea': idea, 'files': files}


def load_manifest(target):
    p = safe(target, '.factory/work-manifest.json')
    if not p.is_file():
        raise ValueError('No universal Work Factory manifest: run init')
    data = json.loads(p.read_text(encoding='utf-8'))
    if data.get('schema') != 1 or data.get('profile') not in PROFILES or data.get('depth') not in DEPTHS:
        raise ValueError('Unsupported or corrupt manifest; migration required')
    if not isinstance(data.get('files'), dict):
        raise ValueError('Invalid file inventory')
    return data


def init(target, factory_root, idea, profile='auto', depth='auto'):
    if not target.is_dir() or target.is_symlink() or target.resolve() == factory_root.resolve():
        raise ValueError('Choose an existing target directory distinct from the factory')
    if not idea.strip():
        raise ValueError('Idea is required')
    target, factory_root = target.resolve(), factory_root.resolve()
    meta_path = safe(target, '.factory/work-manifest.json')
    if meta_path.exists():
        raise ValueError('Already initialized: use upgrade')
    profile = choose_profile(idea) if profile == 'auto' else profile
    depth = choose_depth(idea, depth)
    bundle = source_bundle(factory_root, profile, depth, idea)
    records = {}
    for rel, data in sorted(bundle.items()):
        dest = safe(target, rel)
        if write_new(dest, data):
            records[rel] = sha256(data)
        else:
            records[rel] = None
    meta = manifest(profile, depth, idea, records)
    if not write_new(meta_path, (json.dumps(meta, indent=2, sort_keys=True) + '\n').encode()):
        raise ValueError('Concurrent manifest creation; do not overwrite')
    return {'profile': profile, 'depth': depth,
            'created': sum(x is not None for x in records.values()),
            'preserved': sum(x is None for x in records.values())}


def upgrade(target, factory_root, apply=False):
    target = target.resolve()
    meta = load_manifest(target)
    bundle = source_bundle(factory_root, meta['profile'], meta['depth'], meta['idea'])
    decisions = []
    for rel, incoming in sorted(bundle.items()):
        dest = safe(target, rel)
        old = meta['files'].get(rel, '__UNTRACKED__')
        fresh = sha256(incoming)
        if not dest.exists():
            decision = 'CREATE' if old in ('__UNTRACKED__', None) else 'RESTORE'
        elif not dest.is_file():
            decision = 'CONFLICT'
        else:
            local = sha256(dest.read_bytes())
            if old in ('__UNTRACKED__', None):
                decision = 'PRESERVE_LOCAL'
            elif local != old:
                decision = 'PRESERVE_LOCAL'
            elif local == fresh:
                decision = 'CURRENT'
            else:
                decision = 'UPDATE'
        decisions.append({'path': rel, 'action': decision})
        if apply and decision in ('CREATE', 'RESTORE', 'UPDATE'):
            if decision == 'UPDATE':
                atomic_replace(dest, incoming)
            else:
                if not write_new(dest, incoming):
                    raise ValueError('Concurrent file write: ' + rel)
            meta['files'][rel] = fresh
    if apply:
        meta['factory_version'] = VERSION
        atomic_replace(safe(target, '.factory/work-manifest.json'),
                       (json.dumps(meta, indent=2, sort_keys=True) + '\n').encode())
    return decisions


def check(target, gate='structure'):
    problems = []
    try:
        meta = load_manifest(target)
    except (ValueError, OSError, json.JSONDecodeError) as e:
        return ['MANIFEST ' + str(e)]
    for rel, digest in meta['files'].items():
        try:
            path = safe(target, rel)
            if not path.is_file():
                problems.append('MISSING ' + rel)
            elif digest and sha256(path.read_bytes()) != digest:
                pass  # Local customization is permitted.
        except ValueError:
            problems.append('UNSAFE_PATH ' + rel)
    if gate in ('delivery', 'release'):
        for name in paths_for(meta['profile'], meta['depth']):
            p = safe(target, 'docs/' + name)
            if not p.is_file() or b'<!-- TODO' in p.read_bytes() or b'{{IDEA}}' in p.read_bytes():
                problems.append('UNFINISHED docs/' + name)
        ev = safe(target, '.factory/evidence.json')
        if not ev.is_file():
            problems.append('NO_EVIDENCE')
        else:
            try:
                obj = json.loads(ev.read_text(encoding='utf-8'))
                if obj.get('status') not in STATUS:
                    problems.append('INVALID_STATUS')
                if gate == 'release' and obj.get('status') not in ('VERIFIED', 'DELIVERED'):
                    problems.append('NOT_VERIFIED')
                if obj.get('status') in ('VERIFIED', 'DELIVERED'):
                    items = obj.get('proof')
                    if not isinstance(items, list) or not items or any(
                        not isinstance(x, dict) or not x.get('description') or
                        not x.get('artifact') or not x.get('method') or
                        x.get('result') != 'PASS_REAL' for x in items):
                        problems.append('VERIFICATION_WITHOUT_REAL_PROOF')
                    if meta['profile'] in ('software', 'automation', 'infrastructure') and not obj.get('commit_sha'):
                        problems.append('CODE_PROOF_WITHOUT_SHA')
                if gate == 'release' and meta['depth'] == 'high-assurance' and not obj.get('approval'):
                    problems.append('HIGH_ASSURANCE_APPROVAL_MISSING')
            except (OSError, ValueError, TypeError):
                problems.append('CORRUPT_EVIDENCE')
    return problems


def main():
    p = argparse.ArgumentParser(description='Universal Work Factory (structural tooling)')
    p.add_argument('--factory-root', type=Path, default=Path(__file__).resolve().parent.parent)
    sub = p.add_subparsers(dest='action', required=True)
    i = sub.add_parser('init')
    i.add_argument('--repo', required=True, type=Path)
    i.add_argument('--idea', required=True)
    i.add_argument('--profile', choices=('auto',) + PROFILES, default='auto')
    i.add_argument('--depth', choices=('auto',) + DEPTHS, default='auto')
    u = sub.add_parser('upgrade')
    u.add_argument('--repo', required=True, type=Path)
    u.add_argument('--apply', action='store_true')
    c = sub.add_parser('check')
    c.add_argument('--repo', required=True, type=Path)
    c.add_argument('--gate', choices=('structure', 'delivery', 'release'), default='structure')
    d = sub.add_parser('doctor')
    d.add_argument('--repo', required=True, type=Path)
    args = p.parse_args()
    if args.action == 'init':
        print(json.dumps(init(args.repo, args.factory_root, args.idea, args.profile, args.depth), indent=2))
    elif args.action == 'upgrade':
        print(json.dumps({'applied': args.apply, 'changes': upgrade(args.repo, args.factory_root, args.apply)}, indent=2))
    else:
        errors = check(args.repo, 'structure' if args.action == 'doctor' else args.gate)
        print(json.dumps({'status': 'STRUCTURE_PASS' if not errors else 'NOT_READY',
                          'note': 'Not evidence of actual execution', 'findings': errors}, indent=2))
        if errors:
            raise SystemExit(1)


if __name__ == '__main__':
    main()
