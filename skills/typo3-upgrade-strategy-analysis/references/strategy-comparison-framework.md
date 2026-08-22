# Strategy comparison framework

Compare all three strategies against the same evidence. Do not let a weighted total hide a disqualifier, evidence gap, or risk concentration.

## Strategy definitions

### Sequential major-version upgrades

Stabilize the specified source release, then move through every supported intermediate TYPO3 major required to reach the specified target. Preserve the working system and data model through version-specific transformations. Treat the existing v11-to-v12, v12-to-v13, and v13-to-v14 Skills as possible downstream execution aids only when the chosen path includes those transitions.

### Clean target-version rebuild

Create a new application on the specified target version and deliberately reimplement required configuration, extensions, templates, and integrations. Migrate selected content, files, metadata, identities, relations, URLs, and operational state through a controlled, tested migration process. "Clean" describes the target application, not a license to discard data invariants.

### Hybrid strategy

Define explicit domains that keep their data lineage or upgrade path and domains that are rebuilt or replaced. Typical examples include migrating content and FAL with controlled transformations while rebuilding the site package and frontend, or sequentially upgrading custom domain extensions while replacing abandoned presentation extensions. A hybrid without named boundaries is not a strategy.

## Default criteria and weights

Use these defaults unless explicit business constraints justify a change. Derive adjustments before rating, show and freeze the weights, and keep their sum at 100. Ask for confirmation only when priorities conflict or an adjustment could change the winner.

| Criterion | Default weight | What the rating must address |
| --- | ---: | --- |
| Technical feasibility | 16 | Viable platform and dependency chain, available migration mechanisms, skills, and blockers |
| Estimated engineering labor | 12 | Relative labor and coordination burden; a higher rating means less expected labor |
| Extension replacement and custom-code work | 12 | Porting, replacement, data ownership, vendor support, and abandoned components |
| Content and relation integrity | 14 | Records, localization, workspaces, MM and inline relations, custom schemas, files, and reconciliation |
| Template and frontend reconstruction | 8 | Fluid, TypoScript, content elements, forms, assets, accessibility, and design parity |
| URL, redirect, language, FAL, SEO, and metadata preservation | 12 | Identity maps, canonical URLs, redirects, hreflang, metadata, and file continuity |
| Testability and defect-detection cost | 8 | Isolation, representative fixtures, automated checks, observability, and reconciliation |
| Downtime and rollout complexity | 6 | Freeze, delta migration, cutover, dual running, external coordination, and editorial interruption |
| Rollback quality | 6 | Reversibility of code, data, files, traffic, integrations, and elapsed rollback time |
| Long-term maintainability | 6 | Supported architecture, reduced legacy burden, ownership, deployment fitness, and future upgrades |

Weight changes are appropriate when the user supplies explicit priorities, such as a near-zero downtime requirement, regulatory data-integrity needs, a fixed redesign, or a hard support deadline. Do not lower a safety-critical criterion merely to make a preferred strategy win.

## Rating scale

Rate each criterion from 1 to 5 and attach evidence:

| Rating | Meaning |
| ---: | --- |
| 1 | Infeasible or unacceptable without a major unresolved breakthrough |
| 2 | Feasible only with large unresolved risk, effort, or weak controls |
| 3 | Feasible with material work and manageable but significant uncertainty |
| 4 | Good fit with understood work, evidence, and controls |
| 5 | Strong fit with direct evidence, low residual uncertainty, and verified controls |

Use `unrated` when decision-blocking evidence is missing. Do not replace `unrated` with a neutral 3. Do not publish a single total while a decision-blocking criterion is unrated. Show a range based on defensible low and high ratings and name the evidence that could move it.

For rated criteria, calculate the contribution as `weight × rating / 5`. Show the contribution beside the rating. The maximum total is 100. A total without criterion rows, evidence, and interpretation is invalid.

## Disqualifying conditions

A disqualifier overrides the weighted total until resolved. Mark it as confirmed, probable, possible, or cleared.

Common sequential disqualifiers include:

- no supportable or isolatable runtime for a required intermediate version;
- an extension or custom data owner that cannot be upgraded, replaced, or safely removed at an intermediate step;
- required source state is corrupt or too incomplete for official upgrade mechanisms;
- the number of intermediate transformations cannot fit a hard business or security deadline.

Common clean-rebuild disqualifiers include:

- no credible mapping and reconciliation method for critical content, relations, localization, workspaces, files, identities, or URLs;
- business behavior exists only in undocumented custom code or data and cannot be specified or accepted;
- freeze, delta migration, or cutover constraints make controlled transfer infeasible;
- legal or audit requirements demand lineage that the proposed process cannot prove.

Common hybrid disqualifiers include:

- domain boundaries, owners, identifiers, and synchronization rules cannot be made explicit;
- the plan requires prolonged dual writes without a proven consistency mechanism;
- cross-domain relations make independent migration or rollback untestable;
- the organization cannot own two migration methods and their integration risk.

Do not invent a disqualifier because a path feels awkward. Cite the constraint and the evidence.

## Comparison procedure

1. Write one project-specific sentence defining what each strategy preserves, replaces, and migrates.
2. List hard constraints and disqualifiers before scoring.
3. Set, disclose, and freeze weights before assigning ratings. Explain every deviation from the defaults.
4. Rate each criterion with cited evidence and an explicit confidence level.
5. Calculate transparent contributions and total ranges where evidence is incomplete.
6. Compare labor ranges separately. Do not let the labor score replace the workstream estimate.
7. Run sensitivity checks. Vary every uncertain rating by its credible range and increase the two most important adjustable weights. Record whether the winner changes.
8. Identify risk concentration. A strategy with a high total can still be poor when one critical criterion is rated 1 or 2.
9. State why the recommended strategy wins and why each alternative loses in this project.

## Recommendation rules

Recommend a strategy for human decision when:

- it has no unresolved disqualifier;
- its advantage survives credible sensitivity checks, or a lower score is justified by a documented hard constraint;
- its labor and operational assumptions are plausible;
- its validation and rollback model covers the project's critical data and behavior;
- the evidence confidence is sufficient for the decision's cost.

The recommendation does not approve implementation. Name the human decision owner and leave the decision status pending in the report.

Recommend a proof-of-concept gate when a missing fact or technical hypothesis could reverse the result. Define:

- the exact hypothesis;
- the smallest representative code and data slice;
- read-only analysis inputs and any later separately authorized test environment;
- pass, fail, and inconclusive thresholds;
- timebox and responsible role;
- artifacts to retain;
- which strategy decision follows from each result.

Do not call ordinary discovery a proof of concept. A useful gate tests the risky mechanism or assumption.

## Matrix format

| Criterion | Weight | Sequential rating and evidence | Clean rebuild rating and evidence | Hybrid rating and evidence |
| --- | ---: | --- | --- | --- |

Follow the matrix with:

- weighted totals or ranges;
- disqualifiers by strategy;
- sensitivity results;
- confidence by strategy;
- decisive evidence and gaps;
- explicit rejection reasons.
