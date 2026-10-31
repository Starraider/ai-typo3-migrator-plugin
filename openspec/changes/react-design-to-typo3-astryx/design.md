# Design

## Context

See [proposal.md](proposal.md) for motivation and the three delta specifications under `specs/` for behavior contracts.

This repository distributes portable Agent Skills from immediate child directories of `skills/`. Existing skills combine runtime instructions, detailed READMEs, focused references, optional templates, and evaluation prompts. `plugin.json` has descriptive metadata and automatic skill discovery, not an explicit skill registry. No MCP server is bundled. The existing Tailwind migration skill offers relevant visual-verification concepts, but its styling stack and sibling-skill dependencies are not suitable runtime dependencies for these new skills.

There is no supplied mockup, runnable source site, target TYPO3 installation, or application browser baseline in this repository. Implementation of this change produces skills and small evaluation fixtures. Running a real website migration is subsequent consumer work.

### Inspected upstream evidence

The exploration inspected these upstream revisions on 2026-10-31. They are research anchors, not a requirement to install development branches. Each skill must inspect the consumer's actual installed versions and refresh compatibility evidence where necessary.

| Source | Observed contract | Design consequence |
| --- | --- | --- |
| [StyleX Connector requirements](https://github.com/Starraider/stylex-connector/blob/1958ebcfd52a42fd01778ec4f72db1c2607e901a/composer.json) | `skom/stylex-connector`; TYPO3 `^12.4 || ^13.4 || ^14.3`; package metadata version 1.1.2 | Use the existing connector; its broader compatibility does not establish Astryx compatibility. |
| [Astryx requirements](https://github.com/Starraider/typo3-astryx/blob/29330194828ffa3800663fd01a1694a9c92272ba/composer.json) | TYPO3 `~14.3.0`, PHP `>=8.3 <8.5`, Content Blocks `^2.4.10`, Container `^4.1`, connector `^1.1.2`, Vite Asset Collector `^1.18`; conflicts with Fluid Styled Content | Initial target is TYPO3 14.3.x. Detect conflicts before installation or activation; never make a rendering-stack migration an implicit prerequisite action. |
| [Connector Vite guide](https://github.com/Starraider/stylex-connector/blob/1958ebcfd52a42fd01778ec4f72db1c2607e901a/Documentation/Installation/Vite.rst) | Maintained manifest adapter, separate asset and StyleX manifests, v2 CSS hashes, static style support and dynamic-function limitations | Reuse its build adapter, preserve supported style composition, and verify matching build artifacts. |
| [Astryx token source](https://github.com/Starraider/typo3-astryx/blob/29330194828ffa3800663fd01a1694a9c92272ba/Resources/Private/JavaScript/Stylex/tokens.stylex.js) and [styling guide](https://github.com/Starraider/typo3-astryx/blob/29330194828ffa3800663fd01a1694a9c92272ba/Documentation/Styling/Index.rst) | Stable public CSS properties, theme scopes, ordered layers including `product`; some documented token names and values differ from source | Map installed declarations, retain provenance, and validate computed styles rather than copying examples as authoritative syntax. |
| [Astryx configuration guide](https://github.com/Starraider/typo3-astryx/blob/29330194828ffa3800663fd01a1694a9c92272ba/Documentation/Configuration/Index.rst) | Site settings, page-view paths, component-collection overrides, partial/layout roots, and consuming-project Vite mode | Choose the applicable installed extension point; a partial/layout override is not evidence that arbitrary frontend-template replacement is supported. |
| [Card definition](https://github.com/Starraider/typo3-astryx/blob/29330194828ffa3800663fd01a1694a9c92272ba/ContentBlocks/ContentElements/card/config.yaml), [Card component](https://github.com/Starraider/typo3-astryx/blob/29330194828ffa3800663fd01a1694a9c92272ba/Resources/Private/Components/Card.html), and [recipe ViewHelper](https://github.com/Starraider/typo3-astryx/blob/29330194828ffa3800663fd01a1694a9c92272ba/Classes/ViewHelpers/RecipeViewHelper.php) | Content fields and component arguments/slots are different interfaces; recipe dimensions are hard-coded in a final class | Compare editorial and rendering capabilities separately. Do not assume a new recipe option can be registered from a site package. |

## Goals / Non-Goals

**Goals:**

- Make each skill usable in a fresh session or as a standalone installation through explicit, validated handoffs.
- Separate evidence collection, editorial modeling, and implementation so uncertainty remains visible at each boundary.
- Use site-package-owned branding and component adaptations through the installed extensions, preserving upgradeability.
- Turn visual fidelity into a recorded, repeatable comparison of the reference and target, including responsive transitions and functional states.
- Keep deterministic validation useful locally and in CI without making an MCP host or a particular agent client necessary.

**Non-Goals:**

- Build a general React-to-Fluid transpiler, infer unseen behavior from screenshots, or claim browser-independent pixel identity.
- Bundle a React runtime into the target by default or replace the selected extensions with another styling or component stack.
- Backport Astryx to TYPO3 13, change upstream repositories, migrate an existing FSC website automatically, or run production deployment.
- Introduce a full extraction service, remote asset catalogue, or custom MCP server in this change.

## Decisions

### 1. Package three self-contained skills

Create `skills/typo3-design-system-extract/`, `skills/typo3-component-analyze/`, and `skills/typo3-component-build/`. Each owns a portable `SKILL.md`, detailed `README.md`, directly linked references/templates, and `evals/evals.json`. Add small deterministic validation helpers and contract fixtures where they prevent malformed or stale handoffs. Do not create unused directories or copy a complete frontend toolchain into a skill.

Each README explains prerequisites, outputs, side effects, standalone use, related skills, validation, licensing, and at least three realistic prompts. Plugin-level documentation adds concise links and accurate descriptions. Retain the package's CC-BY-4.0 skill licensing; upstream extensions remain separately licensed. No release/version bump or publishing is implied.

**Alternative considered:** one orchestration skill with three modes. Separate skills match the user's explicit workflow and allow repeated analysis/building of individual components after a single foundation extraction.

Shared handoff documentation has one authoring contract, but each distributed skill contains the resources it needs. Check shared contract copies for drift during validation; do not create runtime references into sibling skill directories.

### 2. Use explicit, versioned migration bundles

Use a migration bundle at a resolved consumer-project destination. A proposed default is `design-migration/<design-id>/` in that project, unless its conventions specify another location. The future skill resolves and reports the path before writing, rejects escaping symlinks, respects existing edits, and reuses a supplied bundle rather than inventing session-only state. Analysis can target another explicitly authorized destination when no TYPO3 project exists.

The bundle contains:

| Artifact | Owner | Purpose |
| --- | --- | --- |
| `design-system.json` and `design-system.md` | Extract skill | Global inventory, source evidence, token mappings, assets, target compatibility, and foundation verification |
| `components/<component-id>/component-spec.json` and `component-spec.md` | Analyze skill | Whole-component visual design, structure, variants, content model, target placement, behavior, assets, reference captures, and unresolved requirements |
| `components/<component-id>/build-report.json` and `build-report.md` | Build skill | Global design coverage, candidate assessment, implementation disposition, changes, executed checks, differences, and completion status |
| `references/` and `components/<component-id>/references/` | Relevant skill | Authorized captures and supporting evidence referenced by the handoffs |

The runtime filenames and schema are part of the handoff contract, not files to generate in this plugin during planning.

Common JSON envelope fields are `schemaVersion` (initially `1.0.0`), `artifactType`, `artifactId`, `revision`, `sources`, `dependencies`, `target`, `evidence`, `verification`, `decisions`, and `unresolved`. `decisions` records each decision gate (question, options, answer, date, applicability); decisions that change binding requirements or accept deviations enter the revision, run-only ones do not, and answered decisions are reused across sessions until their binding requirements change. Sources record kind, locator, relevant file/selector/screen identity, and revision or digest when obtainable; unavailable identity is explicit. Dependencies record referenced artifact identity, schema version, and revision. Target evidence records exact installed versions when known, not just the intended target range.

Compute `revision` from stable, canonical payload data and dependency identities, excluding the revision field, timestamps, and run-only metadata. A changed source revision, mapping, or required asset invalidates dependent claims. Unknown source identity cannot establish freshness. Reject unsupported schema major versions and missing required fields; report outdated dependencies before implementation. Never silently relabel an old handoff as current.

Verification entries use `passed`, `failed`, `not-run`, or `not-applicable` with evidence and reasons. Artifact readiness separately uses `ready`, `incomplete`, or `blocked`; neither code generation nor one successful command proves overall parity. Avoid a single unqualified success flag.

**Alternative considered:** Markdown-only handoffs. They are easy to read but weak for automated freshness checks, required-field validation, and CI. Pair JSON with a readable report; do not require another service to interpret it.

### 3. Extract facts before deriving a token system

The extract skill inspects supplied React/TSX, stylesheets, CSS variables, Tailwind configuration where present, package/lock files, font declarations, assets, and a running reference when available. Stitch input can be an existing React export, retrieved HTML and screenshots, or local export files; source format must be detected rather than assumed.

Maintain an evidence ledger: observed source value, rendered value when measured, source location, semantic role, target mapping, scope, and confidence class (`observed`, `inferred`, or `unknown`). Record primitive tokens separately from semantic aliases and component-specific values. Preserve units, fluid formulas, and responsive changes. Consolidate duplicates only when semantics and fidelity permit it.

Do not invent mobile layouts, brand palettes, missing fonts, or dark-mode counterparts from a single reference. Source-only or screenshot-only extraction can be useful, but its limitations prevent a claim of verified rendered integration.

**Alternative considered:** automatically normalize every mockup into Astryx's default scale. This would reduce token count but can change spacing, typography, and layout. Keep exact observed exceptions when needed.

### 4. Map the site package onto Astryx's public tokens

Use installed `tokens.stylex.*`, theme sources, CSS selectors, and computed values to establish actual names and scopes. Source evidence takes precedence over stale examples. The mapping records source token/value, semantic purpose, target public property, conversion if any, active selector/theme/mode, and unresolved conflicts.

Author extracted project tokens in the site package as StyleX definitions with a project namespace such as `--brand-*`. Reuse suitable existing Astryx tokens in component styles; map the public `--astryx-*` properties to project values through the supported branding layer. Avoid declaring the same globally named token through independent competing `defineVars` sources. If token alias generation requires a small CSS bridge, derive it from the mapping so it cannot become a second manually maintained source of design values.

Respect Astryx's layer order. Emit branding overrides at the actual scope where the active theme declares values: a declaration on `:root` cannot override a child element's own declaration merely through layer priority. Verify nested themes, page inheritance, and mode selection with computed-style checks. A new theme name requires a verified registration/selection path; adding a selector alone does not establish that the backend can select it.

Keep breakpoint/query values as compile-time constants supported by the selected compiler. Do not put CSS custom properties into media-query conditions. Include applicable base typography, global element styles, reset adjustments, font loading, and editor/preview token delivery; token declarations alone do not reproduce a site's base design.

**Alternatives considered:** editing Astryx's default token files or replacing its theme system. Both couple a project's branding to dependency internals. Use supported site-package ownership and report gaps that genuinely require upstream work.

### 5. Reuse the connector's build and delivery contracts

Inspect the consumer's existing package manager, lockfiles, Vite configuration, DDEV/environment instructions, entrypoints, asset collector, and Astryx asset mode before adding anything. Use the existing StyleX unplugin and maintained connector adapter where compatible. Keep all referenced style modules reachable from actual build entrypoints and use package-qualified stable keys without basename collisions.

Distinguish the Vite asset manifest, which resolves emitted files, from the StyleX manifest, which resolves semantic style keys. Preserve the v2 manifest/CSS integrity checks supported by the installed connector. Build and deploy matching artifacts as one release unit; JSON's atomic write does not make separate CSS publication atomic. Verify development stylesheet loading as well as production CSS because TYPO3 owns the HTML document.

Astryx has packaged assets and a consuming-project Vite mode. Select the existing intended mode, record it, and avoid loading the same stylesheet twice. Follow its layered build rather than blindly copying connector examples designed for unlayered legacy CSS.

The class ViewHelper's verified interface uses `styles:`. It supports static conflict maps and complete class recipes, not arbitrary runtime class-plus-variable style functions. Do not concatenate independently completed recipes expecting conflict resolution. Select one complete recipe per slot or compose supported static maps. Use a site-package-owned adapter only for a specifically evidenced dynamic-value need, with that need visible in the component specification.

**Alternative considered:** a new bridge or hard-coded generated class names in Fluid. The existing connector already supplies semantic lookup and validation, while hard-coded hashes would break on rebuilds.

### 6. Analyze component intent separately from target selection

The analyze skill is read-only with respect to source and target application code. Its writes are its analysis handoff and authorized reference captures. It describes the full component design from component-specific evidence: frame, composition, surface, typography, spacing, important parts, and visual states. It does not map this design to global tokens; the build skill records that coverage during implementation. It maps React props and rendered states into semantic parts, editable content, derived data, static presentation, and interaction state. React's internal props do not automatically become backend fields.

Record content cardinality and defaults, image roles/crops, links, language requirements when known, heading semantics, and optional/long content. Specify layout transitions and state behavior as rules, including viewport and container conditions where applicable. Keep observed source behavior distinct from accessibility improvements or design changes requiring a decision.

Classify target placement before proposing fields: content element, nested container, reusable native component, or page-layout part. Primary navigation can use the page tree and existing page layout; a full-width editorial section can use an Astryx container. Optional Astryx candidate notes are advisory. The build skill owns the definitive installed-version assessment and selected adaptation.

**Alternative considered:** combine analysis with immediate element generation. That makes it too easy to fit the specification to the first available element and obscures missing source behavior.

### 7. Require a reuse decision before component implementation

Build a candidate matrix from the installed extension, not just a README inventory. For each candidate record its definition/component path, persisted fields and relations, slot/argument API, variants, responsive rules, client behavior, styling keys, assets, tests, fit evidence, gaps, and proposed disposition. For the selected target, trace the active inherited style chain, distinguish it from globally available-but-unapplied tokens, and record exact local component tokens needed for any remaining design requirements.

Use this selection order while preserving the component contract:

1. Configure an existing content element and theme its values.
2. Compose existing content elements, containers, and native Fluid components.
3. Extend through a verified site-package template/component/data/style mechanism.
4. Implement a new site-package Content Block or component when the assessment justifies it.

For every option, record rejected alternatives and why. Do not count superficial visual similarity as reuse. A component can support a slot that its editorial Content Block does not expose; backend field coverage and frontend extensibility must both be checked.

The current recipe ViewHelper has a fixed allowlist. Do not invent a dynamic registration API, subclass its final class, or add unsupported options that silently fall back to defaults. Where necessary, consume site-package style keys through the connector in a site-package-owned component/override. If a clean adaptation is unavailable, report the upstream gap and its consequences. Changing upstream source is a separately scoped task, not a hidden part of this change.

Use local extension ownership, native TYPO3 fields/FAL for editorial content, shared components for shared rendering, and block-owned styles for a single block. Preserve existing identifiers and relations when extending types. Never write into Composer-managed dependencies as a project customization.

**Alternative considered:** always generate a new block from JSX. That duplicates Astryx's field models, interaction code, and maintenance burden. Reuse remains a means to fidelity; requirements must not be weakened to force reuse.

### 8. Make asset handling explicit

The manifest records source locator or local path, checksum when obtainable, media type/dimensions, intended usage, available rights evidence, ownership, target destination, and missing status. Keep expiring download URLs out of reproducibility claims; record provider identity and content digest where available. Do not expose signed credentials in reports.

Fixed logos, icons, fonts, and decorative assets belong to the site package when rights and files permit. Editor-selected media belongs to TYPO3 FAL, with crop/aspect-ratio and alternate-text requirements represented in the specification. Unknown rights, inaccessible images, unavailable icon libraries, and missing font weights remain explicit dependencies. A placeholder never counts as a matching required asset.

**Alternative considered:** add a remote asset service initially. A local manifest suffices for the first workflow and is easier to version with the design evidence. Shared storage can be added later without changing the skill boundaries.

### 9. Verify fidelity with stable reference conditions

At the foundation stage, check representative type, colors, containers, theme scopes, and asset loading. At the component stage, create a comparison matrix covering selected variants/states, mobile/tablet/desktop widths derived from the source, and checks immediately around actual layout transitions. Include supported browsers from the target's requirements rather than assuming a universal browser matrix.

Use identical content, assets, loaded fonts, device scale, browser version, viewport, mode, interaction state, and animation/time controls where relevant. Store those capture conditions beside baseline references. Use screenshot comparisons plus computed layout/style checks when useful; exercise real interactions, focus, keyboard controls, reduced motion, and backend editing separately. Include long titles, absent optional media, and repeated items relevant to the content model.

Set comparison criteria before evaluating. Prefer the project's existing thresholds; otherwise require no unexplained visual or functional differences and record rendering noise separately. A measured pixel threshold is project-specific and cannot establish fidelity alone. Accepted deviations name the changed requirement and decision evidence. Never replace reference captures just to clear failures.

No target project is supplied here, so evaluation fixtures can verify contract handling and decision logic without proving live TYPO3 parity. Final implementation reporting must distinguish executed fixture checks from unexecuted application checks.

**Alternative considered:** one desktop screenshot and a successful build. That cannot verify responsive transitions, interactions, editorial behavior, or correct fonts.

### 10. Keep MCP optional and processing reusable

| Need | Initial approach | When an MCP addition is justified |
| --- | --- | --- |
| Stitch design intake | Existing Stitch read tools or supplied local HTML/React exports and captures | Already useful when a provider connection is available; inspect actual tool capabilities before use. |
| Lovable source intake | Supplied exported/local source or GitHub synchronization | A verified provider integration provides additional required read access not available from the export. |
| Automated processing | Skill-guided source inspection plus small deterministic handoff validation helpers | Multiple agent clients need a common hosted processing service or expensive shared workers. |
| Asset management | Local versioned manifest, site-package assets, and TYPO3 FAL | Shared search/deduplication, remote asset ownership, or controlled FAL access requires a service. |
| CI/CD integration | Invoke the same deterministic validators and existing project build/visual checks directly | Agents need to trigger or inspect authorized remote runs through a shared tool interface. |

No new MCP server, credentials, daemon, remote asset store, or deployment workflow is bundled in this change. Runtime browser and source-provider tools remain interchangeable capabilities. When tools are unavailable, accept supplied exports and report unexecuted checks rather than inventing access.

If a future server is added, expose the same processing operations through a thin adapter; keep contracts, checksums, and reports independent of the protocol. CI must remain able to run without an interactive model session or live provider design changing underneath it. Source retrieval stays separate from explicit write operations such as FAL imports, remote design edits, deployment, and baseline replacement.

**Alternative considered:** build one MCP server first to orchestrate all stages. It would add maintenance and service operation before repeated processing needs are established. Existing provider tools plus local contracts address the initial use case.

### 11. Evaluate the skills as behavior, not only Markdown

Add per-skill representative, edge-case, and near-miss prompts with expected outputs, evidence fixtures, and observable assertions following the repository's existing evaluation format. Include at least:

- Extraction: React/Tailwind input, Stitch HTML input, conflicting/unknown tokens, a missing font, nested theme behavior, unsupported target/FSC conflict, and extraction-only scope.
- Analysis: a variant-rich card, page-tree navigation, a full-width section, a carousel with unknown behavior, screenshot-only evidence, an available global handoff that analysis must ignore, and the analysis-to-implementation boundary.
- Build: unchanged Hero reuse, container composition, additional Card metadata, a fixed recipe-allowlist gap, a justified new block, stale dependencies, CSS/manifest mismatch, mobile or keyboard regression, and unavailable live verification.

Use small repository-owned synthetic fixtures and versioned expected handoff examples. Do not copy upstream application assets or vendor implementations wholesale. Validate malformed contracts and stale revisions with deterministic tests; inspect representative model runs when execution is available and compare with a no-skill or prior baseline where feasible. Prompts alone are coverage definitions, not proof of successful execution.

Run available portable-skill validators, link checks, JSON/contract fixture checks, and package metadata validation. Do not add a generic web application test suite to this skills repository or claim end-to-end parity from textual fixtures.

### 12. Decision gates and user-directed boundaries

Decided during design review (2026-10-31):

- **Contract tooling:** ship the full v1 contract tooling now; see `docs/adr/0001-full-v1-handoff-contract-tooling.md`.
- **Placement:** the component spec separates binding requirements from a non-binding `targetHypothesis`. Build adopts or overrides it with a recorded reason; an override does not make the spec stale. Container placement records columns, allowed children (b13/container with content-defender restrictions), and per-column counts. Only placeable elements (content elements, Content Blocks) can sit in a column; embedded Fluid components cannot.
- **Scope:** analyze takes a user-directed `scope` (`single` or `parent-with-children`) and asks when it is missing; non-interactive runs default to `single`, marked `incomplete`.
- **FSC conflict:** a target requiring `typo3/cms-fluid-styled-content` stops target-touching steps and asks the user; non-interactive runs end `blocked`. Read-only extraction and analysis continue.
- **Fidelity gate:** computed style and layout (±1px geometry, exact typography/color/spacing values) are the hard gate; screenshots are advisory. Accepted deviations name requirement, reason and approver.
- **Recipe gap:** try a clean site-package adaptation first; otherwise ask the user to choose an accepted deviation or `blocked`; never silently deviate.

Each of these is a decision gate whose answer is stored in `decisions` (decision 2).

## Risks / Trade-offs

- **Upstream APIs and documentation drift:** use recorded research revisions as context, inspect installed definitions, and include negative evaluations for stale token names and nonexistent extension points.
- **Global branding changes affect reused elements unexpectedly:** map semantic roles rather than names alone and compare representative reused elements after foundation changes.
- **Theme inheritance defeats a global override:** verify actual declaration scopes and computed values across relevant theme roots and modes.
- **Finite recipes grow into too many combinations:** identify meaningful combinations in analysis and test representative intersections plus known interaction boundaries; justify every added option.
- **Responsive intent is absent from exports:** retain unknowns and obtain focused decisions rather than describing invented layouts as extracted behavior.
- **Static connector adapter cannot represent a required dynamic style:** identify the need explicitly and use a supported site-package-owned implementation; do not hide unsupported values in a class-only manifest.
- **Local contracts duplicated for standalone skills can drift:** maintain a common authoring contract, compare consumer schema copies and fixtures, and include cross-skill handoff checks.
- **FSC conflict implies a larger website migration:** preflight blocks automatic removal; report prerequisite migration work separately.
- **No real consumer project is available:** deliver evaluated skill behavior and clearly report the boundary of fixture-based validation; live application verification occurs during an actual migration.

## Migration Plan

1. Implement the contracts, three self-contained skills, references/templates, focused validators, fixtures, and evaluations in this plugin.
2. Update root discovery documentation, relevant installation skill lists, changelog, and descriptive plugin metadata without adding an MCP declaration or changing existing skill behavior.
3. Validate portable packaging, links, contracts, scenario coverage, and representative workflows. Present implementation evidence and unexecuted live checks for review.
4. Consumers install or update the plugin or the individual skills. Skills run against explicitly selected source and target projects; no target website changes occur merely from installing them.
5. For a later authorized target migration, capture a version-control diff and current references before changes, integrate the foundation, then migrate components incrementally. Publish matching CSS/manifests through the project's existing release process only when separately requested. Roll back affected site-package source, matching artifacts, and dependent caches using that process; persisted-data changes require their own migration/rollback treatment.

Plugin rollback is removal of the three new skill directories and reversal of their discovery/documentation changes. There is no database, daemon, service, or remote state to roll back for this plugin change. Pre-existing worktree changes remain untouched.
