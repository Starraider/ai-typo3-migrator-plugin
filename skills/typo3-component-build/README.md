# TYPO3 Component Building & Verification

Implement ONE already-specified mockup component in TYPO3 14.3 using Astryx reuse or targeted site-package adaptation, and verify its visual, responsive, and functional parity. Produces a sealed `build-report` handoff.

## What this skill solves

Turning a design specification into a TYPO3 content element often defaults to writing a completely new, bespoke element from scratch. This bloats the site package, duplicates existing Astryx elements (such as Hero, Card, or Container), bypasses StyleX Connector optimization, and skips rigorous responsive and accessibility verification.

This skill provides a structured implementation and verification workflow:
- Enforces preflight checks (TYPO3 14.3.x, PHP 8.3+, and blocking on Fluid Styled Content conflicts).
- Performs a mandatory Astryx candidate assessment before editing any target files.
- Traces the selected Content Block's active style inheritance, compares it with the global design system, and records inherited values separately from exact component-specific tokens needed.
- Applies the disposition hierarchy: Configure → Compose → Extend → Create New.
- Implements adaptations cleanly within the site package, preserving native TYPO3 fields and FAL relations.
- Verifies visual parity with a hard computed style/layout gate (±1px geometry) rather than relying on noisy screenshot thresholds.
- Tests functional states, keyboard navigation, focus management, and editorial content boundaries.
- Produces a machine-sealed `build-report.json` and human-readable `build-report.md`.

## Use when

- When a valid `component-spec.json` and `design-system.json` exist and the component is ready for TYPO3 implementation.
- To adapt or extend an existing Astryx content element (like Card or Hero) for a specific mockup design.
- To compose composite sections using Astryx Containers and Content Blocks.
- To execute formal visual and functional verification gates in a TYPO3 project.

## When NOT to use

- Do not use for initial global design token extraction. Use `typo3-design-system-extract` instead.
- Do not use for analyzing React components without implementing them. Use `typo3-component-analyze` instead.
- Do not use on TYPO3 13 or older installations; Astryx strictly requires TYPO3 14.3.x.

## Context requirements

- A TYPO3 14.3.x project with `skom/typo3-astryx` (~14.3.0) and `skom/stylex-connector` (^1.1.2).
- Valid, sealed input handoffs: `design-system.json` and `component-spec.json`.
- Site package with Node.js and Vite configured.
- `typo3/cms-fluid-styled-content` must NOT be installed.
- Python 3.8+ for handoff sealing and validation.

## Expected outputs

All outputs are written to the migration bundle (`design-migration/<design-id>/components/<component-id>/`):
- `build-report.json`: Sealed handoff conforming to `build-report.payload.schema.json`.
- `build-report.md`: Comprehensive completion and verification report.
- Site-Package Changes: Creates or updates Content Blocks, templates, partials, or StyleX definitions strictly within the authorized site package (e.g. `packages/site_theme/`). Never modifies `vendor/` or remote repositories.

## Example prompts

- **Configure / reuse an existing Hero:** "Implement the Hero component specified in `design-migration/site/components/hero/component-spec.json`. Assess the installed Astryx Hero element, configure its styling tokens in `packages/site_theme`, and verify computed styles match the mockup within ±1px."

- **Extend Astryx Card with metadata:** "We need to build the card in `design-migration/site/components/card/component-spec.json`. Astryx Card matches except for a missing editorial badge field. Extend the Card in `packages/site_theme`, verify FAL image handling, and test keyboard navigation."

- **Compose a section with a container:** "Implement the 3-column feature section from `design-migration/site/components/feature-grid/component-spec.json` using an Astryx Container, verify allowed child elements, and check responsive layout transitions at 767px and 768px."

- **Map component design to inherited styles and global tokens:** "Implement the card from its component spec. Identify the selected Content Block and trace its active inherited styling. Compare every analyzed design requirement with inherited values and the global `design-system.json`; record matching global tokens and exact component-specific token IDs/values needed before editing, then implement and verify the full appearance."

## Installation

This skill is bundled in the plugin and can also be installed as a standalone skill directory. Keep its `references/`, `templates/`, and `scripts/` alongside `SKILL.md`.

## Validation

Validate any generated `build-report.json` using the bundled Python script:

```bash
python3 scripts/validate_handoff.py validate design-migration/<design-id>/components/<component-id>/build-report.json
```

To recompute digests and seal the build report:
```bash
python3 scripts/validate_handoff.py seal design-migration/<design-id>/components/<component-id>/build-report.json
```

## Related skills

- [`typo3-design-system-extract`](../typo3-design-system-extract/README.md) — extract global design tokens and site-wide foundations.
- [`typo3-component-analyze`](../typo3-component-analyze/README.md) — describe a component before implementation.

## License

This skill is distributed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](../../LICENSE). Upstream extensions (`skom/typo3-astryx`, `skom/stylex-connector`) remain under their respective licenses.

