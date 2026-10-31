# Handoff contract v1

Authoring source: `docs/contracts/handoff-v1/` in the plugin repository. Each skill ships an identical copy of this file, the [schemas](schemas/envelope.schema.json), the example artifacts in `templates/`, and `scripts/validate_handoff.py`. Do not edit a skill's copy; edit the authoring source and run `python3 tools/sync_contracts.py`.

The three skills exchange **handoffs**: a JSON artifact (machine-checked) plus a Markdown report with the same facts (human-read). The JSON is authoritative; the Markdown never adds facts.

## Migration bundle layout

Resolve the bundle path before writing, report it, and reuse a supplied bundle. Proposed default: `design-migration/<design-id>/` in the consumer project, unless its conventions say otherwise.

| Artifact | Owner | Files |
| --- | --- | --- |
| design-system | extract | `design-system.json`, `design-system.md` |
| component-spec | analyze | `components/<id>/component-spec.json`, `component-spec.md` |
| build-report | build | `components/<id>/build-report.json`, `build-report.md` |
| references | any | `references/`, `components/<id>/references/` |

## Envelope

Every JSON artifact has these top-level fields ([schema](schemas/envelope.schema.json)):

| Field | Meaning |
| --- | --- |
| `schemaVersion` | `1.0.0`. Reject any other major version; never relabel an old handoff as current. |
| `artifactType` | `design-system`, `component-spec` or `build-report`. |
| `artifactId` | Lowercase id (`^[a-z0-9][a-z0-9._-]*$`). |
| `revision` | Canonical hash, see below. |
| `payloadDigest` | Hash of the binding payload; used to detect an edited payload that was not resealed. |
| `readiness` | `ready`, `incomplete` or `blocked`. |
| `sources` | `kind`, `locator`, `identityStatus` (`known` needs `digest` or `revision`; `unavailable` is explicit), optional `selector`. |
| `dependencies` | `artifactType`, `artifactId`, `schemaVersion`, `revision`, `ref` (relative path). |
| `target` | `versionsKnown` plus exact installed `typo3`, `php`, `astryx`, `styleXConnector` when known, and `conflicts`. |
| `evidence` | `id`, `class` (`observed`, `inferred`, `unknown`), `kind`, optional `locator`, `note`. |
| `verification` | `id`, `status` (`passed`, `failed`, `not-run`, `not-applicable`), non-empty `reason`, optional `command`. |
| `decisions` | Decision-gate records, see below. |
| `unresolved` | `id`, `description`, `readinessEffect` (`blocked` or `incomplete`). |
| `payload` | Type-specific content: [design-system](schemas/design-system.payload.schema.json), [component-spec](schemas/component-spec.payload.schema.json), [build-report](schemas/build-report.payload.schema.json). |

Readiness and verification are separate. Readiness answers "may a consumer rely on this?"; verification entries say what was checked. There is no single success flag.

### Component visual design

The component-spec payload may include `design` for backward-compatible v1 handoffs. Current `typo3-component-analyze` outputs include it with an overview, frame, composition, surface, typography, spacing, important part appearances, and visual states. Each description carries its evidence class (`source`, `rendered`, `user`, `inferred`, or `unknown`). This is a component-level design description. It does not map to, compare with, or depend on global design-system tokens; `typo3-component-build` performs that assessment during implementation. The design object is part of the binding payload and therefore affects the revision and payload digest.

The build-report payload may include `designCoverage`, an implementation-time comparison of each component design requirement with the selected Content Block/content element's active inheritance chain and the current global design-system handoff. Current rows identify the target, inheritance status/source/effective value, matching global token IDs, overall coverage (`inherited`, `global-token`, `partial`, `component-specific`, or `unknown`), and exact component-specific token IDs/values/statuses. This field is optional for older v1 reports; current build outputs include it when a component `design` section is available.

### Canonical revision

`revision` is `sha256:` plus the SHA-256 of the canonical JSON (sorted keys, no whitespace, UTF-8) of:

