# ADD Framework CLI — Test: Test Cases and Coverage

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

The CLI module currently lacks automated tests. Testing is performed manually through CLI usage and repair agent execution. This document tracks what should be tested and current coverage gaps.

**Testing philosophy:**
- Commands should be tested in isolation first
- Integration tests should verify end-to-end flows
- Agent tests require mocking claude subprocess

---

## UNIT TESTS

### Init Command

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| init_creates_protocol_dir | empty directory | .add-framework/ created | NOT TESTED |
| init_creates_claude_md | directory without CLAUDE.md | CLAUDE.md created | NOT TESTED |
| init_updates_claude_md | directory with existing CLAUDE.md | Protocol section appended | NOT TESTED |
| init_no_duplicate | CLAUDE.md already has protocol | No duplicate section | NOT TESTED |
| init_force_overwrites | --force flag | Existing .add-framework/ replaced | NOT TESTED |
| init_rejects_existing | no --force, existing protocol | Error message, exit 1 | NOT TESTED |

### Validate Command

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| validate_passes_healthy | complete protocol | All checks pass, exit 0 | NOT TESTED |
| validate_fails_missing_protocol | no .add-framework/ | V6 fails | NOT TESTED |
| validate_fails_missing_views | incomplete views/ | V7 fails | NOT TESTED |
| validate_fails_missing_patterns | module without PATTERNS | V2 fails | NOT TESTED |
| validate_detects_broken_chain | invalid CHAIN link | V3 fails | NOT TESTED |

### Doctor Command

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| doctor_detects_monolith | 600-line file | MONOLITH issue | NOT TESTED |
| doctor_detects_undocumented | unmapped code dir | UNDOCUMENTED issue | NOT TESTED |
| doctor_detects_stale_sync | 30-day-old SYNC | STALE_SYNC issue | NOT TESTED |
| doctor_score_100 | healthy project | score = 100 | NOT TESTED |
| doctor_score_decreases | critical issues | score < 100 | NOT TESTED |
| doctor_saves_report | default run | SYNC_Project_Health.md created | NOT TESTED |

### Repair Command

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| repair_spawns_agents | issues exist | Claude subprocess started | NOT TESTED |
| repair_respects_depth | depth=links | Only link fixes attempted | NOT TESTED |
| repair_respects_max | --max 3 | At most 3 issues fixed | NOT TESTED |
| repair_dry_run | --dry-run | No agents spawned | NOT TESTED |
| repair_parallel | --parallel 3 | 3 concurrent agents | NOT TESTED |

---

## INTEGRATION TESTS

### Full Init-Validate Cycle

```
GIVEN:  Empty project directory
WHEN:   add-framework init && add-framework validate
THEN:   All validation checks pass
STATUS: NOT TESTED
```

### Doctor-Repair Cycle

```
GIVEN:  Project with known issues
WHEN:   add-framework doctor && add-framework repair
THEN:   Health score improves
STATUS: NOT TESTED
```

### Context Navigation

```
GIVEN:  Source file with DOCS: reference
WHEN:   add-framework context <file>
THEN:   Documentation chain is displayed
STATUS: NOT TESTED
```

---

## EDGE CASES

| Case | Test | Status |
|------|------|--------|
| Empty project | init on empty dir | Manual testing only |
| Large codebase | doctor on 1000+ files | Manual testing only |
| No YAML dependency | doctor without pyyaml | Manual testing only |
| Agent timeout | repair with slow agent | NOT TESTED |
| Broken templates | init with missing templates | NOT TESTED |
| Unicode paths | files with special characters | NOT TESTED |

---

## TEST COVERAGE

| Component | Coverage | Notes |
|-----------|----------|-------|
| cli.py | 0% | No automated tests |
| init_cmd.py | 0% | No automated tests |
| validate.py | 0% | No automated tests |
| doctor.py | 0% | No automated tests |
| repair.py | 0% | No automated tests |
| sync.py | 0% | No automated tests |
| context.py | 0% | No automated tests |
| utils.py | 0% | No automated tests |

**Overall: 0% automated test coverage**

---

## HOW TO RUN

```bash
# Currently no automated tests exist
# Manual testing commands:

# Test init
add-framework init --dir /tmp/test-project
add-framework validate --dir /tmp/test-project

# Test doctor
add-framework doctor --no-github

# Test repair (dry run)
add-framework repair --dry-run --max 3

# Test context
add-framework context src/add_framework/cli.py
```

---

## KNOWN TEST GAPS

- [ ] No unit tests for any module
- [ ] No integration tests
- [ ] No property-based tests
- [ ] No CI/CD test pipeline
- [ ] No mocking infrastructure for claude subprocess
- [ ] No test fixtures for project structures

---

## PROPOSED TEST STRUCTURE

```
tests/
├── conftest.py           # Shared fixtures
├── fixtures/
│   ├── healthy_project/  # Project passing all checks
│   ├── broken_project/   # Project with various issues
│   └── templates/        # Test template files
├── unit/
│   ├── test_init.py
│   ├── test_validate.py
│   ├── test_doctor.py
│   ├── test_repair.py
│   └── test_utils.py
└── integration/
    ├── test_full_cycle.py
    └── test_context_flow.py
```

---

## FLAKY TESTS

| Test | Flakiness | Root Cause | Mitigation |
|------|-----------|------------|------------|
| (none yet) | — | — | — |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Set up pytest infrastructure
- [ ] Create test fixtures for common project states
- [ ] Add CI/CD with GitHub Actions
- [ ] Consider snapshot testing for CLI output
- IDEA: Use hypothesis for property-based testing
- IDEA: Mock claude subprocess for repair tests
- QUESTION: Should we test against real Claude or always mock?
