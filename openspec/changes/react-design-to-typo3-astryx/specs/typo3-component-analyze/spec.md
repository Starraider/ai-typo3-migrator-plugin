# Spec Delta

## Purpose

Provide a reusable skill that converts a selected mockup component into a traceable content, whole-component visual design, asset, and behavior specification for later TYPO3 implementation.

## ADDED Requirements

### Requirement: Independently usable analysis skill

The plugin SHALL expose `typo3-component-analyze` as a self-contained portable skill with a matching directory and skill name, detailed documentation, and representative, edge-case, and near-miss evaluations. It SHALL accept a selected component and its design references without requiring a global design-system handoff or an earlier skill to have run in the same session.

#### Scenario: Analysis starts in a fresh session
- **WHEN** the user supplies a component source, with or without a global design-system handoff
- **THEN** the skill SHALL resolve the component inputs explicitly and produce analysis without relying on hidden conversation state, token mappings, or another installed skill's files

#### Scenario: A global design-system handoff is present or absent
- **WHEN** a component is supplied with or without a global design-system handoff
- **THEN** the skill SHALL describe the component's own design from its source and rendered evidence, SHALL NOT compare it with global tokens or record global mappings as unresolved, and SHALL leave that comparison to implementation

### Requirement: Whole-component visual design

The skill SHALL describe the complete visual design of the selected component or section, including its overall frame, composition, surface treatment, typography, spacing, important part appearances, and evidenced visual states. It SHALL distinguish exact source values from rendered measurements, screenshot estimates, user requirements, and unknowns. It SHALL describe the design as observed without extracting or mapping global design-system tokens.

#### Scenario: A card has a complete visual treatment
- **WHEN** source and rendered evidence show a card's frame, media placement, type hierarchy, spacing, surface, and focus or hover treatment
- **THEN** the specification SHALL record those properties across the whole card and its meaningful parts with evidence classes, rather than limiting the analysis to structure and content fields

#### Scenario: Screenshot-only design evidence
- **WHEN** only a static screenshot is available
- **THEN** the specification SHALL describe visible composition, approximate geometry, colors, typography appearance, spacing, and surface while marking inferred measurements and unobserved states clearly

### Requirement: Component identity and evidence boundary

The skill SHALL resolve the selected component, source revision or digest, dependency context, and representative rendered location. It SHALL distinguish local source facts, rendered observations, user requirements, and assumptions, and disclose inaccessible states or dependencies.

#### Scenario: Component name matches several implementations
- **WHEN** the source contains multiple cards and the selection does not identify the intended one
- **THEN** the skill SHALL inspect available context and request only the missing selection before treating one implementation as the reference

### Requirement: Structure and variant specification

The skill SHALL describe the component's semantic structure, nested parts, content slots, dependencies, exposed variants, and meaningful combinations of options. It SHALL distinguish genuinely supported variants from hypothetical alternatives and record which evidence supports each identified state.

#### Scenario: Source exposes several card variants
- **WHEN** the selected component supports horizontal, vertical, and featured layouts
- **THEN** the specification SHALL describe their structural differences, applicable conditions, and representative combinations without flattening them into one generic card

### Requirement: Editorial content and TYPO3 placement

The skill SHALL distinguish editor-managed content, fixed presentation, derived data, and interaction state. It SHALL propose fields, relations, cardinality, defaults, and validation where evidenced, and classify the target as a content element, container, shared component, or page-layout part without assuming every visual component is a content element.

#### Scenario: Primary navigation uses site hierarchy
- **WHEN** the selected mockup component is a primary navigation menu
- **THEN** the analysis SHALL consider page-tree data and page-layout placement rather than automatically proposing manually maintained menu item records

#### Scenario: Card contains repeatable editorial content
- **WHEN** a card has a title, image, optional badge, and several actions
- **THEN** the specification SHALL identify editable fields and action cardinality separately from layout variants and transient UI state

### Requirement: Responsive and interaction contract

The skill SHALL record layout transitions, sizing and ordering rules, image behavior, and applicable interaction states from available evidence. It SHALL specify keyboard behavior, focus, reduced motion, and no-JavaScript behavior where relevant, and distinguish required behavior from unresolved or proposed behavior.

#### Scenario: Desktop and mobile layouts differ
- **WHEN** the reference changes image order and navigation presentation at a breakpoint
- **THEN** the analysis SHALL record those transitions and the supporting source or rendered observations, including checks around the transition width

#### Scenario: Only one viewport is evidenced
- **WHEN** the user provides a desktop screenshot without source or mobile references
- **THEN** the analysis SHALL mark mobile rules and interaction states as unknown instead of declaring exact responsive behavior

### Requirement: Component asset manifest

The skill SHALL identify required images, icons, fonts, and other assets with their source references, available provenance, dimensions or formats when known, intended roles, and unresolved dependencies. It SHALL record image crops, aspect ratios, alternate text requirements, and editorial versus fixed ownership where applicable.

