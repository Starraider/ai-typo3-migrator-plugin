# Legacy TYPO3 v8 assessment

Load this reference for TYPO3 v8, non-Composer installations, mixed installations with legacy artifacts, or projects whose exact source state is uncertain.

## Establish the real source state

Do not trust a directory name such as `typo3_src-8.7` by itself. Corroborate the exact core patch version, PHP runtime, database server, webserver, symlink target, loaded extensions, and active configuration through read-only evidence.

Inspect when present:

- `typo3_src` links or copied core directories, `index.php`, `typo3/`, and vendor state;
- `typo3conf/LocalConfiguration.php`, `AdditionalConfiguration.php`, `PackageStates.php`, `extTables.php`, `ext/`, and environment-specific includes;
- `typo3conf/ext/*/ext_emconf.php`, `ext_localconf.php`, `ext_tables.php`, `ext_tables.sql`, TCA, TypoScript, Fluid, language files, and vendor libraries;
- TER keys, manually patched extensions, archived vendor packages, forks, XCLASS registrations, hooks, signals, eID scripts, scheduler tasks, and custom CLI entry points;
- `uploads/`, `fileadmin/`, FAL storage configuration, processed files, and any pre-FAL path conventions;
- RealURL or other routing configuration, domain records, redirects, URL caches, and custom slug fields;
- deployment scripts, cron, webserver rewrite rules, filesystem permissions, and undocumented server-side patches.

Label artifacts as active, probably active, historical, or unknown. Old files often survive after a partial conversion.

## Compatibility-chain questions

A sequential path from v8 to a much newer target crosses several platform, API, persistence, and packaging transitions. Verify the supported major-by-major route to the user-specified target in current or archived official TYPO3 documentation. Do not assume that skipping a major is supported or that every historical package release remains installable.

For each intermediate major, assess:

- a mutually compatible PHP, database, Composer, webserver, and operating environment;
- the latest supported patch state required before the next step;
- availability of historical extension versions and their release archives;
- core and extension upgrade wizards or one-time data transformations;
- removed hooks, APIs, Extbase behavior, TCA forms, TypoScript parsers, Fluid versions, RTE changes, routing, FAL, workspaces, and database abstraction changes;
- whether custom code can be staged while both the current and next major still run;
- whether the team can reproduce and retain every intermediate environment and rollback point.

Treat the absence of v8-to-v11 execution Skills in this package as an ownership gap, not proof that sequential upgrades are impossible. The strategy report may describe phases, but it must not improvise detailed execution commands for those majors.

## Extension archaeology

For every legacy extension, determine:

- exact installed source and local modifications;
- TER or vendor identity and last maintained release;
- owned tables, fields, file paths, scheduled tasks, routes, plugins, content types, and business workflows;
- whether records still exist and whether frontend or backend usage can be demonstrated;
- a target-version replacement, a custom port, a controlled retirement, or an unresolved dependency;
- required content and relation transformations if the implementation changes.

An abandoned extension with no live records is different from an abandoned extension that owns a critical domain table. Price discovery before porting or replacement.

## Legacy persistence and migration traps

Investigate before proposing row transfer:

- FAL adoption state, duplicate files, missing files, storage ids, reference ordering, processed files, metadata, and old path fields;
- `pages_language_overlay` and historical localization models, source pointers, free or connected translation modes, and orphan overlays;
- workspaces, `pages` and content version records, deleted history, hidden content, start and end times, permissions, and backend user ownership;
- `tt_content` CTypes, `list_type` plugins, FlexForms, IRRE, MM tables, comma-separated uid fields, custom soft references, and extension-specific serialized or XML data;
- RealURL caches, path segments, redirects, domain records, canonical URLs, and inbound-link evidence;
- custom tables without TCA, TCA without schema, database fields absent from code, inconsistent collations, zero dates, invalid encodings, and MyISAM tables;
- direct SQL assumptions that bypass DataHandler, reference index, slugs, permissions, localization, FAL, workspace, and cache behavior.

Use metadata and aggregate anomaly counts. Do not expose record bodies or personal data.

## Strategy implications

Legacy evidence changes the three paths in different ways:

- Sequential upgrades may preserve official data transformations and behavior incrementally, but historical environments, abandoned extensions, and repeated validation can dominate labor.
- A clean rebuild removes obsolete application structure, but content and relation migration becomes a software project with its own mappings, invariants, delta plan, reconciliation, and rollback.
- A hybrid can preserve selected domain data or staged transformations while replacing templates and obsolete extensions, but it needs explicit ownership boundaries and identifier maps.

Do not award or penalize a strategy merely because the source is old. Score the evidenced migration mechanisms, data complexity, behavior ownership, testability, and operations.

## Minimum proof-of-concept candidates

When evidence remains weak, choose the smallest gate that tests the decisive uncertainty, for example:

- boot one isolated copy at the exact source patch level and inventory active packages without changing source data;
- migrate a representative multilingual page tree with nested content, FAL, redirects, and custom relations into a disposable installation of the specified target;
- port the highest-risk custom extension far enough to test its schema, core APIs, and business behavior;
- prove one sequential intermediate step on a disposable clone and measure extension, wizard, and validation fallout;
- reconstruct one representative page family and editorial workflow to measure rebuild effort.

The analysis may specify this gate. Running it requires a separate, write-authorized implementation process and a disposable environment.
