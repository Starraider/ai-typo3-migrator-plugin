# Execution runbook

## Read-only inventory

Adapt table quoting and CLI prefixes to the project. Run these only on the copied database.

```sql
SELECT tx_gridelements_backend_layout AS layout_key, COUNT(*) AS parent_count
FROM tt_content
WHERE deleted = 0
  AND CType = 'gridelements_pi1'
GROUP BY tx_gridelements_backend_layout
ORDER BY tx_gridelements_backend_layout;

SELECT parent.uid AS parent_uid, parent.pid AS parent_pid,
       parent.tx_gridelements_backend_layout AS layout_key,
       child.uid AS child_uid, child.pid AS child_pid,
       child.colPos, child.tx_gridelements_columns, child.sorting,
       child.sys_language_uid, child.l18n_parent
FROM tt_content AS child
JOIN tt_content AS parent ON parent.uid = child.tx_gridelements_container
WHERE child.deleted = 0
  AND child.tx_gridelements_container > 0
ORDER BY parent.pid, parent.uid, child.tx_gridelements_columns, child.sorting, child.uid;

SELECT uid, pid, CType, tx_gridelements_container, tx_gridelements_columns, colPos
FROM tt_content
WHERE deleted = 0
  AND tx_gridelements_container > 0
  AND colPos <> -1;
```

Before writes, record counts by layout, container parent, old cell, `CType`, language, and page. Capture backend screenshots and frontend HTML or approved screenshots for one instance of every used layout, including nested and translated instances.

## Approval gate before apply

State the following in the approval request:

- database and file-storage backup locations, plus a tested restore command or procedure;
- target branch and copied environment;
- exact source-layout to target-CType and old-cell to new-`colPos` mappings;
- dry-run totals and all zero-count exception queries;
- the command and its explicit write flags;
- rollback method, normally restoring the captured database backup.

The supplied command template refuses writes without both `--apply` and `--i-understand-this-rewrites-tt-content`. Those flags are not a substitute for user approval.

## Reconciliation after apply

Run the command in dry-run/report mode again. It should find no eligible legacy parent or child rows. Then run:

```sql
SELECT COUNT(*) AS remaining_legacy_parents
FROM tt_content
WHERE deleted = 0 AND CType = 'gridelements_pi1';

SELECT COUNT(*) AS remaining_legacy_children
FROM tt_content
WHERE deleted = 0
  AND (tx_gridelements_container <> 0 OR tx_gridelements_columns <> 0);

SELECT child.uid, child.pid, child.tx_container_parent, parent.pid AS parent_pid,
       child.colPos, child.sorting
FROM tt_content AS child
LEFT JOIN tt_content AS parent ON parent.uid = child.tx_container_parent
WHERE child.deleted = 0
  AND child.tx_container_parent > 0
  AND (parent.uid IS NULL OR child.pid <> parent.pid);
```

Run `vendor/bin/typo3 container:sorting` and `vendor/bin/typo3 container:sorting-in-page` if these commands are available in the installed Container release. Review their output. Get separate approval before a command that changes sorting. Rebuild caches and update the reference index with the project-standard commands, then test:

- every approved legacy page and viewport against its baseline;
- child count, target column, and relative order for every converted parent;
- nested containers, translated and free-mode records as applicable;
- backend creation, move, copy, localize, hide, and drag-and-drop behavior;
- links, FAL/media, shortcuts, and any template logic that uses FlexForm values.

Report every result as pass, fail, blocked, or not run. A failed relation check or a meaningful frontend difference means restore the database copy or resolve it before removing legacy support.

## Retirement after acceptance

Wait until the agreed acceptance period ends. Then, with approval, remove legacy rendering TypoScript, Page TSconfig, layout records if no longer required, dependencies that require Gridelements, and the Composer package. Use TYPO3's schema tools to remove the legacy columns only after the final reconciliation has found no live relation values. Keep the pre-conversion backup according to the project's retention policy.
