# TYPO3 v11 to v12 Upgrade

A reusable, safety-first workflow for upgrading a Composer-based TYPO3 project from 11.5 LTS to 12.4 LTS. The skill covers readiness assessment, dependency and extension compatibility, code and configuration migration, and acceptance evidence.

## Use when

- You need to analyze, plan, or execute a TYPO3 11 to 12 major-version upgrade.
- Composer constraints, extensions, Rector, Fractor, deprecations, or platform requirements may block the migration.
- You need a reviewable upgrade plan before modifying a non-production copy of a project.

## What this skill solves

It turns a high-risk TYPO3 11 to 12 migration into a staged, reviewable workflow with explicit blocker discovery, approval boundaries, rollback points, and verification evidence.

## Expected outputs

- An `analyze` mode for inventorying versions, blockers, and risks without changing code.
- A `plan` mode with phased commands, rollback points, and acceptance criteria.
- An `execute` mode for incremental, verified implementation after approval.

## Context requirements

Run major upgrades on a local, DDEV, or parallel non-production copy with database and file backups. Read the target repository's `AGENTS.md` first, verify version-specific facts against current official documentation, and establish a dedicated Git branch before edits. The skill flags that TYPO3 v12 is no longer in regular support after 2026-04-30, so it should normally be an interim step toward a supported target or use ELTS.

## Installation

Install this package through an Agent Plugins-compatible client. Compatible clients discover this skill at `skills/typo3-v11-to-v12-upgrade/`; installation, enablement, and permissions are client-managed.

## Example prompts

- "Analyze this TYPO3 11.5 project for readiness to upgrade to TYPO3 12.4 without changing files."
- "Create a phased TYPO3 11 to 12 migration plan that includes Composer blockers, Rector, and a rollback strategy."
- "Review this proposed TYPO3 12 Composer update for unsafe schema, extension, or platform decisions."

## Validation

Validate the package from its root with the Agent Plugin validator, and validate this directory with an Agent Skills validator before release.

## Related skills

Use `typo3-v12-to-v13-upgrade` when the project must continue from TYPO3 12 to 13. Use `typo3-merge-sitepackages` for a separately scoped site-package consolidation.

## License

No package-wide license file is supplied. Confirm the applicable terms before redistributing this skill.

## Resources

- [Command reference](references/command-reference.md) — inspection, migration, and verification commands.
- [v12 change hotspots](references/v12-change-hotspots.md) — areas commonly affected by the upgrade.
- [Plan template](references/plan-template.md) — phased migration and reporting structure.
