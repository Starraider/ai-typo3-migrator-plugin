# Ship the full v1 handoff contract tooling up front

The three TYPO3 migration skills exchange versioned JSON handoffs with canonical revision hashing, a validator helper, per-skill schema copies and drift checks, even though no real mockup or TYPO3 project exists yet to validate the schema. We chose this over a minimal `0.x` envelope so stale or malformed handoffs are detectable from the first consumer run, accepting that the schema is validated only by synthetic fixtures.
