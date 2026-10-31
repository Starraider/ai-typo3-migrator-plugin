# Evidence ledger

Every conclusion has a class. Store tokens with `confidence` and list sources and gaps in the envelope's `evidence` array.

| Class | Meaning | Examples |
| --- | --- | --- |
| `observed` | Read directly from source or measured in a render | `--accent: #0b5fff` in `index.css:12`; computed `padding-top: 96px` at 1440px |
| `inferred` | A rule derived from observed values | a 4px spacing scale concluded from 8/12/16/24; a breakpoint guessed from one layout change |
| `unknown` | Cannot be determined from available evidence | font family from a screenshot; hover states; mobile layout |

## Rules

1. **Never promote** inferred to observed. If an inferred rule is later confirmed by a render, add a new observed entry and keep the old one.
2. **Declared vs rendered:** with a running reference, record both `value` (declared) and `renderedValue` (computed). Differences are evidence: note which wins visually and why (override, cascade, inline style).
3. **Approximations:** a color sampled from a screenshot is `observed` only as "sampled pixel"; mark the token `inferred` and note the sampling tolerance. Do not round into a design color.
4. **Unknown is an answer.** Record an `unknown` entry and an `unresolved` item with `readinessEffect` (`incomplete` for missing evidence, `blocked` if the requested work cannot proceed).
5. **Single-reference limits:** do not invent dark mode, a mobile layout, hover or focus states, or fonts from one reference.
6. **Provenance:** each entry has `id`, `class`, `kind` (source, render, screenshot, docs, installed-source), `locator`, and a one-line `note`.
7. **Discrepancy entries:** docs vs installed Astryx, declared vs rendered, and two sources disagreeing each get a `note` naming both values.

## Readiness mapping

| Situation | Readiness |
| --- | --- |
| Complete source + required checks passed | `ready` |
| Missing evidence (screenshot-only, no fonts, unrun render check) | `incomplete` |
| Unsupported target, FSC conflict, unanswered gate that stops requested work | `blocked` |

`ready` is invalid with any unresolved entry, unanswered decision or failed verification. Screenshot-only evidence never yields a complete or verified extraction.
