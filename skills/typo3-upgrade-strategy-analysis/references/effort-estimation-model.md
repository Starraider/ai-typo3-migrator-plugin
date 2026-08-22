# Effort estimation model

Estimate implementation labor as person-hour ranges with one-hour endpoints. The figures support strategy selection. They are not bids, schedules, prices, or contractual commitments.

## Unit and calibration

Record the team convention for one person-hour and state:

- roles and skill levels included;
- whether coordination, product ownership, editorial work, vendor work, and infrastructure operations are included;
- environment access, representative data, documentation, and stakeholder availability;
- expected review, test, and rework cycles;
- parallel work assumptions and dependencies;
- exclusions, third-party lead times, calendar downtime, and procurement.

Use the owner's historical experience that a complete migration normally stays within 48 person-hours as a calibration and anomaly check. It is not a cap, score, target, or disqualifier. When evidence produces a range above 48 hours, report the range and explain which project characteristics fall outside the historical pattern.

Person-hours do not convert directly to elapsed time. Show a calendar range only when staffing and dependencies are known.

## Required workstreams

Estimate every workstream for every strategy. Use zero only with evidence that the workstream does not apply.

| Workstream | Include |
| --- | --- |
| Discovery and proof of concept | Evidence collection, archaeology, representative trials, decision gates, architecture and mapping design |
| Platform and intermediate environments | PHP, database, webserver, containers, historical runtimes, hosting, local and CI parity |
| TYPO3 core and system extensions | Required major steps, package changes, compatibility review, and version-specific remediation |
| Third-party extensions | Vendor research, updates, replacement evaluation, configuration, and owned-data migration |
| Custom PHP and Extbase | Core API changes, hooks and events, persistence, commands, modules, services, and tests |
| Templates, configuration, and frontend | TypoScript, TCA, Fluid, content elements, forms, site configuration, assets, accessibility, and design parity |
| Content, files, and database migration | Mapping, transformations, identifiers, relations, localization, workspaces, FAL, files, metadata, and delta runs |
| Integrations and scheduled work | APIs, authentication, search, CRM or ERP, queues, cron, scheduler, imports, exports, and monitoring |
| Verification and acceptance | Automated tests, reconciliation, URL and SEO checks, performance, security, editorial UAT, and defect cycles |
| Deployment, cutover, and rollback | Pipelines, backups, restore trials, freeze, delta migration, traffic switch, observability, and rollback rehearsal |
| Coordination and documentation | Decision records, stakeholder reviews, handover, runbooks, training, and release planning |

Keep uncertainty allowance separate so the report shows the base estimate and its risk margin.

## Range method

For each workstream:

1. Define the deliverable and completion evidence.
2. Identify countable drivers such as extensions, custom modules, template families, content types, tables, languages, integrations, environments, URL rules, or acceptance journeys.
3. Divide drivers into low, medium, and high complexity using repository and database evidence.
4. Estimate lower and upper person-hour bounds. Use one-hour endpoints and keep a range even when confidence is high.
5. Name dependencies and unknowns that widen the range.
6. Check the result against the 48-hour historical calibration and trustworthy analogous work when available.

One-hour endpoints are the agreed reporting precision, not proof that the forecast is accurate to one hour. Preserve broad ranges when evidence is weak.

## Strategy-specific effort

For sequential upgrades, include repeated platform setup, extension-chain resolution, source stabilization, intermediate validation, data transformations, and rollback points for every required major.

For a clean rebuild, include requirements archaeology, target architecture, reimplementation, content and file mapping, identifier and URL strategy, migration tooling, trial migrations, delta handling, reconciliation, editorial UAT, and cutover. Installing the target is only one task.

For a hybrid, estimate upgraded and rebuilt domains separately, then add boundary design, identifier mapping, cross-domain integration, combined validation, and rollback coordination. Do not assume a hybrid is the cheaper half of the other two strategies.

## Uncertainty allowance

Choose the allowance from evidence, then round lower and upper totals outward to whole person-hours:

| Evidence condition | Typical allowance applied to base range | Confidence tendency |
| --- | ---: | --- |
| Current versions, full inventories, database profile, representative tests, backup evidence, and verified vendor support | 10-20% | high or medium-high |
| Unknown extension behavior, incomplete tests, or partial database or infrastructure evidence | 20-40% | medium |
| Missing database evidence, unknown custom-code ownership, abandoned dependencies, or unverified historical runtime | 40-75% or a separate discovery phase | low |

These bands are defaults. Explain the selected percentage and covered unknowns. Do not pad a workstream and add the same uncertainty again.

## Confidence

Give confidence per strategy and for the recommended total:

- `high`: direct evidence covers the main drivers and representative validation supports the migration mechanism;
- `medium`: the direction is supported, but several workstreams or dependencies can move the range;
- `low`: missing or contradictory evidence could reverse the strategy or widen the range sharply.

List the inputs most likely to narrow each range. Show proof-of-concept effort separately from later implementation.

## Reconciliation table

| Workstream | Sequential hours | Clean rebuild hours | Hybrid hours | Evidence and assumptions | Confidence |
| --- | ---: | ---: | ---: | --- | --- |
| Base subtotal |  |  |  |  |  |
| Uncertainty allowance |  |  |  |  |  |
| Total person-hour range |  |  |  |  |  |

After the table, state exclusions, vendor costs, calendar constraints, whether any total exceeds the 48-hour calibration, and which evidence would change the result.
