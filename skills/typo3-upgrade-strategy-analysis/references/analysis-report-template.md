# Analysis report template

Use this structure for the final strategy report. Keep facts, inferences, reported claims, assumptions, and unknowns distinct. Remove instructional text when filling it, but retain every required section.

```markdown
# TYPO3 upgrade strategy analysis: <source> to <target>

Analysis date:
Repository or project scope:
Source TYPO3 version:
Target TYPO3 version and release status:
Report path:
Analysis boundary: Technical inspection was read-only. This report is the only file written.

## Executive recommendation

- Favored strategy for human decision:
- Why this path fits the evidence:
- Decisive constraints:
- Estimated implementation range and confidence:
- Relationship to the 48-hour historical calibration:
- Decision conditions or expiry date:

## Decision record

| Field | Value |
| --- | --- |
| Recommended strategy | |
| Decision owner | |
| Status | pending |
| Decision date | |
| Accepted deviations | |
| Approval evidence | |

The report recommends. A human updates the decision record in a separate action.

## Project baseline and evidence inventory

### Installation and platform

| Item | Observed version or state | Evidence | Evidence class | Observed date | Confidence or conflict |
| --- | --- | --- | --- | --- | --- |

State whether the installation is Composer-based, legacy, or mixed and explain the evidence.

### Evidence availability

| Evidence category | Available evidence | Missing input | Decision impact | Collection method |
| --- | --- | --- | --- | --- |

### Database or dump coverage

| Item | Result | Exact, approximate, or unavailable | Limitation |
| --- | --- | --- | --- |

When a dump was used, record its database product, format, checksum or integrity result, tables and byte ranges inspected, supported and unsupported constructs, errors, skipped sections, and provisional findings. Record the dump as a database backup, not a file-storage backup.

## Extension and custom-code compatibility matrix

| Extension or area | Type | Current state | Target evidence | Owned code or data | Proposed action | Effort driver | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |

Cover TYPO3 system extensions, third-party extensions, custom extensions, site packages, PHP and Extbase, hooks or events, TCA, TypoScript, Fluid, localization, routing, forms, workspaces, FAL, assets, scheduled tasks, integrations, APIs, and custom tables.

## Findings

### Content, database, and files

Report metadata, aggregate counts, relation and localization complexity, FAL, workspaces, hidden and deleted records, custom schemas, anomaly counts, and unknowns. Keep credentials, secrets, and unnecessary record content out of the report.

### Templates, frontend, URLs, and SEO

Report template families, content elements, assets, forms, routes, redirects, languages, canonical and hreflang needs, accessibility, and reconstruction scope.

### Integrations and scheduled work

Report each external API, import or export, queue, CLI command, scheduled task, authentication flow, search service, and operational owner.

### Infrastructure, testing, deployment, and recovery

Report environment versions, parity, automation, test relevance, observability, database backup, file backup, downtime, freeze and delta constraints, acceptance ownership, and rollback quality.

## Strategy comparison matrix

Weight rationale and changes from defaults:
Frozen before rating: yes or no

| Criterion | Weight | Sequential rating, contribution, evidence | Clean target rebuild rating, contribution, evidence | Hybrid rating, contribution, evidence |
| --- | ---: | --- | --- | --- |

### Totals, disqualifiers, and sensitivity

- Sequential total or range, disqualifiers, and confidence:
- Clean target rebuild total or range, disqualifiers, and confidence:
- Hybrid total or range, disqualifiers, and confidence:
- Unrated decision-blocking criteria:
- Sensitivity result:
- Risk concentrations hidden by totals:

Do not publish a single total while a decision-blocking criterion is unrated.

## Labor estimate by strategy and workstream

Unit and team assumptions:
Scope and exclusions:
Historical calibration: complete migrations normally remain within 48 person-hours

| Workstream | Sequential hours | Clean rebuild hours | Hybrid hours | Evidence and uncertainty |
| --- | ---: | ---: | ---: | --- |
| Discovery and proof of concept | | | | |
| Platform and intermediate environments | | | | |
| TYPO3 core and system extensions | | | | |
| Third-party extensions | | | | |
| Custom PHP and Extbase | | | | |
| Templates, configuration, and frontend | | | | |
| Content, files, and database migration | | | | |
| Integrations and scheduled work | | | | |
| Verification and acceptance | | | | |
| Deployment, cutover, and rollback | | | | |
| Coordination and documentation | | | | |
| Base subtotal | | | | |
| Uncertainty allowance | | | | |
| Total person-hour range | | | | |

Use ranges with one-hour endpoints. Explain any total above the 48-hour calibration. These estimates support planning and are not contractual quotes.

## Risks, assumptions, confidence, and missing evidence

| Risk or assumption | Strategy affected | Evidence | Probability or uncertainty | Impact | Mitigation or decision gate |
| --- | --- | --- | --- | --- | --- |

### Missing evidence by priority

- Decision-blocking:
- Range-widening:
- Implementation-only:

## Recommended proof of concept

Use this section when evidence or a technical hypothesis could reverse the recommendation. Otherwise state why a proof of concept is not required for strategy selection.

- Hypothesis:
- Representative code and data slice:
- Timebox and owner:
- Required disposable environment and separate authorization:
- Pass threshold:
- Fail threshold:
- Inconclusive result:
- Evidence retained:
- Decision unlocked:

## Phased implementation plan

This plan is advisory. It does not authorize execution.

| Phase | Objective | Main workstreams | Entry evidence | Validation gate | Rollback gate | Exit decision |
| --- | --- | --- | --- | --- | --- | --- |

Include discovery closure, proof of concept when required, target architecture, extension and code work, content and file migration development, trial migrations, validation, editorial acceptance, cutover rehearsal, production cutover, and post-cutover monitoring as applicable. Refer to available downstream version-specific Skills without copying their commands. Mark uncovered transitions that need separate execution guidance.

## Reasons for rejecting the other strategies

### Sequential upgrades

State project-specific reasons, disqualifiers, and evidence. Project age alone is not a rejection reason.

### Clean target-version rebuild

State project-specific reasons, disqualifiers, and evidence. Installing a fresh target is only one part of a rebuild.

### Hybrid strategy

State project-specific reasons, disqualifiers, and evidence. Define why domain boundaries do or do not work.

## Source list

| Source | Owner | Version or publication | URL or repository path | Accessed | Supports | Limitations |
| --- | --- | --- | --- | --- | --- | --- |

Use current or archived official TYPO3 sources and primary extension-vendor material for time-sensitive claims. Record access dates as `YYYY-MM-DD`.

## Validation status

### Passed

### Failed

### Blocked

### Unavailable or not run

Do not imply that a blocked, unavailable, or unrun check passed.
```
