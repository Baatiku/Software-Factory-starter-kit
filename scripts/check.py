#!/usr/bin/env python3
"""Evidence-aware *structural* checks; never represent these as actual E2E proof."""
import argparse
import json
import re
from pathlib import Path

REQUIRED = [
    'PROJECT-CHARTER.md', 'COMPETITOR-RESEARCH.md', 'PRODUCT-SCOPE.md',
    'SCREEN-INVENTORY.md', 'SCREEN-SPECS.md', 'DESIGN-SYSTEM.md',
    'FEATURE-CONTRACTS.md', 'REQUIREMENTS-TRACEABILITY.md',
    'ARCHITECTURE-CONTRACTS.md', 'STACK-DECISIONS.md', 'COST-MODEL.md',
    'THREAT-MODEL.md', 'PRIVACY-DATA-MAP.md', 'TEST-STRATEGY.md',
    'OPERATIONS-RUNBOOK.md', 'WORKSTREAMS.md', 'RELEASE-GATES.md',
    'ACCEPTANCE-JOURNEYS.md', 'DECISIONS.md', 'LESSONS-LEARNED.md',
    'WINDOW-HANDOFF.md', 'TRACEABILITY.json', 'RELEASE-EVIDENCE.json',
]


def sha(s):
    return isinstance(s, str) and bool(re.fullmatch('[0-9a-f]{40}', s))


def check_delivery_handoff(h: dict) -> list[str]:
    """Validate optional milestone metadata, never certify actual execution."""
    if 'delivery_schema_version' not in h:
        return []  # Existing projects adopt deliberately; no forced migration.
    findings = []
    if h.get('delivery_schema_version') != 1:
        return ['UNSUPPORTED DELIVERY SCHEMA']
    if not isinstance(h.get('milestone_id'), str) or not h['milestone_id'].strip():
        findings.append('DELIVERY MISSING MILESTONE')
    journeys = h.get('journeys')
    if not isinstance(journeys, list) or not journeys or any(
            not isinstance(j, str) or not j.strip() for j in journeys):
        findings.append('DELIVERY MISSING JOURNEYS')
    complete = h.get('source_complete')
    remaining = h.get('remaining_source')
    if not isinstance(complete, bool) or not isinstance(remaining, list) or any(
            not isinstance(item, str) or not item.strip() for item in remaining):
        findings.append('DELIVERY INVALID SOURCE COMPLETENESS')
    elif complete and remaining:
        findings.append('DELIVERY COMPLETE WITH SOURCE REMAINING')
    elif not complete and (not remaining or h.get('status') != 'PARTIAL_IMPLEMENTATION'):
        findings.append('DELIVERY PARTIAL SOURCE MISCLASSIFIED')
    blockers = h.get('blocked_actions')
    if not isinstance(blockers, list):
        findings.append('DELIVERY MISSING BLOCKER ASSIGNMENTS')
    else:
        for blocker in blockers:
            if not isinstance(blocker, dict) or any(
                    not isinstance(blocker.get(k), str) or not blocker[k].strip()
                    for k in ('reason', 'owner', 'next_action')):
                findings.append('DELIVERY BLOCKER MISSING REASON/OWNER/NEXT ACTION')
    return findings


