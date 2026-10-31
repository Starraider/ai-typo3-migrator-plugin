---
name: typo3-component-analyze
description: Analyze ONE selected component or composite section from React source, a URL, Stitch design, exports, or screenshots into a TYPO3-oriented specification of its whole visual design, structure, variants, editorial content, assets, responsive and interaction behavior, and non-binding placement hypothesis. Combine available resources and capture URL views in the internal browser. Use before building a component with Astryx. Do not compare against global design tokens or implement code.
license: CC-BY-4.0
compatibility: Needs mockup resources and Python 3.8+ for the validator. A supplied URL requires the internal browser; Stitch-MCP and Astryx evidence are optional. No global design-system handoff or TYPO3 installation is needed.
---

# TYPO3 Component Analysis

Describe one selected mockup component, or one composite section, so a later build step can implement it in TYPO3 without re-reading the mockup. Write analysis documents only. The result is a `component-spec.json` plus a matching `component-spec.md`, sealed with the bundled validator.

Read [handoff-contract.md](references/handoff-contract.md) once before writing JSON. It defines the envelope, revisions, decisions and readiness rules. Do not edit the contract copy, schemas, validator or `templates/*.example.json` while producing a component analysis.

## Side effects and boundaries

- Write only the spec JSON, report, and URL/browser captures inside the migration bundle.
- Never edit mockup source or target TYPO3 code, install dependencies, run migrations, or touch a database.
- Do not implement the component, even when a near-identical Astryx element exists. Record it as a candidate note and stop.
- Describe the selected component's complete visual design from component-specific evidence. Do not inspect or compare it against the global design system, map it to global tokens, or record missing global mappings as unresolved; implementation owns that comparison.
- Never claim live TYPO3 parity. This skill produces a specification, not a verified result.

## 1. Resolve inputs explicitly

Do not rely on hidden conversation state. List what you resolved and what is missing.

1. **Component selection.** Identify the one component or section. If several implementations match (for example two `Card` files), inspect usage context first, then ask only for the missing selection. Do not treat one as the reference until it is identified.
2. **Component source set.** Inventory all supplied or accessible resources: source files, one or more URLs, browser captures, Stitch screens, screenshots, assets and related artifacts. Treat complementary resources together; use code to establish declared structure and styles and rendered URL views to establish appearance and observed behavior. Record and explain disagreements. For every supplied URL, inspect it in the internal browser and save representative screenshots inside the bundle. See [source-and-evidence.md](references/source-and-evidence.md).
3. **Existing component specs** in the bundle: reuse child component specs as dependencies after validating them. Do not add a `design-system.json` dependency to a component spec or inspect one for token overlap.
4. **Bundle path:** reuse a supplied bundle; otherwise propose `design-migration/<design-id>/` and report it before writing.

Completion: selection, every component-source identity and bundle path are each stated as known, unavailable or assumed; URL captures are linked to their source and capture conditions.

## 2. Establish identity and the evidence boundary

Record source locator and digest or revision, dependency context (styles, data, child components), and one representative rendered location. Tag every claim with one class:

| Class | Meaning |
| --- | --- |
| Source fact | Read from code or styles. |
| Rendered observation | Measured or seen in a render or capture, with viewport and state. |
| User requirement | Stated by the user. |
| Assumption | Anything else. Keep assumptions few and listed. |

Disclose inaccessible states, assets and dependencies. Details and screenshot-only handling are in [source-and-evidence.md](references/source-and-evidence.md).

Completion: no claim lacks a class, and every inaccessible item appears in `unresolved` or `evidence` (`unknown`).

## 3. Describe structure, variants and the whole visual design

List semantic parts, nesting, content slots, child components and exposed variants (props, classes, conditions). Mark each variant `source`, `rendered`, `user` or `hypothetical`. Describe structural differences per variant and representative combinations. Never flatten distinct variants into one generic component.

Describe the entire component's visual design: overall hierarchy, frame and width constraints, composition and alignment, surface treatment, typography roles, spacing relationships, appearance of important parts, and default/interactive visual states. Record raw component-specific source values or rendered measurements where available; label screenshot estimates and unknowns. Include the full section background and inner content frame for composite sections. Do not translate observations into global token names or check whether the global design system already covers them. Store this account in `payload.design` as defined by the schema. Method: [component-analysis.md](references/component-analysis.md).

## 4. Classify content

Sort every part into `editorial` (editor-managed), `fixed` (presentation), `derived` (computed from site data) or `interaction-state` (transient UI state). Give cardinality, defaults and validation only where evidenced. Keep editable fields and action counts separate from layout variants and state.

## 5. Describe responsive and interaction behavior

