#!/usr/bin/env python3
"""Structural integrity of sole maintained universal kit (not outcome E2E proof)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from factory import PROFILES, CORE_FILES
ROOT = Path(__file__).resolve().parents[1]

def check(root=ROOT):
    issues=[]
    required = ['README.md','AGENTS.md','CHANGELOG.md','CONTRIBUTING.md',
        '.agents/skills/work-factory/SKILL.md','scripts/factory.py',
        'scripts/check_kit.py','scripts/package_work_factory.py',
        'factory/tools/github_claims.py','factory/MIGRATION.md',
        'install/CUSTOM-INSTRUCTIONS.txt','install/CHATGPT-SETUP.md']
    required += ['factory/core/'+n for n in CORE_FILES]
    required += ['factory/packs/'+p+'/PLAYBOOK.md' for p in PROFILES]
    required += ['.agents/skills/'+p+'-work/SKILL.md' for p in PROFILES]
    required += ['factory/packs/software/references/'+n for n in (
       'screen-design.md','research-and-simplicity.md','technology-economics.md',
       'parallel-delivery.md','verification-and-release.md','security-privacy-operations.md')]
    required += ['factory/templates/'+n for n in ('WORK-OUTCOME.md','ACCEPTANCE.md','CONTINUE-HERE.md')]
    retired = ['references','templates','.agents/skills/software-factory',
       'scripts/bootstrap.py','scripts/check.py','scripts/claims.py',
       'scripts/package_skill.py','install/INSTALLATION.md',
       'install/MEMORY-SUMMARY-PROPOSAL.txt']
    for path in required:
        if not (root/path).is_file():
            issues.append('MISSING '+path)
    for path in retired:
        if (root/path).exists():
            issues.append('OBSOLETE '+path)
    for profile in PROFILES:
        skill=(root/'.agents/skills'/f'{profile}-work/SKILL.md')
        if skill.is_file() and not skill.read_text().startswith('---\nname:'):
            issues.append('SKILL_METADATA '+profile)
    return issues

if __name__ == '__main__':
    findings=check()
    print('STRUCTURE_PASS (not product delivery verification)' if not findings else '\n'.join(findings))
    raise SystemExit(bool(findings))
