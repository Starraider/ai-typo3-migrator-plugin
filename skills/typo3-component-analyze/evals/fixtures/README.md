# Evaluation fixtures

Synthetic, tiny inputs for [evals.json](../evals.json). They are not a real mockup.

- `mockup/src/`: React sources (`Card`, a second blog `Card`, `Nav`, `Carousel`, `Banner`, `CardGrid`, `FullWidthHero`) and `index.css`. `desktop-1440.png` is a placeholder screenshot used for screenshot-only runs.
- `bundles/fresh-session/`: a valid component bundle (`card` spec and `card-grid` parent spec). A design-system handoff is also present only to exercise the analysis boundary; the component specs do not depend on it. `validate` exits `0`.
- `bundles/missing-child/`: an `incomplete` parent spec whose child `card` spec is absent. `validate` exits `2` (`unknown-freshness`).

Validate from the skill root:

```bash
python3 scripts/validate_handoff.py validate evals/fixtures/bundles/fresh-session/components/card-grid/component-spec.json
```
