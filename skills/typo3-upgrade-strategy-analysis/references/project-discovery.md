# Project discovery

Use this reference for the baseline, inventory, and privacy-preserving database profile. Gather only evidence that can affect strategy, effort, risk, or confidence.

## Evidence ledger

Track each material fact in a ledger:

| Area | Claim or question | Status | Evidence source | Observed or accessed | Reliability | Gap or conflict |
| --- | --- | --- | --- | --- | --- | --- |

Use four statuses:

- `known`: direct, current evidence from the repository, a read-only runtime result, database metadata, or a primary source.
- `inferred`: multiple signals support the conclusion, but direct evidence is missing. State the inference.
- `reported`: a stakeholder supplied the fact. Name the role and date when available.
- `unknown`: evidence is absent, inaccessible, stale, or contradictory.

Never promote `inferred`, `reported`, or `unknown` to `known` in the final report.

## Safe inspection rules

Before running a command, decide whether it can start services, install packages, execute project hooks, warm caches, alter timestamps, create generated files, or contact a remote system. If so, skip it. State what evidence it would collect and put the step behind a later implementation or evidence-collection gate.

Safe operations, when already available and allowed by repository guidance, normally include:

- file reads and repository searches with `rg --files`, `rg`, `git status --short`, `git ls-files`, `sed`, and JSON or YAML readers;
- version output such as `php -v`, `composer --version`, database client `--version`, webserver `-v`, and container image declarations;
- Composer inspection that does not update state, such as reading `composer.json` and `composer.lock`, or using `composer show --locked` and `composer why-not` when the installed Composer behavior is known to be read-only;
- TYPO3 version and CLI listing commands that the user and project permit, provided the installed entry point does not create caches or bootstrap a writable environment;
- `SELECT` and metadata queries through an existing read-only account;
- read-only integrity checks and streaming inspection of a supplied SQL dump;
- official documentation and primary vendor research.

Do not start DDEV, Docker, a database, a webserver, or TYPO3 merely for inspection. Do not use `composer install`, `composer update`, `composer require`, `composer remove`, `composer dump-autoload`, TYPO3 cache commands, database analyzers, upgrade commands, schedulers, imports, or asset builds. Do not import, repair, normalize, extract, or rewrite a supplied dump.

## Installation classification

Classify from combined evidence, not a single file.

| Classification | Strong signals | Contradictory signals to resolve |
| --- | --- | --- |
| Composer-based | root `composer.json` requires `typo3/cms-*`; `composer.lock`; `vendor/`; `public/typo3`; local path repositories | copied legacy `typo3conf/ext`; stale lock file; manually installed extensions |
| Legacy non-Composer | core source tree in web root; `typo3_src` symlink or archive; `typo3conf/LocalConfiguration.php`; extensions under `typo3conf/ext`; no core Composer lock | extension-level Composer files; deployment scripts that assemble a Composer release elsewhere |
| Mixed | Composer-managed core plus manually copied extensions, legacy configuration, or non-Composer deployment steps | a partial conversion or stale files may only look mixed |

Record the web root, project root, local extension roots, file storage roots, configuration locations, and deployment artifact shape.

## Version baseline

Establish exact versions and cite the source for each:

- TYPO3 core and every installed system extension;
- PHP CLI, PHP-FPM or web runtime, Composer, and required PHP extensions;
- database product and server version, not only the client version;
- Apache, NGINX, Caddy, IIS, reverse proxy, search service, queue, cache, and image tooling when relevant;
- operating system, container images, DDEV or Docker configuration, orchestration, CI runners, hosting constraints, and deployment tooling;
- Node.js and frontend build tooling when templates or assets must be rebuilt.

Prefer lock files, immutable image tags or digests, runtime output, and database server results over README claims. Keep conflicting CLI and web-runtime versions visible.

## Extension and custom-code inventory

Inventory these categories separately:

1. TYPO3 system extensions.
2. Third-party extensions from Composer, TER, vendor archives, or copied source.
3. Custom domain extensions.
4. Site packages and theme packages.
5. Integrations, CLI commands, scheduler tasks, queues, imports, exports, webhooks, authentication, payment, search, DAM, CRM, ERP, and external APIs.

For each extension record:

| Extension | Type | Location | Current version | Declared TYPO3 range | Target evidence | Usage evidence | Custom schema/data | Action | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Use action values `maintain`, `upgrade`, `port`, `replace`, `retire`, or `unresolved`. A compatible Composer constraint is not proof that runtime behavior or stored data is compatible.

For target compatibility, inspect the installed or tagged source, Composer constraints, `ext_emconf.php`, TYPO3 and vendor changelogs, release notes, and the actual code paths used by the project. Record the source and access date. Mark compatibility `unverified` when those sources do not prove it. If an unverified extension owns important behavior or persisted data, require a representative proof of concept before making a final strategy recommendation.

Search custom code and configuration for:

