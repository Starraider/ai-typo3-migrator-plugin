# Merge TYPO3 Site Packages

A reusable workflow for consolidating two TYPO3 site packages, side packages, or theme extensions into one TYPO3-compliant target extension while preserving deliberate customizations and resolving conflicts explicitly.

## Use when

- Combining two TYPO3 site packages or theme extensions into one target package.
- Reconciling TypoScript, site sets, Fluid templates, TCA overrides, Composer metadata, assets, or version compatibility.
- You need an evidence-based merge process with a clear conflict winner.

## What this skill solves

It makes a potentially destructive package consolidation reviewable by establishing a conflict winner, target TYPO3 version, and evidence-led merge process before edits.

## Expected outputs

- A required decision about which package has priority when files or configuration conflict.
- Target TYPO3 version discovery from the repository or the user.
- Structured guidance for comparing and merging file trees, configuration, templates, assets, and extension metadata.

## Context requirements

The priority package must be known before the merge begins. The target TYPO3 version must be established from the root `composer.json` or confirmed by the user. Perform the work in a reviewable branch and preserve source-package history until the merged result has been verified.

## Installation

Install this package through an Agent Plugins-compatible client. Compatible clients discover this skill at `skills/typo3-merge-sitepackages/`; installation, enablement, and permissions are client-managed.

## Example prompts

- "Merge these two TYPO3 site packages into one target extension, using the design-system package as the conflict winner."
- "Compare our legacy and replacement TYPO3 sitepackages and produce a safe consolidation plan for TYPO3 13."
- "Consolidate the TypoScript, Fluid templates, assets, and Composer metadata from these two TYPO3 theme extensions."

## Validation

Validate the package from its root with the Agent Plugin validator, then run the target project's prescribed checks after applying a merge.

## Related skills

Use the version-specific upgrade skills before or after the merge when the target project also needs a major TYPO3 upgrade.

## License

No package-wide license file is supplied. Confirm the applicable terms before redistributing this skill.

## Resources

- [Merge guidelines](references/merge-guidelines.md) — file-by-file merge workflow, validation commands, and reporting format.
- [TYPO3 site package standards](references/typo3-sitepackage-standards.md) — expected layout, Composer configuration, and compatibility considerations.
