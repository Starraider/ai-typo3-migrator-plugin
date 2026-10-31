---
name: typo3-design-system-extract
description: Extract the global design system (colors, typography, spacing, radii, shadows, motion, layout widths, breakpoints, themes, fonts, assets) from a React/Tailwind mockup, URL, Stitch design, export, or screenshots; combine available sources, map values to installed Astryx tokens, and optionally build a TYPO3 14.3 site-package foundation with StyleX Connector and Vite. Use for site-wide extraction before components. Do not use for one component, section, or page.
license: CC-BY-4.0
compatibility: Analysis needs readable mockup resources and Python 3.8+; URL sources require the internal browser, and Stitch-MCP is optional. Target changes need TYPO3 14.3.x, skom/typo3-astryx, skom/stylex-connector, Composer, Node.js, Vite, and permission to edit the site package. Unavailable checks are reported as not-run.
---

# TYPO3 Design-System Extraction

Extract the global design of a mockup into evidence-backed tokens, map them onto the installed Astryx tokens, and optionally establish a site-package foundation through the existing StyleX Connector and Vite. Output a sealed `design-system` handoff that later per-component work can consume. Never claim live TYPO3 parity unless a rendered comparison actually ran.

Scope boundary: global values only. A request to analyze or build one component, section or page belongs to a component-level skill (`typo3-component-analyze`, `typo3-component-build`); mention them but do not do their work.

Read these on demand, not up front:

- [Source intake](references/source-intake.md) — formats, MCP and tool guidance.
- [Evidence ledger](references/evidence-ledger.md) — observed / inferred / unknown rules.
- [Token mapping](references/token-mapping.md) — Astryx mapping, scopes, fonts, base styles.
- [Target and build](references/target-and-build.md) — 14.3.x constraints, Vite, manifests.
- [Verification](references/verification.md) — foundation checks and the fidelity gate.
- [Handoff contract](references/handoff-contract.md) — envelope, decisions, validator.
- Templates: [design-system report](templates/design-system-report.md), [token-mapping ledger](templates/token-mapping-ledger.md), [sealed example](templates/design-system.example.json).

## 1. Resolve scope and destination

Decide and state before reading anything in depth:

- **Mode:** `analysis-only` (report and handoff only) or `implementation` (also edit the site package). Default to `analysis-only` unless the user explicitly asks for target changes. "Token report", "extract", "what are the values" mean analysis-only.
- **Bundle path:** reuse a supplied bundle, else propose `design-migration/<design-id>/` and report it. Write only there (plus the site package in implementation mode, after preflight).
- **Mockup source is read-only.** Never modify it, and never modify a remote design (Stitch, Lovable, Figma) as a side effect.

Completion: mode, bundle path and `design-id` are stated.

## 2. Source intake

Inventory every available input and record identity (digest, commit or revision; mark `unavailable` explicitly): React/TSX, Tailwind config, CSS files and custom properties, Stitch exports/HTML, screenshots, assets, and running references. Treat them as one composite reference set: combine complementary evidence, use the evidence best suited to each claim, and preserve disagreements instead of silently choosing one source. See [source intake](references/source-intake.md).

- For every supplied URL, inspect the rendered design in the internal browser and save representative screenshots into the migration bundle. Record the final safe URL, viewport, page state and capture time; do not mutate the remote page. If the browser cannot reach it, record the failure and continue with the other resources.
- For a Stitch URL or project/screen reference, optionally use available Stitch-MCP read tools to retrieve its existing screen HTML, screenshots and design-system data. Keep Stitch access read-only; never create, edit or delete remote designs. Local exports remain valid sources.
- Use Lovable local or GitHub source. Use a local asset manifest and TYPO3 FAL for assets.
- Validate by running the validator script directly, locally and in CI.
- Do not create a custom MCP server, install services, add credentials, or deploy.
- If a tool is unavailable, accept supplied exports and record what could not be checked.

Completion: every URL, screenshot, source-code tree and other artifact has a separate `sources` entry with its locator and identity, or an explicit `unavailable`; screenshots are stored in the bundle and linked to their URL/state. The combined set and any source conflicts are summarized in the report.

## 3. Evidence ledger

Classify every conclusion as `observed` (read from source or measured in a render), `inferred` (derived rule, e.g. a spacing scale from several values) or `unknown` (not determinable). Never invent values, fonts, breakpoints or states. Reconcile declared styles with rendered output when a running reference exists. Screenshot-only evidence yields approximate values, unknown fonts/breakpoints/states, and readiness `incomplete`. See [evidence ledger](references/evidence-ledger.md).

Completion: every token, font and breakpoint carries a confidence; gaps are in `unresolved`.

## 4. Global inventory

Inventory colors, typography, spacing, borders, radii, shadows, motion, layout widths, grids, breakpoints, fluid sizing (keep `clamp()` expressions), global styles, themes and modes, fonts, assets.

- Keep nearby but different values (e.g. 14px, 15px, 16px) with their evidence. Do not snap them to an assumed scale without documenting the design change.
- Separate shared values from component-specific exceptions; note exceptions for later component work instead of tokenizing them.
- Record fonts with availability and rights: `available`, `unavailable`, `rights-unknown`, `substitution-proposed`. Propose a substitution only as a proposal; never silently swap.
- Record assets with ownership (`site-package` or `fal-editorial`), checksum and rights.

