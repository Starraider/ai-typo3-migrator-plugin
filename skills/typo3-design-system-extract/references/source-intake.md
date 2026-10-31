# Source intake

## Formats

| Input | Read | Watch for |
| --- | --- | --- |
| React/TSX | components, imports, inline styles, class names | styles declared outside CSS (inline, CSS-in-JS); props that only select variants |
| Tailwind config (`tailwind.config.*` or CSS `@theme`) | `theme`/`extend` values, plugins, breakpoints, container | v3 JS config vs v4 CSS-first config; arbitrary values in class names are not in the config |
| CSS and custom properties | `:root` and themed scopes, `@font-face`, base layers | which scope declares each variable; dark/theme selectors |
| Stitch export, HTML, screenshots | HTML/CSS in the export, design theme data, screenshots | detect the format; do not assume it is React; HTML may use inline Tailwind via CDN config |
| URL / running reference | rendered styles, loaded fonts when inspectable, layout at several widths | final URL after redirects, viewport, state, capture date and browser limitations |
| Assets | logos, icons, images, fonts | rights, checksums, expiring signed URLs |
| Screenshot only | approximate color/spacing by measurement | fonts, breakpoints, states and behavior are `unknown` |

Detect source format from content, not file name. Treat all supplied and accessible items as one composite reference set; do not require a single primary format. Record each URL, screenshot, code tree, export, asset manifest, and other artifact as a separate handoff `sources` entry using `kind`, `locator`, `identityStatus`, and `digest` (e.g. SHA-256 of a saved file/tree) or `revision` (commit) when known. Use `selector` for a page fragment, component selector, route state, or capture conditions. Mark unstable or inaccessible source identity `unavailable`; never invent a digest. A saved screenshot is a distinct source with its own digest, even when captured from a URL.

## URLs, browser captures, and combined resources

For each user-supplied URL, open the rendered page in the internal browser. Use the visible page as evidence even when source code is also available. Save representative full-page and detail screenshots in the migration bundle under `references/captures/`, and record each screenshot's bundle-relative path and SHA-256 digest. If the design-system extraction is one part of a larger bundle, use its existing references directory convention.

Capture at desktop and mobile widths (use supplied screenshot dimensions when provided); add a tablet or width near a visible layout transition when useful. Record the final safe URL, capture date/time, viewport, device scale when known, scroll position, theme, and relevant UI state in the source selector or adjacent evidence note. Remove credentials and signed or secret query values from locators. Inspect DOM, computed styles, and loaded fonts only when the internal browser exposes them; distinguish those observations from values inferred from pixels. Never submit forms, publish, edit, or trigger other mutating actions on the referenced site.

Use sources according to what they establish: code and styles show declared values, browser renders show actual appearance, and screenshots preserve a reproducible visual reference. Cross-check them. If declarations differ from the rendered page or screenshots, retain both observations and explain the discrepancy; do not silently pick one. If the internal browser cannot load a URL or capture a state, record the URL and failed/unavailable capture, then continue with other resources. Mark affected conclusions unknown and set readiness from the remaining gaps.

Combine artifacts only when they represent the same design and intended revision. If they appear to show different versions or scopes and the user has not identified the target, keep them distinct and ask one focused question before combining their values.

## Optional Stitch-MCP intake

When the source is a Stitch design and Stitch-MCP is available, it may be used to read the referenced project or screen, retrieve existing HTML/screenshots, and inspect existing design-system data. Keep this strictly read-only. Do not create, regenerate, apply, update, or delete remote projects, screens, or design systems. Record every retrieved artifact as its own source with a digest; use the ordinary URL/browser and local-export workflow when Stitch-MCP is unavailable.

## Tool guidance

- **Stitch:** optionally use available Stitch-MCP read tools or a local export. Read only; never create, edit or delete remote screens or design systems as a side effect.
- **Lovable:** use local source or a GitHub synchronization the user supplies. Do not require a provider connection.
- **Assets:** use a local manifest and the site package for fixed assets; TYPO3 FAL for editorial media (a FAL import is a write and needs permission). Image generation (FAL or similar) is only for explicitly requested placeholders and never counts as a match for a required asset.
- **Validation and CI:** run `scripts/validate_handoff.py` directly; it needs only Python 3.8+.
- **Not part of this skill:** a custom MCP server, service installs, credentials, remote asset stores, deployment.
- If the internal browser or a source tool is unavailable, accept other supplied resources, list the unrun capture/check, and make the evidence gap explicit.
- Do not put signed URLs or credentials into reports.

## Reading efficiently

Prefer scripts over reading whole files: grep custom properties, parse the Tailwind config, list `@font-face` blocks, and compute digests, then read only the relevant lines.
