# TYPO3 Gridelements to Container

This skill moves a TYPO3 site's used Gridelements layouts to `b13/container` without treating it as a visual redesign. It reconstructs every used grid as a normal Container CType, ports the rendering that gave it its look, and replaces the legacy parent and column relations in `tt_content` with a reviewed database command.

## What this skill solves

Gridelements and Container model nested content differently. This skill prevents the tempting but broken shortcut of changing only the parent CType. It maps the real legacy child cell, preserves parent links and sorting, and checks the rendering that the data model alone cannot retain.

## Use when

- A TYPO3 project must replace EXT:gridelements with the current Container extension.
- Existing nested grids, translated content, FlexForms, or carefully styled layouts must retain their structure and frontend output.
- A project still has Gridelements 8.7.0 data and is moving that database through a TYPO3 upgrade to Container on TYPO3 13.4 or 14.3.

It is not for a core upgrade with no Gridelements work, a new Container layout with no legacy content to convert, or a frontend redesign.

## Expected outputs

- A used-layout inventory and a complete source-to-target mapping.
- One registered Container CType, rendering configuration, and template per used source layout.
- A project-owned command that reports first, then rewrites only approved `tt_content` rows in one transaction.
- Reconciliation evidence for row counts, parent/column relations, ordering, translations, backend editing, and frontend output.

## Important compatibility rule

Gridelements 8.7.0 records use `CType = gridelements_pi1`, `tx_gridelements_container`, `tx_gridelements_columns`, and `colPos = -1` for children. Current Container uses real custom `colPos` values plus `tx_container_parent`. Container 4.1.0 supports TYPO3 13.4 and 14.3, not TYPO3 8.7. Migrate a database copy only after it reaches a supported target runtime, while retaining the old columns and layout definitions needed by the conversion.

## Context requirements

- A copied, restorable database and file-storage backup. Never point the command at production.
- Source Gridelements configuration in Page TSconfig, `tx_gridelements_backend_layout`, and rendering TypoScript or Fluid files.
- The target site package, target TYPO3 version, current `b13/container`, and a way to run project commands.
- Approved baseline pages in each language and one instance of every used layout, including nested layouts.

## Installation

This directory is part of the plugin's `skills/` folder. Install the plugin using [the project installation guide](../../plugin-installation.md), or install this directory as a standalone portable Agent Skill in a client-supported skill location. Codex can discover it automatically or invoke it as `$typo3-gridelements-to-container`.

## Example prompts

- "Analyze this TYPO3 project for replacing Gridelements with Container. Do not change the project or database."
- "Create equivalent Container CTypes for our Gridelements layouts, then prepare a dry-run migration command for the copied DDEV database."
- "Our content was created with Gridelements 8.7.0 on TYPO3 8.7. We are moving to TYPO3 14. Build the staged mapping and database conversion, preserving translations and nested grids."

## Validation

Run the structural checks from the repository root:

```bash
/Users/svenkalbhenn/.agents/skills/new-skill/scripts/validate-skill.sh skills/typo3-gridelements-to-container --strict-portable
skills-ref validate skills/typo3-gridelements-to-container
```

For a real migration, run the generated command without `--apply`, resolve every reported exception, then run the target project's tests and the Container integrity commands. The required database and visual comparisons are described in [the execution runbook](references/execution-runbook.md).

## Related skills

- [TYPO3 v11 to v12 upgrade](../typo3-v11-to-v12-upgrade/README.md), [TYPO3 v12 to v13 upgrade](../typo3-v12-to-v13-upgrade/README.md), and [TYPO3 v13 to v14 upgrade](../typo3-v13-to-v14-upgrade/README.md) cover the core-version path that may bring a Gridelements 8.7 database to a Container-compatible runtime.

## License

This skill is licensed under the [Creative Commons Attribution 4.0 International License](../../LICENSE).

Copyright (c) 2026 Sven Kalbhenn.
