# TYPO3 Update Skills

`typo3-update-skills` is an Agent Plugins 1.0.0 package containing portable Agent Skills for TYPO3 upgrades and site-package consolidation. It has no bundled MCP servers.

## Skills

- [TYPO3 v11 to v12 upgrade](skills/typo3-v11-to-v12-upgrade/README.md) — analyze, plan, and execute a staged TYPO3 11.5 to 12.4 migration.
- [TYPO3 v12 to v13 upgrade](skills/typo3-v12-to-v13-upgrade/README.md) — safely move a Composer-based TYPO3 12.4 project to TYPO3 13.4.
- [TYPO3 v13 to v14 upgrade](skills/typo3-v13-to-v14-upgrade/README.md) — assess blockers and complete a controlled TYPO3 13 to 14 migration.
- [Merge TYPO3 site packages](skills/typo3-merge-sitepackages/README.md) — consolidate two TYPO3 site packages into one target extension.

## Package layout

Compatible Agent Plugins clients discover the skills from immediate child directories of `skills/`. Each skill is self-contained and includes runtime instructions, supporting references, a detailed README, and representative/edge-case/boundary evaluation prompts. The `agents/openai.yaml` files retained within skill directories are optional client-specific display metadata; they are not part of the portable Agent Plugins core.

The package declares Agent Plugins schema version 1.0.0 in [plugin.json](plugin.json). Installation, enablement, permissions, and client-specific presentation are managed by the consuming client.

## License

This project and all contained Agent Skills are licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).
