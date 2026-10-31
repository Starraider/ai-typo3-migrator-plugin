# Astryx Component Reuse Assessment Template

Use this template to record candidate evaluation from the installed Astryx extension before making code edits.

## 1. Component Specification Requirements
- **Component ID:** `{{componentId}}`
- **Required Editorial Fields:** `{{requiredFields}}`
- **Required Variants / Recipes:** `{{requiredVariants}}`
- **Required Behaviors:** `{{requiredBehaviors}}`

## 2. Installed Candidates Evaluation

| Candidate | Path / Version | Available Fields | Slots / Recipes | Fit (full/partial/none) | Gaps Identified |
| --- | --- | --- | --- | --- | --- |
| Astryx Hero | `vendor/skom/typo3-astryx/...` | header, subheader, bodytext, image | default, cta | full | none |
| Astryx Card | `vendor/skom/typo3-astryx/...` | header, image, links | vertical | partial | missing badge field |

## 3. Component Design Inheritance and Global Token Coverage

| Requirement | Selected Target Element | Analyzed Value | Inheritance (full / partial / none / unknown) | Inherited From / Effective Value | Global Token IDs | Coverage | Component Tokens (ID / value / status) | Evidence / Remaining Detail |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `{{requirement}}` | `{{targetElement}}` | `{{componentValue}}` | `{{inheritance}}` | `{{inheritedFrom}} / {{inheritedValue}}` | `{{globalRefs}}` | `{{coverage}}` | `{{componentTokens}}` | `{{evidence}}` |

## 4. Disposition Decision
- **Chosen Disposition:** `{{configure | compose | extend | create}}`
- **Technical Justification:** `{{justification}}`
- **Rejected Alternatives:**
  - `{{alternative 1}}`: `{{reason for rejection}}`
  - `{{alternative 2}}`: `{{reason for rejection}}`

