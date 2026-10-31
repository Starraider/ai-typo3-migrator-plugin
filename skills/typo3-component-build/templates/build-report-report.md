# Build & Verification Report: {{component.id}}

- **Artifact ID:** `{{artifactId}}`
- **Schema Version:** `1.0.0`
- **Revision:** `{{revision}}`
- **Component ID:** `{{component.id}}` (Spec: `{{component.specRef}}`)
- **Completion Status:** `{{completion}}` (verified | qualified | blocked)
- **Selected Disposition:** `{{disposition}}` (configure | compose | extend | create)
- **Readiness:** `{{readiness}}`

---

## 1. Candidate Assessment & Disposition

| Candidate Name | Installed Version | Fit | Identified Gaps | Selected? |
| --- | --- | --- | --- | --- |
| `{{candidate.name}}` | `{{candidate.installedVersion}}` | `{{candidate.fit}}` | `{{candidate.gaps}}` | `{{candidate.selected}}` |

### Rejected Alternatives
| Option Considered | Reason for Rejection |
| --- | --- |
| `{{rejected.option}}` | `{{rejected.reason}}` |

---

## 2. Component Design Inheritance and Global Token Coverage

| Requirement | Selected Target Element | Analyzed Value | Inheritance | Inherited From / Effective Value | Global Token IDs | Coverage | Component Tokens (ID / value / status) | Evidence / Remaining Detail |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `{{designCoverage.requirement}}` | `{{designCoverage.targetElement}}` | `{{designCoverage.componentValue}}` | `{{designCoverage.inheritance}}` | `{{designCoverage.inheritedFrom}} / {{designCoverage.inheritedValue}}` | `{{designCoverage.globalRefs}}` | `{{designCoverage.coverage}}` | `{{designCoverage.componentTokens}}` | `{{designCoverage.evidence}}` |

## 3. Target Preflight & Hypothesis Outcome

- **Preflight Status:** `{{preflight.status}}`
- **Fluid Styled Content Conflict:** `{{preflight.fscConflict}}`
- **Target Hypothesis Outcome:** `{{hypothesis.outcome}}`
  - *Reason:* `{{hypothesis.reason}}`

---

## 4. Site-Package Modifications

| File Path | Change Kind |
| --- | --- |
| `{{change.path}}` | `{{change.kind}}` |

- **Extension Points Used:** `{{extensionPoints}}`

---

## 5. Verification Results

| Check ID | Kind | Gate | Viewport / State | Status | Detail / Command |
| --- | --- | --- | --- | --- | --- |
| `{{check.id}}` | `{{check.kind}}` | `{{check.gate}}` | `{{check.viewport}}` | `{{check.status}}` | `{{check.detail}}` |

---

## 6. Differences & Accepted Deviations

### Observed Differences
| ID | Description | Disposition | Decision ID |
| --- | --- | --- | --- |
| `{{diff.id}}` | `{{diff.description}}` | `{{diff.disposition}}` | `{{diff.decisionId}}` |

### Accepted Deviations
| Requirement | Justification | Approver | Decision ID |
| --- | --- | --- | --- |
| `{{dev.requirement}}` | `{{dev.reason}}` | `{{dev.approver}}` | `{{dev.decisionId}}` |

---

## 7. Recorded Decisions

| Decision ID | Question | Answer | Wording | Effect |
| --- | --- | --- | --- | --- |
| `{{decision.id}}` | `{{decision.question}}` | `{{decision.answer}}` | `{{decision.answerWording}}` | `{{decision.effect}}` |

