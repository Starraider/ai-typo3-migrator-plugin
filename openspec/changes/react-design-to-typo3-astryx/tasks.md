# Tasks

## 1. Define the handoff contracts and validation foundation

- [x] 1.1 Define and document the common v1 handoff envelope, artifact payloads, readiness/verification states, relative-reference rules, and canonical revision calculation in directly linked skill resources; verify complete example design-system, component-specification, and build-report artifacts against the three specifications.
- [x] 1.2 Add self-contained contract templates and schemas to the skills that produce or consume them, with a documented authoring source and no runtime sibling-directory references; verify standalone copies contain all required resources and equivalent contract definitions.
- [x] 1.3 Add a small non-interactive handoff validation helper with documented dependencies, `--help`, actionable errors, and machine-readable results; verify valid fixtures pass, `decisions` entries are validated (required fields, binding vs run-only revision effects, stale decisions), and malformed fields, unsupported schema majors, unknown freshness, stale dependencies, and changed payload digests are distinguished correctly.
- [x] 1.4 Add local synthetic contract fixtures and focused tests for revision stability, source/token invalidation, reference resolution, and contract-copy consistency; verify the documented local/CI command executes without a provider connection or target TYPO3 installation.

## 2. Implement the global design extraction skill

- [x] 2.1 Write `skills/typo3-design-system-extract/SKILL.md` with portable metadata, source intake, evidence classification, global design inventory, analysis-only behavior, and explicit completion criteria; verify its description routes global extraction requests and excludes isolated component implementation.
- [x] 2.2 Add token mapping and site-package foundation references/templates covering installed-source precedence, project-owned StyleX tokens, scoped Astryx aliases, theme/layer behavior, fonts, base styling, and editor/preview consistency; verify examples against the inspected upstream sources and a synthetic mapping fixture without modifying dependencies.
- [x] 2.3 Add target/build guidance for TYPO3 14.3.x, installed dependency constraints, FSC conflicts, existing package-manager/environment conventions, Astryx asset modes, Vite entrypoints, both manifests, and required-key/integrity checks; verify supported and conflicting target fixtures produce distinct outcomes and example APIs match the selected extension version.
- [x] 2.4 Write the skill README with prerequisites, outputs, side effects, at least three prompts, installation/validation guidance, licensing, and related-skill links; verify all relative links resolve in a standalone copy.
- [x] 2.5 Add and exercise extraction evaluations for React/Tailwind input, Stitch HTML input, inferred versus observed values, unavailable fonts, scoped themes, unsupported target/FSC conflict, and extraction-only requests; verify expected handoffs preserve uncertainty and report any unavailable rendered checks instead of marking them passed.

- [x] 2.6 Add FSC stop-and-ask handling to extract preflight (read-only extraction continues, target steps `blocked` when non-interactive); verify fixture outcomes.

## 3. Implement the component analysis skill

- [x] 3.1 Write `skills/typo3-component-analyze/SKILL.md` with portable metadata, explicit component selection, source/dependency freshness checks, independent invocation, and application-code read-only boundaries; verify analysis can begin with supplied artifacts in a fresh-session fixture.
- [x] 3.2 Add a component analysis reference and paired report/structured templates for semantic parts, whole-component visual design, variants, content model, target placement, assets, responsive transitions, interaction states, reference conditions, candidate notes, and unresolved requirements; verify a card and page-tree menu produce different editorial models and placement recommendations.
- [x] 3.3 Write the skill README with at least three prompts and standalone input/output, scope, validation, licensing, and related-skill guidance; verify its links and examples do not require another skill's local files.
- [x] 3.4 Add and exercise analysis evaluations for a variant-rich card, full-width section, page-tree navigation, ambiguous carousel, no global handoff, screenshot-only evidence, inaccessible assets, a supplied global handoff that must not be compared, and premature implementation; verify readiness and unknowns are explicit and target code remains unchanged.

- [x] 3.5 Implement the `targetHypothesis` split (container columns, allowed children, placeable vs embedded) and user-directed `scope` (ask first; non-interactive `single` marked `incomplete`; parent and child specs); verify a three-card section yields one parent plus one reused child spec and a missing child leaves the parent `incomplete`.
- [x] 3.6 Extend component handoffs and reports with evidence-labeled whole-element visual design; keep global design-system comparison out of analysis and verify that coverage is recorded during build.