Record layout transitions, sizing and ordering rules, image behavior and interaction states with their evidence. Include checks at and around each transition width. Cover keyboard, focus, reduced motion and no-JavaScript behavior where relevant. Mark each item `source`, `rendered`, `user`, `unknown` or `proposed`; "required" means source, rendered or user evidence only. With one viewport evidenced, mark the rest `unknown`. See [responsive-and-interaction.md](references/responsive-and-interaction.md).

If behavior is ambiguous (for example a carousel with unclear loop, autoplay-pause or last-slide behavior), ask one focused question. Do not mark the interaction contract ready by assumption. Record the answer as a decision, or leave it in `unresolved`.

## 6. Build the asset manifest

For each image, icon, font or other asset: source reference, provenance, dimensions or format when known, role, crop or aspect ratio, alt-text requirement, and ownership (`fal-editorial` or `site-package`). If an asset cannot be retrieved, keep the reference, set status `unresolved`, and record any placeholder as a temporary difference with status `placeholder`, never as the required asset.

## 7. Add Astryx candidate notes (advisory)

When target Astryx evidence is available, note plausible existing elements and known gaps, for example "Astryx Card has no badge field". Set `advisory: true`. Visual similarity is not implementation equivalence and reuse is not proven here. The build skill decides reuse.

## 8. Write the target hypothesis

Keep binding requirements (content parts, cardinality, defaults, assets, behavior) target-neutral. Put placement in `targetHypothesis`, which is non-binding:

- `placementClass`: content element, nested container, native component or page-layout part. A visual component is not automatically a content element. Primary navigation derives from the page tree and belongs to the page layout, not to hand-maintained menu item records.
- `placeable`: true for content elements and Content Blocks, false for embedded components. An embedded component is never `placeable`.
- For a container: each column, its `allowedChildren` (placeable only) and per-column `min` and `max`.

Changing only the hypothesis never makes the spec stale. Rules and examples: [target-placement.md](references/target-placement.md).

## 9. Set the analysis scope

For a composite section, `scope` is `single` (one spec, inline children) or `parent-with-children` (a parent spec plus one child spec per distinct child component).

1. If the user directed a scope, use it. Record the directive as a source and as an answered decision.
2. If scope is missing and the section has repeated or distinct children, ask one focused question before analyzing.
3. If you cannot ask (non-interactive run), default to `single`, set readiness `incomplete`, and add `granularity not confirmed` to `unresolved` with an unanswered decision.
4. For `parent-with-children`, write one child spec per distinct child and reuse it for all repeats (three identical cards: one `card` spec, `count: 3`). The parent lists each child in `dependencies` and `children[]`.
5. A missing or stale child makes the parent `incomplete`, not `ready`.

Re-validate children before sealing the parent.

## 10. Set readiness and decisions

- `ready`: nothing in `unresolved`, no unanswered decision, no failed verification.
- `incomplete`: required facts are unknown but nothing prevents later completion (screenshot-only evidence, unconfirmed scope, unresolved visual details, unresolved assets, missing child).
- `blocked`: a decision or input prevents any reliable result (for example the selection cannot be identified).

Record every decision gate in `decisions` (question, options, answer, the user's wording, date, `appliesTo`, `effect`). Reuse an answered decision from a handoff in a later session instead of asking again. If the `payloadDigest` it applies to differs from its `bindingDigest`, mark it stale and ask again before relying on it. A decision that changes binding requirements has effect `binding`; a run-only choice has `run-only`.

## 11. Write, seal and validate

1. Write `components/<id>/component-spec.json` and `component-spec.md` ([report template](templates/component-spec-report.md)). The Markdown adds no facts that the JSON lacks.
2. Run `python3 scripts/validate_handoff.py seal <file>`, then `python3 scripts/validate_handoff.py validate --json <file>`.
3. Fix `invalid` findings. Report exit `2` (stale or unknown component-source/child-dependency freshness) rather than hiding it. Global design-system freshness and overlap are outside this analysis.
4. Confirm against [analysis-checklist.md](templates/analysis-checklist.md).

Start from [component-spec.example.json](templates/component-spec.example.json) or [component-spec-parent.example.json](templates/component-spec-parent.example.json) (copy, never edit them).

## Final response

State: bundle path, spec files, readiness, scope, unresolved items, decisions asked or reused, component-source/child freshness, validator exit code. Say explicitly that global design-system alignment is left for implementation, no target or mockup code was changed, and nothing was implemented or verified live.

## References

- [Component analysis](references/component-analysis.md): method, content classes, card vs page-tree menu.
- [Source and evidence](references/source-and-evidence.md): identity, intake, screenshot-only and inaccessible assets.
- [Responsive and interaction](references/responsive-and-interaction.md): transitions and states.
- [Target placement](references/target-placement.md): placement classes and containers.
- [Handoff contract](references/handoff-contract.md): envelope, revisions, decisions, readiness.
