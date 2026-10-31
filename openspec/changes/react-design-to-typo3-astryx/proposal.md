# Proposal

## Why

React mockups from Lovable or Stitch contain useful design and behavior evidence, but converting them into an editable TYPO3 website currently requires repeated manual analysis. Three portable skills will make that process repeatable while using the existing StyleX Connector and TYPO3 Astryx integration and preserving the mockup's appearance and responsive behavior.

## What Changes

- Add `typo3-design-system-extract` to extract global design values, map them onto Astryx tokens, and establish a site-package foundation using Vite and StyleX Connector.
- Add `typo3-component-analyze` to describe a selected component's structure, variants, editorial content, assets, interactions, and responsive rules without implementing its replacement.
- Add `typo3-component-build` to assess existing Astryx components and content elements, then configure, compose, extend, or create the smallest suitable implementation and verify its visual and functional behavior.
- Define versioned handoffs with source provenance, token mappings, component specifications, asset manifests, reference captures, and explicit evidence gaps so skills can run independently and detect stale inputs.
- Support TYPO3 14.3.x initially with `skom/stylex-connector` and `skom/typo3-astryx`. Defer TYPO3 13 support and require compatibility checks before target-project changes, including Astryx's conflict with Fluid Styled Content.
- Provide per-skill documentation, focused references/templates, representative and boundary evaluations, and concise plugin-level discovery documentation.
- Record an MCP assessment: use existing Stitch tools and exported/local source first; use scripts or a CLI for repeatable processing and CI. Do not bundle a custom MCP server initially.

## Capabilities

### New Capabilities

- `typo3-design-system-extract`: Evidence-backed global design extraction and integration with an Astryx site package through Vite and StyleX Connector.
- `typo3-component-analyze`: Implementation-independent component analysis with a structured TYPO3-oriented content and behavior contract.
- `typo3-component-build`: Reuse assessment, implementation, and verification of mockup components using installed Astryx capabilities.

### Modified Capabilities

None. The project currently has no main OpenSpec capability specifications, and existing migration skills retain their behavior.

## Impact

The implementation will add three immediate child directories under `skills/` and update relevant plugin documentation and descriptive metadata. Existing skills and their dependencies remain unchanged. Each skill must be self-contained for standalone installation.

Runtime consumers need source evidence and, for implementation, a compatible TYPO3 14.3.x project/site package with Astryx, StyleX Connector, and their required dependencies. Browser tooling is required to verify rendered parity; missing source states or unavailable browser execution must be reported rather than treated as success. No particular mockup or target TYPO3 installation is supplied in this repository, so this change delivers reusable skills and evaluation fixtures, not a completed website migration.

Upstream extension changes, TYPO3 upgrades, bulk content/data migration, deployment automation, a shared asset service, and a custom MCP server are outside the initial implementation scope. An upstream capability gap is reported with a concrete recommendation rather than silently patched in a dependency.
