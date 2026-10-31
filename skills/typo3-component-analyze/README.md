# TYPO3 Component Analysis

Analyze ONE selected mockup component or composite section from source code, a URL, Stitch design, export, screenshots, or related artifacts. Combine available resources into an implementation-independent, TYPO3-oriented specification of the complete component design, structure, variants, editorial content, assets, responsive and interaction behavior, and a non-binding placement hypothesis, sealed as a versioned handoff.

## What this skill solves

Bridging the gap between React mockup code and TYPO3 content elements is error-prone when developers immediately attempt code generation. Direct translation often misses editorial data requirements, turns transient UI state into unnecessary database columns, misclassifies structural navigation menus as content elements, and flattens responsive variants.

This skill isolates the analysis phase:
- Extracts structural parts and distinguishes genuine variants from hypothetical alternatives.
- Analyzes editorial content models (cardinality, field types, validation) distinct from fixed template text.
- Differentiates navigation structures (which derive from the TYPO3 page tree) from modular content elements.
- Describes the whole component visually: frame, composition, surface, typography, spacing, important parts, and evidenced visual states.
- Identifies assets, required aspect ratios, and accessibility metadata.
- Inspects supplied URLs in the internal browser and saves representative screenshots in the migration bundle.
- Uses source code, browser renders, screenshots, Stitch artifacts, and other available resources together, with explicit evidence when they disagree.
- Specifies responsive layout transitions and interaction contracts (keyboard, focus, reduced-motion).
- Establishes a target hypothesis separating placeable content elements from embedded Fluid components.
- Seals the resulting specification into a versioned `component-spec.json` and human-readable `component-spec.md`.

## Use when

- Before implementing a mockup component in TYPO3 14.3 with Astryx.
- To produce an unambiguous component specification from React, HTML/CSS, or screenshots.
- To analyze a component from a rendered URL, alone or alongside source code, screenshots, Stitch exports, and other artifacts.
- To analyze a composite section and decide whether to break it into parent and child specifications.

## When NOT to use

- Do not use for extracting global design tokens or site-package Vite setup. Use `typo3-design-system-extract` instead. This skill records the component's observed design without comparing it with global tokens; `typo3-component-build` performs that comparison during implementation.
- Do not use to edit TYPO3 site-package code, create Content Blocks, or run build tasks. Use `typo3-component-build` instead.
- Do not use when the request asks to implement or code the component immediately.

## Context requirements

- **Inputs:** React component source code, CSS styles, one or more URLs, rendered screenshots, Stitch screens/exports, assets, or a combination of these. A supplied URL is inspected through the internal browser. A global `design-system.json` handoff is not required or analyzed.

## Expected outputs

- **Outputs:** Written to `design-migration/<design-id>/components/<component-id>/`:
  - `component-spec.json`: Sealed JSON artifact adhering to `component-spec.payload.schema.json`, including an evidence-labeled `payload.design` for the whole component.
  - `component-spec.md`: Companion human-readable specification with the same design, structure, content, and behavior facts.
  - `references/`: Representative URL captures, each registered as a source with capture conditions and a digest.

## Scope & Side Effects

This skill is strictly **read-only** regarding source mockup and target TYPO3 application code. Supplied URLs and Stitch designs are inspected without modifying them.
- Never edits site packages, Content Blocks, or templates.
- Never installs npm packages or composer dependencies.
- Writes only the specification handoff and URL screenshot captures inside the migration bundle.

## Example prompts

- **Full card design analysis:** "Analyze the card in `src/components/Card.tsx` and its rendered URL. Describe its full visual design, including frame, layout, surface, typography, spacing, media crop, and hover/focus appearance. Capture desktop and mobile, and save the sealed spec in `design-migration/site/components/card/`. Leave global-token comparison for implementation."

- **Combined source set:** "Analyze the feature grid in `src/sections/FeatureGrid.tsx` together with `https://example.test/features`, the supplied mobile screenshots, and the Stitch export. Describe the whole section and child-card design, capture the URL in the internal browser, and document evidence conflicts and container constraints."

- **Ambiguous interaction:** "Analyze the carousel mockup in `src/components/Carousel.tsx`. It has next/previous buttons, but it's unclear whether it auto-advances. Capture the ambiguity as a decision gate and output an incomplete spec until clarified."

## Installation

This skill is self-contained in this directory. For project-level Codex discovery, place or link the directory at `.agents/skills/typo3-component-analyze/` and keep its `references/`, `templates/`, and `scripts/` beside `SKILL.md`.

## Validation

Validate any generated `component-spec.json` using the bundled Python script:

```bash
python3 scripts/validate_handoff.py validate design-migration/<design-id>/components/<component-id>/component-spec.json
```

To recompute digests and seal the specification:
```bash
python3 scripts/validate_handoff.py seal design-migration/<design-id>/components/<component-id>/component-spec.json
```

## Related skills

- [`typo3-design-system-extract`](../typo3-design-system-extract/README.md) — extract global design tokens and site-wide foundations.
- [`typo3-component-build`](../typo3-component-build/README.md) — implement a component from its specification.

### Reference documentation

- [Handoff Contract](references/handoff-contract.md)
- [Component Analysis Method](references/component-analysis.md)
- [Source & Evidence Guide](references/source-and-evidence.md)
- [Responsive & Interaction Rules](references/responsive-and-interaction.md)
- [Target Placement & Scope](references/target-placement.md)

## License

This skill is distributed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](../../LICENSE).

