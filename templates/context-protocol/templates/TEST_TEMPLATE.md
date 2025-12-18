# {Module} — Test: Test Cases and Coverage

```
STATUS: {DRAFT | STABLE | DEPRECATED}
CREATED: {DATE}
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_{name}.md
BEHAVIORS:       ./BEHAVIORS_{name}.md
ALGORITHM:       ./ALGORITHM_{name}.md
VALIDATION:      ./VALIDATION_{name}.md
IMPLEMENTATION:  ./IMPLEMENTATION_{name}.md
THIS:            TEST_{name}.md
SYNC:            ./SYNC_{name}.md

IMPL:            {path/to/test/file.py}
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## TEST STRATEGY

{High-level approach to testing this module. What's the philosophy?}

---

## UNIT TESTS

### {Test Group}

| Test | Input | Expected | Status |
|------|-------|----------|--------|
| {test_name} | {input} | {expected output} | {pass/fail/pending} |

---

## INTEGRATION TESTS

### {Integration Scenario}

```
GIVEN:  {preconditions}
WHEN:   {action}
THEN:   {expected result}
STATUS: {pass/fail/pending}
```

---

## EDGE CASES

| Case | Test | Status |
|------|------|--------|
| {edge case description} | {how it's tested} | {status} |

---

## TEST COVERAGE

| Component | Coverage | Notes |
|-----------|----------|-------|
| {component} | {%} | {gaps or notes} |

---

## HOW TO RUN

```bash
# Run all tests for this module
{command}

# Run specific test
{command}
```

---

## KNOWN TEST GAPS

- [ ] {Untested scenario}
- [ ] {Missing edge case}

---

## FLAKY TESTS

| Test | Flakiness | Root Cause | Mitigation |
|------|-----------|------------|------------|
| {test} | {frequency} | {why} | {fix} |

---

## GAPS / IDEAS / QUESTIONS

- [ ] {Missing test}
- IDEA: {Testing improvement}
- QUESTION: {Testing uncertainty}
