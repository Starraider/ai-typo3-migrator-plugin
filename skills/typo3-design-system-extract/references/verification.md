# Verification

Record each check in the envelope's `verification` array with `id`, `status` (`passed`, `failed`, `not-run`, `not-applicable`), a non-empty `reason`, and the `command` when one ran. An unavailable check is `not-run`, never `passed`. `foundation.status: verified` is invalid while any check is `failed` or `not-run`.

## 1. Foundation checks (implementation mode)

| Check | How |
| --- | --- |
| Build | project's Vite build exits 0 |
| CSS ↔ StyleX manifest | the CSS hash in the v2 StyleX manifest equals the emitted CSS; fail otherwise |
| Style keys | every key referenced from Fluid is in the StyleX manifest of the same build |
| Entrypoints | each entrypoint appears in the Vite manifest and the emitted file exists |
| Single stylesheet load | the same stylesheet is not loaded twice |
| Dev loading | development stylesheet loads through the Vite Asset Collector |
| Fonts | intended family loads, not a fallback |
| Token delivery | project `--brand-*` and mapped `--astryx-*` values resolve at each theme scope |
| Editor preview | tokens and fonts reach the backend preview, or the gap is recorded |

A missing or foreign style mapping with CSS present is `failed`; name the inconsistent outputs.

## 2. Capture conditions

Record beside every capture or measurement: browser and version, viewport, device scale factor, color scheme/mode, theme, fonts loaded, content/assets used, interaction state, animation/time controls (reduced motion or paused), URL. Compare reference and target under identical conditions. Never replace reference captures to clear a failure.

## 3. Fidelity gate

- **Hard gate: computed style and layout.** Geometry within ±1px; typography (family, size, weight, line-height, letter-spacing), colors and spacing exact. Measure representative elements at the widths derived from the source plus widths around observed layout transitions.
- **Advisory: screenshots.** Use them to find differences; they cannot establish fidelity alone and are never the only evidence.
- Pass a rendered check only after it executed against the TYPO3 target. Without a browser or a target, record `not-run` with the reason and mark the handoff "extraction complete, rendered integration unverified".
- An accepted deviation (e.g. font substitution) requires an answered binding decision naming requirement, reason and approver.

## 4. Fixture checks versus live checks

Validator runs and fixture evals prove contract handling only. They do not prove live TYPO3 rendering. Report the two separately and never claim live parity from fixtures.
