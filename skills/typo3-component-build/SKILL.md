---
name: typo3-component-build
description: Implement ONE already-specified mockup component in TYPO3 14.3 using Astryx reuse or targeted site-package adaptation, and verify its visual, responsive, and functional parity. Trace the selected element's inherited design, compare it with global tokens, and record component-specific tokens that are needed. Produces a sealed build-report handoff. Do not use for global design-token extraction, initial component analysis, or unconstrained custom development.
license: CC-BY-4.0
compatibility: Requires a TYPO3 14.3.x project with skom/typo3-astryx and skom/stylex-connector, valid handoff artifacts (design-system.json, component-spec.json), Node.js/Vite in the site package, and Python 3.8+ for handoff sealing. Browser tooling is optional; unexecuted checks are marked not-run.
---

# TYPO3 Astryx Component Building & Verification

Implement one specified component or composite section in a TYPO3 14.3 project using installed Astryx capabilities, targeted site-package adaptations, and StyleX Connector delivery. Validate input handoffs, assess existing candidates before editing, follow the disposition hierarchy, execute visual and functional verification gates, and seal a `build-report.json` handoff paired with a readable `build-report.md`.

Read these on demand before implementation:
- [Reuse Assessment](references/reuse-assessment.md) — candidate matrix, fits/gaps, disposition order.
- [Implementation Guide](references/implementation-guide.md) — site-package ownership, FAL, StyleX keys, upstream gaps.
- [Verification Guide](references/verification-guide.md) — computed style/layout hard gate (±1px), capture conditions, a11y.
- [Decision Gates](references/decision-gates.md) — FSC preflight, recipe-gap sequence, hypothesis adopt/override.
- [Handoff Contract](references/handoff-contract.md) — envelope, revisions, decisions, validator.
- Templates: [Build report template](templates/build-report-report.md), [reuse assessment](templates/reuse-assessment.md), [decision record](templates/decision-record.md).

## Operational Scope & Guardrails

- **Scope:** Edit ONLY the authorized site package in the target TYPO3 project.
- **Forbidden:** Never edit `vendor/` or Composer-managed dependency code, never subclass final classes (e.g. `RecipeViewHelper`), and never invent unregistered recipe APIs.
- **Target Boundaries:** Do not perform production deployment, database migrations beyond standard Content Block generation, or bulk content importing.
- **Reporting Parity:** Never claim live TYPO3 parity unless real browser comparisons have executed and passed. Unexecuted checks are reported as `not-run`.

---

## 1. Input Handoff Validation & Freshness

Before any target edit, resolve and validate input handoffs:

```bash
python3 scripts/validate_handoff.py validate --json design-migration/<design-id>/design-system.json
python3 scripts/validate_handoff.py validate --json design-migration/<design-id>/components/<component-id>/component-spec.json
```

1. **Schema Check:** Confirm both artifacts use `schemaVersion: "1.0.0"`. Reject unsupported major versions.
2. **Freshness:** If either validator call returns exit code `2` or reports `stale-dependency` / `unknown-freshness`, STOP and reassess. Never implement against an outdated or unprovable token mapping or component specification.
3. **Completeness:** Ensure the component spec has `readiness: "ready"`. If it is `incomplete` or `blocked` due to unresolved items (such as unconfirmed carousel behavior), do not proceed.

Completion: input handoffs are validated as fresh, ready, and compatible.

---

## 2. Target Preflight & FSC Conflict Gate

Inspect the target project's `composer.json` and environment before touching files:

1. **TYPO3 Core:** Must be `~14.3.0`. Never attempt to implement against TYPO3 13 or older; Astryx requires 14.3.
2. **PHP Runtime:** Must be `>=8.3 <8.5`.
3. **Extensions:** Verify `skom/typo3-astryx` and `skom/stylex-connector` are installed.
4. **Fluid Styled Content Conflict (Decision Gate):**
   - Check if `typo3/cms-fluid-styled-content` is present.
   - If present: **STOP immediately and make NO target edits.**
   - In interactive mode: ask the user how to proceed.
   - In non-interactive mode: set `preflight.status: "blocked"` and `preflight.fscConflict: true`, and exit `blocked`.
   - Never automatically remove FSC or tamper with Composer dependencies.

Completion: target passes preflight or stops at the FSC decision gate.

---

## 3. Mandatory Astryx Candidate Assessment

Before creating a new Content Block or writing templates, inspect the **installed** Astryx code in `vendor/skom/typo3-astryx/` (ContentBlocks, Components, ViewHelpers, StyleX tokens). Build a candidate matrix comparing:
- Persisted database fields and relations.
- Component slots and argument APIs.
- Available recipes and finite variant options.
- Client behaviors and responsive rules.
- Candidate styles and how those styles inherit from the selected Content Block, Fluid component, recipe, active theme, and global design system (see [reuse-assessment.md](references/reuse-assessment.md)).

### Disposition Order (Smallest Suitable Adaptation)

Always evaluate options in this strict order:
1. **Configure (`configure`):** Existing element fits the content model and behavior directly; style changes handled via extracted design tokens.
2. **Compose (`compose`):** Combine existing elements and containers (e.g., placing existing cards into an Astryx Container).
3. **Extend (`extend`):** Clean site-package template, partial, or field extension preserving existing identifiers and FAL relations.
4. **Create (`create`):** New site-package Content Block or component, only when existing elements cannot meet the specification cleanly.

For every selected disposition, explicitly record the **rejected alternatives** and the technical justification. Never weaken binding requirements to force reuse of an unsuitable candidate.

