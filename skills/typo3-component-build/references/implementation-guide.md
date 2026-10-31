# Site-Package Implementation Guide

This guide details the technical implementation rules for Astryx and StyleX Connector adaptations inside a TYPO3 site package.

## 1. Extension Ownership & File Locations

All project-specific adaptations must reside strictly in the site package (e.g. `packages/site_theme/`). Never edit files inside `vendor/` or Composer-managed extensions.

- **Content Blocks:** `packages/site_theme/ContentBlocks/ContentElements/<element-name>/`
  - `config.yaml`: Editor fields, TCA definitions, and icon mappings.
  - `EditorInterface.yaml`: Backend form layout and palette grouping.
  - `Frontend.html`: Fluid template rendering the element.
- **Fluid Components:** `packages/site_theme/Resources/Private/Components/`
- **Partials & Layouts:** `packages/site_theme/Resources/Private/Partials/`
- **StyleX Definitions:** `packages/site_theme/Resources/Private/JavaScript/Stylex/`

## 2. Safe Content Extension & FAL Media

When extending an existing Astryx element (e.g., adding a metadata badge to Card):
- **Preserve Existing Identifiers:** Retain the base CType and database table (`tt_content`).
- **Native Fields:** Define the new property in the site package's Content Block extension YAML:
  ```yaml
  fields:
    - identifier: badge
      type: Text
      label: 'Badge / Tag'
  ```
- **FAL Relations:** Editorial images must use native TYPO3 File Abstraction Layer (FAL) references:
  ```yaml
  fields:
    - identifier: image
      type: File
      label: 'Card Image'
      maxitems: 1
      allowed: ['jpg', 'png', 'webp', 'svg']
  ```
- **Never Hard-Code Mockup Strings:** Templates must bind to Fluid variables (`{data.badge}`, `{data.header}`), never static strings from the React mockup.

## 3. StyleX Connector & Semantic Class Lookup

Astryx delivers compiled CSS via `skom/stylex-connector`.

- **Class Lookup ViewHelper:** Use `<stylex:class styles="{styles.root}" />` to resolve semantic style objects into compiled hash classes.
- **Delivery Integrity:** Ensure Vite compiles all referenced style modules into the build entrypoint. If a style key is used in Fluid but absent from `Resources/Public/stylex-manifest.json`, the build is incomplete.
- **Static vs Dynamic:** StyleX Connector maps static style definitions. Do not attempt to pass dynamic runtime styling functions directly to the ViewHelper; use static style variants or project CSS custom properties.

## 4. Finite Recipe Limits & Upstream Capability Gaps

Astryx's `RecipeViewHelper` is implemented as a final PHP class with a hard-coded allowlist of recipe keys (e.g. `vertical`, `horizontal`).
- **No Nonexistent APIs:** Do NOT attempt to register new recipe keys via TypoScript, event listeners, or subclassing, as the core class does not expose dynamic extension hooks.
- **Clean Site-Package Adaptation:** When a mockup requires an unsupported layout recipe:
  1. Define a site-package StyleX style object or utility class in `Resources/Private/JavaScript/Stylex/`.
  2. Bind this class directly in your site-package template override using the connector.
- **Reporting an Upstream Gap:** If a clean adaptation cannot be achieved without core changes, do not hack the vendor directory. Report the gap in the build report with a concrete recommendation for upstream contribution.

