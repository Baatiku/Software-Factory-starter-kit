# Contributing and factory updates

This project should continuously improve through evidence, not accumulated bureaucracy.

1. Open a GitHub issue or explain a concrete observed gap (missing page, duplicate work, security incident, bad vendor choice, integration failure).
2. Separate universally reusable process rules from one product's requirements.
3. Change the smallest affected skill/reference/template/script. Update CHANGELOG.md and, for changed scripts, add a failing-before/passing-after regression test.
4. Preserve generated-project compatibility; document migration when renaming or removing templates/fields.
5. Run: python -m unittest discover -s tests -v; python scripts/check.py --repo . --gate kit
6. Use a PR for nontrivial changes, with expected files, safety impact and clear verification evidence. Protect main with human review where possible.
7. A project-specific adaptation belongs in that project's docs; only generalizable lessons come back here.

Do not include private user memories, personal secrets, proprietary reference files or provider tokens in this public repository.
