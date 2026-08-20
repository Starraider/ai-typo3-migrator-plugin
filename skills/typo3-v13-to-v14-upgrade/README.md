# TYPO3 v13 to v14 Upgrade

A reusable workflow for analyzing, planning, and safely executing a TYPO3 13 to 14 major-version upgrade. It emphasizes dependency compatibility, staged migrations, dry-run refactoring, explicit data-safety boundaries, and evidence-based verification.

## Use when

- Moving a Composer-based TYPO3 project from v13 to v14.
- Investigating Composer blockers, extension support, deprecations, Rector or Fractor migrations.
- Preparing an implementation plan with rollback points and acceptance checks.

## What this skill solves

It converts a complex TYPO3 13 to 14 migration into a controlled sequence that identifies blockers before changes, separates consequential decisions, and records verification evidence.

## Expected outputs

- `analyze` mode to establish a baseline, extension inventory, and blocker list without changing project files, Composer state, caches, or the database.
- `plan` mode for an ordered migration plan, risks, project-adapted commands, approval gates, rollback points, and acceptance criteria.
- `execute` mode for narrow, reversible changes with dry-runs and verification at each phase.

## Context requirements

Use a local, DDEV, or parallel non-production environment with database and file backups. Read the target repository's `AGENTS.md`, work on a dedicated branch, and confirm version-specific behavior in current official TYPO3 and package-vendor documentation before acting. Data-changing upgrade wizards, schema changes, and deployments require explicit authorization.

## Installation

Install this package through an Agent Plugins-compatible client. Compatible clients discover this skill at `skills/typo3-v13-to-v14-upgrade/`; installation, enablement, and permissions are client-managed.

## Example prompts

- "Analyze this TYPO3 13 Composer project for TYPO3 14 readiness without changing files."
- "Plan our TYPO3 13 to 14 upgrade with Rector, Fractor, DDEV, rollback points, and acceptance checks."
- "Identify extensions and Composer constraints that block upgrading this sitepackage to TYPO3 14."

## Validation

Run `skills-ref validate skills/typo3-v13-to-v14-upgrade` when the reference validator is available, then review [evals/evals.json](evals/evals.json) against the representative, edge-case, and production-boundary cases. For a real migration, run the target repository's checks and report every required check as pass, fail, blocked, or not run.

## Related skills

Use `typo3-merge-sitepackages` when the migration also requires a separately scoped package consolidation. The other upgrade skills cover earlier TYPO3 major-version transitions.

## License

This skill is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](../../LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).

## Resources

- [Command reference](references/command-reference.md) — commands and validation guidance.
- [Plan template](references/plan-template.md) — the staged migration-plan format.
- [Evaluation cases](evals/evals.json) — representative prompts and expected safety behavior.