## 4. Implement Astryx reuse and component building

- [x] 4.1 Write `skills/typo3-component-build/SKILL.md` with portable metadata, target preflight, current-handoff checks, scoped implementation, and the mandatory candidate assessment before target edits; verify incompatible targets and stale inputs cannot proceed as verified implementations.
- [x] 4.2 Add reuse-assessment and decision templates covering installed paths/versions, fields, relations, slots, recipes, responsive rules, interactions, assets, fit/gaps, rejected alternatives, and configuration/composition/extension/new-block disposition; verify unchanged Hero reuse, container composition, and justified new-block fixtures take the intended branches.
- [x] 4.3 Add implementation references for site-package component/partial/data/style ownership, native fields/FAL, safe extension of existing content, connector key usage, finite recipe limits, and concrete upstream-gap reporting; verify a Card metadata extension and a fixed-allowlist gap do not rely on nonexistent APIs or edits to installed dependencies.
- [x] 4.4 Add paired build-report templates and a visual/functional/editorial verification guide covering equivalent content/fonts/capture conditions, transition widths, relevant states, baseline protection, keyboard/reduced-motion behavior, optional/long content, and missing live evidence; verify failed and not-run checks cannot produce an unqualified verified result.
- [x] 4.5 Write the skill README with at least three prompts and prerequisites, outputs, side effects, supported target, reuse examples, validation, licensing, and related-skill guidance; verify its documented standalone workflow and links.
- [x] 4.6 Add and exercise build evaluations for Hero reuse, section composition, Card extension, unsupported recipe variants, a justified new element, CSS/manifest mismatch, mobile regression, keyboard failure, and unavailable backend/browser verification; verify every decision and remaining difference appears in the completion handoff.

- [x] 4.7 Implement decision gates in build: FSC stop-and-ask, recipe-gap sequence (adaptation, then deviation or blocked), hypothesis adopt/override recording, container column checks, and computed-style/layout hard gate with advisory screenshots; verify non-interactive runs end `blocked` and recorded decisions are reused.
- [x] 4.8 Trace the selected Content Block/content element's active styling inheritance; distinguish inherited values from available global tokens; record exact component-specific token IDs and values needed for uncovered design requirements in the build handoff.

## 5. Integrate plugin discovery and MCP guidance

- [x] 5.1 Update the root README and relevant installation skill inventories with concise links and the three-stage TYPO3 14.3 workflow; update descriptive `plugin.json` metadata and the changelog without changing discovery semantics or release version; verify metadata parses, new links resolve, and existing skills retain their entries.
- [x] 5.2 Include focused MCP/source-intake guidance in the new skills' relevant references and summarize it in plugin documentation: existing Stitch reads or exports, Lovable local/GitHub source, local asset manifests/FAL, and direct CI validation; verify no custom server declaration, mandatory provider connection, service install, or deployment action is introduced.
- [x] 5.3 Run the available portable-skill and plugin checks, including the current Agent Skills reference validator when available, plus JSON, link, line-ending, and standalone-resource checks; verify all new skill errors are resolved and distinguish any tool-unavailability or pre-existing findings in the validation report.

## 6. Verify the complete workflow

- [x] 6.1 Run a synthetic end-to-end handoff sequence from global extraction through card analysis and Astryx reuse selection, then change the token revision; verify the original sequence is consumable and the changed dependency is detected before implementation claims are reused.
- [x] 6.2 Exercise representative fresh-session prompts for all three skills and boundary prompts for analysis-only, unsupported-target, and missing-live-evidence cases; verify observed behavior against the scenario expectations, compare with a no-skill/prior baseline where feasible, and report unexecuted evaluations explicitly.
- [x] 6.3 Review the final implementation diff against all three capability specifications and the planned exclusions; verify only intended plugin files changed, all completed task claims have evidence, no upstream/target site was modified implicitly, and no live TYPO3 visual-parity claim is made without an actual consumer run.
