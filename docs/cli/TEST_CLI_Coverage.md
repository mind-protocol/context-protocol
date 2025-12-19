# ngram Framework CLI — Test: Test Cases and Coverage

```
STATUS: DRAFT
CREATED: 2025-12-18
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Why_CLI_Over_Copy.md
BEHAVIORS:       ./BEHAVIORS_CLI_Command_Effects.md
ALGORITHM:       ./ALGORITHM_CLI_Logic.md
VALIDATION:      ./VALIDATION_CLI_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_CLI_Code_Architecture.md
THIS:            TEST_CLI_Coverage.md (you are here)
SYNC:            ./SYNC_CLI_State.md
```

---

## TEST STRATEGY

The CLI currently has no automated tests. Validation is manual through CLI usage. Tests should cover each command in isolation, then a small set of end-to-end flows.

---

## COVERAGE SUMMARY

- Automated unit tests: none
- Automated integration tests: none
- Manual smoke tests: ad hoc during development and repairs

---

## PRIORITY TESTS (PLANNED)

- **Init:** protocol files created, force behavior, bootstrap file updates
- **Validate:** healthy project pass, missing protocol fail, broken chain detection
- **Doctor:** monolith detection, stale sync detection, score calculation
- **Repair:** agent spawning, depth filtering, max limit, dry-run, parallel behavior
- **Context:** docs chain resolution from `DOCS:` references

---

## INTEGRATION FLOWS (PLANNED)

- `init` → `validate`
- `doctor` → `repair` (health score improves)
- `context` → doc chain output for known file

---

## MANUAL SMOKE

```bash
ngram init --dir /tmp/test-project
ngram validate --dir /tmp/test-project
ngram doctor
ngram repair --dry-run --max 3
ngram context ngram/cli.py
```

---

## KNOWN GAPS

- No automated tests or fixtures
- No CI pipeline
- No mocking for agent subprocess
