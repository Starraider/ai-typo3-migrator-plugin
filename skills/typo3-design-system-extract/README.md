# TYPO3 Design-System Extraction

Extract the global design system (colors, typography, spacing, radii, shadows, motion, layout widths, breakpoints, themes, fonts, assets) from a mockup URL, React/Tailwind source, Stitch design or export, screenshots, and related artifacts. Combine the available resources, map values onto installed Astryx tokens, and optionally build a TYPO3 14.3 site-package foundation with StyleX Connector and Vite.

## What this skill solves

React mockups from tools like Lovable, Stitch or Figma contain rich design specifications. Manually translating these into TYPO3 site-package configurations often results in inconsistent tokens, missing font declarations, broken media queries, and broken layer ordering.

This skill automates and structures the global design extraction:
- Reconciles declared CSS and Tailwind variables with rendered evidence.
- Opens supplied URLs in the internal browser and captures representative desktop/mobile screenshots into the migration bundle.
- Combines URLs, screenshots, source code, Stitch exports/design-system data, and other artifacts into one traceable reference set, preserving disagreements as evidence.
- Maps discovered tokens onto installed `skom/typo3-astryx` public tokens, documenting discrepancies.
- Defines project-owned StyleX tokens (`--brand-*`) for values unique to the mockup.
- Sets up or verifies the site-package Vite configuration, StyleX Connector integration, and dual manifests.
- Produces a machine-validated, versioned `design-system.json` handoff and readable `design-system.md` report.

## Use when

- At the start of migrating a React or Stitch mockup to TYPO3 14.3 with Astryx.
- To audit, extract, and reconcile global design tokens without modifying code (`analysis-only` mode).
- To initialize the StyleX Connector and Vite asset foundation in a TYPO3 site package.

## When NOT to use

- Do not use for analyzing or implementing individual components, cards, menus, or sections. Use `typo3-component-analyze` and `typo3-component-build` instead.
- Do not use for migrating legacy CSS or Gridelements in older TYPO3 versions. Use `typo3-tailwind-migration` or `typo3-gridelements-to-container`.
- Do not use on TYPO3 13 or older; Astryx requires TYPO3 14.3.x.

## Context requirements

- **Analysis mode:** At least one readable mockup resource: source code, an export, a screenshot, or a URL accessible through the internal browser. Python 3.8+ for the handoff validator. Stitch-MCP is optional.
- **Implementation mode:** A TYPO3 14.3.x project with Composer, `skom/typo3-astryx` (~14.3.0), and `skom/stylex-connector` (^1.1.2). Node.js and Vite in the frontend workspace.
- **FSC Check:** `typo3/cms-fluid-styled-content` must NOT be installed, as it conflicts with Astryx.

## Expected outputs

All outputs are written to the resolved migration bundle directory (default: `design-migration/<design-id>/`):
- `design-system.json`: Versioned, sealed JSON artifact conforming to `envelope.schema.json` and `design-system.payload.schema.json`.
- `design-system.md`: Comprehensive human-readable report.
- In implementation mode: Site-package StyleX token definitions, font assets, and Vite configuration.

## Side Effects

- In `analysis-only` mode: Reads mockup files and remote pages, captures screenshots for supplied URLs into the migration bundle, and generates the handoff. Remote pages and Stitch designs are read-only.
- In `implementation` mode: Edits only the designated site package. Never modifies vendor code, composer dependencies, or mockup sources.

## Example prompts

- **URL-based extraction:** "Analyze the design system at `https://example.test/landing`. Use the internal browser to capture desktop and mobile screenshots, inspect the rendered design, and extract global colors, spacing, typography, and layout rules into a migration bundle."

- **Combined resources:** "Combine `frontend/mockup/src`, `exports/stitch/`, the reference screenshots, and `https://example.test/landing` as one design source set. Inspect the URL in the internal browser, use Stitch-MCP read tools if available, reconcile any differences, and produce an analysis-only handoff."

- **Foundation implementation:** "We verified the extracted design tokens in `design-migration/corporate-v1/design-system.json`. Please implement the StyleX foundation in `packages/site_distribution`, configure the Vite entrypoints, and verify the StyleX manifest builds cleanly."

## Installation

This skill is self-contained in this directory. For project-level Codex discovery, place or link the directory at `.agents/skills/typo3-design-system-extract/` and keep its `references/`, `templates/`, and `scripts/` beside `SKILL.md`.

## Validation

Validate any generated `design-system.json` using the included Python helper without a provider connection or TYPO3 installation:

```bash
python3 scripts/validate_handoff.py validate design-migration/<design-id>/design-system.json
```

To recompute digests and seal a file:
```bash
python3 scripts/validate_handoff.py seal design-migration/<design-id>/design-system.json
```

## Related skills

- [`typo3-component-analyze`](../typo3-component-analyze/README.md) — analyze one component or section.
- [`typo3-component-build`](../typo3-component-build/README.md) — implement a component from its specification.

### Reference documentation

- [Handoff Contract](references/handoff-contract.md)
- [Source Intake Guide](references/source-intake.md)
- [Evidence Ledger](references/evidence-ledger.md)
- [Token Mapping Reference](references/token-mapping.md)
- [Target & Build Requirements](references/target-and-build.md)
- [Verification Guide](references/verification.md)

## License

This skill is distributed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](../../LICENSE). Upstream extensions (`skom/typo3-astryx`, `skom/stylex-connector`) are subject to their respective licenses.