- `schemaVersion`, `artifactType`, `artifactId`;
- `payload` **without** `targetHypothesis`;
- `sources` (kind, locator, selector, identityStatus, digest, revision), sorted;
- `dependencies` (artifactType, artifactId, schemaVersion, revision), sorted;
- answered `binding` decisions (id, appliesTo, answer, effect, bindingDigest), sorted by id.

It excludes `revision`, `payloadDigest`, `generatedAt`, `evidence`, `verification`, `unresolved`, `readiness`, run-only decisions and the target hypothesis. `payloadDigest` is the same hash over the payload without `targetHypothesis` only.

Consequences: a changed source digest, token mapping, required asset or dependency revision changes the revision; changing only the target hypothesis, timestamps, verification results or a run-only decision does not.

Use `python3 scripts/validate_handoff.py seal <file>` after every edit to write both hashes.

### Dependencies and freshness

A dependency records the revision the artifact was produced against. A consumer recomputes the referenced file's revision:

- equal: fresh;
- different: `stale-dependency`, reassess affected claims before reuse;
- file absent or source identity `unavailable`: `unknown-freshness`, which cannot establish freshness.

### Reference rules

Every `ref` (dependencies, `children[].ref`, `specRef`, captures) is a relative POSIX path resolved from the referencing file. It must not be absolute, contain a URL scheme or backslash, or leave the bundle root (including through symlinks).

## Decision gates

A decision gate is a point where a skill stops and asks. Record every gate in `decisions`:

| Field | Rule |
| --- | --- |
| `id`, `question`, `options` | Always present. |
| `status` | `answered` or `unanswered`. An unanswered gate also appears in `unresolved` (same `id`) and prevents `ready`. |
| `answer`, `answerWording`, `date` | Required when answered. `answer` is one of `options`; `answerWording` is the user's own words; `date` is `YYYY-MM-DD`. |
| `appliesTo` | The `artifactId` the decision concerns (this artifact or a dependency). |
| `effect` | `binding` (changes binding requirements or accepts a deviation; enters the revision) or `run-only` (does not). |
| `bindingDigest` | Binding decisions: the `payloadDigest` of `appliesTo` when answered. |

Reuse an answered decision in a later session instead of asking again. If the current `payloadDigest` of `appliesTo` differs from `bindingDigest`, the decision is stale (`decision-stale`): mark it, and ask again before relying on it.

## Readiness rules checked by the validator

- `ready` is invalid with any `unresolved` entry, unanswered decision or `failed` verification.
- A `blocked` unresolved entry requires readiness `blocked`.
- design-system `foundation.status: verified` and build-report `completion: verified` are invalid while any verification is `failed` or `not-run`; build-report `verified` also needs a passed **hard** check (computed style or layout), no open difference, and every hard check passed. Screenshots are advisory.
- Every accepted deviation and accepted difference references an answered binding decision.
- A `parent-with-children` component spec lists each child in `dependencies`; a missing or stale child makes the parent `incomplete`, not `ready`.
- An embedded native component is never `placeable`.
- A build report records no target edits when `preflight.fscConflict` is true.

## Validator

`scripts/validate_handoff.py` needs Python 3.8+ and nothing else; no provider connection, network or TYPO3 installation.

```bash
python3 scripts/validate_handoff.py validate --json design-migration/site/components/card/component-spec.json
python3 scripts/validate_handoff.py revision <file>
python3 scripts/validate_handoff.py seal <file>
```

`validate` exit codes: `0` valid and fresh, `1` invalid, `2` valid but stale or of unknown freshness, `64` usage or I/O error. Finding codes: `missing-field`, `bad-type`, `bad-enum`, `bad-value`, `unsupported-schema-major`, `payload-digest-mismatch`, `revision-mismatch`, `stale-dependency`, `unknown-freshness`, `invalid-reference`, `escaping-reference`, `unresolved-reference`, `child-dependency-missing`, `decision-invalid`, `decision-stale`, `readiness-inconsistent`, `unqualified-verified`, `unreadable`.

## Examples

`templates/` contains sealed example artifacts: `design-system.example.json`, `component-spec.example.json`, `component-spec-parent.example.json` (a section with a child reference) and `build-report.example.json`. Copy one, replace the values, and run `seal`, then `validate`. They form one valid bundle when placed at the layout above.

