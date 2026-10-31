# Visual, Functional and Editorial Verification Guide

This guide establishes the mandatory verification protocol for validating a TYPO3 component against its mockup specification.

## 1. Controlled Capture Conditions

When comparing rendered TYPO3 output against the reference mockup:
- **Identical Content:** Use the exact same strings, heading lengths, and image aspect ratios.
- **Identical Typography:** Verify that the required webfonts are fully loaded; fallback system fonts invalidate geometry checks.
- **Environment Parity:** Match Device Pixel Ratio (DPR 1), browser rendering engine, zoom level, and color scheme (light/dark).
- **Time & Animation Control:** Freeze CSS animations, transitions, and carousels before measurement.

## 2. Hard Fidelity Gate: Computed Style & Layout

Computed style and layout measurements constitute the **hard gate** for visual parity:
- **Box Geometry:** Computed width, height, padding, margin, and borders must match the reference within **±1px**.
- **Computed Styles:** Exact match required for:
  - `font-family`, `font-size`, `font-weight`, `line-height`
  - `color`, `background-color`
  - `letter-spacing`, `border-radius`
- **Screenshots are Advisory Only:**
  - A pixel difference below a numeric threshold does NOT pass if layout geometry shifted > 1px.
  - Subpixel anti-aliasing differences are recorded as `noise` and do not fail the check.
  - Never overwrite baseline captures merely to make a failing visual test pass.

## 3. Responsive Breakpoint Verification

Inspect layout behavior at and immediately around each transition width:
- **Transition - 1px (e.g. 767px):** Verify mobile stacked layout is fully preserved.
- **Transition (e.g. 768px):** Verify the switch to tablet/desktop occurs smoothly without clipping or horizontal scroll.
- **Transition + 256px (e.g. 1024px):** Verify desktop expansion.

## 4. Functional & Accessibility Verification

Visual appearance alone does not establish parity:
- **Keyboard Navigation:** Tab key moves logically through interactive elements; visible focus rings are present.
- **Focus Management:** Modals trap focus; closing returns focus to trigger.
- **Reduced Motion:** If `prefers-reduced-motion: reduce` is active, smooth scroll and transitions must be disabled or instant.
- **JavaScript Degradation:** Content must remain readable and functional if JavaScript is disabled.

## 5. Editorial Robustness Testing

Exercise backend content edge cases in the TYPO3 editing interface:
- **Long Content:** Enter an 80+ character headline and extended body text to verify text wraps without breaking container boundaries.
- **Missing Optional Content:** Omit optional badges or images to confirm layout adapts gracefully without rendering broken image tags or empty gaps.

## 6. Handling Missing Live Evidence

If no live TYPO3 instance or browser testing harness is available during execution:
- Mark executed build/manifest checks according to their result.
- Mark all live rendered, interaction, and editorial checks as `status: "not-run"` with a clear reason.
- Set overall `completion: "qualified"`, NOT `verified`.
- **Strict Rule:** Any `failed` or `not-run` check strictly prevents an unqualified `verified` completion status.

