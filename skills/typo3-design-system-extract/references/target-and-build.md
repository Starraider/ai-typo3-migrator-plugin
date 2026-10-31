# Target preflight and build

Versions below come from upstream revisions inspected on 2026-10-31. They are research anchors. Read the project's installed versions (`composer.lock`, `composer show`, `package.json`, lockfiles) and re-read the extensions' own `composer.json` before deciding.

## 1. Supported target (14.3.x only)

Constraints observed for `skom/typo3-astryx`:

| Requirement | Constraint |
| --- | --- |
| TYPO3 | `~14.3.0` |
| PHP | `>=8.3 <8.5` |
| Content Blocks | `^2.4.10` |
| Container (`b13/container`) | `^4.1` |
| `skom/stylex-connector` | `^1.1.2` |
| Vite Asset Collector | `^1.18` |
| Conflicts | `typo3/cms-fluid-styled-content` |

The connector alone lists wider TYPO3 support (12.4, 13.4, 14.3). That does not make Astryx work on those versions.

Outcomes (record as `targetCompatibility.status` plus per-check results):

| Situation | Status | Behavior |
| --- | --- | --- |
| TYPO3 14.3.x, constraints met, no conflict | `supported` | Target steps allowed after permission. |
| TYPO3 13 or other than 14.3 | `unsupported` | Source extraction continues; target steps `blocked`. Do not claim TYPO3 13 support or upgrade TYPO3. |
| FSC installed or required | `conflict` | Stop target-touching steps and ask; non-interactive: target steps `blocked`. |
| Versions unreadable | `unknown` | `versionsKnown: false`; no target edits. |

## 2. Fluid Styled Content conflict

Detect FSC in `composer.lock` (`packages` and `packages-dev`), `composer.json` `require`, and the extension list. Report:

- the conflict (Astryx declares `conflict` with `typo3/cms-fluid-styled-content`; Composer will refuse resolution);
- the rendering implication: existing FSC content elements, templates and TypoScript would need a rendering-stack migration;
- options for the user (for example: stop here, treat the target as a separate migration project, or provide a different project without FSC).

Interactive: ask, record the gate in `decisions` with `effect: binding`. Non-interactive: record `target.conflicts`, an `unresolved` entry (`readinessEffect: blocked`), set readiness `blocked`; read-only extraction continues. Never remove FSC, loosen constraints, or migrate content on your own.

## 3. Project conventions

Before adding anything, read: package manager and lockfile, DDEV or other environment instructions, existing Vite config, site-package layout, TypoScript/site-set asset loading, browser support. Use the project's own commands (for example `ddev composer`, `ddev npm`). Ask before installing or upgrading packages.

## 4. Astryx asset modes

Astryx ships packaged assets and supports a consuming-project Vite mode. Identify the mode in use from the installed documentation and site settings, record it in `foundation.assetMode`, and make sure the same stylesheet is not loaded twice. Follow the layered build; do not copy connector examples designed for unlayered legacy CSS.

## 5. Vite entrypoints

- Add or confirm entrypoints in the site package for the style modules; every module that defines or consumes StyleX styles must be reachable from an actual entrypoint.
- Use package-qualified stable keys; avoid basename collisions between modules.
- Use the existing StyleX unplugin and the maintained connector adapter; do not write a replacement bridge or hard-code generated class names in Fluid.

## 6. Two manifests

| Manifest | Resolves | Typical check |
| --- | --- | --- |
| Vite manifest (`.vite/manifest.json`) | entrypoint to emitted files | each entrypoint present, file exists |
| StyleX manifest | semantic style key to class recipe | every key referenced from Fluid is present |

Confirm both exist and belong to the same build. The connector's v2 format carries a CSS hash; compare it with the emitted CSS and honor the integrity checks the installed connector supports. CSS present but a referenced style key missing or belonging to another build is a **failed** check; name both inconsistent outputs.

Build and deploy CSS, StyleX manifest and Vite manifest as one release unit. Atomic JSON writes do not make a separate CSS publication atomic.

## 7. Development loading

TYPO3 owns the HTML document, so verify development stylesheet loading (Vite dev server through Vite Asset Collector, correct origin and HMR) as well as production CSS. If a dev server cannot run, mark the dev check `not-run`.

## 8. `styles:` ViewHelper limits

The class ViewHelper takes `styles:`. It supports static conflict maps and complete class recipes, not arbitrary runtime class-plus-variable style functions. Do not concatenate independently resolved recipes expecting conflict resolution. Choose one complete recipe per slot, or compose supported static maps. Use a site-package-owned adapter only for a specifically evidenced dynamic-value need. Check the installed ViewHelper before using any example API.

## 9. Gaps

An upstream capability gap is reported with a concrete recommendation. Never patch `vendor/` or the extension.
