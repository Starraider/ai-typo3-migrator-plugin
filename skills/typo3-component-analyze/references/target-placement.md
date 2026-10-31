# Target Placement and Scope Reference

This reference covers the separation of target-neutral binding requirements from the non-binding target hypothesis, container column constraints, and composite section scoping.

## 1. Target Hypothesis vs Binding Requirements

The component specification separates **binding requirements** from the non-binding **target hypothesis**:

- **Binding Requirements:** Semantic structure, editorial content fields, cardinality, media aspect ratios, responsive transition rules, and interaction states. These define WHAT the component is. Changing them invalidates dependent build claims and decisions.
- **Target Hypothesis:** The analyst's non-binding recommendation of WHERE and HOW the component could live in TYPO3. Changing the hypothesis alone does NOT alter the component's binding requirements, does not make the specification stale, and does not require resealing dependent artifacts.

## 2. Placement Classes

The hypothesis classifies the component into one of four placement classes:

| Placement Class | Description | Can Be Placeable in Columns? |
| --- | --- | --- |
| `content-element` | Standalone content element (TCA `tt_content` record or Content Block). | Yes |
| `nested-container` | Multi-column or wrapper container (e.g. `b13/container`). | Yes |
| `native-component` | Embedded Fluid component used inside templates (`<f:render component="..." />`). | **NO** (Must NOT be placed in container columns) |
| `page-layout-part` | Structural part of the page template (e.g., header, navigation, footer). | No |

## 3. Container Columns & Allowed Children

When the placement class is `nested-container`, the hypothesis specifies the column configuration:
- `colPos`: Integer column position (e.g., 101, 102).
- `name`: Descriptive column title (e.g., "Cards Column").
- `allowedChildren`: Allowlist of content element types or Content Block identifiers (e.g., `["astryx_card"]`).
- `min` and `max`: Cardinality bounds for the column.
- **Strict Rule:** Only **placeable elements** (`content-element` or Content Blocks) may be listed in `allowedChildren`. Embedded native components cannot be placed by an editor in a container column.

## 4. User-Directed Analysis Scope: Single vs Parent-With-Children

When analyzing a composite section (e.g., a grid containing three identical cards):

1. **Ask First:** Prompt the user to choose the granularity:
   - `single`: A single monolithic specification describing the entire section with inline cards.
   - `parent-with-children`: A parent section specification referencing one reusable child specification (`components/card/component-spec.json`).
2. **Interactive vs Non-Interactive:**
   - In an interactive session, ask the user one clear question before proceeding.
   - In a non-interactive run where scope is unconfirmed, default to `single`, set readiness to `incomplete`, and record `"granularity not confirmed"` under `unresolved`.
3. **Parent and Child Dependencies:**
   - In `parent-with-children` mode, the parent specification includes child entries under `children` and records child specs in `dependencies`.
   - If a referenced child specification is missing, unreadable, or stale, the parent cannot be `ready`; its readiness must be set to `incomplete`.

