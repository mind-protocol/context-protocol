# ngram Framework CLI — Validation: Invariants and Correctness Checks

```
STATUS: STABLE
CREATED: 2025-12-18
VERIFIED: 2025-12-18 against commit 6e0062c
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Why_CLI_Over_Copy.md
BEHAVIORS:       ./BEHAVIORS_CLI_Command_Effects.md
ALGORITHM:       ./ALGORITHM_CLI_Logic.md
THIS:            VALIDATION_CLI_Invariants.md (you are here)
IMPLEMENTATION:  ./IMPLEMENTATION_CLI_Code_Architecture.md
HEALTH:          ./HEALTH_CLI_Coverage.md
SYNC:            ./SYNC_CLI_State.md
```

---

## INVARIANTS

These must ALWAYS be true:

### V1: Protocol Files Integrity

```
After successful init:
  .ngram/PROTOCOL.md exists
  .ngram/PRINCIPLES.md exists
  .ngram/CLAUDE.md exists
  AGENTS.md exists at repo root
  AGENTS.md includes Codex communication principles
  .ngram/views/ contains all 11 VIEW files
  .ngram/templates/ contains all template files
```

**Checked by:** `validate` command (check_protocol_installed, check_views_exist)

### V2: Module Doc Minimum

```
For every directory in docs/ containing doc files:
  At least PATTERNS_*.md exists
  At least SYNC_*.md exists
```

**Checked by:** `validate` command (check_module_docs_minimum)

### V3: CHAIN Link Validity

```
For every CHAIN section in doc files:
  All referenced files exist at specified paths
  Paths are relative to the doc file location
```

**Checked by:** `validate` command (check_chain_links)

### V4: Health Score Bounds

```
Health score is always in range [0, 100]
score = max(0, 100 - penalties)
```

**Checked by:** `doctor` command (calculate_health_score)

### V5: Repair Agent Isolation

```
Each repair agent:
  Works on exactly ONE issue
  Follows exactly ONE VIEW
  Updates relevant SYNC when done
  Does not modify unrelated files
```

### V6: Escalation Scan Respects Ignores

```
- `solve-markers`: finds markers, sorts correctly, exits 0
```

**Checked by:** Agent prompt structure, manual review

---

## PROPERTIES

For property-based testing:

### P1: Validate Idempotency

```
FORALL projects P:
    result1 = validate(P)
    result2 = validate(P)
    result1 == result2  # Same result without changes
```

**Tested by:** NOT YET TESTED — need property test framework

### P2: Doctor Monotonicity

```
FORALL projects P, fix F:
    IF fix(P, issue) succeeds
    THEN score(P_after) >= score(P_before)
```

**Tested by:** NOT YET TESTED — need to verify fixes improve score

### P3: Init Completeness

```
FORALL target directories D:
    IF init(D) succeeds
    THEN validate(D).protocol_installed == True
    AND  validate(D).views_exist == True
```

**Tested by:** Manual testing during development

---

## ERROR CONDITIONS

### E1: Templates Not Found

```
WHEN:    get_templates_path() can't find templates
THEN:    FileNotFoundError raised with paths checked
SYMPTOM: "Templates directory not found" message
```

**Tested by:** NOT YET TESTED — requires removing templates

### E2: Agent Timeout

```
WHEN:    repair agent runs > 10 minutes
THEN:    process.kill() called
SYMPTOM: RepairResult with error="Agent timed out after 10 minutes"
```

**Tested by:** NOT YET TESTED — requires slow agent

### E3: Invalid YAML

```
WHEN:    modules.yaml has syntax errors
THEN:    yaml.safe_load returns None or raises
SYMPTOM: Module manifest checks skipped/failed gracefully
```

**Tested by:** Manual testing with malformed YAML

---

## HEALTH COVERAGE

| Requirement | Test(s) | Status |
|-------------|---------|--------|
| V1: Protocol files | — | Not automated |
| V2: Module doc min | — | Not automated |
| V3: CHAIN links | — | Not automated |
| V4: Score bounds | — | Not automated |
| V5: Agent isolation | — | Manual only |
| P1: Idempotency | — | NOT YET TESTED |
| P2: Monotonicity | — | NOT YET TESTED |
| E1: Templates | — | NOT YET TESTED |
| E2: Timeout | — | NOT YET TESTED |

---

## VERIFICATION PROCEDURE

### Manual Checklist

```
[ ] V1 holds — run init, check all files exist
[ ] V2 holds — create docs/test/, verify validate catches missing PATTERNS
[ ] V3 holds — add broken CHAIN link, verify validate catches it
[ ] V4 holds — check score output is 0-100
[ ] V5 holds — run repair, verify agent only touches relevant files
[ ] All behaviors from BEHAVIORS_*.md work
[ ] All edge cases handled
```

### Automated

```bash
# Run CLI commands manually for now
ngram init --force
ngram validate
ngram doctor
ngram context ngram/cli.py

# No automated test suite yet
# TODO: Add pytest tests
```

---

## CHECK REFERENCES

For detailed check definitions, see `ALGORITHM_CLI_Logic.md`:
- **Validate checks:** V6, V7, V2, FC, NC, V3, MM (8 total)
- **Doctor checks:** MONOLITH, UNDOCUMENTED, STALE_SYNC, PLACEHOLDER, INCOMPLETE_CHAIN, NO_DOCS_REF, BROKEN_IMPL_LINK, STUB_IMPL, INCOMPLETE_IMPL, UNDOC_IMPL, LARGE_DOC_MODULE, YAML_DRIFT, LOG_ERROR (13 total)

---

## GAPS / IDEAS / QUESTIONS

- [ ] Add automated tests for all invariants
- [ ] Property-based testing for idempotency/monotonicity
- [ ] Integration tests for repair agent behavior
- IDEA: Add pre-commit hook to run validate
- QUESTION: Should validate fail on warnings or only critical issues?
