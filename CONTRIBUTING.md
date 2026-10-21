# Contributing

Contributions are welcome: new tools, corrected metadata, project identity checks, and maintenance updates.

1. Open an issue or pull request with an official upstream link and evidence.
2. Edit `data/tools.json`; use a unique lowercase kebab-case `id`.
3. Keep `teams` and `capabilities` consistent with `data/taxonomy.json`.
4. Use `verification: unverified` for new entries until review. Never claim enterprise readiness without evidence.
5. Run `python scripts/validate.py`, `python scripts/generate.py`, and `python -m unittest discover -s tests`.
6. Commit both source data and generated pages.

**Verification checklist:** confirm official ownership, exact project/edition, current upstream license, latest maintenance evidence, official documentation, deployment modes, and any material restrictions. Document evidence in PR discussion. A GitHub URL alone does not constitute verification.

Avoid exploit payloads, credentials, personal information, unauthorized access instructions, and misleading capability claims. Keep descriptions neutral and concise.
