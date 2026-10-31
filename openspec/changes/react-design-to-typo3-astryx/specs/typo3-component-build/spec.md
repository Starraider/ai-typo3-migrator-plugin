# Spec Delta

## Purpose

Provide a reusable skill that implements specified mockup components in TYPO3 14.3 through Astryx reuse or targeted adaptation and verifies their appearance, responsive behavior, and editorial usability.

## ADDED Requirements

### Requirement: Portable implementation skill

The plugin SHALL expose `typo3-component-build` as a self-contained portable skill with a matching directory and skill name, detailed documentation, and representative, edge-case, and boundary evaluations. It SHALL distinguish component implementation from global design extraction and analysis-only requests.

#### Scenario: Implementation starts from supplied artifacts
- **WHEN** a new session receives compatible design-system and component handoffs and an authorized target project
- **THEN** the skill SHALL resolve the necessary evidence and implementation boundary without requiring the earlier skills to run again

### Requirement: Current inputs and acceptance boundary

The skill SHALL inspect source, token, component-specification, and target-version provenance before implementation. It SHALL flag incompatible handoff versions, stale dependencies, or material missing requirements and establish the affected variants, states, viewports, and comparison criteria before treating implementation as ready to verify.

#### Scenario: Global design-system handoff has stale provenance
- **WHEN** the supplied global design-system handoff has an outdated dependency or unprovable source freshness
- **THEN** the skill SHALL identify affected mappings and require reassessment before treating those mappings as current

### Requirement: Component design coverage assessment

When the component specification includes a component-level `design` description, the build skill SHALL compare its visual requirements with the actual active style inheritance of the selected Content Block/content element and the current global design-system handoff before target edits. It SHALL distinguish active inherited values from merely available global tokens, and record exact component-specific token IDs and values needed for uncovered details.

#### Scenario: Selected element inherits only part of the analyzed design
- **WHEN** the selected Card inherits the specified title style and radius, while a global color token exists but is not applied to the Card and no global hover token exists
- **THEN** the assessment SHALL identify the title and radius as inherited, the color as available through a global token, and the hover treatment as requiring an exact component-specific token

### Requirement: Preserve component visual requirements during implementation

Global coverage SHALL inform implementation choices without changing component visual requirements. It SHALL NOT replace rendered parity verification. For composed sections, the assessment SHALL identify the actual selected content element or Content Block for each requirement.

#### Scenario: Global design covers only part of a component's appearance
- **WHEN** some component design details are mapped to global tokens
- **THEN** the build SHALL retain all original requirements for implementation and visual verification and record which selected element supplies each inherited value

### Requirement: Supported target and rendering compatibility

The skill SHALL verify TYPO3 14.3.x and the selected Astryx, StyleX Connector, runtime, and dependency constraints before target changes. It SHALL identify conflicting rendering packages and SHALL NOT silently upgrade TYPO3, remove Fluid Styled Content, or implement against an unsupported target.

#### Scenario: Astryx requirements conflict with the installation
- **WHEN** the target has incompatible TYPO3 or PHP versions or a conflicting rendering extension
- **THEN** the skill SHALL report the concrete incompatibility and required prerequisite work without modifying package constraints to bypass it

### Requirement: Mandatory Astryx reuse assessment

Before creating or modifying a target element, the skill SHALL inspect existing Astryx content elements, containers, shared components, fields, variants, styles, assets, and interaction behavior relevant to the specification. It SHALL produce an evidence-backed candidate assessment that identifies fits, gaps, required changes, and the selected approach.

#### Scenario: Existing Card is a plausible candidate
- **WHEN** the specification describes an image card with heading, badge, body, and actions
- **THEN** the assessment SHALL compare the installed Card's actual field model, slots, variants, responsiveness, and behavior against those requirements before selecting it

