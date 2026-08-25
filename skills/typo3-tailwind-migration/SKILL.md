---
name: typo3-tailwind-migration
description: Migrate a TYPO3 site package from legacy or custom CSS to Tailwind CSS v4 in DDEV while preserving approved rendered behavior. Use for a planned theme migration that needs legacy visual baselines, Tailwind build integration, Fluid-template conversion, accessibility checks, and cross-browser verification. Do not use for a small isolated CSS fix or for setting up Playwright alone.
license: CC-BY-4.0
compatibility: Requires a TYPO3 project with DDEV, a site package that can run Node.js/npm in the DDEV web container, and permission for dependency, build, template, snapshot, and eventual legacy-CSS deletion changes.
---

# TYPO3 Tailwind CSS v4 Migration

Migrate one TYPO3 site package to Tailwind CSS v4 while comparing each approved page and component against known legacy behavior. The target is documented visual parity at agreed URLs and viewports, not an unreviewed snapshot refresh.

## 1. Inventory and agree the migration boundary

Before editing, inspect the DDEV project, site package, current CSS entry points and build scripts, Fluid templates, TypoScript/asset loading, supported browsers, representative page URLs, and existing tests. Create a migration inventory covering layouts, global partials, content elements, themes, client-side behavior, and legacy CSS files.

Ask for any missing mounted URL, viewport, or required intentional design change. If Playwright infrastructure is missing, use `typo3-playwright-ddev` before continuing. A small local styling change belongs in the project’s normal frontend workflow, not this migration skill.

Completion: the package, migration inventory, test URLs, viewport matrix, and acceptance criteria are agreed.

## 2. Capture and protect legacy baselines

Create or extend tests for each representative layout and each content-element state that the inventory identifies. Include the real page URLs and stable, section-level locators where appropriate. Review the initial screenshots before accepting them as baselines.

Creating tests and snapshots writes source files and binary baseline images. Obtain permission immediately before those writes. Do not overwrite existing baselines, stage changes, or commit them without explicit authorization.

Use [the migration checklist](references/migration-checklist.md) to ensure coverage; use `typo3-playwright-workflow` for day-to-day test execution and visual-diff investigation.

Completion: every agreed acceptance surface has a reviewed baseline and a runnable test, with no guessed URLs.

## 3. Add the Tailwind foundation

After permission, make the smallest compatible build change in the site-package directory inside DDEV:

1. Install the Tailwind v4/PostCSS dependencies using the existing package manager.
2. Configure the existing build pipeline or create the minimal one if absent.
3. Add explicit Fluid source scanning and map legacy design values to semantic `@theme` tokens.
4. Load the compiled CSS through the TYPO3 asset collector and prove that a literal utility used in a Fluid template appears in the output.

Do not run host-side package commands when the project requires DDEV. Follow [the build-pipeline guide](references/build-pipeline.md) and [design-token mapping](references/design-tokens.md). Keep complete utility names literal; avoid dynamic class construction unless the classes are explicitly safelisted.

Completion: the DDEV build succeeds, TYPO3 loads the generated stylesheet, and one representative utility renders from the compiled output.

## 4. Migrate incrementally and verify each slice

Migrate in this order unless the project’s dependency graph requires a documented exception:

1. Page layouts and global asset loading.
2. Header, navigation, footer, and shared partials.
3. Content elements, including responsive and sidebar variants.
4. Remaining component-specific legacy styles.

Keep editor-managed content in TYPO3 content APIs; preserve semantic HTML and keyboard behavior. Apply mobile-first utilities and keep JavaScript breakpoint logic aligned with the CSS token. For Fluid patterns, `colPos` propagation, image loading, and accessibility details, read [Fluid integration guidance](references/fluid-integration.md).

After each slice, build inside DDEV, run the narrow smoke/VRT coverage, and review every diff before proceeding. Use [anti-pattern guidance](references/anti-patterns.md) for failure modes that otherwise look like a quick CSS fix.

Completion: the migrated slice passes its agreed smoke and visual checks, or each intentional difference is documented and approved.

## 5. Complete quality checks and clean up safely

Run the agreed full visual suite plus relevant accessibility, mobile, and supported-browser smoke checks. Use a project-specific performance budget or compare the compiled CSS to the agreed baseline; do not assume a universal bundle-size target.

Do not delete legacy CSS until all agreed checks pass and the user explicitly authorizes deletion. Preserve a reviewable migration diff through version control rather than creating unmanaged backup copies. After removal, rebuild and rerun the full affected suite.

Completion: the agreed test matrix passes, intentional changes are documented, legacy files are removed only with approval, and project documentation reflects the final build/test commands.

## Maintainer evaluation

Scenario coverage for this skill is recorded in [evals/evals.json](evals/evals.json). Run the validation commands in the README after editing this skill.
