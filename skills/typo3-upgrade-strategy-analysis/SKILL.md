---
name: typo3-upgrade-strategy-analysis
description: Use when the user explicitly requests a TYPO3 upgrade strategy analysis for a specified source and newer target version, comparing sequential major upgrades, a clean target rebuild with controlled content migration, and a hybrid approach. Inspects the project and database read-only, recommends a favored option for human decision, estimates effort, and writes one Markdown report inside the project. Not for executing upgrades or changing Composer or database state.
license: CC-BY-4.0
---

# TYPO3 upgrade strategy analysis

Recommend the most sensible path from the user-specified TYPO3 source version to a newer user-specified target version. Compare all three strategies, estimate implementation effort, and write one final report. A human owns the decision. Stop before migration execution.

## Scope and safety

- Activate only when the user explicitly asks for strategy selection, rebuild-versus-upgrade advice, feasibility, or an upgrade-strategy report. Do not replace version-specific execution Skills.
- Require the source and target TYPO3 versions before scoring. Ask for either when missing. The target must be a newer major. Treat an unreleased target as provisional research.
- Keep repository, Composer, cache, database, schema, file storage, remote service, and deployment inspection read-only. The sole write allowed in this run is the final Markdown report described below.
- Allowed inspection includes repository searches, file reads, version checks, Composer inspection, TYPO3 CLI listing, read-only database metadata and `SELECT` queries, SQL-dump streaming, and documentation research.
- Do not install or update packages, start services merely for evidence, run upgrade wizards, update schemas or reference indexes, migrate data, flush or warm caches, build assets, deploy, import a dump, or run a command whose useful path may change state.
- Keep credentials, secrets, and unnecessary record content out of commands and reports. Treat a user's statement that a dump contains no personal data as reported evidence and still inspect only fields that affect the strategy.
- Explicit invocation authorizes creation of one new report after its path is resolved. Ask before overwriting. Do not create a documentation directory or write outside the project root.
- If the user asks to begin implementation, complete only the analysis and hand execution to a separately authorized process.

## Required workflow

1. **Establish the contract.** Read applicable repository instructions and inspect Git status. Record the source and target versions, business constraints, requested decision owner, accessible evidence, and safe tools. Ask for a missing version before scoring. Use [project discovery](references/project-discovery.md) to classify facts as known, inferred, reported, or unknown.

   **Complete when:** source and target are recorded, the target is newer, every evidence category has a status and limitation, and prerelease status is visible.

2. **Classify the installation and platform.** Determine whether the project is Composer-based, legacy non-Composer, or mixed. Establish exact TYPO3, PHP, database, webserver, operating environment, container, hosting, and deployment versions from corroborated evidence. For TYPO3 v8 or a similarly old installation, load [the legacy v8 assessment](references/legacy-v8-assessment.md).

   **Complete when:** each version is evidenced or explicitly unresolved, and conflicting signals remain visible.

3. **Inventory the application.** Identify TYPO3 system extensions, third-party extensions, custom extensions, site packages, integrations, scheduled tasks, CLI jobs, and external APIs. Inspect custom PHP and Extbase, hooks, TCA, TypoScript, Fluid, localization, routing, forms, workspaces, FAL, frontend assets, custom tables, and deployment configuration. Classify each extension as maintain, upgrade, port, replace, retire, or unresolved.

   **Complete when:** every discovered extension and custom-code area has source evidence, target evidence, owned data or behavior, proposed action, and confidence.

4. **Profile data and operations.** Prefer an existing read-only database connection. Use metadata and aggregate queries to measure content types, records, relations, languages, files, FAL references, hidden and deleted records, workspaces, and custom schemas. When no connection exists, inspect a supplied SQL dump without importing or changing it. Follow the dump coverage and privacy rules in [project discovery](references/project-discovery.md). Assess tests, deployment automation, database and file backups, rollback, downtime, URLs, SEO, and editorial acceptance.

   **Complete when:** content and integrity drivers are measured or decision-blocking, dump coverage is disclosed, and database backup evidence is separate from file-storage recovery.

5. **Research compatibility.** Use current or archived official TYPO3 documentation first, then TYPO3 changelogs and tagged source, primary extension-vendor material, and package registries or vendor repositories. Community material may identify leads but cannot be sole compatibility evidence. Record direct URLs and access dates. If online research is unavailable, explain the affected claims and ask whether to continue provisionally, pause, or use primary documents supplied by the user.

   **Complete when:** every time-sensitive feasibility claim has a primary source or is marked unverified.

