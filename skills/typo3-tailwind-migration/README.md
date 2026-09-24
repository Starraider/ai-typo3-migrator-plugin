# TYPO3 Tailwind CSS v4 Migration

## What this skill solves

It guides a planned migration of one TYPO3 site package from legacy/custom CSS to Tailwind CSS v4 in DDEV. The workflow protects approved legacy behavior with reviewed visual baselines, then incrementally changes the build pipeline, design tokens, Fluid templates, components, and legacy styles.

## Use when

- A TYPO3 theme needs a full or staged Tailwind CSS v4 migration.
- Existing page and component rendering must remain consistent at agreed URLs and viewports.
- The work includes baseline capture, build integration, template conversion, accessibility, and supported-browser checks.

Do not use it for a small isolated CSS fix. Use `typo3-playwright-ddev` (available in `ai-typo3-integrator-plugin` or project test suite) when the required test infrastructure is not ready.

## Expected outputs

- An agreed migration inventory, URL/viewport matrix, and reviewed legacy baseline set.
- A DDEV build pipeline that compiles Tailwind v4 and loads the resulting stylesheet through TYPO3.
- Incrementally migrated layouts and components, each verified with narrow smoke/VRT coverage.
- A final quality result and legacy-CSS deletion only after explicit authorization.

## Context requirements

- A TYPO3 DDEV project and the target site-package directory.
- The legacy site’s representative mounted URLs, supported viewport/browser matrix, and any intentional design changes.
- A working Playwright environment or permission to establish one first.
- Permission before dependency, build, template, snapshot, and deletion changes.

## Installation

This directory is a portable Agent Skill. Install the complete plugin through a compatible Agent Plugin client, or copy/symlink this directory into that client’s Agent Skills discovery path. Codex can use the bundled `agents/openai.yaml` for presentation metadata.

Keep the full directory—including all `references/` and `evals/`—with `SKILL.md` during installation.

## Example prompts

- “Plan a Tailwind v4 migration for this TYPO3 site package, starting by inventorying layouts, content elements, and real test URLs.”
- “Migrate the header and navigation to Tailwind while keeping the existing approved mobile and desktop screenshots green.”
- “We have no visual baselines yet. Set up the test-first portion of a TYPO3 Tailwind migration, but ask before dependencies or snapshots are written.”

## Included resources

- [Migration checklist](references/migration-checklist.md)
- [Tailwind v4 build-pipeline guidance](references/build-pipeline.md)
- [Design-token mapping](references/design-tokens.md)
- [TYPO3 Fluid integration guidance](references/fluid-integration.md)
- [Migration anti-patterns](references/anti-patterns.md)

## Validation

From the plugin root, validate the portable structure with the `new-skill` validator and the reference validator when available:

```bash
/path/to/new-skill/scripts/validate-skill.sh skills/typo3-tailwind-migration --strict-portable
skills-ref validate skills/typo3-tailwind-migration
```

Then review the representative, edge-case, and near-miss scenarios in [evals/evals.json](evals/evals.json). A migration is complete only when its agreed test matrix passes and any legacy-CSS deletion was explicitly authorized.

## Related skills

- [Merge TYPO3 site packages](../typo3-merge-sitepackages/README.md) — consolidate multiple theme extensions or site packages before or during Tailwind CSS migration.
- [TYPO3 upgrade strategy analysis](../typo3-upgrade-strategy-analysis/README.md) — evaluate frontend theme and CSS modernization effort alongside core upgrade paths.
- [TYPO3 v11 to v12 upgrade](../typo3-v11-to-v12-upgrade/README.md), [TYPO3 v12 to v13 upgrade](../typo3-v12-to-v13-upgrade/README.md), and [TYPO3 v13 to v14 upgrade](../typo3-v13-to-v14-upgrade/README.md) — handle the core upgrade path that modern site packages and Tailwind pipelines run against.
- `typo3-playwright-ddev` and `typo3-playwright-workflow` (available in `ai-typo3-integrator-plugin`) provide the underlying visual regression test infrastructure and focused check execution.

## License

This skill is licensed under [CC BY 4.0](../../LICENSE). Copyright (c) 2026 Sven Kalbhenn.