Completion: [token-mapping ledger](templates/token-mapping-ledger.md) lists every value with evidence.

## 5. Target preflight (implementation mode, or when a target is named)

Inspect the actual project; do not assume versions. Details in [target and build](references/target-and-build.md).

1. Read installed versions from `composer.lock`/`composer show`: TYPO3, PHP, `skom/typo3-astryx`, `skom/stylex-connector`, Content Blocks, Container, Vite Asset Collector.
2. Supported target is **TYPO3 14.3.x only**. For TYPO3 13 or anything else: mark `targetCompatibility.status: unsupported`, keep source extraction going, mark target steps `blocked`. Never claim TYPO3 13 support and never upgrade TYPO3.
3. Astryx conflicts with `typo3/cms-fluid-styled-content` (FSC). If it is installed or required:
   - Describe the conflict and its rendering implication (existing FSC content elements and templates would be affected).
   - **Stop all target-touching steps and ask** the user how to proceed. Record the gate in `decisions`.
   - Never remove FSC, edit Composer constraints to bypass the conflict, or migrate content as an implicit step.
   - **Non-interactive run:** mark target-touching steps `blocked`, record `target.conflicts` and an `unresolved` entry with `readinessEffect: blocked`, and continue read-only extraction.
4. Check PHP, Content Blocks, Container, connector and Vite Asset Collector against the installed Astryx constraints. A connector that supports more TYPO3 versions does not prove Astryx compatibility.
5. Follow existing package-manager and environment conventions (DDEV, Composer, npm/pnpm lockfile).
6. Reuse an answered decision from a prior handoff instead of asking again unless its binding requirements changed.

Completion: `targetCompatibility` has per-check results; blockers are recorded.

## 6. Map tokens onto installed Astryx tokens

Open the **installed** Astryx token source in `vendor/` or the extension directory; installed source beats documentation. Map by semantic role; record discrepancies between docs and source. Keep source token, target property, value, conversion and rationale per token. Account for theme scopes and layers. Add project-owned `--brand-*` StyleX tokens for values without an Astryx equivalent. See [token mapping](references/token-mapping.md).

Status per token: `mapped`, `project-token`, `unmapped`, `conflict`. Never edit files in installed dependencies.

Completion: every token has a mapping status; discrepancies and conflicts are listed.

## 7. Site-package foundation (implementation mode only)

After preflight passes and edits are authorized:

- Use the existing StyleX Connector and Vite; do not write a replacement bridge.
- Put project tokens, theme scopes, fonts and base styles in the site package. Never modify installed dependency files.
- Choose the Astryx asset mode that the installed version documents and the project uses; wire Vite entrypoints for development and production.
- Ask before running installs or writing build output the user did not authorize. Do not upgrade packages without asking.
- An upstream gap is reported with a concrete recommendation, not patched in a dependency.

Completion: build runs, both manifests exist, entrypoints load in development and production.

## 8. Verify

Run what is available; see [verification](references/verification.md). Foundation checks: build success, CSS hash matches the StyleX manifest, required style keys present, entrypoints in the Vite manifest, fonts load. Rendered checks: computed styles and layout are the hard gate (±1px geometry; exact typography, color, spacing); screenshots are advisory.

An unavailable check is `not-run` with a reason, never `passed`. A CSS/style-manifest mismatch is `failed`. Do not set `foundation.status: verified` while any verification is `failed` or `not-run`.

Completion: every check has a status and reason; remaining differences are listed.

## 9. Produce and seal the handoff

1. Write `design-system.json` (payload per [contract](references/handoff-contract.md)) and `design-system.md` from the [report template](templates/design-system-report.md). The JSON is authoritative; the report adds no facts.
2. Record every decision gate in `decisions`. An unanswered gate goes into `unresolved` and prevents `ready`.
3. Set `readiness`: `ready` only with nothing unresolved and no failed verification; `incomplete` for missing evidence; `blocked` for unsupported target or FSC conflict that prevents the requested work.
4. Seal and validate:

```bash
python3 scripts/validate_handoff.py seal design-migration/<design-id>/design-system.json
python3 scripts/validate_handoff.py validate design-migration/<design-id>/design-system.json
```

Fix every error. Exit 2 means stale or unknown freshness: report it. A changed token mapping or source digest changes `revision`, so dependent component work must reassess.

Completion: validator exits 0 (or the reason for 2 is reported), report and JSON agree.

## 10. Side effects and scope rules

- Analysis-only: write only the bundle files. No installs, no site-package edits, no Composer changes.
- Implementation: edit only the site package after preflight; run installs or builds only with permission.
- Never write to the mockup source, remote designs, installed dependencies, or outside the resolved destination.
- No deployment, publishing, or baseline replacement.
- Final message: state mode, files written, readiness, `not-run` checks, blocked steps, and open decisions. Do not describe the result as verified TYPO3 parity unless a rendered comparison passed.