#### Scenario: Section can use an existing container
- **WHEN** a section requires nested editorial content and a full-width background
- **THEN** the assessment SHALL inspect relevant Astryx containers and composition options before proposing a new section content type

### Requirement: Smallest suitable adaptation

The skill SHALL prefer configuration and theming, composition, and supported site-package overrides before introducing new content types. It SHALL select a new element only when the assessment documents why existing foundations cannot meet the contract cleanly. Reuse SHALL preserve the specified appearance, content model, accessibility, and behavior rather than weakening requirements to fit a candidate.

#### Scenario: Existing Hero fits through configuration
- **WHEN** an installed Hero supports the required structure and behavior and only its design values differ
- **THEN** the skill SHALL configure and theme that element rather than create a duplicate Hero type

#### Scenario: Existing Carousel has different behavior
- **WHEN** a carousel candidate resembles the mockup but lacks a required interaction
- **THEN** the assessment SHALL identify the behavior gap and choose a justified adaptation or new implementation without claiming unchanged reuse satisfies the specification

### Requirement: Extension ownership and capability gaps

The skill SHALL keep project-specific changes in the site package and use extension points verified in the installed versions. It SHALL distinguish supported overrides from missing upstream capabilities and SHALL NOT edit installed dependency files or remote repositories as an implicit implementation step.

#### Scenario: New recipe option is not extensible
- **WHEN** the required variant is rejected by the installed recipe allowlist and no supported registration mechanism exists
- **THEN** the skill SHALL identify that gap and use a suitable site-package implementation or report a concrete upstream change recommendation without silently patching the dependency

### Requirement: Native editorial implementation

The implementation SHALL use TYPO3-native editable fields and relations for editorial content and native rendering for the specified target placement. It SHALL preserve applicable existing content identifiers and relations when extending an element, distinguish fixed assets from editorial media, and avoid importing mockup content as hard-coded production data.

#### Scenario: Card extension introduces metadata
- **WHEN** an existing card needs an additional editable metadata value
- **THEN** the implementation SHALL add or reuse an appropriate field and render it without destroying existing card content or substituting a hard-coded mock value

#### Scenario: Menu belongs to the page layout
- **WHEN** the specification identifies a page-tree navigation component
- **THEN** the implementation SHALL use the required placement and data source rather than creating a redundant manually maintained menu element

### Requirement: Existing StyleX integration

Component styling SHALL consume the extracted design system through the existing Astryx and StyleX Connector integration. The skill SHALL verify referenced style mappings, finite variants, required assets, and production CSS delivery and SHALL NOT replace that integration with an unrelated styling stack or a second connector implementation.

#### Scenario: New variant is compiled but not available in Fluid
- **WHEN** styling exists in source but its required style mapping is missing from the delivered build
- **THEN** the skill SHALL treat the variant as incomplete and correct or report the build integration before declaring success

### Requirement: Visual and responsive verification

The skill SHALL compare source and target using equivalent content, fonts, assets, capture conditions, representative widths, and relevant states. It SHALL inspect layout transitions and record commands, captures, differences, and accepted deviations. It SHALL NOT claim exact or verified parity when reference behavior or executed comparisons are missing.

#### Scenario: Desktop passes but mobile layout differs
- **WHEN** the target matches the desktop reference but places media incorrectly on mobile
- **THEN** verification SHALL fail for the mobile requirement and completion SHALL remain qualified until the difference is resolved or explicitly accepted

#### Scenario: Screenshot baselines would hide a regression
- **WHEN** a comparison exposes an unexplained difference
- **THEN** the skill SHALL investigate it and SHALL NOT overwrite the reference baseline merely to make the check pass

### Requirement: Functional and editorial verification

The skill SHALL verify relevant interactions, keyboard navigation, focus, reduced-motion handling, and content readability with and without enhancement where specified. It SHALL exercise backend editing and representative content edge cases and distinguish functional checks from screenshot comparisons.

