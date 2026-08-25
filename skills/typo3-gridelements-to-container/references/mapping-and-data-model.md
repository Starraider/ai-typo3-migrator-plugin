# Mapping and data model

## Build one mapping per used layout

Do not convert every configured layout by default. First identify layouts with live parent records. For each used `tx_gridelements_backend_layout` value, record:

| Mapping field | Required decision |
| --- | --- |
| Legacy layout key and label | Exact stored key, source title or alias, and source configuration location |
| Target CType | Unique, stable, project-owned name such as `site-two-columns` |
| Target cell grid | Every cell name, row, `colspan`, `rowspan`, restrictions, and `maxitems` |
| Column map | Every old `tx_gridelements_columns` value to one nonnegative custom Container `colPos` |
| Rendering | Legacy wrapper, classes, conditions, child variables, partials, and nested-container behavior |
| FlexForms | Preserve only when the new CType has an equivalent data structure and template consumer. Otherwise migrate the data deliberately or block. |
| Languages | Connected or free mode, plus URLs and records to test |

Prefer dedicated Container `colPos` values such as `200`, `201`, and `202`. They may match the source grid values only after confirming that the project uses them safely. A Container identifies children by `tx_container_parent` and `colPos`; it does not use Gridelements' negative `colPos` convention.

## Register the Container first

Adapt [the registration template](../templates/ContainerRegistration.php.template) in the target site package. Register it before the command is run. Add the target CType's TypoScript and Fluid rendering too. Container does not reproduce Gridelements rendering or FlexForms on its own.

For TYPO3 13, use `B13\\Container\\DataProcessing\\ContainerProcessor` and render the produced column variables. For TYPO3 14, `ContentAreaProcessor` and the Fluid content-area rendering helpers are an option. Choose one rendering path that reproduces the source output. Do not change wrappers, classes, or responsive behavior while this migration is under acceptance.

## Relation rewrite

For every mapped Gridelements parent row:

```text
CType                             = mapped target CType
tx_gridelements_backend_layout    = ''
```

For every direct child of that parent:

```text
colPos                            = mapped target colPos for tx_gridelements_columns
tx_container_parent               = source parent uid, or source parent's l18n_parent in connected mode
tx_gridelements_container         = 0
tx_gridelements_columns           = 0
```

Keep the original `uid`, `pid`, `sorting`, `sys_language_uid`, `l18n_parent`, content fields, IRRE/FAL references, and workspace-independent metadata. A nested Gridelements layout is both a converted parent and an outer child, so convert all mapped parents and all their direct child relations in the same transaction.

Container requires a child `pid` to equal its parent's `pid`. It uses ordinary page-wide sorting, so preserve source `sorting` during this rewrite and run Container's sorting check afterwards. Do not apply an automatic sorting repair until the check output has been reviewed and approved.

## FlexForms and rendering are separate migrations

Gridelements commonly stores layout-specific FlexForm values in `pi_flexform`. Container intentionally does not create a FlexForm for a CType. If a layout's template reads legacy FlexForm data, create an equivalent target data structure and test the values against real records before preserving `pi_flexform`. If the replacement has no equivalent field, do not silently retain unread data and call it parity. Map it to a supported field, preserve it temporarily with a documented adapter, or ask for a product decision.

Likewise, Gridelements may render columns with layout-specific TypoScript objects or `GridChildrenProcessor` output. Rebuild that output for the target CType. The data rewrite alone cannot preserve frontend markup.