- PHP, Extbase models and repositories, persistence mappings, dependency injection, CLI commands, middleware, backend modules, hooks, signals, PSR-14 events, XCLASS, eID, AJAX, and direct core API calls;
- TCA, FlexForms, custom render types, DataHandler integrations, `ext_tables.sql`, Doctrine queries, MM tables, and raw SQL;
- TypoScript, TSconfig, site configuration, site sets, routing, redirects, RealURL remnants, speaking URL fields, language configuration, and domain records;
- Fluid templates, layouts, partials, ViewHelpers, content elements, Content Blocks, RTE configuration, forms, mail templates, localization files, and translation workflows;
- FAL storage and processing configuration, file metadata, remote storage drivers, legacy `fileadmin` paths, and generated derivatives;
- workspaces, versioning, permissions, backend user workflows, scheduled tasks, integrations, consent, tracking, search, frontend assets, and build pipelines.

Report counts and hotspot density where useful, but inspect representative implementations. Line counts alone do not measure migration effort.

## Database and content profile

Prefer an existing read-only database connection. Verify read-only status when the platform exposes it. Never echo the password, DSN, environment file, or shell history. Do not use a privileged account merely because it is available.

Start with schema metadata and grouped counts. Adapt names to the database product and actual TYPO3 schema. Useful evidence includes:

- database product, server version, character set, collation, table engine, table sizes, and custom tables;
- row counts by table and grouped counts for `pages.doktype`, `tt_content.CType`, `tt_content.list_type`, language ids, hidden state, deletion state, and workspace or version state;
- counts for `sys_file`, `sys_file_metadata`, `sys_file_reference` grouped by referenced table and field, storage, missing references, and processing status;
- MM tables, parent-child relations, inline records, Extbase persistence tables, FlexForm usage, custom schemas, and orphan indicators;
- redirects, slugs, language overlays, translations without sources, pages without valid parents, and duplicate identity candidates;
- scheduler task types and state, form definitions or submissions by count only, and extension-owned records.

Use exact counts where practical. Database optimizer estimates may be labeled approximate. Group small or sensitive categories when disclosure could identify a person. Do not select content bodies, emails, usernames, form submissions, addresses, tokens, filenames, or individual URLs into the report.

Every proposed migration mechanism must account for TYPO3 invariants, including:

- stable identifier mapping and foreign keys;
- `pid`, sorting, enable fields, deletion, timestamps, creator fields, and permissions;
- localization source pointers and translation state;
- workspace and version records;
- MM and inline relations;
- FAL file identifiers, storage identifiers, metadata, references, ordering, and file availability;
- slugs, route enhancers, redirects, canonical URLs, hreflang, SEO fields, and legacy URL maps;
- TCA transformations, DataHandler side effects, extension-specific upgrade logic, reference index, and cache invalidation.

Direct SQL may be a controlled implementation component, but raw row insertion is never presumed safe. The strategy report must price mapping, transformations, invariant checks, reconciliation, trial runs, and rollback.

## SQL-dump fallback

Use a supplied SQL dump only when no read-only database connection is available. Treat it as a valid database backup and a local analysis input. It does not cover FAL files or other file storage.

Do not import or execute the dump. Check its size, checksum, compression integrity, source database product, declared version, creation metadata, schema coverage, and table list without changing it. Stream compressed content when supported. Keep improvised parsing in memory or pipelines and create no parser scripts, extracted copies, indexes, caches, or temporary project files.

Database dump formats vary. Detect the product and format before parsing. A best-effort parser must report:

- supported and unsupported statements or archive constructs;
- tables and byte ranges inspected;
- whether counts are exact, approximate, or unavailable;
- syntax errors, skipped sections, and truncation;
- findings that remain provisional because coverage is incomplete.

Never present a partial parse as a complete database profile. When the dump cannot provide decision-critical aggregates, ask for a read-only connection or user-generated aggregate evidence.

Treat a user's statement that the dump contains no personal data as `reported`. Inspect individual fields only when they affect the strategy. Keep credentials, tokens, backend-user secrets, and unnecessary content out of outputs.

## Operations and acceptance inventory

Record:

- automated tests by layer, last known result, coverage relevance, fixtures, and production-like test data availability;
- deployment pipeline, environment parity, configuration and secret handling, asset builds, observability, and release ownership;
- database and file backups as separate artifacts, retention, off-site copies, encryption, restore evidence, restore duration, and point-in-time recovery;
- rollback units for code, database, files, queues, search indexes, and external integrations;
- allowed downtime, content freeze, delta migration, dual-run needs, DNS or proxy cutover, and rollback decision time;
- canonical URL, redirect, hreflang, sitemap, metadata, analytics, consent, search, performance, and accessibility acceptance;
- editorial workflows, permissions, workspaces, training, UAT participants, sign-off criteria, and legal retention requirements.

A supplied SQL dump remains a valid database backup even when no restore test is documented. Record restore confidence separately and do not infer a restore result. A green unit-test suite without content, routing, and editorial tests is weak migration evidence.

## Missing-input priority

Rank gaps by decision impact:

- `decision-blocking`: the recommendation could reverse without it;
- `range-widening`: the likely strategy is stable, but effort or risk remains broad;
- `implementation-only`: needed after strategy approval, not for the current decision.

For each gap, state the read-only collection method, owner, expected artifact, and which score or estimate it could change.
