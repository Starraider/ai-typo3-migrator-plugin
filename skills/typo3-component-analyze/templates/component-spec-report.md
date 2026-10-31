# Component Specification Report: {{component.name}}

- **Artifact ID:** `{{artifactId}}`
- **Schema Version:** `1.0.0`
- **Revision:** `{{revision}}`
- **Readiness:** `{{readiness}}` (ready | incomplete | blocked)
- **Scope:** `{{scope}}` (single | parent-with-children)
- **Source Locator:** `{{component.sourceLocator}}`

---

## 1. Source Set & Evidence Boundary

List every URL, browser capture, source tree, Stitch artifact, screenshot, and other input from the JSON `sources[]` array. Treat them as one combined reference set. For each browser capture, give its viewport and page state; preserve source/render differences as separate evidence.

| Kind | Locator | Selector / Capture Conditions | Identity / Digest |
| --- | --- | --- | --- |
| `{{source.kind}}` | `{{source.locator}}` | `{{source.selector}}` | `{{source.identityStatus}}` / `{{source.digest}}` |

---

## 2. Structure & Semantic Parts

| Part | Semantic Role | Children / Slots |
| --- | --- | --- |
| `{{part.part}}` | `{{part.role}}` | `{{part.children}}` |

### Variants
| Variant Name | Evidence | Display Condition |
| --- | --- | --- |
| `{{variant.name}}` | `{{variant.evidence}}` | `{{variant.condition}}` |

---

## 3. Whole-Component Visual Design

### Overview, frame, composition, and surface
| Aspect | Description | Evidence |
| --- | --- | --- |
| Overall design | `{{design.overview.description}}` | `{{design.overview.evidence}}` |
| Frame | `{{design.frame.description}}` | `{{design.frame.evidence}}` |
| Composition | `{{design.composition.description}}` | `{{design.composition.evidence}}` |
| Surface | `{{design.surface.description}}` | `{{design.surface.evidence}}` |

### Typography
| Text Role | Appearance | Evidence |
| --- | --- | --- |
| `{{type.role}}` | `{{type.appearance}}` | `{{type.evidence}}` |

### Spacing
| Relationship | Appearance | Evidence |
| --- | --- | --- |
| `{{spacing.relationship}}` | `{{spacing.appearance}}` | `{{spacing.evidence}}` |

### Important Parts
| Part | Appearance | Evidence |
| --- | --- | --- |
| `{{part.part}}` | `{{part.appearance}}` | `{{part.evidence}}` |

### Visual States
| State | Appearance | Evidence |
| --- | --- | --- |
| `{{visualState.state}}` | `{{visualState.appearance}}` | `{{visualState.evidence}}` |

## 4. Editorial Content Model

| Field Name | Kind | Cardinality | Default | Validation / Constraints |
| --- | --- | --- | --- | --- |
| `{{field.name}}` | `{{field.kind}}` | `{{field.cardinality}}` | `{{field.default}}` | `{{field.validation}}` |

---

## 5. Assets & Media

| Asset ID | Role | Ownership | Aspect Ratio | Alt Text Required | Status |
| --- | --- | --- | --- | --- | --- |
| `{{asset.id}}` | `{{asset.role}}` | `{{asset.ownership}}` | `{{asset.aspectRatio}}` | `{{asset.altRequired}}` | `{{asset.status}}` |

---

## 6. Responsive & Interaction Rules

### Responsive Transitions
| Condition (Breakpoint) | Rule | Evidence |
| --- | --- | --- |
| `{{resp.condition}}` | `{{resp.rule}}` | `{{resp.evidence}}` |

### Interactions & Accessibility
| Interaction | Expected Behavior | Evidence | Keyboard / A11y Details |
| --- | --- | --- | --- |
| `{{int.name}}` | `{{int.behavior}}` | `{{int.evidence}}` | `{{int.keyboard}}` |

---

## 7. Advisory Astryx Candidate Notes

| Candidate Element / Component | Fit Assessment | Identified Gaps |
| --- | --- | --- |
| `{{candidate.name}}` | `{{candidate.fit}}` | `{{candidate.gaps}}` |

---

## 8. Target Hypothesis (Non-Binding)

- **Placement Class:** `{{targetHypothesis.placementClass}}`
- **Placeable in Container Columns:** `{{targetHypothesis.placeable}}`
- **Proposed Fields:** `{{targetHypothesis.proposedFields}}`

---

## 9. Decisions & Unresolved Issues

### Recorded Decisions
| ID | Question | Answer | Wording | Effect |
| --- | --- | --- | --- | --- |
| `{{decision.id}}` | `{{decision.question}}` | `{{decision.answer}}` | `{{decision.answerWording}}` | `{{decision.effect}}` |

### Unresolved Items
| ID | Description | Readiness Effect |
| --- | --- | --- |
| `{{unresolved.id}}` | `{{unresolved.description}}` | `{{unresolved.readinessEffect}}` |

---

## 10. Verification Criteria

| ID | Criterion | Viewport | Target State |
| --- | --- | --- | --- |
| `{{crit.id}}` | `{{crit.criterion}}` | `{{crit.viewport}}` | `{{crit.state}}` |

