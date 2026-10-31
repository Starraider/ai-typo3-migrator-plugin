# Token mapping onto Astryx

Map extracted global values onto the **installed** Astryx extension. Upstream file names and examples named in this skill are research anchors; inspect the versions actually installed in the target before relying on any name, selector or value.

## 1. Installed source beats documentation

1. Locate the installed extension (`vendor/skom/typo3-astryx/` or the path `composer show -P` reports).
2. Read the token source (`Resources/Private/JavaScript/Stylex/tokens.stylex.*` in the inspected revision), theme sources and the compiled CSS, not just the styling guide.
3. Build the list of real public properties (`--astryx-*`) and their scopes from that source.
4. Where documentation names a token or value that the source does not declare, use the source, set `mapping.discrepancy` to a short description ("docs: `--astryx-color-primary`; installed: not declared"), and never emit a reference to a nonexistent token.
5. Record the installed Astryx version and the files read in the evidence ledger.

Without an installed copy (analysis-only run with no target), mark mappings `unmapped` with rationale "target not inspected" and set `target.versionsKnown: false`. Do not map against remembered or documented names.

## 2. Mapping rules

- Map by semantic role (accent, surface, text, border, radius-card, space-section), not by nearest value alone. A color that merely resembles an Astryx color but plays another role is not a match.
- Statuses: `mapped` (same role exists), `project-token` (no equivalent; add a brand token), `unmapped` (undecided or blocked), `conflict` (two plausible targets or a source disagreement).
- Keep: source token, source location, value, rendered value, target property, conversion (unit change, `rem` to `px`), rationale, scope.
- Keep exact values. Do not round or snap to the Astryx scale without recording the resulting design change; if snapping is proposed, record it as a decision.
- Preserve fluid formulas (`clamp()`), units and responsive changes.

## 3. Project-owned StyleX tokens

- Define extracted project values in the site package as StyleX variables with a project namespace, `--brand-*` (for example `--brand-space-section`).
- Reuse suitable Astryx tokens directly in component styles instead of duplicating them.
- Point public `--astryx-*` properties at project values through the supported branding layer, using scoped aliases: the alias lives where the active theme declares its value.
- Never declare the same globally named variable from two independent `defineVars` sources; one source of truth per name.
- If a small CSS bridge is needed to emit aliases, generate it from the mapping so it is not a second hand-maintained list of values.
- Never edit Astryx default token files or replace its theme system.

## 4. Theme scopes and layers

- Astryx orders CSS in layers; in the inspected revision the order includes a `product` layer for project-level overrides. Read the installed layer declaration and place branding overrides in the layer intended for them.
- **Nested theme pitfall:** a declaration on `:root` does not beat a child element's own declaration just because of layer priority. If a theme scope such as `[data-theme="x"]` or a section class declares the variable itself, override at that same scope (or deeper). Check every scope the mockup uses (page, section, card) and record which selector carries each value.
- Record themes and modes in `themes` with selector and mode. Do not invent a dark mode or a mobile palette that the reference does not show.
- **New theme registration:** a new theme name needs a verified selection path (site setting, content field option or TypoScript, whichever the installed Astryx documents and implements). Adding a CSS selector alone does not show that editors can select it; mark `selectable: unverified` until a rendered check proves the path.
- Verify inheritance with computed styles at the nested element, not only at `body`.

## 5. Fonts

- For each font: family, weights, styles, files, license/rights, status.
- `available`: files exist in the site package and rights are stated. `unavailable` or `rights-unknown`: record an unresolved dependency; a proposed substitute is `substitution-proposed` and counts as a visual difference that needs a decision.
- Load fonts from the site package (`@font-face` with `font-display`, preload for the critical weight). Do not hotlink a font CDN unless the user states it is intended and allowed.
- Confirm in the render that the intended family is used, not a fallback (`document.fonts.check`, computed `font-family`, loaded font list).

## 6. Base styling

Tokens alone do not reproduce a site. Inventory and carry over: body typography and line-height, heading scale, link styles, global element styles, reset adjustments, selection and focus styles, scroll behavior, and container/layout widths. Put them in site-package styles consumed through the same build, keeping them in the intended layer.

## 7. Editor and preview consistency

Backend editing and preview must receive the same token delivery as the frontend: confirm how the installed Astryx loads its stylesheet in the TYPO3 backend preview and that project tokens, fonts and theme scopes reach it. If preview does not receive them, record it as a gap; do not assume parity.

## 8. Media-query constants limitation

Breakpoint and query values must be compile-time constants that the StyleX compiler supports. CSS custom properties cannot appear inside media-query conditions. Record each breakpoint as a literal query with its confidence; derive intermediate "layout transition" widths from observed behavior, not from a guessed scale.

Use the [token-mapping ledger](../templates/token-mapping-ledger.md) to record each decision.