#### Scenario: Remote image cannot be retrieved
- **WHEN** a required image URL is unavailable
- **THEN** the manifest SHALL preserve the reference and mark the asset unresolved, and any placeholder SHALL be recorded as a temporary difference rather than the required asset

### Requirement: Existing Astryx candidates are advisory evidence

When target Astryx evidence is available, the skill SHALL identify plausible existing content elements and components and record known gaps without claiming reuse has been proven. Final reuse selection and implementation verification SHALL belong to the component-build skill.

#### Scenario: Similar existing element has fewer fields
- **WHEN** an Astryx Card appears suitable but the reference requires additional editorial metadata
- **THEN** the analysis SHALL record the candidate and the missing data requirement without treating visual similarity as implementation equivalence

### Requirement: Versioned component handoff

The skill SHALL produce a readable specification and structured handoff containing component identity, source provenance, full component visual design, structure, variants, content model, assets, behavior, reference captures, unresolved questions, and verification criteria. It SHALL flag unsupported handoff versions and stale component-source or child-spec dependencies before reuse. Global design-system alignment and token overlap SHALL be assessed during implementation, outside this skill.

#### Scenario: Existing component specification has child dependencies
- **WHEN** a composite specification reuses a child component handoff
- **THEN** the skill SHALL validate the child dependency freshness while ignoring any global design-system handoff for component-design comparison

### Requirement: Analysis scope and side effects

The skill SHALL limit writes to authorized analysis documents, structured handoffs, and reference evidence. It SHALL keep source and target implementation code unchanged, avoid dependency installation or database changes, and SHALL NOT implement a component merely because an Astryx candidate is apparent.

#### Scenario: Analysis request includes an implementation temptation
- **WHEN** a user asks to analyze a card and the target already contains a nearly identical element
- **THEN** the skill SHALL finish the analysis and identify the implementation handoff without editing that element or its configuration

### Requirement: Explicit readiness and missing evidence

The output SHALL distinguish ready-for-implementation sections from unresolved requirements. Unknowns affecting structure, content, asset selection, or behavior SHALL remain visible; the skill SHALL request a focused clarification when available evidence cannot resolve a material requirement and SHALL NOT mark the affected component ready by assumption.

#### Scenario: Carousel behavior is ambiguous
- **WHEN** the reference does not establish whether the carousel loops or advances automatically
- **THEN** the skill SHALL record the ambiguity and obtain the needed behavior decision before treating that interaction contract as complete

### Requirement: Target hypothesis separate from binding requirements

The component specification SHALL record target-neutral binding requirements (content parts, cardinality, defaults, assets, behavior) separately from a non-binding `targetHypothesis` containing the placement class and proposed fields. Placement SHALL distinguish placeable elements (content elements and Content Blocks) from embedded components. For container placement, the hypothesis SHALL describe each column, the allowed child components, and per-column minimum and maximum counts. Changing only the hypothesis SHALL NOT make the specification stale.

#### Scenario: Container column restricts children
- **WHEN** a section is hypothesized as a container whose column accepts only cards
- **THEN** the hypothesis SHALL list the card component as an allowed placeable child and SHALL NOT list an embedded component as placeable

#### Scenario: Build overrides the hypothesis
- **WHEN** the build skill selects a different placement
- **THEN** the analysis specification SHALL remain current and the build report SHALL record the override and its reason

### Requirement: User-directed analysis scope

For a composite section, the skill SHALL accept a `scope` of `single` (one specification with inline children) or `parent-with-children` (a parent specification referencing one child specification per distinct child component). The skill SHALL record the user's directive as a source and a decision. When scope is not given and the section has repeated or distinct children, the skill SHALL ask one focused question rather than guess.

#### Scenario: Scope given as parent with children
- **WHEN** the user directs `parent-with-children` for a section of three cards
- **THEN** the skill SHALL produce a parent specification with a dependency on one card specification reused by all three

#### Scenario: Scope unconfirmed in a non-interactive run
- **WHEN** scope is not given and no question can be asked
- **THEN** the skill SHALL default to `single`, set readiness to `incomplete`, and list "granularity not confirmed" under `unresolved`

#### Scenario: Missing child specification
- **WHEN** a parent specification references a child specification that is missing or stale
- **THEN** the parent SHALL be `incomplete`, not `ready`

### Requirement: Recorded decisions

The structured handoff SHALL include a `decisions` array. Each entry SHALL record an identifier, the question, the offered options, the user's answer and wording, the date, and the artifact or component it applies to. A decision that changes binding requirements or accepts a deviation SHALL contribute to the artifact revision; a run-only decision SHALL NOT. A later session SHALL reuse a recorded decision instead of asking again unless its binding requirements changed. An unanswered decision gate SHALL appear in `unresolved` and SHALL set readiness to `blocked`, or `incomplete` where this specification says so.

#### Scenario: Fresh session reuses an answered decision
- **WHEN** a handoff records an answered decision whose binding requirements are unchanged
- **THEN** the skill SHALL apply it without asking again

#### Scenario: Decision becomes stale
- **WHEN** the binding requirements a decision applies to change
- **THEN** the skill SHALL mark the decision stale and ask again before relying on it