#### Scenario: Visually matching menu traps keyboard focus
- **WHEN** a menu matches reference screenshots but keyboard focus cannot leave or return correctly
- **THEN** functional verification SHALL fail despite the visual match

#### Scenario: Editor uses longer content
- **WHEN** a user enters a longer heading or omits an optional image
- **THEN** the element SHALL follow the specified content rules without clipping required content, rendering broken media, or losing essential actions

### Requirement: Completion report and operational scope

The skill SHALL report the reuse decision, changed files, extension points used, asset disposition, executed checks, remaining gaps, and verification status in a versioned handoff. It SHALL keep changes within the authorized project scope and SHALL NOT deploy, publish, migrate bulk content, modify upstream projects, or require a custom MCP server as an implicit step.

#### Scenario: Live target verification is unavailable
- **WHEN** code and build checks pass but no TYPO3 browser or backend session is available
- **THEN** the report SHALL mark rendered and editorial verification as pending rather than claiming the component fully verified

### Requirement: FSC conflict decision gate

When the target requires `typo3/cms-fluid-styled-content`, the skill SHALL stop before any target edit and ask the user what to do. In a non-interactive run it SHALL end as `blocked` with the conflict recorded.

#### Scenario: Target uses Fluid Styled Content
- **WHEN** preflight finds the conflicting package
- **THEN** the skill SHALL make no target edits, report the conflict, and ask the user how to proceed

### Requirement: Hard fidelity gate

Computed style and layout checks SHALL be the hard gate for parity: box geometry within ±1px, and exact font family, size, weight, line-height, color, and spacing values, at each breakpoint and state in the comparison matrix. Screenshot comparison SHALL be advisory and SHALL NOT alone pass or fail a component. An accepted deviation SHALL name the changed requirement, reason, and approver and SHALL be recorded as a decision; any unrecorded difference SHALL fail.

#### Scenario: Pixel diff is small but layout shifted
- **WHEN** a screenshot diff is below any threshold but a computed box differs by more than 1px
- **THEN** verification SHALL fail

#### Scenario: Only anti-aliasing noise differs
- **WHEN** computed styles and layout match and the screenshot differs by rendering noise
- **THEN** the noise SHALL be recorded separately and verification SHALL NOT fail

### Requirement: Recipe gap decision sequence

When a required variant is not expressible through the installed recipe options, the skill SHALL first attempt a clean site-package-owned adaptation, recording `extend` or `create` and the rejected alternatives. If no clean adaptation exists, the skill SHALL ask the user to choose between an accepted deviation (nearest existing recipe) and `blocked` with an upstream-gap report, and SHALL NOT choose a deviation silently. In a non-interactive run the component SHALL end as `blocked`.

#### Scenario: No clean adaptation exists
- **WHEN** the required variant cannot be built in the site package without editing dependencies
- **THEN** the skill SHALL ask the user to choose between deviation and blocked

### Requirement: Placement hypothesis and container columns

The skill SHALL record whether it adopted or overrode the specification's target hypothesis, with the reason. For container placement it SHALL verify column definitions, allowed child types (including the content-defender dependency where used), and that every child is a placeable element; an embedded component SHALL NOT be placed in a column.

#### Scenario: Hypothesis overridden
- **WHEN** the installed assessment selects composition where the hypothesis proposed a standalone element
- **THEN** the build report SHALL record the override and reason without invalidating the specification

### Requirement: Recorded decisions

The build report SHALL include a `decisions` array with identifier, question, offered options, answer and wording, date, and applicable component. Deviation and override decisions that change binding requirements SHALL contribute to the revision; run-only decisions SHALL NOT. Recorded decisions SHALL be reused rather than re-asked unless their binding requirements changed, and unanswered gates SHALL set readiness to `blocked`.

#### Scenario: Fresh session reuses an accepted deviation
- **WHEN** a build report records an accepted deviation with unchanged requirements
- **THEN** the skill SHALL apply it without asking again
