---
name: typo3-v11-to-v12-upgrade
description: Use when analyzing, planning, or executing a Composer-based TYPO3 11.5 to 12.4 upgrade, including extension compatibility, Composer blockers, PHP/database readiness, Rector or Fractor migrations, and deprecated APIs. Not for patch updates, production deployment, or an unrelated site-package merge.
---

# TYPO3 v11 to v12 Upgrade

Produce an evidence-based, staged migration from TYPO3 11.5 to 12.4. Establish readiness and blockers before changing dependencies, then preserve rollback evidence and verify the upgraded non-production copy.

## Scope and safety

- Start in `analyze` mode when the user has not chosen a mode. `analyze` and `plan` are read-only: do not alter project files, Composer state, caches, or the database.
- `execute` requires a local, DDEV, or parallel non-production copy, a recoverable database and file-storage backup, and a dedicated branch or an explicitly chosen alternative. Preserve unrelated worktree changes.
- Ask for explicit approval immediately before database-changing commands or backend actions, including database schema updates, upgrade wizards, reference-index updates, data conversions, cleanup, and production deployment. Explain the intended effect first.
- TYPO3 12 regular support ended on 2026-04-30. State whether 12.4 is an interim destination toward a supported release or requires ELTS.

## Workflow

1. **Establish context.** Read applicable repository instructions. Inspect the Composer manifests/lock file, runtime, DDEV configuration, installed TYPO3 packages, local extensions, test scripts, and Git status. Confirm the current and target TYPO3, PHP, and database versions. **Complete when** the project type, execution mode, target environment, and constraints are recorded.
2. **Collect evidence.** In `analyze`, use only inspection commands. Build an extension compatibility matrix and identify Composer, platform, deprecation, and custom-code blockers. Verify time-sensitive version requirements and extension support in current official TYPO3 and vendor documentation. **Complete when** every direct extension is classified as ready, update, migrate, replace, remove, or blocked with evidence.
3. **Plan the migration.** Use [the plan template](references/plan-template.md) to define ordered phases, exact project-adapted commands, approval gates, rollback points, and acceptance checks. Keep Rector/Fractor and optional modernization separate from the core migration. **Complete when** no Composer transaction or data-changing step lacks prerequisites and a rollback point.
4. **Execute incrementally.** Follow [the command reference](references/command-reference.md): stabilize the latest TYPO3 11 patch release, resolve blockers, run and review refactor dry-runs, then update all installed TYPO3 packages together. Do not copy sample package lists blindly. Review the diff after each applied step. **Complete when** Composer resolves without ignored blockers and every approved database action is documented.
5. **Verify and report.** Run the repository's checks first, then the applicable automated and manual checks. Use [v12 change hotspots](references/v12-change-hotspots.md) for targeted review. Report results as pass, fail, blocked, or not run; do not claim production readiness while required checks remain incomplete. **Complete when** the completion report records changed packages, wizards, data/schema actions, tests, manual checks, residual risks, and rollback instructions.

## Mode outputs

- `analyze`: baseline, compatibility matrix, blockers, risks, and missing evidence; no mutations.
- `plan`: a filled migration plan with approval gates and acceptance criteria; no mutations.
- `execute`: scoped changes plus a completion report. Pause at every unapproved consequential boundary.

## Resources

- [Command reference](references/command-reference.md) — inspection, migration, and verification commands.
- [v12 change hotspots](references/v12-change-hotspots.md) — platform and migration areas requiring focused review.
- [Plan template](references/plan-template.md) — migration-plan and completion-report structure.
- [Evaluation cases](evals/evals.json) — representative, edge-case, and boundary prompts.