### Component Design Inheritance and Token Coverage

After choosing the actual content element or Content Block path, and before the first target edit, compare every relevant requirement in `component-spec.payload.design` with the selected element's active styling chain. Trace the installed Content Block or CType through its Fluid component, recipe/variant styles, imported component styles, active theme, and global rules. Inspect the actual selected variant and applicable scope. A token present in `design-system.json` is not inherited unless an active rule applies it to this element.

For each design requirement, record a `designCoverage[]` row in the build report with:

- The exact `targetElement` (Content Block or content element and selected recipe/variant).
- The analyzed `componentValue` and the `inheritance` status: `full`, `partial`, `none`, or `unknown`.
- `inheritedFrom` and `inheritedValue`, based on the active rendering/style chain. Include concrete installed file paths, recipe IDs, and active theme selectors where available.
- Applicable `globalRefs`, even when a shared token exists but is not yet applied to the element.
- The final `coverage`: `inherited` when active inherited styling already meets the requirement; `global-token` when an existing global token can meet it but must be wired to the element; `partial` when only part is satisfied; `component-specific` when a local value/rule is needed; or `unknown` when evidence is insufficient.
- `componentTokens[]` with the exact local token ID and value for every uncovered value that should be tokenized. Set status to `required` before implementation and `defined` once added; do not create a duplicate component token when inheritance or a matching global token already provides the value. If a component-specific rule needs no token, explain why in `evidence`.

For a composed section, assess each selected content element/Content Block separately and identify which rows belong to the container versus each child. Preserve every analyzed visual requirement; this assessment determines where the value comes from, not whether it can be dropped. If the active inheritance chain cannot be established, mark it `unknown` and do not claim that a global token is inherited.

Completion: the candidate matrix, selected disposition, and rejected alternatives are documented before target edits. Each design coverage row identifies its target, evidence-backed inheritance and effective value, applicable global tokens, and any exact component-specific token ID/value needed or the reason it remains unknown.

---

## 4. Hypothesis Handling & Container Placement

1. **Adopt or Override:** Review the specification's `targetHypothesis`. Record in `hypothesis.outcome` whether it was `adopted` or `overridden`, along with the technical reason. (An override does NOT invalidate the component spec).
2. **Container Placement Rules:**
   - Verify column definitions, `colPos`, and allowed child types.
   - Confirm all allowed children are **placeable elements** (Content Blocks or content elements).
   - **Embedded Fluid components** must NEVER be listed as placeable container children.

---

## 5. Recipe Gap Decision Sequence

Astryx's `RecipeViewHelper` uses a hard-coded allowlist. If a required variant or recipe is missing:
1. Attempt a clean site-package adaptation first (e.g., using site-package StyleX classes via the connector).
2. If no clean adaptation exists, invoke the **Recipe Gap Decision Gate**:
   - Ask the user to choose: **Accepted Deviation** (use nearest existing recipe) OR **Blocked** (report upstream capability gap).
   - In non-interactive mode: mark the component `blocked`. Never silently substitute a variant.

---

## 6. Implementation in the Site Package

Implement the component following these extension ownership rules:
- **Ownership:** All created Content Blocks, Fluid templates, partial overrides, and StyleX styling belong strictly to the project's site package (e.g. `packages/site_theme/`).
- **Editorial Fields:** Use native TYPO3 TCA fields and FAL relations for editorial media. Never hard-code mockup strings or temporary asset URLs in production templates.
- **StyleX Delivery:** Consume tokens via `skom/stylex-connector`. Ensure all referenced style keys exist in the generated StyleX manifest.
- **Manifest Integrity:** Verify that the Vite asset manifest and the StyleX manifest match the compiled CSS release unit.

Completion: code and template files are written; build commands succeed.

---

## 7. Visual, Responsive & Functional Verification

Execute verification according to [verification-guide.md](references/verification-guide.md):

### Hard Fidelity Gate (Computed Style & Layout)
- Geometry within **±1px** of reference at each specified viewport (desktop, tablet, mobile).
- Exact match for font family, size, weight, line-height, color, and spacing.
- **Screenshots are advisory only.** A passing pixel diff does NOT override a layout shift > 1px. Anti-aliasing noise is recorded separately.

### Responsive & Interaction Gates
- Verify layout transition widths (inspect 1px below, at, and above the breakpoint).
- Test keyboard tab navigation, visible focus indicators, and reduced-motion behavior.
- Test editorial edge cases: extra-long titles, absent optional images.

### Missing Live Evidence Rule
If no TYPO3 browser or backend session is available, mark checks as `status: "not-run"`. Set overall `completion: "qualified"`. Never mark unexecuted checks as passed or declare unqualified verified parity.

Completion: comparison matrix is executed or qualified; differences and deviations are documented.

---

## 8. Completion Report & Sealing

1. Produce `build-report.json` conforming to `build-report.payload.schema.json`.
2. Generate companion `build-report.md` from [templates/build-report-report.md](templates/build-report-report.md).
3. Record all decisions (FSC, recipe gaps, accepted deviations, hypothesis overrides) in `decisions`.
4. Seal and validate:

```bash
python3 scripts/validate_handoff.py seal design-migration/<design-id>/components/<component-id>/build-report.json
python3 scripts/validate_handoff.py validate design-migration/<design-id>/components/<component-id>/build-report.json
```

Completion: validator exits 0 (or 2 if live verification is unprovable); build report is sealed.

