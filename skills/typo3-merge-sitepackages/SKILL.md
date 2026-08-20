---
name: typo3-merge-sitepackages
description: Use when analyzing, planning, or merging two TYPO3 site packages, theme extensions, or side packages into one target extension, including Composer metadata, TypoScript, site sets, Fluid templates, TCA overrides, PHP namespaces, assets, and target-version compatibility. Not for a TYPO3 core upgrade or a production deployment.
---

# Merge TYPO3 Site Packages

Consolidate two TYPO3 site packages into one target extension while preserving deliberate behavior, making each conflict decision auditable, and retaining a safe rollback path.

## Scope and safety

- Start in `analyze` mode when the user has not chosen a mode. `analyze` and `plan` are read-only: do not copy, move, delete, rename, or overwrite files.
- Before `execute`, establish the target package path, extension key, Composer package name, PHP namespace, target TYPO3 version or supported range, and whether the source packages remain temporarily available.
- A conflict winner is required before resolving same-path or same-key conflicts. Ask the user when it is not specified; do not silently discard the other package's behavior.
- Use a dedicated branch or explicitly chosen alternative. Preserve unrelated worktree changes and source-package history until the merged package passes the agreed checks. Ask before destructive cleanup or production deployment.

## Workflow

1. **Establish the contract.** Read applicable repository instructions and inspect the root Composer manifests/lock file, both packages, target project conventions, and Git status. Determine the execution mode and target TYPO3 compatibility from evidence; ask if signals conflict. **Complete when** every target identifier and supported version is recorded.
2. **Inventory both packages.** Compare file trees and usage sites for Composer metadata, PHP classes, TypoScript, TSconfig, site sets, TCA, Fluid, assets, build tooling, and extension-key/namespace references. Classify each item as unique, equivalent, structured conflict, or winner-takes-path conflict. **Complete when** every conflicting item has an evidence-backed proposed disposition.
3. **Plan the merge.** Use [the merge guidelines](references/merge-guidelines.md) to map each source path to the target and list conflict decisions, reference rewrites, backward-compatibility choices, validation, and rollback. **Complete when** all source behavior is mapped as retained, intentionally replaced, or explicitly dropped.
4. **Execute conservatively.** Apply the approved plan in small reviewable batches. Treat Composer JSON, YAML, TypoScript, TCA, services, templates, and build manifests as structured content; do not use blind directory copies or overwrite them. Normalize names and paths consistently. **Complete when** no stale source extension key, namespace, package name, Fluid path, or asset reference remains in affected code.
5. **Validate and report.** Run repository checks first, then the relevant Composer, TYPO3, build, and browser checks. Use [site-package standards](references/typo3-sitepackage-standards.md) for the target-version shape. Report merged items, retained conflicts, intentionally dropped behavior, validation results, residual risks, and rollback instructions. **Complete when** results are pass, fail, blocked, or not run—never implied.

## Mode outputs

- `analyze`: package inventory, conflict matrix, compatibility risks, and missing decisions; no mutations.
- `plan`: source-to-target mapping, conflict decisions, validation, and rollback plan; no mutations.
- `execute`: scoped merge changes and an evidence-based completion report.

## License

This skill is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](../../LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).

## Resources

- [Merge guidelines](references/merge-guidelines.md) — structured merge rules, validation, and reporting.
- [TYPO3 site-package standards](references/typo3-sitepackage-standards.md) — target layout and compatibility guidance.
- [Evaluation cases](evals/evals.json) — representative, edge-case, and boundary prompts.
