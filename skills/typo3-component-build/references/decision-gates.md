# Decision Gates Reference for Component Build

This document outlines the mandatory decision gates encountered during component building, their options, and non-interactive handling.

## 1. Decision Gate: Fluid Styled Content (FSC) Conflict

- **Condition:** Preflight detects `typo3/cms-fluid-styled-content` in target `composer.json`.
- **Options:**
  - Stop and ask user:
    1. "Stop target edits and keep build blocked until FSC is migrated."
    2. "Proceed with extraction/analysis only; do not modify target site package."
- **Non-Interactive Behavior:** End as `blocked`, record conflict in `preflight.fscConflict: true`, and make NO target file modifications.
- **Strict Rule:** Never automatically remove FSC or edit Composer dependencies to bypass the gate.

## 2. Decision Gate: Recipe Gap Sequence

- **Condition:** Required component variant is unsupported by Astryx's fixed `RecipeViewHelper` allowlist and cannot be solved cleanly in the site package.
- **Sequence:**
  1. Attempt site-package StyleX adaptation first.
  2. If impossible without core hacks, prompt user:
     - Option A: "Accept deviation (use nearest existing recipe variant)."
     - Option B: "Mark blocked and generate upstream capability gap report."
- **Non-Interactive Behavior:** End as `blocked`. Never silently choose an accepted deviation without explicit user confirmation.
- **Recording:** An accepted deviation requires an answered `binding` decision entry referencing the requirement, reason, and approver.

## 3. Decision Gate: Target Hypothesis Adopt vs Override

- **Condition:** Build evaluates the specification's `targetHypothesis`.
- **Action:**
  - Adopt hypothesis if candidate assessment confirms it is the cleanest path.
  - Override hypothesis if installed assessment reveals a better disposition (e.g., container composition instead of a new standalone element).
- **Recording:** Record outcome in `hypothesis.outcome` (`adopted` or `overridden`) along with the justification. Overriding the hypothesis does NOT invalidate the component specification.

## 4. Decision Gate: Container Column & Placeable Element Check

- **Condition:** Implementing a container layout with columns.
- **Verification Rule:**
  - Every child component placed in a column must be a **placeable element** (Content Block or content element).
  - Embedded native Fluid components are strictly rejected from container columns.

## 5. Decision Gate: Visual Fidelity Gate & Deviations

- **Condition:** Layout geometry differs by > 1px or computed typography/colors differ from reference.
- **Action:**
  - Verification fails unless an explicit deviation is approved.
  - If approved, record an answered binding decision in `decisions`, and document the deviation under `acceptedDeviations`.
  - Unrecorded differences fail the build verification.

