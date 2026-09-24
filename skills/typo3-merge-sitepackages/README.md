# Merge TYPO3 Site Packages

A reusable workflow for consolidating two TYPO3 site packages, side packages, or theme extensions into one TYPO3-compliant target extension while preserving deliberate customizations and resolving conflicts explicitly.

## Use when

- Combining two TYPO3 site packages or theme extensions into one target package.
- Reconciling TypoScript, site sets, Fluid templates, TCA overrides, Composer metadata, assets, or version compatibility.
- You need an evidence-based merge process with a clear conflict winner.

## What this skill solves

It makes a potentially destructive package consolidation reviewable by establishing a conflict winner, target TYPO3 version, and evidence-led merge process before edits.

## Expected outputs

- An `analyze` mode with a package inventory, conflict matrix, and compatibility risks without file mutations.
- A `plan` mode with a source-to-target mapping, explicit conflict decisions, validation, and rollback.
- An `execute` mode that merges structured configuration and code in reviewable batches with an evidence-based completion report.

## Context requirements

The priority package must be known before the merge begins. The target TYPO3 version must be established from the root `composer.json` or confirmed by the user. Perform the work in a reviewable branch and preserve source-package history until the merged result has been verified.

## Installation

Install this package through an Agent Plugins-compatible client. Compatible clients discover this skill at `skills/typo3-merge-sitepackages/`; installation, enablement, and permissions are client-managed.

## Example prompts

- "Merge these two TYPO3 site packages into one target extension, using the design-system package as the conflict winner."
- "Compare our legacy and replacement TYPO3 sitepackages and produce a safe consolidation plan for TYPO3 13."
- "Consolidate the TypoScript, Fluid templates, assets, and Composer metadata from these two TYPO3 theme extensions."

## Validation

Run `skills-ref validate skills/typo3-merge-sitepackages` when the reference validator is available, then review [evals/evals.json](evals/evals.json) against the representative, compatibility, and destructive-boundary cases. After a real merge, run the target project's prescribed checks and report every required check as pass, fail, blocked, or not run.

## Related skills

- [TYPO3 upgrade strategy analysis](../typo3-upgrade-strategy-analysis/README.md) compares sequential, rebuild, and hybrid paths when site package consolidation is part of a larger migration.
- [TYPO3 v11 to v12 upgrade](../typo3-v11-to-v12-upgrade/README.md), [TYPO3 v12 to v13 upgrade](../typo3-v12-to-v13-upgrade/README.md), and [TYPO3 v13 to v14 upgrade](../typo3-v13-to-v14-upgrade/README.md) handle major TYPO3 core migrations before or after merging packages.
- [TYPO3 Tailwind CSS migration](../typo3-tailwind-migration/README.md) helps when consolidating and modernizing divergent CSS assets into a unified Tailwind CSS v4 pipeline.
- [TYPO3 Gridelements to Container](../typo3-gridelements-to-container/README.md) guides converting legacy Gridelements layouts to Container CTypes when reconciling content element definitions.

## License

This skill is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](../../LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).

## Resources

- [Merge guidelines](references/merge-guidelines.md) — file-by-file merge workflow, validation commands, and reporting format.
- [TYPO3 site package standards](references/typo3-sitepackage-standards.md) — expected layout, Composer configuration, and compatibility considerations.
- [Evaluation cases](evals/evals.json) — regression prompts for runtime safety and routing.