def check(repo: Path, gate: str) -> list[str]:
    problems = []

    def need(path):
        if not (repo / path).is_file():
            problems.append('MISSING ' + path)
            return False
        return True

    if gate == 'kit':
        for p in ['README.md', 'AGENTS.md', '.agents/skills/software-factory/SKILL.md',
                  'scripts/bootstrap.py', 'scripts/check.py', 'scripts/claims.py',
                  'scripts/package_skill.py', 'tests/test_package_skill.py',
                  '.github/workflows/skill-package.yml', 'install/INSTALLATION.md',
                  'install/CUSTOM-INSTRUCTIONS.txt', 'install/MEMORY-SUMMARY-PROPOSAL.txt',
                  'tests/test_factory.py', 'tests/test_claims.py',
                  '.github/workflows/checks.yml', 'CONTRIBUTING.md', 'CHANGELOG.md']:
            need(p)
        for p in ['operating-protocol.md','owner-defaults.md','research-and-simplicity.md',
                  'screen-design.md','technology-economics.md','parallel-delivery.md',
                  'security-privacy-operations.md','verification-and-release.md',
                  'continuous-improvement.md','skill-capability-audit.md']:
            need('references/' + p)
        for p in REQUIRED:
            need('templates/' + p)
        for p in ['AGENTS.md', 'CONTINUE-HERE.md']:
            need('templates/' + p)
        return problems
    for p in ['.agents/skills/software-factory/SKILL.md',
              '.factory/FACTORY-VERSION', '.factory/bin/check.py',
              '.factory/bin/claims.py', '.factory/playbooks/operating-protocol.md']:
        need(p)
    for p in REQUIRED:
        need('docs/' + p)
    need('AGENTS.md')
    need('CONTINUE-HERE.md')
    if gate == 'scaffold' or problems:
        return problems
    docs = repo / 'docs'
    readable = [p for p in REQUIRED if p.endswith('.md') and p not in
                ('WINDOW-HANDOFF.md', 'LESSONS-LEARNED.md', 'DECISIONS.md',
                 'RELEASE-GATES.md', 'OPERATIONS-RUNBOOK.md')]
    for p in readable:
        value = (docs / p).read_text(encoding='utf-8')
        if '<!-- TODO' in value or '{{' in value:
            problems.append('UNRESOLVED ' + p)
    if gate in {'design', 'handoff', 'release'}:
        inventory = (docs / 'SCREEN-INVENTORY.md').read_text(encoding='utf-8')
        specs = (docs / 'SCREEN-SPECS.md').read_text(encoding='utf-8')
        ids = re.findall(r'^\|\s*(SC-\d{3,})\s*\|', inventory, re.M)
        sections = re.findall(r'^##\s+(SC-\d{3,})\b', specs, re.M)
        if not ids or len(ids) != len(set(ids)):
            problems.append('EMPTY OR DUPLICATE SCREEN INVENTORY')
        if len(sections) != len(set(sections)) or set(ids) != set(sections):
            problems.append('SCREEN SPECS NOT ONE-TO-ONE WITH INVENTORY')
        for sid in set(sections):
            match = re.search(r'^##\s+' + sid + r'\b(.*?)(?=^##\s+SC-\d{3,}\b|\Z)', specs, re.M | re.S)
            part = match.group(1) if match else ''
            for word in ['Layout', 'Controls', 'States', 'Data', 'Access', 'Proof']:
                if word not in part:
                    problems.append(f'{sid} MISSING {word}')
        try:
            trace = json.loads((docs / 'TRACEABILITY.json').read_text(encoding='utf-8'))
            for key in ('requirements', 'screens', 'journeys', 'workstreams'):
                if not isinstance(trace.get(key), list) or not trace[key]:
                    problems.append('TRACEABILITY EMPTY ' + key)
            valid_screen_ids = set(ids)
            valid_journeys = {j.get('id') for j in trace.get('journeys', [])}
            valid_workstreams = {w.get('id') for w in trace.get('workstreams', [])}
            for s in trace.get('screens', []):
                if s.get('id') not in valid_screen_ids:
                    problems.append('UNMAPPED SCREEN ' + str(s.get('id')))
            if {s.get('id') for s in trace.get('screens', [])} != valid_screen_ids:
                problems.append('TRACEABILITY SCREENS DIFFER FROM INVENTORY')
            for r in trace.get('requirements', []):
                if r.get('scope') not in ('CORE_NOW', 'DIFFERENTIATOR_NOW', 'LATER', 'EXCLUDE'):
                    problems.append('UNCLASSIFIED REQUIREMENT ' + str(r.get('id')))
                if r.get('scope') in ('CORE_NOW', 'DIFFERENTIATOR_NOW'):
                    if not set(r.get('screens', [])) & valid_screen_ids:
                        problems.append('CORE REQ MISSING SCREEN ' + str(r.get('id')))
                    if not set(r.get('journeys', [])) & valid_journeys:
                        problems.append('CORE REQ MISSING JOURNEY ' + str(r.get('id')))
                    if not set(r.get('owners', [])) & valid_workstreams:
                        problems.append('CORE REQ MISSING OWNER ' + str(r.get('id')))
                    if not r.get('tests'):
                        problems.append('CORE REQ MISSING TEST ' + str(r.get('id')))
        except (OSError, ValueError, TypeError) as e:
            problems.append('INVALID TRACEABILITY JSON ' + str(e))
    if gate in ('handoff', 'release'):
        handoffs = sorted((docs / 'workstreams').glob('*.json'))
        if not handoffs:
            problems.append('NO WORKSTREAM HANDOFF JSON')
        for f in handoffs:
            try:
                h = json.loads(f.read_text(encoding='utf-8'))
                problems.extend(issue + ' ' + f.name for issue in check_delivery_handoff(h))
                if not sha(h.get('base_sha')) or not sha(h.get('head_sha')):
                    problems.append('HANDOFF MISSING COMMIT SHAS ' + f.name)
                if not h.get('paths') or not h.get('tests') or not h.get('pr'):
                    problems.append('HANDOFF MISSING PATHS/TESTS/PR ' + f.name)
                if h.get('status') in ('VERIFIED_E2E', 'DEPLOYED_VERIFIED'):
                    if not any(isinstance(t, dict) and t.get('status') == 'PASS_REAL'
                               and t.get('commit_sha') == h.get('head_sha') and t.get('artifact') and t.get('command')
                               for t in h.get('tests', [])):
                        problems.append('VERIFIED CLAIM WITHOUT PASS_REAL EVIDENCE ' + f.name)
                if h.get('status') not in ('PARTIAL_IMPLEMENTATION', 'IMPLEMENTED_UNVERIFIED', 'VERIFIED_E2E', 'DEPLOYED_VERIFIED'):
                    problems.append('INVALID HANDOFF STATUS ' + f.name)
            except (OSError, ValueError) as e:
                problems.append('INVALID HANDOFF ' + f.name + ': ' + str(e))
    if gate == 'release':
        try:
            ev = json.loads((docs / 'RELEASE-EVIDENCE.json').read_text(encoding='utf-8'))
            if not sha(ev.get('commit_sha')) or not ev.get('human_approval'):
                problems.append('RELEASE SHA OR HUMAN APPROVAL MISSING')
            if not isinstance(ev.get('journeys'), list) or not ev['journeys']:
                problems.append('NO RELEASE JOURNEY EVIDENCE')
            else:
                required_journeys = {j for r in trace.get('requirements', [])
                                     if r.get('scope') in ('CORE_NOW', 'DIFFERENTIATOR_NOW')
                                     for j in r.get('journeys', [])} if 'trace' in locals() else set()
                found_journeys = {j.get('id') for j in ev['journeys']}
                for missing in required_journeys - found_journeys:
                    problems.append('MISSING RELEASE JOURNEY ' + str(missing))
                for j in ev['journeys']:
                    if j.get('status') != 'PASS_REAL' or not j.get('command') or not j.get('artifact') or not sha(j.get('commit_sha')) or j.get('commit_sha') != ev.get('commit_sha'):
                        problems.append('UNVERIFIED RELEASE JOURNEY ' + str(j.get('id')))
        except (OSError, ValueError, TypeError) as e:
            problems.append('INVALID RELEASE EVIDENCE ' + str(e))
    return problems


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--gate', choices=['kit', 'scaffold', 'design', 'handoff', 'release'], default='scaffold')
    args = p.parse_args()
    problems = check(args.repo.resolve(), args.gate)
    if problems:
        print(args.gate.upper() + ': NOT READY (STRUCTURE ONLY)')
        for issue in problems:
            print(' -', issue)
        raise SystemExit(1)
    print(args.gate.upper() + ': STRUCTURE PASS (NOT proof of real test execution or release fitness)')


if __name__ == '__main__':
    main()

