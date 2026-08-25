# Gridelements 8.7 compatibility

## Why this needs a staged route

Gridelements 8.7.0 ran with TYPO3 8.7. Current `b13/container` 4.1.0 declares support for TYPO3 13.4 and 14.3. Do not try to install current Container into the old runtime.

Instead, create a restorable copy of the legacy database and files, retain the Gridelements data while upgrading the copy to the chosen current runtime, register the replacement Container types there, and then convert the retained rows. Extra legacy columns can remain in the database during that transition. Do not let a schema cleanup remove them before the conversion is reconciled.

## Confirmed 8.7.0 record model

The 8.7.0 extension archive shows these `tt_content` fields:

| Purpose | Legacy field/value |
| --- | --- |
| Container record | `CType = gridelements_pi1` |
| Selected grid layout | `tx_gridelements_backend_layout` |
| Child's parent | `tx_gridelements_container` |
| Child's grid cell | `tx_gridelements_columns` |
| Child's page column | `colPos = -1` |
| Child order | `sorting` |

Gridelements reads a parent's children by `tx_gridelements_container` and orders them by the legacy column value, then `sorting`. Its Grid TS model stores each cell's `name`, `colPos`, optional `colspan`, `rowspan`, `allowed`, `disallowed`, and `maxitems`.

The migration command must read the actual column from `tx_gridelements_columns`, not from the child's `colPos`. Treat a linked child with a different `colPos`, a missing layout, an unknown legacy cell, a parent on a different `pid`, workspace rows, or a mixed language setup as a hard stop that needs a project-specific decision.

## Translation rule

Gridelements 8.7 can point translated children at translated parent records. Container's connected language mode intentionally points a translated child's `tx_container_parent` at the default-language parent, not the translated parent. For a child whose source parent has `l18n_parent > 0`, write that `l18n_parent` value as its new Container parent. Preserve the child's own `l18n_parent` unchanged.

Classify the target language setup before conversion. Container supports connected and free mode, but not mixed mode. Do not convert live and workspace versions together.

## Primary sources checked on 2026-08-25

- [Gridelements 8.7 Grid TS syntax](https://docs.typo3.org/p/gridelementsteam/gridelements/8.7/en-us/Chapters/GridTsSyntax/Index.html)
- [Gridelements 8.7 TSconfig reference](https://docs.typo3.org/p/gridelementsteam/gridelements/8.7/en-us/Chapters/Tsconfig/Index.html)
- [Gridelements 8.7.0 TER archive](https://extensions.typo3.org/extension/download/gridelements/8.7.0/zip), inspected for `ext_tables.sql`, TCA, and child retrieval code
- [Current Container package metadata](https://raw.githubusercontent.com/b13/container/master/composer.json)
- [Container migration model](https://github.com/b13/container/blob/master/README.md#migration-to-extcontainer)
