# Source and Evidence Intake Guide

This reference explains how to resolve component identity, inspect sources, handle partial or screenshot-only evidence, and avoid premature implementation.

## 1. Component Identity Resolution

Before analyzing:
1. Inventory the full resource set: component source files and styles, one or more URLs, screenshots, Stitch screens/exports, assets, and related artifacts. These resources may be combined; do not require one file or URL to contain all evidence.
2. If multiple components share the same name (e.g., `components/Card.tsx` vs `components/blog/Card.tsx`), check usage contexts across page templates. If ambiguity remains, ask the user one focused question specifying the candidates.
3. For every supplied URL, open the rendered page in the internal browser, locate the selected component or section, and capture representative screenshots into the bundle under `components/<component-id>/references/`. Capture desktop and mobile widths (and a width around an observed transition when useful); capture relevant visible states only through read-only interactions. If the target cannot be isolated within the URL, state the assumption or ask for the missing locator.
4. Record every URL, screenshot, source tree, Stitch artifact, and other input separately in `sources[]`: `kind`, safe `locator`, `identityStatus`, `digest` or `revision`, and `selector` when relevant. A screenshot is its own source, with a SHA-256 digest and capture conditions (final URL, viewport, date/time, scroll, theme/state) in `selector` or its evidence note. Remove credentials and signed or secret query values from locators.
5. Compute a source locator digest (`sha256:...`) or record the exact git revision where available. URLs without a stable content revision and inaccessible resources use `identityStatus: "unavailable"`; never invent a digest. A saved browser capture can have known identity independently of its live URL.

Use all resources together: source code establishes declared structure and behavior; the browser establishes rendered appearance and only the states actually inspected; screenshots preserve visual evidence. Preserve mismatches as separate observations and explain them. Do not silently treat a rendered difference as a source-code fact or vice versa.

Combine resources only when they represent the same design and intended revision. If a URL, screenshot, Stitch screen, or source tree appears to represent a different version or component scope and the user has not identified the target, keep the alternatives separate and ask one focused question before combining them.

## 2. MCP and Source Intake Workflow

- **Internal browser:** A supplied URL must be inspected in the internal browser and captured to the bundle. If it cannot be reached or the browser is unavailable, record the failed/unrun capture and continue with other resources; do not pretend a URL was inspected.
- **Optional Stitch-MCP:** When the source is a Stitch project/screen and Stitch-MCP is available, use read-only tools to inspect the existing project/screen and retrieve its screen-specific HTML or screenshot. Do not create, regenerate, apply, update, or delete remote Stitch resources. If unavailable, use supplied URLs and local exports.
- **Lovable Projects:** Read local workspace files or cloned GitHub repositories.
- **Assets:** Record image and media references in a local manifest. Do not require remote CDN credentials.
- **Zero Custom MCP Overhead:** Do not create custom servers, run local background daemons, or install services. Direct file inspection and Python validator scripts are sufficient locally and in CI.

Use the safest evidence source for each claim. Declared classes/props/styles establish code facts; browser captures establish rendered observations. A screenshot alone cannot establish interactions, fonts, or breakpoints. Never submit, save, or publish through the referenced site; use only read-only inspection and harmless navigation/toggles.

## 3. Evidence Classification

Tag every extracted property, variant, and responsive rule with one of these classes:

| Class | Definition | Consequence |
| --- | --- | --- |
| `observed` | Measured from rendered output or read directly from source code. | Verified fact; can form binding requirements. |
| `inferred` | Derived logically from recurring patterns or common conventions. | Subject to review; do not present as authoritative. |
| `unknown` | Missing from inputs (e.g., hover states, mobile layout in desktop shot). | Stays explicit in `unresolved` or marked with readiness effect. |

## 4. Screenshot-Only Evidence

When only static screenshots (e.g., PNG/JPEG) are available, or a URL yields only static pixels without inspectable DOM/source:
- **Do not invent behavior:** Hover states, focus rings, keyboard navigation, and breakpoint behavior cannot be observed from a static image.
- Mark responsive transitions and interaction behavior as `unknown`.
- Set component spec readiness to `incomplete` with an item under `unresolved` noting missing source evidence.
- Still describe the entire visible design in `payload.design`: frame, composition, surface, typography appearance, spacing, and important parts. Mark measurements and font identification as `inferred` or approximate where exact values cannot be read; mark unobserved states as `unknown`.

Do not inspect a global design-system handoff to interpret component-specific values. Record the visible or declared component design as-is; implementation compares it with global foundations later.

If a URL is inaccessible or a relevant state cannot be inspected, retain the URL and capture details in `sources[]`/`evidence`; mark only the affected facts `unknown`. Do not downgrade the entire spec solely because a URL is dynamic if other stable sources fully establish the required facts.

## 5. Inaccessible Assets & Incomplete States

- If an asset (image, icon, font) is referenced by an external URL that cannot be fetched, record the locator in the asset manifest and mark `status: "unresolved"`.
- A temporary placeholder image is recorded as a placeholder difference, NOT as proof that the required asset exists.

