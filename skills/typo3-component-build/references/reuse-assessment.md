# Astryx Reuse Assessment Guide

This reference details how to systematically evaluate installed Astryx content elements, components, and recipes before modifying or creating TYPO3 site-package code.

## 1. Candidate Discovery in Installed Astryx

Inspect the actual files located in `vendor/skom/typo3-astryx/` or the installed extension root. Look into:
- `ContentBlocks/ContentElements/`: Definitions, fields, TCA configuration, and partial templates.
- `Resources/Private/Components/`: Native Fluid components and their arguments/slots.
- `Classes/ViewHelpers/`: ViewHelpers such as `RecipeViewHelper`.
- `Resources/Private/JavaScript/Stylex/`: Available component styles and tokens.

Do not rely solely on online documentation or README examples; installed code is authoritative.

## 2. Comparing Capabilities: Content Model vs Component Slots

An element's editorial configuration and its frontend component API are distinct:
- A Content Block defines editorial fields (database columns in `tt_content`), labels, and editor validation.
- A Fluid component defines rendering slots, presentation arguments, and CSS style bindings.

A component may support a rendering slot that the Content Block does not expose to backend editors. In such cases, determine whether a site-package field extension can expose that slot without creating a whole new element.

## 3. Component Inheritance and Design-Token Coverage

Run this assessment after selecting the actual Content Block/content element and before editing target code. Compare the analyzed `payload.design` against the selected implementation's active style chain and the current global design-system handoff.

1. Trace the actual path from the selected Content Block or CType through its Fluid component, selected recipe/variant, imported component styles, active theme, and applicable global rules. Use installed source and current target configuration; do not infer inheritance from a matching token name.
2. For every analyzed design requirement, record which style source applies to the selected element, the effective inherited value when known, and any matching global token IDs. Cite installed file paths, recipe IDs, and active selectors where possible. Distinguish tokens available in the global handoff from tokens actually used by the active style chain.
3. Classify `inheritance` as `full`, `partial`, `none`, or `unknown`:
   - `full`: active inherited styling already meets the analyzed requirement.
   - `partial`: some properties or values match; state the remainder.
   - `none`: the active chain does not provide the requirement.
   - `unknown`: evidence cannot establish the chain or effective value.
4. Classify overall `coverage` separately:
   - `inherited`: active inherited styling meets the full requirement.
   - `global-token`: a matching shared token exists, but the selected element does not currently use it; wire the shared token instead of defining a duplicate.
   - `partial`: inheritance or shared tokens meet only part; record local tokens for the remainder.
   - `component-specific`: no applicable inherited value or shared token exists; identify the needed component-scoped token(s) or explain why a direct component rule needs no token.
   - `unknown`: retain the evidence gap and do not claim coverage.
5. Record one `designCoverage[]` row for each meaningful requirement. Include `targetElement`, analyzed `componentValue`, `inheritance`, `inheritedFrom`, `inheritedValue`, `globalRefs`, `coverage`, `componentTokens`, and evidence. For each tokenizable local value, record its exact ID, value, and status (`required` before implementation; `defined` after adding it). If no component token is needed for a local rule, explain why in the evidence.

For a composed section, assess the container and each selected child element/Content Block independently. Keep the component specification binding: coverage identifies the source for each required value, not permission to omit or change it. Unknown inheritance remains unknown until verified from the active chain.

## 4. The 4-Tier Disposition Hierarchy

Evaluate candidates in this exact precedence order:

```
[1. Configure] ---> [2. Compose] ---> [3. Extend] ---> [4. Create New]
```

### 1. Configure (`configure`)
- **When to choose:** An installed Astryx content element (e.g. `astryx_hero` or `astryx_card`) already possesses the required fields, variants, and behavior. Only color/typography tokens differ.
- **Action:** Configure site settings, map design tokens, or use existing element options.
- **Example:** Reusing the default Astryx Hero element where only the background color and button radius differ from the mockup.

### 2. Compose (`compose`)
- **When to choose:** The mockup component is a composite structure (e.g., a full-width background section containing a heading and three cards).
- **Action:** Compose existing content elements inside an Astryx Container (e.g., `b13/container`), using container columns and layout settings.
- **Example:** A 3-column card section composed using an Astryx Container holding three standard Astryx Card elements.

### 3. Extend (`extend`)
- **When to choose:** An installed element meets 80%+ of the contract, but lacks a specific editorial field (e.g., a metadata tag or author badge) or requires a custom template slot.
- **Action:** Extend the element in the site package via a Content Block extension or template/partial override, preserving native identifiers and relations.
- **Example:** Adding a `badge` string field to `astryx_card` in the site package.

### 4. Create New (`create`)
- **When to choose:** No existing element can fulfill the required data structure or interaction contract without fragile workarounds.
- **Action:** Author a clean, dedicated Content Block or component in the site package.
- **Example:** A complex multi-step interactive calculator or timeline widget with bespoke data structures.

## 5. Recording Rejected Alternatives

For every candidate assessment, document why the other tiers were rejected:
- "Why not Configure? Existing Card lacks the editorial badge field required by the mockup."
- "Why not Create New? Extending the existing Card preserves editorial workflows and reduces code duplication."

