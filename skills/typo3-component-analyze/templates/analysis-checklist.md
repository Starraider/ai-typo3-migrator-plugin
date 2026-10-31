# Component Analysis Quality Checklist

Review this checklist before sealing `component-spec.json`:

- [ ] **Component Identity:** Source locator is explicit; multiple candidate matches were disambiguated.
- [ ] **Evidence Boundary:** Observed facts are distinguished from inferred or unknown properties.
- [ ] **Whole-Component Design:** Frame, composition, surface, typography, spacing, key part appearances, and default/observed visual states are described with evidence labels; no global token mapping is attempted.
- [ ] **Content Model:** Editorial fields are separated from fixed presentation and client-side UI states.
- [ ] **Asset Manifest:** Assets record FAL vs site-package ownership, aspect ratios, and alt text requirements.
- [ ] **Responsive Rules:** Breakpoint transitions define specific rules; checks are planned at transition widths.
- [ ] **Interactions:** Keyboard navigation, focus indicators, and reduced-motion behaviors are specified.
- [ ] **Advisory Candidates:** Astryx candidate notes are labeled advisory and do not force compromise of requirements.
- [ ] **Hypothesis Split:** Target hypothesis is separated from binding requirements; placeable flag matches placement class.
- [ ] **Container Rules:** If container, columns define allowed placeable children; no embedded components are listed.
- [ ] **Granularity / Scope:** User directive on `single` vs `parent-with-children` is recorded as a decision.
- [ ] **Validation:** `python3 scripts/validate_handoff.py seal` and `validate` exit 0 without errors.

