# Component Analysis Reference

This guide covers decomposing a React component or composite mockup section into an implementation-independent specification suitable for TYPO3 and Astryx.

## 1. Whole-Component Visual Design

Describe the complete visual treatment of the selected element. The goal is to give implementation enough information to reproduce the actual component even when no global design-system handoff exists.

- **Frame:** Record whether the component is full bleed or bounded, its width constraints, alignment, overall proportions, and section-level padding or gutters. For composite sections, cover both the outer section and the inner content frame.
- **Composition:** Describe visual hierarchy, grouping, columns, ordering, alignment, overlap, and relative proportions. Explain how the parts relate at each evidenced variant and viewport.
- **Surface:** Record backgrounds, borders, corner shapes, shadows, gradients, overlays, and decorative treatments.
- **Typography:** For each meaningful text role, describe observed family when identifiable, size, weight, line-height, color, letter-spacing, casing, and alignment. A screenshot can support an approximate appearance, not an exact font declaration.
- **Spacing:** Describe outer and inner padding, gaps, margins, and their relationships. Preserve exact source values when declared; estimate from a rendered view only with viewport and evidence noted.
- **Parts:** Describe the appearance of every visually important part, including media placement/crop, headings, badges, copy, actions, and decorative items.
- **Visual states:** Describe default appearance and evidenced hover, focus, active, selected, disabled, expanded, or other states. Unknown states remain unknown.

Put these facts in `payload.design` using the component-spec schema. Tag each description as `source`, `rendered`, `user`, `inferred`, or `unknown`. Prefer concrete local values (for example `24px`, `#f5f5f5`, `1px solid`) over vague labels when evidence supports them. Do not translate them into global token names or check the component against a global token inventory; that comparison belongs to implementation.

## 2. Semantic Structure & Variants

Break the component down into hierarchical parts:
- **Parts:** Outer wrapper, media container, header, body text, action links, badges, tags.
- **Variants:** Identify distinct structural forms (e.g. `horizontal` vs `vertical`, `featured` vs `compact`).
  - Differentiate supported variants from hypothetical ones.
  - Document the conditions under which each variant is displayed.
  - Never collapse functionally different variants into a single generic component.

## 3. Content Model Decomposition

Categorize each data property into one of four distinct classes:

| Class | Description | TYPO3 Translation |
| --- | --- | --- |
| `editorial` | Content authored, edited, or selected by an editor in the backend. | Database field in TCA / Content Block config, FAL file reference, or link field. |
| `fixed` | Static UI labels, boilerplate decoration, or markup constant across all instances. | Hard-coded in Fluid template or translation XLIFF. |
| `derived` | Values computed at render time (dates, item counts, active menu states). | ViewHelper calculation, controller data processing, or TypoScript menu processor. |
| `interaction-state` | Ephemeral client-side state (accordion open/closed, dropdown toggle). | Client JavaScript or CSS `:focus-within` / `:checked`. Never persisted as database fields. |

## 4. Placement Comparison: Editorial Card vs Page-Tree Navigation

To illustrate how different components require fundamentally different TYPO3 editorial architectures, consider a Card vs a Primary Navigation Menu:

### Case A: Editorial Image Card
- **Nature:** Reusable content element placed in various pages and containers.
- **Content Model:**
  - `header` (editorial, string, cardinality 1)
  - `subheader` / `badge` (editorial, string, cardinality 0..1)
  - `bodytext` (editorial, rich text, cardinality 0..1)
  - `image` (editorial, FAL sys_file_reference, cardinality 0..1, aspect ratio 16:9)
  - `links` (editorial, link/button records, cardinality 0..3)
- **Target Placement:** `content-element` (or Content Block). Placeable in container columns.
- **Astryx Candidate:** Inspect `vendor/skom/typo3-astryx/ContentBlocks/ContentElements/card`. Record advisory candidate notes and any field gaps (e.g., missing badge field).

### Case B: Primary Navigation Menu
- **Nature:** Site-wide structural navigation derived from the TYPO3 page hierarchy.
- **Content Model:**
  - Page titles, URLs, and active states are **derived** from the TYPO3 rootline and page tree.
  - Editorial fields for manual menu item entry would cause content drift and maintenance burden.
- **Target Placement:** `page-layout-part` (rendered in the main page template or layout via a `MenuProcessor`).
- **Astryx Candidate:** Rendered as part of the site package page header layout, consuming Astryx navigation styling if available, NOT as a standalone content element in `tt_content`.

## 5. Advisory Astryx Candidate Notes

Record potential candidates found in the installed Astryx distribution:
- Note matches (e.g., Astryx Card, Astryx Hero, Astryx Container).
- Document observed gaps (missing fields, different slots, fixed recipe limits).
- Candidate notes are explicitly non-binding advisory information for the build skill. Analysis remains implementation-neutral.

