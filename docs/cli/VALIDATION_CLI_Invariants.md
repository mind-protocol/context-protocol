# ADD Framework CLI — Validation: Invariants and Correctness Checks

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
TEST:            ./TEST_CLI_Coverage.md
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

## TEST COVERAGE

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
ngram doctor --no-github
ngram context src/ngram/cli.py

# No automated test suite yet
# TODO: Add pytest tests
```

---

## VALIDATION CHECKS REFERENCE

The `validate` command runs these checks:

| Check ID | Name | What It Verifies |
|----------|------|------------------|
| V6 | Protocol installed | .ngram/ exists with core files |
| V7 | VIEWs exist | All 11 VIEW files present |
| V6 | Project SYNC exists | SYNC_Project_State.md exists and initialized |
| V2 | Module docs minimum | Every doc module has PATTERNS + SYNC |
| FC | Full chain | Doc modules have complete chain (7 types) |
| NC | Naming conventions | Files follow PATTERNS_/BEHAVIORS_/etc pattern |
| V3 | CHAIN links valid | All CHAIN references point to existing files |
| MM | Module manifest | modules.yaml has mappings for code directories |

---

## DOCTOR CHECKS REFERENCE

The `doctor` command runs these health checks:

| Check | Severity | Threshold |
|-------|----------|-----------|
| MONOLITH | critical | > 500 lines (1000 for .md) |
| UNDOCUMENTED | critical | Code dir not in modules.yaml |
| STALE_SYNC | warning | LAST_UPDATED > 14 days ago |
| PLACEHOLDER | critical | Template markers in non-template files |
| INCOMPLETE_CHAIN | warning | Missing doc types (< 7) |
| NO_DOCS_REF | info | Source file > 50 lines without DOCS: |
| BROKEN_IMPL_LINK | critical | IMPLEMENTATION doc refs non-existent files |
| STUB_IMPL | warning | >= 3 stub indicators (TODO, pass, etc.) |
| INCOMPLETE_IMPL | warning | >= 2 empty functions |
| UNDOC_IMPL | info | File not in IMPLEMENTATION doc |
| LARGE_DOC_MODULE | warning | > 50K chars total in module |
| YAML_DRIFT | critical | modules.yaml paths don't exist |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Add automated tests for all invariants
- [ ] Property-based testing for idempotency/monotonicity
- [ ] Integration tests for repair agent behavior
- IDEA: Add pre-commit hook to run validate
- QUESTION: Should validate fail on warnings or only critical issues?
