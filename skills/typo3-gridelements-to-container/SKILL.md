---
name: typo3-gridelements-to-container
description: Use when analyzing, planning, or executing a TYPO3 migration from EXT:gridelements to the current b13/container extension. Recreate every used legacy grid as a project-owned Container CType, preserve its frontend markup and child ordering, then use a reviewed, dry-run-first database migration script to replace Gridelements relations. Includes a staged route for data created by Gridelements 8.7.0. Not for a TYPO3 core upgrade without this extension migration, a visual redesign, or an unreviewed production database rewrite.
license: CC-BY-4.0
compatibility: Requires a copied non-production TYPO3 13.4 or 14.3 project with b13/container installed, access to legacy Gridelements records/configuration, and explicit approval before source or database writes.
---

# TYPO3 Gridelements to Container

Replace used Gridelements layouts with project-owned Container CTypes and convert their existing `tt_content` rows without changing content-element UIDs. The target is equivalent child placement, ordering, language behavior, and frontend markup on a restorable non-production copy.

## Scope and safety

- Start in `analyze` mode unless the user selects `plan` or `execute`. `analyze` and `plan` are read-only. Do not alter source, Composer state, caches, or the database.
- `execute` requires a dedicated branch or explicitly accepted alternative, a verified restore of the database and file storage, a copied non-production environment, and recorded page and content baselines. Preserve unrelated worktree changes.
- Ask for explicit approval immediately before creating or changing project files, installing or removing extensions, applying the migration script, repairing sorting, running a reference-index update, deleting legacy fields, or deploying. Describe the records and effect first.
- Never run the migration against production, remove `gridelements`, or drop its columns until the converted database, frontend, backend editing, languages, and rollback have passed review.

## Workflow

1. **Establish the source and target.** Read repository instructions and inspect the TYPO3, PHP, database, Composer, DDEV, site-package, Gridelements, and Container state. Inventory source records, layout definitions from Page TSconfig and `tx_gridelements_backend_layout`, legacy rendering TypoScript and Fluid templates, translations, workspaces, references, FlexForms, and direct Gridelements dependencies. Record exact source Gridelements and target Container versions. **Complete when** every used legacy layout and its rendered URLs are known, and the target supports the installed core version.
2. **Handle Gridelements 8.7.0 correctly.** Read [the 8.7 compatibility notes](references/gridelements-8-7-compatibility.md) before deciding the route. Current Container supports TYPO3 13.4 and 14.3, so it cannot be installed in a TYPO3 8.7 runtime. Preserve the legacy `tt_content` columns and layout definitions in the copied database while it reaches the target runtime, then run the conversion there. **Complete when** the old `CType`, layout, parent, column, and sorting values are demonstrably available on the target copy.
3. **Create and prove the replacement CTypes.** For each used source layout, build a mapping record and use [the registration template](templates/ContainerRegistration.php.template) to register one distinct Container CType. Translate the complete grid matrix, including names, `colPos`, `colspan`, `rowspan`, allowed/disallowed types, and `maxitems`. Choose collision-safe custom target `colPos` values and map every source column. Rebuild each layout's TypoScript and Fluid rendering with the Container processor appropriate to the target core, preserving its deliberate wrappers, classes, conditions, and FlexForm behavior. **Complete when** every mapped target CType loads in TYPO3, accepts its intended columns, and renders a manually created representative instance like the legacy one.
4. **Plan the data rewrite.** Use [the mapping and data-model reference](references/mapping-and-data-model.md) and fill [the migration-command template](templates/MigrateGridelementsToContainerCommand.php.template) with the approved layout, column, and FlexForm mappings. Keep the legacy relation columns until post-migration cleanup. The command must default to dry run, reject unknown layouts/columns, reject bad parent PIDs, exclude workspaces, preserve UIDs and `sorting`, and convert connected translations to the original container parent. **Complete when** the dry-run report accounts for every mapped parent and child and reports zero unmapped or invalid records.
5. **Apply and validate.** After approval, run the reviewed command once with its explicit write flags inside one transaction. Run the relevant Container integrity checks in report mode, then obtain separate approval before any repair mode. Flush caches and update the reference index according to the target project's normal procedure. Compare record counts, UIDs, parent links, columns, ordering, languages, backend drag and drop, and frontend output at the approved URLs. Follow [the execution runbook](references/execution-runbook.md). **Complete when** all checks are pass, fail, blocked, or not run, with evidence and a rollback instruction.
6. **Retire the legacy extension.** Only after approval and a stable acceptance period, remove Gridelements rendering/configuration and Composer dependency, handle other extensions that reference it, and remove the old schema columns through the target project's normal schema process. **Complete when** zero live records use `CType = gridelements_pi1` or a nonzero Gridelements parent/column field, and the final backup can still be restored.

## Required outputs

- A source-layout inventory and one explicit legacy-layout to Container-CType mapping per used layout.
- Container registration, TypoScript, Fluid, FlexForm, and icon changes that preserve the approved frontend.
- A dry-run-first, project-owned TYPO3 command based on the bundled template, plus its machine-readable report.
- A post-apply reconciliation report with database, backend, frontend, language, and rollback evidence.

## Resources

- [Gridelements 8.7 compatibility](references/gridelements-8-7-compatibility.md) — legacy storage model and target-runtime route.
- [Mapping and data model](references/mapping-and-data-model.md) — relation, column, language, FlexForm, and rendering rules.
- [Execution runbook](references/execution-runbook.md) — inventory queries, approval gates, reconciliation, and cleanup.
- [Container registration template](templates/ContainerRegistration.php.template) — adapt one registration per used layout.
- [Migration command template](templates/MigrateGridelementsToContainerCommand.php.template) — copy into the target extension and tailor before dry run.
- [Evaluation cases](evals/evals.json) — representative, 8.7 edge-case, and production-boundary prompts.
