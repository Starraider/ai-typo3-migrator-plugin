# Token Mapping Ledger Template

Use this template to track token discovery, confidence level, and mapping status onto installed Astryx properties.

## Instructions
1. Inspect installed `vendor/skom/typo3-astryx/Resources/Private/JavaScript/Stylex/tokens.stylex.js`.
2. Map source tokens to public `--astryx-*` properties where semantic roles align.
3. If an extracted design token has no Astryx equivalent, create a project-owned `--brand-*` token in the site package.
4. Record discrepancies where upstream documentation conflicts with installed source.

| Source ID | Source Value | Rendered Value | Source Location | Confidence | Astryx Target Property | Mapping Status | Mapping Rationale / Discrepancy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `color.primary` | `#0b5fff` | `rgb(11, 95, 255)` | `src/index.css:14` | observed | `--astryx-color-primary` | mapped | Exact match to installed token |
| `spacing.hero` | `clamp(2rem, 5vw, 4rem)` | - | `src/styles/hero.css:8` | observed | `--brand-spacing-hero` | project-token | Fluid formula not supported in standard Astryx scale |
| `radius.card` | `12px` | `12px` | `tailwind.config.js:22` | observed | `--astryx-radius-medium` | mapped | Matches Astryx md radius |

