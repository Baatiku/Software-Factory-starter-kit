# Contributing to Universal Work Factory

Keep **one** maintained skill family and shared references. New domain capability belongs in `factory/packs/<profile>/`, and universal reusable guidance in `factory/core/`; avoid copy-pasted variants.

1. Identify a real limitation or lesson from a project. Classify it as universal, pack-specific or project-only.
2. Make the smallest necessary update, remove conflicting rules, and keep requirements accurate.
3. Add positive/negative tests for code changes and document a migration for existing generated projects when a format/path changes.
4. Execute `python -m unittest discover -s tests -v`, `python scripts/check_kit.py` and `python scripts/package_work_factory.py --profile all --output dist/work-factory.zip`.
5. Open a reviewed PR, merge safe compatible source after checks, separately qualify publication/prod effects.
6. Never commit secrets, private memories, proprietary datasets or fabricated execution evidence.

The factory repository is the source of truth for methods; do not assume changing this repository changes anyone's ChatGPT account.
