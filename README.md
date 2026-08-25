# AI TYPO3 Migrator Plugin

`ai-typo3-migrator-plugin` is an Agent Plugins 1.0.0 package containing portable Agent Skills for TYPO3 upgrades, extension migrations and site-package consolidation. It has no bundled MCP servers.

## Use cases

- PlanTYPO3 upgrade paths (sequential, rebuild, hybrid).
- Migrate from TYPO3 v11 → v12, v12 → v13, and v13 → v14.
- Consolidate multiple site packages into a single extension.
- Analyze extension compatibility and deprecations.
- Generate migration strategies and change-management summaries.

## Installation

- [Install the complete Agent Plugin](plugin-installation.md) in Codex, Cursor,
  GitHub Copilot, or Visual Studio Code.
- [Install individual Agent Skills](skill-installation.md) in Antigravity,
  OpenCode, Windsurf, Zed, Trae, or Qoder.

## Skills

- [TYPO3 upgrade strategy analysis](skills/typo3-upgrade-strategy-analysis/README.md) compares sequential upgrades, a clean rebuild, and a hybrid migration between user-specified TYPO3 versions, then writes one strategy report.
- [TYPO3 v11 to v12 upgrade](skills/typo3-v11-to-v12-upgrade/README.md) — analyze, plan, and execute a staged TYPO3 11.5 to 12.4 migration.
- [TYPO3 v12 to v13 upgrade](skills/typo3-v12-to-v13-upgrade/README.md) — safely move a Composer-based TYPO3 12.4 project to TYPO3 13.4.
- [TYPO3 v13 to v14 upgrade](skills/typo3-v13-to-v14-upgrade/README.md) — assess blockers and complete a controlled TYPO3 13 to 14 migration.
- [Merge TYPO3 site packages](skills/typo3-merge-sitepackages/README.md) — consolidate two TYPO3 site packages into one target extension.

- [TYPO3 Gridelements to Container](skills/typo3-gridelements-to-container/README.md) — recreate used Gridelements layouts as Container CTypes and migrate their content relations with a dry-run-first database command, including Gridelements 8.7.0 data.

## Package layout

Compatible Agent Plugins clients discover the skills from immediate child directories of `skills/`. Each skill is self-contained and includes runtime instructions, supporting references, a detailed README, and representative/edge-case/boundary evaluation prompts. The `agents/openai.yaml` files retained within skill directories are optional client-specific display metadata; they are not part of the portable Agent Plugins core.

The package declares Agent Plugins schema version 1.0.0 in [plugin.json](plugin.json). Installation, enablement, permissions, and client-specific presentation are managed by the consuming client.

## License

This project and all contained Agent Skills are licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).
