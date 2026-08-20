# TYPO3 12 LTS → 13.4 LTS Upgrade

A portable, safety-first workflow for moving a TYPO3 project from version 12 LTS to version 13.4 LTS. It covers dependency resolution, copied-database upgrades, Content Blocks 0.x compatibility, TSConfig changes, and evidence-based verification.

## What this skill solves

It turns a risky major-version change into a staged, reviewable migration with explicit dependency, data-preservation, and acceptance evidence.

## Use when

- Planning or implementing a TYPO3 12 to 13.4 migration.
- Reviewing a proposed v13 dependency, database, or Content Blocks migration.
- Building a migration evidence report before a separately approved deployment.

It is not for TYPO3 patch updates, deployments, or unrelated extension migrations.

## Expected outputs

- A read-only `analyze` mode with a compatibility matrix, blockers, and missing evidence.
- A `plan` mode with approval-gated database work, rollback points, and project-adapted commands.
- An `execute` mode with a reviewed dependency/source migration, preservation comparisons, and pass/fail/blocked verification evidence.

## Context requirements

- Composer manifests and lock file.
- Project runtime/build/test commands and database CLI.
- A non-production database and file-storage backup location.
- Approval for any data-changing wizard, conversion, rename, cleanup, or deployment.

## Installation

Install this package through an Agent Plugins-compatible client, then invoke `typo3-v12-to-v13-upgrade` for the relevant project. Client installation, enablement, and permissions are client-managed. The skill itself uses portable Agent Skills frontmatter.

## Example prompts

- “Plan and execute the upgrade of this TYPO3 12.4 site to TYPO3 13.4 on our local DDEV copy.”
- “Review this TYPO3 12→13 Composer update and identify unsafe schema or extension decisions.”
- “Migrate our Content Blocks 0.7 definitions as part of a TYPO3 13 upgrade, preserving CTypes and FAL data.”

## Validation

Run `skills-ref validate skills/typo3-v12-to-v13-upgrade` when the reference validator is available, then review [evals/evals.json](evals/evals.json) with the migration, Content Blocks, and production-boundary prompts. For a real migration, run the target repository's checks and report every required check as pass, fail, blocked, or not run.

## Related skills

Use `typo3-v13-to-v14-upgrade` only after the v13 migration is stable and separately verified. Use `typo3-merge-sitepackages` for a separately scoped package consolidation.

## License

CC-BY-SA-4.0.

## Resources

- [Command reference](references/command-reference.md) — inspection, migration, and verification commands.
- [Content Blocks migration checks](references/content-blocks-0x-to-1x.md) — preservation-focused 0.x to 1.x migration guidance.
- [v13 change hotspots](references/v13-change-hotspots.md) — targeted technical review areas.
- [Plan template](references/plan-template.md) — migration-plan and completion-report structure.
- [Evaluation cases](evals/evals.json) — regression prompts for runtime safety and routing.
