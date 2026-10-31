# Spec Delta

## Purpose

Provide a reusable skill that extracts a mockup's global design and establishes an evidence-backed Astryx site-package foundation for TYPO3 14.3.

## ADDED Requirements

### Requirement: Portable skill discovery and documentation

The plugin SHALL expose `typo3-design-system-extract` as a self-contained portable skill with a matching directory and skill name, a discoverable description, detailed usage documentation, and representative, edge-case, and boundary evaluations. Its description SHALL distinguish global design extraction from individual component analysis and implementation.

#### Scenario: Standalone invocation
- **WHEN** a user installs only the design-system extraction skill and provides an exported mockup
- **THEN** its instructions and directly referenced resources SHALL explain the necessary inputs, outputs, prerequisites, and verification without relying on another installed skill's files

### Requirement: Source evidence and limitations

The skill SHALL inspect available source styles, configuration, assets, and rendered evidence, accepting React projects and available Stitch exports. It SHALL record source identity and revision or digest, distinguish observed values from inferred rules, and disclose missing evidence without inventing design values or responsive states.

#### Scenario: React source and running reference available
- **WHEN** the mockup includes source code, styling configuration, and a runnable reference
- **THEN** the extraction SHALL reconcile declared styling with rendered output and record where each conclusion came from

#### Scenario: Screenshot-only evidence
- **WHEN** only a screenshot is available
- **THEN** the output SHALL identify approximate values and unknown fonts, breakpoints, states, and behavior and SHALL NOT claim a complete or verified design extraction

### Requirement: Global design inventory

The skill SHALL inventory colors, typography, spacing, borders, radii, shadows, motion, layout widths, grids, breakpoints, fluid sizing, global styles, and available themes or modes. It SHALL preserve values needed for fidelity and distinguish shared design values from component-specific exceptions.

#### Scenario: Similar values have different uses
- **WHEN** multiple nearby spacing values occur in the mockup
- **THEN** the extraction SHALL retain their evidence and SHALL NOT normalize them to an assumed scale without documenting the resulting design change

### Requirement: Astryx token mapping

The skill SHALL map extracted values to semantically matching tokens from the installed Astryx sources, identify unmapped values and conflicts, and define project-specific additions where needed. It SHALL keep source token identity, target token identity, values, and mapping rationale traceable and SHALL account for applicable theme and mode scopes.

#### Scenario: Documentation disagrees with installed tokens
- **WHEN** a documented token name or value differs from the installed extension's declarations
- **THEN** the mapping SHALL use the installed declarations, record the discrepancy, and avoid generating references to nonexistent tokens

#### Scenario: Global mapping affects nested themes
- **WHEN** the reference has a global accent and scoped section colors
- **THEN** the mapping SHALL preserve those scopes and verify that inherited Astryx themes do not unexpectedly override them

### Requirement: Asset provenance and ownership

The skill SHALL identify global fonts and design assets with source references, destination or disposition, available usage rights, and unresolved dependencies. It SHALL distinguish fixed site-package assets from editorial media and SHALL report missing or unavailable assets instead of silently substituting them.

#### Scenario: Required font is unavailable
- **WHEN** the mockup names a font whose required files or usage rights cannot be established
- **THEN** the skill SHALL record the unresolved dependency and any proposed substitution as a visual difference requiring a decision

### Requirement: Target compatibility preflight

Before target-project implementation, the skill SHALL verify TYPO3 14.3.x and the installed Astryx, StyleX Connector, PHP, and build dependency constraints. It SHALL report incompatibilities, including Fluid Styled Content conflicts, before changing the target. It SHALL NOT silently upgrade TYPO3, remove conflicting extensions, or claim TYPO3 13 support.

#### Scenario: Target uses TYPO3 13
- **WHEN** the user requests integration into a TYPO3 13 project
- **THEN** the skill SHALL identify the unsupported target and keep any useful source analysis separate from blocked implementation

#### Scenario: Fluid Styled Content is installed
- **WHEN** the target contains a package that conflicts with the selected Astryx version
- **THEN** the skill SHALL describe the conflict and its rendering implications, SHALL stop target-touching steps and ask the user what to do, and SHALL NOT remove the package as an implicit setup step

#### Scenario: Fluid Styled Content in a non-interactive run
- **WHEN** the target requires `typo3/cms-fluid-styled-content` and no question can be asked
- **THEN** target-touching steps SHALL end as `blocked` with the conflict recorded, while read-only source extraction MAY continue

### Requirement: Site-package foundation integration

For an authorized compatible target, the skill SHALL establish the extracted design through site-package-owned StyleX tokens and the existing Astryx and StyleX Connector integration. It SHALL preserve the extension's supported customization mechanisms, include required global styles and fonts, and provide working development and production asset loading.

#### Scenario: Foundation integrated through existing extensions
- **WHEN** the target passes preflight and foundation implementation is requested
- **THEN** the resulting site package SHALL use the existing connector rather than a replacement bridge and SHALL keep project branding changes outside installed dependency files

### Requirement: Build and visual verification

The skill SHALL verify that built CSS and corresponding style mappings are delivered consistently and that representative typography, colors, and layouts render correctly in TYPO3. It SHALL record commands, capture conditions, comparisons, and remaining differences. An unavailable build or browser check SHALL be reported as unverified rather than passed.

#### Scenario: Required style mapping is missing
- **WHEN** CSS exists but a Fluid-referenced style mapping is absent or belongs to a different build
- **THEN** verification SHALL fail and the skill SHALL identify the inconsistent outputs before reporting completion

#### Scenario: Rendered verification is unavailable
- **WHEN** source extraction succeeds but no target browser session can be run
- **THEN** the output SHALL distinguish completed extraction from unverified rendered integration

### Requirement: Versioned downstream handoff

The skill SHALL produce a readable extraction report and a versioned structured handoff containing source provenance, target versions when known, token mappings, asset references, evidence gaps, and verification status. It SHALL identify its own output revision so later skills can detect changed source or token inputs.

#### Scenario: Component analysis receives changed tokens
- **WHEN** a subsequent run changes the global token mapping
- **THEN** the handoff SHALL expose a changed revision or digest so dependent component analysis and implementation can be reassessed

### Requirement: Respect run scope

The skill SHALL keep the mockup source unchanged, constrain outputs to the resolved authorized destination, and distinguish analysis-only runs from target implementation. It SHALL reuse available source exports or connections without requiring a custom MCP server, installing services, publishing, or modifying remote designs as an implicit step.

#### Scenario: User requests extraction only
- **WHEN** the user asks for a token report without target-project changes
- **THEN** the skill SHALL write only authorized analysis outputs and SHALL NOT install packages or change site-package code

### Requirement: Recorded decisions

The structured handoff SHALL include a `decisions` array. Each entry SHALL record an identifier, the question, the offered options, the user's answer and wording, the date, and the artifact or component it applies to. A decision that changes binding requirements or accepts a deviation SHALL contribute to the artifact revision; a run-only decision SHALL NOT. A later session SHALL reuse a recorded decision instead of asking again unless its binding requirements changed. An unanswered decision gate SHALL appear in `unresolved` and SHALL set readiness to `blocked`, or `incomplete` where this specification says so.

#### Scenario: Fresh session reuses an answered decision
- **WHEN** a handoff records an answered decision whose binding requirements are unchanged
- **THEN** the skill SHALL apply it without asking again

#### Scenario: Decision becomes stale
- **WHEN** the binding requirements a decision applies to change
- **THEN** the skill SHALL mark the decision stale and ask again before relying on it
