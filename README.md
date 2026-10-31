# AI TYPO3 Migrator Plugin

`ai-typo3-migrator-plugin` is an Agent Plugins 1.0.0 package containing portable Agent Skills for TYPO3 upgrades, extension migrations and site-package consolidation. It has no bundled MCP servers.

## Use cases

- Plan TYPO3 upgrade paths (sequential, rebuild, hybrid).
- Migrate from TYPO3 v11 → v12, v12 → v13, and v13 → v14.
- Consolidate multiple site packages into a single extension.
- Migrate legacy or custom CSS site-package themes to Tailwind CSS v4 in DDEV.
- Recreate Gridelements layouts as Container CTypes and migrate content relations.
- Analyze extension compatibility and deprecations.
- Generate migration strategies and change-management summaries.
- Extract global design systems from React or Stitch mockups and establish TYPO3 14.3 site-package foundations with Astryx and StyleX Connector.
- Analyze React mockup components into structured, implementation-independent TYPO3 specifications.
- Implement and verify mockup components in TYPO3 14.3 using Astryx reuse, container composition, or site-package extension.

## Installation

- [Install the complete Agent Plugin](plugin-installation.md) in Codex, Cursor,
  GitHub Copilot, or Visual Studio Code.
- [Install individual Agent Skills](skill-installation.md) in Antigravity,
  OpenCode, Windsurf, Zed, Trae, or Qoder.

## Skills

- [TYPO3 upgrade strategy analysis](skills/typo3-upgrade-strategy-analysis/README.md) compares sequential upgrades, a clean rebuild, and a hybrid migration between user-specified TYPO3 versions, then writes one strategy report.
- [TYPO3 v11 to v12 upgrade](skills/typo3-v11-to-v12-upgrade/README.md) — analyze, plan, and execute a staged TYPO3 11.5 to 12.4 migration.
- [TYPO3 v12 to v13 upgrade](skills/typo3-v12-to-v13-upgrade/README.md) — safely move a Composer-based TYPO3 12.4 project to TYPO3 13.4.
- [TYPO3 v13 to v14 upgrade](skills/typo3-v13-to-v14-upgrade/README.md) — assess blockers and complete a controlled TYPO3 13 to 14 migration.
- [Merge TYPO3 site packages](skills/typo3-merge-sitepackages/README.md) — consolidate two TYPO3 site packages into one target extension.
- [TYPO3 Gridelements to Container](skills/typo3-gridelements-to-container/README.md) — recreate used Gridelements layouts as Container CTypes and migrate their content relations with a dry-run-first database command, including Gridelements 8.7.0 data.
- [TYPO3 Tailwind CSS migration](skills/typo3-tailwind-migration/README.md) — migrate a TYPO3 site package from legacy or custom CSS to Tailwind CSS v4 in DDEV with visual regression baselines.
- [TYPO3 Design-System Extraction](skills/typo3-design-system-extract/README.md) — combine mockup URLs, React/Stitch sources, screenshots, and artifacts to extract global tokens, map installed Astryx tokens, and optionally build a TYPO3 14.3 foundation.
- [TYPO3 Component Analysis](skills/typo3-component-analyze/README.md) — combine URLs, source code, screenshots, Stitch designs, and artifacts to describe a component's complete visual design and TYPO3 content model without implementing it.
- [TYPO3 Component Building](skills/typo3-component-build/README.md) — implement and verify a specified mockup component in TYPO3 14.3 via Astryx reuse, container composition, or targeted site-package adaptation.

## React Mockup to TYPO3 14.3 Astryx Workflow

For teams modernizing or building TYPO3 14.3 websites from React mockups (Lovable, Stitch, Figma), the plugin provides a structured three-stage pipeline linked by machine-validated JSON handoff contracts:

1. **Global Extraction (`typo3-design-system-extract`):** Combines URLs, React/CSS source, screenshots, Stitch exports and other artifacts to analyze global colors, typography, spacing, breakpoints, and themes. Supplied URLs are inspected and captured in the internal browser. Outputs `design-system.json`.
2. **Component Analysis (`typo3-component-analyze`):** Combines rendered URL evidence, source files, screenshots, Stitch artifacts and other resources to specify a selected component's complete visual design, structure, editorial model, assets, and responsive/interaction behavior. It records component-specific design without comparing against global tokens. Outputs `component-spec.json`.
3. **Component Building (`typo3-component-build`):** Traces the selected element's inherited styling, compares it with the global design-system handoff, identifies component-specific tokens, evaluates installed Astryx elements before writing code following a strict disposition order (Configure → Compose → Extend → Create), verifies parity against a hard computed style/layout gate (±1px geometry), and produces `build-report.json`.

### MCP & Source Intake Guidance

- **URLs:** Inspect supplied mockup URLs in the internal browser and save representative screenshots in the migration bundle.
- **Stitch:** Optionally use Stitch-MCP read tools to retrieve existing screens, HTML, screenshots, and design-system data; keep access read-only. Local exports also work.
- **Combined sources:** Treat screenshots, URLs, code, and other artifacts as one reference set. Record each resource separately and preserve disagreements as evidence.
- **Lovable:** Inspect local workspace files or cloned GitHub repositories.
- **Assets:** Manage image references via local manifests and TYPO3 FAL without requiring remote CDN credentials.
- **Validation:** Run deterministic Python validation scripts (`validate_handoff.py`) directly locally and in CI. No custom MCP server, daemon, background service, or deployment action is introduced.

## Package layout

Compatible Agent Plugins clients discover the skills from immediate child directories of `skills/`. Each skill is self-contained and includes runtime instructions, supporting references, a detailed README, and representative/edge-case/boundary evaluation prompts. The `agents/openai.yaml` files retained within skill directories are optional client-specific display metadata; they are not part of the portable Agent Plugins core.

The package declares Agent Plugins schema version 1.0.0 in [plugin.json](plugin.json). Installation, enablement, permissions, and client-specific presentation are managed by the consuming client.

## License

This project and all contained Agent Skills are licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).
