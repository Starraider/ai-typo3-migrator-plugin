# Design System Extraction Report: {{artifactId}}

- **Artifact ID:** `{{artifactId}}`
- **Schema Version:** `1.0.0`
- **Revision:** `{{revision}}`
- **Readiness:** `{{readiness}}` (ready | incomplete | blocked)
- **Mode:** `{{mode}}` (analysis-only | implementation)
- **Generated At:** `{{generatedAt}}`

---

## 1. Sources & Evidence Boundary

| Kind | Locator | Selector / Capture Conditions | Identity / Digest | Status |
| --- | --- | --- | --- | --- |
| `{{source.kind}}` | `{{source.locator}}` | `{{source.selector}}` | `{{source.digest}}` | `{{source.identityStatus}}` |

All listed sources form the composite reference set. For browser captures, include viewport and page state in the source selector or evidence note; record disagreements between source declarations and rendered observations below or under unresolved items.

- **Evidence Classifications:**
  - *Observed:* Directly measured or declared in source code/CSS variables/Tailwind config.
  - *Inferred:* Derived from patterns or layout heuristics (subject to confirmation).
  - *Unknown:* Not evidenced in provided inputs (e.g., missing breakpoints or states).

---

## 2. Target Compatibility Preflight

- **TYPO3 Core:** `{{target.typo3}}` (Requirement: `~14.3.0`)
- **PHP Version:** `{{target.php}}` (Requirement: `>=8.3 <8.5`)
- **Astryx Extension (`skom/typo3-astryx`):** `{{target.astryx}}`
- **StyleX Connector (`skom/stylex-connector`):** `{{target.styleXConnector}}`
- **Fluid Styled Content Conflict:** `{{fscConflictStatus}}` (Must NOT be installed)
- **Preflight Outcome:** `{{targetCompatibility.status}}`

---

## 3. Token Inventory & Astryx Mapping

Installed source declarations take precedence over documentation. Discrepancies are explicitly recorded.

| Source Token / Value | Semantic Role | Target Property / Alias | Tier | Status | Discrepancy / Rationale |
| --- | --- | --- | --- | --- | --- |
| `{{token.id}}`: `{{token.value}}` | `{{token.role}}` | `{{token.mapping.targetProperty}}` | `{{token.tier}}` | `{{token.mapping.status}}` | `{{token.mapping.discrepancy}}` |

- **Project Additions (`--brand-*`):**
  - Project-owned tokens are declared in the site package under StyleX definitions.

---

## 4. Typography & Assets

### Fonts
| Family | Weights | Status | Files / Substitution |
| --- | --- | --- | --- |
| `{{font.family}}` | `{{font.weights}}` | `{{font.status}}` | `{{font.files}}` |

### Assets
| Asset ID | Ownership | Media Type | Destination | Rights / Status |
| --- | --- | --- | --- | --- |
| `{{asset.id}}` | `{{asset.ownership}}` | `{{asset.mediaType}}` | `{{asset.destination}}` | `{{asset.status}}` |

---

## 5. Themes, Layers & Breakpoints

- **Breakpoints (Compile-time Constants):**
  - `{{breakpoint.name}}`: `{{breakpoint.query}}`
- **Themes & Scopes:**
  - `{{theme.name}}`: `{{theme.selector}}` (`{{theme.mode}}`) - Scope verified: `{{theme.selectable}}`

---

## 6. Site-Package Foundation Status

- **Status:** `{{foundation.status}}` (not-started | implemented | verified | blocked)
- **Asset Mode:** `{{foundation.assetMode}}`
- **Vite Entrypoints:** `{{foundation.entrypoints}}`
- **Generated Manifests:** `{{foundation.manifests}}`

---

## 7. Decisions & Unresolved Issues

### Recorded Decisions
| ID | Question | Answer | Wording | Effect |
| --- | --- | --- | --- | --- |
| `{{decision.id}}` | `{{decision.question}}` | `{{decision.answer}}` | `{{decision.answerWording}}` | `{{decision.effect}}` |

### Unresolved Items
| ID | Description | Readiness Effect |
| --- | --- | --- |
| `{{unresolved.id}}` | `{{unresolved.description}}` | `{{unresolved.readinessEffect}}` |

---

## 8. Verification Ledger

| Check ID | Description / Command | Status | Reason / Evidence |
| --- | --- | --- | --- |
| `{{verification.id}}` | `{{verification.command}}` | `{{verification.status}}` | `{{verification.reason}}` |

