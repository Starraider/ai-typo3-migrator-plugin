# TYPO3 upgrade strategy analysis

This portable Agent Skill recommends how to move a TYPO3 project from a user-specified source version to a newer user-specified target. It compares sequential upgrades, a clean target rebuild with controlled content migration, and a hybrid path. Technical analysis is read-only. The Skill writes one final Markdown report inside the project and stops before implementation.

## What this skill solves

TYPO3 upgrade choices depend on extension support, custom PHP, templates, content relations, URLs, editorial workflows, infrastructure, and recovery quality. This Skill turns that evidence into a transparent comparison, person-hour ranges, a favored option for human decision, and a phased implementation plan.

## Use when

- The user explicitly asks whether a TYPO3 project should be upgraded sequentially, rebuilt on a specified target, or handled as a hybrid migration.
- A legacy, Composer-based, or mixed installation needs feasibility and effort analysis before code or data changes.
- A project team needs a source-backed strategy report with risks, confidence, missing evidence, validation gates, and rollback planning.

Do not use it to execute an upgrade, mutate a database, update Composer dependencies, deploy a release, or replace a version-specific migration Skill.

## Expected outputs

- A recommendation for a named human decision owner, or a proof-of-concept gate.
- A project baseline and evidence inventory.
- Extension and custom-code compatibility findings.
- Content, database, file, template, integration, and infrastructure findings.
- A comparison of all three strategies with frozen weights, disclosed disqualifiers, and sensitivity results.
- Person-hour ranges by strategy and workstream, using one-hour endpoints and the under-48-hour historical calibration as an anomaly check.
- A phased implementation plan with validation and rollback gates.
- Explicit rejection reasons, a source list with access dates, and a decision record whose initial status is `pending`.
- One report named `typo3-upgrade-strategy-analysis-<source>-to-<target>.md` in the project's documentation folder.

## Context requirements

Invoke the Skill inside the TYPO3 project repository and provide the source and target TYPO3 versions. The target must be a newer major. Confidence improves with access to:

- repository instructions, Composer or legacy package metadata, custom extensions, templates, configuration, build files, and deployment definitions;
- exact PHP, database, webserver, and infrastructure versions;
- an existing read-only database connection, or a supplied SQL dump when no connection is available;
- current or archived official TYPO3 documentation and primary extension-vendor sources;
- test, database backup, file backup, rollback, downtime, URL, SEO, and editorial acceptance requirements.

The Skill keeps technical inspection read-only. Explicit invocation authorizes one new report-file write after the destination is resolved. Existing reports require overwrite approval. The Skill never creates a documentation directory or writes outside the project root.

## Installation

The Skill follows the portable Agent Skills specification and is bundled at `skills/typo3-upgrade-strategy-analysis/` in this Agent Plugins 1.0.0 package. Agent Plugin-compatible clients can use the portable `SKILL.md` and its relative references. Installation, enablement, tool permissions, and invocation syntax remain client-managed.

## Compatibility

`agents/openai.yaml` is optional Codex presentation metadata. It disables implicit invocation for Codex. Other clients may not honor that file, so the portable description also limits activation to explicit strategy requests. The report-write behavior is part of the Skill contract and does not depend on Codex metadata.

## Example prompts

- "Use typo3-upgrade-strategy-analysis to compare sequential, rebuild, and hybrid paths from TYPO3 8.7 to TYPO3 14. Write the report to our Documentation folder."
- "Analyze this Composer-based TYPO3 11 project for a move to TYPO3 13. Include compatibility evidence, person-hour ranges, confidence, and a phased plan."
- "Our database is unavailable, but the repository contains a SQL dump. Compare the paths from TYPO3 9.5 to TYPO3 14 without importing or modifying the dump."
- "Assess whether controlled SQL migration could preserve multilingual content, workspaces, custom tables, and FAL relations. Do not begin the migration."

## Validation

From the plugin root, run:

```bash
skills-ref validate skills/typo3-upgrade-strategy-analysis
python3 -m json.tool skills/typo3-upgrade-strategy-analysis/evals/evals.json >/dev/null
```

When the `new-skill` maintainer tooling is installed, also run its `scripts/validate-skill.sh skills/typo3-upgrade-strategy-analysis --strict-portable` command. Check every relative Markdown link and review the maintained evaluation cases. Report unavailable checks instead of claiming they passed.

## Related skills

- `typo3-v11-to-v12-upgrade` may execute that transition after strategy approval.
- `typo3-v12-to-v13-upgrade` may execute that transition after TYPO3 12 is stable.
- `typo3-v13-to-v14-upgrade` may execute that transition after TYPO3 13 is stable.
- `typo3-merge-sitepackages` may help with a separately authorized site-package consolidation.

The strategy Skill does not invoke these automatically or duplicate their execution commands. Paths outside their version coverage need separately designed execution guidance.

## License

This Skill is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](../../LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).

## Resources

- [Project discovery](references/project-discovery.md)
- [Strategy comparison framework](references/strategy-comparison-framework.md)
- [Legacy v8 assessment](references/legacy-v8-assessment.md)
- [Effort estimation model](references/effort-estimation-model.md)
- [Analysis report template](references/analysis-report-template.md)
- [Evaluation cases](evals/evals.json)
