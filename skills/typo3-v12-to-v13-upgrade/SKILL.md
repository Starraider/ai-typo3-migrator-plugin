---
name: typo3-v12-to-v13-upgrade
description: Use when analyzing, planning, or executing a Composer-based TYPO3 12.4 to 13.4 upgrade, including extension compatibility, Composer blockers, PHP/database readiness, Content Blocks 0.x migrations, Rector or Fractor migrations, and deprecated APIs. Not for patch updates, production deployment, or an unrelated site-package merge.
license: CC-BY-SA-4.0
---

# TYPO3 v12 to v13 Upgrade

Produce an evidence-based, staged migration from TYPO3 12.4 to 13.4. Stabilize the source release, resolve compatibility blockers, and verify a copied non-production environment before considering deployment.

## Scope and safety

- Start in `analyze` mode when the user has not chosen a mode. `analyze` and `plan` are read-only: do not alter project files, Composer state, caches, or the database.
- `execute` requires a local, DDEV, or parallel non-production copy, a recoverable database and file-storage backup, and a dedicated branch or an explicitly chosen alternative. Preserve unrelated worktree changes.
- Ask for explicit approval immediately before database-changing commands or backend actions, including database schema updates, upgrade wizards, reference-index updates, Content Blocks data conversions, cleanup, and production deployment. Explain the intended effect first.

## Workflow

1. **Establish context.** Read applicable repository instructions. Inspect Composer manifests/lock file, runtime, DDEV configuration, installed TYPO3 packages, local extensions, Content Blocks, test scripts, and Git status. Confirm current and target TYPO3, PHP, and database versions. **Complete when** project type, execution mode, target environment, and constraints are recorded.
2. **Collect evidence.** In `analyze`, use only inspection commands. Build an extension compatibility matrix and identify Composer, platform, deprecation, webserver, and custom-code blockers. Verify time-sensitive requirements and extension support in current official TYPO3 and vendor documentation. **Complete when** every direct extension is classified as ready, update, migrate, replace, remove, or blocked with evidence.
3. **Plan the migration.** Use [the plan template](references/plan-template.md) to define ordered phases, project-adapted commands, approval gates, rollback points, and acceptance checks. Treat site sets and PAGEVIEW as optional modernization unless explicitly in scope. **Complete when** no Composer transaction or data-changing step lacks prerequisites and a rollback point.
4. **Execute incrementally.** Follow [the command reference](references/command-reference.md): stabilize TYPO3 12, resolve blockers, run and review refactor dry-runs, then update all installed TYPO3 packages together. Do not copy sample package lists blindly. For affected Content Blocks, record data contracts before changing structure and use [the migration checks](references/content-blocks-0x-to-1x.md). **Complete when** Composer resolves without ignored blockers and every approved data action is documented.
5. **Verify and report.** Run repository checks first, then automated and manual checks. Use [v13 change hotspots](references/v13-change-hotspots.md) for targeted review. Report results as pass, fail, blocked, or not run; do not claim production readiness while required checks remain incomplete. **Complete when** the completion report records changed packages, wizards, data/schema actions, tests, manual checks, residual risks, and rollback instructions.

## Mode outputs

- `analyze`: baseline, compatibility matrix, blockers, risks, and missing evidence; no mutations.
- `plan`: a filled migration plan with approval gates and acceptance criteria; no mutations.
- `execute`: scoped changes plus a completion report. Pause at every unapproved consequential boundary.

## Resources

- [Command reference](references/command-reference.md) — inspection, migration, and verification commands.
- [Content Blocks migration checks](references/content-blocks-0x-to-1x.md) — use only for Content Blocks 0.x to 1.x work.
- [v13 change hotspots](references/v13-change-hotspots.md) — platform and migration areas requiring focused review.
- [Plan template](references/plan-template.md) — migration-plan and completion-report structure.
- [Evaluation cases](evals/evals.json) — representative, edge-case, and boundary prompts.
