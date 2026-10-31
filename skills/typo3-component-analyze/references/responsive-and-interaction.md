# Responsive and Interaction Contract Guide

This reference details how to specify layout transitions, client-side behaviors, and accessibility conditions without coupling the spec to a specific CSS framework or JavaScript library.

## 1. Responsive Layout Transitions

Specify breakpoint transitions as responsive rules tied to evidenced viewport conditions:
- **Condition:** Exact min-width or max-width query (e.g., `min-width: 48rem` or `min-width: 768px`).
- **Rule:** Structural change (e.g., "Media shifts from top-stacked to left-side column; flex-direction changes from column to row").
- **Evidence:** Record whether the transition was directly observed in React source, observed in rendered browser tests, or inferred from CSS utility classes.
- **Transition Width Checks:** In verification criteria, mandate inspection at:
  - 1px below transition (e.g. 767px): confirms stacked layout.
  - Exactly at transition (e.g. 768px): confirms switch occurs cleanly.
  - Above transition (e.g. 1024px): confirms desktop presentation.

## 2. Image Behavior & Cropping

- Define aspect ratios for each viewport state (e.g. 1:1 on mobile, 16:9 on desktop).
- Specify focal point or crop handling (e.g. center crop, cover, contain).
- Document alternate text requirements (`altRequired: true`) for editorial accessibility.

## 3. Interaction & Accessibility Contract

Capture all evidenced interaction states:

Describe the visual appearance of each evidenced state in the component's `design.states` list, and describe its behavior and accessibility contract below in `interactions`. Keep the appearance and behavior linked by state name and evidence.

### Focus & Keyboard Navigation
- Interactive elements (buttons, links, form inputs) must have a visible focus indicator.
- Tab order must follow logical document structure.
- Modal or menu dialogs must trap focus when open and return focus upon escape.

### Hover, Active & Pressed States
- Document color transitions, shadow elevations, or subtle scale transforms.
- Differentiate hover effects from required click/touch targets.

### Reduced Motion (`prefers-reduced-motion`)
- Animations (slide-in, carousel transitions, pulse effects) must disable or gracefully reduce when `prefers-reduced-motion: reduce` is active.

### No-JavaScript Fallback
- Determine how the component behaves if JavaScript fails or is disabled (e.g. collapsible content falls back to statically expanded or uses native `<details>/<summary>`).