6. **Compare all strategies.** Apply [the strategy comparison framework](references/strategy-comparison-framework.md) to sequential upgrades through the required intermediate majors, a clean installation of the specified target with controlled content and file migration, and a hybrid approach. Derive weights from explicit constraints and defaults, show and freeze them before rating, and request confirmation only when priorities conflict or a weight change could alter the winner.

   **Complete when:** all three strategies have criterion-level ratings, evidence, disqualifiers, uncertainty, sensitivity results, and project-specific rejection reasons.

7. **Estimate labor.** Apply [the effort estimation model](references/effort-estimation-model.md). Estimate person-hour ranges for every strategy and workstream using one-hour endpoints. Use the user's historical under-48-hour migration experience as a calibration and anomaly check, not a cap, score, or disqualifier. Explain any range that exceeds it. State assumptions, exclusions, uncertainty, and confidence. Do not present estimates as quotes.

   **Complete when:** strategy totals reconcile with workstreams and every range names its evidence and uncertainty drivers.

8. **Recommend for human decision.** Favor one strategy when the evidence supports it. Otherwise recommend a proof-of-concept gate with a hypothesis, representative slice, pass and fail thresholds, timebox, and decision unlocked. Add a phased implementation plan with validation and rollback gates. Keep detailed execution in separately authorized downstream work.

   **Complete when:** the recommendation follows from evidence, rejected strategies have explicit reasons, and the decision record identifies a human owner with status `pending`.

9. **Build and save the report.** Fill [the analysis report template](references/analysis-report-template.md) in memory. Follow repository instructions for documentation paths. Otherwise use an existing `Documentation/`, then an existing `docs/`. If neither exists or both are plausible, ask for an in-project destination. Resolve the path inside the project root and reject escaping symlinks. Name the file `typo3-upgrade-strategy-analysis-<source>-to-<target>.md` with filesystem-safe version labels. Ask before overwriting an existing or modified report. A dirty worktree alone does not block creation. After every path decision is settled, write the report once. If saving fails or the user declines a path, return the complete report in the conversation and state why no file was written.

   **Complete when:** the report passes the evidence and safety audit and is written once or returned completely with the blocked write reported.

## Decision rules

- Require an evidenced baseline, extension and custom-code inventory, content and relation profile, operational constraints, and current compatibility sources for a final recommendation. If a missing category could change the winner, issue a provisional comparison and proof-of-concept gate.
- Do not publish a single weighted total while a decision-blocking criterion is unrated. Show a bounded range and the evidence that could move it.
- Treat a supplied SQL dump as a valid database backup and analysis input. Do not treat it as a file-storage backup. Record its origin and coverage without modifying it.
- Prefer a read-only database connection over dump parsing. A best-effort dump parser must disclose product and format, supported and unsupported constructs, tables or byte ranges inspected, exact or approximate counts, errors, skipped sections, and provisional findings. Keep parsing in memory or streams and create no helper files.
- Direct SQL may be proposed as a later controlled migration mechanism. Database writes require separate authorization, database and file backups as applicable, mapping, TYPO3 invariant checks, reconciliation, trial runs, and rollback criteria.
- Keep strategy advice separate from approval. The report recommends; the human decision owner approves or rejects later.
- Refer to `typo3-v11-to-v12-upgrade`, `typo3-v12-to-v13-upgrade`, and `typo3-v13-to-v14-upgrade` only when the chosen sequential path includes those transitions. Do not invoke them automatically or invent detailed commands for uncovered transitions.

## Resources

- [Project discovery](references/project-discovery.md) covers evidence classes, safe inspection, database access, and SQL-dump profiling.
- [Strategy comparison framework](references/strategy-comparison-framework.md) defines strategies, weights, scoring, disqualifiers, and sensitivity checks.
- [Legacy v8 assessment](references/legacy-v8-assessment.md) covers old non-Composer and mixed projects.
- [Effort estimation model](references/effort-estimation-model.md) defines person-hour ranges, workstreams, the 48-hour calibration, and confidence.
- [Analysis report template](references/analysis-report-template.md) defines the required deliverable and decision record.
- [Evaluation cases](evals/evals.json) cover project types, evidence gaps, SQL safety, report writes, and execution boundaries.
