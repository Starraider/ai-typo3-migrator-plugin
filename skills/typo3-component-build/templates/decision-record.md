# Decision Record Template

Use this format to record decision gate resolutions in the build report:

```json
{
  "id": "decision-identifier",
  "question": "Exact question asked to the user?",
  "options": ["option_a", "option_b"],
  "status": "answered",
  "answer": "option_a",
  "answerWording": "User's exact natural language response",
  "date": "YYYY-MM-DD",
  "appliesTo": "target-artifact-id",
  "effect": "binding",
  "bindingDigest": "sha256:..."
}
```

- **effect: "binding":** Changes binding requirements or accepts a visual/recipe deviation. Alters the artifact revision and requires `bindingDigest`.
- **effect: "run-only":** Operational choice (e.g. logging preference or rerun choice). Does not affect revision hash.

